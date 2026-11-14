# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md

`AGENTS.md` (importado arriba) contiene la identidad del proyecto, el principio rector, las fuentes de verdad, las invariantes, las decisiones cerradas y abiertas y el glosario. Léelo primero: prevalece sobre cualquier comportamiento por defecto.

## Idioma

- Comunícate con el usuario **en español**.
- Redacta en español toda la documentación, los comentarios de código y los textos generados.
- No traduzcas nombres propios ni términos técnicos: Winamax, baseline, bad beat, trigger, VPIP, PFR, 3-Bet, EVbb/100, FDR, A-Game, MTT, HandRecord, Session Builder, etc.

## Estado actual

El proyecto está en la **fase de requisitos y modelo de datos. Todavía no hay código de la aplicación** (AGENTS.md §10: «No implementar todavía»). No hay build, lint ni tests. El único código está en `tools/`: scripts de Python 3 que solo usan la biblioteca estándar y generan los entregables del TFG (`.docx`, diagramas y matriz de trazabilidad) a partir de datos en Python.

## Estructura

- `sources/`: entradas que no se editan.
  - `master-doc.txt` (especificación funcional) y el PPTX del prototipo (fuente de verdad de la UI; ver más abajo).
  - `design-thinking.pptx` y la plantilla oficial de la UNED `Plantilla - Documentación.docx`.
  - `txtExamples/`: hand histories reales de MTT de Winamax. Son los únicos datos de ejemplo permitidos; no hay datos sintéticos.
- `docs/`: documentos de trabajo en Markdown, internos y no entregables.
  - `01-requisitos.md`: fichas `RF-DSH-*` detalladas, redactadas pantalla a pantalla. **Por ahora solo cubre el Dashboard.** Las demás pantallas existen como RF-01…RF-21 en `tools/plantilla_content.py` y como fichas en `SECTIONS` de `tools/build_requisitos_docx.py`.
  - `01-notas-internas.md`: registro de decisiones (IDs como `A01` o `B05`, enlazados a requisitos), dudas abiertas `P-*` y trazabilidad con el prototipo.
  - `02-modelo-datos.md`: modelo lógico relacional.
  - `03-matriz-trazabilidad.md`: se genera con un script.
- `docs/entrega/`: `.docx` generados. No se editan a mano; se regeneran.
- `tools/`: generadores (ver abajo).

## Estado de la memoria (`docs/entrega/Memoria-TFG-requisitos.docx`)

La memoria sigue la plantilla oficial (capítulos 1–10: Design Thinking + DevOps). Se rellena poco a poco con `tools/fill_plantilla.py`.

- **Cerrado:** 7.1 Plan al completo.
  - Introducción de 7.1.
  - 7.1.1 Product Backlog: 18 HU en 5 epics.
  - 7.1.2 Actores: Jugador y Sistema.
  - 7.1.3: RF-01…RF-21.
  - 7.1.4: RNF-01…RNF-11.
  - 7.1.5: RI-01…RI-16.
  - 7.1.6: 3 diagramas de secuencia.
- **Cerrado también:** 7.4.1 Casos de uso, con una prueba positiva y otra negativa por RF.
- **2.2 Planificación temporal:** rellenada solo con lo estimado (6 etapas, 300 h, 33 semanas hasta finales de mayo de 2027, tablas Gantt 7 a 12 e Ilustración 1). El descubrimiento ya está cerrado (16 oct a 8 nov de 2026, unas 30 h) y su sobrante se repartió en otras tareas. Falta añadir las horas reales y la desviación al terminar el proyecto; las filas rojas de los Gantt están vacías a propósito. Datos en `PLANIFICACION` (`tools/plantilla_content.py`); decisiones L01–L06 en `docs/01-notas-internas.md` §1.3. 2.1 (costes) sigue con el texto de ejemplo y debe coincidir con estas 300 h.
- **5.1 Gestión de la fase de descubrimiento:** hecho con datos reales (Tabla 13: 3 sprints, Plan-Do-Check-Act, etapas Understand and Empathy, Define, Idea y Prototype). Datos en `GESTION_DESCUBRIMIENTO`. La división en sprints y los días son una propuesta que el usuario puede ajustar. **5.2 y 5.3 se dejan con el ejemplo de la plantilla hasta que se avance en cada fase: no inventar datos, porque el capítulo 5 no admite aproximaciones.**
- **Siguiente bloque:** apartados 3 y 4 (prácticas y herramientas) y después el capítulo 6. La plantilla trae 6.4 Decide y 6.6 Validate, pero esas etapas no se realizaron: hay que quitarlas o indicarlo al escribir el capítulo 6.
- **Pendiente:** incrustar los UML del modelo de datos (`tools/build_uml.py` → `tools/diagrams/uml/`) cuando el usuario los revise. Hoy son una entrega aparte.
- **Sin rellenar:** capítulo 1, 2.1, capítulos 3, 4 y 6, 5.2, 5.3, 7.2, 7.3, 7.4.2, 7.5, 8, 9 y 10 conservan el texto de ejemplo de la plantilla, con restos ajenos al proyecto (Universidad de Sevilla, Ionic, tutores de ejemplo). Sustitúyelos cuando se aborde cada capítulo.
- **Manual del usuario:** tras regenerar el `.docx`, hay que abrirlo en Word y pulsar `Ctrl+A` y `F9` para actualizar el índice y las ilustraciones.

