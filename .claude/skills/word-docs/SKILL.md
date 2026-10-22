---
name: word-docs
description: Crea documentos Word (.docx) profesionales desde un spec JSON con bloques Markdown - planeaciones, exámenes, rúbricas, reportes, SRS, oficios, minutas, tesis APA 7 - con presets UTEZ, índices, gráficas y Mermaid. Usar al pedir un Word, .docx, documento, planeación, examen, rúbrica, reporte, SRS, oficio, minuta o tesis APA, o al llenar o editar un .docx existente.
---

# Word Docs

Genera `.docx` profesionales sin pelear con OOXML: el modelo escribe un **spec JSON** (con bloques Markdown) y `uv run docs-build` resuelve lo difícil: estilos con jerarquía real, índice e índices de tablas y figuras con números de página, leyendas numeradas con campos SEQ, portada institucional, numeración romana/arábiga por sección, encabezado con logo, notas al pie, listas reales, tablas con anchos correctos, callouts, código, preguntas de examen, rúbricas, firmas y referencias APA con sangría francesa.

Fusiona prácticas del skill oficial `docx` de Anthropic, minimax-docx (recetas tipográficas, gate-checks), kimi-docx (gráficas, completitud por escenario), officecli-docx (delivery gate, revisión visual), scholar-thesis-docx (auditoría académica) y docx-contracts (plantillas estrictas).

**Cómo usar este archivo:** aquí viven el flujo y las reglas. El detalle se carga por fase desde `references/` (tabla de abajo). Los scripts son comandos `uv run docs-*` del paquete Python del repo.

| Archivo | Para qué | Cuándo leerlo |
|---|---|---|
| `references/spec.md` | Campos del spec, todos los bloques, reactivos, texto en línea, clave de respuestas | Fase 3, al escribir el spec |
| `references/presets.md` | Los 5 presets (fuentes, colores), defaults y logo | Fase 1 y 3, al elegir el estilo |
| `references/recetas.md` | Estructura por tipo de documento y completitud por escenario | Fase 2, al planear |
| `references/formatos-y-edicion.md` | Llenar formatos oficiales (modos C/D) y editar un .docx existente (modo E) | Modos C, D y E |
| `references/reglas-tecnicas.md` | Reglas de python-docx/OXML del generador | Solo si modificas `src/cmx_teach/docs/` |
| `examples/*.json` | Specs de referencia: `planeacion`, `examen`, `apa`, `oficio`, `srs` | Fase 3, como modelo |
| `examples/figs/` | Fuentes de figuras: `herencia.mmd`, `avance.chart.json`, `evaluacion.chart.json` | Fase 4, como modelo |
| skill `mermaid-diagrams` | Sintaxis y validación de diagramas Mermaid | Fase 4, al crear un `.mmd` |

**Principio rector:** el modelo decide *contenido y estructura*; `docs-build` decide *formato*. No escribas XML ni python-docx a mano para documentos nuevos: escribe el spec. Si algo no se puede expresar con los bloques, agrega un bloque nuevo al generador respetando `references/reglas-tecnicas.md`.

## Comandos

Instalación, una sola vez: `uv sync` y `uv run playwright install chromium` (solo para diagramas y gráficas). Para el render de revisión: LibreOffice y poppler (`brew install --cask libreoffice && brew install poppler`). Para el modo E: pandoc.

```bash
uv run docs-build SPEC.json [OUT.docx] [--clave]       # genera el .docx (+ NOMBRE.outline.json)
uv run docs-qa DOC.docx [--out DIR] [--no-render]      # revisa y renderiza (default: qa/<nombre>/ junto al .docx)
uv run docs-visuals DIR|FILES [--preset P]             # .mmd y .chart.json -> PNG con los colores del preset
uv run docs-fill plantilla.docx --vars                 # lista los {{campos}}
uv run docs-fill plantilla.docx datos.json salida.docx # llena un formato oficial
```

---

## Flujo de trabajo

