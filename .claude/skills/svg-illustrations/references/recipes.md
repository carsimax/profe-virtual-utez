# Recetas SVG para slides

Cada receta es un SVG **completo y mínimo** que pasa `uv run svg-check` con cero errores. Están escritas con las clases del deck (`.d-*`, `.ill-*`); para pegarlas en una slide, copia solo el `<svg>…</svg>` dentro de `<figure class="fig">` y **cambia el prefijo de los IDs** (`r1-`, `r2-`…) al número de la slide (`s07-`). Para validarlas fuera de un deck, guárdalas como `.svg`: el checker las envuelve con el tema `utez`.

Convenciones comunes: `viewBox` explícito sin `width`/`height`; capas en orden fondo → conectores → formas → texto; texto de 24 px (`.d-text`) o etiquetas de 15 px mono (`.d-label`); una sola forma en `--tone` como punto focal.

Índice: 1 isométrico · 2 flechas · 3 callouts · 4 clase UML · 5 red · 6 cilindro BD · 7 línea de tiempo · 8 capas · 9 cliente–servidor · 10 wireframe.

## 1. Proyección isométrica y caja

Fórmula (ángulo 30°, escala `s`, origen de pantalla `(ox, oy)`):

```
sx = ox + (x − y) · cos30° · s      cos30° = 0.866
sy = oy + (x + y) · sin30° · s − z · s   sin30° = 0.5
```

Caja de 2 × 2 × 1.5 con `s = 60`, `ox = 450`, `oy = 200`. Esquinas superiores (z = 1.5, resta 90 px): `(0,0)→(450,110)`, `(2,0)→(554,170)`, `(2,2)→(450,230)`, `(0,2)→(346,170)`; inferiores: lo mismo con `sy + 90`. Cara superior la más clara (foco), cara izquierda media, derecha la más oscura. Las caras se rellenan con una clase `.ill-*` y el contorno va aparte con `.ill-line`.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 400" role="img" aria-labelledby="r1-t r1-d">
  <title id="r1-t">Caja isométrica</title>
  <desc id="r1-d">Un servidor representado como una caja isométrica con una etiqueta a la derecha.</desc>
  <!-- grid: s=60, origin (450,200); top face z=1.5; unit vectors x->(52,30), y->(-52,30), z->(0,-60) -->
  <path class="ill-soft" d="M346 170L450 230V320L346 260Z"/>
  <path class="ill-surface" d="M554 170L450 230V320L554 260Z"/>
  <path class="ill-tone" d="M450 110L554 170L450 230L346 170Z"/>
  <path class="ill-line" d="M450 110L554 170V260L450 320L346 260V170Z M346 170L450 230L554 170 M450 230V320"/>
  <path class="d-line" d="M570 170H620"/>
  <text class="d-text" x="640" y="178">Servidor</text>
  <text class="d-label" x="640" y="208">Caja 2 × 2 × 1.5</text>
</svg>
```

## 2. Puntas de flecha (marcadores)

`orient="auto-start-reverse"` permite usar el mismo marcador al inicio y al final. `context-stroke` hereda el color de la línea, así una flecha `.hot` sale del tono sin duplicar marcadores. Para el triángulo hueco de UML el relleno es el fondo (`.ill-bg`).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 480" role="img" aria-labelledby="r2-t r2-d">
  <title id="r2-t">Tipos de flecha</title>
  <desc id="r2-d">Cinco líneas con distinta punta: normal, abierta, herencia, composición y agregación.</desc>
  <defs>
    <marker id="r2-n" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="d-arrow" d="M0 0L10 5L0 10z"/></marker>
    <marker id="r2-o" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="context-stroke" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>
    <marker id="r2-h" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="8" markerHeight="8" orient="auto"><path class="ill-bg" d="M1 1L11 6L1 11z" stroke="context-stroke" stroke-width="1.4" stroke-linejoin="round"/></marker>
    <marker id="r2-c" viewBox="0 0 16 10" refX="1" refY="5" markerWidth="11" markerHeight="7" orient="auto"><path class="d-arrow" d="M1 5L8 1L15 5L8 9z"/></marker>
    <marker id="r2-a" viewBox="0 0 16 10" refX="1" refY="5" markerWidth="11" markerHeight="7" orient="auto"><path class="ill-bg" d="M1 5L8 1L15 5L8 9z" stroke="context-stroke" stroke-width="1.2" stroke-linejoin="round"/></marker>
  </defs>
  <path class="d-line" d="M400 60H840" marker-end="url(#r2-n)"/>
  <path class="d-line" d="M400 150H840" marker-end="url(#r2-o)"/>
  <path class="d-line" d="M400 240H840" marker-end="url(#r2-h)"/>
  <path class="d-line" d="M400 330H840" marker-start="url(#r2-c)"/>
  <path class="d-line hot" d="M400 420H840" marker-start="url(#r2-a)"/>
  <text class="d-text" x="40" y="68">Flecha normal</text>
  <text class="d-text" x="40" y="158">Flecha abierta</text>
  <text class="d-text" x="40" y="248">Herencia (UML)</text>
  <text class="d-text" x="40" y="338">Composición</text>
  <text class="d-text" x="40" y="428">Agregación</text>
</svg>
```

