"""Fill an official .docx with {{variable}} tags (docxtpl), failing when data is missing.
Usage: docs-fill plantilla.docx datos.json salida.docx
  --vars   only list the variables the template asks for (to ask the user)
Tags: {{campo}} · {%p if x %}…{%p endif %} (paragraph) · {%tr for r in filas %}…{%tr endfor %} (table row)."""
import json
import re
import sys
import zipfile

from docxtpl import DocxTemplate
from jinja2 import Environment, StrictUndefined


def main():
    a = sys.argv[1:]
    if not a:
        print("Uso: docs-fill plantilla.docx datos.json salida.docx  (o --vars para listar variables)", file=sys.stderr)
        sys.exit(2)
    tpl = DocxTemplate(a[0])
    if "--vars" in a:
        print("\n".join(sorted(tpl.get_undeclared_template_variables())))
        return
    if len(a) < 3:
        print("Uso: docs-fill plantilla.docx datos.json salida.docx", file=sys.stderr)
        sys.exit(2)
    with open(a[1], encoding="utf-8") as f:
        ctx = json.load(f)
    missing = sorted(tpl.get_undeclared_template_variables(context=ctx))
    if missing:
        sys.exit("Faltan datos para: " + ", ".join(missing))
    tpl.render(ctx, jinja_env=Environment(undefined=StrictUndefined), autoescape=True)
    tpl.save(a[2])
    left = set()
    with zipfile.ZipFile(a[2]) as z:
        for n in z.namelist():
            if n.startswith("word/") and n.endswith(".xml"):
                left |= set(re.findall(r"\{\{[^}]*\}\}|\{%[^%]*%\}", re.sub(r"<[^>]+>", "", z.read(n).decode("utf8"))))
    if left:
        sys.exit("Quedaron etiquetas sin procesar: " + ", ".join(sorted(left)))
    print(f"✔ {a[2]}")


if __name__ == "__main__":
    main()
