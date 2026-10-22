# Spec JSON y bloques

El documento se describe en un `documento.json` (sin comentarios: el JSON real no los admite). Lo construye `uv run docs-build documento.json`.

## Campos de nivel superior

```json
{
  "preset": "utez",
  "page": "letter",
  "orientation": "portrait",
  "lang": "es-MX",
  "cover": true,
  "numberedHeadings": false,
  "pageFormat": "auto",
  "runningHead": false,
  "header": true, "footer": true,
  "updateFields": false,
  "theme": { "accent": "8B1E3F" },
  "meta": { "...": "ver abajo" },
  "front": [],
  "body": [],
  "back": []
}
```

| Campo | Valores | Notas |
|---|---|---|
| `preset` | `utez` · `apa` · `corporativo` · `tecnico` · `editorial` | Ver `presets.md` |
| `page` | `letter` (Carta, default) · `a4` | |
| `orientation` | `portrait` · `landscape` | `landscape` para tablas anchas o rúbricas con ≥ 5 niveles |
| `lang` | `es-MX` | |
| `cover` | `true` · `"institucional"` · `"apa"` · `false` | Sin `cover` ni `front`, el documento es de una sola sección (oficios, exámenes, prácticas) y el pie muestra "Página N de M" |
| `numberedHeadings` | bool | 1. / 1.1 / 1.1.1; default `true` en `tecnico` |
| `pageFormat` | `auto` · `simple` ("N") · `total` ("Página N de M") | |
| `runningHead` | bool | APA: título corto en el encabezado |
| `header` `footer` | bool | |
| `updateFields` | bool | Fuerza que Word pregunte "¿Deseas actualizar los campos?" al abrir |
| `theme` | `{accent, ...}` | Sobrescribe colores del preset; contraste ≥ 4.5:1 en texto |
| `front` | bloques | Preliminares, numeración romana: resumen, índice, índices de tablas/figuras |
| `body` | bloques | Cuerpo, numeración arábiga desde 1 |
| `back` | bloques | Referencias, anexos, firmas (sigue la numeración del cuerpo) |

### `meta`

```json
{
  "title": "…", "subtitle": "…", "kicker": "Planeación didáctica",
  "institution": "Universidad Tecnológica Emiliano Zapata del Estado de Morelos",
  "department": "División Académica de Tecnologías de la Información y Diseño",
  "logo": "logo.png", "logoHeight": 110,
  "author": "…", "teacher": "…", "course": "…",
  "date": "15 de octubre de 2026", "place": "Emiliano Zapata, Morelos",
  "fields": [["Asignatura", "…"], ["Docente", "…"]],
  "headerText": "Título corto para el encabezado"
}
```

- `kicker` es la categoría ("Planeación didáctica"); no repitas el título.
- `fields` es la tabla de datos de la portada institucional.
- `logo`: solo el archivo que dé el profesor. Nunca lo redibujes ni lo inventes.
- `teacher`/`author`: toma el nombre de "Profesor" en `CLAUDE.md`. Sin dato: `[DATO PENDIENTE]`.

## Bloques

Un bloque es **un string Markdown** o un objeto.

### Markdown

Un string admite: `#`/`##`/`###`, párrafos, listas `-`/`1.` (anidadas con 2 espacios), `- [ ]` casillas, tablas `|…|` (con `:---:` para alinear), bloques de código con triple acento grave, `> cita`, `> [!tip] Título` callout (`info`, `tip`, `warn`, `important`, `example`), `![leyenda](figs/x.png)` figura, `\newpage`, dos espacios al final de línea = salto de línea.

### Bloques tipados

