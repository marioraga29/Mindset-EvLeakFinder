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
| C06 | El baseline inicial excluye las ventanas T+30 de los triggers y las recalibraciones también los tramos de desviación (ver K06); si no hay detecciones, el conjunto queda vacío; la fatiga no se excluye | RF-DSH-GLB-03 |
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
| G09 | Versión del motor y última recalibración visibles | RF-DSH-CFG-01 |
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
| K24 | Conducta con desviación sin trigger: solo las métricas de la alerta frente al baseline, sin fuga neta ni inicio y fin de tramo (a la espera de P-22) | RF-16, RF-VTR-05 |
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

---

## 2. Dudas abiertas

| ID | Duda | Impacto |
|---|---|---|
| P-03 | Umbral exacto de obsolescencia (manos nuevas y días). **Fuera del MVP**; el aviso de RF-07 queda sin implementar | Aviso de recalibración |
| P-05 | Mínimo de manos por tramo de fatiga | Fusión de tramos |
| P-07 | Comportamiento de recuperación en errores de bloque | Patrón de estados |
| P-08 | Comportamiento exacto de cierre de overlays (backdrop, Esc) | UI |
| P-09 | Confirmación de que el contador del enlace al historial es de pendientes | Feed |
| P-10 | Definición exacta de `CON ALERTA` si un torneo tiene tilt y desviación | Resumen |
| P-11 | Tokenización de colores y valores concretos de contraste AA | UI |
| P-12 | Copy exacto de los toasts y modales | UI |
| P-14 | Cómo se identifica el punto crítico si hay un tramo exactamente en 0 | Gráfica |
| P-15 | Qué filtros aplica el enlace del feed al abrir el historial | Navegación |
| P-20 | Pérdida mínima para que un bad beat (all-in perdido con equidad ≥ 70 %) cuente como trigger | RF-08, Modelo |
| P-21 | Alcance de la comparativa Baseline vs Tilt: de momento el último lote; está por estudiar si debe ser un periodo o el histórico | RF-21 |
| P-17 | Si `CON ALERTA` cuenta las alertas ya auditadas o solo las pendientes | Resumen |
| P-22 | Si la desviación sin trigger se representa como tramo (inicio, fin y fuga) o solo como torneo marcado | RF-10, RF-12, RF-14, `tramo_desviacion`, diapositiva 48 |

**Total:** 14 dudas abiertas. Resueltas en el cierre de 7.1:

| ID | Resolución |
|---|---|
| P-01 | Mínimo duro del baseline: 2.000 manos |
| P-02 | Muestra recomendada: 10.000 manos; por debajo se avisa «muestra pequeña» |
| P-04 | Fuga neta: `max(0, (EVbb/100 baseline − EVbb/100 observado) × manos / 100)`; sin EV, «no estimable» |
| P-06 | La pausa que separa dos sesiones es de 30 minutos |
| P-16 | Resuelta con las diapositivas 5 y 8 (K07): sin baseline no hay feed ni resumen; con baseline y sin lotes auditados, el feed explica que no hay casos y un panel «Baseline actual» sustituye al resumen |
| P-13 | El baseline inicial excluye las ventanas T+30 por trigger (K06); si no hay detecciones, no hay nada que avisar |

P-03 se queda fuera del MVP y no bloquea la entrega. Las dudas P-07 a P-17 son de interfaz y pertenecen a la especificación del Dashboard, no a 7.1.

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

### 3.1 Cambios en el prototipo por K17–K33

| Diapositivas | Cambio |
|---|---|
| 11, 16–18 | Quitar VPIP/PFR; BB ganadas, All-in EV (verde y rojo) y Suerte all-in (sin color), con ⓘ |
| 41–46 | Bloque Lectura con ventana T+30 (métricas de la alerta y fuga neta) y Suerte del torneo; quitar impacto, cierre, contexto y lectura agregada; contexto en la cabecera; subtítulo fijo |
| 48 | Bloque Lectura sin fuga ni tramo; quitar fuga estimada y resto del patrón |
| 49–50 | Bloque Lectura sin métricas del torneo; quitar tarjetas, resultado, caja de EV y contexto |
| 56–60 | Cuatro términos nuevos del Glosario |

Aplicados en el PPTX v2 (14 de noviembre de 2026, 65 diapositivas: las cinco nuevas son los modales ⓘ de BB ganadas, All-in EV, Suerte all-in y Fuga neta). Las cuatro correcciones siguientes se aplicaron en el PPTX v3 (`sources/Mindset-EV-Leak-Finder-TFG-v3.pptx`, 14 de noviembre de 2026, 14:32) y se revisaron en unas 25 de las 54 diapositivas que cambian (9, 11, 12, 16, 18, 19, 20, 23, 25, 27, 31, 41, 46, 47, 49, 50, 51, 60 y 65, entre otras):

