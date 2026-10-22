# Recursos visuales, íconos y marca

> Referencia de html-slides. Léela en la Fase 3 al elegir el visual de cada slide.

Elige el recurso por lo que la slide necesita mostrar, no por decoración:

| Necesitas mostrar | Recurso | Cómo |
|---|---|---|
| Un concepto en una palabra (tarjeta, lista) | Ícono del sprite | `<span class="ico-badge"><svg class="ico"><use href="#i-bolt"/></svg></span>` |
| Arquitectura o mecanismo con posiciones que importan | Diagrama SVG a mano | skill `svg-illustrations` (clases `.d-*`) |
| Flujo, secuencia, estados, ER, clases UML, gitGraph | **Mermaid** | skill `mermaid-diagrams`; `<pre class="mermaid">` dentro de `figure.fig` |
| Cantidades, tendencias, comparaciones numéricas | **Gráfica** | `slides-chart` → pega el `<svg class="chart">` |
| Una metáfora o escena (capas, embudo, puente, antes/después) | **Ilustración SVG propia** | skill `svg-illustrations` (clases `.ill-*` + íconos) |
| El producto real, una persona, un lugar | Captura o foto real | `img` embebida; si no la hay, `.placeholder` honesto |

**Íconos (sprite incluido):** `check`, `x`, `arrow`, `alert`, `info`, `user`, `users`, `code`, `terminal`, `database`, `server`, `cloud`, `lock`, `bolt`, `clock`, `chart`, `sliders`, `book`, `branch`, `bulb`, `target`, `search`, `globe`, `cpu`, `school`, `robot`, `layers`, `flow`. Uso: `<svg class="ico"><use href="#i-NOMBRE"/></svg>` (toma `currentColor`; tamaño = `font-size`). Dentro de un diagrama o ilustración: `<use href="#i-database" x="…" y="…" width="48" height="48" class="d-ico tone"/>` (sin `<svg>` anidado). Si falta uno, agrégalo al sprite como `<symbol id="i-nombre" viewBox="0 0 24 24">` con trazos de 1.75 en rejilla de 24, mismo estilo (líneas, puntas redondeadas, sin relleno). Un ícono siempre acompaña a un texto; nunca lo reemplaza.

**Diagramas e ilustraciones SVG:** los escribe la skill `svg-illustrations` (receta, reglas y `uv run svg-check <deck>/index.html`). **Diagramas Mermaid:** los escribe la skill `mermaid-diagrams` (`uv run mermaid-check <deck>/index.html`; para incrustarlos como SVG, `uv run slides-mermaid`). Ambas usan las clases y el tema del preset; no repitas aquí sus reglas.

**Gráficas (`slides-chart`):** escribe un JSON con `type` (`bar`, `hbar`, `line`), `categories`, `series` (≤ 4), `unit` y opcional `focus` (solo con 1 serie: resalta una categoría y apaga el resto), `label` (`all`, `max`, `end`); ejecuta `uv run slides-chart datos.json > grafica.svg` y pega el SVG en `figure.fig`. La fuente y si son datos de ejemplo van en el `figcaption`. Reglas: un solo eje (nunca doble eje Y), nada de pies, donas ni 3D; ≤ 12 categorías; leyenda automática con ≥ 2 series; etiquetas selectivas; el texto va en colores de texto, nunca en el de la serie; cifras con fuente en el pie o en notas; cada barra o punto lleva `<title>` con su valor (tooltip al pasar el mouse) y el SVG lleva `<desc>` con la tabla de datos.

## Marca y logo

- Usa solo el logo que te dé el usuario (archivo en su carpeta o adjunto). **Nunca** lo redibujes, vectorices ni inventes uno.
- Conviértelo y pégalo como variable dentro del bloque de tokens (`1. DISEÑO UTEZ`):

```bash
uv run python -c "import base64,sys;from PIL import Image;im=Image.open(sys.argv[1]).convert('RGBA');im=im.crop(im.getbbox());w=400;im=im.resize((w,round(im.height*w/im.width)));im.save('logo.webp','WEBP',quality=80);print('--logo:url(\"data:image/webp;base64,'+base64.b64encode(open('logo.webp','rb').read()).decode()+'\");')" logo.png
```

- Si el logo tiene fondo blanco opaco, usa una versión con transparencia o pon `--logo-bg:#ffffff;` para que se vea como pastilla intencional.
- Con `--logo` definido aparece en la esquina superior derecha de cada slide (salvo portada, `.bleed` y slides con clase `no-logo`). En la portada agrega `<div class="brand-logo reveal" role="img" aria-label="Nombre"></div>` antes del kicker.
- UTEZ: si el usuario no adjunta el logo, pídeselo; el diseño UTEZ funciona sin él.
