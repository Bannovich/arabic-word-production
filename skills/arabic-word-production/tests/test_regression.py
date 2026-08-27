from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "scripts" / "run_regression.py"


def load_runner(testcase: unittest.TestCase):
    if not RUNNER.exists():
        testcase.fail("regression_runner_missing: scripts/run_regression.py does not exist")
    spec = importlib.util.spec_from_file_location("arabic_word_run_regression", RUNNER)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module.run_suite


class RegressionRunnerTests(unittest.TestCase):
    def test_builds_audits_and_reopens_fixture(self):
        run_suite = load_runner(self)
        with TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            model_path = temp / "fixture.json"
            model_path.write_text(
                json.dumps(
                    {
                        "title": "اختبار الانحدار",
                        "blocks": [
                            {"type": "paragraph", "text": "اشتراك Google Workspace بسعر 263.80 EGP."},
                            {
                                "type": "table",
                                "headers": ["الخدمة", "السعر"],
                                "rows": [["Google Workspace", "263.80 EGP"]],
                                "width_weights": [2, 1],
                            },
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            result = run_suite(model_path, temp / "out")

            self.assertTrue(result["passed"], result)
            self.assertTrue(Path(result["docx"]).is_file())
            self.assertTrue(result["reopen_stable"])
            self.assertTrue(result.get("content_model_checked"))
            self.assertEqual(result["builds"], 1)
            self.assertEqual(result["repairs"], 0)


if __name__ == "__main__":
    unittest.main()
