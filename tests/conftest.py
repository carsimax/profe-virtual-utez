import shutil
import socket
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / ".claude/skills/html-slides/assets/template.html"


def run_main(main, argv, monkeypatch):
    """Call a console-script main() as the CLI would; return its exit code."""
    monkeypatch.setattr(sys, "argv", ["prog", *map(str, argv)])
    try:
        main()
    except SystemExit as e:
        return e.code or 0
    return 0


@pytest.fixture
def deck(tmp_path):
    """A copy of the deck template (assets/template.html) at tmp_path/index.html."""
    f = tmp_path / "index.html"
    shutil.copy(TEMPLATE, f)
    return f


@pytest.fixture(scope="session")
def chromium():
    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as p:
            p.chromium.launch().close()
    except Exception as e:
        pytest.skip(f"Chromium unavailable: {e}")


@pytest.fixture(scope="session")
def online():
    try:
        socket.create_connection(("cdn.jsdelivr.net", 443), timeout=3).close()
    except OSError:
        pytest.skip("no network (Mermaid loads from the CDN)")