### Decisiones cerradas recientes

Están en `docs/01-notas-internas.md` §1.1 (J01–J12) y en `AGENTS.md` §10: mínimo de 2.000 manos y recomendado de 10.000 para el baseline, tramos fusionados a 10 manos, fórmula de la fuga neta, cartas en `TEXT`, glosario estático, snapshots archivados conservados y «auditar no es recalcular». El baseline inicial solo excluye las ventanas T+30 por trigger (K06); los tramos de desviación, solo las recalibraciones. La obsolescencia queda fuera del MVP. K01–K16: el baseline inicial se crea desde Mi Baseline vacío con archivos que no se auditan (lote de tipo `baseline`), y el jugador declara su nivel de juego (buy-in habitual) al registrarse, editable desde el drawer, solo para ponderar sus etiquetas (no ajusta referencias ni baseline); el buy-in de los torneos no se muestra ni se guarda. K07: estados del Dashboard antes del primer lote (diapositivas 5 y 8). K11–K12: la Comparativa Baseline vs Tilt agrega las ventanas del último lote contra el baseline activo y tiene RF-21. K15–K16: contexto del torneo sin posición final ni inscritos y glosario sin «Modo coach». K09: trigger = bad beat o pérdida de bote grande (amplía el `master-doc.txt`). K10: la comparativa muestra 5 métricas. K08: añadir y sustituir crean versiones nuevas; deshacer y restaurar eliminan la recién creada y sus archivos, solo desde el aviso efímero. K17–K27: suerte frente a conducta; BB ganadas, All-in EV y Suerte all-in (1σ provisional), bloque «Lectura» en el visor, sin VPIP/PFR en el Historial y 4 términos nuevos del Glosario. K28–K33: composición del baseline por torneos (`baseline_snapshot_torneo`), `origen`, `snapshot_padre_id` y `muestra_sesiones`; un archivo es siempre un torneo; el jugador solo ve el baseline activo; sin datos de ajuste all-in; fuga neta en positivo.

Dudas abiertas: `docs/01-notas-internas.md` §2 y `docs/02-modelo-datos.md` §9. No las resuelvas por tu cuenta.

**Esperando datos del usuario:** P-20 (pérdida mínima para que un bad beat cuente como trigger; el usuario la estudiará y avisará) y P-21 (alcance de la comparativa Baseline vs Tilt). No los fijes hasta que los comunique.

**Esperando decisión del usuario:** P-22 (la desviación sin trigger, ¿tramo con inicio, fin y fuga, o solo torneo marcado?). Mientras tanto, la Conducta de #8488 no muestra fuga ni límites de tramo (K24).

## Generadores (`tools/`)

Ejecútalos desde la raíz del repositorio con `python3`. No requieren pip; la conversión a PNG llama a `ffmpeg` (librsvg).

