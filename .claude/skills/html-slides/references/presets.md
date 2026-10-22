# Diseño UTEZ (claro)

> Referencia de html-slides. Léela en la Fase 3 (construcción). Es el único diseño del sistema; ya viene incorporado en `assets/template.html`.

Los tokens salen del logo institucional: verde UTEZ `#009475`, azul `#002e60` y gris `#737375`. Cumplen AA (texto y acentos ≥ 4.5:1 sobre fondo y superficies). El verde puro solo pasa 3.8:1, así que en texto se usa la versión oscurecida `#00735b`; el verde original queda como `--series-1` en las gráficas. El azul institucional es la base del texto (`#0d1d33`); como tono 2 se usa un azul más vivo (`#2563a8`) para que el resaltado se distinga del texto. `--series-1…4` son los colores de gráficas, validados aparte para daltonismo (no uses los acentos de texto como series). Tipografía Saira (cercana a la rotulación del logo) + Source Sans 3. El fondo lleva un trazo de circuito propio y sutil en la esquina inferior izquierda, inspirado en el emblema (no es el emblema).

```html
<link href="https://fonts.googleapis.com/css2?family=Saira:wght@500;700;800&family=Source+Sans+3:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
```
```css
:root{
  --bg:#f7f8f6; --surface:#eef1ee; --surface-2:#e2e8e4; --line:#d0d8d3; --line-strong:#68716d;
  --text:#0d1d33; --text-dim:#47505a;
  --accent:#00735b; --accent-2:#2563a8; --accent-3:#a3470f; --accent-4:#6a3fa0;
  --font-display:"Saira", "Arial Narrow", sans-serif; --display-weight:800;
  --font-body:"Source Sans 3", system-ui, sans-serif;
  --font-mono:"JetBrains Mono", ui-monospace, monospace;
  --radius:12px;
  --bg-art:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600' fill='none' stroke='%23009475' stroke-width='3' stroke-opacity='.10' stroke-linecap='round' stroke-linejoin='round'%3E%3Cg transform='rotate(180 300 300)'%3E%3Cpath d='M600 70H430l-50 50H270'/%3E%3Ccircle cx='256' cy='120' r='12'/%3E%3Cpath d='M600 130H470l-50 50v80'/%3E%3Ccircle cx='420' cy='274' r='12'/%3E%3Cpath d='M600 190H510l-40 40v110l-50 50'/%3E%3Ccircle cx='410' cy='400' r='12'/%3E%3Cpath d='M600 250h-50v180'/%3E%3Ccircle cx='550' cy='444' r='12'/%3E%3Cpath d='M520 0v30l-30 30H350l-40-40'/%3E%3Ccircle cx='300' cy='10' r='12'/%3E%3C/g%3E%3C/svg%3E") left -16px bottom -16px / 360px 360px no-repeat;
  --series-1:#009475; --series-2:#2a78d6; --series-3:#eb6834; --series-4:#6250d6;
  /* --logo:url("data:image/webp;base64,…"); --logo-bg:#ffffff; (ver Marca y logo) */
}
```

Escala tipográfica (lienzo 1920×1080; el piso de `slides-qa` es 24 px). Usa los tokens, no px sueltos:

```css
:root{
  --fs-hero:150px; --fs-h1:104px; --fs-h2:72px; --fs-h3:46px; --fs-lead:44px;
  --fs-body:36px; --fs-small:26px; --fs-stat:150px; --fs-code:30px;
}
```
