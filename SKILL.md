---
name: deeprouter-editorial-print-studio
description: Transform user-uploaded food, beverage, landscape, architecture, portrait, or product photos into vintage editorial print illustrations through the OpenAI-compatible DeepRouter image endpoint at https://deeprouter.top/v1. Use when Codex must generate or edit bitmap images with DeepRouter while preserving source aspect ratio, composition, subject relationships, and Japanese archive print, mid-century graphic, risograph, specimen-sheet, or handmade editorial-art direction.
---

# DeepRouter Editorial Print Studio

Run this as a multi-stage generation system, not as a single filter prompt:

```text
Uploaded photo → image analysis → class router → editorial prompt plan → DeepRouter image edit → geometry + visual quality gate → delivery
```

Use the bundled `scripts/deeprouter_image.py` CLI for generation. It fixes the API base URL to `https://deeprouter.top/v1` and resolves `DEEPROUTER_API_KEY` before `OPENAI_API_KEY`, first from the process environment and then from macOS `launchctl` when available. Never read, print, persist, or include either key in commands, prompts, logs, or delivery artifacts.

Before a real request, verify only the non-secret configuration state:

```bash
python3 scripts/deeprouter_image.py --show-config
```

The API script requires Python 3.10+ and the `openai` package; image inspection also uses Pillow when available. Prefer the active project Python when it provides these packages. In Codex Desktop, use the configured bundled workspace Python when the system `python3` lacks them. Do not install or upgrade packages unless the user asks.

## Phase 1: Prompt Engine

For the current Phase 1 deliverable, load exactly one prompt module after the image type and analysis result are supplied:

| Image type | Prompt module |
| --- | --- |
| Food or beverage | `prompts/food.md` |
| Landscape or architecture | `prompts/landscape.md` |
| Portrait | `prompts/portrait.md` |
| Product | `prompts/product.md` |

Fill every `{{placeholder}}` from the image-analysis result. Output the populated **Complete generation prompt** followed by its six labeled controls: style, composition, subject ratio, negative prompt, texture, and typography. Do not call an image API or run quality checks as part of Phase 1.

## Phase 2: Image Analyzer

For the current Phase 2 deliverable, analyze the uploaded source image and output only the JSON defined in `references/image-analysis-schema.json`.

1. Obtain source geometry and a dominant-colour hint:

   ```bash
   python3 scripts/extract_image_metadata.py <image>
   ```

2. Inspect the actual image with vision. Load `prompts/image-analysis.md`, follow its classification rules, and emit its exact JSON shape. Do not guess from the filename or use dominant-colour hints to determine the class.
3. Validate the JSON before handing it to Phase 1:

   ```bash
   python3 scripts/validate_image_analysis.py <analysis.json>
   ```

The Phase 2 output contains exactly: `type`, `subject_position`, `subject_ratio`, `background_type`, `colors`, `has_people`, `has_text`, and `elements`. Do not generate an illustration, compile an editorial prompt, or run output quality checks as part of Phase 2.

## Phase 3: Composition Controller

For the current Phase 3 deliverable, pass a validated Phase 2 JSON file to the controller:

```bash
python3 scripts/build_composition_controls.py <analysis.json>
```

The resulting `prompt_fragment` is appended to the Phase 1 prompt only in a later orchestration phase; this phase outputs control JSON and does not generate an image.

- If food, beverage, product, or portrait exceeds its maximum subject ratio, emit `scale subject down` with its class target and `preserve generous negative space`.
- Food and beverage always include `food illustration occupies 35% canvas`.
- Simplify each image without losing its recognisable atmosphere, composition, subject relationships, and key visual identity. Do not turn this into an over-specified rendering recipe: observation should inform the result, not overwrite the class prompt's art direction.
- Every class must keep the complete study inside its coverage limit, with visibly distributed paper around it—not a close-up with white margin only on one side.
- Landscape and architecture always include `organic irregular silhouette` and `natural border breaking`, plus a no-rectangle constraint. Keep generous, asymmetrical paper space and let scene-led edges extend or dissolve naturally.
- Preserve subject identity and source relationships in every branch. Read `references/composition-controller-rules.json` for the exact target/max values.

