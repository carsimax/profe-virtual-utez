# Catálogo de layouts

> Referencia de html-slides. Léela en la Fase 2 (plan: elegir layout por slide) y en la Fase 3 (estructura exacta de cada uno). La plantilla (`assets/template.html`) trae una slide de ejemplo de cada layout: cópiala y reemplaza el contenido.

## Catálogo

| Clase | Para qué | Estructura |
|---|---|---|
| `l-cover` | Portada | `.brand-logo` opcional, kicker, `h1`, `.lead`, `.meta` con `.pill` |
| `l-section` | Apertura de capítulo / respiro | `.sec-num` (“02”), `h2`, `.lead` opcional |
| `l-statement` | Una afirmación grande o el giro | kicker, `.claim` con `<em>` en la parte clave, fuente |
| `l-split` (`.flip`) | Explicación + figura (layout base) | `.col` (kicker, `h2`, `p`) + `figure.fig` con SVG o imagen |
| `l-stats` | 2–4 cifras | `header.head` + `.stats` (`style="--cols:3"`) con `.stat > b + span` |
| `l-grid` | 2–6 tarjetas paralelas | `.head` + `.cards` (`--cols`) con `.card` (`.is-tone` para destacar una) |
| `l-compare` | Antes / después, A vs B | `.head` + `.compare` con 2 `.card` (la segunda gana) |
| `l-steps` | Proceso 3–5 pasos | `.head` + `ol.steps` (`--cols`) con `li > h3 + p` (`.is-tone` = paso clave) |
| `l-code` | Comando, código, salida de terminal | `.head` + `.term > .term-bar + pre` (spans `.c .k .s .p` para resaltar) |
| `l-table` | Comparativa tabular | `.head` + `table.tbl` (primera columna en mono y tono) |
| `l-image` (`.bleed`) | Captura o foto | `.head` + `figure.media > img(.contain) + figcaption` o `.placeholder` |
| `l-quote` | Cita real | `blockquote` + `cite` |
| `l-diagram` | Diagrama o gráfica a lo ancho | `.head` + `figure.fig` con `pre.mermaid`, SVG o `.chart` |
| `l-bento` | 4–7 piezas con una dominante | `.head` + `.body > .bento` con `.card.cell`; una celda grande `.span-2x2` y el resto `.span-2x1` / `.span-1x2` / sin span (rejilla de 4 columnas × 2 filas) |
| `l-sidebar` | Título + contexto a la izquierda (34 %), 3 elementos apilados a la derecha | `.col` (kicker, `h2`, `.lead`) + `.stack` con 3 `.card` |
| `l-timeline` | Secuencia en el tiempo, 4–7 hitos | `.head` + `.body > ol.timeline` (`style="--cols:5"`) con `li > .t-body > .when + h3 + p`; las etiquetas alternan arriba y abajo del eje. `.timeline.vertical` pone el eje en vertical (ideal con 4–5 hitos de texto largo) |
| `l-evidence` | Afirmación + prueba visual (assertion-evidence) | `.head` con título-oración + `.body` con `figure.fig` (gráfica o captura; lo clave en color, el resto `ch-mute`) y `.card.is-tone.focus` con una sola frase |
| `l-walk` | Recorrido de código anotado | `.head` + `.body > .walk` con `.term > pre` (cada línea `span.ln`, las comentadas `.hl`, marcador `b.mk` pegado al final de la línea) y `ol.labs` con `li > b.mk + div(h3 + p)`. Las `span.ln` van pegadas, sin saltos de línea entre ellas |
| `l-worked` | Un paso de un ejemplo resuelto o de una práctica guiada | kicker «Paso N de M», `span.subgoal`, `h2` con la acción, `.worked` con `dl.sc` (Qué, Por qué) y `.term` «Resultado intermedio», y `p.verify` con la verificación |
| `l-predict` | Predice y luego revela | `.head` con la pregunta + `.pred` con `.term` y `ol.opts > li.opt > b.mk + texto`. La slide de revelación repite el layout con `.opt.is-right` y la salida real, y va separada de la pregunta por otra slide |
| `l-myth` | Concepción errónea: «lo que parece / lo que pasa» | Igual que `l-compare`; la primera tarjeta (borde punteado) es el mito, la segunda es lo que ocurre |
| `l-case` | Caso o contexto real | `.head` + `.case` con `dl.facts` (Quién, Qué pasa, Qué cuesta) y `.card.is-tone` «Tu turno» con la pregunta de decisión |
| `l-corte` | Corte: parada de actividad, práctica, demostración, coevaluación, examen o cierre | kicker `.corte-tag`, `h2`, `dl.corte-facts` (Duración, Modalidad, Material, Producto) y `p.corte-back` («Regresamos a: …») |
| `l-closing` | Siguiente paso | `.head` + `ul.list.checklist` + `.links` con `.pill` |

En modo lector (móvil) `l-bento`, `l-sidebar`, `l-walk`, `l-worked`, `l-predict` y `l-case` se apilan en una columna y `l-timeline` pasa a eje vertical; no hace falta nada extra.

Componentes sueltos: `.ico` (ícono en línea), `.ico-badge` (ícono en recuadro, para tarjetas), `.brand-logo`, `.chart`, `pre.mermaid`, `.kicker`, `.lead`, `.dim`, `.tone`, `.small`, `.mono`, `em.hl`, `code`, `.pill`, `ul.list`, `.card`, `.placeholder` (`style="--ratio:4/3"`), `.num` (cifras tabulares), `.g12` (rejilla de 12 columnas; hijos con `style="--col:4"`).

