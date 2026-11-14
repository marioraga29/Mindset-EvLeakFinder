# AGENTS.md — Mindset & EV Leak Finder

## 1. Identidad del proyecto

- **Título:** Mindset & EV Leak Finder: Detección algorítmica de desviaciones conductuales y degradación del rendimiento en póker online mediante análisis de series temporales y baseline individual.
- **Autor:** Mario Ramírez García.
- **Titulación:** Grado en Ingeniería Informática, UNED.
- **Año:** 2026.
- **Tipo:** Trabajo de Fin de Grado.

## 2. Elevator pitch

Los trackers tradicionales resumen miles de manos en medias globales y obligan al jugador a buscar manualmente el momento en el que su conducta cambió. Este proyecto compara cada torneo contra el **baseline individual** del propio jugador y localiza dos fenómenos: **ventanas reactivas T+30** tras un bad beat crítico y **tramos continuos de sobrefrecuencia** sin trigger aparente. La interfaz no juzga el resultado: muestra evidencia estadística auditable mano a mano y separa mala suerte de mal juego. Sobre esa base, una capa colaborativa permite etiquetar jugadas para entrenar un clasificador común con validación humana.

## 3. Principio rector

> **El resultado no define la conducta.**

Un torneo puede ganar dinero y contener una desviación conductual; otro puede perder y ser una sesión limpia porque la pérdida se explica por varianza. Las alertas se basan en conducta observable contrastada contra el baseline, nunca en el resultado económico aislado.

## 4. Fuentes de verdad

| Fuente | Ruta | Uso |
|---|---|---|
| Especificación técnica | `sources/master-doc.txt` | Pipeline, módulos, criterios funcionales |
| Prototipo visual | `sources/Mindset-EV-Leak-Finder-TFG.pptx` (60 diapositivas) | Fuente de verdad de la UI |
| Design Thinking | `sources/design-thinking.pptx` (14 diapositivas) | Investigación UX, personas, decisiones de diseño |

Regla de conflicto: **el prototipo manda en UI**, `master-doc.txt` manda en comportamiento funcional, `design-thinking` explica el porqué. Si hay contradicción, preguntar antes de asumir.

## 5. Alcance del MVP

Incluido:

- Ingesta de hand histories `.txt` de torneos Winamax.
- Normalización monetaria a ciegas grandes (BB).
- Session Builder y agrupación por torneo.
- Baseline individual congelado y recalibración.
- Detección de trigger, ventana T+30, tramos continuos y fatiga.
- Dashboard macro, historial, visor de torneo y visor de mano.
- Etiquetado colaborativo con validación humana.
- Glosario y ayuda contextual.

Fuera del MVP:

- HUD en tiempo real.
- Replayer 3D animado.
- Cash game.
- Modo coach.
- Multiusuario completo si no es necesario para la demo.

## 6. Pipeline de datos

```
.txt Winamax
  → Parser ETL
  → HandRecord canónico
  → Normalización a BB
  → Session Builder (sesión + torneo)
  → Baseline individual (snapshot congelado)
  → Detectores Nivel 1
       ├─ Trigger bad beat
       ├─ Ventana T+30
       ├─ Sliding window + interval merging
       └─ Fatiga por horas
  → Corrección FDR
  → API REST
  → Frontend
```

## 7. Nivel 1 vs. Nivel 2

- **Nivel 1 — Individual:** baseline personal, detección de anomalías, evidencia auditable. Es la fuente de verdad del diagnóstico conductual.
- **Nivel 2 — Colectivo:** etiquetado semántico de jugadas y entrenamiento de un clasificador común. Es crowdsourcing desde el diseño, aunque al principio solo haya un usuario. Nunca altera una alerta ya emitida.

## 8. Reglas e invariantes

1. El baseline solo usa datos cronológicamente anteriores al periodo evaluado.
2. El resultado no define la conducta.
3. T+30: el trigger queda excluido; se analizan las 30 manos posteriores; si dos triggers se solapan, se fusionan.
4. La fatiga no entra en el feed de alertas: solo se visualiza en la gráfica macro y se mide en horas.
5. Una etiqueta comunitaria no modifica el baseline ni las alertas del Nivel 1.
6. No se inventan datos ni etiquetas sintéticas para la demo.
7. Las métricas deben guardar numerador y denominador, no solo porcentajes.
8. El baseline se congela como snapshot inmutable y versionado.

