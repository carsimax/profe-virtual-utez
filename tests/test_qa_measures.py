from cmx_teach.slides.qa import main as qa_main
from conftest import TEMPLATE, run_main

MARK = "<!-- ===== SLIDES"
TAIL = '</div>\n</div>\n<div class="hud"'


def slide(layout, body="<h2>Una afirmación concreta</h2><p>Texto real.</p>", extra=""):
    return (f'<section class="slide {layout}" data-id="s" data-chapter="C" data-minutes="1"{extra}>'
            f'<p class="kicker"><span class="n"></span> · C</p>{body}<aside class="notes"><p>n</p></aside></section>\n')


def build(tmp_path, slides, title="Mi deck"):
    """A deck made of the template's head/tail with only the given slides."""
    t = TEMPLATE.read_text(encoding="utf-8").replace("TÍTULO DEL DECK", title)
    head, rest = t.split(MARK, 1)
    tail = rest[rest.index(TAIL):]
    f = tmp_path / "index.html"
    f.write_text(head + MARK + " -->\n" + "".join(slides) + tail, encoding="utf-8")
    return f


def qa(deck, tmp_path, monkeypatch, capsys, *extra):
    code = run_main(qa_main, [deck, "--out", tmp_path / "qa", *extra], monkeypatch)
    return code, capsys.readouterr().out


def test_overflow_px_and_ladder(tmp_path, monkeypatch, capsys, chromium):
    big = "".join(f"<p>Línea {i}</p>" for i in range(40))
    deck = build(tmp_path, [slide("l-split", f'<div class="col"><h2>Título</h2>{big}</div>')])
    code, out = qa(deck, tmp_path, monkeypatch, capsys)
    assert code == 1
    assert "slide desbordada" in out and "px → " in out  # measured px + ladder hint


def test_font_below_24px_is_a_problem(tmp_path, monkeypatch, capsys, chromium):
    small = '<p style="font-size:22px">Texto sustantivo pequeño</p>'
    deck = build(tmp_path, [slide("l-split", f"<h2>Una afirmación</h2>{small}")])
    code, out = qa(deck, tmp_path, monkeypatch, capsys)
    assert code == 1 and "fuente < 24px" in out


def test_font_at_24px_is_accepted(tmp_path, monkeypatch, capsys, chromium):
    ok = '<p style="font-size:24px">Texto en el piso</p>'
    deck = build(tmp_path, [slide("l-split", f"<h2>Una afirmación</h2>{ok}")])
    _, out = qa(deck, tmp_path, monkeypatch, capsys)
    assert "fuente <" not in out


def test_placeholder_text_is_a_problem(tmp_path, monkeypatch, capsys, chromium):
    deck = build(tmp_path, [slide("l-split", "<h2>Lorem ipsum dolor</h2><p>x</p>")])
    code, out = qa(deck, tmp_path, monkeypatch, capsys)
    assert code == 1 and "texto de plantilla sin reemplazar: “Lorem ipsum”" in out


def test_placeholder_title_is_a_problem(tmp_path, monkeypatch, capsys, chromium):
    deck = build(tmp_path, [slide("l-split")], title="TÍTULO DEL DECK")
    code, out = qa(deck, tmp_path, monkeypatch, capsys)
    assert code == 1 and "<title> de plantilla sin reemplazar" in out


def test_minutes_target_warning(tmp_path, monkeypatch, capsys, chromium):
    deck = build(tmp_path, [slide("l-split"), slide("l-grid")])  # 2 planned minutes
    _, out = qa(deck, tmp_path, monkeypatch, capsys, "--minutes", "2")
    assert "minutos planeados 2 > 90 % de 2" in out
    _, out = qa(deck, tmp_path, monkeypatch, capsys, "--minutes", "20")
    assert "minutos planeados" not in out


def test_same_layout_twice_warning(tmp_path, monkeypatch, capsys, chromium):
    deck = build(tmp_path, [slide("l-split"), slide("l-split")])
    _, out = qa(deck, tmp_path, monkeypatch, capsys)
    assert "slides 1–2: mismo layout dos veces seguidas (l-split)" in out


def test_bottom_whitespace_warning(tmp_path, monkeypatch, capsys, chromium):
    deck = build(tmp_path, [slide("l-grid", '<h2 style="align-self:flex-start">Poco contenido arriba</h2>')])
    _, out = qa(deck, tmp_path, monkeypatch, capsys)
    assert "espacio vacío inferior" in out


def test_todo_inside_code_is_not_a_placeholder(tmp_path, monkeypatch, capsys, chromium):
    code_block = '<div class="term"><pre>// TODO: agrega el atributo placa</pre></div>'
    deck = build(tmp_path, [slide("l-code", f"<h2>Completa la clase Taxi</h2>{code_block}")])
    code, out = qa(deck, tmp_path, monkeypatch, capsys)
    assert "texto de plantilla" not in out