```bash
python3 tools/build_secuencias.py          # diagramas de secuencia → tools/diagrams/seq-0N.{svg,png}
python3 tools/build_planificacion.py       # valida PLANIFICACION y genera tools/diagrams/horas-estimadas.{svg,png}
python3 tools/build_uml.py                 # UML del modelo de datos → tools/diagrams/uml/uml-0N-*.{svg,png}
python3 tools/verificar_uml.py             # comprueba que los UML reflejan docs/02-modelo-datos.md (entidades, campos y relaciones); pásalo tras cada cambio de modelo
python3 tools/fill_plantilla.py            # → docs/entrega/Memoria-TFG-requisitos.docx (requiere antes los PNG de secuencia y de horas estimadas)
python3 tools/build_requisitos_docx.py     # → docs/entrega/Requisitos-Funcionales-TFG.docx
python3 tools/build_matriz_trazabilidad.py # → docs/03-matriz-trazabilidad.md
```

Cómo encajan las piezas:

- **Dos granularidades de requisitos.**
  - `build_requisitos_docx.py` contiene la lista `SECTIONS` con las **78 fichas internas** (`RF-ING-*`, `RF-PAR-*`, `RF-SES-*`, `RF-BAS-*`, `RF-DSH-*`, `RF-CMP-*`…).
  - `plantilla_content.py` contiene los **21 RF oficiales** (`RF-01`…`RF-21`) y además `BACKLOG`, `ACTORS`, `RNFS`, `RIS` (entidades de almacenamiento `RI-*`) y `CASOS_USO`, que se usan en la memoria.
- **Matriz de trazabilidad.** `build_matriz_trazabilidad.py` asigna fichas a RF con el diccionario `MAPPING`.
  - Carga `SECTIONS` haciendo `exec` de ese bloque de `build_requisitos_docx.py`: lee desde la línea que empieza por `SECTIONS` hasta la primera línea que sea exactamente `]`. Mantén ese formato.
  - Si añades o renombras una ficha, actualiza `MAPPING`.
- **Relleno de la plantilla.** `fill_plantilla.py` abre la plantilla oficial y sustituye en el OOXML los apartados 2.2 (planificación, con una tabla Gantt por etapa generada desde cero), 7.1.1–7.1.6 y 7.4.1.
  - Localiza cada apartado por el prefijo de su encabezado (`SECTION_PREFIXES`), así que el texto de esos encabezados en la plantilla debe coincidir.
  - Reutiliza las tablas de la propia plantilla como base de estilo e incrusta los PNG de secuencia.
  - Conserva el resto del documento y activa `w:updateFields` para que Word actualice el índice al abrirlo.
- **Escritor OOXML.** `docx_builder.py` es un escritor OOXML mínimo hecho a mano, que usa `build_requisitos_docx.py`.

**Modelo de datos y UML.** `build_uml.py` es una copia manual de `docs/02-modelo-datos.md` (entidades, campos y relaciones; no recoge restricciones, invariantes ni parámetros). Cuando cambies una entidad o una relación, edita las dos cosas y ejecuta `verificar_uml.py`.

Para cambiar el contenido de los requisitos, edita los datos en Python (`plantilla_content.py` o `SECTIONS`), mantenlos coherentes con `docs/*.md` y regenera las salidas afectadas.

## Prototipo (`sources/Mindset-EV-Leak-Finder-TFG.pptx`)

Es un PPTX de 60 diapositivas formado **solo por imágenes, sin texto extraíble**. Para revisar la diapositiva N, extrae `ppt/media/image-N-1.png` a un directorio temporal y léela como imagen. Los datos que muestra son simulados y sirven solo como referencia visual. El archivo se sustituye por versiones nuevas con el mismo nombre: comprueba siempre su fecha y su número de diapositivas antes de apoyarte en la numeración.

El prototipo se genera desde otro proyecto, `/home/marioraga29/dev/prototipo/prototipo/`, fuera de este repositorio. Allí están `LEEME.md` y `MAPA-CLICKS.md`, con el índice completo, las notas del orador y el mapa de clics en texto: son más fiables que las capturas.

