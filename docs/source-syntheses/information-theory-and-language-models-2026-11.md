# Information theory and language models — source synthesis

**Status:** first source synthesis, anchored in Wayland Zhang (2026-02-17) and checked against the canonical LLM Lab explanations and definitions.

## 1. Learning question and scope

How do probability, uncertainty, next-token loss and compression connect — and where do attractive analogies stop being mathematically valid?

Canonical destinations: [entropy](../../site/fr/entropy.qmd), [cross-entropy](../../site/fr/cross-entropy.qmd), and [scaled dot-product attention](../../site/fr/scaled-dot-product-attention.qmd), with English counterparts. This dossier complements the existing scoring stage; it does not create a parallel route.

## 2. Source and contribution

| Source | Distinct contribution | Evidence type | Integration |
|---|---|---|---|
| [Wayland Zhang, Information Theory Is All You Need (2026)](https://waylandz.com/blog/information-theory-and-llm/) | A compact narrative connecting surprisal, entropy, cross-entropy, attention, Landauer, compression and V-information | Secondary tutorial; standard equations mixed with analogies and broad claims | Source record, extraction and technical review; selective additions to canonical pages |
| Canonical LLM Lab lessons | Contextualized token prediction, loss, perplexity and Transformer attention | Project explanations and mathematical derivations | Remain the teaching backbone; avoid duplicating entropy material |
| Shannon coding identities | Formal link between probability, expected code length and entropy | Mathematical result under source-coding assumptions | Reproducible toy experiment and revision sheet |

Detailed evidence and locators remain in [the extraction](../../data/extractions/wayland-zhang-information-theory-llm.yml) and [technical review](../source-reviews/information-theory-wayland-zhang-2026-11.md).

## 3. Integrated synthesis

For an event with probability p, surprisal is -log(p). Its expectation is Shannon entropy. For target q and predictive distribution p, cross-entropy is the expected negative log probability assigned by p to outcomes from q, and decomposes as:

```text
H(q,p) = H(q) + D_KL(q || p)
```

When q and the conditioning context are fixed, H(q) is independent of model parameters, so minimizing cross-entropy is equivalent to minimizing forward KL. In ordinary one-hot next-token supervision, the per-token cross-entropy is exactly NLL. Log base determines units: base 2 gives bits; natural logarithms give nats.

A probabilistic predictor can support efficient coding: ideal information lengths are -log2(p). This is a connection between predictive quality and compression, not an equivalence between compression and intelligence.

## 4. Critical distinctions

- **Attention vs mutual information:** attention weights are normalized compatibility coefficients used to aggregate value vectors. Mutual information is defined from a joint distribution. The former is not an estimator of the latter.
- **Landauer vs statistical learning:** a physical lower bound on heat dissipation for logically irreversible erasure does not establish a universal bound on what a learner can infer from data.
- **Compression vs intelligence:** coding performance depends on corpus, tokenizer, representation and protocol; it does not by itself measure reasoning or general intelligence.
- **V-information:** potentially useful model-class-relative framing, but the article does not supply a sufficiently precise operational definition or reproducible estimator. Defer a canonical concept until a formal source and experiment are selected.

## 5. What changed in LLM Lab

1. Cross-entropy lessons now derive the KL decomposition, state support/fixed-target assumptions, distinguish bits and nats, and show the one-hot special case.
2. Attention lessons explicitly reject the identity between attention weights and mutual information.
3. The source catalogue, extraction and technical review preserve provenance and claim-level dispositions.
4. A bilingual revision resource and a deterministic experiment make the central identities reviewable and executable.
5. Entropy content was not duplicated; speculative claims were not promoted to canonical facts.

## 6. Remaining limits and next steps

The companion notebook linked by the author has not been executed or audited. The source remains marked as partially scanned for that reason. The synthetic experiment validates arithmetic identities only; it is not evidence about trained LLMs. A future empirical study should compare predictive code length and held-out NLL across a documented corpus/tokenizer setup, while controlling for data size and model capacity.

## 7. Operational conclusion

Teach the robust chain — surprisal → entropy → cross-entropy/NLL → KL → predictive coding — as the core. Teach attention/MI and Landauer as examples of analogies that require careful boundaries. Keep compression/intelligence and V-information as qualified advanced discussion, not settled equivalences.