### Fase 0 · Detectar el modo

| Modo | Señal | Qué hacer |
|---|---|---|
| A · Nuevo | Tema o petición sin archivo | Fases 1→6 |
| B · Desde material | Notas, Markdown, transcripción, PDF, otro .docx como fuente | Inventario del material (Fase 2) y luego A |
| C · Formato oficial con etiquetas | El profesor da un .docx con `{{campos}}` | `uv run docs-fill ... --vars` → pedir datos faltantes → llenar → QA |
| D · Formato oficial sin etiquetas | Un .docx institucional "para llenar" | Convertir los huecos en `{{campos}}` sin tocar estilos y seguir C (ver `references/formatos-y-edicion.md`) |
| E · Editar un .docx existente | "Corrige / actualiza / agrega a este Word" | Ver `references/formatos-y-edicion.md` (no regeneres desde cero) |

### Fase 1 · Brief (una sola ronda)

Revisa primero la conversación, `asignaturas/` y materiales previos; no preguntes lo que ya está en el proyecto. Pregunta en una sola lista breve solo lo que no se pueda deducir:

1. **Tipo de documento** y **para quién** (alumnos, coordinación, cliente, comité de tesis).
2. **Extensión** o páginas aproximadas.
3. **Preset**: `utez`, `apa`, `corporativo`, `tecnico`, `editorial`.
4. **Datos institucionales**: logo (archivo), nombres, cargos, asignatura, grupo, periodo. El nombre y cargo del docente salen de "Profesor" en `CLAUDE.md`. Dato institucional que el proyecto no confirma (clave, fecha oficial, escala): `[CONFIRMAR]`. Contenido que simplemente falta: `[DATO PENDIENTE]`, visible.
5. **¿Existe un formato oficial?** Si sí, pídelo: un formato oficial siempre gana sobre el diseño propio.

Defaults si el profesor no responde: tamaño **Carta**, idioma `es-MX`, preset `utez` para lo académico/institucional, `apa` para investigación, `tecnico` para documentación de software. Declara los supuestos al inicio.

### Fase 2 · Plan

Lee la receta del documento en `references/recetas.md`. Escribe el esquema antes del spec: tipo, preset, portada sí/no, preliminares (índice, índice de tablas/figuras, resumen), lista de títulos H1/H2, tablas y figuras previstas, datos pendientes. Con material fuente, inventaria cada dato y no inventes cifras. El `kicker` de portada es la categoría ("Planeación didáctica"), no repitas el título. Si el profesor está presente y el documento pasa de ~5 páginas, muestra el esquema y espera el OK.

En exámenes, rúbricas y planeaciones aplican `.claude/rules/evaluacion.md` y la plantilla de su tipo: tres saberes, ≥ 2 tipos de evaluación, ponderaciones que sumen 100 %, escala confirmada.

### Fase 3 · Escribir el spec

Crea `documento.json` (campos y bloques en `references/spec.md`; modelos en `examples/`). Usa bloques Markdown para la prosa y bloques tipados para tablas, figuras, exámenes, rúbricas y firmas. Respeta "Reglas de redacción" y "Reglas de diseño".

### Fase 4 · Visuales (si hay)

- Diagramas: `figs/nombre.mmd` (Mermaid). Gráficas: `figs/nombre.chart.json` (formato en "Visuales").
- `uv run docs-visuals figs --preset <preset>` → `figs/nombre.png` con los colores del preset.
- En el spec referencia `figs/nombre.mmd` o `figs/nombre.chart.json` (`docs-build` usa el PNG generado) o cualquier PNG/JPG del profesor.

### Fase 5 · Construir y revisar (dos pasadas)

```bash
uv run docs-build documento.json         # 1ª pasada -> documento.docx + documento.outline.json
uv run docs-qa documento.docx            # revisión + PDF + capturas + documento.pages.json
uv run docs-build documento.json         # 2ª pasada: índices con números de página
uv run docs-qa documento.docx            # repite hasta "Sin cambios: índices al día"
```

