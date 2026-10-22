---
paths:
  - "cursos/**/*presentacion*/**"
---
# Plantilla: presentación

- Esquema diapositiva por diapositiva: título, 3–5 ideas, ejemplo de código cuando aplique y notas del orador.
- Pregunta de verificación cada 3–4 diapositivas (predicción de salida, opción múltiple o discusión en pares).
- Actividad de apertura (activación de conocimientos previos) y de cierre (ticket de salida).
- Bloques de exposición de máximo 10–15 min.
- Si el profesor lo pide, entrega código Marp o reveal.js, o texto listo para PowerPoint/Google Slides.

## Formato por defecto: HTML con la skill `html-slides`

- Usa la skill `html-slides` (`.claude/skills/html-slides/SKILL.md`) para generar el deck como un solo HTML.
- Defaults del proyecto (reemplazan los de la skill): diseño UTEZ claro, uso `ponente`, arco **Microclase**, notas del presentador en todas las slides.
- Diagramas Mermaid (flujo, UML de clases, secuencia, estados, ER, git): usa la skill `mermaid-diagrams` (`.claude/skills/mermaid-diagrams/SKILL.md`) y valida con `uv run mermaid-check`.
- Ilustraciones y diagramas SVG a mano: usa la skill `svg-illustrations` (`.claude/skills/svg-illustrations/SKILL.md`) y valida con `uv run svg-check`.
- Guarda cada deck en `cursos/<periodo>/<curso>/semana-NN/alumno/<prefijo>-presentacion-<tema>/index.html` (ver «Organización de materiales» en `CLAUDE.md`); las demos van en `demos/` dentro de esa misma carpeta.
- QA, PDF, Mermaid y gráficas se ejecutan con `uv run slides-*` desde la raíz del repo (`slides-qa`, `slides-mermaid`, `slides-chart`, `slides-inline-images`, `slides-pptx`); no se usa Node.
- Las reglas pedagógicas de esta plantilla mandan sobre las de la skill: la pregunta de verificación cada 3–4 slides, la apertura y el ticket de salida son slides obligatorias.
- **Corte obligatorio en cada parada.** Cada punto donde la exposición se detiene (actividad, práctica, demostración o ejercicio guiado, coevaluación, examen, cierre) lleva una slide de corte visible y con el mismo estilo en todo el deck (layout `l-corte`): tipo, duración, modalidad (individual o equipo, con o sin computadora), material, producto y «Regresamos a: …».
- Si el material debe seguir proyectado durante la actividad (definiciones, catálogo, tabla de apoyo), ponlo en una slide de apoyo de 0 minutos justo después del corte (`data-minutes="0"`).
- **Obligatorio:** Todo ejercicio guiado o demostración, en cualquier materia, se respalda paso a paso en la presentación: tras su diapositiva de corte van diapositivas de apoyo (0 min) que se proyectan mientras los alumnos lo resuelven, una por paso o sección del documento del ejercicio, en el mismo orden y con los mismos nombres y números, mostrando cómo se llega a cada sección y cada cálculo con los datos reales del ejercicio, con notas del presentador.
- **Enseña el procedimiento paso a paso antes del ejemplo resuelto**: no uses una técnica en un ejemplo, ejercicio o práctica sin haberla enseñado antes (pasos, ejemplo construido de forma incremental, ejercicio guiado «yo hago, hacemos, haces»).
- Pon el nombre del profesor y el de la asignatura en la portada (ver "Profesor" en `CLAUDE.md`).
- Publicar en gist solo si el profesor lo pide. Un gist secreto **no es privado**: cualquiera con el link lo ve, así que no incluyas datos de alumnos.

## Contenido rico y tiempos (evidencia: `.claude/referencia/pedagogia-evidencia.md`, secciones 1–3)

- **Cada concepto lleva tres cosas:** un ejemplo concreto (código real o un caso de Morelos o del sector productivo, sin datos personales), un visual que muestre el mecanismo (no decoración) y una comprobación (predicción, pregunta de pares o mini ejercicio). Layouts útiles en `references/layouts.md`: `l-evidence`, `l-walk`, `l-worked`, `l-predict`, `l-myth`, `l-case`.
- **Título = oración con verbo**, una idea por slide; se señala solo lo que se comenta y la etiqueta va pegada al elemento. No se duplica en la slide lo que se dice en voz.
- **Slides de apoyo de un ejercicio guiado = ficha de paso:** cada una (layout `l-worked`) lleva subobjetivo, qué, por qué, cómo, predicción, resultado intermedio y verificación (con un error típico y su señal). Las etiquetas de subobjetivo son las mismas que en la práctica y en la clave, y ningún resultado aparece «de la nada»: se deriva del paso anterior con los datos reales.
- **Presupuesto por sesión:** unos 40 % de exposición (apertura y cierre dirigidos incluidos) y al menos 60 % de práctica; anota la suma de minutos en el plan. Si la hoja de asignatura es más práctica, manda la hoja. No lo presentes como resultado de investigación: es una decisión de diseño.
- **Segmentos de exposición ≤ 10–12 min**, cada uno seguido de una parada (corte, predicción o pregunta de pares). Abre con 2–3 preguntas de recuperación de sesiones previas y cierra con el ticket de salida.
- **Notas del presentador en voz natural**, como las diría el profesor (ver «Voz» en `.claude/rules/estilo.md`); sin guion rígido ni frases de relleno.