## 3. Callouts numerados con leyenda

Círculo de radio 18 con número, línea guía recta u ortogonal **debajo** del círculo y de las formas, y leyenda al lado. El número va en `style="font-size:20px"` porque `.d-text` fija el tamaño por CSS (el atributo `font-size` no le gana).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 400" role="img" aria-labelledby="r3-t r3-d">
  <title id="r3-t">Formulario con anotaciones</title>
  <desc id="r3-d">Un formulario con campo de correo y botón; dos círculos numerados lo explican en la leyenda.</desc>
  <path class="d-line" d="M522 155H442"/>
  <path class="d-line" d="M522 265H262"/>
  <rect class="d-box" x="60" y="80" width="420" height="260" rx="14"/>
  <rect class="d-box tone" x="100" y="130" width="340" height="50" rx="8"/>
  <text class="d-text" x="116" y="163">correo@utez.edu.mx</text>
  <rect class="d-box fill" x="100" y="240" width="160" height="50" rx="8"/>
  <text class="d-text on-fill" x="180" y="273" text-anchor="middle">Enviar</text>
  <circle class="d-box fill" cx="540" cy="155" r="18"/>
  <text class="d-text on-fill" style="font-size:20px" x="540" y="162" text-anchor="middle">1</text>
  <circle class="d-box fill" cx="540" cy="265" r="18"/>
  <text class="d-text on-fill" style="font-size:20px" x="540" y="272" text-anchor="middle">2</text>
  <text class="d-text" x="574" y="163">Campo de correo</text>
  <text class="d-text" x="574" y="273">Botón de envío</text>
</svg>
```

## 4. Caja de clase UML con herencia

Tres rectángulos apilados (nombre en negrita centrado, atributos, métodos); el texto empieza en `x = caja.x + 16`. Visibilidad con `+` / `-`. La herencia es una línea sólida con triángulo hueco que apunta a la superclase.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 530" role="img" aria-labelledby="r4-t r4-d">
  <title id="r4-t">Herencia Perro hereda de Animal</title>
  <desc id="r4-d">Diagrama de clases UML: la clase Perro hereda de la clase Animal; se muestran atributos y métodos.</desc>
  <defs>
    <marker id="r4-h" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="8" markerHeight="8" orient="auto"><path class="ill-bg" d="M1 1L11 6L1 11z" stroke="context-stroke" stroke-width="1.4" stroke-linejoin="round"/></marker>
  </defs>
  <path class="d-line" d="M450 330V230" marker-end="url(#r4-h)"/>
  <rect class="d-box" x="280" y="30" width="340" height="56"/>
  <rect class="d-box" x="280" y="86" width="340" height="88"/>
  <rect class="d-box" x="280" y="174" width="340" height="54"/>
  <text class="d-text" style="font-weight:700" x="450" y="66" text-anchor="middle">Animal</text>
  <text class="d-text" x="296" y="118">+ nombre: String</text>
  <text class="d-text" x="296" y="152">+ edad: int</text>
  <text class="d-text" x="296" y="208">+ hacerSonido(): void</text>
  <rect class="d-box tone" x="280" y="330" width="340" height="56"/>
  <rect class="d-box tone" x="280" y="386" width="340" height="54"/>
  <rect class="d-box tone" x="280" y="440" width="340" height="54"/>
  <text class="d-text" style="font-weight:700" x="450" y="366" text-anchor="middle">Perro</text>
  <text class="d-text" x="296" y="420">+ raza: String</text>
  <text class="d-text" x="296" y="474">+ ladrar(): void</text>
</svg>
```

