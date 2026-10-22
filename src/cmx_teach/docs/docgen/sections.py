"""Cover, header/footer and page setup."""
from .context import as_list
from .inline import runs
from .presets import PAGES
from .tables import kv
from .xmlkit import page_break, para, run, single, spacer
from .fields import numpages_field, page_field


def logo(ctx, part, h):
    m = ctx.meta
    if not m.get("logo"):
        return None
    rid, pw, ph = ctx.load_image(part, ctx.resolve(m["logo"]))
    return ctx.pic_run(rid, round(h * pw / ph), h, "Logo", m.get("institution") if isinstance(m.get("institution"), str) else "Logo", "logo")


def cover_kind(ctx):
    c = ctx.spec.get("cover")
    return ("apa" if ctx.P["captionStyle"] == "apa" else "institucional") if c is True else c


def cover(ctx):
    P, m = ctx.P, ctx.meta
    part = ctx.doc.part
    if cover_kind(ctx) == "apa":
        lg = logo(ctx, part, 80)
        out = para(lg, align="center", after=480) if lg else spacer(1440)
        out += para(runs(ctx, m.get("title"), {"bold": True}), align="center", before=1440, after=480)
        out += "".join(para(runs(ctx, t), align="center") for t in as_list(m.get("subtitle"))) + spacer(480)
        for v in (m.get(k) for k in ("author", "institution", "department", "course", "teacher", "date")):
            if v:
                out += "".join(para(runs(ctx, t), align="center", after=0) for t in as_list(v))
        return out
    out = ""
    lg = logo(ctx, part, m.get("logoHeight") or 110)
    if lg:
        out += para(lg, after=240)
    out += "".join(para(runs(ctx, t, {"bold": True, "color": P["head"], "size": P["size"] + 2}), after=0) for t in as_list(m.get("institution")))
    out += "".join(para(runs(ctx, t, {"color": P["muted"]}), after=0) for t in as_list(m.get("department")))
    out += spacer(1600)
    if m.get("kicker"):
        out += para(run(str(m["kicker"]).upper(), {"bold": True, "color": P["accent"], "size": P["size"] - 2, "spacing": 40}), after=120)
    out += para(runs(ctx, m.get("title")), style="Title")
    out += "".join(para(runs(ctx, t), style="Subtitle") for t in as_list(m.get("subtitle")))
    out += para(before=120, after=480, border=dict(bottom=single(P["rule"], 24, "single", 1)))
    if m.get("fields"):
        out += kv(ctx, {"rows": m["fields"], "cols": 2})
    else:
        out += "".join(para(runs(ctx, t, {"bold": True})) for t in as_list(m.get("author")))
    foot = ", ".join(str(x) for x in (m.get("place"), m.get("date")) if x)
    avail = (ctx.page["width"] if ctx.landscape else ctx.page["height"]) - 2 * ctx.M
    if foot:  # anchored to the page foot with a frame, independent of the content above
        out += para(runs(ctx, foot, {"color": P["muted"]}), align="right", after=0, frame=dict(w=ctx.text_w, h=360, x=0, y=avail - 360))
    return out


def short_title(ctx):
    m = ctx.meta
    for k in ("headerText", "shortTitle", "title"):
        if m.get(k) is not None:
            return m[k]
    return None


def header(ctx):
    """Returns fn(part) -> header paragraphs xml, or None."""
    if ctx.spec.get("header") is False:
        return None
    P, tw, st = ctx.P, ctx.text_w, short_title(ctx)

    def build(part):
        if P["captionStyle"] == "apa":
            txt = str(st or "").upper() if ctx.spec.get("runningHead") else ""
            return para(run(txt, {"size": P["size"]}) + run("\t", {"size": P["size"]}) + page_field({"size": P["size"]}),
                        tabs=[("right", tw, None)], after=0)
        lg = logo(ctx, part, 26)
        inst = as_list(ctx.meta.get("institution"))
        left = lg or run(inst[0] if inst else "", {"color": P["muted"], "size": P["hdr"]})
        return para(left + run("\t" + (str(st).replace("*", "") if st else ""), {"color": P["muted"], "size": P["hdr"]}),
                    tabs=[("right", tw, None)], after=0, border=dict(bottom=single(P["rule"], 6, "single", 4)))
    return build


def footer(ctx, roman):
    if ctx.spec.get("footer") is False or ctx.P["captionStyle"] == "apa":
        return None
    P, T, spec = ctx.P, ctx.T, ctx.spec
    o = {"size": 18, "color": P["muted"]}
    multi = bool(spec.get("cover") or as_list(spec.get("front")))
    fmt = spec.get("pageFormat")
    if roman or fmt == "simple" or (multi and fmt != "total"):
        kids = page_field(o)
    else:
        kids = run(T["page"] + " ", o) + page_field(o) + run(f" {T['of']} ", o) + numpages_field(o)
    xml = para(kids, align="center")
    return lambda part: xml


def sect_children(ctx, fmt=None, start=1):
    pw, ph = ctx.page["width"], ctx.page["height"]
    M = ctx.M
    size = f'<w:pgSz w:w="{ph}" w:h="{pw}" w:orient="landscape"/>' if ctx.landscape else f'<w:pgSz w:w="{pw}" w:h="{ph}" w:orient="portrait"/>'
    return (size + f'<w:pgMar w:top="{M}" w:right="{M}" w:bottom="{M}" w:left="{M}" w:header="{ctx.P["hdrDist"]}" w:footer="{ctx.P["hdrDist"]}" w:gutter="0"/>'
            + (f'<w:pgNumType w:start="{start}" w:fmt="{fmt}"/>' if fmt else "") + '<w:docGrid w:linePitch="360"/>')
