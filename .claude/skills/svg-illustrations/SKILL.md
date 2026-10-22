---
name: svg-illustrations
description: Crea imágenes SVG escritas a mano y las valida con `svg-check`. Usar al pedir imagen SVG, ilustración, diagrama a mano, isométrico, infografía, wireframe, ícono, esquema de arquitectura o figura para slides, tareas o prácticas. Para diagramas de flujo, clases, secuencia o ER con sintaxis estándar usa `mermaid-diagrams`.
---

# SVG hecho a mano para enseñar

Produce figuras SVG limpias, legibles a distancia y temadas con el deck, y las comprueba con un validador determinista antes de entregarlas. Funciona de forma independiente o desde `html-slides` (figuras dentro de `<figure class="fig">`).

## Cuándo SVG a mano, Mermaid o captura real

| Necesidad | Herramienta |
|---|---|
| Flujo, secuencia, clases UML, estados, ER, gitGraph con sintaxis estándar y distribución automática | `mermaid-diagrams` (más rápido y editable como texto) |
| Composición espacial propia: isométrico, arquitectura con capas a medida, topología, línea de tiempo, wireframe, infografía, ícono, metáfora visual | **SVG a mano** (esta skill) |
| Mostrar una interfaz o resultado real (terminal, IDE, navegador, salida de un programa) | **Captura real**; no la dibujes |
| Gráfica de datos (barras, líneas, dispersión) | `slides-chart` de `html-slides`, no SVG manual |

Regla práctica: si el diagrama cabe en Mermaid sin forzarlo, usa Mermaid. Pasa a SVG cuando necesites control de posición, formas propias o una ilustración. Nunca dibujes a mano algo que sea una captura de pantalla.

## Flujo de seis pasos

1. **Plan (especificación en texto).** Antes de escribir una etiqueta, define: mensaje en una frase, lienzo (`viewBox`), nodos y relaciones, orden de lectura, punto focal único, paleta (tema del deck) y política de texto. Si falta el mensaje, pregunta; no adivines.
2. **Rejilla.** Elige `viewBox` (p. ej. `0 0 900 520`, 16:9 aproximado para slides; `0 0 1280 720` para una imagen suelta) y una cuadrícula de 8 o 10 px. Escribe en un comentario antes de dibujar una **tabla de coordenadas** `id x y w h` de cada caja y de los puntos de anclaje de las flechas. Las flechas salen de esa tabla, no de la intuición.
3. **Escribir en orden de capas.** `<title>` y `<desc>`, `<defs>` (marcadores, símbolos), fondo, zonas, conectores, formas, texto al final. Coordenadas absolutas, formas simples, sin filtros exóticos. Escribe corto: los SVG largos se truncan y se rompen.
4. **Validar y renderizar.** `uv run svg-check figura.svg --render figura.png` (o sobre el deck completo: `uv run svg-check index.html`). Corrige primero todos los `ERROR`; los `WARN` se revisan uno por uno.
5. **Mirar el PNG.** Abre la imagen y haz zoom en lo que más falla: puntas de flecha, líneas finas, texto pequeño, cruces de líneas, bordes del lienzo. Compara contra la especificación del paso 1: ¿falta un nodo?, ¿una flecha apunta al lado equivocado?, ¿el foco es evidente?
6. **Arreglos dirigidos, máximo 3 rondas.** Cada ronda corrige una lista concreta de defectos con ediciones puntuales, no reescribe todo. **El último pase refina y nunca agrega formas.** Tras cada ronda vuelve a correr `svg-check` y verifica el color y el fondo explícitamente (los modelos tienden a ignorar instrucciones de color).

Si tras tres rondas persisten defectos, simplifica la figura (menos nodos) en lugar de seguir parchando.

## El comando `svg-check`

```bash
uv run svg-check FILE [--bg COLOR] [--min-font 14] [--width 1600] [--render OUT.png] [--scale 2] [--json]
```

