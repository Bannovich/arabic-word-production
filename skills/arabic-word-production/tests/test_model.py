from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODEL_SCRIPT = ROOT / "scripts" / "doc_model.py"


def load_module(testcase: unittest.TestCase):
    if not MODEL_SCRIPT.exists():
        testcase.fail("model_loader_missing: scripts/doc_model.py does not exist")
    spec = importlib.util.spec_from_file_location("arabic_word_doc_model", MODEL_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class DocumentModelTests(unittest.TestCase):
    def test_loads_utf8_json_and_rejects_unknown_block_types(self):
        module = load_module(self)
        with TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            valid = temp / "valid.json"
            valid.write_text(
                json.dumps(
                    {"title": "مستند عربي", "blocks": [{"type": "paragraph", "text": "نص"}]},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            self.assertEqual(module.load_model(valid)["title"], "مستند عربي")

            invalid = temp / "invalid.json"
            invalid.write_text(
                json.dumps({"title": "x", "blocks": [{"type": "unknown"}]}),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Unsupported block type"):
                module.load_model(invalid)

    def test_build_cli_creates_docx_and_prints_metrics_json(self):
        with TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            model = temp / "model.json"
            output = temp / "output.docx"
            model.write_text(
                json.dumps(
                    {"title": "مستند CLI", "blocks": [{"type": "paragraph", "text": "جاهز"}]},
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "build_docx.py"), str(model), str(output)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.is_file())
            payload = json.loads(result.stdout)
            self.assertEqual(payload["output"], str(output))


if __name__ == "__main__":
    unittest.main()
