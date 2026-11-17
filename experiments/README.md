# Experiments

Store small, reviewable experiment definitions here—not model weights, raw datasets, or large generated outputs.

Each experiment should include a stable identifier, hypothesis, baseline, configuration, command, data provenance, metrics, environment, results, and limitations. Follow [the experiment protocol](../docs/experiment-protocol.md).

Current reproducible examples include [information theory: entropy, cross-entropy, KL and coding](information-theory/README.md), [synthetic decoding distributions](decoding-distribution/README.md), [predictive compression](predictive-compression/README.md), and [soft-target distillation](soft-target-distillation/README.md) (with a [French guide](soft-target-distillation/README.fr.md)). The [Hugging Face Jobs remote-training recipe](huggingface-jobs/README.md) (and [French version](huggingface-jobs/README.fr.md)) documents an optional managed-GPU workflow; it is a static source-based recipe, not a reproduced experiment.

Suggested layout:

```text
experiments/
  README.md
  configs/
  scripts/
```

Prefer configurations and scripts that call reusable code from `src/llm_lab`. Notebooks can explain an experiment, but should not be the only place where critical logic exists.
