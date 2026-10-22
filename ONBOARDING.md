# Profe Virtual UTEZ: cómo empezar

Este repo convierte a Claude Code en un co-docente que conoce el modelo educativo 2024, la escala 2025 y las reglas de evaluación de la UTEZ. Le das tu hoja de asignatura y tu secuencia, y te ayuda a planear cada semana y a producir presentaciones, prácticas, tareas, exámenes y claves en Word o HTML. Tú apruebas cada paso.

## Requisitos

| Herramienta | Para qué |
|---|---|
| Claude Code | Es el asistente; se abre dentro de esta carpeta |
| git | Clonar el repo y guardar tu avance |
| [uv](https://docs.astral.sh/uv/) | Instala Python 3.12 y las dependencias del proyecto |
| `gh` (opcional) | Publicar presentaciones como gist para compartirlas con el grupo |

## Instalación

```bash
git clone [CONFIRMAR: URL del repo] profe-virtual
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

## Flujo de trabajo

| Comando en Claude Code | Qué hace |
|---|---|
| `/curso-nuevo <slug> <periodo>` | Crea el `curso.md` del grupo: escala, resultados de aprendizaje, calendario y decisiones |
| `/planear-semana NN` | Escribe el `00-plan.md` de la semana, minuto a minuto, y se detiene para que lo apruebes |
| `/producir-semana NN` | Con el plan aprobado, genera decks, prácticas, tareas, exámenes y claves, y los manda revisar |
| `/registrar-avance` | Anota lo que de verdad pasó en clase y propone reajustar las semanas que siguen |

Los archivos quedan en `cursos/<periodo>/<slug>-<cuatrimestre>/semana-NN/`:

- `alumno/`: lo que repartes al grupo.
- `docente/`: claves y guías de observación. No lo compartas con alumnos.
- `fuentes/`: los JSON y Markdown con los que se generan los documentos.

`uv run course-lint` revisa nombres, claves y ponderaciones del curso. También corre solo al terminar cada respuesta de Claude.

## Privacidad

- Guarda tu copia en un repo **privado**.
- No subas calificaciones ni nombres de alumnos a un repo que compartas con otros docentes.
- Las claves de `docente/` tampoco van en repos que vean los alumnos.

## Cómo recibir mejoras

Al clonar, el repo compartido queda como `origin`. Para guardar tu trabajo en tu propio repo privado, renómbralo a `plantilla` y apunta `origin` al tuyo:

```bash
git remote rename origin plantilla
git remote add origin [URL de tu repo privado]
git push -u origin main
```

Cuando haya una versión nueva del sistema, tráela con `git pull plantilla main`.

Tus carpetas `asignaturas/` y `cursos/` no chocan con las mejoras, porque la plantilla las trae vacías.
