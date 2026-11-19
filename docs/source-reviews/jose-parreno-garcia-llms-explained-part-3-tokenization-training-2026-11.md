# Jose Parreño Garcia — LLMs Explained (Part 3): From tokens to training

**Source:** [LLMs explained (Part 3): From tokens to training – how a baseline LLM learns](https://joseparreogarcia.substack.com/p/llms-explained-part-3-tokenization-training)  
**Author:** Jose Parreño Garcia · **Publisher/date:** Substack, 3 May 2025  
**Inspection:** 19 November 2026 · complete visible author-authored article text  
**Structured extraction:** [YAML extraction](../../data/extractions/jose-parreno-garcia-llms-explained-part-3-tokenization-training-2025.yml)

## Executive synthesis

This is an accessible bridge between corpus preparation, tokenization and baseline autoregressive pretraining. Its strongest teaching contribution is the transition from cleaned text to token IDs and then to a concrete next-token prediction task. It also makes an important point: a model trained to continue text fluently is not thereby guaranteed to answer factual questions reliably.

**Integration decision:** retain the source as complementary material, add one bounded bilingual clarification about training-token occurrences versus vocabulary size and parameter count, and avoid duplicating existing lessons. No new concept or page is warranted.

## Inspection scope and limits

The complete visible article text was retrieved directly from the canonical Substack page. Inspected sections include the data-cleaning recap; tokenization and token IDs; BPE, WordPiece and character-level approaches; baseline next-token objective; Eiffel Tower toy example; probability-knobs explanation; text/token/model synthesis; compute-cost discussion and takeaways.

Embedded FineWeb screenshots, tokenizer demonstrations, model-output screenshots, Karpathy examples and Epoch AI charts were not retrieved as image bytes or visually inspected. Linked resources were identified but not exhaustively opened. No code, model, dataset or experiment was executed. Comments were not substantively audited. No text or figure reuse licence was established.

The author text is complete, but the source scan remains **partially scanned**.

## Reconstructed pipeline

1. Cleaned corpus text is supplied to a tokenizer.
2. Tokenization segments strings into model-specific units and maps them to integer IDs.
3. The model consumes an ordered sequence of token IDs after embedding lookup and subsequent model processing.
4. During causal pretraining, the model estimates a distribution over the next token conditioned on the available prefix.
5. A loss compares the predicted distribution with the observed next token; gradients update shared model parameters.
6. At inference, a decoding rule selects token IDs and the tokenizer maps them back to text.

The source offers a useful high-level story, but training is more accurately described through logits, cross-entropy/negative log-likelihood, backpropagation and optimizer updates—not independent per-word probability knobs.

## Technical corrections and qualifications

### Tokenization is not vocabulary lookup alone

A production tokenizer can include normalization, pre-tokenization, subword segmentation, byte fallback and special-token handling. BPE, WordPiece and character-level approaches are useful families to compare, but the article's short descriptions are not implementation specifications.

### Corpus token count is not vocabulary size

The article describes “13 trillion tokens” as “13 trillion unique tokens”. This is a category error:

- **Token occurrences / training tokens:** token instances in a corpus or training run.
- **Vocabulary size:** number of distinct token IDs the tokenizer can emit.
- **Model parameters:** learned numerical values in the neural network.

These quantities are not interchangeable. The article's 13-trillion GPT-4 figure is not verified here and should not be repeated as a confirmed statistic.

### Next word versus next token

The objective is next-token prediction, not necessarily next-word prediction. A token may be a whole word, part of a word, punctuation or another tokenizer-specific unit.

For an autoregressive model:

\[
p_\theta(x_t \mid x_{<t})
\]

The training loss is the negative log-probability assigned to the observed next token, aggregated over positions and examples. The article's toy completion is an intuition, not the optimization procedure.

### The probability-knobs metaphor needs a boundary

Real neural models do not maintain independent knobs for candidate words. They compute logits from shared parameters; a differentiable loss produces gradients that update those parameters. The same parameter changes affect many contexts and token predictions.

### Fluency is not factuality

The base-model objective rewards prediction of observed text, not truth verification. The author's specific screenshot examples remain unverified because the images were not inspected.

### Tokenizer encoding/decoding is not encoder-decoder architecture

The article's encoding-decoding machine is best read as a text-processing pipeline: text → token IDs → model → token IDs → text. It should not be confused with an encoder-decoder Transformer architecture. Decoder-only GPT models still use tokenizer encoding and decoding.

### Compute claims are qualitative here

The general point that frontier-scale training requires major accelerator and infrastructure resources is plausible. Specific charts, cost estimates and market-concentration claims were not independently checked; defer their reuse until Epoch AI figures and methodology are inspected.

## Pedagogical assessment

| Contribution | Value | Proposed use |
|---|---|---|
| Clean text → tokens → IDs | Moderate complementarity | Bridge corpus preparation and tokenization lessons |
| BPE / WordPiece / character contrast | Moderate complementarity | Beginner orientation, not replacement for algorithm pages |
| Eiffel Tower next-token example | High complementarity | Candidate worked example or flashcard in language modelling |
| Probability knobs | Useful but risky | Reuse only with explicit correction to gradients and shared parameters |
| Fluency versus factuality | High learner value | Connect base-model pretraining to post-training and evaluation |
| 13T “unique tokens” | Incorrect terminology | Correct as a misconception, not a fact |
| Compute-cost charts | Unresolved | Defer pending figure and source inspection |

## LLM Lab destinations and Phase B questions

Candidate destinations to verify against current page content:

- fr/text-data / en/text-data
- fr/tokenization-strategies / en/tokenization-strategies
- fr/language-modeling-math / en/language-modeling-math
- Relevant tokenizer and training-loop Build material

Compare the article's teaching moves against these pages, including summaries/flashcards and current Understand and Build routes. The likely outcome is a small number of bounded additions, especially the worked example and vocabulary-size/token-count distinction, not new pages or concepts.

## Remaining Phase C work

1. Inspect the embedded visual assets and record exact locators and reuse/rights status.
2. Verify any GPT-4 token-count or parameter-count claims against reliable dated primary evidence; otherwise keep them explicitly unverified.
3. Open the linked Epoch AI charts and methodology before considering cost figures.
4. Revisit the optional Eiffel Tower worked example only if a later review identifies a specific gap in the current next-token practice sequence.

The bilingual quantity clarification is integrated in the corpus-preparation pages. The source remains **partially scanned** because figures, comments, linked materials and rights were not fully inspected.
