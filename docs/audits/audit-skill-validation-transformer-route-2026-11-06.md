# Audit-skill validation — Transformer attention route (2026-11-06)

**Repository:** `JM-Brun/llm-lab`  
**Baseline inspected:** `main`, 2026-11-06  
**Purpose:** exercise the specialist audit skills against a real bilingual concept route, identify missing skill boundaries, and verify that findings can lead to bounded, testable corrections.

## 1. Skill selection and scope

The routing decision for this task is:

- **Primary:** `page-group-audit` — the target is a coherent pedagogical route, not an isolated page.
- **Supporting:** `page-content-audit` — sample internal page contracts and section roles.
- **Supporting:** `scientific-content-audit` — verify the attention equations, mask semantics and claims about implementation behavior.
- **Supporting:** `knowledge-architecture-audit` — compare guided-route membership, page metadata and sidebar placement.
- **Rendered-site audit:** not executed in this pass. The source and current browser harness were inspected, but no browser run or screenshot was produced.
- **Visual-asset audit:** source assets are not the main question in this route review; exact provenance/licensing is not re-audited here.

**Core route (Understand):**
1. `site/fr/transformer.qmd` / EN counterpart — overview and entry context.
2. `site/fr/queries-keys-values.qmd` / EN counterpart — Q/K/V roles and projections.
3. `site/fr/scaled-dot-product-attention.qmd` / EN counterpart — score, scale, mask, softmax and aggregation.
4. `site/fr/causal-masking.qmd` / EN counterpart — autoregressive information constraint.

**Optional depth:** `attention-score-scaling.qmd` (FR/EN), a mathematical derivation of the (1/\sqrt{d_k}) scale.  
**Separate Build branch:** `transformer-block-walkthrough.qmd` (FR/EN), which explains the concrete implementation and is not a fifth conceptual step.  
**Downstream context:** logits.  
**Excluded from core:** cross-attention, a different attention setting; tensor reference and other architecture deep dives.

## 2. Group assessment

**Verdict: coherent core route, with one optional-depth membership omission.**

The route's sequence is well founded:

| Transition | What the previous page establishes | What the next page adds | Assessment |
|---|---|---|---|
| Transformer → Q/K/V | Self-attention is a computation inside a Transformer block. | The three learned projections and their distinct roles. | Strong; the Q/K/V page explicitly isolates these objects. |
| Q/K/V → scaled attention | Q/K determine weights; V supplies content; shapes are introduced. | Dot-product scores, scaling, softmax and weighted aggregation. | Strong; each page owns a distinct layer of the mechanism. |
| Scaled attention → causal mask | Scores are scaled, optionally masked, normalized and applied to values. | The causal rule determining which key positions are allowed. | Strong; the attention page explicitly delegates temporal constraints. |
| Causal mask → logits | Future positions are excluded from autoregressive computation. | Vocabulary scores are produced from the final hidden states. | Acceptable; the Transformer overview supplies the larger forward-pass context. No new bridge page is justified. |

The conceptual route is not the Build route. The block walkthrough has `destination:build`, its own previous/next Build sequence, and links back to the concept pages. Keep this distinction.

## 3. Page-content and bilingual checks

- FR/EN counterparts exist for all core pages and have matching page types, destinations, levels, route predecessors/successors, hierarchy roles and core scope.
- Q/K/V pages have parallel section roles: intuition, source projections, operations, distinctions and self-check. Both distinguish learned projections from token categories and explicitly bound coreference/semantic interpretations.
- Scaled-attention pages have matching four-step computation, numerical example, misconception coverage, self-check and advanced implementation note.
- Causal-mask pages have matching intuition/definition/provenance/misconceptions/invariance example/connections/self-check structure.
- The FR/EN implementation notes for scaled attention both state the one-head unbatched NumPy contract, additive-mask behavior, fully masked-row convention and test coverage. These details are not silently omitted in either language.
- Differences in headings and decimal notation are natural localization, not scope drift.

No material bilingual content gap was found in the inspected sections. This is source-level parity, not rendered parity.

## 4. Scientific claim ledger

