"""docs-build: python-docx port of docgen.mjs.
Usage: docs-build documento.json [salida.docx] [--clave]"""
import json
import re
import sys
from pathlib import Path

from .docgen import BuildError, build_document, save_deterministic
from .paths import default_docx, sidecar

USAGE = "Uso: docs-build documento.json [salida.docx] [--clave]"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else [str(a) for a in argv]
    key_mode = "--clave" in argv or "--key" in argv
    pos = [a for a in argv if not a.startswith("--")]
    if not pos:
        print(USAGE, file=sys.stderr)
        sys.exit(2)
    spec_path = Path(pos[0])
    out_arg = pos[1] if len(pos) > 1 else None
    try:
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"✘ No se pudo leer {spec_path}: {e}", file=sys.stderr)
        sys.exit(1)
    out = out_arg or spec.get("output") or str(default_docx(spec_path))
    if key_mode:
        spec["_answerKey"] = True
        if not out_arg:
            out = re.sub(r"\.docx$", "_clave.docx", out, flags=re.I)
    pages = sidecar(Path(out), ".pages.json")
    if pages.exists():
        spec["_pages"] = json.loads(pages.read_text(encoding="utf-8"))
    try:
        doc, outline = build_document(spec, spec_path.resolve().parent)
    except BuildError as e:
        print(f"✘ {e}", file=sys.stderr)
        sys.exit(1)
    except (KeyError, IndexError, TypeError, ValueError) as e:  # malformed spec field, not a generator bug
        print(f"✘ Spec inválido: campo faltante o con formato incorrecto ({type(e).__name__}: {e})", file=sys.stderr)
        sys.exit(1)
    sidecar(Path(out), ".outline.json").write_text(json.dumps(outline, ensure_ascii=False, indent=1), encoding="utf-8")
    save_deterministic(doc, out)
    print(f"✔ {out}")
    sys.exit(0)


if __name__ == "__main__":
    main()
