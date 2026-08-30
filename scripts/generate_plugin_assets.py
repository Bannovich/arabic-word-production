#!/usr/bin/env python3
"""Generate deterministic, original PNG identity assets for the plugin.

The mark is intentionally geometric: a document page, right-aligned lines, and
an RTL-flow arrow.  It uses no third-party logo, text, or trademark.
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
TRANSPARENT = (0, 0, 0, 0)
BLUE = (31, 78, 120, 255)
MID_BLUE = (65, 123, 173, 255)
PAPER = (244, 249, 253, 255)
INK = (24, 54, 82, 255)
WHITE = (255, 255, 255, 255)


def canvas(width: int, height: int, color: tuple[int, int, int, int] = TRANSPARENT) -> bytearray:
    return bytearray(color * width * height)


def rect(
    pixels: bytearray,
    width: int,
    height: int,
    left: int,
    top: int,
    right: int,
    bottom: int,
    color: tuple[int, int, int, int],
) -> None:
    for y in range(max(0, top), min(height, bottom)):
        start = (y * width + max(0, left)) * 4
        end = (y * width + min(width, right)) * 4
        pixels[start:end] = bytes(color) * (max(0, min(width, right) - max(0, left)))


def write_png(path: Path, width: int, height: int, pixels: bytearray) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + bytes(pixels[row * width * 4 : (row + 1) * width * 4]) for row in range(height))
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, level=9)) + chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)


def draw_page_mark(pixels: bytearray, width: int, height: int, x: int, y: int, scale: int, dark: bool = False) -> None:
    page = PAPER if not dark else WHITE
    line = BLUE if not dark else INK
    shadow = MID_BLUE if not dark else BLUE
    rect(pixels, width, height, x + 16 * scale, y + 8 * scale, x + 136 * scale, y + 168 * scale, shadow)
    rect(pixels, width, height, x, y, x + 120 * scale, y + 160 * scale, page)
    # Folded upper-left page corner.
    rect(pixels, width, height, x, y, x + 30 * scale, y + 30 * scale, shadow)
    # Right-aligned text lines: their shared right edge expresses Arabic flow.
    for offset, line_width in ((48, 76), (70, 90), (92, 62)):
        right = x + 102 * scale
        rect(pixels, width, height, right - line_width * scale, y + offset * scale, right, y + (offset + 10) * scale, line)
    # RTL arrow points left beneath the lines.
    arrow_y = y + 126 * scale
    rect(pixels, width, height, x + 35 * scale, arrow_y, x + 95 * scale, arrow_y + 10 * scale, line)
    rect(pixels, width, height, x + 25 * scale, arrow_y + 5 * scale, x + 45 * scale, arrow_y + 15 * scale, line)
    rect(pixels, width, height, x + 15 * scale, arrow_y + 10 * scale, x + 35 * scale, arrow_y + 20 * scale, line)


def generate() -> None:
    icon = canvas(512, 512)
    draw_page_mark(icon, 512, 512, 72, 46, 3)
    write_png(ASSETS / "icon.png", 512, 512, icon)

    logo = canvas(1024, 512)
    draw_page_mark(logo, 1024, 512, 88, 44, 2)
    rect(logo, 1024, 512, 390, 156, 816, 184, BLUE)
    rect(logo, 1024, 512, 390, 214, 734, 238, MID_BLUE)
    rect(logo, 1024, 512, 390, 268, 786, 292, MID_BLUE)
    write_png(ASSETS / "logo.png", 1024, 512, logo)

    dark_logo = canvas(1024, 512)
    rect(dark_logo, 1024, 512, 0, 0, 1024, 512, INK)
    draw_page_mark(dark_logo, 1024, 512, 88, 44, 2, dark=True)
    rect(dark_logo, 1024, 512, 390, 156, 816, 184, WHITE)
    rect(dark_logo, 1024, 512, 390, 214, 734, 238, PAPER)
    rect(dark_logo, 1024, 512, 390, 268, 786, 292, PAPER)
    write_png(ASSETS / "logo-dark.png", 1024, 512, dark_logo)


if __name__ == "__main__":
    generate()
