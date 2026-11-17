#!/usr/bin/env python3
"""Genera el documento de entrega de requisitos funcionales en formato .docx."""

from __future__ import annotations

from pathlib import Path

from docx_builder import (
    BRAND,
    BRAND_LIGHT,
    LABEL_FILL,
    MUTED,
    ZEBRA,
    DocxBuilder,
    para,
    page_break,
    run,
    spacer,
    table,
    tc,
    tr,
)

OUT = Path(__file__).resolve().parents[1] / "docs" / "entrega" / "Requisitos-Funcionales-TFG.docx"

doc = DocxBuilder()


# ---------------------------------------------------------------------------
# Utilidades de composición
# ---------------------------------------------------------------------------

def h1(text: str) -> None:
    doc.add(para(run(text), style="Heading1"))


def h2(text: str) -> None:
    doc.add(para(run(text), style="Heading2"))


def h3(text: str) -> None:
    doc.add(para(run(text), style="Heading3"))


def body(text: str) -> None:
    doc.add(para(run(text, size=10.5)))


def intro(text: str) -> None:
    doc.add(para(run(text), style="SectionIntro"))


def bullet(text: str) -> None:
    doc.add(
        para(
            run("•  ", bold=True, color=BRAND, size=10.5) + run(text, size=10.5),
            left=300,
            hanging=200,
            after=50,
        )
    )


def note(title: str, text: str) -> None:
    """Recuadro informativo de una sola celda."""
    content = (
        para(run(title.upper(), bold=True, color=BRAND, size=8), after=40)
        + para(run(text, size=9.5), style="CardText", after=0)
    )
    doc.add(table([tr([tc(content, 9000, fill=LABEL_FILL)])], [9000]))
    doc.add(spacer(100))


def criteria_xml(items: list[str]) -> str:
    out = []
    for i, item in enumerate(items):
        out.append(
            para(
                run(f"{chr(97 + i)}) ", bold=True, color=BRAND, size=9.5)
                + run(item, size=9.5),
                style="CardText",
                left=280,
                hanging=220,
                after=40,
            )
        )
    return "".join(out)


def text_xml(text: str) -> str:
    return para(run(text, size=9.5), style="CardText", after=0)


def label_cell(label: str, width: int = 1700) -> str:
    content = para(run(label.upper(), bold=True, color=MUTED, size=8), after=0)
    return tc(content, width, fill=LABEL_FILL)


def req_card(req: dict) -> None:
    header = para(
        run(f"{req['id']} · {req['title']}", bold=True, color="FFFFFF", size=11),
        after=30,
    ) + para(
        run(f"Prioridad {req['priority'].lower()}  ·  {req['module']}", color="D9E2F3", size=8),
        after=0,
    )
    rows = [tr([tc(header, 9000, span=2, fill=BRAND)], header=True)]
    rows.append(tr([label_cell("Descripción"), tc(text_xml(req["desc"]), 7300)]))
    rows.append(tr([label_cell("Actor"), tc(text_xml(req["actor"]), 7300)]))
    rows.append(tr([label_cell("Precondiciones"), tc(text_xml(req["pre"]), 7300)]))
    rows.append(tr([label_cell("Criterios de aceptación"), tc(criteria_xml(req["crit"]), 7300)]))
    doc.add(table(rows, [1700, 7300]))
    doc.add(spacer(90))


def nfr_card(item: dict) -> None:
    header = para(
        run(f"{item['id']} · {item['title']}", bold=True, color="FFFFFF", size=11),
        after=30,
    ) + para(run(f"Categoría: {item['category']}", color="D9E2F3", size=8), after=0)
    rows = [tr([tc(header, 9000, span=2, fill=BRAND_LIGHT)], header=True)]
    rows.append(tr([label_cell("Descripción"), tc(text_xml(item["desc"]), 7300)]))
    rows.append(tr([label_cell("Criterio medible"), tc(criteria_xml(item["crit"]), 7300)]))
    rows.append(tr([label_cell("Verificación"), tc(text_xml(item["verification"]), 7300)]))
    doc.add(table(rows, [1700, 7300]))
    doc.add(spacer(90))


def table_head(cells: list[str], widths: list[int]) -> str:
    tcs = []
    for text, width in zip(cells, widths):
        content = para(run(text.upper(), bold=True, color="FFFFFF", size=8.5), after=0)
        tcs.append(tc(content, width, fill=BRAND))
    return tr(tcs, header=True)


def simple_cell(text: str, width: int, *, bold: bool = False, color: str | None = None) -> str:
    content = para(run(text, bold=bold, color=color, size=8.8), style="TableText", after=0)
    return tc(content, width)


# ---------------------------------------------------------------------------
# Contenido
# ---------------------------------------------------------------------------

