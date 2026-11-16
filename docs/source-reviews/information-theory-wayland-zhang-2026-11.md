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

The article introduces V-information informally as information accessible to a restricted predictive model class. The primary formal source is Xu et al., [A Theory of Usable Information under Computational Constraints](https://arxiv.org/abs/2002.10689) (ICLR 2020). It defines predictive families, optional ignorance, predictive conditional V-entropy and predictive V-information under logarithmic loss. The quantity is directional and family-relative; the unrestricted family recovers Shannon mutual information. The paper's estimation guarantees require bounded log-probabilities and complexity assumptions. The article itself still supplies no controlled comparison showing that self-attention extracts more V-information than bag-of-words. LLM Lab now teaches the formal concept through a small exact finite-family experiment; see the [primary-source review](predictive-v-information-xu-2020.md).

## 4. Integration decisions

1. **Source catalogue:** add the article with partial-scan status and explicit access/reuse limitations.
2. **Extraction:** preserve atomic claims, assumptions, qualifications, dispositions and the article's source-local teaching sequence.
3. **Entropy lesson:** no duplicate content; the existing bilingual lesson already explains entropy, surprisal, NLL, perplexity and context dependence.
4. **Cross-entropy lesson:** add the KL decomposition with a worked numerical example, assumptions and bits/nats distinction.
5. **Attention lesson:** add a short “attention is not mutual information” guardrail beside the interpretation of attention weights.
6. **Compression:** retain the predictive-coding interpretation as an optional connection; do not assert compression equals intelligence.
7. **Landauer:** retain only as a critical-review example of an invalid cross-domain inference.
8. **Predictive V-information:** integrate it as an advanced supporting concept from Xu et al., not as a claim established by the blog. A finite-family example is included in the existing bilingual experiment guide; no separate duplicate learning path is created.

## 5. Reuse and provenance

The article and its companion repository are linked as external study resources. No article prose, figures or notebook code are copied. The English companion notebook received a static audit of all 18 cells, code and saved textual outputs; it was not executed, so its runtime behavior and figures are not treated as reproduced experimental evidence. See [the notebook audit](wayland-notebook-audit-2026-11.md). The formal V-information source is separately catalogued and reviewed. No licence or figure/code reuse permission was established.

## 6. Reproducibility and review boundary

This review is a technical and pedagogical assessment of the article text retrieved on 2026-11-16. The notebook was statically inspected but not executed; the Xu et al. paper was inspected for the definitions and principal estimation assumptions needed for the project example, not exhaustively replicated. These are source-ingestion and reproducibility records, not evidence that learners have mastered the material. The article source remains `partially-scanned`.


## 3.6 Controlled counterexample: attention-row KL is not mutual information

LLM Lab now includes a deterministic counterexample in `experiments/information-theory/attention_kl_vs_mutual_information.py`. With two equally likely contexts and the same non-uniform row (0.9, 0.1) for each context, the mean row-wise KL to uniform is approximately 0.531 bits, while mutual information between context and key is exactly zero. The context does not change the key distribution, so the variables are independent.

For a genuine joint distribution, the correct identity is:

\[
I(X;Y)=\mathbb E_X\left[D_{KL}\left(P(Y\mid X)\|P(Y)\right)\right].
\]

The reference distribution is the marginal \(P(Y)\), not an arbitrary uniform distribution. The experiment also includes opposite rows, where both quantities happen to equal approximately 0.531 bits; that numerical coincidence does not make the definitions equivalent. Attention weights are not automatically calibrated conditional probabilities, so even the conditional-KL identity cannot be applied to them without an explicit probabilistic model.

A reusable discrete mutual-information function and tests for independence, perfect dependence and invalid joint tables were added to `src/llm_lab/foundations/information_theory.py` and `tests/unit/test_information_theory.py`. This is a mathematical counterexample, not an experiment on a trained Transformer.
