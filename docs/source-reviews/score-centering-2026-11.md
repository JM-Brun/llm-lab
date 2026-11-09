# Score centering: source review and integration decision

**Review date:** 2026-11-09  
**Status:** partial ingestion; conceptual integration scoped; learner-facing page deferred pending full-paper audit.

## Sources and provenance

1. Cameron R. Wolfe, [Score Centering](https://cameronrwolfe.substack.com/p/score-centering). The canonical Substack page returned a cache miss in this pass. Only its title/author and indexed references linking it to the primary paper were available. Its article body, section sequence, examples and equations have **not** been inspected. The source catalogue therefore records it as partially scanned and deferred; no technical claim below is attributed to Wolfe.
2. Martin Marek and Max Ryabinin, [Score Centering Stabilizes Off-policy Reinforcement Learning](https://arxiv.org/abs/2609.20807), arXiv:2609.20807, submitted 2026-09-17. The abstract and bibliographic metadata were inspected.
3. [Official implementation repository](https://github.com/martin-marek/score-centering). The README's loss contract, top-k approximation, correction composition and test instructions were inspected. Source code and tests were not run.

This is a **source-cluster ingestion**, not a claim that the Substack article was fully scanned. The primary paper and implementation have separate provenance records.

## Technical synthesis supported by the inspected material

### Problem

Off-policy LLM RL may generate rollouts with an inference/sampling engine and compute gradients with a training engine whose effective distributions differ. Quantization, numerical implementation differences and stale sampler weights are examples discussed in the primary-source material. Exact train/inference equivalence may impose unacceptable systems costs.

### Mathematical hinge: the score function

For a parameterized categorical policy,

\[
s_\theta(a\mid x)=\nabla_\theta\log p_\theta(a\mid x).
\]

Under the policy's own distribution, normalization gives the zero-expected-score identity (under the usual differentiability/interchange conditions):

\[
\mathbb{E}_{a\sim p_\theta(\cdot\mid x)}
[s_\theta(a\mid x)]
=\nabla_\theta\sum_a p_\theta(a\mid x)=0.
\]

If actions/tokens are sampled instead from a behavior distribution \(q\), then in general

\[
\mathbb{E}_{a\sim q(\cdot\mid x)}
[s_\theta(a\mid x)]\ne 0.
\]

The key distinction is the distribution under which the score is averaged. This is not a centering of attention logits, raw log-probabilities, rewards, or advantages.

### Method at conceptual level

The paper identifies an off-policy drift component associated with the non-zero sampler expectation of the trainer score. Score centering adds a correction that subtracts this sampler-expected score contribution, isolating the reward-correlated signal from a component that can pull the trainer toward the sampler independently of which actions earned reward.

The full paper must be read before publishing its exact estimator equation, conditioning, stop-gradient placement, assumptions or proof details. The extraction deliberately does not reconstruct those from a high-level summary.

### Relationship to importance sampling

These methods are not synonyms:

- Importance sampling reweights samples to change the distribution under which an expectation is estimated; practical clipping/truncation introduces its own trade-offs.
- Score centering is an additive correction aimed at the drift component.
- The official implementation explicitly supports composing score centering with compatible importance-sampling corrections.

The official implementation also describes a practical top-k estimator: sampler top-k log-probabilities/IDs are retained and the vocabulary tail is modelled using the trainer distribution rescaled to match sampler tail mass. Full-vocabulary sampler log-probabilities provide the exact-centering alternative. These are implementation details, not prerequisites for the first conceptual explanation.

## Placement in LLM Lab

**Primary domain:** probabilistic-foundations-training  
**Secondary domain:** inference-efficiency

**Tags proposed for retrieval:** topic:score-centering, topic:off-policy-reinforcement-learning, topic:training-inference-mismatch, topic:policy-gradient, topic:policy-drift, method:score-function, method:importance-sampling.

This belongs to advanced RL/post-training and the boundary between inference systems and optimization. It does **not** belong in the Transformer attention sequence: the score function is \(\nabla_\theta\log p_\theta\), not the attention compatibility matrix \(QK^\top/\sqrt{d_k}\).

It also should not be inserted into the core eight-stage computational spine. The current spine correctly distinguishes generation, observed-target scoring/evaluation and teacher-forced training; policy-gradient RL is a further optimization regime that uses sampled trajectories and reward/advantage signals. It is not a fourth step in ordinary next-token prediction and it does not replace supervised teacher-forced training.

## Proposed learning sequence (not yet added to the canonical guided route)

1. Expected reward and policy-gradient objective.
2. Log-probability gradient / score function.
3. Why the expected score is zero on-policy.
4. Behavior policy versus trainer policy; off-policy rollouts and training-inference mismatch.
5. Drift decomposition and score-centering correction.
6. Distinction and composition with importance sampling (IS, TIS/MIS, PPO/GRPO-family corrections).
7. Implementation details: sampler log-probabilities, top-k approximation, vocabulary tail, token masks and numerical precision.

Prerequisites: probability distributions, log-likelihood, gradients, conditional next-token distributions, supervised training versus sampling. PPO/GRPO and advantages should be introduced before the method's full derivation, not assumed silently.

## Integration decisions

| Contribution | Decision | Reason |
|---|---|---|
| Off-policy training/inference mismatch | Integrate conceptually | Connects inference-engine behavior to RL update stability |
| Score-function zero-mean identity | Integrate conceptually | Essential mathematical explanation |
| Drift correction / score centering | Integrate as advanced topic | Central method; exact derivation still pending |
| Importance-sampling distinction | Integrate by reference | Prevents conceptual conflation |
| Top-k tail approximation and code contract | Defer to implementation deep dive | Too detailed for first conceptual treatment |
| Cameron Wolfe article's specific explanations | Defer | Canonical article body not retrieved |

## What must not be claimed yet

- That the Cameron Wolfe article has been fully read or that its distinctive contribution is known.
- That the full paper's proof, assumptions, every experiment or appendix has been audited.
- That reported results have been independently reproduced.
- That the official implementation or its framework integrations have been executed and verified.
- That score centering fixes all off-policy mismatch: the current evidence supports drift correction and composability, not universal correction of every distributional/reweighting error.
- That score centering is a form of attention-score normalization.

## Next bounded work

1. Retrieve and read the full arXiv PDF, especially the derivation and experimental appendix.
2. Retry the canonical Substack page or a legitimate indexed mirror; compare its actual added explanation against the primary paper.
3. Inspect the official implementation's loss and tests; verify the exact correction, stop-gradient semantics, masking and top-k tail approximation.
4. Only then create canonical concept IDs and a bilingual advanced lesson, with a small graph projection derived from the existing registries. Keep the guided core route unchanged; link the advanced branch from training/gradients and the RL/post-training domain when that curriculum exists.
5. Add a numerical toy exercise demonstrating \(\mathbb{E}_{p_\theta}[s_\theta]=0\) and how a different sampler can make the expectation nonzero, followed by a controlled comparison of no correction, importance sampling and score centering.

## References

- [Cameron R. Wolfe — Score Centering](https://cameronrwolfe.substack.com/p/score-centering)
- [Marek & Ryabinin — arXiv:2609.20807](https://arxiv.org/abs/2609.20807)
- [Official reference implementation](https://github.com/martin-marek/score-centering)
- [Hugging Face Papers summary](https://huggingface.co/papers/2609.20807)
- [Fei Tian — What Score-Function Centering Fixes, and What It Leaves](https://fei-tian.ai/blog/what-score-function-centering-fixes/) (independent secondary discussion; not treated as a primary source)
