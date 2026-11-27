# Source review — Zsombor Veres-Lakos, “Attention from scratch”

**Source ID:** `zsombor-veres-lakos-attention-from-scratch-2026`  
**Author:** Zsombor Veres-Lakos · **Publisher:** Substack · **Publication:** 2026-11-16  
**Canonical URL:** https://zsomborvereslakos.substack.com/p/attention-from-scratch  
**Review date:** 2026-11-27 · **Type / language / audience:** blog post / English / introductory learner  
**Input:** user-provided 12-page PDF · SHA-256: `3945aa733c4d9c635bb6c721fa8bab922bc85f2d5218e9c891206bf311681b98`

## 1. Scope, provenance and scan status

The canonical Substack page and PDF endpoint were inaccessible during the initial retrieval attempt. The user then supplied the 12-page PDF export. All pages, equations, tables and visible figures were inspected. Page 1 identifies the title, author and date and states that the text was written by the author with LLM-assisted review and editing.

| Component | Status | Coverage and evidence | Limitations |
|---|---|---|---|
| Author-authored text | inspected | Full 12-page PDF | Live page edits not checked |
| Figures / tables | inspected-in-PDF | Matrices and attention figure on pp. 2–11 | Original assets and reuse rights not retrieved |
| Code / data | not-applicable | No executable code or dataset in PDF | No implementation to run |
| Comments / community | not-inspected | Not included in export | Live comments not reviewed |
| Linked resources | not-inspected | No linked destinations followed | Book and other posts not independently inspected |
| Metadata / version | partial | Title, author and date visible | Current live version/update history unknown |
| Licence / reuse rights | unknown | No licence identified | Text and figures remain link-only |

**Overall status: partially-scanned.** The supplied PDF's full content was inspected, but the live page, comments, linked resources and asset-level rights were not.

## 2. Atomic contribution inventory

See the [structured extraction](../../data/extractions/zsombor-veres-lakos-attention-from-scratch-2026.yml) for the source-local graph, teaching route, claims, figures, omissions and item dispositions.

| Contribution | Novelty for LLM Lab | Disposition |
|---|---|---|
| Meeting analogy: participants seek missing competencies and offer what they know | High as a teaching form; distinct from search/index-card analogies | Integrate by reference |
| Hand-designed W_Q and W_K selectors | Low; canonical lesson already explains projections | Already covered; preserve source example |
| Full score → softmax → V aggregation calculation | Low as mathematics; high as a continuous worked narrative | Already covered mathematically; link source |
| Distinction between W_K (matching) and W_V (transmitted information) | Reinforces canonical role separation | Already covered |
| Context vector → W_O → Delta X → X_new | Useful bridge from attention output to state update | Integrate by reference; link to block walkthrough |
| GPT mapping to embedding space and residual stream | Useful terminology bridge | Clarify by reference; no duplicate definition |
| Bank, pronoun and adjective examples | Alternative illustrations, not empirical evidence | Already covered; do not accumulate examples |
| Explicit omissions of causal masking and multi-head attention | Useful scope boundary | Already covered in dedicated lessons |
| Page-11 attention matrix | Visual reference credited to Raschka Figure 3.11 | Citation only; no image reuse |

## 3. Technical assessment

### Correct and useful

- The toy construction uses a shared state matrix $X$ and three distinct projections: $Q=XW_Q$, $K=XW_K$, $V=XW_V$ (pp. 2–7).
- Under the stated row convention, $QK^\top$ produces one score row per query. Row-wise softmax yields attention weights (pp. 4–6).
- $PV$ is the weighted aggregation of Value vectors (p. 8).
- $W_O$ maps the aggregate back to the toy state coordinates; $\Delta X=(PV)W_O$ and $X_{new}=X+\Delta X$ (pp. 8–9).
- The mapping from the toy competence matrix to the GPT residual stream is a useful conceptual bridge (p. 10).
- The article explicitly acknowledges that its attention figure omits GPT's causal restriction and that masking and multi-head attention are outside its scope (pp. 11–12).

