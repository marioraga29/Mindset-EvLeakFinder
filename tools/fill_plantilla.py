"""Rellena los apartados 7.1.1 a 7.1.5 de la plantilla oficial del TFG.

Uso:
    python3 tools/fill_plantilla.py

Entrada:
    sources/Plantilla - Documentación.docx
Salida:
    docs/entrega/Memoria-TFG-requisitos.docx

El script conserva portada, estilos, índice, encabezados y el resto del
documento. Sustituye 7.1.1 a 7.1.6 y 7.4.1, y añade ``w:updateFields`` para
que Word actualice el índice y la tabla de ilustraciones al abrir el archivo.
"""

from __future__ import annotations

import datetime as dt
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_secuencias import DIAGRAMS as SEQ_DIAGRAMS  # noqa: E402
from plantilla_content import (  # noqa: E402
    ACTORS, BACKLOG, CASOS_USO, GESTION_DESCUBRIMIENTO, PLANIFICACION, RFS, RIS, RNFS,
)
from build_planificacion import (  # noqa: E402
    MESES, MESES_LARGO, NUMEROS, SLUG as PLAN_SLUG, domingo, horas_etapa, lunes,
    rango_etapa, rango_semanas, semana_larga, validar as validar_planificacion,
)

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "sources" / "Plantilla - Documentación.docx"
DST = ROOT / "docs" / "entrega" / "Memoria-TFG-requisitos.docx"

SECTION_PREFIXES = [
    "7.1.1 Product Backlog",
    "7.1.2 Definición de actores del sistema",
    "7.1.3 Requisitos funcionales",
    "7.1.4 Requisitos no funcionales",
    "7.1.5 Requisitos de almacenamiento de información",
    "7.1.6 Definición de diagramas de secuencias",
]


# ---------------------------------------------------------------------------
# Lectura y troceado del cuerpo
# ---------------------------------------------------------------------------

def split_top(body: str) -> list[tuple[str, str]]:
    """Divide el cuerpo en elementos XML de primer nivel."""
    els: list[tuple[str, str]] = []
    i = 0
    n = len(body)
    while i < n:
        if body[i] != "<":
            i += 1
            continue
        m = re.match(r"<(w:[A-Za-z]+)", body[i:])
        if not m:
            i += 1
            continue
        tag = m.group(1)
        j = body.find(">", i)
        if body[j - 1] == "/":
            els.append((tag, body[i:j + 1]))
            i = j + 1
            continue
        if tag in ("w:p", "w:sectPr", "w:bookmarkStart", "w:bookmarkEnd"):
            close = f"</{tag}>"
            k = body.find(close, j)
            els.append((tag, body[i:k + len(close)]))
            i = k + len(close)
            continue
        if tag == "w:tbl":
            depth = 1
            k = j + 1
            while depth > 0:
                nxt = re.search(r"<(/?)w:tbl(?=[ >])", body[k:])
                if not nxt:
                    raise ValueError("Tabla sin cerrar en document.xml")
                if nxt.group(1) == "/":
                    depth -= 1
                else:
                    depth += 1
                k += nxt.end()
            k = body.find(">", k - 1) + 1
            els.append((tag, body[i:k]))
            i = k
            continue
        close = f"</{tag}>"
        k = body.find(close, j)
        if k == -1:
            els.append((tag, body[i:j + 1]))
            i = j + 1
        else:
            els.append((tag, body[i:k + len(close)]))
            i = k + len(close)
    return els


def element_text(e: str) -> str:
    return "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", e))


def find_heading(els: list[tuple[str, str]], prefix: str) -> int:
    """Localiza una cabecera Ttulo3 por su texto, ignorando el índice."""
    for i, (tag, e) in enumerate(els):
        if tag != "w:p":
            continue
        style = re.search(r'<w:pStyle w:val="([^"]+)"', e)
        if not style or style.group(1) != "Ttulo3":
            continue
        if element_text(e).strip().startswith(prefix):
            return i
    raise ValueError(f"No se encontró la cabecera: {prefix}")


def find_any_heading(els: list[tuple[str, str]], prefix: str) -> int:
    """Localiza una cabecera TtuloN, incluida Ttulo2."""
    for i, (tag, e) in enumerate(els):
        if tag != "w:p":
            continue
        style = re.search(r'<w:pStyle w:val="(Ttulo\d+)"', e)
        if not style:
            continue
        if element_text(e).strip().startswith(prefix):
            return i
    raise ValueError(f"No se encontró la cabecera: {prefix}")


def first_table_after(els: list[tuple[str, str]], idx: int) -> str:
    for tag, e in els[idx + 1:]:
        if tag == "w:tbl":
            return e
    raise ValueError(f"No hay tabla después del elemento {idx}")


# ---------------------------------------------------------------------------
# Construcción de tablas y párrafos
# ---------------------------------------------------------------------------

def strip_para_ids(xml: str) -> str:
    return re.sub(r'\s+w14:(?:paraId|textId)="[^"]*"', "", xml)


def make_paragraph(text: str, ppr: str = "", rpr: str = "") -> str:
    return (
        f"<w:p>{ppr}<w:r>{rpr}"
        f'<w:t xml:space="preserve">{escape(text)}</w:t>'
        f"</w:r></w:p>"
    )


