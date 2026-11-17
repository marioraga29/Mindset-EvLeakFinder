"""Genera los diagramas UML del modelo de datos como SVG y PNG.

Uso:
    python3 tools/build_uml.py

Salida:
    tools/diagrams/uml/uml-00-global.svg / .png
    tools/diagrams/uml/uml-01-identidad.svg / .png
    tools/diagrams/uml/uml-02-manos.svg / .png
    tools/diagrams/uml/uml-03-baseline.svg / .png
    tools/diagrams/uml/uml-04-deteccion.svg / .png
    tools/diagrams/uml/uml-05-nivel2.svg / .png

El PNG se obtiene con ffmpeg (librsvg) al doble de resolución. No se usan
dependencias de Python externas.
"""

from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / "diagrams" / "uml"

FONT = "DejaVu Sans"

C_HEADER = "#5B9BD5"
C_HEADER_DARK = "#4472C4"
C_BORDER = "#4472C4"
C_TEXT = "#222222"
C_MUTED = "#5A6B7B"
C_LINE = "#44546A"
C_CLUSTER_FILL = "#F4F8FD"
C_CLUSTER_LINE = "#BDD6EE"
C_CLUSTER_TITLE = "#2F5597"
C_NOTE_FILL = "#FFF9E6"
C_NOTE_LINE = "#BF9000"
C_EXT_FILL = "#EEF2F6"
C_EXT_LINE = "#8FA6BF"

HEAD_H = 46
LINE_H = 23
PAD = 14


# ---------------------------------------------------------------------------
# Entidades del modelo (docs/02-modelo-datos.md)
# ---------------------------------------------------------------------------

