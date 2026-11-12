# Source review — LLM Embeddings Explained: A Visual and Intuitive Guide

**Source:** Hesam Sheikh Hessani, “LLM Embeddings Explained: A Visual and Intuitive Guide” (2025 as cited by the article).  
**Canonical URL:** https://huggingface.co/spaces/hesamation/primer-llm-embedding  
**Embedded article:** https://hesamation-primer-llm-embedding.static.hf.space/index.html  
**Related code repository:** https://github.com/hesamsheikh/llm-mechanics  
**Review date:** 10 November 2026  
**Review status:** partial content review; code and interactive runtime not independently audited.

## Executive assessment

This is a useful, visually oriented introductory tutorial that moves from count-based representations (TF-IDF) through Word2Vec and BERT to input embeddings in a concrete pretrained LLM. Its strongest contribution to LLM Lab is the interactive DeepSeek-R1-Distill-Qwen-1.5B token-embedding atlas: it offers a real-model complement to the synthetic NumPy lookup already shown in the bilingual embedding-space lesson.

The core conceptual distinction is **already covered** in LLM Lab: a token ID indexes an input embedding row, while Transformer layers produce context-dependent hidden states. The resource should therefore be recorded as a complementary source, not used to create another core lesson. A contextual link to the atlas may be valuable after a browser check. The tutorial's dimensionality and TF-IDF explanations need qualification before any claim is reused.

## What was inspected