## Phase 4: Visual Reviewer

After a future image-generation step produces an output, compare the source image and generated image with `prompts/visual-review.md`. The reviewer emits only the JSON defined in `references/visual-review-schema.json`, covering:

1. rectangular-photo failure;
2. oversized-subject failure;
3. insufficient-negative-space failure;
4. source-composition preservation;
5. template-like decoration failure;
6. decoration is source-linked rather than template-like;
7. editorial print-texture presence;
8. overly realistic rendering failure;
9. overly abstract / unrecognisable-subject failure;
10. excessive-detail-density failure;
11. constrained-edge failure.
12. portrait skin-tone drift / paper-bleaching failure.
13. excessive detail-loss / over-minimalisation failure.

Validate the review first:

```bash
python3 scripts/validate_visual_review.py <review.json>
```

If `pass` is false, automatically build the targeted revised prompt:

```bash
python3 scripts/build_regeneration_prompt.py <base-prompt.txt> <review.json>
```

Use the output `prompt` for the next generation attempt. Do not regenerate a prompt when `pass` is true. This Phase 4 module controls review and corrective prompt construction; it does not itself call an image API.

## System architecture

| Module | Responsibility | Resource |
| --- | --- | --- |
| Image Analyzer | Inspect the upload, preserve its dimensions/orientation, and describe visible subjects | `scripts/inspect_image.py` + visual inspection |
| Class Router | Select exactly one: `food`, `beverage`, `landscape`, `architecture`, `portrait`, `product` | this file + `references/visual-rules.json` |
| Art Director | Choose class-specific scale, composition, scene-linked ornaments, palette, print texture, and archive typography | `scripts/build_editorial_prompt.py` |
| Image Generator | Edit the upload through DeepRouter with the generated prompt; preserve identified invariants | `scripts/deeprouter_image.py` |
| Quality Gate | Check delivered geometry automatically and inspect artistic constraints visually | `scripts/validate_editorial_output.py` |

## DeepRouter image endpoint

Send image generation and image editing to the OpenAI-compatible endpoint `https://deeprouter.top/v1` through the bundled launcher. Prefer `gpt-image-2`, `quality=medium`, and `size=auto` unless the user requests otherwise or the endpoint reports that an option is unsupported.

```bash
python3 scripts/deeprouter_image.py edit \
  --image <source-image> \
  --prompt-file <prompt-file> \
  --model gpt-image-2 \
  --quality medium \
  --size auto \
  --out <output-image>
```

- Require `DEEPROUTER_API_KEY` or `OPENAI_API_KEY` to be configured locally in the process environment or macOS `launchctl`. Ask the user to configure it in their shell or operating-system credential environment; never ask them to paste it into chat.
- Do not supply `OPENAI_BASE_URL` at the command line. The launcher sets it internally and overrides inherited values so every request uses DeepRouter.
- Use `edit` for source-photo transformations and `generate` only when the user explicitly requests a new image without a source.
- Use `--dry-run` to inspect a request without a key or network call. A dry run must not be presented as successful generation.
- Do not silently fall back to another endpoint. Change the endpoint only by creating a separately named skill or when the user explicitly requests a code update.

## Mandatory workflow

1. Require a user-uploaded image. If it is only on disk, inspect it with `view_image` before using image generation.
2. Record its geometry:

   ```bash
   python3 scripts/inspect_image.py <image>
   ```

3. Visually inspect the image. Classify it using the dominant subject, not a filename. Keep the class explicit in the handoff: `food`, `beverage`, `landscape`, `architecture`, `portrait`, or `product`.
4. Write short observations of only visible content: e.g. `mountain, forest, water` or `bottle, citrus, ice`. These observations determine decorations; never add a generic circle/square/line motif set.
5. Build the prompt plan:

   ```bash
   python3 scripts/build_editorial_prompt.py <image> \
     --photo-class landscape \
     --observations "mountain, forest, water" \
     --archive-number "NO. 017" \
     --title "Mountain Water Study" \
     --json
   ```

