"""Shared build state (replaces the closures inside docgen.mjs build())."""
import os
import re
from pathlib import Path

from docx import Document
from docx.opc.constants import CONTENT_TYPE as CT, RELATIONSHIP_TYPE as RT
from docx.opc.packuri import PackURI
from docx.opc.part import Part

from .presets import L10N, PAGES, PRESETS
from .xmlkit import BuildError, esc


def as_list(x):
    return [] if x is None else x if isinstance(x, list) else [x]


def plain(t):
    t = re.sub(r"\*\*|\*|`|==|\^\[[^\]]*\]", "", "" if t is None else str(t))
    return re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t).strip()


class Ctx:
    def __init__(self, spec, base_dir):
        name = spec.get("preset") or "utez"
        if name not in PRESETS:
            raise BuildError(f"Preset desconocido: {spec.get('preset')}")
        self.spec = spec
        self.P = {**PRESETS[name], **(spec.get("theme") or {})}
        self.preset_name = name
        self.lang = spec.get("lang") or "es-MX"
        self.T = L10N.get(self.lang[:2], L10N["es"])
        self.meta = spec.get("meta") or {}
        self.page = dict(PAGES[spec.get("page") or "letter"])
        self.landscape = spec.get("orientation") == "landscape"
        m = spec.get("margins")
        self.M = self.P["margins"] if m is None else m
        self.text_w = (self.page["height"] if self.landscape else self.page["width"]) - 2 * self.M
        hn = spec.get("numberedHeadings")
        self.head_numbered = self.P["headNumbered"] if hn is None else hn
        self.pages_map = spec.get("_pages") or {"headings": {}, "captions": {}}
        self.answer_key = bool(spec.get("_answerKey"))
        self.base_dir = Path(base_dir)
        blocks = [b for k in ("front", "body") for b in as_list(spec.get(k))]
        self.has_index = any(isinstance(b, dict) and b.get("type") in ("toc", "lof", "lot") for b in blocks)
        uf = spec.get("updateFields")
        # Word asks "update fields?" on open only when indices lack page numbers (no 2nd pass yet)
        self.update_fields = uf if uf is not None else (self.has_index and not spec.get("_pages"))
        self.doc = Document()
        self.head_log, self.cap_log, self.head_count = [], {}, [0, 0, 0]
        self.head_numbers_on = False
        self.numbering = []  # (numId, abstractNum xml)
        self.footnotes, self.fn_id, self._fn_part = [], 0, None
        self.pic_id = 0
        self.block = None  # set by blocks.py (dispatcher)
        self.heads_num = self.new_numbering("heads") if self.head_numbered else None

    # ── files and images
    def resolve(self, p):
        return Path(p) if os.path.isabs(p) else self.base_dir / p

    def load_image(self, part, path):
        from docx.image.exceptions import UnrecognizedImageError
        try:
            rid, img = part.get_or_add_image(str(path))
        except (FileNotFoundError, IsADirectoryError):
            raise BuildError(f"No se encontró la imagen: {path}")
        except UnrecognizedImageError:
            raise BuildError("Formato de imagen no soportado (usa PNG o JPG)")
        return rid, img.px_width, img.px_height

    def pic_run(self, rid, w, h, title, descr, name):
        """Inline picture run; w/h in px at 96 dpi."""
        from docx.oxml.shape import CT_Inline
        from lxml import etree
        self.pic_id += 1
        inline = CT_Inline.new_pic_inline(self.pic_id, rid, name, int(w) * 9525, int(h) * 9525)
        dp = inline.docPr
        dp.set("name", name)
        dp.set("descr", descr)
        dp.set("title", title)
        return "<w:r><w:drawing>" + etree.tostring(inline, encoding="unicode") + "</w:drawing></w:r>"

    # ── numbering definitions (each list gets its own num so it restarts)
    def new_numbering(self, kind):
        nid = len(self.numbering) + 1
        lv = ""
        for l in range(3):
            if kind == "heads":
                fmt, txt, ind = "decimal", ".".join(f"%{i + 1}" for i in range(l + 1)) + ("." if l == 0 else ""), (0, 0)
            elif kind == "numbers":
                fmt, txt, ind = ["decimal", "lowerLetter", "lowerRoman"][l], f"%{l + 1}.", (720 + 360 * l, 360)
            else:
                fmt, txt, ind = "bullet", (["☐"] * 3 if kind == "check" else ["•", "◦", "▪"])[l], (720 + 360 * l, 360)
            lv += (f'<w:lvl w:ilvl="{l}"><w:start w:val="1"/><w:numFmt w:val="{fmt}"/><w:lvlText w:val="{txt}"/>'
                   f'<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="{ind[0]}" w:hanging="{ind[1]}"/></w:pPr></w:lvl>')
        self.numbering.append((nid, f'<w:abstractNum w:abstractNumId="{nid}"><w:multiLevelType w:val="hybridMultilevel"/>{lv}</w:abstractNum>'))
        return nid

    # ── footnotes
    def fn_part(self):
        if self._fn_part is None:
            self._fn_part = Part(PackURI("/word/footnotes.xml"), CT.WML_FOOTNOTES, b"", self.doc.part.package)
            self.doc.part.relate_to(self._fn_part, RT.FOOTNOTES)
        return self._fn_part

    def add_footnote(self, text):
        from .inline import runs
        from .xmlkit import para, run
        self.fn_id += 1
        fid, part = self.fn_id, self.fn_part()
        ref = '<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r>' + run(" ")
        self.footnotes.append(f'<w:footnote w:id="{fid}">' + para(ref + runs(self, text, None, part), style="FootnoteText") + "</w:footnote>")
        return f'<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteReference w:id="{fid}"/></w:r>'
