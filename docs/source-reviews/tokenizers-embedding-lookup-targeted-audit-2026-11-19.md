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
