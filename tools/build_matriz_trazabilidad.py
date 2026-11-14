"""Genera la matriz de trazabilidad interna entre las 78 fichas y los 21 RF.

Uso:
    python3 tools/build_matriz_trazabilidad.py

Salida:
    docs/03-matriz-trazabilidad.md

La matriz es un documento interno: no se incluye en la memoria oficial. Sirve
para defender de dónde sale cada paso de los flujos y cada criterio de prueba
de los 21 requisitos funcionales de la plantilla.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from plantilla_content import RFS  # noqa: E402

BUILD = ROOT / "tools" / "build_requisitos_docx.py"
OUT = ROOT / "docs" / "03-matriz-trazabilidad.md"

# Correspondencia ficha interna -> RF de la plantilla.
MAPPING = {
    "RF-ING-01": "RF-01",
    "RF-ING-02": "RF-01",
    "RF-ING-03": "RF-01",
    "RF-ING-04": "RF-01",
    "RF-ING-05": "RF-02",
    "RF-ING-06": "RF-02",
    "RF-ING-07": "RF-02",
    "RF-PAR-01": "RF-03",
    "RF-PAR-02": "RF-03",
    "RF-PAR-03": "RF-03",
    "RF-PAR-04": "RF-03",
    "RF-PAR-05": "RF-03",
    "RF-PAR-06": "RF-04",
    "RF-PAR-07": "RF-04",
    "RF-PAR-08": "RF-04",
    "RF-PAR-09": "RF-03",
    "RF-SES-01": "RF-05",
    "RF-SES-02": "RF-05",
    "RF-SES-03": "RF-05",
    "RF-SES-04": "RF-05",
    "RF-SES-05": "RF-05",
    "RF-BAS-01": "RF-06",
    "RF-BAS-02": "RF-07",
    "RF-BAS-03": "RF-06",
    "RF-BAS-04": "RF-07",
    "RF-BAS-05": "RF-07",
    "RF-BAS-06": "RF-06",
    "RF-DET-01": "RF-08",
    "RF-DET-02": "RF-09",
    "RF-DET-03": "RF-09",
    "RF-DET-04": "RF-10",
    "RF-DET-05": "RF-10",
    "RF-DET-06": "RF-11",
    "RF-DET-07": "RF-12",
    "RF-DET-08": "RF-12",
    "RF-DSH-01": "RF-13",
    "RF-DSH-02": "RF-13",
    "RF-DSH-03": "RF-13",
    "RF-DSH-04": "RF-14",
    "RF-DSH-05": "RF-14",
    "RF-DSH-06": "RF-14",
    "RF-DSH-07": "RF-14",
    "RF-DSH-08": "RF-14",
    "RF-DSH-09": "RF-20",
    "RF-DSH-10": "RF-14",
    "RF-HIS-01": "RF-15",
    "RF-HIS-02": "RF-15",
    "RF-HIS-03": "RF-15",
    "RF-HIS-04": "RF-15",
    "RF-HIS-05": "RF-15",
    "RF-VTR-01": "RF-16",
    "RF-VTR-02": "RF-16",
    "RF-VTR-03": "RF-16",
    "RF-VTR-04": "RF-16",
    "RF-VTR-05": "RF-16",
    "RF-VMA-01": "RF-17",
    "RF-VMA-02": "RF-17",
    "RF-VMA-03": "RF-17",
    "RF-VMA-04": "RF-17",
    "RF-VMA-05": "RF-17",
    "RF-VMA-06": "RF-17",
    "RF-ETQ-01": "RF-18",
    "RF-ETQ-02": "RF-18",
    "RF-ETQ-03": "RF-18",
    "RF-ETQ-04": "RF-18",
    "RF-ETQ-05": "RF-18",
    "RF-ETQ-06": "RF-18",
    "RF-ETQ-07": "RF-18",
    "RF-GLO-01": "RF-19",
    "RF-GLO-02": "RF-19",
    "RF-CUE-01": "RF-20",
    "RF-CUE-02": "RF-20",
    "RF-CUE-03": "RF-20",
    "RF-CUE-04": "RF-20",
    "RF-CUE-05": "RF-20",
    "RF-CMP-01": "RF-21",
    "RF-CMP-02": "RF-21",
    "RF-CMP-03": "RF-21",
}

# Ajustes respecto al mapa inicial, documentados para que la matriz sea auditable.
NOTES = {
    "RF-DSH-07": (
        "Se integra en RF-14 porque el resumen del lote se presenta junto al feed "
        "del último lote, no en el bloque de KPIs y fatiga."
    ),
    "RF-DSH-09": (
        "Se integra en RF-20 para no duplicar la configuración de cuenta que ya "
        "cubren RF-CUE-02 y RF-CUE-03."
    ),
}


def load_sections():
    src = BUILD.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(src) if line.startswith("SECTIONS"))
    end = next(i for i in range(start + 1, len(src)) if src[i] == "]")
    ns: dict = {}
    exec("\n".join(src[start:end + 1]), ns)  # noqa: S102
    return ns["SECTIONS"]


def main() -> None:
    sections = load_sections()
    rows = []
    for num, title, _intro, reqs in sections:
        for req in reqs:
            rid = req["id"]
            if rid not in MAPPING:
                raise SystemExit(f"Ficha sin RF asignado: {rid}")
            rows.append(
                {
                    "id": rid,
                    "title": req["title"],
                    "module": f"{num} {title}",
                    "rf": MAPPING[rid],
                    "crit": len(req["crit"]),
                }
            )

    if len(rows) != 78:
        raise SystemExit(f"Se esperaban 78 fichas y hay {len(rows)}")

    rf_names = {rf["id"]: rf["name"] for rf in RFS}
    rf_order = [rf["id"] for rf in RFS]

    by_rf: dict[str, list[dict]] = {rf: [] for rf in rf_order}
    for row in rows:
        by_rf[row["rf"]].append(row)

    lines: list[str] = []
    lines.append("# Matriz de trazabilidad interna")
    lines.append("")
    lines.append(
        "> Documento interno. No forma parte de la entrega de la memoria. "
        "Las 78 fichas se conservan aquí como criterios de aceptación y como "
        "trazabilidad de los 21 requisitos funcionales de la plantilla oficial."
    )
    lines.append("")
    lines.append("## 1. Correspondencia entre los 21 RF y las fichas internas")
    lines.append("")
    lines.append("| RF | Nombre | Fichas absorbidas | Fichas | Criterios |")
    lines.append("|---|---|---|---:|---:|")
    total_fichas = 0
    total_crit = 0
    for rf in rf_order:
        items = by_rf[rf]
        ids = ", ".join(item["id"] for item in items)
        n = len(items)
        c = sum(item["crit"] for item in items)
        total_fichas += n
        total_crit += c
        lines.append(f"| {rf} | {rf_names[rf]} | {ids} | {n} | {c} |")
    lines.append(f"| **Total** | | | **{total_fichas}** | **{total_crit}** |")
    lines.append("")
    lines.append("## 2. Matriz completa por módulo")
    lines.append("")
    lines.append("| Ficha | Nombre | Módulo | RF | Criterios |")
    lines.append("|---|---|---|---:|---:|")
    current_module = None
    for row in rows:
        if row["module"] != current_module:
            current_module = row["module"]
            lines.append(
                f"| | **{current_module}** | | | |"
            )
        lines.append(
            f"| {row['id']} | {row['title']} | {row['module']} | "
            f"{row['rf']} | {row['crit']} |"
        )
    lines.append("")
    lines.append("## 3. Ajustes respecto al mapa inicial")
    lines.append("")
    lines.append(
        "El mapa inicial asignaba RF-DSH-07 a RF-13 y RF-DSH-09 a RF-14. "
        "La redacción final de los flujos aconseja dos ajustes para evitar "
        "duplicidades:"
    )
    lines.append("")
    for rid, note in NOTES.items():
        lines.append(f"- **{rid}**: {note}")
    lines.append("")
    lines.append("## 4. Cómo se usa esta matriz")
    lines.append("")
    lines.append(
        "Cada fila de la matriz identifica la ficha interna que origina uno o "
        "varios pasos del flujo normal, del flujo alternativo o de las "
        "postcondiciones del RF correspondiente. Los criterios de la ficha se "
        "conservan íntegros en `docs/entrega/Requisitos-Funcionales-TFG.docx`, "
        "que pasa a ser el documento interno de detalle. La memoria oficial "
        "solo incluye los 21 RF, los 11 RNF y las 16 entidades de "
        "almacenamiento."
    )
    lines.append("")
    lines.append("## 5. Diagramas de secuencia de 7.1.6")
    lines.append("")
    lines.append(
        "Los tres diagramas de la memoria oficial cubren los flujos de extremo a "
        "extremo. Esta tabla indica qué RF ilustra cada uno."
    )
    lines.append("")
    lines.append("| Ilustración | Flujo | RF cubiertos |")
    lines.append("|---:|---|---|")
    lines.append(
        "| 2 | Importación y procesamiento del lote | RF-01 a RF-06 y RF-08 a RF-12 |"
    )
    lines.append("| 3 | Auditoría de una alerta | RF-14, RF-16, RF-17 y RF-18 |")
    lines.append(
        "| 4 | Cálculo del baseline y detección | RF-06 a RF-12 |"
    )
    lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generado: {OUT}")
    print(f"Fichas: {total_fichas} | Criterios: {total_crit}")


if __name__ == "__main__":
    main()
