"""Field-based pieces: SEQ captions, source line, TOC/LOT/LOF with cached entries, PAGE/NUMPAGES."""
from .context import plain
from .inline import runs
from .xmlkit import esc, field, fld_simple, page_break, para, run, spacer


def seq(ctx, label, text):
    log = ctx.cap_log.setdefault(label, [])
    n = len(log) + 1
    log.append(dict(title=f"{label} {n}. {plain(text)}", key=f"{label} {n}", text=plain(text), level=1))
    return fld_simple(f"SEQ {label} \\* ARABIC", n, {"bold": True})


def caption(ctx, kind, text, position):
    label = ctx.T["fig"] if kind == "fig" else ctx.T["tab"]
    if ctx.P["captionStyle"] == "apa":
        return (para(run(label + " ", {"bold": True}) + seq(ctx, label, text), style="Caption", keepNext=True, before=240, after=0)
                + para(runs(ctx, text, {"italics": True}), style="Caption", keepNext=True, after=120))
    above = position == "above"
    return para(run(label + " ", {"bold": True}) + seq(ctx, label, text) + run(". ", {"bold": True}) + runs(ctx, text),
                style="Caption", keepNext=above, align="center" if kind == "fig" else "left",
                **(dict(before=200, after=80) if above else dict(before=80, after=240)))


def source_line(ctx, text):
    apa = ctx.P["captionStyle"] == "apa"
    lead = run("Nota. " if apa else ctx.T["source"] + ": ", {"italics": apa})
    return para(lead + runs(ctx, text), style="Small", align="left" if apa else "center", after=200)


def front_title(ctx, text):
    return para(runs(ctx, text), style="TOCHeading")


def toc_field(ctx, alias, instr, entries):
    """entries: [(title, level, page|None)]. Field spans first..last entry paragraph inside an sdt, like docx-js."""
    dirty = ' w:dirty="true"' if ctx.update_fields else ""
    begin = (f'<w:r><w:fldChar w:fldCharType="begin"{dirty}/><w:instrText xml:space="preserve">{esc(instr)}</w:instrText>'
             '<w:fldChar w:fldCharType="separate"/></w:r>')
    end = '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
    tabs = [("right", ctx.text_w, "dot")]
    ps = []
    for i, (title, lvl, page) in enumerate(entries):
        body = ""
        if page is not None:
            body = f'<w:r><w:t xml:space="preserve">{esc(title)}</w:t><w:tab/><w:t>{page}</w:t></w:r>'
        else:
            body = run(title)
        ps.append(para((begin if i == 0 else "") + body + (end if i == len(entries) - 1 else ""), style=f"TOC{lvl}", tabs=tabs))
    if not ps:
        ps = [para(begin + end)]
    return f'<w:sdt><w:sdtPr><w:alias w:val="{esc(alias)}"/></w:sdtPr><w:sdtContent>{"".join(ps)}</w:sdtContent></w:sdt>'


def toc_block(ctx, b):
    lv = b.get("levels") or 3
    title = b.get("title") or ctx.T["toc"]
    pm = ctx.pages_map["headings"]
    entries = [(h["title"], h["level"], pm.get(h["key"])) for h in ctx.head_log if h["level"] <= lv]
    tail = spacer(240) if b.get("newPage") is False else page_break()
    return front_title(ctx, title) + toc_field(ctx, title, f'TOC \\h \\o "1-{lv}"', entries) + tail


def index_block(ctx, b):
    """lof / lot"""
    label = ctx.T["fig"] if b["type"] == "lof" else ctx.T["tab"]
    title = b.get("title") or (ctx.T["lof"] if b["type"] == "lof" else ctx.T["lot"])
    pm = ctx.pages_map["captions"]
    entries = [(c["title"], 1, pm.get(c["key"])) for c in ctx.cap_log.get(label, [])]
    tail = page_break() if b.get("newPage") else spacer(360)
    return front_title(ctx, title) + toc_field(ctx, label, f'TOC \\h \\c "{label}"', entries) + tail


def page_field(o):
    return field("PAGE", "1", o)


def numpages_field(o):
    return field("NUMPAGES", "1", o)
