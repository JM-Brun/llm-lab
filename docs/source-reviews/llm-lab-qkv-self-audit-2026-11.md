# LLM Lab Q/K/V lesson — self-audit and comparative positioning

**Audit date:** 2026-11-05  
**Audited revision:** `main` at `79b91333a41bb74aa10a29f9e9a201eeb87a35a7`  
**Scope:** canonical English/French Q/K/V lessons, adjacent scaled-dot-product-attention lessons, attention exercise inventory, project diagrams, and the four extracted introductory sources.  
**Purpose:** assess whether LLM Lab can be treated as a useful public pedagogical source on Q/K/V, rather than only as a consumer of external explanations.

## 1. Executive assessment

**Conclusion: yes, LLM Lab is already a credible and comparatively strong pedagogical resource for the standard Q/K/V formulation.** Its main advantage is not novelty of the mechanism. It is the way it combines a clear conceptual distinction, explicit mathematical notation and tensor shapes, careful boundaries on interpretation, bilingual coverage, a sequenced learning route, worked calculations, exercises, implementation links, and inspectable source provenance.

Against the four scanned introductory sources, LLM Lab has greater explanatory depth and stronger epistemic safeguards. The external sources remain useful for their compact analogies, visual explanations, geometric intuition and quiz design. The project does not need to imitate their page structures or reproduce their media.

This is a **content and source-quality audit**, not a claim of measured learning effectiveness or completed browser QA. CI, Quarto and the publish workflow succeeded for the audited main revision. The published pages could not be opened through the available page-reading interface during this audit; desktop/mobile layout, live equation rendering, disclosure behavior, keyboard navigation and screen-reader output remain unverified.

### Readiness by dimension

| Dimension | Assessment | Evidence / remaining qualification |
|---|---|---|
| Conceptual accuracy | Strong | Q/K determine compatibility scores and weights; V supplies the vectors aggregated with those weights. Distinguishes scores, weights and outputs. |
| Mathematical completeness | Strong for an introductory lesson | Projection equations, dimensions, dot-product geometry and a linked full attention derivation. |
| Misconception control | Strong | Explicitly rejects cosine-only, nearest-neighbour, semantic-relevance and attention-as-causal-explanation interpretations. |
| Pedagogical sequencing | Strong | Context → Transformer → Q/K/V → scaled attention → causal masking; deeper derivation and Build implementation remain separate. |
| Practice | Good, not yet comprehensive | Worked attention example, projection/shape exercise and self-check; limited diagnostic coverage of score geometry and weight interpretation. |
| Bilingual parity | Strong in source content | EN/FR pages share the same core structure, equations, examples and exercise logic. Rendered parity is not yet checked. |
| Visual explanation | Good in source assets | Original EN/FR SVGs have title/description metadata, alt text, matching 1200×660 layouts and explicit one-position simplification. Actual browser rendering remains unverified. |
| Traceability and evidence | Strong | Source-specific YAML extractions, reviews, comparison matrix, graph/route comparison, media audit and explicit scan limitations. |
| Research-source status | Promising, not yet formalized | Public URL and Git history exist; a stable release/citation record and independent learner evaluation would strengthen citability. |

## 2. What the canonical pages currently teach

The Q/K/V page deliberately owns the **roles and learned projections**, not the entire attention algorithm:

1. Q, K and V are three learned transformations of the representation entering the attention sublayer.
2. In self-attention, the three projections share the current input stream:
   `Q = X W_Q`, `K = X W_K`, `V = X W_V`.
3. Q and K determine compatibility scores and, after scaling/masking/softmax, the attention weights. V supplies the vectors combined using those weights.
4. Q and K have width `d_k`; V may have a different width `d_v`.
5. The page distinguishes the current hidden representation from raw token embeddings, and notes that positional information can be injected at the input or within attention (e.g. RoPE on Q/K).
6. It distinguishes self-attention from cross-attention.
7. It treats coreference and lexical polysemy as distinct contextual phenomena and explicitly says the examples are not measurements of attention or proof that a particular head performs a linguistic task.
8. It rejects interpreting a dot product as cosine similarity in general, attention as hard nearest-neighbour retrieval, or attention weights as universal semantic relevance.

The adjacent scaled-dot-product-attention page owns the complete computation:

`S = QK^T` → scaling by `sqrt(d_k)` → optional additive mask → row-wise softmax → `O = AV`.