SECTIONS: list[tuple[str, str, str, list[dict]]] = [
    (
        "3.1",
        "Importación e ingesta",
        "El jugador incorpora torneos nuevos al sistema. La importación valida los archivos, descarta los torneos ya guardados y crea un lote atómico que se audita contra el baseline activo. No interpreta el contenido de las manos: solo identifica el torneo, cuenta las manos y comprueba el archivo.",
        [
            {
                "id": "RF-ING-01",
                "title": "Acceso a la importación",
                "module": "Importación",
                "priority": "Alta",
                "desc": "El sistema debe ofrecer una pantalla dedicada para importar torneos nuevos, accesible desde la cabecera global y condicionada a la existencia de un baseline activo.",
                "actor": "Jugador",
                "pre": "Sesión iniciada.",
                "crit": [
                    "La acción “+ Importar Manos” está presente en la cabecera de todas las pantallas.",
                    "La acción abre una pantalla completa y no un modal.",
                    "Sin baseline activo, la acción no se muestra y el Dashboard ofrece la guía “Crear baseline”, que lleva a Mi Baseline.",
                    "La pantalla no permite modificar el baseline e incluye un enlace a Mi Baseline.",
                ],
            },
            {
                "id": "RF-ING-02",
                "title": "Carga de archivos",
                "module": "Importación",
                "priority": "Alta",
                "desc": "El sistema debe permitir al jugador incorporar uno o varios archivos .txt de torneos MTT de Winamax mediante selección o arrastre.",
                "actor": "Jugador",
                "pre": "Baseline activo y pantalla de importación abierta.",
                "crit": [
                    "Admite selección múltiple de archivos y arrastrar y soltar.",
                    "Acepta únicamente archivos con extensión .txt.",
                    "Asocia cada archivo a un torneo.",
                    "No impone límite de número de archivos ni de tamaño por lote.",
                    "Muestra los archivos cargados en una lista con su estado.",
                    "El jugador puede quitar un archivo de la lista antes de confirmar y el sistema actualiza la lista.",
                    "No incorpora ningún dato al sistema hasta que el jugador confirma el procesamiento.",
                ],
            },
            {
                "id": "RF-ING-03",
                "title": "Validación de archivos",
                "module": "Importación",
                "priority": "Alta",
                "desc": "El sistema debe validar cada archivo antes de procesarlo y separar los válidos de los inválidos.",
                "actor": "Sistema",
                "pre": "Al menos un archivo cargado.",
                "crit": [
                    "Comprueba que el contenido corresponde a un historial de Winamax.",
                    "Rechaza los archivos vacíos o ilegibles.",
                    "Obtiene el identificador de torneo del nombre del archivo y el número de manos de cada archivo válido.",
                    "Detecta el tamaño de mesa y la recompensa (ninguna, KO o Mystery) de cada torneo, sin guardar importes.",
                    "Explica cada archivo inválido en una ventana emergente de error con su motivo.",
                    "Si hay archivos inválidos, pregunta al jugador si continúa con los válidos o cancela el lote.",
                ],
            },
            {
                "id": "RF-ING-04",
                "title": "Detección de torneos duplicados",
                "module": "Importación",
                "priority": "Alta",
                "desc": "El sistema debe impedir que se incorpore un torneo que ya está guardado o que es anterior al final del baseline activo.",
                "actor": "Sistema",
                "pre": "Archivo validado.",
                "crit": [
                    "Compara el identificador de torneo y no el contenido de las manos.",
                    "Un torneo ya existente no se procesa.",
                    "Informa del duplicado en una ventana emergente de error.",
                    "El torneo duplicado no consume análisis ni altera los datos existentes.",
                    "Un torneo que empieza antes de la última mano del baseline activo tampoco se procesa, para evitar fuga de datos: se informa con un aviso, que no es un error, y el lote continúa con los demás.",
                    "Si no queda ningún torneo nuevo, no se crea lote y se avisa al jugador.",
                ],
            },
            {
                "id": "RF-ING-05",
                "title": "Resumen previo del lote",
                "module": "Importación",
                "priority": "Media",
                "desc": "El sistema debe mostrar antes de procesar qué torneos se van a importar.",
                "actor": "Jugador",
                "pre": "Al menos un archivo válido y no duplicado.",
                "crit": [
                    "Muestra cuatro cifras: archivos cargados, manos detectadas, sesiones y torneos.",
                    "Las cifras contabilizan solo los torneos que se van a procesar.",
                    "El número de sesiones se calcula antes de procesar aplicando la definición de sesión del Session Builder a las manos del lote, sin consultar datos ya importados.",
                    "La cifra se etiqueta «Sesiones del lote» y no representa el total global tras la fusión.",
                    "El resumen se actualiza al añadir o quitar archivos.",
                    "Consultar el resumen no crea lote ni modifica datos.",
                ],
            },
            {
                "id": "RF-ING-06",
                "title": "Confirmación y procesamiento atómico",
                "module": "Importación",
                "priority": "Alta",
                "desc": "El sistema debe procesar y auditar el lote confirmado por el jugador contra el baseline activo.",
                "actor": "Jugador y sistema",
                "pre": "Resumen previo con al menos un torneo nuevo.",
                "crit": [
                    "El botón “Procesar y auditar el lote” se habilita cuando hay al menos un torneo nuevo.",
                    "“Cancelar la importación” actúa solo antes de procesar y no deja rastro.",
                    "Mientras el lote se procesa, la pantalla queda bloqueada con el progreso visible.",
                    "El lote es atómico: si un torneo falla, no se guarda ninguno.",
                    "Al confirmar se crea un lote persistente con identificador, fecha y hora UTC, torneos, manos, sesiones del lote y periodo cubierto.",
                    "El procesamiento lanza la auditoría del Nivel 1 contra el baseline activo.",
                ],
            },
            {
                "id": "RF-ING-07",
                "title": "Resultado, errores y destino",
                "module": "Importación",
                "priority": "Alta",
                "desc": "El sistema debe informar del resultado del lote y situar al jugador en la pantalla correspondiente.",
                "actor": "Sistema",
                "pre": "Lote procesado o interrumpido por un fallo.",
                "crit": [
                    "Si el lote termina correctamente, se abre el Dashboard con el lote cargado.",
                    "Si el lote falla, no se guarda ningún torneo ni se crea lote.",
                    "Tras un fallo, el jugador permanece en la pantalla de importación con el error y la opción de reintentar.",
                    "Los errores se muestran en una ventana emergente con su causa.",
                    "El resultado conserva el estado de cada torneo.",
                ],
            },
        ],
    ),
    (
        "3.2",
        "Parser y normalización",
        "El parser transforma cada archivo en registros canónicos de mano. Identifica el torneo y la mano, reconstruye las acciones, calcula el resultado y el EV, y expresa todos los importes en ciegas grandes. La normalización se hace con la ciega grande de cada mano, no con la del torneo.",
        [
            {
                "id": "RF-PAR-01",
                "title": "Identificación del torneo y de la mano",
                "module": "Parser ETL",
                "priority": "Alta",
                "desc": "El sistema debe obtener el torneo del nombre del archivo y asignar identidad única a cada mano.",
                "actor": "Sistema",
                "pre": "Archivo validado por la importación.",
                "crit": [
                    "Lee el identificador de torneo del patrón `YYYYMMDD_<nombre>(<id>)_real_holdem_no-limit.txt`.",
                    "Comprueba que coincide con el identificador del nombre de la mesa; si no coincide, rechaza el archivo.",
                    "La mesa solo se usa para esa comprobación: no se modela como entidad ni como dimensión de análisis.",
                    "Identifica cada mano por su HandId completo.",
                    "Conserva el número de mano original de Winamax.",
                    "Asigna un índice secuencial propio desde 1 por torneo.",
                    "Dos manos con el mismo HandId son la misma mano.",
                ],
            },
            {
                "id": "RF-PAR-02",
                "title": "Metadatos del torneo",
                "module": "Parser ETL",
                "priority": "Alta",
                "desc": "El sistema debe construir la ficha del torneo a partir de las manos que contiene.",
                "actor": "Sistema",
                "pre": "Manos identificadas.",
                "crit": [
                    "Registra nombre e identificador del torneo.",
                    "Registra fecha y hora UTC de la primera y de la última mano.",
                    "Registra ciegas y nivel de cada mano.",
                    "Registra el número máximo de jugadores de la mesa.",
                    "No guarda buy-in, fee, bounty ni rake.",
                    "Acepta torneos que empiezan en cualquier número de mano.",
                ],
            },
            {
                "id": "RF-PAR-03",
                "title": "Jugadores, asientos y posición",
                "module": "Parser ETL",
                "priority": "Alta",
                "desc": "El sistema debe reconstruir quién está en la mesa, con cuántas fichas y en qué posición.",
                "actor": "Sistema",
                "pre": "Metadatos de la mano extraídos.",
                "crit": [
                    "Registra nombre y asiento de cada jugador.",
                    "Registra el stack al inicio de cada mano.",
                    "Obtiene el botón de la línea de mesa.",
                    "Calcula la posición relativa de cada jugador: BTN, SB, BB, UTG y siguientes.",
                    "Identifica al héroe por la línea `Dealt to`.",
                    "Registra las cartas del héroe.",
                    "Admite nombres con espacios, puntos, guiones y guiones bajos.",
                    "Admite cambios de jugadores y de stacks entre manos.",
                ],
            },
            {
                "id": "RF-PAR-04",
                "title": "Secuencia de acciones por calle",
                "module": "Parser ETL",
                "priority": "Alta",
                "desc": "El sistema debe reconstruir la mano calle por calle, en orden.",
                "actor": "Sistema",
                "pre": "Jugadores y posiciones identificados.",
                "crit": [
                    "Ordena ante y ciegas, preflop, flop, turn y river.",
                    "Registra `fold`, `check`, `call`, `bet`, `raise` y all-in.",
                    "Interpreta `raises X to Y` como importe total Y.",
                    "Marca el all-in en `call`, `bet` y `raise`.",
                    "Calcula el bote acumulado al cierre de cada calle.",
                    "Comprueba que la suma de aportaciones coincide con el bote del sumario.",
                ],
            },
            {
                "id": "RF-PAR-05",
                "title": "Botes, showdown y side pots",
                "module": "Parser ETL",
                "priority": "Alta",
                "desc": "El sistema debe determinar cuánto se juega, quién lo gana y cómo se reparte.",
                "actor": "Sistema",
                "pre": "Secuencia de acciones reconstruida.",
                "crit": [
                    "Detecta el showdown y las cartas mostradas.",
                    "Reconstruye el bote principal y cada side pot.",
                    "Interpreta `collected` como cantidad cobrada, que incluye la aportación propia.",
                    "Admite el reparto por empate.",
                    "Usa `Total pot` del sumario como validación.",
                    "Registra ganadores y descripción de la mano del sumario.",
                ],
            },
            {
                "id": "RF-PAR-06",
                "title": "Normalización a ciegas grandes",
                "module": "Normalización",
                "priority": "Alta",
                "desc": "El sistema debe expresar todos los importes en ciegas grandes usando la ciega grande de cada mano.",
                "actor": "Sistema",
                "pre": "Acciones y botes reconstruidos.",
                "crit": [
                    "Lee `(ante/sb/bb)` de la cabecera de cada mano.",
                    "Usa la ciega grande de esa mano para toda conversión, no la del torneo ni la inicial.",
                    "Guarda el nivel de ciegas (ante, SB y BB) en fichas como contexto de la mano.",
                    "Guarda apuestas, botes, stacks, resultado y EV en BB.",
                    "No duplica cada importe en fichas: se deriva multiplicando por la ciega grande.",
                    "Guarda los valores en BB con cuatro decimales.",
                    "Admite una tolerancia de 0,001 BB al comprobar que las aportaciones cuadran con el bote.",
                ],
            },
            {
                "id": "RF-PAR-07",
                "title": "Resultado real y EV del all-in",
                "module": "Parser ETL",
                "priority": "Alta",
                "desc": "El sistema debe calcular el resultado real de la mano y el resultado esperado de los all-in.",
                "actor": "Sistema",
                "pre": "Acciones y botes normalizados.",
                "crit": [
                    "Calcula el resultado real como cantidad cobrada menos aportación total, incluidas antes y ciegas.",
                    "En un all-in con showdown y cartas conocidas, calcula la equidad.",
                    "Reparte el bote por capas y suma la parte esperada del héroe en cada una, incluidos los side pots.",
                    "Guarda equidad, bote, EV y número de jugadores implicados.",
                    "En manos sin all-in, el EV coincide con el resultado real.",
                    "Solo ajusta manos en las que participa el héroe.",
                    "Usa una semilla fija para que el resultado sea reproducible.",
                    "Calcula el EV al importar y lo guarda con la mano.",
                    "La equidad se calcula en la ingesta, antes de guardar la mano, y queda vacía si no hay all-in.",
                    "Acumula por torneo las BB ganadas, el All-in EV y la suerte esperable en los all-in (σ), y clasifica la suerte del torneo como a favor, neutra o en contra.",
                ],
            },
            {
                "id": "RF-PAR-08",
                "title": "Métricas de conducta",
                "module": "Parser ETL",
                "priority": "Alta",
                "desc": "El sistema debe calcular las cinco métricas de conducta del héroe con su numerador y denominador.",
                "actor": "Sistema",
                "pre": "Acciones, botes y resultado calculados.",
                "crit": [
                    "VPIP: manos con dinero voluntario preflop entre manos jugadas; excluye ciegas y antes.",
                    "PFR: manos con subida preflop entre manos jugadas.",
                    "3-Bet: subidas sobre una subida entre oportunidades de 3-bet.",
                    "Fold vs 3-Bet: retiradas ante un 3-bet entre las veces que lo afronta.",
                    "WTSD: manos que llegan a showdown entre manos que vieron flop.",
                    "Cada métrica guarda numerador y denominador.",
                    "Solo se calculan sobre manos del héroe.",
                ],
            },
            {
                "id": "RF-PAR-09",
                "title": "Registro canónico e integridad",
                "module": "Parser ETL",
                "priority": "Alta",
                "desc": "El sistema debe producir un registro único por mano, completo y validado.",
                "actor": "Sistema",
                "pre": "Metadatos, acciones, métricas y EV calculados.",
                "crit": [
                    "Un registro por mano con metadatos, jugadores, acciones, botes, resultado, EV y métricas.",
                    "El registro contiene todo lo necesario para reconstruir la mano en el visor.",
                    "Valida la coherencia de cartas, aportaciones, botes y showdown.",
                    "Si una mano no se puede interpretar, rechaza el archivo completo e indica la línea exacta.",
                    "El registro es inmutable y guarda la versión del parser.",
                    "Procesar dos veces el mismo archivo produce el mismo registro.",
                ],
            },
        ],
    ),
    (
        "3.3",
        "Session Builder: sesiones y torneos",
        "Las manos se ordenan en una línea temporal única y se agrupan en sesiones según su continuidad. La sesión es la unidad de la fatiga y del baseline; el torneo sigue siendo la unidad de competición.",
        [
            {
                "id": "RF-SES-01",
                "title": "Línea temporal global de manos",
                "module": "Session Builder",
                "priority": "Alta",
                "desc": "El sistema debe ordenar todas las manos del jugador en una línea temporal única.",
                "actor": "Sistema",
                "pre": "Manos normalizadas y registradas.",
                "crit": [
                    "Ordena todas las manos por fecha y hora UTC.",
                    "Desempata por HandId cuando dos manos comparten el mismo segundo.",
                    "La línea temporal es única por jugador, sitio y formato.",
                    "Cada mano aparece una sola vez.",
                    "Intercala manos de torneos distintos cuando se juegan en paralelo.",
                    "El orden no depende del orden de importación.",
                ],
            },
            {
                "id": "RF-SES-02",
                "title": "Delimitación de sesiones",
                "module": "Session Builder",
                "priority": "Alta",
                "desc": "El sistema debe agrupar la línea temporal en sesiones según su continuidad.",
                "actor": "Sistema",
                "pre": "Línea temporal construida.",
                "crit": [
                    "Una pausa estrictamente mayor que el umbral entre dos manos consecutivas inicia una sesión nueva.",
                    "El umbral es de 30 minutos y se define en la sección 8.",
                    "Las manos de torneos simultáneos o solapados pertenecen a la misma sesión.",
                    "Todas las manos de un torneo pertenecen a la misma sesión.",
                    "Una sesión puede contener varios torneos y un torneo puede compartir sesión con otros.",
                    "La agrupación no usa el día natural ni la fecha de importación.",
                    "La sesión se identifica por su primera mano.",
                ],
            },
            {
                "id": "RF-SES-03",
                "title": "Metadatos y rendimiento de la sesión",
                "module": "Session Builder",
                "priority": "Media",
                "desc": "El sistema debe calcular y conservar los datos que describen cada sesión.",
                "actor": "Sistema",
                "pre": "Sesiones delimitadas.",
                "crit": [
                    "Inicio: fecha y hora de la primera mano; fin: fecha y hora de la última.",
                    "Duración: fin menos inicio, guardada en minutos y mostrada en horas y minutos; 0 si solo hay una mano.",
                    "Número de manos y de torneos.",
                    "Resultado neto en BB: suma de net_bb de las manos.",
                    "EV en BB: suma de ev_bb de las manos.",
                    "BB/100: 100 × resultado neto / manos.",
                    "EVbb/100: 100 × EV / manos.",
                    "Sitio y formato.",
                    "No guarda datos económicos.",
                    "Los agregados alimentan el baseline, la gráfica de fatiga y el historial.",
                ],
            },
            {
                "id": "RF-SES-04",
                "title": "Sesiones del lote y recálculo global",
                "module": "Session Builder",
                "priority": "Alta",
                "desc": "El sistema debe calcular las sesiones del lote antes de procesar y recalcularlas sobre la línea global al incorporar las manos.",
                "actor": "Sistema",
                "pre": "Lote confirmado y manos registradas.",
                "crit": [
                    "El resumen previo calcula las sesiones del lote en aislamiento, sin consultar manos ya guardadas.",
                    "La cifra se etiqueta «Sesiones del lote» y no representa el total global tras la fusión.",
                    "Al procesar, las manos se incorporan a la línea temporal global y las sesiones se recalculan sobre todas las manos.",
                    "Si un torneo nuevo elimina el hueco entre dos sesiones, se fusionan en una.",
                    "La sesión fusionada conserva el inicio más antiguo y el fin más reciente.",
                    "El recálculo no modifica manos, torneos, alertas ni snapshots.",
                    "Los snapshots conservan las sesiones con las que se calcularon.",
                    "El recálculo es determinista: el mismo conjunto de manos produce las mismas sesiones.",
                ],
            },
            {
                "id": "RF-SES-05",
                "title": "Coherencia e integridad de las sesiones",
                "module": "Session Builder",
                "priority": "Alta",
                "desc": "El sistema debe garantizar que las sesiones son completas, coherentes y no manipulables.",
                "actor": "Sistema",
                "pre": "Sesiones recalculadas.",
                "crit": [
                    "Toda mano pertenece a exactamente un torneo y una sesión.",
                    "Toda sesión tiene al menos una mano.",
                    "La suma de manos de las sesiones es el total de manos del jugador.",
                    "Las sesiones no se crean, editan ni borran a mano.",
                    "Las sesiones se listan en orden cronológico.",
                    "Si un torneo contiene una pausa interna superior al umbral, el archivo se rechaza y el lote no se procesa.",
                    "El error indica torneo, manos y pausa detectada.",
                ],
            },
        ],
    ),
    (
        "3.4",
        "Baseline individual",
        "El baseline es la referencia estable del jugador. Se calcula con datos anteriores al periodo evaluado, se congela como snapshot y se versiona para que ninguna alerta pasada cambie de significado.",
        [
            {
                "id": "RF-BAS-01",
                "title": "Cálculo del baseline individual",
                "module": "Baseline",
                "priority": "Alta",
                "desc": "El sistema debe calcular el perfil habitual del jugador sobre las manos que componen el baseline.",
                "actor": "Sistema",
                "pre": "Manos normalizadas y agrupadas.",
                "crit": [
                    "Calcula VPIP, PFR, 3-Bet, Fold vs 3-Bet, WTSD y EVbb/100.",
                    "Pondera cada métrica por el número de manos.",
                    "Usa exclusivamente manos anteriores al periodo evaluado.",
                    "Guarda el numerador y el denominador de cada métrica.",
                    "Desglosa VPIP, PFR, 3-Bet, Fold vs 3-Bet y WTSD por tramo de stack (menos de 10 BB, 10–20, 20–40 y 40 BB o más, provisionales) y guarda también el total; el EVbb/100 se guarda solo como total.",
                    "El baseline inicial se crea desde Mi Baseline en estado vacío, con archivos que el jugador arrastra a esa pantalla.",
                    "Los archivos del baseline se procesan como un lote de tipo baseline: solo construyen el perfil y no generan alertas ni aparecen en el Historial ni en los visores.",
                    "El baseline inicial excluye las ventanas T+30 de los triggers, que se detectan sin baseline; los tramos de desviación no se excluyen porque aún no hay baseline con el que contrastarlos.",
                ],
            },
            {
                "id": "RF-BAS-02",
                "title": "Congelación y versionado del baseline",
                "module": "Baseline",
                "priority": "Alta",
                "desc": "El sistema debe conservar cada baseline como un snapshot inmutable y versionado.",
                "actor": "Sistema",
                "pre": "Baseline calculado.",
                "crit": [
                    "Cada baseline se guarda con identificador, fecha de congelación y versión.",
                    "Registra si el baseline es inicial o recalibrado.",
                    "Guarda de cada versión los torneos que la componen (un archivo es un torneo), el número de sesiones de la muestra, su origen (inicial, añadir, sustituir o recalibrar) y la versión de la que procede.",
                    "Sustituir deja fuera todos los archivos anteriores, sin importar sus fechas; añadir suma los nuevos a los de la versión activa.",
                    "Una versión nueva no modifica las versiones anteriores.",
                    "Añadir archivos y sustituir el baseline crean una versión nueva y archivan la anterior; ninguna versión archivada se modifica ni se borra.",
                    "Añadir muestra antes una vista previa (manos detectadas, total resultante y métricas del archivo) y «Descartar» cancela sin crear versión.",
                    "Sustituir compara el baseline actual con el resultante y, al confirmar, conserva los archivos anteriores.",
                    "Tras añadir o sustituir, «Deshacer» o «Restaurar archivos anteriores» elimina la versión recién creada junto con los archivos, torneos y manos que solo incorporó esa acción, y la versión anterior vuelve a ser la activa.",
                    "Tras deshacer, los archivos subidos por error pueden volver a subirse sin que se detecten como duplicados.",
                    "El aviso solo existe al realizar la acción: al cambiar de pestaña o cerrarlo, ya no se puede volver al baseline anterior por esta vía.",
                    "No se crea ninguna versión con menos de 2.000 manos.",
                    "Cada alerta conserva el identificador del snapshot con el que se calculó.",
                ],
            },
            {
                "id": "RF-BAS-03",
                "title": "Muestra mínima del baseline",
                "module": "Baseline",
                "priority": "Alta",
                "desc": "El sistema debe impedir la creación de un baseline con muestra insuficiente y advertir cuando la muestra es reducida.",
                "actor": "Sistema",
                "pre": "Manos candidatas seleccionadas.",
                "crit": [
                    "Exige un mínimo de 2.000 manos para crear el baseline.",
                    "Si la muestra alcanza las 2.000 manos pero no las 10.000 recomendadas, muestra el aviso “muestra pequeña”.",
                    "No crea un baseline por debajo del mínimo.",
                ],
            },
            {
                "id": "RF-BAS-04",
                "title": "Recalibración del baseline",
                "module": "Baseline",
                "priority": "Alta",
                "desc": "El sistema debe permitir recalcular el baseline excluyendo los tramos de desviación y, mediante dos casillas marcadas por defecto, las ventanas reactivas y la fatiga prolongada del propio jugador.",
                "actor": "Jugador",
                "pre": "Baseline existente y manos nuevas disponibles.",
                "crit": [
                    "Recalcula el baseline con las manos seleccionadas.",
                    "Excluye automáticamente los tramos de desviación.",
                    "Ofrece dos casillas, marcadas por defecto y desmarcables: excluir ventanas T+30 y filtrar fatiga prolongada.",
                    "La fatiga prolongada son las manos jugadas desde el punto crítico de fatiga del propio jugador, no una hora fija.",
                    "Si el jugador no tiene punto crítico, no excluye fatiga aunque la casilla esté marcada y la pantalla lo indica.",
                    "Crea una versión nueva y archiva la anterior.",
                    "No altera las alertas ya emitidas.",
                ],
            },
            {
                "id": "RF-BAS-05",
                "title": "Aviso de obsolescencia",
                "module": "Baseline",
                "priority": "Media",
                "desc": "Fuera del MVP actual. El sistema avisará cuando el baseline acumule suficiente volumen de manos nuevas o tiempo desde su congelación.",
                "actor": "Sistema",
                "pre": "Baseline activo.",
                "crit": [
                    "Evalúa el volumen de manos nuevas y el tiempo desde la congelación.",
                    "Muestra un aviso cuando se supera el umbral, pendiente de definir.",
                    "No recalibra automáticamente.",
                ],
            },
            {
                "id": "RF-BAS-06",
                "title": "Consulta del baseline activo",
                "module": "Baseline",
                "priority": "Alta",
                "desc": "El sistema debe exponer el estado y la composición del baseline activo.",
                "actor": "Jugador",
                "pre": "Baseline existente.",
                "crit": [
                    "Muestra métricas, muestra y fecha de congelación.",
                    "Muestra el número de archivos y de sesiones de la muestra.",
                    "El jugador solo ve el baseline activo: las versiones archivadas se conservan para auditar las alertas y no se consultan desde la interfaz.",
                ],
            },
        ],
    ),
    (
        "3.5",
        "Detección Nivel 1",
        "El motor compara la conducta del jugador contra su baseline y genera evidencia auditable. Distingue ventanas reactivas tras un bad beat, tramos de sobrefrecuencia sin trigger y degradación por fatiga.",
        [
            {
                "id": "RF-DET-01",
                "title": "Detección del trigger de bad beat",
                "module": "Motor Nivel 1",
                "priority": "Alta",
                "desc": "El sistema debe identificar las manos que actúan como trigger de una posible reacción conductual.",
                "actor": "Sistema",
                "pre": "Manos normalizadas y baseline disponible.",
                "crit": [
                    "Detecta los bad beats: all-in perdidos con una equidad igual o superior al 70 %.",
                    "Detecta las pérdidas de bote grande: manos en las que el héroe pierde 40 BB o más, haya habido all-in o no.",
                    "Una mano puede cumplir las dos condiciones y se registra una sola vez con las dos marcas.",
                    "Registra mano, torneo, tipo de trigger, equidad si hubo all-in, bote y resultado.",
                    "Genera como máximo un trigger por mano.",
                ],
            },
            {
                "id": "RF-DET-02",
                "title": "Ventana reactiva T+30",
                "module": "Motor Nivel 1",
                "priority": "Alta",
                "desc": "El sistema debe analizar las 30 manos inmediatamente posteriores a cada trigger en la sesión del jugador, de cualquier torneo, excluyendo la mano trigger.",
                "actor": "Sistema",
                "pre": "Trigger detectado.",
                "crit": [
                    "Excluye la mano trigger del análisis.",
                    "Analiza las 30 manos siguientes del jugador en su sesión, de cualquier torneo, ordenadas por hora.",
                    "Trunca la ventana al final de la sesión (pausa de más de 30 minutos).",
                    "Fusiona ventanas solapadas, aunque los triggers sean de torneos distintos, y cuenta las manos compartidas una sola vez.",
                    "Si no hay manos posteriores en la sesión, no hay ventana ni alerta; el trigger se muestra en el visor con la nota «sin manos posteriores».",
                    "Si la ventana tiene menos de la mitad de las manos configuradas, queda sin datos suficientes y ninguna métrica se contrasta; con más de la mitad pero menos de las configuradas, se analiza y se marca como incompleta.",
                    "La alerta pertenece al torneo del trigger; los demás torneos con manos de la ventana solo llevan una marca informativa.",
                ],
            },
            {
                "id": "RF-DET-03",
                "title": "Métricas de la ventana reactiva",
                "module": "Motor Nivel 1",
                "priority": "Alta",
                "desc": "El sistema debe medir la conducta observada en la ventana y compararla con el baseline.",
                "actor": "Sistema",
                "pre": "Ventana T+30 construida.",
                "crit": [
                    "Calcula VPIP, PFR, 3-Bet, Fold vs 3-Bet, WTSD y EVbb/100 de la ventana.",
                    "Determina cuáles de VPIP, PFR y 3-Bet son evaluables: las que alcanzan un mínimo de oportunidades igual a la mitad de las habituales del jugador en ese número de manos, según su baseline, con un suelo de 3 (provisional).",
                    "Contrasta contra el baseline activo VPIP, PFR y 3-Bet cuando son evaluables; Fold vs 3-Bet y WTSD se guardan sin contrastarse en la ventana (los contrasta la comparativa); las no evaluables conservan numerador y denominador, sin porcentaje.",
                    "Si ninguna métrica es evaluable, la ventana queda sin datos suficientes: genera una alerta no concluyente, sin fuga neta, y no cuenta como torneo limpio.",
                    "Calcula el esperado de cada mano con el valor del baseline en su tramo de stack y, si ese tramo del baseline tiene menos de 50 oportunidades de la métrica, con el valor total del baseline.",
                    "Obtiene el p-valor con un contraste exacto que admite una probabilidad esperada distinta por mano (Poisson-binomial), en lugar de la binomial con una sola tasa.",
                    "Guarda la diferencia en puntos porcentuales.",
                    "Guarda numerador y denominador de cada métrica, con su desglose por tramo de stack.",
                ],
            },
            {
                "id": "RF-DET-04",
                "title": "Detección de desviaciones sin trigger",
                "module": "Motor Nivel 1",
                "priority": "Alta",
                "desc": "El sistema debe detectar tramos de conducta sostenidamente distinta al baseline sin necesidad de un trigger.",
                "actor": "Sistema",
                "pre": "Manos normalizadas y baseline disponible.",
                "crit": [
                    "Aplica una ventana deslizante sobre la serie temporal.",
                    "Contrasta localmente acciones frente a oportunidades en VPIP, PFR y 3-Bet, con el esperado de cada mano según su tramo de stack y el mismo contraste exacto que la ventana T+30; solo se contrastan las métricas evaluables y la corrección FDR se aplica solo a esas pruebas.",
                    "Calcula el q-value de cada prueba.",
                    "Registra el inicio y el fin del tramo candidato.",
                ],
            },
            {
                "id": "RF-DET-05",
                "title": "Fusión de intervalos anómalos",
                "module": "Motor Nivel 1",
                "priority": "Alta",
                "desc": "El sistema debe consolidar los bloques consecutivos anómalos en un único tramo continuo.",
                "actor": "Sistema",
                "pre": "Bloques anómalos detectados.",
                "crit": [
                    "Fusiona bloques consecutivos separados por menos de 10 manos.",
                    "El tramo fusionado conserva la primera y la última mano.",
                    "Si dos bloques están separados por 10 manos o más, se consideran tramos distintos.",
                ],
            },
            {
                "id": "RF-DET-06",
                "title": "Análisis de fatiga",
                "module": "Motor Nivel 1",
                "priority": "Alta",
                "desc": "El sistema debe medir la evolución del rendimiento esperado a lo largo de las horas de juego continuo.",
                "actor": "Sistema",
                "pre": "Sesiones y manos normalizadas.",
                "crit": [
                    "Calcula el EVbb/100 por tramos de horas de juego.",
                    "Construye tramos de ancho adaptado a las sesiones del baseline, con siempre el mismo número de puntos (por definir), y los fusiona cuando no alcanzan muestra suficiente.",
                    "Calcula la curva con las mismas manos que el baseline (sin ventanas T+30 ni tramos de desviación), salvo la exclusión de fatiga, que no se aplica.",
                    "Guarda con el baseline las horas de inicio y fin de cada tramo (el último, abierto), sus manos, sesiones, suma de EV, EVbb/100 e intervalo de confianza del 95 %, y el punto crítico.",
                    "Localiza el punto de cruce a pérdidas.",
                    "La fatiga se visualiza en la gráfica y no genera alertas en el feed.",
                ],
            },
            {
                "id": "RF-DET-07",
                "title": "Corrección por comparaciones múltiples",
                "module": "Motor Nivel 1",
                "priority": "Alta",
                "desc": "El sistema debe controlar los falsos positivos mediante la corrección de Benjamini-Hochberg.",
                "actor": "Sistema",
                "pre": "Pruebas estadísticas del lote calculadas.",
                "crit": [
                    "Aplica la corrección FDR a las comparaciones del lote.",
                    "Usa un umbral q configurable, con 0,05 como valor por defecto.",
                    "Guarda el q-value de cada prueba.",
                    "Descarta como alerta las pruebas que no superan el umbral.",
                ],
            },
            {
                "id": "RF-DET-08",
                "title": "Generación de alertas",
                "module": "Motor Nivel 1",
                "priority": "Alta",
                "desc": "El sistema debe transformar las detecciones significativas en alertas con evidencia suficiente para su auditoría.",
                "actor": "Sistema",
                "pre": "Detecciones corregidas por FDR.",
                "crit": [
                    "Genera una alerta de tilt por cada ventana T+30 significativa.",
                    "Genera una alerta de desviación por cada tramo significativo.",
                    "Cada alerta guarda tipo, torneo, evidencia, métricas y snapshot.",
                    "Toda alerta nace en estado pendiente.",
                    "La fuga neta se calcula como max(0, (EVbb/100 del baseline − EVbb/100 observado) × manos / 100): el coste en BB de haber jugado distinto al baseline, medido en EV para no atribuir a la conducta la suerte de los all-in. La interfaz la muestra como magnitud positiva en BB.",
                    "Si la ventana no contiene all-in, el EV coincide con el resultado real y la fuga neta se calcula igualmente; si el rendimiento de la ventana iguala o supera el del baseline, vale 0.",
                    "Si no hay EV disponible, la fuga neta queda sin valor y la alerta se muestra igualmente con la indicación «no estimable».",
                ],
            },
        ],
    ),
    (
        "3.6",
        "Dashboard macro",
        "El Dashboard resume el baseline, la fatiga y las alertas del último lote. No juzga el resultado económico: muestra evidencia conductual y separa mala suerte de mal juego.",
        [
            {
                "id": "RF-DSH-01",
                "title": "Resumen del baseline activo",
                "module": "Dashboard",
                "priority": "Alta",
                "desc": "El sistema debe mostrar las métricas principales del baseline activo en el Dashboard.",
                "actor": "Jugador",
                "pre": "Baseline activo.",
                "crit": [
                    "Muestra cuatro indicadores: VPIP, PFR, 3-Bet y Winrate baseline (EV), que es el EVbb/100 con ajuste all-in.",
                    "Los valores proceden del snapshot activo.",
                    "Muestra la muestra y la fecha de congelación.",
                    "VPIP incluye una referencia poblacional para MTT.",
                ],
            },
            {
                "id": "RF-DSH-02",
                "title": "Presentación del EVbb/100",
                "module": "Dashboard",
                "priority": "Alta",
                "desc": "El sistema debe presentar el rendimiento esperado con ajuste all-in y explicar su alcance.",
                "actor": "Jugador",
                "pre": "Baseline activo.",
                "crit": [
                    "El valor principal es EVbb/100, rotulado «Winrate baseline (EV)», con un ⓘ que explica el ajuste all-in por equidad.",
                    "En manos con all-in usa el EV esperado; en el resto, el resultado real.",
                ],
            },
            {
                "id": "RF-DSH-03",
                "title": "Gráfica de fatiga",
                "module": "Dashboard",
                "priority": "Alta",
                "desc": "El sistema debe representar la degradación del rendimiento esperado a lo largo de las horas de sesión.",
                "actor": "Jugador",
                "pre": "Baseline activo con sesiones suficientes.",
                "crit": [
                    "Representa los tramos con línea o barras sin alterar los datos.",
                    "Mantiene el cero visible y etiquetado como break-even.",
                    "Marca el punto crítico cuando hay cruce a pérdidas.",
                    "El tooltip muestra tramo, EVbb/100, manos, sesiones e intervalo de confianza.",
                    "Sin baseline o sin sesiones, muestra el estado de inicio con la guía “Crear baseline”, que lleva a Mi Baseline.",
                    "Con baseline y sin lotes auditados, usa la muestra del baseline y el feed indica que todavía no hay casos que auditar.",
                ],
            },
            {
                "id": "RF-DSH-04",
                "title": "Feed de alertas del último lote",
                "module": "Dashboard",
                "priority": "Alta",
                "desc": "El sistema debe listar todas las alertas y desviaciones del último lote importado.",
                "actor": "Jugador",
                "pre": "Lote importado y analizado.",
                "crit": [
                    "Muestra únicamente alertas del último lote.",
                    "Muestra todas las alertas del lote en un feed desplazable.",
                    "Ordena primero las alertas concluyentes y después las no concluyentes.",
                    "Dentro de cada grupo, ordena primero las alertas de tilt y después las desviaciones.",
                    "Dentro de cada tipo, ordena por solidez (más métricas evaluables primero), después por magnitud de fuga y, a igualdad, por fecha.",
                    "Cada métrica muestra numerador y denominador; la que no alcanza su mínimo de oportunidades se muestra como «k de n» marcada como no evaluable, sin porcentaje.",
                    "Una ventana sin datos suficientes aparece como alerta no concluyente, sin fuga neta y con el aviso de que no se puede evaluar.",
                ],
            },
            {
                "id": "RF-DSH-05",
                "title": "Tarjeta de evidencia de la alerta",
                "module": "Dashboard",
                "priority": "Alta",
                "desc": "El sistema debe presentar cada alerta con la evidencia mínima para decidir su auditoría.",
                "actor": "Jugador",
                "pre": "Alerta pendiente.",
                "crit": [
                    "Muestra tipo, torneo, trigger o métrica, ventana o tramo, valor observado, baseline y delta.",
                    "Muestra la fuga neta estimada, como magnitud positiva en BB.",
                    "Cada alerta tiene su propia tarjeta.",
                    "Solo el botón “Auditar” es clicable.",
                ],
            },
            {
                "id": "RF-DSH-06",
                "title": "Auditoría de una alerta",
                "module": "Dashboard",
                "priority": "Alta",
                "desc": "El sistema debe abrir la evidencia exacta de una alerta, retirarla del feed y conservarla en el historial.",
                "actor": "Jugador",
                "pre": "Alerta pendiente.",
                "crit": [
                    "Una alerta de tilt abre el visor en la mano trigger.",
                    "Una alerta de desviación abre el visor en la primera mano del tramo.",
                    "Al abrir el visor, la alerta pasa a auditada y desaparece del feed.",
                    "La cabecera del feed muestra un contador «n de m auditadas» con las alertas concluyentes del último lote.",
                    "La alerta se conserva en el historial.",
                ],
            },
            {
                "id": "RF-DSH-07",
                "title": "Resumen y origen del lote",
                "module": "Dashboard",
                "priority": "Media",
                "desc": "El sistema debe contextualizar el lote con su magnitud, procedencia y periodo.",
                "actor": "Jugador",
                "pre": "Lote importado.",
                "crit": [
                    "Muestra el número de torneos del lote.",
                    "Muestra los torneos con al menos una alerta de tilt o desviación; la fatiga no cuenta.",
                    "Muestra el porcentaje de manos dentro de ventanas T+30, con absoluto y denominador.",
                    "Muestra torneos, manos, fecha de carga y periodo cubierto.",
                    "Las fechas se guardan en UTC y se muestran en la zona local.",
                ],
            },
            {
                "id": "RF-DSH-08",
                "title": "Shell y navegación global",
                "module": "Dashboard",
                "priority": "Alta",
                "desc": "El sistema debe ofrecer una cabecera común con la navegación y las acciones globales del producto.",
                "actor": "Jugador",
                "pre": "Sesión iniciada.",
                "crit": [
                    "La cabecera permanece visible durante el scroll y está presente en todas las pantallas.",
                    "El logo devuelve al Dashboard.",
                    "La navegación incluye Historial Torneos, Baseline, Baseline vs Tilt (T+30) y Glosario.",
                    "El ítem activo se marca fuera del Dashboard.",
                    "La cabecera incluye “+ Importar Manos” y el botón de cuenta.",
                    "El diseño es desktop-first y se valida desde 1280×720.",
                ],
            },
            {
                "id": "RF-DSH-09",
                "title": "Cuenta y configuración del motor",
                "module": "Dashboard",
                "priority": "Media",
                "desc": "El sistema debe permitir consultar la cuenta y ajustar la configuración del motor desde cualquier pantalla.",
                "actor": "Jugador",
                "pre": "Sesión iniciada.",
                "crit": [
                    "El drawer de cuenta muestra usuario, sitio activo, estado y nivel de juego.",
                    "La ventana reactiva se configura entre T+20, T+30, T+50 y T+100.",
                    "La sensibilidad FDR se configura entre q < 0,10, q < 0,05 y q < 0,01.",
                    "Los cambios se guardan de forma explícita y afectan únicamente al siguiente lote.",
                    "Si se cierra con cambios sin guardar, se pide confirmación.",
                ],
            },
            {
                "id": "RF-DSH-10",
                "title": "Estados, avisos y accesibilidad",
                "module": "Dashboard",
                "priority": "Media",
                "desc": "El sistema debe informar de las acciones y de los estados de cada bloque sin ocultar información relevante.",
                "actor": "Sistema",
                "pre": "Uso normal del Dashboard.",
                "crit": [
                    "Cada bloque tiene estados de vacío, carga, error, parcial y sin permisos.",
                    "Un error en un bloque no impide el funcionamiento del resto.",
                    "Los toasts de éxito se cierran solos; los errores permanecen hasta que el usuario los cierra.",
                    "Estados y alertas combinan color, icono y texto.",
                    "El contraste cumple WCAG AA, con un mínimo de 4,5:1 en texto normal.",
                ],
            },
        ],
    ),
    (
        "3.7",
        "Historial de torneos",
        "El historial conserva todos los torneos procesados y permite localizar torneos limpios, alertas de tilt y desviaciones.",
        [
            {
                "id": "RF-HIS-01",
                "title": "Listado de torneos",
                "module": "Historial",
                "priority": "Alta",
                "desc": "El sistema debe listar los torneos procesados con la información necesaria para compararlos.",
                "actor": "Jugador",
                "pre": "Al menos un lote importado.",
                "crit": [
                    "Cada fila muestra torneo, fecha, manos, BB ganadas, All-in EV, suerte all-in, estado conductual y acción.",
                    "BB ganadas y All-in EV se muestran en verde si son positivas y en rojo si son negativas; la suerte all-in (a favor, neutra o en contra) se muestra sin color.",
                    "Las cabeceras de BB ganadas, All-in EV y suerte all-in ofrecen un ⓘ con definición breve y el enlace «Ver en el Glosario».",
                    "El listado no muestra VPIP ni PFR por torneo.",
                    "El orden por defecto es por fecha descendente.",
                    "El listado se pagina cuando supera el tamaño de página.",
                    "Hasta que se audita el primer lote, el acceso al Historial está desactivado.",
                ],
            },
            {
                "id": "RF-HIS-02",
                "title": "Filtros del historial",
                "module": "Historial",
                "priority": "Alta",
                "desc": "El sistema debe permitir filtrar el historial por los criterios relevantes para la revisión.",
                "actor": "Jugador",
                "pre": "Listado de torneos disponible.",
                "crit": [
                    "Filtra por estado conductual: tilt, desviación o torneo limpio.",
                    "Filtra por periodo.",
                    "Filtra por tamaño de mesa (por ejemplo 6-max o 3-max).",
                    "Filtra por recompensa del torneo: ninguna, KO o Mystery.",
                    "Los filtros son combinables y se pueden limpiar.",
                ],
            },
            {
                "id": "RF-HIS-03",
                "title": "Estado conductual del torneo",
                "module": "Historial",
                "priority": "Alta",
                "desc": "El sistema debe clasificar cada torneo según la evidencia conductual disponible.",
                "actor": "Sistema",
                "pre": "Torneo analizado.",
                "crit": [
                    "Marca tilt cuando el torneo contiene al menos una alerta de tilt.",
                    "Marca desviación cuando contiene un tramo significativo sin trigger.",
                    "Marca no concluyente cuando contiene alguna ventana sin datos suficientes y ninguna alerta ni tramo significativo.",
                    "Muestra una marca informativa, con enlace a la alerta, en el torneo que contiene manos de la ventana T+30 de otro torneo; esa marca no es una alerta y no permite el torneo limpio.",
                    "Marca torneo limpio cuando no contiene alertas ni tramos ni ventanas sin datos suficientes.",
                    "La prioridad es tilt, después desviación, después no concluyente y después torneo limpio.",
                ],
            },
            {
                "id": "RF-HIS-04",
                "title": "Acceso al visor del torneo",
                "module": "Historial",
                "priority": "Media",
                "desc": "El sistema debe permitir abrir el detalle de cualquier torneo desde el historial.",
                "actor": "Jugador",
                "pre": "Listado de torneos disponible.",
                "crit": [
                    "Al seleccionar una fila se abre el visor del torneo.",
                    "Todos los torneos auditados se pueden abrir, tengan o no alertas, incluidos los no concluyentes y los torneos limpios (M28).",
                    "El visor conserva el contexto del torneo seleccionado.",
                ],
            },
            {
                "id": "RF-HIS-05",
                "title": "Persistencia del historial",
                "module": "Historial",
                "priority": "Media",
                "desc": "El sistema debe conservar el historial aunque el lote activo cambie.",
                "actor": "Sistema",
                "pre": "Torneos procesados.",
                "crit": [
                    "Los torneos auditados permanecen en el historial.",
                    "La importación de un lote nuevo no elimina los torneos anteriores.",
                    "Cada torneo conserva el snapshot con el que se evaluó.",
                ],
            },
        ],
    ),
    (
        "3.8",
        "Visor de torneo",
        "El visor de torneo enfrenta el resultado real con el esperado y sitúa las anomalías en el eje de manos.",
        [
            {
                "id": "RF-VTR-01",
                "title": "Gráfica dual real vs. EV",
                "module": "Visor de torneo",
                "priority": "Alta",
                "desc": "El sistema debe representar la evolución acumulada del resultado real y del resultado esperado a lo largo del torneo.",
                "actor": "Jugador",
                "pre": "Torneo seleccionado.",
                "crit": [
                    "Muestra la evolución acumulada de fichas reales en ciegas grandes.",
                    "Muestra el EV esperado mano a mano.",
                    "El eje X representa el número de mano.",
                    "Ambas series comparten escala y ejes.",
                    "El subtítulo de la gráfica es fijo: «Resultado real frente a EV esperado, mano a mano».",
                ],
            },
            {
                "id": "RF-VTR-02",
                "title": "Franjas de anomalías",
                "module": "Visor de torneo",
                "priority": "Alta",
                "desc": "El sistema debe resaltar en la gráfica las ventanas reactivas y los tramos de desviación.",
                "actor": "Jugador",
                "pre": "Torneo con alertas o tramos.",
                "crit": [
                    "Resalta la ventana T+30 en rojo.",
                    "Resalta el tramo de desviación en ámbar.",
                    "El tooltip identifica el tipo de anomalía y sus métricas.",
                    "Con una ventana que toca varios torneos, la franja de cada torneo cubre solo sus manos de la ventana.",
                ],
            },
            {
                "id": "RF-VTR-03",
                "title": "Navegación a la mano",
                "module": "Visor de torneo",
                "priority": "Alta",
                "desc": "El sistema debe permitir pasar de cualquier punto de la gráfica al visor de la mano correspondiente.",
                "actor": "Jugador",
                "pre": "Torneo seleccionado.",
                "crit": [
                    "Al seleccionar un punto se abre la mano correspondiente.",
                    "El visor permite avanzar y retroceder mano a mano.",
                    "La navegación conserva el contexto del torneo.",
                ],
            },
            {
                "id": "RF-VTR-04",
                "title": "Cabecera del torneo",
                "module": "Visor de torneo",
                "priority": "Media",
                "desc": "El sistema debe identificar el torneo en la cabecera del visor.",
                "actor": "Jugador",
                "pre": "Torneo seleccionado.",
                "crit": [
                    "Muestra en una línea el torneo, el formato y el número de manos.",
                    "Muestra el estado conductual del torneo.",
                    "No muestra posición final, inscritos ni un bloque aparte de contexto.",
                ],
            },
            {
                "id": "RF-VTR-05",
                "title": "Lectura: conducta y suerte",
                "module": "Visor de torneo",
                "priority": "Alta",
                "desc": "El sistema debe presentar en un único bloque «Lectura» la conducta y la suerte del torneo por separado, para distinguir mal juego de mala suerte.",
                "actor": "Jugador",
                "pre": "Torneo seleccionado.",
                "crit": [
                    "El bloque Lectura aparece bajo el desglose de la mano, o en lugar de la lectura de sesión en un torneo sin alertas, y tiene dos partes: Conducta y Suerte del torneo.",
                    "Suerte del torneo muestra las BB ganadas, el All-in EV y la suerte all-in del torneo, con un ⓘ y el enlace «Ver en el Glosario».",
                    "La suerte all-in es neutra si la diferencia entre BB ganadas y All-in EV no supera 1σ, a favor si es mayor que σ y en contra si es menor que −σ; un torneo sin all-in es neutro. El umbral 1σ es provisional.",
                    "Con ventana T+30, Conducta muestra el trigger, la posición de la mano dentro de la ventana, las métricas de la alerta frente al baseline y la fuga neta estimada con un ⓘ.",
                    "Con desviación sin trigger, Conducta muestra el tramo detectado (manos de inicio y fin y número de manos, de forma aproximada), las métricas de la alerta frente al baseline y la fuga neta estimada con un ⓘ, y la gráfica marca el tramo con una franja; si una ventana T+30 lo atraviesa, la gráfica la muestra dentro del tramo con su propia franja y Conducta indica que el tramo está interrumpido por esa ventana.",
                    "Conducta solo aparece cuando la mano abierta pertenece a una alerta y muestra esa alerta; una mano fuera de cualquier alerta muestra solo Suerte del torneo, y la cabecera del visor indica si el torneo tiene alertas o no tiene anomalías.",
                    "El visor no muestra «resultado adicional» ni subtramos dentro de la ventana T+30, ni las cajas de impacto, cierre, fuga estimada o resto del patrón.",
                    "En un torneo con manos de la ventana de otro torneo, Conducta remite a esa alerta en lugar de indicar que no hay anomalías.",
                ],
            },
            {
                "id": "RF-VTR-06",
                "title": "Pestañas por torneo en la ventana T+30",
                "module": "Visor de torneo",
                "priority": "Alta",
                "desc": "El sistema debe permitir recorrer los torneos que aportan manos a una ventana T+30 sin mezclar sus gráficas.",
                "actor": "Jugador",
                "pre": "Ventana T+30 con manos de más de un torneo.",
                "crit": [
                    "Muestra una pestaña por cada torneo que aporta manos a la ventana; si solo toca uno, no hay pestañas.",
                    "La pestaña del torneo del trigger se abre primero.",
                    "Cada pestaña muestra la gráfica real frente a EV de su torneo y la franja T+30 solo sobre las manos de ese torneo dentro de la ventana.",
                    "Un torneo que no es el del trigger muestra un aviso informativo con enlace a la alerta, sin generar alerta propia, y no cuenta como torneo limpio.",
                    "Un trigger sin manos posteriores no genera ventana ni alerta y se muestra con la nota «sin manos posteriores».",
                ],
            },
            {
                "id": "RF-VTR-07",
                "title": "Pantalla de la ventana T+30",
                "module": "Visor de torneo",
                "priority": "Alta",
                "desc": "El sistema debe mostrar las manos de una ventana T+30 en el orden en que se jugaron, con la evidencia conductual de la ventana.",
                "actor": "Jugador",
                "pre": "Ventana T+30 detectada.",
                "crit": [
                    "Muestra las manos de la ventana ordenadas por hora, cada una con su torneo, su número de mano en el torneo, su resultado en BB y su acción.",
                    "Pulsar una mano abre su visor en la pestaña de su torneo.",
                    "El título identifica el torneo del trigger y el subtítulo la mano trigger y el tamaño de la ventana; si la ventana toca otros torneos, lo indica.",
                    "Muestra las manos de la ventana sobre las configuradas («n de 30» si es incompleta) y la fuga neta estimada con un ⓘ, o «no estimable» si la ventana es no concluyente.",
                    "Muestra VPIP, PFR y 3-Bet frente al baseline; las que no alcanzan su mínimo de oportunidades se muestran como «k de n» sin porcentaje.",
                    "Una ventana sin datos suficientes se identifica como no concluyente.",
                    "El resultado de cada mano es verde si es ganada, ámbar si pierde menos de 5 BB y rojo si pierde 5 BB o más.",
                    "No muestra un total de resultado de la ventana ni el recuento de manos con pérdida.",
                    "«Abrir la mano» lleva a la primera mano de la ventana.",
                ],
            },
        ],
    ),
    (
        "3.9",
        "Visor de mano",
        "El visor de mano presenta la evidencia mano a mano y permite etiquetar la jugada para el Nivel 2.",
        [
            {
                "id": "RF-VMA-01",
                "title": "Datos de la mano",
                "module": "Visor de mano",
                "priority": "Alta",
                "desc": "El sistema debe mostrar los datos completos de la mano seleccionada.",
                "actor": "Jugador",
                "pre": "Mano seleccionada.",
                "crit": [
                    "Muestra metadatos, cartas del héroe, cartas de los rivales y cartas comunitarias.",
                    "Muestra bote, ciegas, posición y stack.",
                    "Muestra el resultado real y el EV de la mano.",
                    "El jugador puede recorrer todas las manos del torneo una a una y seleccionar cualquiera desde la gráfica; un torneo sin alertas abre en su primera mano (M28).",
                ],
            },
            {
                "id": "RF-VMA-02",
                "title": "Secuencia de apuestas",
                "module": "Visor de mano",
                "priority": "Alta",
                "desc": "El sistema debe reconstruir la mano calle por calle.",
                "actor": "Jugador",
                "pre": "Mano seleccionada.",
                "crit": [
                    "Muestra preflop, flop, turn y river.",
                    "Muestra la acción de cada jugador y su importe.",
                    "Resalta las acciones del héroe.",
                ],
            },
            {
                "id": "RF-VMA-03",
                "title": "Contexto conductual de la mano",
                "module": "Visor de mano",
                "priority": "Alta",
                "desc": "El sistema debe situar la mano dentro de la evidencia conductual del torneo.",
                "actor": "Jugador",
                "pre": "Mano seleccionada.",
                "crit": [
                    "Indica si la mano pertenece a una ventana T+30 o a un tramo de desviación.",
                    "Muestra la equidad y el resultado esperado cuando hay all-in.",
                    "Muestra el baseline aplicable a la métrica observada.",
                ],
            },
            {
                "id": "RF-VMA-04",
                "title": "Navegación secuencial",
                "module": "Visor de mano",
                "priority": "Media",
                "desc": "El sistema debe permitir recorrer las manos del torneo sin perder el contexto.",
                "actor": "Jugador",
                "pre": "Mano seleccionada.",
                "crit": [
                    "Permite avanzar y retroceder a la mano anterior o siguiente.",
                    "Ofrece la acción “Siguiente en T+30” cuando la mano pertenece a una ventana.",
                    "Conserva el torneo y la posición dentro de la secuencia.",
                ],
            },
            {
                "id": "RF-VMA-05",
                "title": "Diagnóstico comunitario",
                "module": "Visor de mano",
                "priority": "Media",
                "desc": "El sistema debe mostrar la etiqueta sugerida por la comunidad y permitir validarla o cambiarla.",
                "actor": "Jugador",
                "pre": "Mano seleccionada y catálogo de etiquetas disponible.",
                "crit": [
                    "Muestra la etiqueta sugerida para la jugada.",
                    "Permite aceptar la sugerencia con un clic.",
                    "Permite cambiarla desde el catálogo de etiquetas.",
                    "Registra la etiqueta validada para el Nivel 2.",
                ],
            },
            {
                "id": "RF-VMA-06",
                "title": "Apertura desde una alerta",
                "module": "Visor de mano",
                "priority": "Alta",
                "desc": "El sistema debe abrir el visor en la mano que contiene la evidencia de la alerta.",
                "actor": "Jugador",
                "pre": "Alerta seleccionada.",
                "crit": [
                    "Una alerta de tilt abre la mano trigger.",
                    "Una alerta de desviación abre la primera mano del tramo.",
                    "La mano abierta queda resaltada dentro de la secuencia.",
                ],
            },
        ],
    ),
    (
        "3.10",
        "Etiquetado colaborativo Nivel 2",
        "El Nivel 2 recoge etiquetas semánticas validadas por personas y las usa para entrenar un clasificador común. Nunca modifica el baseline ni las alertas del Nivel 1.",
        [
            {
                "id": "RF-ETQ-01",
                "title": "Catálogo de etiquetas",
                "module": "Nivel 2",
                "priority": "Alta",
                "desc": "El sistema debe disponer de un catálogo versionado de etiquetas semánticas para clasificar jugadas.",
                "actor": "Sistema y jugador",
                "pre": "Acceso al visor de mano.",
                "crit": [
                    "Cada etiqueta tiene un código estable; su nombre, definición y ejemplo se cargan del archivo de traducción.",
                    "El catálogo está versionado.",
                    "La taxonomía se define en la sección 8. Los pesos por nivel de juego son provisionales y se calibrarán con datos reales.",
                ],
            },
            {
                "id": "RF-ETQ-02",
                "title": "Etiquetado de una mano",
                "module": "Nivel 2",
                "priority": "Alta",
                "desc": "El sistema debe permitir asignar una etiqueta semántica a una mano.",
                "actor": "Jugador",
                "pre": "Mano abierta en el visor.",
                "crit": [
                    "Cada usuario puede registrar una etiqueta por mano.",
                    "Se puede etiquetar cualquier mano de cualquier torneo auditado, tenga o no alerta (M28).",
                    "El registro guarda usuario, fecha y origen de la etiqueta.",
                    "La etiqueta queda asociada a la mano y al torneo.",
                ],
            },
            {
                "id": "RF-ETQ-03",
                "title": "Validación humana de etiquetas",
                "module": "Nivel 2",
                "priority": "Alta",
                "desc": "El sistema debe exigir validación humana antes de usar una etiqueta para entrenamiento.",
                "actor": "Jugador",
                "pre": "Etiqueta sugerida o registrada.",
                "crit": [
                    "El flujo ofrece aceptar la sugerencia o cambiarla.",
                    "La validación se completa con una acción explícita.",
                    "Las etiquetas sin validar no se usan para entrenar.",
                ],
            },
            {
                "id": "RF-ETQ-04",
                "title": "Ponderación de etiquetas",
                "module": "Nivel 2",
                "priority": "Media",
                "desc": "El sistema debe ponderar las etiquetas según el nivel de juego que el usuario declara en su cuenta.",
                "actor": "Sistema",
                "pre": "Etiqueta validada.",
                "crit": [
                    "Asigna un peso a cada etiqueta según el nivel de juego declarado en la cuenta.",
                    "Guarda el peso y el nivel de juego aplicados.",
                    "Los pesos provisionales por nivel de juego son Micro 0,6, Bajo 0,8, Medio 1,0, Alto 1,2 y Muy alto 1,4; se calibrarán con datos reales.",
                ],
            },
            {
                "id": "RF-ETQ-05",
                "title": "Entrenamiento del clasificador",
                "module": "Nivel 2",
                "priority": "Media",
                "desc": "El sistema debe entrenar un clasificador multiclase con las etiquetas validadas y registrar la versión del modelo.",
                "actor": "Sistema",
                "pre": "Etiquetas validadas y consentimiento del usuario.",
                "crit": [
                    "Entrena el clasificador con etiquetas validadas.",
                    "Registra la versión del modelo y la fecha de entrenamiento.",
                    "No usa etiquetas sin consentimiento.",
                ],
            },
            {
                "id": "RF-ETQ-06",
                "title": "Aislamiento del Nivel 1",
                "module": "Nivel 2",
                "priority": "Alta",
                "desc": "El sistema debe mantener el etiquetado comunitario separado del diagnóstico conductual individual.",
                "actor": "Sistema",
                "pre": "Etiqueta registrada.",
                "crit": [
                    "Una etiqueta no modifica el baseline.",
                    "Una etiqueta no modifica las alertas ya emitidas.",
                    "La etiqueta solo alimenta el clasificador del Nivel 2.",
                ],
            },
            {
                "id": "RF-ETQ-07",
                "title": "Consentimiento y privacidad",
                "module": "Nivel 2",
                "priority": "Alta",
                "desc": "El sistema debe informar y recoger el consentimiento del usuario antes de usar sus etiquetas de forma colaborativa.",
                "actor": "Jugador",
                "pre": "Primer acceso al etiquetado.",
                "crit": [
                    "Informa del uso colaborativo de las etiquetas.",
                    "Requiere consentimiento explícito.",
                    "Permite retirar el consentimiento.",
                    "El detalle se define en la sección 8.",
                ],
            },
        ],
    ),
    (
        "3.11",
        "Glosario y ayuda contextual",
        "El glosario explica las métricas y los conceptos del producto sin exigir conocimientos estadísticos previos.",
        [
            {
                "id": "RF-GLO-01",
                "title": "Consulta del glosario",
                "module": "Glosario",
                "priority": "Media",
                "desc": "El sistema debe ofrecer un glosario consultable con los términos del producto.",
                "actor": "Jugador",
                "pre": "Sesión iniciada.",
                "crit": [
                    "Los términos se ordenan alfabéticamente.",
                    "El glosario incluye buscador.",
                    "Cada término incluye definición y ejemplo.",
                    "Incluye BB ganadas, All-in EV, suerte all-in y fuga neta; la fuga neta se explica paso a paso, con un ejemplo con all-in y otro sin ellos.",
                ],
            },
            {
                "id": "RF-GLO-02",
                "title": "Enlace contextual al glosario",
                "module": "Glosario",
                "priority": "Media",
                "desc": "El sistema debe enlazar cada métrica con su término del glosario.",
                "actor": "Jugador",
                "pre": "Modal de métrica o tooltip abierto.",
                "crit": [
                    "El enlace abre el término concreto y no la portada.",
                    "El enlace está disponible desde los modales de métricas.",
                    "El glosario conserva el contexto de la pantalla de origen.",
                ],
            },
        ],
    ),
    (
        "3.12",
        "Cuenta, registro, sesión y configuración",
        "La cuenta permite registrarse, aísla los datos del jugador y concentra la configuración del motor y el cierre de sesión.",
        [
            {
                "id": "RF-CUE-01",
                "title": "Registro y autenticación",
                "module": "Cuenta",
                "priority": "Alta",
                "desc": "El sistema debe permitir crear una cuenta y exigir autenticación para acceder a los datos del jugador.",
                "actor": "Jugador",
                "pre": "Acceso a la aplicación sin sesión iniciada.",
                "crit": [
                    "El jugador crea una cuenta con nombre, correo, contraseña y su nivel de juego (buy-in habitual en MTT); hay cinco tramos (1–5 €, 5–10 €, 10–25 €, 25–50 € y 50 € o más); cada tramo tiene un peso provisional (Micro 0,6, Bajo 0,8, Medio 1,0, Alto 1,2 y Muy alto 1,4).",
                    "El correo y el nombre son únicos.",
                    "La contraseña tiene entre 8 y 64 caracteres, sin reglas de composición.",
                    "La contraseña se almacena como hash y sal.",
                    "Tras el alta, el jugador puede iniciar sesión.",
                    "El acceso requiere credenciales válidas.",
                    "La sesión se mantiene hasta el cierre o la expiración.",
                    "El error de acceso no revela si el usuario existe.",
                ],
            },
            {
                "id": "RF-CUE-02",
                "title": "Drawer de cuenta",
                "module": "Cuenta",
                "priority": "Media",
                "desc": "El sistema debe reunir la identidad y la configuración del motor en un drawer global.",
                "actor": "Jugador",
                "pre": "Sesión iniciada.",
                "crit": [
                    "Muestra nombre de usuario, sitio activo, nivel de juego y estado de la cuenta.",
                    "Incluye la ventana reactiva y la sensibilidad FDR.",
                    "Se abre desde cualquier pantalla.",
                ],
            },
            {
                "id": "RF-CUE-03",
                "title": "Configuración del motor",
                "module": "Cuenta",
                "priority": "Alta",
                "desc": "El sistema debe permitir ajustar la ventana reactiva y la sensibilidad estadística para el siguiente lote.",
                "actor": "Jugador",
                "pre": "Drawer de cuenta abierto.",
                "crit": [
                    "La ventana reactiva admite T+20, T+30, T+50 y T+100.",
                    "La sensibilidad admite q < 0,10, q < 0,05 y q < 0,01.",
                    "El guardado es explícito.",
                    "La configuración afecta únicamente al siguiente lote.",
                    "El nivel de juego se puede cambiar desde el drawer y afecta solo a las etiquetas posteriores al cambio.",
                ],
            },
            {
                "id": "RF-CUE-04",
                "title": "Aislamiento por usuario, sitio y formato",
                "module": "Cuenta",
                "priority": "Alta",
                "desc": "El sistema debe garantizar que cada usuario accede únicamente a sus propios datos.",
                "actor": "Sistema",
                "pre": "Sesión iniciada.",
                "crit": [
                    "Cada usuario ve solo sus manos, su baseline y sus alertas.",
                    "El sitio activo es Winamax.",
                    "El formato es MTT.",
                    "La interfaz no ofrece cambio de usuario, sitio ni formato.",
                ],
            },
            {
                "id": "RF-CUE-05",
                "title": "Cierre de sesión",
                "module": "Cuenta",
                "priority": "Media",
                "desc": "El sistema debe cerrar la sesión de forma segura y confirmada.",
                "actor": "Jugador",
                "pre": "Sesión iniciada.",
                "crit": [
                    "El cierre de sesión pide confirmación.",
                    "Al confirmar, la sesión se invalida.",
                ],
            },
        ],
    ),
    (
        "3.13",
        "Comparativa Baseline vs Tilt (T+30)",
        "La comparativa agrega las ventanas T+30 del último lote y las contrasta con el baseline activo en cinco métricas.",
        [
            {
                "id": "RF-CMP-01",
                "title": "Acceso y alcance de la comparativa",
                "module": "Comparativa",
                "priority": "Alta",
                "desc": "El sistema debe ofrecer una pantalla que compare las ventanas T+30 del último lote con el baseline activo.",
                "actor": "Jugador",
                "pre": "Baseline activo y al menos un lote auditado.",
                "crit": [
                    "Se accede desde “Baseline vs Tilt (T+30)” en la navegación global.",
                    "Hasta que se audita el primer lote, el acceso está desactivado.",
                    "Agrega las ventanas T+30 del último lote auditado y las compara con el baseline activo, no con el snapshot de cada alerta.",
                    "El alcance de la comparativa (último lote, periodo o histórico) está por estudiar.",
                    "Muestra las manos del baseline, las manos dentro de ventanas T+30 y el número de episodios.",
                    "Si el último lote no contiene ventanas T+30, muestra un estado vacío.",
                ],
            },
            {
                "id": "RF-CMP-02",
                "title": "Métricas y contraste estadístico",
                "module": "Comparativa",
                "priority": "Alta",
                "desc": "El sistema debe contrastar la conducta en ventana frente al baseline con cinco métricas.",
                "actor": "Sistema",
                "pre": "Ventanas T+30 calculadas.",
                "crit": [
                    "Compara VPIP, PFR, 3-Bet, Fold vs 3-Bet y WTSD.",
                    "Muestra, para cada métrica, el valor del baseline, el valor de las ventanas y su diferencia en puntos porcentuales.",
                    "Cada métrica guarda su numerador y su denominador.",
                    "Contrasta solo las métricas evaluables sobre las oportunidades acumuladas de las ventanas; las demás se muestran como «k de n» sin porcentaje.",
                    "Aplica la corrección FDR solo a las pruebas evaluables, con el umbral q configurado, y lo muestra en una insignia.",
                    "Indica cuántas de las métricas evaluables son significativas.",
                ],
            },
            {
                "id": "RF-CMP-03",
                "title": "Indicadores y lectura de la comparativa",
                "module": "Comparativa",
                "priority": "Media",
                "desc": "El sistema debe resumir la comparativa en indicadores y explicar cómo leerla.",
                "actor": "Jugador",
                "pre": "Comparativa disponible.",
                "crit": [
                    "Muestra la desviación de VPIP y la agresividad impulsiva (desviación de 3-Bet) en puntos porcentuales.",
                    "Muestra la fuga neta acumulada de las ventanas, calculada con la fórmula de la fuga neta, y “no estimable” si falta el EV.",
                    "Explica qué es el baseline, qué es una ventana T+30, qué significa q y qué no demuestra la comparación.",
                    "La lectura distingue un ajuste técnico (una sola métrica) de un patrón de descontrol (varias a la vez).",
                ],
            },
        ],
    ),
]


