# Q/K/V source-media and visual-evidence audit

**Review date:** 2026-11-05  
**Scope:** Nishanthan K (DEV and author-controlled Medium mirror), Neha KK (Medium), Codefinity lesson, and the corresponding LLM Lab pages.  
**Purpose:** close the media-evidence part of issue [#473](https://github.com/JM-Brun/llm-lab/issues/473) without inferring visual content or reuse rights from captions, placeholders or attribution.

## 1. Results at a glance

| Source/component | What was inspected in this pass | What remains unavailable | Reuse / accessibility decision |
|---|---|---|---|
| Nishanthan K — DEV article / author-controlled Medium mirror | The canonical DEV article is now directly readable and exposes the full visible author text plus two top-level comments: a reader suggestion by Jessica Williams and Nishanthan's acknowledgement. No pedagogical image placement is exposed in the DEV article-body rendering. The author-controlled Medium mirror is also directly readable and exposes one in-body full-size-image placeholder after the introduction. The DEV header says “Posted on Oct 22” and “Edited on Oct 22”; the year is not exposed in the retrieved header. | The mirror's image bytes, stable image URL, composition, embedded labels, image-specific creator metadata, alt text and reuse terms were not exposed. It remains unresolved whether the mirror placeholder corresponds to an asset omitted from the DEV article-body rendering. | Link-only. Do not reproduce, trace or describe the unseen image. The mirror improves text and metadata confidence but does not close the visual scan. |
| Neha KK — Medium article | The canonical Medium page is directly readable in this pass. The page reader exposes three captioned figures (self-attention; linear projections; scaled dot-product attention) and one additional uncaptioned in-body image placeholder. The visible text, captions and placement can be reconciled with the indexed snapshot. | The four image files/bytes, stable asset URLs, actual visual content, embedded labels, image-specific creator metadata, alt text and reuse terms were not exposed. A separate cover/hero asset remains undetermined. | Link-only. Captions are not substitutes for image inspection. Do not infer what the uncaptioned slot contains. |
| Codefinity — Q/K/V lesson | The lesson text is directly readable, including the vector-alignment introduction, bank/river example and one four-option role-discrimination question. Two in-body SVG interface assets resolve to versioned CDN URLs: the Note icon (`.../definition.c461b802.svg?q=75&w=64`) and question-mark icon (`.../question-blue-sign-rounded.5e7468bd.svg?q=75&w=64`). | Both exact SVG URLs were resolved, but opening either asset failed in the page reader because the returned `image/svg+xml` content type is unsupported there. The icon artwork therefore was not visually inspected. These are interface/section icons, not pedagogical diagrams. No substantive explanatory diagram was exposed in the retrieved lesson text. Full interactive course behavior and asset rights remain unverified. | Treat the two identified assets as interface/section icons, not as evidence of a Q/K/V explanatory figure. No copying. The course lesson remains partially scanned. |
| LLM Lab — bilingual Q/K/V pages | In addition to the Quarto source, the EN/FR project SVG source was inspected directly. Both diagrams use the same 1200×660 composition and parallel flow: input X branches into Q/K/V; Q and K feed score/softmax computation; the resulting weights combine V. SVG `<title>` and `<desc>` metadata are present in both languages. | No rendered browser screenshot or desktop/mobile interaction test was available in this pass. Source inspection cannot establish actual layout, disclosure behavior, responsive rendering, equation appearance, or whether assistive technology receives the SVG description as intended. | Existing project-owned diagrams remain in place. No external figure is imported. One wording refinement is worth considering: EN “information to retrieve” / FR “l'information à récupérer” may overstate a hard-retrieval metaphor; “content to aggregate” / “contenu à agréger” would align more tightly with the soft weighted-sum explanation. This is a wording observation, not a demonstrated rendering defect. Manual rendered review remains open. |

## 2. Asset-level inventory and provenance

### 2.1 Nishanthan K

- Author-authored article: [DEV Community](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a).
- Author-controlled mirror: [Medium](https://nishanthan-k.medium.com/how-query-key-and-value-qkv-work-in-transformers-1274bfa14ea8).
- The DEV article is directly readable and exposes two top-level comments. Jessica Williams proposes a KV-cache follow-up; Nishanthan replies with a short acknowledgement. The reader suggestion is not part of the author's article and is not a technical endorsement.
- The author-controlled Medium mirror exposes one in-body image placeholder after the introduction. Its original asset URL and bytes remain unavailable; no correspondence between this placeholder and a DEV-rendered image is established.
- No figure licence or permission to reuse was established.

### 2.2 Neha KK

- Canonical article: [Medium](https://medium.com/@nkk18072004/understanding-queries-keys-and-values-in-transformers-149ed07c9f8b).
- Four in-body visual placements are visible in the article text: three captioned figures (self-attention; linear projections; scaled dot-product attention) and one uncaptioned placeholder.
- The current page-reader output does not expose the underlying image URLs or image bytes. A “No responses yet” state was visible on 2026-11-05; this is only a point-in-time comment-state observation.
- No figure licence or permission to reuse was established.

### 2.3 Codefinity

- Canonical lesson: [Queries, Keys, and Values: The Building Blocks](https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/7ce26687-f7a7-4728-be33-7014c6c7b707/a5ac1dbf-dbec-4dd1-a8d6-f3d83cbb905b).
- The retrieved lesson exposes two linked SVG interface assets with exact, versioned CDN URLs: `https://cdn.codefinity.com/master/f42d6a4a7b49c3a3f94ea4c125d3d5938acf2e8f/_next/static/media/definition.c461b802.svg?q=75&w=64` and `https://cdn.codefinity.com/master/f42d6a4a7b49c3a3f94ea4c125d3d5938acf2e8f/_next/static/media/question-blue-sign-rounded.5e7468bd.svg?q=75&w=64`. Opening either URL failed because SVG content is unsupported by this inspection path. This is a retrieval limitation, not evidence that the assets are broken for normal browsers. They are interface/section icons, not Q/K/V explanatory figures.
- No substantive Q/K/V figure was exposed in the retrieved lesson text. The vector-space explanation is prose, not an inspected diagram.
- The quiz is interactive; only the visible prompt and four options were inspected. Submission feedback and state behavior were not tested.
- No licence or figure-reuse terms were established.

## 3. Project-owned diagram source inspection

The bilingual Q/K/V SVGs were fetched as source text and compared, rather than inferred from their page captions. Both have an accessible-name pattern (`role="img"` with `aria-labelledby`), a `<title>`, and a `<desc>`. The diagram content is structurally parallel: the input representation fans out into Q, K and V; Q/K feed score and softmax computation; the weights and V feed aggregation. The SVGs explicitly state that vectors and numerical weights are omitted, so they are role diagrams rather than quantitative demonstrations.

**Wording reconciliation (2026-11-08):** the current project-owned SVGs already use “content to aggregate” (EN) and “contenu à agréger” (FR). The earlier “information to retrieve” / “l'information à récupérer” observation is therefore historical and no longer an outstanding change request. This wording is consistent with the soft weighted-sum account and avoids suggesting hard retrieval. The SVG sources also retain the same bilingual structure and accessible `<title>` / `<desc>` metadata; rendered exposure and responsive legibility still require browser evidence.

This is source-level SVG inspection only. It does not prove that the diagrams render without clipping, that text remains legible at mobile widths, or that the SVG accessibility metadata is exposed correctly in the browser accessibility tree.

## 4. Accessibility and rights are separate checks

For all source assets, the current evidence does not establish image-specific alt text, creator identity for each asset, or permission to reuse. Attribution is not a licence. Keep the sources link-only until the original asset and its rights are verified.

The LLM Lab Q/K/V SVGs are project assets and have descriptive alt text in both Quarto source pages. This source-level check does not replace inspecting the rendered accessibility tree or verifying that the alt text is actually emitted by the site renderer.

## 5. Rendered-page visual review status

**Not completed.** This audit inspected Quarto source files and live source-page text, not the deployed LLM Lab site in a graphical browser. The following checks remain open for both languages:

- desktop and narrow/mobile viewport;
- collapsed and expanded geometric disclosure;
- equation rendering and line wrapping;
- project diagram scaling, clipping and alt-text exposure;
- source links and local cross-links;
- language-switch behavior and route navigation;
- keyboard access and focus order for disclosures and links.

Do not mark the issue's manual visual-review checkbox complete until screenshot evidence or an equivalent reproducible browser-review record is attached.

## 6. Follow-up protocol

1. If a future retrieval exposes exact source image URLs, retrieve the original bytes and record URL, dimensions, format, caption, creator/provenance, alt text and licence independently.
2. Inspect image content before assigning a pedagogical role. Do not infer content from a caption or placeholder.
3. Record accessibility findings separately from reuse rights.
4. If rights remain unknown, link to the original page; do not recreate the source illustration as a substitute.
5. For LLM Lab, perform rendered desktop/mobile checks after a deploy and record screenshots or concrete observations. CI/Quarto success is not visual evidence.

## 7. Related records

- [Q/K/V source collection](qkv-source-collection.md)
- [Nishanthan K source review](qkv-nishanthan-devto-2026-11.md)
- [Neha KK source review](qkv-neha-kk-medium-2026-11.md)
- [Codefinity source review](qkv-codefinity-course-2026-11.md)
- [Pedagogical coverage matrix](../source-syntheses/qkv-pedagogical-coverage-matrix-2026-11.md)


## 8. Rendered-page evidence update — PR #680 (2026-11-08)

The responsive projection-equation correction in [PR #680](https://github.com/JM-Brun/llm-lab/pull/680) was validated with the repository's existing Chromium browser-review workflow. The Quarto site run produced artifact `site-browser-review-2bb8564f7ce46a1e2e3a35e9923d100d661f3b68` (workflow run 42483941869; tested head `4e15f3900a8eff9248788541e6eea4f56dc3538b`). The PR was merged as `3ee3f004b8d3c9f8c83f24842c4e35a776c5f1c6`.

### Scope and observations

- Six local-render cases: EN/FR × desktop 1440×1000 (light) and mobile 390×844 (light and dark).
- All six returned HTTP 200, with no console errors or uncaught page errors.
- No document-level horizontal overflow was reported in any case.
- The project-owned Q/K/V SVG loaded in both languages and had descriptive image alt text.
- Each language/viewport rendered all 28/28 MathJax expressions; no unrendered delimiters were reported.
- Desktop Axe: zero violations in both languages (33 passed rules and one incomplete check per language). The artifact did not run Axe on mobile.
- Desktop keyboard probe: visible focus indicators were observed; the disclosure was initially closed and opened with Enter in both languages.
- Route-context probe found one native breadcrumb trail, no duplicate custom breadcrumb, and resolving previous/next links.
- The mobile screenshots were inspected. The three position-wise projection equations now appear as an aligned display block; this addresses the narrow-width inline-expression defect identified by the earlier #531 artifact.

### Evidence boundary

This is a PR-local Chromium render of the Quarto site, not a fresh check of the deployed Pages host. The keyboard probe is not a complete manual keyboard audit; no touch-device test or screen-reader session was performed. The presence of SVG image alt text does not establish how assistive technology announces the SVG or exposes its internal `<title>`/`<desc>` metadata. Mobile Axe coverage is absent.

The artifact therefore closes the specific responsive-equation defect, and provides rendered FR/EN desktop/mobile evidence for the current PR head. It does **not** close the manual accessibility or deployed-site criteria in #483. Original third-party media identity, bytes, creator metadata and reuse terms remain unresolved; retain the link-only decisions in sections 1–4 and do not copy or trace those assets.

## 9. Rendered-page evidence update — PR #787 (2026-11-09)

The latest Q/K/V page-content revision was included in [PR #787](https://github.com/JM-Brun/llm-lab/pull/787), which adds the canonical reader-facing page summary and learning-map projection. Its Quarto workflow completed successfully and uploaded artifact `site-browser-review-e0098c2e668ff2c604f54fc7d3fc0d633b922be4` (workflow run [42661332708](https://github.com/JM-Brun/llm-lab/actions/runs/42661332708); artifact [13694538026](https://github.com/JM-Brun/llm-lab/actions/runs/42661332708/artifacts/13694538026); tested PR head `ce8db069e13fca3812023487e6e9b5af4712b006`). The run report and four Q/K/V screenshots were downloaded and inspected.

### Q/K/V cases and observations

- Four Q/K/V cases: EN/FR × desktop 1440×1000 and mobile 390×844, light theme.
- All four returned HTTP 200, with no browser console errors or uncaught page errors.
- No document-level horizontal overflow or reported overflow candidates.
- The project-owned bilingual SVG loaded in every case and emitted the localized descriptive image alternative text.
- All 31/31 MathJax expressions rendered in every case; no unrendered delimiters were reported.
- Desktop Axe: zero violations in both languages (33 passed rules and one incomplete check per language). Mobile Axe was skipped by the existing audit profile.
- Desktop keyboard probe: 35 focus targets per language were sampled; visible focus indicators were reported. This is automated coverage, not a complete manual keyboard audit.
- The route-context probe found one localized learning-path context, one stage link, and a resolving stage anchor in both languages.
- Desktop and mobile screenshots were inspected. The mobile projection equations remain readable as aligned display blocks; the page layout and diagrams remain within the 390px viewport.

The workflow covered 92 browser cases overall with zero reported browser-script failures. This total is site-wide; the Q/K/V-specific evidence is the four cases listed above.

### Evidence boundary

This is a PR-local Chromium render of the Q/K/V page content at PR #787's tested head. The Q/K/V source page has not changed since that revision, but later main-branch work changed shared site navigation (including PR #818); this artifact therefore does not establish the exact current-main site chrome or a fresh deployed GitHub Pages check. The public Pages URL was not accessible through the available page reader during this review.

The automated keyboard probe does not replace manual keyboard testing. No touch-device or screen-reader session was performed, and mobile Axe was not run. SVG image alt text was observed in the rendered DOM, but assistive-technology announcement of the SVG and its internal `<title>`/`<desc>` remains unverified.

This evidence supersedes the older PR #680 evidence for the Q/K/V page body and provides a more recent render of its one-minute mental model, projection equations and explanatory sections. It does not close #483: deployed-site verification, manual keyboard/touch/screen-reader checks and original third-party media provenance/reuse terms remain open.


## 10. DEV illustration retrieval update — 2026-11-12

This section supersedes the earlier DEV row and the Nishanthan subsection wherever they state that the image bytes/composition were unavailable. The maintainer supplied the exact image URL, and the image was retrieved and visually inspected on 2026-11-12:

- Article: https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a
- Transformed image URL: https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.us-east-2.amazonaws.com%2Fuploads%2Farticles%2Fys3yd2cf5dpvzprf2n6a.png
- Underlying uploaded asset: https://dev-to-uploads.s3.us-east-2.amazonaws.com/uploads/articles/ys3yd2cf5dpvzprf2n6a.png

The figure shows a continuous overview from input tokens and representations X through learned Q/K/V projections, QKᵀ scores, scaling and softmax, and weighted Value aggregation. It includes simplified sequence-level matrix shapes and the scaled dot-product equation.

The image is useful as a *composition benchmark*: it makes the whole computational path visible in one view, rather than presenting Q/K/V as isolated roles. Its boundaries are also important: it is static, does not show causal masking or multi-head splitting/concatenation, omits batch/head axes, and does not represent the entire Transformer block after attention output projection/residual/MLP. Its simplified shapes should not be mistaken for a complete batched multi-head tensor contract.

**Rights decision unchanged:** figure-specific licence and reuse permission remain unverified. Keep it link-only; do not embed, trace, crop, recolor or recreate it. Attribution is not a licence.

The project-owned EN/FR diagrams have a bounded independent refinement proposed in [PR #1030](https://github.com/JM-Brun/llm-lab/pull/1030): show projection equations and sequence-level shapes, make scaling visible, and retain the existing Q/K-versus-V explanation. This does not import the external asset or duplicate the detailed scaled-attention lesson.

The source is still partially scanned: this retrieval resolves the image-bytes/composition gap, but does not resolve figure-specific reuse rights, all linked materials, publication metadata or the previously inconsistent comment/reply history. The earlier access record remains valid as historical evidence; this addendum records the later retrieval.
