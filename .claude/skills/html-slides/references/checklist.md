# QA, crítica y checklist

> Referencia de html-slides. Léela en la Fase 4 (QA) y antes de entregar.

## Pre-flight (antes de escribir HTML)

- Cada clase que uses existe en `assets/template.html` (`grep -c 'l-nombre' assets/template.html`). Si no existe, defínela en la sección 5 y 7 del CSS antes de usarla.
- El plan fija layout y tono (`data-tone`) por slide, y la diversidad de layouts cumple la cuota (ver `layouts.md`).
- Cada slide de contenido tiene su visual definido en el plan (columna `visual`).

## Modos de densidad

| Modo | Cuerpo por slide |
|---|---|
| `ponente` | 1–3 viñetas o un visual; el detalle va a las notas |
| `lectura` | 4–8 viñetas o 4–6 tarjetas, con pies explicativos |

En ambos modos: ≤ 6 elementos por slide. Si no cabe, **divide la slide; no encojas la fuente**.

## Prueba de borrado y acción cognitiva

- **Prueba de borrado de texto:** quita mentalmente el texto de la slide. Si el visual no comunica la idea, rediseña el visual.
- **Acción cognitiva → visual:**

| Acción cognitiva | Visual |
|---|---|
| Entender un proceso | flujo (`l-steps`, Mermaid flowchart) |
| Comparar | un solo visual de la diferencia (`l-compare`, barras con foco) |
| Magnitud | tamaño codificado (cifra grande, barra) |
| Ubicar en el tiempo | `l-timeline` |
| Estructura o jerarquía | diagrama SVG de cajas, árbol |
| Decorar | no cuenta como visual |

## Escalera de corrección de desbordes (con medida)

`slides-qa` imprime los px de desborde por slide. Aplica la acción de su rango:

| Desborde | Acción |
|---|---|
| 1–40 px | ajusta espaciado: baja un paso en `--sp-*` / `--gap` de esa slide |
| 40–90 px | compacta huecos y paddings; quita un elemento secundario |
| 90–160 px | ajusta el texto (recorta, reescribe) o divide la slide |
| > 160 px | cambia de layout o recorta contenido |

Nunca bajes la fuente por debajo de los tokens ni metas scroll. Título de 3 o más líneas: reescríbelo.

## Cortes y contenido pedagógico

- [ ] Cada parada (actividad, práctica, demostración o ejercicio guiado, coevaluación, examen, cierre) tiene su slide `l-corte` con tipo, duración, modalidad, material, producto y «Regresamos a».
- [ ] Entre cortes consecutivos hay una slide de transición de 0 minutos (si no, `slides-qa` marca layout repetido).
- [ ] El material que debe seguir proyectado durante una actividad está en una slide de apoyo de 0 minutos.
- [ ] Todo procedimiento se enseña paso a paso antes de usarse en un ejemplo o práctica.

## Orden de QA

1. Desborde (px medidos) → 2. solapes (SVG) → 3. choque con la franja del HUD → 4. huecos bajo el margen mínimo y espacio vacío inferior → 5. columnas desalineadas → 6. contraste → 7. texto de plantilla sin reemplazar (lorem, TODO, textos de ejemplo) → 8. diversidad y ritmo de layouts → 9. minutos vs duración (≤ 90 %).

Con diagramas: `uv run svg-check <deck>/index.html` y `uv run mermaid-check <deck>/index.html` antes de `slides-qa`. Visibilidad por `visibility`/`opacity`, nunca alternando `display` (la plantilla ya cumple).

## Crítica de cinco ejes (antes de entregar)

Puntúa 0–10 por eje y reporta:

| Eje | Pregunta |
|---|---|
| **Idea (veto)** | ¿La tesis es clara y específica? Si cambias el tema/cliente y el deck sigue “funcionando”, es una plantilla genérica. Si saca ≤ 5, la nota total no pasa de 6. |
| Jerarquía | Entrecerrando los ojos, ¿se ve primero el título y luego la figura? ¿Título ≥ 2.5× el cuerpo? ¿Un solo punto focal? |
| Ejecución | Rejilla y tokens de espaciado consistentes, ≤ 3–4 colores, ≤ 2 familias, sin desbordes ni solapes en SVG. |
| Función | ¿Cada elemento se gana su lugar? Si lo borras y no se pierde nada, sobra. ¿El layout corresponde a la cantidad y tipo de contenido? |
| Coherencia e innovación | ¿Todas las slides parecen del mismo deck y del diseño UTEZ? ¿El ritmo de layouts varía y hay al menos un momento memorable? |

Salida con tres bloques: **Mantener** (2–3 cosas que funcionan) · **Arreglar** (con severidad `fatal` / `importante` / `mejora` y el cambio concreto) · **Quick wins** (3 cambios de 5 minutos). Aplica los fatales e importantes antes de entregar.

## Checklist final

- [ ] Un solo `.html`; imágenes embebidas; recursos externos solo Google Fonts (con fallbacks) y el respaldo de Mermaid por CDN, que no se usa si los diagramas ya están incrustados.
- [ ] Runtime y CSS de impresión intactos; tokens UTEZ y `<link>` de fuentes de la plantilla sin cambios.
- [ ] Cada slide: `data-id`, `data-chapter`, `data-minutes`, kicker (salvo exentas), título-afirmación, ≤ 6 `.reveal`; `<html lang>` y `<title>` correctos.
- [ ] Ritmo: cuota de diversidad cumplida, sin el mismo layout dos veces seguidas, respiro cada 3–4 slides (decks de 8 o más); cierre con siguiente paso concreto.
- [ ] Cero cifras inventadas; `[DATO PENDIENTE]` visible donde falte; cero texto de plantilla.
- [ ] Cada slide de contenido con un visual que carga la idea; íconos del sprite (no emoji); diagramas validados con `svg-check` / `mermaid-check`; gráficas de `slides-chart`; logo solo si el usuario lo dio.
- [ ] Notas en todas las slides si el uso es `ponente`.
- [ ] `slides-qa` en `OK` (con `--minutes N` si hay duración fija) y capturas revisadas (escritorio y móvil).
- [ ] Crítica aplicada; entrega con ruta, controles y oferta de gist/PDF.
