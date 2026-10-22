# Cheatsheet por tipo (Mermaid 11.4.1)

Cada ejemplo está validado con `uv run mermaid-check`. Todos llevan `accTitle` y `accDescr` justo después de la palabra clave. Los ejemplos pasan sin errores; `mermaid-check` puede avisar `small-text` en sequence, class, ER y gitGraph porque son anchos o altos: en tus diapositivas usa menos nodos o etiquetas más cortas hasta que el aviso desaparezca.

## flowchart: procesos y algoritmos

Usa `flowchart` (no `graph`). `LR` para flujos de ≤ 6 nodos; `TB` para pasos secuenciales largos. IDs estables y etiqueta entre comillas: `userSvc["Servicio de usuarios"]`.

```mermaid
flowchart LR
  accTitle: Flujo de inicio de sesión
  accDescr: Una solicitud se valida; si es válida llega al tablero y si no muestra un error.
  req["Solicitud"] --> ok{"¿Credenciales válidas?"}
  ok -- sí --> dash["Tablero"]
  ok -- no --> err["Error 401"]
  classDef bad fill:#fde8e8,stroke:#b42318,color:#4a0d0a
  class err bad
```

Formas útiles: `[rect]`, `(redondeado)`, `{decisión}`, `[(base de datos)]`, `((círculo))`, `[[subrutina]]`. Subgrafos para agrupar capas:

```mermaid
flowchart TB
  accTitle: Arquitectura en capas
  accDescr: El navegador llama a la API, que usa el servicio y este la base de datos.
  web["Navegador"] --> api
  subgraph Servidor
    api["API REST"] --> svc["Servicio"]
    svc --> db[("PostgreSQL")]
  end
```

Errores comunes: `end` en minúscula como texto (usa `End` o `"end"`); `A---oB` se vuelve arista con círculo (deja espacio: `A --- oB`); paréntesis sin comillas dentro de `[...]`; `linkStyle N` cuenta aristas desde 0 en orden de definición.

## classDiagram: UML estático

Visibilidad `+` público, `-` privado, `#` protegido, `~` paquete. Sufijos: `*` abstracto, `$` estático. Sin `()` es atributo. Genéricos con `~T~` (no con `<T>`). Estereotipos: `<<interface>>`, `<<abstract>>`, `<<enumeration>>`.

| Relación | Sintaxis |
|---|---|
| Herencia | `A <\|-- B` |
| Realización (implementa) | `A <\|.. B` o `B ..\|> A` |
| Composición | `A *-- B` |
| Agregación | `A o-- B` |
| Asociación | `A --> B` |
| Dependencia | `A ..> B` |

Cardinalidad entre comillas: `Order "1" *-- "1..*" Line : contiene`.

```mermaid
classDiagram
  accTitle: Jerarquía de figuras
  accDescr: Figura es abstracta; Circulo hereda de ella e implementa Dibujable.
  direction LR
  class Figura {
    <<abstract>>
    -String nombre
    +area() double*
    +crear()$ Figura
  }
  class Dibujable {
    <<interface>>
    +dibujar() void
  }
  class Circulo {
    -double radio
    +area() double
  }
  Figura <|-- Circulo : extiende
  Dibujable <|.. Circulo
  Pedido "1" *-- "1..*" Linea : contiene
```

Máximo 6 clases por diapositiva; muestra solo atributos y métodos relevantes para la idea.

## sequenceDiagram: interacción en el tiempo

`participant X as Alias` fija el orden. `->>` solicitud, `-->>` respuesta, `->>+` / `-->>-` activan y desactivan. Bloques: `alt/else`, `opt`, `loop`, `par`, `critical`, `break`, cerrados con `end`. `Note over A,B: texto`.

```mermaid
sequenceDiagram
  accTitle: Consulta con caché
  accDescr: El cliente pide datos a la API; si no están en caché los lee de la base de datos.
  autonumber
  participant C as Cliente
  participant A as API
  participant D as Base de datos
  C->>+A: GET /alumnos
  alt en caché
    A-->>C: 200 desde caché
  else sin caché
    A->>+D: SELECT
    D-->>-A: filas
    A-->>-C: 200
  end
  Note over C,A: Idempotente
```

Errores comunes: `;` termina la sentencia (usa `#59;` en el mensaje); `end` como texto de mensaje; colores de `box` requieren `rgb()`.

## stateDiagram-v2: ciclo de vida

`[*]` inicio/fin. Estados con nombre largo: `state "Texto largo" as id`. Compuestos con `state X { ... }`; no hay transiciones entre internos de compuestos distintos.

```mermaid
stateDiagram-v2
  accTitle: Ciclo de vida de un pedido
  accDescr: Un pedido pasa de creado a pagado, enviado y entregado, o se cancela antes del pago.
  [*] --> Creado
  Creado --> Pagado : pagar
  Creado --> Cancelado : cancelar
  Pagado --> Enviado : despachar
  Enviado --> Entregado : confirmar
  Entregado --> [*]
  Cancelado --> [*]
```

## erDiagram: modelo de datos

Cardinalidad (lado izquierdo / derecho): `||` exactamente uno, `|o` cero o uno, `}o` cero o más, `}|` uno o más. `--` identificante, `..` no identificante. Atributos: `tipo nombre PK|FK|UK`.

```mermaid
erDiagram
  accTitle: Alumnos e inscripciones
  accDescr: Un alumno tiene cero o más inscripciones y cada inscripción pertenece a un grupo.
  ALUMNO ||--o{ INSCRIPCION : realiza
  GRUPO ||--o{ INSCRIPCION : recibe
  ALUMNO {
    int id PK
    string matricula UK
    string nombre
  }
  GRUPO {
    int id PK
    string clave
  }
  INSCRIPCION {
    int alumno_id FK
    int grupo_id FK
    date fecha
  }
```

No uses `?` para nulos (llega en v11.16); documenta la opcionalidad con la cardinalidad.

## gitGraph: ramas y fusiones

`commit`, `branch x`, `checkout x`, `merge x`, `cherry-pick id:"..."`. Etiqueta con `commit id:"f1" tag:"v0.1"`.

```mermaid
gitGraph
  accTitle: Flujo con rama de funcionalidad
  accDescr: Se crea una rama feature desde main, se hacen dos commits y se fusiona de vuelta.
  commit id:"inicio"
  branch feature
  checkout feature
  commit id:"f1"
  commit id:"f2"
  checkout main
  merge feature tag:"v0.1"
  commit id:"fix"
```

## mindmap y timeline (breve)

`mindmap` en 11.4.1 no admite `accTitle`/`accDescr` (rompe el parser): descríbelo en el `figcaption` o `aria-label` de la diapositiva; `mermaid-check` avisará de la ausencia y es esperable.

```mermaid
mindmap
  root((POO))
    Pilares
      Encapsulamiento
      Herencia
      Polimorfismo
    Ventajas
      Reuso
```

```mermaid
timeline
  accTitle: Historia de Git
  accDescr: Línea de tiempo con tres hitos de Git.
  title Git
  2005 : Linus Torvalds crea Git
  2008 : Nace GitHub
  2018 : Microsoft compra GitHub
```

## Principales trampas

1. `end` en minúscula dentro de flowchart/sequence rompe el parser.
2. Etiquetas con `()[]{}:;#"/<>` sin comillas.
3. Colores con `var()` o nombres: Mermaid solo acepta hex en `themeVariables` y `classDef`.
4. Más de 12 nodos (6 clases): no se lee en proyector; divide.
5. Usar sintaxis de v12 (radar, treemap, `look: neo`, `autonumber start step`, ER `?`): no existe en 11.4.1.
