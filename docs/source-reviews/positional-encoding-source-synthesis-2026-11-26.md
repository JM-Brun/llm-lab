# Positional encoding: source compilation and editorial model

**Reviewed:** 2026-11-26  
**Collection:** positional-encoding  
**Status:** source corpus consolidated; core FR/EN lesson, synthesis and Practice companions updated; deep dives retained as the canonical destinations for derivations. AiEdge is recorded as a supplementary partial scan after meta-comparison; its two supplied URLs resolve to one source identity.

## 1. Editorial question

How can a Transformer use the order of a sequence when token embeddings initially identify token content but do not, by themselves, identify where an occurrence appears?

The answer is not one universal positional vector. The source corpus describes several mechanisms that inject positional information at different places in the computation, plus architectures that omit an explicit positional transformation and rely partly on causal structure.

The central distinctions are:

1. **Token identity / content:** the embedding lookup selects a vector for a token ID.
2. **Absolute position:** an input representation is associated with a sequence index.
3. **Relative position:** an attention computation receives information about the displacement between a query and a key.
4. **Causal visibility:** a query is restricted to an allowed prefix. This is an access constraint, not an explicit coordinate system.
5. **Implicit order in NoPE:** nested causal prefixes can expose structural order without an explicit position transform. This is not equivalent to a learned absolute coordinate or an explicit pairwise distance.

## 2. Ingested source inventory

The collection deliberately distinguishes primary technical sources from pedagogical and implementation references.

