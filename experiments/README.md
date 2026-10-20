# Experiments

Store small, reviewable experiment definitions here—not model weights, raw datasets, or large generated outputs.

Each experiment should include a stable identifier, hypothesis, baseline, configuration, command, data provenance, metrics, environment, results, and limitations. Follow [the experiment protocol](../docs/experiment-protocol.md).

Suggested layout:

```text
experiments/
  README.md
  configs/
  scripts/
```

Prefer configurations and scripts that call reusable code from `src/llm_lab`. Notebooks can explain an experiment, but should not be the only place where critical logic exists.
