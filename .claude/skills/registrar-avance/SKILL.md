---
name: registrar-avance
description: Anota en curso.md lo que realmente pasó en clase y propone reajustar las semanas siguientes si hubo retraso. Usar al pedir /registrar-avance, anotar el avance real, reportar un retraso o replanificar semanas.
---

# Registrar avance

`/registrar-avance [NN]` en el curso activo. Sin NN, usa la última semana planeada sin registro.

## Pasos
1. Lee `curso.md` (calendario y `## Avance`) y `semana-NN/00-plan.md`.
2. Pregunta en una sola lista breve lo que falte: fecha, qué se cubrió, qué no, incidencias (suspensión, ritmo del grupo).
3. Agrega o actualiza el renglón de la semana en `## Avance` (tabla `Semana | Fecha | Planeado | Real | Ajuste`; formato en `plantilla-planeacion.md`). Solo hechos en «Real»; sin inventar fechas oficiales (**[CONFIRMAR]**).
4. Si hubo retraso, propón el reajuste de las semanas siguientes (qué se mueve, qué se recorta, qué evidencia cambia) respetando RA, horas y ponderaciones de la unidad. Presenta la propuesta y **detente**: aplícala al calendario y a los `00-plan.md` solo con la aprobación del profesor (después, `planear-semana` para replanear).
5. Corre `uv run course-lint cursos/<periodo>/<curso>`; corrige los errores de lo que escribiste.

## Salida
Renglón registrado, propuesta de ajuste (si aplica) y resultado de `course-lint`.
