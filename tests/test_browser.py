import re
from pathlib import Path

from cmx_teach.slides.mermaid import main as mermaid_main
from cmx_teach.slides.qa import main as qa_main
from conftest import run_main


def test_qa_contract(deck, tmp_path, monkeypatch, capsys, chromium):
    out = tmp_path / "qa"
    code = run_main(qa_main, [deck, "--pdf", "--out", out], monkeypatch)
    text = capsys.readouterr().out
    assert code == 1  # the template ships placeholder text, so QA reports PROBLEMAS
    assert "texto de plantilla sin reemplazar" in text
    assert re.search(r"\d+ slides · .* min planeados · \d+ layouts distintos", text)
    assert ("OK: sin desbordes" in text) == (code == 0)
    assert (code == 1) == ("PROBLEMAS (corrige y vuelve a correr):" in text)
    assert "slide-01.png" in {p.name for p in out.iterdir()}
    assert (out / "mobile.png").is_file() and (out / "deck.pdf").is_file()


def test_qa_default_out_is_next_to_deck(deck, tmp_path, monkeypatch, chromium):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    run_main(qa_main, [deck], monkeypatch)
    assert (Path(deck).parent / "qa" / "mobile.png").is_file()
    assert not (elsewhere / "qa").exists()


def test_qa_usage_exit_2(monkeypatch):
    assert run_main(qa_main, [], monkeypatch) == 2


def test_mermaid_no_blocks(tmp_path, monkeypatch, capsys):
    deck = tmp_path / "plain.html"
    deck.write_text("<html><body><p>hola</p></body></html>", encoding="utf-8")
    assert run_main(mermaid_main, [deck], monkeypatch) == 0
    assert "No hay bloques pre.mermaid." in capsys.readouterr().out


def test_mermaid_embeds_svg(deck, monkeypatch, capsys, chromium, online):
    assert '<pre class="mermaid">' in deck.read_text(encoding="utf-8")  # the template ships one
    assert run_main(mermaid_main, [deck], monkeypatch) == 0
    s = deck.read_text(encoding="utf-8")
    assert '<pre class="mermaid">' not in s and '<div class="mermaid-svg"><!--mmd:' in s and "<svg" in s
    assert "diagrama(s) Mermaid incrustados" in capsys.readouterr().out
    assert not list(deck.parent.glob("*.mermaid-tmp.html"))
    # re-runnable
    assert run_main(mermaid_main, [deck], monkeypatch) == 0
