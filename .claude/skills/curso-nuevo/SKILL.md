---
name: curso-nuevo
description: Crea el curso.md de un curso nuevo a partir de la hoja de asignatura y la secuencia. Usar al pedir /curso-nuevo <slug> <periodo>, crear o dar de alta un curso, o cuando falte curso.md antes de planear una semana.
---

# Curso nuevo

`/curso-nuevo <slug> <periodo>` (por ejemplo `/curso-nuevo poo 2027-1`).

## Pasos
1. Lee `asignaturas/<slug>/hoja-asignatura.md` y `secuencia-<periodo>-<cuatrimestre>.md`; empieza por su front matter. Si hay varias secuencias, pregunta cuál (cuatrimestre) en una sola pregunta.
2. Lee `.claude/rules/plantilla-planeacion.md` (sección `curso.md`), `evaluacion.md` y `datos-a-pedir.md`.
3. Crea `cursos/<periodo>/<slug>-<cuatrimestre>/curso.md` con las seis secciones de esa plantilla. Copia el RA y las ponderaciones de las fuentes; lo que no esté (grupo, horario, duración, fechas oficiales) va como **[CONFIRMAR]**.
4. Escala: propón la que marca `evaluacion.md` para el cuatrimestre y déjala **[CONFIRMAR]** hasta que el profesor la confirme.
5. Deja la sección `## Avance` con su tabla vacía.
6. Corre `uv run course-lint cursos/<periodo>/<slug>-<cuatrimestre>`; corrige los errores (tabla de saberes por unidad suma 100) y reporta los avisos de `[CONFIRMAR]`.

## Salida
Ruta del `curso.md`, lista de **[CONFIRMAR]** pendientes y 2–4 sugerencias. Detente: no planees semanas sin que el profesor responda o pida avanzar.
