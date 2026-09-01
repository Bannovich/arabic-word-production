from __future__ import annotations

import json
import struct
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ASSET_DIRECTORY = REPOSITORY_ROOT / "assets"
REQUIRED_DIRECTORY_ASSETS = ("icon.png", "logo.png")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise AssertionError(f"not a PNG: {path.name}")
    if data[12:16] != b"IHDR":
        raise AssertionError(f"PNG has no IHDR chunk: {path.name}")
    return struct.unpack(">II", data[16:24])


def project_version(path: Path) -> str:
    in_project_table = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("["):
            in_project_table = line == "[project]"
            continue
        if in_project_table and line.startswith("version"):
            key, value = line.split("=", 1)
            if key.strip() == "version":
                parsed = json.loads(value.strip())
                if isinstance(parsed, str):
                    return parsed
    raise AssertionError("pyproject.toml has no [project].version")


class PluginAssetTests(unittest.TestCase):
    def test_required_directory_assets_meet_openai_image_limits(self) -> None:
        for name in REQUIRED_DIRECTORY_ASSETS:
            path = ASSET_DIRECTORY / name
            self.assertTrue(path.is_file(), f"missing plugin asset: {name}")
            width, height = png_dimensions(path)
            self.assertEqual(width, height, name)
            self.assertGreaterEqual(width, 48, name)
            self.assertLessEqual(width, 4096, name)
            self.assertLessEqual(path.stat().st_size, 5 * 1024 * 1024, name)

    def test_manifest_exposes_new_brand_without_renaming_stable_package(self) -> None:
        manifest = json.loads(
            (REPOSITORY_ROOT / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual("arabic-word-production", manifest["name"])
        self.assertEqual("0.1.1", manifest["version"])
        self.assertEqual("Arabic DOCX RTL", manifest["interface"]["displayName"])
        self.assertEqual("#4E249F", manifest["interface"]["brandColor"])
        self.assertEqual("./assets/logo.png", manifest["interface"]["logo"])
        self.assertEqual("./assets/icon.png", manifest["interface"]["composerIcon"])
        self.assertNotEqual(
            manifest["interface"]["logo"], manifest["interface"]["composerIcon"]
        )

    def test_release_version_matches_python_package_metadata(self) -> None:
        manifest = json.loads(
            (REPOSITORY_ROOT / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            manifest["version"], project_version(REPOSITORY_ROOT / "pyproject.toml")
        )


if __name__ == "__main__":
    unittest.main()
