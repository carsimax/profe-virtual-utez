---
name: html-slides
description: Crea presentaciones como un solo HTML (16:9, presentador, PDF, móvil, Mermaid, gráficas e íconos SVG, diseño UTEZ claro) y publícalas con gist. Usar al pedir slides, deck, charla o convertir un .pptx.
---

# HTML Slides

Genera decks como **un único `index.html`** autocontenido: lienzo fijo 1920×1080 que escala a cualquier pantalla, navegación por teclado/clic/swipe, URL con `#n`, índice visual, modo presentador con notas y timer, exportación a PDF, modo lector en móvil y publicación con un gist. Recursos visuales integrados: 28 íconos SVG, ilustraciones SVG propias, diagramas Mermaid con los colores del preset, gráficas SVG generadas por script y logo de marca.

Fusiona prácticas de frontend-slides, html-ppt, guizang-ppt, huashu-design, visual-explainer, slide-creator, visual-cognition-slides.

**Cómo usar este archivo:** aquí viven el flujo y las reglas. El detalle se carga por fase desde `references/` y `assets/` (tabla de abajo); no leas la plantilla completa, cópiala. Los scripts son comandos `uv run slides-*` del paquete Python del repo.

| Archivo | Para qué | Cuándo leerlo |
|---|---|---|
| `assets/template.html` | Plantilla del deck: runtime, CSS, 24 slides de ejemplo (todos los layouts) | Fase 3: cópiala, no la leas completa |
| `references/presets.md` | Diseño UTEZ (claro): tokens y fuentes, ya incorporados en la plantilla | Fase 3, al construir |
| `references/layouts.md` | Catálogo de layouts, layout por cantidad de elementos, cuota de diversidad, rejilla y tokens de espaciado, ajuste de imágenes | Fase 2 (plan) y Fase 3 |
| `references/visuals.md` | Qué recurso visual usar, íconos, gráficas, marca y logo | Fase 3, al elegir el visual de cada slide |
| `references/checklist.md` | Pre-flight, densidad, escalera de desbordes, crítica de cinco ejes, checklist final | Fase 4 y antes de entregar |
| `references/tools.md` | Comandos `slides-*`, `svg-check`, `mermaid-check`, gist y PDF | Al ejecutar comandos o publicar |
| skill `svg-illustrations` | Diagramas e ilustraciones SVG a mano | Cuando un slide necesite un SVG propio |
| skill `mermaid-diagrams` | Diagramas Mermaid (flujo, UML, secuencia, estados, ER, git) | Cuando un slide necesite Mermaid |

Plantilla: `cp .claude/skills/html-slides/assets/template.html <deck>/index.html`.

**Principio rector:** el modelo decide el *contenido* (plan); la plantilla decide el *runtime*. Nunca reescribas la navegación, el escalado ni el CSS de impresión: copia la plantilla y escribe solo slides y tokens.

---

## Flujo de trabajo

### Fase 0 · Detectar el modo

| Modo | Señal | Qué hacer |
|---|---|---|
| A · Nuevo | Solo un tema o idea | Fases 1→6 completas |
| B · Desde material | Notas, Markdown, doc, transcripción, PDF, README, PR | Inventario del material (Fase 2) antes de planear |
| C · Convertir .pptx | Adjunta un PowerPoint | Ejecuta `uv run slides-pptx` (ver `references/tools.md`), muestra lo extraído, luego Fase 1 |
| D · Editar deck existente | Un HTML hecho con este skill | Edita solo las `<section>` pedidas; no toques runtime ni tokens salvo que lo pidan |

### Fase 1 · Brief (una sola ronda de preguntas)

Pregunta **en un solo mensaje** (con la herramienta de preguntas si existe) únicamente lo que no se pueda deducir:

1. **Audiencia** y nivel técnico.
2. **La única idea que deben recordar** (una frase). Si no la hay, el deck no está listo.
3. **Duración** o número de slides.
4. **Uso:** `ponente` (se presenta en vivo: poco texto, notas ricas) o `lectura` (se comparte el link sin ponente: títulos y pies más explicativos).
5. **Extras:** notas del presentador, publicar en gist, PDF.

Inferencias antes de preguntar: “charla”, “presentar”, “stream”, “clase”, “notas del presentador” → `ponente`; “compartir el link”, “informe”, “resumen”, “para leer”, “changelog” → `lectura`. Defaults si el usuario no está o no responde: lo inferido, si no `lectura`; idioma del usuario (ajusta `<html lang>`); notas breves; sin publicar. Declara los supuestos al inicio de tu respuesta.

