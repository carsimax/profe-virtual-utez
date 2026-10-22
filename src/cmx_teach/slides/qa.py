"""QA + PDF of an HTML deck. Usage: slides-qa index.html [--pdf] [--out qa] [--minutes N]
Set CHROMIUM_PATH to use a preinstalled Chromium."""
import os
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# Layouts whose content is meant to float in space: no bottom-whitespace warning
SPARSE_LAYOUTS = {"l-cover", "l-section", "l-statement", "l-quote"}
PLACEHOLDERS = re.compile(r"[Ll]orem ipsum|\bTODO\b|TÍTULO DEL DECK|Título que promete|Evento · Fecha")
LADDER = [(40, "ajusta el espaciado (tokens --sp-*)"), (90, "compacta huecos y paddings"),
          (160, "ajusta el texto o divide la slide"), (None, "cambia de layout o recorta contenido")]

WAIT_MERMAID = "() => !document.querySelector('pre.mermaid') || document.documentElement.dataset.mermaid"

SLIDE_CHECK = r"""
i => {
  const s = window.deck.slides[i], R = s.getBoundingClientRect(), bad = [], soft = [];
  const tag = el => el.tagName.toLowerCase() + (typeof el.className === 'string' && el.className.trim() ? '.' + el.className.trim().split(/\s+/).join('.') : '');
  const hasText = el => [...el.childNodes].some(t => t.nodeType === 3 && t.textContent.trim());
  for (const el of s.querySelectorAll('*')) {
    if (el.closest('.notes,defs')) continue;
    const b = el.getBoundingClientRect();
    if (!b.width || !b.height) continue;
    if (b.bottom > R.bottom + 1 || b.right > R.right + 1 || b.left < R.left - 1 || b.top < R.top - 1)
      bad.push(`se sale del lienzo: ${tag(el)}`);
    else if (hasText(el)) {
      const rg = document.createRange(); rg.selectNodeContents(el);
      if (rg.getBoundingClientRect().bottom > R.bottom - 40) bad.push(`texto en la franja del HUD (últimos 40 px): ${tag(el)}`);
    }
    const cs = getComputedStyle(el);
    if (/(hidden|clip)/.test(cs.overflow) && el !== s && el.scrollHeight > el.clientHeight + 2) bad.push(`texto recortado: ${tag(el)}`);
    if (el instanceof SVGElement) { if (el.tagName === 'text' && b.height < 14) soft.push(`texto SVG muy pequeño (${Math.round(b.height)} px): “${el.textContent.trim().slice(0, 20)}”`); }
    else if (hasText(el) && parseFloat(cs.fontSize) < 24) bad.push(`fuente < 24px: ${tag(el)} (${cs.fontSize})`);
  }
  const over = s.scrollHeight - s.clientHeight;
  if (over > 2) bad.push(`slide desbordada ${over}px`);
  let bottom = 0;  // lowest edge of real content (text ranges, media), in slide-relative px
  for (const el of s.querySelectorAll('*')) {
    if (el.closest('.notes,defs') || (el.parentElement && el.parentElement.closest('svg'))) continue;
    const leaf = hasText(el) || /^(img|svg|canvas|video)$/i.test(el.tagName);
    if (!leaf) continue;
    let b = el.getBoundingClientRect();
    if (hasText(el)) { const rg = document.createRange(); rg.selectNodeContents(el); b = rg.getBoundingClientRect(); }
    if (b.width && b.height) bottom = Math.max(bottom, b.bottom - R.top);
  }
  const text = [...s.querySelectorAll('*')].filter(e => !e.closest('.notes,defs,pre,code') && hasText(e)).map(e => e.textContent).join(' ');
  const layout = [...s.classList].find(c => c.startsWith('l-')) || '';
  if (s.querySelectorAll('.reveal').length > 6) soft.push('más de 6 .reveal');
  if (!s.querySelector('.notes')) soft.push('sin notas');
  if (!s.querySelector('.kicker') && !/l-(cover|section|quote|image)/.test(layout)) soft.push('sin kicker');
  return { bad: [...new Set(bad)].slice(0, 8), soft: [...new Set(soft)].slice(0, 6), layout, min: parseFloat(s.dataset.minutes) || 0, over, bottom: bottom / R.height, text };
}
"""


def _uniq(xs):
    return list(dict.fromkeys(xs))


def _num(x):
    # JS prints 5 for 5.0; keep that for the minutes summary
    return int(x) if float(x).is_integer() else x


def ladder_hint(px):
    return next(h for lim, h in LADDER if lim is None or px <= lim)


def diversity_min(n):
    # 7-9 slides need >= 6 distinct layouts, 10+ need >= 8 (research: guizang/html-ppt)
    return 8 if n >= 10 else 6 if n >= 7 else 0


def wait_mermaid(p):
    try:
        p.wait_for_function(WAIT_MERMAID, timeout=20000)
    except Exception:
        pass
    return p.evaluate("document.documentElement.dataset.mermaid || ''")


