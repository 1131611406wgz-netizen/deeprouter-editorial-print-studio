#!/usr/bin/env python3
"""Validate a Phase 4 visual-review JSON and its internally consistent pass status."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED = {"rectangular_photo", "subject_oversized", "negative_space_insufficient", "composition_preserved", "decorations_template_like", "decorations_source_linked", "print_texture_present", "overly_realistic", "overly_abstract", "detail_loss_excessive", "detail_density_excessive", "fragmentation_excessive", "edges_too_constrained", "skin_tone_drift", "pass"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Visual Reviewer JSON.")
    parser.add_argument("review", type=Path)
    args = parser.parse_args()
    try:
        result = json.loads(args.review.read_text())
    except (OSError, json.JSONDecodeError) as error:
        parser.error(f"Cannot read valid JSON: {error}")
    if not isinstance(result, dict) or set(result) != REQUIRED:
        parser.error(f"Review must contain exactly: {', '.join(sorted(REQUIRED))}")
    if not all(isinstance(value, bool) for value in result.values()):
        parser.error("Every review field must be a boolean.")
    expected = (not result["rectangular_photo"] and not result["subject_oversized"] and not result["negative_space_insufficient"] and result["composition_preserved"] and not result["decorations_template_like"] and result["decorations_source_linked"] and result["print_texture_present"] and not result["overly_realistic"] and not result["overly_abstract"] and not result["detail_loss_excessive"] and not result["detail_density_excessive"] and not result["fragmentation_excessive"] and not result["edges_too_constrained"] and not result["skin_tone_drift"])
    if result["pass"] != expected:
        parser.error("pass does not match the visual quality gates.")
    print(json.dumps({"valid": True, "review": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