def fill_cell(tc: str, value: str | list[str]) -> str:
    """Sustituye el contenido de una celda conservando su formato."""
    tcpr_m = re.search(r"<w:tcPr>.*?</w:tcPr>", tc, re.S)
    tcpr = tcpr_m.group(0) if tcpr_m else ""

    p_m = re.search(r"<w:p[ >].*?</w:p>", tc, re.S)
    p = p_m.group(0) if p_m else "<w:p/>"
    ppr_m = re.search(r"<w:pPr>.*?</w:pPr>", p, re.S)
    ppr = ppr_m.group(0) if ppr_m else ""

    rpr = ""
    r_m = re.search(r"<w:r[ >].*?</w:r>", p, re.S)
    if r_m:
        rpr_m = re.search(r"<w:rPr>.*?</w:rPr>", r_m.group(0), re.S)
        if rpr_m:
            rpr = rpr_m.group(0)
    if not rpr:
        rpr_m = re.search(r"<w:rPr>.*?</w:rPr>", ppr, re.S)
        if rpr_m:
            rpr = rpr_m.group(0)

    lines = value if isinstance(value, list) else [value]
    lines = [line for line in lines if line and line.strip()]
    if not lines:
        paras = f"<w:p>{ppr}</w:p>"
    else:
        paras = "".join(make_paragraph(line, ppr, rpr) for line in lines)
    return f"<w:tc>{tcpr}{paras}</w:tc>"


def replace_cell(row: str, index: int, value: str | list[str]) -> str:
    cells = list(re.finditer(r"<w:tc[ >].*?</w:tc>", row, re.S))
    m = cells[index]
    return row[:m.start()] + fill_cell(m.group(0), value) + row[m.end():]


def table_parts(table: str) -> tuple[str, list[str], str]:
    rows = re.findall(r"<w:tr[ >].*?</w:tr>", table, re.S)
    prefix = table[:table.index(rows[0])]
    suffix = table[table.rindex(rows[-1]) + len(rows[-1]):]
    return prefix, rows, suffix


def set_sz(xml: str, sz: int) -> str:
    """Fija el tamaño de fuente (en medios puntos) de un fragmento."""
    xml = re.sub(r'<w:sz w:val="\d+"\s*/>', f'<w:sz w:val="{sz}"/>', xml)
    xml = re.sub(r'<w:szCs w:val="\d+"\s*/>', f'<w:szCs w:val="{sz}"/>', xml)
    return xml


def resize_row(row: str, sizes: list[int]) -> str:
    cells = list(re.finditer(r"<w:tc[ >].*?</w:tc>", row, re.S))
    out = row
    for m, sz in reversed(list(zip(cells, sizes))):
        tc = set_sz(m.group(0), sz)
        out = out[:m.start()] + tc + out[m.end():]
    return out


def compact(
    table: str,
    header_rows: int = 1,
    label: bool = False,
    label_sz: int = 22,
    value_sz: int = 20,
) -> str:
    """Reduce el cuerpo de la tabla para que no ocupe páginas enteras.

    La fila de nombre se conserva a 14 pt. Las etiquetas de la primera
    columna quedan a 11 pt y los valores a 10 pt.
    """
    prefix, rows, suffix = table_parts(table)
    out: list[str] = []
    for i, row in enumerate(rows):
        if i < header_rows:
            out.append(row)
            continue
        n = len(re.findall(r"<w:tc[ >]", row))
        sizes = [label_sz if label and j == 0 else value_sz for j in range(n)]
        out.append(resize_row(row, sizes))
    return prefix + "".join(out) + suffix


def build_backlog_table(base: str) -> str:
    prefix, rows, suffix = table_parts(base)
    header, even, odd = rows[0], rows[1], rows[2]
    data = []
    for i, hu in enumerate(BACKLOG):
        row = even if i % 2 == 0 else odd
        row = replace_cell(row, 0, hu["id"])
        row = replace_cell(row, 1, hu["desc"])
        row = replace_cell(row, 2, hu["priority"])
        data.append(row)
    return compact(strip_para_ids(prefix + header + "".join(data) + suffix))


def build_two_row_table(base: str, name: str, desc: str | list[str]) -> str:
    prefix, rows, suffix = table_parts(base)
    row0 = replace_cell(rows[0], 1, name)
    row1 = replace_cell(rows[1], 1, desc)
    return compact(strip_para_ids(prefix + row0 + row1 + suffix), label=True)


def build_rf_table(base: str, rf: dict) -> str:
    prefix, rows, suffix = table_parts(base)
    normal = [f"{i}. {step}" for i, step in enumerate(rf["normal"], 1)]
    alt = [f"• {step}" for step in rf["alt"]]
    values = [
        f"{rf['id']}. {rf['name']}",
        rf["desc"],
        rf["actors"],
        rf["pre"],
        normal,
        alt,
        rf["post"],
    ]
    new_rows = [replace_cell(row, 1, value) for row, value in zip(rows, values)]
    return compact(strip_para_ids(prefix + "".join(new_rows) + suffix), label=True)


def build_rnf_table(base: str, rnf: dict) -> str:
    prefix, rows, suffix = table_parts(base)
    desc = [rnf["desc"], "Criterios de aceptación:"]
    desc += [f"• {c}" for c in rnf["crit"]]
    desc += [f"Verificación: {rnf['ver']}"]
    values = [f"{rnf['id']}. {rnf['name']}", desc]
    new_rows = [replace_cell(row, 1, value) for row, value in zip(rows, values)]
    return compact(strip_para_ids(prefix + "".join(new_rows) + suffix), label=True)


