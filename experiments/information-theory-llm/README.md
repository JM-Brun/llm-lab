# Information theory and LLMs: reproducible mini-experiment

Run from the repository root:

```bash
python experiments/information-theory-llm/run.py
uv run pytest tests/unit/test_information_theory_llm.py
```

The standard-library-only script computes entropy, cross-entropy, KL divergence and mutual information for tiny synthetic categorical distributions. It verifies (H(P,Q)=H(P)+D_{KL}(P\|Q)).

This is a numerical illustration of definitions, not an LLM experiment or an attention analysis. Mutual information is computed from an explicit joint distribution. Attention weights are input-dependent aggregation coefficients and are not themselves mutual information.

Floating-point results are approximate. No neural network, training run, real dataset or attention tensor is involved.