def main():
    args = sys.argv[1:]
    out_idx = args.index("--out") if "--out" in args else -1
    out = args[out_idx + 1] if out_idx > -1 else "qa"
    min_idx = args.index("--minutes") if "--minutes" in args else -1
    target = None
    if min_idx > -1:
        try:
            target = float(args[min_idx + 1])
        except (IndexError, ValueError):
            print("Uso: --minutes N (número de minutos)", file=sys.stderr)
            sys.exit(2)
    value_idx = {out_idx + 1, min_idx + 1} - {0}
    file = next((a for i, a in enumerate(args) if not a.startswith("--") and i not in value_idx), None)
    if not file:
        print("Uso: slides-qa index.html [--pdf] [--out qa] [--minutes N]", file=sys.stderr)
        sys.exit(2)
    if out_idx == -1:
        out = str(Path(file).parent / "qa")  # default next to the deck, not the cwd (commands run from repo root)
    Path(out).mkdir(parents=True, exist_ok=True)
    url = Path(file).resolve().as_uri()
    problems, warnings, notes, layouts = [], [], [], []
    minutes = 0

    with sync_playwright() as pw:
        launch = {"executable_path": os.environ["CHROMIUM_PATH"]} if os.environ.get("CHROMIUM_PATH") else {}
        browser = pw.chromium.launch(**launch)

        # 1) Desktop 1920x1080: screenshots, overflows, minimum sizes
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.on("pageerror", lambda e: problems.append(f"[js] {e}"))

        def on_console(m):
            if m.type != "error":
                return
            (warnings if re.search("Failed to load resource", m.text) else problems).append(f"[console] {m.text}")

        page.on("console", on_console)
        page.goto(url, wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.add_style_tag(content=".hint{display:none!important}")
        if wait_mermaid(page) == "error":
            problems.append("Mermaid no se pudo renderizar (sin red: se carga desde el CDN); ejecuta slides-mermaid con red para incrustar los diagramas.")
        if not page.evaluate("[...document.fonts].some(f => f.status === 'loaded')"):
            warnings.append("Las fuentes web no cargaron (sin red): capturas y medidas usan fuentes de respaldo; revisa con red si es posible.")
        n = page.evaluate("window.deck.count")
        for i in range(n):
            page.evaluate("i => window.deck.go(i)", i)
            page.wait_for_timeout(1100)
            page.screenshot(path=f"{out}/slide-{i + 1:02d}.png")
            r = page.evaluate(SLIDE_CHECK, i)
            problems += [f"slide {i + 1}: {x}" + (f" → {ladder_hint(r['over'])}" if x.startswith("slide desbordada") else "") for x in r["bad"]]
            if m := PLACEHOLDERS.search(r["text"]):
                problems.append(f"slide {i + 1}: texto de plantilla sin reemplazar: “{m.group(0)}”")
            if r["layout"] and r["layout"] not in SPARSE_LAYOUTS and r["bottom"] < 0.6:
                notes.append(f"slide {i + 1}: espacio vacío inferior: el contenido termina al {round(r['bottom'] * 100)} % de la altura ({r['layout']})")
            notes += [f"slide {i + 1}: {x}" for x in r["soft"]]
            layouts.append(r["layout"])
            minutes += r["min"]
        if m := PLACEHOLDERS.search(page.title()):
            problems.append(f"<title> de plantilla sin reemplazar: “{m.group(0)}”")
        for i in range(1, len(layouts)):
            if layouts[i] and layouts[i] == layouts[i - 1]:
                notes.append(f"slides {i}–{i + 1}: mismo layout dos veces seguidas ({layouts[i]})")
        need = diversity_min(n)
        if len(set(layouts)) < need:
            notes.append(f"diversidad de layouts: {len(set(layouts))} distintos en {n} slides (mínimo {need})")
        if target and minutes > 0.9 * target:
            notes.append(f"minutos planeados {_num(minutes)} > 90 % de {_num(target)} (límite {_num(round(0.9 * target, 1))})")
        for i in range(2, len(layouts)):
            if layouts[i] and layouts[i] == layouts[i - 1] == layouts[i - 2]:
                notes.append(f"slides {i - 1}–{i + 1}: mismo layout tres veces seguidas ({layouts[i]})")

        # 2) Mobile (reader mode): no horizontal scroll
        m = browser.new_page(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
        m.on("pageerror", lambda e: problems.append(f"[js móvil] {e}"))
        m.goto(url, wait_until="networkidle")
        m.evaluate("document.fonts.ready")
        wait_mermaid(m)
        mob = m.evaluate("({ reader: document.documentElement.classList.contains('reader'), sw: document.documentElement.scrollWidth, w: innerWidth })")
        if not mob["reader"]:
            problems.append("móvil: no activó el modo lector")
        if mob["sw"] > mob["w"] + 1:
            problems.append(f"móvil: scroll horizontal ({mob['sw']}px > {mob['w']}px)")
        m.screenshot(path=f"{out}/mobile.png", full_page=True)

        # 3) Vector PDF (one 1920x1080 page per slide)
        if "--pdf" in args:
            page.emulate_media(media="print")
            page.pdf(path=f"{out}/deck.pdf", prefer_css_page_size=True, print_background=True)
            print(f"PDF: {out}/deck.pdf")
        browser.close()

    print(f"{n} slides · {_num(minutes)} min planeados · {len(set(layouts))} layouts distintos · capturas en {out}/")
    if warnings:
        print("AVISOS DE ENTORNO:\n- " + "\n- ".join(_uniq(warnings)))
    if notes:
        print("REVISAR (no bloquea):\n- " + "\n- ".join(notes))
    if problems:
        print("PROBLEMAS (corrige y vuelve a correr):\n- " + "\n- ".join(problems))
        sys.exit(1)
    print("OK: sin desbordes, sin errores de JS, móvil sin scroll horizontal.")


if __name__ == "__main__":
    main()