| Cambio | Origen |
|---|---|
| Fuga neta en positivo en el feed, los visores, el resumen del Historial y Baseline vs Tilt; ajustar la nota del orador de la diapositiva 65 | K33 |
| Texto de «Conducta» sin alertas (49 y 50): «No se han detectado anomalías conductuales frente a tu baseline» | K25 |
| De 18 a 14 torneos en Historial, filtros, Dashboard, diapositiva 51, Importar y Glosario | K30 |
| Sesiones coherentes con los archivos (12 archivos con 9 sesiones; 13 con 10; 1 con 1) y la misma cifra en el subtítulo de la gráfica de fatiga | K30 |

**Limitaciones conocidas del prototipo, aceptadas como datos simulados** (decisión del usuario, 14 de noviembre):

- Con un archivo por torneo, las manos por archivo del baseline no son creíbles: «12 archivos · 24.500 manos» (unas 2.000 por archivo, frente a unas 270 en el lote de auditoría), «1 archivo · 2.480 manos» (diapositivas 7 y 8) y «1 archivo · 18.400 manos» (27). Un MTT real tiene unas pocas centenas de manos. No se corrige.
- La comparativa Baseline vs Tilt (19) agrega «18 episodios · 540 manos», mientras que el Dashboard dice «0,8 % manos en T+30» (unas 30 manos, una ventana). Depende del alcance de la comparativa (K11 y P-21).

**Pendiente tras revisar el PPTX v2 y el v3** (sin resolver): la rejilla de la ventana T+30 (diapositiva 47) sigue con «Resultado adicional −42.5 BB», que es la suma real y no la fuga neta (punto 5); el feed y el resumen del Historial siguen contando fuga en #8488 aunque el visor ya no la muestra (P-22).

**Desajustes entre requisitos y prototipo detectados el 14 de noviembre** (punto 24, sin resolver):

- La tarjeta del Dashboard se llama «Winrate baseline» y su modal habla de «ganancia media por 100 manos», mientras que los requisitos hablan de «EVbb/100 (ajuste all-in)»; el prototipo no muestra la etiqueta ni la palabra EV.
- RF-06 y RF-DSH-KPI-01 dicen que se muestran la versión y «Inicial/Recalibrado»; las diapositivas 23 a 27 no lo muestran.

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

La entrega oficial no usa las 78 fichas. La plantilla de la ETSII pide, en 7.1, un Product Backlog, una definición de actores, un RF por caso de uso, los RNF y los requisitos de almacenamiento. Para que el volumen sea defendible se acuerda:

| Elemento | Cantidad | Ubicación |
|---|---:|---|
| Historias de usuario | 18 | 7.1.1 Product Backlog |
| Actores | 2 | 7.1.2 Definición de actores |
| Requisitos funcionales | 21 | 7.1.3 Requisitos funcionales |
| Requisitos no funcionales | 11 | 7.1.4 Requisitos no funcionales |
| Entidades de almacenamiento | 16 | 7.1.5 Requisitos de almacenamiento |

Las 78 fichas y sus 386 criterios se conservan en `docs/03-matriz-trazabilidad.md` como matriz interna. No se incluyen en la memoria oficial.

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

El documento resultante contiene 72 tablas nuevas: 51 en 7.1.1 a 7.1.5 (1 backlog, 2 actores, 21 RF, 11 RNF y 16 RI) y 21 en 7.4.1. Las tablas de 7.1 llevan los números 16 a 66 y las de 7.4.1, del 67 al 87. Además, 7.1.6 incluye tres diagramas de secuencia con los números 2 a 4.

### 6.4 Parámetros y umbrales

Los parámetros viven dentro del RF o RNF que los usa, no en una sección aparte. Los valores acordados están escritos en su requisito (30 manos en RF-09, q < 0,05 en RF-12 y RF-20, 70 % y 40 BB en RF-08, 30 minutos en RF-05, cuatro decimales y 0,001 BB en RF-04, 2.000 y 10.000 manos en RF-06, 10 manos en RF-10, fórmula con EV en RF-12, 2 s y 60 s en RNF-03, reintento y recarga en RNF-11). Lo que sigue sin cerrar se marca como «pendiente de definir» en la frase que lo menciona:

| Dónde | Parámetro pendiente |
|---|---|
| RF-07 | Umbral de obsolescencia del baseline; fuera del MVP |
| RF-18 | Taxonomía y consentimiento; los pesos por nivel son provisionales (K14) |

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
- **Tabla de ilustraciones**: al abrir el documento en Word hay que aceptar la actualización de campos o pulsar `Ctrl+A` y `F9`. Si no se actualiza, la tabla de ilustraciones conserva las entradas antiguas, incluida «Ilustración 36: Diagrama de Secuencia 1».

### 6.8 Modelo de datos

`docs/02-modelo-datos.md` (v0.8) desarrolla el modelo lógico relacional: 20 entidades, 24 relaciones, 33 invariantes, índices recomendados y trazabilidad `RI → entidad`.

Las 16 entidades de 7.1.5 se mantienen. El modelo añade cuatro detalles de implementación que no llegan a la memoria:

| Entidad | Función |
|---|---|
| `bote` | Bote principal y side pots, que en `mano` solo caben como total |
| `metrica_valor` | Numerador y denominador de las 8 métricas en baseline, ventana, tramo, sesión y torneo |
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