## 9. Pantallas principales

- Portada, guía rápida y login.
- Dashboard macro con KPIs, gráfica de fatiga y feed de alertas.
- Historial de torneos con filtros.
- Mi Baseline y recalibración.
- Importación de nuevas sesiones.
- Visor de torneo con gráfica dual real vs EV.
- Visor de mano con diagnóstico comunitario y etiquetado.
- Ventana T+30.
- Glosario, tooltips y drawer de configuración.

## 10. Decisiones ya cerradas

- Parser inicial: Winamax MTT `.txt`, con interfaz para añadir otros sitios.
- T+30: trigger excluido, 30 manos posteriores, fusión de solapes.
- Fatiga: solo gráfica, en horas, fuera del feed.
- Nivel 2: crowdsourcing multiusuario, arranque real con un solo usuario, sin semilla ficticia.
- Fuga neta: se mantiene el nombre y el campo en la UI. Fórmula: `max(0, (EVbb/100 baseline − EVbb/100 observado) × manos / 100)`; sin EV, «no estimable».
- EV: all-in con ajuste por equidad; el resto de manos, resultado real. La métrica de rendimiento es `EVbb/100`.
- Baseline: mínimo 2.000 manos y recomendado 10.000 (por debajo, aviso «muestra pequeña»). El baseline inicial excluye solo las ventanas T+30 de los triggers (se detectan sin baseline); las recalibraciones excluyen además los tramos de desviación; la fatiga no se excluye. Se conservan todos los snapshots archivados.
- Obsolescencia del baseline: fuera del MVP; umbral pendiente.
- Sesión: pausa de 30 minutos; es un dato derivado y recalculable. Un torneo pertenece a una sola sesión.
- Tramos de desviación: se fusionan bloques separados por menos de 10 manos.
- Cartas y board: `TEXT` compacto (por ejemplo `AhKd7c`); el API los entrega estructurados al visor.
- Glosario estático en el frontend. Índices por consulta, sin particiones ni `bote_ganador`.
- Auditar una alerta no la recalcula: cada alerta conserva el snapshot con el que se calculó.
- Baseline inicial: se crea desde Mi Baseline en estado vacío. Esos archivos solo construyen el perfil: no se auditan ni aparecen en el Historial.
- Mi Baseline: añadir y sustituir archivos crean una versión nueva; «Deshacer» y «Restaurar» eliminan esa versión recién creada junto con los archivos que solo incorporó, y reactivan la anterior, solo desde el aviso que aparece al hacer la acción (se pierde al cambiar de pestaña o cerrarlo). Una versión que ha servido para alguna alerta nunca se elimina.
- Trigger: bad beat o pérdida de bote grande de 40 BB o más (amplía `master-doc.txt`). La pérdida mínima de un bad beat está pendiente y el umbral de 40 BB se prevé relativo al stack, fuera del MVP. La comparativa Baseline vs Tilt (RF-21) muestra 5 métricas (VPIP, PFR, 3-Bet, Fold vs 3-Bet y WTSD), agrega las ventanas T+30 del último lote y las compara con el baseline activo.
- Pesos por nivel de juego (provisionales, a calibrar con datos reales): Micro 0,6, Bajo 0,8, Medio 1,0, Alto 1,2 y Muy alto 1,4.
- Nivel de juego: el jugador declara su buy-in habitual al registrarse y puede cambiarlo; solo pondera sus etiquetas del Nivel 2. El buy-in de los torneos no se muestra ni se guarda.
- Suerte frente a conducta (K17–K27): el Historial y el visor de torneo muestran **BB ganadas**, **All-in EV** y **Suerte all-in** (A favor, Neutra o En contra). Neutra si la diferencia entre BB ganadas y All-in EV no supera 1σ, con σ = √Σ(bote² · e · (1 − e)) sobre los all-in del torneo (1σ provisional; sin all-in, neutra). La equidad se calcula en la ingesta y se guarda en `mano.equidad`. BB ganadas y All-in EV conservan verde y rojo; Suerte all-in va sin color. El Historial no muestra VPIP/PFR. El visor tiene un único bloque «Lectura» con Conducta (según el caso: ventana T+30 con métricas de la alerta y fuga neta; desviación sin fuga ni tramo; sin alertas sin métricas) y Suerte del torneo; el contexto del torneo va en la cabecera.
- Composición del baseline (K28–K33): cada versión guarda los torneos que la componen (entidad de enlace `baseline_snapshot_torneo`), su origen (inicial, añadir, sustituir o recalibrar), la versión de la que procede y el número de sesiones congelado. Sustituir deja fuera todos los archivos anteriores sin importar sus fechas. **Un archivo es siempre un torneo**: no hay entidad `archivo` y el número de archivos es el número de torneos de la lista. El jugador solo ve el baseline activo; las versiones archivadas son internas y sirven para auditar alertas. El baseline no guarda datos de ajuste all-in. La fuga neta se muestra como magnitud positiva en BB.
- Fase actual: requisitos funcionales y modelo de datos. **No implementar todavía.** El apartado 7.1 de la memoria está cerrado.