| Claim | Evidence inspected | Result |
|---|---|---|
| (Q,K\in\mathbb{R}^{T\times d_k}), (V\in\mathbb{R}^{T\times d_v}); scores are (QK^\top/\sqrt{d_k}). | FR/EN Q/K/V and scaled-attention pages. | Consistent dimensions and formula. |
| Masking is applied to scores before row-wise softmax; causal access is (j\le i). | FR/EN scaled-attention and causal-mask pages. | Correctly stated and sequenced. |
| A fully masked row is not a probability distribution; the reference implementation returns zero weights/output by explicit convention. | `src/llm_lab/foundations/attention.py`, FR/EN implementation notes, `tests/unit/test_attention.py`. | Consistent. |
| The causal invariance example changes future keys and values and checks earlier outputs, but is not a complete-GPT proof. | FR/EN embedded example and unit test inventory. | Scope is appropriately bounded. |

The implementation source validates 2-D single-head inputs, shape compatibility, finite inputs, mask shape and invalid mask entries. The tests include fully masked rows, allowed-key normalization, hand-computable weighted sums, shape invariants and causal invariance. Source and test assertions were inspected; this audit did not execute the test suite independently. No confirmed scientific error was found in the sampled claims.

## 5. Finding and correction

### TAR-01 — The optional score-scaling deep dive is absent from the computation-stage optional resources

- **Severity:** low / P2.
- **Evidence:** `data/guided-route.yml` lists cross-attention as the only optional page for the computation stage. In contrast, `site/fr/attention-score-scaling.qmd` and its EN counterpart declare `type:deep-dive`, `destination:deepen`, and `hierarchy.parents: [fr/scaled-dot-product-attention]` (EN equivalent). The core attention page directly links to this derivation as its optional deeper explanation.
- **Impact:** the deep dive is discoverable through the page and Deepen sidebar, but the stage's route-context projection does not expose it as an optional resource beside the core attention calculation.
- **Decision:** include FR/EN score-scaling pages in the computation stage's `optional_pages`. This preserves their Deepen destination and does not make them a core prerequisite or a sequential next step.
- **Implementation in this branch:** updated the canonical route YAML, added an explicit bilingual membership regression assertion, updated the generated route fragments, added route-context includes to the deep-dive pages, and updated the narrative/projection documentation.

### TAR-02 — Rendered verification remains unproven by source audits

- **Severity:** observation / P2.
- **Evidence:** source pages contain interactive disclosures, SVG diagrams, equations and generated route context. The existing browser harness has a bounded page inventory and conditional workflow execution; no run covering this full route was observed in this audit.
- **Impact:** source parity and Quarto compilation do not prove responsive layout, browser interaction, keyboard operation or accessibility exposure on these pages.
- **Recommendation:** extend the existing browser-review inventory for this route only if the project wants a durable regression gate; otherwise perform a bounded manual browser review and record exact pages/viewports. Do not claim accessibility conformance from source inspection or an Axe pass alone.

## 6. Skill-design conclusions

This real case exposed one genuine boundary not covered by the initial four new skills:

- `rendered-site-audit` verifies how a visual asset is displayed and exposed in the browser.
- It does **not** establish exact asset identity, creator/rightsholder, asset-level licence or permission to reproduce, adapt, host or redistribute it.
- The repository already has a detailed asset-audit template and explicit preservation rules. This is a durable, distinct responsibility and warrants `visual-asset-audit`.

The new `visual-asset-audit` skill therefore uses the existing template, separates existing use from proposed new use, treats attribution and licence as distinct evidence, and prohibits silent removal or replacement of existing assets. The routing matrix and rendered-site hand-off now make this boundary explicit.

No separate skill is warranted for bilingual parity, route topology or transition matrices: these remain responsibilities of page-content, page-group and knowledge-architecture audits, respectively.

## 7. Evidence limits and validation

- Repository source, page metadata, guided-route YAML, narrative curriculum, Quarto sidebar, implementation and unit-test assertions were inspected.
- No local test execution, rendered browser session, screenshot, keyboard test or assistive-technology review was performed in this audit.
- The existing PR #571 had successful CI and Quarto workflows at the time of revalidation, but its branch was reported non-mergeable against the current base. This follow-up is therefore recreated on a fresh branch from current `main`.
- This report records source-level findings and bounded changes, not measured learner outcomes.
