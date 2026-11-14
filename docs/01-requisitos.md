# 01 — Requisitos funcionales

**Proyecto:** Mindset & EV Leak Finder  
**Autor:** Mario Ramírez García  
**Versión:** 0.6 — Dashboard  
**Fecha:** 11 de noviembre de 2026  
**Estado:** Dashboard especificado. Pendiente de validación y de las demás pantallas.

> Documento vivo. Se redacta por pantallas. Esta versión cubre el **Dashboard macro** y sus overlays globales. Las pantallas de Importar, Historial, Visor, Mi Baseline, Glosario y Etiquetado se añadirán en secciones posteriores.
>
> Fuente de verdad de la UI: el prototipo (`sources/Mindset-EV-Leak-Finder-TFG.pptx`).  
> Fuente de verdad del comportamiento: `sources/master-doc.txt`.  
> Si hay contradicción entre fuentes, se documenta y se pregunta antes de decidir.

---

## 0. Convenciones

- **ID:** `RF-DSH-<bloque>-<nn>` para requisitos funcionales del Dashboard.
- **Bloques:** `SHL` shell, `KPI` indicadores, `FAT` fatiga, `FED` feed, `SUM` resumen, `ORG` origen, `TST` toasts, `CFG` configuración, `EST` estados, `GLB` alcance global.
- **Granularidad:** un RF agrupa una capacidad verificable. Los detalles de comportamiento se recogen como criterios `a)`, `b)`, `c)` dentro del mismo RF.
- **Criterios de aceptación:** comprobables sin ambigüedad; se referencian como `RF-DSH-KPI-02.c`.
- **Prioridad:** todos los requisitos listados son de alcance MVP.
- **Parámetros:** los valores concretos que configuran el producto se recogen en la sección 1.10. Un requisito remite allí cuando depende de un valor todavía no fijado.
- **Datos:** el sistema solo opera con datos reales. La interfaz no muestra valores inventados.

---

## 1. Dashboard macro

### 1.1 Propósito

El Dashboard responde a una pregunta: **¿cómo estoy jugando contra mi baseline y qué merece auditoría en el último lote?**

No juzga el resultado económico. Muestra evidencia conductual contrastada contra el baseline individual y separa mala suerte de mal juego.

### 1.2 Alcance

**Incluido:**

- Shell global: cabecera, navegación, importación y cuenta.
- Cuatro KPIs del baseline.
- Gráfica de fatiga.
- Feed de alertas del último lote.
- Resumen del lote.
- Origen de los datos.
- Toasts.
- Drawer de cuenta y modales de configuración.
- Modales explicativos de métricas.
- Estados, accesibilidad y comportamiento global.

**Excluido de esta sección:**

- Importar Manos (solo punto de entrada).
- Historial de torneos.
- Visor de torneo y visor de mano.
- Ventana T+30 como pantalla.
- Mi Baseline y recalibración.
- Glosario.
- Etiquetado colaborativo (Nivel 2).

La recalibración se ejecuta desde **Mi Baseline**. El Dashboard no incluye el botón de recalibración.

### 1.3 Actores

| Actor | Papel |
|---|---|
| Jugador | Único usuario. Consulta el Dashboard y audita alertas. |
| Sistema | Calcula el baseline, detecta anomalías y alimenta los bloques. |
| Comunidad | No interviene en el Dashboard. El Nivel 2 queda fuera de esta pantalla. |

### 1.4 Mapa de bloques

| Bloque | Propósito | Fuente de datos |
|---|---|---|
| Shell | Navegación y acciones globales | Sesión de usuario |
| KPIs | Resumen del baseline activo | `BaselineSnapshot` |
| Fatiga | Rendimiento por duración de sesión | `BaselineSnapshot` |
| Feed | Alertas y desviaciones del último lote | Detecciones del lote |
| Resumen | Magnitud del lote | `ImportBatch` |
| Origen | Procedencia y fecha del lote | `ImportBatch` |
| Toasts | Confirmación de acciones | Eventos del sistema |
| Overlays | Cuenta y configuración | `UserSession`, `EngineConfig` |

---

### 1.5 Requisitos funcionales

> **Granularidad:** cada `RF-DSH-*` describe una capacidad verificable. Los detalles de comportamiento se recogen como criterios `a)`, `b)`, `c)` dentro del mismo requisito.

#### 1.5.1 Shell y navegación

##### RF-DSH-SHL-01 — Cabecera y navegación global

**Requisito:** El Dashboard muestra una cabecera global con la navegación del producto, que permanece visible durante el scroll y sitúa al usuario en la pantalla actual.

**Criterios de aceptación:**

- **a)** La cabecera es sticky y contiene el logo y la navegación global.
- **b)** La cabecera está presente en todas las pantallas.
- **c)** El logo devuelve al Dashboard desde cualquier pantalla.
- **d)** La navegación incluye “Historial Torneos”, “Baseline”, “Baseline vs Tilt (T+30)” y “Glosario”.
- **e)** El ítem activo se marca fuera del Dashboard; en el Dashboard no hay ítem activo.
- **f)** Existe un `H1` visible con el texto “Dashboard”.
- **g)** El diseño es desktop-first y se valida desde 1280×720.
- **h)** Hasta que se audita el primer lote, “Historial Torneos” y “Baseline vs Tilt (T+30)” aparecen desactivados; “+ Importar Manos” está oculto hasta que exista un baseline.

