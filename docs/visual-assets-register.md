# Visual asset register

**Tracking issue:** [#156 — Audit all embedded visual assets](https://github.com/JM-Brun/llm-lab/issues/156)  
**Snapshot date:** 2026-10-30  
**Scope:** visual files under `site/images/` and externally hosted image assets embedded by the published Quarto pages.  
**Status:** initial source-level inventory; not a legal opinion, exhaustive rendered-DOM audit, or browser visual inspection.

## Preservation and decision rule

An unknown, unclear, or restrictive licence is an audit finding—not an automatic instruction to remove an illustration. Keep existing illustrations in place while the exact asset, provenance, licence/permission evidence, and intended use are investigated. Do not remove, replace, hide, or disable an existing external illustration solely because rights are uncertain. A later change requires a separate, explicit, documented decision.

Attribution establishes provenance; it does not by itself grant permission. Conversely, a restrictive licence must be assessed against the actual use and applicable terms rather than treated as proof that the current use is unlawful.

## Repository-level licensing finding

The GitHub repository metadata reports no declared repository licence (`license: null`), and no root `LICENSE`, `COPYING`, or `NOTICE` file was found in the repository tree at the snapshot date.

Consequences:
- Do not assume that the project's own SVGs are automatically available for third-party reuse merely because they are versioned here or described as original.
- Establish the authorship/provenance of each local asset from its history and contribution context, then decide and document an explicit licence for project-owned material.
- Do not retroactively claim that external figures are covered by a future repository licence.
- This is a project governance issue, not a reason to remove or disable any current asset.

## Externally hosted images currently embedded

The same image is embedded in both language variants unless otherwise noted.

| Asset | Embedded page(s) | Source / creator | Current evidence and status |
|---|---|---|---|
| Rushang Chauhan, article-cover illustration | `site/en/contextualized-representations.qmd`; `site/fr/contextualized-representations.qmd` | [LinkedIn article, *Embeddings: The Bridge Between Tokens and Context*](https://www.linkedin.com/pulse/embeddings-bridge-between-tokens-context-rushang-chauhan-oqpzf/); image served from LinkedIn CDN | Attribution and source are recorded. The article page does not display an explicit reuse licence for the image. No asset-level reuse permission has been established. **Pending**. The image was restored unchanged in PR #161 while this review is pending. |
| Catherine Arnett, tokenizer-fertility figure | `site/en/tokenization-strategies.qmd`; `site/fr/tokenization-strategies.qmd` | [Hugging Face article, *wHy DoNt YoU jUsT uSe ThE lLaMa ToKeNiZeR??*](https://huggingface.co/blog/catherinearnett/dangers-of-tokenizer-recycling); [exact image URL](https://cdn-uploads.huggingface.co/production/uploads/6384d424ac61472e5e92d403/yZnGPoBwKK4d19aCR7Ypo.png) | Source and creator are attributed. The community article does not display an explicit reuse licence for the exact image asset. Permission/licence remains unconfirmed. **Pending**; retained unchanged. |
| Petrov et al., tokenization-length/runtime figure | `site/en/tokenization-strategies.qmd`; `site/fr/tokenization-strategies.qmd` | [Paper/source page](https://www.adelbibi.com/publication/langugage_unfairness_tokenizers/); [exact image URL](https://www.adelbibi.com/publication/langugage_unfairness_tokenizers/featured_hu3a085884cc9c15c3954ff8e09a76a4a3_251753_720x2500_fit_q75_h2_lanczos.webp) | The author's page identifies the work as CC BY-NC-ND 4.0. The precise asset's coverage by that licence, rights-holder, and compatibility with this site's actual embedding/hosting context still require verification. Do not infer that the licence automatically prohibits unchanged embedding, or that attribution alone clears it. **Pending assessment**; retained unchanged. |
| Hugging Face tokenizer-pipeline diagram | `site/en/tokenization-strategies.qmd`; `site/fr/tokenization-strategies.qmd` | [Hugging Face course page](https://huggingface.co/docs/course/chapter6/8); [exact SVG asset](https://huggingface.co/datasets/huggingface-course/documentation-images/resolve/main/en/chapter6/tokenization_pipeline.svg) | The source dataset repository [declares Apache-2.0](https://huggingface.co/datasets/huggingface-course/documentation-images/blob/main/README.md). This is useful repository-level evidence, but verify that the exact file is covered by that licence and that contributor provenance/attribution conditions are satisfied. **Provisionally identified as Apache-2.0; exact-file scope check pending**. Retained unchanged. |

### Remote image links that are not currently embedded

These appear as source links in `site/references.qmd`; they are not current image embeds in the course pages and must not be counted as embedded assets:

- Jay Alammar, [GPT-2 transformer block image](https://jalammar.github.io/images/gpt2/gpt2-transformer-block-vectors-2.png).
- Jay Alammar, [GPT-2 masked-attention dataset image](https://jalammar.github.io/images/gpt2/transformer-decoder-attention-mask-dataset.png).
- 3Blue1Brown, [attention still image](https://storage.googleapis.com/3blue1brown-website-bucket/lessons/2024/gpt/attent.jpg).

The references page links to the original sources and records that these images are not currently integrated into the chapter. Their rights still matter if a future change embeds or copies them.

## Local visual assets under `site/images/`

The source-level scan found 32 SVG files. The table records source references found in the EN/FR Quarto pages. “Project-managed” describes repository location, not a verified legal licence. The page's references section describes several figures as original project diagrams; authorship and reuse terms for every file still need confirmation.

| File(s) | Referenced from | Initial classification |
|---|---|---|
| `attention-calculation-flow-en.svg`, `attention-calculation-flow.svg` | EN/FR `scaled-dot-product-attention.qmd` and `transformer.qmd` | Project-managed SVG pair; verify authorship/history and licence |
| `attention-vs-mlp-en.svg`, `attention-vs-mlp.svg` | EN/FR `transformer.qmd` | Project-managed SVG pair; verify authorship/history and licence |
| `bpe-merges-en.svg`, `bpe-merges-fr.svg` | No reference found in the scanned Quarto source files | Present but currently unreferenced; retain files and investigate intended use/provenance |
| `causal-attention-mask.svg` | EN/FR `causal-masking.qmd` | Project-managed SVG; verify authorship/history and licence |
| `contextualized-embeddings-en.svg`, `contextualized-embeddings-fr.svg` | EN/FR `contextualized-representations.qmd` | Project-managed SVG pair; verify authorship/history and licence |
| `cross-entropy-target-probability.svg`, `cross-entropy-target-probability-fr.svg` | EN/FR `cross-entropy.qmd` | Project-managed SVG pair; described as original in `site/references.qmd`; verify authorship/history and licence |
| `embedding-space-en.svg`, `embedding-space-fr.svg` | EN/FR `embedding-space.qmd` | Project-managed SVG pair; verify authorship/history and licence |
| `gpt-data-flow-en.svg`, `gpt-data-flow.svg` | EN/FR `transformer.qmd` | Project-managed SVG pair; verify authorship/history and licence |
| `math-training-pipeline.svg` | EN/FR `mathematical-foundations.qmd` | Project-managed SVG; described as original in `site/references.qmd`; verify authorship/history and licence |
| `queries-keys-values-en.svg`, `queries-keys-values.svg` | EN/FR `queries-keys-values.qmd` | Project-managed SVG pair; described as original in `site/references.qmd`; verify authorship/history and licence |
| `rope-en.svg`, `rope-fr.svg` | EN/FR `positional-encoding.qmd` | Project-managed SVG pair; verify authorship/history and licence |
| `softmax-axis-comparison-en.svg`, `softmax-axis-comparison-fr.svg` | EN/FR `tensors.qmd` | Project-managed SVG pair; verify authorship/history and licence |
| `tensors-en.svg`, `tensors-fr.svg` | EN/FR `tensors.qmd` | Project-managed SVG pair; verify authorship/history and licence |
| `token-embedding-matrix-en.svg`, `token-embedding-matrix-fr.svg` | No reference found in the scanned Quarto source files | Present but currently unreferenced; retain files and investigate intended use/provenance |
| `tokenization-language-cost.svg`, `tokenization-language-cost-fr.svg` | EN/FR `text-data.qmd` | Project-managed SVG pair; verify authorship/history and licence |
| `tokenizer-evaluation-dimensions.svg`, `tokenizer-evaluation-dimensions-fr.svg` | EN/FR `tokenization-strategies.qmd` | Project-managed SVG pair; verify authorship/history and licence |
| `unicode-utf8-tokenization-en.svg`, `unicode-utf8-tokenization-fr.svg` | EN/FR `unicode-text.qmd` | Project-managed SVG pair; verify authorship/history and licence |

## Audit method and limitations

The initial inventory was produced by:
1. Enumerating repository files under `site/` and `site/images/`.
2. Scanning the EN/FR Quarto source files for Markdown image references and remote image URLs.
3. Matching local SVG references to the 32 files in `site/images/`.
4. Separating embedded images from linked-only visual resources in `site/references.qmd`.

Not yet completed:
- inspect every SVG's embedded metadata, creation history, and contributor provenance;
- verify exact licence/permission evidence for each of the four external embeds;
- inspect external source terms and any relevant platform/CDN terms;
- verify all assets in the rendered HTML/DOM, including any future HTML/JS-generated images;
- confirm remote asset availability and actual rendering in desktop/mobile browsers;
- resolve the repository's missing licence declaration and define a policy for original project assets.

Do not mark this register complete until these checks have evidence recorded for each asset. Update it when figures are added, moved, replaced, or removed; record changes and rationale in the associated PR and #156.


## Local SVG source inspection — 2026-10-30

A direct source inspection was completed for all 32 files listed above (32/32 fetched from the repository default branch). The checks covered SVG root declarations and dimensions, XML/SVG metadata elements, comments, embedded raster images, `foreignObject`, scripts, and explicit external HTTP(S) references in `href`/`xlink:href`.

Findings:

- No SVG in this 32-file set contains an explicit `<metadata>` block or XML comment identifying an author, creator, source, copyright holder, or licence.
- No SVG contains an embedded `<image>`, `<foreignObject>`, or `<script>` element.
- No explicit external HTTP(S) `href` or `xlink:href` was found.
- The files are predominantly hand-authored SVG markup with accessible `title`/`desc` labels and vector elements. This is a description of file structure, not proof of authorship.
- Consequently, the SVG source itself does not currently provide enough provenance to establish who created each diagram or whether any underlying visual design was adapted from another source. The absence of metadata is not evidence of original authorship or a particular licence.

### Git history evidence and limitation

A repository commit search for `path:site/images` surfaced commit `c37b04483f0f6f1ae75fe767622068e445ca1d51` (21 October 2026), whose GitHub commit metadata identifies `JM-Brun` as the author. However, the returned commit is a broad site-organization commit and its exposed file list does not establish the introduction history of every SVG. The earlier directory-level history observation that commits were authored by the repository owner is likewise not asset-level proof of original creation or exclusive rights.

**Status for all 32 local SVGs: provenance/licence unresolved.** No files were modified, removed, replaced, hidden, or disabled. The two unreferenced pairs remain preserved. Next evidence required: per-file introduction commit and diff, any source/design notes outside the SVG, and confirmation from the project owner of authorship or adaptation history. Only then can the project-owned licence decision in #163 be made responsibly.


## External figure licence evidence — focused follow-up, 2026-10-30

This section records additional source-level evidence. It does not constitute legal advice or resolve whether every embedded asset is covered by the identified site/repository terms.

### Petrov et al. — CC BY-NC-ND 4.0

The author's publication page identifies *Language Model Tokenizers Introduce Unfairness Between Languages* (NeurIPS 2023) and displays CC BY-NC-ND 4.0 in its page footer. The exact image URL used by this site is the page's featured WebP asset.

The official Creative Commons deed states that CC BY-NC-ND 4.0 permits copying and redistribution in any medium or format for non-commercial purposes, subject to attribution; it does not permit public sharing of adapted material. The legal code allows technical format modifications necessary to exercise the licence, but does not remove the NonCommercial condition. The current LLM Lab pages describe the figure as embedded unchanged and link to the source. Their attribution does not currently include a direct link to the CC licence.

**Assessment:** the source-page licence is materially more informative than a generic rights-unknown status, but two questions remain open: (1) whether the featured image itself is within the material licensed under the page's CC notice and who holds the relevant rights; and (2) whether the project's public use meets the licence's NonCommercial condition. Do not infer an answer from the educational subject matter or the absence of monetisation information. Keep the image unchanged and escalate these questions for rights-holder/project-owner confirmation. If asset-level coverage is confirmed, update the attribution to include a direct licence link and any required notices.

Evidence:
- [Author's publication page](https://www.adelbibi.com/publication/langugage_unfairness_tokenizers/)
- [Exact featured image](https://www.adelbibi.com/publication/langugage_unfairness_tokenizers/featured_hu3a085884cc9c15c3954ff8e09a76a4a3_251753_720x2500_fit_q75_h2_lanczos.webp)
- [Official CC BY-NC-ND 4.0 deed](https://creativecommons.org/licenses/by-nc-nd/4.0/)
- [Official CC BY-NC-ND 4.0 legal code](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.en)

### Hugging Face tokenizer-pipeline SVG — Apache-2.0 repository evidence

The exact remote path used by LLM Lab is `en/chapter6/tokenization_pipeline.svg` in the Hugging Face dataset repository `huggingface-course/documentation-images`. Its repository README declares Apache-2.0. The Hugging Face course repository's contribution instructions also direct course authors to place course images in this documentation-images repository and use this path pattern. This corroborates that the asset is intended to be distributed as part of the course image repository.

The repository-level licence is therefore stronger evidence than a licence inferred only from the course page. However, the exact file's history/blame and any file-specific third-party notices or exclusions have not yet been inspected. The asset itself has no local copy or embedded metadata in LLM Lab; the current pages load it remotely and cite the course page.

**Assessment:** provisionally Apache-2.0 at repository level; verify exact-file provenance and notices before marking the asset fully cleared. Preserve the current remote embed unchanged.

Evidence:
- [Exact asset URL](https://huggingface.co/datasets/huggingface-course/documentation-images/resolve/main/en/chapter6/tokenization_pipeline.svg)
- [Dataset repository README](https://huggingface.co/datasets/huggingface-course/documentation-images/blob/main/README.md)
- [Hugging Face course contribution instructions](https://github.com/huggingface/course)

### Catherine Arnett and Rushang Chauhan

The inspected article pages still provide source attribution but no explicit reuse licence for the exact embedded image assets. No permission has been obtained or established in this follow-up. Both remain **unclear/pending**; keep them in place and unchanged. A permission request may be considered as a separate project-owner action; none has been sent.

### Current external-asset status

| Asset | Evidence level | Remaining check |
|---|---|---|
| Rushang Chauhan | Source identified; no explicit asset reuse licence found | Rights-holder permission/licence |
| Catherine Arnett | Source article and exact CDN image identified; no explicit asset reuse licence found | Rights-holder permission/licence |
| Petrov et al. | Source page displays CC BY-NC-ND 4.0; exact featured image identified | Confirm image coverage, rights holder, NonCommercial applicability, and complete attribution |
| Hugging Face pipeline | Exact repository path identified; dataset repository declares Apache-2.0 | Confirm exact-file history and any file-specific notices/exclusions |

No image was removed, replaced, hidden, disabled, copied locally, or modified during this follow-up.
