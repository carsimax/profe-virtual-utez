import io
import json
import subprocess
import sys

import pytest

from cmx_teach.course import hooks
from conftest import run_main


def call(event, payload, monkeypatch, capsys, project=None, raw=None):
    """Run `teach-hook <event>` with a JSON payload on stdin; return (exit code, stdout)."""
    monkeypatch.setattr(sys, "stdin", io.StringIO(raw if raw is not None else json.dumps(payload)))
    if project is not None:
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project))
    code = run_main(hooks.main, [event], monkeypatch)
    return code, capsys.readouterr().out


def course(tmp_path, curso_md=True):
    c = tmp_path / "cursos" / "2026-sep-dic" / "formulacion-7"
    (c / "semana-01" / "alumno").mkdir(parents=True)
    (c / "semana-01" / "docente").mkdir()
    if curso_md:
        (c / "curso.md").write_text("# Curso\n\n**Escala:** A (NA/R/B/A/E) [CONFIRMAR]\n", encoding="utf-8")
    return c


def pre(path, tmp_path, monkeypatch, capsys, tool="Write"):
    return call("pre", {"tool_name": tool, "tool_input": {"file_path": str(path)}, "cwd": str(tmp_path)}, monkeypatch, capsys, tmp_path)


def reason(out):
    d = json.loads(out)["hookSpecificOutput"]
    assert d["hookEventName"] == "PreToolUse" and d["permissionDecision"] == "deny"
    return d["permissionDecisionReason"]


def test_pre_denies_missing_curso_md(tmp_path, monkeypatch, capsys):
    c = course(tmp_path, curso_md=False)
    code, out = pre(c / "semana-01/alumno/s1-01-practica-x.docx", tmp_path, monkeypatch, capsys)
    assert code == 0 and "curso.md" in reason(out)


def test_pre_denies_bad_week_name(tmp_path, monkeypatch, capsys):
    c = course(tmp_path)
    code, out = pre(c / "semana-7/alumno/s1-01-practica-x.docx", tmp_path, monkeypatch, capsys)
    assert "semana-NN" in reason(out)


def test_pre_denies_bad_file_name_and_exposed_key(tmp_path, monkeypatch, capsys):
    c = course(tmp_path)
    _, out = pre(c / "semana-01/docente/Examen Final.docx", tmp_path, monkeypatch, capsys, "Edit")
    assert "sN-NN" in reason(out)
    _, out = pre(c / "semana-01/alumno/s1-01-examen-x_clave.docx", tmp_path, monkeypatch, capsys, "MultiEdit")
    assert "docente/" in reason(out)


def test_pre_silent_paths(tmp_path, monkeypatch, capsys):
    c = course(tmp_path)
    for p in [c / "semana-01/alumno/s1-01-practica-x.docx", c / "semana-01/00-plan.md",
              c / "semana-01/alumno/00-presentacion/index.html", c / "semana-01/alumno/s1-00-presentacion-git/Raro Nombre.html",
              c / "semana-01/fuentes/Mi Spec.json", c / "semana-01/alumno/.keep", tmp_path / "README.md",
              tmp_path.parent / "fuera/cursos/p/c/semana-1/alumno/X.docx"]:
        assert pre(p, tmp_path, monkeypatch, capsys) == (0, ""), p


@pytest.mark.parametrize("raw", ["", "not json", "[]", '{"tool_input": 3}', '{"tool_name":"Write"}'])
def test_hooks_fail_open_on_bad_input(raw, tmp_path, monkeypatch, capsys):
    for event in ("pre", "post", "stop"):
        assert call(event, None, monkeypatch, capsys, tmp_path, raw=raw) == (0, "")


def test_unknown_event_is_silent(tmp_path, monkeypatch, capsys):
    assert call("nope", {}, monkeypatch, capsys, tmp_path) == (0, "")


class Run:
    """Records subprocess.run calls; answers with a canned (returncode, output)."""

    def __init__(self, rc=0, out="", exc=None):
        self.calls, self.rc, self.out, self.exc = [], rc, out, exc

    def __call__(self, cmd, **kw):
        self.calls.append(cmd)
        if self.exc:
            raise self.exc
        return subprocess.CompletedProcess(cmd, self.rc, stdout=self.out, stderr="")


