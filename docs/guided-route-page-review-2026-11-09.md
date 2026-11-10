# Guided route page-by-page review — 2026-11-09

**Status:** dated snapshot; the FR editions of the 18 core guided-route pages were read in full, and FR/EN parity was checked on every page touched by the fixes below.  
**Scope:** the core pages of the route in `data/guided-route.yml` (stages 1–8), read in stage order. Optional pages, the Build branch and the exercise hub were not re-reviewed here.  
**Method:** each page's PAGE-MAP contract (id, summary, scope, purpose, suggested_route, hierarchy) was compared with the stage objective in `data/guided-route.yml`, with the page's own headings and prose, and with its explicit boundaries or "where does this step sit" statements. Numerical examples were recomputed.

## Route-level result

The page-level suggested_route chain is continuous over all 18 core pages and matches the guided-route stage order:

`index → llm-overview → generation → text-data → tokenization-strategies → embedding-space → positional-encoding → contextualized-representations → transformer → queries-keys-values → scaled-dot-product-attention → causal-masking → logits → probabilites → entropy → vraisemblance → cross-entropy → loss → gradients → (null)`

- Each stage objective in `data/guided-route.yml` is covered by the scope of its core pages.
- Concepts are introduced before use along the route: attention scores only after Q/K/V, entropy only after the conditional distribution, NLL only after likelihood, the aggregated loss only after cross-entropy, parameter updates only after gradients.
- Recomputed examples all check out: softmax of (0, ln 3) → (0.25, 0.75) [probabilites]; entropy of (0.5, 0.5) = 1 bit and of (0.9, 0.1) ≈ 0.469 bit [entropy]; likelihood 0.5 × 0.25 × 0.8 = 0.1, NLL ≈ 2.303 nats, mean ≈ 0.768 nat/token [vraisemblance]; −ln 0.9 ≈ 0.105 nat and −ln 0.1 ≈ 2.303 nats [cross-entropy]; attention output ≈ (6.7, 6.6) [scaled-dot-product-attention].
- Terminology distinctions are stable across pages: prefill vs teacher forcing, decode phase vs decoding rule, loss mask vs attention mask, predictive entropy vs observed surprisal.

## Defects fixed in this change

1. **generation (FR, EN) — stray closing math delimiter in §1.** A `\]` without an opening `\[` rendered as a stray "]" after the four-candidate-probability example. Removed in both languages.
2. **generation (FR) — accent.** "La génération autoregressive" → "La génération autorégressive" (§2).
3. **gradients (FR, EN) — displaced equation in the chain-rule section.** "Si les logits dépendent des paramètres z = z(θ), alors :" / "If logits depend on parameters z = z(θ), then:" was followed by an inserted explanatory paragraph, with the display equation pushed below it. The equation now directly follows the colon, and the paragraph refers to "la formule ci-dessus" / "the formula above". No content was added or removed.
4. **Missing PAGE-MAP `summary` on tokenization-strategies and entropy (FR, EN).** Bilingual summaries were added, consistent with the other route pages. `data/concepts.yml` carries no page summaries, so no registry change is required.

## Open observations (no change made)

- `generation` is a core page at stages 1 and 6 of `data/guided-route.yml`, but its PAGE-MAP `suggested_route` is a single linear chain encoding the stage-1 position (previous: llm-overview, next: text-data). The generated suggested-route and guided-context partials should be re-inspected at the next render to confirm the stage-6 revisit is presented as designed.
- The linear page chain links entropy → vraisemblance, so a reader following only the per-page navigation skips the stage-6 revisit of generation and its optional continuation (decoding-strategies). The stage-6 revisit must come from the route projections, not from the page chain.
- `cross-entropy` is core at stage 7 and optional at stage 8 (double membership, like `generation`). Intentional; recorded so future audits do not report it as drift.
- The external LinkedIn-sourced figure on contextualized-representations remains pending #156; the page already discloses this.
- `gradients` closes the route (`next: null`), consistent with stage 8 being the last stage.

## Maintenance note

This is a textual and metadata review from the repository sources. It does not substitute for the browser-render, accessibility or learner evidence tracked in #483, #584 and #447, and it modifies neither `data/guided-route.yml` nor `data/concepts.yml`.

## Follow-up: guided-context partial verification (2026-11-09)

Re-inspection confirms that a generated multi-stage partial exists for `generation`, and that the canonical route registry places this page in both stage 1 (orientation) and stage 6 (inference). This is **not** a missing lesson include. Merged PR #787 deliberately keeps `generation` free of the generated `.guided-page-context` panel: the stage-1/stage-6 memberships belong to the guided-route projection in the learning map, not to reader-facing lesson commentary. The existing browser contract in `scripts/site-browser-review.mjs` explicitly checks that this panel is absent on `generation.html`; that assertion must remain.

The route registry and its generated learning-map projection remain the source for both memberships. Do not add the generated partial to `site/fr/generation.qmd` or `site/en/generation.qmd`. The other core and optional route pages (58 pages checked across FR and EN) retain their existing guided-context behavior; optional pages whose suggested route is null correctly omit the suggested-route partial. No change to `data/guided-route.yml`, `data/concepts.yml` or `site/tools/build_learning_map.py` is justified by this inspection.

Unverified follow-up for a separate Build-branch review (not classified as a defect here): `fr/training-examples` and `en/training-examples` declare a non-null `previous` route (`<lang>/corpus-preparation`, `next: null`) but include no suggested-route partial. Verify the intended Build navigation contract before changing either page.