def build_ri_table(base: str, ri: dict) -> str:
    prefix, rows, suffix = table_parts(base)
    values = [
        f"{ri['id']}. {ri['name']}",
        ri["desc"],
        ri["attrs"],
    ]
    new_rows = [replace_cell(row, 1, value) for row, value in zip(rows, values)]
    return compact(strip_para_ids(prefix + "".join(new_rows) + suffix), label=True)


def build_caso_uso_table(base: str, caso: dict) -> str:
    """Rellena la tabla de 7.4.1: título y pares prueba/salida esperada."""
    prefix, rows, suffix = table_parts(base)
    values = {
        0: f"{caso['id']}. {caso['name']}",
        2: caso["pos_prueba"],
        3: caso["pos_salida"],
        5: caso["neg_prueba"],
        6: caso["neg_salida"],
    }
    new_rows = []
    for i, row in enumerate(rows):
        if i in values:
            row = replace_cell(row, 0 if i == 0 else 1, values[i])
        new_rows.append(row)
    return compact(
        strip_para_ids(prefix + "".join(new_rows) + suffix), label=True
    )


def intro(text: str) -> str:
    return (
        '<w:p><w:pPr><w:pStyle w:val="Normal"/></w:pPr>'
        f'<w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'
    )


def caption(number: int, text: str) -> str:
    return (
        '<w:p><w:pPr><w:pStyle w:val="Ttulo6"/></w:pPr>'
        f'<w:r><w:t xml:space="preserve">Tabla {number}: {escape(text)}</w:t></w:r>'
        "</w:p>"
    )


def empty() -> str:
    return "<w:p/>"


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"No es un PNG: {path}")
    return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")


def image_paragraph(rId: str, cx: int, cy: int, doc_id: int, name: str) -> str:
    return (
        '<w:p><w:pPr><w:spacing w:line="0" w:lineRule="atLeast"/>'
        '<w:ind w:right="4"/><w:rPr><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
        "</w:pPr><w:r><w:rPr><w:noProof/><w:sz w:val=\"22\"/>"
        '<w:szCs w:val="22"/></w:rPr><w:drawing '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{cx}" cy="{cy}"/>'
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        f'<wp:docPr id="{doc_id}" name="{escape(name)}"/>'
        '<wp:cNvGraphicFramePr><a:graphicFrameLocks noChangeAspect="1"/>'
        "</wp:cNvGraphicFramePr><a:graphic><a:graphicData "
        'uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic><pic:nvPicPr>'
        f'<pic:cNvPr id="0" name="{escape(name)}"/>'
        '<pic:cNvPicPr><a:picLocks noChangeAspect="1" noChangeArrowheads="1"/>'
        "</pic:cNvPicPr></pic:nvPicPr><pic:blipFill>"
        f'<a:blip r:embed="{rId}"/><a:srcRect/>'
        "<a:stretch><a:fillRect/></a:stretch></pic:blipFill>"
        '<pic:spPr bwMode="auto"><a:xfrm><a:off x="0" y="0"/>'
        f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        "<a:noFill/><a:ln><a:noFill/></a:ln></pic:spPr></pic:pic>"
        "</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>"
    )


def caption_ilustracion(number: int, text: str) -> str:
    return (
        '<w:p><w:pPr><w:pStyle w:val="Ttulo7"/></w:pPr>'
        f'<w:r><w:t xml:space="preserve">Ilustración {number}: '
        f"{escape(text)}</w:t></w:r></w:p>"
    )


def build_secuencias_section() -> list[str]:
    parts = [
        intro(
            "Se definen los diagramas de secuencia de los tres flujos principales: "
            "la importación y el procesamiento de un lote, la auditoría de una alerta "
            "y el cálculo del baseline con la detección de anomalías."
        )
    ]
    cx = 5_400_000
    for i, diagram in enumerate(SEQ_DIAGRAMS):
        png = ROOT / "tools" / "diagrams" / f"{diagram['slug']}.png"
        if not png.exists():
            raise SystemExit(
                f"No existe {png}. Ejecuta antes: python3 tools/build_secuencias.py"
            )
        width, height = png_size(png)
        cy = round(cx * height / width)
        parts.append(
            image_paragraph(
                f"rId{200 + i}",
                cx,
                cy,
                100 + i,
                diagram["title"],
            )
        )
        parts.append(caption_ilustracion(2 + i, diagram["title"]))
        parts.append(empty())
    return parts


PLAN_RID = "rId210"


def add_image_relationships(rels: bytes) -> bytes:
    text = rels.decode("utf-8")
    extra = ""
    if f'Id="{PLAN_RID}"' not in text:
        extra += (
            f'<Relationship Id="{PLAN_RID}" Type="http://schemas.openxmlformats.org/'
            f'officeDocument/2006/relationships/image" '
            f'Target="media/{PLAN_SLUG}.png"/>'
        )
    for i, diagram in enumerate(SEQ_DIAGRAMS):
        rId = f"rId{200 + i}"
        if f'Id="{rId}"' in text:
            continue
        extra += (
            f'<Relationship Id="{rId}" Type="http://schemas.openxmlformats.org/'
            f'officeDocument/2006/relationships/image" '
            f'Target="media/{diagram["slug"]}.png"/>'
        )
    return text.replace("</Relationships>", extra + "</Relationships>").encode("utf-8")


# ---------------------------------------------------------------------------
# Secciones
# ---------------------------------------------------------------------------

