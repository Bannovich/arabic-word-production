from __future__ import annotations

import struct
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
ASSET_DIRECTORY = REPOSITORY_ROOT / "assets"
EXPECTED_DIMENSIONS = {
    "icon.png": (512, 512),
    "logo.png": (1024, 512),
    "logo-dark.png": (1024, 512),
}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise AssertionError(f"not a PNG: {path.name}")
    if data[12:16] != b"IHDR":
        raise AssertionError(f"PNG has no IHDR chunk: {path.name}")
    return struct.unpack(">II", data[16:24])


class PluginAssetTests(unittest.TestCase):
    def test_required_directory_assets_are_valid_pngs_at_expected_sizes(self) -> None:
        for name, expected_size in EXPECTED_DIMENSIONS.items():
            path = ASSET_DIRECTORY / name
            self.assertTrue(path.is_file(), f"missing plugin asset: {name}")
            self.assertEqual(expected_size, png_dimensions(path), name)


if __name__ == "__main__":
    unittest.main()
