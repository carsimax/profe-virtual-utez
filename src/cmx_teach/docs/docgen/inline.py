"""Inline Markdown: **bold**, *italic*, `code`, [text](url), ^[footnote], ==highlight==."""
import re

from docx.opc.constants import RELATIONSHIP_TYPE as RT

from .xmlkit import br_run, esc, rpr, run

RE = re.compile(r"(\*\*([^*]+)\*\*|\*([^*]+)\*|`([^`]+)`|\[([^\]]+)\]\(([^)\s]+)\)|\^\[([^\]]+)\]|==([^=]+)==)")


def runs(ctx, text, base=None, part=None):
    base = base or {}
    s = "" if text is None else str(text)
    out, last = "", 0
    for m in RE.finditer(s):
        if m.start() > last:
            out += run(s[last:m.start()], base)
        if m.group(2):
            out += runs(ctx, m.group(2), {**base, "bold": True}, part)
        elif m.group(3):
            out += runs(ctx, m.group(3), {**base, "italics": True}, part)
        elif m.group(4):
            out += run(m.group(4), {**base, "font": ctx.P["mono"], "size": max(18, round((base.get("size") or ctx.P["size"]) * 0.92)) if ctx.P["lineSpacing"] <= 240 else round((base.get("size") or ctx.P["size"]) * 0.92), "shade": "F1F3F5"})
        elif m.group(5):
            rid = (part or ctx.doc.part).relate_to(m.group(6), RT.HYPERLINK, is_external=True)
            out += f'<w:hyperlink r:id="{rid}" w:history="1">{run(m.group(5), {**base, "style": "Hyperlink"})}</w:hyperlink>'
        elif m.group(7):
            out += ctx.add_footnote(m.group(7))
        elif m.group(8):
            out += run(m.group(8), {**base, "highlight": "yellow"})
        last = m.end()
    if last < len(s):
        out += run(s[last:], base)
    return out


def runs_br(ctx, text, base=None):
    """Like runs() but a \\n inside the text is a line break."""
    out = ""
    for i, ln in enumerate(("" if text is None else str(text)).split("\n")):
        out += (br_run() if i else "") + runs(ctx, ln, base)
    return out
