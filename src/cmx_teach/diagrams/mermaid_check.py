"""Validate Mermaid diagrams (.mmd file or HTML deck) with Mermaid 11.4.1 in Chromium.
Usage: mermaid-check FILE [--render DIR] [--json] [--max-nodes 12]
Exit: 0 no errors, 1 errors, 2 unreadable file or no diagrams. Needs network (pinned CDN)."""
import argparse
import base64
import html
import json
import os
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"
SLIDE_W, SLIDE_H, MIN_PX = 1664, 700, 14  # usable area of a 1920x1080 slide, min legible size

# Diagram keywords bundled in Mermaid 11.4.1 (radar, treemap, ... arrived later).
ALLOWED = {
    "flowchart", "flowchart-v2", "graph", "sequencediagram", "classdiagram", "classdiagram-v2", "statediagram",
    "statediagram-v2", "erdiagram", "gitgraph", "gantt", "pie", "mindmap", "timeline", "quadrantchart",
    "requirementdiagram", "c4context", "c4container", "c4component", "c4dynamic", "c4deployment", "sankey-beta",
    "xychart-beta", "block-beta", "packet-beta", "architecture-beta", "kanban", "journey",
}

UTEZ = {
    "--bg": "#f7f8f6", "--surface": "#eef1ee", "--surface-2": "#e2e8e4", "--line": "#d0d8d3", "--line-strong": "#68716d",
    "--text": "#0d1d33", "--text-dim": "#47505a", "--accent": "#00735b", "--accent-2": "#2563a8",
    "--accent-3": "#a3470f", "--accent-4": "#6a3fa0", "--font-body": '"Source Sans 3", system-ui, sans-serif',
    "--series-1": "#009475", "--series-2": "#2a78d6", "--series-3": "#eb6834", "--series-4": "#6250d6",
}

PRE = re.compile(r'<pre\s+class="[^"]*\bmermaid\b[^"]*"[^>]*>([\s\S]*?)</pre>')
EMBED = re.compile(r"<!--mmd:([A-Za-z0-9+/=]*)-->")

# Same mapping as the html-slides template's renderMermaid (themeVariables from CSS variables).
INIT_JS = """(v) => {
  mermaid.initialize({ startOnLoad: false, theme: 'base', securityLevel: 'strict', htmlLabels: false,
    flowchart: { htmlLabels: false, curve: 'basis', padding: 20, nodeSpacing: 60, rankSpacing: 70 },
    themeVariables: { darkMode: false, background: v['--bg'], fontFamily: v['--font-body'], fontSize: '24px',
      primaryColor: v['--surface-2'], primaryTextColor: v['--text'], primaryBorderColor: v['--accent'],
      secondaryColor: v['--surface'], secondaryBorderColor: v['--line-strong'], secondaryTextColor: v['--text'],
      tertiaryColor: v['--bg'], tertiaryBorderColor: v['--line'], tertiaryTextColor: v['--text'],
      mainBkg: v['--surface-2'], nodeBorder: v['--accent'], clusterBkg: v['--surface'], clusterBorder: v['--line-strong'],
      lineColor: v['--line-strong'], textColor: v['--text'], titleColor: v['--text'], edgeLabelBackground: v['--bg'],
      noteBkgColor: v['--surface'], noteBorderColor: v['--line-strong'], noteTextColor: v['--text'],
      actorBkg: v['--surface-2'], actorBorder: v['--accent'], actorTextColor: v['--text'], signalColor: v['--text'], signalTextColor: v['--text'],
      labelBoxBkgColor: v['--surface'], labelTextColor: v['--text'], loopTextColor: v['--text'], activationBkgColor: v['--surface'],
      pie1: v['--series-1'], pie2: v['--series-2'], pie3: v['--series-3'], pie4: v['--series-4'],
      git0: v['--series-1'], git1: v['--series-2'], git2: v['--series-3'], git3: v['--series-4'], git4: v['--accent'], git5: v['--accent-2'], git6: v['--accent-3'], git7: v['--accent-4'],
      gitBranchLabel0: '#ffffff', gitBranchLabel1: '#ffffff', gitBranchLabel2: '#ffffff', gitBranchLabel3: '#ffffff', gitBranchLabel4: v['--bg'], gitBranchLabel5: v['--bg'], gitBranchLabel6: v['--bg'], gitBranchLabel7: v['--bg'],
      commitLabelColor: v['--text'], commitLabelBackground: v['--bg'], commitLabelFontSize: '18px', tagLabelColor: v['--bg'], tagLabelBackground: v['--accent'], tagLabelBorder: v['--accent'] },
    gitGraph: { rotateCommitLabel: false, showCommitLabel: true, mainBranchName: 'main' } });
}"""

