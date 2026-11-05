# Q/K/V — pedagogical coverage matrix

**Status:** living decision artifact  
**Review date:** 2026-11-05  
**Scope:** Nishanthan K (DEV), Neha KK (Medium), Codefinity, and the current LLM Lab learning system.  
**Purpose:** decide which source contributions improve learner understanding, where they belong, and what remains genuinely uncovered. This is a coverage and integration tool, not a vote on technical truth.

> **Reading rule:** source coverage records what was visible in the scanned material, not what the full article/course might contain. All three sources remain partially scanned; consult their individual reviews for retrieval and media limitations.

## 1. Learner-question coverage

| Learner question / difficulty | Nishanthan (DEV) | Neha KK (Medium) | Codefinity | Existing LLM Lab coverage | Decision |
|---|---|---|---|---|---|
| What do Q, K and V each do? | Functional walkthrough and search framing | Database/search framing | Role wording plus three checks on mechanism purpose, pooling and contextual aggregation | Q/K/V page: index-card analogy and projection flow | **Already covered.** Keep one canonical analogy; use alternative phrasings as source references. |
| Why are there three projections rather than one? | Mentions learned projections and roles | Explicit matching-versus-payload rationale | Distinguishes roles, but no equally explicit design rationale observed | Q/K/V page now explains Q/K as matching views and V as payload/content view | **Integrated.** Preserve as a design rationale, not a new mechanism. |
| What is the input to Q/K/V? | Embedding/representation shorthand | Word-embedding shorthand | Not a major focus in inspected lesson | Q/K/V page clarifies incoming hidden representation, first-block embeddings and positional-information variants | **Clarified in project.** Avoid copying source shorthand as a universal statement. |
| What are Q and K mathematically? | Vector/projection description | Projection equations | Geometric vector-alignment lens | Q/K/V page has optional geometric note; attention page owns full score derivation | **Integrated in layers.** Geometry is optional; formal calculation remains in attention lesson. |
| Does dot product mean cosine similarity? | Semantic-similarity caveat, but not the central geometry derivation | Not central | Alignment language risks angle-only reading | Project explicitly includes norm-and-angle identity and distinction from cosine similarity | **Guardrail retained.** Future numerical example may make the distinction more tangible. |
| How do scores become an output? | Score → scale → softmax → aggregation | Compact four-step sequence | No full pipeline derivation in inspected lesson | Dedicated scaled-dot-product-attention lesson, including equations and numerical work | **Do not duplicate.** Link/hand off to canonical derivation. |
| Is attention a hard nearest-neighbour lookup? | Warns against winner-take-all reading | Retrieval language needs qualification | Geometric alignment could invite nearest-neighbour interpretation | Q/K/V and attention pages distinguish softmax weighting from hard retrieval | **Guardrail retained.** Test with a distractor in a future exercise revision. |
| Why does context matter across positions? | Bank ambiguity and pronoun reference | Pronoun “it” with candidate antecedents | Bank/river context | Q/K/V page uses coreference; contextualized-representations owns fuller lexical ambiguity treatment | **Integrate by contrast.** Keep coreference and polysemy distinct. |
| Does an example prove that a head performs coreference or disambiguation? | No measured head evidence in inspected article | No measured head evidence in inspected article | No measured head evidence in inspected lesson | Project labels examples as illustrations, not empirical evidence | **Explicit limitation.** Keep this qualification wherever examples could be over-read. |
| What do attention weights mean? | Cautions against semantic-similarity readings | Broad interpretability suggestion needs qualification | Not developed in inspected lesson | Project warns weights alone are not causal explanations | **Project treatment takes precedence.** Use sources as misconception prompts, not authority. |
| How do multiple heads fit in? | Brief architecture summary | Follow-on mention | Listed in parent outline; lesson body not inspected | Overview and dedicated multi-head/Build material | **No change from outline alone.** Scan full lesson before extracting more. |
| What changes with causal masking, cross-attention or encoder/decoder placement? | Not sufficiently developed in inspected article | Not sufficiently developed in inspected article | Parent outline lists related lessons; their bodies were not scanned | Covered elsewhere in the project route | **Out of scope for these scans.** Do not infer lesson content from course headings. |
| Can a learner calculate QKᵀ and the weighted sum by hand? | Compact conceptual sequence | Compact equations | Not observed | Dedicated attention lesson / numerical workbench | **Project-owned.** Source overlap is not a reason to add another derivation. |
| Can learners explain the purpose and effect of attention? | Misconception warnings | Role rationale | Three questions on Q/K/V purpose, dynamic attention versus pooling, and contextual aggregation | Existing self-check and extended exercises | **Assessment-design reference.** Reuse the question patterns only if a learner gap is observed; do not duplicate a quiz. |

