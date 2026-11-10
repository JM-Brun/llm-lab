# Source review — Brij Pandey, inference and generation diagram

**Source:** [LinkedIn post](https://www.linkedin.com/posts/brijpandeyji_you-ask-llm-a-question-it-pauses-then-share-7525787285829804032-YNEl)  
**Creator:** Brij Pandey  
**Accessed:** 2026-11-10  
**Status:** partially scanned; partially integrated

## Inspected material

The visible post text and the supplied diagram were inspected. The post follows one SQL-style request through tokenization, input embeddings, a decoder-only Transformer, next-token logits, greedy selection or sampling, detokenization, and streamed output. It explicitly separates prefill from incremental decode and identifies KV-cache reuse, TTFT, ITL, and speculative decoding.

## Useful pedagogical contribution

The strongest contribution is the connection between the internal generation loop and observable serving behavior:

- prompt length primarily increases the amount of initial prefill work and can delay the first token;
- generated length increases the number of incremental decode steps;
- the KV cache trades memory for avoiding repeated computation over the full prefix;
- TTFT and ITL describe different user-visible latency intervals;
- speculative decoding is a distinct optional optimization, not part of the basic autoregressive definition;
- fluent, syntactically valid output still requires task-specific validation (the SQL example can execute while encoding the wrong business definition).

## Integration into LLM Lab

The bilingual [generation lesson](../../site/fr/generation.qmd) / [English version](../../site/en/generation.qmd) now adds an operational subsection on TTFT, ITL, approximate KV-cache memory scaling, common prefill/decode bottlenecks, and speculative decoding. The linked figure is not embedded or copied.

## Qualification and limitations

The diagram is an intentionally simplified Llama-style decoder illustration. RMSNorm, RoPE, GQA and SwiGLU are common architectural choices, not universal Transformer requirements. Prefill being compute-bound and decode being memory-bandwidth-bound are useful tendencies, not guarantees; actual bottlenecks depend on hardware, kernels, batch size, context length, quantization and serving implementation. The post does not provide benchmark data or a concrete deployment configuration. The SQL example's semantic correctness cannot be inferred from syntax or successful execution alone.

No independent performance experiment or speculative-decoding implementation was run as part of this review. The source supports orientation and vocabulary, not quantitative claims about speedups.
