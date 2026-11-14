"""Genera los diagramas de secuencia de 7.1.6 como SVG y PNG.

Uso:
    python3 tools/build_secuencias.py

Salida:
    tools/diagrams/seq-01.svg / seq-01.png
    tools/diagrams/seq-02.svg / seq-02.png
    tools/diagrams/seq-03.svg / seq-03.png

El PNG se obtiene con ffmpeg (librsvg). No se usan dependencias de Python
externas. El generador de la memoria lee los PNG y los incrusta en el .docx.
"""

from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / "diagrams"

WIDTH = 1000
MARGIN = 30
HEADER_Y = 26
HEADER_H = 48
STEP_H = 54
FONT = "DejaVu Sans"

COLOR_HEADER = "#5B9BD5"
COLOR_HEADER_LINE = "#4472C4"
COLOR_LIFELINE = "#9DC3E6"
COLOR_CALL = "#333333"
COLOR_RETURN = "#666666"
COLOR_TEXT = "#222222"

DIAGRAMS = [
    {
        "slug": "seq-01",
        "title": "Importación y procesamiento del lote",
        "participants": [
            "Jugador",
            "Interfaz",
            "API",
            "Parser",
            "Session Builder",
            "Motor",
        ],
        "steps": [
            (0, 1, "Selecciona archivos .txt", "call"),
            (1, 2, "Envía el lote", "call"),
            (2, 3, "Valida e interpreta", "call"),
            (3, 3, "Comprueba duplicados", "call"),
            (3, 1, "Válidos, duplicados y errores", "return"),
            (0, 1, "Confirma el procesamiento", "call"),
            (1, 2, "Procesa el lote", "call"),
            (2, 3, "Registra manos canónicas", "call"),
            (3, 4, "Manos normalizadas", "call"),
            (4, 5, "Sesiones y agregados", "call"),
            (5, 5, "Audita el lote", "call"),
            (5, 2, "Resultado y alertas", "return"),
            (2, 1, "Lote procesado", "return"),
            (1, 0, "Dashboard con el lote", "return"),
        ],
    },
    {
        "slug": "seq-02",
        "title": "Auditoría de una alerta",
        "participants": [
            "Jugador",
            "Dashboard",
            "API",
            "Motor",
            "Base de datos",
        ],
        "steps": [
            (3, 4, "Guarda alerta y evidencia", "call"),
            (1, 2, "Pide alertas del último lote", "call"),
            (2, 4, "Consulta alertas y métricas", "call"),
            (4, 2, "Alertas con evidencia", "return"),
            (2, 1, "Feed del lote", "return"),
            (0, 1, "Pulsa «Auditar»", "call"),
            (1, 2, "Abre visor de torneo y mano", "call"),
            (2, 4, "Consulta mano y baseline", "call"),
            (4, 2, "Mano con contexto", "return"),
            (2, 1, "Visor de mano", "return"),
            (0, 1, "Valida la etiqueta", "call"),
            (1, 2, "Guarda etiqueta", "call"),
            (2, 4, "Registra etiqueta validada", "call"),
            (1, 0, "Alerta auditada", "return"),
        ],
    },
    {
        "slug": "seq-03",
        "title": "Cálculo del baseline y detección",
        "participants": [
            "Motor",
            "Baseline",
            "Detectores",
            "FDR",
            "Base de datos",
        ],
        "steps": [
            (0, 4, "Lee manos anteriores al periodo", "call"),
            (4, 0, "Manos y métricas", "return"),
            (0, 1, "Calcula snapshot", "call"),
            (1, 4, "Congela versión inmutable", "call"),
            (0, 2, "Evalúa el lote", "call"),
            (2, 2, "Trigger, T+30 y tramos", "call"),
            (2, 3, "Pruebas estadísticas", "call"),
            (3, 2, "q-values", "return"),
            (2, 4, "Alertas significativas", "call"),
            (0, 4, "Resultado del lote", "call"),
        ],
    },
]


def participant_x(index: int, count: int) -> float:
    column = (WIDTH - 2 * MARGIN) / count
    return MARGIN + column * (index + 0.5)


def wrap_lines(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width) or [""]


def arrowhead(x: float, y: float, direction: int) -> str:
    """Triángulo relleno que apunta a la derecha (1) o a la izquierda (-1)."""
    tip = x
    base = x - direction * 12
    return (
        f'<polygon points="{tip},{y} {base},{y - 6} {base},{y + 6}" '
        f'fill="{COLOR_CALL}"/>'
    )


