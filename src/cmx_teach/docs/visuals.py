"""Convert Mermaid diagrams (.mmd) and charts (.chart.json) to PNG with the document preset colours.
Usage: docs-visuals DIR|FILE... [--preset utez]   (needs network for Mermaid: pinned CDN, Playwright Chromium)"""
import json
import os
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from cmx_teach.slides.charts import chart

MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"
# Subset of the document presets that visuals need (same values as docs build presets).
PRESETS = {
    "utez": dict(font="Arial", text="1B2633", muted="5B6573", accent="00735B", line="C9D3CD", labelFill="E6EFEA",
                 series=["009475", "2A78D6", "EB6834", "6250D6"]),
    "apa": dict(font="Times New Roman", text="000000", muted="404040", accent="000000", line="000000", labelFill="F2F2F2",
                series=["1F4E79", "9E3508", "0A6155", "6250D6"]),
    "corporativo": dict(font="Calibri", text="262626", muted="595959", accent="2E75B6", line="BFC9D9", labelFill="E8EEF7",
                        series=["2A78D6", "EB6834", "1BAF7A", "6250D6"]),
    "tecnico": dict(font="Calibri", text="1F2328", muted="57606A", accent="0B5CAD", line="C8D1DC", labelFill="E7EEF6",
                    series=["0B5CAD", "D95926", "1BAF7A", "9085E9"]),
    "editorial": dict(font="Georgia", text="1A1A1A", muted="55504A", accent="8B1E3F", line="1A1A1A", labelFill="F1EDE5",
                      series=["8B1E3F", "2A78D6", "008300", "EDA100"]),
}
MMD_RE = re.compile(r"\.mmd$|\.chart\.json$", re.I)

INIT_JS = """async (T) => {
  try {
    window.mermaid.initialize({ startOnLoad: false, theme: 'base', securityLevel: 'strict', htmlLabels: false,
      flowchart: { htmlLabels: false, curve: 'basis', padding: 16 }, gitGraph: { rotateCommitLabel: false },
      themeVariables: { fontFamily: T.font + ', Arial', fontSize: '20px', background: '#ffffff',
        primaryColor: '#' + T.labelFill, primaryTextColor: '#' + T.text, primaryBorderColor: '#' + T.accent, lineColor: '#' + T.muted,
        secondaryColor: '#F4F6F8', tertiaryColor: '#ffffff', clusterBkg: '#F7F9FA', clusterBorder: '#' + T.line, edgeLabelBackground: '#ffffff',
        noteBkgColor: '#FFF8E1', noteTextColor: '#' + T.text, actorBkg: '#' + T.labelFill, actorBorder: '#' + T.accent,
        git0: '#' + T.series[0], git1: '#' + T.series[1], git2: '#' + T.series[2], git3: '#' + T.series[3],
        pie1: '#' + T.series[0], pie2: '#' + T.series[1], pie3: '#' + T.series[2], pie4: '#' + T.series[3] } });
    await window.mermaid.run({ querySelector: '.mermaid' });
    const s = document.querySelector('#box svg'); const vb = s.viewBox.baseVal;
    s.style.maxWidth = 'none'; s.style.width = Math.max(vb.width, 900) + 'px';
    return null;
  } catch (e) { return String(e.message || e); }
}"""


def _css(P):
    c = lambda h: "#" + h
    f = P["font"]
    series = "".join(f".ch-s{i + 1}{{fill:{c(s)};stroke:{c(s)}}}" for i, s in enumerate(P["series"]))
    return f"""body{{margin:0;background:#fff;font-family:{f},Arial,sans-serif}}
#box{{display:inline-block;padding:16px;background:#fff}}
.chart{{width:1000px;height:auto;overflow:visible}}
.ch-grid{{stroke:#E3E6EA;stroke-width:1}}.ch-axis{{stroke:#8A9099;stroke-width:1.5}}
.ch-tick{{fill:{c(P['muted'])};font:500 20px {f},Arial}}.ch-label{{fill:{c(P['text'])};font:500 22px {f},Arial}}.ch-value{{fill:{c(P['text'])};font:700 22px {f},Arial}}
{series}
path.ch-s1:not(.ch-line),path.ch-s2:not(.ch-line),path.ch-s3:not(.ch-line),path.ch-s4:not(.ch-line){{stroke:none}}
.ch-mute{{fill:#B8BEC6!important}}.ch-line{{fill:none!important;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}}.ch-area{{opacity:.12}}
.ch-dot{{stroke:#fff!important;stroke-width:3}}.ch-hit{{fill:transparent;stroke:none}}"""


def main():
    args = sys.argv[1:]
    name = "utez"
    if "--preset" in args:
        i = args.index("--preset")
        name = args[i + 1] if i + 1 < len(args) else ""
        del args[i:i + 2]
    P = PRESETS.get(name)
    if not P:
        print("Preset desconocido", file=sys.stderr)
        sys.exit(2)
    paths = [Path(a) for a in args if not a.startswith("--")]
    files = [f for p in paths for f in (sorted(p.iterdir()) if p.is_dir() else [p])]
    files = [f for f in files if MMD_RE.search(f.name)]
    if not files:
        print("Uso: docs-visuals figs/ [--preset utez]  (busca *.mmd y *.chart.json)", file=sys.stderr)
        sys.exit(2)
    css = _css(P)
    with sync_playwright() as pw:
        launch = {"executable_path": os.environ["CHROMIUM_PATH"]} if os.environ.get("CHROMIUM_PATH") else {}
        browser = pw.chromium.launch(**launch)
        page = browser.new_page(device_scale_factor=2, viewport={"width": 1400, "height": 1000})
        for f in files:
            out = f.with_name(MMD_RE.sub(".png", f.name))
            if f.name.lower().endswith(".mmd"):
                src = f.read_text(encoding="utf-8").replace("<", "&lt;")
                body = f'<div id="box"><pre class="mermaid">{src}</pre></div>'
            else:
                body = f'<div id="box">{chart(json.loads(f.read_text(encoding="utf-8")))}</div>'
            page.set_content(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>')
            if f.name.lower().endswith(".mmd"):
                try:
                    page.add_script_tag(url=MERMAID_URL)
                except Exception as e:
                    print(f"Falta Mermaid (se carga desde el CDN): {e}", file=sys.stderr)
                    browser.close()
                    sys.exit(1)
                err = page.evaluate(INIT_JS, P)
                if err:
                    print(f"✘ {f}: {err}", file=sys.stderr)
                    continue
            page.locator("#box").screenshot(path=str(out))
            print(f"✔ {out}")
        browser.close()


if __name__ == "__main__":
    main()