ENTITIES: dict[str, dict] = {
    "usuario": {
        "ri": "RI-01",
        "attrs": [
            "id: UUID «PK»",
            "nombre: TEXT «UQ»",
            "email: TEXT «UQ»",
            "hash_contrasena: TEXT",
            "sal_contrasena: TEXT",
            "sitio_activo: TEXT",
            "formato_activo: TEXT",
            "nivel_juego: TEXT",
            "ventana_reactiva: INTEGER",
            "fdr_q: NUMERIC(4,3)",
            "consentimiento_nivel2: BOOLEAN",
            "consentimiento_fecha: TIMESTAMPTZ",
            "creado_en: TIMESTAMPTZ",
        ],
    },
    "lote_importacion": {
        "ri": "RI-12",
        "attrs": [
            "id: UUID «PK»",
            "usuario_id: UUID «FK»",
            "tipo: TEXT",
            "fecha_utc: TIMESTAMPTZ",
            "torneos: INTEGER",
            "manos: INTEGER",
            "sesiones_lote: INTEGER",
            "periodo_desde: TIMESTAMPTZ",
            "periodo_hasta: TIMESTAMPTZ",
            "ventana_reactiva: INTEGER",
            "fdr_q: NUMERIC(4,3)",
            "creado_en: TIMESTAMPTZ",
        ],
    },
    "sesion": {
        "ri": "RI-03",
        "attrs": [
            "id: UUID «PK»",
            "usuario_id: UUID «FK»",
            "inicio: TIMESTAMPTZ",
            "fin: TIMESTAMPTZ",
            "duracion_min: INTEGER",
            "manos: INTEGER",
            "torneos: INTEGER",
            "sitio: TEXT",
            "formato: TEXT",
            "resultado_bb: NUMERIC(12,4)",
            "ev_bb: NUMERIC(12,4)",
            "bb100: NUMERIC(10,4)",
            "evbb100: NUMERIC(10,4)",
            "recalculada_en: TIMESTAMPTZ",
        ],
    },
    "torneo": {
        "ri": "RI-02",
        "attrs": [
            "id: UUID «PK»",
            "usuario_id: UUID «FK»",
            "lote_id: UUID «FK»",
            "sesion_id: UUID «FK»",
            "id_externo: TEXT «UQ»",
            "nombre: TEXT",
            "sitio: TEXT",
            "formato: TEXT",
            "fecha_inicio: TIMESTAMPTZ",
            "fecha_fin: TIMESTAMPTZ",
            "nivel_inicial: INTEGER",
            "nivel_final: INTEGER",
            "max_jugadores: INTEGER",
            "recompensa: TEXT",
            "manos: INTEGER",
            "bb_ganadas: NUMERIC(12,4)",
            "ev_bb: NUMERIC(12,4)",
            "sigma_suerte_bb: NUMERIC(12,4)",
            "suerte_allin: TEXT",
            "nombre_archivo: TEXT",
            "hash_archivo: TEXT",
            "parser_version: TEXT",
            "creado_en: TIMESTAMPTZ",
        ],
    },
    "mano": {
        "ri": "RI-04",
        "attrs": [
            "id: UUID «PK»",
            "torneo_id: UUID «FK»",
            "hand_id: TEXT «UQ»",
            "indice: INTEGER «UQ»",
            "numero_original: INTEGER «UQ»",
            "timestamp_utc: TIMESTAMPTZ",
            "ante: INTEGER",
            "sb: INTEGER",
            "bb: INTEGER",
            "board: TEXT",
            "bote_bb: NUMERIC(12,4)",
            "net_bb: NUMERIC(12,4)",
            "ev_bb: NUMERIC(12,4)",
            "ev_version: TEXT",
            "equidad: NUMERIC(5,4)",
            "all_in: BOOLEAN",
            "showdown: BOOLEAN",
            "parser_version: TEXT",
        ],
    },
    "participacion": {
        "ri": "RI-05",
        "attrs": [
            "id: UUID «PK»",
            "mano_id: UUID «FK»",
            "jugador: TEXT",
            "asiento: SMALLINT",
            "posicion: TEXT",
            "stack_bb: NUMERIC(12,4)",
            "aportacion_bb: NUMERIC(12,4)",
            "cobrado_bb: NUMERIC(12,4)",
            "neto_bb: NUMERIC(12,4)",
            "cartas: TEXT",
            "all_in: BOOLEAN",
            "estado: TEXT",
            "es_heroe: BOOLEAN",
        ],
    },
    "accion": {
        "ri": "RI-06",
        "attrs": [
            "id: UUID «PK»",
            "mano_id: UUID «FK»",
            "participacion_id: UUID «FK»",
            "calle: TEXT",
            "orden: SMALLINT",
            "tipo: TEXT",
            "importe_bb: NUMERIC(12,4)",
            "importe_total_bb: NUMERIC(12,4)",
            "all_in: BOOLEAN",
            "bote_bb: NUMERIC(12,4)",
        ],
    },
    "bote": {
        "ri": "nueva",
        "attrs": [
            "id: UUID «PK»",
            "mano_id: UUID «FK»",
            "nivel: SMALLINT",
            "importe_bb: NUMERIC(12,4)",
        ],
    },
    "baseline_snapshot": {
        "ri": "RI-07",
        "attrs": [
            "id: UUID «PK»",
            "usuario_id: UUID «FK»",
            "version: INTEGER «UQ»",
            "tipo: TEXT",
            "origen: TEXT",
            "snapshot_padre_id: UUID «FK»",
            "estado: TEXT",
            "fecha_congelacion: TIMESTAMPTZ",
            "muestra_manos: INTEGER",
            "muestra_sesiones: INTEGER",
            "desde: TIMESTAMPTZ",
            "hasta: TIMESTAMPTZ",
            "ventana_reactiva: INTEGER",
            "fdr_q: NUMERIC(4,3)",
            "punto_critico_horas: NUMERIC(5,2)",
        ],
    },
    "metrica_valor": {
        "ri": "nueva",
        "attrs": [
            "id: UUID «PK»",
            "entidad_tipo: TEXT",
            "entidad_id: UUID",
            "metrica: TEXT",
            "tramo_stack: TEXT",
            "numerador: NUMERIC(12,4)",
            "denominador: NUMERIC(12,4)",
            "valor: NUMERIC(12,6)",
        ],
    },
    "baseline_exclusion": {
        "ri": "nueva",
        "attrs": [
            "id: UUID «PK»",
            "snapshot_id: UUID «FK»",
            "tipo: TEXT",
            "referencia_id: UUID",
            "motivo: TEXT",
            "desde: TIMESTAMPTZ",
            "hasta: TIMESTAMPTZ",
        ],
    },
    "baseline_snapshot_torneo": {
        "ri": "nueva",
        "attrs": [
            "snapshot_id: UUID «PK» «FK»",
            "torneo_id: UUID «PK» «FK»",
        ],
    },
    "ventana_mano": {
        "ri": "nueva",
        "attrs": [
            "ventana_id: UUID «PK» «FK»",
            "mano_id: UUID «PK» «FK»",
            "orden: SMALLINT",
        ],
    },
    "trigger": {
        "ri": "RI-15",
        "attrs": [
            "id: UUID «PK»",
            "mano_id: UUID «FK»",
            "torneo_id: UUID «FK»",
            "ventana_id: UUID «FK»",
            "es_bad_beat: BOOLEAN",
            "es_bote_grande: BOOLEAN",
            "equidad: NUMERIC(5,4)",
            "bote_bb: NUMERIC(12,4)",
            "perdida_bb: NUMERIC(12,4)",
            "umbral_equidad: NUMERIC(5,4)",
            "umbral_perdida_bb: NUMERIC(12,4)",
            "creado_en: TIMESTAMPTZ",
        ],
    },
    "ventana_reactiva": {
        "ri": "RI-09",
        "attrs": [
            "id: UUID «PK»",
            "torneo_id: UUID «FK»",
            "mano_inicio_id: UUID «FK»",
            "mano_fin_id: UUID «FK»",
            "ventana_manos: INTEGER",
            "manos_analizadas: INTEGER",
            "creado_en: TIMESTAMPTZ",
        ],
    },
    "tramo_desviacion": {
        "ri": "RI-10",
        "attrs": [
            "id: UUID «PK»",
            "torneo_id: UUID «FK»",
            "mano_inicio_id: UUID «FK»",
            "mano_fin_id: UUID «FK»",
            "manos: INTEGER",
            "metrica_principal: TEXT",
            "q_value: NUMERIC(6,5)",
            "creado_en: TIMESTAMPTZ",
        ],
    },
    "tramo_fatiga": {
        "ri": "RI-11",
        "attrs": [
            "id: UUID «PK»",
            "snapshot_id: UUID «FK»",
            "orden: SMALLINT",
            "hora_desde: NUMERIC(5,2)",
            "hora_hasta: NUMERIC(5,2)",
            "manos: INTEGER",
            "sesiones: INTEGER",
            "ev_bb: NUMERIC(12,4)",
            "evbb100: NUMERIC(10,4)",
            "ic95_inferior: NUMERIC(10,4)",
            "ic95_superior: NUMERIC(10,4)",
        ],
    },
    "prueba_estadistica": {
        "ri": "RI-16",
        "attrs": [
            "id: UUID «PK»",
            "lote_id: UUID «FK»",
            "snapshot_id: UUID «FK»",
            "tipo: TEXT",
            "referencia_id: UUID",
            "metrica: TEXT",
            "observado: NUMERIC(12,6)",
            "esperado: NUMERIC(12,6)",
            "estadistico: NUMERIC(12,6)",
            "p_value: NUMERIC(6,5)",
            "q_value: NUMERIC(6,5)",
            "significativa: BOOLEAN",
        ],
    },
    "alerta": {
        "ri": "RI-08",
        "attrs": [
            "id: UUID «PK»",
            "usuario_id: UUID «FK»",
            "lote_id: UUID «FK»",
            "tipo: TEXT",
            "torneo_id: UUID «FK»",
            "ventana_id: UUID «FK»",
            "tramo_id: UUID «FK»",
            "baseline_snapshot_id: UUID «FK»",
            "estado: TEXT",
            "fuga_neta_bb: NUMERIC(12,4)",
            "fecha: TIMESTAMPTZ",
        ],
    },
    "etiqueta": {
        "ri": "RI-13",
        "attrs": [
            "id: UUID «PK»",
            "codigo: TEXT «UQ»",
            "version: INTEGER",
            "peso_base: NUMERIC(4,3)",
            "activa: BOOLEAN",
        ],
    },
    "etiqueta_mano": {
        "ri": "RI-14",
        "attrs": [
            "id: UUID «PK»",
            "mano_id: UUID «FK»",
            "usuario_id: UUID «FK»",
            "etiqueta_id: UUID «FK»",
            "fecha: TIMESTAMPTZ",
            "nivel_aplicado: TEXT",
            "peso_aplicado: NUMERIC(4,3)",
            "origen: TEXT",
            "validada: BOOLEAN",
        ],
    },
}


