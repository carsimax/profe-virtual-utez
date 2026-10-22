"""Claude Code hooks for the teaching tree.

Usage: teach-hook <pre|post|stop|session>   (hook JSON on stdin)
pre      PreToolUse Write|Edit|MultiEdit: deny writes under cursos/<periodo>/<curso>/semana-*/ that would break the
         layout (no curso.md, bad week or file name, answer key in alumno/).
post     PostToolUse Write|Edit|MultiEdit|Bash: run svg-check / mermaid-check on the written file, docs-qa on the
         .docx a `docs-build` command wrote; a failing check blocks with the tail of its output.
stop     Stop: run course-lint on the courses with changes in git; errors block the stop (once: stop_hook_active).
session  SessionStart: print each course's curso.md, escala line and [CONFIRMAR] count as context.
Contract: https://code.claude.com/docs/en/hooks. Malformed input or missing fields exit 0 silently (fail open).
"""
import json
import os
import shlex
import subprocess
import sys
import traceback
from pathlib import Path

from cmx_teach.docs.paths import default_docx

from .lint import DECK_RE, FILE_RE, WEEK_RE, lint  # noqa: F401  (DECK_RE: deck dirs are never checked here)

TAIL_LINES = 30
SEPARATORS = {";", "&&", "||", "|", "&"}


def _read():
    try:
        data = json.loads(sys.stdin.read())
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


def _root(data):
    base = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd")
    return Path(base).resolve() if isinstance(base, str) and base else None


def _file(data, root):
    """tool_input.file_path as a project-relative Path (resolved against cwd), or None when outside the project."""
    ti = data.get("tool_input")
    fp = ti.get("file_path") if isinstance(ti, dict) else None
    if not isinstance(fp, str) or not fp or root is None:
        return None
    p = Path(fp)
    if not p.is_absolute():
        p = Path(data.get("cwd") or root) / p
    try:
        return p.resolve().relative_to(root)
    except ValueError:
        return None


def _out(obj):
    print(json.dumps(obj, ensure_ascii=False))


