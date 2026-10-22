---
name: docs-to-md
description: Convierte PDF, Word (.doc/.docx), Excel (.xls/.xlsx) y PowerPoint a Markdown con `uv run docs-to-md`. Usar al pedir convertir o pasar a Markdown un PDF, Word, Excel o PowerPoint, o al leer una hoja de asignatura, secuencia didáctica o el modelo educativo que viene en PDF, Word o Excel.
---

# Documentos a Markdown

Convierte documentos institucionales a `.md` para poder leerlos y citarlos. Construido sobre [firecrawl/anydoc](https://github.com/firecrawl/anydoc) (MIT); aquí solo hay un wrapper delgado.

## Cuándo usar

Hojas de asignatura, secuencias didácticas, modelo educativo o reglamentos que llegan en PDF, Word, Excel o PowerPoint (también odt, rtf, csv, epub) y necesitas leerlos o trabajar con ellos.

## Comando

```bash
uv run docs-to-md asignaturas/poo.pdf --out-dir asignaturas/poo
uv run docs-to-md institucional/modelo-educativo.docx institucional/reglamento.pdf   # junto a cada original
```

Escribe `<nombre>.md` por archivo, imprime la ruta y sigue con los demás si uno falla. `--out-dir` se crea si no existe.

| Código | Significado |
|---|---|
| 0 | Todo convertido |
| 1 | Algún archivo falló (mensaje en stderr) |
| 3 | Páginas escaneadas: requiere OCR |

## Dónde guardar

- Hojas de asignatura → `asignaturas/<asignatura>/hoja-asignatura.md`
- Modelo educativo, reglamentos → `institucional/<nombre>.md`
- Secuencias → `asignaturas/<asignatura>/secuencia-<periodo>-<cuatrimestre>.md`

Conserva el original junto al `.md`. Renombra a minúsculas con guiones (`u2-practica-03.md`).

## Revisar antes de confiar

Lee el `.md` generado y comprueba encabezados, tablas (cada hoja de Excel sale como tabla) y que sobrevivieron las horas y los resultados de aprendizaje. Marca lo dudoso como **[CONFIRMAR]**; nunca inventes datos. En documentos largos lee por partes, no todo de golpe.

### Limpieza después de convertir (PDF de diseño)

Los PDF maquetados (modelo educativo, reglamentos) suelen salir con tres defectos. Corrígelos una sola vez a mano; no escribas un limpiador automático.

1. **Portada, directorio e índice:** bórralos. Empieza con un solo `#` con el título oficial y una línea en cursiva que diga que es conversión con anydoc y revisión manual.
2. **Encabezados:** capítulos con `##`, secciones con `###`. Quita los encabezados falsos que son fragmentos de figuras o números de página.
3. **Párrafos partidos por salto de página:** une al anterior todo párrafo que empiece en minúscula; corrige guiones de corte (`rel- ación`).
4. **Figuras y tablas dibujadas:** su texto sale revuelto. Abre la página con `Read` y `pages` (el PDF se ve como imagen) y transcribe a tabla Markdown o Mermaid, conservando cada número (horas, créditos, porcentajes). Antecede `> Transcripción de la Figura N (p. X del PDF).` y usa **[CONFIRMAR]** en lo ilegible.

Ejemplo terminado: `institucional/modelo-educativo-2024.md`.

## OCR

Código 3 = el PDF son imágenes escaneadas. `--ocr hosted` **sube el documento completo** a Firecrawl Parse (servicio externo). Pide consentimiento explícito al profesor antes; nunca lo uses por defecto.

Si un PDF que parece escaneado sale con código 1 (por ejemplo, páginas de imagen sin texto detectable), trátalo igual que el código 3: pide consentimiento antes de usar `--ocr hosted`.
