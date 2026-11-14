"""Constructor mínimo de documentos .docx sin dependencias externas.

Genera OOXML válido a partir de utilidades de párrafo, tabla y estilo.
Solo usa la biblioteca estándar de Python.
"""

from __future__ import annotations

import datetime as _dt
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape as _escape

NS = (
    'xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
    'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
    'xmlns:o="urn:schemas-microsoft-com:office:office" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
    'xmlns:v="urn:schemas-microsoft-com:vml" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:w10="urn:schemas-microsoft-com:office:word" '
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
    'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
    'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
    'mc:Ignorable="w14"'
)

BRAND = "1F3864"
BRAND_LIGHT = "2E5496"
TEXT = "262626"
MUTED = "595959"
BORDER = "C9D3E3"
LABEL_FILL = "EEF2F8"
ZEBRA = "F7F9FC"


def esc(text: str) -> str:
    return _escape(text)


def run(
    text: str,
    *,
    bold: bool = False,
    italic: bool = False,
    color: str | None = None,
    size: float | None = None,
    font: str | None = None,
) -> str:
    props: list[str] = []
    if font:
        props.append(f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:cs="{font}"/>')
    if bold:
        props.append("<w:b/><w:bCs/>")
    if italic:
        props.append("<w:i/><w:iCs/>")
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    if size:
        half = int(round(size * 2))
        props.append(f'<w:sz w:val="{half}"/><w:szCs w:val="{half}"/>')
    rpr = f'<w:rPr>{"".join(props)}</w:rPr>' if props else ""
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'


def br() -> str:
    return "<w:r><w:br/></w:r>"


def para(
    content: str = "",
    *,
    style: str | None = None,
    align: str | None = None,
    before: int | None = None,
    after: int | None = None,
    line: int | None = None,
    left: int | None = None,
    hanging: int | None = None,
    keep_next: bool = False,
    page_break_before: bool = False,
    bottom_border: bool = False,
) -> str:
    props: list[str] = []
    if style:
        props.append(f'<w:pStyle w:val="{style}"/>')
    if keep_next:
        props.append("<w:keepNext/>")
    if page_break_before:
        props.append("<w:pageBreakBefore/>")
    if bottom_border:
        props.append(
            '<w:pBdr><w:bottom w:val="single" w:sz="8" w:space="4" '
            f'w:color="{BRAND}"/></w:pBdr>'
        )
    if before is not None or after is not None or line is not None:
        attrs = ""
        if before is not None:
            attrs += f' w:before="{before}"'
        if after is not None:
            attrs += f' w:after="{after}"'
        if line is not None:
            attrs += f' w:line="{line}" w:lineRule="auto"'
        props.append(f"<w:spacing{attrs}/>")
    if left is not None or hanging is not None:
        attrs = ""
        if left is not None:
            attrs += f' w:left="{left}"'
        if hanging is not None:
            attrs += f' w:hanging="{hanging}"'
        props.append(f"<w:ind{attrs}/>")
    if align:
        props.append(f'<w:jc w:val="{align}"/>')
    ppr = f'<w:pPr>{"".join(props)}</w:pPr>' if props else ""
    return f"<w:p>{ppr}{content}</w:p>"


def page_break() -> str:
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def tc(
    content: str,
    width: int,
    *,
    span: int = 1,
    fill: str | None = None,
    valign: str = "top",
) -> str:
    props = f'<w:tcW w:w="{width}" w:type="dxa"/>'
    if span > 1:
        props += f'<w:gridSpan w:val="{span}"/>'
    if fill:
        props += f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>'
    props += (
        '<w:tcMar><w:top w:w="90" w:type="dxa"/><w:left w:w="130" w:type="dxa"/>'
        '<w:bottom w:w="90" w:type="dxa"/><w:right w:w="130" w:type="dxa"/></w:tcMar>'
    )
    props += f'<w:vAlign w:val="{valign}"/>'
    return f"<w:tc><w:tcPr>{props}</w:tcPr>{content}</w:tc>"


def tr(cells: list[str], *, cant_split: bool = True, header: bool = False) -> str:
    props = ""
    if cant_split:
        props += "<w:cantSplit/>"
    if header:
        props += "<w:tblHeader/>"
    trpr = f"<w:trPr>{props}</w:trPr>" if props else ""
    return f"<w:tr>{trpr}{''.join(cells)}</w:tr>"


def table(
    rows: list[str],
    widths: list[int],
    *,
    borders: bool = True,
    border_color: str = BORDER,
) -> str:
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    border_xml = ""
    if borders:
        border_xml = (
            "<w:tblBorders>"
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
            f'<w:left w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
            f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
            f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
            "</w:tblBorders>"
        )
    total = sum(widths)
    return (
        f'<w:tbl><w:tblPr><w:tblW w:w="{total}" w:type="dxa"/>'
        f'<w:jc w:val="center"/>{border_xml}<w:tblLayout w:type="fixed"/></w:tblPr>'
        f"<w:tblGrid>{grid}</w:tblGrid>{''.join(rows)}</w:tbl>"
    )


def spacer(height: int = 60) -> str:
    return (
        "<w:p><w:pPr>"
        f'<w:spacing w:before="0" w:after="{height}" w:line="20" w:lineRule="exact"/>'
        '<w:rPr><w:sz w:val="2"/></w:rPr></w:pPr></w:p>'
    )


STYLES = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles {NS}>
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>
        <w:color w:val="{TEXT}"/>
        <w:sz w:val="21"/><w:szCs w:val="21"/>
        <w:lang w:val="es-ES" w:eastAsia="es-ES" w:bidi="ar-SA"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr>
    </w:pPrDefault>
  </w:docDefaults>

  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/><w:qFormat/>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:before="120" w:after="180" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:b/><w:color w:val="{BRAND}"/><w:sz w:val="52"/><w:szCs w:val="52"/></w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:color w:val="{MUTED}"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr>
      <w:keepNext/><w:spacing w:before="360" w:after="160" w:line="240" w:lineRule="auto"/>
      <w:outlineLvl w:val="0"/>
    </w:pPr>
    <w:rPr><w:b/><w:color w:val="{BRAND}"/><w:sz w:val="34"/><w:szCs w:val="34"/></w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr>
      <w:keepNext/><w:spacing w:before="280" w:after="100" w:line="240" w:lineRule="auto"/>
      <w:outlineLvl w:val="1"/>
    </w:pPr>
    <w:rPr><w:b/><w:color w:val="{BRAND_LIGHT}"/><w:sz w:val="26"/><w:szCs w:val="26"/></w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>
    <w:pPr>
      <w:keepNext/><w:spacing w:before="200" w:after="80" w:line="240" w:lineRule="auto"/>
      <w:outlineLvl w:val="2"/>
    </w:pPr>
    <w:rPr><w:b/><w:color w:val="{BRAND}"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="SectionIntro">
    <w:name w:val="Section Intro"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="200" w:line="264" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:i/><w:color w:val="{MUTED}"/><w:sz w:val="21"/></w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="CardText">
    <w:name w:val="Card Text"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="40" w:line="252" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:sz w:val="19"/><w:szCs w:val="19"/></w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="TableText">
    <w:name w:val="Table Text"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="TableHead">
    <w:name w:val="Table Head"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:b/><w:color w:val="FFFFFF"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>
  </w:style>

  <w:style w:type="paragraph" w:styleId="Caption">
    <w:name w:val="caption"/><w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="60" w:after="160" w:line="240" w:lineRule="auto"/></w:pPr>
    <w:rPr><w:i/><w:color w:val="7F7F7F"/><w:sz w:val="17"/><w:szCs w:val="17"/></w:rPr>
  </w:style>
</w:styles>
"""

SETTINGS = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings {NS}>
  <w:zoom w:percent="100"/>
  <w:defaultTabStop w:val="720"/>
  <w:compat>
    <w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>
  </w:compat>
</w:settings>
"""

FOOTER = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr {NS}>
  <w:p>
    <w:pPr>
      <w:pBdr><w:top w:val="single" w:sz="4" w:space="6" w:color="{BORDER}"/></w:pBdr>
      <w:spacing w:before="80" w:after="0"/>
      <w:jc w:val="center"/>
      <w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr>
    </w:pPr>
    <w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr>
      <w:t xml:space="preserve">Mindset &amp; EV Leak Finder · Documento de requisitos funcionales · Página </w:t></w:r>
    <w:r><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:fldChar w:fldCharType="separate"/></w:r>
    <w:r><w:rPr><w:color w:val="7F7F7F"/><w:sz w:val="16"/></w:rPr><w:t>1</w:t></w:r>
    <w:r><w:fldChar w:fldCharType="end"/></w:r>
  </w:p>
</w:ftr>
"""

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""

DOC_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
</Relationships>
"""


def core_xml(title: str, subject: str, author: str, created: str | None = None) -> str:
    created = created or _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{esc(title)}</dc:title>
  <dc:subject>{esc(subject)}</dc:subject>
  <dc:creator>{esc(author)}</dc:creator>
  <cp:lastModifiedBy>{esc(author)}</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{created}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{created}</dcterms:modified>
  <cp:revision>1</cp:revision>
</cp:coreProperties>
"""


APP = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Mindset &amp; EV Leak Finder</Application>
  <DocSecurity>0</DocSecurity>
  <ScaleCrop>false</ScaleCrop>
  <Company>UNED</Company>
  <AppVersion>1.0</AppVersion>
</Properties>
"""


class DocxBuilder:
    def __init__(self) -> None:
        self.body: list[str] = []

    def add(self, xml: str) -> None:
        self.body.append(xml)

    def save(self, path: Path, *, title: str, subject: str, author: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        document = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f"<w:document {NS}><w:body>{''.join(self.body)}"
            '<w:sectPr><w:footerReference w:type="default" r:id="rId3"/>'
            '<w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1247" w:right="1247" w:bottom="1247" w:left="1247" '
            'w:header="708" w:footer="708" w:gutter="0"/>'
            '<w:cols w:space="708"/><w:docGrid w:linePitch="360"/>'
            "</w:sectPr></w:body></w:document>"
        )
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", CONTENT_TYPES)
            z.writestr("_rels/.rels", ROOT_RELS)
            z.writestr("word/document.xml", document)
            z.writestr("word/styles.xml", STYLES)
            z.writestr("word/settings.xml", SETTINGS)
            z.writestr("word/footer1.xml", FOOTER)
            z.writestr("word/_rels/document.xml.rels", DOC_RELS)
            z.writestr("docProps/core.xml", core_xml(title, subject, author))
            z.writestr("docProps/app.xml", APP)