- The complete article text exposed by the Hugging Face Space's embedded static page, from overview to conclusion and the 2025 citation block.
- Sections on embedding terminology, proposed quality properties, TF-IDF, Word2Vec, BERT, modern LLM input embeddings, `torch.nn.Embedding`, DeepSeek-R1-Distill-Qwen-1.5B extraction, cosine nearest neighbours and token-neighbour graphs.
- The article's link to the author's [LLM Mechanics repository](https://github.com/hesamsheikh/llm-mechanics).

Not inspected: manual interaction with the atlas, the repository notebooks/source code, model weights, runtime settings, linked primary references, image bytes, comments, or reuse permissions. The page extraction exposed some blank or unresolved references and figure-source placeholders. No code was run and no model result was reproduced.

## Contribution and relationship to the current curriculum

| Source contribution | Existing LLM Lab coverage | Decision |
|---|---|---|
| Token IDs retrieve fixed input vectors; deeper layers contextualize them | [Embedding-space lesson (FR)](../../site/fr/embedding-space.qmd) and [EN](../../site/en/embedding-space.qmd); contextualized representations (FR/EN) | Already covered; do not duplicate |
| Word2Vec static vectors versus Transformer contextual states | Existing embedding-space lesson includes a historical Word2Vec contrast | Keep the source as an optional complementary explanation |
| TF-IDF and count-based vectorization | Not part of the current core embedding-lookup lesson | Defer; verify the linked notebook before any worked example |
| Embedding dimension as a design trade-off | Current lesson focuses on lookup semantics, not model-dimension selection | Potential concise clarification or later model-comparison exercise |
| Real-model input embedding extraction and cosine neighbours | Current lesson uses a synthetic NumPy matrix and does not show a real model atlas | Strong optional external visual companion; link only unless rights are clarified |
| Token-neighbour graph and spelling/subword variants | Related to the cosine-similarity lesson, but no equivalent interactive graph is embedded | Potential optional case study with explicit limitations |

## Technical review and corrections

### 1. Keep the objects distinct

The article usefully distinguishes:
- **Input token embedding:** a learned row selected by token ID from the model's input embedding table.
- **Contextual hidden state:** the representation after model layers have processed the token with surrounding context.
- **Sentence/document embedding:** an output designed to represent a longer text, usually with a separate model or pooling/aggregation procedure.

These are not interchangeable. In particular, cosine neighbours in a causal language model's input embedding table do not establish the quality of a sentence-embedding model for semantic search. The current bilingual lesson already makes this distinction explicitly.

### 2. Qualify “what makes a good embedding?”

Semantic proximity is not a universal quality criterion. It is meaningful only relative to the model, training objective, representation layer, metric, data distribution and downstream task. For a retrieval system, task-level retrieval metrics and hard negatives matter; for an internal token table, nearest-neighbour inspection is descriptive rather than a direct quality score.

The dimensionality discussion is too categorical. Larger vectors increase parameter/storage and often compute costs, but do not automatically encode more useful relationships. Nor does a larger dimension, by itself, imply overfitting. Capacity, data, regularization, architecture, training objective and evaluation determine the trade-off. Treat the article's GPT-2 and DeepSeek dimensions as model-specific examples, not recommendations.

### 3. Check the TF-IDF dimensionality statement

The article says that splitting Tiny Shakespeare into ten chunks gives a “10 dimensional embedding, each for a document.” Under the standard document-term representation, ten chunks yield ten document rows, while the feature dimension is the vocabulary size (subject to vocabulary filtering). A later PCA projection can produce two coordinates for visualization. The prose appears to conflate document count, feature dimension and visualization dimension.

The linked notebook was not inspected, so this is a correction to the retrieved prose under the standard TF-IDF convention, not a claim about the actual code tensor shape.

### 4. Preserve historical qualifications

The Word2Vec summary is useful at an introductory level, but CBOW/Skip-gram, the context-window aggregation and negative sampling should be checked against the original implementation or a reliable technical reference before reuse.

The BERT section describes masked-language modeling and next-sentence prediction. This is accurate for original BERT, but not a universal property of encoder Transformers: for example, RoBERTa removed the next-sentence-prediction objective. The statement that BERT handles “token generation” also needs care; common BERT task heads are discriminative rather than autoregressive text-generation heads.

### 5. Interpret the DeepSeek atlas narrowly

The article describes extracting the input embedding table of `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`, tokenizing a sample sentence, inspecting 1536-dimensional token vectors and retrieving nearest tokens by cosine similarity. This is a useful concrete inspection workflow.

However:
- the result is specific to the checkpoint, tokenizer, input table, vector normalization, precision and chosen metric;
- token IDs and token strings are not necessarily whole words; casing, whitespace and subword variants can have separate rows;
- nearest input-token vectors are not contextualized states or sentence/document embeddings;
- a top-`k` nearest-neighbour graph can be directed; a symmetric graph requires an explicit symmetrization rule;
- visual proximity in a 2D projection can distort high-dimensional distances;
- this atlas is an illustration, not a benchmark or evidence of retrieval quality.

## Integration decision

1. **No duplicate core lesson.** The existing bilingual embedding-space lesson already explains the central lookup and contextualization mechanism.
2. **Optional visual link.** Consider adding the Space as a “real-model exploration” link after checking the live atlas in desktop and mobile browsers. Keep the link external; do not copy its figures or code.
3. **No unverified technical claims.** Do not reuse the dimensionality or TF-IDF claims without checking the author's notebook and adding the missing mathematical qualifications.
4. **Possible future exercise.** A small reproducible exercise could load a public checkpoint's input embedding matrix, inspect tokenization variants, compute cosine neighbours, and compare raw neighbours with a task-specific evaluation. This requires a model/runtime budget and a documented checkpoint/revision; it is not part of this ingestion.
5. **Rights.** Text, figures, code and model-derived assets remain link-only/unknown until the applicable licences and reuse terms are checked.

## Source graph and learning route

The source-local explanatory graph and inferred teaching route are recorded in [the extraction record](../../data/extractions/hesam-sheikh-hessani-llm-embeddings-explained-2025.yml). They are editorial reconstructions, not additions to the canonical concept graph.

## References used for this review

- [Hugging Face Space](https://huggingface.co/spaces/hesamation/primer-llm-embedding)
- [Embedded article page](https://hesamation-primer-llm-embedding.static.hf.space/index.html)
- [Author's LLM Mechanics repository](https://github.com/hesamsheikh/llm-mechanics)
- [LLM Lab embedding-space lesson (FR)](../../site/fr/embedding-space.qmd) and [EN](../../site/en/embedding-space.qmd)


---

## Consolidated implementation and learning-design supplement

This supplement extends the original 10 November content review. It audits the current Space-linked `primer-llm-embeddings` repository; the previously referenced `llm-mechanics` repository is a distinct, unaudited target.

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


## 9. Implemented learning integration: autonomous Deepen dossier and optional Practice experiment

The source contributes two complementary learning assets: (1) a standalone, bilingual **Deepen** dossier that surveys embeddings beyond LLMs, and (2) a small optional Practice/Experiment activity attached to the existing embedding-space and contextualized-representations lessons. The dossier intentionally revisits core notions from a broader historical, mathematical and cross-modal perspective; it does not replace or expand the main learning path.

### Learning objectives

After the activity, learners should be able to:
- trace a visible token string to one or more tokenizer IDs;
- explain that each ID selects a row of the checkpoint's input-embedding matrix;
- retrieve a vector by ID without decoding and re-tokenizing it;
- calculate cosine similarity and interpret top-k results as model-parameter neighbourhoods;
- distinguish token-ID identity, decoded token spelling, and contextual hidden states;
- explain how graph construction choices (directed/symmetrized, weighted/unweighted, node identity) change the visual result;
- identify why a nearest-neighbour list is not a semantic truth oracle.

### Optional model-inspection activity sequence (FR/EN parity)

| Step | Learner action | Evidence of understanding |
|---|---|---|
| 1. Predict / Prédire | Choose a token and predict likely neighbours; include a word with punctuation, whitespace or a subword fragment | Predictions distinguish spelling, usage and tokenization |
| 2. Tokenize / Tokeniser | Inspect text, token strings and IDs; show one-to-many word/token relationships | Learner can explain why a visible word is not necessarily one token |
| 3. Lookup / Consulter la matrice | Retrieve rows directly by token ID and display only a small vector slice plus dimension/norm | Correct identity mapping; no full model forward pass required |
| 4. Compare / Comparer | Compute cosine top-k for selected rows; show exact checkpoint and whether normalization is applied | Learner interprets ranking as a conditional numerical result |
| 5. Inspect / Examiner | Compare token variants, whitespace/case/prefix variants and special tokens | Learner notices tokenizer-dependent identity and decode/re-encode pitfalls |
| 6. Graph / Construire le graphe | Toggle directed vs symmetrized edges and weighted vs unweighted edges; retain IDs as node keys | Learner explains graph construction instead of reading it as ontology |
| 7. Contextualize / Contextualiser | Compare input row with a hidden state for the same token in two different contexts (only if a small reproducible model path is available) | Learner distinguishes static input parameter from context-dependent state |
| 8. Reflect / Interpréter | Explain one surprising neighbour and one limitation | Learner avoids equating cosine proximity with interchangeable meaning |

### Remaining technical contract for checkpoint-level reproduction

- Pin model identifier and immutable revision; record tokenizer revision, library versions, dtype and device.
- Load only the input embedding table for the lookup experiment; do not imply that this produces a contextual representation.
- Use token IDs as canonical identity; decoded strings are labels only. Never decode and re-tokenize to recover a vector row.
- Read matrix shape from the loaded checkpoint; assert every ID is in range and tokenizer/model vocabularies are compatible.
- Do not add special tokens unless the embedding matrix is resized and the new row's initialization/training status is explained.
- State whether cosine is computed on raw rows or normalized rows; include self-neighbour handling and tie behavior.
- Keep top-k edges directed unless the learner explicitly selects symmetrization; if symmetrized, state the rule (union or mutual-kNN).
- If a graph layout is shown, explain that layout coordinates are a force-directed projection and do not encode vector-space distances faithfully.
- Make a small fixture/test independent of downloading the 1.5B checkpoint; add a separate optional heavyweight model path only if resource requirements are explicit.
- Keep all learner-facing explanation and controls bilingual; keep the external Space as a further-exploration link rather than an embedded dependency.

### Scope decision

The autonomous dossier is implemented at `site/fr/embeddings-deep-dive.qmd` and `site/en/embeddings-deep-dive.qmd`, registered in the Deepen sidebar, bilingual map lists and language switch. Intentional overlap with the core embedding lessons is accepted because the page has a different purpose: a self-contained, broad survey and a hub toward further specialist topics. No new canonical concept, prerequisite edge, process breadcrumb or mandatory learning route is introduced. The small fixture-based Practice activity remains attached to the existing lessons.

## 10. Reproducible project-side inspection exercise

A small NumPy-only implementation now exists in `src/llm_lab/foundations/embedding_inspection.py`, with unit tests in `tests/unit/test_embedding_inspection.py`. It deliberately avoids loading or downloading the 1.5B checkpoint and complements (rather than duplicates) the autonomous Deepen dossier; it introduces no new canonical concept or mandatory route.

- `lookup_embedding_rows` retrieves rows directly by integer token IDs, preserving order and duplicate IDs; it returns a copy and never decodes/re-tokenizes labels.
- `cosine_top_k` computes cosine neighbours in the input embedding table, returns token IDs alongside scores, excludes the query by default, excludes zero-norm candidates, and uses ascending token ID as a deterministic tie-break.
- The query row must have non-zero norm; `k` must fit the eligible candidate set. The function returns a directed top-k list, not a symmetrized graph.
- Both helpers validate matrix shape, real finite values, integer IDs and row bounds. They are NumPy-only; no model, tokenizer, PyTorch or network dependency is introduced.
- The existing bilingual embedding-space exercise hubs now include the same executable example and explicitly state that input-table neighbours are not contextualized states or sentence-level retrieval evidence.

This is a tested reference-scale pedagogical implementation, not a reproduction of the external Space's checkpoint, extraction pipeline, interactive atlas or graph layout. The bilingual autonomous Deepen dossier now covers the broader embedding landscape, learning objectives, geometry, evaluation and non-LLM applications. The source atlas remains an external exploration link; live-atlas inspection and checkpoint-level reproduction remain open validation tasks.

### Visual reuse and attribution

The Hugging Face Space README metadata declares Apache-2.0. The source article also embeds illustrations credited to third parties (including Manning), so those assets are not copied into LLM Lab. The dossier preserves the pedagogical progression with original Mermaid diagrams, uses existing project SVGs for geometric intuition, and links to the original interactive Space and code. Any future direct reuse of a source figure should be limited to clearly author-created assets and retain the licence notice and attribution.
