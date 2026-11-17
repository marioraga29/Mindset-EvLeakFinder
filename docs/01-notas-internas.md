# 01 — Notas internas del Dashboard

> **Documento interno.** No forma parte de la entrega. Recoge las decisiones tomadas, las dudas abiertas y la trazabilidad de cada decisión hacia los requisitos funcionales de `docs/01-requisitos.md`.

**Proyecto:** Mindset & EV Leak Finder  
**Autor:** Mario Ramírez García  
**Versión:** 1.1  
**Fecha:** 10 de noviembre de 2026

---

## 1. Decisiones cerradas

| ID | Decisión final | Requisitos |
|---|---|---|
| A01 | Sin ítem “Dashboard” en la navegación; el logo vuelve al Dashboard | RF-DSH-SHL-01 |
| A02 | “+ Importar Manos” global | RF-DSH-SHL-02 |
| A03 | Botón de cuenta con nombre de usuario y sitio; “Hero” solo como alias de jugador | RF-DSH-SHL-02 |
| A04 | Cabecera sticky | RF-DSH-SHL-01 |
| A05 | Desktop-first, mínimo 1280×720 | RF-DSH-SHL-01 |
| A06 | H1 visible “Dashboard” | RF-DSH-SHL-01 |
| B01 | Sin baseline: valores vacíos y guía de inicio | RF-DSH-KPI-03, RF-DSH-FAT-06 |
| B02 | No se permite baseline insuficiente; aviso si la muestra es justa | RF-DSH-KPI-03 |
| B03 | Aviso manual de obsolescencia por volumen; sin auto-recalibración. Fuera del MVP: el umbral queda pendiente | RF-DSH-KPI-03 |
| B04 | Referencia poblacional MTT para VPIP en lugar de “Rango óptimo” | RF-DSH-KPI-01 |
| B05 | “Winrate” pasa a `EVbb/100` | RF-DSH-KPI-01, RF-DSH-KPI-02 |
| B06 | Fecha de congelación visible junto a la muestra | RF-DSH-KPI-01 |
| B07 | Formato español: coma decimal, % con un decimal, BB/100 con dos decimales y signo | RF-DSH-KPI-01, RF-DSH-KPI-04 |
| B08 | Solo el icono de información abre el modal | RF-DSH-KPI-04 |
| B09 | Sin animación en los KPIs | RF-DSH-KPI-04 |
| B10 | Solo `EVbb/100` con ajuste all-in | RF-DSH-KPI-02, RF-DSH-FAT-03, RF-DSH-GLB-04 |
| C01 | Eje X categórico por tramos; línea visual | RF-DSH-FAT-02, RF-DSH-FAT-04 |
| C02 | Tramos adaptativos por mediana; congelados con el baseline | RF-DSH-FAT-02 |
| C03 | La etiqueta del tramo sustituye a “Hora 2.5” | RF-DSH-FAT-02 |
| C04 | `EVbb/100` por tramo ponderado por manos | RF-DSH-FAT-03 |
| C05 | Solo sesiones del baseline, para evitar data leakage | RF-DSH-FAT-01, RF-DSH-GLB-01 |
| C06 | El baseline inicial excluye las ventanas T+30 de los triggers y las recalibraciones también los tramos de desviación (ver K06); si no hay detecciones, el conjunto queda vacío; la fatiga no se excluye (sustituido por M03 en las recalibraciones) | RF-DSH-GLB-03 |
| C08 | Tooltip con tramo, EVbb/100, manos, sesiones e IC 95 % | RF-DSH-FAT-06 |
| C09 | Punto crítico por interpolación; primer cruce tras la fase positiva | RF-DSH-FAT-05 |
| C11 | Eje Y dinámico con 0 visible | RF-DSH-FAT-04 |
| C13 | Una sola sesión válida si cumple el mínimo de manos | RF-DSH-KPI-03, RF-DSH-FAT-02 |
| C14 | Subtítulo dinámico con número de sesiones y periodo | RF-DSH-FAT-01 |
| D01 | Solo el último lote importado | RF-DSH-FED-01 |
| D02 | Todas las alertas del lote; scroll; orden tipo → fuga → fecha | RF-DSH-FED-01, RF-DSH-FED-02 |
| D04 | Abrir el visor marca la alerta como auditada y la retira del feed | RF-DSH-FED-04 |
| D05 | Sin descartar ni silenciar alertas | RF-DSH-FED-05 |
| D06 | Solo el botón “Auditar” es clicable | RF-DSH-FED-03 |
| D07 | Tilt abre en la mano trigger; desviación en el inicio del tramo | RF-DSH-FED-04 |
| D08 | Una tarjeta por alerta | RF-DSH-FED-03 |
| D09 | Estado vacío con enlace al historial | RF-DSH-FED-05 |
| D10 | Observado + baseline + delta en puntos porcentuales | RF-DSH-FED-03 |
| D11 | Sin q-value ni confianza en la tarjeta | RF-DSH-FED-03 |
| D12 | Sin fecha ni estado en la tarjeta | RF-DSH-FED-03 |
| D13 | Dos niveles visuales: tilt rojo y desviación ámbar; prioridad por tipo | RF-DSH-FED-02 |
| E01 | Manos T+30 / manos totales del lote | RF-DSH-SUM-01 |
| E02 | Todo lote tiene manos; validación en Importar | RF-DSH-SUM-02 |
| E03 | Solo archivos válidos | RF-DSH-SUM-02 |
| E04 | Sin manos duplicadas; archivos-torneo; lógica en Importar | RF-DSH-SUM-02 |
| E05 | Etiqueta “Cargado el” para la fecha de carga | RF-DSH-ORG-01 |
| E06 | UTC en datos, local en UI | RF-DSH-ORG-01 |
| E07 | Sin badge de estado de auditoría | RF-DSH-ORG-02 |
| E08 | Periodo cubierto visible | RF-DSH-ORG-01 |
| E09 | Sin enlace a los archivos | RF-DSH-ORG-02 |
| F01 | Toasts de éxito de 6–8 s; errores persistentes | RF-DSH-TST-01 |
| F02 | Máximo dos toasts, el más nuevo arriba | RF-DSH-TST-01 |
| F03 | Solo los errores persisten al navegar | RF-DSH-TST-01 |
| F04 | Sin enlace “Ver historial recalibrado” | RF-DSH-TST-02 |
| F05 | “Ver alertas nuevas” filtra por lote | RF-DSH-TST-03 |
| F06 | Sin número de alertas en el toast de recalibración | RF-DSH-TST-02 |
| F07 | Sin reintento en el toast de error | RF-DSH-TST-03 |
| F08 | Toasts encolados si coinciden | RF-DSH-TST-01 |
| F09 | Sin “Deshacer” al auditar | RF-DSH-FED-04, RF-DSH-TST-03 |
| G01 | Overlays globales | RF-DSH-CFG-01 |
| G02 | Guardado explícito | RF-DSH-CFG-02 |
| G03 | Confirmación al cerrar con cambios | RF-DSH-CFG-02 |
| G04 | Configuración solo para el siguiente lote | RF-DSH-CFG-02 |
| G05 | “Ventana reactiva”, T+30 por defecto | RF-DSH-CFG-01, RF-DSH-CFG-02 |
| G06 | “Sensibilidad (FDR q)” | RF-DSH-CFG-01, RF-DSH-CFG-02 |
| G07 | Enlace directo al término del glosario | RF-DSH-CFG-03 |
| G08 | Logout con confirmación | RF-DSH-CFG-04 |
| G09 | ~~Versión del motor y última recalibración visibles~~ Retirado en M12: la v6 (diapositiva 34) no las muestra | RF-DSH-CFG-01 |
| H01 | Estados vacío, carga, error, parcial y sin permisos | RF-DSH-EST-01 |
| H02 | Error por bloque | RF-DSH-EST-02 |
| H03 | Color + icono + texto | RF-DSH-EST-03, RF-DSH-FAT-04, RF-DSH-FED-02 |
| H04 | Contraste WCAG AA | RF-DSH-EST-03 |
| H05 | Sin teclado ni lector de pantalla; limitación declarada | RF-DSH-EST-03 |
| H06 | Solo tema oscuro y español | RF-DSH-EST-03 |
| H07 | Sin `prefers-reduced-motion` | RF-DSH-EST-03 |
| I01 | Feed y resumen del último lote; gráfica del baseline | RF-DSH-GLB-01 |
| I02 | Solo Winamax | RF-DSH-SHL-03, RF-DSH-GLB-02 |
| I03 | Un usuario y un formato | RF-DSH-SHL-03, RF-DSH-GLB-01, RF-DSH-GLB-02 |
| I04 | Versión del baseline visible | RF-DSH-KPI-01 |
| I05 | La gráfica usa solo el baseline congelado | RF-DSH-FAT-01, RF-DSH-GLB-01 |
| I06 | Sesión = bloque de manos separadas por poco tiempo | RF-DSH-FAT-01 |
| I07 | Manos reales en la demo | RF-DSH-GLB-02 |
| I08 | Datos aislados por usuario | RF-DSH-GLB-01 |

**Total:** 81 decisiones cerradas en el Dashboard (A–I), 12 más en el cierre de 7.1 (J01–J12, sección 1.1), 16 en baseline inicial, nivel de juego, buy-in, gestión de archivos, trigger, comparativa y prototipo (K01–K16, sección 1.2) y 6 en la planificación temporal y la gestión del proyecto (L01–L06, sección 1.3).

### 1.1 Cierre de 7.1

| ID | Decisión | Requisitos |
|---|---|---|
| J01 | Mínimo duro del baseline: 2.000 manos | RF-06 |
| J02 | Muestra recomendada: 10.000 manos; por debajo, aviso «muestra pequeña» | RF-06 |
| J03 | Obsolescencia del baseline fuera del MVP; umbral pendiente | RF-07 |
| J04 | Separación de tramos: 10 manos | RF-10 |
| J05 | Fuga neta con EV; sin EV, «no estimable» | RF-12, RF-14 |
| J06 | Rendimiento: Dashboard en menos de 2 s y 10.000 manos en menos de 60 s | RNF-03 |
| J07 | Recuperación: reintentar el bloque y, si persiste, estado parcial y recarga | RNF-11 |
| J08 | Cartas y board en TEXT compacto; el API los entrega estructurados al visor | Modelo |
| J09 | Se conservan todos los snapshots archivados; solo se elimina el snapshot recién creado al deshacer o restaurar (ver K08) | Modelo |
| J10 | Sin `bote_ganador`; basta `participacion.cobrado_bb` | Modelo |
| J11 | Solo se guarda la exclusión; el baseline inicial también excluye ventanas T+30 (matizado por K06) | Modelo |
| J12 | Auditar una alerta es revisar su snapshot, no rejuzgarla con el baseline activo | Modelo, RF-14 |