It includes a worked one-query/two-key example, explicit shapes, mask semantics, and a warning that attention weights are not causal explanations. The score-scaling rationale is delegated to a separate deep dive; causal masking has its own lesson.

The exercise hub currently provides:
- a hand calculation of weighted aggregation and a value-swap counterfactual;
- a NumPy projection exercise with `Q=(3,2)`, `K=(3,2)`, `V=(3,3)`;
- a prompt to explain why changing `W_V` does not alter Q/K-derived scores.

This division of responsibility is a strength: the Q/K/V page introduces the objects, the attention page derives their interaction, and the exercise hub tests application.

## 3. Comparison with the three scanned introductory sources

The comparison below uses the source-specific reviews and structured extractions in this repository. It does not infer the contents of uninspected images, assignments or linked lessons.

| Resource | Strongest contribution | Limits observed in the scan | LLM Lab's relative position |
|---|---|---|---|
| Nishanthan K, [DEV Community](https://dev.to/nishanthan-k/how-query-key-and-value-qkv-work-in-transformers-199a) / [author's Medium mirror](https://nishanthan-k.medium.com/how-query-key-and-value-qkv-work-in-transformers-1274bfa14ea8) | Compact functional narrative; visual explanation; bank ambiguity and pronoun examples; warnings against semantic-similarity and winner-take-all readings | Original illustration bytes and reuse rights unresolved; year in visible DEV header unverified; no substantial worked tensor exercise observed in the scanned article | LLM Lab is more formal, explicit about scope and misconceptions, and provides a linked mathematical continuation and practice. DEV remains a useful alternative short explanation and potential visual reference. |
| Neha KK, [Medium](https://medium.com/@nkk18072004/understanding-queries-keys-and-values-in-transformers-149ed07c9f8b) | Clear “why three projections?” motivation; separates matching from payload; useful pronoun/coreference scenario | Four image placements are visible but image bytes and rights remain unresolved; some broad efficiency/parallelism wording needs qualification; no measured model evidence for the linguistic example | LLM Lab preserves the design rationale but states it more carefully, distinguishes jointly optimized parameters from independently parameterized projections, and avoids claiming measured coreference behavior. |
| Codefinity, [Q/K/V lesson](https://codefinity.com/courses/v2/e7ee0772-6b82-4a1c-96ba-69b85ddee608/7ce26687-f7a7-4728-be33-7014c6c7b707/a5ac1dbf-dbec-4dd1-a8d6-f3d83cbb905b) | Geometric Q/K perspective; bank/river polysemy example; one multiple-choice item with role-confusion distractors | Two resolved SVG URLs are interface icons, not pedagogical figures; their bytes were not inspected; full interactive course and assignments were not scanned | LLM Lab turns the geometric lens into an explicit dot-product identity with norm dependence, connects it to the full calculation, and retains the quiz pattern without duplicating a quiz. |
| Michael Brenndoerfer, [Q/K/V chapter](https://mbrenndoerfer.com/writing/query-key-value-attention-mechanism) | Assumption-explicit variance derivation; shape walkthrough; complete toy trace; routing/payload distinction; message-passing and convex-hull interpretations | Random projections are not learned behavior; variance result depends on independence/variance assumptions; figures and quiz interactions not inspected; convex-hull claim needs pre-projection/accessibility limits | The derivation and toy trace remain references; routing/payload, message passing and convex-hull interpretations are integrated as bounded optional notes in existing bilingual pages. |
| **LLM Lab (this project)** | Integrated learning route, explicit projection and tensor notation, boundaries between concepts, bilingual pages, worked numerical calculation, exercises, implementation route and source traceability | More material than a short tutorial; no learner-pilot evidence; rendered accessibility and media review incomplete; no stable scholarly release/citation record yet | Strongest overall as a structured learning resource, provided its scope is stated as an introductory treatment of the standard formulation rather than an exhaustive account of all attention variants. |

### What should not be copied from the sources

- Do not stack multiple near-identical database/search analogies. Keep one canonical intuition and retain alternatives in the source dossier.
- Do not add another complete score → softmax → aggregation derivation to the Q/K/V page.
- Do not copy or redraw third-party images while their asset identity and reuse terms remain unresolved.
- Do not turn illustrative language examples into claims about attention-head interpretability.
- Do not add a duplicate multiple-choice quiz without evidence that the existing open-response checks fail to diagnose a real misconception.

The project's [pedagogical coverage matrix](../source-syntheses/qkv-pedagogical-coverage-matrix-2026-11.md), [complementary-perspectives synthesis](../source-syntheses/qkv-complementary-perspectives-2026-11.md), and [learning-graph comparison](qkv-learning-graph-comparison-2026-11.md) preserve the more detailed source-to-project mapping.

## 4. Comparison with primary and current technical references

Introductory tutorials are pedagogical material, not independent technical validation. The canonical explanation should be anchored in primary and implementation sources.

| Reference | What it establishes or contributes | Consequence for LLM Lab |
|---|---|---|
| Vaswani et al. (2017), [Attention Is All You Need](https://arxiv.org/abs/1706.03762) | Defines attention as a query and key-value set mapped to an output; the output is a weighted sum of values, with weights derived from query-key compatibility. Gives the scaled dot-product and multi-head formulations. | Primary anchor for the standard baseline. The Q/K/V page should cite it directly, not rely only on tutorial references. |
| Ainslie et al. (2023), [GQA](https://arxiv.org/abs/2305.13245) | Describes grouped-query attention: multiple query heads share a smaller number of key/value heads, reducing KV-cache size while trading off speed and quality. | Prevents the phrase “three projections” from being read as a universal head-count or architecture invariant. |
| Kayyam et al. (2026), [Do Transformers Need Three Projections?](https://proceedings.mlr.press/v306/kayyam26a.html) | Studies projection sharing constraints, including shared key/value projections, and reports empirical quality/cache trade-offs across synthetic, vision and language-modeling experiments. | A current research extension that makes projection separability a design question rather than an immutable law. Keep it as an advanced reference; do not turn its results into a beginner-level universal claim. |
| Hugging Face, [How caching works](https://huggingface.co/docs/transformers/main/cache_explanation) | Documents how past K/V tensors are stored and concatenated with current K/V during autoregressive inference, with cache state managed per layer. | Supports a future KV-cache lesson and implementation walkthrough. It is an implementation reference, not a replacement for the mathematical derivation. |

**Important distinction:** GQA/MQA primarily change the number and sharing pattern of key/value heads relative to query heads. Projection tying (for example, sharing key/value projection parameters) is a related but distinct design choice. The Q/K/V page should not conflate these.

The current Q/K/V lesson is correct as a standard-form introduction, but its title/subtitle could otherwise sound universal. A collapsed bilingual scope note has therefore been added to identify the standard formulation and point readers to GQA and projection-sharing research without expanding the core lesson.

## 5. Findings and bounded corrections

### 5.1 Parameterization is separate; optimization is joint

The previous wording said the model learns the matching function “independently” from the payload function, immediately after stating that the three matrices are learned jointly. That could suggest independent optimization or statistical independence.

**Correction:** the projections are separately parameterized and represent distinct learned spaces, while their parameters are optimized jointly. This is more precise and preserves the intended intuition.

### 5.2 Projection count and head sharing are architecture-dependent

The introductory page describes the standard separate-Q/K/V formulation. It should not imply that all Transformer variants have the same number of query and KV heads or wholly independent projection parameters.

**Correction:** add a collapsed note in both languages. Keep GQA/MQA and projection tying as advanced variants; do not overload the main explanatory flow.

### 5.3 Exercise wording should not imply an unconditional change

The exercise answer previously said changing `W_V` “changes the aggregated vectors.” This is the generic expectation, but special inputs or parameter changes can leave a particular output unchanged.

**Correction:** say changing `W_V` *can* change `V` and the aggregated output, while scores and weights remain unchanged as long as Q and K are held fixed.

### 5.4 Visual and bilingual source checks

The project-owned Q/K/V SVGs:
- use matching 1200×660 dimensions and a consistent information flow;
- include SVG `title` and `desc`, `role="img"`, and `aria-labelledby`;
- explicitly state that the diagram is simplified for one position and omits vector/numerical values;
- use the revised “content to aggregate” wording in the V branch;
- provide bilingual text and page-level alt text.

The two diagrams are explanatory role diagrams, not a numerical attention visualization. Their source is inspectable, but browser rendering, responsive scaling, contrast under the actual site theme and screen-reader behavior were not verified in this audit.

### 5.5 Exercise maturity

The current exercise set is a good starting point, but it is not yet a complete assessment of Q/K/V mastery. The most defensible next step is a small diagnostic set in the existing Attention exercise collection, not a new Q/K/V page:
- a non-unit-norm dot-product-versus-cosine counterexample;
- a softmax weighted-mixture-versus-argmax discrimination item;
- a projection intervention that changes `W_V` while holding `X, W_Q, W_K` fixed.

The first candidate is already owned by [issue #80](https://github.com/JM-Brun/llm-lab/issues/80). Do not duplicate it elsewhere. The second is partly demonstrated by the existing numerical example; add an assessment item only if it tests a distinct misconception. The third is already partially addressed by the current NumPy exercise and should be strengthened only if a learner pilot reveals a gap.

## 6. Can LLM Lab be cited as a Q/K/V source?

**Yes—as a pedagogical synthesis and learning resource for the standard Q/K/V formulation.** It should not be cited as the origin of the mechanism, as primary experimental evidence, or as an exhaustive reference for every attention architecture.

A suitable description is:

> *LLM Lab — Queries, Keys, and Values (Q, K, V): a bilingual, source-traceable tutorial on the standard Transformer self-attention projections, their mathematical roles, tensor shapes, and relation to scaled dot-product attention.*

For stronger citability, add the following publication hygiene:
1. Create a tagged release or immutable versioned snapshot for the Q/K/V lesson and its linked attention lesson.
2. Provide a citation block (authors/maintainer, project title, version, date, canonical URL, repository URL and licence).
3. Ensure the repository/site licence clearly covers original lesson text, diagrams and code; keep third-party references link-only unless separately licensed.
4. Cite primary papers for technical definitions and cite tutorial sources only for their distinctive pedagogical contributions.
5. Preserve an explicit scope statement: standard formulation, not all variants.
6. Add a small learner evaluation: task, participant context, pre/post questions, rubric, observed misconceptions and limitations. Do not claim learning gains before this exists.
7. Complete browser-based desktop/mobile and accessibility review before describing the site as fully validated.

The project's distinctive contribution is the **auditable synthesis and learning design**, not a novel Q/K/V theory. That is a legitimate and useful kind of public source.

## 7. Remaining validation gates

| Gate | Status |
|---|---|
| EN/FR source-content parity | Reviewed in source |
| Projection equations, dimensions and numerical arithmetic | Reviewed |
| Comparison with four scanned tutorials and their extracted claims | Reviewed |
| Primary/advanced technical reference comparison | Reviewed at the cited paper/documentation level |
| Quarto site build | Passed on audited main revision |
| CI | Passed on audited main revision |
| Publish workflow | Passed on audited main revision |
| Actual published-page browser rendering | Not verified through available inspection interface |
| Desktop/mobile responsive review | Not verified |
| Keyboard/focus and accessibility-tree review | Not verified |
| Third-party article figure bytes and rights | Unresolved; no reuse approved |
| Learner pilot / outcome evidence | Not performed |
| Versioned citation release | Not yet created |

## 8. Evidence and related project records

- [Q/K/V source collection](qkv-source-collection.md)
- [Q/K/V pedagogical coverage matrix](../source-syntheses/qkv-pedagogical-coverage-matrix-2026-11.md)
- [Complementary perspectives synthesis](../source-syntheses/qkv-complementary-perspectives-2026-11.md)
- [Learning-impact baseline](../source-syntheses/qkv-learning-impact-baseline-2026-11.md)
- [Source learning graph and route comparison](qkv-learning-graph-comparison-2026-11.md)
- [Visual asset audit](qkv-visual-asset-audit-2026-11-05.md)
- [Neha KK source review](qkv-neha-kk-medium-2026-11.md)
- [Nishanthan K source review](qkv-nishanthan-devto-2026-11.md)
- [Codefinity source review](qkv-codefinity-course-2026-11.md)
- [Brenndoerfer source review](qkv-mbrenndoerfer-2026-11.md)
- [Four-source comparison and canonical-page audit](../source-syntheses/qkv-four-source-comparison-2026-11.md)

**Audit boundary:** this document records a source-content and repository-level audit. It does not substitute for rendered-site, accessibility, user-study or legal/licensing review.


## 10. Post-audit implementation and publication status — 2026-11-05

The audit above describes the pre-audit baseline at commit `79b91333a41bb74aa10a29f9e9a201eeb87a35a7`. The following changes were merged after that baseline; they should not be mistaken for evidence that every publication-readiness item is complete.

| Follow-up | Result | Evidence / boundary |
|---|---|---|
| Comparative self-audit and bounded bilingual corrections | Merged in [PR #486](https://github.com/JM-Brun/llm-lab/pull/486), merge commit `0ccd87668f72a77174abf9254b58d3eaefe5426e` | CI, Quarto and publish workflows passed for the merged revision |
| Attention regression fixtures | Merged in [PR #489](https://github.com/JM-Brun/llm-lab/pull/489), merge commit `bd1f9ac3045ae6f6ad70916cbdf15f83828c33f4` | Python CI and Quarto passed; deterministic fixtures now cover weighted aggregation, unequal key/value widths, one-position attention, masked-key normalization, dot-product/cosine ranking and a wrong-axis softmax failure |
| Independent learner pilot protocol | Extended in [PR #490](https://github.com/JM-Brun/llm-lab/pull/490), merge commit `c3f980b21b5a9f56a7a226f409636eff608843e7` | Adds bilingual pre-reading and post-reading Q/K/V probes, an optional geometry transfer item and a lightweight rubric; protocol only, not executed |
| Source comparison and provenance | Continued in [#483](https://github.com/JM-Brun/llm-lab/issues/483) | Fresh page-text inspection confirms figure placements and course quiz text; embedded source image bytes and reuse rights remain unresolved |
| Code-to-page attention contract | Merged in [PR #493](https://github.com/JM-Brun/llm-lab/pull/493) | CI and Quarto passed; the bilingual lesson now distinguishes hard masks, finite additive biases and fully masked rows, and states the single-head/unbatched NumPy API boundary |
| Reusable source-to-knowledge method | Merged in [PR #494](https://github.com/JM-Brun/llm-lab/pull/494); method issue #492 closed | CI and Quarto passed; includes a worked incremental Codefinity addition case; second transfer test is tracked in [#496](https://github.com/JM-Brun/llm-lab/issues/496) |
| Codefinity assessment inventory | Corrected in [PR #495](https://github.com/JM-Brun/llm-lab/pull/495) | Three visible four-option questions are now represented as separate extraction items; source review, coverage matrix and learning-impact decisions are reconciled; answer feedback remains untested |
| Browser/accessibility validation | Still open in [#483](https://github.com/JM-Brun/llm-lab/issues/483) | The published EN/FR URLs remain inaccessible to the available page reader. No graphical desktop/mobile, keyboard, focus, disclosure, equation or screen-reader review is claimed |
| Citation/release | Still open in [#488](https://github.com/JM-Brun/llm-lab/issues/488) | A citation draft exists, but no immutable tag/release or DOI has been created. Wait for rendered/accessibility evidence before release |
| Broader attention implementation | Still gated by [#82](https://github.com/JM-Brun/llm-lab/issues/82) | The current reference implementation is unbatched, single-head NumPy; this work does not add a PyTorch duplicate, multi-head API or gradient validation |

### Current interpretation

LLM Lab is a useful public educational source for the standard Q/K/V formulation because it combines a bilingual conceptual lesson, mathematical continuation, implementation reference, tests, source comparison and explicit epistemic limits. The new tests improve implementation confidence for the cases they exercise; they do **not** establish correctness for all shapes, numerical regimes, architectures or optimized kernels, and they do not establish learner mastery.

The pilot protocol improves the ability to collect formative evidence but remains unrun. The source-media audit remains partial. A stable scholarly citation should identify an immutable release after the browser/accessibility review, not a moving branch or an unverified DOI.


## 11. Fourth-source integration reconciliation — 2026-11-05

The original audit's comparative baseline covered three tutorials. Brenndoerfer was subsequently added as a fourth source. The canonical bilingual pages were enriched in bounded ways: routing versus payload on the Q/K/V pages, and message passing plus the convex-hull property on the scaled-attention pages. The convex-hull statement is restricted to normalized nonnegative weights over accessible values, before output projection or residual/MLP transformations. The variance derivation and end-to-end toy trace remain reference-only because the project already owns the scaling deep dive and numerical workbench.

This later source comparison does not establish learner effectiveness. The current evidence remains content inspection, implementation tests and an unrun pilot protocol. See the [four-source comparison and canonical-page audit](../source-syntheses/qkv-four-source-comparison-2026-11.md) for the item-level mapping and remaining validation boundaries.
