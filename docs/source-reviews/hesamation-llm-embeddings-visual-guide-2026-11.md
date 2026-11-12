# Hesam Sheikh Hessani — LLM Embeddings Explained: A Visual and Intuitive Guide

**Review date:** 2026-11-12 · **Owning audit:** [#765 — Hugging Face](https://github.com/JM-Brun/llm-lab/issues/765), under [#756](https://github.com/JM-Brun/llm-lab/issues/756)  
**Source:** [Hugging Face Space](https://huggingface.co/spaces/hesamation/primer-llm-embedding) · [rendered article](https://hesamation-primer-llm-embedding.static.hf.space/index.html)  
**Citation metadata:** Hesam Sheikh Hessani, 2025 · **Status:** partially scanned.

## Scope and evidence

Inspected the rendered article text: introduction; embeddings and their properties; TF-IDF; word2vec/CBOW/Skip-gram; BERT; modern LLM token lookup and contextualized representations; PyTorch lookup; the DeepSeek-R1-Distill-Qwen-1.5B example; cosine nearest neighbours; and token-neighbour graphs. The article describes a 50-token interactive atlas and recommends desktop (12–15 minute reading).

Not inspected: live atlas interaction/rendering, code execution, linked LLM Mechanics repository, audio, comments, outbound resources, asset bytes or licences. Do not treat this as a full Space/repository audit.

## Source-local model and route

**Objects:** tokens/IDs; vocabulary-indexed embedding matrix; static input embeddings; position information; contextual hidden states; similarity scores; nearest-neighbour sets; graph nodes/edges.

**Computational flow:** text → tokenizer → token IDs → embedding-row lookup → position-aware input representations → Transformer layers → contextual hidden states. A separate analysis branch compares selected vectors → computes cosine similarities → selects top-k neighbours → projects them as a graph.

**Historical comparison branch:** TF-IDF (document-term weighting), word2vec (predictive word-type vectors), BERT (encoder contextualization). These are comparison points, not sequential components of the illustrated modern LLM.

**Source teaching route:** motivate vector representations → explain geometric intuition → compare historical methods → introduce contextualization with BERT → locate embedding lookup in an LLM → inspect real token vectors → explore nearest neighbours/graph. This is the source's pedagogical order, not a prerequisite graph.

## Technical assessment

- Static token/input vectors and context-dependent hidden states are distinct; this is the source's strongest alignment with LLM Lab's canonical treatment.
- “Embedding” is used for both input lookup vectors and hidden states in wider literature. Preserve the distinction in LLM Lab without claiming universal terminology.
- TF-IDF is useful as a statistical contrast, but is not a learned word embedding in the same sense as word2vec or a Transformer token table. It often represents documents in term space.
- Higher dimensionality increases storage/compute and may enable richer representations, but dimensionality alone does not imply overfitting or quality.
- The simplified word2vec one-hot/hidden-layer account is pedagogical, not a full implementation specification; inspect code before reusing implementation claims.
- Original BERT used MLM and NSP; NSP should not be generalized to every BERT-family model. BERT task heads are not generic autoregressive generation heads.
- Position handling differs by architecture; not every LLM adds a learned positional vector in the same way.
- Cosine nearest neighbours are an inspection method, not a universal semantic-quality test. Results depend on model, representation, normalization, anisotropy, tokenization and token variants.
- A kNN graph is a projection induced by a selected similarity rule, not the model's native ontology, causal graph or proof of semantic interchangeability.
- The stated 1536-dimensional example is checkpoint-specific, not a general property of DeepSeek or LLMs.

## Contribution decisions and project crosswalk

| Contribution | Decision |
|---|---|
| Static lookup vs contextual hidden states | Reuse as a cross-check for existing bilingual Understand lessons; no duplicate page |
| Historical TF-IDF → word2vec → BERT comparison | Optional link; preserve task/architecture qualifications |
| Real token-ID → embedding-row lookup | Candidate numerical Practice investigation, pending code verification |
| Real-model nearest-neighbour atlas and graph | Distinctive visual/experimental contribution; link to original Space, do not copy |
| Dimensionality heuristics | Do not import as universal rules |
| Embedded code and linked repository | Defer until inspected and reproduced |

- **Understand:** existing embedding-space and contextualized-representations pages remain canonical.
- **Deepen:** optional geometry/similarity/anisotropy links; do not conflate token vectors with sentence/document embeddings.
- **Practice:** strongest candidate is a controlled nearest-neighbour investigation with predictions, top-k output, token variants and failure cases.
- **Build:** lookup-table explanation may support existing implementation; no new module or implementation is authorized by this source review.
- **Meta:** retain a source-local similarity graph separately from canonical semantic relations, computational dependencies and learner routes. Do not create a new concept, relation, breadcrumb or curriculum stage just because the Space visualizes neighbours.

## Visual rights and validation gate

The atlas is distinctive, but its actual visual quality, controls, accessibility, responsiveness and learning value were not inspected. Link to the original; do not copy/trace its figures or graph layout. Asset rights remain unknown and are governed by #156.

**Accepted now:** source registration, this bounded review and cross-reference under #765.  
**Link-only:** the external interactive atlas and article.  
**Deferred:** bilingual runnable Practice experiment and code reuse until the linked repository, model-loading path, dependencies, vector source, normalization and outputs are checked/reproduced.  
**Next evidence:** inspect the live atlas on desktop; reproduce one nearest-neighbour example; verify model configuration/dimension; then decide whether a compact bilingual experiment adds value. No learner-outcome claim is made.


## 8. Repository and implementation inspection — 2026-11-12

The Space source tree and its linked implementation were inspected after the initial text-only review:

- Space source: `src/index.html` (main revision `aa0a8f2`), fragments under `src/fragments/`, and `python/code/`.
- Linked implementation repository: [hesamsheikh/primer-llm-embeddings](https://github.com/hesamsheikh/primer-llm-embeddings). Its README documents `npm install`, `npm run build`, and a static Distill-style page with runtime/compile-time HTML fragments. Dependencies include D3 and Plotly.
- Python entry points: `save_qwen_embeddings.py` and `qwen_per_token_visualization.py`; the page also embeds Gists for tokenization, embedding lookup and nearest-neighbour examples.
- Visual structure: the article uses a Distill-style narrative, expandable code sections, a TF-IDF visualization, a word2vec hierarchy, token/neighbor graph fragments, and an atlas captioned as 50 random tokens plus nearest tokens from the named checkpoint. The page also links a TensorFlow Embedding Projector as an external exploration tool.

### Implementation semantics and reproducibility caveats

1. `save_qwen_embeddings.py` loads the named tokenizer/model, adds a new `[PAD]` token, extracts `get_input_embeddings()`, and saves its state dict. Adding a tokenizer token without resizing/replacing the model embedding matrix can create a tokenizer/model vocabulary mismatch if that token is later used. The sample does not appear to need padding; avoid mutating the tokenizer or explicitly resize and document the model if padding is required.
2. The visualization script reconstructs an `nn.Embedding` table with hard-coded `vocab_size=151936` and `dimensions=1536`. These values are checkpoint-specific. A robust reproduction should read the actual embedding tensor/config and assert tokenizer/model vocabulary compatibility rather than duplicate constants.
3. `find_similar_embeddings` computes cosine similarity against the full input-embedding matrix and takes top-k. This is a useful parameter-inspection operation, not contextual semantic similarity. The displayed score/rank is conditioned on the selected checkpoint, input embedding table and normalization convention.
4. The function decodes neighbour IDs to strings and later re-tokenizes those strings to recover vectors. Decoding and re-tokenization need not be an identity for byte/subword/special tokens. The script then selects a fixed sequence position (`[0][1]`), which may not correspond to the original token ID and can select only the first subtoken when a decoded token splits again. Preserve token IDs and retrieve rows directly from the matrix instead.
5. The graph uses decoded token strings as node keys. Distinct token IDs can decode to colliding or visually confusing strings; use token IDs as node identity and decoded forms only as labels. Also, top-k neighbour membership is directed by construction, but `networkx.Graph` renders it as an undirected edge; the graph must be labelled as a symmetrized kNN view (or preserve direction/weights explicitly).
6. The page's statement that the embedding module is “a simple Linear layer” is only an equivalence under one-hot input and matching weight/bias conventions. The implementation distinction is that `nn.Embedding` performs indexed row lookup without materializing one-hot vectors.
7. The article's BERT task-head description says “token generation or classification”; this is misleading for generic BERT. BERT is an encoder representation model with task-specific heads; it is not a causal next-token generation model.
8. The article's TF-IDF visualization describes a 10-dimensional document representation, but the figure caption refers to “word embeddings”. This is a terminology mismatch: the shown TF-IDF vectors represent document/chunk term-weight profiles, not learned word-type embeddings.

### Integration consequence

The resource is now more than a general visual primer: it provides a traceable end-to-end case study connecting tokenizer IDs, parameter-table lookup, vector comparison, top-k retrieval, token decoding and graph construction. LLM Lab should teach this as a **parameter-inspection experiment** with explicit identity/provenance and failure analysis, not as proof that nearest neighbours are semantically equivalent. A safe learner exercise should keep IDs throughout, compare decoded forms only for display, expose whether the graph is directed/symmetrized, and distinguish input embeddings from contextual hidden states.

### Inspection boundary

The HTML and Python source were read, but the code was not executed and the running interactive Space was not operated. No benchmark, runtime, visual usability, output correctness or learner outcome is claimed. The repository's build instructions were inspected, but no independent build was performed.
