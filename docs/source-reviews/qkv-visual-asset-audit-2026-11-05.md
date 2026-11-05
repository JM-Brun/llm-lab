# Q/K/V source-media and visual-evidence audit

**Review date:** 2026-11-05  
**Scope:** Nishanthan K (DEV and author-controlled Medium mirror), Neha KK (Medium), Codefinity lesson, and the corresponding LLM Lab pages.  
**Purpose:** close the media-evidence part of issue [#473](https://github.com/JM-Brun/llm-lab/issues/473) without inferring visual content or reuse rights from captions, placeholders or attribution.

## 1. Results at a glance

| Source/component | What was inspected in this pass | What remains unavailable | Reuse / accessibility decision |
|---|---|---|---|
| Nishanthan K — DEV article / author-controlled Medium mirror | The author-controlled Medium mirror is directly readable. It exposes one in-body full-size-image placeholder after the introduction, followed by the article text, equations and one reader response. The article identifies its publication date as 22 October 2026 on the mirror. | The image bytes, stable image URL, composition, embedded labels, image-specific creator metadata, alt text and reuse terms were not exposed. The DEV canonical URL did not yield a direct page in this pass. | Link-only. Do not reproduce, trace or describe the unseen image. The mirror improves text and metadata confidence but does not close the visual scan. |
| Neha KK — Medium article | The canonical Medium page is directly readable in this pass. The page reader exposes three captioned figures (self-attention; linear projections; scaled dot-product attention) and one additional uncaptioned in-body image placeholder. The visible text, captions and placement can be reconciled with the indexed snapshot. | The four image files/bytes, stable asset URLs, actual visual content, embedded labels, image-specific creator metadata, alt text and reuse terms were not exposed. A separate cover/hero asset remains undetermined. | Link-only. Captions are not substitutes for image inspection. Do not infer what the uncaptioned slot contains. |
| Codefinity — Q/K/V lesson | The lesson text is directly readable, including the vector-alignment introduction, bank/river example and one four-option role-discrimination question. Two in-body SVG assets are linked: a “Note” icon and a question-mark icon. | Both SVG retrievals failed in the page reader because the returned image/svg+xml content type is unsupported there. The icon artwork therefore was not visually inspected. No substantive explanatory diagram was exposed in the retrieved lesson text. Full interactive course behavior and asset rights remain unverified. | Treat the two identified assets as interface/section icons, not as evidence of a Q/K/V explanatory figure. No copying. The course lesson remains partially scanned. |
| LLM Lab — bilingual Q/K/V pages | Source files site/en/queries-keys-values.qmd and site/fr/queries-keys-values.qmd were inspected. Each references its own project SVG diagram with descriptive alt text and includes the same optional geometric note, source links and linguistic contrast. | No rendered browser screenshot or desktop/mobile interaction test was available in this pass. Source inspection cannot establish actual layout, disclosure behavior, responsive rendering or equation appearance. | Existing project-owned diagrams remain in place. No external figure is imported. Manual rendered review remains open. |

## 2. Asset-level inventory and provenance

### 2.1 Nishanthan K

- Author-authored article: [DEV Community](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a).
- Author-controlled mirror: [Medium](https://nishanthan-k.medium.com/how-query-key-and-value-qkv-work-in-transformers-1274bfa14ea8).
- The mirror exposes one image placeholder after the introductory paragraphs. The page reader does not expose its original asset URL or bytes.
- A reader comment on the mirror is separately attributable to the commenter; it is not part of the author's article. The KV-cache suggestion remains a community contribution and must not be attributed to Nishanthan.
- No figure licence or permission to reuse was established.

### 2.2 Neha KK

- Canonical article: [Medium](https://medium.com/@nkk18072004/understanding-queries-keys-and-values-in-transformers-149ed07c9f8b).
- Four in-body visual placements are visible in the article text: three captioned figures (self-attention; linear projections; scaled dot-product attention) and one uncaptioned placeholder.
- The current page-reader output does not expose the underlying image URLs or image bytes.
- No figure licence or permission to reuse was established.

### 2.3 Codefinity

- Canonical lesson: [Queries, Keys, and Values: The Building Blocks](https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/7ce26687-f7a7-4728-be33-7014c6c7b707/a5ac1dbf-dbec-4dd1-a8d6-f3d83cbb905b).
- The retrieved lesson exposes two linked SVG assets: a “Note” icon and a question-mark icon. Their retrieval failed in this inspection environment because SVG content is unsupported by the image-opening path. This is a retrieval limitation, not evidence that the assets are broken for normal browsers.
- No substantive Q/K/V figure was exposed in the retrieved lesson text. The vector-space explanation is prose, not an inspected diagram.
- The quiz is interactive; only the visible prompt and four options were inspected. Submission feedback and state behavior were not tested.
- No licence or figure-reuse terms were established.

## 3. Accessibility and rights are separate checks

For all source assets, the current evidence does not establish image-specific alt text, creator identity for each asset, or permission to reuse. Attribution is not a licence. Keep the sources link-only until the original asset and its rights are verified.

The LLM Lab Q/K/V SVGs are project assets and have descriptive alt text in both Quarto source pages. This source-level check does not replace inspecting the rendered accessibility tree or verifying that the alt text is actually emitted by the site renderer.

## 4. Rendered-page visual review status

**Not completed.** This audit inspected Quarto source files and live source-page text, not the deployed LLM Lab site in a graphical browser. The following checks remain open for both languages:

- desktop and narrow/mobile viewport;
- collapsed and expanded geometric disclosure;
- equation rendering and line wrapping;
- project diagram scaling, clipping and alt-text exposure;
- source links and local cross-links;
- language-switch behavior and route navigation;
- keyboard access and focus order for disclosures and links.

Do not mark the issue's manual visual-review checkbox complete until screenshot evidence or an equivalent reproducible browser-review record is attached.

## 5. Follow-up protocol

1. If a future retrieval exposes exact source image URLs, retrieve the original bytes and record URL, dimensions, format, caption, creator/provenance, alt text and licence independently.
2. Inspect image content before assigning a pedagogical role. Do not infer content from a caption or placeholder.
3. Record accessibility findings separately from reuse rights.
4. If rights remain unknown, link to the original page; do not recreate the source illustration as a substitute.
5. For LLM Lab, perform rendered desktop/mobile checks after a deploy and record screenshots or concrete observations. CI/Quarto success is not visual evidence.

## 6. Related records

- [Q/K/V source collection](qkv-source-collection.md)
- [Nishanthan K source review](qkv-nishanthan-devto-2026-11.md)
- [Neha KK source review](qkv-neha-kk-medium-2026-11.md)
- [Codefinity source review](qkv-codefinity-course-2026-11.md)
- [Pedagogical coverage matrix](../source-syntheses/qkv-pedagogical-coverage-matrix-2026-11.md)