6. Save the plan's `prompt` field to a text file and generate using the upload as the edit target:

   ```bash
   python3 scripts/deeprouter_image.py edit \
     --image <image> \
     --prompt-file <prompt.txt> \
     --model gpt-image-2 \
     --quality medium \
     --size auto \
     --out <output.png>
   ```

   State these invariants again in every correction: same aspect ratio/orientation; source identity and composition preserved; no forced 1:1 crop.
7. After generation, run the geometry gate:

   ```bash
   python3 scripts/validate_editorial_output.py <source> <output> --photo-class landscape
   ```

8. Read the report and visually complete each listed manual gate. Regenerate when any hard constraint fails. Do not deliver a square conversion, a pasted rectangular photo, an oversized subject, or a glossy digital rendering.

## Class routing rules

Read `references/visual-rules.json` before building a prompt. Apply its full class rule plus the shared visual system.

| Class | Hard composition rule |
| --- | --- |
| Food / beverage | Preserve food/drink and container relationships. Complete visual group: 30–40% of canvas; for a single bowl, its visible width/height stays below roughly 42% of page size. Merge ingredients into 3–4 calm masses; avoid individually countable food detail. |
| Product | Preserve silhouette, materials, structural/label details. Complete product: 30–40% of canvas. |
| Landscape / architecture | Preserve source ratio; let the illustrated scene occupy roughly 35–50% and off-white paper 50–65%. Never frame it as a rectangle or make it full bleed. Use an organic irregular silhouette with scene-led extensions/dissolution. |
| Portrait | Preserve identity, body structure, pose, clothing relationships, and framing. Person: 40–45% of canvas. |

## Shared artistic direction

- Transform the photo into a living printed work: vintage editorial illustration, Japanese archive print, mid-century modern graphic, handmade risograph, and museum specimen sheet.
- Before generating, read `references/deconstructed-editorial-direction.md` and `references/observational-editorial-balance.md` and apply them to every type. Use an observational editorial middle ground: irregular colour blocks, curves, organic contours, rough ink, uneven pigment, paper grain, dry-brush marks, slight print misregistration, deliberate omissions, plus a selected layer of recognisable structural/material detail. Make the printing process visible through broad brayer sweeps, imperfect overlaps, local ink skips, softened dry-brush ends, and a small offset of one colour layer. Do not merely add paper texture over an otherwise realistic rendering, and do not reduce the source to anonymous flat icons or ultra-minimal poster shapes.
- Use the restrained palette from `visual-rules.json`; retain the source's colour relationships. For portraits, preserve the source subject's relative skin-tone family and facial-plane contrast in simplified printed pigment; off-white paper is a background field only and must not bleach, wash out, or replace visible skin.
- Add only scene-linked visual language: mountains use topographic marks, forest botanical patterns, water ripple lines, city architecture lines, and equivalent source-specific details for other classes. Use only 2–5 quiet companion marks derived from visible source elements and the source palette, never a reusable decoration template. Small bars, dots, and short lines are valid only when sampled from source colour and geometry.
- Do not reproduce source surfaces literally. Simplify them into irregular colour fields, loose brush forms, layered blocks, and organic contours while preserving atmosphere, spatial depth, and the most recognisable relationships. Use rough ink, uneven pigment, paper grain, dry-brush marks, slight print misregistration, and handmade printing imperfections. Never scatter tiny disconnected colour chips, peppered white holes, or uniform AI-noise texture across the whole study.
- Add subordinate archive typography: upper-right `NO. XXX`; lower-left date and a short English title. Use user-supplied text verbatim. When no copy is supplied, the builder creates a source-grounded poetic archive title from visible cues (for example, `The Roofs Remember` for roof + cloud), never a generic `XXX Study`. Keep it evocative but restrained; never invent place names, brands, products, people, or factual metadata.
- Avoid photorealism, detailed rendering, realistic food or surface textures, shiny/glossy surfaces, smooth digital gradients, 3D, clean-vector polish, cartoon outlines, excessive decorative elements, neon, and high-saturation digital colour.

## Delivery record

Report: source dimensions and ratio; selected class; target subject/open-space rule; observed scene-linked decorators; output dimensions and ratio check; completed visual quality gates. Save the selected final image in the project when the request is project-bound.
