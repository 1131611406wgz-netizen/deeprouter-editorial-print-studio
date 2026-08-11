#!/usr/bin/env python3
"""Build a reproducible editorial-illustration prompt from image metadata and class rules."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from inspect_image import describe

ROOT = Path(__file__).resolve().parents[1]
RULES = json.loads((ROOT / "references" / "visual-rules.json").read_text())


def artistic_title(photo_class: str, observations: str) -> str:
    """Create a short, source-grounded archival title when no title is supplied."""
    visible = observations.lower()
    titles = {
        "architecture": [
            (("roof", "cloud"), "The Roofs Remember"),
            (("roof",), "A Quiet Roofline"),
            (("window",), "Windows at Dusk"),
            (("building",), "Between Old Walls"),
        ],
        "landscape": [
            (("mountain", "water"), "Where the Hills Meet Water"),
            (("mountain",), "Contour of Stillness"),
            (("lake", "cloud"), "Weather over Water"),
            (("water",), "The Water Holds Light"),
            (("forest",), "Green in the Distance"),
        ],
        "food": [
            (("fruit",), "A Small Harvest"),
            (("flower",), "Still Life with Flowers"),
            (("bowl",), "An Ordinary Feast"),
        ],
        "beverage": [
            (("tea",), "The Afternoon Pour"),
            (("coffee",), "A Dark Morning"),
            (("citrus",), "A Little Bit of Sun"),
        ],
        "portrait": [
            (("book",), "Between Pages"),
            (("flower",), "A Brief Bloom"),
        ],
        "product": [
            (("camera",), "An Instrument for Looking"),
            (("bottle",), "A Useful Vessel"),
        ],
    }
    for cues, title in titles.get(photo_class, []):
        if all(cue in visible for cue in cues):
            return title
    return {
        "architecture": "A Quiet Structure",
        "landscape": "A Place of Weather",
        "food": "Still Life, Slowly",
        "beverage": "A Moment to Pour",
        "portrait": "A Presence in Quiet",
        "product": "Object in Waiting",
    }[photo_class]


def select_decorators(photo_class: str, observations: str) -> list[str]:
    choices = RULES["classes"][photo_class]["decorators"]
    lower = observations.lower()
    selected = [value for key, value in choices.items() if key in lower][:5]
    return selected or ["no generic decoration; derive any marks only from visible source content"]


def layout_guardrail(photo_class: str) -> str:
    if photo_class in {"landscape", "architecture"}:
        return ("Keep approximately 50–65% of the canvas as generous off-white textured paper. "
                "Place the scene asymmetrically as an organic irregular silhouette, letting some scene-led areas extend while others dissolve naturally into paper. "
                "Preserve spatial depth and composition; do not make a rectangle, equal margins, or a full-bleed landscape poster.")
    if photo_class in {"food", "beverage"}:
        return ("Place the complete food/drink study small and centered on off-white textured paper. "
                "Keep the complete visual unit at 35–45% of the page and leave 55–65% uninterrupted paper around it; for a single bowl, keep the bowl itself below roughly 42% of page width and height. "
                "scale down instead of zooming, cropping, or touching page edges.")
    if photo_class == "product":
        return "Keep the entire product at 30–40% of the page and leave 60–70% off-white paper around it; never use an advertising pack-shot scale."
    if photo_class == "portrait":
        return "Keep the complete figure at 40–45% of the page and leave 55–60% calm off-white paper around it; never use a close beauty crop."
    return "Preserve the class-specific restrained subject scale and intentional negative space specified above."


def relaxed_print_guardrail(photo_class: str) -> str:
    return ("Handmade editorial print treatment: simplify without losing the source's recognisable identity and relationships. "
            "Use rough ink, uneven pigment coverage, subtle paper grain, worn edges, dry-brush marks, slight print misregistration, and imperfect handmade printing artifacts. "
            "Avoid photorealism, detailed rendering, realistic food or surface textures, gloss, smooth digital gradients, clean-vector polish, cartoon outlines, and excessive decoration. Use only a few quiet source-linked marks.")


def portrait_skin_guardrail(photo_class: str) -> str:
    if photo_class != "portrait":
        return ""
    return ("For visible skin, retain the source subject's relative skin-tone family and facial-plane contrast with two to four muted printed pigments. "
            "Off-white paper belongs around the figure only; never bleach, grey out, or replace skin with the paper colour.")


def build(args: argparse.Namespace) -> dict[str, object]:
    source = describe(args.image)
    item = RULES["classes"][args.photo_class]
    style = RULES["style"]
    labels = {
        "number": args.archive_number,
        "date": args.date or datetime.fromtimestamp(args.image.stat().st_mtime).date().isoformat(),
        "title": args.title or artistic_title(args.photo_class, args.observations),
    }
    decorators = select_decorators(args.photo_class, args.observations)
    prompt = f'''Use case: style-transfer
Asset type: AI editorial illustration / archival print
Input image: Image 1 is the edit target. Source canvas: {source["width"]}×{source["height"]}, exact ratio {source["aspect_ratio"]}, {source["orientation"]}.
Photo class: {args.photo_class}.
Primary request: Transform the source into a living printed artwork, not a photo filter or a photo placed inside a template.
Preserve: {item["preserve"]}.
Style/medium: {style["direction"]}; simplify photographic detail into geometric shapes, irregular colour blocks, curves, and organic contours.
Composition/framing: Preserve Image 1's exact aspect ratio and orientation. Do not crop and do not convert to 1:1. {item["composition"]}. Primary-subject / open-space target: {item["coverage"]}. {layout_guardrail(args.photo_class)} {relaxed_print_guardrail(args.photo_class)} {portrait_skin_guardrail(args.photo_class)}
Scene-linked graphic language: {"; ".join(decorators)}.
Colour palette: {", ".join(style["palette"])}; retain the source's colour relationships.
Print texture: {", ".join(style["texture"])}.
Typography: small, subordinate museum label — upper right "{labels["number"]}"; lower left "{labels["date"]}" and "{labels["title"]}". Render this text verbatim; do not add other copy.
Avoid: {", ".join(style["avoid"])}; no unrelated people, objects, ingredients, brands, or decorations.'''
    return {"analysis": source, "photo_class": args.photo_class, "observations": args.observations, "decorators": decorators, "typography": labels, "prompt": prompt}


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an editorial-print prompt for an uploaded image.")
    parser.add_argument("image", type=Path)
    parser.add_argument("--photo-class", required=True, choices=sorted(RULES["classes"]))
    parser.add_argument("--observations", default="", help="Visible scene notes used only for content-linked decoration.")
    parser.add_argument("--archive-number", default="NO. 001")
    parser.add_argument("--date")
    parser.add_argument("--title", help="Short English title; defaults to a source-grounded poetic archive title.")
    parser.add_argument("--json", action="store_true", help="Emit the full handoff plan as JSON.")
    args = parser.parse_args()
    plan = build(args)
    print(json.dumps(plan, ensure_ascii=False, indent=2) if args.json else plan["prompt"])


if __name__ == "__main__":
    main()
