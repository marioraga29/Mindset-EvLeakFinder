# Matriz de trazabilidad interna

> Documento interno. No forma parte de la entrega de la memoria. Las 80 fichas se conservan aquí como criterios de aceptación y como trazabilidad de los 21 requisitos funcionales de la plantilla oficial.

## 1. Correspondencia entre los 21 RF y las fichas internas

| RF | Nombre | Fichas absorbidas | Fichas | Criterios |
|---|---|---|---:|---:|
| RF-01 | Importar archivos de Winamax | RF-ING-01, RF-ING-02, RF-ING-03, RF-ING-04 | 4 | 23 |
| RF-02 | Resumir y procesar el lote | RF-ING-05, RF-ING-06, RF-ING-07 | 3 | 17 |
| RF-03 | Interpretar y registrar el historial | RF-PAR-01, RF-PAR-02, RF-PAR-03, RF-PAR-04, RF-PAR-05, RF-PAR-09 | 6 | 39 |
| RF-04 | Normalizar, calcular EV y métricas | RF-PAR-06, RF-PAR-07, RF-PAR-08 | 3 | 24 |
| RF-05 | Agrupar manos en sesiones | RF-SES-01, RF-SES-02, RF-SES-03, RF-SES-04, RF-SES-05 | 5 | 38 |
| RF-06 | Calcular el baseline individual | RF-BAS-01, RF-BAS-03, RF-BAS-06 | 3 | 14 |
| RF-07 | Congelar y recalibrar el baseline | RF-BAS-02, RF-BAS-04, RF-BAS-05 | 3 | 23 |
| RF-08 | Detectar el trigger de bad beat | RF-DET-01 | 1 | 5 |
| RF-09 | Analizar la ventana T+30 | RF-DET-02, RF-DET-03 | 2 | 15 |
| RF-10 | Detectar desviaciones sin trigger | RF-DET-04, RF-DET-05 | 2 | 7 |
| RF-11 | Analizar la fatiga | RF-DET-06 | 1 | 6 |
| RF-12 | Corregir FDR y generar alertas | RF-DET-07, RF-DET-08 | 2 | 11 |
| RF-13 | Dashboard: KPIs y fatiga | RF-DSH-01, RF-DSH-02, RF-DSH-03 | 3 | 12 |
| RF-14 | Dashboard: feed y evidencia | RF-DSH-04, RF-DSH-05, RF-DSH-06, RF-DSH-07, RF-DSH-08, RF-DSH-10 | 6 | 32 |
| RF-15 | Historial de torneos | RF-HIS-01, RF-HIS-02, RF-HIS-03, RF-HIS-04, RF-HIS-05 | 5 | 24 |
| RF-16 | Visor de torneo | RF-VTR-01, RF-VTR-02, RF-VTR-03, RF-VTR-04, RF-VTR-05, RF-VTR-06, RF-VTR-07 | 7 | 37 |
| RF-17 | Visor de mano | RF-VMA-01, RF-VMA-02, RF-VMA-03, RF-VMA-04, RF-VMA-05, RF-VMA-06 | 6 | 20 |
| RF-18 | Etiquetar jugadas del Nivel 2 | RF-ETQ-01, RF-ETQ-02, RF-ETQ-03, RF-ETQ-04, RF-ETQ-05, RF-ETQ-06, RF-ETQ-07 | 7 | 23 |
| RF-19 | Glosario y ayuda contextual | RF-GLO-01, RF-GLO-02 | 2 | 7 |
| RF-20 | Cuenta, registro y configuración | RF-DSH-09, RF-CUE-01, RF-CUE-02, RF-CUE-03, RF-CUE-04, RF-CUE-05 | 6 | 27 |
| RF-21 | Comparar el baseline con las ventanas T+30 | RF-CMP-01, RF-CMP-02, RF-CMP-03 | 3 | 16 |
| **Total** | | | **80** | **420** |

## 2. Matriz completa por módulo