## 2. Perspective matrix

This matrix captures the *teaching move* that makes a source useful, even when the underlying mechanism is already covered.

| Source | Explanatory lens | Teaching move | Best learner use | Limitation / risk | Disposition |
|---|---|---|---|---|---|
| Nishanthan K | Functional / visual / retrieval | Walks from role definitions into the attention flow; names common misreadings | First-pass orientation and misconception checking | Search language may imply hard retrieval; visual asset not inspected | Integrate by reference; retain misconception checks |
| Neha KK | Architectural design rationale / linguistic coreference | Asks why matching and payload should use separate learned projections; gives a pronoun-context scenario | Understanding why Q/K and V have distinct roles; contextual information flow | Compact computation is less complete than project derivation; example is illustrative | Integrated in canonical explanation |
| Codefinity | Geometric / lexical polysemy / three-question formative check | Relates Q/K to vector alignment; uses bank/river; checks mechanism purpose, attention versus pooling, and contextual aggregation | Optional bridge from conceptual roles to vector geometry; transfer to a second language phenomenon | Qualitative geometry can be mistaken for cosine-only similarity; quiz feedback untested; media not inspected | Geometric note and contrast integrated; three question patterns retained as design references |

## 3. Coverage status and genuine gaps

### Covered sufficiently — do not add another canonical explanation

- Functional Q/K/V roles and the index-card mental model.
- Learned projections from a shared incoming representation.
- Matching (Q/K) versus content aggregation (V).
- The score → scale → softmax → weighted-sum computation.
- Coreference and lexical polysemy as distinct contextual phenomena.
- Soft weighting versus hard nearest-neighbour retrieval.
- The warning that attention weights are not standalone causal explanations.

### Candidate improvements: current decisions

