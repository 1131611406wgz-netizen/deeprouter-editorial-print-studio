#!/usr/bin/env python3
"""Read image geometry without modifying the source image."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


def image_size(path: Path) -> tuple[int, int]:
    try:
        from PIL import Image  # type: ignore
        with Image.open(path) as image:
            return image.size
    except ImportError:
        pass

    try:
        result = subprocess.run(
            ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
            check=True, capture_output=True, text=True,
        )
        found = dict(re.findall(r"(pixelWidth|pixelHeight):\s*(\d+)", result.stdout))
        return int(found["pixelWidth"]), int(found["pixelHeight"])
    except (FileNotFoundError, subprocess.CalledProcessError, KeyError) as error:
        raise RuntimeError("Install Pillow or run this script on macOS with sips available.") from error


def describe(path: Path) -> dict[str, object]:
    width, height = image_size(path)
    orientation = "square" if width == height else "landscape" if width > height else "portrait"
    return {
        "image": str(path.resolve()),
        "width": width,
        "height": height,
        "aspect_ratio": f"{width}:{height}",
        "aspect_ratio_decimal": round(width / height, 6),
        "orientation": orientation,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect an image's dimensions and aspect ratio.")
    parser.add_argument("image", type=Path)
    args = parser.parse_args()
    print(json.dumps(describe(args.image), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
