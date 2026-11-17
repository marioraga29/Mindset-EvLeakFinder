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
  - 7.1.4: RNF-01…RNF-12.
  - 7.1.5: RI-01…RI-16.
  - 7.1.6: 3 diagramas de secuencia.
- **Cerrado también:** 7.4.1 Casos de uso, con una prueba positiva y otra negativa por RF.
- **2.2 Planificación temporal:** rellenada solo con lo estimado (6 etapas, 300 h, 33 semanas hasta finales de mayo de 2027, tablas Gantt 7 a 12 e Ilustración 1). El descubrimiento ya está cerrado (16 oct a 8 nov de 2026, unas 30 h) y su sobrante se repartió en otras tareas. Falta añadir las horas reales y la desviación al terminar el proyecto; las filas rojas de los Gantt están vacías a propósito. Datos en `PLANIFICACION` (`tools/plantilla_content.py`); decisiones L01–L06 en `docs/01-notas-internas.md` §1.3. 2.1 (costes) sigue con el texto de ejemplo y debe coincidir con estas 300 h.
- **5.1 Gestión de la fase de descubrimiento:** hecho con datos reales (Tabla 13: 3 sprints, Plan-Do-Check-Act, etapas Understand and Empathy, Define, Idea y Prototype). Datos en `GESTION_DESCUBRIMIENTO`. La división en sprints y los días son una propuesta que el usuario puede ajustar. **5.2 y 5.3 se dejan con el ejemplo de la plantilla hasta que se avance en cada fase: no inventar datos, porque el capítulo 5 no admite aproximaciones.**
- **Siguiente bloque:** apartados 3 y 4 (prácticas y herramientas) y después el capítulo 6. La plantilla trae 6.4 Decide y 6.6 Validate, pero esas etapas no se realizaron: hay que quitarlas o indicarlo al escribir el capítulo 6.
- **Pendiente:** incrustar los UML del modelo de datos (`tools/build_uml.py` → `tools/diagrams/uml/`) cuando el usuario los revise. Hoy son una entrega aparte.
- **Sin rellenar:** capítulo 1, 2.1, capítulos 3, 4 y 6, 5.2, 5.3, 7.2, 7.3, 7.4.2, 7.5, 8, 9 y 10 conservan el texto de ejemplo de la plantilla, con restos ajenos al proyecto (Universidad de Sevilla, Ionic, tutores de ejemplo). Sustitúyelos cuando se aborde cada capítulo.
- **Manual del usuario:** tras regenerar el `.docx`, hay que abrirlo en Word y pulsar `Ctrl+A` y `F9` para actualizar el índice y las ilustraciones.

### Decisiones cerradas

Están en `docs/01-notas-internas.md` §1 (J, K, L y M, hasta M29) y en `AGENTS.md` §10; no se repiten aquí. Pendiente de M01 (RNF-12): la revisión del modelo y de los RF campo a campo, que espera la confirmación del usuario, y la librería de traducción (P-29).

Dudas abiertas: `docs/01-notas-internas.md` §2 y `docs/02-modelo-datos.md` §9. No las resuelvas por tu cuenta.

**Esperando datos del usuario:** P-20 (pérdida mínima para que un bad beat cuente como trigger; el usuario la estudiará y avisará) y P-21 (alcance de la comparativa Baseline vs Tilt). No los fijes hasta que los comunique.


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
  - `build_requisitos_docx.py` contiene la lista `SECTIONS` con las **80 fichas internas** (`RF-ING-*`, `RF-PAR-*`, `RF-SES-*`, `RF-BAS-*`, `RF-DSH-*`, `RF-CMP-*`…).
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

## Prototipo (`sources/Mindset-EV-Leak-Finder-TFG-v6.pptx`)

Es un PPTX de 71 diapositivas (v6, 16-nov-2026) formado **solo por imágenes**; las notas del orador de cada diapositiva sí son texto extraíble (`ppt/notesSlides`) y describen lo que muestra. Para revisar la diapositiva N, extrae `ppt/media/image-N-1.png` a un directorio temporal y léela como imagen (en la v6 la imagen N coincide con la diapositiva N). Los datos que muestra son simulados y sirven solo como referencia visual. El archivo se sustituye por versiones nuevas (v2, v3, v6…): usa la más reciente y comprueba siempre su fecha y su número de diapositivas antes de apoyarte en la numeración.

