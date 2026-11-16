# Information theory: entropy, cross-entropy, KL and coding

**Question.** How do target uncertainty, model mismatch and idealized code length relate for a small categorical prediction problem?

**Pre-specified checks.**
- For q = [0.5, 0.5] and p = [0.75, 0.25], H(q,p) = H(q) + KL(q || p).
- The target entropy is 1 bit; cross-entropy and KL are reported in both bits and nats.
- For a one-hot target, cross-entropy equals the negative log probability of the observed outcome.
- Ideal code lengths are -log2(p_i); their expectation under q equals cross-entropy in bits.

Run from the repository root:

```bash
uv run --locked python experiments/information-theory/run.py
```

The JSON output records the distributions, units, entropy, cross-entropy, KL, perplexity and ideal code lengths. It also makes the expected ideal code length explicit and checks the one-hot NLL/perplexity special case. The calculation is deterministic and uses synthetic probabilities only; it does not train or evaluate an LLM.

**Interpretation boundary.** Ideal lengths are real-valued information quantities, not a complete finite code construction. Actual codes have integer lengths and overhead; entropy is an asymptotic lower bound under source-coding assumptions. This experiment demonstrates identities, not model intelligence, generalization or a universal entropy of language.


## Predictive V-information extension

Run the separate finite-family example:

```bash
uv run --locked python experiments/information-theory/v_information.py
```

It computes population log-loss minima exactly for a finite predictive family that includes constant predictors for every output distribution (optional ignorance). The correlated feature gives about 0.531 bits to the feature-aware family; an independent feature and a constant-only family give zero. This isolates the model-class dependence of predictive V-information without training a model or estimating it from samples. See the bilingual experiment guide for the assumptions and interpretation limits.


## Entropy rate and finite compression

Run the deterministic source-coding comparison:

    uv run --locked python experiments/information-theory/compression.py

It generates constant, IID-uniform and symmetric first-order Markov sources over the same four-symbol alphabet, using a fixed seed and equal sequence lengths. It reports source entropy rate, empirical marginal entropy, and zlib size in bits per symbol including container overhead. For the Markov source, the stationary marginal entropy is close to 2 bits per symbol while the entropy rate is lower because successive symbols are dependent. This corrects the notebook's mismatch between marginal character entropy and a dependency-aware compressor. The output is a finite implementation comparison, not a proof of the asymptotic source-coding theorem.
