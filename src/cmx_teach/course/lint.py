"""Lint the teaching tree: cursos/<periodo>/<curso>/semana-NN/{alumno,docente}.

Usage: course-lint [PATH ...] [--json]
PATH is the cursos/ root, a course dir (cursos/<periodo>/<curso>/) or a week dir; default: cursos/ under cwd.
Exit codes: 0 ok (warnings allowed), 1 errors found, 2 path missing / unreadable.

Errors: (a) course with weeks but no curso.md; (b) week dir not semana-NN; (c) file or deck dir names in
alumno/ and docente/; (d) a _clave file in alumno/; (e) practica/tarea/examen/quiz without its _clave in docente/;
(f) .docx left in the week folder; (g) broken relative link in 00-plan.md; (h) curso.md unit without a
Saber / Saber hacer / Saber ser table whose weights sum 100.
Warning: [CONFIRMAR] markers per .md file.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

WEEK_RE = re.compile(r"^semana-\d{2}$")
FILE_RE = re.compile(r"^s\d+-\d{2}-[a-z0-9]+(-[a-z0-9]+)*(_clave)?\.[a-z0-9]+$")
DECK_RE = re.compile(r"^(00-presentacion|s\d+-00-presentacion-[a-z0-9]+(-[a-z0-9]+)*)$")
KEYED = ("practica", "tarea", "examen", "quiz")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)")
UNIT_RE = re.compile(r"^(#{1,6})\s+Unidad\b", re.M)
HEADING_RE = re.compile(r"^(#{1,6})\s", re.M)


def _f(level, path, message):
    return {"level": level, "path": str(path), "message": message}


def _children(d):
    return sorted(d.iterdir()) if d.is_dir() else []


def _weight(cells):
    """Last numeric cell of a table row (a % suffix is allowed), or None."""
    for c in reversed(cells):
        try:
            return float(c.strip().rstrip("%").strip())
        except ValueError:
            continue
    return None


def _check_unit(name, text, path):
    kinds = {}
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        first, w = cells[0].lower(), _weight(cells[1:])
        kind = "hacer" if first == "saber hacer" else "ser" if first.startswith("saber ser") else "saber" if first == "saber" else None
        if kind and w is not None:
            kinds[kind] = w
    if len(kinds) < 3:
        return [_f("error", path, f"«{name}» necesita una tabla con filas Saber, Saber hacer y Saber ser y convivir con su peso (%).")]
    total = sum(kinds.values())
    if abs(total - 100) > 1e-9:
        return [_f("error", path, f"«{name}»: las ponderaciones de los tres saberes suman {total:g}, deben sumar 100.")]
    return []


def _check_curso_md(path):
    text = path.read_text(encoding="utf-8")
    out = []
    for m in UNIT_RE.finditer(text):
        end = next((h.start() for h in HEADING_RE.finditer(text, m.end()) if len(h.group(1)) <= len(m.group(1))), len(text))
        out += _check_unit(text[m.start():end].splitlines()[0].lstrip("# ").strip(), text[m.end():end], path)
    return out


def _check_week(week):
    out = []
    if not WEEK_RE.match(week.name):
        out.append(_f("error", week, f"«{week.name}» no cumple semana-NN (dos dígitos, p. ej. semana-07)."))
    docente = week / "docente"
    for f in _children(week):
        if f.is_file() and f.suffix == ".docx":
            out.append(_f("error", f, "documento .docx suelto en la semana: muévelo a alumno/ o docente/."))
    for sub in ("alumno", "docente"):
        for f in _children(week / sub):
            if f.name.startswith((".", "~$")):  # dotfiles and Word lock files
                continue
            if f.is_dir():
                if sub == "alumno" and not DECK_RE.match(f.name):
                    out.append(_f("error", f, "carpeta de deck inválida: usa 00-presentacion o sN-00-presentacion-<tema>."))
            elif not FILE_RE.match(f.name):
                out.append(_f("error", f, "nombre inválido: usa sN-NN-<tipo>-<tema>[_clave].<ext> en minúsculas con guiones."))
            elif sub == "alumno" and f.stem.endswith("_clave"):
                out.append(_f("error", f, "clave expuesta a los alumnos: muévela a docente/."))
            elif sub == "alumno" and any(k in f.name for k in KEYED):
                if not any(c.name.startswith(f.stem + "_clave.") for c in _children(docente)):
                    out.append(_f("error", f, f"falta docente/{f.stem}_clave.<ext>."))
    plan = week / "00-plan.md"
    if plan.is_file():
        for target in LINK_RE.findall(plan.read_text(encoding="utf-8")):
            t = unquote(target.split("#")[0])
            if t and not re.match(r"(https?:|mailto:)", t) and not (week / t).exists():
                out.append(_f("error", plan, f"enlace roto: {target}"))
    return out


def _check_course(course, weeks):
    out = []
    curso_md = course / "curso.md"
    if weeks and not curso_md.is_file():
        out.append(_f("error", course, "falta curso.md (créalo antes de planear semanas)."))
    if curso_md.is_file():
        out += _check_curso_md(curso_md)
    for w in weeks:
        out += _check_week(w)
    for md in sorted(course.rglob("*.md")):
        n = md.read_text(encoding="utf-8").count("[CONFIRMAR]")
        if n:
            out.append(_f("warning", md, f"{n} marcador(es) [CONFIRMAR] pendientes."))
    return out


def _weeks(course):
    return [d for d in _children(course) if d.is_dir() and d.name.startswith("semana-")]


def lint(paths):
    """Lint cursos/ roots, course dirs or week dirs; return findings as {level, path, message} dicts."""
    out = []
    for p in map(Path, paths):
        if not p.is_dir():
            raise FileNotFoundError(f"no existe o no es carpeta: {p}")
        if p.name.startswith("semana-"):
            out += _check_week(p)
        elif (p / "curso.md").is_file() or _weeks(p):
            out += _check_course(p, _weeks(p))
        else:  # cursos/ root: <periodo>/<curso>
            for course in (c for per in _children(p) for c in _children(per) if c.is_dir()):
                out += _check_course(course, _weeks(course))
    return out


def main():
    ap = argparse.ArgumentParser(prog="course-lint", description="Verifica la estructura de cursos/ (nombres, claves, enlaces, ponderaciones).")
    ap.add_argument("paths", nargs="*", default=["cursos"], metavar="PATH", help="cursos/, una carpeta de curso o de semana (por defecto cursos/)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        findings = lint(a.paths)
    except OSError as e:
        print(f"ERROR input {e}", file=sys.stderr)
        sys.exit(2)
    nerr = sum(f["level"] == "error" for f in findings)
    nwarn = len(findings) - nerr
    if a.json:
        print(json.dumps(findings, ensure_ascii=False))
    else:
        for f in findings:
            print(f"{'✘' if f['level'] == 'error' else '⚠'} {f['path']}: {f['message']}")
        print(f"{nerr} error(es), {nwarn} aviso(s)")
    sys.exit(1 if nerr else 0)


if __name__ == "__main__":
    main()
