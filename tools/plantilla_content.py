"""Contenido de los apartados 7.1.1 a 7.1.5 de la memoria del TFG.

Los datos se han redactado a partir de las 78 fichas de requisitos y de las
decisiones cerradas en docs/01-notas-internas.md. No se inventan umbrales,
etiquetas ni métricas: lo que depende de una decisión abierta se remite a la
sección 8 de la memoria.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# 7.1.1 Product Backlog
# ---------------------------------------------------------------------------

BACKLOG = [
    # E1 · Importar y ordenar
    {
        "id": "HU-01",
        "desc": (
            "Como jugador recreacional, al terminar de jugar quiero soltar el "
            "archivo del torneo y que el sistema me diga qué ha entendido, para "
            "saber que mi sesión ha quedado registrada sin configurar nada."
        ),
        "priority": "Alta",
    },
    {
        "id": "HU-02",
        "desc": (
            "Como jugador semi-profesional, quiero que al importar varios torneos "
            "se detecten los que ya tenía, para no duplicar mi histórico ni "
            "perder tiempo limpiando datos."
        ),
        "priority": "Alta",
    },
    {
        "id": "HU-03",
        "desc": (
            "Como jugador semi-profesional, quiero que las manos se agrupen en la "
            "sesión en la que las jugué, para revisar mi rendimiento como lo viví "
            "y no como archivos sueltos."
        ),
        "priority": "Media",
    },
    # E2 · Revisar en dos minutos
    {
        "id": "HU-04",
        "desc": (
            "Como jugador semi-profesional, al cerrar el ordenador quiero un "
            "resumen que me diga en dos minutos dónde estuvo el problema, para no "
            "pasar horas filtrando manos."
        ),
        "priority": "Alta",
    },
    {
        "id": "HU-05",
        "desc": (
            "Como jugador recreacional, quiero ver mi sesión en una sola gráfica "
            "con las alertas marcadas, para entender qué pasó sin leer números que "
            "no entiendo."
        ),
        "priority": "Alta",
    },
    {
        "id": "HU-06",
        "desc": (
            "Como jugador semi-profesional, quiero saltar de una alerta a la mano "
            "exacta que la provocó, para revisar la decisión sin buscar entre miles "
            "de manos."
        ),
        "priority": "Alta",
    },
    # E3 · Entender qué pasó
    {
        "id": "HU-07",
        "desc": (
            "Como jugador semi-profesional, quiero comparar mi conducta con mi "
            "propia forma de jugar y no con la media de otros, para saber si de "
            "verdad me he desviado."
        ),
        "priority": "Alta",
    },
    {
        "id": "HU-08",
        "desc": (
            "Como jugador semi-profesional, quiero que mi baseline se congele y "
            "pueda recalibrarlo sin perder la versión anterior, para que las "
            "alertas pasadas sigan teniendo sentido."
        ),
        "priority": "Alta",
    },
    {
        "id": "HU-09",
        "desc": (
            "Como jugador recreacional, tras perder un bote grande quiero ver cómo "
            "jugué las manos siguientes, para saber si el bad beat me afectó de "
            "verdad."
        ),
        "priority": "Alta",
    },
    {
        "id": "HU-10",
        "desc": (
            "Como jugador semi-profesional, quiero que el sistema detecte también "
            "los bajones que no vienen de un bad beat, para encontrar fugas que ni "
            "yo mismo noto."
        ),
        "priority": "Alta",
    },
    {
        "id": "HU-11",
        "desc": (
            "Como jugador semi-profesional, quiero saber a partir de qué hora de "
            "sesión mi EV empieza a caer, para decidir si paro o dejo de "
            "registrarme en torneos."
        ),
        "priority": "Media",
    },
    {
        "id": "HU-12",
        "desc": (
            "Como jugador semi-profesional, quiero que una alerta venga con "
            "evidencia suficiente para creérmela, para no cambiar mi forma de "
            "jugar por un aviso que era casualidad."
        ),
        "priority": "Alta",
    },
    # E4 · Decidir y actuar
    {
        "id": "HU-13",
        "desc": (
            "Como jugador recreacional, quiero cerrar el ordenador con una "
            "explicación clara de si perdí por mala suerte o por mal juego, para no "
            "quedarme dándole vueltas."
        ),
        "priority": "Alta",
    },
    {
        "id": "HU-14",
        "desc": (
            "Como jugador semi-profesional, quiero fijar mis propios umbrales de "
            "alerta y de ventana reactiva, para que el sistema se adapte a mi forma "
            "de jugar."
        ),
        "priority": "Media",
    },
    {
        "id": "HU-15",
        "desc": (
            "Como jugador semi-profesional, quiero revisar mi evolución por torneo "
            "y por sesión con filtros, para detectar tendencias a lo largo del mes."
        ),
        "priority": "Media",
    },
    # E5 · Aprender y compartir
    {
        "id": "HU-16",
        "desc": (
            "Como jugador semi-profesional, quiero etiquetar mis jugadas y validar "
            "las de otros, para que el clasificador aprenda de casos reales y no de "
            "etiquetas inventadas."
        ),
        "priority": "Media",
    },
    {
        "id": "HU-17",
        "desc": (
            "Como jugador recreacional, quiero consultar qué significa cada métrica "
            "sin salir de la pantalla, para no depender de un tracker que no "
            "entiendo."
        ),
        "priority": "Baja",
    },
    {
        "id": "HU-18",
        "desc": (
            "Como jugador semi-profesional, quiero saber si mi muestra es suficiente "
            "para fiarme del baseline, para no tomar decisiones con datos de dos "
            "torneos."
        ),
        "priority": "Media",
    },
]

# ---------------------------------------------------------------------------
# 7.1.2 Actores
# ---------------------------------------------------------------------------

ACTORS = [
    {
        "name": "Jugador",
        "desc": (
            "Usuario que crea su cuenta, inicia sesión, importa sus torneos, consulta "
            "su baseline, audita las alertas y etiqueta jugadas. Es el único actor "
            "humano del MVP."
        ),
    },
    {
        "name": "Sistema",
        "desc": (
            "Componente que interpreta los historiales, normaliza los importes, "
            "calcula métricas y EV, agrupa sesiones, detecta anomalías y genera alertas."
        ),
    },
]

# ---------------------------------------------------------------------------
# 7.1.3 Requisitos funcionales
# ---------------------------------------------------------------------------

RFS = [
    {
        "id": "RF-01",
        "name": "Importar archivos de Winamax",
        "desc": (
            "El jugador incorpora uno o varios archivos .txt de torneos MTT de Winamax. "
            "El sistema valida cada archivo, descarta los duplicados y deja el lote preparado "
            "sin incorporar ningún dato hasta la confirmación."
        ),
        "actors": "Jugador y sistema",
        "pre": "Sesión iniciada y baseline activo.",
        "normal": [
            "El jugador abre la pantalla de importación desde la acción «+ Importar Manos» de la cabecera global.",
            "El sistema muestra una pantalla dedicada, no un modal, con un enlace a Mi Baseline.",
            "El jugador selecciona uno o varios archivos .txt o los arrastra a la pantalla; no hay límite de número de archivos ni de tamaño por lote.",
            "El sistema comprueba que cada archivo es un historial de Winamax, no está vacío y es legible.",
            "El sistema obtiene el identificador de torneo del nombre del archivo, asocia cada archivo a un torneo y cuenta las manos detectadas.",
            "El sistema compara el identificador de torneo con los torneos ya guardados.",
            "El sistema muestra los archivos cargados en una lista con su estado y separa los válidos, los inválidos y los duplicados.",
            "El jugador puede quitar cualquier archivo de la lista antes de confirmar; el sistema actualiza la lista y los recuentos.",
            "El jugador confirma la carga para continuar con el resumen del lote.",
        ],
        "alt": [
            "Solo se aceptan archivos con extensión .txt.",
            "Sin baseline activo, la acción «+ Importar Manos» no se muestra y el Dashboard ofrece la guía «Crear baseline», que lleva a Mi Baseline.",
            "La pantalla de importación no permite modificar el baseline.",
            "Si un archivo no es válido, el sistema muestra una ventana emergente con el motivo y pregunta si se continúa con los válidos o se cancela el lote.",
            "Si un torneo ya existe, no se procesa y se informa del duplicado en una ventana emergente.",
            "Si no queda ningún torneo nuevo, no se crea lote y se avisa al jugador.",
            "Quitar un archivo solo afecta al lote pendiente y no modifica los torneos ya importados.",
            "Si se quitan todos los archivos, no se puede continuar y se muestra el estado vacío.",
            "Si el jugador cancela antes de confirmar, no se incorpora ningún dato.",
        ],
        "post": (
            "Existe una lista de archivos válidos y no duplicados, con sus manos detectadas, "
            "sin datos incorporados todavía."
        ),
    },
    {
        "id": "RF-02",
        "name": "Resumir y procesar el lote",
        "desc": (
            "El sistema resume el lote antes de procesarlo, lo ejecuta de forma atómica contra "
            "el baseline activo y comunica el resultado y los errores."
        ),
        "actors": "Jugador y sistema",
        "pre": "Al menos un archivo válido y no duplicado.",
        "normal": [
            "El sistema muestra el resumen previo con archivos cargados, manos detectadas, sesiones del lote y torneos.",
            "El sistema calcula las sesiones del lote en aislamiento, sin consultar las manos ya importadas.",
            "El jugador revisa el resumen y pulsa «Procesar y auditar el lote».",
            "El sistema bloquea la pantalla y muestra el progreso mientras procesa.",
            "El sistema procesa todos los torneos como una unidad atómica.",
            "El sistema crea un lote persistente con identificador, fecha y hora UTC, torneos, manos, sesiones del lote y periodo cubierto.",
            "El sistema lanza la auditoría del Nivel 1 contra el baseline activo.",
            "El sistema abre el Dashboard con el lote cargado.",
        ],
        "alt": [
            "El resumen se actualiza al añadir o quitar archivos y no crea lote ni modifica datos.",
            "La cifra de sesiones se etiqueta «Sesiones del lote» y no representa el total global tras la fusión.",
            "«Cancelar la importación» solo actúa antes de procesar y no deja rastro.",
            "Si un torneo falla, no se guarda ninguno y no se crea lote.",
            "Tras un fallo, el jugador permanece en la pantalla de importación con el error y la opción de reintentar.",
            "Los errores se muestran en una ventana emergente con su causa.",
        ],
        "post": (
            "Lote persistente con su resultado por torneo y la auditoría lanzada, "
            "o ningún cambio si el lote falla."
        ),
    },
    {
        "id": "RF-03",
        "name": "Interpretar y registrar el historial",
        "desc": (
            "El sistema interpreta el historial de cada torneo, reconstruye las manos y produce "
            "un registro canónico, completo, inmutable y validado."
        ),
        "actors": "Sistema",
        "pre": "Archivo validado por la importación.",
        "normal": [
            "El sistema lee el identificador de torneo del nombre del archivo y lo contrasta con el identificador de la mesa.",
            "El sistema identifica cada mano por su HandId, conserva el número original de Winamax y asigna un índice propio desde 1 por torneo.",
            "El sistema construye la ficha del torneo con nombre, identificador, fechas UTC de la primera y la última mano, ciegas y nivel de cada mano y número máximo de jugadores.",
            "El sistema reconstruye jugadores, asientos, stacks al inicio de cada mano, botón y posición relativa; identifica al héroe por la línea «Dealt to» y registra sus cartas. Admite nombres con espacios, puntos, guiones y guiones bajos.",
            "El sistema reconstruye la secuencia de acciones por calle, interpreta «raises X to Y» como importe total Y, registra fold, check, call, bet, raise y all-in, marca los all-in y calcula el bote acumulado al cierre de cada calle.",
            "El sistema reconstruye el bote principal y cada side pot, el showdown, los ganadores y el reparto, incluido el empate; interpreta «collected» como cantidad cobrada, que incluye la aportación propia.",
            "El sistema usa «Total pot» del sumario como validación y comprueba la coherencia de cartas, aportaciones, botes y showdown.",
            "El sistema guarda un registro canónico por mano con la versión del parser.",
        ],
        "alt": [
            "Si el identificador del nombre del archivo no coincide con el de la mesa, el sistema rechaza el archivo. La mesa solo se usa para esa comprobación y no se modela como entidad.",
            "Si una mano no se puede interpretar, el sistema rechaza el archivo completo e indica la línea exacta.",
            "Si la suma de aportaciones no cuadra con el bote del sumario, el sistema rechaza el archivo.",
            "Dos manos con el mismo HandId se consideran la misma mano.",
            "El sistema acepta torneos que empiezan en cualquier número de mano y cambios de jugadores o stacks entre manos.",
            "El sistema no guarda buy-in, fee, bounty ni rake.",
        ],
        "post": (
            "Un registro canónico e inmutable por mano con metadatos, jugadores, acciones, "
            "botes y resultado, reproducible al procesar dos veces el mismo archivo."
        ),
    },
    {
        "id": "RF-04",
        "name": "Normalizar, calcular EV y métricas",
        "desc": (
            "El sistema expresa todos los importes en ciegas grandes, calcula el resultado real "
            "y esperado de los all-in y obtiene las ocho métricas de conducta del héroe."
        ),
        "actors": "Sistema",
        "pre": "Acciones y botes reconstruidos.",
        "normal": [
            "El sistema lee la terna (ante/sb/bb) de la cabecera de cada mano.",
            "El sistema convierte apuestas, botes, stacks, resultado y EV a ciegas grandes usando la ciega grande de esa mano.",
            "El sistema guarda el nivel de ciegas en fichas como contexto y los importes en BB con cuatro decimales; no duplica cada importe en fichas, porque se deriva multiplicando por la ciega grande.",
            "El sistema calcula el resultado real como cantidad cobrada menos la aportación total, incluidas antes y ciegas.",
            "En los all-in con showdown y cartas conocidas, el sistema calcula la equidad y reparte el bote por capas, incluidos los side pots.",
            "El sistema guarda equidad, bote, EV y número de jugadores implicados, y calcula el EV al importar; la equidad se calcula en la ingesta, antes de guardar la mano, y queda vacía en las manos sin all-in.",
            "El sistema obtiene por torneo las BB ganadas (suma del resultado real), el All-in EV (suma del EV) y la suerte esperable en los all-in (σ), y clasifica la suerte del torneo como a favor, neutra o en contra según la diferencia entre ambos frente a σ.",
            "El sistema calcula VPIP, PFR, 3-Bet, Fold vs 3-Bet, C-Bet, Fold vs C-Bet, WTSD y WSSD con numerador y denominador.",
        ],
        "alt": [
            "En manos sin all-in, el EV coincide con el resultado real.",
            "Un torneo sin all-in tiene diferencia nula y suerte neutra.",
            "La suerte se mide con EV y la conducta con frecuencias frente al baseline: la clasificación de suerte no modifica el estado conductual ni las alertas.",
            "El umbral de suerte neutra es 1σ, provisional hasta revisarlo con datos reales.",
            "Solo se ajustan las manos en las que participa el héroe.",
            "La comprobación de aportaciones admite una tolerancia de 0,001 BB.",
            "El cálculo usa una semilla fija para que el resultado sea reproducible.",
        ],
        "post": (
            "Cada mano guarda importes en BB, resultado real, EV y las ocho métricas "
            "con numerador y denominador."
        ),
    },
    {
        "id": "RF-05",
        "name": "Agrupar manos en sesiones",
        "desc": (
            "El sistema ordena todas las manos en una línea temporal única, las agrupa en sesiones "
            "según su continuidad y calcula los agregados de cada sesión."
        ),
        "actors": "Sistema",
        "pre": "Manos normalizadas y registradas.",
        "normal": [
            "El sistema ordena todas las manos por fecha y hora UTC, desempata por HandId cuando comparten el mismo segundo y garantiza que cada mano aparece una sola vez.",
            "El sistema intercala manos de torneos distintos cuando se juegan en paralelo; el orden no depende del orden de importación.",
            "El sistema inicia una sesión nueva cuando la pausa entre dos manos consecutivas supera 30 minutos.",
            "El sistema mantiene en la misma sesión las manos de torneos simultáneos o solapados y todas las manos de un torneo.",
            "El sistema identifica la sesión por su primera mano y calcula inicio, fin, duración, manos, torneos, resultado neto en BB, EV en BB, BB/100 y EVbb/100. No guarda datos económicos; los agregados alimentan el baseline, la gráfica de fatiga y el historial.",
            "Al incorporar un lote, el sistema recalcula las sesiones sobre la línea temporal global.",
            "Si un torneo nuevo elimina el hueco entre dos sesiones, el sistema las fusiona conservando el inicio más antiguo y el fin más reciente.",
        ],
        "alt": [
            "El resumen previo calcula las sesiones del lote en aislamiento y las etiqueta «Sesiones del lote».",
            "La agrupación no usa el día natural ni la fecha de importación.",
            "Si un torneo contiene una pausa interna superior a 30 minutos, el archivo se rechaza y el lote no se procesa; el error indica torneo, manos y pausa detectada.",
            "El recálculo no modifica manos, torneos, alertas ni snapshots; los snapshots conservan las sesiones con las que se calcularon.",
        ],
        "post": (
            "Toda mano pertenece a exactamente un torneo y una sesión; las sesiones son "
            "coherentes, cronológicas y deterministas. Las sesiones no se crean, editan "
            "ni borran a mano y se listan en orden cronológico."
        ),
    },
    {
        "id": "RF-06",
        "name": "Calcular el baseline individual",
        "desc": (
            "El sistema calcula el perfil habitual del jugador sobre las manos del baseline, "
            "exige una muestra mínima y expone el estado del baseline activo."
        ),
        "actors": "Jugador y sistema",
        "pre": "Sesión iniciada. Para el baseline inicial, no existe baseline activo.",
        "normal": [
            "Sin baseline activo, el jugador abre Mi Baseline en estado vacío desde la guía «Crear baseline» del Dashboard.",
            "El jugador arrastra sus archivos .txt; el sistema los valida y los procesa como en una importación, pero como lote de baseline: sirven solo para construir el perfil y no se auditan.",
            "El sistema selecciona las manos cronológicamente anteriores al periodo evaluado.",
            "El sistema calcula VPIP, PFR, 3-Bet y EVbb/100 y pondera cada métrica por el número de manos.",
            "El sistema guarda el numerador y el denominador de cada métrica.",
            "El sistema comprueba que la muestra alcanza el mínimo de 2.000 manos.",
            "El sistema crea el baseline y lo deja activo.",
            "El sistema muestra métricas, muestra, fecha de congelación, versión y si el baseline es inicial o recalibrado.",
        ],
        "alt": [
            "Si la muestra no alcanza las 2.000 manos, no se crea el baseline.",
            "Si alcanza las 2.000 manos pero no las 10.000 recomendadas, se muestra el aviso «muestra pequeña».",
            "El baseline solo usa datos anteriores al periodo evaluado.",
            "Los archivos del lote de baseline no generan alertas ni aparecen en el Historial ni en los visores.",
            "El baseline inicial excluye las ventanas T+30 de los triggers; los tramos de desviación no se excluyen hasta que existe un baseline con el que contrastarlos.",
            "Mientras no exista baseline, «+ Importar Manos» permanece oculto.",
        ],
        "post": (
            "Baseline activo con métricas, muestra y numeradores/denominadores, "
            "o ningún baseline si la muestra es insuficiente."
        ),
    },
    {
        "id": "RF-07",
        "name": "Congelar y recalibrar el baseline",
        "desc": (
            "El sistema conserva cada baseline como snapshot inmutable y versionado, permite "
            "actualizarlo con archivos, sustituirlo o recalibrarlo, permite volver de inmediato a la "
            "composición anterior y conserva las versiones que han dado servicio a alguna alerta."
        ),
        "actors": "Jugador y sistema",
        "pre": "Baseline calculado.",
        "normal": [
            "El sistema congela el baseline como snapshot con identificador, fecha, versión y estado inicial o recalibrado.",
            "El sistema guarda de cada versión los torneos que la componen (un archivo es un torneo), el número de sesiones de la muestra, su origen (inicial, añadir, sustituir o recalibrar) y la versión de la que procede.",
            "Cada alerta conserva el identificador del snapshot con el que se calculó.",
            "El jugador solicita la recalibración con las manos nuevas disponibles.",
            "El sistema recalcula el baseline, excluye automáticamente las ventanas T+30 y los tramos de desviación y conserva las sesiones de fatiga.",
            "El sistema crea una versión nueva y archiva la anterior sin modificarla.",
            "El jugador arrastra archivos .txt de Winamax a Mi Baseline; el sistema muestra una vista previa con las manos detectadas, el total resultante y las métricas del archivo.",
            "El jugador pulsa «Añadir al baseline» y el sistema crea una versión nueva que incluye los archivos anteriores y los nuevos.",
            "Para empezar de cero, el jugador pulsa «Sustituir baseline»; el sistema compara el baseline actual con el resultante y, al confirmar, crea una versión nueva solo con los archivos nuevos. Los archivos anteriores siguen guardados.",
            "Tras añadir o sustituir, un aviso ofrece «Deshacer» o «Restaurar archivos anteriores»; al pulsarlo, el sistema elimina la versión recién creada junto con los archivos, torneos y manos que solo incorporó esa acción, y la versión anterior vuelve a ser la activa.",
        ],
        "alt": [
            "«Descartar» en la vista previa cancela la operación antes de crear ninguna versión.",
            "Añadir y sustituir crean una versión nueva y archivan la anterior; ninguna versión archivada se modifica ni se borra.",
            "El aviso con «Deshacer» o «Restaurar» solo existe al realizar la acción: si el jugador cambia de pestaña o cierra el aviso, ya no puede volver al baseline anterior por esta vía.",
            "Como el aviso desaparece al salir de Mi Baseline, la versión que se elimina nunca ha servido para auditar un lote ni ha generado alertas.",
            "Al deshacer no queda rastro de los archivos subidos por error, de modo que pueden volver a subirse sin que se detecten como duplicados.",
            "No se puede crear una versión con menos de 2.000 manos: el sistema lo indica y el baseline activo no cambia.",
            "Una versión nueva no modifica las versiones anteriores.",
            "La recalibración no altera las alertas ya emitidas.",
            "El aviso de obsolescencia queda fuera del MVP; su umbral está pendiente de definir.",
            "El jugador solo ve el baseline activo; las versiones archivadas se conservan para auditar las alertas y no se consultan desde la interfaz.",
            "Sustituir deja fuera del baseline todos los archivos anteriores, sin importar sus fechas; añadir suma los archivos nuevos a los de la versión activa.",
            "Todos los snapshots archivados se conservan para que cada alerta mantenga el baseline con el que se calculó.",
        ],
        "post": (
            "Snapshot inmutable y versionado, con la versión anterior archivada y las alertas "
            "ligadas al snapshot con el que se calcularon."
        ),
    },
    {
        "id": "RF-08",
        "name": "Detectar el trigger de bad beat",
        "desc": (
            "El sistema identifica las manos que actúan como trigger de una posible reacción "
            "conductual: un bad beat o la pérdida de un bote grande."
        ),
        "actors": "Sistema",
        "pre": "Manos normalizadas y baseline disponible.",
        "normal": [
            "El sistema recorre las manos del lote.",
            "El sistema detecta los bad beats: all-in perdidos por el héroe habiendo entrado con una equidad igual o superior al 70 %.",
            "El sistema detecta las pérdidas de bote grande: manos en las que el héroe pierde 40 BB o más, haya habido all-in o no.",
            "El sistema registra mano, torneo, tipo de trigger, equidad si hubo all-in, bote y resultado.",
            "El sistema genera como máximo un trigger por mano.",
        ],
        "alt": [
            "Si no se puede calcular la equidad, la mano solo puede ser trigger por pérdida de bote grande.",
            "Si la mano no es un bad beat y la pérdida no alcanza los 40 BB, no se genera trigger.",
            "Si una mano cumple las dos condiciones, se registra una sola vez con las dos marcas.",
            "La pérdida mínima de un bad beat está pendiente de definir; el umbral de 40 BB se prevé sustituir por uno relativo al tamaño del stack, fuera del MVP.",
        ],
        "post": "Lista de triggers con su evidencia, sin ventanas ni alertas todavía.",
    },
    {
        "id": "RF-09",
        "name": "Analizar la ventana T+30",
        "desc": (
            "El sistema analiza las 30 manos inmediatamente posteriores a cada trigger, "
            "excluyendo la mano trigger, y contrasta la conducta observada con el baseline."
        ),
        "actors": "Sistema",
        "pre": "Trigger detectado.",
        "normal": [
            "El sistema excluye la mano trigger del análisis.",
            "El sistema toma las 30 manos posteriores dentro del mismo torneo.",
            "El sistema trunca la ventana si el torneo termina antes.",
            "El sistema fusiona las ventanas solapadas y cuenta las manos compartidas una sola vez.",
            "El sistema calcula VPIP, PFR, 3-Bet y EVbb/100 de la ventana.",
            "El sistema contrasta cada métrica con el baseline activo y guarda la diferencia en puntos porcentuales.",
            "El sistema guarda el numerador y el denominador de cada métrica.",
        ],
        "alt": [
            "Si el trigger es la última mano del torneo, la ventana queda vacía y no se analiza.",
            "Si dos triggers se solapan, sus ventanas se fusionan.",
            "El trigger nunca se incluye en la ventana.",
        ],
        "post": (
            "Ventana reactiva con métricas, diferencias frente al baseline y "
            "numeradores/denominadores."
        ),
    },
    {
        "id": "RF-10",
        "name": "Detectar desviaciones sin trigger",
        "desc": (
            "El sistema detecta tramos de conducta sostenidamente distinta al baseline "
            "sin necesidad de un trigger."
        ),
        "actors": "Sistema",
        "pre": "Manos normalizadas y baseline disponible.",
        "normal": [
            "El sistema aplica una ventana deslizante sobre la serie temporal.",
            "El sistema contrasta localmente acciones frente a oportunidades.",
            "El sistema calcula el q-value de cada prueba.",
            "El sistema registra el inicio y el fin de cada tramo candidato.",
            "El sistema fusiona los bloques consecutivos separados por menos de 10 manos.",
            "El tramo fusionado conserva la primera y la última mano.",
        ],
        "alt": [
            "Si un bloque no supera el umbral estadístico, no se considera anómalo.",
            "Si dos bloques están separados por 10 manos o más, se consideran tramos distintos.",
            "La detección no depende de que exista un trigger previo.",
        ],
        "post": "Tramos continuos con inicio, fin, métricas y q-value.",
    },
    {
        "id": "RF-11",
        "name": "Analizar la fatiga",
        "desc": (
            "El sistema mide la evolución del rendimiento esperado a lo largo de las horas "
            "de juego continuo."
        ),
        "actors": "Sistema",
        "pre": "Sesiones y manos normalizadas.",
        "normal": [
            "El sistema calcula el EVbb/100 por tramos de horas de juego.",
            "El sistema construye tramos adaptativos.",
            "El sistema fusiona los tramos que no alcanzan muestra suficiente.",
            "El sistema localiza el punto de cruce a pérdidas.",
            "El sistema guarda desde, hasta, manos, sesiones y EVbb/100 de cada tramo.",
        ],
        "alt": [
            "La fatiga no genera alertas en el feed.",
            "La fatiga solo se visualiza en la gráfica macro.",
            "Si no hay sesiones suficientes, no se construyen tramos.",
        ],
        "post": "Tramos de fatiga con sus métricas, disponibles para la gráfica macro.",
    },
    {
        "id": "RF-12",
        "name": "Corregir FDR y generar alertas",
        "desc": (
            "El sistema controla los falsos positivos mediante la corrección de Benjamini-Hochberg, "
            "transforma las detecciones significativas en alertas auditables y estima su coste "
            "en BB a partir del EV."
        ),
        "actors": "Sistema",
        "pre": "Pruebas estadísticas del lote calculadas.",
        "normal": [
            "El sistema reúne las comparaciones del lote.",
            "El sistema aplica la corrección FDR de Benjamini-Hochberg.",
            "El sistema usa un umbral q configurable, con 0,05 como valor por defecto.",
            "El sistema guarda el q-value de cada prueba.",
            "El sistema descarta como alerta las pruebas que no superan el umbral.",
            "El sistema genera una alerta de tilt por cada ventana T+30 significativa.",
            "El sistema genera una alerta de desviación por cada tramo significativo.",
            "Cada alerta guarda tipo, torneo, evidencia, métricas, snapshot y estado pendiente.",
            "El sistema calcula la fuga neta estimada como max(0, (EVbb/100 del baseline − EVbb/100 observado) × manos / 100): el coste en BB de haber jugado distinto al baseline, medido en EV para no atribuir a la conducta la suerte de los all-in. La interfaz la muestra como magnitud positiva en BB.",
        ],
        "alt": [
            "La fatiga no genera alertas.",
            "Si no hay pruebas significativas, no se genera ninguna alerta.",
            "Una alerta ya emitida no cambia aunque se recalibre el baseline.",
            "Si la ventana o el tramo no tiene EV disponible, la fuga neta queda sin valor y la alerta se muestra igualmente con la indicación «no estimable».",
            "Si la ventana no contiene all-in, el EV de sus manos coincide con el resultado real y la fuga neta se calcula igualmente.",
            "Si el rendimiento de la ventana iguala o supera el del baseline, la fuga neta es 0.",
            "Si el rendimiento esperado del baseline es negativo, la fuga neta se calcula con la misma fórmula.",
        ],
        "post": (
            "Alertas pendientes con evidencia, q-value, snapshot y fuga neta estimada, "
            "o sin valor cuando no hay EV disponible."
        ),
    },
    {
        "id": "RF-13",
        "name": "Dashboard: KPIs y fatiga",
        "desc": (
            "El sistema muestra en el Dashboard el baseline activo, el EVbb/100 con ajuste "
            "all-in y la evolución de la fatiga a lo largo de las horas de sesión."
        ),
        "actors": "Jugador",
        "pre": "Baseline activo.",
        "normal": [
            "El sistema muestra VPIP, PFR, 3-Bet y EVbb/100 con ajuste all-in del snapshot activo; VPIP incluye una referencia poblacional para MTT.",
            "El sistema muestra la muestra, la fecha de congelación y la versión.",
            "El sistema indica si el baseline es inicial o recalibrado.",
            "El sistema dibuja la gráfica de fatiga con los tramos, el cero visible como break-even y el punto crítico de cruce a pérdidas.",
            "El sistema muestra en el tooltip el tramo, el EVbb/100, las manos, las sesiones y el intervalo de confianza.",
        ],
        "alt": [
            "Sin baseline o sin sesiones, el sistema muestra el estado de inicio con la guía «Crear baseline», que lleva a Mi Baseline.",
            "Con baseline y sin lotes auditados, el Dashboard muestra los KPIs y la gráfica de fatiga con la muestra del baseline, un feed sin casos con la acción «Importar Manos» y un panel «Baseline actual»; Historial y Baseline vs Tilt permanecen desactivados hasta auditar el primer lote.",
            "Si un bloque falla, el resto del Dashboard sigue funcionando.",
            "La fatiga no aparece en el feed de alertas.",
        ],
        "post": (
            "Dashboard con los KPIs del baseline y la gráfica de fatiga, sin alertas "
            "de fatiga en el feed."
        ),
    },
    {
        "id": "RF-14",
        "name": "Dashboard: feed y evidencia",
        "desc": (
            "El sistema lista las alertas del último lote, presenta la evidencia de cada una, "
            "permite auditarlas y mantiene la navegación y los estados de la interfaz."
        ),
        "actors": "Jugador",
        "pre": "Lote importado y analizado.",
        "normal": [
            "El sistema muestra el resumen del lote con torneos, manos, fecha de carga, periodo cubierto y porcentaje de manos dentro de ventanas T+30.",
            "El sistema muestra únicamente las alertas del último lote en un feed desplazable.",
            "El sistema ordena primero las alertas de tilt y después las desviaciones; dentro de cada tipo, por magnitud de fuga y, a igualdad, por fecha.",
            "Cada tarjeta muestra tipo, torneo, trigger o métrica, ventana o tramo, valor observado, baseline, delta y fuga neta estimada (magnitud positiva en BB).",
            "Cada métrica muestra su numerador y su denominador.",
            "El jugador pulsa «Auditar» en una tarjeta.",
            "El sistema abre el visor en la mano trigger o en la primera mano del tramo.",
            "La alerta pasa a auditada, desaparece del feed y se conserva en el historial.",
            "La cabecera global permanece visible y permite navegar al Dashboard, Historial de torneos, Baseline, Baseline vs Tilt (T+30) y Glosario; el ítem activo se marca fuera del Dashboard.",
            "Cada bloque del Dashboard dispone de estados de vacío, carga, error, parcial y sin permisos.",
        ],
        "alt": [
            "Si el lote no tiene alertas, el feed muestra el estado vacío; si aún no se ha auditado ningún lote, indica que todavía no hay casos que auditar.",
            "Si una alerta no se puede auditar, el sistema muestra el error y la conserva pendiente.",
            "Un error en un bloque no impide el funcionamiento del resto.",
            "Los toasts de éxito se cierran solos; los errores permanecen hasta que el usuario los cierra.",
            "Estados y alertas combinan color, icono y texto.",
        ],
        "post": (
            "Alertas auditadas conservadas en el historial y feed del último lote actualizado."
        ),
    },
    {
        "id": "RF-15",
        "name": "Historial de torneos",
        "desc": (
            "El sistema lista los torneos procesados, permite filtrarlos y clasifica cada torneo "
            "según la evidencia conductual disponible."
        ),
        "actors": "Jugador",
        "pre": "Al menos un lote importado.",
        "normal": [
            "El sistema lista los torneos con torneo, fecha, manos, BB ganadas, All-in EV, suerte all-in, estado conductual y acción.",
            "El sistema muestra BB ganadas y All-in EV en verde si son positivas y en rojo si son negativas, y la suerte all-in (a favor, neutra o en contra) sin color.",
            "El sistema ofrece un ⓘ en las cabeceras de BB ganadas, All-in EV y suerte all-in, con una definición breve y el enlace «Ver en el Glosario».",
            "El sistema ordena por fecha descendente y pagina cuando el listado supera el tamaño de página.",
            "El jugador filtra por estado conductual, periodo y formato de torneo.",
            "El sistema combina los filtros y permite limpiarlos.",
            "El sistema asigna a cada torneo el estado tilt, desviación o sin alertas.",
            "El jugador selecciona una fila y abre el visor del torneo.",
            "El sistema conserva los torneos auditados y el snapshot con el que se evaluaron.",
        ],
        "alt": [
            "Si no hay torneos, el historial muestra el estado vacío.",
            "La importación de un lote nuevo no elimina los torneos anteriores.",
            "Hasta que se audita el primer lote, el acceso al Historial está desactivado.",
            "El Historial no muestra VPIP ni PFR por torneo, porque en torneos cortos las métricas inducen a error; la conducta se comunica con el estado y las alertas.",
            "El orden de prioridad es tilt, desviación y sin alertas.",
        ],
        "post": (
            "Historial persistente, filtrable y con el estado conductual de cada torneo."
        ),
    },
    {
        "id": "RF-16",
        "name": "Visor de torneo",
        "desc": (
            "El sistema representa la evolución acumulada del resultado real y del EV, "
            "resalta las anomalías y permite navegar a la mano correspondiente."
        ),
        "actors": "Jugador",
        "pre": "Torneo seleccionado.",
        "normal": [
            "El sistema muestra la evolución acumulada de fichas reales en ciegas grandes y el EV esperado mano a mano.",
            "El sistema usa el número de mano como eje X y comparte escala y ejes entre ambas series.",
            "El sistema resalta la ventana T+30 en rojo y el tramo de desviación en ámbar.",
            "El tooltip identifica el tipo de anomalía y sus métricas.",
            "El jugador selecciona un punto de la gráfica y abre la mano correspondiente.",
            "El sistema permite avanzar y retroceder mano a mano conservando el contexto del torneo.",
            "El sistema muestra en la cabecera el torneo, el formato y el número de manos, y un subtítulo fijo de la gráfica («Resultado real frente a EV esperado, mano a mano»).",
            "El sistema presenta en el panel derecho un único bloque «Lectura» con dos partes: Conducta y Suerte del torneo.",
            "La parte Suerte del torneo muestra las BB ganadas, el All-in EV y la suerte all-in del torneo, con un ⓘ y el enlace «Ver en el Glosario».",
            "En un torneo con ventana T+30, la parte Conducta muestra el trigger, la posición de la mano dentro de la ventana, las métricas de la alerta frente al baseline y la fuga neta estimada, con un ⓘ.",
            "En un torneo con desviación sin trigger, la parte Conducta muestra solo las métricas de la alerta frente al baseline, sin fuga neta ni inicio y fin de tramo.",
            "En un torneo sin alertas, la parte Conducta indica que no se han detectado anomalías conductuales frente al baseline, sin métricas del torneo.",
        ],
        "alt": [
            "Si el torneo no tiene anomalías, la gráfica se muestra sin franjas.",
            "La navegación conserva siempre el torneo seleccionado.",
            "Un torneo sin all-in muestra la suerte all-in como neutra.",
            "El visor no muestra «resultado adicional» ni subtramos dentro de la ventana T+30: la ventana se lee como un todo de 30 manos.",
        ],
        "post": (
            "Visor del torneo con gráfica dual, franjas de anomalías y navegación a la mano."
        ),
    },
    {
        "id": "RF-17",
        "name": "Visor de mano",
        "desc": (
            "El sistema muestra la mano completa, su contexto conductual y permite recorrer "
            "el torneo y validar la etiqueta comunitaria."
        ),
        "actors": "Jugador",
        "pre": "Mano seleccionada.",
        "normal": [
            "El sistema muestra metadatos, cartas del héroe, cartas de los rivales y cartas comunitarias.",
            "El sistema muestra bote, ciegas, posición, stack, resultado real y EV de la mano.",
            "El sistema reconstruye preflop, flop, turn y river con la acción y el importe de cada jugador.",
            "El sistema resalta las acciones del héroe.",
            "El sistema indica si la mano pertenece a una ventana T+30 o a un tramo de desviación.",
            "El sistema muestra la equidad, el resultado esperado y el baseline aplicable a la métrica observada.",
            "El sistema permite avanzar y retroceder a la mano anterior o siguiente y ofrece la acción «Siguiente en T+30» cuando la mano pertenece a una ventana.",
            "El sistema muestra la etiqueta sugerida y permite aceptarla o cambiarla desde el catálogo.",
        ],
        "alt": [
            "Una alerta de tilt abre la mano trigger; una alerta de desviación abre la primera mano del tramo.",
            "La mano abierta queda resaltada dentro de la secuencia.",
            "Si no hay etiqueta sugerida, el sistema permite elegirla del catálogo.",
        ],
        "post": (
            "Mano mostrada con su contexto, navegación y etiqueta validada registrada "
            "para el Nivel 2."
        ),
    },
    {
        "id": "RF-18",
        "name": "Etiquetar jugadas del Nivel 2",
        "desc": (
            "El sistema permite etiquetar jugadas, validar las etiquetas y entrenar un clasificador "
            "común sin alterar el diagnóstico individual del Nivel 1."
        ),
        "actors": "Jugador y sistema",
        "pre": "Acceso al visor de mano.",
        "normal": [
            "El sistema dispone de un catálogo versionado de etiquetas con nombre, definición y ejemplo.",
            "El jugador registra una etiqueta por mano; el sistema guarda usuario, fecha y origen de la etiqueta.",
            "El sistema ofrece aceptar la sugerencia o cambiarla y exige una acción explícita de validación.",
            "El sistema asigna un peso a cada etiqueta según el nivel de juego declarado por el jugador y guarda el peso y el nivel aplicados.",
            "El sistema entrena un clasificador multiclase con las etiquetas validadas y registra la versión y la fecha de entrenamiento.",
            "El sistema mantiene la etiqueta separada del baseline y de las alertas ya emitidas.",
        ],
        "alt": [
            "Las etiquetas sin validar no se usan para entrenar.",
            "No se usan etiquetas sin consentimiento.",
            "El jugador puede retirar el consentimiento.",
            "Los pesos por nivel de juego son provisionales (Micro 0,6, Bajo 0,8, Medio 1,0, Alto 1,2 y Muy alto 1,4) y se calibrarán con datos reales; la taxonomía y el consentimiento están pendientes de definir.",
        ],
        "post": (
            "Etiquetas validadas, ponderadas y disponibles para el clasificador, sin efecto "
            "sobre el Nivel 1."
        ),
    },
    {
        "id": "RF-19",
        "name": "Glosario y ayuda contextual",
        "desc": (
            "El sistema ofrece un glosario consultable con los términos del producto y enlaza "
            "cada métrica con su término correspondiente."
        ),
        "actors": "Jugador",
        "pre": "Sesión iniciada.",
        "normal": [
            "El sistema muestra los términos ordenados alfabéticamente.",
            "El sistema ofrece un buscador.",
            "Cada término incluye definición y ejemplo.",
            "Desde un modal de métrica o un tooltip, el sistema enlaza con el término concreto.",
            "El glosario conserva el contexto de la pantalla de origen.",
            "El glosario incluye BB ganadas, All-in EV, suerte all-in y fuga neta, con su definición y un ejemplo.",
        ],
        "alt": [
            "Si el término no existe, el buscador muestra un estado vacío.",
            "El enlace abre el término concreto y no la portada del glosario.",
        ],
        "post": "Glosario consultable y enlaces contextuales operativos.",
    },
    {
        "id": "RF-20",
        "name": "Cuenta, registro y configuración",
        "desc": (
            "El sistema permite crear una cuenta, autentica al jugador, aísla sus datos "
            "y permite ajustar la ventana reactiva y la sensibilidad estadística para el "
            "siguiente lote."
        ),
        "actors": "Jugador y sistema",
        "pre": "Acceso a la aplicación sin sesión iniciada.",
        "normal": [
            "El jugador crea una cuenta con nombre, correo, contraseña y su nivel de juego (el buy-in en el que suele jugar sus MTT) desde la pantalla de acceso; hay cinco tramos (1–5 €, 5–10 €, 10–25 €, 25–50 € y 50 € o más); cada tramo tiene un peso provisional para ponderar las etiquetas (Micro 0,6, Bajo 0,8, Medio 1,0, Alto 1,2 y Muy alto 1,4).",
            "El sistema comprueba que el correo y el nombre no estén registrados y que la contraseña cumpla los requisitos mínimos, pendientes de definir.",
            "El sistema crea la cuenta con la contraseña almacenada como hash y sal, y permite iniciar sesión.",
            "El sistema exige credenciales válidas y mantiene la sesión hasta el cierre o la expiración.",
            "El sistema muestra en el drawer de cuenta el usuario, el sitio activo, el estado, el nivel de juego, la versión del motor y la última recalibración.",
            "El jugador ajusta la ventana reactiva entre T+20, T+30, T+50 y T+100.",
            "El jugador ajusta la sensibilidad FDR entre q < 0,10, q < 0,05 y q < 0,01.",
            "El jugador puede cambiar su nivel de juego desde el drawer; el cambio afecta solo a las etiquetas que registre a partir de ese momento.",
            "El sistema guarda los cambios de forma explícita; la ventana reactiva y la sensibilidad se aplican solo al siguiente lote.",
            "El sistema aísla manos, baseline y alertas por usuario, sitio y formato.",
            "El jugador cierra la sesión con confirmación y el sistema invalida la sesión.",
        ],
        "alt": [
            "Si el correo o el nombre ya existen, no se crea la cuenta y el aviso no revela datos de la cuenta existente.",
            "Si la contraseña no cumple los requisitos mínimos, no se crea la cuenta y se indica qué falta.",
            "Si el alta falla, no se guarda ningún dato de la cuenta.",
            "El error de acceso no revela si el usuario existe.",
            "Si se cierra el drawer con cambios sin guardar, se pide confirmación.",
            "La interfaz no ofrece cambio de usuario, sitio ni formato.",
            "El sitio activo es Winamax y el formato es MTT.",
        ],
        "post": (
            "Cuenta creada, sesión autenticada, datos aislados y configuración aplicada "
            "al siguiente lote."
        ),
    },
    {
        "id": "RF-21",
        "name": "Comparar el baseline con las ventanas T+30",
        "desc": (
            "El sistema compara, en una pantalla propia, la conducta del jugador en las "
            "ventanas T+30 del último lote con su baseline activo, con cinco métricas, su "
            "diferencia en puntos porcentuales y su significación tras la corrección FDR."
        ),
        "actors": "Jugador y sistema",
        "pre": "Baseline activo y al menos un lote auditado.",
        "normal": [
            "El jugador abre «Baseline vs Tilt (T+30)» desde la navegación global.",
            "El sistema reúne las ventanas T+30 del último lote auditado y las compara con el baseline activo.",
            "El sistema muestra las manos del baseline, las manos dentro de ventanas T+30 y el número de episodios.",
            "El sistema muestra tres indicadores: la desviación de VPIP en puntos porcentuales, la agresividad impulsiva (desviación de 3-Bet) y la fuga neta acumulada de las ventanas.",
            "El sistema representa, para VPIP, PFR, 3-Bet, Fold vs 3-Bet y WTSD, el valor del baseline frente al de las ventanas y su diferencia en puntos porcentuales.",
            "El sistema contrasta cada métrica con el baseline, aplica la corrección FDR con el umbral q configurado y muestra cuántas de las cinco métricas son significativas.",
            "El sistema ofrece una explicación de lectura: qué es el baseline, qué es una ventana T+30, qué significa q y qué no demuestra la comparación.",
        ],
        "alt": [
            "¡El alcance de la comparativa (último lote, periodo o histórico) es algo que está por estudiar todavía! De momento solo agrega las ventanas del último lote.",
            "La comparación usa el baseline activo, no el snapshot de cada alerta; las alertas ya emitidas no cambian.",
            "Si el último lote no contiene ventanas T+30, la pantalla muestra un estado vacío y no calcula ninguna comparación.",
            "Hasta que se audita el primer lote, el acceso a la pantalla está desactivado.",
            "Cada métrica guarda su numerador y su denominador.",
            "La comparación mide un patrón repetido: no demuestra intención ni explica la causa.",
            "Si el tilt solo mueve una métrica, la lectura lo trata como un ajuste técnico; si se separan a la vez VPIP y 3-Bet, apunta a descontrol emocional.",
        ],
        "post": (
            "Comparativa agregada del último lote con cinco métricas, su diferencia con el "
            "baseline activo y su significación tras la corrección FDR."
        ),
    },
]

# ---------------------------------------------------------------------------
# 7.1.4 Requisitos no funcionales
# ---------------------------------------------------------------------------

RNFS = [
    {
        "id": "RNF-01",
        "name": "Usabilidad",
        "desc": (
            "La interfaz debe poder utilizarse sin formación previa y sin conocer la "
            "terminología estadística."
        ),
        "crit": [
            "El diseño es desktop-first y se valida desde 1280×720.",
            "El flujo importar, revisar el Dashboard y auditar se completa sin cambiar de contexto.",
            "Cada métrica dispone de ayuda contextual.",
            "Todos los textos de la interfaz están en español.",
        ],
        "ver": "Prueba de usuario con el prototipo y revisión heurística.",
    },
    {
        "id": "RNF-02",
        "name": "Accesibilidad",
        "desc": (
            "La interfaz debe ser legible y comprensible para personas con limitaciones "
            "visuales o cognitivas."
        ),
        "crit": [
            "El contraste cumple WCAG AA, con un mínimo de 4,5:1 en texto normal.",
            "Estados y alertas combinan color, icono y texto.",
            "Las gráficas incluyen etiquetas y descripciones textuales.",
        ],
        "ver": "Auditoría de contraste y revisión de componentes.",
    },
    {
        "id": "RNF-03",
        "name": "Rendimiento",
        "desc": (
            "El sistema debe procesar los lotes sin bloquear la interfaz y mostrar el "
            "Dashboard con rapidez."
        ),
        "crit": [
            "La interfaz permanece operable durante el análisis de un lote.",
            "El procesamiento se ejecuta por lotes.",
            "El Dashboard lee el último lote sin recalcular el histórico completo.",
            "El Dashboard con el último lote se muestra en menos de 2 segundos.",
            "El procesamiento de 10.000 manos termina en menos de 60 segundos en el equipo de referencia.",
        ],
        "ver": "Medición sobre un lote de prueba con el volumen de la demo.",
    },
    {
        "id": "RNF-04",
        "name": "Seguridad",
        "desc": (
            "El sistema debe proteger las credenciales y aislar los datos de cada usuario."
        ),
        "crit": [
            "El acceso requiere autenticación.",
            "Las contraseñas se almacenan con hash y sal.",
            "El transporte utiliza HTTPS.",
            "Cada consulta se limita al usuario autenticado.",
        ],
        "ver": "Revisión de configuración y pruebas de acceso cruzado.",
    },
    {
        "id": "RNF-05",
        "name": "Privacidad",
        "desc": (
            "El sistema debe recoger solo los datos necesarios y respetar el consentimiento "
            "del usuario."
        ),
        "crit": [
            "Solo se solicitan los datos imprescindibles para el análisis.",
            "El Nivel 2 requiere consentimiento explícito.",
            "El consentimiento se puede retirar.",
            "Las etiquetas comunitarias no exponen la identidad del jugador.",
        ],
        "ver": "Revisión del flujo de consentimiento y de los datos almacenados.",
    },
    {
        "id": "RNF-06",
        "name": "Integridad y auditabilidad",
        "desc": (
            "El sistema debe conservar la trazabilidad de cada alerta e impedir que el "
            "baseline se contamine."
        ),
        "crit": [
            "El baseline es inmutable y versionado.",
            "Cada alerta guarda el snapshot con el que se calculó.",
            "Cada métrica guarda numerador y denominador.",
            "Cada prueba estadística conserva su q-value.",
            "La demo utiliza manos reales.",
        ],
        "ver": "Revisión de la base de datos y reproducción de una alerta.",
    },
    {
        "id": "RNF-07",
        "name": "Mantenibilidad",
        "desc": (
            "El sistema debe organizarse en módulos desacoplados que permitan sustituir "
            "o ampliar componentes."
        ),
        "crit": [
            "La arquitectura separa ingesta, dominio, análisis, API y frontend.",
            "Los módulos se comunican mediante contratos explícitos.",
            "La API REST está documentada.",
            "Parser, baseline y detectores disponen de pruebas automatizadas.",
            "La configuración está externalizada.",
        ],
        "ver": "Revisión de la arquitectura y ejecución de la suite de pruebas.",
    },
    {
        "id": "RNF-08",
        "name": "Compatibilidad",
        "desc": (
            "El sistema debe funcionar en el entorno de escritorio definido para el MVP."
        ),
        "crit": [
            "Funciona en las últimas versiones de los navegadores de escritorio mayoritarios.",
            "La resolución mínima soportada es 1280×720.",
            "No existe versión móvil en el MVP.",
        ],
        "ver": "Prueba en los navegadores soportados.",
    },
    {
        "id": "RNF-09",
        "name": "Idioma y formato",
        "desc": (
            "El sistema debe presentar la información con el idioma y el formato numérico "
            "definidos."
        ),
        "crit": [
            "La interfaz está en español.",
            "Los textos están externalizados.",
            "Las fechas se guardan en UTC y se muestran en la zona local.",
            "Los porcentajes usan coma decimal y un decimal.",
            "Las cifras de BB/100 usan dos decimales, signo y separador de miles.",
        ],
        "ver": "Revisión de textos y de formato en la interfaz.",
    },
    {
        "id": "RNF-10",
        "name": "Trazabilidad",
        "desc": (
            "El sistema debe permitir reconstruir por qué se emitió cada alerta."
        ),
        "crit": [
            "Cada alerta enlaza con la mano o el tramo que la origina.",
            "Cada métrica conserva su origen y su muestra.",
            "La versión del motor es visible.",
            "El historial conserva las alertas auditadas.",
        ],
        "ver": "Auditoría de una alerta de principio a fin.",
    },
    {
        "id": "RNF-11",
        "name": "Recuperación",
        "desc": (
            "El sistema debe aislar los fallos y conservar los datos ya confirmados."
        ),
        "crit": [
            "Un error en un bloque no tumba el Dashboard.",
            "Los estados parciales indican qué información falta.",
            "Un lote confirmado no se pierde ante un error de la interfaz.",
            "La recuperación reintenta el bloque fallido sin perder el lote confirmado.",
            "Si el fallo persiste, el bloque queda en estado parcial y se ofrece recargarlo.",
        ],
        "ver": "Prueba de fallo inducido por bloque.",
    },
]

# ---------------------------------------------------------------------------
# 7.1.5 Requisitos de almacenamiento de información
# ---------------------------------------------------------------------------

RIS = [
    {
        "id": "RI-01",
        "name": "Usuario",
        "desc": "Cuenta y preferencias del jugador.",
        "attrs": "id, nombre, email, sitio activo, nivel de juego, consentimiento",
    },
    {
        "id": "RI-02",
        "name": "Torneo",
        "desc": "Unidad de competición que agrupa manos.",
        "attrs": (
            "id, nombre, fecha inicio, fecha fin, nivel inicial, nivel final, "
            "formato, manos, BB ganadas, All-in EV, σ de suerte, suerte all-in"
        ),
    },
    {
        "id": "RI-03",
        "name": "Sesión",
        "desc": "Bloque continuo de manos separadas por pausas no superiores al umbral.",
        "attrs": (
            "id, primera mano, inicio, fin, duración, manos, torneos, sitio, formato, "
            "resultado_bb, ev_bb, bb100, evbb100"
        ),
    },
    {
        "id": "RI-04",
        "name": "Mano",
        "desc": "Registro canónico de una mano.",
        "attrs": (
            "id, hand_id, índice propio, número original, torneo, timestamp UTC, "
            "ante, SB, BB, board, bote_bb, net_bb, ev_bb, versión del EV, equidad, all_in, "
            "showdown"
        ),
    },
    {
        "id": "RI-05",
        "name": "Participación en mano",
        "desc": "Intervención de un jugador en una mano.",
        "attrs": (
            "mano, jugador, asiento, posición, stack_bb, aportación_bb, cobrado_bb, "
            "neto_bb, cartas, all_in, estado"
        ),
    },
    {
        "id": "RI-06",
        "name": "Acción",
        "desc": "Intervención de un jugador en una calle.",
        "attrs": (
            "id, mano, jugador, calle, orden, tipo, importe_bb, importe_total_bb, "
            "all_in, bote_bb"
        ),
    },
    {
        "id": "RI-07",
        "name": "Snapshot de baseline",
        "desc": "Versión congelada del baseline.",
        "attrs": "id, fecha, estado, muestra, sesiones, métricas, versión, origen, versión padre",
    },
    {
        "id": "RI-08",
        "name": "Alerta",
        "desc": "Detección significativa con evidencia.",
        "attrs": "id, tipo, torneo, métricas, snapshot, estado",
    },
    {
        "id": "RI-09",
        "name": "Ventana reactiva",
        "desc": "Ventana T+30 asociada a un trigger.",
        "attrs": "id, trigger, inicio, fin, métricas",
    },
    {
        "id": "RI-10",
        "name": "Tramo de desviación",
        "desc": "Intervalo continuo con sobrefrecuencia.",
        "attrs": "id, inicio, fin, métricas, q-value",
    },
    {
        "id": "RI-11",
        "name": "Tramo de fatiga",
        "desc": "Intervalo de horas con EVbb/100.",
        "attrs": "id, desde, hasta, manos, sesiones, evbb100",
    },
    {
        "id": "RI-12",
        "name": "Lote de importación",
        "desc": "Conjunto de torneos incorporados en una operación de importación.",
        "attrs": (
            "id, tipo (baseline o auditoría), fecha UTC, torneos, manos, sesiones, periodo"
        ),
    },
    {
        "id": "RI-13",
        "name": "Etiqueta",
        "desc": "Etiqueta semántica del Nivel 2.",
        "attrs": "id, nombre, definición, versión, peso",
    },
    {
        "id": "RI-14",
        "name": "Etiqueta de mano",
        "desc": "Asignación validada de una etiqueta.",
        "attrs": "id, mano, usuario, etiqueta, fecha, nivel de juego aplicado, peso",
    },
    {
        "id": "RI-15",
        "name": "Trigger",
        "desc": "Evento gatillo que abre una ventana reactiva.",
        "attrs": (
            "id, mano, torneo, ventana, tipo, equidad, bote_bb, pérdida_bb, "
            "umbral de equidad, umbral de pérdida"
        ),
    },
    {
        "id": "RI-16",
        "name": "Prueba estadística",
        "desc": "Comparación de una métrica sometida a la corrección FDR.",
        "attrs": (
            "id, lote, tipo, referencia, métrica, observado, esperado, "
            "p-value, q-value, significativa"
        ),
    },
]


# ---------------------------------------------------------------------------
# 7.4.1 Casos de uso
# ---------------------------------------------------------------------------

CASOS_USO = [
    {
        "id": "RF-01",
        "name": "Importar archivos de Winamax",
        "pos_prueba": (
            "El jugador abre «+ Importar Manos» con baseline activo, arrastra tres "
            "archivos .txt de torneos Winamax no importados y quita uno de la lista "
            "antes de confirmar."
        ),
        "pos_salida": (
            "La lista se actualiza a dos archivos válidos, con sus manos detectadas y "
            "los recuentos ajustados, y permite confirmar la carga sin incorporar datos "
            "todavía."
        ),
        "neg_prueba": (
            "El jugador arrastra un archivo .pdf y un .txt de un torneo ya importado."
        ),
        "neg_salida": (
            "El .pdf se rechaza por extensión y el .txt se marca como duplicado; "
            "el motivo se muestra en una ventana emergente y no se crea lote."
        ),
    },
    {
        "id": "RF-02",
        "name": "Resumir y procesar el lote",
        "pos_prueba": (
            "El jugador confirma un lote de dos torneos válidos y pulsa "
            "«Procesar y auditar el lote»."
        ),
        "pos_salida": (
            "Se crea un lote persistente con torneos, manos, sesiones del lote y "
            "periodo; la auditoría se lanza y se abre el Dashboard con el lote cargado."
        ),
        "neg_prueba": "Uno de los dos torneos falla durante el procesamiento.",
        "neg_salida": (
            "No se guarda ningún torneo, no se crea lote y el jugador permanece en "
            "la pantalla de importación con el error y la opción de reintentar."
        ),
    },
    {
        "id": "RF-03",
        "name": "Interpretar y registrar el historial",
        "pos_prueba": (
            "Se procesa un archivo con manos completas, all-in con showdown y side pots."
        ),
        "pos_salida": (
            "Cada mano genera un registro canónico con metadatos, jugadores, acciones, "
            "botes y resultado; el índice propio empieza en 1 y se conserva el número original."
        ),
        "neg_prueba": (
            "Se procesa un archivo con una línea de acción corrupta o con aportaciones "
            "que no cuadran con el bote del sumario."
        ),
        "neg_salida": (
            "El archivo completo se rechaza y el error indica la línea exacta; no se "
            "guarda ninguna mano."
        ),
    },
    {
        "id": "RF-04",
        "name": "Normalizar, calcular EV y métricas",
        "pos_prueba": (
            "Se procesa una mano con all-in pagado y cartas conocidas de ambos jugadores."
        ),
        "pos_salida": (
            "Los importes quedan en BB con cuatro decimales y se guardan la equidad, "
            "el EV por capas y las ocho métricas con numerador y denominador; el "
            "torneo acumula BB ganadas, All-in EV y suerte esperable."
        ),
        "neg_prueba": "Se procesa una mano sin all-in.",
        "neg_salida": (
            "El EV coincide con el resultado real, la equidad queda vacía, la mano no "
            "genera ajuste EV y las métricas se calculan igualmente; un torneo sin "
            "all-in tiene suerte neutra."
        ),
    },
    {
        "id": "RF-05",
        "name": "Agrupar manos en sesiones",
        "pos_prueba": (
            "Se importan dos torneos cuyas manos se intercalan y con pausas inferiores "
            "a 30 minutos."
        ),
        "pos_salida": (
            "Las manos se ordenan en una línea temporal única y forman una sola sesión "
            "con sus agregados en BB y BB/100."
        ),
        "neg_prueba": "Se importa un torneo con una pausa interna de 45 minutos.",
        "neg_salida": (
            "El archivo se rechaza, el lote no se procesa y el error indica torneo, "
            "manos y pausa detectada."
        ),
    },
    {
        "id": "RF-06",
        "name": "Calcular el baseline individual",
        "pos_prueba": (
            "Un jugador sin baseline abre Mi Baseline vacío desde el Dashboard y arrastra "
            "archivos con más de 2.000 manos."
        ),
        "pos_salida": (
            "Se crea un baseline activo con VPIP, PFR, 3-Bet, EVbb/100, muestra, fecha "
            "y versión, guardando numerador y denominador de cada métrica; esos archivos "
            "no generan alertas ni aparecen en el Historial."
        ),
        "neg_prueba": (
            "El jugador solicita el baseline con una muestra inferior al mínimo definido."
        ),
        "neg_salida": "No se crea baseline y el sistema indica que la muestra es insuficiente.",
    },
    {
        "id": "RF-07",
        "name": "Congelar y recalibrar el baseline",
        "pos_prueba": "El jugador añade un archivo al baseline, pulsa «Deshacer» y recalibra con manos nuevas.",
        "pos_salida": (
            "Añadir crea una versión nueva; deshacer la elimina con los archivos que subió y la "
            "versión anterior vuelve a ser la activa; recalibrar crea otra versión y archiva la anterior sin cambios. "
            "Las alertas conservan el snapshot con el que se calcularon."
        ),
        "neg_prueba": "El jugador sustituye el baseline por un archivo con menos de 2.000 manos.",
        "neg_salida": (
            "No se crea ninguna versión, el sistema indica que la muestra es insuficiente y "
            "el baseline activo no cambia."
        ),
    },
    {
        "id": "RF-08",
        "name": "Detectar el trigger de bad beat",
        "pos_prueba": (
            "Se procesa una mano con all-in del héroe, equidad favorable del 75 % y "
            "pérdida de 50 BB, y otra mano sin all-in en la que el héroe pierde 45 BB."
        ),
        "pos_salida": "Se genera un trigger por cada mano, con tipo, torneo, bote y resultado, y con la equidad cuando hubo all-in.",
        "neg_prueba": (
            "Se procesa una mano sin all-in en la que el héroe pierde 25 BB."
        ),
        "neg_salida": "No se genera trigger porque no es un bad beat y la pérdida no alcanza los 40 BB.",
    },
    {
        "id": "RF-09",
        "name": "Analizar la ventana T+30",
        "pos_prueba": "Se detecta un trigger con 40 manos posteriores en el mismo torneo.",
        "pos_salida": (
            "Se analizan las 30 manos posteriores sin incluir el trigger y se guardan "
            "métricas, diferencias frente al baseline y numeradores/denominadores."
        ),
        "neg_prueba": "Dos triggers consecutivos generan ventanas solapadas.",
        "neg_salida": "Las ventanas se fusionan y las manos compartidas se cuentan una sola vez.",
    },
    {
        "id": "RF-10",
        "name": "Detectar desviaciones sin trigger",
        "pos_prueba": (
            "Se procesa un tramo de manos con sobrefrecuencia sostenida y sin trigger previo."
        ),
        "pos_salida": "Se registra un tramo con inicio, fin, métricas y q-value.",
        "neg_prueba": "El tramo no supera el umbral estadístico.",
        "neg_salida": "No se considera anómalo y no se genera tramo.",
    },
    {
        "id": "RF-11",
        "name": "Analizar la fatiga",
        "pos_prueba": "Se procesan sesiones con varias horas de juego continuo.",
        "pos_salida": (
            "Se construyen tramos de fatiga con desde, hasta, manos, sesiones y EVbb/100, "
            "disponibles para la gráfica macro."
        ),
        "neg_prueba": "La fatiga detecta un tramo con EVbb/100 negativo.",
        "neg_salida": (
            "El tramo se muestra en la gráfica macro, pero no genera ninguna alerta en el feed."
        ),
    },
    {
        "id": "RF-12",
        "name": "Corregir FDR y generar alertas",
        "pos_prueba": (
            "El lote produce varias pruebas y una de ellas supera la corrección de "
            "Benjamini-Hochberg con q < 0,05."
        ),
        "pos_salida": (
            "Se genera una alerta pendiente con tipo, torneo, evidencia, métricas, "
            "q-value, snapshot y fuga neta estimada."
        ),
        "neg_prueba": "Ninguna prueba supera el umbral tras la corrección FDR.",
        "neg_salida": (
            "No se genera ninguna alerta y las pruebas quedan registradas con su q-value."
        ),
    },
    {
        "id": "RF-13",
        "name": "Dashboard: KPIs y fatiga",
        "pos_prueba": (
            "El jugador abre el Dashboard con un baseline activo y sesiones disponibles."
        ),
        "pos_salida": (
            "Se muestran VPIP, PFR, 3-Bet y EVbb/100 con ajuste all-in, la muestra, la "
            "versión y la gráfica de fatiga con el punto de cruce a pérdidas."
        ),
        "neg_prueba": "El jugador abre el Dashboard sin baseline activo.",
        "neg_salida": (
            "El sistema muestra el estado de inicio con la guía «Crear baseline» y no "
            "dibuja la gráfica de fatiga."
        ),
    },
    {
        "id": "RF-14",
        "name": "Dashboard: feed y evidencia",
        "pos_prueba": "El último lote contiene una alerta de tilt y una desviación.",
        "pos_salida": (
            "El feed muestra primero el tilt y después la desviación, con evidencia, "
            "delta, fuga neta y numerador/denominador; «Auditar» abre la mano correspondiente."
        ),
        "neg_prueba": "El último lote no contiene alertas.",
        "neg_salida": (
            "El feed muestra el estado vacío y el resto del Dashboard sigue funcionando."
        ),
    },
    {
        "id": "RF-15",
        "name": "Historial de torneos",
        "pos_prueba": (
            "El jugador abre el historial y filtra por estado «tilt» y por periodo."
        ),
        "pos_salida": (
            "Se listan solo los torneos que cumplen ambos filtros, ordenados por fecha "
            "descendente y con BB ganadas, All-in EV, suerte all-in y estado conductual."
        ),
        "neg_prueba": "El jugador combina filtros que no devuelven resultados.",
        "neg_salida": "El historial muestra el estado vacío y permite limpiar los filtros.",
    },
    {
        "id": "RF-16",
        "name": "Visor de torneo",
        "pos_prueba": (
            "El jugador selecciona un torneo con una ventana T+30 y un tramo de desviación."
        ),
        "pos_salida": (
            "La gráfica dual muestra el resultado real y el EV, resalta la ventana en rojo "
            "y el tramo en ámbar, el bloque Lectura separa conducta y suerte, y se "
            "puede abrir la mano correspondiente."
        ),
        "neg_prueba": "El jugador selecciona un torneo sin anomalías.",
        "neg_salida": (
            "La gráfica se muestra sin franjas, la parte Conducta indica que no hay "
            "anomalías sin mostrar métricas del torneo y la navegación conserva el "
            "torneo seleccionado."
        ),
    },
    {
        "id": "RF-17",
        "name": "Visor de mano",
        "pos_prueba": "El jugador abre una mano perteneciente a una ventana T+30.",
        "pos_salida": (
            "Se muestran metadatos, cartas, acciones por calle, equidad, EV, baseline "
            "aplicable y la acción «Siguiente en T+30»."
        ),
        "neg_prueba": "La mano no tiene etiqueta sugerida.",
        "neg_salida": (
            "El sistema permite elegir una etiqueta del catálogo y exige validación "
            "explícita antes de registrarla."
        ),
    },
    {
        "id": "RF-18",
        "name": "Etiquetar jugadas del Nivel 2",
        "pos_prueba": "El jugador valida una etiqueta sugerida para una mano.",
        "pos_salida": (
            "Se guarda la etiqueta con usuario, fecha, origen y peso aplicado, y queda "
            "disponible para el clasificador sin alterar el Nivel 1."
        ),
        "neg_prueba": "El jugador intenta entrenar el clasificador con etiquetas sin validar.",
        "neg_salida": "El sistema excluye las etiquetas sin validar del entrenamiento.",
    },
    {
        "id": "RF-19",
        "name": "Glosario y ayuda contextual",
        "pos_prueba": "El jugador abre el glosario desde el tooltip de «3-Bet».",
        "pos_salida": (
            "Se abre directamente el término «3-Bet» con su definición y ejemplo, "
            "conservando el contexto de origen."
        ),
        "neg_prueba": "El jugador busca un término que no existe.",
        "neg_salida": "El buscador muestra un estado vacío.",
    },
    {
        "id": "RF-20",
        "name": "Cuenta, registro y configuración",
        "pos_prueba": (
            "El jugador crea una cuenta nueva con correo y contraseña, inicia sesión, "
            "cambia la ventana reactiva a T+50 y la sensibilidad FDR a q < 0,01, y guarda."
        ),
        "pos_salida": (
            "La cuenta queda creada, la sesión se inicia, la configuración se guarda y se "
            "aplica solo al siguiente lote, sin alterar las alertas ya emitidas."
        ),
        "neg_prueba": "El jugador intenta registrarse con un correo que ya tiene cuenta.",
        "neg_salida": (
            "El alta se rechaza, no se crea ninguna cuenta y el mensaje no revela datos de "
            "la cuenta existente."
        ),
    },
    {
        "id": "RF-21",
        "name": "Comparar el baseline con las ventanas T+30",
        "pos_prueba": (
            "El jugador abre la comparativa con un último lote que contiene ventanas T+30 "
            "y un baseline activo."
        ),
        "pos_salida": (
            "Se muestran las cinco métricas del baseline frente a las ventanas, sus "
            "diferencias en puntos porcentuales, las métricas significativas tras la "
            "corrección FDR y la fuga neta acumulada."
        ),
        "neg_prueba": "El último lote no contiene ninguna ventana T+30.",
        "neg_salida": "La pantalla muestra un estado vacío y no calcula ninguna comparación.",
    },
]



# ---------------------------------------------------------------------------
# 2.2 Planificación temporal del problema (solo planificación estimada)
# ---------------------------------------------------------------------------
#
# Las semanas se numeran desde 1 (lunes 12 de octubre de 2026) hasta 33
# (semana del 24 al 30 de mayo de 2027). Cada actividad es una tupla
# (nombre, semana_inicial, semana_final, horas). Las horas de las actividades
# de una etapa suman las horas de la etapa y el total del proyecto es de 300 h.
# El descubrimiento terminó en la semana 4 (2 a 8 de noviembre de 2026) con unas
# 30 h reales; las 15 h que sobraban de la estimación inicial (45 h) se repartieron
# en las tareas con menos horas.

PLANIFICACION = {
    "inicio": (2026, 10, 12),
    "semanas": 33,
    "horas_totales": 300,
    "etapas": [
        {
            "nombre": "Estudio y análisis del problema",
            "corto": "Estudio y análisis",
            "desc": (
                "analiza las limitaciones de los trackers tradicionales, revisa la "
                "literatura de referencia sobre tilt y fatiga y fija el alcance del MVP "
                "y el principio de que el resultado no define la conducta."
            ),
            "acts": [
                ("Plantear el proyecto y su problemática", 1, 1, 5),
                ("Estudiar trackers y literatura de referencia", 1, 2, 8),
                ("Definir el alcance del MVP y la especificación técnica", 2, 3, 7),
            ],
        },
        {
            "nombre": "Fase de descubrimiento",
            "corto": "Descubrimiento",
            "desc": (
                "aplica Design Thinking (empatía, definición, ideación y prototipado) "
                "y construye un prototipo navegable que se refina en varias iteraciones."
            ),
            "acts": [
                ("Empatía y definición: personas y retos de diseño", 1, 2, 10),
                ("Ideación de la solución", 2, 3, 7),
                ("Prototipo navegable (primera versión)", 2, 3, 8),
                ("Iteraciones del prototipo", 4, 4, 5),
            ],
        },
        {
            "nombre": "Fase de desarrollo: Plan",
            "corto": "Desarrollo: Plan",
            "desc": (
                "define el Product Backlog, los actores, los requisitos funcionales y no "
                "funcionales, el modelo de datos y los diagramas que sostienen el diseño."
            ),
            "acts": [
                ("Historias de usuario, actores y Product Backlog", 4, 5, 8),
                ("Requisitos funcionales y no funcionales", 5, 9, 16),
                ("Modelo de datos y requisitos de almacenamiento", 8, 11, 14),
                ("Diagramas UML y de secuencia", 10, 12, 9),
                ("Casos de uso y trazabilidad de requisitos", 12, 14, 8),
            ],
        },
        {
            "nombre": "Fase de desarrollo: Code, Build y Test",
            "corto": "Desarrollo: Code, Build y Test",
            "desc": (
                "implementa el parser, el cálculo de EV y de sesiones, el baseline, los "
                "detectores con corrección FDR, la API y el frontend y el etiquetado del "
                "Nivel 2, y prueba cada módulo."
            ),
            "acts": [
                ("Arquitectura y contratos de la API", 14, 15, 10),
                ("Parser de Winamax y normalización a BB", 15, 17, 18),
                ("Cálculo de EV y Session Builder", 17, 19, 16),
                ("Baseline individual: congelación y recalibración", 19, 21, 18),
                ("Detectores del Nivel 1 y corrección FDR", 21, 24, 24),
                ("API REST y frontend", 22, 26, 22),
                ("Etiquetado del Nivel 2 y clasificador", 25, 26, 12),
                ("Pruebas y correcciones", 25, 27, 14),
            ],
        },
        {
            "nombre": "Fase de operaciones",
            "corto": "Operaciones",
            "desc": (
                "prepara las versiones, despliega la aplicación y define las métricas de "
                "monitorización."
            ),
            "acts": [
                ("Release y entornos", 27, 27, 6),
                ("Despliegue", 28, 28, 6),
                ("Operación y monitorización", 29, 29, 6),
            ],
        },
        {
            "nombre": "Documentación y defensa",
            "corto": "Documentación y defensa",
            "desc": (
                "redacta la memoria a medida que avanzan las demás etapas y prepara la "
                "defensa del trabajo."
            ),
            "acts": [
                ("Memoria: planificación y descubrimiento (cap. 2 a 6)", 6, 9, 8),
                ("Memoria: plan y casos de uso (7.1 y 7.4.1)", 10, 14, 9),
                ("Memoria: implementación, pruebas y operaciones", 26, 31, 12),
                ("Introducción, conclusiones y bibliografía", 30, 31, 6),
                ("Revisión final y preparación de la defensa", 31, 33, 8),
            ],
        },
    ],
}


# ---------------------------------------------------------------------------
# 5.1 Gestión de la fase de descubrimiento (datos reales)
# ---------------------------------------------------------------------------
#
# Cuatro semanas (de la del 12 de octubre a la del 2 de noviembre de 2026) con
# tres sprints. Las fechas son (año, mes, día). Cada actividad se colorea en los
# días laborables (L a V) del intervalo; Plan se marca el primer día laborable de
# cada sprint y Check y Act, el último, como en el ejemplo de la plantilla.
# Las etapas Decide y Validate del marco no se realizaron.

GESTION_DESCUBRIMIENTO = {
    "inicio": (2026, 10, 12),
    "semanas": 4,
    "sprints": [
        {
            "n": 1,
            "desde": (2026, 10, 16),
            "hasta": (2026, 10, 25),
            "acts": [
                ("Understand & Empathy y Define", (2026, 10, 16), (2026, 10, 23)),
                ("Idea", (2026, 10, 19), (2026, 10, 23)),
                ("Prototype", (2026, 10, 19), (2026, 10, 23)),
            ],
        },
        {
            "n": 2,
            "desde": (2026, 10, 26),
            "hasta": (2026, 11, 1),
            "acts": [
                ("Idea", (2026, 10, 26), (2026, 10, 30)),
                ("Prototype", (2026, 10, 26), (2026, 10, 30)),
            ],
        },
        {
            "n": 3,
            "desde": (2026, 11, 2),
            "hasta": (2026, 11, 8),
            "acts": [
                ("Prototype", (2026, 11, 2), (2026, 11, 6)),
            ],
        },
    ],
}