### 1.2 Baseline inicial y nivel de juego

| ID | Decisión | Requisitos |
|---|---|---|
| K01 | El baseline inicial se crea desde Mi Baseline en estado vacío, al que lleva la guía «Crear baseline» del Dashboard; hasta entonces Importar permanece oculto | RF-06, RF-01, RF-13 |
| K02 | Los archivos del baseline no se auditan: son un lote de tipo `baseline` que solo construye el perfil, sin alertas ni Historial | RF-06, Modelo |
| K03 | El jugador declara su nivel de juego (buy-in habitual en MTT) al registrarse, lo puede cambiar desde el drawer y solo pondera sus etiquetas del Nivel 2 | RF-20, RF-18, Modelo |
| K04 | El buy-in del torneo no se muestra ni se guarda; el nivel de juego declarado es el único dato de nivel y solo pondera etiquetas | RF-03, RF-17, Modelo |
| K05 | El nivel de juego solo pondera las etiquetas del Nivel 2; no ajusta referencias ni baseline. Corregido en el prototipo: el registro y el modal de nivel ya dicen que se ajusta aquí y no modifica lo auditado | RF-20, RF-18 |
| K06 | El baseline inicial solo excluye las ventanas T+30 por trigger, que se detectan sin baseline; los tramos de desviación se excluyen solo en recalibraciones, cuando ya hay baseline. Resuelve P-19 y M-09. La «calidad» de Mi Baseline en el baseline inicial pasa a significar manos fuera de ventanas T+30 | RF-06, RF-07, Modelo |
| K07 | Estados del Dashboard antes del primer lote: sin baseline (KPIs en blanco, sin feed, Importar oculto, Historial y Baseline vs Tilt desactivados) y con baseline sin lotes auditados (KPIs y fatiga con la muestra del baseline, feed «Todavía no hay casos que auditar», panel «Baseline actual», Historial y Baseline vs Tilt desactivados hasta el primer lote). Resuelve P-16 | RF-13, RF-14, RF-15 |
| K08 | Añadir y sustituir archivos del baseline crean una versión nueva. «Deshacer» y «Restaurar» eliminan la versión recién creada y los archivos, torneos y manos que solo incorporó esa acción (si te equivocaste, no queda rastro, y no habrá duplicados falsos), y reactivan la anterior; el aviso solo existe al hacer la acción (se pierde al cambiar de pestaña o cerrarlo), así que esa versión nunca ha servido para auditar un lote. «Descartar» (antes de aplicar) no es «Deshacer» (después de congelar). No se admiten versiones con menos de 2.000 manos | RF-06, RF-07, Modelo |
| K09 | El trigger es un bad beat (all-in perdido con equidad ≥ 70 %) o la pérdida de un bote grande (≥ 40 BB, haya habido all-in o no). Amplía el criterio de `sources/master-doc.txt`, que exigía las dos condiciones a la vez. La pérdida mínima de un bad beat queda por definir (P-20) y el umbral de 40 BB se prevé relativo al tamaño del stack, fuera del MVP | RF-08, Modelo |
| K10 | La Comparativa Baseline vs Tilt (T+30) muestra 5 métricas: VPIP, PFR, 3-Bet, Fold vs 3-Bet y WTSD | Pantalla Baseline vs Tilt |
| K11 | La Comparativa Baseline vs Tilt agrega solo las ventanas T+30 del último lote y las compara con el baseline activo, no con el snapshot de cada alerta (las alertas ya emitidas no cambian). El alcance (último lote, periodo o histórico) está por estudiar y la memoria lo indica con exclamaciones | RF-21 |
| K12 | La pantalla Baseline vs Tilt tiene requisito propio: RF-21 con tres fichas (RF-CMP-01 a RF-CMP-03), colocado al final para no renumerar | RF-21 |
| K13 | Los cinco tramos del nivel de juego (1–5, 5–10, 10–25, 25–50 y 50 € o más) se dejan tal cual: son rangos de nivel que declara el jugador, no una clasificación de torneos, y no se especifican fronteras (un mismo buy-in puede ser caro para un jugador y barato para otro). Los pesos siguen pendientes (P-18) | RF-20, Modelo |
| K14 | Pesos provisionales por nivel de juego para ponderar las etiquetas del Nivel 2: Micro 0,6, Bajo 0,8, Medio 1,0, Alto 1,2 y Muy alto 1,4. Son valores orientativos, crecientes y acotados, que se calibrarán con datos reales cuando haya varios jugadores; con un solo usuario apenas influyen. Se guardan en `etiqueta_mano.peso_aplicado` al etiquetar. Resuelve P-18 | RF-18, RF-20, Modelo |
| K15 | El contexto del torneo de los visores muestra solo formato, manos y resultado: se quitan la posición final y los inscritos, que no están en el `.txt` | RF-16, RF-17 |
| K16 | «Modo coach» se quita del glosario (fuera del MVP); el glosario de Producto queda con 7 términos | RF-19 |
| K17 | El EV de una mano es el valor según la equidad en un all-in y el resultado real en el resto. El All-in EV de un torneo o ventana es la suma de sus manos; sin all-in coincide con las BB ganadas | RF-04, `mano.equidad` |
| K18 | El Historial sustituye «Resultado (EV)» por tres columnas: BB ganadas, All-in EV y Suerte all-in (solo la palabra: A favor, Neutra o En contra) | RF-15, RF-HIS-01, diapositivas 11 y 16–18 |
| K19 | Suerte all-in: diferencia = BB ganadas − All-in EV; σ del torneo = √Σ(bote² · e · (1 − e)) sobre sus all-in; neutra si la diferencia no supera 1σ, a favor si es mayor que +σ y en contra si es menor que −σ; sin all-in, neutra. **1σ provisional**, a revisar con datos reales (con 1σ, un bad beat aislado con equidad ≥ 70 % sale «En contra», coherente con el trigger) | RF-04, `torneo.sigma_suerte_bb`, `torneo.suerte_allin` |
| K20 | Color: BB ganadas y All-in EV conservan verde (≥ 0) y rojo (< 0); Suerte all-in va sin color; el estado conductual conserva verde, ámbar y rojo | RF-15, RF-HIS-01 |
| K21 | Se quita VPIP/PFR del Historial: las métricas de un torneo corto engañan | RF-15, RF-HIS-01 |
| K22 | Visor: un único bloque «Lectura» con dos partes, Conducta y Suerte del torneo (BB ganadas, All-in EV y Suerte all-in), que sustituye a las cajas de impacto, fuga estimada, cierre, contexto, resto del patrón, lectura agregada y EV | RF-16, RF-VTR-05 |
| K23 | Conducta en la ventana T+30: trigger, posición de la mano en la ventana, solo las métricas de la alerta frente al baseline y fuga neta. Se quita «BB adicionales» y los subtramos dentro de la ventana | RF-16, RF-VTR-05, RF-12 |
| K24 | ~~Conducta con desviación sin trigger sin fuga ni tramo (a la espera de P-22)~~ Sustituida por M18: tramo con inicio, fin y fuga neta | RF-16, RF-VTR-05 |
| K25 | Conducta sin alertas: «No se han detectado anomalías conductuales frente a tu baseline», sin métricas del torneo | RF-16, RF-VTR-05 |
| K26 | El contexto del torneo pasa a una línea de la cabecera («Torneo #N · formato · manos»); subtítulo fijo de la gráfica («Resultado real frente a EV esperado, mano a mano»); la leyenda no cambia | RF-16, RF-VTR-01, RF-VTR-04 |
| K27 | Glosario: BB ganadas, All-in EV, Suerte all-in y Fuga neta (paso a paso, con ejemplos con y sin all-in); ⓘ con «Ver en el Glosario» en las cabeceras del Historial y en Suerte all-in y Fuga neta del visor | RF-19, RF-GLO-01 |
| K28 | Composición de cada versión del baseline: entidad de enlace `baseline_snapshot_torneo` (versión y torneo). Dato interno que usan añadir, sustituir, restaurar, deshacer y recalibrar. Sustituir deja fuera todos los archivos anteriores sin importar sus fechas; auditar una alerta no la necesita, porque las cifras del baseline ya están en `metrica_valor` | RF-07, RF-BAS-02, modelo §4.20 |
| K29 | `baseline_snapshot` añade `origen` (inicial, añadir, sustituir o recalibrar), `snapshot_padre_id` (a la que se vuelve al deshacer) y `muestra_sesiones` (congelada, porque las sesiones se recalculan). El número de archivos no se guarda: es el número de torneos de la lista. `tipo` sigue siendo la etiqueta visible: añadir y sustituir siguen siendo «Inicial» y solo recalibrar da «Recalibrado» | RF-06, RF-07, modelo §4.9 |
| K30 | Un archivo es siempre un torneo: no hay entidad `archivo`. «14 archivos → 18 torneos» y «12 archivos · 42 sesiones» eran errores del prototipo (nunca hay más sesiones que archivos) | RF-01, modelo §4.4 |
| K31 | El jugador no consulta versiones anteriores del baseline; solo ve el activo. Cada alerta se audita con su propio baseline y se busca por fecha en el historial. Se quita esa frase de RF-07 | RF-07 |
| K32 | Se quita el ajuste all-in del baseline: sin `allin_manos`, `allin_ajustados`, `ajuste_ev`, insignia con número ni «Sin ajuste EV». El prototipo nunca los mostró | RF-13, RF-DSH-KPI-02 |
| K33 | La fuga neta se muestra como magnitud positiva en BB (por ejemplo 42,5 BB), coherente con el Glosario («si la diferencia es negativa, no hay fuga»). El modelo ya la guarda ≥ 0 | RF-12, RF-14, RF-DSH-FED-03 |

### 1.3 Planificación temporal (memoria 2.2)

| ID | Decisión | Dónde |
|---|---|---|
| L01 | El proyecto empieza el 16 de octubre de 2026 y se planifica hasta finales de mayo de 2027: 33 semanas, de la del 12 de octubre a la del 24 al 30 de mayo | Memoria 2.2 |
| L02 | Solo se planifica lo estimado; las horas reales y la desviación se añaden al terminar | Memoria 2.2 |
| L03 | Seis etapas y 300 h: estudio 20, descubrimiento 30, plan 55, code/build/test 134, operaciones 18 y documentación 43 (reparto tras L05) | Memoria 2.2 |
| L04 | Una tabla Gantt semanal por etapa (tablas 7 a 12). Cada actividad ocupa dos filas: estimada (verde) y real (roja, vacía por ahora) | Memoria 2.2 |

| L05 | El descubrimiento terminó la semana del 2 al 8 de noviembre de 2026 con unas 30 h (estimadas 45). Las 15 h sobrantes se repartieron en las tareas con menos horas: pruebas +5, Nivel 2 +4, release +2, monitorización +1, introducción y conclusiones +2 y memoria del plan +1 | Memoria 2.2 |
| L06 | De 5 solo se redacta 5.1, con datos reales: 3 sprints (16–25 oct, 26 oct–1 nov y 2–8 nov), con las etapas Understand and Empathy, Define, Idea y Prototype; no se hicieron Decide ni Validate. 5.2 y 5.3 se rellenan al avanzar cada fase, sin aproximaciones | Memoria 5.1 |

Los datos viven en `PLANIFICACION` y `GESTION_DESCUBRIMIENTO` de `tools/plantilla_content.py`; el gráfico de horas se genera con `tools/build_planificacion.py`. En 5.1 la división en tres sprints y los días de cada actividad son una propuesta apoyada en las fechas de los archivos (prototipo del 26 de octubre y v2 del 3 de noviembre) y la convención de la plantilla; el usuario puede ajustarla en `GESTION_DESCUBRIMIENTO`.

### 1.4 Idioma, métricas, recalibración, fuga de datos, stack y evaluabilidad (M01–M29)

| ID | Decisión | Requisitos |
|---|---|---|
| M01 | Interfaz solo en español en el MVP, preparada para traducirse (francés e inglés en el futuro) sin rehacer pantallas. (1) Ningún texto visible va en el código: pantallas, avisos, toasts, modales, alertas, bloque «Lectura», tooltips y glosario se cargan desde archivos de traducción por idioma (en el MVP solo `es`) mediante claves, por ejemplo `dashboard.kpi.winrate`. (2) El backend y la base de datos no guardan ni devuelven frases montadas: alertas, lecturas, avisos de muestra pequeña y estados son un código con sus parámetros, por ejemplo `{ "codigo": "alerta_tilt", "metrica": "VPIP", "delta_pp": 8.2 }`, y el frontend compone el texto. (3) Los datos se guardan en bruto (números sin formato, fechas en UTC, métricas con numerador y denominador) y el formato de números, porcentajes y fechas se aplica solo al mostrarlos, según el idioma. (4) Los términos técnicos de póker no se traducen en ningún idioma (VPIP, PFR, 3-Bet, Fold vs 3-Bet, WTSD, bad beat, tilt, trigger, A-Game, EVbb/100, BB, FDR, MTT). (5) El glosario sigue siendo estático en el frontend (decisión ya cerrada), pero su contenido vive en el archivo de traducción. (6) `usuario.idioma` queda fuera del MVP: se añadirá cuando exista un segundo idioma (trabajo futuro) | RNF-12 |
| M02 | Métricas del baseline y la ventana (decidido con el usuario el 14-nov-2026): ambos guardan VPIP, PFR, 3-Bet, Fold vs 3-Bet, WTSD y EVbb/100, las que usa la comparativa Baseline vs Tilt (K10). Fold vs 3-Bet y WTSD siguen dentro del MVP (se guardan y la comparativa las muestra); solo quedan fuera de la detección de tramos, que contrasta VPIP, PFR y 3-Bet, por las pocas oportunidades que tienen en un trozo corto. El Dashboard sigue con cuatro KPIs. C-Bet, Fold vs C-Bet y WSSD salen del MVP y quedan como trabajo futuro. Cierra el punto 16 de la lista de trabajo | RF-04, RF-06, RF-09, RF-10, RF-21, Modelo |
| M03 | Recalibración y fatiga (decidido con el usuario el 14-nov-2026): la recalibración excluye de la muestra los tramos de desviación (automático, K06) y, con dos casillas marcadas por defecto y desmarcables, las ventanas T+30 y la fatiga prolongada. La fatiga prolongada depende de cada jugador: son las manos jugadas desde su punto crítico, el punto en que su gráfica de fatiga cruza a pérdidas, y no una hora fija. Si no tiene punto crítico (pocas manos o una gráfica que nunca cruza a pérdidas), no se excluye fatiga aunque la casilla esté marcada y la pantalla lo indica. El baseline inicial no cambia: solo excluye ventanas T+30 (K06). La gráfica de fatiga se sigue midiendo con todas las manos. Sustituye a C06 en lo relativo a la fatiga; cierra el punto 17 | RF-07, RF-DSH-GLB-03, Modelo (`baseline_exclusion`) |
| M04 | Fuga de datos (decidido con el usuario el 14-nov-2026): al importar para auditar, el torneo que empieza antes de la última mano (`hasta`) del baseline activo no se procesa ni se guarda: se omite con un aviso informativo, como un duplicado y sin tratarlo como error, y el lote continúa con los demás; el aviso dice que ese torneo no se va a auditar. Garantiza que ninguna alerta se calcula con un baseline que contiene partidas posteriores al torneo. La comprobación se hace solo al importar: añadir archivos al baseline después puede mover `hasta` más allá de torneos ya auditados y no los afecta, porque cada alerta conserva su snapshot. Los lotes de tipo `baseline` no se comprueban. Descartado de momento: importarlo sin evaluar, con un estado «Sin evaluar» (el torneo se guardaría y se vería en el Historial). Cierra el punto 20 | RF-01, RF-ING-03, RF-DSH-GLB-03, Modelo (invariante 34) |
| M05 | Profundidad de stack (punto 25, decidido con el usuario el 15-nov-2026): el baseline y la ventana T+30 guardan las cinco métricas de conducta por tramo de stack (menos de 10 BB, 10–20, 20–40 y 40 BB o más, provisionales) además del total, con el campo `tramo_stack` de `metrica_valor` y el código `total` para la cifra global; el EVbb/100 se guarda solo como total y la fuga neta no cambia (el sesgo del stack en la fuga se documenta como limitación). El esperado de cada mano es el valor del baseline en su tramo; si ese tramo tiene menos de 50 oportunidades de la métrica (provisional), se usa el total del baseline. El contraste pasa de la binomial exacta del `master-doc.txt` a un contraste exacto Poisson-binomial, que admite una probabilidad distinta por mano y no aproxima con pocas manos; se aplica a la ventana T+30 y a la detección de tramos. Las filas por tramo son internas: el jugador solo ve el total. Los mínimos de oportunidades por métrica y el estado «no evaluable» se deciden en el punto 27 (P-25); límites y mínimo de 50 se calibrarán con datos reales | RF-06, RF-09, RF-10, RF-21, `metrica_valor`, `prueba_estadistica` |
| M06 | Métricas no evaluables y ventanas cortas (punto 27, decidido con el usuario el 15-nov-2026): (1) una métrica es evaluable en una ventana si sus oportunidades alcanzan el mínimo `max(3, ⌈0,5 × oportunidades habituales del jugador en ese número de manos⌉)`, calculado con su propio baseline (½ y 3 provisionales); (2) la métrica no evaluable no se contrasta y se muestra como «k de n» sin porcentaje, mientras el porcentaje del baseline sí puede verse; (3) la corrección FDR se aplica solo a las métricas evaluables; (4) estados derivados de la ventana: con desviación, sin desviación y sin datos suficientes; (5) la ventana sin datos suficientes aparece en el feed como alerta no concluyente y no cuenta como torneo limpio; (6) el feed ordena por solidez (más métricas evaluables primero), sin exigir las cinco; (7) el análisis de sensibilidad (15, 30 y 60 manos) lo hace el autor con sus datos en la memoria y no forma parte del producto; la ventana óptima por jugador queda como trabajo futuro; (8) las etiquetas del Nivel 2 no completan una métrica con pocas muestras (invariante 5); como contexto junto a un «k de n» podrían mostrarse en el futuro. Derivado por mí y pendiente de revisión: las no concluyentes van al final del feed, sin fuga neta, y el Historial las marca «no concluyente» | RF-09, RF-10, RF-14, RF-15, RF-21, `prueba_estadistica`, `alerta` |
| M07 | Ventana T+30 por sesión y multi-table (puntos 26 y 5, decidido con el usuario el 15-nov-2026): (1) una sola regla: la ventana son las siguientes `ventana_manos` manos del jugador en su sesión, de cualquier torneo, ordenadas por hora; con una mesa coincide con la ventana del torneo y continúa en el siguiente si no hay una pausa de más de 30 minutos; no cruza sesiones; (2) la alerta vive solo en el torneo del trigger; si otro trigger cae dentro de la ventana se fusionan y hay una sola alerta; los demás torneos con manos de la ventana llevan una marca informativa con enlace a la alerta, no generan alerta propia y no cuentan como torneo limpio; (3) mínimo de manos de la ventana = la mitad de la configurada (10 con T+20, 15 con T+30), sin suelo; por debajo, no concluyente y ninguna métrica se contrasta; (4) ventana de 0 manos: no existe, sin alerta ni marca; el trigger se ve en el visor con «sin manos posteriores»; (5) empates de hora: cualquier orden estable; (6) entidad nueva `ventana_mano` (ventana, mano, orden); (7) visor con una pestaña por torneo que aporta manos (solo si son varios), cada una con su gráfica y la franja solo sobre sus manos; la rejilla (diapositiva 47) muestra las manos por hora con su torneo, la fuga neta en lugar del «Resultado adicional», las métricas evaluadas y sin «24 de 30 con pérdida» (ficha RF-VTR-06 y RF-VTR-07, dentro de RF-16). Pendiente en el punto 31: qué «Lectura» y qué `CON ALERTA` ve cada torneo con varias alertas | RF-09, RF-15, RF-16, `ventana_reactiva`, `ventana_mano`, `trigger` |
| M08 | Métricas de la auditoría (decidido con el usuario el 15-nov-2026): la ventana T+30 contrasta y muestra solo VPIP, PFR y 3-Bet, igual que la detección de tramos; la solidez de una alerta va de 0 a 3. Fold vs 3-Bet y WTSD se guardan en la ventana y solo se contrastan en la comparativa Baseline vs Tilt, donde se acumulan las ventanas del lote y tienen oportunidades suficientes. Enmienda M02 y M06 (la familia del FDR de la ventana pasa de 5 a 3 pruebas) | RF-09, RF-VTR-07, RF-21, `prueba_estadistica` |
| M09 | Gráfica de fatiga y `tramo_fatiga` (punto 9, decidido con el usuario el 15-nov-2026): la curva es el promedio de todas las sesiones del baseline, con el tiempo desde el inicio de cada sesión en el eje X; la gráfica tiene siempre el mismo número de puntos y ocupa siempre el mismo espacio, y lo que se adapta al jugador es el ancho de cada tramo (calculado con la duración de sus sesiones); ni el número de puntos, ni la regla del ancho, ni el mínimo de manos por tramo están fijados (por definir). `tramo_fatiga` cuelga del `baseline_snapshot`, se calcula al crear el baseline y se congela con él; guarda horas numéricas, suma de EV, EVbb/100 e intervalo de confianza del 95 %, y el último tramo es abierto; `baseline_snapshot.punto_critico_horas` guarda el punto crítico; la zona se deduce del signo. Precisado el 16-nov-2026: la curva usa las mismas manos que el baseline (sin ventanas T+30 ni, en recalibraciones, tramos de desviación) salvo la exclusión de fatiga, que no se aplica; al recalibrar, la exclusión de la fatiga usa el punto crítico del snapshot padre (derivado por mí, pendiente de revisión) | RF-DET-06, RF-DSH-FAT-02, `tramo_fatiga`, `baseline_snapshot` |
| M10 | Fatiga frente al stack (punto 28, decidido con el usuario el 17-nov-2026): la gráfica de fatiga se queda como está en M09 (EVbb/100 total por tramo horario); la corrección por el EV esperado según el stack (diferencia observado − esperado por mano, con IC 95 %) queda como **trabajo futuro**. Motivos: con multi-table las horas no se corresponden con stacks (a la hora 3 conviven un torneo recién abierto y otro terminando); un stack profundo cambia sobre todo la varianza, no necesariamente la media; el IC de la diferencia saldría ancho; y reabriría M05 y M09 (prototipo, modelo, RF y UML). Encaja después sin reestructurar: el stack por mano y los tramos ya existen, falta guardar el EVbb/100 por tramo en el baseline. Se documenta como limitación | RF-DET-06, RF-DSH-FAT-02, limitaciones |
| M11 | Configuración aplicada por lote (punto 10, decidido con el usuario el 17-nov-2026, que delegó el criterio): `lote_importacion` guarda `ventana_reactiva` y `fdr_q` con los valores de `usuario` al importar, obligatorios en los lotes de `auditoria` y nulos en los de `baseline`. Motivo: `usuario.fdr_q` puede cambiar después y sin esta copia no se sabría con qué umbral se decidió `significativa`; la ventana se guarda aunque ya esté en `ventana_reactiva.ventana_manos` porque un lote sin triggers no tiene ninguna fila donde verla. Un cambio de configuración sigue afectando solo al siguiente lote. No cambia la UI ni el prototipo | RI-12, `lote_importacion`, invariante 45 |
| M12 | Versión del motor (punto 11, decidido con el usuario el 17-nov-2026): no se guarda en `alerta`, `ventana_reactiva`, `tramo_desviacion` ni `prueba_estadistica`, ni en `lote_importacion`. Motivo: la v6 (diapositiva 34, drawer de Perfil) no muestra ni la versión del motor ni la fecha de la última recalibración, y el prototipo manda en UI; además cada alerta ya conserva su snapshot, la configuración del lote (M11), los umbrales del trigger y `ev_version`, y el MVP tiene una sola versión del motor. Se retira el criterio d) de RF-DSH-CFG-01, `EngineConfig.engine_version` y `last_recalibration_at`, y el criterio «La versión del motor es visible» del requisito de auditabilidad, sustituido por «Cada alerta conserva el baseline y la configuración con los que se calculó». Trabajo futuro: un campo `version_motor` en el lote si el motor llega a tener varias versiones | RF-DSH-CFG-01, RF-20, RNF de auditabilidad |
| M13 | `snapshot_id` en `prueba_estadistica` (punto 12, decidido con el usuario el 17-nov-2026, que pidió ampliar el modelo si está justificado): cada prueba guarda el baseline con el que se calculó su `esperado`. Motivo: una ventana o un tramo pueden tener pruebas sin alerta (p. ej. una desviación que no supera el umbral) y `referencia_id` es polimórfica, así que el camino prueba → ventana o tramo → alerta → snapshot no siempre existe. Con alerta, el `snapshot_id` coincide con `alerta.baseline_snapshot_id`. No cambia la UI | RI-16, `prueba_estadistica`, invariante 46 |
| M14 | Nivel 2: clasificador y manos similares (punto 13 completo, decidido con el usuario el 17-nov-2026): (1) no se guardan `coincidencia` ni `manos_similares` en `etiqueta_mano`: se muestra siempre la sugerencia del clasificador actual y `origen` ya distingue aceptadas de manuales (trabajo futuro: guardar la confianza vigente al aceptar); (2) aprendizaje supervisado de clasificación multiclase con Random Forest (`master-doc.txt`), pesos por nivel de juego y bucle humano; (3) «similares» son las manos con etiqueta validada que coinciden en posición, tramo de stack (M05), calle, tipo de acción, rango de pot odds, rango de outs y si las outs superan las pot odds, sin las cartas concretas; (4) «manos similares» es el recuento de ese grupo, el «% de coincidencia» es la probabilidad del bosque para la etiqueta sugerida, y por debajo de 50 manos similares no se sugiere nada (provisional); (5) pot odds = pago ÷ (bote + pago) desde `accion.bote_bb` e `importe_bb`; outs por enumeración con un evaluador de manos (candidatos `eval7`, `treys`, `phevaluator`, a decidir en 7.2 con la librería de equidad) y regla del 2 y el 4. (6) hueco 3: `etiqueta` no lleva campo `ejemplo`; el nombre y la definición de cada etiqueta viven en el archivo de traducción (M01) y el significado de cada opción se explica en una sección nueva del Glosario, estático en el frontend, con imágenes anotadas; el selector sigue mostrando solo los nombres. Esa sección se anota en §3.2 para el producto real y no se pide al prototipo. (7) hueco 4: `etiqueta` no lleva `polaridad`; las etiquetas no califican la mano como buena o mala y el selector no usa colores para ello, coherente con que la herramienta no juzga el resultado ni la jugada, solo muestra evidencia. Todo se calcula al importar o al consultar, sin cambiar el modelo. Alternativas descartadas: Gower con k-NN (posible si los grupos quedan vacíos con datos reales) y abstracción con Earth Mover's Distance (pensada para resolver juegos, no para etiquetar conducta) | Nivel 2, parámetros del modelo |
| M15 | Sin `validador_id` en `etiqueta_mano` (decidido con el usuario el 17-nov-2026): solo se etiquetan las manos propias, así que quien valida es siempre el autor (`usuario_id`) y la validación ya la expresa `validada`. Se elimina el campo y la restricción que lo exigía. La influencia entre jugadores es solo a través de las sugerencias del clasificador común | RI-14, `etiqueta_mano` |
| M16 | Alias de Winamax (punto 14, decidido con el usuario el 17-nov-2026): `usuario` no guarda el alias de Winamax. El héroe se identifica en cada mano por la línea `Dealt to` y `participacion.jugador`/`es_heroe` ya lo registran. El botón de cuenta y el drawer muestran `usuario.nombre` y el sitio activo (el «Hero» del prototipo es un nombre de ejemplo); «Hero» y «Rival» quedan como rótulos del visor y se explican en el Glosario (§3.2). Limitación para la memoria: el sistema no verifica que los archivos pertenezcan al jugador, de modo que subir archivos ajenos contaminaría el baseline. Trabajo futuro: fijar el alias en la primera importación y avisar de archivos con otro `Dealt to`, y contemplar jugadores con varias cuentas | RF-DSH-SHL-02, `usuario`, `participacion` |
| M17 | Tipo de torneo y formato de mesa (puntos 15 y 29, decidido con el usuario el 17-nov-2026; P-27 resuelta): el Historial filtra por dos ejes, **tamaño de mesa** (`torneo.max_jugadores`, de la línea `Table` del `.txt`: 3-max, 6-max) y **recompensa** (`torneo.recompensa`: `ninguna`, `ko` o `mystery`, campo nuevo). La recompensa se detecta por «bounty» en los asientos (KO) y por el nombre del torneo (Mystery, heurística). Solo se detecta: sin importes ni baseline por combinación. Se ignoran los valores del prototipo (MTT 6-Max, MTT Deep, KO Battle y Winamax Series), que eran de ejemplo; no hay filtro por serie. Limitación: la detección de Mystery depende del nombre. Verificado con los 4 `.txt` de ejemplo | RI-02, `torneo`, RF-HIS-03, RF-ING-03, RF-15 |
| M18 | Desviación sin trigger (P-22, decidido con el usuario el 17-nov-2026): se representa como **tramo** con inicio, fin y fuga neta, no como torneo marcado. Motivos: el Dashboard (diapositiva 34) ya la muestra con rango de manos y fuga; la recalibración (M03) necesita saber qué manos excluir; y marcar solo el torneo no ahorra cálculo estadístico, porque el motor tiene que contrastar igualmente por ventanas. Detección: ventana deslizante de **60 manos** (provisional; con 30 solo se detectarían desviaciones enormes: a un VPIP de 24,2 % haría falta pasar del 40 % con p < 0,05 y del 53 % con p < 0,001), de una mano en una, **por torneo** (la versión por sesión para multi-table queda como trabajo futuro); contraste exacto Poisson-binomial (M05), métricas evaluables (M06) y FDR; fusión de ventanas significativas contiguas o separadas por menos de 10 manos; límites aproximados y algo más anchos que la desviación real. Garantías de calidad: una ventana sin métrica evaluable no cuenta, y la fuga neta es «no estimable» sin EV o con pocas manos. Sustituye a K24. Análisis de sensibilidad del tamaño de ventana en la memoria. Limitaciones: tramos más anchos de lo real y desviaciones repartidas entre varias mesas no detectadas | RF-10, RF-12, RF-14, RF-16, RF-VTR-05, `tramo_desviacion` |
| M19 | Valores permitidos de la configuración (punto 24A, decidido con el usuario el 17-nov-2026): `usuario.ventana_reactiva` solo admite 20, 30, 50 o 100 y `usuario.fdr_q` solo 0,10, 0,05 o 0,01, las opciones de las diapositivas 35 y 36. Las copias históricas (`lote_importacion`, `baseline_snapshot`, `ventana_reactiva.ventana_manos`) mantienen la restricción abierta (`> 0` y `0 < q < 1`) para que quitar una opción en el futuro no invalide los datos auditados | `usuario`, RF-DSH-CFG |
| M20 | Contraseña (punto 24B, decidido con el usuario el 17-nov-2026): entre 8 y 64 caracteres y sin reglas de composición (sin exigir mayúsculas, números ni símbolos), siguiendo la guía NIST SP 800-63B, que las desaconseja porque llevan a contraseñas previsibles. Provisional: es una propuesta basada en una guía externa. Mejora futura: rechazar contraseñas muy comunes. Se guarda con hash y sal | RF-02, RNF de seguridad |
| M21 | Nombre de la tarjeta de rendimiento (punto 24C, decidido con el usuario el 17-nov-2026): se rotula «Winrate baseline (EV)» y no «Winrate» a secas ni «EVbb/100», con un ⓘ que explica que está ajustado por equidad en all-in. Motivo: «Winrate» solo sugiere el resultado real y la métrica es el EVbb/100; la palabra EV evita el malentendido y es más familiar que la sigla. Se aplica en el Dashboard, Mi Baseline y el modal de ayuda | RF-DSH-KPI-01, RF-DSH-KPI-02, RF-04, RF-06 |
| M22 | Versión y origen del baseline no visibles (punto 24D, decidido con el usuario el 17-nov-2026): Mi Baseline y el Dashboard muestran la fecha de congelación, la muestra y las métricas, pero no el número de versión ni «Inicial/Recalibrado», como en la diapositiva 23 de la v6. Motivo: el jugador solo ve el baseline activo y las versiones archivadas son internas. El modelo sigue guardando `version` y `origen` para auditar alertas y para «Deshacer» y «Restaurar» | RF-06, RF-DSH-KPI-01, RF-DSH-BAS |
| M23 | Fecha de auditoría de la alerta (punto 24E, decidido con el usuario el 17-nov-2026): `alerta` no guarda cuándo se audita. Ninguna pantalla ni requisito la usa (el «Última auditoría» del Dashboard es la fecha del lote). Trabajo futuro: un campo `auditada_en` nulo hasta que se audita, si se quiere mostrar «auditada el…» en el Historial o medir el tiempo de revisión | `alerta`, RF-DSH-FED-04 |
| M24 | Alertas inmutables (decidido con el usuario el 17-nov-2026, por utilidad real y no solo por la invariante 11): recalibrar nunca recalcula alertas ya emitidas. Motivos: recalcular con un baseline que incluye las manos del torneo evaluado lo haría parte de su propia referencia (fuga de datos) y normalizaría el tilt con el tiempo; un feed que cambia deja de ser evidencia reproducible; y cada medición debe conservar con qué referencia se hizo. Trabajo futuro: una acción explícita «Reevaluar este lote con el baseline actual» que cree una comparación nueva sin tocar la alerta original | Invariante 11, RF-DSH-GLB-03 b) |
| M25 | Varias alertas en un torneo, parte (c) del punto 31 (decidido con el usuario el 17-nov-2026): el escaneo de desviación excluye las manos de las ventanas T+30, igual que el baseline las excluye (M03). Motivos: el trigger ya explica esa conducta, la desviación se define «sin trigger aparente», y así la misma conducta no sale como tilt y como desviación ni se cuenta dos veces la fuga neta. Ninguna mano es a la vez de una ventana y de un tramo (invariante 47); una desviación que atraviesa una ventana sigue siendo **un único tramo y una sola alerta** (decisión del usuario): el escaneo salta las manos de la ventana, el tramo abarca de su primera a su última mano con la ventana dentro, y sus estadísticas y su fuga solo usan sus propias manos; el visor muestra el tramo cortado por la ventana con su propia franja. Un torneo con tilt y desviación aparece en el feed como dos tarjetas separadas, cada una con su auditoría y su fuga (partes (a) y (b) pendientes) | RF-10, RF-12, `tramo_desviacion` |
| M26 | Varias alertas en un torneo, parte (a) del punto 31 (decidido con el usuario el 17-nov-2026): el bloque «Lectura» muestra en Conducta la alerta a la que pertenece la mano abierta (ventana T+30 o tramo de desviación); **simplificado el 17-nov-2026 (M28)**: si la mano no está en ninguna alerta no hay parte Conducta, solo Suerte del torneo, y el estado del torneo («con alertas» o «sin anomalías») va en la cabecera del visor; Suerte del torneo no cambia. Motivo: el visor se navega mano a mano y la lectura debe corresponder a donde se está, sin mezclar métricas de dos alertas | RF-16, RF-VTR-05 |
| M27 | `CON ALERTA` y contador de auditadas, parte (b) del punto 31 (P-10, P-17 y P-30 resueltas; decidido con el usuario el 17-nov-2026): `CON ALERTA` cuenta **torneos** con al menos una alerta concluyente (un torneo con tilt y desviación cuenta como uno) e **incluye las auditadas**, porque describe el contenido del lote y no la cola de pendientes; el contador del enlace al historial también cuenta las auditadas. Además, la cabecera del feed muestra un contador «n de m auditadas» (m = alertas del último lote), visible también cuando todas están auditadas. (m incluye las no concluyentes desde M28). Con la parte (c) y (a), el punto 31 queda cerrado | RF-DSH-SUM-01, RF-DSH-FED-04 |
| M28 | Visor para todos los torneos (decidido con el usuario el 17-nov-2026): todos los torneos auditados se abren en el visor, tengan o no alertas, incluidos los no concluyentes y los torneos limpios; se recorren todas las manos una a una y se puede seleccionar cualquiera desde la gráfica; cualquier mano se puede etiquetar (no hay entidad nueva: `etiqueta_mano` ya no depende de las alertas). Una alerta de tilt abre en la mano trigger y una de desviación en el inicio del tramo, y un torneo sin alertas en su primera mano. Una alerta no concluyente se audita al abrir su visor, así que entra en el contador «n de m» y el estado vacío del feed vuelve a ser alcanzable. El concepto de «mano clave» y las «manos bisagra» de la rejilla (diapositivas 41–47) son un recurso de la demo para no dibujar las 30 manos: en el producto cada mano abre su propio visor y no hay saltos a manos clave. Motivo: un visor único es más simple, mejora la muestra del Nivel 2 (hoy sesgada a manos de alerta) y cierra el hueco de las no concluyentes. Riesgo: casi todas las manos mostrarán el arranque en frío con un solo usuario | RF-15, RF-16, RF-17, RF-18, RF-HIS-04, RF-VMA, RF-ETQ-02 |
| M29 | Torneo limpio, no «sesión limpia» (punto 21, decidido con el usuario el 17-nov-2026): el término «sesión limpia» no existe; lo que se quería representar es el **torneo limpio**, el torneo sin alertas de tilt ni desviaciones significativas, con independencia de su resultado. Se sustituye en todo el proyecto (glosario, requisitos, modelo y notas). Motivo: la sesión es un bloque de juego con varios torneos y rotular un torneo como «sesión limpia» era falso si otro torneo de su sesión tenía una alerta. El Historial rotula «TORNEO LIMPIO» y el resumen «TORNEOS CON ALERTA». HU-15 pasa a «evolución por torneo»; una vista por sesión queda como trabajo futuro (`sesion` ya existe como dato derivado) | HU-15, RF-15, RF-DSH-SUM-01, glosario |

