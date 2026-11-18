# Predictive coding: primary-source review / Codage prédictif : revue des sources primaires

**Date:** 2026-11-18  
**Status:** three primary references catalogued and extracted; no project coder implemented or tested in this review.

## Executive decision / Décision

The source chain now supports a carefully scoped bridge between predictive log loss and lossless coding, but not an identity between a model's NLL and the byte length of an arbitrary compressed file.

1. Shannon establishes the asymptotic entropy limit for lossless coding of a discrete source and gives a finite-block construction with integer code lengths.
2. Rissanen and Langdon develop arithmetic coding as a finite-state family, relating ideal probability-derived lengths to code construction while treating finite precision and decodability as separate technical requirements.
3. Witten, Neal and Cleary provide an operational model-based arithmetic coder: the decoder must reproduce the same conditional distribution in the same context; termination and finite-precision implementation are explicit parts of the protocol.

The next experiment should implement one deliberately small deterministic coder/decoder, not reproduce all three papers. It should use a shared conditional probability table and explicit integer-frequency quantization. The ideal NLL, emitted payload bits, final byte count and framing/termination overhead must be reported separately.

## 1. Shannon (1948)

**Source:** Claude E. Shannon, “A Mathematical Theory of Communication,” *The Bell System Technical Journal*, 27(3), 379–423, July 1948. DOI: [10.1002/j.1538-7305.1948.tb01338.x](https://doi.org/10.1002/j.1538-7305.1948.tb01338.x).  
**Primary text inspected:** accessible full-text PDF, Part I.

### Exact evidence

- §7, pp. 12–14, Theorems 3–6: entropy of a finite-state source is expressed through state-weighted conditional symbol entropies; Theorem 6 relates finite-context conditional entropies to the source entropy in the limit.
- §9, pp. 16–17, Theorem 9: establishes the noiseless-channel entropy rate bound and a construction approaching it.
- §9, pp. 16–17, second proof: block messages are ordered by probability and assigned binary code lengths (m_s) satisfying (log_2(1/p_s) le m_s < 1+log_2(1/p_s)). The average code length per source symbol is bounded by the block entropy approximation plus (1/N).

### Interpretation boundary

This is a source-coding theorem, not a guarantee that a finite model-conditioned file has exactly (-sum_i log_2 q(x_imid x_{<i})) bits. The finite construction uses integer code lengths; its convergence is an average/asymptotic statement. A mismatched predictor introduces cross-entropy relative to the true source, and a practical file format introduces additional protocol costs.

## 2. Rissanen & Langdon (1979)

**Source:** Jorma Rissanen and G. G. Langdon, Jr., “Arithmetic Coding,” *IBM Journal of Research and Development*, 23(2), 149–162, March 1979. DOI: [10.1147/rd.232.0149](https://doi.org/10.1147/rd.232.0149).  
**Primary text inspected:** accessible scan of the journal article.

### Exact evidence

- pp. 149–150: motivation and generalization of variable-rate noiseless coding; arithmetic code strings are treated as binary fractional quantities and recursive shift/add constructions.
- pp. 150–152, Eqs. (1)–(5): cumulative probabilities, probability-derived ideal lengths and sequence-level accumulation are discussed.
- pp. 151–152: finite-precision rational approximations are introduced to avoid unlimited precision; unique inversion/decodability is not assumed automatically.
- § “Decodability criteria,” pp. 157–159: invertibility conditions are analyzed for the described arithmetic-code family.

### Interpretation boundary

This paper is a theoretical and finite-state treatment of a family of arithmetic codes. It is not a universal specification for every modern range coder. The exact conditions depend on the paper's state, shift, augend and ordering conventions. The available scan has OCR/layout artefacts; exact equation typography should be checked against the publisher copy before quotation.

## 3. Witten, Neal & Cleary (1987)

**Source:** Ian H. Witten, Radford M. Neal and John G. Cleary, “Arithmetic Coding for Data Compression,” *Communications of the ACM*, 30(6), 520–540, June 1987. DOI: [10.1145/214762.214771](https://doi.org/10.1145/214762.214771).  
**Primary text inspected:** accessible article PDF, pp. 520–527.

### Exact evidence

- p. 520, “Data Compression”: the input string and model produce an encoded string; the decoder has access to the same model and must reproduce exactly the same next-symbol distribution in the same context to regenerate the input.
- pp. 521–522, “The Idea of Arithmetic Coding”: successive symbols narrow an interval according to model probabilities; the decoder reverses this process.
- p. 522: a distinguished EOF symbol resolves the stopping ambiguity; the worked example relates the negative logarithm of the final interval width to the accumulated ideal information cost.
- pp. 523–527, Figs. 2–3: encoder/decoder pseudocode and finite-precision integer implementation, including renormalization and finalization.
- pp. 523–524: precision growth, incremental operation, overflow/underflow and efficient model representation are identified as practical concerns.

### Interpretation boundary

This is the most useful implementation reference for the pilot. It directly justifies the shared-model contract, deterministic update rules, exact round-trip test and explicit termination. The article's historical C code is a reference, not code to copy blindly; its empirical performance was not reproduced here.

## 4. Evidence chain and project implications

| Claim | Primary support | What it supports | What it does not support |
|---|---|---|---|
| Expected source information is an entropy rate | Shannon §7, Theorems 3–6 | Source entropy and conditional-context limit | Equality between arbitrary predictor loss and source entropy |
| Lossless coding approaches the entropy limit | Shannon §9, Theorem 9 | Asymptotic/average source-coding bound | Exact finite-file byte count |
| Probability products induce additive ideal lengths | Rissanen–Langdon pp. 150–152; Witten–Neal–Cleary pp. 521–522 | Negative log probability as ideal interval/code cost | A complete protocol from a list of floating-point probabilities alone |
| A practical decoder reconstructs the input | Witten–Neal–Cleary pp. 520–527 | Shared model, same context probabilities, encoder/decoder algorithm | Compatibility when model quantization or update order differs |
| Finite precision and termination matter | Rissanen–Langdon pp. 151–152, 157–159; Witten–Neal–Cleary pp. 522–527 | Explicit implementation constraints and decodability | Zero-overhead realization |

For an autoregressive predictor (q), the ideal sequence cost is:

[
L_q(x_{1:n})=-sum_{i=1}^{n}log_2 q(x_imid x_{<i}).
]

This is a model-assigned ideal cost. To encode losslessly, encoder and decoder must agree on tokenization, vocabulary/support, context initialization, model parameters, probability quantization, symbol ordering, integer-frequency construction, update rules and termination/framing. In a finite coder, quantized frequencies may induce a coding distribution different from the original floating-point (q); therefore report both the original-model NLL and the coder's effective quantized-model cost.

## 5. Experiment contract / Contrat expérimental

The next implementation should:

1. Use a small finite alphabet and a deterministic conditional probability table (q(x_imid x_{<i})), preferably a first-order Markov model.
2. Convert each conditional row into deterministic integer cumulative frequencies with a declared total and a positive frequency for every symbol that may occur.
3. Use the same table, quantization, context update and termination convention in encoder and decoder.
4. Encode and decode a fixed sequence; assert exact byte/symbol reconstruction.
5. Report separately:
   - floating-point ideal NLL under the declared (q);
   - effective ideal cost under the quantized coder probabilities;
   - emitted payload bit count;
   - final serialized byte count;
   - termination, padding, length/header and framing overhead.
6. Test invalid/out-of-support symbols, zero-probability handling, deterministic repeatability, empty/single-symbol messages and boundary cases.
7. Keep zlib as a distinct baseline; do not call it a model-conditioned coder.

No canonical concept relation is added by this review. The evidence-bearing bridge remains in source extractions and the audit until the coder experiment and claim/provenance representation are reviewed.
