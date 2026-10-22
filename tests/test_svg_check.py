import json

import pytest

from cmx_teach.diagrams.svg_check import main
from conftest import run_main

NS = 'xmlns="http://www.w3.org/2000/svg"'
A11Y = 'role="img" aria-labelledby="t d"'
HEAD = '<title id="t">Titulo</title><desc id="d">Descripcion</desc>'


def svg(body, head=HEAD, attrs=A11Y, viewbox='viewBox="0 0 400 200"'):
    return f'<svg {NS} {viewbox} {attrs}>{head}{body}</svg>'


BOX = '<rect x="20" y="20" width="360" height="160" rx="8" fill="#eeeeee" stroke="#333333"/>'
HELLO = '<text x="200" y="110" text-anchor="middle" font-size="24" fill="#111111">Hola</text>'
CLEAN = svg(BOX + HELLO)


@pytest.fixture
def check(tmp_path, monkeypatch, capsys):
    def run(content, *args, name="a.svg"):
        f = tmp_path / name
        f.write_text(content, encoding="utf-8")
        code = run_main(main, [f, *args], monkeypatch)
        return code, capsys.readouterr().out
    return run


def test_clean_svg_exit_0(chromium, check):
    code, out = check(CLEAN)
    assert code == 0, out
    assert "0 error" in out


def test_invalid_xml_exit_2(check):
    code, out = check("<svg><rect></svg>")
    assert code == 2


def test_missing_viewbox_is_error(chromium, check):
    code, out = check(svg(BOX + HELLO, viewbox=""))
    assert code == 1 and "ERROR viewbox" in out


def test_outside_viewbox_is_error(chromium, check):
    code, out = check(svg('<rect x="380" y="20" width="100" height="50" fill="#333"/>' + HELLO))
    assert code == 1 and "ERROR outside-viewbox" in out


def test_text_overlap_is_error(chromium, check):
    code, out = check(svg(BOX + HELLO + HELLO.replace("Hola", "Chau")))
    assert code == 1 and "ERROR text-overlap" in out


def test_text_overflow_is_error(chromium, check):
    body = '<rect x="20" y="60" width="60" height="60" fill="#eeeeee" stroke="#333"/>' \
           '<text x="30" y="100" font-size="24" fill="#111111">Un texto muy largo</text>'
    code, out = check(svg(body))
    assert code == 1 and "ERROR text-overflow" in out


def test_tiny_font_is_error(chromium, check):
    code, out = check(svg(BOX + HELLO.replace('font-size="24"', 'font-size="2"')))
    assert code == 1 and "ERROR min-font" in out


def test_broken_ref_is_error(chromium, check):
    code, out = check(svg(BOX + HELLO + '<path d="M20 190H380" stroke="#333" marker-end="url(#nope)"/>'))
    assert code == 1 and "ERROR broken-ref" in out


def test_duplicate_id_is_error(chromium, check):
    code, out = check(svg(BOX.replace("<rect", '<rect id="x"') + HELLO.replace("<text", '<text id="x"')))
    assert code == 1 and "ERROR duplicate-id" in out


def test_missing_title_is_warning_only(chromium, check):
    code, out = check(svg(BOX + HELLO, head="", attrs=""))
    assert code == 0 and "WARN a11y-title" in out


def test_json_shape(chromium, check):
    code, out = check(CLEAN, "--json")
    data = json.loads(out)
    assert code == 0 and data["ok"] is True and data["file"].endswith("a.svg")
    s = data["svgs"][0]
    assert s["index"] == 1 and s["errors"] == [] and "minFont" in s["stats"]


def test_render_writes_png(chromium, check, tmp_path):
    png = tmp_path / "out.png"
    code, _ = check(CLEAN, "--render", png)
    assert code == 0 and png.read_bytes()[:4] == b"\x89PNG"


def test_deck_inline_svg_is_checked(chromium, check):
    bad = svg(BOX + HELLO + HELLO.replace("Hola", "Chau"))
    page = f'<!doctype html><body><figure class="fig">{bad}</figure></body>'
    code, out = check(page, name="deck.html")
    assert code == 1 and "svg[1]" in out and "ERROR text-overlap" in out


def test_deck_without_svg_figures_ok(chromium, check):
    code, out = check("<!doctype html><body><p>hola</p></body>", name="deck.html")
    assert code == 0


def test_deck_skips_embedded_mermaid_svg(chromium, check):
    bad = svg(BOX + HELLO + HELLO.replace("Hola", "Chau"))
    page = f'<!doctype html><body><figure class="fig"><div class="mermaid-svg">{bad}</div></figure></body>'
    code, out = check(page, name="deck.html")
    assert code == 0  # Mermaid output is validated by mermaid-check, not svg-check
