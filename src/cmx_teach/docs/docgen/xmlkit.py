"""Tiny WordprocessingML string builders. Child order follows the OOXML schema sequences."""
from xml.sax.saxutils import escape

ALIGN = {"left": "left", "center": "center", "right": "right", "justify": "both"}
NONE = ("none", 0, "FFFFFF")


class BuildError(Exception):
    """User-facing build error; `named` is set once the failing block has been named."""

    named = False


def esc(s):
    return escape(str(s), {'"': "&quot;"})


def rpr(o=None):
    o = o or {}
    x = ""
    if o.get("style"):
        x += f'<w:rStyle w:val="{o["style"]}"/>'
    if o.get("font"):
        f = esc(o["font"])
        x += f'<w:rFonts w:ascii="{f}" w:eastAsia="{f}" w:hAnsi="{f}" w:cs="{f}"/>'
    if o.get("bold"):
        x += "<w:b/><w:bCs/>"
    if o.get("italics"):
        x += "<w:i/><w:iCs/>"
    if o.get("color"):
        x += f'<w:color w:val="{o["color"]}"/>'
    if o.get("spacing"):
        x += f'<w:spacing w:val="{o["spacing"]}"/>'
    if o.get("size"):
        s = round(o["size"])
        x += f'<w:sz w:val="{s}"/><w:szCs w:val="{s}"/>'
    if o.get("highlight"):
        x += f'<w:highlight w:val="{o["highlight"]}"/>'
    if o.get("underline"):
        x += '<w:u w:val="single"/>'
    if o.get("shade"):
        x += f'<w:shd w:val="clear" w:color="auto" w:fill="{o["shade"]}"/>'
    if o.get("vert"):
        x += f'<w:vertAlign w:val="{o["vert"]}"/>'
    return f"<w:rPr>{x}</w:rPr>" if x else ""


def run(text, o=None):
    """One run; \\t becomes <w:tab/> and \\n becomes <w:br/> (never raw in w:t)."""
    out = ""
    for i, line in enumerate(str(text).split("\n")):
        if i:
            out += "<w:br/>"
        for j, seg in enumerate(line.split("\t")):
            if j:
                out += "<w:tab/>"
            if seg:
                out += f'<w:t xml:space="preserve">{esc(seg)}</w:t>'
    return f"<w:r>{rpr(o)}{out}</w:r>"


def br_run(o=None):
    return f"<w:r>{rpr(o)}<w:br/></w:r>"


def border(tag, spec):
    """spec = (style, size, color[, space])"""
    style, size, color, *sp = spec
    return f'<w:{tag} w:val="{style}" w:sz="{size}" w:space="{sp[0] if sp else 0}" w:color="{color}"/>'


def single(color, size=4, style="single", space=0):
    return (style, size, color, space)


def borders(tag, d):
    """d: side -> spec; emitted in schema order."""
    order = ("top", "left", "bottom", "right", "insideH", "insideV")
    inner = "".join(border(k, d[k]) for k in order if k in d)
    return f"<w:{tag}>{inner}</w:{tag}>" if inner else ""


def ppr(o=None, sect=""):
    o = o or {}
    x = ""
    if o.get("style"):
        x += f'<w:pStyle w:val="{o["style"]}"/>'
    if o.get("keepNext"):
        x += "<w:keepNext/>"
    if o.get("keepLines"):
        x += "<w:keepLines/>"
    if o.get("pageBreakBefore"):
        x += "<w:pageBreakBefore/>"
    if o.get("frame"):
        f = o["frame"]
        x += (f'<w:framePr w:w="{f["w"]}" w:h="{f["h"]}" w:x="{f["x"]}" w:y="{f["y"]}" '
              'w:hAnchor="margin" w:vAnchor="margin"/>')
    if o.get("numId"):
        x += f'<w:numPr><w:ilvl w:val="{o.get("ilvl", 0)}"/><w:numId w:val="{o["numId"]}"/></w:numPr>'
    if o.get("border"):
        x += borders("pBdr", o["border"])
    if o.get("tabs"):
        x += "<w:tabs>" + "".join(
            f'<w:tab w:val="{t}" w:pos="{p}"' + (f' w:leader="{ld}"' if ld else "") + "/>"
            for t, p, ld in o["tabs"]) + "</w:tabs>"
    sp = "".join(f' w:{k}="{o[k]}"' for k in ("before", "after", "line") if o.get(k) is not None)
    if sp:
        x += f"<w:spacing{sp}" + (' w:lineRule="auto"' if o.get("line") is not None else "") + "/>"
    if o.get("ind"):
        x += "<w:ind" + "".join(f' w:{k}="{v}"' for k, v in o["ind"].items()) + "/>"
    if o.get("align"):
        x += f'<w:jc w:val="{ALIGN[o["align"]]}"/>'
    if o.get("outline") is not None:
        x += f'<w:outlineLvl w:val="{o["outline"]}"/>'
    x += sect
    return f"<w:pPr>{x}</w:pPr>" if x else ""


def para(inner="", sect="", **o):
    return f"<w:p>{ppr(o, sect)}{inner}</w:p>"


def spacer(after=120):
    return para(before=0, after=after)


def page_break():
    return "<w:p><w:r><w:br w:type=\"page\"/></w:r></w:p>"


def field(instr, cached="1", o=None):
    """Complex field, one run per part, each with the same rPr (LibreOffice ignores the rPr of a one-run field)."""
    r = rpr(o)
    return (f'<w:r>{r}<w:fldChar w:fldCharType="begin"/></w:r>'
            f'<w:r>{r}<w:instrText xml:space="preserve">{instr}</w:instrText></w:r>'
            f'<w:r>{r}<w:fldChar w:fldCharType="separate"/></w:r>'
            f'<w:r>{r}<w:t>{cached}</w:t></w:r>'
            f'<w:r>{r}<w:fldChar w:fldCharType="end"/></w:r>')


def fld_simple(instr, cached, o=None):
    return f'<w:fldSimple w:instr="{esc(instr)}"><w:r>{rpr(o)}<w:t>{cached}</w:t></w:r></w:fldSimple>'
