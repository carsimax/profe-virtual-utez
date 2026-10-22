---
paths:
  - "cursos/**/00-plan.md"
  - "cursos/**/curso.md"
  - "asignaturas/**/secuencia-*.md"
---
# Plantilla: planeación / secuencia didáctica

1. **Datos generales:** programa, asignatura, cuatrimestre, grupo, periodo, docente, propósito, competencia a la que contribuye y su tipo, créditos, modalidad, horas de saber, saber hacer, totales y por semana.
2. **Unidad:** nombre, propósito, horas, % de la unidad, temas.
3. **Saberes:** Saber (dimensión conceptual) / Saber hacer (actuacional) / Saber ser y convivir (socioafectiva).
4. **Tabla de evaluación:**

| Semanas | Resultado de aprendizaje | Evidencia | Tipo de evaluación | Ponderación | Instrumento |
|---|---|---|---|---|---|

5. **Secuencia por sesión**, en fases Apertura / Desarrollo / Cierre:

| Fase | Métodos y técnicas | Actividades docente | Actividades estudiantes | Evidencia | Recursos | Minutos |
|---|---|---|---|---|---|---|

6. **Referencias.**

Verifica: un solo resultado de aprendizaje, tres saberes, ≥2 tipos de evaluación, ponderaciones = 100%, sin evidencias evaluadas en el cierre.

## Presupuesto de minutos por sesión (40/60)

Base: `.claude/referencia/pedagogia-evidencia.md`, sección 3.
- Exposición (▶) ≤ 40 % y práctica (PARADA) ≥ 60 % de los minutos de la sesión; si la hoja es más práctica, manda la hoja. La apertura y el cierre dirigidos por el docente cuentan como ▶.
- Parte la exposición en segmentos de ~10–12 min, cada uno seguido de una PARADA (pregunta, predicción o mini práctica). Es regla de diseño (puntos de recuperación y verificación), no un dato de atención.
- Abre con 2–3 preguntas de recuperación de sesiones anteriores y cierra con un boleto de salida de 1–3 reactivos (sin contenido ni evidencias nuevas).
- El plan declara al pie de cada sesión: `▶ X min (Y %) · PARADA Z min (W %)`, con la suma igual a la duración **[CONFIRMAR]** de la sesión.

Si el profesor pide el material en Word (.docx), usa la skill `word-docs` con su receta de planeación didáctica (`.claude/skills/word-docs/references/recetas.md`).

## `curso.md` (una vez por curso)

Ruta: `cursos/<periodo>/<slug>-<cuatrimestre>/curso.md`. Se crea desde la secuencia y la hoja, antes de planear cualquier semana. Contenido mínimo:

1. **Datos:** enlaces a la hoja y a la secuencia, grupo, horario y duración de sesión (**[CONFIRMAR]** si falta).
2. **Escala aplicable:** A (NA/R/B/A/E) o B (SA/DE/AU), según `evaluacion.md`; **[CONFIRMAR]** hasta que el profesor la confirme.
3. **Por unidad:** resultado de aprendizaje (`### Resultado de aprendizaje` de la hoja) y ponderación de los saberes (de la secuencia). Cada unidad lleva un encabezado que empieza con «Unidad» (p. ej. `## Unidad 1: Fundamentos`) y, debajo, esta tabla (la verifica `course-lint`; deben sumar 100):

| Saber | Porcentaje |
|---|---|
| Saber | 30% |
| Saber hacer | 50% |
| Saber ser y convivir | 20% |

4. **Calendario:** `Semana | Fechas | Unidad | Tema | Evidencia`, tomado de los bloques de semana de la secuencia.
5. **Decisiones del curso:** herramientas adoptadas, cada una con su fecha.
6. **Avance** (`## Avance`): lo que realmente pasó, lo llena `registrar-avance`.

| Semana | Fecha | Planeado | Real | Ajuste |
|---|---|---|---|---|
