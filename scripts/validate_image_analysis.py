#!/usr/bin/env python3
"""Validate Phase 2 Image Analyzer JSON without external dependencies."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


TYPES = {"food", "beverage", "landscape", "architecture", "portrait", "product"}
POSITIONS = {"upper-left", "upper-center", "upper-right", "center-left", "center", "center-right", "lower-left", "lower-center", "lower-right", "distributed"}
BACKGROUNDS = {"natural", "urban", "indoor", "studio", "plain", "mixed", "unknown"}
REQUIRED = {"type", "subject_position", "subject_ratio", "background_type", "colors", "has_people", "has_text", "elements"}


def fail(message: str) -> None:
    print(json.dumps({"valid": False, "error": message}, ensure_ascii=False))
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an Image Analyzer JSON result.")
    parser.add_argument("analysis", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.analysis.read_text())
    except (OSError, json.JSONDecodeError) as error:
        fail(f"Cannot read valid JSON: {error}")
    if not isinstance(data, dict) or set(data) != REQUIRED:
        fail(f"JSON must contain exactly: {', '.join(sorted(REQUIRED))}")
    if data["type"] not in TYPES:
        fail("type is invalid")
    if data["subject_position"] not in POSITIONS:
        fail("subject_position is invalid")
    if not isinstance(data["subject_ratio"], str) or not re.fullmatch(r"(?:100|[1-9]?\d)%", data["subject_ratio"]):
        fail("subject_ratio must be an integer percentage string")
    if data["background_type"] not in BACKGROUNDS:
        fail("background_type is invalid")
    if not isinstance(data["colors"], list) or not 1 <= len(data["colors"]) <= 6 or not all(isinstance(item, str) and item for item in data["colors"]):
        fail("colors must contain 1–6 non-empty strings")
    if not isinstance(data["elements"], list) or not 1 <= len(data["elements"]) <= 12 or not all(isinstance(item, str) and item for item in data["elements"]):
        fail("elements must contain 1–12 non-empty strings")
    if not isinstance(data["has_people"], bool) or not isinstance(data["has_text"], bool):
        fail("has_people and has_text must be booleans")
    print(json.dumps({"valid": True, "analysis": data}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