##### RF-DSH-SHL-02 — Acciones globales de cabecera

**Requisito:** La cabecera ofrece importación y acceso a la cuenta desde cualquier pantalla.

**Criterios de aceptación:**

- **a)** “+ Importar Manos” está visible en la cabecera de todas las pantallas y abre el flujo de importación.
- **b)** El botón de cuenta muestra el nombre de usuario y el sitio activo.
- **c)** Al pulsar el botón de cuenta se abre el drawer de cuenta.
- **d)** “Hero” queda reservado como alias de jugador dentro de las manos.

##### RF-DSH-SHL-03 — Alcance de plataforma

**Requisito:** El Dashboard opera con un único usuario, en Winamax y en formato MTT.

**Criterios de aceptación:**

- **a)** El sitio activo es Winamax.
- **b)** La interfaz opera con un único usuario y no ofrece cambio de usuario.
- **c)** El formato de juego es MTT y no se ofrece cambio de formato.

#### 1.5.2 KPIs del baseline

##### RF-DSH-KPI-01 — Mostrar los cuatro KPIs del baseline activo

**Requisito:** El Dashboard muestra cuatro tarjetas KPI calculadas sobre el snapshot de baseline activo.

**Criterios de aceptación:**

- **a)** Las tarjetas son `Baseline VPIP`, `Baseline PFR`, `Baseline 3-Bet` y `EVbb/100 (ajuste all-in)`, con subtítulos “Entrada voluntaria”, “Subida preflop”, “Resubida” y “Muestra: N manos”.
- **b)** Los valores proceden del snapshot activo.
- **c)** La fila muestra `Muestra: N manos` y `Congelado el <fecha>` junto al KPI de EVbb/100 o en una línea común.
- **d)** VPIP muestra el valor del baseline y, separada, una referencia poblacional para MTT.
- **e)** Se muestra el badge “Baseline inicial” o “Recalibrado”.
- **f)** La versión o fecha de congelación es visible en badge o tooltip.
- **g)** El valor de `EVbb/100` usa color y signo: positivo en verde, negativo en rojo, cero en neutro, siempre con signo explícito.

##### RF-DSH-KPI-02 — Calcular y presentar EVbb/100 con ajuste all-in

**Requisito:** El KPI de rendimiento se expresa como `EVbb/100` con ajuste all-in.

**Criterios de aceptación:**

- **a)** El valor principal es `EVbb/100` con la etiqueta “ajuste all-in”.
- **b)** En manos con all-in se usa el EV esperado según equidad; en el resto, el resultado real.
- **c)** La tarjeta no muestra insignia ni tooltip con el número de all-in ajustados (K32): el prototipo nunca los mostró y el dato no se guarda en el baseline.

##### RF-DSH-KPI-03 — Gestionar los estados del baseline

**Requisito:** El Dashboard gestiona los estados de validez del baseline sin mostrar valores inventados.

**Criterios de aceptación:**

- **a)** Sin baseline, se muestra un estado vacío con la guía “Crear baseline”, que lleva a Mi Baseline en estado vacío, y no se muestran ceros ni la gráfica de fatiga. Los KPIs aparecen en blanco, el feed no se muestra y “+ Importar Manos” permanece oculto.
- **b)** El sistema exige una muestra mínima para crear el baseline; el umbral se define en 1.10.
- **e)** Con baseline y sin ningún lote auditado, los KPIs y la gráfica de fatiga usan la muestra del baseline, el feed muestra “Todavía no hay casos que auditar” con la acción “Importar Manos” y un panel “Baseline actual” (archivos, manos y fecha de creación) sustituye al resumen y al origen del lote.
- **c)** Si la muestra alcanza el mínimo pero no llega al recomendado, se permite crear el baseline con el aviso “muestra pequeña”; el umbral se define en 1.10.
- **d)** Un baseline obsoleto muestra un aviso manual por volumen; la obsolescencia se evalúa con el umbral de 1.10 y no provoca recalibración automática.

##### RF-DSH-KPI-04 — Formato e interacción de las tarjetas

**Requisito:** Las tarjetas KPI tienen un formato y una interacción homogéneos.

**Criterios de aceptación:**

- **a)** Formato español: porcentajes con un decimal y coma; BB/100 con dos decimales, signo y separador de miles.
- **b)** Solo el icono de información abre el modal de métrica.
- **c)** Los valores cambian sin animación al recalibrar.

#### 1.5.3 Gráfica de fatiga

##### RF-DSH-FAT-01 — Propósito, fuente y alcance de la gráfica

**Requisito:** La gráfica muestra el rendimiento esperado por duración de sesión usando el baseline congelado activo.

**Criterios de aceptación:**

- **a)** Título “Degradación por Fatiga: Rendimiento vs. Horas de Sesión”; eje Y “Rendimiento Esperado (EVbb/100)”.
- **b)** El subtítulo es dinámico y muestra el número real de sesiones y el periodo del baseline.
- **c)** La serie se deriva del snapshot activo y usa únicamente sesiones del baseline.
- **d)** La fatiga no entra en el feed de alertas; solo se visualiza aquí.
- **e)** La unidad de sesión es un bloque de manos separadas por un intervalo corto; el umbral se define en 1.10.
- **f)** La agrupación se realiza por sesión, no por torneo ni por día natural.

