# Learner feedback integration and generation-page split proposal

**Date:** 2026-11-13  
**Origin:** external learner simulation — reading the 17-page Understand path in route order, in French, from `llm-overview` to `gradients`/`llm-limits`.  
**Status:** historical audit and proposal; the branch also contains experimental source edits, which are not approved for merge. Decisions marked **Decision** need the maintainer's choice. The source diff was re-audited against current `main` on 2026-11-17; see §6.  
**Relation to existing audits:** this document extends the findings of:
- `docs/reviews/understand-path-reader-review-2026-11-10.md` (E2 — generation asks too much as the second page)
- `docs/understand-llms-route-audit-2026-11-09.md` (§4 — generation belongs to "Question 3: What can be done with the prediction?")
- `docs/learner-journey-audit-2026-11-05.md` (§3.2 — conceptual sequence)
- `docs/work-backlog-status.md` (P1 — reconcile learning-depth placement)

It does not duplicate or replace those audits. It adds concrete learner-perspective findings and a specific split proposal with a complete content-destination map.

---

## 1. Learner-perspective findings not yet recorded in existing audits

These observations complement — do not contradict — the existing audit findings. Each is tagged with the existing audit item it extends, or marked **New** if no prior audit covers it.

### F-L1. `generation` uses concepts not yet introduced (extends E2)

The second page of the path uses the following terms and notation before any of them are defined:

| Term / notation | First defined on | Gap (pages) |
|---|---|---|
| Token, tokenizer | `text-data` (page 3) | 1 |
| Logits | `logits` (page 11) | 9 |
| Softmax | `probabilites` (page 12) | 10 |
| $p_\theta(\cdot \mid c_t)$, $\operatorname{softmax}(z_t)$ | `probabilites` (page 12) | 10 |
| Forward pass | `transformer` (page 7) | 5 |
| KV cache, Q/K/V | `queries-keys-values` (page 8) | 6 |
| Prefill / decode phases | Not formally defined elsewhere | — |

The page addresses this with a "Première lecture" note (line 43) suggesting to read only "La boucle sur un exemple." However, this note is inside a collapsed callout; a reader who opens the full page encounters the dense notation immediately.

**Assessment:** The current `generation` page combines two distinct pedagogical goals:
1. **Goal A (overview):** Show *what* generation looks like — a loop of predict/select/reinject — using the same fictitious probabilities as the panorama.
2. **Goal B (reference):** Provide the formal notation ($c_t$, $p_\theta$, Dec), the prefill/decode distinction, the KV cache mechanics, speculative decoding, TTFT/ITL latency metrics, and the relationship between greedy, sampling, temperature, top-k and top-p.

Goal A belongs early in the path. Goal B belongs after the reader has seen logits, softmax, and Q/K/V.

### F-L2. No synthesis page closes the parcours (New)

The path ends on `gradients` (→ no `suggested_route.next`) without a page that ties together the full pipeline on the running example. The learner has traversed 17 pages and never sees the complete picture reassembled.

**Cross-reference:** The `understand-llms-route-audit-2026-11-09.md` §5 proposes a "view of the path to present to the reader" but it is an orientation view, not a concluding synthesis. The `learner-journey-audit` §3.2 validates the conceptual sequence but does not call for a closing page.

### F-L3. `text-data` lacks a concrete tokenization example (extends A1 partially)

The page explains the pipeline conceptually but never shows the running example ("C'est une bonne situation, ça, scribe ?") actually tokenized. The reader is told "la segmentation dépend du tokenizer" but never sees one. The `understand-path-reader-review` F-A1 notes that the exercise collection link is stale but does not flag the missing in-page example.

### F-L4. The attention block (Q/K/V → scaled-dot → causal-masking) lacks a worked numerical example in the main text (New)

The formulas are present and correct. The exercises (AT-A to AT-C) contain numerical computations. But in the body of the three concept pages, no single 3-token × 2-dimension example follows Q/K/V through scores → scale → mask → softmax → output. The reader must either go to the exercises or reconstruct the chain themselves.

