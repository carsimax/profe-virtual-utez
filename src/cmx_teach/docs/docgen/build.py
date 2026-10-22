"""Assemble the document: sections, headers/footers, numbering, footnotes, settings, core properties."""
import io
import zipfile
from datetime import datetime

from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.section import Section

from . import blocks, sections as sec
from .context import Ctx, as_list
from .styles import install_styles
from .xmlkit import esc, para

NS = nsdecls("w", "r", "wp", "a", "pic")


def _children(xml, tag="w:body"):
    root = parse_xml(f"<{tag} {NS}>{xml}</{tag}>")
    return list(root)


def _plain(t):
    return str(t or "").replace("*", "")


def build_document(spec, base_dir="."):
    ctx = Ctx(spec, base_dir)
    ctx.block = blocks.block
    ctx.head_numbers_on = ctx.head_numbered
    body_list = [blocks.block(ctx, b) for b in as_list(spec.get("body"))]
    body_kids = "".join(body_list)
    ctx.head_numbers_on = False
    back_kids = blocks.blocks(ctx, spec.get("back"))
    front_kids = blocks.blocks(ctx, spec.get("front"))  # after the body: indices already know headings and captions

    # (xml, sectPr children, header builder, footer builder)
    plan = []
    if spec.get("cover"):
        plan.append((sec.cover(ctx), sec.sect_children(ctx), None, None))
    if front_kids:
        plan.append((front_kids, sec.sect_children(ctx, "lowerRoman", 1), sec.header(ctx), sec.footer(ctx, True)))
    plan.append((body_kids + back_kids, sec.sect_children(ctx, "decimal", 1), sec.header(ctx), sec.footer(ctx, False)))

    doc = ctx.doc
    body = doc.element.body
    final = body.sectPr
    for c in list(body):
        if c is not final:
            body.remove(c)
    for i, (xml, props, _, _) in enumerate(plan):
        last = i == len(plan) - 1
        for el in _children(xml):
            final.addprevious(el)
        if not last:
            for el in _children(para(sect=f"<w:sectPr>{props}</w:sectPr>")):
                final.addprevious(el)
    for c in list(final):
        final.remove(c)
    for c in _children(plan[-1][1], "w:sectPr"):
        final.append(c)

    sects = body.findall(f".//{qn('w:sectPr')}")
    for sp, (_, _, hdr, ftr) in zip(sects, plan):
        s = Section(sp, doc.part)
        for fn, part_of in ((hdr, s.header), (ftr, s.footer)):
            if fn is None:
                continue
            part_of.is_linked_to_previous = False
            root = part_of._element
            for c in list(root):
                root.remove(c)
            for el in _children(fn(part_of.part), "w:hdr"):
                root.append(el)

    install_styles(ctx)
    _numbering(ctx)
    _footnotes(ctx)
    _settings(ctx)
    _properties(ctx)
    ctx.doc.part.package  # noqa: B018 (keep reference alive)
    return doc, outline(ctx)


def outline(ctx):
    return dict(
        cover=sec.cover_kind(ctx) or False,
        hasIndex=ctx.has_index,
        headings=[dict(key=h["key"], level=h["level"]) for h in ctx.head_log],
        captions=[dict(key=c["key"], text=c["text"][:30]) for caps in ctx.cap_log.values() for c in caps],
    )


def _numbering(ctx):
    root = ctx.doc.part.numbering_part.element
    for c in list(root):
        root.remove(c)
    for nid, xml in ctx.numbering:
        root.append(parse_xml(xml.replace("<w:abstractNum ", f"<w:abstractNum {nsdecls('w')} ", 1)))
    for nid, _ in ctx.numbering:
        root.append(parse_xml(f'<w:num {nsdecls("w")} w:numId="{nid}"><w:abstractNumId w:val="{nid}"/></w:num>'))


def _footnotes(ctx):
    if ctx._fn_part is None:
        return
    sep = ('<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:separator/></w:r></w:p></w:footnote>'
           '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>')
    ctx._fn_part._blob = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<w:footnotes {NS}>{sep}{"".join(ctx.footnotes)}</w:footnotes>').encode("utf-8")
    st = ctx.doc.settings.element
    fp = parse_xml(f'<w:footnotePr {nsdecls("w")}><w:footnote w:id="-1"/><w:footnote w:id="0"/></w:footnotePr>')
    _insert_setting(st, fp, ("w:endnotePr", "w:compat", "w:docVars", "w:rsids"))


def _insert_setting(st, el, successors):
    for tag in successors:
        nxt = st.find(qn(tag))
        if nxt is not None:
            nxt.addprevious(el)
            return
    st.append(el)


def _settings(ctx):
    zoom = ctx.doc.settings.element.find(qn("w:zoom"))
    if zoom is not None and zoom.get(qn("w:percent")) is None:  # the default template omits the required attribute
        zoom.set(qn("w:percent"), "100")
    if ctx.update_fields:
        el = parse_xml(f'<w:updateFields {nsdecls("w")} w:val="true"/>')
        _insert_setting(ctx.doc.settings.element, el, ("w:hdrShapeDefaults", "w:footnotePr", "w:endnotePr", "w:compat", "w:docVars", "w:rsids"))


def _properties(ctx):
    m, cp = ctx.meta, ctx.doc.core_properties
    author = (as_list(m.get("author")) or [""])[0]
    cp.author = author or "word-docs"
    cp.title = _plain(m.get("title"))
    cp.comments = m.get("description") or ""
    cp.subject = m.get("subject") or ""
    cp.keywords = ", ".join(as_list(m.get("keywords")))
    cp.last_modified_by = author
    cp.category = ""
    cp.revision = 1
    cp.created = cp.modified = datetime(2000, 1, 1)


def save_deterministic(doc, path):
    """Save with fixed zip timestamps so equal specs give identical bytes."""
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    with zipfile.ZipFile(buf) as zin, zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            zi = zipfile.ZipInfo(info.filename, date_time=(2000, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = info.external_attr
            zout.writestr(zi, zin.read(info.filename))