# ---------------------------------------------------------------------------
# Utilidades de dibujo
# ---------------------------------------------------------------------------

def text_w(text: str, size: float, bold: bool = False) -> float:
    factor = 0.60 if bold else 0.545
    return len(text) * size * factor


def header(width: int, height: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect width="{width}" height="{height}" fill="#FFFFFF"/>',
    ]


def text_el(
    x: float,
    y: float,
    content: str,
    size: float = 15,
    fill: str = C_TEXT,
    bold: bool = False,
    anchor: str = "start",
    italic: bool = False,
) -> str:
    weight = ' font-weight="bold"' if bold else ""
    style = ' font-style="italic"' if italic else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" '
        f'font-size="{size}" fill="{fill}"{weight}{style} '
        f'text-anchor="{anchor}">{escape(content)}</text>'
    )


def badge(x: float, y: float, content: str) -> str:
    """Texto con fondo blanco, para etiquetas sobre líneas."""
    w = text_w(content, 14) + 8
    return (
        f'<rect x="{x - w / 2:.1f}" y="{y - 14:.1f}" width="{w:.1f}" '
        f'height="19" fill="#FFFFFF" fill-opacity="0.92"/>'
        + text_el(x, y, content, 14, C_MUTED, anchor="middle")
    )


def class_width(name: str, attrs: list[str]) -> float:
    candidates = [text_w(name, 19, True)]
    candidates += [text_w(a, 15) for a in attrs]
    return max(190, max(candidates) + 2 * PAD + 8)


