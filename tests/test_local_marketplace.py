from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = REPOSITORY_ROOT / "scripts" / "build_local_marketplace.py"


def load_builder():
    if not BUILDER_PATH.is_file():
        raise AssertionError(f"marketplace builder is missing: {BUILDER_PATH}")
    spec = importlib.util.spec_from_file_location("local_marketplace", BUILDER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError("could not import local marketplace builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LocalMarketplaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.root = Path(self.temp_dir.name) / "source"
        self.destination = Path(self.temp_dir.name) / "marketplace"
        self.write(
            ".codex-plugin/plugin.json",
            json.dumps(
                {
                    "name": "arabic-word-production",
                    "interface": {"displayName": "Arabic Word Production"},
                }
            ),
        )
        self.write("skills/arabic-word-production/SKILL.md", "# Synthetic Skill")
        self.write("assets/icon.png", "synthetic icon")
        self.write(".venv/private.txt", "do not copy")

    def write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def build(self):
        return load_builder().build_marketplace(self.root, self.destination)

    def test_catalog_has_canonical_marketplace_policy_and_source(self) -> None:
        result = self.build()
        catalog = json.loads(Path(result["catalog_path"]).read_text(encoding="utf-8"))
        self.assertEqual("arabic-word-production-local", catalog["name"])
        self.assertEqual("Arabic Word Production Local", catalog["interface"]["displayName"])
        self.assertEqual(
            [
                {
                    "name": "arabic-word-production",
                    "source": {"source": "local", "path": "./plugins/arabic-word-production"},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    "category": "Productivity",
                }
            ],
            catalog["plugins"],
        )

    def test_plugin_copy_is_byte_identical_and_excludes_local_environment(self) -> None:
        result = self.build()
        plugin_root = Path(result["plugin_root"])
        for relative in (
            ".codex-plugin/plugin.json",
            "skills/arabic-word-production/SKILL.md",
            "assets/icon.png",
        ):
            self.assertEqual((self.root / relative).read_bytes(), (plugin_root / relative).read_bytes())
        self.assertFalse((plugin_root / ".venv").exists())


if __name__ == "__main__":
    unittest.main()