Aplicada al modelo y a los requisitos (modelo v0.9): `etiqueta.nombre` pasa a `codigo` y se elimina `etiqueta.definicion`; `usuario.nivel_juego` y `etiqueta_mano.nivel_aplicado` guardan un código (`micro`, `bajo`, `medio`, `alto`, `muy_alto`); `baseline_snapshot.tipo` se aclara como código. En los contratos de la API, `Notification` pasa a `code`, `params` y `action_code`, se elimina `FatigueBucket.label` (el frontend formatea `hours_from` y `hours_to`), `vpip_population_range` pasa a `min` y `max` numéricos y `play_level` es un código. RNF-09 queda solo con idioma y formato; la externalización de los textos es RNF-12. Para añadir un idioma solo hay que crear su archivo de traducción con las mismas claves.

---

## 2. Dudas abiertas

| ID | Duda | Impacto |
|---|---|---|
| P-03 | Umbral exacto de obsolescencia (manos nuevas y días). **Fuera del MVP**; el aviso de RF-07 queda sin implementar | Aviso de recalibración |
| P-05 | Mínimo de manos por tramo de fatiga | Fusión de tramos |
| P-07 | Comportamiento de recuperación en errores de bloque | Patrón de estados |
| P-08 | Comportamiento exacto de cierre de overlays (backdrop, Esc) | UI |
| P-09 | Confirmación de que el contador del enlace al historial es de pendientes | Feed |
| P-11 | Tokenización de colores y valores concretos de contraste AA | UI |
| P-12 | Copy exacto de los toasts y modales | UI |
| P-14 | Cómo se identifica el punto crítico si hay un tramo exactamente en 0 | Gráfica |
| P-15 | Qué filtros aplica el enlace del feed al abrir el historial | Navegación |
| P-20 | Pérdida mínima para que un bad beat (all-in perdido con equidad ≥ 70 %) cuente como trigger | RF-08, Modelo |
| P-21 | Alcance de la comparativa Baseline vs Tilt: de momento el último lote; está por estudiar si debe ser un periodo o el histórico | RF-21 |
| P-28 | Umbral de trigger relativo al stack en el MVP (propuesta: 50 % del stack con un mínimo de 10 BB). Se decide junto con P-20 | RF-08, `trigger` |
| P-29 | Librería de traducción del frontend (i18n): depende del framework, que se elige en 7.2. Hasta entonces solo se fija el contrato: claves, archivo por idioma y mensajes como código más parámetros (M01) | RNF-12, 7.2 |
| P-31 | Cómo pedir el etiquetado sin saturar al jugador, ahora que se puede etiquetar cualquier mano (M28): carácter opcional y posible sistema de recompensas por etiquetar manos al día; riesgo a valorar: un incentivo por cantidad puede bajar la calidad de las etiquetas (etiquetar al azar) | RF-18, visor de mano, Nivel 2 |