def class_box(spec: dict) -> tuple[str, dict]:
    key = spec["key"]
    name = spec["name"]
    attrs = spec.get("attrs") or []
    x, y = spec["x"], spec["y"]
    external = spec.get("external", False)

    if external:
        w = spec.get("w") or max(150, text_w(name, 16, True) + 44)
        h = 58
        svg = [
            f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
            f'fill="{C_EXT_FILL}" stroke="{C_EXT_LINE}" stroke-width="1.4" '
            f'stroke-dasharray="6 4"/>',
            text_el(x + w / 2, y + 27, name, 16, "#44546A", True, "middle", True),
            text_el(x + w / 2, y + 45, "referencia externa", 11, C_MUTED, anchor="middle"),
            "</g>",
        ]
        return "".join(svg), {"x": x, "y": y, "w": w, "h": h}

    if not attrs:
        w = spec.get("w") or max(170, text_w(name, 16, True) + 44)
        h = 62
        svg = [
            f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
            f'fill="#FFFFFF" stroke="{C_BORDER}" stroke-width="1.5"/>',
            text_el(x + w / 2, y + 26, name, 16, C_TEXT, True, "middle"),
            text_el(x + w / 2, y + 46, spec.get("ri", ""), 12, C_MUTED, anchor="middle"),
            "</g>",
        ]
        return "".join(svg), {"x": x, "y": y, "w": w, "h": h}

    w = spec.get("w") or class_width(name, attrs)
    h = HEAD_H + 12 + LINE_H * len(attrs) + 8

    svg = [
        f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" '
        f'fill="#FFFFFF" stroke="{C_BORDER}" stroke-width="1.6"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{HEAD_H}" rx="7" fill="{C_HEADER}"/>',
        f'<rect x="{x}" y="{y + HEAD_H - 7}" width="{w}" height="7" fill="{C_HEADER}"/>',
        text_el(x + w / 2, y + 25, name, 19, "#FFFFFF", True, "middle"),
        text_el(x + w / 2, y + 40, spec.get("ri", ""), 11, "#E8F1FA", anchor="middle"),
        f'<line x1="{x}" y1="{y + HEAD_H}" x2="{x + w}" y2="{y + HEAD_H}" '
        f'stroke="{C_BORDER}" stroke-width="1.2"/>',
    ]
    for i, attr in enumerate(attrs):
        ty = y + HEAD_H + 12 + LINE_H * i + 16
        if "«PK»" in attr:
            name_part, mark = attr.split("«PK»", 1)
            svg.append(text_el(x + PAD, ty, name_part.rstrip(), 15, C_TEXT))
            svg.append(text_el(x + w - PAD, ty, "PK", 12, "#C00000", True, "end"))
        elif "«FK»" in attr:
            name_part, mark = attr.split("«FK»", 1)
            svg.append(text_el(x + PAD, ty, name_part.rstrip(), 15, C_TEXT))
            svg.append(text_el(x + w - PAD, ty, "FK", 12, "#1F6FB2", True, "end"))
        elif "«UQ»" in attr:
            name_part, mark = attr.split("«UQ»", 1)
            svg.append(text_el(x + PAD, ty, name_part.rstrip(), 15, C_TEXT))
            svg.append(text_el(x + w - PAD, ty, "UQ", 12, "#7F6000", True, "end"))
        else:
            svg.append(text_el(x + PAD, ty, attr, 15, C_TEXT))
    svg.append("</g>")
    return "".join(svg), {"x": x, "y": y, "w": w, "h": h}


