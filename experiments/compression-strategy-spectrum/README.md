# Sequential structure and predictive compression — toy experiment

## Question

Does a predictive model that uses symbol order exploit regularities that a model based only on marginal frequencies cannot see?

## Protocol

1. Generate a sequence from a simple deterministic rule over a finite alphabet.
2. Hold out a contiguous test segment; do not shuffle train/test boundaries.
3. Fit two baselines: a smoothed unigram model and a smoothed bigram model.
4. Permute the corpus while preserving marginal symbol frequencies, then retrain and reevaluate.
5. Report cross-entropy in bits/token across multiple seeds.

## What this experiment can show

It illustrates that sequential dependencies can improve held-out prediction and that permutation can destroy those dependencies while preserving marginal symbol frequencies.

## What it cannot show

- It does not calculate Finzi et al.'s formal epiplexity measure.
- It does not measure understanding, consciousness, or subjectivity.
- It does not prove that LLMs indiscriminately learn noise or that narrative compression is superior.
- It does not establish an equivalence between An/Fn monoids and neural networks.

## Run

From the repository root:

~~~bash
python experiments/compression-strategy-spectrum/run.py
uv run pytest tests/unit/test_compression_strategy_spectrum.py
~~~

The script uses only the Python standard library. Its outputs are reproducible synthetic measurements, not language-model benchmarks.