## 5. Nodos de red con íconos

Rectángulo redondeado + ícono (`<symbol>` propio, porque un `.svg` suelto no tiene el sprite del deck; dentro de un deck puedes usar `<use href="#i-server"/>` directamente) + etiqueta centrada. Conectores ortogonales con la etiqueta del protocolo **encima** de la línea, nunca sobre ella.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 520" role="img" aria-labelledby="r5-t r5-d">
  <title id="r5-t">Topología cliente, router, servidor y base de datos</title>
  <desc id="r5-d">Un cliente llega por HTTPS a un router, que lo envía al servidor; el servidor consulta una base de datos por SQL.</desc>
  <defs>
    <marker id="r5-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="d-arrow" d="M0 0L10 5L0 10z"/></marker>
    <symbol id="r5-pc" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/></symbol>
    <symbol id="r5-rt" viewBox="0 0 24 24"><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 16.5h.01M11 16.5h.01M8 13V8M16 13V8"/></symbol>
    <symbol id="r5-sv" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="6" rx="1.5"/><rect x="3" y="14" width="18" height="6" rx="1.5"/><path d="M7 7h.01M7 17h.01"/></symbol>
    <symbol id="r5-db" viewBox="0 0 24 24"><ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></symbol>
  </defs>
  <path class="d-line" d="M240 125H350" marker-end="url(#r5-a)"/>
  <path class="d-line" d="M550 125H660" marker-end="url(#r5-a)"/>
  <path class="d-line hot" d="M760 190V330" marker-end="url(#r5-a)"/>
  <rect class="d-box" x="40" y="60" width="200" height="130" rx="14"/>
  <use href="#r5-pc" class="d-ico" x="112" y="76" width="56" height="56"/>
  <text class="d-text" x="140" y="170" text-anchor="middle">Cliente</text>
  <rect class="d-box" x="350" y="60" width="200" height="130" rx="14"/>
  <use href="#r5-rt" class="d-ico" x="422" y="76" width="56" height="56"/>
  <text class="d-text" x="450" y="170" text-anchor="middle">Router</text>
  <rect class="d-box tone" x="660" y="60" width="200" height="130" rx="14"/>
  <use href="#r5-sv" class="d-ico tone" x="732" y="76" width="56" height="56"/>
  <text class="d-text" x="760" y="170" text-anchor="middle">Servidor</text>
  <rect class="d-box" x="660" y="330" width="200" height="130" rx="14"/>
  <use href="#r5-db" class="d-ico" x="732" y="346" width="56" height="56"/>
  <text class="d-text" x="760" y="440" text-anchor="middle">Base de datos</text>
  <text class="d-label" x="295" y="108" text-anchor="middle">HTTPS</text>
  <text class="d-label" x="605" y="108" text-anchor="middle">reenvía</text>
  <text class="d-label" x="780" y="268">SQL</text>
</svg>
```

## 6. Cilindro de base de datos

Elipse superior + cuerpo + arco inferior del mismo relleno; las franjas son arcos que repiten la curvatura inferior (`A rx ry 0 0 0`). El contorno se dibuja aparte para que no se duplique entre las partes.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 420" role="img" aria-labelledby="r6-t r6-d">
  <title id="r6-t">Base de datos</title>
  <desc id="r6-d">Cilindro que representa una base de datos con la tabla usuarios.</desc>
  <!-- grid: cx=450, rx=120, ry=36; top cy=100, body bottom cy=300 -->
  <path class="ill-soft" d="M330 100V300A120 36 0 0 0 570 300V100Z"/>
  <ellipse class="ill-surface" cx="450" cy="100" rx="120" ry="36"/>
  <path class="ill-line" d="M330 100V300A120 36 0 0 0 570 300V100"/>
  <path class="ill-line" d="M330 180A120 36 0 0 0 570 180"/>
  <ellipse class="ill-line" cx="450" cy="100" rx="120" ry="36"/>
  <text class="d-text" x="450" y="262" text-anchor="middle">usuarios</text>
  <text class="d-label" x="450" y="390" text-anchor="middle">PostgreSQL</text>
</svg>
```

## 7. Línea de tiempo

