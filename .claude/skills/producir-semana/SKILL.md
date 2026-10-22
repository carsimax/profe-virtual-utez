---
name: producir-semana
description: Con el plan de la semana aprobado, genera cada material con las skills existentes, ordena los archivos en alumno/ y docente/, corre course-lint y los agentes revisores. Usar al pedir /producir-semana NN o producir los materiales de una semana.
---

# Producir semana

`/producir-semana NN`. Requiere `00-plan.md` aprobado por el profesor; si no lo está, detente y pide `planear-semana`.

## Pasos
1. Lee `00-plan.md` (sección `## Por producir`) y `curso.md`.
2. Para cada fila, lee primero su plantilla `.claude/rules/plantilla-*.md` y genera con la skill que corresponda; no repitas sus reglas aquí:
   - decks: `html-slides` (carpeta `alumno/00-presentacion/` o `alumno/sN-00-presentacion-<tema>/`);
   - exámenes, prácticas, tareas, rúbricas y planeaciones .docx: `word-docs` (`docs-build fuentes/<x>.json`, con `--clave` cuando haya clave);
   - diagramas e ilustraciones: `mermaid-diagrams`, `svg-illustrations`.
3. Ordena: los .docx de la semana a `alumno/`, las `_clave` a `docente/`, con el prefijo `sN-NN-` del plan. Nunca dejes una clave en `alumno/`.
4. Revisa que los enlaces de `00-plan.md` apunten a los archivos y secciones finales.
5. Corre `uv run course-lint cursos/<periodo>/<curso>/semana-NN` y corrige hasta que no haya errores.
6. Lanza el agente `revisor-alineamiento` sobre cada material, y `alumno-simulado` sobre cada examen, práctica y tarea (pasa la ruta de `alumno/`). Pueden ir en paralelo.
7. Corrige los hallazgos de severidad alta y media que no cambien la intención del plan; reporta el resto sin tocarlos. Si corriges, vuelve a correr `course-lint`.

## Salida
Lista de archivos producidos (ruta absoluta), resultado de `course-lint`, tablas de hallazgos corregidos y pendientes, **[CONFIRMAR]** abiertos y 2–4 sugerencias. El profesor tiene la última palabra sobre los hallazgos pendientes.
