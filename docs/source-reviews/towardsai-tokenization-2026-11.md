# Source review — Towards AI tokenization overview

**Source:** Madjid Korrabi, [Understanding LLMs from Scratch — Part 1: How LLMs Process Human Language (Tokenization)](https://pub.towardsai.net/understanding-llms-from-scratch-part-1-how-llms-process-human-language-tokenization-115b52c5f1d0), 2026-11-03.  
**Reviewed:** 2026-11-27  
**Decision:** screened; not selected for the tokenization-embeddings collection; no lesson or graph changes.

## 1. Scope and retrieval limits

The author-authored article text was inspected from introduction through conclusion using the complete search-index snapshot returned for the article's Medium canonical URL. Opening the indexed page and the supplied Freedium mirror directly returned cache misses. The assessment therefore applies to the full indexed text, not a verified live-page DOM.

The indexed article text contains an embedded-image marker, but the image bytes, exact asset URL, visual content, creator and reuse permissions could not be inspected. The Python example was not executed. Comments and outbound references were not reviewed. No content or image reuse permission is established; link-only treatment is appropriate.

## 2. Comparison with current LLM Lab

The article's scope maps to existing bilingual material:

| Article contribution | Existing destination | Decision |
|---|---|---|
| Word / character / subword tradeoff | `text-data`, `tokenization-strategies` | Already covered with more precise caveats |
| BPE, WordPiece and Unigram | `tokenization-strategies` | Already covered |
| SentencePiece and tokenizer pipeline | `tokenization-strategies` | Existing treatment is more precise |
| Unicode code points and UTF-8 bytes | `unicode-text` | Already covered with explicit byte output |
| Special tokens and implementation policies | `tokenization-strategies` | Already covered, including trust-boundary caveat |
| Language-dependent token cost | `tokenizer-multilingual-evaluation`, `tokenizer-design-evaluation` | Already covered with scoped evidence |
| tiktoken IDs and token bytes | `text-data`, `tokenization-strategies` and implementation audits | Existing examples and audits are more useful |

The article is a short introductory panorama. It does not contribute a new algorithm, a new canonical concept, a reproducible experiment or a distinct learning sequence. Its BPE walkthrough is a familiar toy example and is less inspectable than the project's existing BPE resources. The emoji-to-UTF-8-bytes example is potentially reusable as an alternative illustration, but the current Unicode lesson already demonstrates the relevant distinction exactly.

## 3. Technical cautions

1. **WordPiece adoption and worked score:** the article's claim that modern LLMs abandoned WordPiece because its pair score is computationally expensive is a broad historical/causal assertion without evidence. The q/u versus e/s illustration provides no frequencies, so it does not demonstrate the claimed ranking. The score formula itself is a documented WordPiece heuristic; the unsupported part is the historical explanation and the unquantified example. [Hugging Face's algorithm summary](https://huggingface.co/docs/transformers/en/tokenizer_summary) describes the score and contrasts it with BPE.
2. **Unigram pruning and probability:** the stated 10–20% removal per iteration is not a universal algorithmic constant. The sentence-probability explanation simplifies the model to one segmentation path; Unigram tokenization considers alternative segmentations and their scores. [Hugging Face's algorithm summary](https://huggingface.co/docs/transformers/en/tokenizer_summary) distinguishes Unigram's vocabulary pruning and most-likely segmentation.
3. **SentencePiece:** describing it merely as a wrapper is misleading; SentencePiece is a tokenizer library that trains and applies BPE or Unigram directly to raw text. Its `▁` marker preserves whitespace in the normalized representation, but default `nmt_nfkc` normalization removes redundant spaces and strips leading/trailing spaces. Exact raw-input recovery is therefore configuration-dependent. [SentencePiece documentation](https://google.github.io/sentencepiece/) and [normalization options](https://google.github.io/sentencepiece/docs/options.html) make this distinction explicit.
4. **Byte-level BPE:** a byte-level tokenizer with complete byte coverage can represent arbitrary byte sequences without an unknown-byte fallback, but this depends on the tokenizer's alphabet and implementation. The article's 'ultimate solution' framing overstates the claim: byte coverage prevents OOV byte failures; it does not guarantee semantic understanding.
5. **Llama 3 and tiktoken:** the article names OpenAI's tiktoken for GPT-family examples and separately mentions Llama 3 as a byte-level BPE model. These should not be read as a claim that Llama 3 uses the OpenAI `tiktoken` package or vocabulary; the article does not specify Llama 3's exact implementation.
6. **Multilingual cost:** the ten-versus-thirty token comparison is not reproducible without exact sentences, tokenizer identities and versions. Its causal explanation is not demonstrated.
7. **tiktoken code:** the displayed snippet was not run; the retrieved text concatenates the final print statement and the `if __name__ == "__main__":` guard, so it is syntactically invalid if copied literally. Repair and execute it before using it as a teaching example.

## 4. Ingestion disposition

The source and its eight atomic items are registered in `data/sources.yml` and `data/extractions/towardsai-understanding-llms-tokenization-2026.yml`. Items distinguish already-covered explanations and worked examples from unsupported claims and misleading simplifications. No new concepts, relations, pages, exercises or route entries are proposed.

The source is explicitly assigned to no curated collection (`collections: []`): screening it does not mean it should be added to the selected source corpus or inflate the collection's inventory.

## 5. Conclusion

**The article does not improve the current LLM Lab lessons enough to justify integration.** Its value is as a compact secondary overview and as a source of one optional emoji/byte illustration. The existing project material is broader, more technically qualified and better connected to tokenizer implementations and evaluation evidence. No content should be copied from this post.


## 6. External technical cross-checks

The following primary or technical references were consulted to separate the article's statements from established implementation behavior:

- [Hugging Face — Tokenization algorithms](https://huggingface.co/docs/transformers/en/tokenizer_summary): WordPiece pair score; BPE, WordPiece and Unigram training/encoding distinctions; SentencePiece raw-text handling.
- [SentencePiece — Documentation](https://google.github.io/sentencepiece/): library purpose, direct training from raw sentences, BPE and Unigram support, whitespace marker.
- [SentencePiece — Training options](https://google.github.io/sentencepiece/docs/options.html): default normalization, whitespace escaping and removal of repeated/leading/trailing spaces.
- [SentencePiece — Text normalization](https://github.com/google/sentencepiece/blob/master/doc/normalization.md): default NFKC-related normalization and configurable identity normalization.

These references support the technical corrections above; they do not establish the correctness of the article's unsourced historical or multilingual-cost claims.
