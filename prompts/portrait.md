# Portrait Editorial Print Prompt

## Input contract

- `source_size`: `{{width}}×{{height}}`, `{{orientation}}`, ratio `{{aspect_ratio}}`
- `subject`: `{{person_description}}`
- `identity_and_pose`: `{{facial_structure_body_pose}}`
- `clothing_relationships`: `{{clothing_and_visible_personal_objects}}`
- `composition_to_preserve`: `{{composition}}`
- `colour_relationships`: `{{colours}}`
- `visible_decorators`: `{{source_linked_details}}`
- `archive_number`, `date`, `english_title`: `{{archive_number}}`, `{{date}}`, `{{english_title}}`

## Complete generation prompt

Transform Image 1 into a vintage editorial portrait print illustration, not a beauty filter or a fashion-ad poster. Preserve the source canvas exactly at `{{width}}×{{height}}`, ratio `{{aspect_ratio}}`, and `{{orientation}}` orientation. Do not crop or convert to 1:1. Preserve the person's identity, facial/body structure and pose `{{facial_structure_body_pose}}`, clothing relationships `{{clothing_and_visible_personal_objects}}`, composition `{{composition}}`, and colour relationships `{{colours}}`.

## Style

Vintage editorial illustration, Japanese archive print, mid-century modern graphic, handmade risograph, and museum specimen sheet. Stay midway between a painted likeness and abstract symbol: preserve identity through 8–14 selective face, hair, garment, hand, and shadow forms, plus partial garment seams, hair rhythms, and personal-object cues. Make the likeness visibly hand printed through rough ink, uneven pigment, dry-brush ends, worn contours, and subtle colour-layer misregistration. Render visible skin with two to four muted printed pigments sampled from the source's relative skin-tone family and facial-plane contrast; use warm paper only around the figure, never as a substitute for skin. Omit skin pores, photographic lighting, detailed rendering, and continuous modelling.

## Composition

Keep the pose and source framing intact inside a calm 40%–45% figure study, with visibly dominant off-white paper distributed around it. Break selected clothing and silhouette edges into dry-brush ends and paper gaps; avoid a neat fully rendered cutout. Add only 2–5 source-adaptive marks from `{{source_linked_details}}`, such as garment seams, textile rhythms, botanical elements, or personal objects; they may become small colour chips or short marks only when sampled from visible source geometry and palette. Do not introduce generic ornaments or new accessories.

## Subject ratio

The person occupies 40%–45% of the full canvas, targeting 42%. Retain 55%–60% calm paper space for an editorial composition; do not make a tight beauty crop or a full-bleed fashion hero frame.

## Negative prompt

No identity change, altered pose, altered body structure, invented clothing/accessories, beauty retouch, fully modelled skin, photographic lighting, detailed rendering, photorealism, glossy skin, pale washed-out skin, skin rendered as off-white paper, greyed or desaturated skin that loses the source's tonal relationship, smooth digital gradients, 3D, clean vector finish, cartoon outline, excessive decorative elements, fixed generic circles/squares/lines, watermark, or pasted photo rectangle.

## Texture

Use warm beige, terracotta red, mustard yellow, olive/forest green, dusty orange, dark navy, earthy brown, soft grey, and faded cream as a restrained adaptation of the source palette. Add rough ink texture, uneven pigment coverage, paper grain, dry-brush marks, slight print misregistration, and handmade imperfections.

## Typography

Use small archive typography: upper-right `{{archive_number}}`; lower-left `{{date}}` and `{{english_title}}`. Keep it subordinate and museum-label-like. Render the supplied text verbatim; do not add extra words.
