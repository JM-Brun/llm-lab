# Language-model surprisal and bits per character (BPC)

**Status: protocol specification only. No model has been evaluated and no empirical result is claimed.**

## Question

How does a causal language model's predictive code cost vary across held-out text domains, and how sensitive is the estimate to context length and evaluation conventions?

This makes the distinction between token-level surprisal and corpus-level bits per character operational. It is not a reproduction of Huang et al. (2024), a benchmark of intelligence, or evidence that compression causes capability.

## Primary quantities

For tokens \(x_1,\ldots,x_T\), token surprisal is

\[
s_t=-\log_2 P(x_t\mid x_{<t}),
\]

and total negative log-likelihood is \(L=\sum_t s_t\), in bits.

For a precisely defined text segment containing \(C\) Unicode code points:

\[
\mathrm{BPC}=L/C.
\]

This protocol uses Unicode code points in the decoded evaluation text, not bytes, grapheme clusters, tokens, or characters after undocumented normalization. Report UTF-8 byte count as a secondary denominator so BPC and bits per byte (BPB) cannot be confused.

Perplexity is derived from average token NLL and is tokenizer-dependent. It is not interchangeable with BPC.

## Experimental design

### Phase 1 — controlled, single-checkpoint evaluation

- Select one causal checkpoint and pin its immutable revision, architecture, tokenizer files and tokenizer revision.
- Load only from an explicit local snapshot or revision-pinned source. Record whether weights were downloaded; never silently resolve a moving model tag.
- Use a small, legally redistributable evaluation corpus or user-provided local text. Record provenance, licence, exact file hashes, encoding and preprocessing.
- Define document-level splits before inspection or tuning. Keep evaluation documents out of prompt construction, training, calibration and model selection.
- Separate domains (for example, general prose, technical prose and code) only where provenance and licences permit; do not merge domain scores into one unqualified headline.
- Score each document independently. Do not concatenate documents in a way that allows one document to condition the next.

### Scoring conventions

- Use a causal attention mask and inference mode; disable dropout.
- Score each content token exactly once. Overlapping windows may provide left context, but tokens already scored in a previous window must not be scored again.
- Pin maximum context length and stride. Record effective context available for each target token, including the initial-prefix policy.
- State how the first content token is scored. Prefer an explicit, documented BOS token where supported. If no BOS exists, use a declared model-compatible prefix convention and disclose the consequence.
- Do not count special prefix tokens in the content-character denominator. State whether tokenizer-added special tokens are scored or excluded.
- Sum log probabilities stably (log-softmax; no rounded probabilities). Report total scored tokens, total NLL bits, Unicode code points, UTF-8 bytes and resulting BPC/BPB.
- Verify that each target position is scored once, the scored content-token count matches the intended sequence, and a hand-computed tiny example matches the implementation.

### Pre-registered comparisons

1. **Context ablation:** evaluate the same checkpoint and texts at several supported context lengths. Hold every other setting fixed.
2. **Domain shift:** report per-domain BPC on the same checkpoint, with document-level counts and uncertainty.
3. **Stride control:** repeat scoring with different valid strides and confirm total NLL invariance (within floating-point tolerance) when effective context for each target is unchanged. If context changes, treat it as a distinct condition.
4. **Optional checkpoint comparison:** compare checkpoints only with a shared corpus, explicit model/tokenizer revisions, compatible scoring rules and a clear statement that tokenizers differ.

## Cross-tokenizer comparability

BPC normalizes by text characters, but does **not** automatically make different tokenizers equivalent. Different tokenizers induce different segmentations and probability models over token sequences. A comparison is meaningful only when each model assigns probabilities to the same underlying text under a clearly specified encoding/decoding convention. Report tokenizer identity, vocabulary, normalization, byte fallback and special-token policy. Treat cross-tokenizer rankings as protocol-dependent, not universal.

Where possible, include a within-tokenizer checkpoint comparison as the cleaner control. Never compare token-average NLL or perplexity across tokenizers as though the units were identical.

## Required record

Record at minimum:

- checkpoint repository, immutable revision, architecture and weight format;
- tokenizer repository/revision, vocabulary and special-token configuration;
- dataset source, version, licence, file hashes, document IDs and split;
- text decoding, Unicode normalization (prefer none unless required), newline handling and character-counting convention;
- context length, stride, prefix/BOS convention, truncation policy and target-token accounting;
- software versions, hardware, dtype, attention implementation, deterministic settings and command;
- per-document token count, NLL bits, character count, byte count, BPC and BPB;
- aggregation method, uncertainty procedure, exclusions and error analysis.

Report macro-average document BPC and corpus-level \(\sum L/\sum C\) separately: they answer different questions. Estimate uncertainty by resampling documents (or higher-level source groups where documents are dependent), not individual tokens. With few independent documents, state that uncertainty is weakly identified.

## Interpretation limits

- Lower BPC means the model assigns greater probability to evaluated text under this protocol; it does not establish broader intelligence, reasoning, truthfulness or causal capability.
- Domain alignment, contamination, corpus composition, model size, training data, tokenizer and context all affect the score.
- BPC is a predictive-compression measure, not model-size compression (quantization, pruning or distillation).
- Correlation between BPC and benchmark scores is not causation and does not define intelligence.
- A result on one checkpoint or a few corpora cannot establish a universal relationship.

## Reproduction status

This directory currently specifies the protocol only. Before reporting results, implement and test a scorer with exact-once target accounting, a tiny hand-checkable fixture, document-level aggregation and an explicit local-model loading path. Then run full CI, Quarto rendering and browser checks. No result should be added to the source synthesis until the run, data rights and limitations are independently reviewed.

## Related LLM Lab material

- [Predictive compression toy experiment](../predictive-compression/README.md)
- [Entropy and surprisal toy experiment](../entropy-surprisal-toy/README.md)
- [Information-theory experiments](../information-theory/README.md)
- [Experiment protocol](../../docs/experiment-protocol.md)
- [Compression and inference-efficiency synthesis](../../docs/source-syntheses/compression-intelligence-and-inference-efficiency-2026-11.md)