- `FILE` es un `.svg` suelto o un deck `.html`. En un deck mide cada `<svg>` dentro de `.fig` a su tamaño real en la slide (1920×1080) y activa cada slide con `window.deck.go(i)`.
- Un `.svg` suelto se renderiza a `--width` px (1600 por defecto, escala de slide) dentro de una página con el tema `utez`: las clases `.d-*` y `.ill-*` funcionan igual que en el deck. Los íconos `#i-*` del sprite del deck **no** existen fuera del deck: en un `.svg` suelto define tus propios `<symbol>` (ver receta 5).
- Salida: líneas `ERROR|WARN regla svg[n] elemento mensaje` y un resumen. `--json` entrega `{file, ok, svgs:[{index, errors, warnings, stats}]}`. Códigos de salida: 0 sin errores, 1 con errores, 2 archivo ilegible o XML inválido.

| Nivel | Reglas |
|---|---|
| ERROR | `viewbox` (falta), `outside-viewbox`, `text-overlap`, `text-overflow` (texto más ancho que su caja), `min-font` (< `--min-font` a escala real), `broken-ref` (`url(#x)`, `href="#x"`, `aria-labelledby`), `duplicate-id` |
| WARN | `a11y-title`, `a11y-desc`, `a11y-role`, `text-line` (una línea cruza texto), `text-shape`, `contrast-text` (< 4.5:1; 3:1 si el texto ≥ 24 px), `contrast-graphic` (< 3:1), `unused-def`, `duplicate-element`, `path-complexity` (> 200 comandos), `path-decimals` (> 3), `hardcoded-color` (solo en decks), `size` (> 30 KB) |

El solape se mide con intersección de cajas con tolerancia pequeña; la "caja contenedora" de un texto es el rect/círculo/elipse más pequeño que contiene su punto de anclaje. Son heurísticas: un `WARN` puede ser un falso positivo y debes justificarlo, un `ERROR` se corrige.

## Reglas

### Geometría

- `viewBox` siempre explícito. Sin `width`/`height` en SVG en línea (el contenedor escala).
- Todo dentro del `viewBox` con margen mínimo de 20 unidades. Nada se sale del lienzo.
- Coordenadas absolutas y números enteros o con 1 decimal (máx. 2). Rejilla de 8/10 px: alinear evita flechas torcidas.
- Conectores **debajo** de las formas y terminando en el borde de la caja, no en el centro ni flotando. Líneas ortogonales o rectas; evita curvas salvo que signifiquen algo.
- Una forma = un significado: rect = servicio o paso, rect punteado (`.d-zone`) = frontera o zona, círculo = estado o dato. Máximo 8 nodos por figura (en móvil se ven pequeños); si hay más, una figura general y figuras de detalle.
- Un solo punto focal en `--tone`; el resto neutro.

### Texto

- SVG no hace saltos de línea: parte el texto a mano con `<tspan x="…" dy="1.2em">` o con un `<text>` por línea (separación ≥ 1.2 × tamaño).
- Estima el ancho antes de dibujar la caja: **ancho ≈ 0.55 × tamaño de fuente × número de caracteres**. A 24 px, 13 px por carácter; "Controlador" (11) ≈ 145 px. Deja 16 px de holgura por lado.
- Posiciona con `text-anchor` (`middle` centra en `x`) y calcula `y` como línea base: para centrar texto de 24 px en una caja de alto `h`, `y ≈ caja.y + h/2 + 8`.
- Tamaño mínimo **14 px a escala real** (el checker lo mide). Con el deck a 1920×1080: etiquetas `.d-label` de 15 px solo en mayúsculas mono; texto normal `.d-text` de 24 px. Las clases fijan el tamaño por CSS: para variarlo usa `style="font-size:20px"`, el atributo `font-size` no le gana a la clase.
- Etiquetas junto a las formas, nunca sobre una línea. La etiqueta de una flecha va encima de ella, a la mitad, y lleva un verbo ("lee", "emite", "cada 30 s").

### Color y tema