def find_heading_text(els: list[str], prefix: str) -> int:
    """Localiza una cabecera Ttulo3 en una lista de fragmentos ya serializados."""
    for i, e in enumerate(els):
        style = re.search(r'<w:pStyle w:val="([^"]+)"', e)
        if not style or style.group(1) != "Ttulo3":
            continue
        if element_text(e).strip().startswith(prefix):
            return i
    raise ValueError(f"No se encontró la cabecera: {prefix}")


def first_table_after_text(els: list[str], idx: int) -> str:
    for e in els[idx + 1:]:
        if e.startswith("<w:tbl"):
            return e
    raise ValueError(f"No hay tabla después del elemento {idx}")


def find_any_heading_text(els: list[str], prefix: str) -> int:
    """Localiza cualquier cabecera TtuloN, incluida Ttulo2."""
    for i, e in enumerate(els):
        style = re.search(r'<w:pStyle w:val="(Ttulo\d+)"', e)
        if not style:
            continue
        if element_text(e).strip().startswith(prefix):
            return i
    raise ValueError(f"No se encontró la cabecera: {prefix}")


def build_sections(els: list[tuple[str, str]]) -> dict[str, list[str]]:
    i711 = find_heading(els, SECTION_PREFIXES[0])
    i712 = find_heading(els, SECTION_PREFIXES[1])
    i713 = find_heading(els, SECTION_PREFIXES[2])
    i714 = find_heading(els, SECTION_PREFIXES[3])
    i715 = find_heading(els, SECTION_PREFIXES[4])

    base_backlog = first_table_after(els, i711)
    base_actor = first_table_after(els, i712)
    base_rf = first_table_after(els, i713)
    base_rnf = first_table_after(els, i714)
    base_ri = first_table_after(els, i715)

    table_no = 16
    sections: dict[str, list[str]] = {}

    parts = [
        intro(
            "El Product Backlog recoge las dieciocho historias de usuario del MVP, "
            "agrupadas en cinco epics que siguen el recorrido del jugador. "
            "La prioridad expresa el orden de implementación acordado, no el valor "
            "económico de la funcionalidad."
        ),
        build_backlog_table(base_backlog),
        caption(table_no, "Product Backlog"),
        empty(),
    ]
    table_no += 1
    sections["7.1.1"] = parts

    parts = [
        intro(
            "El MVP define dos actores: el jugador, único actor humano, y el sistema, "
            "que ejecuta el pipeline de análisis."
        )
    ]
    for actor in ACTORS:
        parts.append(build_two_row_table(base_actor, actor["name"], actor["desc"]))
        parts.append(caption(table_no, f"Actor {actor['name']}"))
        parts.append(empty())
        table_no += 1
    sections["7.1.2"] = parts

    parts = [
        intro(
            "Se especifican veintiún requisitos funcionales. Cada uno se describe con su "
            "nombre, descripción, actores, precondiciones, flujo normal, flujo "
            "alternativo y postcondiciones."
        )
    ]
    for rf in RFS:
        parts.append(build_rf_table(base_rf, rf))
        parts.append(caption(table_no, rf["id"]))
        parts.append(empty())
        table_no += 1
    sections["7.1.3"] = parts

    parts = [
        intro(
            "Se recogen doce requisitos no funcionales, agrupados por calidad de uso, "
            "eficiencia, protección, fiabilidad, evolución, portabilidad y localización."
        )
    ]
    for rnf in RNFS:
        parts.append(build_rnf_table(base_rnf, rnf))
        parts.append(caption(table_no, rnf["id"]))
        parts.append(empty())
        table_no += 1
    sections["7.1.4"] = parts

    parts = [
        intro(
            "Se describen las dieciséis entidades que almacenan la información del MVP, "
            "con su descripción y sus atributos principales."
        )
    ]
    for ri in RIS:
        parts.append(build_ri_table(base_ri, ri))
        parts.append(caption(table_no, ri["id"]))
        parts.append(empty())
        table_no += 1
    sections["7.1.5"] = parts

    return sections


def build_casos_uso(base: str, table_no: int) -> list[str]:
    parts = [
        intro(
            "Se recoge un caso de uso por requisito funcional, con una prueba "
            "positiva y una negativa y la salida esperada de cada una."
        )
    ]
    for caso in CASOS_USO:
        parts.append(build_caso_uso_table(base, caso))
        parts.append(caption(table_no, caso["id"]))
        parts.append(empty())
        table_no += 1
    return parts


# ---------------------------------------------------------------------------
# 2.2 Planificación temporal del problema
# ---------------------------------------------------------------------------

GANTT_VERDE = "70AD47"
GANTT_ETAPA = "D5DCE4"
GANTT_ANCHO = 9000


def rich_paragraph(parts: list[tuple[str, bool]]) -> str:
    runs = "".join(
        "<w:r>" + ("<w:rPr><w:b/><w:bCs/></w:rPr>" if bold else "")
        + f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r>'
        for text, bold in parts
    )
    return f'<w:p><w:pPr><w:pStyle w:val="Normal"/></w:pPr>{runs}</w:p>'


