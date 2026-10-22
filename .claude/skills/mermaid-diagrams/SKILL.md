---
name: mermaid-diagrams
description: Crea, valida y corrige diagramas Mermaid (11.4.1) legibles para clase y diapositivas. Usar al pedir un diagrama, Mermaid, flujo, UML, clases, secuencia, estados, ER, entidad-relación, gitGraph o "dibuja el proceso/arquitectura". Incluye verificación con `uv run mermaid-check`.
---

# Diagramas Mermaid

Diagramas de texto que se versionan, se corrigen rápido y heredan el tema del deck. Funciona solo o desde `html-slides`. Versión fija: **Mermaid 11.4.1** (CDN jsDelivr); lo que llegó en v12 no existe aquí.

## Cuándo usar Mermaid y cuándo SVG a mano

| Usa Mermaid | Usa SVG a mano (skill `svg-illustrations`) |
|---|---|
| Procesos, algoritmos, UML, secuencias, estados, ER, ramas Git | Ilustraciones, isométricos, composición espacial exacta |
| Más de ~5 iteraciones de edición esperadas | Posición pixel a pixel, anotaciones, callouts |
| El layout automático basta | Más de ~15 nodos o jerarquía visual propia |

Regla: si necesitas mover una caja "tantito a la derecha", es SVG, no Mermaid.

## Elegir el tipo

| Quiero mostrar… | Tipo | Notas |
|---|---|---|
| Un proceso, algoritmo o decisión | `flowchart` | `LR` ≤ 6 nodos, `TB` para secuencias largas |
| Mensajes entre actores en el tiempo | `sequenceDiagram` | 3 a 5 participantes |
| Clases, herencia, interfaces (UML estático) | `classDiagram` | ≤ 6 clases |
| Ciclo de vida de un objeto | `stateDiagram-v2` | |
| Modelo de datos | `erDiagram` | ≤ 5 entidades |
| Ramas y fusiones de Git | `gitGraph` | |
| Capas de un sistema | `flowchart` + `subgraph` | Evita `architecture-beta` y `block-beta` en slides |
| Ideas jerárquicas / hitos | `mindmap` / `timeline` | Sin `accTitle` en mindmap |

No existen en 11.4.1: `radar`, `treemap`, `look: neo`, ELK incluido. `mermaid-check` los marca como error.

## Reglas de legibilidad

- **≤ 12 nodos** por diagrama (clases ≤ 6). Si hay más, divide en dos diapositivas o cambia a SVG.
- Texto renderizado **≥ 14 px** en el área útil de la diapositiva (1664×700); el checker lo mide.
- Etiquetas cortas (1 a 4 palabras); verbos en las aristas no obvias (`valida`, `envía`).
- IDs estables y etiquetas entre comillas: `svc["Servicio de usuarios"]`.
- Declara los nodos en orden de flujo; usa un nodo "hub" para reducir cruces; `---->` alarga una arista.
- `subgraph` agrupa capas (su `direction` se ignora si un nodo se enlaza hacia afuera).
- Un diagrama = una idea. Resalta lo que importa, no todo.

## Tema

- En un deck, el tema **sale del diseño UTEZ**: `renderMermaid` lee las variables CSS y las pasa a `theme:'base'`. No lo repitas en el diagrama.
- Mermaid solo acepta **colores hexadecimales** (nada de `var()`, `rgb()` salvo `box`, ni nombres).
- Resaltar un nodo: `classDef foco fill:#e2e8e4,stroke:#00735b,color:#0d1d33` y `A:::foco` o `class A foco`. No llames `default` a una clase.
- `linkStyle N` cuenta las aristas desde 0, en orden de definición.
- El CSS externo pierde contra los estilos de Mermaid; usa `classDef`.
- No codifiques significado solo con color: añade texto, forma o línea punteada.

## Seguridad de sintaxis