Cantidad: `ponente` ≈ 1–1.5 min por slide (30 min → 20–26 slides); `lectura` → lo que pida el contenido, una idea por slide. La suma de `data-minutes` (portada y cierre incluidos, ~0.5 min cada uno) no debe pasar del 90 % de la duración real.

### Fase 2 · Plan (fuente de verdad, antes de escribir HTML)

Escribe el plan en el chat (o en `deck-plan.md` si es largo). La columna `por qué` justifica el layout por la cantidad y el tipo de contenido (mapa en `references/layouts.md`); `visual` nombra el recurso o deja “—” si la slide es de respiro. Antes de pasar a HTML haz el **pre-flight**: cada clase usada existe en la plantilla y el plan cumple la cuota de diversidad.

```
Tesis: <una frase>
Arco: <estructura elegida>
| # | id | capítulo | rol | título-afirmación | layout | por qué | visual | min |
|---|----|----------|-----|-------------------|--------|---------|--------|-----|
| 1 | portada | Intro | gancho | … | l-cover | abre con la promesa | — | 1 |
```

**Arcos disponibles**
- **Charla:** Gancho → Contexto → Núcleo (3–5 módulos) → Giro → Qué llevarse.
- **Ejecutivo / informe:** conclusión primero → evidencia → riesgos → decisión pedida.
- **Microclase:** gancho → conocimiento previo → concepto + analogía → mecanismo → ejemplo → contraejemplo → error común → resumen → mini-quiz → siguiente paso.
- **Changelog / PR:** feedback recibido → causa raíz → nuevo flujo → detalles → antes/después → checklist para el usuario → referencias.

**Con material fuente:** primero haz un inventario de cada punto, número y condición del material; asigna cada ítem a una slide (si no cabe, agrega slides, no descartes). Prueba de reconstrucción: alguien que no vio la fuente debe poder reconstruir cada punto desde el deck + notas. **Nunca inventes cifras**; si falta un dato, pon `[DATO PENDIENTE]` visible y avísalo. Los ejemplos ilustrativos (un `git log` de muestra, una salida de terminal) están permitidos si se ven como ejemplo (“ejemplo”, nombres genéricos) y no se presentan como datos reales.

**Tipo de conocimiento → visual**

| Tipo | Visual que funciona | Evitar |
|---|---|---|
| Concepto | analogía + definición desglosada, ejemplo/contraejemplo | pegar la definición de Wikipedia |
| Procedimiento | `l-steps` con 3–5 pasos, error → corrección | 7 pasos en una slide |
| Relación / arquitectura | diagrama SVG de cajas y flechas con verbos, matriz 2×2 | flechas sin explicar el porqué |
| Comparación | `l-compare` o `l-table` con la opción ganadora resaltada | tablas de 10 filas |
| Datos | `l-stats` (2–4 cifras), barras simples con la serie clave en acento | pies, 3D, gráficas sin fuente |
| Historia / caso | `l-case` (quién, qué pasa, qué cuesta, tu turno), cita real, línea de tiempo, captura | stock photos |
| Evidencia de una afirmación | `l-evidence`: título-oración + una gráfica o captura con lo clave resaltado | gráfica sin la barra o dato que se discute |
| Código nuevo | `l-walk` (líneas resaltadas y etiqueta pegada a cada una), `l-predict` antes de ejecutar | código largo sin resaltar nada |
| Paso de un ejemplo resuelto | `l-worked`: subobjetivo, qué, por qué, resultado intermedio, verificación | resultado que aparece sin su paso |
| Concepción errónea | `l-myth`: «lo que parece / lo que pasa» con el contraejemplo | corregir sin mostrar el error |

**Diversidad y ritmo (se miden en `slides-qa`):**
- Decks de 7–9 slides: ≥ 6 layouts distintos; de 10 o más: ≥ 8.
- Nunca el mismo layout dos veces seguidas ni 3 slides con la misma estructura de cuerpo.
- Respiro (`l-section` o `l-statement`) cada 3–4 slides en decks de 8 o más; un “reinicio de atención” (pregunta, demo, cita, dato sorpresa) cada 8–10.
- Máximo 2 slides seguidas con el mismo tono (`data-tone`).
- **Variedad con función:** elige el layout por lo que le pides al alumno (predecir → `l-predict`, localizar → `l-walk`, comparar → `l-compare`, desmentir → `l-myth`, decidir → `l-case`, ver la prueba → `l-evidence`) y anótalo en las notas. Variar por variar no cuenta.
- **Ritmo de sesión:** un segmento de exposición dura ≤ 10–12 min y termina en una parada (corte, predicción o pregunta); no encadenes más de 8–10 slides de exposición sin una. Evidencia y razones en `.claude/referencia/pedagogia-evidencia.md` (secciones 1 y 3).
- **Prueba de borrado de texto:** si quitas el texto y el visual no comunica la idea, rediseña el visual. Acción cognitiva → visual: proceso → flujo; comparación → un solo visual de la diferencia; magnitud → tamaño codificado; decorar no cuenta (tabla en `references/checklist.md`).

