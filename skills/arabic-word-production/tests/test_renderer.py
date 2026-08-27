from __future__ import annotations

import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from zipfile import ZipFile

from lxml import etree
from PIL import Image
from docx import Document


ROOT = Path(__file__).resolve().parents[1]
BUILD_SCRIPT = ROOT / "scripts" / "build_docx.py"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def load_builder(testcase: unittest.TestCase):
    if not BUILD_SCRIPT.exists():
        testcase.fail("renderer_missing: scripts/build_docx.py does not exist")
    spec = importlib.util.spec_from_file_location("arabic_word_build_docx", BUILD_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module.build_document


def document_paragraphs(path: Path):
    with ZipFile(path) as archive:
        root = etree.fromstring(archive.read("word/document.xml"))
    return root.xpath("//w:body/w:p | //w:tc/w:p", namespaces=NS)


def document_root(path: Path):
    with ZipFile(path) as archive:
        return etree.fromstring(archive.read("word/document.xml"))


def paragraph_text(paragraph) -> str:
    return "".join(paragraph.xpath(".//w:t/text()", namespaces=NS))


def bidi_value(paragraph):
    nodes = paragraph.xpath("./w:pPr/w:bidi", namespaces=NS)
    if not nodes:
        return None
    value = nodes[0].get(f"{{{W}}}val")
    return True if value in (None, "1", "true", "on") else False


def justification_value(paragraph):
    nodes = paragraph.xpath("./w:pPr/w:jc", namespaces=NS)
    if not nodes:
        return None
    return nodes[0].get(f"{{{W}}}val")


def run_rtl_value(run):
    nodes = run.xpath("./w:rPr/w:rtl", namespaces=NS)
    if not nodes:
        return None
    value = nodes[0].get(f"{{{W}}}val")
    return True if value in (None, "1", "true", "on") else False


class RendererDirectionTests(unittest.TestCase):
    def test_sets_explicit_paragraph_direction_for_arabic_mixed_and_english(self):
        build_document = load_builder(self)
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "directions.docx"
            model = {
                "title": "اختبار الاتجاهات",
                "blocks": [
                    {"type": "paragraph", "text": "هذه فقرة عربية بالكامل."},
                    {
                        "type": "paragraph",
                        "text": "اشتراك Google Workspace بسعر 263.80 EGP شهريًا.",
                    },
                    {
                        "type": "paragraph",
                        "text": "Operational owner: Growth Team. SLA: 99.9%.",
                    },
                ],
            }

            build_document(model, output)

            directions = {
                paragraph_text(p): bidi_value(p)
                for p in document_paragraphs(output)
                if paragraph_text(p)
            }
            self.assertIs(directions["هذه فقرة عربية بالكامل."], True)
            self.assertIs(
                directions["اشتراك Google Workspace بسعر 263.80 EGP شهريًا."],
                True,
            )
            self.assertIs(
                directions["Operational owner: Growth Team. SLA: 99.9%."],
                False,
            )

    def test_uses_logical_start_alignment_for_rtl_and_ltr_paragraphs(self):
        build_document = load_builder(self)
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "logical-alignment.docx"
            model = {
                "title": "اختبار المحاذاة المنطقية",
                "blocks": [
                    {"type": "paragraph", "text": "فقرة عربية قصيرة."},
                    {"type": "paragraph", "text": "Short English paragraph."},
                ],
            }

            build_document(model, output)

            paragraphs = {
                paragraph_text(p): p
                for p in document_paragraphs(output)
                if paragraph_text(p)
            }
            self.assertEqual(
                justification_value(paragraphs["فقرة عربية قصيرة."]),
                "start",
            )
            self.assertEqual(
                justification_value(paragraphs["Short English paragraph."]),
                "start",
            )

    def test_builds_rtl_table_with_repeating_header(self):
        build_document = load_builder(self)
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "table.docx"
            model = {
                "title": "جدول الخدمات",
                "blocks": [
                    {
                        "type": "table",
                        "direction": "rtl",
                        "headers": ["الخدمة", "الخطة", "السعر"],
                        "rows": [["Google Workspace", "Business", "263.80 EGP"]],
                    }
                ],
            }

            build_document(model, output)

            root = document_root(output)
            tables = root.xpath("//w:tbl", namespaces=NS)
            self.assertEqual(len(tables), 1)
            self.assertEqual(
                len(tables[0].xpath("./w:tblPr/w:bidiVisual", namespaces=NS)),
                1,
            )
            self.assertEqual(
                len(tables[0].xpath("./w:tr[1]/w:trPr/w:tblHeader", namespaces=NS)),
                1,
            )
            for text in ["الخدمة", "الخطة", "السعر", "263.80 EGP"]:
                paragraphs = [
                    p
                    for p in tables[0].xpath(".//w:p", namespaces=NS)
                    if paragraph_text(p) == text
                ]
                self.assertEqual(len(paragraphs), 1)
                self.assertIs(bidi_value(paragraphs[0]), True)

    def test_keeps_url_run_ltr_inside_rtl_paragraph(self):
        build_document = load_builder(self)
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "url.docx"
            url = "https://example.com/support/path?currency=EGP&plan=pro"
            model = {
                "title": "اختبار الرابط",
                "blocks": [
                    {
                        "type": "paragraph",
                        "text": f"افتح رابط الدعم: {url} ثم تابع التعليمات.",
                    }
                ],
            }

            build_document(model, output)

            paragraph = next(
                p
                for p in document_paragraphs(output)
                if url in paragraph_text(p)
            )
            self.assertIs(bidi_value(paragraph), True)
            url_runs = [
                run
                for run in paragraph.xpath("./w:r", namespaces=NS)
                if url in "".join(run.xpath(".//w:t/text()", namespaces=NS))
            ]
            self.assertEqual(len(url_runs), 1)
            self.assertIs(run_rtl_value(url_runs[0]), False)
            rtl_runs = [
                run
                for run in paragraph.xpath("./w:r", namespaces=NS)
                if run_rtl_value(run) is True
            ]
            self.assertGreaterEqual(len(rtl_runs), 1)

    def test_caps_inline_image_to_text_width_and_keeps_caption_adjacent(self):
        build_document = load_builder(self)
        with TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "wide.png"
            Image.new("RGB", (2400, 400), "#2D5BFF").save(source)
            output = temp / "image.docx"
            caption = "الشكل 1: ملخص بصري للخدمات"
            model = {
                "title": "اختبار الصورة",
                "blocks": [
                    {
                        "type": "image",
                        "path": str(source),
                        "max_width_inches": 20,
                        "alt": "شريط أزرق عريض لاختبار التحجيم",
                        "caption": caption,
                    }
                ],
            }

            build_document(model, output)

            root = document_root(output)
            self.assertEqual(len(root.xpath("//wp:inline", namespaces={**NS, "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"})), 1)
            self.assertEqual(len(root.xpath("//wp:anchor", namespaces={**NS, "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"})), 0)
            drawing_ns = {**NS, "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"}
            extent = root.xpath("//wp:inline/wp:extent", namespaces=drawing_ns)[0]
            image_cx = int(extent.get("cx"))
            section = root.xpath("//w:sectPr[last()]", namespaces=NS)[0]
            page_width = int(section.xpath("./w:pgSz", namespaces=NS)[0].get(f"{{{W}}}w"))
            margins = section.xpath("./w:pgMar", namespaces=NS)[0]
            text_width_dxa = page_width - int(margins.get(f"{{{W}}}left")) - int(margins.get(f"{{{W}}}right"))
            self.assertLessEqual(image_cx, text_width_dxa * 635)

            body_paragraphs = root.xpath("//w:body/w:p", namespaces=NS)
            image_index = next(
                index
                for index, paragraph in enumerate(body_paragraphs)
                if paragraph.xpath(".//wp:inline", namespaces=drawing_ns)
            )
            self.assertEqual(paragraph_text(body_paragraphs[image_index + 1]), caption)
            style = body_paragraphs[image_index + 1].xpath("./w:pPr/w:pStyle", namespaces=NS)[0]
            self.assertIn("caption", style.get(f"{{{W}}}val").lower())

    def test_routes_wide_table_through_landscape_then_returns_to_portrait(self):
        build_document = load_builder(self)
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "sections.docx"
            headers = [
                "الخدمة",
                "الخطة",
                "السعر",
                "العملة",
                "التفعيل",
                "الضمان",
                "الإجراء التالي",
            ]
            model = {
                "title": "اختبار الجداول الواسعة",
                "blocks": [
                    {
                        "type": "table",
                        "direction": "rtl",
                        "headers": headers,
                        "rows": [["أ", "ب", "1", "EGP", "24 ساعة", "30 يومًا", "تأكيد"]],
                    },
                    {"type": "paragraph", "text": "عودة إلى الصفحة الرأسية."},
                ],
            }

            build_document(model, output)

            root = document_root(output)
            sections = root.xpath("//w:sectPr", namespaces=NS)
            self.assertGreaterEqual(len(sections), 3)
            landscape = [
                section
                for section in sections
                if section.xpath("./w:pgSz[@w:orient='landscape']", namespaces=NS)
            ]
            self.assertEqual(len(landscape), 1)
            last_size = sections[-1].xpath("./w:pgSz", namespaces=NS)[0]
            self.assertLess(
                int(last_size.get(f"{{{W}}}w")),
                int(last_size.get(f"{{{W}}}h")),
            )

    def test_applies_reusable_styles_to_titles_headings_bodies_lists_and_callouts(self):
        build_document = load_builder(self)
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "styles.docx"
            model = {
                "title": "عنوان المستند",
                "blocks": [
                    {"type": "heading", "level": 1, "text": "القسم الأول"},
                    {"type": "heading", "level": 2, "text": "قسم فرعي"},
                    {"type": "paragraph", "text": "فقرة عربية."},
                    {"type": "paragraph", "text": "English-only paragraph."},
                    {"type": "list", "ordered": True, "items": ["الخطوة الأولى", "الخطوة الثانية"]},
                    {"type": "callout", "kind": "warning", "text": "تنبيه مهم."},
                ],
            }

            build_document(model, output)

            result = Document(output)
            styles = {p.text: p.style.name for p in result.paragraphs if p.text}
            self.assertEqual(styles["عنوان المستند"], "Arabic Title RTL")
            self.assertEqual(styles["القسم الأول"], "Arabic Heading 1 RTL")
            self.assertEqual(styles["قسم فرعي"], "Arabic Heading 2 RTL")
            self.assertEqual(styles["فقرة عربية."], "Arabic Body RTL")
            self.assertEqual(styles["English-only paragraph."], "English Body LTR")
            self.assertEqual(styles["الخطوة الأولى"], "Arabic List Number RTL")
            self.assertEqual(styles["الخطوة الثانية"], "Arabic List Number RTL")
            self.assertEqual(styles["تنبيه مهم."], "Warning")

    def test_uses_semantic_table_width_weights_instead_of_equal_columns(self):
        build_document = load_builder(self)
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "geometry.docx"
            model = {
                "title": "هندسة الجدول",
                "blocks": [
                    {
                        "type": "table",
                        "direction": "rtl",
                        "headers": ["وصف طويل", "الحالة", "الرقم"],
                        "rows": [["شرح يحتاج مساحة كبيرة داخل العمود", "مكتمل", "7"]],
                        "width_weights": [4, 2, 1],
                    }
                ],
            }

            build_document(model, output)

            root = document_root(output)
            table = root.xpath("//w:tbl", namespaces=NS)[0]
            grid = [
                int(node.get(f"{{{W}}}w"))
                for node in table.xpath("./w:tblGrid/w:gridCol", namespaces=NS)
            ]
            self.assertEqual(len(grid), 3)
            self.assertGreater(grid[0], grid[1])
            self.assertGreater(grid[1], grid[2])
            self.assertAlmostEqual(grid[0] / grid[2], 4.0, delta=0.15)
            self.assertAlmostEqual(grid[1] / grid[2], 2.0, delta=0.15)
            for row in table.xpath("./w:tr", namespaces=NS):
                cell_widths = [
                    int(value)
                    for value in row.xpath("./w:tc/w:tcPr/w:tcW/@w:w", namespaces=NS)
                ]
                self.assertEqual(cell_widths, grid)

    def test_adds_title_header_and_dynamic_page_numbers_to_every_section(self):
        build_document = load_builder(self)
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "headers-footers.docx"
            title = "دليل التشغيل المختلط"
            model = {
                "title": title,
                "blocks": [
                    {
                        "type": "table",
                        "headers": [
                            "الخدمة",
                            "الخطة",
                            "السعر",
                            "العملة",
                            "التفعيل",
                            "الضمان",
                            "الإجراء",
                        ],
                        "rows": [["أ", "ب", "1", "EGP", "24 ساعة", "30 يومًا", "تأكيد"]],
                        "landscape": True,
                    },
                    {"type": "paragraph", "text": "عودة إلى القسم الرأسي."},
                ],
            }

            build_document(model, output)

            with ZipFile(output) as archive:
                root = etree.fromstring(archive.read("word/document.xml"))
                sections = root.xpath("//w:sectPr", namespaces=NS)
                self.assertGreaterEqual(len(sections), 3)
                for section in sections:
                    self.assertEqual(
                        len(section.xpath("./w:headerReference", namespaces=NS)),
                        1,
                    )
                    self.assertEqual(
                        len(section.xpath("./w:footerReference", namespaces=NS)),
                        1,
                    )

                header_names = sorted(
                    name for name in archive.namelist() if name.startswith("word/header") and name.endswith(".xml")
                )
                footer_names = sorted(
                    name for name in archive.namelist() if name.startswith("word/footer") and name.endswith(".xml")
                )
                self.assertGreaterEqual(len(header_names), 1)
                self.assertGreaterEqual(len(footer_names), 1)
                for name in header_names:
                    header = etree.fromstring(archive.read(name))
                    self.assertIn(title, "".join(header.xpath("//w:t/text()", namespaces=NS)))
                    self.assertTrue(header.xpath("//w:pPr/w:bidi", namespaces=NS))
                for name in footer_names:
                    footer = etree.fromstring(archive.read(name))
                    instructions = " ".join(footer.xpath("//w:instrText/text()", namespaces=NS))
                    self.assertIn("PAGE", instructions)
                    self.assertIn("NUMPAGES", instructions)
                    self.assertEqual(
                        footer.xpath("string(//w:pPr/w:bidi/@w:val)", namespaces=NS),
                        "0",
                    )
                    self.assertEqual(
                        footer.xpath("string(//w:pPr/w:jc/@w:val)", namespaces=NS),
                        "center",
                    )
                    self.assertIn(
                        "/",
                        "".join(footer.xpath("//w:t/text()", namespaces=NS)),
                    )

    def test_targets_modern_word_compatibility_mode(self):
        build_document = load_builder(self)
        with TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "modern-word.docx"
            build_document(
                {
                    "title": "اختبار Word الحديث",
                    "blocks": [{"type": "paragraph", "text": "فقرة RTL."}],
                },
                output,
            )

            with ZipFile(output) as archive:
                settings = etree.fromstring(archive.read("word/settings.xml"))
            modes = settings.xpath(
                "//w:compatSetting[@w:name='compatibilityMode']/@w:val",
                namespaces=NS,
            )
            self.assertEqual(modes, ["15"])
            update_fields = settings.xpath("//w:updateFields/@w:val", namespaces=NS)
            self.assertEqual(
                update_fields,
                [],
                "The generated document must not request field updates on open; "
                "Word can show an intrusive external-field warning.",
            )


if __name__ == "__main__":
    unittest.main()
