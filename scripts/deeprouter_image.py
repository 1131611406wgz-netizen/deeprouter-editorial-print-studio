#!/usr/bin/env python3
"""Generate or edit images through DeepRouter's OpenAI-compatible API."""

from __future__ import annotations

import argparse
import base64
from contextlib import ExitStack
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any
from urllib.request import urlopen


BASE_URL = "https://deeprouter.top/v1"
DEFAULT_MODEL = "gpt-image-2"
DEFAULT_QUALITY = "medium"
DEFAULT_FORMAT = "png"


def die(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_prompt(prompt: str | None, prompt_file: Path | None) -> str:
    if prompt and prompt_file:
        die("Use --prompt or --prompt-file, not both.")
    if prompt_file:
        if not prompt_file.is_file():
            die(f"Prompt file not found: {prompt_file}")
        value = prompt_file.read_text(encoding="utf-8").strip()
    else:
        value = (prompt or "").strip()
    if not value:
        die("A non-empty --prompt or --prompt-file is required.")
    return value


def output_paths(path: Path, count: int, output_format: str) -> list[Path]:
    suffix = ".jpg" if output_format == "jpeg" else f".{output_format}"
    if not path.suffix:
        path = path.with_suffix(suffix)
    if count == 1:
        return [path]
    return [path.with_name(f"{path.stem}-{index}{path.suffix}") for index in range(1, count + 1)]


def response_bytes(item: Any) -> bytes:
    encoded = getattr(item, "b64_json", None)
    if encoded:
        return base64.b64decode(encoded)
    url = getattr(item, "url", None)
    if url:
        with urlopen(url, timeout=120) as response:
            return response.read()
    die("The API response contained neither b64_json nor url image data.")
    return b""


def write_results(result: Any, paths: list[Path], force: bool) -> None:
    items = list(getattr(result, "data", []) or [])
    if not items:
        die("The API returned no images.")
    if len(items) != len(paths):
        die(f"Expected {len(paths)} image(s), received {len(items)}.")
    for item, path in zip(items, paths):
        if path.exists() and not force:
            die(f"Output already exists: {path} (use --force to overwrite)")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response_bytes(item))
        print(f"Wrote {path}")


def make_client(api_key: str) -> Any:
    try:
        from openai import OpenAI
    except ImportError:
        die("The openai Python package is required. Install it in the active environment.")
    return OpenAI(api_key=api_key, base_url=BASE_URL)


def resolve_api_key() -> str | None:
    direct = os.getenv("DEEPROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if direct:
        return direct
    launchctl = shutil.which("launchctl")
    if not launchctl:
        return None
    for name in ("DEEPROUTER_API_KEY", "OPENAI_API_KEY"):
        result = subprocess.run(
            [launchctl, "getenv", name],
            capture_output=True,
            check=False,
            text=True,
        )
        value = result.stdout.strip()
        if result.returncode == 0 and value:
            return value
    return None


def request_payload(args: argparse.Namespace, prompt: str) -> dict[str, Any]:
    payload = {
        "model": args.model,
        "prompt": prompt,
        "n": args.n,
        "size": args.size,
        "quality": args.quality,
        "output_format": args.output_format,
        "background": args.background,
        "moderation": args.moderation,
    }
    return {key: value for key, value in payload.items() if value is not None}


def run(args: argparse.Namespace) -> None:
    prompt = read_prompt(args.prompt, args.prompt_file)
    payload = request_payload(args, prompt)
    paths = output_paths(args.out, args.n, args.output_format)

    preview = {
        "base_url": BASE_URL,
        "endpoint": "/images/edits" if args.command == "edit" else "/images/generations",
        "outputs": [str(path) for path in paths],
        **payload,
    }
    if args.command == "edit":
        for image in args.image:
            if not image.is_file():
                die(f"Image file not found: {image}")
        preview["image"] = [str(path) for path in args.image]
        if args.mask:
            if not args.mask.is_file():
                die(f"Mask file not found: {args.mask}")
            preview["mask"] = str(args.mask)

    if args.dry_run:
        print(json.dumps(preview, ensure_ascii=False, indent=2))
        return

    api_key = resolve_api_key()
    if not api_key:
        die("Set DEEPROUTER_API_KEY or OPENAI_API_KEY in the local environment.")
    client = make_client(api_key)

    if args.command == "generate":
        result = client.images.generate(**payload)
    else:
        with ExitStack() as stack:
            images = [stack.enter_context(path.open("rb")) for path in args.image]
            payload["image"] = images[0] if len(images) == 1 else images
            if args.mask:
                payload["mask"] = stack.enter_context(args.mask.open("rb"))
            result = client.images.edit(**payload)
    write_results(result, paths, args.force)


def add_shared_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--quality", default=DEFAULT_QUALITY, choices=["low", "medium", "high", "auto"])
    parser.add_argument("--size", default="auto")
    parser.add_argument("--n", type=int, default=1, choices=range(1, 11))
    parser.add_argument("--output-format", default=DEFAULT_FORMAT, choices=["png", "jpeg", "webp"])
    parser.add_argument("--background", choices=["transparent", "opaque", "auto"])
    parser.add_argument("--moderation")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] == "--show-config":
        print(
            json.dumps(
                {
                    "base_url": BASE_URL,
                    "credential_configured": bool(resolve_api_key()),
                },
                indent=2,
            )
        )
        return

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    generate_parser = subparsers.add_parser("generate", help="Generate an image from text")
    add_shared_arguments(generate_parser)
    edit_parser = subparsers.add_parser("edit", help="Edit one or more source images")
    add_shared_arguments(edit_parser)
    edit_parser.add_argument("--image", type=Path, action="append", required=True)
    edit_parser.add_argument("--mask", type=Path)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
