from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = REPOSITORY_ROOT / "scripts" / "build_submission_bundle.py"


def load_builder():
    if not BUILDER_PATH.is_file():
        raise AssertionError(f"bundle builder is missing: {BUILDER_PATH}")
    spec = importlib.util.spec_from_file_location("submission_bundle", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("could not import submission bundle builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SubmissionBundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name) / "source"
        self.root.mkdir(parents=True)
        self.write(".codex-plugin/plugin.json", "{}")
        self.write("README.md", "Synthetic repository")
        self.write("skills/arabic-word-production/SKILL.md", "# Synthetic Skill")
        self.write("skills/arabic-word-production/assets/arabic-word-template.docx", "template-bytes")
        self.write("skills/arabic-word-production/references/qa.md", "safe reference")
        self.write(".venv/ignored.txt", "local environment")
        self.write("artifacts/ignored.txt", "generated output")
        self.write("arabic_word_production.egg-info/PKG-INFO", "local build metadata")
        self.write(".git/config", "private git metadata")

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_bundle_inventory_is_sorted_and_excludes_local_material(self) -> None:
        result = load_builder().build_bundles(self.root, Path(self.temp_dir.name) / "output")
        self.assertEqual(["plugin", "skill"], sorted(result["bundles"]))
        for bundle in result["bundles"].values():
            names = bundle["members"]
            self.assertEqual(sorted(names), names)
            self.assertFalse(any(name.startswith((".git/", ".venv/", "artifacts/")) for name in names))
            self.assertFalse(any(".egg-info/" in name for name in names))

    def test_skill_bundle_places_skill_md_at_archive_root_and_preserves_template(self) -> None:
        result = load_builder().build_bundles(self.root, Path(self.temp_dir.name) / "output")
        skill = result["bundles"]["skill"]
        self.assertIn("SKILL.md", skill["members"])
        self.assertNotIn("skills/arabic-word-production/SKILL.md", skill["members"])
        with zipfile.ZipFile(skill["path"]) as archive:
            self.assertEqual(b"template-bytes", archive.read("assets/arabic-word-template.docx"))
            self.assertTrue(archive.testzip() is None)

    def test_same_source_produces_identical_digests(self) -> None:
        builder = load_builder()
        first = builder.build_bundles(self.root, Path(self.temp_dir.name) / "first")
        second = builder.build_bundles(self.root, Path(self.temp_dir.name) / "second")
        self.assertEqual(first["bundles"]["skill"]["sha256"], second["bundles"]["skill"]["sha256"])
        self.assertEqual(first["bundles"]["plugin"]["sha256"], second["bundles"]["plugin"]["sha256"])


if __name__ == "__main__":
    unittest.main()