- `docs-qa` dice al final del mapa de páginas **"CAMBIARON"** (repite build + QA) o **"Sin cambios: índices al día"** (listo). Sin índices en el documento basta una pasada.
- `docs-qa` valida estructura (XML, saltos de nivel, viñetas falsas, párrafos vacíos, tablas, fuentes, campo de página, imágenes sin alt), lista los datos pendientes, renderiza con LibreOffice a `qa/<nombre>/<nombre>.pdf`, `page-N.png` y `sheet.png`, detecta páginas en blanco y última página casi vacía, y calcula las páginas de títulos y leyendas para los índices.
- **Mira `qa/<nombre>/sheet.png` y las páginas clave** con tus propios ojos: portada, índice, tablas largas, figuras, firmas, última página.
- Sin LibreOffice: corre con `--no-render`, dilo explícitamente al profesor y recuérdale que Word preguntará "¿Deseas actualizar los campos?" al abrir (Sí) para poner los números de página del índice.
- Con la 2ª pasada el índice ya trae sus números y Word **no** muestra el aviso. Si el profesor edita el documento, clic derecho en el índice → Actualizar campo. `"updateFields": true` en el spec fuerza el aviso.
- Exámenes: `uv run docs-build examen.json --clave` genera además `examen_clave.docx`.

### Fase 6 · Entregar

Entrega el `.docx` (y el PDF de `qa/` si lo piden), una línea con lo que contiene y la lista de `[DATO PENDIENTE]` y `[CONFIRMAR]` que quedaron. Ofrece: ajustar contenido, cambiar preset, exportar PDF. Guarda el `.docx` en `cursos/<periodo>/<curso>/semana-NN/alumno/` (claves en `docente/`) con su prefijo de orden (`s1-02-…`) y el spec `.json` en `fuentes/` de esa semana: `docs-build fuentes/<nombre>.json` deja el `.docx` en la carpeta de la semana (muévelo a `alumno/` o `docente/`) y `.outline.json`, `.pages.json` y `qa/` en `fuentes/`. Nombres en minúsculas y guiones.

---

## Reglas de redacción

- Abre cada sección con lo importante (conclusión, objetivo o instrucción) y luego el detalle.
- Párrafos de 3–6 líneas, voz activa, un término por concepto; listas solo para elementos paralelos (no conviertas todo en viñetas).
- Títulos descriptivos y únicos ("Requisitos de seguridad", no "Otros").
- Cifras con unidad y fuente; **nunca inventes datos**: `[DATO PENDIENTE]` visible y reportado al entregar. Los ejemplos ilustrativos se marcan como tales.
- Español de México: fechas "15 de octubre de 2026", horas "10:00 h", decimales con punto, comillas " ", rangos con guion corto (2024–2026), incisos con raya (—).
- APA 7: citas (Autor, año) o Autor (año); con 3+ autores, "et al." desde la primera cita; citas textuales < 40 palabras entre comillas con página, ≥ 40 como `quote`; referencias con título de libro/revista en *cursivas*, DOI como URL `https://doi.org/…`, orden alfabético.
- Instrucciones de examen claras: tiempo, valor total, material permitido.

## Reglas de diseño