def pre(data):
    root = _root(data)
    rel = _file(data, root)
    if rel is None or len(rel.parts) < 5 or rel.parts[0] != "cursos" or not rel.parts[3].startswith("semana-"):
        return
    course, week = root / Path(*rel.parts[:3]), rel.parts[3]
    why = None
    if not (course / "curso.md").is_file():
        why = f"Falta {Path(*rel.parts[:3])}/curso.md. Créalo antes de escribir materiales (skill curso-nuevo)."
    elif not WEEK_RE.match(week):
        why = f"«{week}» no cumple semana-NN (dos dígitos, p. ej. semana-07). Usa ese nombre de carpeta."
    elif len(rel.parts) == 6 and rel.parts[4] in ("alumno", "docente") and not rel.name.startswith("."):
        if not FILE_RE.match(rel.name):
            why = f"«{rel.name}» no cumple sN-NN-<tipo>-<tema>[_clave].<ext> (minúsculas con guiones). Renombra el archivo."
        elif rel.parts[4] == "alumno" and "_clave." in rel.name:
            why = f"«{rel.name}» es una clave: guárdala en docente/, no en alumno/ (la verían los alumnos)."
    if why:
        _out({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": why}})


def _run(cmd):
    """Run a check; return None when it passes, else a message for Claude (tool output tail or why it did not start)."""
    name = " ".join(cmd)
    try:
        r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    except OSError as e:
        return f"No se pudo ejecutar `{name}`: {e}. Revisa que el entorno uv tenga instalado el proyecto."
    if r.returncode == 0:
        return None
    tail = "\n".join((r.stdout or "").strip().splitlines()[-TAIL_LINES:])
    return f"`{name}` falló (código {r.returncode}). Corrige y vuelve a correrlo:\n{tail}"


def _docs_build_outputs(command, cwd):
    """The .docx files each `docs-build` in a shell command writes (mirrors cmx_teach.docs.build.main)."""
    lex = shlex.shlex(command, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    try:
        tokens = list(lex)
    except ValueError:
        return []
    segs, cur = [], []
    for t in tokens:
        if t in SEPARATORS:
            segs.append(cur)
            cur = []
        else:
            cur.append(t)
    segs.append(cur)
    outs = []
    for seg in segs:
        idx = next((i for i, t in enumerate(seg) if Path(t).name == "docs-build"), None)
        if idx is None:
            continue
        args = seg[idx + 1:]
        key = "--clave" in args or "--key" in args
        pos = [a for a in args if not a.startswith("--")]
        if not pos:
            continue
        spec = Path(cwd, pos[0])
        explicit = len(pos) > 1
        out = pos[1] if explicit else None
        if not out:
            try:
                out = json.loads(spec.read_text(encoding="utf-8")).get("output")
            except (OSError, ValueError, AttributeError):
                out = None
            out = out or str(default_docx(Path(pos[0])))
        if key and not explicit:
            out = out[:-5] + "_clave.docx" if out.lower().endswith(".docx") else out
        outs.append(Path(cwd, out))
    return outs


def post(data):
    root = _root(data)
    tool = data.get("tool_name")
    cmds = []
    if tool == "Bash":
        ti = data.get("tool_input")
        command = ti.get("command") if isinstance(ti, dict) else None
        if isinstance(command, str) and "docs-build" in command:
            cwd = data.get("cwd") or root
            cmds = [["docs-qa", str(f), "--no-render"] for f in _docs_build_outputs(command, cwd) if f.is_file()]
    elif _file(data, root) is not None:
        f = root / _file(data, root)
        tool_for = {".svg": "svg-check", ".mmd": "mermaid-check"}.get(f.suffix.lower())
        if tool_for and f.is_file():
            cmds = [[tool_for, str(f)]]
    problems = [m for m in map(_run, cmds) if m]
    if problems:
        _out({"decision": "block", "reason": "\n\n".join(problems)})


def _changed_courses(root):
    try:
        r = subprocess.run(["git", "status", "--porcelain", "-z", "-uall", "--", "cursos/"], cwd=root,
                           capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return []
    courses, entries = set(), r.stdout.split("\0")
    i = 0
    while i < len(entries):
        e = entries[i]
        i += 1
        if len(e) < 4:
            continue
        paths = [e[3:]]
        if e[0] in "RC" and i < len(entries):  # rename/copy: the next entry is the origin path
            paths.append(entries[i])
            i += 1
        for p in paths:
            parts = Path(p).parts
            if len(parts) >= 3 and parts[0] == "cursos" and (root / Path(*parts[:3])).is_dir():
                courses.add(root / Path(*parts[:3]))
    return sorted(courses)


def stop(data):
    root = _root(data)
    if data.get("stop_hook_active") or root is None:
        return
    courses = _changed_courses(root)
    errors = [f for f in lint(courses) if f["level"] == "error"] if courses else []
    if errors:
        lines = [f"✘ {Path(f['path']).relative_to(root)}: {f['message']}" for f in errors]
        _out({"decision": "block", "reason": "course-lint encontró errores en los cursos modificados. Corrígelos antes de terminar:\n" + "\n".join(lines)})


def session(data):
    root = _root(data)
    curso_mds = sorted(root.glob("cursos/*/*/curso.md")) if root else []
    if not curso_mds:
        print("Cursos: sin cursos todavía; usa /curso-nuevo <slug> <periodo>.")
        return
    lines = ["## Cursos"]
    for md in curso_mds:
        text = md.read_text(encoding="utf-8", errors="replace")
        escala = next((ln.strip() for ln in text.splitlines() if "escala" in ln.lower()), "sin línea de escala")
        lines.append(f"- `{md.relative_to(root).as_posix()}` | {escala} | {text.count('[CONFIRMAR]')} [CONFIRMAR]")
    print("\n".join(lines))


EVENTS = {"pre": pre, "post": post, "stop": stop, "session": session}


def main():
    handler = EVENTS.get(sys.argv[1]) if len(sys.argv) > 1 else None
    if handler is None:
        sys.exit(0)
    try:
        handler(_read())
    except Exception:  # hooks must never break the session  # shortcut: fails open (exit 0) so a broken guard lets edits through, traceback on stderr is the only signal
        traceback.print_exc()
    sys.exit(0)


if __name__ == "__main__":
    main()
