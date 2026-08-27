from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from lxml import etree


W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
WP = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
NS = {"w": W, "wp": WP}
ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]")
PLACEHOLDER_RE = re.compile(r"(?<!\w)(?:TBD|TODO)(?!\w)|\[\s*PLACEHOLDER\s*\]", re.I)
INTERNAL_TOKEN_RE = re.compile(r"(?:chatgpt-content-reference|turn\d+(?:search|view|file)\d+)")


def _paragraph_text(paragraph) -> str:
    parts: list[str] = []
    for node in paragraph.xpath(
        ".//w:t | .//w:tab | .//w:br | .//w:cr",
        namespaces=NS,
    ):
        kind = etree.QName(node).localname
        if kind == "t":
            parts.append(node.text or "")
        elif kind == "tab":
            parts.append("\t")
        else:
            parts.append("\n")
    return "".join(parts)


def _on(node) -> bool:
    value = node.get(f"{{{W}}}val")
    return value in (None, "1", "true", "on")


def _effective_paragraph_property(
    paragraph,
    property_name: str,
    styles_by_id: dict[str, etree._Element],
    default_style_id: str | None,
    document_default_ppr,
):
    direct = paragraph.xpath(f"./w:pPr/w:{property_name}", namespaces=NS)
    if direct:
        return direct[0]

    style_values = paragraph.xpath("./w:pPr/w:pStyle/@w:val", namespaces=NS)
    style_id = style_values[0] if style_values else default_style_id
    visited: set[str] = set()
    while style_id and style_id not in visited:
        visited.add(style_id)
        style = styles_by_id.get(style_id)
        if style is None:
            break
        inherited = style.xpath(f"./w:pPr/w:{property_name}", namespaces=NS)
        if inherited:
            return inherited[0]
        base = style.xpath("./w:basedOn/@w:val", namespaces=NS)
        style_id = base[0] if base else None

    if document_default_ppr is not None:
        inherited = document_default_ppr.xpath(
            f"./w:{property_name}",
            namespaces=NS,
        )
        if inherited:
            return inherited[0]
    return None


def _effective_paragraph_bidi(
    paragraph,
    styles_by_id: dict[str, etree._Element],
    default_style_id: str | None,
    document_default_ppr,
) -> bool:
    node = _effective_paragraph_property(
        paragraph,
        "bidi",
        styles_by_id,
        default_style_id,
        document_default_ppr,
    )
    return _on(node) if node is not None else False


def _effective_paragraph_justification(
    paragraph,
    styles_by_id: dict[str, etree._Element],
    default_style_id: str | None,
    document_default_ppr,
) -> str:
    node = _effective_paragraph_property(
        paragraph,
        "jc",
        styles_by_id,
        default_style_id,
        document_default_ppr,
    )
    return node.get(f"{{{W}}}val", "start") if node is not None else "start"


def _finding(error_id: str, message: str, count: int = 1, severity: str = "error") -> dict:
    return {"id": error_id, "severity": severity, "count": count, "message": message}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _expected_texts(model: dict) -> list[str]:
    expected: list[str] = []
    title = str(model.get("title", "")).strip()
    if title:
        expected.append(title)
    for block in model.get("blocks", []):
        block_type = block.get("type")
        if block_type in {"heading", "paragraph", "callout"}:
            expected.append(str(block.get("text", "")))
        elif block_type == "list":
            expected.extend(str(item) for item in block.get("items", []))
        elif block_type == "table":
            expected.extend(str(item) for item in block.get("headers", []))
            for row in block.get("rows", []):
                expected.extend(str(item) for item in row)
        elif block_type == "image" and block.get("caption"):
            expected.append(str(block["caption"]))
    return [text for text in expected if _normalize(text)]