NFRS = [
    {
        "id": "RNF-01",
        "title": "Usabilidad",
        "category": "Calidad de uso",
        "desc": "La interfaz debe poder utilizarse sin formación previa y sin conocer la terminología estadística.",
        "crit": [
            "El diseño es desktop-first y se valida desde 1280×720.",
            "El flujo importar, revisar el Dashboard y auditar se completa sin cambiar de contexto.",
            "Cada métrica dispone de ayuda contextual.",
            "Todos los textos de la interfaz están en español.",
        ],
        "verification": "Prueba de usuario con el prototipo y revisión heurística.",
    },
    {
        "id": "RNF-02",
        "title": "Accesibilidad",
        "category": "Calidad de uso",
        "desc": "La interfaz debe ser legible y comprensible para personas con limitaciones visuales o cognitivas.",
        "crit": [
            "El contraste cumple WCAG AA, con un mínimo de 4,5:1 en texto normal.",
            "Estados y alertas combinan color, icono y texto.",
            "Las gráficas incluyen etiquetas y descripciones textuales.",
        ],
        "verification": "Auditoría de contraste y revisión de componentes.",
    },
    {
        "id": "RNF-03",
        "title": "Rendimiento",
        "category": "Eficiencia",
        "desc": "El sistema debe procesar los lotes sin bloquear la interfaz y mostrar el Dashboard con rapidez.",
        "crit": [
            "La interfaz permanece operable durante el análisis de un lote.",
            "El procesamiento se ejecuta por lotes.",
            "El Dashboard lee el último lote sin recalcular el histórico completo.",
            "El Dashboard con el último lote se muestra en menos de 2 segundos.",
            "El procesamiento de 10.000 manos termina en menos de 60 segundos en el equipo de referencia.",
        ],
        "verification": "Medición sobre un lote de prueba con el volumen de la demo.",
    },
    {
        "id": "RNF-04",
        "title": "Seguridad",
        "category": "Protección",
        "desc": "El sistema debe proteger las credenciales y aislar los datos de cada usuario.",
        "crit": [
            "El acceso requiere autenticación.",
            "Las contraseñas se almacenan con hash y sal.",
            "El transporte utiliza HTTPS.",
            "Cada consulta se limita al usuario autenticado.",
        ],
        "verification": "Revisión de configuración y pruebas de acceso cruzado.",
    },
    {
        "id": "RNF-05",
        "title": "Privacidad",
        "category": "Protección",
        "desc": "El sistema debe recoger solo los datos necesarios y respetar el consentimiento del usuario.",
        "crit": [
            "Solo se solicitan los datos imprescindibles para el análisis.",
            "El Nivel 2 requiere consentimiento explícito.",
            "El consentimiento se puede retirar.",
            "Las etiquetas comunitarias no exponen la identidad del jugador.",
        ],
        "verification": "Revisión del flujo de consentimiento y de los datos almacenados.",
    },
    {
        "id": "RNF-06",
        "title": "Integridad y auditabilidad",
        "category": "Fiabilidad",
        "desc": "El sistema debe conservar la trazabilidad de cada alerta y impedir que el baseline se contamine.",
        "crit": [
            "El baseline es inmutable y versionado.",
            "Cada alerta guarda el snapshot con el que se calculó.",
            "Cada métrica guarda numerador y denominador.",
            "Cada prueba estadística conserva su q-value.",
            "La demo utiliza manos reales.",
        ],
        "verification": "Revisión de la base de datos y reproducción de una alerta.",
    },
    {
        "id": "RNF-07",
        "title": "Mantenibilidad",
        "category": "Evolución",
        "desc": "El sistema debe organizarse en módulos desacoplados que permitan sustituir o ampliar componentes.",
        "crit": [
            "La arquitectura separa ingesta, dominio, análisis, API y frontend.",
            "Los módulos se comunican mediante contratos explícitos.",
            "La API REST está documentada.",
            "Parser, baseline y detectores disponen de pruebas automatizadas.",
            "La configuración está externalizada.",
        ],
        "verification": "Revisión de la arquitectura y ejecución de la suite de pruebas.",
    },
    {
        "id": "RNF-08",
        "title": "Compatibilidad",
        "category": "Portabilidad",
        "desc": "El sistema debe funcionar en el entorno de escritorio definido para el MVP.",
        "crit": [
            "Funciona en las últimas versiones de los navegadores de escritorio mayoritarios.",
            "La resolución mínima soportada es 1280×720.",
            "No existe versión móvil en el MVP.",
        ],
        "verification": "Prueba en los navegadores soportados.",
    },
    {
        "id": "RNF-09",
        "title": "Idioma y formato",
        "category": "Localización",
        "desc": "El sistema debe presentar la información con el idioma del MVP y el formato numérico y de fecha definidos. La externalización de los textos se recoge en RNF-12.",
        "crit": [
            "La interfaz está en español.",
            "Las fechas se guardan en UTC y se muestran en la zona local.",
            "Los porcentajes usan coma decimal y un decimal.",
            "Las cifras de BB/100 usan dos decimales, signo y separador de miles.",
        ],
        "verification": "Revisión de textos y de formato en la interfaz.",
    },
    {
        "id": "RNF-10",
        "title": "Trazabilidad",
        "category": "Fiabilidad",
        "desc": "El sistema debe permitir reconstruir por qué se emitió cada alerta.",
        "crit": [
            "Cada alerta enlaza con la mano o el tramo que la origina.",
            "Cada métrica conserva su origen y su muestra.",
            "Cada alerta conserva el baseline y la configuración con los que se calculó.",
            "El historial conserva las alertas auditadas.",
        ],
        "verification": "Auditoría de una alerta de principio a fin.",
    },
    {
        "id": "RNF-11",
        "title": "Recuperación",
        "category": "Fiabilidad",
        "desc": "El sistema debe aislar los fallos y conservar los datos ya confirmados.",
        "crit": [
            "Un error en un bloque no tumba el Dashboard.",
            "Los estados parciales indican qué información falta.",
            "Un lote confirmado no se pierde ante un error de la interfaz.",
            "La recuperación reintenta el bloque fallido sin perder el lote confirmado.",
            "Si el fallo persiste, el bloque queda en estado parcial y se ofrece recargarlo.",
        ],
        "verification": "Prueba de fallo inducido por bloque.",
    },
    {
        "id": "RNF-12",
        "title": "Internacionalización",
        "category": "Localización",
        "desc": "El sistema debe estar preparado para traducir la interfaz a otros idiomas sin rehacer pantallas, aunque el MVP solo ofrezca español.",
        "crit": [
            "Ningún texto visible se escribe en el código: pantallas, avisos, toasts, modales, alertas, bloque «Lectura», tooltips y glosario se cargan desde archivos de traducción por idioma (en el MVP solo español) mediante claves.",
            "El backend y la base de datos no guardan ni devuelven frases montadas: alertas, lecturas, avisos de muestra pequeña y estados se representan con un código y sus parámetros, y el frontend compone el texto en el idioma activo.",
            "Los datos se guardan en bruto, con números sin formato, fechas en UTC y métricas con numerador y denominador; el formato de números, porcentajes y fechas se aplica solo al mostrarlos, según el idioma.",
            "Los términos técnicos de póker (VPIP, PFR, 3-Bet, Fold vs 3-Bet, WTSD, bad beat, tilt, trigger, A-Game, EVbb/100, BB, FDR, MTT) no se traducen en ningún idioma.",
        ],
        "verification": "Búsqueda de textos visibles en el código y de frases montadas en las respuestas de la API; comprobación con un archivo de traducción de prueba.",
    },
]