### Claims and formulations requiring qualification

1. **The scalar 10 is not standard attention scaling.** It is a separate pedagogical multiplier introduced to sharpen the softmax distribution (pp. 4 and 6). It is not the fixed $1/\sqrt{d_k}$ factor. Learned projection norms can affect logit magnitudes, but this is not equivalent to inserting a separately learned temperature parameter. The canonical attention lesson and score-scaling deep dive remain authoritative.
2. **The all-zero score row becomes uniform.** Cara's query is the zero vector, so all scores are zero and softmax returns approximately $(1/3,1/3,1/3)$ (p. 6). This is correct for the unmasked toy example. It does not mean causal GPT attention must allocate mass to every token: the causal mask limits accessible positions.
3. **The toy state is not a full GPT block.** The source maps the attention branch's $\Delta X$ to a residual-stream update, but does not trace the MLP branch and its residual update (pp. 8–10). Its shorthand about each attention block adding $\Delta X$ must not replace the complete block computation.
4. **$W_O$ is not the vocabulary output projection.** Here it is the attention sublayer's output projection back into the residual-stream dimension (p. 8), not the final language-model head mapping hidden states to vocabulary logits.
5. **The clean needs/offers features are hand-designed.** The article itself cautions that real model features are rarely as clean as “need adjective” and are distributed over many dimensions (p. 11).
6. **The second-meeting behavior is a toy-model feedback effect.** After Cara's needs become negative, the same W_Q/W_K would give Bob's zero key a higher score than Alice's or Cara's key, so Cara would mostly attend to the participant with least to offer (pp. 9–10). This follows from the unbounded additive update and hand-designed features; it is not a general Transformer behavior.
7. **The linguistic examples are illustrative.** “Bank”, “Peter … he” and “quick brown fox” motivate contextual information flow (pp. 11–12); they do not establish that a specific attention head performs word-sense disambiguation, coreference or adjective composition.

### Unsupported or out of scope

- No executable from-scratch implementation, parameter-learning derivation, gradient calculation, multi-head derivation or causal-mask implementation is supplied.
- The PDF provides no empirical evidence for semantic interpretations of attention.
- The hand-designed projection matrices are not evidence about learned GPT weights.

## 4. Source-local knowledge model

The article's teaching sequence can be reconstructed as:

$$
X \xrightarrow{W_Q,W_K,W_V} Q,K,V
\quad ; \quad
S=10QK^\top
\quad ; \quad
P=\operatorname{softmax}_{row}(S)
\quad ; \quad
C=PV
\quad ; \quad
\Delta X=CW_O
\quad ; \quad
X_{new}=X+\Delta X.
$$

This is an editorial reconstruction, not a graph supplied by the author. The example uses one head, three participants, four toy state coordinates and a manually selected scalar 10.

The distinctive teaching move is to keep one analogy alive across every operation: Q represents what a participant seeks; K what they can offer; V what they transmit; the weighted sum what they receive; W_O how received information becomes a state change.

## 5. Source teaching route

1. State the meeting problem and introduce a competence matrix (pp. 1–2).
2. Construct W_Q and compute Q as a projection of needs (pp. 2–3).
3. Construct W_K and compute K as a projection of offers (pp. 3–4).
4. Compute attention scores and choose the row-as-query convention (pp. 4–5).
5. Apply row-wise softmax and interpret the weights, including the all-zero row (pp. 5–6).
6. Construct W_V and compute transmissible values with different absorption rates (pp. 6–7).
7. Aggregate values into context vectors and apply W_O (pp. 7–8).
8. Compute Delta X and X_new (pp. 8–9).
9. Map the toy example to GPT's embedding space, residual stream and learned projections (p. 10).
10. Interpret an attention matrix and give token examples; state masking and multi-head omissions (pp. 11–12).