##### RF-DSH-FAT-02 — Construcción y fusión de tramos

**Requisito:** Los tramos de duración se construyen de forma adaptativa, se congelan con el baseline y se fusionan si no alcanzan muestra suficiente.

**Criterios de aceptación:**

- **a)** El eje X es categórico por tramos; cada punto es un tramo agregado.
- **b)** Los tramos se definen por la mediana de duración: hasta 2 h en intervalos de 30 min; más de 2 h y hasta 5 h en intervalos de 1 h; más de 5 h en intervalos de 2 h.
- **c)** El último tramo es abierto (`X+`).
- **d)** La definición de tramos se congela con el baseline y solo cambia al recalibrar.
- **e)** Si un tramo no alcanza el mínimo de manos, se fusiona con el vecino; el mínimo se define en 1.10.
- **f)** Si tras la fusión sigue sin muestra suficiente, se muestra “Datos insuficientes”.
- **g)** Las etiquetas del eje X adaptan sus unidades: minutos para sesiones cortas y horas para largas.
- **h)** Una única sesión válida puede mostrarse si cumple el mínimo de manos.

##### RF-DSH-FAT-03 — Cálculo del EVbb/100 por tramo

**Requisito:** El `EVbb/100` de cada tramo se calcula ponderando por manos y con la definición única de EV.

**Criterios de aceptación:**

- **a)** Fórmula: `100 × suma(EV de las manos del tramo) / número de manos del tramo`.
- **b)** En all-in se usa el EV esperado; en el resto, el resultado real. La misma definición se usa en baseline, gráfica, feed y visores.

##### RF-DSH-FAT-04 — Representación, zonas y break-even

**Requisito:** La gráfica representa los tramos con línea o barras, con zonas y break-even legibles.

**Criterios de aceptación:**

- **a)** El toggle cambia entre línea y barras sin alterar los datos.
- **b)** El eje Y es dinámico, pero el cero siempre queda visible y se etiqueta “0.0 Breakeven (Equilibrio)”.
- **c)** En línea, el trazo es verde hasta el cruce por cero y rojo después.
- **d)** En barras, verdes para positivos y rojas para negativos; el cero se marca con línea discontinua y etiqueta `0.0`.
- **e)** Las zonas se comunican con color y texto.
- **f)** Existe una leyenda fija que explica zona verde, zona roja, break-even y punto crítico.
- **g)** La línea entre puntos es visual y una nota lo indica.
- **h)** La gráfica no admite clic ni filtrado en el MVP.

##### RF-DSH-FAT-05 — Punto crítico

**Requisito:** El punto crítico se calcula por interpolación lineal y se anota cuando hay cruce por cero.

**Criterios de aceptación:**

- **a)** Se marca el cruce por cero entre tramos.
- **b)** Si no hay cruce, no se muestra la anotación.
- **c)** Si hay varios cruces, se muestra el primero tras la fase positiva.
- **d)** La anotación indica “PUNTO CRÍTICO (0 BB) · <tramo>: Cruce a Pérdidas”.
- **e)** La identificación del punto crítico cuando un tramo vale exactamente 0 se rige por el parámetro correspondiente de 1.10.

##### RF-DSH-FAT-06 — Tooltip, datos del punto y estados vacíos

**Requisito:** El tooltip y los datos de cada punto permiten auditar el tramo, y la gráfica tiene estados vacíos claros.

**Criterios de aceptación:**

- **a)** El tooltip muestra tramo, `EVbb/100`, manos, sesiones e intervalo de confianza del 95 %.
- **b)** Cada punto guarda etiqueta, horas desde/hasta, `EVbb/100`, manos, sesiones, intervalo de confianza, zona e indicador de interpolación.
- **c)** Sin baseline o sin sesiones, la gráfica no se muestra y aparece el estado de inicio con la guía para crear el baseline.

#### 1.5.4 Feed de alertas

##### RF-DSH-FED-01 — Alcance, contenido y regla T+30

**Requisito:** El feed muestra todas las alertas y desviaciones del último lote, con la regla T+30 y métricas auditables.

**Criterios de aceptación:**

- **a)** El feed usa únicamente las alertas del último lote importado.
- **b)** Se muestran todas las alertas y desviaciones del lote; el feed es desplazable.
- **c)** El subtítulo indica que se listan todas las alertas del lote.
- **d)** En T+30, el trigger queda excluido; se analizan las 30 manos posteriores; si dos triggers se solapan, las ventanas se fusionan y las manos compartidas se cuentan una vez.
- **e)** Las métricas guardan numerador y denominador, no solo el porcentaje.

##### RF-DSH-FED-02 — Orden y severidad

**Requisito:** El feed ordena por tipo, magnitud de fuga y fecha, y distingue visualmente tilt y desviación.

**Criterios de aceptación:**

- **a)** Primero las alertas de tilt, después las desviaciones.
- **b)** Dentro de cada tipo, mayor fuga primero; a igualdad, la más reciente.
- **c)** Tilt en rojo y desviación en ámbar.
- **d)** La prioridad de orden se basa en el tipo de alerta.

##### RF-DSH-FED-03 — Tarjeta de alerta

**Requisito:** Cada alerta tiene una tarjeta con la evidencia mínima de la desviación.

**Criterios de aceptación:**

