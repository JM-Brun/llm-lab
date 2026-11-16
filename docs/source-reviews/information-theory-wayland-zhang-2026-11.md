# Source review: Wayland Zhang — Information Theory Is All You Need (to Understand LLMs)

**Review date:** 2026-11-16  
**Source:** https://waylandz.com/blog/information-theory-and-llm/  
**Author:** Wayland Zhang  
**Publication date:** 2026-02-17  
**Source record:** `wayland-zhang-information-theory-llm`  
**Extraction:** [`data/extractions/wayland-zhang-information-theory-llm.yml`](../../data/extractions/wayland-zhang-information-theory-llm.yml)

## 1. Executive synthesis

The article offers a useful unifying teaching narrative: event surprisal and Shannon entropy lead to cross-entropy; cross-entropy connects directly to the token-level negative log-likelihood used in autoregressive training; probabilistic prediction is also closely related to efficient coding. It then extends the narrative to attention, thermodynamics, intelligence and V-information.

The strongest contribution is the cross-entropy decomposition:

[
H(q,p)=H(q)+D_{KL}(q|p).
]

For a fixed target distribution (q) and conditioning context, (H(q)) does not depend on the model distribution (p). Minimizing expected cross-entropy over (p) is therefore equivalent to minimizing the forward KL divergence. In ordinary next-token training with a one-hot observed target, the per-token cross-entropy is simply the negative log probability assigned to that observed token.

The article is best used as a **cross-cutting explanatory source**, not as a new curriculum. The existing entropy, cross-entropy and attention pages already own the relevant concepts.

## 2. Claim-by-claim assessment

| Article claim | Assessment | LLM Lab decision |
|---|---|---|
| Surprisal is (-log p(x)); entropy is expected surprisal | Established, with the logarithm base determining bits or nats | Already covered by the bilingual entropy lessons; cite as corroboration |
| Cross-entropy decomposes into target entropy plus KL | Established for normalized distributions, with finite-divergence/support conditions | Integrate the identity and assumptions into the existing cross-entropy lessons |
| Attention is analogous to mutual information | A possible intuition about dependencies, not a mathematical equivalence | Integrate a concise guardrail into the attention lessons |
| Landauer establishes a ceiling on information learnable from a dataset | Unsupported inference | Correct in this review; do not repeat as a theorem |
| Compression is intelligence | Overstatement | Keep the coding connection; reject the equivalence |
| V-information captures information accessible to bounded computation | Potentially useful advanced framing, but the article is informal | Defer until a formal definition and operational example are selected |

## 3. Technical qualifications

### 3.1 Entropy and cross-entropy depend on the distribution being discussed

For discrete variables:

[
H(q)=-sum_x q(x)log q(x),qquad
H(q,p)=-sum_x q(x)log p(x).
]

Then:

[
H(q,p)-H(q)=D_{KL}(q|p)geq 0.
]

The identity assumes normalized distributions and a finite KL divergence; in particular, (p(x)) must be positive wherever (q(x)) is positive. In language modeling, the relevant distributions are conditional on a context and tokenization. There is no single context-free “entropy of language” that is fixed for every dataset, tokenizer and evaluation protocol. The target distribution is fixed during a particular model comparison, not universally fixed across all training settings.

Logarithm base is a unit convention: base 2 gives bits; natural logarithms give nats. LLM training implementations commonly use natural logarithms, while coding discussions often express expected code lengths in bits.

### 3.2 Attention weights are not mutual information

Scaled dot-product attention computes:

[
A(Q,K,V)=operatorname{softmax}left(rac{QK^	op}{sqrt{d_k}}+Might)V,
]

where (M) represents any applicable mask. The softmax weights are normalized compatibility coefficients over accessible key positions. They are used to aggregate value vectors.

Mutual information is defined from a joint probability distribution:

[
I(X;Y)=sum_{x,y}p(x,y)lograc{p(x,y)}{p(x)p(y)}
      =H(X)-H(Xmid Y).
]

These objects differ in definition, inputs and interpretation. A row of attention weights is not an estimate of mutual information, and a high attention weight does not prove that one token provides a corresponding amount of statistical information about another. Studying attention and statistical dependence together can be useful, but it requires an explicit estimator and experimental design.

### 3.3 Landauer does not prove a general learning ceiling

Landauer's principle concerns the minimum heat dissipation associated with logically irreversible erasure of information in a physical system under specified thermodynamic conditions. It is not a theorem about statistical learning, generalization or the maximum amount of structure a model can infer from observations.

A learner can infer a regularity not explicitly written as an individual training example by exploiting assumptions, inductive biases and statistical structure. This does not mean information is created ex nihilo; it means inference is not the same operation as copying or extracting a literal stored bit. The article's physical analogy does not establish its broad learning claim.

### 3.4 Compression and intelligence are not equivalent

A probabilistic predictor can support efficient coding. Under an idealized arithmetic-coding interpretation, assigning probability (p(x)) gives an ideal code length near (-log_2 p(x)) bits. Expected code length is therefore connected to cross-entropy and predictive performance.

But compression performance is conditional on corpus, representation, tokenizer, coding protocol and overhead. It is not a sufficient measure of reasoning, factuality, planning or general intelligence. The Hutter Prize is an example of a compression-oriented benchmark, not proof that the best compressor is always the best model for every cognitive task.

### 3.5 V-information requires a precise operational setup

The article introduces V-information informally as information accessible to a restricted predictive model class. That motivation is useful, but an operational treatment needs a specified predictive family, target variable, conditioning information, loss or scoring rule, and estimator. The article supplies no controlled comparison showing that one architecture extracts a stated quantity of V-information better than another. LLM Lab should defer a dedicated lesson until a primary formal source and reproducible example are selected.

## 4. Integration decisions

1. **Source catalogue:** add the article with partial-scan status and explicit access/reuse limitations.
2. **Extraction:** preserve atomic claims, assumptions, qualifications, dispositions and the article's source-local teaching sequence.
3. **Entropy lesson:** no duplicate content; the existing bilingual lesson already explains entropy, surprisal, NLL, perplexity and context dependence.
4. **Cross-entropy lesson:** add the KL decomposition with a worked numerical example, assumptions and bits/nats distinction.
5. **Attention lesson:** add a short “attention is not mutual information” guardrail beside the interpretation of attention weights.
6. **Compression:** retain the predictive-coding interpretation as an optional connection; do not assert compression equals intelligence.
7. **Landauer:** retain only as a critical-review example of an invalid cross-domain inference.
8. **V-information:** defer canonical concept creation and a new page until the formalism and an operational experiment are independently sourced.

## 5. Reuse and provenance

The article and its companion repository are linked as external study resources. No article prose, figures or notebook code are copied. The author links the English notebook at https://github.com/waylandzhang/information-theory-and-language-models; its cells were not executed in this review and are not treated as reproduced experimental evidence. No licence or figure/code reuse permission was established.

## 6. Reproducibility and review boundary

This review is a technical and pedagogical assessment of the article text retrieved on 2026-11-16. It is not an independent replication of the companion notebook, a primary-paper survey of every advanced concept, or evidence that learners have mastered the material. The source remains `partially-scanned` for that reason.
