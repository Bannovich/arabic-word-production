from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "check_environment.py"


def load_module():
    if not SCRIPT_PATH.is_file():
        raise AssertionError(f"environment diagnostic is missing: {SCRIPT_PATH}")
    spec = importlib.util.spec_from_file_location("arabic_word_environment", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot import environment diagnostic")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EnvironmentDiagnosticTests(unittest.TestCase):
    def inspect(self, modules: set[str], executables: set[str], word_available: bool = False):
        return load_module().inspect_environment(
            module_finder=lambda name: name in modules,
            executable_finder=lambda name: name if name in executables else None,
            word_desktop_finder=lambda: word_available,
        )

    def test_all_required_modules_are_reported_as_available(self) -> None:
        result = self.inspect({"docx", "lxml"}, {"soffice"})
        self.assertTrue(result["ready_for_structural_route"])
        self.assertEqual([], result["missing_required_modules"])
        self.assertTrue(result["optional_renderers"]["soffice"])
        self.assertFalse(result["word_desktop_available"])

    def test_one_required_module_missing_blocks_structural_route(self) -> None:
        result = self.inspect({"docx"}, set())
        self.assertFalse(result["ready_for_structural_route"])
        self.assertEqual(["lxml"], result["missing_required_modules"])
        self.assertFalse(result["optional_renderers"]["soffice"])

    def test_word_desktop_status_is_reported_independently(self) -> None:
        result = self.inspect({"docx", "lxml"}, set(), word_available=True)
        self.assertTrue(result["word_desktop_available"])
        self.assertTrue(result["ready_for_structural_route"])


if __name__ == "__main__":
    unittest.main()
