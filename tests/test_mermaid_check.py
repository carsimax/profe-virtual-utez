import json

import pytest

from cmx_teach.diagrams.mermaid_check import main
from conftest import run_main

GOOD = """flowchart LR
  accTitle: Login flow
  accDescr: A request is validated and leads to the dashboard or an error.
  A["Request"] --> B{"Valid?"}
  B -- yes --> C[Dashboard]
  B -- no --> D[Error]
"""


def mmd(tmp_path, text, name="d.mmd"):
    f = tmp_path / name
    f.write_text(text, encoding="utf-8")
    return f


def test_no_diagrams_exit_2(tmp_path, monkeypatch):
    f = mmd(tmp_path, "<html><body>nothing</body></html>", "empty.html")
    assert run_main(main, [f], monkeypatch) == 2


def test_missing_file_exit_2(tmp_path, monkeypatch):
    assert run_main(main, [tmp_path / "nope.mmd"], monkeypatch) == 2


def test_valid_flowchart_ok(tmp_path, monkeypatch, capsys, chromium, online):
    assert run_main(main, [mmd(tmp_path, GOOD)], monkeypatch) == 0
    assert "0 error(s), 0 warning(s)" in capsys.readouterr().out


def test_syntax_error(tmp_path, monkeypatch, capsys, chromium, online):
    assert run_main(main, [mmd(tmp_path, "flowchart LR\n  A --> \n  B[[[\n")], monkeypatch) == 1
    assert "ERROR 1 parse" in capsys.readouterr().out


def test_unsupported_type_message(tmp_path, monkeypatch, capsys, chromium, online):
    assert run_main(main, [mmd(tmp_path, "radar-beta\n  axis a, b\n")], monkeypatch) == 1
    assert "unsupported-type" in capsys.readouterr().out


def test_missing_acc_is_warning_only(tmp_path, monkeypatch, capsys, chromium, online):
    assert run_main(main, [mmd(tmp_path, "flowchart LR\n  A --> B\n")], monkeypatch) == 0
    out = capsys.readouterr().out
    assert "WARN 1 a11y-title" in out and "WARN 1 a11y-descr" in out


def test_lowercase_end_warns(tmp_path, monkeypatch, capsys, chromium, online):
    run_main(main, [mmd(tmp_path, "flowchart LR\n  A --> end\n")], monkeypatch)
    assert "lowercase-end" in capsys.readouterr().out


def test_deck_pre_mermaid_checked(tmp_path, monkeypatch, capsys, chromium, online):
    html = f'<!doctype html><html><head><style>:root{{--bg:#06182f}}</style></head><body><pre class="mermaid">{GOOD}</pre></body></html>'
    assert run_main(main, [mmd(tmp_path, html, "deck.html"), "--json"], monkeypatch) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["ok"] is True and len(data["diagrams"]) == 1


def test_json_shape_and_render(tmp_path, monkeypatch, capsys, chromium, online):
    out = tmp_path / "png"
    assert run_main(main, [mmd(tmp_path, GOOD), "--json", "--render", out], monkeypatch) == 0
    data = json.loads(capsys.readouterr().out)
    d = data["diagrams"][0]
    assert set(data) == {"file", "ok", "diagrams"} and set(d) == {"index", "type", "errors", "warnings", "stats"}
    assert d["stats"]["nodes"] == 4
    assert (out / "diagram-01.png").stat().st_size > 1000
