#!/usr/bin/env python3
"""Check measurable delivery constraints and emit remaining visual-review gates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from inspect_image import describe


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an editorial illustration against source geometry.")
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--photo-class", required=True, choices=["food", "beverage", "landscape", "architecture", "portrait", "product"])
    parser.add_argument("--ratio-tolerance", type=float, default=0.01)
    args = parser.parse_args()
    source = describe(args.source)
    output = describe(args.output)
    ratio_delta = abs(float(source["aspect_ratio_decimal"]) - float(output["aspect_ratio_decimal"]))
    ratio_ok = ratio_delta <= args.ratio_tolerance and source["orientation"] == output["orientation"]
    class_gate = {
        "food": "Primary food/vessel group visually occupies 30–40% of canvas.",
        "beverage": "Primary beverage/vessel group visually occupies 30–40% of canvas.",
        "product": "Complete product visually occupies 30–40% of canvas.",
        "portrait": "Person retains identity, body structure, pose, clothing relationship, and occupies 40–50% of canvas.",
        "landscape": "No rectangular photo frame; organic scene-led silhouette and 50–65% intentional open space are visible.",
        "architecture": "No rectangular photo frame; organic scene-led silhouette and 50–65% intentional open space are visible."
    }[args.photo_class]
    report = {
        "result": "PASS" if ratio_ok else "FAIL",
        "source": source,
        "output": output,
        "ratio_delta": round(ratio_delta, 6),
        "ratio_tolerance": args.ratio_tolerance,
        "automatic_checks": {"same_orientation": source["orientation"] == output["orientation"], "aspect_ratio_within_tolerance": ratio_delta <= args.ratio_tolerance},
        "manual_visual_checks": [class_gate, "Artwork reads as printed editorial illustration, not a photo filter or a pasted rectangular photo.", "Decorations are linked to visible source content, not a repeated generic motif set.", "Palette is restrained and print texture is visible; no glossy 3D or smooth digital-gradient treatment.", "Typography is subordinate and exact, if included."],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if ratio_ok else 1)


if __name__ == "__main__":
    main()