# ---------------------------------------------------------------------------
# Portada
# ---------------------------------------------------------------------------

doc.add(spacer(1200))
doc.add(
    para(
        run("MINDSET & EV LEAK FINDER", bold=True, color=BRAND_LIGHT, size=13),
        align="center",
        after=180,
    )
)
doc.add(
    para(
        run("Documento de requisitos funcionales", bold=True, color=BRAND, size=30),
        align="center",
        after=140,
    )
)
doc.add(
    para(
        run(
            "Detección algorítmica de desviaciones conductuales y fugas de EV en póker online",
            color=MUTED,
            size=13,
        ),
        align="center",
        after=360,
        line=300,
    )
)
doc.add(para("", bottom_border=True, after=360))
doc.add(para(run("Autor", bold=True, color=BRAND, size=9), align="center", after=20))
doc.add(para(run("Mario Ramírez García", size=13), align="center", after=160))
doc.add(para(run("Titulación", bold=True, color=BRAND, size=9), align="center", after=20))
doc.add(para(run("Grado en Ingeniería Informática · UNED", size=13), align="center", after=160))
doc.add(para(run("Curso académico", bold=True, color=BRAND, size=9), align="center", after=20))
doc.add(para(run("2025–2026", size=13), align="center", after=160))
doc.add(para(run("Versión 1.0 · 6 de noviembre de 2026", color=MUTED, size=10), align="center", after=0))