def gantt_cell(
    width: int,
    text: str = "",
    *,
    span: int = 1,
    vmerge: str | None = None,
    fill: str = "auto",
    sz: int = 16,
    bold: bool = False,
    align: str = "center",
) -> str:
    tcpr = f'<w:tcW w:w="{width}" w:type="dxa"/>'
    if span > 1:
        tcpr += f'<w:gridSpan w:val="{span}"/>'
    if vmerge == "restart":
        tcpr += '<w:vMerge w:val="restart"/>'
    elif vmerge == "cont":
        tcpr += "<w:vMerge/>"
    tcpr += f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/><w:vAlign w:val="center"/>'
    rpr = (
        "<w:rPr>" + ("<w:b/><w:bCs/>" if bold else "")
        + f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
    )
    run = (
        f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>' if text else ""
    )
    para = (
        '<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" '
        f'w:lineRule="auto"/><w:jc w:val="{align}"/>{rpr}</w:pPr>{run}</w:p>'
    )
    return f"<w:tc><w:tcPr>{tcpr}</w:tcPr>{para}</w:tc>"


def gantt_row(cells: list[str], height: int = 280) -> str:
    return (
        f'<w:tr><w:trPr><w:cantSplit/><w:trHeight w:val="{height}" '
        f'w:hRule="atLeast"/></w:trPr>{"".join(cells)}</w:tr>'
    )