The source assumes matrix multiplication, vectors and softmax but states no formal prerequisites or learning outcomes. Its worked numerical sequence is its strongest pedagogical feature.

## 6. Differential comparison with LLM Lab

| Learner question | Source treatment | Existing project treatment | Decision |
|---|---|---|---|
| What do Q, K and V mean? | Needs, offers and transmitted information | Canonical Q/K/V page: roles and shared learned projections | Do not add a fourth analogy to the page; link as an optional worked alternative |
| How do scores become weights and output? | Complete toy matrices from QKᵀ through softmax and PV | Dedicated scaled-dot-product-attention page and numerical workbench | Do not duplicate derivation |
| Why distinguish K and V? | W_K determines who is attended to; W_V what is transmitted | Canonical lesson already distinguishes compatibility from payload | Reinforcement only |
| How does attention change the state? | W_O, Delta X and X_new | Transformer-block walkthrough traces attention branch and residual path | Link to Build walkthrough; retain MLP caveat |
| What does GPT's residual stream mean? | Toy competence matrix maps to residual stream | Existing Transformer and block pages describe hidden states and residual paths | No new canonical node in this source-only pass; flag for wider architecture audit |
| What about causal masking and multiple heads? | Explicitly omitted | Dedicated causal-mask and multi-head/block content exists | No change |

The canonical pages already provide stronger mathematical precision, tensor-shape notation, explicit masking, a separate scaling explanation, bilingual coverage and exercises. The article complements them; it does not replace them.

## 7. Integration decision

**Changes justified**
- Register the source in the Q/K/V catalogue and source collection.
- Preserve a source-local extraction and review.
- Add a concise optional link to the article on both Q/K/V pages, describing the meeting analogy and its (W_O\rightarrow\Delta X\rightarrow X_{new}) progression.
- Add it to the pedagogical comparison matrix as a fifth introductory resource.

**Changes not justified**
- No new canonical Q/K/V, softmax, attention-score, residual-stream or output-projection concept.
- No new attention derivation or duplicate numerical workbench.
- No copied figure or article section added to the main lesson.
- No change to the conceptual graph or learner route on the basis of one secondary tutorial.

## 8. Visual assets and rights

| Location | Content | Inspection | Attribution / rights | Decision |
|---|---|---|---|---|
| pp. 2–4 | Competence matrix and W_Q/Q/W_K/K tables | Rendered tables inspected in PDF | Article attribution; reuse permission unknown | Cite/link only |
| pp. 5–6 | Attention-score and softmax-weight tables | Inspected in PDF | Article attribution; reuse permission unknown | Cite/link only |
| pp. 7–9 | W_V/V, context, W_O, Delta X and X_new tables | Inspected in PDF | Article attribution; reuse permission unknown | Cite/link only |
| p. 10 | Token-embedding table | Inspected in PDF | Article attribution; reuse permission unknown | Cite/link only |
| p. 11 | Attention matrix with highlighted second-token row | Inspected in PDF; caption credits Sebastian Raschka, Figure 3.11, *Build a Large Language Model (From Scratch)* | Underlying asset and reuse rights not independently checked | Preserve credit; do not reproduce |

## 9. Validation evidence

- The supplied PDF was fully parsed and its rendered pages inspected.
- The Q/K/V FR/EN pages, scaled-attention page and Transformer-block walkthrough were compared against the article.
- The existing Q/K/V source collection and pedagogical matrix were inspected before integration.
- Repository schema/CI, Quarto bilingual rendering, link validation and browser accessibility were not run as part of this review; these remain normal project validation gates.
- No code was executed; displayed matrices were checked algebraically against the described operations.

## 10. Open questions and next actions

- If the live Substack page later becomes accessible, compare it with the supplied PDF for post-export edits, comments and linked resources.
- During the broader conceptual-architecture audit, decide whether “residual stream” warrants a canonical concept identity distinct from generic hidden/contextualized representations.
- Keep this article's $W_O$ distinct from the final vocabulary projection whenever referenced.