doc.add(page_break())

# ---------------------------------------------------------------------------
# Control del documento y contenido
# ---------------------------------------------------------------------------

h2("Control del documento")

control_rows = [
    table_head(["Versión", "Fecha", "Autor", "Estado"], [1400, 2200, 3000, 2400]),
    tr([
        simple_cell("1.0", 1400),
        simple_cell("6 de noviembre de 2026", 2200),
        simple_cell("Mario Ramírez García", 3000),
        simple_cell("Borrador para revisión", 2400),
    ]),
]
doc.add(table(control_rows, [1400, 2200, 3000, 2400]))
doc.add(spacer(220))

h2("Contenido")

TOC = [
    (1, "1. Introducción"),
    (2, "1.1 Objetivo"),
    (2, "1.2 Alcance"),
    (2, "1.3 Definiciones"),
    (2, "1.4 Referencias"),
    (1, "2. Descripción general"),
    (2, "2.1 Contexto"),
    (2, "2.2 Principio rector"),
    (2, "2.3 Actores"),
    (2, "2.4 Supuestos y dependencias"),
    (2, "2.5 Restricciones"),
    (1, "3. Requisitos funcionales"),
    (2, "3.0 Resumen de requisitos"),
    (2, "3.1 Importación e ingesta"),
    (2, "3.2 Parser y normalización"),
    (2, "3.3 Session Builder: sesiones y torneos"),
    (2, "3.4 Baseline individual"),
    (2, "3.5 Detección Nivel 1"),
    (2, "3.6 Dashboard macro"),
    (2, "3.7 Historial de torneos"),
    (2, "3.8 Visor de torneo"),
    (2, "3.9 Visor de mano"),
    (2, "3.10 Etiquetado colaborativo Nivel 2"),
    (2, "3.11 Glosario y ayuda contextual"),
    (2, "3.12 Cuenta, sesión y configuración"),
    (1, "4. Requisitos no funcionales"),
    (1, "5. Requisitos de datos"),
    (1, "6. Interfaces externas"),
    (1, "7. Trazabilidad"),
    (1, "8. Parámetros del producto"),
    (1, "9. Fuera de alcance"),
    (1, "10. Referencias"),
    (1, "Anexo A · Datos extraídos del historial"),
    (2, "A.1 Torneo"),
    (2, "A.2 Mano"),
    (2, "A.3 Participación en mano"),
    (2, "A.4 Acción"),
    (2, "A.5 Bote"),
    (2, "A.6 Métricas y EV"),
]
for level, text in TOC:
    doc.add(
        para(
            run(
                text,
                bold=level == 1,
                color=BRAND if level == 1 else None,
                size=10.5 if level == 1 else 9.5,
            ),
            left=0 if level == 1 else 360,
            after=30 if level == 2 else 90,
        )
    )