### F-L5. `contextualized-representations` uses English example sentences (extends B6)

Already recorded as B6 in `understand-path-reader-review-2026-11-10.md`. Confirmed from the learner perspective: the French-immersion reader encounters "The river bank eroded" / "The financial bank collapsed" unexpectedly.

### F-L6. The glossary is not linked from the early pages (New)

`glossary.qmd` exists but is never referenced from `llm-overview`, `generation`, or `text-data`. A learner encountering mixed FR/EN terminology ("la *loss*", "le *prefill*", "le *teacher forcing*") in the first three pages has no way to find the glossary unless they navigate the sidebar.

### F-L7. `logits` and `loss` have no figures (New)

Of the 17 core pages, `logits` (706 words) and `loss` (1,323 words) have zero SVG figures. Both describe pipelines (state → projection → scores; per-token penalty → aggregation → scalar) that would benefit from a visual representation consistent with the style used in `transformer` and `llm-overview`.

---

## 2. The generation-page split proposal

### 2.1 Rationale

The existing audits converge on this point:
- **E2** (reader review): "generation asks too much as the second page; splitting the page in two is the larger alternative."
- **§4 / Question 3** (route audit): generation belongs with scoring and learning as a usage of the predictive distribution, after the reader understands the distribution.
- **§3.2** (learner journey): the conceptual sequence lists "Preview a complete generation loop" as step 2, then "Connect hidden states to logits, probabilities and token selection" as step 6.

The proposal resolves the tension: keep a light preview early, move the reference material later.

### 2.2 Concrete split

**Two pages replace one, with zero content deletion.**

#### Page A — `generation-overview` (new file)

**Position in route:** after `llm-overview`, before `text-data` (unchanged position 2).  
**Title:** "Générer du texte : la boucle en un coup d'œil"  
**Scope:** What generation looks like, no notation beyond $p(\cdot)$.

Content moved from current `generation.qmd`:

| Current section | Lines (approx.) | Destination |
|---|---|---|
| Chapter lead (lines 26–30) | 5 | **Page A** — reworded to remove "distribution" formalism |
| Callout "Fil rouge" (lines 32–36) | 5 | **Page A** — unchanged |
| "L'idée à retenir en une minute" (lines 38–44) | 7 | **Page A** — simplified: remove "Première lecture" sub-note about softmax |
| § "La boucle sur un exemple" (lines 63–84) | 22 | **Page A** — this is the core: the 3-turn table, the 4 gestures |
| § "Ce que la génération ne fait pas" (lines 188–198) | 11 | **Page A** — guardrails belong early |

**New content for Page A (to write):**
- A one-sentence forward-reference: "Comment le modèle calcule-t-il ces probabilités ? La suite du parcours l'explique, depuis le découpage du texte jusqu'à la distribution de sortie."
- Simplified pipeline-stepper (no "Prefill" or "Decode incrémental" labels).

**Page A word count estimate:** ~600–800 words (comparable to `logits`).

#### Page B — `generation` (existing file, trimmed)

**Position in route:** after `entropy` or `probabilites`, as stage 06 "Exécuter l'inférence et générer du texte" (matches `guided-route.yml` stage 6).  
**Title:** "Générer du texte : l'inférence pas à pas" (unchanged).  
**Scope:** Formal notation, prefill/decode, KV cache, decoding strategies, TTFT/ITL, speculative decoding.

Content remaining in current `generation.qmd`:

| Current section | Lines (approx.) | Stays in Page B |
|---|---|---|
| § "Une étape, en notation" (lines 86–117) | 32 | ✅ — this requires logits, softmax, $p_\theta$ |
| § "Du prompt aux tokens suivants : prefill et decode" (lines 120–159) | 40 | ✅ — requires Q/K/V for KV cache |
| § "Comment le prochain token est-il choisi ?" (lines 161–180) | 20 | ✅ — temperature table, top-k/top-p pointers |
| § "Idées reçues" (lines 182–186) | 5 | ✅ |
| Pipeline-stepper with prefill/decode labels | — | ✅ |