- **Estilos, no formato directo:** todo título es H1–H3 (entra al índice); nada de párrafos en negritas haciendo de título.
- **Espacio con espaciado de párrafo**, nunca con Enters vacíos; saltos con `pagebreak`, no con líneas en blanco.
- **Jerarquía clara:** máximo 3 niveles de título; no saltes niveles (H1 → H3).
- **Formato de la casa (todos los presets menos `apa`):** márgenes de 1.5 cm por lado, fuentes de 9 a 11 pt en todo (títulos incluidos: portada y H1 11 pt negrita con el color de títulos del preset (utez: azul institucional), H2 10.5 pt negrita, H3 10 pt negrita cursiva, cuerpo/listas/tablas 10 pt, notas, leyendas, encabezado, pie y código 9 pt) e interlineado sencillo (1.0). La jerarquía se logra con peso, color y estilo, no con tamaño. `apa` es la única excepción (Times 12 pt, doble espacio, 2.54 cm). `docs-qa` avisa (REVISAR) si un documento no APA se sale de esto.
- **Tablas sin "cárcel":** banded o lines por defecto; grid solo para rúbricas y formatos de llenado. Encabezado repetido, filas que no se parten, números alineados a la derecha, ≤ 7 columnas (si no caben, `orientation: "landscape"` o divide la tabla).
- **Máximo 2 familias + monoespaciada**, un color de acento; nada de títulos de colores distintos ni todo en negritas.
- **Alineación a la izquierda** (justificar solo si el formato oficial lo exige).
- **Portada llena ≥ 60 %** de la página; la última página no debe quedar con 1–2 líneas (QA lo avisa).
- **Imágenes** con leyenda, fuente y texto alternativo; nunca más anchas que el área útil.
- **Callouts** para advertencias o claves, no para decorar.
- **Prohibido:** viñetas escritas a mano (`•`), tablas de una celda como línea divisoria, texto blanco sobre colores claros, Comic Sans/Papyrus, WordArt, clip-art, emoji.

## Visuales

- **Mermaid** (`.mmd`): sintaxis, tipos y validación en el skill `mermaid-diagrams` (`uv run mermaid-check`). Consejo para Word: la página es vertical, así que prefiere `flowchart TB`, `sequenceDiagram`, `stateDiagram-v2`, `erDiagram`, `gantt`; ≤ 8–10 nodos, etiquetas de 1–4 palabras. Un `flowchart LR` largo queda con letra diminuta. No pongas `%%{init}` ni colores: `docs-visuals --preset` aplica los del preset.
- **Gráficas** (`.chart.json`): `{"type": "bar" | "hbar" | "line", "title", "categories", "series": [{"name", "values"}], "unit": "%", "focus": "categoría", "label": "all" | "max" | "end"}`. El título no se dibuja: va en la leyenda de la figura (`caption`); `unit` aparece en los valores. Etiquetas largas se parten en renglones y, si no caben, la gráfica pasa sola a barras horizontales. Un solo eje, ≤ 4 series, ≤ 12 categorías, sin pastel ni 3D; los colores salen del preset (validados para daltonismo). Modelos en `examples/figs/`.
- **Capturas y fotos**: solo reales del profesor; si faltan, deja un `callout` "Captura pendiente: …".
- Ancho: diagramas y gráficas `width: 0.8–1`; logos y capturas pequeñas `0.3–0.5`.
- **Logo:** solo el archivo que dé el profesor. Nunca lo redibujes ni lo inventes.

## Checklist final

- [ ] Spec con preset, idioma, tamaño de página y metadatos correctos; logo solo si el profesor lo dio.
- [ ] Estructura de la receta completa (completitud por escenario); títulos jerárquicos sin saltos.
- [ ] Docente tomado de `CLAUDE.md`; datos institucionales dudosos como `[CONFIRMAR]`.
- [ ] Reglas de evaluación cumplidas (exámenes, rúbricas, planeaciones): tres saberes, ≥ 2 tipos, 100 %, escala.
- [ ] Cero datos inventados; los `[DATO PENDIENTE]` se reportan al entregar.
- [ ] Visuales generados con `docs-visuals` y con leyenda; tablas ≤ 7 columnas.
- [ ] Dos pasadas de `docs-build` + `docs-qa` hasta "Sin cambios: índices al día".
- [ ] `qa/<nombre>/sheet.png` revisada: portada, índices, tablas, figuras, firmas, última página.
- [ ] Entrega con la lista de pendientes.

## Créditos

Basado en el skill `docx` de Anthropic, minimax-docx, kimi-docx, officecli-docx, scholar-thesis-docx y docx-contracts. Generador portado a Python (python-docx + OXML).