**Total:** 14 dudas abiertas. Las P-26, P-27 y P-28 proceden del informe de revisión del 14 de noviembre de 2026 (generado por otra IA); los valores son propuestas suyas, no decisiones. Resueltas en el cierre de 7.1:

Las dudas ya resueltas (P-01 a P-26) están archivadas en `docs/archivo/dudas-resueltas.md`; sus decisiones, con su porqué, siguen en §1.

---

## 3. Trazabilidad con el prototipo

> Numeración del prototipo (`sources/Mindset-EV-Leak-Finder-TFG.pptx`, 60 diapositivas).

| Diapositiva | Contenido | Requisitos |
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

---|---|---|
| 4–5 | Dashboard con gráfica de línea | SHL, KPI, FAT, FED, SUM, ORG |
| 28–30 | Dashboard tras recalibrar y tras auditoría | KPI, TST, FED |
| 31 | Drawer de cuenta | CFG |
| 32 | Modal de ventana de tilt | CFG |
| 33 | Modal de sensibilidad | CFG |
| 45 | Dashboard con gráfica de barras | FAT |
| 46–49 | Modales de VPIP, PFR, 3-Bet y EVbb/100 | KPI, CFG |

---

### 3.1 Cambios que faltan en el prototipo (revisado contra la v6, 17-nov-2026)

