# Tokenizers and embedding lookup — targeted audit and experiment plan

**Review date:** 2026-11-19  
**Repository snapshot:** `main` at `0412befbad7d1c8413eeef5aeb798e5dc4ec121a`  
**Nature:** bounded static review and experiment design; no tests or comparative benchmarks were executed.

## 1. SentencePiece revision and upstream test inventory

Use official release `google/sentencepiece v0.2.3`, tag commit:

```text
eafd99cf3b8bfa5101c2c5f42aab2cc39947938d
```

Do not silently substitute inspected `master` HEAD `b85b750589487f545a752e0dd51df497ade6f4fc`.

| Test file | Test areas identified by static inspection |
|---|---|
| `python/test/sentencepiece_test.py` | Loading; invalid/empty decode; round trips; Japanese model; training; special-token combinations; sampling/N-best; pre-tokenizers; normalization; offsets; bytes; batch/parallel APIs; pickle; native batch methods |
| `python/test/numpy_test.py` | NumPy encode/decode; single/batch inputs; return-type validation; non-contiguous arrays; invalid types; parallel/N-best; memory safety; empty inputs |
| `src/sentencepiece_processor_test.cc` | Status, encode/decode, N-best/sampling, dummy prefix, byte fallback, invalid model loading, end-to-end, normalization, special pieces |
| `src/unigram_model_test.cc` | Lattice, Viterbi, N-best, forward algorithm, sampling, piece-to-ID, unknowns, control/special symbols, score edge cases |
| `src/bpe_model_test.cc` | BPE encode, ambiguous segmentations, unused symbols, deep merge chains, control/special-token behavior |

This is a test-name/source-structure inventory only. No upstream test suite was run. Before using these tests as behavioral evidence, execute selected targets against the pinned release and retain exact commands, environment and results.

## 2. PyTorch embedding: what is implemented

The project declares PyTorch only in optional dependency group `ml` (`torch>=2.6`); the base dependency is NumPy.

The core GPT implementation in `src/llm_lab/foundations/gpt.py` stores two NumPy matrices:
- `token_embedding`, indexed with `token_embedding[ids]`;
- `position_embedding`, indexed with `position_embedding[:seq_len]`.

The source explicitly describes fancy-indexing lookup. This is not `torch.nn.Embedding`. The forward path adds these NumPy arrays before transformer blocks. `gpt_ops.py` uses NumPy operations and references the PyTorch Linear convention only as a layout analogy.

Targeted inspection of GPT, transformer-block, attention, embedding-inspection and related unit-test paths found no direct `torch.nn.Embedding`, `nn.Embedding`, `F.embedding` or `torch.embedding` call. The inspected repository tree contained no `.ipynb` notebooks. Exact GitHub code searches returned no matches, but the code-search index was incomplete.

**Scope limitation:** this is not an exhaustive scan of every Python file, external example, dependency or future branch. The defensible conclusion is that the inspected core GPT implementation performs NumPy table lookup and does not demonstrate PyTorch's Embedding module. Run a local full-repository static scan before making an exhaustive negative claim.

Pedagogically distinguish (1) abstract indexed lookup (E[i]), (2) the project's NumPy implementation, and (3) PyTorch `torch.nn.Embedding` tensor/device/gradient semantics. Do not label the current GPT implementation as PyTorch-based.

## 3. Individual source disposition: SentencePiece documentation

**Source ID:** `google-sentencepiece-documentation`  
**Canonical source:** https://google.github.io/sentencepiece/  
**Catalogue metadata:** living documentation; no immutable revision; publication/update dates unknown; licence status unknown.

**Decision: covered by existing synthesis; no separate extraction in this pass.**

The bilingual tokenization-strategies pages and the collection dossier already cover the relevant contribution: SentencePiece is a library rather than one algorithm; it supports BPE and Unigram; whitespace-marker conventions are visible in a named SentencePiece-based configuration; normalization and whitespace handling are configuration-sensitive. A separate extraction would duplicate these concepts without a demonstrated new atomic claim.

This decision applies only to the documentation source, not the separate repository source or the pinned v0.2.3 code audit. The T5 example in the lesson is configuration-specific, not a universal SentencePiece output guarantee. The living documentation remains unpinned.

## 4. Discriminating comparison protocol

Compare SentencePiece v0.2.3, a pinned tiktoken release/encoding, and a pinned Hugging Face Tokenizers release/configuration. Record package versions, source commits, model/vocabulary checksums, configuration and runtime. Use identical raw input strings, but do not expect unrelated vocabularies to yield identical IDs or boundaries.

| Case | Input family | Discriminating property |
|---|---|---|
| A | Empty, whitespace-only, leading/trailing/repeated spaces, tabs/newlines | Empty handling, whitespace normalization and prefix conventions |
| B | NFC and NFD forms of accented text | Unicode normalization and offsets |
| C | French accents, combining marks, rare Latin characters | Normalization, byte coverage, unknown handling |
| D | Chinese, Japanese, Arabic | Script coverage, segmentation, whitespace assumptions |
| E | Emoji, modifiers, flags, ZWJ sequences | Multi-code-point graphemes, byte fallback, offsets |
| F | Punctuation, contractions, mixed numbers | Pre-tokenization and merge boundaries |
| G | Indented source code, identifiers, operators | Whitespace and punctuation segmentation |
| H | Literal strings resembling special-token spellings | Special-token recognition and allow/deny policy |
| I | Characters outside a deliberately restricted test vocabulary | Unknown token versus byte fallback |

