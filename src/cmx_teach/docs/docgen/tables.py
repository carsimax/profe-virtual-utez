"""Tables and table-based blocks: table, kv, callout, code, signatures, rubric."""
from .fields import caption, source_line
from .inline import runs
from .xmlkit import NONE, borders, esc, para, single, spacer

CELL_MAR = dict(top=80, bottom=80, left=120, right=120)


def widths(ctx, n, pct=None):
    fr = pct if pct and len(pct) == n else [1] * n
    s = sum(fr)
    w = [int(ctx.text_w * f / s) for f in fr]  # floor, like Math.floor
    w[-1] += ctx.text_w - sum(w)
    return w


def tc(w, kids, brd=None, fill=None, mar=CELL_MAR, valign="center", span=None):
    x = f'<w:tcW w:w="{w}" w:type="dxa"/>'
    if span:
        x += f'<w:gridSpan w:val="{span}"/>'
    if brd:
        x += borders("tcBorders", brd)
    if fill:
        x += f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
    if mar:
        x += "<w:tcMar>" + "".join(f'<w:{k} w:w="{mar[k]}" w:type="dxa"/>' for k in ("top", "left", "bottom", "right") if k in mar) + "</w:tcMar>"
    if valign:
        x += f'<w:vAlign w:val="{valign}"/>'
    return f"<w:tc><w:tcPr>{x}</w:tcPr>{kids or '<w:p/>'}</w:tc>"


def tr(cells, header=False, cant_split=True, height=None):
    x = ("<w:cantSplit/>" if cant_split else "") + (f'<w:trHeight w:val="{height}" w:hRule="atLeast"/>' if height else "") + ("<w:tblHeader/>" if header else "")
    return f"<w:tr>{'<w:trPr>' + x + '</w:trPr>' if x else ''}{''.join(cells)}</w:tr>"


def tbl(width, grid, rows, brd=None, jc=None, ind=None):
    pr = f'<w:tblW w:w="{width}" w:type="dxa"/>'
    if jc:
        pr += f'<w:jc w:val="{jc}"/>'
    if ind:
        pr += f'<w:tblInd w:w="{ind}" w:type="dxa"/>'
    if brd:
        pr += borders("tblBorders", brd)
    pr += '<w:tblLayout w:type="fixed"/>'
    g = "".join(f'<w:gridCol w:w="{w}"/>' for w in grid)
    return f"<w:tbl><w:tblPr>{pr}</w:tblPr><w:tblGrid>{g}</w:tblGrid>{''.join(rows)}</w:tbl>"


def cell(ctx, content, w, align=None, size=None, bold=False, color=None, fill=None, brd=None, valign="center"):
    kids = "".join(
        para(runs(ctx, t, {"size": size or ctx.P["cell"], "bold": bold, "color": color}), align=align, before=0, after=0, line=ctx.P["cellLine"])
        for t in ("" if content is None else str(content)).split("\n"))
    return tc(w, kids, brd, fill, valign=valign)


NO_SIDES = dict(top=NONE, bottom=NONE, left=NONE, right=NONE)


def table(ctx, b):
    P = ctx.P
    style = b.get("style") or P["tableStyle"]
    n = len(b.get("headers") or b["rows"][0])
    W = widths(ctx, n, b.get("widths"))
    aligns = b.get("align") or []
    al = lambda i: {"r": "right", "c": "center"}.get(aligns[i] if i < len(aligns) else None, "left")
    outer = single(P["line"]) if style == "grid" else NONE
    hb = (dict(top=single(P["line"], 8), bottom=single(P["line"], 4), left=NONE, right=NONE) if style == "apa"
          else dict(top=single(P["head"], 12), bottom=single(P["head"], 6), left=NONE, right=NONE) if style == "lines"
          else dict(top=outer, bottom=outer, left=outer, right=outer) if style == "grid" else dict(NO_SIDES))
    fill_head = P["tableHead"] if style in ("banded", "grid") else None
    color_head = P["tableHeadText"] if fill_head else P["text"]
    rows = []
    if b.get("headers"):
        rows.append(tr([cell(ctx, h, W[i], bold=True, fill=fill_head, color=color_head, align=al(i), brd=hb)
                        for i, h in enumerate(b["headers"])], header=True))
    for ri, r in enumerate(b["rows"]):
        last = ri == len(b["rows"]) - 1
        bb = (dict(top=NONE, left=NONE, right=NONE, bottom=single(P["line"], 8) if last else NONE) if style == "apa"
              else dict(top=NONE, left=NONE, right=NONE, bottom=single(P["head"], 12) if last else single(P["line"], 4)) if style == "lines"
              else dict(top=outer, bottom=outer, left=outer, right=outer) if style == "grid"
              else dict(top=NONE, left=NONE, right=NONE, bottom=single(P["line"], 4)))
        rows.append(tr([cell(ctx, c, W[i], align=al(i), brd=bb, fill=P["band"] if style == "banded" and ri % 2 == 1 else None,
                             bold=bool(b.get("firstColBold")) and i == 0) for i, c in enumerate(r)]))
    return tbl(ctx.text_w, W, rows, brd=dict(top=NONE, bottom=NONE, left=NONE, right=NONE, insideH=NONE, insideV=NONE))