| Ficha | Nombre | Módulo | RF | Criterios |
|---|---|---|---:|---:|
| | **3.1 Importación e ingesta** | | | |
| RF-ING-01 | Acceso a la importación | 3.1 Importación e ingesta | RF-01 | 4 |
| RF-ING-02 | Carga de archivos | 3.1 Importación e ingesta | RF-01 | 7 |
| RF-ING-03 | Validación de archivos | 3.1 Importación e ingesta | RF-01 | 6 |
| RF-ING-04 | Detección de torneos duplicados | 3.1 Importación e ingesta | RF-01 | 6 |
| RF-ING-05 | Resumen previo del lote | 3.1 Importación e ingesta | RF-02 | 6 |
| RF-ING-06 | Confirmación y procesamiento atómico | 3.1 Importación e ingesta | RF-02 | 6 |
| RF-ING-07 | Resultado, errores y destino | 3.1 Importación e ingesta | RF-02 | 5 |
| | **3.2 Parser y normalización** | | | |
| RF-PAR-01 | Identificación del torneo y de la mano | 3.2 Parser y normalización | RF-03 | 7 |
| RF-PAR-02 | Metadatos del torneo | 3.2 Parser y normalización | RF-03 | 6 |
| RF-PAR-03 | Jugadores, asientos y posición | 3.2 Parser y normalización | RF-03 | 8 |
| RF-PAR-04 | Secuencia de acciones por calle | 3.2 Parser y normalización | RF-03 | 6 |
| RF-PAR-05 | Botes, showdown y side pots | 3.2 Parser y normalización | RF-03 | 6 |
| RF-PAR-06 | Normalización a ciegas grandes | 3.2 Parser y normalización | RF-04 | 7 |
| RF-PAR-07 | Resultado real y EV del all-in | 3.2 Parser y normalización | RF-04 | 10 |
| RF-PAR-08 | Métricas de conducta | 3.2 Parser y normalización | RF-04 | 7 |
| RF-PAR-09 | Registro canónico e integridad | 3.2 Parser y normalización | RF-03 | 6 |
| | **3.3 Session Builder: sesiones y torneos** | | | |
| RF-SES-01 | Línea temporal global de manos | 3.3 Session Builder: sesiones y torneos | RF-05 | 6 |
| RF-SES-02 | Delimitación de sesiones | 3.3 Session Builder: sesiones y torneos | RF-05 | 7 |
| RF-SES-03 | Metadatos y rendimiento de la sesión | 3.3 Session Builder: sesiones y torneos | RF-05 | 10 |
| RF-SES-04 | Sesiones del lote y recálculo global | 3.3 Session Builder: sesiones y torneos | RF-05 | 8 |
| RF-SES-05 | Coherencia e integridad de las sesiones | 3.3 Session Builder: sesiones y torneos | RF-05 | 7 |
| | **3.4 Baseline individual** | | | |
| RF-BAS-01 | Cálculo del baseline individual | 3.4 Baseline individual | RF-06 | 8 |
| RF-BAS-02 | Congelación y versionado del baseline | 3.4 Baseline individual | RF-07 | 13 |
| RF-BAS-03 | Muestra mínima del baseline | 3.4 Baseline individual | RF-06 | 3 |
| RF-BAS-04 | Recalibración del baseline | 3.4 Baseline individual | RF-07 | 7 |
| RF-BAS-05 | Aviso de obsolescencia | 3.4 Baseline individual | RF-07 | 3 |
| RF-BAS-06 | Consulta del baseline activo | 3.4 Baseline individual | RF-06 | 3 |
| | **3.5 Detección Nivel 1** | | | |
| RF-DET-01 | Detección del trigger de bad beat | 3.5 Detección Nivel 1 | RF-08 | 5 |
| RF-DET-02 | Ventana reactiva T+30 | 3.5 Detección Nivel 1 | RF-09 | 7 |
| RF-DET-03 | Métricas de la ventana reactiva | 3.5 Detección Nivel 1 | RF-09 | 8 |
| RF-DET-04 | Detección de desviaciones sin trigger | 3.5 Detección Nivel 1 | RF-10 | 4 |
| RF-DET-05 | Fusión de intervalos anómalos | 3.5 Detección Nivel 1 | RF-10 | 3 |
| RF-DET-06 | Análisis de fatiga | 3.5 Detección Nivel 1 | RF-11 | 6 |
| RF-DET-07 | Corrección por comparaciones múltiples | 3.5 Detección Nivel 1 | RF-12 | 4 |
| RF-DET-08 | Generación de alertas | 3.5 Detección Nivel 1 | RF-12 | 7 |
| | **3.6 Dashboard macro** | | | |
| RF-DSH-01 | Resumen del baseline activo | 3.6 Dashboard macro | RF-13 | 4 |
| RF-DSH-02 | Presentación del EVbb/100 | 3.6 Dashboard macro | RF-13 | 2 |
| RF-DSH-03 | Gráfica de fatiga | 3.6 Dashboard macro | RF-13 | 6 |
| RF-DSH-04 | Feed de alertas del último lote | 3.6 Dashboard macro | RF-14 | 7 |
| RF-DSH-05 | Tarjeta de evidencia de la alerta | 3.6 Dashboard macro | RF-14 | 4 |
| RF-DSH-06 | Auditoría de una alerta | 3.6 Dashboard macro | RF-14 | 5 |
| RF-DSH-07 | Resumen y origen del lote | 3.6 Dashboard macro | RF-14 | 5 |
| RF-DSH-08 | Shell y navegación global | 3.6 Dashboard macro | RF-14 | 6 |
| RF-DSH-09 | Cuenta y configuración del motor | 3.6 Dashboard macro | RF-20 | 5 |
| RF-DSH-10 | Estados, avisos y accesibilidad | 3.6 Dashboard macro | RF-14 | 5 |
| | **3.7 Historial de torneos** | | | |
| RF-HIS-01 | Listado de torneos | 3.7 Historial de torneos | RF-15 | 7 |
| RF-HIS-02 | Filtros del historial | 3.7 Historial de torneos | RF-15 | 5 |
| RF-HIS-03 | Estado conductual del torneo | 3.7 Historial de torneos | RF-15 | 6 |
| RF-HIS-04 | Acceso al visor del torneo | 3.7 Historial de torneos | RF-15 | 3 |
| RF-HIS-05 | Persistencia del historial | 3.7 Historial de torneos | RF-15 | 3 |
| | **3.8 Visor de torneo** | | | |
| RF-VTR-01 | Gráfica dual real vs. EV | 3.8 Visor de torneo | RF-16 | 5 |
| RF-VTR-02 | Franjas de anomalías | 3.8 Visor de torneo | RF-16 | 4 |
| RF-VTR-03 | Navegación a la mano | 3.8 Visor de torneo | RF-16 | 3 |
| RF-VTR-04 | Cabecera del torneo | 3.8 Visor de torneo | RF-16 | 3 |
| RF-VTR-05 | Lectura: conducta y suerte | 3.8 Visor de torneo | RF-16 | 8 |
| RF-VTR-06 | Pestañas por torneo en la ventana T+30 | 3.8 Visor de torneo | RF-16 | 5 |
| RF-VTR-07 | Pantalla de la ventana T+30 | 3.8 Visor de torneo | RF-16 | 9 |
| | **3.9 Visor de mano** | | | |
| RF-VMA-01 | Datos de la mano | 3.9 Visor de mano | RF-17 | 4 |
| RF-VMA-02 | Secuencia de apuestas | 3.9 Visor de mano | RF-17 | 3 |
| RF-VMA-03 | Contexto conductual de la mano | 3.9 Visor de mano | RF-17 | 3 |
| RF-VMA-04 | Navegación secuencial | 3.9 Visor de mano | RF-17 | 3 |
| RF-VMA-05 | Diagnóstico comunitario | 3.9 Visor de mano | RF-17 | 4 |
| RF-VMA-06 | Apertura desde una alerta | 3.9 Visor de mano | RF-17 | 3 |
| | **3.10 Etiquetado colaborativo Nivel 2** | | | |
| RF-ETQ-01 | Catálogo de etiquetas | 3.10 Etiquetado colaborativo Nivel 2 | RF-18 | 3 |
| RF-ETQ-02 | Etiquetado de una mano | 3.10 Etiquetado colaborativo Nivel 2 | RF-18 | 4 |
| RF-ETQ-03 | Validación humana de etiquetas | 3.10 Etiquetado colaborativo Nivel 2 | RF-18 | 3 |
| RF-ETQ-04 | Ponderación de etiquetas | 3.10 Etiquetado colaborativo Nivel 2 | RF-18 | 3 |
| RF-ETQ-05 | Entrenamiento del clasificador | 3.10 Etiquetado colaborativo Nivel 2 | RF-18 | 3 |
| RF-ETQ-06 | Aislamiento del Nivel 1 | 3.10 Etiquetado colaborativo Nivel 2 | RF-18 | 3 |
| RF-ETQ-07 | Consentimiento y privacidad | 3.10 Etiquetado colaborativo Nivel 2 | RF-18 | 4 |
| | **3.11 Glosario y ayuda contextual** | | | |
| RF-GLO-01 | Consulta del glosario | 3.11 Glosario y ayuda contextual | RF-19 | 4 |
| RF-GLO-02 | Enlace contextual al glosario | 3.11 Glosario y ayuda contextual | RF-19 | 3 |
| | **3.12 Cuenta, registro, sesión y configuración** | | | |
| RF-CUE-01 | Registro y autenticación | 3.12 Cuenta, registro, sesión y configuración | RF-20 | 8 |
| RF-CUE-02 | Drawer de cuenta | 3.12 Cuenta, registro, sesión y configuración | RF-20 | 3 |
| RF-CUE-03 | Configuración del motor | 3.12 Cuenta, registro, sesión y configuración | RF-20 | 5 |
| RF-CUE-04 | Aislamiento por usuario, sitio y formato | 3.12 Cuenta, registro, sesión y configuración | RF-20 | 4 |
| RF-CUE-05 | Cierre de sesión | 3.12 Cuenta, registro, sesión y configuración | RF-20 | 2 |
| | **3.13 Comparativa Baseline vs Tilt (T+30)** | | | |
| RF-CMP-01 | Acceso y alcance de la comparativa | 3.13 Comparativa Baseline vs Tilt (T+30) | RF-21 | 6 |
| RF-CMP-02 | Métricas y contraste estadístico | 3.13 Comparativa Baseline vs Tilt (T+30) | RF-21 | 6 |
| RF-CMP-03 | Indicadores y lectura de la comparativa | 3.13 Comparativa Baseline vs Tilt (T+30) | RF-21 | 4 |

