# Reglas técnicas del generador

Para quien modifique `src/cmx_teach/docs/` (generador basado en python-docx + OXML). Tras cualquier cambio, reconstruye los ejemplos de `examples/` y valida con `uv run docs-qa`.

- **Medidas en DXA** (1440 = 1″; Carta 12240×15840; área útil = ancho − márgenes).
- **Tablas:** ancho de columnas (`w:tblGrid`) **y** `w:tcW` en cada celda, tipo `dxa`, sumando el ancho de la tabla; nunca porcentajes (se rompen en Google Docs). Sombreado con `w:shd` `val="clear"` (`solid` pinta negro). Encabezado repetido (`w:tblHeader`) y filas que no se parten (`w:cantSplit`).
- **Listas:** numeración real (`w:numPr` con definiciones en `numbering.xml`: bullet / decimal), nunca `•` escrito; cada lista crea su propia instancia (`w:num`) para reiniciar la numeración.
- **Títulos:** estilos `Heading 1–3` con `w:outlineLvl` (si no, no entran al índice). Sin saltos de nivel.
- **Saltos de página** siempre dentro de un párrafo (`w:br w:type="page"`); nunca `\n` en un run (usa `w:br`).
- **Imágenes:** con texto alternativo (`descr`, `title` y `name` en `wp:docPr`); nunca más anchas que el área útil.
- **Formato de la casa:** presets no APA con márgenes 850 DXA, `sz` entre 18 y 22 (medios puntos) en estilos, `docDefaults`, ejecuciones directas, encabezados, pies y notas, e interlineado `w:line="240"`. Las claves de tamaño viven en `presets.py` (`size`, `h1`–`h3`, `title`, `small`, `cell`, `lead`, `subtitle`, `hdr`, `hdrDist`, `cellLine`, `kvLine`, `titleLine`); el preset `apa` conserva sus valores (su salida debe ser idéntica byte a byte). Los estilos sobrantes de la plantilla de python-docx (y `stylesWithEffects.xml`) se limpian de `sz` y `line` en `styles.py`. `docs-qa` (`layout_warnings`) revisa márgenes, tamaños e interlineado en documentos que no usan Times New Roman como fuente predeterminada.
- **Interlineado:** `w:spacing w:lineRule="auto"` explícito (LibreOffice lo trata como exacto si falta y recorta imágenes).
- **Campos:** el índice (`TOC`, `TOC \c "Tabla"`, `TOC \c "Figura"`) lleva **entradas cacheadas** (se ven en cualquier visor) y `updateFields` solo si faltan los números de página (si no, Word muestra un aviso de seguridad al abrir); las leyendas usan campos `SEQ Tabla \* ARABIC` / `SEQ Figura \* ARABIC` con el número como resultado cacheado.
- **Dos pasadas:** la 1ª escribe `NOMBRE.outline.json` (títulos y leyendas); `docs-qa` renderiza y escribe `NOMBRE.pages.json` (páginas reales); la 2ª pasada inserta esos números en las entradas cacheadas.
- **Valida siempre con `uv run docs-qa`** después de cambiar el generador, y corre `uv run pytest`.