**Page B additions (to write):**
- A new chapter lead: "La page [Générer du texte : la boucle en un coup d'œil](generation-overview.qmd) a montré la boucle. Maintenant que nous connaissons les logits, le softmax et les projections Q/K/V, détaillons le calcul."
- A back-reference to the 3-turn table in Page A.

### 2.3 Route and navigation changes

```
BEFORE:
  llm-overview → generation → text-data → ... → entropy → vraisemblance → ...

AFTER:
  llm-overview → generation-overview → text-data → ... → entropy → generation → vraisemblance → ...
```

| Artefact | Change |
|---|---|
| `data/guided-route.yml` | Stage 01 replaces `generation` with `generation-overview` as core page; Stage 06 keeps `generation` |
| `site/_quarto.yml` sidebar | Under "Comprendre les LLM": `generation-overview` after `llm-overview`; `generation` after `entropy` in "Des scores aux probabilités" or in its own stage 06 section |
| Page A `suggested_route` | `previous: fr/llm-overview`, `next: fr/text-data` |
| Page B `suggested_route` | `previous: fr/entropy` (or `fr/probabilites`), `next: fr/vraisemblance` |
| `site/en/` | Mirror split: `generation-overview.qmd` + `generation.qmd` |
| Exercise pages | `exercises/generation.qmd` stays linked from Page B |
| Existing links to `generation.qmd` | All 14 internal references (from `llm-overview`, `text-data`, `transformer`, `loss`, `training-examples`, etc.) remain valid: `generation.qmd` still exists with its original URL |

### 2.4 Information preservation checklist

| Content unit | Original file | Destination file | Deleted? |
|---|---|---|---|
| 3-turn generation table | `generation.qmd` L67–71 | `generation-overview.qmd` | No — moved |
| 4-gesture loop explanation | `generation.qmd` L73–84 | `generation-overview.qmd` | No — moved |
| "Ce que la génération ne fait pas" | `generation.qmd` L188–198 | `generation-overview.qmd` | No — moved |
| Formal notation $c_t$, $p_\theta$ | `generation.qmd` L86–117 | `generation.qmd` (stays) | No |
| Prefill/decode distinction | `generation.qmd` L120–159 | `generation.qmd` (stays) | No |
| Temperature table | `generation.qmd` L169–177 | `generation.qmd` (stays) | No |
| Greedy/sampling explanation | `generation.qmd` L163–180 | `generation.qmd` (stays) | No |
| Misconceptions callout | `generation.qmd` L182–186 | `generation.qmd` (stays) | No |
| Exercise links | `generation.qmd` L200–202 | `generation.qmd` (stays) | No |
| Pipeline-stepper (full) | `generation.qmd` L46–61 | `generation.qmd` (stays) | No |
| Pipeline-stepper (simple) | — | `generation-overview.qmd` (new) | N/A |
| Fil rouge callout | `generation.qmd` L32–36 | Both (duplicated) | No |

**Proposal-only accounting:** this checklist describes the proposed two-page split, not the later source diff currently attached to this branch. It is not evidence that the branch preserves all current `main` content; see §6 for the actual comparison.

---

## 3. Cross-reference with existing issues and audits

### Updates to `understand-path-reader-review-2026-11-10.md`

| Item | Status update |
|---|---|
| **E2** | Concrete split proposal in this document (§2). Decision: maintainer chooses between the split and the in-place restructure. Both preserve all information. |
| **B6** | Confirmed by learner (F-L5). No new information. |
| **A1** | Extended by F-L3 (text-data lacks concrete tokenization example, not just stale exercise link). |

### Updates to `understand-llms-route-audit-2026-11-09.md`

| Section | Update |
|---|---|
| §3.2 | The generation-in-position-2 problem is now quantified (F-L1: 9 concepts used before definition). |
| §4 Question 3 | The split aligns with the audit's model: generation-overview stays in Q1/Q2 as a preview; the detailed generation page moves to Q3 as a usage branch. |
| §6 P0 "Rendre visible la bifurcation après la distribution" | The split implements recommendation 3 ("Présenter génération, scoring et apprentissage comme trois branches") by placing the detailed generation page alongside vraisemblance/cross-entropy/loss rather than before them. |