def table_block(ctx, b):
    out = caption(ctx, "tab", b["caption"], "above") if b.get("caption") else ""
    return out + table(ctx, b) + (source_line(ctx, b["source"]) if b.get("source") else spacer(200))


def all_borders(ctx):
    s = single(ctx.P["line"])
    return dict(top=s, bottom=s, left=s, right=s)


def kv(ctx, b):
    cols, pairs, P = b.get("cols") or 2, b["rows"], ctx.P
    W = widths(ctx, 4, [1.1, 2, 1.1, 2]) if cols == 4 else widths(ctx, 2, [1, 2.6])
    rows = []
    for i in range(0, len(pairs), cols // 2):
        cells = []
        for j in range(cols // 2):
            pr = pairs[i + j] if i + j < len(pairs) else ["", ""]
            cells.append(cell(ctx, pr[0], W[j * 2], bold=True, fill=P["labelFill"], size=P["cell"], brd=all_borders(ctx)))
            cells.append(cell(ctx, pr[1], W[j * 2 + 1], brd=all_borders(ctx)))
        rows.append(tr(cells))
    return tbl(ctx.text_w, W, rows) + spacer(160)


def callout(ctx, b):
    from .presets import CALLOUTS
    fill, bar, deftitle = CALLOUTS.get(b.get("kind") or "info", CALLOUTS["info"])
    kids = ""
    if b.get("title") is not False:
        kids += para(_bold(b.get("title") or deftitle, bar), after=60)
    import re
    for t in re.split(r"\n\s*\n", str(b.get("text") or "")):
        kids += para(runs(ctx, t), after=60, line=ctx.P["kvLine"])
    cellx = tc(ctx.text_w, kids, dict(left=single(bar, 24), top=NONE, bottom=NONE, right=NONE), fill, mar=dict(top=140, bottom=140, left=220, right=220), valign=None)
    return tbl(ctx.text_w, [ctx.text_w], [tr([cellx])]) + spacer(120)


def _bold(text, color):
    from .xmlkit import run
    return run(text, {"bold": True, "color": color})


def code(ctx, b):
    from .xmlkit import run
    out = para(runs(ctx, b["caption"]), style="Caption", keepNext=True) if b.get("caption") else ""
    lines = str(b.get("text") or "").replace("\t", "  ").split("\n")
    d = single("D0D7DE")
    kids = "".join(para(run(l if l else " "), style="CodeBlock") for l in lines)
    cellx = tc(ctx.text_w, kids, dict(top=d, bottom=d, left=d, right=d), "F6F8FA", mar=dict(top=120, bottom=120, left=200, right=200), valign=None)
    return out + tbl(ctx.text_w, [ctx.text_w], [tr([cellx], cant_split=False)]) + spacer(120)


def signatures(ctx, b):
    from .xmlkit import run
    P = ctx.P
    people = b.get("people") or []
    people = people if isinstance(people, list) else [people]
    cols = min(b.get("cols") or len(people) or 1, 3)
    tw = round(ctx.text_w * 0.5) if cols == 1 else ctx.text_w
    W = [tw // cols] * cols
    rows = []
    for i in range(0, len(people), cols):
        cells = []
        for j, w in enumerate(W):
            p = people[i + j] if i + j < len(people) else None
            if p:
                roles = p.get("role") or []
                roles = roles if isinstance(roles, list) else [roles]
                kids = para(runs(ctx, p["name"], {"bold": True}), before=900, after=0, border=dict(top=single(P["text"], 6)), align="center")
                kids += "".join(para(runs(ctx, r, {"size": P["cell"], "color": P["muted"]}), align="center", after=0) for r in roles)
            else:
                kids = "<w:p/>"
            cells.append(tc(w, kids, dict(NO_SIDES), mar=dict(left=240, right=240), valign=None))
        rows.append(tr(cells))
    return tbl(sum(W), W, rows, brd=dict(top=NONE, bottom=NONE, left=NONE, right=NONE, insideH=NONE, insideV=NONE), jc="center") + spacer(200)


def rubric(ctx, b):
    levels = b["levels"]
    headers = [b.get("criterionLabel") or "Criterio", *levels]
    has_w = any(c.get("weight") is not None for c in b["criteria"])
    if has_w:
        headers.insert(1, b.get("weightLabel") or "Peso")
    rows = [[f"**{c['name']}**" + ("\n" + c["desc"] if c.get("desc") else ""),
             *([str(c["weight"]) if c.get("weight") is not None else ""] if has_w else []), *c["levels"]] for c in b["criteria"]]
    wts = [1.4, *([0.75] if has_w else []), *[1.6 for _ in levels]]
    cap = caption(ctx, "tab", b["caption"], "above") if b.get("caption") else ""
    return cap + table(ctx, dict(headers=headers, rows=rows, widths=wts, style="grid", align=["l", "c"] if has_w else [])) + spacer(200)
