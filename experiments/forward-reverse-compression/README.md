# Forward/reverse compression and model-description cost

## Question

Does reversing a sequence systematically change its compressed size, and does including a model-description charge change which predictive model is preferred?

This experiment deliberately separates two questions:

1. **Codec directionality:** for the exact same bytes and compressor settings, compare a sequence with its byte-reversed form.
2. **Two-part model selection:** on a synthetic stationary Markov source, compare IID and first-order Markov predictors using test-data code length alone and after adding an explicit model-description charge.

It does **not** reproduce the article's enwik8 numbers and does not test a universal law of causality.

## Run

From the repository root:

```bash
python experiments/forward-reverse-compression/run.py
python experiments/forward-reverse-compression/run.py --csv
uv run pytest tests/unit/test_forward_reverse_compression.py
```

Only the Python standard library is required. Defaults are eight paired seeds, 16,384 symbols per sequence, alphabet bytes 0–3, and zlib level 9, bzip2 level 9, and XZ/LZMA preset 6. The script prints exact per-seed rows with `--csv`; the normal view reports paired mean/median size differences and the fraction of seeds where forward is smaller.

## Synthetic controls

- **IID uniform:** independent equiprobable symbols.
- **Stationary first-order Markov:** probability 0.9 of repeating the previous symbol, otherwise uniformly choose one of the other three.
- **Non-stationary regime shift:** the stay probability changes from 0.98 in the first half to 0.55 in the second half. This is an explicit time-inhomogeneous control, not a model of causality.

Each generated sequence is reversed at the byte/symbol level. Every codec receives the same payload bytes and fixed settings in both directions. Compression headers and format overhead are included in the measured output size.

## Two-part MDL illustration

A separate, fixed-seed Markov sequence is split in half. The first half is training context and the second half is held-out test data; the reversed sequence is evaluated with the same protocol. Two predictors are fit on the training half:

- IID: one four-symbol probability table.
- First-order Markov: one four-symbol next-symbol table for each previous symbol.

Counts receive additive-one smoothing and are quantized to positive integer frequencies summing to 255. Test-data cost is the ideal Shannon length under those quantized probabilities, in bits. A deliberately transparent fixed-width parameter charge is then added: one model-family bit plus eight bits per stored table entry (33 bits for IID, 129 bits for bigram). This makes the accounting visible; it is **not** an optimal parameter code and the fractional Shannon lengths are not an emitted arithmetic-coded stream.

The score is conditional on the training prefix being available as learning context. The model table is charged as if it must be described to a decoder. This is an educational two-part MDL approximation, not a complete end-to-end compressor or a claim that these particular parameter costs are universally optimal.

## Interpretation

- Positive `reverse_minus_forward_bytes` means the forward payload compressed to fewer bytes for that seed and codec; negative means reverse did.
- Report the paired distribution, not just one seed or a cherry-picked compressor.
- If IID and stationary Markov controls show small/no consistent directionality, that is a useful negative control.
- Any directional advantage on the non-stationary source can arise from the regime boundary, finite context, compressor implementation, initialization, and framing. It does not establish causal direction as a general property.
- The stationary source has the same underlying entropy rate in either temporal direction. A finite compressor may still exhibit finite-sample or implementation asymmetry.
- The MDL comparison illustrates why data fit alone can prefer a more elaborate model while a model-plus-data score charges for complexity. It does not prove generalization or identify the true model.

## Limitations

- Synthetic four-symbol data are not natural language and do not reproduce enwik8.
- Eight seeds are a small controlled demonstration, not a population-level statistical study.
- Codec implementations and output sizes may vary across Python/runtime versions; record Python and zlib/liblzma/bz2 versions when publishing results.
- The regime-shift source is intentionally non-stationary; results depend on the split and transition probabilities.
- The fixed-width model code is pedagogical and intentionally simple. A production MDL study should compare defensible universal codes, prequential coding, or Bayesian marginal likelihood and account for all side information and compute/update costs.
- No causal inference or general intelligence claim follows from compressed byte counts.

## Connection to the source review

The experiment operationalizes the review's recommendation to separate sequential order, compressor behavior, and model description cost. It tests a narrow reproducible claim without treating compression asymmetry as proof of causal structure.
