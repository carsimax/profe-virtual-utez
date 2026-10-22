"""Embed the deck's Mermaid diagrams as inline SVG (works offline afterwards and in the PDF).
Usage: slides-mermaid index.html   (needs network: Mermaid loads from the pinned CDN)
Re-runnable: embedded blocks keep their source and are rendered again."""
import base64
import os
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BLOCK = re.compile(r'<div class="mermaid-svg"><!--mmd:([A-Za-z0-9+/=]*)-->[\s\S]*?<!--/mmd--></div>')
PRE = re.compile(r'<pre class="[^"]*\bmermaid\b[^"]*"[^>]*>[\s\S]*?</pre>')


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    if len(sys.argv) < 2:
        print("Uso: slides-mermaid index.html", file=sys.stderr)
        sys.exit(2)
    file = Path(sys.argv[1])
    html = BLOCK.sub(lambda m: f'<pre class="mermaid">{_esc(base64.b64decode(m.group(1)).decode("utf-8"))}</pre>',
                     file.read_text(encoding="utf-8"))
    count = len(PRE.findall(html))
    if not count:
        print("No hay bloques pre.mermaid.")
        sys.exit(0)
    resolved = file.resolve()
    tmp = resolved.with_name(re.sub(r"\.html?$", "", resolved.name) + ".mermaid-tmp.html")
    tmp.write_text(html, encoding="utf-8")
    try:
        with sync_playwright() as pw:
            launch = {"executable_path": os.environ["CHROMIUM_PATH"]} if os.environ.get("CHROMIUM_PATH") else {}
            browser = pw.chromium.launch(**launch)
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            page.goto(tmp.as_uri(), wait_until="networkidle")
            page.evaluate("document.fonts.ready")
            state = ""
            try:
                page.wait_for_function("() => document.documentElement.dataset.mermaid", timeout=30000)
                state = page.evaluate("document.documentElement.dataset.mermaid")
            except Exception:
                state = "timeout"
            out = page.eval_on_selector_all(".mermaid-svg", "els => els.map(e => ({ svg: e.innerHTML, src: e.dataset.src || '' }))")
            browser.close()
    finally:
        tmp.unlink(missing_ok=True)
    if state != "done" or len(out) != count:
        print(f"Error: {state}, {len(out)}/{count} diagramas. Revisa la sintaxis o la conexión (Mermaid se carga desde el CDN).", file=sys.stderr)
        sys.exit(1)
    it = iter(out)

    def embed(_):
        o = next(it)
        return f'<div class="mermaid-svg"><!--mmd:{base64.b64encode(o["src"].encode("utf-8")).decode()}-->{o["svg"]}<!--/mmd--></div>'

    file.write_text(PRE.sub(embed, html), encoding="utf-8")
    print(f"{count} diagrama(s) Mermaid incrustados en {file}")


if __name__ == "__main__":
    main()