def audit_docx(path: str | Path, model: dict | str | Path | None = None) -> dict:
    source = Path(path)
    findings: list[dict] = []
    if not source.is_file():
        return {
            "passed": False,
            "findings": [_finding("ERR-PACKAGE-001", f"File does not exist: {source}")],
            "metrics": {},
        }

    try:
        with ZipFile(source) as archive:
            names = set(archive.namelist())
            if "word/document.xml" not in names:
                return {
                    "passed": False,
                    "findings": [_finding("ERR-PACKAGE-002", "word/document.xml is missing")],
                    "metrics": {},
                }
            root = etree.fromstring(archive.read("word/document.xml"))
            settings_root = (
                etree.fromstring(archive.read("word/settings.xml"))
                if "word/settings.xml" in names
                else None
            )
            styles_root = (
                etree.fromstring(archive.read("word/styles.xml"))
                if "word/styles.xml" in names
                else None
            )
            media_entries = [name for name in names if name.startswith("word/media/")]
            header_entries = sorted(
                name
                for name in names
                if name.startswith("word/header") and name.endswith(".xml")
            )
            footer_entries = sorted(
                name
                for name in names
                if name.startswith("word/footer") and name.endswith(".xml")
            )
            header_roots = [etree.fromstring(archive.read(name)) for name in header_entries]
            footer_roots = [etree.fromstring(archive.read(name)) for name in footer_entries]
    except (BadZipFile, etree.XMLSyntaxError) as error:
        return {
            "passed": False,
            "findings": [_finding("ERR-PACKAGE-003", f"Invalid DOCX package: {error}")],
            "metrics": {},
        }

    update_fields_on_open = (
        settings_root.xpath("//w:updateFields", namespaces=NS)
        if settings_root is not None
        else []
    )
    if any(_on(node) for node in update_fields_on_open):
        findings.append(
            _finding(
                "ERR-FIELD-001",
                "The document requests field updates on open; Word Desktop may show an intrusive external-field warning.",
                len(update_fields_on_open),
            )
        )

    styles_by_id: dict[str, etree._Element] = {}
    default_style_id: str | None = None
    document_default_ppr = None
    if styles_root is not None:
        for style in styles_root.xpath("//w:style", namespaces=NS):
            style_id = style.get(f"{{{W}}}styleId")
            if style_id:
                styles_by_id[style_id] = style
            if (
                style.get(f"{{{W}}}type") == "paragraph"
                and style.get(f"{{{W}}}default") in {"1", "true", "on"}
            ):
                default_style_id = style_id
        defaults = styles_root.xpath(
            "./w:docDefaults/w:pPrDefault/w:pPr",
            namespaces=NS,
        )
        document_default_ppr = defaults[0] if defaults else None

    body_paragraphs = root.xpath("//w:p", namespaces=NS)
    auxiliary_paragraphs = [
        paragraph
        for part in [*header_roots, *footer_roots]
        for paragraph in part.xpath("//w:p", namespaces=NS)
    ]
    paragraphs = [*body_paragraphs, *auxiliary_paragraphs]
    arabic_paragraphs = [p for p in paragraphs if ARABIC_RE.search(_paragraph_text(p))]
    missing_rtl = []
    for paragraph in arabic_paragraphs:
        if not _effective_paragraph_bidi(
            paragraph,
            styles_by_id,
            default_style_id,
            document_default_ppr,
        ):
            missing_rtl.append(_paragraph_text(paragraph))
    if missing_rtl:
        findings.append(
            _finding(
                "ERR-RTL-001",
                "Arabic or mixed paragraphs are missing an explicit RTL base direction.",
                len(missing_rtl),
            )
        )

    trailing_edge_rtl = []
    for paragraph in arabic_paragraphs:
        if not _effective_paragraph_bidi(
            paragraph,
            styles_by_id,
            default_style_id,
            document_default_ppr,
        ):
            continue
        justification = _effective_paragraph_justification(
            paragraph,
            styles_by_id,
            default_style_id,
            document_default_ppr,
        )
        if justification in {"right", "end"}:
            trailing_edge_rtl.append(_paragraph_text(paragraph))
    if trailing_edge_rtl:
        findings.append(
            _finding(
                "ERR-RTL-003",
                "RTL paragraphs use trailing-edge justification; use logical 'start' so Word displays them on the visual right.",
                len(trailing_edge_rtl),
            )
        )

    tables = root.xpath("//w:tbl", namespaces=NS)
    missing_table_rtl = [
        table
        for table in tables
        if not table.xpath("./w:tblPr/w:bidiVisual", namespaces=NS)
    ]
    if missing_table_rtl:
        findings.append(
            _finding(
                "ERR-TABLE-001",
                "Tables are missing explicit RTL visual order.",
                len(missing_table_rtl),
            )
        )

    sections = root.xpath("//w:sectPr", namespaces=NS)
    sections_missing_chrome = [
        section
        for section in sections
        if not section.xpath("./w:headerReference", namespaces=NS)
        or not section.xpath("./w:footerReference", namespaces=NS)
    ]
    footers_missing_fields = []
    footers_with_unstable_layout = []
    for footer in footer_roots:
        instructions = " ".join(footer.xpath("//w:instrText/text()", namespaces=NS)).upper()
        if not re.search(r"\bPAGE\b", instructions) or not re.search(r"\bNUMPAGES\b", instructions):
            footers_missing_fields.append(footer)
            continue
        page_paragraphs = footer.xpath("//w:p[.//w:instrText]", namespaces=NS)
        stable_layout = False
        for paragraph in page_paragraphs:
            bidi = _effective_paragraph_bidi(
                paragraph,
                styles_by_id,
                default_style_id,
                document_default_ppr,
            )
            justification = _effective_paragraph_justification(
                paragraph,
                styles_by_id,
                default_style_id,
                document_default_ppr,
            )
            text = _paragraph_text(paragraph)
            if (
                not bidi
                and justification == "center"
                and "/" in text
            ):
                stable_layout = True
                break
        if not stable_layout:
            footers_with_unstable_layout.append(footer)
    if (
        sections_missing_chrome
        or not header_entries
        or not footer_entries
        or footers_missing_fields
        or footers_with_unstable_layout
    ):
        findings.append(
            _finding(
                "ERR-SECTION-001",
                "A section is missing page chrome, or its footer lacks stable centered LTR PAGE / NUMPAGES fields.",
                max(
                    1,
                    len(sections_missing_chrome)
                    + len(footers_missing_fields)
                    + len(footers_with_unstable_layout),
                ),
            )
        )

    full_text = "\n".join(_paragraph_text(p) for p in body_paragraphs)
    placeholders = PLACEHOLDER_RE.findall(full_text)
    if placeholders:
        findings.append(
            _finding(
                "ERR-CONTENT-001",
                "Placeholder text remains in the document.",
                len(placeholders),
            )
        )
    internal_tokens = INTERNAL_TOKEN_RE.findall(full_text)
    if internal_tokens:
        findings.append(
            _finding(
                "ERR-CONTENT-002",
                "Internal citation or content-reference tokens remain in the document.",
                len(internal_tokens),
            )
        )

    if model is not None:
        source_model = (
            json.loads(Path(model).read_text(encoding="utf-8"))
            if isinstance(model, (str, Path))
            else model
        )
        normalized_document = _normalize(full_text)
        missing = [
            text
            for text in _expected_texts(source_model)
            if _normalize(text) not in normalized_document
        ]
        if missing:
            findings.append(
                _finding(
                    "ERR-CONTENT-003",
                    "Source-model content is missing from the DOCX: "
                    + "; ".join(_normalize(text)[:80] for text in missing[:3]),
                    len(missing),
                )
            )

    metrics = {
        "paragraphs": len(body_paragraphs),
        "arabic_or_mixed_paragraphs": len(
            [p for p in body_paragraphs if ARABIC_RE.search(_paragraph_text(p))]
        ),
        "style_inherited_rtl_paragraphs": len(
            [
                p
                for p in arabic_paragraphs
                if not p.xpath("./w:pPr/w:bidi", namespaces=NS)
                and _effective_paragraph_bidi(
                    p,
                    styles_by_id,
                    default_style_id,
                    document_default_ppr,
                )
            ]
        ),
        "tables": len(tables),
        "sections": len(sections),
        "header_parts": len(header_entries),
        "footer_parts": len(footer_entries),
        "page_field_footers": len(footer_entries) - len(footers_missing_fields),
        "stable_page_footers": len(footer_entries)
        - len(footers_missing_fields)
        - len(footers_with_unstable_layout),
        "inline_images": len(root.xpath("//wp:inline", namespaces=NS)),
        "floating_images": len(root.xpath("//wp:anchor", namespaces=NS)),
        "media_entries": len(media_entries),
    }
    return {"passed": not findings, "findings": findings, "metrics": metrics}


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Arabic/mixed DOCX invariants")
    parser.add_argument("docx", type=Path)
    parser.add_argument("--out-json", type=Path)
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()
    result = audit_docx(args.docx, args.model)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out_json:
        args.out_json.parent.mkdir(parents=True, exist_ok=True)
        args.out_json.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = ["audit_docx"]