Eje horizontal, hitos equiespaciados y etiquetas que alternan arriba y abajo para que ninguna choque con la vecina. Un solo hito en `--tone` (el actual).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 480" role="img" aria-labelledby="r7-t r7-d">
  <title id="r7-t">Línea de tiempo del cuatrimestre</title>
  <desc id="r7-d">Cuatro hitos: entorno en la semana 1, Git en la 4, API en la 8 y proyecto final en la 14.</desc>
  <path class="d-line" d="M60 240H840"/>
  <path class="d-line" d="M140 226V196M540 226V196M340 254V284M740 254V284"/>
  <circle class="d-dot" cx="140" cy="240" r="14"/>
  <circle class="d-dot" cx="340" cy="240" r="14"/>
  <circle class="d-dot" cx="540" cy="240" r="14"/>
  <circle class="d-box tone" cx="740" cy="240" r="14"/>
  <text class="d-label" x="140" y="188" text-anchor="middle">Sem 1</text>
  <text class="d-text" x="140" y="158" text-anchor="middle">Entorno</text>
  <text class="d-label" x="340" y="312" text-anchor="middle">Sem 4</text>
  <text class="d-text" x="340" y="350" text-anchor="middle">Git y GitHub</text>
  <text class="d-label" x="540" y="188" text-anchor="middle">Sem 8</text>
  <text class="d-text" x="540" y="158" text-anchor="middle">API REST</text>
  <text class="d-label" x="740" y="312" text-anchor="middle">Sem 14</text>
  <text class="d-text" x="740" y="350" text-anchor="middle">Proyecto final</text>
</svg>
```

## 8. Arquitectura por capas

Bandas de ancho completo, título de capa a la izquierda, componentes a la derecha y flechas **solo entre capas adyacentes**, con el verbo en el hueco entre bandas (40 px de espacio para que la etiqueta no toque ninguna banda).

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 440" role="img" aria-labelledby="r8-t r8-d">
  <title id="r8-t">Arquitectura en tres capas</title>
  <desc id="r8-d">Presentación llama a dominio y dominio usa persistencia; cada capa contiene tres componentes.</desc>
  <defs>
    <marker id="r8-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="d-arrow" d="M0 0L10 5L0 10z"/></marker>
  </defs>
  <path class="d-line hot" d="M315 110V190" marker-end="url(#r8-a)"/>
  <path class="d-line hot" d="M315 250V330" marker-end="url(#r8-a)"/>
  <rect class="d-box" x="40" y="30" width="820" height="100" rx="14"/>
  <rect class="d-box" x="40" y="170" width="820" height="100" rx="14"/>
  <rect class="d-box" x="40" y="310" width="820" height="100" rx="14"/>
  <text class="d-label" x="64" y="85">Presentación</text>
  <text class="d-label" x="64" y="225">Dominio</text>
  <text class="d-label" x="64" y="365">Persistencia</text>
  <rect class="d-box tone" x="220" y="50" width="190" height="60" rx="10"/>
  <text class="d-text" x="315" y="88" text-anchor="middle">Controlador</text>
  <rect class="d-box tone" x="430" y="50" width="190" height="60" rx="10"/>
  <text class="d-text" x="525" y="88" text-anchor="middle">Vista</text>
  <rect class="d-box tone" x="640" y="50" width="190" height="60" rx="10"/>
  <text class="d-text" x="735" y="88" text-anchor="middle">Validación</text>
  <rect class="d-box tone" x="220" y="190" width="190" height="60" rx="10"/>
  <text class="d-text" x="315" y="228" text-anchor="middle">Servicio</text>
  <rect class="d-box tone" x="430" y="190" width="190" height="60" rx="10"/>
  <text class="d-text" x="525" y="228" text-anchor="middle">Entidad</text>
  <rect class="d-box tone" x="640" y="190" width="190" height="60" rx="10"/>
  <text class="d-text" x="735" y="228" text-anchor="middle">Regla</text>
  <rect class="d-box tone" x="220" y="330" width="190" height="60" rx="10"/>
  <text class="d-text" x="315" y="368" text-anchor="middle">Repositorio</text>
  <rect class="d-box tone" x="430" y="330" width="190" height="60" rx="10"/>
  <text class="d-text" x="525" y="368" text-anchor="middle">Mapeador</text>
  <rect class="d-box tone" x="640" y="330" width="190" height="60" rx="10"/>
  <text class="d-text" x="735" y="368" text-anchor="middle">Conexión</text>
  <text class="d-label" x="335" y="156">llama</text>
  <text class="d-label" x="335" y="296">usa</text>
</svg>
```

