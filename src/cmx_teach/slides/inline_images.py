"""Replace src="local/path.png" with data URIs. Usage: slides-inline-images index.html"""
import base64
import mimetypes
import re
import sys
from pathlib import Path

# (?<![\w-]) keeps data-src="..." (and similar) untouched: only a real src= attribute matches.
PATTERN = re.compile(r'(?<![\w-])(src=")(?!data:|https?:)([^"]+)(")')


def main():
    html = Path(sys.argv[1])
    base = html.parent

    def repl(m):
        p = base / m.group(2)
        if not p.is_file():
            return m.group(0)
        mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        return f'{m.group(1)}data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}{m.group(3)}'

    s = PATTERN.sub(repl, html.read_text(encoding="utf-8"))
    html.write_text(s, encoding="utf-8")
    print(f"{html} · {len(s)/1024:.0f} KB")


if __name__ == "__main__":
    main()
