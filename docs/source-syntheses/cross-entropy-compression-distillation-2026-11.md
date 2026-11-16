# Cross-entropy, compression and distillation — 3Blue1Brown Part 2

**Source:** Grant Sanderson / 3Blue1Brown, [*But what is cross-entropy? | Compression is Intelligence Part 2*](https://www.youtube.com/watch?v=GlYgs6v2YfU), 16 July 2026. [Official lesson page](https://www.3blue1brown.com/?lesson=cross-entropy&topic=neural-networks). [Creator's Substack post](https://3blue1brown.substack.com/p/but-what-is-cross-entropy).

**Scope and provenance.** This review uses the creator-published caption transcript as exposed by a third-party transcript mirror and static inspection of the upstream `3b1b/videos/_2026/cross_entropy` Manim source files. It is not a frame-by-frame audiovisual review, and no upstream code or visual asset was executed or copied. The source catalogue and extraction record these limits.

## 1. The central idea

Cross-entropy answers an operational question:

> If events actually follow one distribution, but the code lengths were designed using another distribution, what is the average coding cost?

In LLM Lab's notation, let $q$ be the data/target distribution and $p$ the model distribution. A code designed from $p$ assigns ideal lengths $-\log_2 p_i$, and the average cost when data follow $q$ is:

$$
$H(q,p)$=-\sum_i q_i\log_2 p_i.
$$

The decomposition

$$
$H(q,p)$=H$q$+$D_{\mathrm{KL}}(q\Vert p)$
$$

says that the cost is the optimal source entropy plus the excess caused by the mismatch between the source and the code model. The minimum occurs at $p=q$.

## 2. A concrete distribution-shift example

Part 2 reuses the four-symbol robot example from Part 1.

- Original code/model distribution: $p=(1/2,1/4,1/8,1/8)$.
- Its ideal code lengths: $(1,2,3,3)$ bits.
- New data distribution: $q=(1/8,1/8,1/4,1/2)$.

Keeping the old code gives:

$$
$H(q,p)$=\tfrac18(1)+\tfrac18(2)+\tfrac14(3)+\tfrac12(3)
=2.625\text{ bits}.
$$

The entropy of the new source is (H$q$=1.75) bits, so the excess cost is ($D_{\mathrm{KL}}(q\Vert p)$=0.875) bit per symbol. Swapping the roles of the distributions changes the answer: cross-entropy is directional, not a symmetric distance.

### Notation warning

The video labels the actual data distribution $P$ and the code/model distribution $Q$, giving a weighted sum $\sum_i P_i(-\log Q_i)$. LLM Lab uses $q$ for target/data and $p$ for model prediction. The roles are identical, but the letters differ. Read the semantic roles before comparing formulas.

## 3. From compression to language-model training

At each context $x_{<t}$, a language model produces a distribution over the next token. The observed token contributes:

$$
-\log p_\theta(x_t\mid x_{<t}).
$$

Averaging this quantity over observed target tokens is empirical next-token NLL / cross-entropy. In expectation under the data-generating distribution, it measures the model's expected information cost on those data. This is the bridge between the compression interpretation and the familiar pretraining objective.

The project already had this mechanism in its canonical pages:
- [Cross-entropy FR](../../site/fr/cross-entropy.qmd) and [EN](../../site/en/cross-entropy.qmd): target distribution, one-hot reduction to token NLL, logits, causal alignment, masks and reductions.
- [Language-modeling mathematics FR](../../site/fr/language-modeling-math.qmd) and [EN](../../site/en/language-modeling-math.qmd): autoregressive factorization, soft targets and the cross-entropy/KL identity.
- [Loss FR](../../site/fr/loss.qmd) and [EN](../../site/en/loss.qmd): aggregation and perplexity conventions.

No duplicate core cross-entropy lesson was needed.

## 4. Why the logarithm is principled — and the assumptions

Part 2 motivates the negative logarithm through constrained optimization. Suppose the expected per-event loss has the separable form

$$
\mathcal L(p;q)=\sum_i q_iF(p_i), \qquad \sum_i p_i=1.
$$

If the loss must be minimized at $p=q$ for every interior data distribution $q$, and (F) is differentiable, the Lagrange first-order condition gives

$$
q_iF'(q_i)+\lambda=0.
$$

Thus (xF'(x)) must be constant, so (F'(x)=c/x), and integration gives (F(x)=c\log x+d). A minimum requires (c<0), yielding negative log up to positive scaling and an additive constant.

This is a scoped argument, not a universal claim that all learning tasks must use log loss. It depends on the separable expected-loss form, normalized predictions, differentiability and the matching-distribution minimizer requirement. Robust, decision-theoretic or otherwise task-specific objectives can have different goals.

## 5. Distillation: from one observed token to a full target distribution

Standard next-token pretraining uses a one-hot target: only the observed token receives target mass, so the loss is its negative log-probability.

In distribution-level distillation, a teacher model supplies a full target distribution $q_T(\cdot\mid x_{<t})$, and a student predicts $p_S(\cdot\mid x_{<t})$. A token-level objective can be:

$$
\mathcal L_{\mathrm{KD}}=
H(q_T(\cdot\mid x_{<t}),p_S(\cdot\mid x_{<t})).
$$

This conveys relative probability across several candidate continuations rather than only the token that happened to occur in one training example. It is a richer soft-target signal per example, but it is not ground truth: the teacher can pass on its errors, biases and uncertainty. Distillation is model compression (a smaller student learns from a larger teacher), not predictive data compression (encoding a text stream).

The project already has a canonical concept for [knowledge distillation](../../site/fr/llm-evolution.qmd); Part 2 adds the useful mathematical bridge from that concept to cross-entropy and soft targets.

## 6. Language trees and gzip: a useful analogy, not an identity

The opening example describes appending a snippet from one document to another and observing how well a compressor adapted to the first document compresses the second. Shared linguistic regularities can lower the incremental compressed size.

This is a memorable cross-context-compression intuition, but it is **not exactly Shannon cross-entropy**:
- gzip is a practical dictionary/repetition compressor, not an ideal entropy coder;
- the distance described in the video has additional details;
- a document snippet is a sample, not a known probability distribution;
- compressor overhead and finite sample effects matter.

Keep it as an optional case study, not as a definition or a benchmark of language understanding.

## 7. Pedagogical integration decisions

| Contribution from Part 2 | Existing coverage | Integration |
|---|---|---|
| Mismatched codebook cost | Formula and KL identity existed; operational code interpretation was less explicit | Add worked 2.625-bit example to advanced math FR/EN |
| Direction and notation | Project notation was consistent but differed from video notation | Explicit mapping of video (P/Q) to project (q/p) |
| Log-loss rationale | NLL and KL decomposition existed; Lagrange argument was absent | Add optional derivation with assumptions and limits |
| Pretraining loss | Already explained in canonical loss chain | Link/reuse; no duplication |
| Teacher/student soft targets | Mentioned, but distribution-level distillation was not sufficiently concrete | Add teacher/student objective and warning about teacher errors |
| KL as excess coding cost | Algebra and asymmetry existed | Add numerical coding interpretation |
| gzip language-tree application | Not in core concept chain | Keep as qualified optional case study |

## 8. What learners should now be able to do

1. Given data $q$ and model $p$, compute the average ideal code length ($H(q,p)$).
2. Explain why ($H(q,p)$-H$q$=$D_{\mathrm{KL}}(q\Vert p)$) is the excess coding cost.
3. Explain why swapping $q$ and $p$ changes the result.
4. Map one-hot next-token NLL to the empirical cross-entropy objective.
5. State the assumptions behind the Lagrange-multiplier argument for logarithmic loss.
6. Explain what a teacher distribution contributes to student training, and why it is not ground truth.
7. Distinguish predictive compression from model compression.

## 9. Open limits

- No frame-by-frame visual audit or learner study has been performed.
- The upstream Manim scripts were inspected statically, not executed.
- The original paper behind the language-tree/gzip example was not independently audited in this pass.
- Part 2 points forward to a subsequent predictor-to-compressor construction; that later mechanism is outside this source review.
- The lesson's use of “smarter” is rhetorical shorthand. Cross-entropy alone does not establish factuality, intelligence or broad task performance.
