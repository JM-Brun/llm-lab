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