- **a)** La tarjeta muestra badge, torneo, trigger o métrica, ventana o tramo, valor observado, baseline, delta en puntos porcentuales, fuga neta estimada y botón “Auditar”.
- **b)** Cada alerta tiene su propia tarjeta, aunque varias sean del mismo torneo.
- **c)** Solo el botón “Auditar” es clicable.
- **d)** La fuga neta se etiqueta “Fuga Neta Estimada”; su fórmula se define en 1.10. Es el coste en BB de haber jugado distinto al baseline, medido en EV para no atribuir a la conducta la suerte de los all-in. Se muestra como magnitud positiva en BB (K33).
- **e)** La tarjeta muestra la evidencia indicada en `a)` y omite metadatos estadísticos secundarios.

##### RF-DSH-FED-04 — Auditar una alerta

**Requisito:** Auditar una alerta abre la evidencia exacta, la retira del feed y la conserva en el historial.

**Criterios de aceptación:**

- **a)** Tilt abre en la mano trigger; desviación abre al inicio del tramo.
- **b)** Al abrir el visor, la alerta pasa a auditada, desaparece del feed y sube la siguiente.
- **c)** La alerta se conserva en el historial.
- **d)** El enlace al historial muestra un contador de alertas; el criterio de recuento se define en 1.10.

##### RF-DSH-FED-05 — Estado vacío y alcance del feed

**Requisito:** El feed tiene un estado vacío claro y limita sus acciones a la auditoría.

**Criterios de aceptación:**

- **a)** Si no hay alertas o todas están auditadas, se muestra “Sin alertas pendientes en este lote” y un enlace al historial.
- **b)** El feed no ofrece descartar ni silenciar alertas en el MVP.
- **c)** Si todavía no se ha auditado ningún lote, el feed no habla de “este lote” sino de que no hay casos que auditar, y ofrece “Importar Manos”.

#### 1.5.5 Resumen del lote y origen de datos

##### RF-DSH-SUM-01 — Resumen del lote

**Requisito:** El resumen cuantifica el lote y sus alertas.

**Criterios de aceptación:**

- **a)** Etiqueta `TORNEOS` con el recuento del último lote.
- **b)** Etiqueta `CON ALERTA` con los torneos que tienen al menos una alerta de tilt o desviación; la fatiga no cuenta. El criterio exacto cuando un torneo acumula ambos tipos se define en 1.10.
- **c)** Porcentaje de manos en T+30: numerador = manos dentro de ventanas T+30, sin duplicar solapes y truncando al final del torneo; denominador = manos totales del lote. Se muestra el valor absoluto y el denominador en tooltip.
- **d)** El recuento de `CON ALERTA` se rige por el parámetro correspondiente de 1.10.

##### RF-DSH-SUM-02 — Validez del lote

**Requisito:** El Dashboard opera sobre un lote válido y no muestra datos de lotes vacíos o duplicados.

**Criterios de aceptación:**

- **a)** Todo lote contiene manos; la validación se realiza en Importar Manos.
- **b)** Solo se cuentan archivos válidos; los rechazados no suman.
- **c)** No existen manos duplicadas; los archivos representan torneos completos. La lógica se define en Importar Manos.

##### RF-DSH-ORG-01 — Origen, fecha y periodo del lote

**Requisito:** El bloque de origen identifica la procedencia, la fecha de carga y el periodo del lote.

**Criterios de aceptación:**

- **a)** La fecha de carga se muestra con la etiqueta “Cargado el”.
- **b)** Las fechas se guardan en UTC y se muestran en la zona local del usuario.
- **c)** Se muestra el periodo cubierto por el lote.
- **d)** Se muestran archivos, manos, fecha y periodo.

##### RF-DSH-ORG-02 — Alcance informativo del bloque de origen

**Requisito:** El bloque de origen presenta exclusivamente la información de procedencia del lote.

**Criterios de aceptación:**

- **a)** El bloque no muestra badge de estado de auditoría.
- **b)** El bloque no enlaza a la lista de archivos.

#### 1.5.6 Toasts

##### RF-DSH-TST-01 — Comportamiento general de los toasts

**Requisito:** Los toasts se comportan de forma homogénea en duración, apilamiento y persistencia.

**Criterios de aceptación:**

- **a)** Los éxitos duran 6–8 s y se cierran solos o con la X; los errores permanecen hasta que el usuario los cierra.
- **b)** Como máximo hay dos toasts apilados; el más nuevo aparece arriba.
- **c)** Los errores persisten al navegar; los éxitos desaparecen al cambiar de pantalla.
- **d)** Si coinciden auditoría y recalibración, los toasts se encolan y se muestran uno tras otro.

##### RF-DSH-TST-02 — Toast de recalibración

**Requisito:** El toast de recalibración confirma el nuevo baseline.

**Criterios de aceptación:**

- **a)** Texto: “Baseline actualizado y congelado · N manos”.
- **b)** El toast no muestra métricas adicionales.
- **c)** El toast no incluye enlace al historial.

##### RF-DSH-TST-03 — Toast de auditoría y errores

**Requisito:** El toast de auditoría resume el lote y enlaza a las alertas nuevas; el toast de error informa del fallo.

**Criterios de aceptación:**

