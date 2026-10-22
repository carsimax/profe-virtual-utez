---
paths:
  - "cursos/**/*practica*"
  - "cursos/**/*ejercicio*"
---
# Plantilla: práctica de laboratorio

Base: `.claude/referencia/pedagogia-evidencia.md`, secciones 2 y 4. La práctica es material de apoyo para el alumno **y** para el docente: ningún resultado aparece sin su derivación.

1. Título y número de práctica.
2. Resultado de aprendizaje y saberes que evalúa.
3. Duración, con minutos por parte.
4. Prerrequisitos.
5. Entorno y herramientas (versiones).
6. Instrucciones paso a paso (ver «Secuencia» y «Ficha de paso»).
7. Entregables: repositorio, capturas, pruebas.
8. Criterios de éxito verificables.
9. Retos de extensión (nivel DE/AU).
10. Instrumento de evaluación (rúbrica o lista de cotejo).
11. Versión docente (`docente/<prefijo>_clave`), ver abajo.

## Secuencia (andamiaje que se retira)

| Parte | Qué recibe el alumno | Quién lleva el peso |
|---|---|---|
| A. Ejemplo resuelto | Un problema parecido resuelto completo, con todas sus fichas | Docente / material |
| B. Ejemplo con huecos | El mismo tipo de problema; faltan 1–3 pasos o resultados | Pareja, con pistas |
| C. Problema propio | Problema nuevo, solo con el objetivo y los criterios | Alumno |

- Código nuevo: cada paso sigue PRIMM (predecir, ejecutar, investigar, modificar; crear en la parte C).
- Menos andamiaje con grupos con base previa (p. ej. 7.º y 10.º frente a 1.º y 2.º): si ya dominan el tema, empieza en B o en C con pistas (inversión por experiencia). Declara en «Supuestos» el nivel previo asumido.
- Etiquetas de subobjetivo iguales en práctica, deck y clave.

## Ficha de paso

Cada paso de las partes A y B lleva todos estos campos (formato en tabla o lista, el mismo en todos los pasos):

| Campo | Contenido |
|---|---|
| Subobjetivo | Etiqueta corta («Preparar el entorno», «Aislar la causa») |
| Qué haces | La acción concreta, ejecutable sin interpretar |
| Por qué | Una frase ligada al concepto: qué pasa si lo omites |
| Cómo | Comando o código exacto y dónde va; lo nuevo se explica línea por línea |
| Predicción | Espacio para que el alumno escriba qué cree que pasará, antes de ejecutar |
| Resultado intermedio | Salida real tras el paso (texto, captura descrita o valor parcial), obtenida ejecutándolo |
| Cómo verificas | Qué debes ver y qué comparar |
| Error típico | Mensaje o síntoma real y cómo se corrige |

Prohibido: entregar el resultado final sin su derivación; saltos como «como se observa…» o «entonces se obtiene…»; pasos de solo copiar sin predecir ni explicar.

## Versión docente (`docente/<prefijo>_clave`)

Se escribe al mismo tiempo que la práctica, con las mismas etiquetas de paso. Contiene:

1. **Resultado intermedio esperado** de cada paso (el mismo que ve el alumno en A y B; la solución derivada paso a paso en C, no solo el final).
2. **Concepciones erróneas** (≥ 2): señal, causa, corrección y una **pregunta detectora**. Si no se han observado, márcalas «supuesta» y valídalas en la primera aplicación.
3. **Puntos de control con minuto** (qué mirar en 2–3 equipos antes de seguir).
4. **Qué recortar** si el reloj va mal, en orden, con la holgura de 5–10 % de la parada central.
5. **Preguntas para circular**, con respuesta esperada y qué revela una respuesta mala.
6. **Errores de ejecución** con el mensaje literal y su arreglo.
7. **Variantes:** más apoyo y menos apoyo.

No repitas el guion de las diapositivas: añade lo que el docente no ve en ellas.

Si el profesor pide el material en Word (.docx), usa la skill `word-docs` con su receta de práctica de laboratorio (`.claude/skills/word-docs/references/recetas.md`).
