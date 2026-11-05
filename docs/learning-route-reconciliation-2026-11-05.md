# Reconciliation of the learning-path representations

**Audit date:** 2026-11-05  
**Repository:** `JM-Brun/llm-lab`  
**Scope:** reconcile the conceptual curriculum, the guided-route diagram, the Quarto navigation, the page graph, and the concept/resource graph. This audit coordinates [#225](https://github.com/JM-Brun/llm-lab/issues/225), [#355](https://github.com/JM-Brun/llm-lab/issues/355), and [#415](https://github.com/JM-Brun/llm-lab/issues/415).

## 1. Decision: one curriculum, multiple projections

The representations answer different questions and must not be forced into one sequence.

| Representation | Canonical source | What it represents | What it must not imply |
|---|---|---|---|
| Narrative curriculum | `docs/learning-path.md` | Conceptual learning order, explanations, branches and status-aware crosswalk | That every page is a mandatory step |
| Guided-route diagram | `data/guided-route.yml` | Six bilingual conceptual stages, core pages and optional pages | The implementation dependency order |
| Practical Build route | `site/fr/build-path.qmd`, `site/en/build-path.qmd` | G0–G9 implementation checkpoints, including the G1b → G2 training-data branch | That corpus/windows are needed to demonstrate inference |
| Quarto navigation | `site/_quarto.yml` | Published destinations and reader-facing grouping | A strict prerequisite graph or a complete course sequence |
| Page graph | Page-map metadata in `site/**/*.qmd`, projected by the learning-map generator | Suggested reading transitions, conceptual page hierarchy and cross-links | That hierarchy edges are reading-order or computational-dependency edges |
| Concept/resource graph | `data/concepts.yml`, `data/domains.yml`, `data/resources.yml` | Language-independent concepts, typed semantic relations, domains and non-page artifacts | Page order, a syllabus, or a complete ontology |

The narrative curriculum is authoritative for pedagogical intent. The route YAML is its machine-readable, reader-facing projection. The Build milestone table is a separate implementation projection. Navigation and graphs expose the available resources without redefining the curriculum.

## 2. Canonical conceptual route ↔ diagram ↔ pages

The six stages in `data/guided-route.yml` correspond to the conceptual order in `docs/learning-path.md`:

| Guided stage | Core page IDs (FR; EN counterpart follows the same topic) | Build crosswalk | Quarto destination |
|---|---|---|---|
| `orientation` | `llm-overview`, `generation` | G0; early preview of G7 | Understand |
| `text-input` | `text-data`, `tokenization-strategies` | G1 | Understand → text/representations |
| `representations` | `embedding-space`, `positional-encoding`, `contextualized-representations` | G3 for initial vectors; G4–G5 for contextualization | Understand → text/representations |
| `computation` | `transformer`, `queries-keys-values`, `scaled-dot-product-attention`, `causal-masking` | G4–G5 | Understand → Transformer/attention |
| `prediction` | `logits`, `probabilities`, `likelihood`, `generation` | G6 and a return to G7 | Understand → attention/output |
| `learning-evaluation` | `cross-entropy`, `loss`, `gradients`, `evaluation-experimentale` | G8–G9 / E1 | Understand learning pages; Practice for evaluation |

The bilingual route generator resolves core and optional page IDs against published page metadata. The learning-map pages render the route before the exploratory maps. The route is a suggested conceptual progression: pages inside a stage are complementary, not strict prerequisites.

**Intentional revisit:** `generation` appears in both `orientation` and `prediction`. The first occurrence is a black-box preview of the complete autoregressive loop with fixed parameters; the later occurrence reconnects token selection to logits and probabilities. This is a pedagogical revisit, not a second canonical generation lesson. The preview must not suggest that the model has useful learned parameters.

## 3. Build dependencies: the separate training-data branch

The Build path has two branches that join at parameter learning:

- **Inference branch:** G0 → G1 → G3 → G4 → G5 → G6 → G7.
- **Training-data branch:** G1 → G1b → G2.
- **Join:** both the model path and the training-data branch are needed for G8; G9/E1 evaluates the resulting evidence.

| Milestone | Responsibility | Dependency / boundary |
|---|---|---|
| G0 | Define the small decoder-only GPT being built | Orientation |
| G1 | Prepare prompt text and tokenizer behavior | Shared text/tokenization foundation |
| G1b | Corpus provenance, eligibility, parsing, filtering, deduplication, splits and tokenizer fitting/freezing | Training-data branch; not needed for inference |
| G2 | Convert token streams into context windows, shifted targets, batches and masks | Follows G1b; needed before G8, not before G3–G7 |
| G3–G6 | Represent tokens, compute attention, assemble GPT, predict/select | Inference branch |
| G7 | Demonstrate autoregressive inference with fixed, randomly initialized parameters | Inference branch; incoherent output is expected |
| G8 | Calculate loss, backpropagate, update parameters, validate and checkpoint | Requires model path and G1b → G2 |
| G9 / E1 | Verify compatibility and evaluate claims with appropriate baselines and error analysis | Evaluation checkpoint; evaluation remains cross-cutting |

The following source corrections are included in this reconciliation:

1. `docs/learning-path.md` now names the data branch as **G1b → G2**, rather than incorrectly assigning corpus preparation to G2.
2. The FR/EN Build tables now expose G1b as a separate branch milestone and reserve G2 for training-example construction. Corpus loading and split audits are no longer mixed into G2's implementation status.
3. `docs/full-curriculum-plan.md` now distinguishes the inference branch, training-data branch and G8 join. Its earlier flat list placed training examples before representation building and inference last, which could be mistaken for the operational route and conflicted with the published Build milestones.

## 4. Navigation correspondence

The bilingual Quarto sidebars preserve the intended four destinations:

- **Understand:** orientation, inference preview, text/tokenization, representations, Transformer computation, prediction and learning concepts.
- **Build:** the practical small-GPT path, corpus preparation, training examples and code walkthroughs.
- **Practice & experiment:** exercises, controlled visual exploration and experimental evaluation.
- **Deepen:** optional mathematical, architectural, tokenizer and inference-efficiency branches.
- **Reference:** glossary, history and bibliography.

The route is not a mirror of sidebar indentation. In particular, Practice is transversal rather than a mandatory final stage; Deepen is optional; glossary/history/reference pages support discovery rather than extend the core sequence. The Build branch is linked as a practical companion to the conceptual route, not inserted into the inference stages.

The route and navigation should be checked against the actual Quarto render list as well as the sidebar. A sidebar entry alone is not proof that a page is published; generated route links must resolve to published page IDs.

## 5. Graph correspondence and semantic boundaries

Three graph-like structures coexist:

1. **Suggested page route** (`suggested_route.previous/next`): a recommended reader transition.
2. **Page hierarchy and cross-links** (`hierarchy.parents/children`, `related`): conceptual containment or useful association between pages.
3. **Concept relations** in `data/concepts.yml`: directed, typed semantic relations between language-independent concepts. Page-resource links associate concepts with their explanations; they do not establish reading order.

The resource registry `data/resources.yml` describes non-page artifacts such as implementation modules. These are useful evidence and exploration nodes, not additional mandatory curriculum steps.

The exploratory page map is derived from Quarto navigation and page metadata. Its BFS rank combines suggested-route and hierarchy edges as a deterministic **display-order heuristic only**. It is not a curriculum sequence, a prerequisite ordering, or a topological sort of conceptual dependencies. Do not reuse this rank to render the guided route.

The concept graph is separate from the page graph. A concept's prerequisite relation must not be turned automatically into a page-navigation edge. Likewise, a page parent/child relation must not be interpreted as a prerequisite merely because one page is nested under another.

## 6. Findings and status

| Check | Result | Evidence / interpretation |
|---|---|---|
| Six-stage route ↔ narrative conceptual order | Aligned | Route YAML and `docs/learning-path.md` use orientation → inference preview → text → representations → computation → prediction → learning/evaluation |
| Route page references ↔ published bilingual pages | Generator-enforced | Core and optional IDs resolve against published metadata; FR/EN route copy is required |
| Conceptual route ↔ Build milestones | Aligned after this change | G0/G1/G3–G7 map to the inference route; G1b/G2 are a separate branch; G8/G9 follow |
| Build branch ↔ navigation | Aligned after this change | Both languages expose corpus preparation and training examples under Build |
| Quarto sidebar ↔ exploratory page map | Generated from the same navigation source | Map generator reads the Quarto sidebar and page metadata |
| Page metadata integrity and FR/EN parity | Existing automated validator | Reuse the existing page-metadata validator; do not add a duplicate validator |
| Concept graph ↔ curriculum | Deliberately separate | Typed concept relations are for semantic exploration, not route generation |
| Rendered UX and learner comprehension | Not established by source checks | Desktop/mobile, keyboard/touch and learner validation remain separate evidence |

## 7. Remaining work and ownership

### P1 — Keep the sources synchronized

- [ ] When G1b/G2 scope or evidence changes, update the learning-path crosswalk, content-section mapping and both Build tables in the same change.
- [ ] Keep `data/guided-route.yml` limited to conceptual stages; do not add G1b/G2 as conceptual stages.
- [ ] Keep the six-stage route and the G0–G9 implementation branch linked by a crosswalk, not by duplicating all milestone data in the route YAML.
- [ ] Re-run the existing metadata, route-generation, bilingual Quarto render and local-link checks after edits.

### P2 — Reader-experience validation

- [ ] Inspect the rendered guided route and exploratory page/concept maps on desktop and mobile.
- [ ] Verify keyboard and touch operation, focus visibility, accessible labels and the static list alternative.
- [ ] Confirm that the repeated generation link reads as a deliberate preview/revisit rather than an accidental duplicate.
- [ ] Conduct a small learner walkthrough against the acceptance questions in #225. CI and page publication are not learner evidence.

### Ownership

- **#225:** conceptual sequence, overview boundaries, progressive disclosure and learner-facing acceptance.
- **#355:** canonical page ownership and residual cross-page duplication. The route crosswalk does not close its page-by-page editorial audit.
- **#415:** guided route versus exploratory map and their source alignment. Source-level route generation/topology work is in place; rendered browser validation remains coordinated with #337/#417.
- **#337 / #417:** rendered visual, responsive, keyboard and touch review.
- **#78:** implementation dependency and concept-to-code evidence inventory.

## 8. Validation commands

Use the existing project checks; do not create a workflow per concept or a second page-graph validator.

```bash
uv run --with-requirements docs/requirements-history-validation.txt python site/tools/check_page_metadata.py
uv run --locked pytest
uv run python site/tools/build_learning_map.py
quarto render site
```

The repository's CI/Quarto workflows may wrap these commands and add rendered local-link checks. A passing structural validator proves reference integrity and declared parity, not pedagogical quality or learner mastery.
