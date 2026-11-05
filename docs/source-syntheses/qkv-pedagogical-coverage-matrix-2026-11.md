# Q/K/V — pedagogical coverage matrix

**Status:** living decision artifact  
**Review date:** 2026-11-05  
**Scope:** Nishanthan K (DEV), Neha KK (Medium), Codefinity, and the current LLM Lab learning system.  
**Purpose:** decide which source contributions improve learner understanding, where they belong, and what remains genuinely uncovered. This is a coverage and integration tool, not a vote on technical truth.

> **Reading rule:** source coverage records what was visible in the scanned material, not what the full article/course might contain. All three sources remain partially scanned; consult their individual reviews for retrieval and media limitations.

## 1. Learner-question coverage

| Learner question / difficulty | Nishanthan (DEV) | Neha KK (Medium) | Codefinity | Existing LLM Lab coverage | Decision |
|---|---|---|---|---|---|
| What do Q, K and V each do? | Functional walkthrough and search framing | Database/search framing | Role wording and role-check quiz | Q/K/V page: index-card analogy and projection flow | **Already covered.** Keep one canonical analogy; use alternative phrasings as source references. |
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
| Can learners identify Q/K/V role confusions? | Misconception warnings | Role rationale | Explicit multiple-choice distractor pattern | Existing self-check and extended exercises | **Reference for next exercise revision.** Reuse the diagnostic principle, not a duplicate quiz. |

## 2. Perspective matrix

This matrix captures the *teaching move* that makes a source useful, even when the underlying mechanism is already covered.

| Source | Explanatory lens | Teaching move | Best learner use | Limitation / risk | Disposition |
|---|---|---|---|---|---|
| Nishanthan K | Functional / visual / retrieval | Walks from role definitions into the attention flow; names common misreadings | First-pass orientation and misconception checking | Search language may imply hard retrieval; visual asset not inspected | Integrate by reference; retain misconception checks |
| Neha KK | Architectural design rationale / linguistic coreference | Asks why matching and payload should use separate learned projections; gives a pronoun-context scenario | Understanding why Q/K and V have distinct roles; contextual information flow | Compact computation is less complete than project derivation; example is illustrative | Integrated in canonical explanation |
| Codefinity | Geometric / lexical polysemy / formative assessment | Relates Q/K to vector alignment; uses bank/river; tests role discrimination | Optional bridge from conceptual roles to vector geometry; transfer to a second language phenomenon | Qualitative geometry can be mistaken for cosine-only similarity; quiz is a single-item sample; media not inspected | Geometric note and contrast integrated; distractor pattern retained |

## 3. Coverage status and genuine gaps

### Covered sufficiently — do not add another canonical explanation

- Functional Q/K/V roles and the index-card mental model.
- Learned projections from a shared incoming representation.
- Matching (Q/K) versus content aggregation (V).
- The score → scale → softmax → weighted-sum computation.
- Coreference and lexical polysemy as distinct contextual phenomena.
- Soft weighting versus hard nearest-neighbour retrieval.
- The warning that attention weights are not standalone causal explanations.

### Covered, but worth improving through assessment or visualization

- Dot product versus cosine similarity: a small worked numerical comparison could expose the role of vector norms more concretely.
- Q/K/V role discrimination: the existing exercise set could include distractors based on the three roles and the matching/payload distinction.
- Soft versus hard retrieval: a tiny example with two nonzero weights could counter the winner-take-all misconception.

These are **candidate improvements**, not confirmed content gaps. Before implementing them, inspect the current exercise and numerical-workbench coverage to avoid duplication.

### Not established by the three source scans

- Full causal-mask treatment, cross-attention, encoder/decoder placement and interpretability: Codefinity's parent outline lists related lessons, but those lesson bodies and assignments were not scanned.
- A worked non-symmetric attention-score matrix and the exact conditions under which asymmetry holds.
- Empirical evidence that specific heads implement coreference or word-sense disambiguation.
- A comparative audit of the original source figures, their accessibility and reuse rights.

These items must not be marked as absent from the project merely because the tutorials do not cover them. They are source-scan boundaries or possible future audit topics.

## 4. Current project learning-impact baseline

The project already has a Q/K/V self-check, a hand-worked weighted aggregation and a NumPy projection/shape exercise. The remaining opportunities are primarily assessment gaps: numerical dot-product versus cosine comparison, softmax mixture versus hard retrieval, and transfer of role discrimination to changed projection parameters. See the [learning-impact baseline and assessment plan](qkv-learning-impact-baseline-2026-11.md) for the page-by-page audit and proposed minimal diagnostic bundle. Do not add another generic projection or weighted-sum exercise.

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
