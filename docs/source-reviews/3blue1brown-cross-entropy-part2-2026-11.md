# 3Blue1Brown Part 2 — pedagogical integration review

Date: 2026-11-16

## Verdict

The core cross-entropy mathematics was already integrated well in LLM Lab. The source's main added value is not another definition or another one-hot NLL derivation; it is the pedagogical bridge from a mismatched codebook to language-model loss, plus the constrained-optimization rationale and a more concrete teacher/student distillation story.

## Audit of existing coverage

- `site/fr/cross-entropy.qmd` / `site/en/cross-entropy.qmd`: general target distribution, one-hot NLL, logit expression, target alignment, causal masking, valid-token masking, reductions, stable implementation and visual one-token comparison.
- `site/fr/language-modeling-math.qmd` / `site/en/language-modeling-math.qmd`: autoregressive factorization, soft targets, (H(q,p)=H(q)+D_{KL}(q||p)), KL directionality and zero-support edge case.
- `site/fr/loss.qmd` / `site/en/loss.qmd`: batch aggregation, perplexity and distinction between objective and metrics.
- `site/fr/llm-evolution.qmd` / `site/en/llm-evolution.qmd`: model compression and a brief mention of distillation.
- `data/concepts.yml`: canonical concepts already exist for cross-entropy, KL divergence, negative log-likelihood, model compression and knowledge distillation.

## New value integrated

1. Operational cross-entropy: average cost of code lengths built from (p) when data follow (q).
2. Four-symbol example: (p=(1/2,1/4,1/8,1/8)), (q=(1/8,1/8,1/4,1/2)), (H(q,p)=2.625) bits, (H(q)=1.75) bits, KL excess (0.875) bit/symbol.
3. Notation mapping: video (P=) data and (Q=) model; project (q=) target/data and (p=) prediction.
4. Lagrange-multiplier derivation of negative log under explicit assumptions.
5. Distillation as cross-entropy from a teacher's full distribution to a student's output, with teacher imperfections explicitly noted.

## Deliberately not added

- No duplicate cross-entropy core lesson.
- No new canonical concept for a synonym of existing cross-entropy or KL.
- No new gzip experiment before reviewing the original language-tree paper and defining a defensible protocol.
- No temperature-scaled distillation formula: the video segment does not specify a general temperature convention, and practical variants differ.
- No claim that the student's performance is bounded by or guaranteed to match the teacher in every downstream setting.

## Graph changes

- Reuse existing `knowledge-distillation`, `cross-entropy`, `kl-divergence` and `model-compression` concepts.
- Add the advanced language-modeling mathematics pages as resources for cross-entropy and knowledge distillation.
- Add a pedagogical prerequisite edge from cross-entropy to knowledge distillation.

## Validation still required

Schema validation for source/extraction, concept graph validation, bilingual Quarto rendering and link checks, repository tests and CI on the final PR head. The source review does not claim browser visual review or learner validation.
