# Scripts, publicación y PDF

> Referencia de html-slides. Léela al ejecutar comandos `uv run slides-*`, al publicar con gist o al exportar PDF.

Los scripts viven en el paquete Python del repositorio (`src/cmx_teach/slides/`), gestionado con uv. No se copian junto al deck: se ejecutan con `uv run` desde la raíz del repo, con la ruta del deck relativa a esa raíz (por ejemplo `cursos/<periodo>/<curso>/semana-NN/alumno/<prefijo>-presentacion-<tema>/index.html`). Primera vez: `uv sync` y `uv run playwright install chromium`.

### `slides-qa` — QA y PDF

`uv run slides-qa <deck>/index.html [--pdf] [--out DIR] [--minutes N]`. Si hay un Chromium preinstalado, `CHROMIUM_PATH=/ruta/al/chromium uv run slides-qa …`. Detecta: errores de JS, elementos fuera del lienzo o en la franja inferior del HUD, texto recortado, fuente < 24 px, scroll horizontal en móvil. Guarda las capturas en `qa/` (o en `--out`); `--pdf` genera `qa/deck.pdf` vectorial con una página por slide. Termina en `OK` o lista los problemas y una sección “REVISAR”. Los avisos de Google Fonts sin red no son errores.

Medidas que imprime:

- **Desborde en px por slide** (`slide desbordada 70px → …`) con la pista de la escalera de corrección (ver `checklist.md`).
- **Texto de plantilla sin reemplazar** (lorem ipsum, TODO, “TÍTULO DEL DECK”, “Título que promete”, “Evento · Fecha”) → PROBLEMAS.
- **Espacio vacío inferior**: el contenido de una slide de contenido termina antes del 60 % de la altura → REVISAR.
- **Diversidad de layouts** (7–9 slides ≥ 6 distintos; ≥ 10 slides ≥ 8) y **mismo layout dos veces seguidas** → REVISAR.
- **`--minutes N`**: si los minutos planeados superan el 90 % de N → REVISAR.

### `mermaid-check` y `svg-check` — validar diagramas

`uv run mermaid-check <deck>/index.html` valida cada bloque Mermaid (sintaxis, versión 11.4.1, tamaño de texto, accesibilidad). `uv run svg-check <deck>/index.html` revisa los SVG en línea (geometría, solapes, texto que no cabe, referencias rotas). Detalle en las skills `mermaid-diagrams` y `svg-illustrations`.

### `slides-pptx` — convertir un PowerPoint

`uv run slides-pptx charla.pptx pptx-extract`. Produce `extracted.json` (título, bloques de texto con nivel, tablas, imágenes, notas) y `assets/` en la carpeta de salida. Muestra al usuario un resumen de lo extraído, luego **rediseña** (no calques el layout del PowerPoint): aplica el plan, las reglas de contenido y un preset; las notas del pptx pasan a `<aside class="notes">`.

### `slides-inline-images` — mantener un solo archivo

`uv run slides-inline-images <deck>/index.html`. Reemplaza cada `src="ruta/local.png"` por un data URI, reescribe el HTML en su lugar e imprime el nuevo tamaño en KB.

### `slides-chart` — gráficas temáticas

`uv run slides-chart datos.json > grafica.svg` (o `--demo` para ver un ejemplo). Imprime en stdout un SVG con las clases `.ch-*` y `--series-N` del diseño UTEZ. Spec JSON:

```text
{"type": "bar" | "hbar" | "line", "title": "texto para aria-label",
 "categories": ["Ene", "Feb"], "series": [{"name": "2026", "values": [1, 2]}],
 "unit": "%" (texto como " min" lleva espacio duro automático),
 "focus": "Feb" (opcional, solo con 1 serie: resalta una categoría; el resto en gris),
 "label": "end" | "max" | "all" (opcional), "width": 1000, "height": 560}
```

### `slides-mermaid` — incrustar Mermaid como SVG

`uv run slides-mermaid <deck>/index.html`. Dibuja cada `pre.mermaid` en Chromium con el tema UTEZ y escribe el SVG en el archivo (la fuente queda en `<!--mmd:…-->`). Re-ejecutable. Carga Mermaid desde el CDN fijado (`mermaid@11.4.1`), así que necesita red; sin ella informa el error.

Antes de embeber, reduce imágenes a ≤ 1600 px de ancho y JPEG/WebP calidad ~80. Mantén el HTML **por debajo de ~1 MB** si se va a publicar en gist (la API de gists trunca archivos grandes).

---

## Publicar con gist + gistpreview

```bash
gh auth status                                    # requiere gh con sesión
gh gist create index.html -d "Título de la charla"  # secreto por defecto; --public para listarlo
# → https://gist.github.com/<usuario>/<ID>
```

Link para compartir: `https://gistpreview.github.io/?<ID>/index.html#1`

Actualizar el mismo gist (el link no cambia):

```bash
gh api -X PATCH gists/<ID> -F "files[index.html][content]=@index.html"
# alternativa: git clone https://gist.github.com/<ID>.git && cp index.html <ID>/ && cd <ID> && git commit -am "update" && git push
```

Notas: “secreto” significa no listado, no privado: cualquiera con el link lo ve. gistpreview carga el gist vía la API de GitHub (límite de ~60 cargas/hora por IP sin sesión), así que para presentar en vivo abre el archivo local; el link es para compartir. El modo presentador también funciona ahí (`#presenter-N` y `#preview-N` van en el hash, compatibles con gistpreview). Si `gh` no está disponible, entrega el archivo y los pasos para subirlo en gist.github.com. Alternativas de hosting: GitHub Pages, Vercel o Netlify Drop con el mismo archivo.

## Exportar PDF

- Rápido: tecla **P** → Guardar como PDF (Chrome/Edge: márgenes “Ninguno”, activar “Gráficos de fondo”).
- Exacto: `uv run slides-qa <deck>/index.html --pdf` → `qa/deck.pdf` (texto vectorial, una página por slide, animaciones en su estado final).

---
