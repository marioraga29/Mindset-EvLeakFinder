"""Comprueba que los diagramas UML reflejan el modelo de datos.

Uso:
    python3 tools/verificar_uml.py

Compara `docs/02-modelo-datos.md` con `tools/build_uml.py` y avisa de:
    - entidades que están en un lado y no en el otro,
    - campos que faltan en los diagramas o sobran en ellos,
    - relaciones del documento (sección 5) que ningún diagrama dibuja.

Termina con código 1 si encuentra alguna diferencia, para poder encadenarlo
con la generación de los diagramas. No modifica ningún archivo.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_uml as uml  # noqa: E402

MODELO = ROOT / "docs" / "02-modelo-datos.md"


def entidades_del_documento(md: str) -> dict[str, list[str]]:
    """Devuelve {entidad: [campos]} leyendo las tablas de la sección 4."""
    cuerpo = md.split("## 4. Entidades", 1)[1].split("## 5. Relaciones", 1)[0]
    entidades: dict[str, list[str]] = {}
    patron = re.compile(r"^### 4\.\d+ `(\w+)`.*?\n(.*?)(?=^### 4\.\d+ |\Z)", re.S | re.M)
    for m in patron.finditer(cuerpo):
        entidades[m.group(1)] = re.findall(r"^\| `(\w+)` \|", m.group(2), re.M)
    return entidades


def relaciones_del_documento(md: str) -> list[tuple[str, str]]:
    cuerpo = md.split("## 5. Relaciones", 1)[1].split("## 6. Invariantes", 1)[0]
    return re.findall(r"^\| `(\w+)` → `(\w+)` \|", cuerpo, re.M)


def enlaces_dibujados() -> set[frozenset[str]]:
    return {
        frozenset((link["a"], link["b"]))
        for diagrama in uml.DIAGRAMS
        for link in diagrama["links"]
    }


def main() -> int:
    md = MODELO.read_text(encoding="utf-8")
    doc = entidades_del_documento(md)
    dibujo = {
        nombre: [atributo.split(":")[0] for atributo in datos["attrs"]]
        for nombre, datos in uml.ENTITIES.items()
    }

    problemas: list[str] = []

    for nombre in sorted(set(doc) - set(dibujo)):
        problemas.append(f"Entidad solo en el documento: {nombre}")
    for nombre in sorted(set(dibujo) - set(doc)):
        problemas.append(f"Entidad solo en los diagramas: {nombre}")

    for nombre in sorted(set(doc) & set(dibujo)):
        faltan = [c for c in doc[nombre] if c not in dibujo[nombre]]
        sobran = [c for c in dibujo[nombre] if c not in doc[nombre]]
        if faltan:
            problemas.append(f"{nombre}: campos del documento que no salen en el UML: {', '.join(faltan)}")
        if sobran:
            problemas.append(f"{nombre}: campos del UML que no están en el documento: {', '.join(sobran)}")

    dibujados = enlaces_dibujados()
    relaciones = relaciones_del_documento(md)
    for origen, destino in relaciones:
        if frozenset((origen, destino)) not in dibujados:
            problemas.append(f"Relación sin dibujar en ningún diagrama: {origen} → {destino}")

    print(
        f"Documento: {len(doc)} entidades y {len(relaciones)} relaciones. "
        f"Diagramas: {len(dibujo)} entidades y {len(dibujados)} enlaces distintos."
    )
    if problemas:
        print(f"\nSe han encontrado {len(problemas)} diferencias:")
        for problema in problemas:
            print(f"  - {problema}")
        return 1
    print("Los diagramas reflejan el modelo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