| Diap. | Pantalla | Elementos clave |
|---|---|---|
| 1–4 | Portada, guía rápida, registro y acceso | Registro con nombre, correo, contraseña y nivel de juego (cinco tramos de buy-in). |
| 5–8 | Cuenta sin baseline y creación del baseline | Dashboard vacío (5), crear baseline sin archivos (6) y con archivo aceptado (7), y Dashboard con baseline creado y sin lotes auditados (8). |
| 9–10 | Dashboard | Línea (9) y barras (10). 4 KPIs con modal ⓘ, gráfica de fatiga, feed de alertas, resumen del lote y origen de los datos. |
| 11–18 | Historial | Tabla de torneos (11). Modal de filtros (12–15): estado, periodo y tipo de torneo (MTT 6-Max, MTT Deep, KO Battle, Winamax Series). Historiales filtrados (16–18). |
| 19 | Baseline vs Tilt (T+30) | Deltas en pp y fuga acumulada, barras normal vs tilt, explicación en 4 pasos, insignia FDR. |
| 20–22 | Importar | Lista de archivos agrupados por día con una X por archivo (añadir 21, quitar 22). El baseline no se toca aquí. |
| 23–27 | Mi Baseline | Estado congelado, fuente, cobertura y calidad. Añadir archivo (24–25, con «Deshacer»). Sustituir (26) y restaurar (27). |
| 28–30 | Recalibrar | 25.000, 15.000 o rango personalizado; excluir tilt y fatiga; impacto previsto. |
| 31–33 | Dashboard tras congelar | Con 25.000, 15.000 y rango personalizado. |
| 34–40 | Perfil | Drawer (34), ventana de tilt (35), sensibilidad (36), nivel de juego (37) y drawer sobre otras pantallas (38–40). |
| 41–46 | Visor de torneo #8492 | Gráfica real vs EV con trigger y franja T+30; manos #112, #113 (con y sin diagnóstico), #114, #128 y #142; diagnóstico comunitario y etiquetado. |
| 47 | Ventana T+30 | Rejilla de las 30 manos y KPIs de la ventana. |
| 48–50 | Visores de control | Desviación 3-Bet (#8488), sesión limpia (#8475) y pérdida por varianza (#8460). |
| 51 | Auditoría completada | Dashboard tras auditar. |
| 52–55 | Modales de KPI | VPIP, PFR, 3-Bet y Winrate, con «Ver en el Glosario». |
| 56–60 | Glosario | Métricas, mesa, conducta, estadística y producto. |

La mayoría de los conflictos del Dashboard ya están resueltos en `docs/01-notas-internas.md`. **Tensiones aún sin resolver.** Pregunta antes de redactar requisitos de estas pantallas:

Las dos tensiones anteriores están resueltas: sustituir, restaurar y «Deshacer» (K08, K28 y K29) y la relación archivo-torneo (K30: un archivo es siempre un torneo; «14 → 18» y «12 archivos · 42 sesiones» eran errores del prototipo). Quedan P-22 (desviación sin trigger) y los desajustes del punto 24.

Resueltas en el prototipo (K09 a K16; los cambios de K17–K33 los aplica el usuario con opencode, ver `docs/01-notas-internas.md` §3.1): textos del registro y del modal de nivel, trigger y 5 métricas de la comparativa (diapositiva 19), tramos y pesos del nivel de juego, contexto del torneo sin posición final ni inscritos, y glosario sin «Modo coach».

### Lista de trabajo: huecos entre requisitos, modelo y prototipo

Análisis del 8–13 de noviembre de 2026. **Se tratan de uno en uno, en orden.** Cada decisión se aplica a la vez en el prototipo (lo que deba cambiar el usuario), `docs/01-requisitos.md`, los RF y las fichas (`plantilla_content.py`, `build_requisitos_docx.py`), `docs/02-modelo-datos.md`, los UML (`build_uml.py`), `docs/01-notas-internas.md`, `AGENTS.md` y esta guía, y se regeneran los entregables.

| # | Punto | Estado |
|---|---|---|
| 1 | Baseline inicial: cómo se crea | **Cerrado** (K01, K02, K06, K07) |
| 2 | Gestión de archivos de Mi Baseline: añadir, sustituir, deshacer y restaurar | **Cerrado** (K08): añadir y sustituir crean versión; deshacer y restaurar eliminan la recién creada y sus archivos; la representación en el modelo se cerró en los puntos 6, 7 y 8 (K28–K30) |
| 3 | Pantalla Baseline vs Tilt (T+30) | **Cerrado** (K09–K12): RF-21 con 3 fichas y diapositiva 19 corregida. Quedan P-20 (pérdida mínima de un bad beat) y P-21 (alcance por estudiar) |
| 4 | Lectura «mala suerte vs mal juego» (EV frente a resultado real y varianza esperada) | **Cerrado** (K17–K27): Historial con BB ganadas, All-in EV y Suerte all-in; visor con bloque «Lectura» (Conducta y Suerte del torneo); `mano.equidad` y agregados en `torneo`; RF-VTR-05 y 4 términos del Glosario. 1σ provisional. Queda P-22 y los cambios del prototipo (`docs/01-notas-internas.md` §3.1) |
| 5 | Pantalla Ventana T+30 (rejilla de 30 manos) sin requisito | Pendiente; su «Resultado adicional» y la suma de la rejilla se revisan con K23 |
| 6 | Qué manos componen cada snapshot (propuesta: tabla de composición) | **Cerrado** (K28, K31): entidad `baseline_snapshot_torneo`; dato interno; el jugador solo ve el baseline activo |
| 7 | Entidad `archivo`. Incluye que Importar muestra más torneos que archivos (14 → 18) frente a «un archivo = un torneo» | **Cerrado** (K30): un archivo es siempre un torneo; no hay entidad `archivo`; las cifras del prototipo eran errores |
| 8 | `baseline_snapshot` corto: versión padre, origen (inicial, añadir, sustituir, recalibrar), muestra elegida, `sample_files`, `sample_sessions`, `allin_count`, `ev_adjustment` | **Cerrado** (K29, K32): `origen`, `snapshot_padre_id` y `muestra_sesiones`; los archivos se cuentan por la lista de torneos; sin datos de ajuste all-in |
| 9 | `tramo_fatiga`: colgar del snapshot, horas numéricas, IC 95 %, zona, punto crítico y último tramo abierto | Pendiente |
| 10 | Configuración aplicada (`fdr_q`, ventana) en `lote_importacion` | Pendiente |
| 11 | Versión del motor en alerta, ventana, tramo y prueba estadística | Pendiente |
| 12 | `snapshot_id` en `prueba_estadistica` | Pendiente |
| 13 | Nivel 2 incompleto: sugerencia con % de coincidencia, modelo clasificador, `ejemplo` y polaridad de `etiqueta` | Pendiente |
| 14 | Alias de Winamax en `usuario` | Pendiente |
| 15 | Tipo de torneo para el filtro del Historial | Valores ya en el prototipo (MTT 6-Max, MTT Deep, KO Battle, Winamax Series); falta el modelo |
| 16 | RF-06 y RF-09 calculan 4 métricas; la comparativa usa 5 (VPIP, PFR, 3-Bet, Fold vs 3-Bet y WTSD, K10) | Pendiente: que baseline y ventana calculen esas 5 |
| 17 | ¿La recalibración excluye la fatiga? Decidido que no (C06); el prototipo tiene la casilla «Excluir fatiga» (diapositivas 28–30) | Pendiente de reconciliar |
| 18 | Peso por stake frente al buy-in | **Cerrado** (K03–K05 y pesos provisionales K14) |
| 19 | Contexto del torneo en los visores: posición final e inscritos no están en el `.txt` | **Cerrado** (K15): el prototipo solo muestra formato, manos y resultado |
| 20 | Torneos anteriores al `hasta` del baseline activo (fuga de datos) | Pendiente |
| 21 | Sesión limpia por sesión frente a Historial por torneo; HU-15 pide evolución por sesión sin vista | Pendiente |
| 22 | Tramos del nivel de juego y sus pesos | **Cerrado** (K13 tramos, K14 pesos provisionales) |
| 23 | Glosario con «Modo coach», fuera del MVP | **Cerrado** (K16): quitado del glosario (Producto: 7 términos) |
| 24 | Desajustes menores: erratas como «CÓMO SE LEER» (RF-DSH-CFG-03.a); RI-02 lista «rango de manos» y RI-09 lista «trigger»; `usuario.ventana_reactiva` y `fdr_q` deberían limitarse a los valores permitidos; `alerta` no guarda la fecha de auditoría; requisitos de contraseña ausentes de la nota 6.4; la tarjeta del Dashboard se llama «Winrate baseline» (sin la etiqueta «ajuste all-in» ni la palabra EV) mientras los requisitos hablan de «EVbb/100 (ajuste all-in)»; RF-06 y RF-DSH-KPI-01 piden mostrar versión e «Inicial/Recalibrado», que no aparecen en las diapositivas 23 a 27 | Pendiente |
