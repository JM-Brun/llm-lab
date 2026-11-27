# Source review — Damien Benveniste, “How LLMs Encode Token Position”

**Canonical source:** [The AiEdge Newsletter](https://newsletter.theaiedge.io/p/how-llms-encode-token-position)  
**Alternate URL for the same post:** [Substack inbox post 225953856](https://substack.com/inbox/post/225953856)  
**Structured extraction:** [aiedge-how-llms-encode-token-position-2026.yml](../../data/extractions/aiedge-how-llms-encode-token-position-2026.yml)

**Identity:** one article, one source ID. The user confirmed that the Substack inbox URL and the AiEdge publication URL point to the same post. The inbox URL is recorded as an alias; it is not a second source.

**Inspection boundary:** indexed search snapshot inspected on 27 November 2026. It exposed the title, author, publication date, subtitle, introductory framing, four-method outline and distinction between positional rules and causal visibility. Direct retrieval of the full article returned a cache miss. The full body, equations, diagrams, figures, examples, code, comments and linked references were not inspected. Rights remain unknown; reuse remains link-only.

## 1. Editorial decision

Keep this source in the existing `positional-encoding` collection as a **supplementary short-form cross-check**. It does not justify a new canonical concept, page, computation node, learning-route stage, diagram or exercise.

The visible framing—following learned vectors, sinusoids, RoPE and ALiBi from token indices to attention scores—is useful because it asks learners to locate each mechanism in the computation. However, that organizing principle is already central to the existing LLM Lab lesson and synthesis, and it is developed in greater technical depth by the Raschka article and the primary-source extractions.

The conclusion is intentionally limited: because the full AiEdge article was inaccessible, this review assesses only the indexed outline and cannot judge its complete teaching sequence, diagrams or worked examples.

## 2. Meta-comparison with the existing corpus

| Existing source | What it establishes in the collection | Increment beyond the accessible AiEdge outline |
|---|---|---|
| Vaswani et al. (2017) | Primary sinusoidal equations, frequency schedule, wavelength and fixed-offset linear-transform property | Mathematical authority and derivation; not merely a method label |
| Jay Alammar / The Illustrated Transformer | Visual intuition for positional matrices and multi-frequency patterns | Visual reference for explaining absolute position |
| Harvard NLP / The Annotated Transformer | Positional-encoding equations mapped to a PyTorch implementation and finite precomputed buffer | Implementation-level grounding |
| Stanford EE269 | Signal-processing interpretation of angular frequencies, wavelengths and logarithmic spacing | Mathematical intuition for the frequency bank |
| Jay Joshi (2026) | Numerical/geometric explanation, embedding lookup and permutation-equivariance motivation | Alternative hand-checkable pedagogical explanation; its scan remains partial |
| Shaw et al. (2018) | Learned relative-position vectors contribute separately to key compatibility and value aggregation | A distinct relative mechanism absent from the accessible four-family outline |
| Raffel et al. / T5 (2020) | Learned scalar relative-position values selected by logarithmic buckets and added before softmax | Distinguishes bucketed learned score bias from other relative methods |
| Press et al. / ALiBi (2021) | Fixed, head-specific linear distance penalties added to attention scores, with protocol-bounded extrapolation results | Primary derivation and experimental evidence behind one of the four named methods |
| Su et al. / RoFormer (2021) | Pairwise Q/K rotations, relative-offset identity, orthogonality and frequency-schedule derivation | Mathematical foundation behind the RoPE label |
| Sebastian Raschka (2026) | Progression from absolute position to RoPE geometry, PyTorch/Qwen3 implementation, partial RoPE, NoPE, relative bias and hybrid layers | Most substantial pedagogical overlap; broader architecture and implementation coverage |
| Khan et al. (2026) | Experimental study of partial-RoPE fractions and positional-table memory | Focused experimental qualification not present in the accessible outline |

### 2.1 What AiEdge adds

Only three contributions can be supported from the indexed material:

1. **A concise organizing lens:** compare positional methods by where they enter the computation, from token indices to attention scores.
2. **An explicit contrast:** positional information and causal visibility answer different questions.
3. **A qualification:** positional distance is not the sole determinant of attention or successful retrieval; content and available positions also matter.

These are useful as a compact orientation and a reminder of common confusions. They are not new mechanisms or independently established results.

### 2.2 What the existing corpus already does better

- The bilingual core lesson already distinguishes absolute and relative information, explains the Shaw/T5/ALiBi/RoPE insertion points, separates causal visibility and qualifies NoPE.
- Its original project diagram already compares input addition, Q/K rotation and score-level bias. Creating a second diagram from the AiEdge outline would duplicate an existing asset.
- Raschka's extraction is substantially deeper: sections 1–7, equations, code snippets, 38 figure captions/context, Qwen3 static-code inspection, partial RoPE, NoPE and hybrid-layer discussion.
- Primary-source records prevent the four-family summary from flattening distinct mechanisms: Shaw changes both key compatibility and value aggregation; T5 and ALiBi share a score-level insertion point but use different parameterizations; RoPE acts on projected Q/K and does not rotate V.
- The collection already separates the ability to compute a positional signal from evidence that a trained model generalizes to longer contexts.

### 2.3 Coverage gap assessment

| Candidate gap | Is it genuinely missing? | Decision |
|---|---|---|
| A map from method to insertion point | No; present in the core lesson and project SVG | No change |
| Position versus causal visibility | No; explicitly taught in FR/EN and in the NoPE comparison | No change |
| Token-index-to-score narrative | The accessible article suggests this framing, but the complete sequence cannot be assessed | Keep as source-review note; no new route |
| Shaw relative key/value paths | No; covered by primary extraction and core comparison | No change |
| T5 bucketed score bias | No; covered by primary extraction and core comparison | No change |
| ALiBi head-specific linear slopes | No; covered by primary extraction and core comparison | No change |
| RoPE derivation and implementation | No; covered by Su and Raschka plus bilingual deep dives | No change |
| Partial RoPE, NoPE and hybrid architectures | No; covered by Raschka and Khan | No change |
| New experiment or benchmark | Not evidenced in the accessible snapshot | Do not infer one |

## 3. Source-route crosswalk (partial evidence only)

The full article was not accessible, so its section-by-section teaching route cannot be reconstructed. The available indexed material supports only this limited route sketch:

| Learning function | AiEdge evidence available | LLM Lab comparison | Decision |
|---|---|---|---|
| Orientation | Frames the question as encoding token position | The existing core lesson already motivates why order must be represented | No new introduction |
| Method comparison | Names learned absolute vectors, sinusoids, RoPE and ALiBi | The bilingual lesson and existing diagram compare the mechanisms by computational insertion point | Retain as a concise cross-check |
| Computational placement | The indexed framing runs from token indices toward attention scores | The canonical lesson distinguishes input addition, Q/K rotation and score-level bias; the synthesis preserves Shaw's separate key/value path | No new route stage or diagram |
| Qualification | Separates positional information from causal visibility | The lesson already distinguishes positional mechanisms from the causal mask and discusses NoPE | No new section |
| Practice / implementation / conclusion | Not available in the inspected snapshot | Cannot compare these stages or claim that the source lacks them | Keep unknown; do not infer |

This is not a full route comparison. In particular, the source's ordering, prerequisites, worked examples, exercises, implementation sequence and conclusion remain unverified. The decision not to change the LLM Lab route is based on the overlap of the *visible* framing with existing material, not on a claim that the complete article has been audited.

## 4. Placement in the canonical computational model

The article's visible insertion-point framing is consistent with the project's computational spine, but the mechanisms must not be collapsed into a single pre-block operation:

- **Absolute learned/sinusoidal position:** modifies the input representation before the Transformer blocks.
- **RoPE:** modifies projected Q and K inside attention, before their dot product; V is not rotated.
- **T5 / ALiBi:** modify attention scores before softmax.
- **Shaw:** contributes relative representations to both compatibility and value aggregation.
- **Causal mask:** constrains visibility; it is not itself an explicit positional coordinate.
- **NoPE:** omits explicit positional transformation while retaining causal structure; this is not equivalent to explicit relative-distance encoding.

Thus the source is relevant to the forward-pass subgraph (input embeddings, block-local attention, scores and masking), but it does not motivate a new computational node or relation. The canonical concept graph, computational graph and learning routes remain unchanged.

## 5. Disposition and maintenance

- **Source identity:** one record, with the AiEdge URL canonical and the Substack inbox URL recorded as an alias.
- **Collection:** existing `positional-encoding`; no new collection.
- **Extraction:** retain atomic claims with their exact inspection boundary and evidence confidence.
- **Core lesson and Practice:** no edits; the relevant concepts, diagram and exercises are already present.
- **Deep dives:** no edits; Su, Shaw, T5, ALiBi, Raschka and Khan already supply the detailed evidence and derivations.
- **Rights:** no text, code or figures copied; permissions remain unknown.

## 6. Remaining gate

If the complete AiEdge article becomes directly accessible, inspect its full section sequence, equations, diagrams, examples and outbound references. Reopen this decision only if it reveals a distinct explanation, a missing mechanism or evidence not already represented. Until then, keep the source partially scanned and avoid promoting the indexed outline into a full-text audit.
