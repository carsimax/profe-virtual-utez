import json

from cmx_teach.course.lint import DECK_RE, FILE_RE, WEEK_RE, lint, main
from conftest import run_main

UNIT = """## Unidad 1 Fundamentos

| Saber | Instrumento | Peso |
|---|---|---|
| Saber | Examen | 30% |
| Saber hacer | Práctica | 50 |
| Saber ser y convivir | Guía de observación | 20% |
"""


def make_course(tmp_path, curso_md=UNIT, weeks=("semana-01",)):
    course = tmp_path / "cursos" / "2026-3" / "movil-7"
    for w in weeks:
        (course / w / "alumno").mkdir(parents=True)
        (course / w / "docente").mkdir()
    if curso_md is not None:
        (course / "curso.md").write_text(curso_md, encoding="utf-8")
    return course


def touch(path, text=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def messages(findings, level="error"):
    return [f["message"] for f in findings if f["level"] == level]


def test_clean_course_has_no_findings(tmp_path):
    course = make_course(tmp_path)
    wk = course / "semana-01"
    touch(wk / "alumno" / "s1-03-practica-1-matriz.docx")
    touch(wk / "docente" / "s1-03-practica-1-matriz_clave.docx")
    touch(wk / "alumno" / ".DS_Store")
    (wk / "alumno" / "00-presentacion").mkdir()
    touch(wk / "alumno" / "00-presentacion" / "Cualquier Nombre.html")
    (wk / "alumno" / "s2-00-presentacion-git-basico").mkdir()
    touch(wk / "00-plan.md", "[a](alumno/s1-03-practica-1-matriz.docx#x) [w](https://x.mx) [m](mailto:a@b) [f](#top)")
    assert lint([tmp_path / "cursos"]) == []


def test_a_missing_curso_md(tmp_path):
    course = make_course(tmp_path, curso_md=None)
    f = lint([course])
    assert len(messages(f)) == 1 and "curso.md" in messages(f)[0]
    assert f[0]["path"] == str(course)


def test_b_week_name(tmp_path):
    course = make_course(tmp_path, weeks=("semana-01", "semana-7"))
    msgs = messages(lint([course]))
    assert len(msgs) == 1 and "semana-7" in msgs[0]
    assert WEEK_RE.match("semana-07") and not WEEK_RE.match("semana-007")


def test_c_file_and_dir_names(tmp_path):
    wk = make_course(tmp_path) / "semana-01"
    touch(wk / "alumno" / "Practica 1.docx")
    touch(wk / "docente" / "s1-3-guia.md")
    (wk / "alumno" / "presentacion").mkdir()
    (wk / "alumno" / "00-presentacion").mkdir()
    f = lint([wk])
    paths = sorted(x["path"].rsplit("/", 1)[1] for x in f if x["level"] == "error")
    assert paths == ["Practica 1.docx", "presentacion", "s1-3-guia.md"]
    assert FILE_RE.match("s1-03-examen-ordinario_clave.docx")
    assert not FILE_RE.match("s1-03-Examen.docx")
    assert DECK_RE.match("s1-00-presentacion-git") and DECK_RE.match("00-presentacion")


def test_word_lock_files_are_ignored(tmp_path):
    wk = make_course(tmp_path) / "semana-01"
    touch(wk / "alumno" / "~$-01-practica-monorepo-con-arnes.docx")
    touch(wk / "docente" / "~$-01-guia.docx")
    assert messages(lint([wk])) == []


def test_d_clave_in_alumno(tmp_path):
    wk = make_course(tmp_path) / "semana-01"
    touch(wk / "alumno" / "s1-01-tarea-x_clave.docx")
    touch(wk / "docente" / "s1-01-tarea-x_clave.docx")
    msgs = messages(lint([wk]))
    assert len(msgs) == 1 and "clave" in msgs[0] and "alumno" in msgs[0]


def test_e_missing_key(tmp_path):
    wk = make_course(tmp_path) / "semana-01"
    for kind in ("practica", "tarea", "examen", "quiz"):
        touch(wk / "alumno" / f"s1-01-{kind}-uno.docx")
    touch(wk / "alumno" / "s1-02-guia-lectura.docx")  # no keyword: no key needed
    touch(wk / "docente" / "s1-01-quiz-uno_clave.md")  # any extension
    msgs = messages(lint([wk]))
    assert len(msgs) == 3 and not any("quiz" in m for m in msgs)


def test_f_docx_in_week_root(tmp_path):
    wk = make_course(tmp_path) / "semana-01"
    touch(wk / "s1-01-tarea-x.docx")
    msgs = messages(lint([wk]))
    assert len(msgs) == 1 and "alumno/" in msgs[0]


def test_g_broken_plan_link(tmp_path):
    wk = make_course(tmp_path) / "semana-01"
    touch(wk / "alumno" / "s1-02-guia.md")
    touch(wk / "00-plan.md", "[ok](alumno/s1-02-guia.md#sec) [mal](alumno/no-existe.docx)")
    msgs = messages(lint([wk]))
    assert len(msgs) == 1 and "no-existe.docx" in msgs[0]


def test_h_unit_table_sum(tmp_path):
    bad = UNIT.replace("| 20% |", "| 25% |") + "\n## Unidad 2 Otra\n\nSin tabla.\n"
    course = make_course(tmp_path, curso_md=bad)
    msgs = messages(lint([course]))
    assert len(msgs) == 2
    assert any("105" in m for m in msgs) and any("Unidad 2" in m for m in msgs)


def test_h_missing_saber_row(tmp_path):
    course = make_course(tmp_path, curso_md="### Unidad 1\n\n| Saber | Peso |\n|---|---|\n| Saber | 100 |\n")
    assert len(messages(lint([course]))) == 1


def test_warning_confirmar_count(tmp_path):
    course = make_course(tmp_path, curso_md=UNIT + "\n[CONFIRMAR] fecha, [CONFIRMAR] escala\n")
    f = lint([course])
    assert messages(f) == [] and len(messages(f, "warning")) == 1
    assert "2" in messages(f, "warning")[0]


def test_default_path_is_cursos_under_cwd(tmp_path, monkeypatch, capsys):
    make_course(tmp_path, curso_md=None)
    monkeypatch.chdir(tmp_path)
    assert run_main(main, [], monkeypatch) == 1
    out = capsys.readouterr().out
    assert "✘" in out and "curso.md" in out and "1 error(es)" in out


def test_cli_exit_codes_and_json(tmp_path, monkeypatch, capsys):
    course = make_course(tmp_path, curso_md=UNIT + "[CONFIRMAR]\n")
    assert run_main(main, [course], monkeypatch) == 0
    out = capsys.readouterr().out
    assert "⚠" in out and "0 error(es), 1 aviso(s)" in out
    assert run_main(main, [tmp_path / "nope"], monkeypatch) == 2
    assert capsys.readouterr().err.strip() != ""
    (course / "curso.md").unlink()
    assert run_main(main, [course, "--json"], monkeypatch) == 1
    data = json.loads(capsys.readouterr().out)
    assert data[0].keys() == {"level", "path", "message"}