## 3. Ajustes respecto al mapa inicial

El mapa inicial asignaba RF-DSH-07 a RF-13 y RF-DSH-09 a RF-14. La redacción final de los flujos aconseja dos ajustes para evitar duplicidades:

- **RF-DSH-07**: Se integra en RF-14 porque el resumen del lote se presenta junto al feed del último lote, no en el bloque de KPIs y fatiga.
- **RF-DSH-09**: Se integra en RF-20 para no duplicar la configuración de cuenta que ya cubren RF-CUE-02 y RF-CUE-03.

## 4. Cómo se usa esta matriz

Cada fila de la matriz identifica la ficha interna que origina uno o varios pasos del flujo normal, del flujo alternativo o de las postcondiciones del RF correspondiente. Los criterios de la ficha se conservan íntegros en `docs/entrega/Requisitos-Funcionales-TFG.docx`, que pasa a ser el documento interno de detalle. La memoria oficial solo incluye los 21 RF, los 12 RNF y las 16 entidades de almacenamiento.

## 5. Diagramas de secuencia de 7.1.6

Los tres diagramas de la memoria oficial cubren los flujos de extremo a extremo. Esta tabla indica qué RF ilustra cada uno.

| Ilustración | Flujo | RF cubiertos |
|---:|---|---|
| 2 | Importación y procesamiento del lote | RF-01 a RF-06 y RF-08 a RF-12 |
| 3 | Auditoría de una alerta | RF-14, RF-16, RF-17 y RF-18 |
| 4 | Cálculo del baseline y detección | RF-06 a RF-12 |
