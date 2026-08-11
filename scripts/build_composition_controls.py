#!/usr/bin/env python3
"""Turn a validated Phase 2 analysis result into composition-control prompt text."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "references" / "composition-controller-rules.json").read_text())


def ratio_value(value: str) -> int:
    match = re.fullmatch(r"(100|[1-9]?\d)%", value)
    if not match:
        raise ValueError("subject_ratio must be an integer percentage string, for example 35%.")
    return int(match.group(1))


def control(analysis: dict[str, object]) -> dict[str, object]:
    photo_class = str(analysis.get("type", ""))
    if photo_class not in RULES:
        raise ValueError("type must be one of food, beverage, landscape, architecture, portrait, product.")
    ratio = ratio_value(str(analysis.get("subject_ratio", "")))
    rule = RULES[photo_class]
    directives = [str(rule["preserve"])]
    action = "preserve_subject_scale"

    if photo_class in {"food", "beverage", "product", "portrait"}:
        target = int(rule["target_ratio"])
        maximum = int(rule["max_ratio"])
        if ratio > maximum:
            action = "scale_subject_down"
            directives.extend([
                f"scale subject down to approximately {target}% of the full canvas",
                "preserve generous negative space around the complete primary subject",
            ])
        else:
            directives.append(f"keep the primary subject at a restrained scale; target approximately {target}% of the full canvas")
        if photo_class in {"food", "beverage"}:
            directives.extend([
                "food illustration occupies 35% canvas; for a single bowl, keep its visible width and height below roughly 42% of the page",
                "merge food details into 3-4 calm ingredient masses; no individually countable grains, seeds, noodles, or repeated micro-textures",
            ])
        directives.extend([
            "rebuild the subject from 6-12 selective imperfect printed forms; retain 3-6 recognisable anchors and a few partial material cues, but omit photographic lighting and micro-detail",
            "break selected contours into dry-brush ends and deliberate paper gaps; no neat fully rendered cutout",
            "add only 2-5 sparse source-adaptive supporting marks derived from visible geometry and palette",
        ])
    else:
        action = "apply_organic_scene_silhouette"
        directives.extend([
            "keep approximately 50-65% of the canvas as generous off-white textured paper",
            "place the scene asymmetrically with distributed quiet space; do not force a fixed vertical field",
            "organic irregular silhouette",
            "natural border breaking",
            "preserve the original atmosphere, spatial depth, natural elements, and recognisable visual identity while simplifying detail into layered printed forms",
            "relax outer edges; no clean closed silhouette or uniform clipping",
            "add only 2-5 sparse decorative marks derived from visible source elements and source palette",
            "do not render the scene as a rectangular photo frame",
            "preserve asymmetric intentional negative space",
        ])

    prompt = "Composition controls: " + "; ".join(directives) + "."
    return {
        "photo_class": photo_class,
        "source_subject_ratio": f"{ratio}%",
        "action": action,
        "directives": directives,
        "prompt_fragment": prompt,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate composition controls from Phase 2 image analysis JSON.")
    parser.add_argument("analysis", type=Path)
    args = parser.parse_args()
    try:
        analysis = json.loads(args.analysis.read_text())
        result = control(analysis)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
