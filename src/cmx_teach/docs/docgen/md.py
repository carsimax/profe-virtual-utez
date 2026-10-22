"""Block Markdown -> blocks (headings, lists, tables, code, quotes/callouts, figures, \\newpage)."""
import re

from .xmlkit import page_break

ITEM = re.compile(r"^(\s*)([-*]|\d+[.)])\s+(?:\[[ xX]\]\s+)?(.*)$")


def md(ctx, src):
    block = ctx.block
    lines = str(src).replace("\r", "").split("\n")
    out, buf, i = "", [], 0

    def flush():
        nonlocal out, buf
        if buf:
            out += block(ctx, {"type": "p", "text": " ".join(buf).replace("\n ", "\n")})
            buf = []

    while i < len(lines):
        l = lines[i]
        if not l.strip():
            flush(); i += 1; continue
        m = re.match(r"^(#{1,3})\s+(.*)$", l)
        if m:
            flush(); out += block(ctx, {"type": "h" + str(len(m.group(1))), "text": m.group(2)}); i += 1; continue
        if re.match(r"^\\newpage\s*$", l):
            flush(); out += page_break(); i += 1; continue
        if l.startswith("```"):
            flush(); lang = l[3:].strip(); code = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i]); i += 1
            i += 1
            out += block(ctx, {"type": "code", "text": "\n".join(code), "lang": lang}); continue
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)", l)
        if m:
            flush(); out += block(ctx, {"type": "figure", "caption": m.group(1) or None, "src": m.group(2)}); i += 1; continue
        if re.match(r"^>\s?", l):
            flush(); q = []
            while i < len(lines) and re.match(r"^>\s?", lines[i]):
                q.append(re.sub(r"^>\s?", "", lines[i])); i += 1
            k = re.match(r"^\[!(\w+)\]\s*(.*)$", q[0] if q else "")
            out += block(ctx, {"type": "callout", "kind": k.group(1).lower(), "title": k.group(2) or None, "text": "\n".join(q[1:])}
                         if k else {"type": "quote", "text": " ".join(q)})
            continue
        if re.match(r"^\s*\|", l):
            flush(); t = []
            while i < len(lines) and re.match(r"^\s*\|", lines[i]):
                t.append(lines[i]); i += 1
            parse = lambda r: [c.strip() for c in re.sub(r"^\||\|$", "", r.strip()).split("|")]
            sep = next((k for k, r in enumerate(t) if re.match(r"^\s*\|?\s*:?-{2,}", r)), -1)
            headers = parse(t[0]) if sep == 1 else None
            align = ([("c" if c.startswith(":") else "r") if c.endswith(":") else "l" for c in parse(t[1])] if sep == 1 else None)
            out += block(ctx, {"type": "table", "headers": headers, "align": align,
                               "rows": [parse(r) for r in t[2 if sep == 1 else 0:]]})
            continue
        if re.match(r"^\s*([-*]|\d+[.)])\s+", l):
            flush()
            items = []; stack = [(-1, items)]
            kind = "numbers" if re.match(r"^\s*\d", l) else "check" if re.match(r"^\s*[-*]\s+\[[ xX]\]", l) else "bullets"
            while i < len(lines) and (m := ITEM.match(lines[i])):
                ind, node = len(m.group(1)), {"text": m.group(3), "items": []}
                while len(stack) > 1 and ind <= stack[-1][0]:
                    stack.pop()
                stack[-1][1].append(node); stack.append((ind, node["items"])); i += 1
            out += block(ctx, {"type": {"numbers": "numbers", "check": "checklist", "bullets": "bullets"}[kind], "items": items})
            continue
        buf.append(re.sub(r"\\$", "", l).strip() + "\n" if re.search(r"\s{2,}$|\\$", l) else l.strip())
        i += 1
    flush()
    return out
