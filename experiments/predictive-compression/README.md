# Predictive compression: a tiny reproducible experiment

## Question

Can a model that assigns higher probabilities to observed symbols help encode a sequence with fewer bits?

## What it demonstrates

A tiny **bigram model** learns conditional probabilities from a fixed synthetic training string. It assigns a probability to each symbol given the previous symbol. These probabilities define nested arithmetic-coding intervals. The script chooses a finite binary fraction inside the final interval and decodes it again.

- More predictable symbols cost fewer ideal bits.
- The sum of token surprisals is the ideal information cost: \`-sum(log2(p(token | context)))\`.
- The arithmetic coder produces a finite code; the decoder reconstructs the exact original sequence.
- A uniform four-symbol model provides a simple reference cost: 2 bits per symbol.

This is a toy model, **not a neural network or an LLM benchmark**. It does not show that a production LLM can compress arbitrary files efficiently.

## Run

From the repository root:

\`\`\`bash
python experiments/predictive-compression/run.py
\`\`\`

Only the Python standard library is required. The training data, test message, alphabet, and smoothing value are constants in the script. Exact round-trip decoding is checked at runtime.

## What to change

1. Change \`MESSAGE\` to a less predictable sequence and compare the ideal model cost with the uniform baseline.
2. Change \`TRAINING\` and observe how conditional probabilities change.
3. Change \`SMOOTHING\`; a positive value prevents unseen transitions from receiving zero probability.
4. Inspect \`interval_for\`: each observed symbol narrows the interval according to its conditional probability.
5. Inspect \`decode\`: the same model and conventions are required to recover the exact symbols.

## Interpretation and limits

- Ideal code length is measured in **bits**, using base-2 logarithms.
- The finite binary code can be slightly longer than the ideal length.
- The decoder is assumed to know the model and message length; their transmission cost is excluded.
- The model is trained and evaluated on a synthetic source; this does not measure generalization to natural language.
- Exact decoding demonstrates lossless coding for this protocol, not lossless reconstruction from an ordinary LLM prompt.
- A neural language model can supply probabilities to an entropy coder, but generation alone is not decompression.

## Connection to LLM Lab

Read the [entropy lesson](../../site/en/entropy.qmd) and [cross-entropy lesson](../../site/en/cross-entropy.qmd). The [compression synthesis](../../docs/source-syntheses/compression-two-meanings-2026-11.md) distinguishes predictive data coding from model compression and runtime-memory optimization.
