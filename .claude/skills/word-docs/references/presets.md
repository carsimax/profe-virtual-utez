# Presets

Elige con `"preset"` en el spec. Para otro color de marca usa `theme` (verifica contraste ≥ 4.5:1 en texto).

| Preset | Uso | Tipografía y color |
|---|---|---|
| `utez` | Documentos académicos e institucionales UTEZ | Arial; títulos azul institucional `#002E60`, acentos verde UTEZ (`#00735B` en texto, `#009475` en líneas y gráficas); tablas con encabezado azul y filas alternas |
| `apa` | Reportes de investigación, estadía, tesis | Times New Roman 12, interlineado doble, sangría 1.27 cm, márgenes 2.54 cm, títulos APA 7 (N1 centrado negrita, N2 negrita, N3 negrita cursiva), número de página arriba a la derecha, tablas de tres líneas, leyendas APA ("**Tabla 1**" + título en cursiva arriba) |
| `corporativo` | Informes ejecutivos, propuestas | Calibri; azul marino y azul medio |
| `tecnico` | SRS, manuales, documentación de software | Calibri + Consolas; títulos numerados 1 / 1.1; tablas de líneas |
| `editorial` | Ensayos, boletines, textos largos de lectura | Georgia; acento vino |

## Formato de la casa

`utez`, `corporativo`, `tecnico` y `editorial` comparten: márgenes de **1.5 cm** (850 DXA) por lado, encabezado y pie a 0.75 cm del borde, fuentes de **9–11 pt**, interlineado **sencillo (1.0)**.

| Elemento | Tamaño |
|---|---|
| Título de portada y H1 | 11 pt, negrita, color de títulos del preset (utez: azul institucional) |
| H2 | 10.5 pt, negrita |
| H3 | 10 pt, negrita cursiva |
| Cuerpo, listas, tablas, kv, preguntas, rúbricas, firmas | 10 pt |
| Notas al pie, leyendas, encabezado, pie, código, código en línea, `small` | 9 pt |

`apa` queda igual (APA 7: Times New Roman 12 pt, doble espacio, 2.54 cm) y es la única excepción; `docs-qa` lo reconoce por su fuente predeterminada Times New Roman.

## Defaults

Tamaño Carta, idioma `es-MX`; `utez` para lo académico/institucional, `apa` para trabajos de investigación, `tecnico` para documentación de software. Declara los supuestos al inicio.

## Notas

- Todas las fuentes existen en Word (Windows/Mac) y tienen equivalentes métricos en LibreOffice.
- La jerarquía usa peso, color y estilo dentro de 9–11 pt (ver "Formato de la casa"); cuerpo en gris muy oscuro, no negro puro (salvo APA).
- Las gráficas y diagramas (`docs-visuals --preset P`) toman los colores del preset; úsalo con el mismo preset del documento.
- **Logo:** solo el archivo que dé el profesor (PNG con transparencia, ideal). Va en la portada y, pequeño, en el encabezado.
