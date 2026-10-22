"""Block dispatcher and the simple blocks (headings, paragraphs, lists, figure, quote, references)."""
import json
import re
import unicodedata

from .context import as_list, plain
from .exam import questions
from .fields import caption, index_block, front_title, source_line, toc_block
from .inline import runs, runs_br
from .md import md
from .tables import callout, code, kv, rubric, signatures, table_block
from .xmlkit import BuildError, page_break, para, run, single, spacer


def heading(ctx, lvl, text, opts=None):
    opts = opts or {}
    numbered = ctx.head_numbers_on and not opts.get("unnumbered")
    num = ""
    if numbered:
        hc = ctx.head_count
        hc[lvl - 1] += 1
        for k in range(lvl, 3):
            hc[k] = 0
        num = ".".join(map(str, hc[:lvl])) + ("." if lvl == 1 else "")
    if not opts.get("noToc"):
        ctx.head_log.append(dict(title=(num + " " if num else "") + plain(text), key=plain(text), level=lvl))
    return para(runs(ctx, text), style=f"Heading{lvl}", pageBreakBefore=bool(opts.get("newPage")),
                numId=ctx.heads_num if numbered else None, ilvl=lvl - 1)


def lst(ctx, items, kind="bullets"):
    nid = ctx.new_numbering({"checklist": "check"}.get(kind, kind))
    line = 480 if ctx.P["lineSpacing"] > 400 else ctx.P["lineSpacing"]
    out = []

    def walk(arr, lvl):
        for it in arr:
            t = it if isinstance(it, str) else it.get("text")
            out.append(para(runs(ctx, t), style="ListParagraph", numId=nid, ilvl=min(lvl, 2), after=60, line=line))
            if isinstance(it, dict) and it.get("items"):
                walk(it["items"], lvl + 1)
    walk(items, 0)
    return "".join(out)


def figure(ctx, b):
    P = ctx.P
    f = ctx.resolve(b["src"])
    if re.search(r"\.mmd$|\.chart\.json$", str(f), re.I):
        png = f.with_name(re.sub(r"\.mmd$|\.chart\.json$", ".png", f.name, flags=re.I))
        if not png.exists():
            d = str(b["src"]).rsplit("/", 1)[0] if "/" in str(b["src"]) else "."
            raise BuildError(f"Falta {png.name}: ejecuta: uv run docs-visuals {d} --preset {ctx.preset_name}")
        f = png
    rid, pw, ph = ctx.load_image(ctx.doc.part, f)
    from .presets import PAGES
    max_w = round(ctx.text_w / 1440 * 96 * (b.get("width") or 0.9))
    max_h = round((PAGES[ctx.spec.get("page") or "letter"]["height"] - 2 * ctx.M) / 1440 * 96 * 0.62)
    w = max_w if b.get("width") else min(max_w, pw)
    h = round(w * ph / pw)
    if h > max_h:
        h = max_h
        w = round(h * pw / ph)
    alt = b.get("alt") or b.get("caption") or "Imagen"
    apa = P["captionStyle"] == "apa"
    img = para(ctx.pic_run(rid, w, h, alt, alt, f.name), align="center", keepNext=bool(b.get("caption")) and not apa, before=120, after=60)
    out = ""
    if b.get("caption") and apa:
        out += caption(ctx, "fig", b["caption"], "above")
    out += img
    if b.get("caption") and not apa:
        out += caption(ctx, "fig", b["caption"], "below")
    if b.get("source"):
        out += source_line(ctx, b["source"])
    return out


def references(ctx, b):
    items = list(as_list(b.get("items")))
    if b.get("sort") is not False:
        def key(t):
            s = unicodedata.normalize("NFD", re.sub(r"[*_]", "", t))
            return ("".join(c for c in s if not unicodedata.combining(c)).casefold(), t)
        items.sort(key=key)
    return (heading(ctx, 1, b.get("title") or ctx.T["refs"], {"unnumbered": True, "newPage": b.get("newPage")})
            + "".join(para(runs(ctx, t), style="Reference") for t in items))


def block(ctx, b):
    try:
        return block0(ctx, b)
    except BuildError as e:
        if e.named:
            raise
        what = (f"Markdown “{b[:40].replace(chr(10), ' ')}…”" if isinstance(b, str)
                else f"bloque {b.get('type', '?')} {json.dumps(b, ensure_ascii=False)[:60]}")
        err = BuildError(f"{e}\n  en {what}")
        err.named = True
        raise err from None


def block0(ctx, b):
    if isinstance(b, str):
        return md(ctx, b)
    if b.get("md"):
        return md(ctx, b["md"])
    t, P = b.get("type"), ctx.P
    if t in ("h1", "h2", "h3"):
        return heading(ctx, int(t[1]), b.get("text"), b)
    if t == "p":
        st = {"lead": "Lead", "small": "Small"}.get(b.get("style")) or (None if b.get("noIndent") or b.get("align") else "BodyText")
        return para(runs_br(ctx, b.get("text")), style=st, align=b.get("align"))
    if t in ("bullets", "numbers", "checklist"):
        return lst(ctx, b["items"], t)
    if t == "quote":
        return (para(runs(ctx, b.get("text")), style="Quote")
                + (para(runs(ctx, "— " + b["cite"]), style="Quote", align="right") if b.get("cite") else ""))
    if t == "table":
        return table_block(ctx, b)
    if t == "kv":
        return kv(ctx, b)
    if t == "figure":
        return figure(ctx, b)
    if t == "callout":
        return callout(ctx, b)
    if t == "code":
        return code(ctx, b)
    if t == "toc":
        return toc_block(ctx, b)
    if t in ("lof", "lot"):
        return index_block(ctx, b)
    if t == "title":
        return front_title(ctx, b.get("text"))
    if t == "references":
        return references(ctx, b)
    if t == "signatures":
        return signatures(ctx, b)
    if t == "questions":
        return questions(ctx, b)
    if t == "rubric":
        return rubric(ctx, b)
    if t == "pagebreak":
        return page_break()
    if t == "spacer":
        return spacer(b.get("size") or 240)
    if t == "rule":
        return para(border=dict(bottom=single(P["rule"], 8)), after=200)
    raise BuildError(f"Bloque desconocido: {json.dumps(b, ensure_ascii=False)[:80]}")


def blocks(ctx, arr):
    return "".join(block(ctx, b) for b in as_list(arr))