def self_loop(x: float, y: float, label: str, right: bool) -> str:
    direction = 1 if right else -1
    out_x = x + direction * 46
    parts = [
        f'<path d="M {x} {y} L {out_x} {y} L {out_x} {y + 22} L {x} {y + 22}" '
        f'fill="none" stroke="{COLOR_CALL}" stroke-width="1.6"/>',
        arrowhead(x, y + 22, -direction),
    ]
    lines = wrap_lines(label, 34)
    text_x = out_x + direction * 8
    anchor = "start" if right else "end"
    for i, line in enumerate(lines):
        parts.extend(
            label_text(
                text_x,
                y + 16 + i * 19,
                line,
                anchor=anchor,
                background=True,
            )
        )
    return "".join(parts)


def label_text(
    x: float,
    y: float,
    line: str,
    anchor: str = "middle",
    background: bool = True,
) -> list[str]:
    """Texto con un fondo blanco para que las lifelines no lo atraviesen."""
    width = len(line) * 9.2
    if anchor == "middle":
        rect_x = x - width / 2 - 3
    elif anchor == "start":
        rect_x = x - 3
    else:
        rect_x = x - width - 3
    parts = []
    if background:
        parts.append(
            f'<rect x="{rect_x:.1f}" y="{y - 15:.1f}" width="{width + 6:.1f}" '
            f'height="20" fill="#FFFFFF"/>'
        )
    parts.append(
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="17" '
        f'fill="{COLOR_TEXT}" text-anchor="{anchor}">{escape(line)}</text>'
    )
    return parts


def render(diagram: dict) -> str:
    participants = diagram["participants"]
    count = len(participants)
    column = (WIDTH - 2 * MARGIN) / count
    box_w = column - 16

    lifeline_top = HEADER_Y + HEADER_H
    step_start = lifeline_top + 56
    height = step_start + len(diagram["steps"]) * STEP_H + 26

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" '
        f'height="{height}" viewBox="0 0 {WIDTH} {height}">',
        f'<rect width="{WIDTH}" height="{height}" fill="#FFFFFF"/>',
    ]

    for i, name in enumerate(participants):
        x = participant_x(i, count)
        parts.append(
            f'<rect x="{x - box_w / 2:.1f}" y="{HEADER_Y}" width="{box_w:.1f}" '
            f'height="{HEADER_H}" rx="6" fill="{COLOR_HEADER}" '
            f'stroke="{COLOR_HEADER_LINE}" stroke-width="1.5"/>'
        )
        lines = wrap_lines(name, 12)
        start_y = HEADER_Y + HEADER_H / 2 - (len(lines) - 1) * 10 + 6
        for j, line in enumerate(lines):
            parts.append(
                f'<text x="{x:.1f}" y="{start_y + j * 20:.1f}" '
                f'font-family="{FONT}" font-size="17" font-weight="bold" '
                f'fill="#FFFFFF" text-anchor="middle">{escape(line)}</text>'
            )
        parts.append(
            f'<line x1="{x:.1f}" y1="{lifeline_top}" x2="{x:.1f}" '
            f'y2="{height - 20}" stroke="{COLOR_LIFELINE}" stroke-width="1.6" '
            f'stroke-dasharray="7 5"/>'
        )

    for k, (src, dst, label, kind) in enumerate(diagram["steps"]):
        y = step_start + k * STEP_H
        x1 = participant_x(src, count)
        x2 = participant_x(dst, count)

        if src == dst:
            parts.append(self_loop(x1, y, label, right=x1 < WIDTH - 180))
            continue

        color = COLOR_CALL if kind == "call" else COLOR_RETURN
        dash = "" if kind == "call" else ' stroke-dasharray="6 4"'
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" '
            f'stroke="{color}" stroke-width="1.6"{dash}/>'
        )
        direction = 1 if x2 > x1 else -1
        parts.append(arrowhead(x2, y, direction))

        lines = wrap_lines(label, 38)
        mid = (x1 + x2) / 2
        base_y = y - 10 - (len(lines) - 1) * 19
        for j, line in enumerate(lines):
            parts.extend(label_text(mid, base_y + j * 19, line))

    parts.append("</svg>")
    return "\n".join(parts)


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
                "-pix_fmt",
                "rgb24",
                str(png_path),
            ],
            check=True,
        )
        print(f"Generado: {png_path}")


if __name__ == "__main__":
    main()
