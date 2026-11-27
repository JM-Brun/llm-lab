# Source review — Towards AI tokenization overview

**Source:** Madjid Korrabi, [Understanding LLMs from Scratch — Part 1: How LLMs Process Human Language (Tokenization)](https://pub.towardsai.net/understanding-llms-from-scratch-part-1-how-llms-process-human-language-tokenization-115b52c5f1d0), 2026-11-03.  
**Reviewed:** 2026-11-27  
**Decision:** screened; not selected for the tokenization-embeddings collection; no lesson or graph changes.

## 1. Scope and retrieval limits

The indexed author-authored text was inspected from introduction through conclusion, including the WordPiece, Unigram, SentencePiece, BPE, byte-level BPE, special-token, multilingual-cost and Python/tiktoken sections. The canonical Towards AI URL and the supplied Freedium mirror both returned retrieval cache misses. The body assessment therefore applies to the complete search-index snapshot, not a verified live-page DOM.

The article contains image placements, but no image bytes, exact asset URLs, placement details, creators or reuse permissions could be inspected. The Python example was not executed. Comments and outbound references were not reviewed. No content or image reuse permission is established; link-only treatment is appropriate.

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

The article is a short introductory panorama. It does not contribute a new algorithm, a new canonical concept, a reproducible experiment, a stronger figure or a distinct learning sequence. The emoji-to-UTF-8-bytes example is potentially reusable as an alternative illustration, but the current Unicode lesson already demonstrates the relevant distinction exactly.

## 3. Technical cautions

1. **WordPiece adoption:** the article's claim that modern LLMs abandoned WordPiece because its pair score is computationally expensive is a broad historical/causal assertion without evidence in the article. Do not repeat it as fact.
2. **Unigram pruning:** the stated 10–20% removal per iteration is not a universal algorithmic constant. The example is illustrative, not a reproduced likelihood calculation.
3. **SentencePiece:** describing it merely as a wrapper around BPE or Unigram is misleading; it provides its own training and encoding implementations. The claim of unconditional lossless reconstruction also ignores normalization and configuration choices.
4. **Byte-level BPE:** a byte-level tokenizer with complete byte coverage can avoid unknown-byte failures, but implementation details matter. The article's wording should not imply every tokenizer has identical fallback behavior.
5. **Llama 3 and tiktoken:** the article conflates byte-level BPE as a family with OpenAI's tiktoken library. These are not interchangeable implementation claims.
6. **Multilingual cost:** the ten-versus-thirty token comparison is not reproducible without exact sentences, tokenizer identities and versions. Its causal explanation is not demonstrated.
7. **tiktoken code:** the displayed snippet was not run; its formatting around the main guard is ambiguous. It should not be copied as a validated example.

## 4. Ingestion disposition

The source and its seven atomic items are registered in `data/sources.yml` and `data/extractions/towardsai-understanding-llms-tokenization-2026.yml`. Items distinguish already-covered explanations from unsupported claims and misleading simplifications. No new concepts, relations, pages, exercises or route entries are proposed.

The source is explicitly assigned to no curated collection (`collections: []`): screening it does not mean it should be added to the selected source corpus or inflate the collection's inventory.

## 5. Conclusion

**The article does not improve the current LLM Lab lessons enough to justify integration.** Its value is as a compact secondary overview and as a source of one optional emoji/byte illustration. The existing project material is broader, more technically qualified and better connected to tokenizer implementations and evaluation evidence. No content should be copied from this post.