def post(tool, tool_input, tmp_path, monkeypatch, capsys):
    return call("post", {"tool_name": tool, "tool_input": tool_input, "cwd": str(tmp_path)}, monkeypatch, capsys, tmp_path)


def test_post_runs_svg_and_mermaid_checks(tmp_path, monkeypatch, capsys):
    run = Run()
    monkeypatch.setattr(subprocess, "run", run)
    (tmp_path / "a.svg").write_text("<svg/>")
    (tmp_path / "b.mmd").write_text("graph TD")
    assert post("Write", {"file_path": str(tmp_path / "a.svg")}, tmp_path, monkeypatch, capsys) == (0, "")
    assert post("Edit", {"file_path": str(tmp_path / "b.mmd")}, tmp_path, monkeypatch, capsys) == (0, "")
    assert run.calls == [["svg-check", str(tmp_path / "a.svg")], ["mermaid-check", str(tmp_path / "b.mmd")]]


def test_post_blocks_with_tail_of_output(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(subprocess, "run", Run(1, "\n".join(f"l{i}" for i in range(100))))
    (tmp_path / "a.svg").write_text("<svg/>")
    _, out = post("Write", {"file_path": str(tmp_path / "a.svg")}, tmp_path, monkeypatch, capsys)
    d = json.loads(out)
    assert d["decision"] == "block" and "l99" in d["reason"] and "l0\n" not in d["reason"] and "svg-check" in d["reason"]


def test_post_tool_that_cannot_start_is_reported(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(subprocess, "run", Run(exc=FileNotFoundError("svg-check")))
    (tmp_path / "a.svg").write_text("<svg/>")
    _, out = post("Write", {"file_path": str(tmp_path / "a.svg")}, tmp_path, monkeypatch, capsys)
    assert json.loads(out)["decision"] == "block" and "svg-check" in json.loads(out)["reason"]


def test_post_ignores_other_files_and_missing_file(tmp_path, monkeypatch, capsys):
    run = Run()
    monkeypatch.setattr(subprocess, "run", run)
    assert post("Write", {"file_path": str(tmp_path / "a.md")}, tmp_path, monkeypatch, capsys) == (0, "")
    assert post("Write", {"file_path": str(tmp_path / "gone.svg")}, tmp_path, monkeypatch, capsys) == (0, "")
    assert post("Bash", {"command": "ls -la"}, tmp_path, monkeypatch, capsys) == (0, "")
    assert run.calls == []


def docx_targets(tmp_path, monkeypatch, capsys, command, files, rc=0):
    run = Run(rc, "PROBLEMAS: x")
    monkeypatch.setattr(subprocess, "run", run)
    for f in files:
        f = tmp_path / f
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(b"x")
    out = post("Bash", {"command": command}, tmp_path, monkeypatch, capsys)
    return run.calls, out


def test_post_docs_build_default_output(tmp_path, monkeypatch, capsys):
    calls, out = docx_targets(tmp_path, monkeypatch, capsys, "uv run docs-build semana-01/fuentes/s1-01-x.json",
                              ["semana-01/s1-01-x.docx"])
    assert calls == [["docs-qa", str(tmp_path / "semana-01/s1-01-x.docx"), "--no-render"]] and out == (0, "")


def test_post_docs_build_clave_and_explicit_output(tmp_path, monkeypatch, capsys):
    # --clave without an output arg writes only <x>_clave.docx
    calls, _ = docx_targets(tmp_path, monkeypatch, capsys, "uv run docs-build fuentes/x.json --clave; echo ok",
                            ["x_clave.docx", "x.docx"])
    assert [c[1] for c in calls] == [str(tmp_path / "x_clave.docx")]
    # an explicit output arg is used verbatim, even with --clave
    calls, _ = docx_targets(tmp_path, monkeypatch, capsys, "docs-build s.json out/final.docx --clave", ["out/final.docx"])
    assert [c[1] for c in calls] == [str(tmp_path / "out/final.docx")]


def test_post_docs_build_spec_output_field_and_block(tmp_path, monkeypatch, capsys):
    (tmp_path / "s.json").write_text(json.dumps({"output": "elegido.docx"}))
    calls, (code, out) = docx_targets(tmp_path, monkeypatch, capsys, "docs-build s.json", ["elegido.docx"], rc=1)
    assert [c[1] for c in calls] == [str(tmp_path / "elegido.docx")]
    assert json.loads(out)["decision"] == "block" and "PROBLEMAS" in json.loads(out)["reason"]


def test_post_docs_build_without_docx_is_silent(tmp_path, monkeypatch, capsys):
    calls, out = docx_targets(tmp_path, monkeypatch, capsys, "docs-build s.json", [])
    assert calls == [] and out == (0, "")


def git(cwd, *a):
    subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True,
                   env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t", "PATH": "/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin", "HOME": str(cwd)})


def stop(tmp_path, monkeypatch, capsys, **extra):
    return call("stop", {"cwd": str(tmp_path), **extra}, monkeypatch, capsys, tmp_path)


def test_stop_blocks_on_lint_errors_in_changed_course(tmp_path, monkeypatch, capsys):
    git(tmp_path, "init", "-q")
    c = course(tmp_path)
    (c / "semana-01/alumno/s1-01-examen-x.docx").write_bytes(b"x")  # no _clave
    code, out = stop(tmp_path, monkeypatch, capsys)
    d = json.loads(out)
    assert code == 0 and d["decision"] == "block" and "_clave" in d["reason"] and "s1-01-examen-x.docx" in d["reason"]


def test_stop_silent_cases(tmp_path, monkeypatch, capsys):
    assert stop(tmp_path, monkeypatch, capsys) == (0, "")  # not a git repo
    git(tmp_path, "init", "-q")
    assert stop(tmp_path, monkeypatch, capsys) == (0, "")  # no changes
    c = course(tmp_path)
    (c / "semana-01/alumno/s1-01-examen-x.docx").write_bytes(b"x")
    assert stop(tmp_path, monkeypatch, capsys, stop_hook_active=True) == (0, "")  # already continuing
    (c / "semana-01/docente").joinpath("s1-01-examen-x_clave.docx").write_bytes(b"x")
    assert stop(tmp_path, monkeypatch, capsys) == (0, "")  # clean (warnings do not block)


def test_stop_handles_non_ascii_paths(tmp_path, monkeypatch, capsys):
    git(tmp_path, "init", "-q")
    c = tmp_path / "cursos/2026-sep-dic/programación-7/semana-01/alumno"
    c.mkdir(parents=True)
    (c / "Mal Nombre.docx").write_bytes(b"x")
    _, out = stop(tmp_path, monkeypatch, capsys)
    assert json.loads(out)["decision"] == "block"


def test_session_lists_courses(tmp_path, monkeypatch, capsys):
    course(tmp_path)
    code, out = call("session", {"cwd": str(tmp_path)}, monkeypatch, capsys, tmp_path)
    assert code == 0 and "cursos/2026-sep-dic/formulacion-7/curso.md" in out
    assert "A (NA/R/B/A/E)" in out and "1 [CONFIRMAR]" in out


def test_session_without_courses_and_fallback_to_cwd(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    code, out = call("session", {"cwd": str(tmp_path)}, monkeypatch, capsys)
    assert code == 0 and "sin cursos" in out and out.count("\n") == 1
    course(tmp_path, curso_md=False)  # course dir without curso.md: still no courses listed
    assert "sin cursos" in call("session", {"cwd": str(tmp_path)}, monkeypatch, capsys)[1]


def test_handler_exception_fails_open_but_reports_to_stderr(tmp_path, monkeypatch, capsys):
    def boom(_payload):
        raise RuntimeError("guard broke")

    monkeypatch.setitem(hooks.EVENTS, "pre", boom)
    monkeypatch.setattr(sys, "stdin", io.StringIO("{}"))
    assert run_main(hooks.main, ["pre"], monkeypatch) == 0
    assert "guard broke" in capsys.readouterr().err