doc.add(page_break())

# ---------------------------------------------------------------------------
# 1. Introducción
# ---------------------------------------------------------------------------

h1("1. Introducción")

h2("1.1 Objetivo")
body(
    "Este documento define los requisitos funcionales del sistema Mindset & EV Leak Finder, "
    "un software que analiza historiales de manos de póker online para detectar desviaciones "
    "conductuales y degradación del rendimiento respecto al baseline individual del jugador."
)
body(
    "El objetivo es servir de referencia cerrada para el diseño, la implementación y la validación "
    "del producto, de modo que cada requisito pueda comprobarse sin depender de decisiones no documentadas."
)

h2("1.2 Alcance")
body("El alcance del MVP incluye:")
bullet("Ingesta de archivos de historiales de Winamax en formato .txt.")
bullet("Parseo, normalización monetaria a ciegas grandes y construcción de sesiones y torneos.")
bullet("Cálculo y congelación del baseline individual.")
bullet("Detección de triggers, ventanas T+30, tramos de desviación y fatiga.")
bullet("Corrección de falsos positivos mediante FDR.")
bullet("Dashboard macro, historial de torneos, visor de torneo y visor de mano.")
bullet("Etiquetado colaborativo con validación humana.")
bullet("Glosario, ayuda contextual y gestión de la cuenta.")
body(
    "El sistema se limita a Winamax, a un único usuario y al formato MTT. Las decisiones de "
    "alcance se recogen en la sección 9."
)

h2("1.3 Definiciones")
body("Los términos siguientes se usan con un significado único en todo el documento.")

