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

The JSON output records the distributions, units, metrics and ideal code lengths. The calculation is deterministic and uses synthetic probabilities only; it does not train or evaluate an LLM.

**Interpretation boundary.** Ideal lengths are real-valued information quantities, not a complete finite code construction. Actual codes have integer lengths and overhead; entropy is an asymptotic lower bound under source-coding assumptions. This experiment demonstrates identities, not model intelligence, generalization or a universal entropy of language.
