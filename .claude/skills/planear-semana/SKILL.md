---
name: planear-semana
description: Genera el 00-plan.md de una semana con sus tablas por sesión y la lista de archivos por producir, y se detiene para que el profesor lo apruebe. Usar al pedir /planear-semana NN, planear o replanear una semana o sesión.
---

# Planear semana

`/planear-semana NN` en el curso activo (si hay más de uno, pregunta cuál).

## Pasos
1. Verifica que existe `curso.md`; si no, ejecuta primero `curso-nuevo`.
2. Lee `curso.md` (escala, RA, calendario, `## Avance`), la hoja y el bloque de la semana en la secuencia. Si `## Avance` marca retraso, parte de lo ajustado.
3. Lee `.claude/rules/plantilla-planeacion.md`, `plantilla-presentacion.md`, las plantillas de cada material previsto, `principios-pedagogicos.md` y `datos-a-pedir.md`. Pregunta una sola vez lo esencial que falte, o declara «Supuestos».
4. Crea `cursos/<periodo>/<curso>/semana-NN/00-plan.md` con el formato de «Plan de semana o de sesión» de `CLAUDE.md`: «Antes de la semana» y una tabla por sesión, con enlaces exactos a documento y clave (aún por producir). Los nombres siguen `sN-NN-<tipo>-<tema>`.
5. Agrega al final `## Por producir`: tabla `Archivo | Tipo | Skill | Destino (alumno/ o docente/)`, con un renglón por material, clave incluida.
6. Respeta las horas de saber y saber hacer de la hoja y el RA de la unidad.
7. Presupuesta cada sesión según «Presupuesto de minutos por sesión» de `plantilla-planeacion.md`: ▶ ≤ 40 % y PARADA ≥ 60 % (la hoja manda si es más práctica); exposición en segmentos de ~10–12 min, cada uno con su parada; abre con 2–3 preguntas de recuperación y cierra con boleto de salida.
8. Antes de presentar, verifica en una línea que cada sesión declara sus totales `▶ X min (Y %) · PARADA Z min (W %)` y que suman la duración de la sesión.

## Parada
Presenta el plan y la lista `## Por producir`, y **detente**: no generes materiales. Continúa solo con la aprobación o los ajustes del profesor; luego sigue `producir-semana`.
