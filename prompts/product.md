# Product Editorial Print Prompt

## Input contract

- `source_size`: `{{width}}×{{height}}`, `{{orientation}}`, ratio `{{aspect_ratio}}`
- `subject`: `{{product_name_or_description}}`
- `structure_and_materials`: `{{silhouette_materials_functional_details}}`
- `labels_to_preserve`: `{{verbatim_label_text_or_none}}`
- `composition_to_preserve`: `{{composition}}`
- `colour_relationships`: `{{colours}}`
- `visible_decorators`: `{{source_linked_structural_details}}`
- `archive_number`, `date`, `english_title`: `{{archive_number}}`, `{{date}}`, `{{english_title}}`

## Complete generation prompt

Transform Image 1 into a vintage editorial product print illustration, not an advertising render. Preserve the source canvas exactly at `{{width}}×{{height}}`, ratio `{{aspect_ratio}}`, and `{{orientation}}` orientation. Do not crop or convert to 1:1. Preserve the product `{{product_name_or_description}}`, silhouette/material/functional relationships `{{silhouette_materials_functional_details}}`, labels `{{verbatim_label_text_or_none}}`, composition `{{composition}}`, and colour relationships `{{colours}}`.

## Style

Vintage editorial illustration, Japanese archive print, mid-century modern graphic, handmade risograph, and museum specimen sheet. Stay midway between a product rendering and abstract icon: reduce real detail into 8–14 clear, imperfect geometric forms, keeping the silhouette plus 5–8 key functional/material cues such as joints, controls, seams, labels, rim thickness, or fold lines. Use irregular colour blocks, rough ink, uneven pigment, local dry-brush ends, worn contour accents, and subtle colour-layer misregistration; omit realistic studio lighting, micro-surface texture, and detailed material rendering.

## Composition

Show the entire product and preserve its structural logic as a compact 30%–40% study on visibly dominant off-white paper. Keep it away from every edge and break selected contours into dry-brush fragments and paper gaps instead of a neat cutout. Add only 2–5 quiet source-adaptive marks derived from `{{source_linked_structural_details}}`, such as a bottle profile, lens ring, package fold, or tool-function line; they may become palette chips or short marks only when they come from the source. Do not add generic graphics or invented brand claims.

## Subject ratio

The complete product occupies 30%–40% of the full canvas, targeting 35%. Maintain generous negative space and do not turn it into an oversized commercial pack shot.

## Negative prompt

No distorted silhouette, changed material/structure, unreadable required label text, invented branding/claims, oversized advertising pack shot, realistic material shine, product-studio lighting, photorealism, detailed rendering, glossy surfaces, smooth digital gradients, 3D, clean vector finish, cartoon outline, excessive decorative elements, fixed generic circles/squares/lines, watermark, or pasted photo rectangle.

## Texture

Use warm beige, terracotta red, mustard yellow, olive/forest green, dusty orange, dark navy, earthy brown, soft grey, and faded cream while retaining source colour relationships. Add rough ink texture, uneven pigment coverage, paper grain, dry-brush marks, slight print misregistration, and handmade imperfections.

## Typography

Place small archive labels: upper-right `{{archive_number}}`; lower-left `{{date}}` and `{{english_title}}`. Keep typography museum-like and secondary. Render provided label and archive text verbatim; do not add other copy.