| Bloque | Campos | Notas |
|---|---|---|
| `h1` `h2` `h3` | `text`, `newPage`, `unnumbered` | Títulos con estilo real (entran al índice) |
| `title` | `text` | Título de preliminares que **no** entra al índice (Resumen, Agradecimientos) |
| `p` | `text`, `align` (left/center/right/justify), `style` (lead/small), `noIndent` | `\n` dentro de `text` = salto de línea |
| `bullets` `numbers` `checklist` | `items` (strings u `{text, items}`) | Listas reales con numeración de Word; cada lista reinicia |
| `table` | `headers`, `rows`, `widths` (proporciones), `align` (`l`/`c`/`r`), `style` (banded/lines/grid/apa), `caption`, `source`, `firstColBold` | Leyenda numerada arriba, "Fuente:" abajo; encabezado repetido en cada página |
| `kv` | `rows` `[[etiqueta, valor]]`, `cols` (2 o 4) | Datos generales (asignatura, grupo, horas…) |
| `figure` | `src` (png/jpg/`.mmd`/`.chart.json`), `caption`, `width` (0–1 del ancho útil), `source`, `alt` | Leyenda numerada (APA: arriba). Con `.mmd`/`.chart.json` se usa el PNG generado por `docs-visuals` |
| `callout` | `kind`, `title`, `text` | Caja con barra de color; ≤ 1 cada 2 páginas |
| `code` | `text`, `lang`, `caption` | Monoespaciada sobre gris claro |
| `quote` | `text`, `cite` | Cita en bloque |
| `toc` | `title`, `levels` (1–3), `newPage` | Índice con números de página (2ª pasada) |
| `lot` `lof` | `title`, `newPage` | Índice de tablas / de figuras |
| `references` | `items` (APA en Markdown: `*cursivas*`), `title`, `sort`, `newPage` | Orden alfabético y sangría francesa |
| `questions` | `items`, `instructions`, `studentHeader` (false para omitir), `fields`, `showAnswers`, `showTotal` | Examen; ver "Reactivos" |
| `rubric` | `levels[]`, `criteria [{name, desc, weight, levels[]}]`, `caption` | Rúbrica analítica en tabla; `weight` es texto o número (`"30 %"`) |
| `signatures` | `people [{name, role}]`, `cols` | Bloque de firmas |
| `pagebreak` `spacer` `rule` | `size` | Salto de página, espacio, línea de acento |

## Reactivos (`questions.items`)

```json
{"q": "¿Qué palabra indica herencia en Java?", "points": 2, "options": ["implements", "extends", "super"], "answer": 1}
{"q": "Java permite herencia múltiple de clases.", "points": 1, "kind": "tf", "answer": false}
{"q": "Explica qué es el polimorfismo.", "points": 5, "lines": 4, "answerText": "Respuesta modelo para la clave…"}
{"q": "Observa el diagrama…", "figure": "figs/clases.mmd"}
```

- Opción múltiple: `answer` es el índice desde 0 o la letra (`"b"`).
- Verdadero/falso (`"kind": "tf"`): `answer` es `true`/`false` (o `"V"`/`"F"`).
- Abiertas: `lines` (default 3) y `answerText` (respuesta modelo para la clave).
- `figure`: ruta o `{src, width, alt}`.
- `studentHeader` genera Asignatura/Docente (desde `meta.course`/`meta.teacher`), Nombre, Grupo, Fecha y Calificación. `fields`: `[["Nombre", ""], ["Grupo", "3° A"]]` los sustituye.
- Puntaje por reactivo y total visibles (`showTotal`).

## Clave de respuestas

No dupliques el spec: `uv run docs-build examen.json --clave` genera `examen_clave.docx` con "CLAVE DE RESPUESTAS", la opción correcta marcada, V/F marcado y las respuestas modelo.

## Texto en línea

Válido en cualquier campo de texto: `**negritas**`, `*cursivas*`, `` `código` ``, `[texto](https://…)`, `^[nota al pie]`, `==resaltado==`.

## Datos pendientes

Todo dato que falte va como `[DATO PENDIENTE]`: pasa visible al `.docx`, `docs-qa` lo lista y se reporta al entregar. Dato institucional que el proyecto no confirma: `[CONFIRMAR]` (regla del proyecto).

## Códigos de salida de `docs-build`

0 correcto · 1 error de construcción · 2 uso incorrecto.