PARSE_JS = """async (src) => { try { const r = await mermaid.parse(src); return { ok: true, type: r.diagramType }; }
  catch (e) { return { ok: false, msg: String(e.message || e) }; } }"""

RENDER_JS = """async ([src, id, W, H, cap]) => {
  const box = document.getElementById('box'); box.innerHTML = '';
  let svg;
  try { svg = (await mermaid.render(id, src)).svg; } catch (e) { return { error: String(e.message || e) }; }
  if (/Syntax error in text|class="error-icon"/.test(svg)) return { error: 'Mermaid rendered its error graphic (syntax error).' };
  box.innerHTML = svg;
  const el = box.querySelector('svg'), vb = el.viewBox.baseVal;
  if (vb && vb.width) el.style.width = Math.min(vb.width * cap, W, H * vb.width / vb.height) + 'px';
  el.style.height = 'auto';
  const scale = vb && vb.width ? el.getBoundingClientRect().width / vb.width : 1;
  const nodes = box.querySelectorAll('g.node, g.actor, g.statediagram-state, g.commit-label-bkg, g.root > g.nodes > g').length || box.querySelectorAll('g.node').length;
  const edges = box.querySelectorAll('.edgePaths path, path.flowchart-link, path.relation, path.transition, line[class^="messageLine"], path.relationshipLine').length;
  let minPx = null; const clipped = [];
  box.querySelectorAll('text, tspan').forEach(t => {
    if (t.tagName === 'tspan' && t.parentElement.tagName === 'text') return;
    if (!t.textContent.trim()) return;
    const px = parseFloat(getComputedStyle(t).fontSize) * scale;
    if (minPx === null || px < minPx) minPx = px;
  });
  box.querySelectorAll('g.node, g.classGroup').forEach(g => {
    const shape = g.querySelector('rect, polygon, circle, ellipse, path'); if (!shape) return;
    const s = shape.getBoundingClientRect();
    g.querySelectorAll('text').forEach(t => {
      if (!t.textContent.trim()) return;
      const r = t.getBoundingClientRect();
      if (r.left < s.left - 2 || r.right > s.right + 2 || r.top < s.top - 2 || r.bottom > s.bottom + 2) clipped.push(t.textContent.trim().slice(0, 40));
    });
  });
  return { nodes, edges, minPx, clipped, scale, w: Math.round(vb.width), h: Math.round(vb.height) };
}"""


def _first_keyword(src):
    lines = src.splitlines()
    i = 0
    if lines and lines[0].strip() == "---":
        i = next((n for n in range(1, len(lines)) if lines[n].strip() == "---"), -1) + 1
    for line in lines[i:]:
        s = line.strip()
        if s and not s.startswith("%%"):
            return re.split(r"[\s;]", s, 1)[0]
    return ""


def extract(path):
    """Return the Mermaid sources found in a .mmd file or an HTML deck."""
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() not in (".html", ".htm"):
        return [text]
    found = [(m.start(), html.unescape(m.group(1)).strip()) for m in PRE.finditer(text)]
    found += [(m.start(), base64.b64decode(m.group(1)).decode("utf-8")) for m in EMBED.finditer(text)]
    return [s for _, s in sorted(found)]


def lint(src, kind):
    """Static checks that need no browser. Returns [(rule, message)]."""
    out = []
    if not re.search(r"^\s*accTitle\s*:", src, re.M):
        out.append(("a11y-title", "missing accTitle (add it right after the diagram keyword)"))
    if not re.search(r"^\s*accDescr\s*(:|\{)", src, re.M):
        out.append(("a11y-descr", "missing accDescr (one sentence describing the diagram)"))
    for n, line in enumerate(src.splitlines(), 1):
        s = re.sub(r'"[^"]*"', '""', line)
        if kind == "sequencediagram":
            s = s.split(":", 1)[0]
        if s.strip() != "end" and re.search(r"(?<![\w\-#])end(?![\w\-])", s) and not s.strip().startswith(("%%", "accTitle", "accDescr")):
            out.append(("lowercase-end", f"line {n}: lowercase 'end' breaks flowcharts and sequence diagrams; write End or \"end\""))
        if kind in ("flowchart", "graph") and re.search(r"\[[^\]\"]*[(){}][^\]\"]*\]", s):
            out.append(("unquoted-special", f"line {n}: label has (), {{}} without quotes; wrap the label in double quotes"))
    return out


def _location(msg):
    return " ".join(x.strip() for x in msg.strip().splitlines()[:3])  # includes "on line N" from the parser