- **a)** Texto: “Auditoría completada · X torneos y Y manos procesadas · Z alertas en el feed”.
- **b)** El enlace “Ver alertas nuevas” filtra el historial por el lote.
- **c)** El toast de error muestra el mensaje del fallo.
- **d)** Los toasts de auditoría y de error no ofrecen deshacer.

#### 1.5.7 Overlays y configuración

##### RF-DSH-CFG-01 — Drawer de cuenta global

**Requisito:** El drawer de cuenta es global y reúne identidad, configuración y versión del motor.

**Criterios de aceptación:**

- **a)** El drawer y los modales se abren desde cualquier pantalla.
- **b)** El drawer muestra nombre de usuario, sitio activo y estado “Activa”.
- **c)** El drawer incluye “Ventana reactiva”, “Sensibilidad (FDR q)” y “Nivel de juego”.
- **d)** El drawer muestra la versión del motor y la fecha de la última recalibración.

##### RF-DSH-CFG-02 — Configuración del motor

**Requisito:** La configuración del motor se edita en modales con guardado explícito y efecto solo en el siguiente lote.

**Criterios de aceptación:**

- **a)** Ventana reactiva: T+20, T+30, T+50 y T+100; la opción activa lleva badge; nota de que se aplica al siguiente lote; acciones Cancelar y Guardar cambios.
- **b)** Sensibilidad: `q < 0,10`, `q < 0,05` y `q < 0,01`; nota de que se aplica tras la corrección FDR y al siguiente lote.
- **c)** Los cambios se aplican al pulsar “Guardar cambios”.
- **d)** Si se cierra con cambios sin guardar, se pide confirmación.
- **e)** La ventana reactiva y la sensibilidad afectan únicamente al siguiente lote.
- **f)** El nivel de juego (buy-in habitual en MTT) se elige al crear la cuenta y se puede cambiar desde el drawer; el cambio afecta solo a las etiquetas posteriores.

##### RF-DSH-CFG-03 — Modales de métricas y glosario

**Requisito:** Los modales de métricas explican cada KPI y enlazan al término correspondiente del glosario.

**Criterios de aceptación:**

- **a)** Categoría “PÓKER · MÉTRICAS”, título, definición, bloque “CÓMO SE LEER” con el dato del baseline y acciones “Entendido” y “Ver en el Glosario”.
- **b)** “Ver en el Glosario” abre el término concreto.

##### RF-DSH-CFG-04 — Cierre de sesión

**Requisito:** El cierre de sesión pide confirmación.

**Criterios de aceptación:**

- **a)** Se muestra un diálogo de confirmación antes de cerrar sesión.

#### 1.5.8 Estados y accesibilidad

##### RF-DSH-EST-01 — Estados por bloque

**Requisito:** Cada bloque del Dashboard tiene estados de vacío, carga, error, parcial y sin permisos.

**Criterios de aceptación:**

- **a)** Los cinco estados existen por bloque.
- **b)** La carga usa skeletons por bloque.
- **c)** El estado parcial indica qué falta y mantiene operativo el resto.
- **d)** El estado sin permisos explica la falta de acceso sin mostrar datos del usuario.

##### RF-DSH-EST-02 — Aislamiento de errores

**Requisito:** Cada bloque falla de forma independiente.

**Criterios de aceptación:**

- **a)** Si falla la gráfica, los KPIs y el feed siguen funcionando.
- **b)** El Dashboard se mantiene operativo aunque falle un bloque.

##### RF-DSH-EST-03 — Accesibilidad, tema e idioma

**Requisito:** La interfaz aplica el nivel de accesibilidad, el tema y el idioma definidos para el producto.

**Criterios de aceptación:**

- **a)** Estados y alertas usan color, icono y texto.
- **b)** El contraste cumple WCAG AA (mínimo 4,5:1 en texto normal).
- **c)** La navegación por teclado y el lector de pantalla se documentan como limitación del MVP.
- **d)** El tema es oscuro y el idioma es español; los textos están externalizados.
- **e)** El MVP no incorpora adaptación a `prefers-reduced-motion`.

#### 1.5.9 Alcance global e invariantes

##### RF-DSH-GLB-01 — Periodos y aislamiento de datos

**Requisito:** El Dashboard separa los periodos y aísla los datos por usuario, sitio y formato.

**Criterios de aceptación:**

- **a)** Feed y resumen usan el último lote; la gráfica usa el baseline.
- **b)** El Dashboard no incluye selector de periodo.
- **c)** Cada usuario ve exclusivamente sus manos, su baseline y sus alertas de Winamax MTT; ningún bloque mezcla otro usuario, sitio o formato.

##### RF-DSH-GLB-02 — Datos reales y alcance del MVP

**Requisito:** El Dashboard opera con datos reales y se limita al alcance del MVP.

**Criterios de aceptación:**

- **a)** La demo usa manos y etiquetas reales.
- **b)** El alcance se limita a Winamax, un único usuario y MTT.

##### RF-DSH-GLB-03 — Integridad del baseline

**Requisito:** El baseline es inmutable, versionado y libre de data leakage.

**Criterios de aceptación:**

