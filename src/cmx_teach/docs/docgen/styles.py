"""Document defaults and named styles, rewritten into the python-docx template's styles part."""
import re

from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

from .xmlkit import esc, ppr, rpr


def _style(sid, name, kind="paragraph", based="Normal", nxt=None, quick=True, run=None, para=None):
    x = f'<w:name w:val="{name}"/>'
    if based:
        x += f'<w:basedOn w:val="{based}"/>'
    if nxt:
        x += f'<w:next w:val="{nxt}"/>'
    if quick:
        x += "<w:qFormat/>"
    x += ppr(para) + rpr(run)
    return f'<w:style w:type="{kind}" w:styleId="{sid}">{x}</w:style>'


def _clamp(style):
    for el in style.iter(qn("w:sz"), qn("w:szCs")):
        el.getparent().remove(el)
    for el in style.iter(qn("w:spacing")):
        if el.get(qn("w:line")) is not None:
            el.set(qn("w:line"), "240")
            el.set(qn("w:lineRule"), "auto")


def install_styles(ctx):
    P, lang = ctx.P, ctx.lang
    apa = P["headingCase"] == "apa"
    sz = P["size"]

    def h(lvl, size, run=None, para=None):
        base_para = (dict(before=240, after=0, line=480) if apa else dict(before=[240, 180, 140][lvl], after=[100, 80, 60][lvl]))
        return _style(f"Heading{lvl + 1}", f"heading {lvl + 1}", nxt="Normal",
                      run={"font": P["fontHead"], "size": size, "bold": True, "color": P["head"], "italics": apa and lvl == 2, **(run or {})},
                      para={"keepNext": True, "keepLines": True, "outline": lvl, **base_para,
                            "align": "center" if apa and lvl == 0 else "left", "ind": {"firstLine": 0}, **(para or {})})

    styles = [
        h(0, P["h1"]),
        h(1, P["h2"], run=None if apa else {"color": P["head"]}),
        h(2, P["h3"], run={"italics": True} if apa else {"italics": True, "color": P["accent"]}),
        _style("Title", "Title", nxt="Normal", run={"font": P["fontHead"], "size": P["title"], "bold": True, "color": P["head"]},
               para={"after": 80 if not apa else 120, "line": P["titleLine"], "ind": {"firstLine": 0}}),
        _style("TOCHeading", "TOC Heading", nxt="Normal", run={"font": P["fontHead"], "size": P["h1"], "bold": True, "color": P["head"]},
               para={"keepNext": True, "before": 0 if apa else 80, "after": 240 if apa else 120, "align": "center" if apa else "left", "ind": {"firstLine": 0}}),
        _style("Subtitle", "Subtitle", nxt="Normal", run={"font": P["font"], "size": P["subtitle"], "color": P["muted"]},
               para={"after": 120, "ind": {"firstLine": 0}}),
        _style("Caption", "caption", nxt="Normal", run={"size": sz if apa else P["small"], "color": P["text"] if apa else P["muted"]},
               para={"line": 480 if apa else 240, "ind": {"firstLine": 0}}),
        _style("Quote", "Quote", nxt="Normal", run={"italics": not apa, "color": P["text"] if apa else P["muted"]},
               para={"ind": {"left": 720, "right": 0 if apa else 720, "firstLine": 0}, "before": 120 if apa else 80, "after": 160 if apa else 100}),
        _style("CodeBlock", "Code Block", quick=False, run={"font": P["mono"], "size": 18, "color": "24292F"},
               para={"before": 0, "after": 0, "line": 240, "ind": {"firstLine": 0}}),
        _style("Reference", "Bibliography Entry", nxt="Reference",
               para={"ind": {"left": 720, "hanging": 720}, "after": 0 if apa else 120, "line": 480 if apa else P["lineSpacing"]}),
        _style("BodyText", "Body Text", nxt="BodyText",
               para={"ind": {"firstLine": P["firstLine"] or 0}, "align": "justify" if P["justify"] else "left"}),
        _style("Lead", "Lead", quick=False, run={"size": P["lead"], "color": P["muted"]}, para={"after": 240 if apa else 160}),
        _style("Small", "Small", quick=False, run={"size": P["small"], "color": P["muted"]}, para={"after": 120 if apa else 80, "line": 240, "ind": {"firstLine": 0}}),
        _style("ListParagraph", "List Paragraph"),
        _style("FootnoteText", "footnote text", quick=False, run={"size": P["small"]}, para={"after": 0, "line": 240, "ind": {"firstLine": 0}}),
        _style("FootnoteReference", "footnote reference", kind="character", based="DefaultParagraphFont", quick=False, run={"vert": "superscript"}),
        _style("Hyperlink", "Hyperlink", kind="character", based="DefaultParagraphFont", quick=False,
               run={"color": "1F4E79" if P["accent"] == "000000" else P["accent"], "underline": True}),
    ]
    root = ctx.doc.styles.element
    defaults = parse_xml(
        f'<w:docDefaults {nsdecls("w")}><w:rPrDefault><w:rPr>'
        f'<w:rFonts w:ascii="{esc(P["font"])}" w:eastAsia="{esc(P["font"])}" w:hAnsi="{esc(P["font"])}" w:cs="{esc(P["font"])}"/>'
        f'<w:color w:val="{P["text"]}"/><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/><w:lang w:val="{lang}"/></w:rPr></w:rPrDefault>'
        f'<w:pPrDefault><w:pPr><w:spacing w:after="{P["after"]}" w:line="{P["lineSpacing"]}" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>')
    old = root.find(qn("w:docDefaults"))
    if old is not None:
        root.replace(old, defaults)
    else:
        root.insert(0, defaults)
    new_ids = {}
    for xml in styles:
        el = parse_xml(xml.replace("<w:style ", f"<w:style {nsdecls('w')} ", 1))
        new_ids[el.get(qn("w:styleId"))] = el
    for s in list(root.findall(qn("w:style"))):
        if s.get(qn("w:styleId")) in new_ids:
            root.remove(s)
        else:  # drop list links to the template's own numbering, which we replace
            for np_ in s.findall(f"{qn('w:pPr')}/{qn('w:numPr')}"):
                np_.getparent().remove(np_)
    for el in new_ids.values():
        root.append(el)
    if not apa:  # house layout: leftover template styles must not bring sizes outside 9-11 pt or non-single spacing
        for st in root.findall(qn("w:style")):
            if st.get(qn("w:styleId")) not in new_ids:
                _clamp(st)
        for part in ctx.doc.part.package.iter_parts():
            if str(part.partname).endswith("stylesWithEffects.xml"):
                part._blob = re.sub(r'w:line="\d+"', 'w:line="240"', re.sub(r'<w:sz(?:Cs)? w:val="\d+"/>', "", part.blob.decode())).encode()
    # Normal: no inherited overrides, everything comes from docDefaults
    normal = next((s for s in root.findall(qn("w:style")) if s.get(qn("w:styleId")) == "Normal"), None)
    if normal is not None:
        for c in list(normal):
            if c.tag in (qn("w:pPr"), qn("w:rPr")):
                normal.remove(c)
