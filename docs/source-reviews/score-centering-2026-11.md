# Score centering: source review and integration decision

**Review date:** 2026-11-09  
**Status:** primary-paper full-text mirror reviewed; canonical PDF/appendix and official tests not fully verified; Cameron Wolfe article remains only partially retrieved.

## 1. Provenance and retrieval

1. Cameron R. Wolfe, [Score Centering](https://cameronrwolfe.substack.com/p/score-centering). Direct retrieval still returns a cache miss. Search indexing and Wolfe's public Substack profile confirm the author identity and publication context, but do not expose the body of this specific post. Its equations, examples, illustrations and added interpretation remain **uninspected**. No technical claims below are attributed to Wolfe.
2. Martin Marek and Max Ryabinin, [Score Centering Stabilizes Off-policy Reinforcement Learning](https://arxiv.org/abs/2609.20807), submitted 2026-09-17. The abstract and a full-text rendering on [alphaXiv](https://www.alphaxiv.org/abs/2609.20807) were inspected, including the method discussion and selected experiment/implementation sections (pp. 1, 5–9 and 12). The canonical arXiv PDF could not be fetched directly; not all appendices and tables were independently audited.
3. [Official implementation](https://github.com/martin-marek/score-centering): README and public losses.py inspected. The test command and expected scope were checked, but tests were not run.

This is a source-cluster review. The Substack article, primary paper and implementation have separate provenance.

## 2. Problem setting

Let \(p_\theta(\cdot\mid h)\) denote the trainer's next-token distribution at prefix \(h\), and \(q(\cdot\mid h)\) the distribution that generated the rollout. Ideally they coincide. In practice they can differ because of inference/training numerical differences, quantization, and stale sampler weights in asynchronous training.

The paper's central diagnosis is not simply that sampled tokens are off-policy. A persistent discrepancy can create a systematic update component which feeds back as the sampler is refreshed from the trainer, accumulating drift. Eliminating all mismatch may impose a substantial throughput cost.

## 3. Mathematical mechanism

For token \(v\) at prefix \(h\), define the trainer score

\[
s_v(h)=\nabla_\theta\log p_\theta(v\mid h)
\]

and its expectation under the sampler

\[
\bar{s}(h)=\mathbb{E}_{v\sim q(\cdot\mid h)}[s_v(h)].
\]

Score centering uses

\[
\widetilde{s}_v(h)=s_v(h)-\bar{s}(h).
\]

By construction,

\[
\mathbb{E}_{v\sim q(\cdot\mid h)}[\widetilde{s}_v(h)]=0.
\]

When \(q=p_\theta\), the usual score identity gives \(\bar{s}(h)=0\), so the correction is inactive. Under mismatch, the sampler expectation of the trainer score need not be zero. Subtracting it removes the per-prefix component that can pull the trainer toward the sampler regardless of which sampled tokens earned reward.

With reward/advantage \(A\), the remaining expected update is the reward–score covariance under \(q\). **It is not generally the covariance under \(p_\theta\).** Score centering cancels the identified drift term; it does not make arbitrary off-policy data equivalent to on-policy data or universally correct every distributional discrepancy.

### Do not confuse three kinds of centering

- **Score centering:** subtracts the sampler-expected trainer score at each prefix.
- **Group reward/advantage centering:** makes advantages sum to zero across a prompt's sampled rollouts; it does not guarantee zero expected advantage at each prefix.
- **Attention-score processing:** operates on \(QK^\top/\sqrt{d_k}\) before softmax. It is unrelated to the policy score \(\nabla_\theta\log p_\theta\).

This topic is not an attention mechanism and should not be inserted into the Transformer attention chain.

## 4. Relationship to importance sampling and PPO-family corrections

Importance sampling applies multiplicative weights based on probability ratios. Clipping or masking ratios can reduce variance but may introduce or preserve bias. Score centering is an additive correction to the expected score. The paper and implementation support composing it with compatible ratio-based corrections by centering under the effective sampling mass \(q\,w\).

The implementation exposes a correction grid: token- or sequence-level ratios, a trust band, behavior outside the band (clamp/drop), and sign selection. The README maps named configurations to PG, naive IS, TIS, MIS, PPO, DAPO, GSPO, TOPR and DPPO. Important boundary: score centering composes with stat=ratio; the code explicitly rejects composition with stat=tv (DPPO's TV-based correction). Thus “composes with importance sampling” must not be generalized to every correction family.

Group-centered rewards in GRPO-style training are orthogonal to score centering; one does not substitute for the other.

## 5. Efficient estimator and implementation contract

Exact centering requires the sampler's full next-token distribution. The implementation offers:
- full-vocabulary sampler log-probabilities for exact centering;
- a top-k sampler head (README default \(k=128\));
- a tail model in which the sampler's remaining probability mass is proportional to the trainer's tail distribution, rescaled to match sampler tail mass.

The loss implementation computes trainer log-probabilities in float32, retains the sampled token's sampler log-probability even when it is outside the top-k head, uses detached sampler-derived centering weights/residuals and detached advantages/importance weights, and applies the generated-token mask. The head contribution remains differentiable; the modeled tail uses the zero-expected-score identity to avoid a full-vocabulary backward contribution.

The paper rendering reports top-32/top-128 estimates close to full-vocabulary centering in tested settings, top-128 covering more than 99.9% of sampler mass in most tested configurations, and under 1% added overhead in the authors' matched-hardware setup. This overhead was not measured for vLLM or SGLang. These are author-reported results, not independently reproduced here.

## 6. Experimental evidence and limitations

The paper reports experiments from 0.6B to 30B parameters, including quantized samplers and stale rollouts.

- In a severe Qwen3-30B-A3B-Base sampler configuration (INT8 weights/activations and INT4 KV cache), the rendering reports 30% training accuracy for score centering versus 12% for TIS, with other methods below 5%.
- “Training accuracy” here is mean reward on sampled rollouts, not held-out benchmark accuracy.
- Under a milder FP8 mismatch, plain policy gradient can remain stable; score centering is not necessarily required.
- In Qwen3-0.6B Countdown with sampler refresh every 64 steps, score centering combined with TIS/MIS performs best in the reported staleness comparison.
- Seed counts vary across some experiments; the severe 30B comparison does not have uniform replication across all methods.

The experiments support a method that can improve stability in the tested mismatch regimes. They do not establish universal superiority over importance sampling, all-engine equivalence, or generalization gains.

## 7. Placement in LLM Lab

**Primary domain:** probabilistic-foundations-training  
**Secondary domain:** inference-efficiency

Do not create a new domain merely for this paper. Reuse existing training/probability and inference-efficiency domains; add a controlled advanced topic branch only when the wider RL/post-training curriculum is reviewed.

### Proposed advanced sequence

1. Expected reward and policy-gradient objective.
2. Log-probability gradient / score function.
3. On-policy score identity and its zero expectation.
4. Behavior policy vs trainer policy; rollout staleness and training-inference mismatch.
5. Per-prefix drift and score-centering equation.
6. Difference from group-centered rewards/advantages.
7. Importance sampling, TIS/MIS and PPO-family correction grid; composition constraints.
8. Top-k approximation and vocabulary-tail model.
9. Experimental evidence, failure boundaries and diagnostics.

Prerequisites: conditional distributions, log-likelihood, gradients, sampling vs teacher-forced training, reward/advantage and policy gradient. This is an advanced post-training branch, not a new stage in the core predictive spine.

## 8. Integration decisions

| Contribution | Decision | Placement |
|---|---|---|
| Training-inference mismatch and rollout staleness | Integrate | Advanced RL/post-training context |
| Per-prefix score function and sampler expectation | Integrate | Mathematical core |
| Score-centering equation and residual covariance under q | Integrate with caveat | Advanced method lesson |
| Difference from group reward centering | Integrate | GRPO/advantage comparison |
| IS composition and stat=ratio constraint | Integrate by reference | Correction-method comparison |
| Top-k tail approximation and stop-gradient contract | Integrate in deep dive | Implementation |
| Experimental comparisons | Integrate with explicit metric/seed caveats | Evaluation |
| Cameron Wolfe's distinctive explanations | Defer | Article body not retrieved |

No learner-facing bilingual page or canonical graph concepts are added in this pass: first inspect existing RL, policy-gradient, PPO/GRPO, importance-sampling and training/inference pages/registries, then reuse their IDs and avoid duplicate ontology.

## 9. Integration completed

- Added bilingual advanced lesson pages: `site/fr/score-centering.qmd` and `site/en/score-centering.qmd`.
- Added six reusable concepts: policy gradient, score function, off-policy RL, training-inference mismatch, score centering, and importance sampling; linked them using existing relation types.
- Added both pages to the Deepen maps and Quarto render/sidebar configuration.
- Left the core guided route and canonical computational graph unchanged; the topic is an advanced optimization method, not a new forward-pass stage.

## 10. Remaining work

1. Retrieve the actual Cameron Wolfe Substack body through a functioning canonical or author-provided route; compare its added pedagogical value with the paper. Keep its record partially scanned until then.
2. Obtain the canonical arXiv PDF and audit all derivation assumptions, appendices, complete experiment tables and figure captions against the alphaXiv rendering.
3. Run the official repository's CPU test suite and add a small independent numerical check for the zero sampler-expected centered score; do not claim reproduction of large-scale results.
4. Inspect the existing LLM Lab curriculum/registries for RL, PPO/GRPO, importance sampling and training-inference mismatch before creating any page, concept ID, graph edge or route entry.
5. Consider [On the Origin and Evolution of Training-Inference Mismatch in LLM Reinforcement Learning](https://arxiv.org/abs/2610.40945) as a separate follow-up source: its distinction between numerical discrepancy and policy lag suggests a useful boundary/limitation review, not a silent extension of this paper's claims.

## References

- [Cameron R. Wolfe — Score Centering](https://cameronrwolfe.substack.com/p/score-centering)
- [Marek & Ryabinin — arXiv:2609.20807](https://arxiv.org/abs/2609.20807)
- [Full-text rendering inspected — alphaXiv](https://www.alphaxiv.org/abs/2609.20807)
- [Official implementation README](https://github.com/martin-marek/score-centering)
- [Official loss implementation](https://github.com/martin-marek/score-centering/blob/main/losses.py)
- [Related follow-up — arXiv:2610.40945](https://arxiv.org/abs/2610.40945)