- **a)** El baseline solo usa datos cronológicamente anteriores al periodo evaluado.
- **b)** Recalibrar solo afecta a lotes futuros; las alertas pasadas conservan su snapshot.
- **c)** Cada adición o recalibración crea una versión nueva congelada; la anterior se conserva intacta.
- **d)** Sustituir el baseline archiva la versión anterior y conserva sus archivos.
- **e)** Deshacer y restaurar eliminan la versión recién creada, junto con los archivos, torneos y manos que solo incorporó esa acción, y reactivan la anterior; los archivos subidos por error pueden volver a subirse sin detectarse como duplicados. Solo son posibles desde el aviso que aparece al añadir o sustituir; al cambiar de pestaña o cerrarlo, la opción se pierde. Como el aviso desaparece al salir de Mi Baseline, la versión eliminada nunca ha servido para auditar un lote.
- **f)** El baseline inicial excluye automáticamente las ventanas T+30 de los triggers, que se detectan sin baseline; las recalibraciones excluyen además los tramos de desviación, porque ya hay un baseline con el que contrastarlos. Si no hay detecciones, el conjunto excluido queda vacío. La fatiga no se excluye.

##### RF-DSH-GLB-04 — Coherencia de métricas y Nivel 2

**Requisito:** Las métricas y el Nivel 2 son coherentes en todo el producto.

**Criterios de aceptación:**

- **a)** La definición de EV es única: all-in → EV esperado; resto → resultado real.
- **b)** Las métricas guardan numerador y denominador.
- **c)** Las etiquetas comunitarias del Nivel 2 no modifican el baseline ni las alertas del Nivel 1.

---

### 1.6 Reglas de negocio

| ID | Regla |
|---|---|
| RN-DSH-01 | El resultado no define la conducta. Una sesión puede ganar y contener una desviación; puede perder y ser limpia. |
| RN-DSH-02 | El baseline solo usa datos cronológicamente anteriores al periodo evaluado. |
| RN-DSH-03 | En T+30, el trigger queda excluido; se analizan las 30 manos posteriores; los solapes se fusionan. |
| RN-DSH-04 | La fatiga no entra en el feed de alertas; solo se visualiza en la gráfica. |
| RN-DSH-05 | Una etiqueta comunitaria no modifica el baseline ni las alertas del Nivel 1. |
| RN-DSH-06 | El sistema solo usa datos, métricas y etiquetas reales. |
| RN-DSH-07 | Las métricas guardan numerador y denominador, no solo el porcentaje. |
| RN-DSH-08 | El baseline se congela como snapshot inmutable y versionado. |
| RN-DSH-09 | Recalibrar solo afecta a lotes futuros; las alertas pasadas conservan su snapshot. |
| RN-DSH-10 | Añadir datos al baseline crea una versión nueva congelada al momento. |
| RN-DSH-11 | El baseline inicial excluye automáticamente las ventanas T+30 de los triggers; la recalibración excluye además los tramos de desviación. La fatiga se conserva y se mide. |
| RN-DSH-12 | Auditar una alerta es irreversible desde el feed; la alerta permanece en el historial. |
| RN-DSH-13 | El orden del feed es tipo (tilt antes que desviación), magnitud de fuga y fecha. |
| RN-DSH-14 | La definición de EV es única en toda la aplicación: all-in → EV esperado; resto → resultado real. |
| RN-DSH-15 | Sustituir el baseline archiva la versión anterior. Mientras no se deshaga, el historial conserva ambas y las alertas pasadas siguen apuntando al snapshot con el que se calcularon. |
| RN-DSH-16 | Los archivos que se suben para crear el baseline solo construyen el perfil: no se auditan, no generan alertas y no aparecen en el Historial ni en los visores. |
| RN-DSH-18 | Añadir y sustituir crean una versión nueva del baseline. «Deshacer» y «Restaurar» eliminan esa versión recién creada y los datos que solo incorporó, y reactivan la anterior, solo mientras el aviso sigue abierto en Mi Baseline. «Descartar» actúa antes de crear versión. Una versión que ha dado servicio a alguna alerta nunca se elimina. |
| RN-DSH-17 | El nivel de juego lo declara el jugador y solo pondera sus etiquetas del Nivel 2; no se deriva del buy-in de ningún torneo, que no se muestra ni se guarda. |

---

### 1.7 Contrato de datos conceptual

> Este contrato describe **qué necesita el Dashboard**, no tablas definitivas. El modelo de datos se detallará en `docs/02-modelo-datos.md`.

#### `BaselineSummary`

| Campo | Tipo | Uso |
|---|---|---|
| `snapshot_id` | ID | Identifica la versión del baseline |
| `frozen_at` | Fecha/hora UTC | Fecha de congelación |
| `state` | `inicial` / `recalibrado` | Badge de estado |
| `sample_hands` | Entero | Muestra del baseline |
| `sample_files` | Entero | Archivos que componen el baseline (número de torneos de su lista; un archivo es un torneo) |
| `sample_sessions` | Entero | Sesiones que componen el baseline (cifra congelada al crear la versión) |
| `vpip` | Decimal | KPI VPIP |
| `pfr` | Decimal | KPI PFR |
| `threebet` | Decimal | KPI 3-Bet |
| `evbb100` | Decimal | KPI EVbb/100 |
| `vpip_population_range` | Texto | Referencia poblacional MTT |

#### `FatigueBucket`

