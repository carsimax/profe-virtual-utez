"""Validate hand-written SVG: static XML checks + geometry checks in Chromium.

Usage: svg-check FILE [--bg COLOR] [--min-font 14] [--width 1600] [--render OUT.png] [--scale 2] [--json]
FILE is a .svg (rendered at --width px, as if it filled a slide) or an .html deck
(every inline <svg> inside a .fig is measured in place at 1920x1080).
Exit codes: 0 ok (warnings allowed), 1 errors found, 2 unreadable / invalid XML.
Set CHROMIUM_PATH to use a preinstalled Chromium.

Geometry heuristics (kept simple on purpose):
- text-text overlap: screen bboxes intersect by > 2 px horizontally and > 25 % of the shorter height vertically
  (text bboxes include ascent/descent padding, so tight stacked lines are tolerated).
- containing box of a text: the smallest rect/circle/ellipse whose bbox contains the text's anchor point
  (left/centre/right edge by text-anchor, vertical middle); full-canvas shapes (> 85 % of the viewBox) are ignored.
- text-overflow: the text bbox sticks out of that box by more than 1 px.
"""
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
SHAPES = {"rect", "circle", "ellipse", "path", "line", "polyline", "polygon", "text", "use", "image"}
REF_RE = re.compile(r"url\(\s*['\"]?#([^)'\" ]+)")
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(")
MAX_BYTES, MAX_PATH_CMDS, MAX_DECIMALS = 30 * 1024, 200, 3

# Preset `utez` variables and deck class rules (copied from the html-slides template) so class-based SVGs render as in a deck.
PAGE_CSS = """
:root{--bg:#f7f8f6;--surface:#eef1ee;--surface-2:#e2e8e4;--line:#d0d8d3;--line-strong:#68716d;--text:#0d1d33;--text-dim:#47505a;
--accent:#00735b;--accent-2:#2563a8;--accent-3:#a3470f;--accent-4:#6a3fa0;--tone:var(--accent);
--font-display:"Saira","Arial Narrow",sans-serif;--font-body:"Source Sans 3",system-ui,sans-serif;--font-mono:"JetBrains Mono",ui-monospace,monospace}
.d-box{fill:var(--surface-2);stroke:var(--line-strong);stroke-width:2}.d-box.tone{stroke:var(--tone);stroke-width:3}.d-box.fill{fill:var(--tone);stroke:none}
.d-zone{fill:none;stroke:var(--line-strong);stroke-width:1.5;stroke-dasharray:6 6}
.d-text{fill:var(--text);font:500 24px var(--font-body)}.d-text.on-fill{fill:var(--bg);font-weight:700}
.d-label{fill:var(--text-dim);font:600 15px var(--font-mono);letter-spacing:.12em;text-transform:uppercase}
.d-big{fill:var(--tone);font:700 64px var(--font-display)}
.d-line{fill:none;stroke:var(--line-strong);stroke-width:2.5}.d-line.dash{stroke-dasharray:8 7}.d-line.hot{stroke:var(--tone);stroke-width:4}
.d-arrow{fill:context-stroke}.d-dot{fill:var(--tone)}
.d-ico{fill:none;stroke:var(--text);stroke-width:1.75;stroke-linecap:round;stroke-linejoin:round}.d-ico.tone{stroke:var(--tone)}
.ill-tone{fill:var(--tone)}.ill-2{fill:var(--accent-2)}.ill-soft{fill:var(--surface-2)}.ill-surface{fill:var(--surface)}
.ill-line{fill:none;stroke:var(--line-strong);stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}.ill-ink{fill:var(--text)}.ill-bg{fill:var(--bg)}
"""

GEOMETRY_JS = r"""
(svg, o) => {
  const out = [], tol = 1.5;
  const issue = (level, rule, el, msg) => out.push({ level, rule, element: el ? describe(el) : 'svg', message: msg });
  function describe(el) {
    let s = el.tagName + (el.id ? '#' + el.id : (el.classList && el.classList.length ? '.' + el.classList[0] : ''));
    if (el.tagName === 'text') s += ' "' + el.textContent.trim().slice(0, 24) + '"';
    return s;
  }
  const rect = el => { const b = el.getBoundingClientRect(); return { l: b.left, t: b.top, r: b.right, b: b.bottom, w: b.width, h: b.height }; };
  const hasVB = svg.hasAttribute('viewBox') && svg.viewBox.baseVal.width > 0;
  const ctm = svg.getScreenCTM(), scale = Math.hypot(ctm.a, ctm.b) || 1;
  let root;
  if (hasVB) {
    const v = svg.viewBox.baseVal, p = (x, y) => { const pt = svg.createSVGPoint(); pt.x = x; pt.y = y; return pt.matrixTransform(ctm); };
    const a = p(v.x, v.y), b = p(v.x + v.width, v.y + v.height);
    root = { l: a.x, t: a.y, r: b.x, b: b.y };
  } else { const r = rect(svg); root = { l: r.l, t: r.t, r: r.r, b: r.b }; }
  const rootArea = (root.r - root.l) * (root.b - root.t);
  const all = [...svg.querySelectorAll('*')].filter(e => !e.closest('defs,symbol,marker,clipPath,mask,pattern,title,desc,metadata,style'));
  const shapes = all.filter(e => SHAPESET.has(e.tagName));
  // colours
  const parse = s => { const m = /rgba?\(([^)]+)\)/.exec(s || ''); if (!m) return null; const v = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: v[0], g: v[1], b: v[2], a: v.length > 3 ? v[3] : 1 }; };
  const blend = (c, bg) => ({ r: c.r * c.a + bg.r * (1 - c.a), g: c.g * c.a + bg.g * (1 - c.a), b: c.b * c.a + bg.b * (1 - c.a), a: 1 });
  const lum = c => { const f = v => { v /= 255; return v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); }; return .2126 * f(c.r) + .7152 * f(c.g) + .0722 * f(c.b); };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  let bg = null;
  if (o.bg) { const d = document.createElement('div'); d.style.color = o.bg; document.body.appendChild(d); bg = parse(getComputedStyle(d).color); d.remove(); }
  for (let n = svg.parentElement; !bg && n; n = n.parentElement) { const c = parse(getComputedStyle(n).backgroundColor); if (c && c.a > 0) bg = blend(c, { r: 255, g: 255, b: 255 }); }
  if (!bg) bg = { r: 255, g: 255, b: 255, a: 1 };
  const paint = (el, prop) => { const v = getComputedStyle(el)[prop]; if (!v || v === 'none') return null; const c = parse(v); return c && c.a > 0 ? blend(c, bg) : null; };

  // outside viewBox
  for (const el of shapes) {
    const r = rect(el); if (!r.w && !r.h) continue;
    if (hasVB && (r.l < root.l - tol || r.t < root.t - tol || r.r > root.r + tol || r.b > root.b + tol))
      issue('error', 'outside-viewbox', el, 'sale del viewBox');
  }
  const texts = all.filter(e => e.tagName === 'text' && e.textContent.trim()).map(el => ({ el, r: rect(el), fs: parseFloat(getComputedStyle(el).fontSize) * scale }));
  const boxes = shapes.filter(e => ['rect', 'circle', 'ellipse'].includes(e.tagName)).map(el => ({ el, r: rect(el) }))
    .filter(b => b.r.w * b.r.h > 0 && b.r.w * b.r.h < .85 * rootArea);
  const inside = (b, x, y) => x >= b.l - .5 && x <= b.r + .5 && y >= b.t - .5 && y <= b.b + .5;
  let minFont = Infinity;
  for (const t of texts) {
    minFont = Math.min(minFont, t.fs);
    if (t.fs < o.minFont) issue('error', 'min-font', t.el, `fuente ${t.fs.toFixed(1)}px < ${o.minFont}px (a la escala real)`);
    const anc = getComputedStyle(t.el).textAnchor, r = t.r;
    const ax = anc === 'middle' ? (r.l + r.r) / 2 : anc === 'end' ? r.r : r.l, ay = (r.t + r.b) / 2;
    const cont = boxes.filter(b => inside(b.r, ax, ay)).sort((a, b) => a.r.w * a.r.h - b.r.w * b.r.h)[0];
    t.cont = cont;
    if (cont) {
      const b = cont.r;
      if (r.l < b.l - 1 || r.r > b.r + 1 || r.t < b.t - 1 || r.b > b.b + 1)
        issue('error', 'text-overflow', t.el, `el texto no cabe en ${describe(cont.el)} (sobra ${Math.round(Math.max(b.l - r.l, r.r - b.r, 0))}px en horizontal)`);
    }
    // contrast vs container fill (or background)
    const fg = paint(t.el, 'fill'), back = (cont && paint(cont.el, 'fill')) || bg;
    if (fg) { const need = t.fs >= 24 ? 3 : 4.5, c = ratio(fg, back); if (c < need) issue('warn', 'contrast-text', t.el, `contraste ${c.toFixed(1)}:1 < ${need}:1`); }
  }
  for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
    const a = texts[i].r, b = texts[j].r;
    const ox = Math.min(a.r, b.r) - Math.max(a.l, b.l), oy = Math.min(a.b, b.b) - Math.max(a.t, b.t);
    if (ox > 2 && oy > .25 * Math.min(a.h, b.h)) issue('error', 'text-overlap', texts[i].el, `se encima con ${describe(texts[j].el)}`);
  }
  // text partially covered by a non-container shape; lines crossing text
  for (const t of texts) {
    const ta = t.r.w * t.r.h; if (!ta) continue;
    for (const b of boxes) {
      if (b === t.cont) continue;
      const ox = Math.min(t.r.r, b.r.r) - Math.max(t.r.l, b.r.l), oy = Math.min(t.r.b, b.r.b) - Math.max(t.r.t, b.r.t);
      const full = t.r.l >= b.r.l - 1 && t.r.r <= b.r.r + 1 && t.r.t >= b.r.t - 1 && t.r.b <= b.r.b + 1;
      if (!full && ox > 0 && oy > 0 && ox * oy > .2 * ta) issue('warn', 'text-shape', t.el, `cruza parcialmente ${describe(b.el)}`);
    }
    const pad = t.r.h * .15;
    for (const l of shapes.filter(e => ['path', 'line', 'polyline'].includes(e.tagName))) {
      const cs = getComputedStyle(l); if (cs.stroke === 'none' || cs.fill !== 'none') continue;
      let len; try { len = l.getTotalLength(); } catch (e) { continue; }
      const m = l.getScreenCTM(), step = Math.max(3, len / 400); let hits = 0;
      for (let d = 0; d <= len; d += step) {
        const p = l.getPointAtLength(d), x = m.a * p.x + m.c * p.y + m.e, y = m.b * p.x + m.d * p.y + m.f;
        if (x > t.r.l && x < t.r.r && y > t.r.t + pad && y < t.r.b - pad) hits++;
      }
      if (hits >= 2) issue('warn', 'text-line', t.el, `una línea (${describe(l)}) cruza el texto`);
    }
  }
  // graphics contrast
  const outlines = shapes.filter(e => { const c = getComputedStyle(e); return c.fill === 'none' && c.stroke !== 'none' && parseFloat(c.strokeWidth) > 0 && e.tagName !== 'line'; })
    .map(rect);
  for (const el of shapes.filter(e => ['rect', 'circle', 'ellipse', 'path', 'polygon'].includes(e.tagName))) {
    const r = rect(el); if (r.w * r.h >= .85 * rootArea) continue;
    const f = paint(el, 'fill'); if (!f) continue;
    const s = paint(el, 'stroke'), best = Math.max(ratio(f, bg), s ? ratio(s, bg) : 1);
    // a separate fill:none outline drawn over the face (e.g. .ill-line) counts as its edge
    const outlined = outlines.some(q => q.l <= r.l + tol && q.t <= r.t + tol && q.r >= r.r - tol && q.b >= r.b - tol);
    if (best < 3 && !outlined) issue('warn', 'contrast-graphic', el, `contraste ${best.toFixed(1)}:1 < 3:1 contra el fondo`);
  }
  const vb = hasVB ? svg.viewBox.baseVal : { width: 0, height: 0 };
  return { issues: out, stats: { texts: texts.length, shapes: shapes.length, minFont: isFinite(minFont) ? +minFont.toFixed(1) : null, scale: +scale.toFixed(3), viewBox: [vb.width, vb.height] } };
}
""".replace("SHAPESET", "new Set(['" + "','".join(sorted(s for s in SHAPES)) + "'])")


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _describe(e):
    s = _local(e.tag)
    if e.get("id"):
        s += "#" + e.get("id")
    elif e.get("class"):
        s += "." + e.get("class").split()[0]
    if s.startswith("text"):
        s += ' "' + "".join(e.itertext()).strip()[:24] + '"'
    return s


def static_checks(root, size, deck_ids=frozenset(), deck_mode=False, seen_ids=None):
    """Static rules over a parsed <svg> element; returns [(level, rule, element, message)]."""
    out = []
    add = lambda lvl, rule, el, msg: out.append((lvl, rule, _describe(el) if el is not None else "svg", msg))
    if not root.get("viewBox"):
        add("error", "viewbox", root, "falta viewBox; sin él no escala")
    kids = {_local(c.tag) for c in root}
    labelled = root.get("aria-label") or root.get("aria-labelledby")
    if "title" not in kids and not root.get("aria-label"):
        add("warn", "a11y-title", root, "sin <title> ni aria-label")
    if "desc" not in kids and not labelled:
        add("warn", "a11y-desc", root, "sin <desc> que explique la figura")
    if root.get("role") != "img":
        add("warn", "a11y-role", root, 'falta role="img"')

    ids, refs, parents = Counter(), set(), {}
    for p in root.iter():
        for c in p:
            parents[c] = p
    for e in root.iter():
        if e.get("id"):
            ids[e.get("id")] += 1
        for k, v in e.attrib.items():
            refs.update(REF_RE.findall(v))
            if _local(k) == "href" and v.startswith("#"):
                refs.add(v[1:])
            if _local(k) == "aria-labelledby":
                refs.update(v.split())
        if _local(e.tag) == "style" and e.text:
            refs.update(REF_RE.findall(e.text))
    for i, n in ids.items():
        if n > 1:
            add("error", "duplicate-id", root, f'id duplicado "{i}" ({n} veces)')
        if seen_ids is not None and i in seen_ids:
            add("error", "duplicate-id", root, f'id "{i}" ya existe en svg[{seen_ids[i]}] del mismo deck')
    for r in sorted(refs):
        if r not in ids and r not in deck_ids:
            add("error", "broken-ref", root, f'referencia rota a "#{r}"')

    def in_defs(e):
        while e in parents:
            e = parents[e]
            if _local(e.tag) in ("defs", "symbol", "marker", "clipPath", "mask", "pattern"):
                return True
        return False

    for d in (e for e in root.iter() if _local(e.tag) == "defs"):
        for c in d:
            if c.get("id") and c.get("id") not in refs:
                add("warn", "unused-def", c, "definición sin usar")

    seen, dup = set(), 0
    for e in root.iter():
        t = _local(e.tag)
        if t not in SHAPES or in_defs(e):
            continue
        key = (t, tuple(sorted((k, v) for k, v in e.attrib.items() if k != "id")), "".join(e.itertext()).strip())
        if key in seen:
            add("warn", "duplicate-element", e, "elemento idéntico repetido")
        seen.add(key)
        if t == "path":
            d = e.get("d", "")
            if len(re.findall(r"[MmLlHhVvCcSsQqTtAaZz]", d)) > MAX_PATH_CMDS:
                add("warn", "path-complexity", e, f"más de {MAX_PATH_CMDS} comandos")
            if re.search(r"\.\d{%d,}" % (MAX_DECIMALS + 1), d):
                add("warn", "path-decimals", e, f"más de {MAX_DECIMALS} decimales")
        if deck_mode:
            vals = [e.get(k, "") for k in ("fill", "stroke")] + [e.get("style", "")]
            if any(HEX_RE.search(v) for v in vals):
                add("warn", "hardcoded-color", e, "color fijo; usa una clase del tema (.d-box, .ill-*, ...)")
    if size > MAX_BYTES:
        add("warn", "size", root, f"{size / 1024:.1f} KB > 30 KB")
    return out


def _wrap(svg_text, width, bg):
    svg_text = re.sub(r"^\s*(<\?xml.*?\?>|<!DOCTYPE[^>]*>)\s*", "", svg_text, flags=re.S).strip()
    body_bg = f"background:{bg};" if bg else "background:var(--bg);"
    return (f"<!doctype html><meta charset=utf-8><style>{PAGE_CSS}html,body{{margin:0;{body_bg}}}"
            f"body>svg{{display:block;width:{width}px;height:auto}}</style>{svg_text}")


def _launch(pw):
    return pw.chromium.launch(**({"executable_path": os.environ["CHROMIUM_PATH"]} if os.environ.get("CHROMIUM_PATH") else {}))


def _geometry(handle, a):
    r = handle.evaluate(GEOMETRY_JS, {"minFont": a.min_font, "bg": a.bg})
    return [(i["level"], i["rule"], i["element"], i["message"]) for i in r["issues"]], r["stats"]


def _split(issues):
    pick = lambda lvl: [{"rule": r, "element": e, "message": m} for l, r, e, m in issues if l == lvl]
    return pick("error"), pick("warn")


def run(a):
    path = Path(a.file)
    if not path.is_file():
        return None, f"no existe el archivo: {path}"
    text = path.read_text(encoding="utf-8-sig")
    deck_mode = path.suffix.lower() in (".html", ".htm")
    results = []
    from playwright.sync_api import sync_playwright
    if not deck_mode:
        try:
            root = ET.fromstring(text.encode("utf-8"))
        except ET.ParseError as e:
            return None, f"XML inválido: {e}"
        if _local(root.tag) != "svg":
            return None, "la raíz no es <svg>"
        issues = static_checks(root, len(text.encode("utf-8")))
        with sync_playwright() as pw:
            b = _launch(pw)
            page = b.new_page(viewport={"width": a.width, "height": 1000}, device_scale_factor=a.scale)
            page.set_content(_wrap(text, a.width, a.bg))
            page.evaluate("document.fonts.ready")
            h = page.query_selector("body > svg")
            g, stats = _geometry(h, a)
            if a.render:
                h.screenshot(path=a.render)
            b.close()
        results.append((issues + g, stats))
        return results, None
    with sync_playwright() as pw:
        b = _launch(pw)
        page = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=a.scale)
        page.goto(path.resolve().as_uri(), wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        page.add_style_tag(content=".hint{display:none!important}.reveal{opacity:1!important;transform:none!important;transition:none!important}")
        deck_ids = set(page.evaluate("[...document.querySelectorAll('[id]')].filter(e => !e.closest('.fig')).map(e => e.id)"))
        handles = page.query_selector_all(".fig svg:not(svg svg):not(.mermaid-svg svg)")  # Mermaid output is mermaid-check's job
        seen = {}
        for n, h in enumerate(handles, 1):
            idx = h.evaluate("s => { const sl = s.closest('.slide'); return window.deck && window.deck.slides ? [...window.deck.slides].indexOf(sl) : -1 }")
            if idx >= 0:
                page.evaluate("i => window.deck.go(i)", idx)
                page.wait_for_timeout(700)
            ser = h.evaluate("s => new XMLSerializer().serializeToString(s)")
            try:
                root = ET.fromstring(ser)
            except ET.ParseError as e:
                results.append(([("error", "xml", "svg", f"no serializable: {e}")], {}))
                continue
            issues = static_checks(root, len(ser.encode("utf-8")), deck_ids, True, seen)
            for i in {e.get("id") for e in root.iter() if e.get("id")}:
                seen.setdefault(i, n)
            g, stats = _geometry(h, a)
            if a.render:
                p = Path(a.render)
                h.screenshot(path=str(p.with_name(f"{p.stem}-{n}{p.suffix}")) if len(handles) > 1 else a.render)
            results.append((issues + g, stats))
        b.close()
    return results, None


def main():
    ap = argparse.ArgumentParser(prog="svg-check", description="Valida un SVG o los SVG en línea de un deck HTML.")
    ap.add_argument("file")
    ap.add_argument("--bg", help="color de fondo para contraste (CSS); por defecto el del tema o del deck")
    ap.add_argument("--min-font", type=float, default=14, help="tamaño mínimo de fuente en px a escala real")
    ap.add_argument("--width", type=int, default=1600, help="ancho de render para un .svg suelto")
    ap.add_argument("--render", metavar="OUT.png", help="guarda un PNG del render")
    ap.add_argument("--scale", type=float, default=2, help="factor de píxeles del PNG")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    results, err = run(a)
    if err:
        print(json.dumps({"file": a.file, "ok": False, "error": err}) if a.json else f"ERROR input {err}", file=sys.stdout if a.json else sys.stderr)
        sys.exit(2)
    nerr = nwarn = 0
    svgs = []
    for n, (issues, stats) in enumerate(results, 1):
        errors, warns = _split(issues)
        nerr, nwarn = nerr + len(errors), nwarn + len(warns)
        svgs.append({"index": n, "errors": errors, "warnings": warns, "stats": stats})
        if not a.json:
            for lvl, rule, el, msg in issues:
                print(f"{'ERROR' if lvl == 'error' else 'WARN'} {rule} svg[{n}] {el} {msg}")
    if a.json:
        print(json.dumps({"file": a.file, "ok": nerr == 0, "svgs": svgs}, ensure_ascii=False))
    else:
        if not results:
            print("(sin <svg> dentro de .fig)")
        print(f"{len(results)} svg · {nerr} error(s), {nwarn} aviso(s)")
    sys.exit(1 if nerr else 0)


if __name__ == "__main__":
    main()
