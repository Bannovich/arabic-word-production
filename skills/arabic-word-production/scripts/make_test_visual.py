from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def _font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def create_activation_flow(output: str | Path) -> Path:
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1600, 520), "#F4F7FB")
    draw = ImageDraw.Draw(image)
    title_font = _font(48, True)
    label_font = _font(34, True)
    detail_font = _font(24)
    draw.text((70, 42), "Claude Pro activation flow", fill="#17365D", font=title_font)

    cards = [
        ("1", "Record", "Start before the link"),
        ("2", "Private", "Use Incognito"),
        ("3", "Create", "Open the Magic Link"),
        ("4", "Confirm", "Verify total = $0"),
    ]
    colors = ["#2F5597", "#5B9BD5", "#70AD47", "#ED7D31"]
    left, top, width, height, gap = 70, 165, 320, 250, 55
    for index, ((number, label, detail), color) in enumerate(zip(cards, colors)):
        x = left + index * (width + gap)
        draw.rounded_rectangle((x, top, x + width, top + height), radius=28, fill="white", outline=color, width=6)
        draw.ellipse((x + 24, top + 26, x + 94, top + 96), fill=color)
        number_box = draw.textbbox((0, 0), number, font=label_font)
        draw.text((x + 59 - (number_box[2] - number_box[0]) / 2, top + 34), number, fill="white", font=label_font)
        draw.text((x + 30, top + 120), label, fill="#17365D", font=label_font)
        draw.text((x + 30, top + 180), detail, fill="#595959", font=detail_font)
        if index < len(cards) - 1:
            arrow_x = x + width + 12
            mid_y = top + height // 2
            draw.line((arrow_x, mid_y, arrow_x + 30, mid_y), fill="#7F8C9A", width=8)
            draw.polygon([(arrow_x + 30, mid_y - 15), (arrow_x + 52, mid_y), (arrow_x + 30, mid_y + 15)], fill="#7F8C9A")
    image.save(target, format="PNG", optimize=True)
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(create_activation_flow(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
