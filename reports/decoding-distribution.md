# Synthetic decoding distribution: temperature and top-k

**Question and baseline.** For fixed synthetic logits `[2, 1, 0, -1]`, compare temperature 0.5 and 2.0 and top-k=2 against temperature 1.0 without truncation. The expectations and reproducible command are in the [experiment](../experiments/decoding-distribution/README.md). There is no dataset, tokenizer, checkpoint, fitted model, random sampling, or data split.

**Measurements.** Entropy is calculated after any truncation and renormalization; retained mass is measured on the original temperature-scaled distribution before top-k renormalization. The recorded [machine-readable output](decoding-distribution.json) includes the full probabilities and environment (Python 3.12.12, NumPy 2.5.4, macOS arm64). Runtime was not measured; no performance claim is made.

| Temperature | Top-k | Entropy (nats) | Retained mass |
|---:|---:|---:|---:|
| 0.5 | none | 0.4554 | 1.0000 |
| 1.0 | none | 0.9475 | 1.0000 |
| 2.0 | none | 1.2451 | 1.0000 |
| 1.0 | 2 | 0.5822 | 0.8808 |

**Observation.** For this vector, the colder distribution has lower entropy and the hotter one has higher entropy. Top-k removes two tokens and renormalizes the remaining 88.08% of baseline mass. These results match the pre-specified directional expectations.

**Limits.** This is a deterministic, single-input illustration; repetition cannot supply statistical uncertainty about other inputs. It says nothing about generated-text quality, factuality, model calibration, real token frequencies, or how a trained model behaves. A broader claim would require a defined model, representative inputs, data provenance, evaluation metrics and uncertainty analysis. No conclusions are drawn from the randomly initialized GPT.
