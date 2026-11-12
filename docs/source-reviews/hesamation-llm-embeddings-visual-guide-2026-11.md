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