def check(sources, vars_, max_nodes, render_dir, page):
    page.set_content(f'<body style="margin:0;background:{vars_["--bg"]}"><div id="box" style="width:{SLIDE_W}px;padding:20px"></div></body>')
    page.add_script_tag(url=MERMAID_URL)
    page.evaluate("typeof mermaid")
    page.evaluate(INIT_JS, vars_)
    results = []
    for i, src in enumerate(sources, 1):
        kind = _first_keyword(src).lower()
        d = {"index": i, "type": kind or "unknown", "errors": [], "warnings": [], "stats": {}}
        err = lambda rule, msg: d["errors"].append({"rule": rule, "message": msg})
        warn = lambda rule, msg: d["warnings"].append({"rule": rule, "message": msg})
        results.append(d)
        for rule, msg in lint(src, kind):
            warn(rule, msg)
        if kind not in ALLOWED:
            err("unsupported-type", f"'{kind or '?'}' is not available in Mermaid 11.4.1 (radar, treemap and similar need v12)")
            continue
        p = page.evaluate(PARSE_JS, src)
        if not p["ok"]:
            err("parse", _location(p["msg"]))
            continue
        d["type"] = p["type"]
        # zoom caps mirror the deck template (gitGraph 2.6, others 1.5)
        r = page.evaluate(RENDER_JS, [src, f"mc-{i}", SLIDE_W, SLIDE_H, 2.6 if kind == "gitgraph" else 1.5])
        if "error" in r:
            err("render", r["error"])
            continue
        d["stats"] = {"nodes": r["nodes"], "edges": r["edges"], "min_text_px": round(r["minPx"], 1) if r["minPx"] else None,
                      "viewbox": [r["w"], r["h"]]}
        limit = 6 if "class" in p["type"] else max_nodes
        if r["nodes"] > limit:
            warn("too-many-nodes", f"{r['nodes']} nodes (limit {limit}); split the diagram")
        if r["edges"] > 20:
            warn("too-many-edges", f"{r['edges']} edges (limit 20); split the diagram")
        if r["minPx"] is not None and r["minPx"] < MIN_PX:
            warn("small-text", f"smallest text renders at {r['minPx']:.1f}px on a slide (min {MIN_PX}px); fewer nodes or shorter labels")
        for t in r["clipped"][:5]:
            warn("text-overflow", f"text overflows its shape: {t!r}")
        if render_dir:
            Path(render_dir).mkdir(parents=True, exist_ok=True)
            page.locator("#box").screenshot(path=str(Path(render_dir) / f"diagram-{i:02d}.png"))
    return results


def deck_vars(browser, path):
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(path.resolve().as_uri(), wait_until="domcontentloaded")
    got = page.evaluate("(names) => { const cs = getComputedStyle(document.documentElement);"
                        " return Object.fromEntries(names.map(n => [n, cs.getPropertyValue(n).trim()])); }", list(UTEZ))
    page.close()
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", got.get("--bg", "")):
        return None
    return {**UTEZ, **{k: v for k, v in got.items() if v}}  # deck vars win; gaps fall back to utez


def main():
    ap = argparse.ArgumentParser(prog="mermaid-check", description=__doc__.split("\n")[0])
    ap.add_argument("file")
    ap.add_argument("--render", metavar="DIR", help="write diagram-NN.png files")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--max-nodes", type=int, default=12)
    a = ap.parse_args()
    path = Path(a.file)
    try:
        sources = [s for s in extract(path) if s.strip()]
    except (OSError, UnicodeDecodeError, ValueError) as e:
        print(f"Error: cannot read {a.file}: {e}", file=sys.stderr)
        sys.exit(2)
    if not sources:
        print(f"No Mermaid diagrams found in {a.file}.", file=sys.stderr)
        sys.exit(2)
    try:
        with sync_playwright() as pw:
            launch = {"executable_path": os.environ["CHROMIUM_PATH"]} if os.environ.get("CHROMIUM_PATH") else {}
            browser = pw.chromium.launch(**launch)
            vars_ = (deck_vars(browser, path) if path.suffix.lower() in (".html", ".htm") else None) or UTEZ
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            try:
                results = check(sources, vars_, a.max_nodes, a.render, page)
            finally:
                browser.close()
    except Exception as e:
        print(f"Error: Mermaid could not load or run ({str(e).splitlines()[0]}). Mermaid 11.4.1 is fetched from the CDN; check your connection.", file=sys.stderr)
        sys.exit(2)
    errors = sum(len(d["errors"]) for d in results)
    warns = sum(len(d["warnings"]) for d in results)
    if a.json:
        print(json.dumps({"file": a.file, "ok": errors == 0, "diagrams": results}, indent=2))
    else:
        for d in results:
            for level, key in (("ERROR", "errors"), ("WARN", "warnings")):
                for x in d[key]:
                    print(f"{level} {d['index']} {x['rule']} {x['message']}")
        print(f"{len(results)} diagram(s): {errors} error(s), {warns} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
