# Profe Virtual UTEZ

Un co-docente para [Claude Code](https://claude.com/claude-code), hecho para profesores de la Universidad Tecnológica Emiliano Zapata (UTEZ). Le das tu hoja de asignatura y tu secuencia didáctica. Con eso planea cada semana minuto a minuto y produce los materiales de clase alineados al resultado de aprendizaje de la unidad. Tú apruebas cada paso: el asistente propone, justifica y ajusta.

Ya conoce el modelo educativo DGUTyP 2024, la escala de calificaciones UTEZ 2025 (NA/R/B/A/E), la escala anterior SA/DE/AU y la regla de evaluar los tres saberes en cada unidad.

## Requisitos

| Herramienta | Para qué |
|---|---|
| Claude Code | Es el asistente; se abre dentro de esta carpeta |
| git | Clonar el repo y guardar tu avance |
| [uv](https://docs.astral.sh/uv/) | Instala Python 3.12 y las dependencias del proyecto |
| `gh` (opcional) | Publicar presentaciones como gist para compartirlas con el grupo |

## Instalación

```bash
git clone https://github.com/carsimax/profe-virtual-utez.git profe-virtual
cd profe-virtual
uv sync                               # crea .venv con Python 3.12 y las dependencias
uv run playwright install chromium    # navegador para revisar decks y diagramas
uv run pytest                         # opcional: comprueba que todo quedó bien
claude                                # abre Claude Code en la carpeta
```

## Primer paso: tus datos

Abre `CLAUDE.md` y reemplaza la línea de la sección «Profesor» con tu nombre, grado, cargo y división. Esos datos salen en las portadas y firmas de los materiales.

## Agrega tu asignatura

Cada materia vive en `asignaturas/<slug>/` con dos archivos:

- `hoja-asignatura.md`: la hoja oficial DGUTyP (unidades, horas, resultados de aprendizaje, evidencias).
- `secuencia-<periodo>-<cuatrimestre>.md`: tu secuencia del periodo, por ejemplo `secuencia-2027-ene-abr-4.md`.

Si las tienes en PDF o Word, pídele a Claude que las convierta con la skill `docs-to-md` (o corre `uv run docs-to-md <archivo>`). Luego agrega el front matter al inicio de cada archivo. Hazlo tú: el repo impide que Claude edite `hoja-asignatura.md` y `institucional/`, para que nadie altere un documento oficial por accidente.

```yaml
---
tipo: hoja-asignatura
asignatura: Nombre oficial de la asignatura
slug: nombre-de-la-asignatura
clave: [clave oficial]
programa: [programa educativo tal como aparece en la hoja]
cuatrimestre: 4
horas: {saber: 24, saber_hacer: 36, total: 60, por_semana: 4}
unidades:
  - {numero: I, nombre: "Nombre de la unidad", saber: 8, saber_hacer: 4, total: 12}
vigencia: "SEPTIEMBRE DE 2024"
---
```

```yaml
---
tipo: secuencia-didactica
asignatura: NOMBRE DE LA ASIGNATURA
slug: nombre-de-la-asignatura
periodo: ENERO ABRIL 2027
cuatrimestre: 4
grupo: A
horas_por_semana: 4
carrera: [carrera]
docente: [tu nombre]
hoja: asignaturas/nombre-de-la-asignatura/hoja-asignatura.md
---
```

El `slug` va en minúsculas con guiones y es igual al nombre de la carpeta.

## Qué produce

| Material | Formato |
|---|---|
| Plan de semana o de sesión, con reloj, paradas y enlaces a cada documento | Markdown |
| Presentaciones 16:9 con notas del presentador, diagramas y gráficas | Un solo HTML (también PDF o .pptx) |
| Prácticas, tareas y exámenes, cada uno con su clave | Word (.docx) |
| Rúbricas, listas de cotejo y guías de observación | Word (.docx) |
| Diagramas Mermaid e ilustraciones SVG validados | .mmd, .svg |

## Cómo trabaja

| Comando en Claude Code | Qué hace |
|---|---|
| `/curso-nuevo <slug> <periodo>` | Crea el `curso.md` del grupo: escala, resultados de aprendizaje, calendario y decisiones |
| `/planear-semana NN` | Escribe el plan de la semana y se detiene hasta que lo apruebes |
| `/producir-semana NN` | Genera los materiales del plan aprobado y los manda revisar |
| `/registrar-avance` | Anota lo que pasó en clase y reajusta las semanas que siguen |

Los archivos quedan en `cursos/<periodo>/<slug>-<cuatrimestre>/semana-NN/`:

- `alumno/`: lo que repartes al grupo.
- `docente/`: claves y guías de observación. No lo compartas con alumnos.
- `fuentes/`: los JSON y Markdown con los que se generan los documentos.

Cada material lo revisan dos agentes antes de entregártelo. `revisor-alineamiento` lo contrasta con el resultado de aprendizaje, la hoja y las ponderaciones. `alumno-simulado` resuelve el examen o la práctica sin ver la clave y reporta reactivos ambiguos o claves erróneas.

Los hooks del proyecto revisan nombres de archivo, impiden que una clave quede en la carpeta de alumnos y corren `course-lint` al terminar cada respuesta. Los permisos impiden que el asistente edite la hoja de asignatura o los documentos institucionales.

## Estructura

```
CLAUDE.md                  instrucciones del asistente (aquí van tus datos)
institucional/             modelo educativo 2024 y lineamientos de escala 2025 (solo lectura)
asignaturas/<slug>/        tu hoja de asignatura y tu secuencia (vacío en la plantilla)
cursos/<periodo>/<curso>/  tus cursos, semana por semana (vacío en la plantilla)
.claude/
  rules/                   reglas pedagógicas, de evaluación, de estilo y plantillas por material
  skills/                  flujo del curso, presentaciones, Word, diagramas, conversión a Markdown
  agents/                  revisor-alineamiento y alumno-simulado
  settings.json            hooks y permisos
src/cmx_teach/             herramientas en Python (uv)
tests/                     pruebas (uv run pytest)
```

## Herramientas

Todas corren con `uv run <comando>`; normalmente las usa el asistente.

| Comando | Para qué |
|---|---|
| `docs-build`, `docs-visuals`, `docs-qa`, `docs-fill` | Generar y revisar documentos Word desde un JSON |
| `slides-qa`, `slides-mermaid`, `slides-chart`, `slides-inline-images`, `slides-pptx` | Revisar y exportar presentaciones HTML |
| `mermaid-check`, `svg-check` | Validar diagramas e ilustraciones |
| `docs-to-md` | Convertir PDF, Word, Excel o PowerPoint a Markdown |
| `course-lint` | Revisar nombres, claves, enlaces del plan y ponderaciones de un curso |

## Base pedagógica

Las reglas de `.claude/rules/principios-pedagogicos.md` se apoyan en `.claude/referencia/pedagogia-evidencia.md`: alineamiento constructivo, ejemplo resuelto con andamiaje que se retira, PRIMM, práctica de recuperación y DUA. Cada regla indica qué tan sólida es su evidencia.

## Contribuir

`main` está protegida. Si encuentras un error o quieres proponer una mejora, abre un issue o haz un fork y manda un pull request.

## Privacidad

- Guarda tus cursos en un repo **privado** (un fork de un repo público también es público; usa los pasos de abajo).
- No subas calificaciones, nombres de alumnos ni claves de examen a un repo público o compartido.

## Cómo recibir mejoras

Al clonar, este repo queda como `origin`. Para guardar tu trabajo en tu propio repo privado, renómbralo a `plantilla` y apunta `origin` al tuyo:

```bash
git remote rename origin plantilla
git remote add origin [URL de tu repo privado]
git push -u origin main
```

Cuando haya una versión nueva del sistema, tráela con `git pull plantilla main`. Tus carpetas `asignaturas/` y `cursos/` no chocan con las mejoras, porque la plantilla las trae vacías.

Mantenido por [@carsimax](https://github.com/carsimax), DATID, UTEZ.