def build_gantt_table(etapa: dict, numero: int) -> str:
    """Tabla semanal de una etapa: una fila verde (estimada) y otra vacía (real) por actividad."""
    desde, hasta = rango_etapa(etapa)
    semanas = list(range(desde, hasta + 1))
    n = len(semanas)
    ancho = min(700, 6000 // n)
    ancho_act = GANTT_ANCHO - n * ancho

    borde = "".join(
        f'<w:{lado} w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        for lado in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    prefix = (
        '<w:tbl><w:tblPr>'
        f'<w:tblW w:w="{GANTT_ANCHO}" w:type="dxa"/><w:tblInd w:w="0" w:type="dxa"/>'
        f"<w:tblBorders>{borde}</w:tblBorders>"
        '<w:tblLayout w:type="fixed"/>'
        '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="60" w:type="dxa"/>'
        '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="60" w:type="dxa"/></w:tblCellMar>'
        '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
        'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
        "<w:tblGrid>"
        + f'<w:gridCol w:w="{ancho_act}"/>'
        + f'<w:gridCol w:w="{ancho}"/>' * n
        + "</w:tblGrid>"
    )

    # Fila de meses: cada mes agrupa las semanas cuyo lunes cae en él.
    meses: list[tuple[str, int]] = []
    for k in semanas:
        mes = MESES[lunes(k).month - 1].capitalize()
        if meses and meses[-1][0] == mes:
            meses[-1] = (mes, meses[-1][1] + 1)
        else:
            meses.append((mes, 1))
    filas = [
        gantt_row(
            [gantt_cell(ancho_act, vmerge="restart")]
            + [gantt_cell(ancho * c, m, span=c, sz=14) for m, c in meses]
        ),
        gantt_row(
            [gantt_cell(ancho_act, vmerge="cont")]
            + [gantt_cell(ancho, str(k), sz=14) for k in semanas]
        ),
        gantt_row(
            [
                gantt_cell(ancho_act, "Actividades", bold=True, align="left"),
                gantt_cell(ancho * n, span=n),
            ]
        ),
        gantt_row(
            [
                gantt_cell(ancho_act, etapa["nombre"], bold=True, fill=GANTT_ETAPA,
                           sz=18, align="left"),
                gantt_cell(ancho * n, span=n),
            ],
            height=380,
        ),
    ]
    for j, (nombre, a, b, horas) in enumerate(etapa["acts"], 1):
        etiqueta = f"{numero}.{j} {nombre} ({horas} h)"
        estimada = [
            gantt_cell(ancho, fill=GANTT_VERDE if a <= k <= b else "auto") for k in semanas
        ]
        real = [gantt_cell(ancho) for _ in semanas]
        filas.append(gantt_row(
            [gantt_cell(ancho_act, etiqueta, vmerge="restart", align="left")] + estimada
        ))
        filas.append(gantt_row([gantt_cell(ancho_act, vmerge="cont")] + real))
    return prefix + "".join(filas) + "</w:tbl>"


def build_planificacion_section(legend: list[str]) -> list[str]:
    """Contenido de 2.2: etapas, diagramas de Gantt, reparto de horas y cierre."""
    validar_planificacion()
    etapas = PLANIFICACION["etapas"]
    total = PLANIFICACION["horas_totales"]
    n_sem = PLANIFICACION["semanas"]
    parts = [
        intro(
            "Para la planificación del Trabajo de Fin de Grado se ha decidido su división "
            f"en {NUMEROS[len(etapas) - 1]} etapas fundamentales, que siguen las fases del marco de "
            "trabajo (descubrimiento, desarrollo y operaciones) y añaden el estudio previo "
            "del problema y la documentación:"
        ),
    ]
    for i, etapa in enumerate(etapas, 1):
        parts.append(intro(f"• Etapa {i}. {etapa['nombre']}."))
    parts += [
        empty(),
        intro(
            f"El proyecto se extiende desde la semana del {lunes(1).day} de octubre de "
            f"{lunes(1).year} hasta finales de mayo de {domingo(n_sem).year}, con {n_sem} "
            f"semanas y una dedicación media de unas {round(total / n_sem)} horas "
            f"semanales. Las {total} horas estimadas son las mismas que se emplean en la "
            "estimación de costes del apartado 2.1."
        ),
        empty(),
        intro(
            "Teniendo claras las diferentes etapas, se detallan las actividades asociadas "
            "a cada una con su duración estimada en horas. Las columnas de cada diagrama "
            f"numeran las semanas del proyecto: la semana 1 va del {semana_larga(1)} "
            f"y la semana {n_sem}, del {semana_larga(n_sem)}."
        ),
        empty(),
        intro(
            "Para más claridad, se ha realizado un Diagrama de Gantt por etapa. Cada "
            "actividad ocupa dos filas: la superior, en verde, recoge la planificación "
            "estimada; la inferior, que de momento queda vacía, recogerá en rojo la "
            "planificación real cuando concluya el proyecto."
        ),
        empty(),
    ]
    parts += legend
    parts.append(empty())

    table_no = 7
    for i, etapa in enumerate(etapas, 1):
        desde, hasta = rango_etapa(etapa)
        parts.append(rich_paragraph([
            (f"Etapa {i}. ", False),
            (etapa["nombre"], True),
            (
                f" ({horas_etapa(etapa)} horas, {rango_semanas(desde, hasta)}). "
                f"Esta etapa {etapa['desc']}",
                False,
            ),
        ]))
        parts.append(empty())
        parts.append(build_gantt_table(etapa, i))
        parts.append(caption(table_no, f"Planificación de la etapa {i}: {etapa['nombre']}"))
        parts.append(empty())
        table_no += 1

    png = ROOT / "tools" / "diagrams" / f"{PLAN_SLUG}.png"
    if not png.exists():
        raise SystemExit(
            f"No existe {png}. Ejecuta antes: python3 tools/build_planificacion.py"
        )
    width, height = png_size(png)
    cx = 5_400_000
    parts += [
        intro(
            f"La siguiente ilustración resume el reparto de las {total} horas estimadas "
            "entre las etapas. La implementación concentra el mayor esfuerzo, seguida del "
            "plan, de la fase de descubrimiento y de la documentación."
        ),
        empty(),
        image_paragraph(PLAN_RID, cx, round(cx * height / width), 110, "Horas estimadas por etapa"),
        caption_ilustracion(1, "Horas estimadas por etapa"),
        empty(),
        intro(
            "Al concluir el proyecto se añadirán las horas reales de cada etapa y la "
            "desviación respecto a esta estimación."
        ),
        empty(),
    ]
    return parts


def replace_planificacion(els: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Sustituye el cuerpo de 2.2 conservando el encabezado y la leyenda de colores."""
    i22 = find_any_heading(els, "2.2 Planificación temporal")
    i3 = find_any_heading(els, "3. Prácticas")
    verde = next(
        k for k in range(i22, i3)
        if element_text(els[k][1]).strip().startswith("Color verde")
    )
    legend = [els[verde - 1][1], els[verde][1], els[verde + 1][1]]
    assert element_text(legend[0]).strip().startswith("Nota")
    assert element_text(legend[2]).strip().startswith("Color rojo")
    nuevos = [
        ("w:tbl" if e.startswith("<w:tbl") else "w:p", e)
        for e in build_planificacion_section(legend)
    ]
    return els[:i22 + 1] + nuevos + els[i3:]


# ---------------------------------------------------------------------------
# 5.1 Gestión de la fase de descubrimiento
# ---------------------------------------------------------------------------

GESTION_VERDE = "92D050"
GESTION_GRIS = "EDEDED"
GESTION_ETIQUETA = 2300
GESTION_DIA = 335
DIAS_SEMANA = ["L", "M", "X", "J", "V"]


def _fecha(valor: tuple[int, int, int]) -> dt.date:
    return dt.date(*valor)


def _laborables(desde: dt.date, hasta: dt.date) -> list[dt.date]:
    dias = []
    d = desde
    while d <= hasta:
        if d.weekday() < 5:
            dias.append(d)
        d += dt.timedelta(days=1)
    return dias


def _fecha_larga(d: dt.date) -> str:
    return f"{d.day} de {MESES_LARGO[d.month - 1]}"


def _rango_prosa(desde: dt.date, hasta: dt.date) -> str:
    if desde.month == hasta.month:
        return f"del {desde.day} al {hasta.day} de {MESES_LARGO[hasta.month - 1]}"
    return f"del {_fecha_larga(desde)} al {_fecha_larga(hasta)}"


def build_gestion_table(cfg: dict) -> str:
    """Tabla Plan-Do-Check-Act por sprint: columnas L a V de cuatro semanas."""
    inicio_sem = _fecha(cfg["inicio"])
    semanas = cfg["semanas"]
    n_dias = semanas * 5
    ancho_total = GESTION_ETIQUETA + n_dias * GESTION_DIA
    fechas = [
        inicio_sem + dt.timedelta(days=7 * (c // 5) + c % 5) for c in range(n_dias)
    ]

    borde = "".join(
        f'<w:{lado} w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        for lado in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    prefix = (
        "<w:tbl><w:tblPr>"
        f'<w:tblW w:w="{ancho_total}" w:type="dxa"/><w:tblInd w:w="0" w:type="dxa"/>'
        f"<w:tblBorders>{borde}</w:tblBorders>"
        '<w:tblLayout w:type="fixed"/>'
        '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="40" w:type="dxa"/>'
        '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="40" w:type="dxa"/></w:tblCellMar>'
        '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" '
        'w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>'
        "<w:tblGrid>"
        + f'<w:gridCol w:w="{GESTION_ETIQUETA}"/>'
        + f'<w:gridCol w:w="{GESTION_DIA}"/>' * n_dias
        + "</w:tblGrid>"
    )

    def cabecera_semana(k: int) -> str:
        a = fechas[k * 5]
        b = fechas[k * 5 + 4]
        if a.month == b.month:
            return f"{a.day}-{b.day} {MESES_LARGO[b.month - 1].upper()}"
        return f"{a.day} {MESES[a.month - 1].upper()}-{b.day} {MESES[b.month - 1].upper()}"

    filas = [
        gantt_row(
            [gantt_cell(GESTION_ETIQUETA, vmerge="restart")]
            + [
                gantt_cell(GESTION_DIA * 5, cabecera_semana(k), span=5, sz=12, bold=True)
                for k in range(semanas)
            ],
            height=300,
        ),
        gantt_row(
            [gantt_cell(GESTION_ETIQUETA, vmerge="cont")]
            + [
                gantt_cell(GESTION_DIA, DIAS_SEMANA[c % 5], sz=12, fill=GESTION_GRIS)
                for c in range(n_dias)
            ],
            height=260,
        ),
    ]

    def fila_vacia(etiqueta: str, *, titulo: bool = False, activos=frozenset()) -> str:
        celdas = [
            gantt_cell(
                GESTION_ETIQUETA, etiqueta, sz=16, bold=titulo, align="left",
                fill=GESTION_GRIS if titulo else "auto",
            )
        ]
        for f in fechas:
            if f in activos:
                relleno = GESTION_VERDE
            else:
                relleno = GESTION_GRIS if titulo else "auto"
            celdas.append(gantt_cell(GESTION_DIA, fill=relleno))
        return gantt_row(celdas, height=300)

    for sprint in cfg["sprints"]:
        lab = _laborables(_fecha(sprint["desde"]), _fecha(sprint["hasta"]))
        primero, ultimo = lab[0], lab[-1]
        filas.append(gantt_row(
            [
                gantt_cell(
                    ancho_total, f"SPRINT {sprint['n']}", span=n_dias + 1, sz=18,
                    bold=True, align="left", fill=GANTT_ETAPA,
                )
            ],
            height=340,
        ))
        filas.append(fila_vacia("Plan", titulo=True))
        filas.append(fila_vacia("Planificar el sprint", activos={primero}))
        filas.append(fila_vacia("Do", titulo=True))
        for nombre, a, b in sprint["acts"]:
            filas.append(fila_vacia(nombre, activos=set(_laborables(_fecha(a), _fecha(b)))))
        filas.append(fila_vacia("Check", titulo=True))
        filas.append(fila_vacia("Revisar el prototipo", activos={ultimo}))
        filas.append(fila_vacia("Act", titulo=True))
        filas.append(fila_vacia("Retrospectiva", activos={ultimo}))
    return prefix + "".join(filas) + "</w:tbl>"


def build_gestion_descubrimiento() -> list[str]:
    cfg = GESTION_DESCUBRIMIENTO
    sprints = cfg["sprints"]
    fin = _fecha(sprints[-1]["hasta"])
    ini = _fecha(sprints[0]["desde"])
    rangos = [
        _rango_prosa(_fecha(s["desde"]), _fecha(s["hasta"])) for s in sprints
    ]
    ordinales = ["primero", "segundo", "tercero", "cuarto", "quinto"]
    descripcion = ", ".join(
        f"el {ordinales[i]}, {r}" for i, r in enumerate(rangos[:-1])
    ) + f" y el {ordinales[len(rangos) - 1]}, {rangos[-1]}"
    return [
        intro(
            "La fase de descubrimiento es la primera etapa del desarrollo y se "
            "caracteriza por un fuerte grado de incertidumbre. Se llevó a cabo entre el "
            f"{_fecha_larga(ini)} y el {_fecha_larga(fin)} de {fin.year} y se organizó en "
            f"{NUMEROS[len(sprints) - 1]} sprints: {descripcion}."
        ),
        empty(),
        intro("Las actividades de cada sprint siguen el ciclo Plan, Do, Check y Act:"),
        empty(),
        intro("• Plan: se define la planificación del alcance del prototipo en el sprint."),
        intro(
            "• Do: se produce el prototipo a través de las etapas de Understand and "
            "Empathy, Define, Idea y Prototype. No se han realizado las etapas de Decide "
            "y Validate."
        ),
        intro("• Check: se revisa el prototipo obtenido en el sprint."),
        intro(
            "• Act: se revisan las prácticas, métodos y técnicas para detectar posibles "
            "mejoras (retrospectiva)."
        ),
        empty(),
        intro(
            "Cada columna de la tabla es un día laborable, de lunes a viernes. Las celdas "
            "verdes señalan los días de cada actividad; la planificación se sitúa el primer "
            "día laborable del sprint y la revisión y la retrospectiva, el último."
        ),
        empty(),
        build_gestion_table(cfg),
        caption(13, "Gestión de la fase de descubrimiento"),
        empty(),
    ]


def replace_gestion_descubrimiento(els: list[tuple[str, str]]) -> list[tuple[str, str]]:
    """Sustituye el ejemplo de 5.1 por la gestión real de la fase de descubrimiento."""
    i51 = find_any_heading(els, "5.1 Planificación temporal de la fase de descubrimiento")
    i52 = find_any_heading(els, "5.2 Planificación temporal de la fase de desarrollo")
    nuevos = [
        ("w:tbl" if e.startswith("<w:tbl") else "w:p", e)
        for e in build_gestion_descubrimiento()
    ]
    return els[:i51 + 1] + nuevos + els[i52:]


# ---------------------------------------------------------------------------
# Ensamblado del documento
# ---------------------------------------------------------------------------

def add_update_fields(settings: bytes) -> bytes:
    if b"<w:updateFields" in settings:
        return settings
    marker = b"<w:hdrShapeDefaults>"
    if marker in settings:
        return settings.replace(
            marker, b'<w:updateFields w:val="true"/>' + marker, 1
        )
    return settings


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"No existe la plantilla: {SRC}")

    with zipfile.ZipFile(SRC) as z:
        document = z.read("word/document.xml").decode("utf-8")
        settings = z.read("word/settings.xml")

    body_start = document.index("<w:body>") + len("<w:body>")
    body_end = document.index("</w:body>")
    body = document[body_start:body_end]
    els = split_top(body)

    # 2.2 Planificación temporal del problema (solo estimada).
    els = replace_planificacion(els)

    # 5.1 Gestión de la fase de descubrimiento (5.2 y 5.3 siguen con el ejemplo).
    els = replace_gestion_descubrimiento(els)

    i711 = find_heading(els, SECTION_PREFIXES[0])
    i716 = find_heading(els, SECTION_PREFIXES[5])

    # Introducción de 7.1: sustituye el texto de ejemplo de la plantilla.
    i71 = find_any_heading(els, "7.1 Plan")
    intro_71 = [
        ("w:p", intro(
            "El plan del proyecto se concreta en el Product Backlog y en los requisitos "
            "que lo desarrollan. El backlog recoge las dieciocho historias de usuario del "
            "MVP, agrupadas en cinco epics que siguen el recorrido del jugador: importar y "
            "ordenar, revisar en dos minutos, entender qué pasó, decidir y actuar y aprender "
            "y compartir."
        )),
        ("w:p", intro(
            "A partir de las historias se definen los actores, veintiún requisitos funcionales, "
            "doce requisitos no funcionales y dieciséis requisitos de almacenamiento de "
            "información. Los requisitos funcionales se presentan como casos de uso con flujo "
            "normal y alternativo, y los tres flujos principales se ilustran con diagramas de "
            "secuencia."
        )),
        ("w:p", intro(
            "Todo el sistema trabaja en ciegas grandes y el resultado económico no interviene "
            "en la detección: las alertas comparan la conducta observable con el baseline "
            "individual del jugador."
        )),
    ]
    els = els[:i71 + 1] + intro_71 + els[i711:]

    i711 = find_heading(els, SECTION_PREFIXES[0])
    i716 = find_heading(els, SECTION_PREFIXES[5])
    idxs = [find_heading(els, p) for p in SECTION_PREFIXES[:5]]

    sections = build_sections(els)
    keys = ["7.1.1", "7.1.2", "7.1.3", "7.1.4", "7.1.5"]
    ends = idxs[1:] + [i716]

    new_els: list[str] = []
    cursor = 0
    for idx, end, key in zip(idxs, ends, keys):
        new_els.extend(e for _, e in els[cursor:idx])
        new_els.append(els[idx][1])
        new_els.extend(sections[key])
        cursor = end
    new_els.extend(e for _, e in els[cursor:])

    # 7.4.1 Casos de uso: una tabla de prueba positiva/negativa por RF.
    table_start = 16 + 1 + len(ACTORS) + len(RFS) + len(RNFS) + len(RIS)
    i741 = find_heading_text(new_els, "7.4.1 Casos de uso")
    i742 = find_heading_text(new_els, "7.4.2 Implementación de las pruebas")
    base_caso = first_table_after_text(new_els, i741)
    casos = build_casos_uso(base_caso, table_start)
    new_els = new_els[:i741 + 1] + casos + new_els[i742:]

    # 7.1.6 Diagramas de secuencia.
    i716n = find_heading_text(new_els, "7.1.6")
    i72 = find_any_heading_text(new_els, "7.2")
    new_els = (
        new_els[:i716n + 1] + build_secuencias_section() + new_els[i72:]
    )

    new_body = "".join(new_els)
    new_document = document[:body_start] + new_body + document[body_end:]

    DST.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(SRC) as zin, zipfile.ZipFile(
        DST, "w", zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = new_document.encode("utf-8")
            elif item.filename == "word/settings.xml":
                data = add_update_fields(data)
            elif item.filename == "word/_rels/document.xml.rels":
                data = add_image_relationships(data)
            zout.writestr(item, data)

        for diagram in SEQ_DIAGRAMS:
            png = ROOT / "tools" / "diagrams" / f"{diagram['slug']}.png"
            zout.writestr(
                f"word/media/{diagram['slug']}.png", png.read_bytes()
            )
        zout.writestr(
            f"word/media/{PLAN_SLUG}.png",
            (ROOT / "tools" / "diagrams" / f"{PLAN_SLUG}.png").read_bytes(),
        )

    print(f"Generado: {DST}")
    print(f"Elementos de cuerpo: {len(els)} -> {len(new_els)}")
    total_tablas = (
        1 + len(ACTORS) + len(RFS) + len(RNFS) + len(RIS) + len(CASOS_USO)
    )
    print(f"Tablas generadas: {total_tablas}")
    print(f"Diagramas generados: {len(SEQ_DIAGRAMS)}")


if __name__ == "__main__":
    main()
