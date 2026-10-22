"""Convert PDF/Word/Excel/PowerPoint files to Markdown using firecrawl/anydoc."""

import argparse
import sys
from pathlib import Path

import anydoc


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="docs-to-md", description=__doc__)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--out-dir", type=Path, help="default: next to each source")
    ap.add_argument(
        "--ocr", choices=["hosted"], default="reject",
        help="OCR scanned pages; uploads the WHOLE document to Firecrawl (ask consent first)",
    )
    args = ap.parse_args(argv)
    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)

    code = 0
    for src in args.files:
        try:
            md = anydoc.to_markdown(src, ocr=args.ocr)
            dest = (args.out_dir or src.parent) / f"{src.stem}.md"
            dest.write_text(md, encoding="utf-8")
            print(dest)
        except anydoc.NeedsOcrError:
            print(f"docs-to-md: {src}: scanned pages; rerun with --ocr hosted "
                  "only with the professor's consent", file=sys.stderr)
            code = 3
        except (anydoc.ConvertError, OSError) as e:
            print(f"docs-to-md: {src}: {e}", file=sys.stderr)
            code = code or 1  # exit 3 (needs OCR) takes precedence over 1
    return code


if __name__ == "__main__":
    sys.exit(main())
