"""Where docs-build/docs-qa put their files.

A spec saved in a `fuentes/` folder builds its .docx one level up, next to the
other class materials; every sidecar (.outline.json, .pages.json, qa/) stays in
`fuentes/` so the week folder only holds the final artifacts.
"""

from pathlib import Path

SOURCES = "fuentes"


def default_docx(spec_path: Path) -> Path:
    spec_path = Path(spec_path)
    folder = spec_path.parent.parent if spec_path.parent.name == SOURCES else spec_path.parent
    return folder / (spec_path.stem + ".docx")


def _sidecar_dir(docx: Path) -> Path:
    docx = Path(docx)
    sources = docx.parent / SOURCES
    return sources if sources.is_dir() else docx.parent


def sidecar(docx: Path, suffix: str) -> Path:
    return _sidecar_dir(docx) / (Path(docx).stem + suffix)


def qa_dir(docx: Path) -> Path:
    return _sidecar_dir(docx) / "qa" / Path(docx).stem
