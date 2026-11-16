# Predictive entropy and surprisal: a toy experiment

## Question

Is the entropy of a distribution the same thing as the surprise of an observed event?

## Run

From the repository root:

```bash
python experiments/entropy-surprisal-toy/run.py
```

No third-party dependency is required.

## Expected result

For a binary source with P(A) = 0.99 and P(B) = 0.01:

- average entropy: about 0.0808 bits per draw;
- surprisal of A: about 0.0145 bits;
- surprisal of B: about 6.6439 bits.

The source has low average entropy, yet the rare event B is highly surprising when it occurs.

## Interpretation

Entropy is an average over a distribution; surprisal concerns a particular observed event. Neither low entropy nor low surprisal proves that a token is useless or safe to remove.

This is a minimal mathematical counterexample. It does not test an LLM, measure semantic utility, or validate a pruning method.
