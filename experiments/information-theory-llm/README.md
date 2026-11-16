# Information theory and LLMs: reproducible mini-experiment

Run from the repository root:

```bash
python experiments/information-theory-llm/run.py
uv run pytest tests/unit/test_information_theory_llm.py
```

The standard-library-only script computes entropy, cross-entropy, KL divergence and mutual information for tiny synthetic categorical distributions. It verifies (H(P,Q)=H(P)+D_{KL}(P\|Q)).

This is a numerical illustration of definitions, not an LLM experiment or an attention analysis. Mutual information is computed from an explicit joint distribution. Attention weights are input-dependent aggregation coefficients and are not themselves mutual information.

Floating-point results are approximate. No neural network, training run, real dataset or attention tensor is involved.


The script also includes a balanced-XOR example of predictive V-information. It contrasts a constant-only predictor family with a family that can represent the XOR interaction. If this predictor assigns 0.9 to the correct class and 0.1 to the other class, its expected log loss is the binary entropy h₂(0.1) ≈ 0.469 bits; the predictive gain is therefore 1 − h₂(0.1) ≈ 0.531 bits. This correctly accounts for errors and illustrates Xu et al. (ICLR 2020); it is not a neural-network benchmark or a reproduction of the paper's PAC theorem.

Primary paper: https://openreview.net/forum?id=r1eBeyHFDH (also https://arxiv.org/abs/2002.10689).
