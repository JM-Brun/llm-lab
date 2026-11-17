# Source review — Jothi Moorthy, “When you type a prompt, the LLM sees numbers, not words”

**Source ID:** jothi-moorthy-llm-processing-linkedin  
**Author:** Jothi Moorthy  
**Publisher:** LinkedIn  
**Canonical URL:** https://www.linkedin.com/posts/jothi-moorthy_%F0%9D%97%AA%F0%9D%97%B5%F0%9D%97%B2%F0%9D%97%BB-%F0%9D%98%86%F0%9D%97%BC%F0%9D%98%82-%F0%9D%98%81%F0%9D%97%BD%F0%9D%97%BF%F0%9D%97%BC%F0%9D%97%BA%F0%9D%97%BD%F0%9D%98%81-share-7528445050129764353-hs6w/  
**Review date:** 2026-11-17  
**Source type:** introductory educational social-media post  
**Language:** English

## 1. Inspection scope and provenance

The directly readable LinkedIn post text was inspected on 2026-11-17. It contains a five-stage sequence: prompt text; tokenization and token IDs; embeddings; attention and Transformer layers; next-token prediction and autoregressive repetition. It also connects token counts to context/pricing limits and warns that plausible predictions are not necessarily true.

| Component | Status | Evidence / limitation |
|---|---|---|
| Author-authored post text | Direct text inspection | Title, five stages, practical implications and closing question were visible |
| Author identity | Visible metadata | Page identifies Jothi Moorthy as author |
| Publication date | Unknown | LinkedIn exposed a relative time only; no exact date is asserted |
| Supplied infographic | Not inspected | Supplied media URL could not be retrieved as image bytes |
| Comments | Not exhaustively inspected | Some comments were visible; they are not merged into author claims |
| Newsletter / outbound links | Not inspected | Linked newsletter was not followed |
| Rights | Unknown | No licence or reuse permission established; link-only handling |

The source is therefore **partially scanned**. The author text is available, but the visual asset, complete comment thread, newsletter and rights remain outside the inspection boundary.

## 2. Technical assessment

The broad data flow is suitable as a beginner's orientation: text is tokenized into model-specific IDs; IDs index learned embedding vectors; Transformer computations transform representations; the final state is projected to vocabulary scores/probabilities; decoding selects a token and repeats.

Important qualifications:

1. **Tokens are not necessarily words or word fragments.** Depending on the tokenizer, units may be bytes, byte sequences, characters or subword/word-like pieces. The example IDs are specific to a tokenizer and vocabulary; they are not portable across models.
2. **Token IDs are categorical indices.** Their numeric values do not express magnitude, semantic distance or similarity. Learned representations are retrieved through embedding parameters.
3. **Initial embeddings are not contextualized meanings.** An embedding lookup supplies an initial vector. Context-dependent hidden states emerge through subsequent network computation; positional information also matters but is omitted from the post's five-step summary.
4. **Attention is not a token consciously deciding.** The metaphor is shorthand for learned, input-dependent weighted aggregation. “Earlier tokens” describes a causal decoder; other Transformer architectures may use different masks and information flow.
5. **Attention weights are not a complete explanation of semantics.** The pronoun example motivates contextualization but does not demonstrate that an individual attention head or weight identifies a reference.
6. **The next-token percentages are illustrative.** No model, tokenizer, prompt, logits or decoding configuration is identified. The conceptual point is the conditional distribution and iterative generation, not the example values.
7. **Prediction is not verification.** The warning that plausible output need not be true is useful; factual reliability remains an evaluation and grounding question, not something solved by prompt wording alone.

## 3. Pedagogical value and comparison with LLM Lab

**Strength:** one compact, approachable, end-to-end recap connecting input representation to autoregressive output. The practical link between token counts and context/pricing limits is a useful audience-facing reminder.

**Limit:** the post compresses several distinct mechanisms into one short overview. It omits positional information, Q/K/V, causal-mask mechanics, residual connections, normalization, logits, decoding alternatives, mathematical details, exercises and reproducible examples. The image could not be checked for additional content.

The substance is already covered more precisely across canonical bilingual lessons:

- llm-overview — overall model and inference orientation;
- text-data and tokenization-strategies — text, token boundaries, vocabulary and tokenizer-specific IDs;
- embedding-space and contextualized-representations — initial lookup vectors versus contextual hidden states;
- transformer, Q/K/V, attention and causal-masking — network computation and information flow;
- logits, probabilities and generation — vocabulary scores, distributions, selection and autoregressive repetition.

No missing concept, evidence-backed relation, learner exercise or implementation is identified. The post does not justify another route stage or a repeated explanation. The source-local five-step route and graph are preserved in the extraction file; they are not merged into the canonical learning route or concept graph.

## 4. Disposition

**Decision: retain a provenance record, but reject substantive integration.** This is a useful external quick-reference for beginners, not a source that improves the current curriculum. Do not add a canonical page, duplicate infographic, learning-route node, concept, code or exercise. Existing pages already supply the distinctions that the post necessarily compresses.

The supplied image remains link-only and uninspected. Reconsider only if the asset can be retrieved and reveals a distinct, technically sound pedagogical contribution; any reuse would still require asset-level rights clearance under issue #156.

Structured source-local reconstruction and atomic dispositions: data/extractions/jothi-moorthy-llm-processing-linkedin.yml.