- **Dot product versus cosine similarity:** the geometric note states the norm/angle identity; [#489](https://github.com/JM-Brun/llm-lab/pull/489) adds a deterministic regression counterexample, and the optional geometry probe is in the #447 pilot protocol. No new learner-facing exercise page is justified before pilot evidence.
- **Q/K/V role discrimination:** the existing self-check and W_V-only exercise already cover the roles; the #447 protocol now records a pre-reading baseline and post-reading V-only counterfactual. Do not add another role quiz.
- **Soft versus hard retrieval:** the canonical worked attention example already shows non-degenerate softmax weights and a weighted output. [#480](https://github.com/JM-Brun/llm-lab/issues/480) was closed as not planned to avoid duplicating this treatment.

These are no longer active page-change requests. The remaining gate is learner evidence, not more generic exercises; see the [learning-impact baseline](qkv-learning-impact-baseline-2026-11.md#9-post-implementation-reconciliation--2026-11-05).

### Not established by the three source scans

- Full causal-mask treatment, cross-attention, encoder/decoder placement and interpretability: Codefinity's parent outline lists related lessons, but those lesson bodies and assignments were not scanned.
- A worked non-symmetric attention-score matrix and the exact conditions under which asymmetry holds.
- Empirical evidence that specific heads implement coreference or word-sense disambiguation.
- A comparative audit of the original source figures, their accessibility and reuse rights.

These items must not be marked as absent from the project merely because the tutorials do not cover them. They are source-scan boundaries or possible future audit topics.

## 4. Current project learning-impact baseline

The project already has a Q/K/V self-check, a hand-worked weighted aggregation and a NumPy projection/shape exercise. PR #489 adds implementation regression tests for dot-product/cosine ranking and attention invariants; PR #490 extends the single formative pilot protocol with a Q/K/V baseline, V-only counterfactual and optional geometry probe. These are not learner-outcome data. The remaining work is to complete the browser/accessibility review in #483 and then, if appropriate, run the existing pilot in #447. Do not add another generic projection, weighted-sum or role quiz.

## 5. Integration decision rules

For every new source contribution, record all of the following before deciding that it is redundant:

1. **Learner question:** what question does this explanation help answer?
2. **Explanatory lens:** functional, geometric, linguistic, architectural, computational, historical, visual, experimental or assessment-oriented?
3. **Teaching move:** analogy, derivation, counterexample, diagram, numerical example, quiz, implementation or experiment?
4. **Incremental value:** what does it add beyond the current canonical page, exercise, visual or Build implementation?
5. **Boundary:** what does the source not establish, or what misconception might its wording create?
6. **Destination:** canonical lesson, optional note, exercise backlog, source dossier, implementation, or nowhere.
7. **Disposition:** integrate; integrate by reference; already covered; defer; reject.

A topical match is not sufficient evidence for **already covered**. First test whether the source contributes a different explanatory lens, learner question, example, teaching move or useful limitation. Conversely, a different analogy alone does not justify adding another canonical paragraph if it creates no new learning outcome.

## 6. How to extend this matrix

- Add a source column only after its source-specific extraction and review exist.
- Preserve source-local provenance; do not collapse disagreements into a synthetic source.
- Mark unavailable material as **not inspected**, not **absent**.
- Separate author text, reader comments, linked resources, course outlines and implementation evidence.
- Keep source coverage distinct from project coverage.
- Update the decision and destination when the canonical lesson or exercises change.
- Do not promote a pedagogical example into a canonical concept node unless it represents a stable concept or relation.

## 7. Traceability

- [Living Q/K/V source collection](../source-reviews/qkv-source-collection.md)
- [Complementary explanatory perspectives](qkv-complementary-perspectives-2026-11.md)
- [Learning-impact baseline and assessment plan](qkv-learning-impact-baseline-2026-11.md)
- [Q/K/V learning-graph and route comparison](../source-reviews/qkv-learning-graph-comparison-2026-11.md)
- [Nishanthan K source review](../source-reviews/qkv-nishanthan-devto-2026-11.md)
- [Neha KK source review](../source-reviews/qkv-neha-kk-medium-2026-11.md)
- [Codefinity source review](../source-reviews/qkv-codefinity-course-2026-11.md)
- [External-source integration workflow](../workflows/source-to-learning-system-integration.md)


## 7. Closure review — 2026-11-05

The following decisions were made after inspecting the merged bilingual Q/K/V pages, the bilingual scaled-attention pages, and the current English attention exercise inventory. They supersede the earlier status of the three candidates as merely unverified possibilities.

| Candidate | Evidence in the canonical project | Decision | Owner / destination |
|---|---|---|---|
| Dot product versus cosine similarity | Both Q/K/V pages state $q^\top k=\lVert q\rVert\lVert k\rVert\cos\theta$ and explicitly explain that vector norms matter. However, the current attention workbench's hand example uses unit-norm Q/K vectors, so it does not demonstrate a ranking difference between dot product and cosine similarity. | **Accept a bounded numerical contrast**, but do not add another Q/K/V page section. Use a two-dimensional, hand-checkable pair with different key norms in the existing attention workbench. | **#80** — scaled dot-product attention. |
| Soft weighting versus hard retrieval | The scaled-attention lesson computes softmax weights approximately $(0.67,0.33)$ and an output $(6.7,6.6)$ from two distinct value vectors. It explicitly says the weights are relative to accessible keys, not semantic relevance. The Q/K/V lesson also rejects nearest-neighbour interpretation. | **Already demonstrated; reject a second numerical example.** The existing example is sufficient to show that aggregation is not argmax retrieval. | No new work. Retain links between Q/K/V and the attention derivation. |
| Attention assessment patterns | The existing Q/K/V self-check tests which projections determine weights and which vectors are aggregated; the exercise tests the W_V-only counterfactual. Codefinity adds three four-option checks on the mechanism's purpose, dynamic attention versus fixed pooling, and contextual aggregation. The interactive answer/feedback behavior was not exercised. | **Retain as design references; do not add a duplicate quiz now.** Revisit if the learner pilot identifies a specific gap in explaining dynamic weighting or contextual aggregation. | Keep all three source items in the extraction; any future learner-facing assessment belongs with the attention exercise owner, coordinated with #80 and #447. |

### Numerical contrast hand-off to #80

The existing attention example uses unit vectors, for which dot product and cosine similarity coincide. A minimal contrast can use:

- $q=(1,0)$;
- $k_1=(0.1,0)$, giving $q^\top k_1=0.1$ and $\cos(q,k_1)=1$;
- $k_2=(10,10)$, giving $q^\top k_2=10$ and $\cos(q,k_2)=1/\sqrt{2}$.

The dot product ranks $k_2$ higher, while cosine similarity ranks $k_1$ higher. This isolates the effect of vector norms without requiring a new concept page. If used in scaled attention, state the key dimension and apply the same scale factor to both scores; the ranking remains unchanged by this common positive scale. The example is a mathematical counterexample, not a claim about semantic relevance.

### Evidence boundary

This is a source-content and canonical-source inspection, not a rendered browser review. The bilingual Q/K/V and scaled-attention source files were compared; the Q/K/V pages have matching optional geometric, linguistic and role distinctions, and the scaled-attention pages have matching worked-example structure. Desktop/mobile layout, disclosure interaction, equation rendering, keyboard behavior and screenshot evidence remain unverified. See the [component-level media and visual audit](../source-reviews/qkv-visual-asset-audit-2026-11-05.md).


## 8. Fourth tutorial — Brenndoerfer (2026-11-05)

[Source review](../source-reviews/qkv-mbrenndoerfer-2026-11.md) · [structured extraction](../../data/extractions/mbrenndoerfer-qkv-attention-mechanism.yml) · [incremental pilot report](qkv-incremental-source-pilot-2026-11-05.md)

| Learner question / difficulty | Brenndoerfer contribution | Existing LLM Lab coverage | Decision |
|---|---|---|---|
| Why divide scores by √d_k? | Assumption-explicit variance derivation and Gaussian simulation | Canonical scaled-attention formula and implementation | Integrate by reference; no duplicated derivation unless learner evidence identifies a gap |
| How do shapes propagate? | Compact unbatched single-head shape walkthrough; explicitly allows d_v ≠ d_k | Existing attention/Build tensor-contract treatment | Already covered; retain as alternative reference |
| Can I trace the full mechanism numerically? | Complete three-token example with intermediate Q/K/V, scores, weights and outputs | Existing numerical workbench | Integrate by reference only; no second workbench |
| What geometric property follows from weighted aggregation? | Convex-hull interpretation of each normalized weighted sum | Weighted-sum formula is canonical; convex geometry is not foregrounded | Defer pending a concrete learner task |
| What can be inferred from attention patterns? | Suggests trained heads may learn linguistic relations and describes positional symmetry | Project already warns against interpreting weights as causal explanations | Keep caveats as a source-quality regression case; do not strengthen canonical claims |
| Which mental model explains the roles? | Database/library lookup analogy | Canonical index-card analogy | Already covered; avoid analogy accumulation |

**Synthesis update:** the fourth source adds depth and a more explicit teaching route, not a new canonical mechanism. Its scaling derivation is the strongest incremental contribution, but reference-only integration is preferred because the canonical lesson already owns the mathematical pipeline. The convex-hull result remains an optional research/geometry lead rather than a learner-facing addition. Source text inspection does not establish figure quality, code execution, interactive assessment quality or learner benefit.