DEFINITIONS = [
    ("Baseline", "Referencia estable del jugador calculada sobre sesiones anteriores al periodo evaluado. Es el estándar contra el que se compara cada ventana o tramo."),
    ("Trigger", "Evento que puede iniciar una reacción conductual. En este sistema, un bad beat (all-in perdido con equidad favorable) o la pérdida de un bote grande."),
    ("Ventana T+30", "Conjunto de las 30 manos que el jugador juega inmediatamente después de un trigger, en cualquier torneo de su sesión. La mano trigger no se incluye."),
    ("Tramo continuo", "Bloque de manos consecutivas con una desviación sostenida, obtenido mediante ventana deslizante y fusión de intervalos."),
    ("Fuga neta", "Estimación del coste en ciegas grandes de haber jugado distinto al baseline en una ventana o tramo, medido en EV: lo esperado a tu ritmo normal menos lo esperado en la ventana. Si la diferencia es negativa, no hay fuga."),
    ("BB ganadas", "Fichas ganadas o perdidas en el torneo, en ciegas grandes: suma del resultado real de todas sus manos. No es la posición final ni el premio."),
    ("All-in EV", "Resultado que se habría obtenido si los all-in hubieran salido como dicta la equidad. En las manos sin all-in coincide con el resultado real."),
    ("Suerte all-in", "Indica si la suerte en los all-in fue a favor, neutra o en contra: neutra si la diferencia entre BB ganadas y All-in EV no supera lo esperable por azar en ese torneo (1σ, provisional)."),
    ("Ciega grande (BB)", "Unidad de referencia del análisis. Cada mano se normaliza con la ciega grande vigente en esa mano, no con la del torneo."),
    ("BB/100", "Ciegas grandes ganadas o perdidas por cada 100 manos."),
    ("EVbb/100", "Rendimiento esperado por cada 100 manos, calculado con la equidad de los all-in en lugar del resultado real."),
    ("FDR", "Corrección de Benjamini-Hochberg para controlar los falsos positivos en comparaciones múltiples."),
    ("A-Game", "Nivel de juego óptimo del jugador, sin fatiga ni sesgo emocional."),
    ("Sesión", "Bloque continuo de manos separadas por pausas no superiores al umbral. Puede contener varios torneos y un torneo nunca se reparte entre sesiones."),
    ("Torneo limpio", "Torneo sin alertas de tilt ni desviaciones significativas, con independencia de su resultado económico."),
    ("Lote de importación", "Conjunto de torneos incorporados en una misma operación de importación. Se registra con identificador propio y se procesa de forma atómica."),
    ("Torneo duplicado", "Torneo cuyo identificador ya existe en el sistema. No se vuelve a procesar."),
]
rows = [table_head(["Término", "Definición"], [2300, 6700])]
for i, (term, definition) in enumerate(DEFINITIONS):
    fill = ZEBRA if i % 2 else None
    rows.append(
        tr([
            tc(para(run(term, bold=True, color=BRAND, size=8.8), style="TableText", after=0), 2300, fill=fill),
            tc(para(run(definition, size=8.8), style="TableText", after=0), 6700, fill=fill),
        ])
    )
doc.add(table(rows, [2300, 6700]))
doc.add(spacer(160))

h2("1.4 Referencias")
REFS = [
    ("Especificación técnica", "sources/master-doc.txt", "Pipeline, módulos y criterios funcionales."),
    ("Prototipo visual", "sources/Mindset-EV-Leak-Finder-TFG.pptx", "Referencia de interfaz y flujos de pantalla."),
    ("Design Thinking", "sources/design-thinking.pptx", "Investigación de usuario, personas y decisiones de diseño."),
]
rows = [table_head(["Documento", "Ruta", "Uso"], [2300, 3400, 3300])]
for i, (name, path, use) in enumerate(REFS):
    fill = ZEBRA if i % 2 else None
    rows.append(
        tr([
            tc(para(run(name, bold=True, size=8.8), style="TableText", after=0), 2300, fill=fill),
            tc(para(run(path, size=8.4, color=MUTED), style="TableText", after=0), 3400, fill=fill),
            tc(para(run(use, size=8.8), style="TableText", after=0), 3300, fill=fill),
        ])
    )
doc.add(table(rows, [2300, 3400, 3300]))
doc.add(spacer(160))

# ---------------------------------------------------------------------------
# 2. Descripción general
# ---------------------------------------------------------------------------

doc.add(page_break())
h1("2. Descripción general")

h2("2.1 Contexto")
body(
    "Los trackers tradicionales resumen miles de manos en medias globales y obligan al jugador a "
    "buscar manualmente el momento en el que su conducta cambió. Este sistema compara cada torneo "
    "contra el baseline individual del propio jugador y localiza dos fenómenos: ventanas reactivas "
    "posteriores a un bad beat crítico y tramos continuos de sobrefrecuencia sin trigger aparente."
)
body(
    "La interfaz no juzga el resultado económico. Muestra evidencia estadística auditable mano a mano "
    "y separa la mala suerte del mal juego. Sobre esa base, una capa colaborativa permite etiquetar "
    "jugadas para entrenar un clasificador común con validación humana."
)

h2("2.2 Principio rector")
note(
    "Principio rector",
    "El resultado no define la conducta. Un torneo puede ganar dinero y contener una desviación "
    "conductual; otro puede perder y ser un torneo limpio porque la pérdida se explica por varianza. "
    "Las alertas se basan en conducta observable contrastada contra el baseline, nunca en el resultado "
    "económico aislado.",
)

h2("2.3 Actores")
ACTORS = [
    ("Jugador", "Único usuario del MVP. Importa sus manos, consulta el Dashboard, audita alertas y etiqueta jugadas."),
    ("Sistema", "Procesa los archivos, calcula el baseline, detecta anomalías y genera la evidencia."),
    ("Comunidad", "Aporta etiquetas semánticas validadas para el clasificador del Nivel 2. No interviene en el diagnóstico individual."),
]
rows = [table_head(["Actor", "Responsabilidad"], [2300, 6700])]
for i, (actor, role) in enumerate(ACTORS):
    fill = ZEBRA if i % 2 else None
    rows.append(
        tr([
            tc(para(run(actor, bold=True, color=BRAND, size=8.8), style="TableText", after=0), 2300, fill=fill),
            tc(para(run(role, size=8.8), style="TableText", after=0), 6700, fill=fill),
        ])
    )
doc.add(table(rows, [2300, 6700]))
doc.add(spacer(140))

h2("2.4 Supuestos y dependencias")
bullet("El jugador dispone de historiales de manos de Winamax en formato .txt.")
bullet("Cada archivo corresponde a un torneo y no se modifica después de exportarlo.")
bullet("El jugador mantiene un volumen suficiente de manos para construir un baseline válido.")
bullet("El sistema se ejecuta en un servidor con acceso a una base de datos relacional.")
bullet("El frontend se utiliza en un navegador de escritorio.")

h2("2.5 Restricciones")
bullet("El MVP se limita a Winamax, un usuario y MTT.")
bullet("El diseño es desktop-first y no incluye versión móvil.")
bullet("El tema es oscuro y el idioma español.")
bullet("El sistema no incorpora datos ni etiquetas sintéticas.")
bullet("La navegación por teclado y el lector de pantalla quedan fuera del MVP y se documentan como limitación.")

# ---------------------------------------------------------------------------
# 3. Requisitos funcionales
# ---------------------------------------------------------------------------

doc.add(page_break())
h1("3. Requisitos funcionales")
intro(
    "Cada requisito se presenta en una ficha con identificador, prioridad, descripción, actor, "
    "precondiciones y criterios de aceptación. Los criterios se numeran con letras y son comprobables "
    "de forma independiente."
)

h2("3.0 Resumen de requisitos")
summary_rows = [table_head(["ID", "Requisito", "Módulo", "Prioridad"], [1150, 4250, 2100, 1500])]
count = 0
for _, _, _, reqs in SECTIONS:
    for req in reqs:
        count += 1
        fill = ZEBRA if count % 2 == 0 else None
        summary_rows.append(
            tr([
                tc(para(run(req["id"], bold=True, color=BRAND, size=8.4), style="TableText", after=0), 1150, fill=fill),
                tc(para(run(req["title"], size=8.4), style="TableText", after=0), 4250, fill=fill),
                tc(para(run(req["module"], size=8.4, color=MUTED), style="TableText", after=0), 2100, fill=fill),
                tc(para(run(req["priority"], size=8.4), style="TableText", after=0), 1500, fill=fill),
            ])
        )
doc.add(table(summary_rows, [1150, 4250, 2100, 1500]))
doc.add(spacer(100))
doc.add(para(run(f"Total: {count} requisitos funcionales.", italic=True, color=MUTED, size=9), style="Caption"))
doc.add(page_break())

for num, title, section_intro, reqs in SECTIONS:
    h2(f"{num} {title}")
    intro(section_intro)
    for req in reqs:
        req_card(req)

# ---------------------------------------------------------------------------
# 4. Requisitos no funcionales
# ---------------------------------------------------------------------------

doc.add(page_break())
h1("4. Requisitos no funcionales")
intro(
    "Los requisitos no funcionales definen la calidad con la que el sistema debe cumplir sus "
    "requisitos funcionales. Cada uno incluye un criterio medible y un método de verificación."
)
for item in NFRS:
    nfr_card(item)

# ---------------------------------------------------------------------------
# 5. Requisitos de datos
# ---------------------------------------------------------------------------

doc.add(page_break())
h1("5. Requisitos de datos")
intro(
    "El sistema debe conservar las entidades necesarias para reconstruir el baseline, las alertas "
    "y la evidencia asociada. El modelo físico se detalla en la documentación de diseño."
)

ENTITIES = [
    ("Usuario", "Cuenta y preferencias del jugador.", "id, nombre, email, sitio activo, consentimiento"),
    ("Torneo", "Unidad de competición que agrupa manos.", "id, nombre, fecha inicio, fecha fin, nivel inicial, nivel final, formato, tamaño de mesa, recompensa, manos"),
    ("Sesión", "Bloque continuo de manos separadas por pausas no superiores al umbral.", "id, primera mano, inicio, fin, duración, manos, torneos, sitio, formato, resultado_bb, ev_bb, bb100, evbb100"),
    ("Mano", "Registro canónico de una mano.", "id, hand_id, índice propio, número original, torneo, sesión, timestamp UTC, ante, SB, BB, board, bote_bb, net_bb, ev_bb, all_in, showdown"),
    ("Participación en mano", "Intervención de un jugador en una mano.", "mano, jugador, asiento, posición, stack_bb, aportación_bb, cobrado_bb, neto_bb, cartas, all_in, estado"),
    ("Acción", "Intervención de un jugador en una calle.", "id, mano, jugador, calle, orden, tipo, importe_bb, importe_total_bb, all_in, bote_bb"),
    ("Snapshot de baseline", "Versión congelada del baseline.", "id, fecha, estado, muestra, métricas, versión"),
    ("Alerta", "Detección significativa con evidencia.", "id, tipo, torneo, métricas, snapshot, estado"),
    ("Ventana reactiva", "Ventana T+30 asociada a un trigger.", "id, trigger, inicio, fin, métricas"),
    ("Tramo de desviación", "Intervalo continuo con sobrefrecuencia.", "id, inicio, fin, métricas, q-value"),
    ("Tramo de fatiga", "Intervalo de horas con EVbb/100.", "id, desde, hasta, manos, sesiones, evbb100"),
    ("Lote de importación", "Conjunto de torneos incorporados en una operación de importación.", "id, fecha UTC, torneos, manos, sesiones, periodo, estado, resultado por torneo"),
    ("Etiqueta", "Etiqueta semántica del Nivel 2.", "id, código, versión, peso"),
    ("Etiqueta de mano", "Asignación validada de una etiqueta.", "id, mano, usuario, etiqueta, fecha, peso"),
]
rows = [table_head(["Entidad", "Descripción", "Campos clave"], [2100, 3800, 3100])]
for i, (entity, description, fields) in enumerate(ENTITIES):
    fill = ZEBRA if i % 2 else None
    rows.append(
        tr([
            tc(para(run(entity, bold=True, color=BRAND, size=8.4), style="TableText", after=0), 2100, fill=fill),
            tc(para(run(description, size=8.4), style="TableText", after=0), 3800, fill=fill),
            tc(para(run(fields, size=8.2, color=MUTED), style="TableText", after=0), 3100, fill=fill),
        ])
    )
doc.add(table(rows, [2100, 3800, 3100]))
doc.add(spacer(160))

body("Invariantes de datos:")
bullet("El baseline solo usa datos cronológicamente anteriores al periodo evaluado.")
bullet("Cada alerta conserva el snapshot con el que se calculó.")
bullet("Cada métrica conserva numerador y denominador.")
bullet("Un archivo de Winamax corresponde a un torneo y no se modifica después de exportarlo.")
bullet("Un torneo se identifica por su identificador y no se importa dos veces.")
bullet("El lote de importación es atómico: se guarda completo o no se guarda.")
bullet("Cada mano se normaliza con la ciega grande vigente en esa mano.")
bullet("Todos los importes del análisis se guardan en ciegas grandes; las fichas solo definen el nivel de ciegas.")
bullet("El registro canónico contiene la mano completa y sustituye al texto original como fuente de verdad.")
bullet("Sustituir el baseline archiva la versión anterior y no la elimina.")
bullet("Las etiquetas del Nivel 2 no modifican el baseline ni las alertas del Nivel 1.")

# ---------------------------------------------------------------------------
# 6. Interfaces externas
# ---------------------------------------------------------------------------

doc.add(page_break())
h1("6. Interfaces externas")
intro("El sistema se comunica con el exterior a través de las siguientes interfaces.")

INTERFACES = [
    ("Entrada de archivos", "Archivo .txt", "Historiales de manos de Winamax. Es la única fuente de datos del MVP."),
    ("API REST", "JSON sobre HTTPS", "Expone los datos y operaciones que consume el frontend."),
    ("Interfaz web", "Navegador de escritorio", "Presenta el Dashboard, el historial y los visores."),
    ("Base de datos", "Relacional", "Persiste usuarios, torneos, manos, baselines, alertas y etiquetas."),
]
rows = [table_head(["Interfaz", "Tecnología", "Descripción"], [2200, 2200, 4600])]
for i, (name, tech, description) in enumerate(INTERFACES):
    fill = ZEBRA if i % 2 else None
    rows.append(
        tr([
            tc(para(run(name, bold=True, color=BRAND, size=8.8), style="TableText", after=0), 2200, fill=fill),
            tc(para(run(tech, size=8.8), style="TableText", after=0), 2200, fill=fill),
            tc(para(run(description, size=8.8), style="TableText", after=0), 4600, fill=fill),
        ])
    )
doc.add(table(rows, [2200, 2200, 4600]))
doc.add(spacer(160))
body("El MVP no integra servicios externos de terceros, HUD en tiempo real ni fuentes de datos distintas de Winamax.")

# ---------------------------------------------------------------------------
# 7. Trazabilidad
# ---------------------------------------------------------------------------

doc.add(page_break())
h1("7. Trazabilidad")
intro(
    "La trazabilidad relaciona los objetivos del trabajo con los módulos y los requisitos que los materializan."
)