def edge_point(box: dict, tx: float, ty: float) -> tuple[float, float]:
    cx = box["x"] + box["w"] / 2
    cy = box["y"] + box["h"] / 2
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    sx = (box["w"] / 2) / abs(dx) if dx else 1e9
    sy = (box["h"] / 2) / abs(dy) if dy else 1e9
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


def arrow_head(x: float, y: float, dx: float, dy: float, color: str = C_LINE) -> str:
    import math

    ang = math.atan2(dy, dx)
    size = 11
    a1 = ang + math.radians(24)
    a2 = ang - math.radians(24)
    p1 = (x - size * math.cos(a1), y - size * math.sin(a1))
    p2 = (x - size * math.cos(a2), y - size * math.sin(a2))
    return (
        f'<path d="M {x:.1f} {y:.1f} L {p1[0]:.1f} {p1[1]:.1f} '
        f'M {x:.1f} {y:.1f} L {p2[0]:.1f} {p2[1]:.1f}" '
        f'fill="none" stroke="{color}" stroke-width="1.6" '
        f'stroke-linecap="round"/>'
    )


def diamond(x: float, y: float, dx: float, dy: float, color: str) -> str:
    import math

    ang = math.atan2(dy, dx)
    length, width = 18, 6
    bx = x + length * math.cos(ang)
    by = y + length * math.sin(ang)
    px, py = -math.sin(ang) * width, math.cos(ang) * width
    return (
        f'<path d="M {x:.1f} {y:.1f} L {bx + px:.1f} {by + py:.1f} '
        f'L {bx:.1f} {by:.1f} L {bx - px:.1f} {by - py:.1f} Z" '
        f'fill="{color}" stroke="{color}" stroke-width="1"/>'
    )


def link_svg(a: dict, b: dict, spec: dict) -> str:
    kind = spec.get("kind", "assoc")
    acx, acy = a["x"] + a["w"] / 2, a["y"] + a["h"] / 2
    bcx, bcy = b["x"] + b["w"] / 2, b["y"] + b["h"] / 2
    p1 = edge_point(a, bcx, bcy)
    p2 = edge_point(b, acx, acy)
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]

    dash = ' stroke-dasharray="7 5"' if kind == "dep" else ""
    parts = [
        f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" '
        f'y2="{p2[1]:.1f}" stroke="{C_LINE}" stroke-width="1.6"{dash}/>'
    ]

    if kind == "comp":
        parts.append(diamond(p1[0], p1[1], dx, dy, C_LINE))
    elif kind in ("assoc", "dep"):
        parts.append(arrow_head(p2[0], p2[1], dx, dy))

    if spec.get("ma"):
        import math

        length = math.hypot(dx, dy) or 1
        off = max(26, min(0.15 * length, 70))
        mx, my = p1[0] + dx / length * off, p1[1] + dy / length * off
        parts.append(badge(mx, my - 9, spec["ma"]))
    if spec.get("mb"):
        import math

        length = math.hypot(dx, dy) or 1
        off = max(26, min(0.15 * length, 70))
        mx, my = p2[0] - dx / length * off, p2[1] - dy / length * off
        parts.append(badge(mx, my - 9, spec["mb"]))
    if spec.get("label"):
        mx, my = p1[0] + dx * 0.5, p1[1] + dy * 0.5
        parts.append(badge(mx, my - 12, spec["label"]))
    return "".join(parts)


def cluster_svg(spec: dict) -> str:
    x, y, w, h = spec["x"], spec["y"], spec["w"], spec["h"]
    return (
        f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
        f'fill="{C_CLUSTER_FILL}" stroke="{C_CLUSTER_LINE}" stroke-width="1.5" '
        f'stroke-dasharray="9 6"/>'
        + text_el(x + 20, y + 32, spec["title"], 20, C_CLUSTER_TITLE, True)
        + "</g>"
    )


def note_svg(spec: dict) -> str:
    x, y, w = spec["x"], spec["y"], spec["w"]
    chars = max(20, int(w / 8.2))
    lines = textwrap.wrap(spec["text"], chars) or [""]
    h = 18 + len(lines) * 20 + 8
    parts = [
        f'<g><path d="M {x} {y} L {x + w - 16} {y} L {x + w} {y + 16} '
        f'L {x + w} {y + h} L {x} {y + h} Z" fill="{C_NOTE_FILL}" '
        f'stroke="{C_NOTE_LINE}" stroke-width="1.3"/>',
        f'<path d="M {x + w - 16} {y} L {x + w - 16} {y + 16} L {x + w} {y + 16}" '
        f'fill="none" stroke="{C_NOTE_LINE}" stroke-width="1.3"/>',
    ]
    for i, line in enumerate(lines):
        parts.append(text_el(x + 12, y + 24 + i * 20, line, 13, "#5C4A00"))
    parts.append("</g>")
    return "".join(parts)


