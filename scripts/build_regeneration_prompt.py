#!/usr/bin/env python3
"""Build a targeted corrective prompt fragment when Phase 4 review fails."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def directives(review: dict[str, bool]) -> list[str]:
    fixes: list[str] = []
    if review["rectangular_photo"]:
        fixes.append("do not render a rectangular photograph, photo card, or framed image on a background; transform the whole image into a living printed artwork")
    if review["subject_oversized"]:
        fixes.append("scale subject down and preserve generous negative space; keep the complete primary subject within its class-specific coverage rule")
    if review["negative_space_insufficient"]:
        fixes.append("reduce the visual mass and move it away from page edges; make off-white paper visibly dominate around the complete study instead of concentrating empty space in only one area")
    if not review["composition_preserved"]:
        fixes.append("preserve the original source aspect ratio, orientation, subject relationships, and compositional logic; do not crop or force 1:1")
    if review["decorations_template_like"]:
        fixes.append("remove generic circles, squares, horizontal lines, and repeated template motifs; derive every decoration from visible source content")
    if not review["decorations_source_linked"]:
        fixes.append("replace arbitrary ornaments with only 2–5 sparse companion marks inferred from visible source elements and the source palette; omit ornaments entirely when the source supplies no meaningful cue")
    if not review["print_texture_present"]:
        fixes.append("strengthen handmade print character with rough ink, uneven pigment coverage, paper grain, dry-brush marks, and subtle print misregistration; avoid glossy photorealism, 3D, and smooth digital gradients")
    if review["overly_realistic"]:
        fixes.append("reduce photographic lighting, surface detail, and material rendering; rebuild the scene from broad distressed dry-brush, scumbled ink, and hand-rolled colour fragments with deliberate paper gaps")
    if review["overly_abstract"]:
        fixes.append("restore 3-6 recognisable source anchors and a few partial material or structure cues; keep the handmade print texture, but do not reduce the subject into anonymous flat symbols")
    if review["detail_loss_excessive"]:
        fixes.append("restore 6-12 selective source-derived structural details—such as rims, overlaps, grouped ingredient divisions, seams, controls, canopy rhythms, path turns, or ridge breaks—while keeping broad connected colour masses and handmade print character")
    if review["detail_density_excessive"]:
        fixes.append("merge repeated micro-details into 3-4 calm grouped masses; remove individually countable ingredients, seeds, noodles, or texture marks and preserve only a few selective descriptive cues")
    if review["fragmentation_excessive"]:
        fixes.append("replace scattered colour chips, peppered white holes, and all-over gritty texture with 3-6 connected calm colour masses; keep print wear only at a few local edges and retain materially continuous sky, ground, foliage, or object planes")
    if review["edges_too_constrained"]:
        fixes.append("relax the scene perimeter: replace tidy continuous or clipped edges with interrupted dry-brush sweeps, local extensions, non-contiguous fragments, and dissolving paper gaps; do not use an enclosing outline")
    if review["skin_tone_drift"]:
        fixes.append("for the portrait, restore the source subject's relative skin-tone family and facial-plane contrast using two to four muted printed pigments; keep off-white paper around the figure only and never use it as a substitute for visible skin")
    return fixes


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a corrective regeneration prompt from a failed visual review.")
    parser.add_argument("base_prompt", type=Path)
    parser.add_argument("review", type=Path)
    args = parser.parse_args()
    try:
        review = json.loads(args.review.read_text())
        base = args.base_prompt.read_text().strip()
    except (OSError, json.JSONDecodeError) as error:
        parser.error(f"Cannot read input: {error}")
    needed = {"rectangular_photo", "subject_oversized", "negative_space_insufficient", "composition_preserved", "decorations_template_like", "decorations_source_linked", "print_texture_present", "overly_realistic", "overly_abstract", "detail_loss_excessive", "detail_density_excessive", "fragmentation_excessive", "edges_too_constrained", "skin_tone_drift", "pass"}
    if not isinstance(review, dict) or set(review) != needed or not all(isinstance(value, bool) for value in review.values()):
        parser.error("Review JSON is invalid; run validate_visual_review.py first.")
    if review["pass"]:
        print(json.dumps({"regeneration_required": False, "prompt": base}, ensure_ascii=False, indent=2))
        return
    fixes = directives(review)
    revised = base + "\n\nREGENERATION CORRECTIONS (mandatory):\n- " + "\n- ".join(fixes)
    print(json.dumps({"regeneration_required": True, "corrections": fixes, "prompt": revised}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