### Updates to `learner-journey-audit-2026-11-05.md`

| Finding | Update |
|---|---|
| F1 | The split resolves the route-representation mismatch: Page A has a clear single-use position (stage 01, orientation), Page B has a clear single-use position (stage 06, inference). No more "page used twice" ambiguity. |

### New items for `page-audit-inventory.md`

| Page pair | Status | Note |
|---|---|---|
| `generation-overview.qmd` (FR/EN) | Proposed — not reviewed | New page; content comes from reviewed `generation.qmd` |

### Suggested issue updates (GitHub)

| Issue | Suggested comment |
|---|---|
| **#130** (high-level learning architecture) | Learner simulation confirms the route audit's diagnosis: `generation` as page 2 introduces 9+ undefined concepts. A concrete split proposal (overview + detailed) is recorded in `docs/learner-feedback-integration-2026-11-13.md`. |
| **#225** (ordering/sidebar) | The generation split implies sidebar reordering: `generation-overview` in the opening pair, `generation` in the inference/usage section. Compatible with the route audit's Q1/Q2/Q3 model. |
| **#420** (softmax/temperature ownership) | The split keeps the temperature table in Page B (detailed generation), where it follows `probabilites`. No conflict with #420's scope. |
| **#447** (learner validation pilot) | Seven new learner-perspective findings (F-L1 to F-L7) provide testable hypotheses for the pilot. |

---

## 4. Other findings — suggested actions

These do not require the generation split and can be addressed independently.

| Finding | Priority | Suggested action | Batch |
|---|---|---|---|
| F-L2 (no synthesis page) | P2 | Create `fr/synthesis.qmd` / `en/synthesis.qmd` after the generation split is stable. Content: redéroule le pipeline complet sur l'exemple du scribe. | Separate PR |
| F-L3 (text-data lacks example) | P1 | Add a concrete tokenization of the scribe prefix with a specified tokenizer (e.g., GPT-2 `tiktoken`). Coordinate with #420/#82. | Batch with existing text-data follow-ups |
| F-L4 (no worked attention example in body) | P2 | Add a 3-token × $d_k=2$ numerical trace in `scaled-dot-product-attention` body, or promote the existing exercise AT-A inline. | Separate PR |
| F-L6 (glossary not linked early) | P1 | Add a footnote or callout link to `glossary.qmd` from `llm-overview` (section "Trois mots à distinguer"). | Small PR |
| F-L7 (no figures in logits/loss) | P2 | Commission SVG figures for the logits projection and the loss aggregation pipeline. | Separate PR, coordinate with #191 design system |

---

## 5. Decisions needed from the maintainer

1. **Split or restructure in place?** (E2 / F-L1) — The split is proposed; the alternative is to keep one page and restructure it with a strong visible "stop here on first reading" marker and collapsed advanced sections.
2. **Route position of Page B:** after `entropy` or after `probabilites`? The route audit suggests after the full "scores to probabilities" section (after `entropy`). The existing `guided-route.yml` stage 06 places it after stage 05.
3. **Synthesis page (F-L2):** worth creating, or is the learning map sufficient as a closing view?
4. **Glossary early link (F-L6):** a footnote from `llm-overview` or a sidebar callout?


---

## 6. Actual source-diff audit against current `main` (2026-11-17)

This section supersedes any earlier claim that the current branch has no source edits or that its source changes delete no information. The PR branch is 13 files wide, including four edited lesson pages (`fr/en/llm-overview`, `fr/en/generation`) and two generation SVGs. The comparison below is based on section headings and source content in the branch versus current `main`; it is not a rendered-page or learner validation.

### 6.1 Sections present on current `main` but absent from the branch