| Source | Evidence inspected | Extracted contribution | Use in LLM Lab |
|---|---|---|---|
| Vaswani et al. (2017), [Attention Is All You Need](https://arxiv.org/abs/1706.03762), §3.5 | Original sinusoidal equations, frequency schedule, wavelength discussion and fixed-offset motivation | Fixed absolute vectors added to input embeddings; paired sine/cosine coordinates; a fixed offset can be represented by a pair-specific linear transformation | Primary authority for the sinusoidal deep dive; not evidence that long-context generalization is guaranteed |
| Jay Alammar, [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) | Positional-encoding passage and its clarification | Visual intuition for the position-by-dimension matrix and multi-frequency pattern | Visual-design reference only; no image copied |
| Harvard NLP, [The Annotated Transformer](https://nlp.seas.harvard.edu/annotated-transformer/) | Positional-encoding explanation and PyTorch implementation | Maps the equation to alternating dimensions, a finite precomputed buffer and input addition | Independent implementation reference; no code copied |
| Stanford EE269, [Transformers for Signal Prediction](https://web.stanford.edu/class/ee269/Lecture_Transformers.pdf) | Indexed lecture passage on angular frequency, wavelength and logarithmic spacing | Signal-processing interpretation of the frequency bank | Secondary mathematical explanation; inspected passage only |
| Jay Joshi (2026), [The Mathematics of a Transformer… Part 1](https://medium.com/@jayjj6272/the-mathematics-of-a-transformer-explained-with-numbers-you-can-check-by-hand-with-geometric-96b5873c95be) | Indexed article snapshot: notation, embedding lookup, permutation-equivariance statement, sinusoidal equations and figure/code descriptions | Connects content-only attention symmetry to the need for order information; interprets sine/cosine pairs geometrically | Complementary explanation already integrated into the bilingual core lesson; live article, figures and code cells were not directly inspectable |
| Shaw et al. (2018), [Self-Attention with Relative Position Representations](https://aclanthology.org/N18-2074/) | Full five-page NAACL-HLT paper, §§1–4 and equations (3)–(5) | Learned edge representations for relative offsets enter both key compatibility and value aggregation; offsets are clipped to a configured range | Primary source for the relative-representation family; empirical results remain bounded to the WMT 2014 setups |
| Raffel et al. (2020), [T5](https://arxiv.org/abs/1910.10683), §2.1 | Primary paper section defining the T5 positional mechanism | A learned scalar indexed by a logarithmically bucketed query–key offset is added to each pre-softmax attention logit; parameters are shared across layers and distinct per head | Primary source for bucketed relative score bias; the 32 buckets and 128-token cap are T5 configuration choices |
| Press et al. (2022), [ALiBi](https://arxiv.org/abs/2108.12409) | Primary paper abstract and §§2–4 | A fixed, head-specific linear distance penalty is added to attention scores before softmax; no positional vector is added at the input | Primary source for ALiBi and its reported length-extrapolation experiments; results are protocol-specific |
| Su et al. (2021), [RoFormer](https://arxiv.org/abs/2104.09864) | RoPE formulation, derivation and relevant experiments; see the existing source review | Position-dependent rotations of paired query/key coordinates produce a relative-offset contribution to their dot product | Primary source for the RoPE deep dive |
| Damien Benveniste (2026), [How LLMs Encode Token Position](https://newsletter.theaiedge.io/p/how-llms-encode-token-position) ([same post: Substack inbox alias](https://substack.com/inbox/post/225953856)) | One indexed snapshot: title, author, subtitle, introduction, four-method outline and causal-visibility distinction; full body and figures unavailable | Short-form insertion-point framing from token indices to scores; explicit position-versus-mask contrast | Supplementary cross-check only; no new mechanism, page, concept, diagram or route justified by available evidence |

| Sebastian Raschka (2026), [Understanding Positional Embeddings in Modern LLMs](https://magazine.sebastianraschka.com/p/understanding-positional-embeddings) | Full article text, equations, code snippets and 38 figure captions/context; linked Qwen3 notebook statically inspected | Modern architecture comparison: partial RoPE, NoPE, hybrid layers, relative bias, frequency configuration and implementation conventions | Cross-check and implementation comparison; figures were not individually inspected as image files and the notebook was not executed |
| Khan et al. (2026), [Fractional Rotation, Full Potential?](https://arxiv.org/abs/2603.11611) | arXiv v2: abstract, setup, principal partial-RoPE analysis, conclusion and Appendix C | Experimental study of partial-RoPE fractions and the size of precomputed sine/cosine tables | Qualifies the partial-RoPE discussion; findings are bounded to the studied model sizes, data and training protocol |

### Evidence boundaries

- The source catalogue records each source's scan scope, version, licence status and reuse boundary. Collection membership is explicit; it is not inferred from tags or links.
- No third-party figure, paragraph or code block is copied into the site. Existing LLM Lab diagrams are original project assets.
- The Jay Joshi scan remains partial because the live Medium page, original figure bytes and full code cells were unavailable.
- Raschka's 38 figures received a caption-and-context audit, not a pixel-level inspection. The linked Qwen3 notebook was not executed.
- No independent training run or long-context benchmark was performed by this source-ingestion pass.

### 2.1 Supplementary short-form cross-check: AiEdge (2026)

Damien Benveniste's *How LLMs Encode Token Position* is registered as one source. The AiEdge publication URL is canonical; the Substack inbox URL with post ID 225953856 is an alias for the same post, as confirmed by the user. It is not a second source record.

The indexed snapshot exposes a framing from token indices to attention scores and names learned vectors, sinusoids, RoPE and ALiBi. It also distinguishes positional information from causal visibility. Direct full-text retrieval returned a cache miss, so this is a partial scan: no equations, full section sequence, examples, diagrams, code or outbound references were inspected.

**Meta-review:** this is a useful compact orientation, but the collection already covers its visible contribution. Raschka offers a deeper explanatory and implementation progression, while Vaswani, Shaw, T5, Press/ALiBi and Su/RoFormer supply the primary technical foundations. The core bilingual lesson already has an insertion-point comparison diagram and an explicit mask-versus-position distinction. No new concept, page, route stage, computational node, diagram or exercise is justified.

The accessible four-method outline is also narrower than the collection: it does not expose Shaw's relative key/value representations, T5's bucketed score bias, NoPE, partial RoPE or hybrid layers. Do not infer that the full article omits these topics until its body is inspected.

## 3. Cross-source synthesis

### 3.1 Absolute input encodings

**Learned absolute embeddings** associate a learned vector with each supported position. **Sinusoidal absolute encodings** compute a fixed vector from a deterministic bank of sine/cosine frequencies.

For the original Transformer, the positional vector is added to the token embedding at the input:

\[
X_0 = E[\text{token IDs}] + PE.
\]

The sinusoidal formula and its frequency/geometry properties belong in the dedicated *Sinusoidal positional encodings* deep dive. Its fixed-offset identity is a property of the positional vectors; it is not a theorem that the complete Transformer is translation-invariant or that a trained model generalizes to arbitrary context lengths.

### 3.2 Relative representations and relative score biases

The word *relative* covers more than one implementation:

- **Shaw et al.:** learned vectors label the relation between query and key positions. The key-side representation contributes to the compatibility score; the value-side representation contributes to the weighted aggregation. Relative distances are clipped to a configured range.
- **T5:** reduces the relative-position contribution to a learned scalar added to the pre-softmax attention logit. Relative offsets are mapped to logarithmically widening buckets. In the cited T5 configuration, there are 32 buckets and distances beyond 128 share a bucket.
- **ALiBi:** adds a fixed, non-learned, head-specific linear penalty to the query–key score. The slope values are set before training. The method does not add a positional vector to the input embeddings.

T5 and ALiBi therefore share a **score-level insertion point**, but not the same parameterization: T5 learns bucketed values; ALiBi uses fixed linear slopes. Shaw's original method is richer than either scalar-bias formulation because relative vectors enter both compatibility and value aggregation.

### 3.3 Rotary position embeddings

RoPE applies position-dependent rotations to paired coordinates of projected Q and K, before their dot product. For fixed unrotated content vectors, the pairwise score contribution depends on the relative offset. The complete attention score still depends on content-derived Q/K; it is not a function of distance alone.

RoPE is therefore a relative-position mechanism with a distinctive **Q/K insertion point**. It is not a third top-level family disjoint from relative methods, and it does not rotate V.

The existing RoPE deep dive remains responsible for:
- the pairwise rotation and relative-offset derivation;
- inverse-frequency schedules and position IDs;
- interleaved versus split-half feature pairing;
- cosine/sine table construction and broadcasting;
- partial RoPE, KV-cache distinctions and implementation checks.

### 3.4 Causal visibility and NoPE

A causal mask specifies which keys each query may access. It does not directly assign an absolute coordinate or a learned relative-distance value.

In a NoPE architecture, explicit positional transformations are omitted while causal masking remains. The nested prefixes visible at successive positions can provide an implicit ordering signal. This does not make NoPE identical to an explicit positional encoding, nor does it guarantee reliable extrapolation. The behaviour depends on architecture, training and task.

### 3.5 Computability is not generalization

A sinusoidal function can be evaluated at an index beyond the training range. That mathematical fact is different from a trained model performing well at that sequence length. Press et al. provide empirical evidence for ALiBi under their own model, data and evaluation conditions; those results must not be promoted to a universal ranking of positional mechanisms.

Likewise, the partial-RoPE study's reported memory reduction concerns the precomputed RoPE cosine/sine tables, not the full KV cache. Its convergence and task findings are specific to the studied configurations.

## 4. Source-derived conceptual model

| Question | Mechanism | Where it acts | What it contributes |
|---|---|---|---|
| Which absolute index is this? | Learned or sinusoidal absolute encoding | Input representation | A position-specific vector |
| How are two positions related? | Shaw-style relative representations | Key compatibility and value aggregation | Learned pairwise relation vectors |
| How should a distance affect attention? | T5 relative bias | Pre-softmax attention score | Learned scalar per relative-distance bucket |
| How should recency affect attention? | ALiBi | Pre-softmax attention score | Fixed head-specific linear distance penalty |
| How does position affect Q/K phase? | RoPE | Projected Q and K, before dot product | A relative-offset contribution to the score |
| What if explicit positional transforms are omitted? | NoPE with causal masking | Structural visibility pattern | Potential implicit order signal, not explicit coordinates |
| Which positions are available? | Causal mask | Attention visibility | A prefix/access constraint |

The concepts are connected, but their operations are not interchangeable. The canonical concept graph and computational graph remain unchanged: this synthesis clarifies existing concepts and mechanisms rather than creating a new computational node.

## 5. Page model and editorial ownership

| Resource | Reader question | Keep here | Keep out |
|---|---|---|---|
| Core lesson positional-encoding (FR/EN) | Why does order matter, and where can it enter? | Motivation, absolute/relative distinction, injection-point comparison, causal-mask distinction, concise NoPE caveat | Full trigonometric derivations, implementation details, architecture catalogue |
| Synthesis revision-positional-encoding (FR/EN) | What distinctions must I recall? | Content vs position, absolute addition, RoPE Q/K, score-level relative bias, NoPE caveat | New explanations and long derivations |
| Practice exercises/positional-encoding (FR/EN) | Can I retrieve and apply the distinctions? | Five short recall cards, self-check questions and transfer exercise | Duplicate theory sections |
| Deep dive sinusoidal-positional-encoding (FR/EN) | How is the original sinusoidal signal constructed? | Formula, frequency bank, wavelength, fixed-offset transform, positional-only similarity, implementation and extrapolation limits | RoPE derivation |
| Deep dive rope (FR/EN) | How do rotations of Q/K create relative-position effects? | Pair rotations, Q/K path, frequency schedules, pairing layouts, cache and architecture variants | Repeating the core introduction or the full sinusoidal derivation |

A separate relative-bias deep dive (Shaw → T5 → ALiBi) is a **future candidate**, not part of this change. Create it only if implementation or mathematical material grows beyond the short comparison appropriate to the core lesson and RoPE page.

## 6. Metadata and integration decisions

- Add the explicit source collection positional-encoding and assign membership only to sources reviewed for this topic.
- Add primary source records for Shaw et al., Raffel et al. (T5) and Press et al. (ALiBi), with partial-scan status and bounded claims.
- Retain the AiEdge short-form article as a supplementary partial scan, with its Substack inbox URL as an alias for the same source identity; no separate source or page is created.
- Add structured source-local extractions for all three papers under data/extractions/ and link each extraction from its source-catalogue record.
- Keep the existing Vaswani, Su, Jay Alammar, Harvard NLP, Stanford EE269, Jay Joshi, Raschka and Khan records; do not duplicate them.
- Keep the canonical concept ID positional-encoding. No new concept, route stage, computation node or page is introduced.
- Keep the two existing deep dives as the destinations for derivations. The core page and synthesis are updated to expose the score-bias family and the NoPE nuance without expanding into an architecture survey.
- Put five recall cards in the existing bilingual Practice companions. The synthesis sheets remain summaries; they are not repurposed as exercise pages.

## 7. Remaining work and validation gates

1. Run the source-catalogue and source-collection validators after the metadata changes.
2. Run the bilingual metadata, revision-coverage and learning-map freshness checks; regenerate the map artifacts from site/tools/build_learning_map.py.
3. Render the Quarto site and check all new links, anchors and mathematical rendering.
4. Inspect the FR/EN lesson, synthesis and Practice pages at desktop and mobile widths, including keyboard operation of the answer disclosures.
5. Revisit the visual design only if an original three-way insertion-point diagram (input addition / QK rotation / score bias) materially improves comprehension; do not copy third-party figures.
6. Consider a separate Shaw/T5/ALiBi deep dive only after a concrete implementation or mathematical need is identified.

No learner outcome, independent benchmark reproduction or long-context performance claim is made by this source compilation.

### Additional source access note (2026-11-27)

- Damien Benveniste's *How LLMs Encode Token Position* is registered and reviewed from the indexed snapshot available on 27 November 2026. Its contribution is complementary but does not justify a new canonical concept, page, computation node or learning-route stage. The complete article remains unverified because direct retrieval returned a cache miss.
- The Substack inbox URL `https://substack.com/inbox/post/225953856` is confirmed as an alias for the same AiEdge article, not a third source. The canonical URL and alias are recorded in the source catalogue and source review.