- **En un deck, nunca colores hex ni `rgb()`**: usa las clases del tema para que la figura use los tokens del diseño UTEZ.

| Clase | Uso |
|---|---|
| `.d-box` (`.tone`, `.fill`) | caja neutra, con borde en el tono, rellena con el tono |
| `.d-zone` | frontera o zona punteada |
| `.d-text` (`.on-fill`) | texto de 24 px; `.on-fill` sobre fondo del tono |
| `.d-label` | etiqueta mono mayúsculas de 15 px |
| `.d-big` | cifra grande en el tono |
| `.d-line` (`.dash`, `.hot`) | conector; punteado; resaltado en el tono |
| `.d-arrow`, `.d-dot` | relleno de punta de flecha (`context-stroke`), punto |
| `.d-ico` (`.tone`) | ícono de trazo dentro de un diagrama |
| `.ill-tone`, `.ill-2`, `.ill-soft`, `.ill-surface`, `.ill-line`, `.ill-ink`, `.ill-bg` | ilustración: relleno foco, segundo acento, fondos suaves, trazo, tinta, fondo |

- Contraste: texto ≥ 4.5:1 contra su relleno o el fondo (3:1 si ≥ 24 px); gráficos ≥ 3:1. 4–6 colores en total; máximo 2 gradientes o patrones (idealmente ninguno).
- El significado nunca depende solo del color: acompáñalo de forma, trazo (sólido/punteado) o texto. Piensa en daltonismo y en el PDF en blanco y negro.
- Fuera de un deck (imagen suelta) usa variables CSS en un `<style>` interno o, si es indispensable, una paleta corta de hex repetida en pocas clases.

### Estructura

- IDs únicos y con prefijo de la slide (`s07-arr`) para evitar choques cuando se incrustan varios SVG en un deck; el checker marca `duplicate-id` entre figuras del mismo deck.
- Sin `defs` sin usar. Marcadores y símbolos se declaran en `<defs>` y se usan con `marker-end` / `<use>`; con ≥ 3 repeticiones de una forma compleja, usa `<symbol>` + `<use>`.
- Trazo consistente: mismo grosor por tipo de línea, `stroke-linecap="round"` y `stroke-linejoin="round"` en ilustraciones.
- Marcadores con `orient="auto-start-reverse"` y `context-stroke` para heredar el color de la línea.
- Sin `<style>` global en figuras para deck (las clases ya vienen); sin fuentes embebidas; sin imágenes raster incrustadas; sin `<foreignObject>`.

### Accesibilidad

- `role="img"` y `aria-labelledby="IDtitulo IDdesc"` apuntando a `<title>` (nombre corto) y `<desc>` (qué muestra y cuál es la conclusión, 1–2 frases). En un deck puede bastar `role="img"` + `aria-label` con la misma idea.
- El `<desc>` describe la información, no la apariencia ("el servidor consulta la base de datos"), para que sirva a quien no ve la figura.

### Tamaño

- Meta: < 30 KB; < 20 primitivas por figura de enseñanza (6–20 es lo normal). Paths de ≤ 200 comandos y ≤ 3 decimales.
- Si necesitas más detalle, divide en dos figuras con la misma estética en dos slides consecutivas.

## Guía de estilo para enseñanza

- Estilo técnico plano o isométrico simple: formas geométricas, líneas de grosor uniforme, esquinas redondeadas consistentes (`rx` 8–14).
- **Un punto focal por figura**: lo que el alumno debe mirar primero está en el tono; todo lo demás es neutro.
- Jerarquía de lectura de izquierda a derecha y de arriba abajo; orden de lectura numerado solo cuando no es evidente (callouts con círculos).
- Sin personas realistas, sin clip-art, sin logotipos de terceros ni marcas; usa formas abstractas, íconos de trazo y metáforas geométricas. Si hace falta una persona, un círculo y un semicírculo.
- Datos de ejemplo del contexto local (Morelos, UTEZ, el grupo) y nunca datos personales reales de alumnos.
- Una idea por figura. Si el pie de figura necesita un párrafo, la figura es demasiado compleja.
- Doble codificación: si borras el texto de la slide, la figura aún comunica la idea (por forma y posición).
- Consistencia entre figuras de una misma presentación: misma escala de cajas, mismas clases, misma dirección de flujo.