| Page | Content absent from branch | Existing canonical destination / required action | Decision |
|---|---|---|---|
| `fr/llm-overview.qmd` | **Où se trouve l'information ?** — distinctions among information in parameters, context, retrieval and external adaptation | The details belong to `fr/context-engineering.qmd` and `fr/rag-memory-boundaries.qmd`, but the panorama's compact conceptual distinction is not demonstrably reproduced there as a single overview. Restore a concise overview and link to those pages. | Restore or explicitly map each paragraph before accepting deletion. |
| `fr/llm-overview.qmd` | **Pourquoi les Transformers et les LLM pré-entraînés ont changé la donne** — historical landmarks, conceptual changes and why next-token prediction supports other tasks | `fr/transformer-history.qmd`, `fr/llm-evolution.qmd`, `fr/in-context-learning.qmd` and `fr/post-training.qmd` cover parts of this material, but the branch does not provide a paragraph-level destination map. | Restore the overview bridge; link to canonical deep dives. |
| `fr/llm-overview.qmd` | **Du modèle au système conversationnel** — distinction between a language model and the application/system around it | `fr/context-engineering.qmd`, `fr/rag-memory-boundaries.qmd` and `fr/llm-evolution.qmd#tool-using-systems` cover related material. The high-level system boundary should remain visible in the overview. | Restore a short distinction and links. |
| `en/llm-overview.qmd` | **Where does information reside?**, **Why Transformers and pretrained LLMs changed the game**, **From a language model to an application** | Same English canonical destinations should be linked after a paragraph-level check; do not assume French destinations prove English parity. | Restore/map in English too. |
| `fr/generation.qmd` | **Servir plusieurs requêtes : ordonnancement et réutilisation du cache** — continuous batching, prefix caching and chunked prefill, including distinct purposes and limits | The current `fr/generation.qmd` is the canonical owner: its scope explicitly includes all three mechanisms. No destination in the branch replaces the deleted section. | Restore the full section, not just a link. |
| `en/generation.qmd` | **Serving multiple requests: scheduling and cache reuse** — same three serving mechanisms | The current English `generation.qmd` is the canonical owner. | Restore the full section and maintain parity. |
| `fr/generation.qmd` | **Ressources d'implémentation complémentaires** — guided implementation resources | `fr/gpt-generation-walkthrough.qmd` and `fr/build-path.qmd` are canonical destinations, but the branch's replacement must preserve the explicit distinction between conceptual generation and implementation. | Restore a concise resource link block. |
| `en/generation.qmd` | **Additional implementation resources** | `en/gpt-generation-walkthrough.qmd` and `en/build-path.qmd`. | Restore the equivalent block. |

### 6.2 What is not lost, and what remains unproven

- The branch retains the core generation loop, notation, prefill/decode, temperature, greedy/sampling and the basic misconceptions sections. This does **not** compensate for the missing serving section.
- The proposed split's information-preservation table in §2.4 describes a different hypothetical change. It cannot be used to certify the current branch's actual diff.
- The overview's shorter prose may improve first-readability, but the reduction is not safe while the three overview sections above disappear without explicit destinations.
- The English pages have the same missing section families. A French-only repair would leave bilingual parity incomplete.
- The generated include files and SVGs must be compared as rendered assets too; heading comparison does not establish visual or accessibility preservation.

### 6.3 Required repair before any source from this branch is reusable

1. Rebuild on current `main`; do not merge or mechanically rebase this stale branch.
2. Restore the three overview bridges in FR and EN, keeping concise summaries and links rather than duplicating the deep-dive pages.
3. Restore the multi-request serving section in both generation pages, including continuous batching, prefix caching and chunked prefill, with their distinct guarantees and trade-offs.
4. Restore the implementation-resource links in both languages.
5. Compare every remaining deleted paragraph and figure against a named destination; mark it as restored, linked, intentionally removed with rationale, or unresolved.
6. Recheck generated includes, SVG alt text, Quarto output, responsive rendering, links and accessibility.
7. Keep the PR in draft until the complete preservation map and validations are reviewed.

**Conclusion:** this branch does contain useful editorial proposals, but the actual page rewrite is not information-preserving yet. The split itself remains undecided; the missing content must be restored or explicitly mapped even if the final decision is to keep a single generation page.