Si el usuario está presente y el deck tiene más de 6 slides, **muestra el plan y espera su OK** antes de construir.

### Fase 3 · Construir

1. Copia la plantilla: `cp .claude/skills/html-slides/assets/template.html <deck>/index.html` (o al nombre pedido). Haz el pre-flight de `references/checklist.md`.
2. El diseño UTEZ (claro) y sus fuentes ya vienen en la plantilla; no cambies los tokens.
3. Si hay logo de marca, configúralo (ver `references/visuals.md`).
4. Borra las 24 slides de ejemplo y escribe las tuyas siguiendo el plan, con el catálogo de `references/layouts.md` y los tokens `--fs-*` y `--sp-*` (no escribas tamaños en px sueltos). Reemplaza también `<title>`, el texto de portada y cualquier texto de ejemplo: `slides-qa` los marca.
5. Cada slide: `<section class="slide l-…" data-id="…" data-chapter="…" data-minutes="…">`, opcional `data-tone="2|3|4"` (color del capítulo) y `data-badge="DEMO"` (insignia en el HUD).
6. Kicker en cada slide de contenido: `<p class="kicker reveal"><span class="n"></span> · Capítulo</p>` (el runtime rellena `.n` con el número de slide, así que reordenar no rompe nada). Opcional en `l-cover` (ahí va evento · fecha), `l-section`, `l-quote` e `l-image`. Título-afirmación. Elementos con `class="reveal"` para la entrada escalonada (máx. 6 por slide).
7. Notas en `<aside class="notes">` dentro de cada slide (ver reglas).
8. Visuales: elige el recurso con `references/visuals.md` (ícono, ilustración o diagrama SVG con la skill `svg-illustrations`, Mermaid con la skill `mermaid-diagrams`, gráfica de `slides-chart`, captura real). Cada slide de contenido debería tener un visual que cargue la idea.
9. Imágenes: embébelas como data URI (`uv run slides-inline-images`) para que el archivo siga siendo único. Sin imagen real → `.placeholder` honesto con lo que falta (“Captura pendiente · 16:9 · …”), nunca ilustraciones falsas.
10. Demos: si la demo tiene más de 3 pasos o prompts para copiar, va en `demos/NN-tema.md` (objetivo, prerrequisitos, pasos con prompts, qué pasó, para pensar) y el deck solo lleva una slide `data-badge="DEMO"` que la nombra; una demo corta se describe en las notas de esa slide.

### Fase 4 · QA (obligatorio, con evidencia)

1. Prepara (una sola vez): desde la raíz del repo, `uv sync` y `uv run playwright install chromium`. Todos los comandos se ejecutan desde la raíz con la ruta del deck (`cursos/<periodo>/<curso>/semana-NN/alumno/<prefijo>-presentacion-<tema>/index.html`).
2. Si hay diagramas SVG a mano: `uv run svg-check <deck>/index.html`. Si hay Mermaid: `uv run mermaid-check <deck>/index.html` y luego `uv run slides-mermaid <deck>/index.html` para incrustarlo (necesitan red para cargar Mermaid; el SVG queda en el HTML y aparece en el PDF). Corrige sus errores antes del paso 3.
3. Ejecuta `uv run slides-qa <deck>/index.html --pdf --minutes <duración>` (omite `--minutes` si no hay duración fija). Debe terminar en `OK`; revisa también “REVISAR” (notas, kicker, layouts repetidos o sin diversidad, espacio vacío inferior, minutos, texto SVG pequeño). Si avisa que las fuentes web no cargaron, las capturas usan fuentes de respaldo: no juzgues la tipografía por ellas.
4. Comprueba que **cada parada del plan tiene su slide de corte** (tipo, duración, modalidad, material, producto, «Regresamos a»). Quirks de `slides-qa`: marca el mismo layout 2–3 veces seguidas, así que intercala una slide de transición de 0 minutos entre cortes consecutivos; `data-minutes="0"` es válido para slides de apoyo; más de 6 `.reveal` por slide se marca.
5. Corrige cada desborde con la **escalera medida** (1–40 px afloja espaciado · 40–90 compacta huecos · 90–160 ajusta texto o divide · > 160 cambia de layout o recorta). Nunca bajes la fuente por debajo de los tokens ni metas scroll.
6. **Mira las capturas** (`qa/slide-NN.png`, `qa/mobile.png`) con tus propios ojos: jerarquía, alineación, solapes en SVG, íconos bien escalados, fondo que no compita con el texto, contraste.
7. Pasa la **crítica de cinco ejes** de `references/checklist.md` (Mantener / Arreglar / Quick wins). Corrige todo lo `fatal` e `importante`.
8. Si no hay Playwright ni forma de instalarlo, dilo explícitamente y revisa al menos el HTML a mano contra el checklist final.

