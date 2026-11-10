# Experiment protocol

Every reported result should be reproducible enough for another engineer to understand what was run and what the evidence supports.

## Required record

For each experiment, record:

1. **Question and hypothesis** — one falsifiable question, including the expected direction of an effect.
2. **Baseline** — the simplest credible comparison and why it is appropriate.
3. **Data** — source, version, license, filtering, splits, preprocessing, and known limitations. Never commit restricted or large raw datasets.
4. **Method** — model/checkpoint, tokenizer, objective, configuration, and implementation reference.
5. **Controls** — random seeds, compute device, software versions, evaluation conditions, and changes from baseline.
6. **Metrics** — primary metric chosen before comparing results, supporting metrics, and any quality/cost trade-off.
7. **Repetitions and uncertainty** — repeated runs or uncertainty estimates where feasible; explain when compute limits prevent them.
8. **Results** — machine-readable outputs plus a concise summary table or plot.
9. **Error analysis** — representative successes, failures, slices, and unexpected effects.
10. **Limitations** — confounders, possible leakage/contamination, external validity, and claims not supported by the experiment.

## Evaluation hygiene

- Split data before fitting transforms, selecting features, deduplicating with label-informed rules, or making other data-dependent decisions.
- Keep a final test set independent from iterative model and hyperparameter selection.
- For grouped data (for example, multiple samples per patient or document), split by the entity that could leak information.
- Avoid comparing models on different examples or incompatible tokenization/evaluation conventions.
- Report class balance and per-slice results when aggregate metrics can hide failure modes.
- A lower training loss alone is not evidence of better generalization.
- Record failures and negative results rather than only successful runs.

## Suggested directory convention

Use a stable experiment identifier, for example `experiments/2026-10-20-cross-entropy-gradient-check/`, with a small README/config and links to code. Do not commit checkpoints or generated datasets; keep large outputs externally and record how to retrieve them.

## Reproduction checklist

- [ ] Clean environment can be created from project metadata and lockfile.
- [ ] Commands and expected outputs are documented.
- [ ] Seed and hardware/software context are recorded.
- [ ] Data source and split logic are explicit.
- [ ] Baseline and primary metric are defined.
- [ ] Tests cover the key implementation assumptions.
- [ ] Conclusions distinguish observation, interpretation, and speculation.
