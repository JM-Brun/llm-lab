# Source review — Brij Pandey's inference-path diagram

**Source:** Brij Pandey, “You ask LLM a question. It pauses. Then the answer starts appearing, piece by piece.”  
**Publisher:** LinkedIn  
**Published:** 10 November 2026 (catalogue metadata; the visible post was inspected)  
**Canonical URL:** https://www.linkedin.com/posts/brijpandeyji_you-ask-llm-a-question-it-pauses-then-share-7525787285829804032-YNEl  
**Review date:** 18 November 2026  
**Scan status:** partially scanned  
**Integration decision:** cite as a secondary visual overview from the existing bilingual generation lesson; do not reproduce the diagram or treat it as an architecture specification.

## Contribution

The inspected post text and supplied 1280-pixel diagram provide a compact overview of an inference request:

- tokenization and preparation of the input;
- prompt prefill and decoder-block computation;
- autoregressive token-by-token decoding;
- reuse of key/value states through a KV cache;
- token selection by greedy decoding or sampling;
- streaming output and latency diagnostics;
- speculative decoding as an optional optimization;
- TTFT (time to first token) and ITL (inter-token latency).

The diagram is useful as an orientation map because it puts the request lifecycle, decoder components, token selection and serving metrics in one view. It is not a substitute for the mathematical and implementation explanations in the project lessons.

## Integration in LLM Lab

The bilingual generation pages already explain the same underlying sequence in a more carefully qualified progression: prefill, incremental decode, optional KV cache, token selection, streaming, speculative decoding and latency metrics. The English page cites this diagram as an external overview. The source is therefore linked to the existing generation lesson rather than used to create a second explanation or a parallel route.

The source-to-knowledge links are limited to the existing canonical concepts:

- `autoregressive-generation`: the repeated predict/select/append loop;
- `prefill`: processing the known prompt before incremental decoding;
- `decode-step`: generating and appending subsequent tokens;
- `kv-cache`: reuse of previously computed keys and values.

These links describe the inspected subject matter; they do not assert that the post is a primary technical source.

## Evidence and limitations

The full visible LinkedIn post text and its supplied diagram were inspected on 10 November 2026. The diagram's decoder-block components, greedy/sampling selection, speculative decoding, TTFT and ITL were recorded in the source scan history.

The following limits remain:

- This is a secondary pedagogical overview, not a primary architecture specification.
- No serving stack, hardware, model configuration or benchmark was inspected; performance bottlenecks and speedups are configuration-dependent.
- The diagram is not reproduced. Figure reuse rights have not been established.
- The post does not establish that all LLM serving systems use the same decoder, scheduling or speculative-decoding implementation.
- The project's lesson and computational explanations remain the authoritative teaching material for the mechanisms.

## Editorial decision

Keep the source as a cited visual overview attached to the existing bilingual generation lesson. Do not create a dedicated extraction file: the source's useful contribution is already represented by the page's explanation and the four existing canonical concepts. A separate atomic extraction would duplicate the same basic inference sequence without adding source-specific evidence.

Revisit if the post is updated, a concrete implementation or benchmark is added, or the project uses a specific diagram element that requires closer technical verification.
