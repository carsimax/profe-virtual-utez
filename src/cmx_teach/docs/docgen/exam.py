"""Exam blocks: questions (+ answer key mode) and the student header."""
import re

from .inline import runs
from .tables import callout, kv
from .xmlkit import NONE, borders, para, run, single, spacer


def is_ans(a, k):
    return (type(a) is int and a == k) or (isinstance(a, str) and len(a.strip()) <= 2 and a.strip() != ""
                                            and ord(a.strip().lower()[0]) - 97 == k)


def tf_val(a):
    s = "" if a is None else str(a)
    if a is True or re.fullmatch(r"(v|verdadero|true|t|c|cierto)", s, re.I):
        return True
    if a is False or re.fullmatch(r"(f|falso|false)", s, re.I):
        return False
    return None


def student_header(ctx, fields):
    T, meta = ctx.T, ctx.meta
    f = fields or [*([[T["course"], meta["course"]]] if meta.get("course") else []),
                   *([[T["teacher"], meta["teacher"]]] if meta.get("teacher") else []),
                   [T["name"], ""], [T["group"], meta.get("group") or ""], [T["date"], ""], [T["score"], ""]]
    return kv(ctx, {"rows": f, "cols": 4})


def questions(ctx, b):
    from .blocks import figure
    from .tables import cell, tbl, tc, tr
    P, T, tw = ctx.P, ctx.T, ctx.text_w
    if ctx.answer_key:
        b = {**b, "showAnswers": True}
    show = b.get("showAnswers")
    out = ""
    if b.get("studentHeader") is not False:
        out += student_header(ctx, b.get("fields"))
    if show:
        out += para(run(T["key"].upper(), {"bold": True, "color": "C0392B", "spacing": 40}), after=160)
    if b.get("instructions"):
        out += callout(ctx, {"kind": "info", "title": b.get("instructionsTitle") or "Instrucciones", "text": b["instructions"]})
    total = 0
    for i, q in enumerate(b["items"]):
        total += q.get("points") or 0
        pts = run(f"\t({q['points']} {T['points']})", {"color": P["muted"], "size": P["cell"]}) if q.get("points") else ""
        out += para(run(f"{i + 1}. ", {"bold": True}) + runs(ctx, q.get("q")) + pts, keepNext=True, before=200, after=80, tabs=[("right", tw, None)])
        if q.get("figure"):
            f = q["figure"]
            out += figure(ctx, {"src": f, "width": 0.6} if isinstance(f, str) else {"width": 0.6, **f})
        opts = q.get("options") or []
        for k, o in enumerate(opts):
            mark = run(f"  ← {T['correct']}", {"bold": True, "color": P["accent"]}) if show and is_ans(q.get("answer"), k) else ""
            out += para(run(chr(97 + k) + ") ", {"bold": True}) + runs(ctx, o) + mark, ind={"left": 720, "hanging": 360}, after=40, keepNext=k < len(opts) - 1)
        if q.get("kind") == "tf":
            v = tf_val(q.get("answer"))
            mk = lambda on: "( X )" if show and on else "(    )"
            out += para(run(f"{mk(v is True)} {T['true']}        {mk(v is False)} {T['false']}", {"bold": bool(show) and v is not None}), ind={"left": 720})
        nl = q.get("lines")
        if nl is None:
            nl = 0 if (opts or q.get("kind") == "tf") else 3
        if nl > 0:
            w = tw - 1080
            line = tc(w, "<w:p/>", dict(top=NONE, left=NONE, right=NONE, bottom=single("A6ADB4", 4, "dotted")), mar=None, valign=None)
            out += tbl(w, [w], [tr([line], height=440) for _ in range(nl)],
                       brd=dict(top=NONE, left=NONE, right=NONE, bottom=NONE, insideV=NONE, insideH=NONE), ind=360)
        if show and q.get("answerText"):
            out += callout(ctx, {"kind": "tip", "title": T["answer"], "text": q["answerText"]})
    if b.get("showTotal") is not False and total:
        out += para(run(f"Total: {total} {T['points']}", {"bold": True}), align="right", before=240)
    return out