For each run retain token strings/count, offsets and their coordinate system (code points, UTF-8 bytes or API-specific units), decoded output, exact round-trip equality, normalization assumptions, special-token policy, determinism, batch behavior and exceptions. Never compare raw IDs across unrelated vocabularies or treat lower token count as inherently better.

Execution phases:
1. Freeze library revisions and tokenizer artifacts.
2. Create shared UTF-8 fixtures with escaped whitespace/Unicode cases.
3. Implement adapters emitting common JSON while preserving native outputs/errors.
4. Test adapters independently.
5. Run the matrix and store raw output/environment metadata.
6. Interpret only measured differences and relate them to source/configuration evidence.

## 5. Remaining work

- Execute selected SentencePiece tests at the pinned commit.
- Complete a local full-repository scan for PyTorch embedding call variants.
- Pin tiktoken and Hugging Face Tokenizers revisions and explicit artifacts/configurations.
- Implement and execute the shared fixtures/adapters; no comparative measurements exist yet.
- Continue the 44-source triage individually. This document finalizes only the bounded disposition for `google-sentencepiece-documentation`.
- Validate candidate collection identities in #1306 before any membership backfill.

## 6. SentencePiece v0.2.3 — bounded implementation spot-check

**Pinned repository:** `google/sentencepiece` tag `v0.2.3`, commit `eafd99cf3b8bfa5101c2c5f42aab2cc39947938`. The following are static observations at that revision; the cited tests were read but not run.

### Normalization and whitespace are executable configuration, not an invariant of the model family

- `src/normalizer.cc:94-116` returns an empty normalized string for empty input and, when `remove_extra_whitespaces` is enabled, strips leading whitespace before processing.
- `src/normalizer.cc:124-142` maps spaces to U+2581 (`▁`) when `escape_whitespaces` is enabled and optionally prepends a dummy whitespace marker. The source comment explains that the prefix helps the trainer learn word-initial pieces; it is not a linguistic token boundary guarantee.
- `src/normalizer.cc:143-188` collapses/removes leading, repeated and trailing whitespace according to `remove_extra_whitespaces`; `treat_whitespace_as_suffix` changes where the dummy marker is placed.
- `src/normalizer_test.cc:63-82` includes compatibility-style examples such as circled digits, the corporate symbol, half-width Katakana and control characters. These fixtures show the configured normalizer's behavior, not complete Unicode NFKC conformance.
- `src/normalizer_test.cc:85-155` explicitly tests dummy-prefix disabled, whitespace-as-suffix, preservation of repeated whitespace, and unescaped spaces. This supports the claim that these outputs depend on the NormalizerSpec and TrainerSpec.

### BPE and Unigram have distinct inference mechanisms

- `src/bpe_model.cc:111-180` initializes symbols by longest-prefix matching from the model vocabulary, with character splitting as fallback, then constructs adjacent candidate pairs from known pieces. `src/bpe_model.cc:183-266` processes candidates through a priority queue using model piece scores; selected pairs are merged and neighboring candidates are reconsidered.
- Control symbols are deliberately excluded from merges: `src/bpe_model.cc:100-106` documents the reserved-ID design; `src/bpe_model.cc:160-169` and `:199-207` skip reserved IDs during candidate creation.
- `src/unigram_model.cc:746-775` implements ordinary encoding and N-best paths. `src/unigram_model.cc:796-818` describes an optimized Viterbi path for the unigram model; its scoring decomposition differs from the BPE pair-merge loop.
- `src/unigram_model.cc:778-793` samples a path from the lattice. The existence of N-best and sampling APIs is model-dependent; the processor checks availability rather than promising them for every model.

### Sampling and byte fallback are configuration/model-dependent

- `src/sentencepiece_processor.cc:420-447` normalizes input before N-best encoding and checks whether the current model supports N-best.
- `src/sentencepiece_processor.cc:449-485` validates that `alpha` is finite and non-negative; depending on model capabilities and `nbest_size`, the API chooses direct sampling, deterministic best encoding, or sampling among N-best candidates. It is therefore incorrect to describe `alpha` as a universal randomness switch independent of model type and `nbest_size`.
- `src/trainer_interface.cc:832-840` shows that byte fallback changes the requirement for an explicit unknown piece and records a backward-compatibility warning for `unk_id=-1` with SentencePiece versions <=0.2.2.
- `src/trainer_interface.cc:894-899` adds all 256 byte pieces when byte fallback is enabled. This is a training/model-construction option, not proof that every existing SentencePiece model has byte fallback.

### Evidence boundary and consequence

This code review narrows the implementation questions but does not complete an exhaustive repository audit. It covers selected normalizer, BPE, Unigram, processor and trainer paths plus representative tests. It does not inspect every language binding, every training option, the full model serialization path or all test cases. No C++/Python test, build, training run, benchmark or cross-library experiment was executed.

**Decision:** keep `google-sentencepiece-documentation` as covered by the existing bilingual synthesis; retain the repository as a version-pinned implementation reference. Do not create a redundant extraction or claim runtime validation. The next evidence step is to run selected upstream tests at v0.2.3 and archive exact commands, environment and results.