Lista revisada diapositiva a diapositiva con la v6 (71 diapositivas, 16-nov-2026): solo quedan los cambios que **aún no están** en el PPTX. Los glosarios no se piden al prototipo (§3.2).

| Diapositivas | Cambio | Origen |
|---|---|---|
| 9–10, 23, 28–30, 52–55 | Renombrar la tarjeta «Winrate» (también «Winrate de Control» en la tabla de impacto) a «Winrate baseline (EV)», con un ⓘ que explique que está ajustado por equidad en all-in | M21 |
| 11–18 | Sustituir el filtro «Tipo de torneo» (MTT 6-Max, MTT Deep, KO Battle y Winamax Series) por dos filtros, tamaño de mesa (3-max, 6-max) y recompensa (ninguna, KO, Mystery); en las filas del Historial (11, 16–18) cambiar el subtítulo del torneo («Winamax MTT Deep», «KO Battle») por tamaño de mesa y recompensa, y en los historiales filtrados mostrar el filtro activo con esos valores | M17 |
| 20–22 | Añadir el aviso informativo de torneo omitido, igual que el de duplicados y sin pedir decisión: «Anterior al final de tu baseline: no se va a auditar» (con la fecha del torneo y la última mano del baseline) | M04 |
| 28–30, 23 | Cambiar el subtítulo de la casilla de fatiga («Aísla únicamente el juego en estado de lucidez óptima (A-Game de horas 1 a 3)») por uno que hable del punto crítico del jugador, y añadir el estado sin punto crítico («Sin punto crítico: no se excluye fatiga» y «Manos excluidas por fatiga: 0») | M03 |
| 23, 28–30 | Cambiar «recalculará las alertas del lote» y «el feed de alertas se recalcula antes de volver al dashboard» por un texto que diga que las alertas ya emitidas conservan su baseline y que el nuevo solo se aplica a los próximos lotes | Invariante 11, RF-DSH-GLB-03 b) |
| 42–43 | Mano #113: Hero tiene 8♥6♥ y el board 10♣ 9♦ 2♠ 7♣ 3♥, es decir, escalera desde el turn, pero el texto dice «El proyecto de escalera de Hero no se completa»; corregir las cartas o el texto | Errata |
| 43 | Quitar los puntos de color del selector de etiquetas (verde, rojo, naranja y azul) y mostrar las ocho etiquetas con el mismo estilo neutro, para no calificar la jugada | M14 |
| 48 | En Conducta, añadir el tramo detectado (por ejemplo «manos #30 a #90 · 60 manos», aproximado) y la fuga neta estimada con ⓘ, y marcar el tramo con una franja en la gráfica; si una ventana T+30 lo atraviesa, dibujarla dentro del tramo con su propia franja y avisar en Conducta de que el tramo está interrumpido por esa ventana | M18, M25 |
| 11, 16–18, 28, 48–50 | M29: sustituir «SESIÓN LIMPIA» por «TORNEO LIMPIO» (filas del Historial, «Sesión limpia de control» del pie de las diapositivas 48–49), «SESIONES CON ALERTA» por «TORNEOS CON ALERTA» (resumen del Historial) y «Sesiones limpias» por «Torneos limpios» (tabla «Qué entra en el cálculo» de la diapositiva 28) | M29 |
| 9, 11 | Habilitar «Auditar» en la tarjeta no concluyente del feed y «Ver Torneo» en su fila del Historial (hoy deshabilitados), con un visor para el #8479 cuya Conducta diga que la alerta es no concluyente | M28 |
| 9–10, 34, 51 | Contador «n de m auditadas» en la cabecera del feed (por ejemplo «2 de 3 auditadas»), que sigue visible cuando todas están auditadas | M27 |
| 41–50 | «Lectura» de una mano que no pertenece a ninguna alerta: sin parte Conducta, solo Suerte del torneo; la cabecera del visor indica si el torneo tiene alertas o no tiene anomalías (en 49–50 quitar la frase «No se han detectado anomalías» del bloque y pasarla a la cabecera) | M26, M28 |
| 41–46, 66–71 | Un trigger sin manos posteriores se muestra con la nota «sin manos posteriores» (no encontrada en la v6) | M07 |
| 3 | Opcional: bajo el campo de contraseña del registro, la pista «Entre 8 y 64 caracteres» | M20 |

**Ya aplicado y comprobado en la v6** (se quitó de la lista): Historial sin VPIP/PFR y con BB ganadas, All-in EV y Suerte all-in con ⓘ; bloque «Lectura» en los visores (41–50); métricas «k de n · no evaluable», feed ordenado sin mostrar la solidez, alerta no concluyente, filtros «Ocultar alertas/torneos con métricas no evaluadas» y estado «no concluyente»; caso multi-table con pestañas, aviso informativo y rejilla por sesión (66–71); rejilla de la ventana T+30 con fuga neta (47); gráfica de fatiga con cinco puntos fijos (9–10); marca informativa del #8507 en el Historial; fuga neta en positivo, 14 torneos y sesiones coherentes (K25, K30, K33); y las ocho diapositivas de glosario con los cuatro términos nuevos y la ventana T+30 por sesión.

**Limitaciones conocidas del prototipo, aceptadas como datos simulados** (decisión del usuario, 14 de noviembre):

- Con un archivo por torneo, las manos por archivo del baseline no son creíbles: «12 archivos · 24.500 manos» (unas 2.000 por archivo, frente a unas 270 en el lote de auditoría), «1 archivo · 2.480 manos» (diapositivas 7 y 8) y «1 archivo · 18.400 manos» (27). Un MTT real tiene unas pocas centenas de manos. No se corrige.
- La comparativa Baseline vs Tilt (19) agrega «18 episodios · 540 manos», mientras que el Dashboard dice «0,8 % manos en T+30» (unas 30 manos, una ventana). Depende del alcance de la comparativa (K11 y P-21).

### 3.2 Glosario del producto real (no se pide al prototipo)

El usuario quiere un Glosario completo en el producto, aunque algunos términos parezcan obvios. Los cambios del Glosario **no se piden al prototipo** (es solo una demostración) y se anotan aquí para añadirlos al producto real (decidido el 17-nov-2026). El Glosario es estático en el frontend y su contenido va en el archivo de traducción (M01).

| Término o sección | Contenido | Origen |
|---|---|---|
| Hero | Término del visor de mano: el jugador cuyas manos se analizan. No es el apodo de Winamax ni el nombre de la cuenta | Punto 14 |
| Rival | Jugador contra el que Hero disputa la mano | Punto 14 |
| Etiquetado (sección nueva) | Qué es el etiquetado comunitario, el diagnóstico y la sugerencia, el arranque en frío (menos de 50 manos similares) y qué significa cada una de las ocho etiquetas, con imágenes anotadas (recursos estáticos del frontend); sin colores que califiquen la jugada | M14 |
| C-Bet | Quitar la frase «Se mide sobre los flops vistos después de haber subido»: el término se queda como vocabulario de póker, porque la herramienta ya no mide C-Bet | M02 |
| WTSD y Fold vs 3-Bet | Términos que la comparativa Baseline vs Tilt muestra y el Glosario no tiene; RF-19 pide enlazar cada métrica con su término | Desajuste de requisitos |
| Mano similar, pot odds y outs | Cómo se agrupan las manos para sugerir una etiqueta y qué son las pot odds y las outs, con un ejemplo | M14 |

Falta escribir los requisitos del Glosario con estos términos y revisar que el resto de términos del producto estén cubiertos.

## 4. Módulos implicados (preliminar)

> Los nombres son los del pipeline de `AGENTS.md`. La arquitectura y los contratos de API se detallarán en una fase posterior; esta tabla solo identifica qué alimenta al Dashboard.

| Módulo | Papel respecto al Dashboard |
|---|---|
| Parser ETL Winamax | Convierte los `.txt` en `HandRecord` canónicos |
| Normalización a BB | Deja las manos en ciegas grandes |
| Session Builder | Agrupa manos en sesiones y torneos |
| Baseline | Produce el `BaselineSnapshot` congelado y versionado |
| Detectores Nivel 1 | Generan triggers, ventanas T+30, tramos y fatiga |
| Corrección FDR | Ajusta la significación de las desviaciones |
| Gestión de lotes | Mantiene el último `ImportBatch` y su resumen |
| API REST | Expone los datos que consume el Dashboard |
| Frontend | Renderiza shell, bloques, overlays y estados |
| Autenticación | Aísla los datos por usuario, sitio y formato |

---

## 5. Criterios de redacción de la entrega

Estas reglas se aplican al documento de requisitos y no se incluyen en él:

1. Cada RF describe **qué debe hacer el sistema**, no por qué se decidió.
2. No se documentan alternativas descartadas.
3. No se incluyen IDs de decisión ni referencias al historial de requisitos.
4. Las cifras solo aparecen si son parámetros reales del producto. Los valores pendientes se marcan “Por definir”.
5. Se prefieren afirmaciones positivas.
6. Un RF agrupa una capacidad visible; los detalles van como criterios.
7. Prueba del lector externo: si para entender un requisito hay que haber leído este documento, el requisito debe reescribirse.

---

## 6. Adaptación a la plantilla oficial de la memoria

### 6.1 Decisión

La entrega oficial no usa las 80 fichas. La plantilla de la ETSII pide, en 7.1, un Product Backlog, una definición de actores, un RF por caso de uso, los RNF y los requisitos de almacenamiento. Para que el volumen sea defendible se acuerda:

| Elemento | Cantidad | Ubicación |
|---|---:|---|
| Historias de usuario | 18 | 7.1.1 Product Backlog |
| Actores | 2 | 7.1.2 Definición de actores |
| Requisitos funcionales | 21 | 7.1.3 Requisitos funcionales |
| Requisitos no funcionales | 11 | 7.1.4 Requisitos no funcionales |
| Entidades de almacenamiento | 16 | 7.1.5 Requisitos de almacenamiento |

Las 80 fichas y sus 415 criterios se conservan en `docs/03-matriz-trazabilidad.md` como matriz interna. No se incluyen en la memoria oficial.

### 6.2 Correspondencia

| RF de la plantilla | Fichas internas |
|---|---|
| RF-01 Importar archivos de Winamax | RF-ING-01 a RF-ING-04 |
| RF-02 Resumir y procesar el lote | RF-ING-05 a RF-ING-07 |
| RF-03 Interpretar y registrar el historial | RF-PAR-01 a RF-PAR-05 y RF-PAR-09 |
| RF-04 Normalizar, calcular EV y métricas | RF-PAR-06 a RF-PAR-08 |
| RF-05 Agrupar manos en sesiones | RF-SES-01 a RF-SES-05 |
| RF-06 Calcular el baseline individual | RF-BAS-01, RF-BAS-03 y RF-BAS-06 |
| RF-07 Congelar y recalibrar el baseline | RF-BAS-02, RF-BAS-04 y RF-BAS-05 |
| RF-08 Detectar el trigger de bad beat | RF-DET-01 |
| RF-09 Analizar la ventana T+30 | RF-DET-02 y RF-DET-03 |
| RF-10 Detectar desviaciones sin trigger | RF-DET-04 y RF-DET-05 |
| RF-11 Analizar la fatiga | RF-DET-06 |
| RF-12 Corregir FDR y generar alertas | RF-DET-07 y RF-DET-08 |
| RF-13 Dashboard: KPIs y fatiga | RF-DSH-01 a RF-DSH-03 |
| RF-14 Dashboard: feed y evidencia | RF-DSH-04 a RF-DSH-08 y RF-DSH-10 |
| RF-15 Historial de torneos | RF-HIS-01 a RF-HIS-05 |
| RF-16 Visor de torneo | RF-VTR-01 a RF-VTR-04 |
| RF-17 Visor de mano | RF-VMA-01 a RF-VMA-06 |
| RF-18 Etiquetar jugadas del Nivel 2 | RF-ETQ-01 a RF-ETQ-07 |
| RF-19 Glosario y ayuda contextual | RF-GLO-01 y RF-GLO-02 |
| RF-20 Cuenta, registro y configuración | RF-CUE-01 a RF-CUE-05 y RF-DSH-09 |
| RF-21 Comparar el baseline con las ventanas T+30 | RF-CMP-01 a RF-CMP-03 |

Dos ajustes respecto al mapa inicial:

- **RF-DSH-07** (resumen y origen del lote) pasa a RF-14 porque se presenta junto al feed del último lote.
- **RF-DSH-09** (cuenta y configuración del motor) pasa a RF-20 para no duplicar RF-CUE-02 y RF-CUE-03.

El registro de cuenta vive en RF-20 y en la ficha RF-CUE-01, que pasa a llamarse «Registro y autenticación». RF-21 (comparativa Baseline vs Tilt) se añadió después, con la pantalla del prototipo, y se coloca al final para no renumerar RF-01 a RF-20.

### 6.3 Generación del documento

| Elemento | Ruta |
|---|---|
| Plantilla oficial | `sources/Plantilla - Documentación.docx` |
| Contenido de 7.1 | `tools/plantilla_content.py` |
| Generador | `tools/fill_plantilla.py` |
| Diagramas de 7.1.6 | `tools/build_secuencias.py` y `tools/diagrams/` |
| Salida | `docs/entrega/Memoria-TFG-requisitos.docx` |
| Matriz interna | `tools/build_matriz_trazabilidad.py` y `docs/03-matriz-trazabilidad.md` |

El generador conserva portada, estilos, índice, encabezados, tablas anteriores a 7.1 y el resto del documento. Sustituye el contenido de 7.1.1 a 7.1.6 y el de 7.4.1, y deja intactos 7.2 y 7.5. Añade `w:updateFields` para que Word actualice el índice y la tabla de ilustraciones al abrir el archivo.

El documento resultante contiene 73 tablas nuevas: 52 en 7.1.1 a 7.1.5 (1 backlog, 2 actores, 21 RF, 12 RNF y 16 RI) y 21 en 7.4.1. Las tablas de 7.1 llevan los números 16 a 67 y las de 7.4.1, del 68 al 88. Además, 7.1.6 incluye tres diagramas de secuencia con los números 2 a 4.

### 6.4 Parámetros y umbrales

Los parámetros viven dentro del RF o RNF que los usa, no en una sección aparte. Los valores acordados están escritos en su requisito (30 manos en RF-09, q < 0,05 en RF-12 y RF-20, 70 % y 40 BB en RF-08, 30 minutos en RF-05, cuatro decimales y 0,001 BB en RF-04, 2.000 y 10.000 manos en RF-06, 10 manos en RF-10, fórmula con EV en RF-12, 2 s y 60 s en RNF-03, reintento y recarga en RNF-11). Lo que sigue sin cerrar se marca como «pendiente de definir» en la frase que lo menciona:

| Dónde | Parámetro pendiente |
|---|---|
| RF-07 | Umbral de obsolescencia del baseline; fuera del MVP |
| RF-18 | Taxonomía y consentimiento; los pesos por nivel son provisionales (K14) |
| RF-02 | Contraseña: entre 8 y 64 caracteres, sin reglas de composición (M20, provisional) |

Los valores estadísticos del cierre de 7.1:

| Parámetro | Valor | Por qué |
|---|---|---|
| Mínimo duro del baseline | 2.000 manos | Con p = 0,5 da ±2,2 % al 95 %; 10–20 MTT, asumible para la demo |
| Muestra recomendada | 10.000 manos | ±1 % en VPIP/PFR y error de EV más estrecho; 40–100 MTT |
| Separación de tramos | 10 manos | Aproximadamente una órbita; menos se fusiona como el mismo episodio |
| Fuga neta | `max(0, (EVbb/100 baseline − EVbb/100 observado) × manos / 100)` | Usa EV, no resultado; sin EV queda «no estimable» |
| Suerte neutra | 1σ, con σ = √Σ(bote² · e · (1 − e)) sobre los all-in del torneo | Provisional; con 1σ un bad beat aislado sale «En contra». Sin all-in, siempre neutra |
| Snapshots archivados | Se conservan todos | Cada alerta debe poder auditarse contra su baseline |

Se descarta una tabla centralizada porque duplicaba los valores ya escritos y añadía una sección que la plantilla no trae.

### 6.5 Formato de las tablas

La plantilla trae las tablas de ejemplo a 14 pt, un tamaño pensado para tablas vacías. Al rellenarlas, cada RF ocupaba casi una página. Se acuerda compactar solo la tipografía, sin tocar el contenido:

| Elemento | Tamaño |
|---|---:|
| Nombre del RF, RNF o entidad | 14 pt |
| Etiquetas de la primera columna | 11 pt |
| Cuerpo de las celdas | 10 pt |
| Títulos de sección | Sin cambios |

El ajuste se aplica en `tools/fill_plantilla.py` mediante las funciones `set_sz`, `resize_row` y `compact`, y afecta a las tablas de 7.1 y 7.4.1.

### 6.6 Diagramas de secuencia

7.1.6 se cubre con tres diagramas de los flujos principales:

| Ilustración | Flujo | Participantes |
|---:|---|---|
| 2 | Importación y procesamiento del lote | Jugador, Interfaz, API, Parser, Session Builder y Motor |
| 3 | Auditoría de una alerta | Jugador, Dashboard, API, Motor y Base de datos |
| 4 | Cálculo del baseline y detección | Motor, Baseline, Detectores, FDR y Base de datos |

Los diagramas se dibujan en SVG desde `tools/build_secuencias.py` y se rasterizan a PNG con `ffmpeg` y `librsvg`. El generador de la memoria los incrusta como partes de imagen (`rId200` a `rId202`), con 15 cm de ancho y la altura proporcional. Los PNG quedan en `tools/diagrams/`.

Para regenerarlos:

```bash
python3 tools/build_secuencias.py
python3 tools/fill_plantilla.py
```

Si `ffmpeg` no está disponible, basta con conservar los PNG ya generados en `tools/diagrams/`; `fill_plantilla.py` no invoca `ffmpeg`, solo lee los PNG.

### 6.7 Pendiente

- **7.4.2 Implementación de las pruebas**: sigue con el contenido de ejemplo. No forma parte de los requisitos; corresponde a la fase de pruebas.
- **7.2 y 7.5**: son capítulos de implementación y retrospectiva, fuera del alcance de esta entrega de requisitos.
- **Obsolescencia del baseline**: fuera del MVP. RF-07 conserva la frase «pendiente de definir» y el aviso no se implementa.
- **Taxonomía y consentimiento del Nivel 2**: pendientes de validación con usuarios. No se inventan etiquetas. Los pesos por nivel son provisionales (K14).
- **Librería de equidad, semilla y versión del EV**: es implementación y se fija en 7.2.
- **Métricas avanzadas (M02, trabajo futuro)**: C-Bet, Fold vs C-Bet y WSSD quedan fuera del MVP; se podrán calcular después desde `accion`, sin reimportar los archivos, para jugadores avanzados.
- **Idioma (M01)**: `usuario.idioma` queda fuera del MVP y se añadirá cuando exista un segundo idioma (francés e inglés, trabajo futuro). La librería de traducción es la duda P-29.
- **Nivel 2, punto 13 (hueco 1 cerrado el 17-nov-2026)**: no se guardan `coincidencia` ni `manos_similares` en `etiqueta_mano`. La sugerencia que se muestra es siempre la del clasificador actual y `origen = sugerida` ya distingue las etiquetas aceptadas de las manuales. Trabajo futuro: guardar la confianza vigente al aceptar, para medir cuánto influyó la sugerencia en el jugador cuando exista un clasificador real que la use.
- **Limitaciones para la memoria (capítulo de limitaciones, sin redactar todavía)**: la herramienta no modela el ICM ni la burbuja (las desviaciones cercanas pueden ser juego correcto); la gráfica de fatiga puede mezclar el efecto horario con la composición de stacks, porque no se corrige por el EV esperado según el stack (M10, P-26); no se estima el coste en buy-ins ni en euros (reabriría la invariante 16). Trabajo futuro: fatiga frente al EV esperado según el stack (M10); tiempo de recuperación tras un trigger y evolución de la fuga en el tiempo.
- **Tabla de ilustraciones**: al abrir el documento en Word hay que aceptar la actualización de campos o pulsar `Ctrl+A` y `F9`. Si no se actualiza, la tabla de ilustraciones conserva las entradas antiguas, incluida «Ilustración 36: Diagrama de Secuencia 1».

### 6.8 Modelo de datos

`docs/02-modelo-datos.md` (v0.8) desarrolla el modelo lógico relacional: 20 entidades, 24 relaciones, 33 invariantes, índices recomendados y trazabilidad `RI → entidad`.

Las 16 entidades de 7.1.5 se mantienen. El modelo añade cuatro detalles de implementación que no llegan a la memoria:

| Entidad | Función |
|---|---|
| `bote` | Bote principal y side pots, que en `mano` solo caben como total |
| `metrica_valor` | Numerador y denominador de las 5 métricas de conducta y del EVbb/100 en baseline, ventana, tramo, sesión y torneo |
| `baseline_exclusion` | Ventanas y tramos descartados al recalibrar; sin ellas un snapshot no es reproducible |
| `baseline_snapshot_torneo` | Torneos que componen cada versión del baseline (K28) |

El modelo obligó a tres cambios en 7.1.5:

| Cambio | Motivo |
|---|---|
| RI-15 Trigger y RI-16 Prueba estadística | RI-09 mencionaba el trigger sin entidad propia y FDR necesitaba el conjunto de comparaciones |
| RI-04 deja de listar la sesión | Se obtiene a través del torneo; el modelo no duplica la FK |
| RI-12 deja de listar el estado | El lote solo existe si el procesamiento termina |

También fijó tres decisiones que antes eran dudas: la ventana copia su tamaño aplicado (`ventana_manos`), la identidad de sesión es `(usuario_id, inicio)` y toda mano guarda la versión del EV con la que se calculó.

La v0.4 cierra M-02 a M-08:

| ID | Decisión |
|---|---|
| M-02 | Cartas y board en TEXT compacto (`AhKd7c`); el API los devuelve estructurados al visor |
| M-03 | Glosario estático versionado en el frontend |
| M-04 | Índices por consulta; sin particiones en el MVP |
| M-05 | Se conservan todos los snapshots archivados |
| M-06 | Sin `bote_ganador`; basta `participacion.cobrado_bb` |
| M-07 | `baseline_exclusion` guarda solo la exclusión; el efecto se recalcula |
| M-08 | La exclusión se aplica también en el baseline inicial, solo de ventanas T+30 (K06); sin detecciones, conjunto vacío |

Las cartas se guardan como texto compacto porque es el formato más eficiente de los tres evaluados (TEXT compacto, TEXT con espacios y JSON). Eso no limita el visor: el API parsea `AhKd7c` y entrega cartas estructuradas para que el frontend las pinte con sus propios componentes. El texto nunca se muestra en crudo.

Los seis diagramas UML (`tools/diagrams/uml/`, SVG y PNG al doble de resolución) se generan con `tools/build_uml.py`: una vista global y cinco vistas de detalle por dominio (identidad, manos, baseline, detección y Nivel 2). Por ahora **no se incrustan en la memoria ni se añade una segunda tanda** de casos de uso, estados, paquetes o actividad; quedan como entrega aparte hasta que se aborde el capítulo de diseño.

### 6.9 Product Backlog

El backlog de 7.1.1 se reescribe desde el design thinking. Las 18 historias se agrupan en cinco epics que reproducen el recorrido del jugador, desde que suelta el archivo hasta que comparte una etiqueta:

| Epic | Nombre | Historias |
|---|---|---:|
| E1 | Importar y ordenar | HU-01 a HU-03 |
| E2 | Revisar en dos minutos | HU-04 a HU-06 |
| E3 | Entender qué pasó | HU-07 a HU-12 |
| E4 | Decidir y actuar | HU-13 a HU-15 |
| E5 | Aprender y compartir | HU-16 a HU-18 |

Los roles son genéricos —«jugador recreacional» y «jugador semi-profesional»— porque las personas del design thinking tienen nombres reales que no deben aparecer en la entrega. Cada historia declara el beneficio esperado, no la pantalla que lo implementa.

Correspondencia con los requisitos funcionales:

| HU | RF | HU | RF |
|---|---|---|---|
| HU-01 | RF-01 a RF-04 | HU-10 | RF-10 |
| HU-02 | RF-01, RF-02 | HU-11 | RF-11 |
| HU-03 | RF-05 | HU-12 | RF-12 |
| HU-04 | RF-13 a RF-15 | HU-13 | RF-12, RF-13, RF-17 |
| HU-05 | RF-13, RF-14 | HU-14 | RF-20 |
| HU-06 | RF-14, RF-16, RF-17 | HU-15 | RF-15, RF-16 |
| HU-07 | RF-06 | HU-16 | RF-18 |
| HU-08 | RF-07 | HU-17 | RF-19 |
| HU-09 | RF-08, RF-09, RF-21 | HU-18 | RF-06, RF-07 |

Dos criterios se han dejado fuera del backlog porque ya viven en los requisitos y repetirlos como historia los debilitaba:

| Criterio | Dónde está |
|---|---|
| Atomicidad del lote | RF-02 y RNF-06, RNF-11 |
| Corrección FDR | RF-12 |

El registro de cuenta es un requisito habilitador de RF-20 y no se representa como HU propia para no romper el límite de 18. Su detalle vive en RF-20 y en la ficha RF-CUE-01, y el modelo ya lo soporta con `email` único, `hash_contrasena`, `sal_contrasena` y `creado_en`.

La numeración `HU-01` a `HU-18` coincide con la que pide la plantilla en el ejemplo de 7.1.1. Los sprints no se incluyen aquí: corresponden a 5.2 y 5.3.

### 6.10 Gestor del lote pendiente

La pantalla de importación muestra la lista editable de los archivos que se acaban de añadir. La X quita un archivo **solo de ese lote pendiente**, antes de procesarlo:

- No borra torneos ya importados ni toca el baseline.
- No necesita cascada ni confirmación, porque todavía no existe ningún dato persistido.
- Al quitar un archivo se actualizan la lista, los recuentos y el resumen previo.
- Si se quitan todos, se vuelve al estado vacío y no se puede continuar.
- Una vez procesado el lote, la lista deja de ser editable.

No se añade borrado de torneos ya procesados: el baseline es inmutable y las alertas deben conservar su evidencia. Esto no cambia el modelo de datos.

### 6.11 Auditar no es recalcular

Una alerta del pasado se audita contra el snapshot con el que se calculó, no contra el baseline activo. El baseline no cambia solo: cambia cuando el jugador pide una recalibración explícita.

| Momento | Qué pasa | Baseline |
|---|---|---|
| Enero | Se importa el lote A y se genera la alerta A1 | v1, 2.000 manos |
| Marzo | El jugador recalibra con manos nuevas | v2 activo; v1 archivado |
| Abril | Se importa el lote B y se genera B1 | v2 |
| Hoy | Se audita A1 | Se muestra contra v1 |

Si A1 se rejuzgara con v2, una alerta antigua podría desaparecer o cambiar de magnitud, y se perdería la trazabilidad. Por eso:

- Cada alerta guarda `baseline_snapshot_id` y ese vínculo no se modifica.
- Los snapshots archivados se conservan todos.
- Rejuzgar una alerta con el baseline actual sería una **re-evaluación**, no una auditoría, y generaría una alerta nueva. Queda como mejora futura, fuera del MVP.