El prototipo se genera desde otro proyecto, `/home/marioraga29/dev/prototipo/prototipo/`, fuera de este repositorio. Allí están `LEEME.md` y `MAPA-CLICKS.md`, con el índice completo, las notas del orador y el mapa de clics en texto: son más fiables que las capturas.

| Diap. | Pantalla | Elementos clave |
|---|---|---|
| 1–4 | Portada, guía rápida, registro y acceso | Registro con nombre, correo, contraseña y nivel de juego (cinco tramos de buy-in). |
| 5–8 | Cuenta sin baseline y creación del baseline | Dashboard vacío (5), crear baseline sin archivos (6) y con archivo aceptado (7), y Dashboard con baseline creado y sin lotes auditados (8). |
| 9–10 | Dashboard | Línea (9) y barras (10). 4 KPIs con modal ⓘ, gráfica de fatiga, feed de alertas, resumen del lote y origen de los datos. |
| 11–18 | Historial | Tabla de torneos (11). Modal de filtros (12–15): estado, periodo y tipo de torneo (MTT 6-Max, MTT Deep, KO Battle, Winamax Series). Historiales filtrados (16–18). |
| 20–22 | Importar | Lista de archivos agrupados por día con una X por archivo (añadir 21, quitar 22). El baseline no se toca aquí. |
| 23–27 | Mi Baseline | Estado congelado, fuente, cobertura y calidad. Añadir archivo (24–25, con «Deshacer»). Sustituir (26) y restaurar (27). |
| 28–30 | Recalibrar | 25.000, 15.000 o rango personalizado; excluir tilt y fatiga; impacto previsto. |
| 31–33 | Dashboard tras congelar | Con 25.000, 15.000 y rango personalizado. |
| 34–40 | Perfil | Drawer (34), ventana de tilt (35), sensibilidad (36), nivel de juego (37) y drawer sobre otras pantallas (38–40). |
| 41–46 | Visor de torneo #8492 | Gráfica real vs EV con trigger y franja T+30; manos #112, #113 (con y sin diagnóstico), #114, #128 y #142; diagnóstico comunitario y etiquetado. |
| 48–50 | Visores de control | Desviación 3-Bet (#8488), torneo limpio (#8475) y pérdida por varianza (#8460). |
| 52–55 | Modales de KPI | VPIP, PFR, 3-Bet y Winrate, con «Ver en el Glosario». |
| 56–60 | Glosario | Métricas, mesa, conducta, estadística y producto. |
| 61–65 | Modales ⓘ | BB ganadas, All-in EV, Suerte all-in (desde el Historial y desde «Lectura») y Fuga neta. |
| 66–71 | Caso multi-table (#8501 y #8507) | Visor con pestañas por torneo, pestaña del #8507, rejilla de la ventana con torneo por mano y tres manos clave. El #8492 sigue siendo el ejemplo de torneo individual. |

Los conflictos del prototipo están resueltos en `docs/01-notas-internas.md`. Las «manos clave» y las «manos bisagra» de las diapositivas 41–47 son un recurso de la demo, no un concepto del producto (M28). Los cambios que el usuario aún debe aplicar al prototipo están en `docs/01-notas-internas.md` §3.1.

### Lista de trabajo

Los 31 huecos entre requisitos, modelo y prototipo (análisis de noviembre de 2026) están cerrados salvo el **punto 30**: umbral de trigger relativo al stack en el MVP (propuesta del informe de revisión: 50 % del stack con un mínimo de 10 BB, provisional), que se decide junto con P-20 (P-28) y espera los datos del usuario. El registro de cada decisión (M01 a M29) y su porqué está en `docs/01-notas-internas.md` §1.4; el estado consolidado, en `AGENTS.md`.

Regla de trabajo: cada decisión se aplica a la vez en `docs/01-requisitos.md`, los RF y las fichas (`plantilla_content.py`, `build_requisitos_docx.py`), `docs/02-modelo-datos.md`, los UML (`build_uml.py`), `docs/01-notas-internas.md`, `AGENTS.md` y esta guía. Lo que deba cambiar el usuario en el prototipo se anota en las notas §3.1 y los términos del Glosario del producto en §3.2 (no se piden al prototipo). Los entregables solo se regeneran cuando el usuario lo autoriza.