OBJECTIVES = [
    ("OE-01", "Ingerir y normalizar historiales de manos de Winamax.", "3.1, 3.2, 3.3", "RF-ING, RF-PAR, RF-SES"),
    ("OE-02", "Construir un baseline individual congelado y libre de data leakage.", "3.4", "RF-BAS"),
    ("OE-03", "Detectar triggers, ventanas T+30, desviaciones y fatiga con control de falsos positivos.", "3.5", "RF-DET"),
    ("OE-04", "Presentar evidencia auditable en Dashboard, historial y visores.", "3.6, 3.7, 3.8, 3.9", "RF-DSH, RF-HIS, RF-VTR, RF-VMA"),
    ("OE-05", "Aprovechar el etiquetado colaborativo para entrenar un clasificador común.", "3.10", "RF-ETQ"),
]
rows = [table_head(["Objetivo", "Descripción", "Secciones", "Requisitos"], [1200, 3900, 1800, 2100])]
for i, (oid, description, sections, reqs) in enumerate(OBJECTIVES):
    fill = ZEBRA if i % 2 else None
    rows.append(
        tr([
            tc(para(run(oid, bold=True, color=BRAND, size=8.6), style="TableText", after=0), 1200, fill=fill),
            tc(para(run(description, size=8.6), style="TableText", after=0), 3900, fill=fill),
            tc(para(run(sections, size=8.6), style="TableText", after=0), 1800, fill=fill),
            tc(para(run(reqs, size=8.4, color=MUTED), style="TableText", after=0), 2100, fill=fill),
        ])
    )
doc.add(table(rows, [1200, 3900, 1800, 2100]))
doc.add(spacer(180))

body(
    "Criterios de aceptación globales: el sistema se considera aceptado cuando un lote real de manos "
    "de Winamax se importa sin duplicados, genera un baseline congelado, produce alertas auditables "
    "y permite recorrer la evidencia hasta la mano concreta."
)

# ---------------------------------------------------------------------------
# 8. Parámetros del producto
# ---------------------------------------------------------------------------

doc.add(page_break())
h1("8. Parámetros del producto")
intro(
    "Los parámetros cerrados se aplican tal cual. Los pendientes se marcan “Por definir” y no se "
    "sustituyen por valores inventados."
)

h2("8.1 Parámetros cerrados")
CLOSED = [
    ("Ventana reactiva por defecto", "T+30"),
    ("Opciones de ventana reactiva", "T+20, T+30, T+50, T+100"),
    ("Equidad mínima del trigger", "70 %"),
    ("Pérdida mínima de bote grande del trigger", "40 BB"),
    ("Pesos provisionales por nivel de juego", "Micro 0,6; Bajo 0,8; Medio 1,0; Alto 1,2; Muy alto 1,4"),
    ("Manos de la ventana reactiva", "30"),
    ("Pausa entre sesiones", "30 minutos sin manos"),
    ("Corrección FDR por defecto", "q < 0,05"),
    ("Opciones de sensibilidad FDR", "q < 0,10, q < 0,05, q < 0,01"),
    ("Intervalo de confianza de la fatiga", "95 %"),
    ("Tramos de fatiga", "Número fijo de puntos y ancho adaptado a las sesiones del baseline (por definir)"),
    ("Resolución mínima de diseño", "1280×720"),
    ("Contraste mínimo", "WCAG AA, 4,5:1 en texto normal"),
    ("Duración de toast de éxito", "6–8 s"),
    ("Toasts apilados", "Máximo 2"),
    ("Formato porcentual", "Un decimal y coma"),
    ("Formato BB/100", "Dos decimales, signo y separador de miles"),
    ("Unidad de análisis", "Ciegas grandes (BB)"),
    ("Precisión de almacenamiento en BB", "Cuatro decimales"),
    ("Tolerancia de validación del bote", "0,001 BB"),
]
rows = [table_head(["Parámetro", "Valor"], [4200, 4800])]
for i, (param, value) in enumerate(CLOSED):
    fill = ZEBRA if i % 2 else None
    rows.append(
        tr([
            tc(para(run(param, size=8.8), style="TableText", after=0), 4200, fill=fill),
            tc(para(run(value, bold=True, size=8.8), style="TableText", after=0), 4800, fill=fill),
        ])
    )
doc.add(table(rows, [4200, 4800]))
doc.add(spacer(200))

h2("8.2 Parámetros pendientes")
PENDING = [
    ("Manos mínimas para crear un baseline", "Modelo y validación"),
    ("Umbral de muestra pequeña del baseline", "Avisos y estados"),
    ("Umbral de obsolescencia del baseline", "Aviso de recalibración"),
    ("Fórmula de la fuga neta", "Alertas y Dashboard"),
    ("Manos mínimas por tramo de fatiga", "Fusión de tramos"),
    ("Separación máxima entre bloques anómalos", "Fusión de intervalos"),
    ("Referencia poblacional MTT para VPIP", "Tarjeta VPIP"),
    ("Taxonomía definitiva de etiquetas", "Nivel 2"),
    ("Alcance del consentimiento colaborativo", "Nivel 2"),
    ("Recuperación ante errores de bloque", "Estados"),
    ("Tiempos de respuesta objetivo", "Rendimiento"),
    ("Tokens de color y valores de contraste", "Accesibilidad"),
    ("Copy exacto de toasts y modales", "Interfaz"),
    ("Definición de torneo con alerta cuando acumula tilt y desviación", "Resumen del lote"),
    ("Librería de evaluación de manos", "Cálculo de equidad"),
    ("Repeticiones de la simulación de equidad", "Cálculo de EV"),
    ("Versión inicial del parser", "Registro canónico"),
]
rows = [table_head(["Parámetro", "Uso"], [5600, 3400])]
for i, (param, use) in enumerate(PENDING):
    fill = ZEBRA if i % 2 else None
    rows.append(
        tr([
            tc(para(run(param, size=8.8), style="TableText", after=0), 5600, fill=fill),
            tc(para(run("Por definir", bold=True, color="B45309", size=8.8), style="TableText", after=0), 3400, fill=fill),
        ])
    )
doc.add(table(rows, [5600, 3400]))
doc.add(spacer(120))
doc.add(
    para(
        run(
            "Los parámetros pendientes no bloquean la arquitectura ni los requisitos funcionales: "
            "determinan valores concretos de validación y presentación.",
            italic=True,
            color=MUTED,
            size=9,
        ),
        style="Caption",
    )
)

# ---------------------------------------------------------------------------
# 9. Fuera de alcance
# ---------------------------------------------------------------------------

doc.add(page_break())
h1("9. Fuera de alcance")
intro("Quedan fuera del MVP y no forman parte de los criterios de aceptación de este documento:")
bullet("HUD en tiempo real.")
bullet("Replayer 3D animado.")
bullet("Cash game.")
bullet("Modo coach.")
bullet("Multisala y multiusuario completo.")
bullet("Versión móvil.")
bullet("Tema claro.")
bullet("Navegación por teclado y lector de pantalla.")
bullet("Descarte o silencio de alertas.")
bullet("Filtros en el feed de alertas.")

# ---------------------------------------------------------------------------
# 10. Referencias
# ---------------------------------------------------------------------------

h1("10. Referencias")
REFS_FINAL = [
    ("Especificación técnica del TFG", "sources/master-doc.txt"),
    ("Prototipo visual", "sources/Mindset-EV-Leak-Finder-TFG.pptx"),
    ("Design Thinking", "sources/design-thinking.pptx"),
]
rows = [table_head(["Documento", "Ruta"], [4200, 4800])]
for i, (name, path) in enumerate(REFS_FINAL):
    fill = ZEBRA if i % 2 else None
    rows.append(
        tr([
            tc(para(run(name, bold=True, size=8.8), style="TableText", after=0), 4200, fill=fill),
            tc(para(run(path, size=8.6, color=MUTED), style="TableText", after=0), 4800, fill=fill),
        ])
    )
doc.add(table(rows, [4200, 4800]))
doc.add(spacer(200))

# ---------------------------------------------------------------------------
# Anexo A. Datos extraídos del historial
# ---------------------------------------------------------------------------

doc.add(page_break())
h1("Anexo A · Datos extraídos del historial")
intro(
    "Este anexo declara todos los datos que el parser obtiene de un historial de Winamax. "
    "No forma parte del recuento de requisitos funcionales: es material de verificación, para que "
    "la procedencia de cada campo pueda contrastarse contra el archivo original."
)

ANNEX_TABLES = [
    (
        "A.1 Torneo",
        [
            ("Id de torneo", "Nombre del archivo; validado con `Table: '…(<id>)#…'`", "Identidad y detección de duplicados"),
            ("Nombre", "`Tournament \"…\"`", "Ficha del torneo e historial"),
            ("Inicio", "`YYYY/MM/DD HH:MM:SS UTC` de la primera mano", "Historial y fatiga"),
            ("Fin", "`YYYY/MM/DD HH:MM:SS UTC` de la última mano", "Duración y fatiga"),
            ("Formato", "`Holdem no limit` y `N-max`", "Ficha del torneo"),
            ("Número de manos", "Recuento de bloques de mano", "Muestra y métricas"),
            ("Rango de manos", "Número original de la primera y la última", "Trazabilidad con Winamax"),
            ("Nivel inicial y final", "`level: N`", "Contexto del torneo"),
            ("Ciegas por tramo", "`(ante/sb/bb)` de cada mano", "Normalización a ciegas grandes"),
        ],
    ),
    (
        "A.2 Mano",
        [
            ("HandId", "`HandId: #…`", "Identidad y auditoría"),
            ("Número original de mano", "Segundo campo del HandId", "Trazabilidad con Winamax"),
            ("Índice propio", "Asignado desde 1 por torneo", "Ventana T+30, tramos y orden"),
            ("Fecha y hora UTC", "Cabecera de la mano", "Sesiones, ventanas y fatiga"),
            ("Nivel de ciegas", "`level: N`", "Contexto de la mano"),
            ("Ante, ciega pequeña y grande", "`(ante/sb/bb)`", "Normalización a ciegas grandes"),
            ("Botón", "`Seat #N is the button`", "Cálculo de posiciones"),
            ("Número de jugadores", "Líneas `Seat`", "Posiciones y contexto"),
            ("Board por calle", "`FLOP`, `TURN`, `RIVER` y `Board:`", "Visor de mano y equidad"),
            ("Bote al cierre de cada calle", "Suma de las aportaciones", "Visor y validación"),
            ("Bote total", "`Total pot N`", "Validación de integridad"),
            ("All-in", "`and is all-in`", "Trigger y EV"),
            ("Showdown", "`*** SHOW DOWN ***`", "WTSD"),
            ("Ganadores", "`collected` y sumario", "Resultado de la mano"),
            ("Descripción de la mano", "`showed … with …`", "Visor de mano"),
            ("Cartas del héroe", "`Dealt to …`", "Métricas y visor"),
            ("Resultado neto", "Cobrado − aportación total", "BB/100 y EV"),
            ("Bote, neto y EV en BB", "Calculados y normalizados", "Dashboard y visores"),
        ],
    ),
    (
        "A.3 Participación en mano",
        [
            ("Nombre y asiento", "`Seat N: nombre (fichas…)`", "Identidad dentro de la mano"),
            ("Stack inicial", "Cifra entre paréntesis del asiento", "Stack en ciegas grandes"),
            ("Posición", "Calculada desde el botón", "Visor y análisis"),
            ("Es el héroe", "Línea `Dealt to`", "Cálculo de métricas"),
            ("Cartas mostradas", "`shows [cartas]`", "Equidad y showdown"),
            ("Aportación total", "Suma de sus acciones en la mano", "Resultado neto"),
            ("Cantidad cobrada", "`collected`", "Resultado neto"),
            ("Resultado neto", "Cobrado − aportación total", "BB/100"),
            ("All-in", "`and is all-in`", "Trigger y EV"),
            ("Estado", "`fold`, `showed`, `won`, `lost`", "WTSD y visor"),
        ],
    ),
    (
        "A.4 Acción",
        [
            ("Jugador", "Prefijo de la línea", "Secuencia y métricas"),
            ("Calle", "`ANTE/BLINDS`, `PRE-FLOP`, `FLOP`, `TURN` y `RIVER`", "Secuencia de la mano"),
            ("Orden", "Posición dentro de la calle", "Reconstrucción cronológica"),
            ("Tipo", "`folds`, `checks`, `calls`, `bets` y `raises`", "Métricas de conducta"),
            ("Importe", "Cifra de la acción", "Bote y EV"),
            ("Importe total", "`to Y` de las subidas", "Validación del bote"),
            ("All-in", "`and is all-in`", "Trigger y EV"),
            ("Bote tras la acción", "Acumulado calculado", "Visor de mano"),
        ],
    ),
    (
        "A.5 Bote",
        [
            ("Tipo", "`from pot`, `from main pot` y `from side pot N`", "Reparto del bote"),
            ("Importe", "`collected N`", "Resultado de la mano"),
            ("Elegibles", "Jugadores cuya aportación alcanza la capa", "Cálculo de side pots"),
            ("Ganador", "Showdown y sumario", "Resultado"),
            ("Bote por capa", "Aportaciones ordenadas", "EV por capas"),
        ],
    ),
    (
        "A.6 Métricas y EV",
        [
            ("VPIP, PFR, 3-Bet y Fold vs 3-Bet", "Calculadas sobre las acciones", "Baseline, ventana y comparativa; VPIP, PFR y 3-Bet también en los tramos"),
            ("WTSD", "Calculada sobre el showdown", "Baseline, ventana y comparativa"),
            ("Numerador y denominador", "Uno por métrica", "FDR y dashboard"),
            ("Equidad", "Calculada en el all-in con cartas conocidas", "Trigger y EV"),
            ("EV y EVbb", "Calculados con reparto por capas", "Visor y EVbb/100"),
        ],
    ),
]

for title, items in ANNEX_TABLES:
    h2(title)
    rows = [table_head(["Dato", "Origen en el .txt", "Uso"], [2600, 3200, 3200])]
    for i, (dato, origen, uso) in enumerate(items):
        fill = ZEBRA if i % 2 else None
        rows.append(
            tr([
                tc(para(run(dato, bold=True, size=8.6), style="TableText", after=0), 2600, fill=fill),
                tc(para(run(origen, size=8.6), style="TableText", after=0), 3200, fill=fill),
                tc(para(run(uso, size=8.6, color=MUTED), style="TableText", after=0), 3200, fill=fill),
            ])
        )
    doc.add(table(rows, [2600, 3200, 3200]))
    doc.add(spacer(160))

note(
    "Datos que se leen y se descartan",
    "El parser lee buy-in, fee, bounty, rake y nombre de la mesa porque aparecen en el archivo, "
    "pero no los almacena. El TFG analiza conducta en ciegas grandes, no retorno económico. "
    "El nombre de la mesa solo se usa para validar el identificador de torneo.",
)
doc.add(spacer(200))

doc.add(
    para(
        run("Fin del documento.", italic=True, color=MUTED, size=9),
        align="center",
    )
)

doc.save(
    OUT,
    title="Mindset & EV Leak Finder — Documento de requisitos funcionales",
    subject="Requisitos funcionales del TFG",
    author="Mario Ramírez García",
)

print(f"Generado: {OUT}")
print(f"Requisitos funcionales: {count}")
print(f"Requisitos no funcionales: {len(NFRS)}")
