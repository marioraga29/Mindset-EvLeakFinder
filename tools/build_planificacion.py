"""Valida la planificación de 2.2 y genera el gráfico de horas estimadas.

Uso:
    python3 tools/build_planificacion.py

Salida:
    tools/diagrams/horas-estimadas.svg / horas-estimadas.png

El PNG se obtiene con ffmpeg (librsvg). No se usan dependencias de Python
externas. El generador de la memoria lee el PNG y lo incrusta en el .docx.
"""

from __future__ import annotations

import datetime as dt
import subprocess
import sys
import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plantilla_content import PLANIFICACION  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools" / "diagrams"
SLUG = "horas-estimadas"

FONT = "DejaVu Sans"
BAR = "#5B9BD5"
BAR_LINE = "#4472C4"
TEXT = "#222222"
MUTED = "#5A6B7B"
GRID = "#D9DEE6"

MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
MESES_LARGO = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
    "septiembre", "octubre", "noviembre", "diciembre",
]
NUMEROS = ["una", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho"]


def inicio() -> dt.date:
    return dt.date(*PLANIFICACION["inicio"])


def lunes(semana: int) -> dt.date:
    return inicio() + dt.timedelta(days=7 * (semana - 1))


def domingo(semana: int) -> dt.date:
    return lunes(semana) + dt.timedelta(days=6)


def fecha_corta(d: dt.date, con_anio: bool = False) -> str:
    texto = f"{d.day} {MESES[d.month - 1]}"
    return f"{texto} {d.year}" if con_anio else texto


def rango_semanas(desde: int, hasta: int) -> str:
    a, b = lunes(desde), domingo(hasta)
    if a.year == b.year:
        return f"{fecha_corta(a)} – {fecha_corta(b, True)}"
    return f"{fecha_corta(a, True)} – {fecha_corta(b, True)}"


def semana_larga(semana: int) -> str:
    """Rango de una semana en prosa: «12 al 18 de octubre de 2026»."""
    a, b = lunes(semana), domingo(semana)
    if a.month == b.month:
        return f"{a.day} al {b.day} de {MESES_LARGO[b.month - 1]} de {b.year}"
    return (
        f"{a.day} de {MESES_LARGO[a.month - 1]} al {b.day} de "
        f"{MESES_LARGO[b.month - 1]} de {b.year}"
    )


def horas_etapa(etapa: dict) -> int:
    return sum(h for _, _, _, h in etapa["acts"])


def rango_etapa(etapa: dict) -> tuple[int, int]:
    return (
        min(d for _, d, _, _ in etapa["acts"]),
        max(h for _, _, h, _ in etapa["acts"]),
    )


def validar() -> None:
    total = 0
    for etapa in PLANIFICACION["etapas"]:
        total += horas_etapa(etapa)
        for nombre, desde, hasta, horas in etapa["acts"]:
            assert 1 <= desde <= hasta <= PLANIFICACION["semanas"], (nombre, desde, hasta)
            assert horas > 0, nombre
    assert total == PLANIFICACION["horas_totales"], f"Las horas suman {total}"
    fin = rango_etapa(PLANIFICACION["etapas"][-1])[1]
    assert fin == PLANIFICACION["semanas"], "La última etapa debe cerrar el calendario"


def render() -> str:
    etapas = PLANIFICACION["etapas"]
    width, height = 1000, 560
    left, right, top, bottom = 90, 30, 50, 150
    plot_w, plot_h = width - left - right, height - top - bottom
    maximo = 150
    paso = plot_w / len(etapas)
    barra = paso * 0.55

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="{FONT}">',
        f'<rect width="{width}" height="{height}" fill="#FFFFFF"/>',
    ]
    for valor in range(0, maximo + 1, 25):
        y = top + plot_h - plot_h * valor / maximo
        out.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left + plot_w}" y2="{y:.1f}" stroke="{GRID}"/>')
        out.append(
            f'<text x="{left - 10}" y="{y + 4:.1f}" font-size="13" fill="{MUTED}" '
            f'text-anchor="end">{valor}</text>'
        )
    out.append(
        f'<text x="24" y="{top + plot_h / 2:.0f}" font-size="14" fill="{MUTED}" '
        f'text-anchor="middle" transform="rotate(-90 24 {top + plot_h / 2:.0f})">'
        "Horas estimadas</text>"
    )
    for i, etapa in enumerate(etapas):
        horas = horas_etapa(etapa)
        x = left + paso * i + (paso - barra) / 2
        h = plot_h * horas / maximo
        y = top + plot_h - h
        out.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{barra:.1f}" height="{h:.1f}" '
            f'fill="{BAR}" stroke="{BAR_LINE}"/>'
        )
        out.append(
            f'<text x="{x + barra / 2:.1f}" y="{y - 8:.1f}" font-size="15" font-weight="bold" '
            f'fill="{TEXT}" text-anchor="middle">{horas} h</text>'
        )
        cx = x + barra / 2
        for j, linea in enumerate(textwrap.wrap(f"{i + 1}. {etapa['corto']}", 16)):
            out.append(
                f'<text x="{cx:.1f}" y="{top + plot_h + 22 + j * 17}" font-size="13" '
                f'fill="{TEXT}" text-anchor="middle">{escape(linea)}</text>'
            )
    out.append(
        f'<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="{MUTED}"/>'
    )
    out.append(
        f'<text x="{left + plot_w}" y="{height - 16}" font-size="14" fill="{MUTED}" '
        f'text-anchor="end">Total estimado: {PLANIFICACION["horas_totales"]} h</text>'
    )
    out.append("</svg>")
    return "\n".join(out)


def main() -> None:
    validar()
    OUT.mkdir(parents=True, exist_ok=True)
    svg = OUT / f"{SLUG}.svg"
    png = OUT / f"{SLUG}.png"
    svg.write_text(render(), encoding="utf-8")
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(svg),
            "-frames:v", "1", "-vf", "scale=iw*2:ih*2", "-pix_fmt", "rgb24", str(png),
        ],
        check=True,
    )
    print(f"Generado: {png}")
    for etapa in PLANIFICACION["etapas"]:
        desde, hasta = rango_etapa(etapa)
        print(f"  {etapa['nombre']}: {horas_etapa(etapa)} h, semanas {desde}-{hasta} ({rango_semanas(desde, hasta)})")


if __name__ == "__main__":
    main()
