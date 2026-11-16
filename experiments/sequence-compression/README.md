# Sequence compression: reproducible entropy vs zlib comparison

Run from the repository root:

```bash
python experiments/sequence-compression/run.py
uv run pytest tests/unit/test_sequence_compression.py
```

The script generates three deterministic 20,000-symbol sequences over A/B/C/D: a repeated motif; a first-order Markov source with probability 0.9 of repeating the previous symbol; and an IID uniform source generated with seed 20261116.

It reports empirical marginal entropy H0, first-order conditional entropy H1, and actual zlib output size in bits per symbol. H1 captures one-step dependencies that a memoryless model misses.

Limitations: empirical plug-in entropies have finite-sample bias; H1 only captures one-step dependencies; zlib uses a richer LZ77/DEFLATE-style mechanism and adds framing/codec overhead. This is a reproducible teaching comparison, not proof that zlib reaches the entropy rate or a benchmark of LLM compression.
