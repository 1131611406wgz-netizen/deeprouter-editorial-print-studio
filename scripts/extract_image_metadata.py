#!/usr/bin/env python3
"""Extract deterministic geometry and a compact dominant-colour hint from an image."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image


PALETTE = {
    "red": (190, 55, 50), "orange": (220, 120, 45), "yellow": (220, 195, 60),
    "green": (70, 130, 75), "blue": (65, 120, 185), "purple": (125, 85, 150),
    "pink": (220, 130, 160), "brown": (120, 82, 55), "black": (35, 35, 35),
    "gray": (130, 130, 130), "white": (235, 235, 230), "beige": (205, 185, 145),
}


def nearest_name(rgb: tuple[int, int, int]) -> str:
    return min(PALETTE, key=lambda name: sum((rgb[i] - PALETTE[name][i]) ** 2 for i in range(3)))


def dominant_colours(image: Image.Image) -> list[str]:
    sample = image.convert("RGB")
    sample.thumbnail((96, 96))
    counts: dict[str, int] = {}
    for rgb in sample.getdata():
        name = nearest_name(rgb)
        counts[name] = counts.get(name, 0) + 1
    return [name for name, _ in sorted(counts.items(), key=lambda item: item[1], reverse=True)[:6]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Read source image geometry and dominant-colour hints.")
    parser.add_argument("image", type=Path)
    args = parser.parse_args()
    with Image.open(args.image) as image:
        width, height = image.size
        orientation = "square" if width == height else "landscape" if width > height else "portrait"
        output = {
            "image": str(args.image.resolve()),
            "width": width,
            "height": height,
            "aspect_ratio": f"{width}:{height}",
            "orientation": orientation,
            "dominant_color_hints": dominant_colours(image),
        }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