| Campo | Tipo | Uso |
|---|---|---|
| `bucket_id` | ID | Identificador del tramo |
| `label` | Texto | Etiqueta visible, en minutos u horas |
| `hours_from` | Decimal | Inicio del tramo |
| `hours_to` | Decimal o nulo | Fin del tramo; nulo si es abierto |
| `evbb100` | Decimal | Valor del tramo |
| `hands` | Entero | Manos del tramo |
| `sessions` | Entero | Sesiones representadas |
| `ci_low` | Decimal o nulo | Límite inferior del IC 95 % |
| `ci_high` | Decimal o nulo | Límite superior del IC 95 % |
| `zone` | `positiva` / `negativa` / `cero` | Zona de la gráfica |
| `is_interpolated` | Booleano | Si el punto es una interpolación |
| `is_critical` | Booleano | Si es el punto crítico |

#### `AlertSummary`

| Campo | Tipo | Uso |
|---|---|---|
| `alert_id` | ID | Identificador |
| `type` | `tilt` / `desviacion` | Tipo de alerta |
| `severity_rank` | Entero | Prioridad de orden |
| `tournament_id` | ID | Torneo |
| `trigger_hand` | ID o nulo | Mano trigger, para tilt |
| `window_start` | ID o nulo | Inicio de la ventana T+30 |
| `window_end` | ID o nulo | Fin de la ventana T+30 |
| `tramo_start` | ID o nulo | Inicio del tramo, para desviación |
| `tramo_end` | ID o nulo | Fin del tramo |
| `metric` | Texto | Métrica observada |
| `observed` | Decimal | Valor observado |
| `baseline` | Decimal | Valor del baseline |
| `delta_pp` | Decimal | Diferencia en puntos porcentuales |
| `numerator` | Entero | Numerador de la métrica |
| `denominator` | Entero | Denominador de la métrica |
| `leak_bb` | Decimal | Fuga neta estimada |
| `status` | `pendiente` / `auditada` | Estado en el feed |
| `snapshot_id` | ID | Baseline usado al calcular la alerta |
| `created_at` | Fecha/hora UTC | Fecha de la alerta |

#### `BatchSummary`

| Campo | Tipo | Uso |
|---|---|---|
| `batch_id` | ID | Identificador del lote |
| `tournaments` | Entero | Total de torneos |
| `tournaments_with_alerts` | Entero | Torneos con al menos una alerta |
| `t30_hands` | Entero | Manos en ventanas T+30 |
| `total_hands` | Entero | Manos totales del lote |
| `t30_pct` | Decimal | Porcentaje calculado |
| `valid_files` | Entero | Archivos válidos |
| `rejected_files` | Entero | Archivos rechazados |
| `loaded_at` | Fecha/hora UTC | Fecha de carga |
| `period_start` | Fecha | Inicio del periodo cubierto |
| `period_end` | Fecha | Fin del periodo cubierto |

#### `EngineConfig`

| Campo | Tipo | Uso |
|---|---|---|
| `tilt_window` | `T+20` / `T+30` / `T+50` / `T+100` | Ventana reactiva |
| `fdr_q` | Decimal | Umbral FDR |
| `engine_version` | Texto | Versión del motor |
| `last_recalibration_at` | Fecha/hora UTC | Última recalibración |

#### `UserSession`

| Campo | Tipo | Uso |
|---|---|---|
| `user_id` | ID | Usuario |
| `display_name` | Texto | Nombre visible |
| `email` | Texto | Cuenta |
| `active_site` | Texto | Sitio activo |
| `permissions` | Lista | Acceso a pantallas |
| `play_level` | Texto | Nivel de juego declarado (buy-in habitual) |

#### `Notification`

| Campo | Tipo | Uso |
|---|---|---|
| `type` | `exito` / `error` / `info` | Tipo de toast |
| `text` | Texto | Mensaje |
| `action_label` | Texto o nulo | Acción opcional |
| `action_target` | Texto o nulo | Destino de la acción |
| `duration_ms` | Entero o nulo | Duración; nulo si es persistente |
| `dismissible` | Booleano | Si se puede cerrar |

---

### 1.8 Matriz de estados

| Bloque | Vacío | Carga | Error | Parcial | Sin permisos |
|---|---|---|---|---|---|
| KPIs | Sin baseline + guía | Skeleton | Mensaje por bloque | Valores con aviso | Mensaje |
| Gráfica de fatiga | Sin baseline o sin sesiones | Skeleton | Mensaje por bloque | Serie con aviso | Mensaje |
| Feed | Sin alertas pendientes; sin lotes auditados: «Todavía no hay casos que auditar» | Skeleton | Mensaje por bloque | Alertas con aviso | Mensaje |
| Resumen | Sin lote: lo sustituye el panel «Baseline actual» | Skeleton | Mensaje por bloque | Datos con aviso | Mensaje |
| Origen | Sin lote: lo sustituye el panel «Baseline actual» | Skeleton | Mensaje por bloque | Datos con aviso | Mensaje |
| Shell | No aplica | No aplica | No aplica | No aplica | Menú reducido |

La acción de recuperación de cada error de bloque es la fijada en 1.10: reintentar el bloque y, si persiste, estado parcial y recarga.

---

### 1.9 Fuera de alcance y limitaciones

