# Formatos oficiales y edición (modos C, D y E)

## Modo C · Formato con etiquetas `{{campo}}`

```bash
uv run docs-fill formato.docx --vars                 # lista los campos
uv run docs-fill formato.docx datos.json salida.docx # llena
```

1. Lista los campos con `--vars` y pide al profesor los que falten.
2. Llena con `datos.json`. Falla si falta un dato o si queda una etiqueta sin resolver.
3. Valida con `uv run docs-qa salida.docx`.

Etiquetas admitidas (docxtpl): `{{campo}}`; `{%p if x %}…{%p endif %}` en su propio párrafo; `{%tr for r in filas %}…{%tr endfor %}` en filas de tabla.

## Modo D · Formato oficial sin etiquetas

- Abre con python-docx y reemplaza los huecos (líneas "_____", "[ ]", celdas vacías) por `{{campos}}` conservando los runs y estilos; guarda como plantilla y sigue el modo C.
- No cambies márgenes, fuentes, encabezados ni pies del formato.
- **Formato largo con estilos propios** (por ejemplo, plantilla de tesis): conserva el archivo como base, borra solo el contenido de ejemplo entre anclas ("Capítulo 1" … "Referencias") y agrega el contenido usando **los nombres de estilo de la plantilla** (resuelve por nombre visible: en Word en español los IDs pueden ser `Ttulo1`). Copia encabezados y pies tal cual.

## Modo E · Editar un .docx existente

- Lee primero: `pandoc documento.docx -t markdown` (y `--track-changes=all` si hay revisiones).
- Cambios de texto simples: python-docx sobre los runs existentes (une runs partidos antes de buscar). No regeneres el documento: perderías el formato del usuario.
- Con control de cambios (`w:ins`/`w:del`) o si piden **cambios rastreados o comentarios**: edita el XML (descomprime el .docx, modifica `word/document.xml`, vuelve a comprimir) con `<w:ins>`/`<w:del>` reales (`w:author`, `w:date`, texto borrado en `<w:delText>`), nunca simulando con colores o tachado. Si el entorno tiene el skill oficial `docx`, úsalo para esta parte.
- Siempre: valida con `uv run docs-qa` y compara el texto antes/después (`pandoc -t plain`) para probar que no se perdió contenido.