### Fase 5 · Entregar

Entrega la ruta del archivo, una línea con los controles (`← → · O índice · F pantalla completa · S presentador · P PDF · B negro`) y ofrece: publicar como gist, exportar PDF, o iterar slides concretas.

---

## Reglas de contenido

- **Título = oración con verbo** (afirmación), no tema: “La opción B reduce el costo a la mitad”, no “Comparativa”. Un título de 3 o más líneas se reescribe. Prohibidos como título: Overview, Resumen, Agenda, Conclusiones, Next steps, Key insights.
- **Una idea por slide.** Si necesitas “y además”, son dos slides. ≤ 3 conceptos nuevos por slide.
- **Regla de 3 segundos** (texto de cuerpo, sin contar título, kicker, pills, código ni pies de figura): ≤ 25 palabras en modo `ponente`; ≤ 60 en `lectura`; o ≤ 4 viñetas de ≤ 12 palabras; o ≤ 4 cifras; o un visual que ocupe ≥ 40 % de la slide.
- **Densidad:** `ponente` → 1–3 viñetas por slide; `lectura` → 4–8 viñetas o 4–6 tarjetas; siempre ≤ 6 elementos. Si no cabe, divide la slide, no encojas la fuente.
- Presupuestos por layout: tarjetas ≤ 6; pasos 3–5; código ≤ 10 líneas; tabla ≤ 6 filas × 4 columnas; cita ≤ 25 palabras; viñetas ≤ 5.
- Habla al público (“tú”, “tu equipo”), frases ≤ 20 palabras, voz activa, un término por concepto. Traduce la jerga con una analogía la primera vez.
- Cifras siempre con unidad y fuente (en pie o en notas). Nada de datos inventados.
- **Cada parada lleva su slide de corte** (`l-corte`): actividad, práctica, demostración o ejercicio guiado, coevaluación, examen y cierre. Muestra tipo, duración, modalidad, material, producto y «Regresamos a: …»; si el material debe seguir proyectado durante la actividad, añade una slide de apoyo de 0 minutos justo después. Todo procedimiento se enseña paso a paso antes de usarse en un ejemplo o práctica.
  Todo ejercicio guiado o demostración, en cualquier materia, se respalda paso a paso: tras su corte van slides de apoyo de 0 minutos que se proyectan mientras los alumnos lo resuelven, una por paso o sección del documento del ejercicio, en el mismo orden y con los mismos nombres y números, mostrando cómo se llega a cada sección y cada cálculo con los datos reales del ejercicio, con notas del presentador.
- Abre con el dolor o la promesa (slides 1–2) y cierra con un siguiente paso concreto (checklist, link, comando), nunca con “¿Preguntas?” solo.

## Reglas de diseño (anti-slop)

