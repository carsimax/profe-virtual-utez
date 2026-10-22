# Recetas por tipo de documento

Estructuras de partida. Si la institución tiene formato oficial, ese manda (modos C/D en `formatos-y-edicion.md`). En materiales docentes aplican también las plantillas de `.claude/rules/plantilla-*.md` y `.claude/rules/evaluacion.md`.

| Documento | Preset / portada | Estructura recomendada |
|---|---|---|
| **Planeación / secuencia didáctica** | `utez`, portada con `fields` (asignatura, docente, cuatrimestre/grupo, periodo) | `kv` datos generales (unidad, horas de saber y saber hacer, semanas, modalidad) → resultado de aprendizaje (uno por unidad) → saber / saber hacer / saber ser y convivir → tabla de secuencia (momento · actividad · evidencia · tiempo) → evaluación (porcentajes por evidencia, ≥ 2 tipos: auto, co, hetero) + rúbrica → recursos → referencias → firmas (docente, director/a) |
| **Práctica de laboratorio** | `utez`, sin portada | `kv` (práctica núm., unidad, duración, equipo) → objetivo → material → desarrollo en partes A (ejemplo resuelto) / B (con huecos) / C (problema propio): cada paso de A y B es una ficha (`h3` con el subobjetivo + `table` de dos columnas con qué haces · por qué · cómo · predicción (fila vacía para escribir) · resultado intermedio · cómo verificas · error típico; el cómo va en `code`) → resultados esperados (figura/tabla) → preguntas de cierre → rúbrica o lista de cotejo (`checklist`). **Versión docente:** segundo spec `fuentes/<prefijo>_clave.json` con `output` a `docente/` (`--clave` solo marca reactivos de `questions`, no sirve aquí): mismas etiquetas de paso → resultado intermedio esperado, ≥ 2 concepciones erróneas con pregunta detectora (`table`), puntos de control con minuto, qué recortar, preguntas para circular, errores con mensaje literal. Detalle en `.claude/rules/plantilla-practica.md` |
| **Examen** | `utez`, sin portada | encabezado institucional (header) → `questions` con `instructions` (tiempo, valor total, material permitido); versión del docente con `--clave`; puntaje total visible |
| **Rúbrica / lista de cotejo** | `utez`, horizontal si hay ≥ 5 niveles | `kv` (actividad, unidad, valor) → `rubric` (niveles NA \| SA \| DE \| AU o la escala confirmada) → espacio de retroalimentación → firmas |
| **Reporte técnico / de proyecto** | `tecnico` o `utez`, portada, `toc` | resumen ejecutivo → introducción → desarrollo → resultados (tablas/figuras) → conclusiones → referencias → anexos |
| **SRS / documento de requisitos** | `tecnico`, portada con versión/estado, `numberedHeadings` | introducción (propósito, alcance, definiciones) → descripción general → requisitos funcionales (tabla ID · requisito · prioridad · criterio de aceptación) → no funcionales → modelo de datos (Mermaid `erDiagram`) → casos de uso → trazabilidad |
| **Manual de usuario** | `corporativo` o `tecnico`, portada, `toc` | requisitos → instalación (`numbers`) → tareas frecuentes (una por H2, con capturas reales) → solución de problemas (tabla síntoma · causa · solución) → glosario |
| **Oficio / carta** | `utez`, sin portada, `pageFormat: "simple"` | lugar y fecha (derecha) → número de oficio → asunto → destinatario (nombre, cargo, "Presente") → cuerpo breve → "Atentamente" → `signatures` → c.c.p. en `small` |
| **Minuta** | `corporativo`/`utez` | `kv` (fecha, hora, lugar, asistentes) → orden del día (`numbers`) → acuerdos (tabla acuerdo · responsable · fecha compromiso) → firmas |
| **Informe ejecutivo** | `corporativo`, portada | conclusión primero (`p` lead) → 3–5 hallazgos con cifras → recomendaciones → anexos |
| **Reporte de estadía / tesis** | `apa`, `cover: "apa"` | front: `title` Resumen (+ Abstract), `toc`, `lot`, `lof` → cuerpo: Introducción, Marco teórico, Metodología, Resultados, Discusión/Conclusiones → back: `references`, anexos |

## Completitud por escenario

- Examen: datos del alumno, puntaje por reactivo y total; saber evaluado por reactivo; clave aparte.
- Planeación: horas y evidencias con su porcentaje, que sume 100 %; los tres saberes; un solo resultado de aprendizaje; sin evidencias nuevas en el cierre.
- Oficio: número, asunto y firma.
- Rúbrica: niveles con valor, alineados a la escala confirmada.
- SRS: IDs únicos de requisito.

## Datos del profesor y la institución

- Nombre y cargo del docente: sección "Profesor" de `CLAUDE.md` (portadas, encabezados y firmas).
- Clave de asignatura, fechas oficiales, escala, ponderaciones que no estén en el proyecto: `[CONFIRMAR]`.
- Contenido que simplemente falta (cifras, nombres de terceros): `[DATO PENDIENTE]`.

## Ejemplos

Specs completos en `examples/`: `planeacion.json`, `examen.json` (genera también la clave con `--clave`), `apa.json`, `oficio.json`, `srs.json`; figuras fuente en `examples/figs/`.