## 9. Flujo cliente–servidor (petición y respuesta)

Dos participantes con línea de vida punteada; la petición va con línea sólida y la respuesta punteada, cada una con su etiqueta encima.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 440" role="img" aria-labelledby="r9-t r9-d">
  <title id="r9-t">Petición HTTP y respuesta</title>
  <desc id="r9-d">El cliente envía GET /alumnos al servidor y el servidor responde 200 con JSON.</desc>
  <defs>
    <marker id="r9-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="d-arrow" d="M0 0L10 5L0 10z"/></marker>
  </defs>
  <path class="d-line dash" d="M180 90V400M720 90V400"/>
  <path class="d-line hot" d="M180 200H720" marker-end="url(#r9-a)"/>
  <path class="d-line dash" d="M720 320H180" marker-end="url(#r9-a)"/>
  <rect class="d-box" x="70" y="30" width="220" height="60" rx="12"/>
  <text class="d-text" x="180" y="68" text-anchor="middle">Cliente</text>
  <rect class="d-box tone" x="610" y="30" width="220" height="60" rx="12"/>
  <text class="d-text" x="720" y="68" text-anchor="middle">Servidor</text>
  <text class="d-text" x="450" y="184" text-anchor="middle">GET /alumnos</text>
  <text class="d-text" x="450" y="304" text-anchor="middle">200 OK · JSON</text>
</svg>
```

## 10. Wireframe de interfaz

Solo rectángulos: marco, encabezado, barra lateral, tarjetas y barras de texto simuladas (`.d-box` bajas). Un único botón relleno como foco. Sirve para explicar pantallas sin captura real ni datos personales.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 440" role="img" aria-labelledby="r10-t r10-d">
  <title id="r10-t">Wireframe de una app</title>
  <desc id="r10-d">Ventana con encabezado, menú lateral, dos tarjetas y un botón Guardar.</desc>
  <rect class="d-box" x="100" y="20" width="700" height="400" rx="14"/>
  <rect class="d-box" x="100" y="20" width="700" height="60" rx="14"/>
  <text class="d-text" x="130" y="60">Mi App</text>
  <circle class="d-dot" cx="730" cy="50" r="7"/>
  <circle class="d-dot" cx="752" cy="50" r="7"/>
  <circle class="d-dot" cx="774" cy="50" r="7"/>
  <rect class="d-box" x="120" y="100" width="170" height="300" rx="10"/>
  <text class="d-label" x="140" y="132">Menú</text>
  <rect class="d-box" x="140" y="160" width="130" height="24" rx="6"/>
  <rect class="d-box" x="140" y="210" width="130" height="24" rx="6"/>
  <rect class="d-box" x="140" y="260" width="130" height="24" rx="6"/>
  <rect class="d-box tone" x="320" y="100" width="220" height="140" rx="10"/>
  <text class="d-text" x="340" y="140">Tarjeta 1</text>
  <rect class="d-box" x="340" y="164" width="180" height="14" rx="5"/>
  <rect class="d-box" x="340" y="190" width="120" height="14" rx="5"/>
  <rect class="d-box tone" x="560" y="100" width="220" height="140" rx="10"/>
  <text class="d-text" x="580" y="140">Tarjeta 2</text>
  <rect class="d-box" x="580" y="164" width="180" height="14" rx="5"/>
  <rect class="d-box" x="580" y="190" width="120" height="14" rx="5"/>
  <rect class="d-box fill" x="320" y="330" width="160" height="56" rx="10"/>
  <text class="d-text on-fill" x="400" y="366" text-anchor="middle">Guardar</text>
</svg>
```

## Fuentes

- Anthropic, *canvas-design* (diseño primero, el último pase refina y no agrega formas): https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md
- svg-precision-skill (especificación con coordenadas fijas → construir → validar → vista previa PNG): https://agentpedia.codes/agent-skills/ui-design/svg-precision-skill
- Marcadores y `context-stroke`: MDN, https://developer.mozilla.org/en-US/docs/Web/SVG/Element/marker
- Proyección isométrica 30°: fórmula estándar de proyección axonométrica (ver `svg-skills.md` en `.cmx_vault/investigacion/`).