- **Prohibido:** emoji (usa los íconos del sprite), degradado morado sobre blanco, `#6366f1`, neón sobre `#0d1117`, Inter/Roboto/Arial como fuente *display*, emoji como iconos, tarjetas con borde izquierdo de color, glassmorphism, sombras decorativas, tarjetas dentro de tarjetas, todo centrado, rejillas de tarjetas idénticas en slides seguidas, easing con rebote, `#000`/`#fff` puros como fondo, texto en degradado, clip-art y fotos de stock.
- **Sí:** un color dominante + un acento usado con escasez (90/8/2); el color de acento solo en ≤ 3 tipos de elemento por slide; tipografía como identidad (máx. 2 familias + mono); título ≥ 2× el cuerpo (h2 72 px frente a 36 px); alineación a la izquierda por defecto; fondos tranquilos (solo el `--bg-art` sutil del preset); un detalle pulido al 120 % por slide, el resto limpio.
- Tamaños a 1920×1080: cuerpo 36 px (`--fs-body`), código 30 px, texto secundario 26 px (`--fs-small`), etiquetas de diagrama 15 px solo en mayúsculas mono. QA marca cualquier texto < 24 px. El código nunca es menor que el cuerpo menos 6 px: si no cabe, recorta el fragmento y resalta las líneas.
- **Señala solo lo que se comenta ahora:** el resto va en gris (`--text-dim`, `.ch-mute`, `.ln` sin `.hl`). La etiqueta se pega al elemento (número sobre la línea, no leyenda aparte). Sin texto redundante: lo que dices en voz no se repite en la slide.
- Contraste WCAG AA: texto ≥ 4.5:1 sobre `--bg`, `--surface` y `--surface-2` (el diseño UTEZ ya cumple; verifica cualquier color nuevo). El texto atenuado usa `--text-dim`, nunca opacidad.
- Caracteres reales: comillas “ ”, raya —, menos −, ×, espacio duro antes de unidades. `text-wrap: balance` en títulos ya viene en la plantilla.
- Animación: solo `transform` y `opacity`; la entrada `.reveal` es el único movimiento; `prefers-reduced-motion` ya está cubierto. Nada de autoplay ni `setInterval` infinitos.

## Diagramas, ilustraciones y Mermaid

Se delegan a skills propias; aquí solo lo esencial:

- **SVG a mano** (arquitectura, mecanismos, ilustraciones): skill `svg-illustrations`. Usa las clases `.d-*` / `.ill-*` de la plantilla para que usen los tokens del diseño. Valida con `uv run svg-check <deck>/index.html`.
- **Mermaid** (flujo, UML de clases, secuencia, estados, ER, gitGraph): skill `mermaid-diagrams`. El runtime lo dibuja con el tema del diseño UTEZ. Valida con `uv run mermaid-check <deck>/index.html`; incrústalo con `uv run slides-mermaid`.
- Prueba de doble codificación: si borras el texto de la slide, el diagrama aún comunica la idea. ≤ 8 nodos por diagrama; si hay más, un diagrama general y slides de detalle.
- **Imágenes:** `contain` para capturas, diagramas y logos; `cover` para fotos; un grupo comparte proporción y altura (más en `references/layouts.md`).

## Notas del presentador

- En `<aside class="notes">` dentro de cada slide (HTML simple: `<ul>`, `<p>`, `<b>`). No se ven en el deck ni en el PDF; aparecen en la ventana del presentador (tecla **S**).
- Formato de ficha, no guion literal (salvo que lo pidan): 2–4 puntos que decir, el dato o ejemplo exacto, **Transición:** frase hacia la siguiente slide, y si aplica **Demo:** / **Pregunta al público:**.
- `data-minutes` en cada slide alimenta el timer: el presentador muestra tiempo transcurrido, si vas adelantado/atrasado y el total planeado.
- Nunca pongas en la slide visible texto dirigido al ponente.

## Controles (ya implementados en la plantilla)

| Tecla / gesto | Acción |
|---|---|
| → ↓ Espacio AvPág Enter · clic en el tercio derecho · swipe ← | Siguiente |
| ← ↑ RePág Retroceso · clic en el tercio izquierdo · swipe → | Anterior |
| Inicio / Fin · número + Enter | Primera / última / ir a la slide N |
| O o Esc | Índice visual de miniaturas |
| F | Pantalla completa |
| S | Ventana del presentador (actual, siguiente, notas, timer, sincronizada) |
| B o . | Pantalla en negro (también desde el presentador) |
| P | Imprimir / Guardar como PDF (una página 1920×1080 por slide) |
| `#5` en la URL | Abre directo en la slide 5; la URL se actualiza al navegar |

En pantallas ≤ 760 px de ancho (o teléfonos en horizontal) el deck pasa a **modo lector**: una columna con scroll, rejillas apiladas y tipografía fluida. `window.deck.go(i)` permite controlarlo desde scripts y escucha `deck:slidechange` para efectos por slide.

---

---

## Entrega y publicación

Gist, PDF y los comandos `slides-*` están en `references/tools.md`. Antes de entregar, pasa el checklist final de `references/checklist.md`. El diseño UTEZ está en `references/presets.md`, y el catálogo de layouts (incluidos `l-bento`, `l-sidebar` y `l-timeline`) en `references/layouts.md`.