## 11. Decisiones abiertas

- Umbral de obsolescencia del baseline (fuera del MVP).
- Alcance de la comparativa Baseline vs Tilt (de momento, el último lote; por estudiar).
- Pérdida mínima de un bad beat para que cuente como trigger.
- Mínimo de manos por tramo de fatiga.
- Si la desviación sin trigger se representa como tramo (inicio, fin y fuga) o solo como torneo marcado (P-22).
- Taxonomía definitiva de etiquetas.
- Privacidad y consentimiento para el etiquetado colaborativo.
- Librería de equidad, semilla y versión del EV (se decide en 7.2).
- Estados vacíos, errores, carga y accesibilidad de las pantallas distintas del Dashboard (en el Dashboard ya están cerrados).
- Detalles de interfaz del Dashboard: cierre de overlays, copy de toasts y modales, tokens de color, contador del enlace al historial y definición de `CON ALERTA`.
- Modo coach: fuera del MVP (ya no aparece en el glosario del prototipo).

## 12. Cómo trabajar en este repositorio
- No inventar datos, métricas ni etiquetas.
- Documentar las decisiones y las dudas en lugar de asumirlas.
- Si una fuente contradice a otra, preguntar antes de decidir.

## 13. Glosario mínimo

- **Baseline:** referencia estable del jugador obtenida de sesiones limpias, sin tilt ni fatiga. Es el estándar contra el que se compara cada ventana.
- **Trigger:** evento gatillo: un bad beat (all-in perdido con equidad ≥ 70 %) o la pérdida de un bote grande (≥ 40 BB, haya habido all-in o no).
- **Ventana T+30:** las 30 manos inmediatamente posteriores a un trigger. El trigger no se incluye.
- **Tramo continuo:** bloque de manos consecutivas con una desviación sostenida, detectado mediante ventanas deslizantes y fusión de intervalos.
- **Fuga neta:** coste estimado en BB de haber jugado distinto al baseline en una ventana, medido en EV para no atribuir a la conducta la suerte de los all-in. Se calcula como `max(0, (EVbb/100 baseline − EVbb/100 observado) × manos / 100)` y se muestra como magnitud positiva en BB.
- **BB ganadas:** fichas ganadas o perdidas en el torneo, en ciegas grandes; suma del resultado real de sus manos. No es la posición final ni el premio.
- **All-in EV:** resultado que se habría obtenido si los all-in hubieran salido como dicta la equidad; sin all-in coincide con las BB ganadas.
- **Suerte all-in:** A favor, Neutra o En contra, según la diferencia entre BB ganadas y All-in EV frente a la suerte esperable por azar (1σ, provisional). No dice nada sobre la conducta.
- **BB/100:** ciegas grandes ganadas o perdidas por cada 100 manos.
- **EVbb/100:** rendimiento esperado por 100 manos, calculado con la equidad de los all-in en lugar del resultado real.
- **FDR (Benjamini–Hochberg):** corrección por comparaciones múltiples para limitar falsos positivos; se trabaja con `q < 0,05`.
- **A-Game:** nivel de juego óptimo del jugador, sin fatiga ni sesgo emocional.
- **Sesión limpia:** sesión sin alertas de tilt ni desviaciones significativas, independientemente de si el resultado económico fue positivo o negativo.