- `end` en minúscula rompe flowchart y sequence: escribe `End` o `"end"`.
- Entre comillas toda etiqueta con `() [] {} : ; # " / < >`. Entidades: `#quot;`, `#35;`, `#59;`.
- `A---oB` y `A---xB` crean aristas con círculo o cruz; deja espacios.
- En sequence `;` termina la sentencia. Los comentarios `%%` van en su propia línea.
- Saltos de línea: `<br>` dentro de etiquetas con comillas, o cadenas markdown.
- Nombres de clase solo con letras, números, `_` y `-`; genéricos con `~T~`, nunca `<T>` ni comas.
- No uses sintaxis posterior a 11.4.1: `@{shape}`, `autonumber start step`, ER `?`, half-arrows.

## Accesibilidad

Pon `accTitle:` y `accDescr:` justo después de la palabra clave, en todo diagrama (excepto `mindmap`):

```
flowchart LR
  accTitle: Flujo de inicio de sesión
  accDescr: Una solicitud se valida y llega al tablero o a un error.
```

Contraste ≥ 4.5:1 (el diseño UTEZ ya lo cumple). Describe en `accDescr` la relación, no el aspecto.

## Flujo de trabajo

1. **Escribe** el `.mmd` (o el `pre.mermaid` en la diapositiva) con el tipo de la tabla y ≤ 12 nodos.
2. **Valida**: `uv run mermaid-check diagrama.mmd` (o `deck/index.html`). Añade `--render out/` para PNG, `--json` para máquina.
3. **Inspecciona** los PNG (`out/diagram-NN.png`) y los avisos.
4. **Corrige** con el mensaje del parser (indica la línea). Máximo **3 rondas**; si persiste, simplifica o pasa a SVG.
5. **En decks**: ejecuta `uv run slides-mermaid deck/index.html` para incrustar el SVG (queda la fuente en `<!--mmd:…-->`, funciona sin red y en PDF); luego `uv run slides-qa`.

Salida de `mermaid-check`: líneas `ERROR|WARN <n> <regla> <mensaje>` y un resumen. Reglas: `parse`, `unsupported-type`, `render`, `too-many-nodes`, `too-many-edges`, `small-text`, `text-overflow`, `a11y-title`, `a11y-descr`, `lowercase-end`, `unquoted-special`. Código de salida 0 sin errores, 1 con errores, 2 sin archivo legible o sin diagramas. Necesita red (carga Mermaid del CDN).

## Lista de verificación

- [ ] Tipo correcto según la tabla; una sola idea.
- [ ] ≤ 12 nodos (clases ≤ 6); etiquetas cortas.
- [ ] `accTitle` y `accDescr` presentes.
- [ ] Sin `end` en minúscula ni caracteres especiales sin comillas.
- [ ] Colores en hex; el tema viene del diseño UTEZ del deck.
- [ ] `mermaid-check` sin errores y sin avisos de `small-text` o `text-overflow`.
- [ ] En decks: `slides-mermaid` ejecutado.

## Archivos

| Archivo | Para qué | Cuándo leerlo |
|---|---|---|
| `SKILL.md` | Decisión de tipo, reglas y flujo | Siempre |
| `references/cheatsheet.md` | Sintaxis mínima validada por tipo (flowchart, clases UML, secuencia, estados, ER, gitGraph, mindmap, timeline) y trampas | Al escribir un tipo concreto |

## Fuentes

Documentación Mermaid: [teoría de temas](https://mermaid.js.org/config/theming.html), [flowchart](https://mermaid.js.org/syntax/flowchart.html), [classDiagram](https://mermaid.js.org/syntax/classDiagram.html), [sequence](https://mermaid.js.org/syntax/sequenceDiagram.html), [state](https://mermaid.js.org/syntax/stateDiagram.html), [ER](https://mermaid.js.org/syntax/entityRelationshipDiagram.html), [gitGraph](https://mermaid.js.org/syntax/gitgraph.html), [accesibilidad](https://mermaid.js.org/config/accessibility.html), [API de uso](https://mermaid.js.org/config/usage.html). Soporte de 11.4.1 según los chunks de [unpkg](https://app.unpkg.com/mermaid@11.4.1/files/dist/chunks/mermaid.esm.min). Ideas de flujo validar→renderizar→corregir: skills comunitarias `mermaid-diagrams` (ccheney) y `beautiful-mermaid` (lukilabs).
