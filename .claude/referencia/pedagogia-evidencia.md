# Pedagogía con evidencia: resumen para diseñar materiales

Fecha de la revisión: 2026-10-21. Uso: consulta para quien diseña decks, prácticas, planes y notas docentes (7.º y 10.º cuatrimestre, ingeniería de software, UTEZ). Cada sección cierra con reglas **Haz / Evita** que se pueden revisar en un material terminado.

**Cómo leer la solidez.** **[Fuerte]** = meta-análisis o varios experimentos controlados. **[Moderada]** = experimentos pocos o con resultados mixtos. **[Débil]** = juicio de expertos, estudios pequeños o evidencia indirecta. Las cifras se tomaron de las fuentes que se citan; las que solo pude ver en resúmenes secundarios van marcadas **(secundaria)** y conviene contrastarlas con el original antes de citarlas a alumnos.

**Exclusiones.** No se usa la «pirámide del aprendizaje» ni los «estilos de aprendizaje» (ver `.claude/rules/principios-pedagogicos.md`). Ninguna sección de este documento depende de ellos.

---

## 1. Diseño de diapositivas y multimedia

### 1.1 Qué dice la evidencia

- **Carga cognitiva (CLT).** La memoria de trabajo es limitada y la de largo plazo no. Aprender es construir esquemas en la de largo plazo, así que el diseño debe quitar procesamiento que no enseña (carga extrínseca) y dejar espacio para el esfuerzo que sí construye esquemas. La revisión de veinte años de la teoría es Sweller, van Merriënboer y Paas (2019), *Educational Psychology Review* 31, 261–292, https://doi.org/10.1007/s10648-019-09465-5 **[Fuerte como marco; no pude leer el texto completo, uso solo su ficha y resúmenes]**.
- **Principios multimedia de Mayer.** *Multimedia Learning*, 3.ª ed. (Cambridge, 2020), https://www.cambridge.org/9780521514125, reúne 15 principios con más de 200 experimentos. Se agrupan en: reducir procesamiento extrínseco (coherencia, señalización, redundancia, contigüidad espacial y temporal), manejar el procesamiento esencial (segmentación, preentrenamiento, modalidad) y favorecer el procesamiento generativo (personalización, voz, entre otros). **[Fuerte en conjunto; los tamaños de efecto varían entre ediciones]**.
- **Coherencia.** Quitar material interesante pero ajeno al objetivo mejora el aprendizaje: Mayer (2014, capítulo del *Cambridge Handbook of Multimedia Learning*) reporta 23 de 23 pruebas a favor, mediana d = 0.86 **(secundaria; otras versiones del mismo capítulo dan cifras distintas)**. https://www.cambridge.org/core/books/abs/cambridge-handbook-of-multimedia-learning/principles-for-reducing-extraneous-processing-in-multimedia-learning-coherence-signaling-redundancy-spatial-contiguity-and-temporal-contiguity-principles/C98AB3A6CE760DD63C048936EA0B3B44
- **Señalización.** Marcar qué es importante (resaltado, flechas, esquema visible) ayuda. Alpizar, Adesope y Wong (2020), meta-análisis de 29 estudios, *Educational Technology Research and Development* 68, 2095–2119: efecto fuerte en retención y moderado en transferencia **(secundaria, vía resumen de QIC-WD, https://qic-wd.org/node/672)**. Mayer (2014): mediana d = 0.41 en 24 de 28 pruebas **(secundaria)**. **[Fuerte]**.
- **Redundancia.** No leer en voz alta lo que la diapositiva ya trae completo en texto, sobre todo si hay gráfico. Mayer (2020), mismo libro. **[Fuerte en multimedia con narración; en clase presencial hay menos estudios, trátalo como regla de prudencia]**.
- **Contigüidad espacial.** Poner etiquetas pegadas al elemento que nombran, no en una leyenda lejana. Mayer (2020). **[Fuerte]**.
- **Segmentación.** Dividir una explicación en partes que el alumno recorre a su ritmo. Mayer y Moreno (2003), «Nine ways to reduce cognitive load in multimedia learning», *Educational Psychologist* 38(1), https://www.uky.edu/~gmswan3/544/9_ways_to_reduce_CL.pdf. **[Moderada–Fuerte]**.
- **Estructura aserción-evidencia.** Título = una oración completa que afirma algo; cuerpo = evidencia visual (figura, código, gráfica, captura) en lugar de viñetas. Alley y Neeley (2005), *Technical Communication* 52(4), https://writing.engr.psu.edu/research.html. Garner, Alley et al. (2013), *Int. J. Engineering Education*: el público entendió y recordó más con aserción-evidencia que con tema-subtema (p < .01) **(secundaria, vía la página de Penn State)**. Aippersbach, Alley y Garner (2013, ASEE): quienes armaron slides así comprendieron mejor el contenido. **[Moderada: pocos estudios, mayormente del mismo grupo]**.
- **Tamaño de letra.** No hay estudios experimentales sobre tamaño mínimo en aula; hay guías de práctica. Penn State recomienda unos 24 pt mínimo para texto proyectado y títulos de 40–60 pt, https://accessibility.psu.edu/legibility/fontsize. Regla de Rindsberg: texto ≥ 1/50 de la altura de la lámina es el piso absoluto, no lo recomendable, https://www.pptfaq.com/FAQ00125_How_big_should_text_be-_What-s_the_ideal_font_size-.htm. **[Débil, juicio experto]**. Conversión para una lámina de 1080 px de alto: piso ≈ 22 px (2%), cuerpo recomendado ≈ 38–48 px (3.5–4.4%, equivalente a 24 pt sobre 540 pt de alto). **[Verificar la base de píxeles real del template antes de aplicar]**.
- **Variedad visual sin decoración.** Variar el tipo de lámina (comparación, secuencia, código anotado, captura, esquema, pregunta) es útil si cada variante sirve a una función distinta; los adornos sin función violan coherencia. No hay estudio que mida «variedad» como tal; es inferencia de coherencia y señalización. **[Débil como inferencia]**.

### 1.2 Reglas de diseño

**Haz**
- Escribe el título de cada lámina de contenido como oración con verbo («El índice evita recorrer toda la tabla»), no como tema («Índices»).
- Usa como evidencia un objeto visual: código anotado, diagrama, captura, gráfica o tabla pequeña. Una idea principal por lámina.
- Señala con color, recuadro o flecha solo lo que el docente va a comentar en ese momento; todo lo demás va en gris o tenue.
- Pega la etiqueta al elemento (flecha o número sobre el código, no leyenda aparte).
- Segmenta: un paso o concepto por lámina; la secuencia de láminas es la segmentación.
- Si usas imagen, que muestre el mecanismo (qué pasa y en qué orden), no ambiente.
- Con el docente hablando, deja en la lámina las palabras clave y la figura; lo explicado en voz no se repite palabra por palabra.
- Variedad con función: elige el tipo de lámina por lo que se pide al alumno hacer (predecir, comparar, ordenar, localizar el error), y anótalo en las notas.
- Cuerpo proyectado ≥ 38 px sobre lámina de 1080 px de alto (≈ 24 pt sobre 540 pt) y nada de texto sustantivo por debajo del piso de 22 px.

**Evita**
- Párrafos o más de unas 6 líneas de viñetas por lámina.
- Clip art, fondos con foto, íconos sin significado, animaciones que no muestren un cambio de estado.
- Duplicar el guion en la lámina.
- Código con letra menor que el cuerpo; si no cabe, recorta el fragmento y resalta las líneas relevantes.
- Afirmar tamaños de efecto de Mayer como universales; cítalos como «apoyo moderado a fuerte».

---

## 2. Ejemplos resueltos y práctica guiada en programación

### 2.1 Qué dice la evidencia

- **Efecto del ejemplo resuelto.** Para aprendices novatos, estudiar ejemplos resueltos y luego practicar supera a resolver problemas desde cero, porque reduce la búsqueda a ciegas. Sweller, van Merriënboer y Paas (2019), arriba. Kirschner, Sweller y Clark (2006), *Educational Psychologist* 41(2), 75–86, sostienen que la guía mínima es poco eficaz para novatos; hay réplicas críticas que señalan que el problema es la falta de andamiaje y corrección, no el trabajo activo en sí. **[Fuerte para novatos; debatido su alcance]**.
- **Inversión por experiencia.** Lo que ayuda a novatos puede estorbar a quien ya domina el tema: el ejemplo resuelto pierde valor y luego perjudica. Kalyuga, Ayres, Chandler y Sweller (2003), *Educational Psychologist* 38(1) **(secundaria, vía https://en.wikipedia.org/wiki/Worked-example_effect)**. **[Fuerte]**.
- **Ejemplos con retirada gradual (faded).** Se pasa de ejemplo completo a ejemplo con pasos faltantes y luego a problema; funciona mejor con indicaciones de autoexplicación, y la retirada adaptada al desempeño supera a la fija. Renkl y Atkinson, resumidos en https://openlearning.mit.edu/mit-faculty/research-based-learning-findings/worked-and-faded-examples **(secundaria)**. **[Moderada–Fuerte]**.
- **Autoexplicación.** Los ejemplos resueltos rinden si el alumno se explica cada paso, y con indicaciones de autoexplicación aprende más que con el ejemplo solo **(secundaria, mismo resumen y Wikipedia)**. No pude confirmar el trabajo original de Chi et al. (1989). **[Moderada]**.
- **Etiquetas de subobjetivo.** Margulieux y Catrambone (2016), *Learning and Instruction*: etiquetas de subobjetivo en el texto y en los ejemplos mejoran la resolución de problemas nuevos. Margulieux, Morrison y Decker (2019, ITiCSE; 2020, *Int. J. STEM Education*): en un CS1 completo, mejor desempeño temprano, menos variabilidad y más permanencia; la afirmación sobre reducción de retiro y reprobación está en el título del artículo de 2020, no pude leer las cifras, https://doaj.org/article/9a2c85d66fd54ec9ab019e9a510bbf17. **[Moderada–Fuerte en programación]**.
- **Diez consejos de Brown y Wilson.** «Ten quick tips for teaching programming» (2018), *PLoS Comput. Biol.* 14(4): e1006023, https://pmc.ncbi.nlm.nih.gov/articles/PMC5886386/: no existe el «gen de programar»; instrucción entre pares con preguntas que sondean concepciones erróneas (voto, discusión de 2–4, nuevo voto); programar en vivo; pedir predicciones públicas antes de ejecutar; programación en pareja; ejemplos con subobjetivos; un lenguaje a la vez; tareas auténticas con código base; tareas pequeñas para novatos; actividades sin escribir código como Parsons. **[Moderada: guía de práctica respaldada en literatura, no un meta-análisis]**.
- **Codificación en vivo.** Los experimentos controlados no muestran ventaja sobre ejemplos estáticos: Soosai Raj et al. (2020), experimento aleatorizado en C++, sin diferencia; Shah et al. (2023), ICER, https://icer2023.acm.org/details/icer-2023-papers/34/An-Empirical-Evaluation-of-Live-Coding-in-CS1, y versión de 2025 sobre «live coding activo», sin mejora de aprendizaje. Selvaraj et al. (2021, ITiCSE) es una revisión de la literatura, y se cita por la carga del docente al hacer live coding **(no pude confirmar título ni hallazgos; léelo antes de citarlo)**. Lectura prudente: el live coding sirve para mostrar proceso y errores reales, pero **no** sustituye al ejemplo resuelto escrito que el alumno puede releer. **[Moderada, resultados nulos]**.
- **PRIMM.** Predecir, Ejecutar, Investigar, Modificar, Crear. Sentance, Waite y Kallia (2019), *Computer Science Education* 29(2–3), 136–176, https://doi.org/10.1080/08993408.2019.1608781; origen: Sentance y Waite (2017), https://doi.org/10.1145/3137065.3137084. La evidencia citada en fuentes de difusión (500 estudiantes de 11–14 años) y un estudio con 35 alumnos de bachillerato técnico (N-gain 0.40) son pequeñas **(secundaria)**. **[Débil–Moderada; sustento teórico sólido, evidencia causal escasa]**.
- **Problemas de Parsons.** Ordenar líneas desordenadas reduce carga de sintaxis. Ericson et al. (2022), ITiCSE-WGR, https://doi.org/10.1145/3571785.3574127, revisión sistemática; la eficacia como herramienta de aprendizaje sigue sin réplicas suficientes (Wikipedia, https://en.wikipedia.org/wiki/Parsons_problem). **[Moderada–Débil]**.
- **Fracaso productivo.** Intentar un problema difícil antes de la explicación puede superar «instrucción primero» para conceptos (Sinha y Kapur, 2021, *Review of Educational Research*; 53 estudios, 166 comparaciones; el «tres veces mejor» viene de prensa, no lo uses). Aplica a alumnos con base previa; no a novatos absolutos. **[Moderada, condicionada]**.

### 2.2 Cómo deben ser los pasos para que el resultado no «salga de la nada»

Combina lo anterior en una ficha mínima. **Cada paso** de una práctica o ejemplo guiado lleva:

| Campo | Qué contiene | Revisable si… |
|---|---|---|
| Subobjetivo | Etiqueta corta del paso («Preparar el entorno», «Aislar la causa») | La etiqueta es la misma en la práctica, el deck y la clave |
| Qué | La acción concreta (comando, línea, clic) | Se puede ejecutar sin interpretar |
| Por qué | La razón en una frase, ligada a un concepto | Responde «¿y si no lo hago?» |
| Cómo | El código o comando exacto y dónde va | Está completo, no «etc.» |
| Predicción | Qué crees que pasará (alumno responde antes de ejecutar) | Hay campo para escribir la predicción |
| Resultado intermedio | La salida o estado exacto tras el paso | Se muestra salida real, no «debería funcionar» |
| Verificación | Cómo comprobar que quedó bien y qué hacer si no | Incluye al menos un error típico y su señal |

### 2.3 Reglas

**Haz**
- Antes de pedir que el alumno escriba algo nuevo, muestra un ejemplo resuelto completo de un problema parecido; luego uno con huecos; luego el problema propio (retiro gradual: «yo hago / hacemos / tú haces»).
- Pide una predicción por escrito antes de cada ejecución nueva (P de PRIMM); después pide que expliquen en una frase por qué el resultado fue ese.
- Etiqueta los subobjetivos y reutiliza las mismas etiquetas en práctica, deck y clave.
- Muestra cada resultado intermedio real (salida, captura o estado del repo) para que el resultado final se derive, no aparezca.
- Incluye un error típico por paso con su mensaje real y la corrección.
- Reduce la ayuda según el grupo: 7.º cuatrimestre con menos retiro de andamiaje que 10.º; si el grupo ya domina el tema, empieza en problema con pistas, no en ejemplo completo (inversión por experiencia).
- Usa Parsons como puente cuando la sintaxis estorbe al razonamiento (cuidando que los distractores sean errores reales).
- Si haces live coding, deja además el ejemplo escrito y los comandos exactos en el material.

**Evita**
- Entregar el resultado final sin pasos, o pasos con saltos («como se observa…», «entonces se obtiene…»).
- Ejercicios en los que el alumno solo copia sin predecir ni explicar (copiar no es aprender).
- Asumir que live coding por sí solo basta como material de apoyo.
- Tareas de «descubre por tu cuenta» para novatos sin andamiaje ni retroalimentación.
- Citar el live coding como eficaz «según la evidencia»; la evidencia disponible es nula o negativa en aprendizaje.

---

## 3. Aprendizaje activo y estructura de la sesión

### 3.1 Qué dice la evidencia

- **Aprendizaje activo frente a clase expositiva.** Freeman et al. (2014), *PNAS* 111(23), 8410–8415, https://pubmed.ncbi.nlm.nih.gov/24821756/, meta-análisis de 225 estudios en STEM universitario: +0.47 DE en exámenes (158 estudios) y razón de momios de reprobar 1.95 en clase expositiva (67 estudios). Porcentajes de reprobación 33.8 % frente a 21.8 % **(secundaria)**. Theobald et al. (2020), *PNAS* 117(12), reportan que reduce brechas de logro en grupos subrepresentados **(solo vi la ficha)**. **[Fuerte]**. Límite: los estudios son de STEM, no específicamente de ingeniería de software; «activo» incluye clickers, problemas en grupo, tutorías, etc., no una proporción fija.
- **Sensación de aprender frente a aprendizaje.** Deslauriers et al. (2019), *PNAS* 116(39), 19251–19257, https://doi.org/10.1073/pnas.1821936116: los alumnos con instrucción activa rindieron más pero creyeron aprender menos. **[Moderada–Fuerte: un diseño aleatorizado en física]**. Implicación: avisa a los alumnos que el esfuerzo se siente peor y funciona mejor.
- **Práctica de recuperación.** Rowland (2014), *Psychological Bulletin* 140(6), 1432–1463: probarse supera a releer, g ≈ 0.50, más con retroalimentación (0.73 frente a 0.39) **(cifras secundarias)**. **[Fuerte]**.
- **Espaciado.** Cepeda et al. (2006), *Psychological Bulletin* 132(3), 354–380, https://pubmed.ncbi.nlm.nih.gov/16719566/: 839 evaluaciones en 317 experimentos; el intervalo óptimo entre sesiones crece con el tiempo que se quiere retener. **[Fuerte, sobre todo en tareas verbales]**.
- **Intercalado.** Brunmair y Richter (2019), *Psychological Bulletin*, https://doi.org/10.1037/bul0000209: g = 0.42 global, 0.34 en tareas matemáticas, ventaja del bloqueado con palabras (g = −0.39) **(cifras secundarias)**. En programación hay poca evidencia directa. **[Moderada; en código, Débil]**.
- **Instrucción entre pares.** Crouch y Mazur (2001), *Am. J. Physics* 69, 970–977, https://mazur.harvard.edu/publications/peer-instruction-ten-years-experience-and-results: ganancia conceptual mayor en una década; comparación de Hake: ganancia normalizada 0.23 frente a 0.48 **(secundaria)**. **[Moderada–Fuerte en física; en programación, ver Brown y Wilson]**.
- **Boleto de salida.** Es práctica de recuperación y evaluación formativa breve; no encontré estudio que la aísle como técnica. **[Débil como técnica; Fuerte como recuperación]**.
- **Cuánto exponer.** El «máximo 10–15 minutos» tiene sustento débil como límite de atención: Wilson y Korn (2007), *Teaching of Psychology* 34(2), 85–89, encontraron que esa cifra se apoya en medición indirecta **(secundaria)**. La regla de partir la exposición sigue siendo útil porque da puntos de recuperación y de verificación, no porque la atención «se acabe» a los 10 minutos. **[Débil como dato de atención]**.
- **40 % exposición / 60 % práctica.** No hay estudio que valide esa proporción exacta. Es coherente con el modelo educativo 2024 (60 % práctica; ver `contexto-institucional.md`) y con Freeman et al., que no fija proporción. Trátala como decisión de diseño institucional, no como hallazgo. La hoja de asignatura manda cuando sea más práctica. **[Sin respaldo directo]**.

### 3.2 Cómo acotar el tiempo de una sesión

Ejemplo de reparto para 100 min (ajustar al tiempo real **[CONFIRMAR]**):

| Bloque | Min | Qué |
|---|---|---|
| Apertura con recuperación | 8–10 | Pregunta de unidades previas (espaciado) y predicción del tema |
| Exposición 1 | ≤ 12 | Concepto + ejemplo resuelto |
| PARADA 1 | 12–15 | Práctica corta o pregunta de pares |
| Exposición 2 | ≤ 10 | Segundo concepto o caso |
| PARADA 2 (práctica central) | 30–35 | Práctica guiada en parejas, con avisos de reloj |
| Cierre | 8–10 | Boleto de salida + resumen en una frase por alumno |

Total exposición ≈ 40 %, incluyendo apertura y cierre dirigidos por el docente; práctica ≈ 60 %.

### 3.3 Reglas

**Haz**
- Presupuesta la sesión en minutos por bloque y suma: exposición ≤ 40 %, práctica ≥ 60 %; anota el cálculo en el plan.
- Parte la exposición en segmentos de unos 10–12 min, cada uno seguido de una PARADA (pregunta, predicción, mini práctica). Justifícalo por recuperación y verificación, no por «atención de 10 minutos».
- Abre cada sesión con 2–3 preguntas de recuperación de sesiones anteriores (espaciado) y cierra con boleto de salida de 1–3 reactivos.
- Pon pregunta de pares con respuestas erróneas que correspondan a una concepción equivocada concreta (voto, discusión, nuevo voto).
- Intercala en las prácticas un problema de un tema previo (intercalado), sin sobrecargar al novato.
- Pon hora de reloj relativa y holgura de 5–10 % en la parada central.
- Dile al grupo que el esfuerzo de la práctica se siente menos fluido que la exposición y que eso es normal.

**Evita**
- Exposiciones de más de ~15 min sin parada.
- Que «práctica» sea el docente haciendo la demostración con alumnos mirando.
- Presentar 40/60 como resultado de investigación.
- Cierre con contenido nuevo o evidencias nuevas (regla de `evaluacion.md`).
- Recuperación sin retroalimentación (pierde casi la mitad del efecto, ver Rowland).

---

## 4. Material de apoyo para el docente

### 4.1 Qué dice la evidencia

La evidencia directa sobre «guías docentes» como formato es escasa **[Débil]**. Lo que sí está respaldado: el docente necesita conocer concepciones erróneas (las preguntas de pares funcionan si cada distractor corresponde a una: Brown y Wilson, 2018); las verificaciones frecuentes permiten ajustar en vivo (Crouch y Mazur, 2001); y la retroalimentación específica mejora la recuperación (Rowland, 2014). El resto es diseño inferido de esas fuentes y de Sweller et al. (2019) para pasos y resultados intermedios.

### 4.2 Contenido mínimo de una guía o nota docente

| Elemento | Qué incluir |
|---|---|
| Objetivo y resultado de aprendizaje | A cuál aporta y qué nivel cognitivo |
| Tiempo por paso | Minutos y holgura; qué recortar si hay retraso |
| Resultado intermedio esperado | Salida o estado exacto de cada paso, con captura o texto |
| Puntos de verificación | Qué mirar en 2–3 equipos antes de seguir |
| Concepciones erróneas frecuentes | Cada una con su señal, su causa y cómo corregirla |
| Errores típicos de ejecución | Mensaje real y arreglo |
| Preguntas para el grupo | Con respuesta esperada y qué revela una respuesta mala |
| Variantes | Más apoyo y menos apoyo (por inversión por experiencia) |
| Clave | Solución completa derivada paso a paso, no solo el final |

### 4.3 Reglas

**Haz**
- Crea la nota docente al mismo tiempo que la práctica, con las mismas etiquetas de pasos.
- Para cada paso, escribe el resultado intermedio real, obtenido ejecutando el código.
- Lista al menos 2 concepciones erróneas por práctica y una pregunta que las detecte.
- Incluye «si falla aquí, revisa esto» con el mensaje de error literal.
- Marca con claridad qué recortar si el reloj va mal.

**Evita**
- Claves con solo el resultado final.
- Concepciones erróneas inventadas; si no se observaron, di «supuesta» y valídalas en la primera aplicación.
- Notas que repiten el guion de las diapositivas sin añadir nada.

---

## 5. Voz natural en los materiales

### 5.1 Qué dice la evidencia

- **Lenguaje claro.** ISO 24495-1:2023, https://scc-ccn.ca/standardsdb/standards/8184602 (ficha de la norma): los lectores deben encontrar, entender y usar lo que leen; incluye elegir palabras, frases y párrafos claros, y probar el documento con lectores. Los ejemplos de la norma son en inglés **[Moderada como norma; sin ejemplos en español]**.
- **Señales de texto de IA.** La guía de Wikipedia «Signs of AI writing», https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing, recoge patrones observados por editores: vocabulario inflado, evitar «es/tiene», paralelismos negativos, reglas de tres, atribuciones vagas, tono promocional, exceso de negritas, listas con etiqueta en negritas y restos de chat. Advierte que son descriptivas, no prueba. **[Débil–Moderada: observación de editores, no experimento]**.
- **Vocabulario de exceso.** Kobak et al. (2025), *Science Advances* 11(27), https://arxiv.org/abs/2406.07016v5: tras 2022 subió la frecuencia de palabras de estilo («delves», «showcasing», «underscores»…) en más de 15 millones de resúmenes biomédicos; estiman al menos 13.5 % procesado con LLM en 2024. **[Fuerte para inglés científico; no se midió en español de clase]**. Las listas de palabras envejecen rápido; úsalas como pista, no como lista fija.
- **Detectores.** Son poco fiables: Liang et al. (2023), https://arxiv.org/abs/2304.02819, vieron que más de la mitad de ensayos de hablantes no nativos se marcaban como IA. No uses detectores para juzgar a nadie; el objetivo aquí es escribir mejor, no «pasar» un detector.
- **Español.** No encontré una guía equivalente validada para español; lo siguiente es adaptación mía de los patrones anteriores y requiere ajuste con tus materiales reales. **[Débil, adaptación]**.

### 5.2 Señales a evitar, adaptadas al español

| Señal | Ejemplo a evitar | Alternativa |
|---|---|---|
| Apertura grandilocuente | «En el mundo actual, cada vez más…» | Empieza con el dato o el problema |
| Inflar importancia | «Es crucial/fundamental/pilar para…», «juega un papel clave» | Di qué pasa si falta |
| Vocabulario de moda | «sumergirse», «tapiz», «panorama», «robusto», «potenciar», «optimizar», «fomentar» sin objeto | La palabra concreta |
| Evitar «es/tiene» | «funge como», «cuenta con», «se erige como» | «es», «tiene» |
| Paralelismo negativo | «No es solo X, sino también Y» | Una afirmación directa |
| Regla de tres automática | «rápido, eficiente y escalable» | La cantidad que realmente haya |
| Cierre moralizante | «En conclusión, es fundamental recordar que…» | Termina en la acción siguiente |
| Atribución vaga | «Los expertos coinciden», «diversos estudios» | Autor, año, enlace |
| Gerundio colgante | «…destacando la importancia de…» | Quítalo o haz otra frase |
| Muletillas de transición | «Cabe destacar», «Es importante señalar», «Asimismo», en cada párrafo | Quita o usa «y», «pero», «por eso» |
| Formato en exceso | Negritas por todos lados, viñetas con **Etiqueta:** en cada una, emojis | Prosa o lista simple |
| Ritmo uniforme | Frases de la misma longitud y estructura | Alterna largas y cortas |
| Neutralidad sin postura | «Depende de varios factores» | Da la recomendación y su condición |
| Restos de chat | «Claro, aquí tienes», «Espero que esto ayude» | Borrarlos siempre |

### 5.3 Reglas

**Haz**
- Habla al alumno en segunda persona, con oraciones de 15–20 palabras de promedio y verbos concretos.
- Nombra cosas con sus términos del curso (la función, la tabla, el commit), no con sustantivos abstractos.
- Incluye detalles del contexto real (Morelos, un error que el grupo ya tuvo, una pregunta de clase pasada) cuando existan en el repo; si no existen, no los inventes.
- Admite incertidumbre con precisión («en nuestras pruebas con Node 20 pasó esto») en lugar de relleno.
- Lee en voz alta: si no lo dirías en clase, reescríbelo.
- Cita fuente con autor, año y enlace cuando afirmes algo empírico.

**Evita**
- Las señales de la tabla 5.2, sobre todo en títulos, aperturas y cierres de lámina.
- «Limpiar» el texto solo cambiando palabras: los patrones estructurales (ritmo, regla de tres, cierre moralizante) delatan igual.
- Usar un detector de IA como criterio de calidad o contra alumnos.

---

## Fuentes (resumen)

Verificadas por ficha o resumen, no todas leídas completas: Sweller et al. 2019; Mayer 2020 y 2014; Mayer y Moreno 2003; Alpizar et al. 2020; Alley y Neeley 2005; Garner et al. 2013; Aippersbach et al. 2013; Kirschner et al. 2006; Kalyuga et al. 2003; Renkl y Atkinson (resumen MIT); Margulieux y Catrambone 2016; Margulieux et al. 2019/2020; Brown y Wilson 2018; Soosai Raj et al. 2020; Shah et al. 2023; Selvaraj et al. 2021; Sentance y Waite 2017; Sentance et al. 2019; Ericson et al. 2022; Sinha y Kapur 2021; Freeman et al. 2014; Theobald et al. 2020; Deslauriers et al. 2019; Rowland 2014; Cepeda et al. 2006; Brunmair y Richter 2019; Crouch y Mazur 2001; Wilson y Korn 2007; Penn State Accessibility; Rindsberg (PPT FAQ); ISO 24495-1:2023; Wikipedia «Signs of AI writing»; Kobak et al. 2025; Liang et al. 2023. Total: 35.

**Huecos conocidos.** No pude abrir el texto completo de Freeman, Sweller 2019, Chi 1989, Rowland, Brunmair ni Wieman 2014. No hay estudio experimental sobre tamaño mínimo de letra, sobre la proporción 40/60, ni sobre señales de IA en español. Antes de citar cifras a alumnos o en documentos oficiales, contrástalas con el original.