## Layout según lo que se le pide al alumno

Cada layout nuevo responde a una regla de `.claude/referencia/pedagogia-evidencia.md` (sección 1 y 2). Elige por la acción, anótala en las notas y reutiliza las etiquetas de subobjetivo de la práctica.

| Acción del alumno | Layout | Regla de la evidencia |
|---|---|---|
| Aceptar una afirmación con su prueba | `l-evidence` | Título-oración y un objeto visual como evidencia |
| Localizar qué mirar en el código | `l-walk` | Señalar solo lo que se comenta; etiqueta pegada al elemento |
| Seguir un paso sin saltos | `l-worked` | Subobjetivo, qué, por qué, resultado intermedio, verificación |
| Predecir antes de ejecutar | `l-predict` | Predicción pública y distractores que son concepciones erróneas |
| Desmentir una idea previa | `l-myth` | Mostrar el error y el contraejemplo |
| Decidir con datos reales | `l-case` | Concepto anclado en un caso de Morelos o del sector |

## Layout según la cantidad de elementos

| Elementos | Layout |
|---|---|
| 1 idea fuerte | `l-statement`, `l-quote`, `l-split` con una figura |
| 2 | `l-compare` (A vs B) o `l-split` |
| 3 | `l-grid` de 3, `l-sidebar`, `l-steps` si hay orden |
| 4 | `l-grid` 2×2, `l-stats`, `l-steps` |
| 5–7 | `l-bento` (si una pieza domina) o `l-timeline` (si hay orden en el tiempo) |
| Ciclo, matriz, jerarquía | `l-diagram` con SVG a mano o Mermaid |
| Más de 7 | divide en dos slides; no encojas |

## Cuota de diversidad y ritmo

- 7–9 slides → al menos 6 layouts distintos; 10 o más → al menos 8.
- Nunca el mismo layout dos veces seguidas ni tres slides con la misma estructura de cuerpo (por ejemplo, tres rejillas de tarjetas).
- Respiro (`l-section` o `l-statement`) cada 3–4 slides en decks de 8 o más.
- Un segmento de exposición dura ≤ 10–12 min y termina en una parada (`l-predict`, pregunta o corte); la secuencia de slides es la segmentación: una idea por slide.
- Una slide de predicción y su revelación nunca van seguidas (QA marca el layout repetido): intercala una slide de explicación.
- No más de 2 slides seguidas con el mismo tono de color (`data-tone`).
- Solo se centran los títulos de las slides héroe (portada, sección, afirmación). Nada de líneas de acento bajo los títulos ni franjas de encabezado o pie.

## Rejilla y espaciado

- Tokens de espaciado `--sp-1…--sp-9` = 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 160 px. Usa solo estos; nada de px sueltos.
- Rejilla de 12 columnas: `<div class="g12"><div style="--col:5">…</div><div style="--col:7">…</div></div>`. Alinea a la izquierda; el espacio vacío es parte del diseño.
- Líneas de texto de hasta ~80 caracteres. Un punto focal por slide con espacio tranquilo alrededor.

## Ajuste de imágenes

- `contain` para capturas, diagramas y logos (`img.contain`); `cover` para fotos.
- Un grupo de imágenes comparte proporción y altura. Proporciones fijas: 16:9, 16:10, 4:3, 21:9.
- Imagen a sangre completa (`l-image.bleed`) lleva el texto sobre un velo (scrim) para el contraste.

## Corte (`l-corte`)

Obligatorio en cada parada de la exposición. Fondo oscuro con banda de acento, igual en todo el deck. Campos: **Duración**, **Modalidad** (individual o equipo, con o sin computadora), **Material**, **Producto** y **Regresamos a**. El CSS ya vive en `assets/template.html` (sección 5, con su regla `.reader`).

```html
<section class="slide l-corte" data-id="practica-1" data-tone="3" data-chapter="Práctica" data-badge="PRÁCTICA" data-minutes="30">
  <p class="kicker corte-tag"><span class="n"></span> · Corte · Práctica 1</p>
  <h2 class="reveal">Arma la matriz de tu proyecto</h2>
  <dl class="corte-facts reveal">
    <div><dt>Duración</dt><dd>30 min</dd></div>
    <div><dt>Modalidad</dt><dd>Por equipo · sin computadora</dd></div>
    <div><dt>Material</dt><dd>Papel y pluma</dd></div>
    <div><dt>Producto</dt><dd>Matriz ponderada con pesos justificados</dd></div>
  </dl>
  <p class="corte-back reveal"><b>Regresamos a:</b> Exposición 2</p>
  <aside class="notes">…</aside>
</section>
```

Quirks de QA: `slides-qa` marca el mismo layout 2–3 veces seguidas; entre cortes consecutivos pon una slide de transición de 0 minutos. `data-minutes="0"` es válido para slides de apoyo que siguen proyectadas durante la actividad (sus minutos son los del corte). Más de 6 `.reveal` por slide se marca.

## Layout nuevo

Si ninguno sirve, defínelo en la sección 5 del CSS con los mismos tokens (`--sp-*`, `--fs-*`, `--radius`), añade su versión para `.reader` en la sección 7 (columna única) y una slide de ejemplo en la plantilla. Anima solo `transform` y `opacity`.