- Sin versión móvil.
- Sin navegación por teclado ni lector de pantalla.
- Sin tema claro.
- Sin descarte ni silencio de alertas.
- Sin filtros en el feed.
- Sin clic ni filtrado en la gráfica.
- Sin metadatos estadísticos secundarios en la tarjeta del feed.
- Sin badge de estado de auditoría en el origen.
- Sin enlace a los archivos desde el origen.
- Sin deshacer al auditar.
- Sin datos sintéticos.
- Sin multi-sala, multiusuario completo ni cash game.
- Sin HUD en tiempo real.
- Sin replayer 3D animado.
- Sin modo coach.

---

### 1.10 Parámetros del producto

> Los parámetros cerrados se aplican tal cual. Los pendientes quedan marcados “Por definir” y no se sustituyen por valores inventados.

#### Parámetros cerrados

| Parámetro | Valor | Uso |
|---|---|---|
| Ventana reactiva por defecto | T+30 | Feed de alertas |
| Opciones de ventana reactiva | T+20, T+30, T+50, T+100 | Configuración del motor |
| Umbral FDR por defecto | `q < 0,05` | Detección de desviaciones |
| Opciones de sensibilidad FDR | `q < 0,10`, `q < 0,05`, `q < 0,01` | Configuración del motor |
| Intervalo de confianza de la fatiga | 95 % | Gráfica de fatiga |
| Tramos de fatiga | Hasta 2 h: 30 min; más de 2 h y hasta 5 h: 1 h; más de 5 h: 2 h | Gráfica de fatiga |
| Resolución mínima de diseño | 1280×720 | Shell |
| Contraste mínimo | WCAG AA, 4,5:1 en texto normal | Accesibilidad |
| Duración de toast de éxito | 6–8 s | Toasts |
| Toasts apilados | Máximo 2 | Toasts |
| Formato porcentual | Un decimal y coma | KPIs |
| Formato BB/100 | Dos decimales, signo y separador de miles | KPIs |
| Pesos provisionales por nivel de juego | Micro 0,6, Bajo 0,8, Medio 1,0, Alto 1,2 y Muy alto 1,4; se calibrarán con datos reales | Etiquetado del Nivel 2 |
| Manos mínimas para crear un baseline | 2.000 | KPIs y estados |
| Muestra recomendada del baseline | 10.000; por debajo, aviso «muestra pequeña» | KPIs y estados |
| Separación entre sesiones | 30 minutos | Session Builder |
| Separación de tramos de desviación | 10 manos | Detección de tramos |
| Fórmula de la fuga neta | `max(0, (EVbb/100 baseline − EVbb/100 observado) × manos / 100)`; sin EV, «no estimable» | Feed y alertas |
| Suerte all-in neutra | La diferencia entre BB ganadas y All-in EV no supera 1σ (σ = suerte esperable por azar en los all-in del torneo); provisional | Historial y visor de torneo |
| Recuperación ante errores de bloque | Reintentar el bloque; si persiste, estado parcial y recarga | Matriz de estados |
| Aviso cuando el baseline inicial incluye tilt | No aplica: el baseline inicial excluye las ventanas T+30; los tramos de desviación no se pueden detectar sin baseline previo | Transparencia |

#### Parámetros pendientes

| Parámetro | Estado | Uso |
|---|---|---|
| Umbral de obsolescencia del baseline | Fuera del MVP; umbral por definir | Aviso de recalibración |
| Manos mínimas por tramo de fatiga | Por definir | Fusión de tramos |
| Referencia poblacional MTT para VPIP | Por definir | Tarjeta VPIP |
| Cierre de overlays (backdrop, Esc) | Por definir | Overlays |
| Recuento del contador del enlace al historial | Por definir | Feed |
| Definición de `CON ALERTA` con tilt y desviación | Por definir | Resumen |
| Tokens de color y valores de contraste | Por definir | Accesibilidad |
| Copy exacto de toasts y modales | Por definir | Toasts y overlays |
| Punto crítico con un tramo exactamente en 0 | Por definir | Gráfica de fatiga |
| Filtros del enlace del feed al historial | Por definir | Navegación |
| Recuento de `CON ALERTA`: auditadas o pendientes | Por definir | Resumen |

---

### 1.11 Referencias

| Referencia | Ruta | Uso |
|---|---|---|
| Prototipo visual | `sources/Mindset-EV-Leak-Finder-TFG.pptx` | Fuente de verdad de la UI |
| Especificación técnica | `sources/master-doc.txt` | Pipeline, módulos y comportamiento funcional |
| Design Thinking | `sources/design-thinking.pptx` | Investigación UX, personas y decisiones de diseño |

| Diapositiva del prototipo | Contenido | Requisitos |
|---|---|---|
| 5 | Dashboard de una cuenta sin baseline | SHL, KPI, FED |
| 8 | Dashboard con baseline creado y sin lotes auditados | KPI, FAT, FED |
| 9 | Dashboard con gráfica de línea | SHL, KPI, FAT, FED, SUM, ORG |
| 10 | Dashboard con gráfica de barras | FAT |
| 31–33 | Dashboard tras recalibrar (25.000, 15.000 y personalizado) | KPI, TST, FED |
| 34 | Drawer de cuenta | CFG |
| 35 | Modal de ventana de tilt | CFG |
| 36 | Modal de sensibilidad | CFG |
| 37 | Modal de nivel de juego | CFG |
| 51 | Dashboard tras auditar una alerta | KPI, TST, FED |
| 52–55 | Modales de VPIP, PFR, 3-Bet y Winrate | KPI, CFG |