def render(diagram: dict) -> str:
    parts = header(diagram["width"], diagram["height"])
    for cluster in diagram.get("clusters", []):
        parts.append(cluster_svg(cluster))
    boxes: dict[str, dict] = {}
    for spec in diagram["boxes"]:
        svg, box = class_box(spec)
        boxes[spec["key"]] = box
        parts.append(svg)
    for link in diagram.get("links", []):
        parts.append(link_svg(boxes[link["a"]], boxes[link["b"]], link))
    for note in diagram.get("notes", []):
        parts.append(note_svg(note))
    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Diagramas
# ---------------------------------------------------------------------------

def box(key: str, x: int, y: int, **extra) -> dict:
    data = {"key": key, "name": key, "x": x, "y": y, **ENTITIES[key], **extra}
    return data


DIAGRAMS = [
    {
        "slug": "uml-00-global",
        "width": 1700,
        "height": 920,
        "clusters": [
            {"x": 40, "y": 40, "w": 560, "h": 340, "title": "Identidad e importación"},
            {"x": 40, "y": 420, "w": 560, "h": 340, "title": "Manos"},
            {"x": 640, "y": 40, "w": 570, "h": 300, "title": "Baseline"},
            {"x": 640, "y": 420, "w": 540, "h": 470, "title": "Detección"},
            {"x": 1220, "y": 40, "w": 420, "h": 240, "title": "Nivel 2 · etiquetado"},
        ],
        "boxes": [
            box("usuario", 80, 110, attrs=[]),
            box("lote_importacion", 330, 110, attrs=[]),
            box("sesion", 80, 250, attrs=[]),
            box("torneo", 330, 250, attrs=[]),
            box("mano", 80, 500, attrs=[]),
            box("participacion", 330, 500, attrs=[]),
            box("bote", 80, 610, attrs=[]),
            box("accion", 330, 610, attrs=[]),
            box("baseline_snapshot", 680, 120, attrs=[]),
            box("metrica_valor", 910, 120, attrs=[]),
            box("baseline_snapshot_torneo", 680, 230, attrs=[]),
            box("baseline_exclusion", 980, 230, attrs=[]),
            box("trigger", 680, 500, attrs=[]),
            box("ventana_reactiva", 900, 500, attrs=[]),
            box("ventana_mano", 900, 800, attrs=[]),
            box("tramo_desviacion", 680, 600, attrs=[]),
            box("prueba_estadistica", 900, 600, attrs=[]),
            box("tramo_fatiga", 680, 700, attrs=[]),
            box("alerta", 900, 700, attrs=[]),
            box("etiqueta", 1260, 110, attrs=[]),
            box("etiqueta_mano", 1260, 190, attrs=[]),
        ],
        "links": [
            {"a": "usuario", "b": "lote_importacion", "kind": "assoc"},
            {"a": "usuario", "b": "sesion", "kind": "assoc"},
            {"a": "lote_importacion", "b": "torneo", "kind": "assoc"},
            {"a": "sesion", "b": "torneo", "kind": "assoc"},
            {"a": "mano", "b": "participacion", "kind": "assoc"},
            {"a": "mano", "b": "bote", "kind": "assoc"},
            {"a": "participacion", "b": "accion", "kind": "assoc"},
            {"a": "baseline_snapshot", "b": "metrica_valor", "kind": "comp"},
            {"a": "baseline_snapshot", "b": "baseline_exclusion", "kind": "comp"},
            {"a": "baseline_snapshot", "b": "baseline_snapshot_torneo", "kind": "comp"},
            {"a": "torneo", "b": "baseline_snapshot_torneo", "kind": "assoc"},
            {"a": "trigger", "b": "ventana_reactiva", "kind": "assoc"},
            {"a": "ventana_reactiva", "b": "prueba_estadistica", "kind": "assoc"},
            {"a": "tramo_desviacion", "b": "prueba_estadistica", "kind": "assoc"},
            {"a": "prueba_estadistica", "b": "alerta", "kind": "assoc"},
            {"a": "baseline_snapshot", "b": "prueba_estadistica", "kind": "assoc"},
            {"a": "alerta", "b": "tramo_desviacion", "kind": "assoc"},
            {"a": "etiqueta", "b": "etiqueta_mano", "kind": "assoc"},
        ],
        "notes": [
            {
                "x": 1220,
                "y": 330,
                "w": 420,
                "text": (
                    "Las cinco agrupaciones cubren las 21 entidades del modelo. "
                    "El detalle de atributos y multiplicidades está en los "
                    "diagramas uml-01 a uml-05."
                ),
            },
            {
                "x": 1220,
                "y": 520,
                "w": 420,
                "text": (
                    "Cada caja es una entidad. El rombo relleno indica "
                    "composición y la flecha discontinua, dependencia. "
                    "«nueva» marca una entidad que no figura en 7.1.5."
                ),
            },
        ],
    },
    {
        "slug": "uml-01-identidad",
        "width": 1500,
        "height": 1000,
        "boxes": [
            box("usuario", 70, 120),
            box("lote_importacion", 600, 80),
            box("torneo", 1120, 80),
            box("sesion", 600, 560),
        ],
        "links": [
            {
                "a": "usuario",
                "b": "lote_importacion",
                "label": "abre",
                "ma": "1",
                "mb": "0..N",
            },
            {
                "a": "lote_importacion",
                "b": "torneo",
                "label": "incorpora",
                "ma": "1",
                "mb": "1..N",
            },
            {
                "a": "usuario",
                "b": "sesion",
                "label": "juega",
                "ma": "1",
                "mb": "0..N",
            },
            {
                "a": "sesion",
                "b": "torneo",
                "label": "agrupa",
                "ma": "1",
                "mb": "1..N",
            },
        ],
    },
    {
        "slug": "uml-02-manos",
        "width": 1500,
        "height": 1000,
        "boxes": [
            box("mano", 70, 300),
            box("participacion", 600, 60),
            box("accion", 600, 640),
            box("bote", 1150, 400),
            box("torneo", 70, 60, external=True),
        ],
        "links": [
            {
                "a": "torneo",
                "b": "mano",
                "label": "contiene",
                "ma": "1",
                "mb": "1..N",
            },
            {
                "a": "mano",
                "b": "participacion",
                "label": "tiene",
                "ma": "1",
                "mb": "2..N",
            },
            {
                "a": "mano",
                "b": "accion",
                "label": "registra",
                "ma": "1",
                "mb": "0..N",
            },
            {
                "a": "mano",
                "b": "bote",
                "label": "reparte",
                "ma": "1",
                "mb": "1..N",
            },
            {
                "a": "participacion",
                "b": "accion",
                "label": "ejecuta",
                "ma": "1",
                "mb": "0..N",
            },
        ],
        "notes": [
            {
                "x": 70,
                "y": 800,
                "w": 430,
                "text": (
                    "La suma de participacion.neto_bb es mano.net_bb y la suma "
                    "de bote.importe_bb es mano.bote_bb."
                ),
            }
        ],
    },
    {
        "slug": "uml-03-baseline",
        "width": 1450,
        "height": 1170,
        "boxes": [
            box("baseline_snapshot", 80, 140),
            box("metrica_valor", 700, 80),
            box("baseline_exclusion", 700, 500),
            box("baseline_snapshot_torneo", 1100, 500),
            box("tramo_fatiga", 700, 790),
            box("torneo", 1200, 300, external=True),
            box("usuario", 80, 650, external=True),
        ],
        "links": [
            {
                "a": "baseline_snapshot",
                "b": "metrica_valor",
                "kind": "comp",
                "label": "congela",
                "ma": "1",
                "mb": "0..N",
            },
            {
                "a": "baseline_snapshot",
                "b": "baseline_exclusion",
                "kind": "comp",
                "label": "excluye",
                "ma": "1",
                "mb": "0..N",
            },
            {
                "a": "baseline_snapshot",
                "b": "tramo_fatiga",
                "kind": "comp",
                "label": "congela la curva",
                "ma": "1",
                "mb": "0..N",
            },
            {
                "a": "baseline_snapshot",
                "b": "baseline_snapshot_torneo",
                "kind": "comp",
                "label": "se compone de",
                "ma": "1",
                "mb": "1..N",
            },
            {
                "a": "torneo",
                "b": "baseline_snapshot_torneo",
                "label": "forma parte de",
                "ma": "1",
                "mb": "0..N",
            },
            {
                "a": "usuario",
                "b": "baseline_snapshot",
                "label": "posee",
                "ma": "1",
                "mb": "0..N",
            },
        ],
        "notes": [
            {
                "x": 700,
                "y": 330,
                "w": 430,
                "text": (
                    "entidad_tipo ∈ {baseline_snapshot, ventana_reactiva, "
                    "tramo_desviacion, sesion, torneo}: referencia polimórfica "
                    "validada por la aplicación."
                ),
            },
            {
                "x": 80,
                "y": 760,
                "w": 430,
                "text": (
                    "La fatiga no genera alertas: la curva se congela con el "
                    "baseline y solo se muestra en la gráfica del Dashboard."
                ),
            }
        ],
    },
    {
        "slug": "uml-04-deteccion",
        "width": 1860,
        "height": 1300,
        "boxes": [
            box("ventana_reactiva", 620, 60),
            box("ventana_mano", 620, 400),
            box("trigger", 70, 180),
            box("tramo_desviacion", 620, 620),
            box("prueba_estadistica", 1200, 320),
            box("alerta", 1200, 820),
            box("usuario", 640, 1040, external=True),
            box("mano", 400, 430, external=True),
            box("baseline_snapshot", 1620, 900, external=True),
        ],
        "links": [
            {
                "a": "ventana_reactiva",
                "b": "trigger",
                "label": "cubre",
                "ma": "1",
                "mb": "1..N",
            },
            {
                "a": "ventana_reactiva",
                "b": "ventana_mano",
                "kind": "comp",
                "label": "se compone de",
                "ma": "1",
                "mb": "1..N",
            },
            {
                "a": "mano",
                "b": "ventana_mano",
                "label": "forma parte de",
                "ma": "1",
                "mb": "0..1",
            },
            {
                "a": "mano",
                "b": "trigger",
                "label": "dispara",
                "kind": "dep",
            },
            {
                "a": "ventana_reactiva",
                "b": "prueba_estadistica",
                "label": "se contrasta",
                "ma": "1",
                "mb": "0..N",
            },
            {
                "a": "tramo_desviacion",
                "b": "prueba_estadistica",
                "label": "se contrasta",
                "ma": "1",
                "mb": "0..N",
            },
            {
                "a": "baseline_snapshot",
                "b": "alerta",
                "label": "respalda",
                "kind": "dep",
            },
            {
                "a": "baseline_snapshot",
                "b": "prueba_estadistica",
                "label": "esperado de",
                "kind": "dep",
            },
            {
                "a": "alerta",
                "b": "ventana_reactiva",
                "label": "tilt",
                "ma": "0..1",
                "mb": "0..N",
            },
            {
                "a": "alerta",
                "b": "tramo_desviacion",
                "label": "desviación",
                "ma": "0..1",
                "mb": "0..N",
            },
            {
                "a": "usuario",
                "b": "alerta",
                "label": "recibe",
                "ma": "1",
                "mb": "0..N",
            },
        ],
        "notes": [

        ],
    },
    {
        "slug": "uml-05-nivel2",
        "width": 1300,
        "height": 700,
        "boxes": [
            box("etiqueta", 90, 160),
            box("etiqueta_mano", 700, 120),
            box("mano", 620, 500, external=True),
            box("usuario", 900, 500, external=True),
        ],
        "links": [
            {
                "a": "etiqueta",
                "b": "etiqueta_mano",
                "label": "clasifica",
                "ma": "1",
                "mb": "0..N",
            },
            {
                "a": "etiqueta_mano",
                "b": "mano",
                "label": "etiqueta",
                "ma": "0..N",
                "mb": "1",
                "kind": "dep",
            },
            {
                "a": "etiqueta_mano",
                "b": "usuario",
                "label": "valida",
                "ma": "0..N",
                "mb": "1",
                "kind": "dep",
            },
        ],
        "notes": [
            {
                "x": 90,
                "y": 420,
                "w": 430,
                "text": (
                    "Solo las etiquetas validadas alimentan el clasificador. "
                    "Ninguna etiqueta modifica el baseline ni las alertas."
                ),
            }
        ],
    },
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for diagram in DIAGRAMS:
        svg_path = OUT / f"{diagram['slug']}.svg"
        png_path = OUT / f"{diagram['slug']}.png"
        svg_path.write_text(render(diagram), encoding="utf-8")
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(svg_path),
                "-frames:v",
                "1",
                "-vf",
                "scale=iw*2:ih*2",
                "-pix_fmt",
                "rgb24",
                str(png_path),
            ],
            check=True,
        )
        print(f"Generado: {png_path}")


if __name__ == "__main__":
    main()