## Recetas

Las recetas completas (SVG mínimo validado con `svg-check`) están en `references/recipes.md`. Copia la más cercana y adáptala en vez de partir de cero.

| Archivo · Receta | Propósito | Cuándo leer |
|---|---|---|
| `references/recipes.md` · 1 Isométrico | Fórmula de proyección y caja con tres caras | ilustraciones de objetos, servidores, bloques |
| · 2 Flechas | Marcadores normal, abierta, herencia, composición, agregación | cualquier conector con significado UML o de flujo |
| · 3 Callouts | Círculos numerados con línea guía y leyenda | anotar una pantalla, código o esquema |
| · 4 Clase UML | Tres compartimentos y herencia | POO, modelado, diagramas de clases a medida |
| · 5 Red | Nodos con ícono y conectores ortogonales | redes, cliente-servidor, topologías |
| · 6 Cilindro BD | Cilindro con franjas | bases de datos, almacenamiento |
| · 7 Línea de tiempo | Eje con hitos alternados | cronogramas, historia, versiones |
| · 8 Capas | Bandas con componentes y flechas entre capas | arquitectura limpia, MVC, hexagonal |
| · 9 Petición-respuesta | Dos líneas de vida con petición y respuesta | HTTP, API, protocolos |
| · 10 Wireframe | Ventana con cajas y barras simuladas | bocetos de interfaz y pantallas |

## Integración con html-slides

- La figura va en `<figure class="fig reveal"><svg …>…</svg><figcaption>Fig. 1 — …</figcaption></figure>`; el ancho lo da el contenedor. En la sección de diagramas de `html-slides` están las clases y el sprite de íconos (`<use href="#i-database" x="…" y="…" width="48" height="48" class="d-ico tone"/>` dentro de un diagrama).
- Valida el deck completo con `uv run svg-check index.html` y luego `uv run slides-qa index.html`.
- En decks, `hardcoded-color` es un aviso: cámbialo por la clase del tema.

## Lista de verificación final

- [ ] El mensaje de la figura cabe en una frase y la figura lo sostiene sin el texto de la slide.
- [ ] `viewBox` presente; sin `width`/`height` fijos; todo dentro del lienzo.
- [ ] Tabla de coordenadas en comentario; flechas salen y llegan a bordes de cajas.
- [ ] Texto ≥ 14 px a escala real; ningún texto desborda su caja ni se encima.
- [ ] Un punto focal; ≤ 8 nodos; ≤ 20 primitivas.
- [ ] Clases del tema (sin hex) en decks; contraste verificado.
- [ ] `role="img"`, `<title>` y `<desc>` informativos; el color no es el único portador de significado.
- [ ] IDs con prefijo de la slide; sin `defs` sin usar; sin duplicados.
- [ ] `uv run svg-check` en 0 errores; avisos revisados o justificados; PNG revisado con zoom.
- [ ] Sin personas realistas, clip-art ni logotipos de terceros.

## Fuentes

- Anthropic, *canvas-design*: diseño antes de render y último pase que refina sin agregar formas — https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md
- svg-precision-skill: especificación con coordenadas fijas → construir → validar → PNG — https://agentpedia.codes/agent-skills/ui-design/svg-precision-skill
- technical-svg-diagrams (biblioteca de patrones) — https://claudemarketplaces.com/skills/somtougeh/dotfiles/technical-svg-diagrams
- Investigación de respaldo: `.cmx_vault/investigacion/svg-skills.md` (SVGenius, SVGEditBench V2, VFIG, Graphic-Design-Bench: la calidad cae con la complejidad; flechas, líneas finas y texto pequeño son lo más débil).
