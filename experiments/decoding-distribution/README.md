# Synthetic decoding-distribution investigation

**Question:** for one fixed vector of synthetic logits, how do temperature and top-k truncation change the next-token distribution?

**Pre-specified expectations:** compared with temperature 1 and no truncation, temperature 0.5 reduces entropy, temperature 2 increases it, and top-k=2 removes two entries and retains less than all of the baseline probability mass before renormalization. Entropy is measured in natural-log units; retained mass is measured under the untruncated distribution. This is a deterministic calculation, with no sampling or train/test data.

From the repository root after `uv sync --locked --dev`:

```bash
uv run --locked python experiments/decoding-distribution/run.py
```

The script emits JSON containing the input, settings, probabilities, entropy, retained mass and runtime environment. The [report](../../reports/decoding-distribution.md) records one run and its limits. Floating-point output and environment metadata can differ slightly across platforms.

The runner models each configuration as a `DecodingScenario` and each result as a `DecodingMeasurement`. `run_experiment` evaluates the scenarios and returns an `ExperimentReport`; the command-line entry point serializes that report as JSON.
