"""docgen: JSON spec -> .docx with python-docx + OXML (port of docgen.mjs)."""
from .build import build_document, save_deterministic
from .presets import PRESETS
from .xmlkit import BuildError

__all__ = ["build_document", "save_deterministic", "PRESETS", "BuildError"]
