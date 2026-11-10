# Source review — sinusoidal positional encodings

**Reviewed:** 2026-11-10  
**Purpose:** select and compare pedagogical sources for the bilingual Deepen page on the original Transformer's sinusoidal positional encoding.  
**Scope:** the positional-encoding passages and directly relevant equations/code only; this is not a full review of the sources.

## Source selection and contribution

| Source | What it contributes | Editorial decision | Inspection boundary |
|---|---|---|---|
| Vaswani et al. (2017), [*Attention Is All You Need*, §3.5](https://arxiv.org/abs/1706.03762) | Canonical equations, frequency schedule, wavelength statement, and the original motivation that a fixed offset can be represented linearly. | Primary technical authority. Reconstruct the equation and derivation from it; qualify the extrapolation claim as a motivation/hypothesis, not a guarantee. | Section 3.5 inspected; the full paper was not re-audited in this pass. |
| Jay Alammar, [*The Illustrated Transformer*](https://jalammar.github.io/illustrated-transformer/) | A clear visual mental model: a toy vector, then a position-by-dimension matrix, making multi-frequency patterns visible. | Use as a link and visual-design reference. Do not copy its images. Preserve the author's July 2020 clarification: the initial visual arrangement concatenated the signals, whereas the paper interleaves sine and cosine across even and odd dimensions. | Positional-encoding section and its update inspected; embedded media rights not assessed. |
| Harvard NLP, [*The Annotated Transformer*](https://nlp.seas.harvard.edu/annotated-transformer/) | A concise PyTorch implementation that maps the equation to positions, frequency terms, alternating columns, a registered buffer, and input addition. | Use as implementation reference. Write independent code and add explicit shape, dtype, finite-buffer and property-test caveats. | Positional-encoding prose and code inspected; code not executed in this source scan. |
| Stanford EE269, [*Transformers for Signal Prediction*](https://web.stanford.edu/class/ee269/Lecture_Transformers.pdf) | Signal-processing interpretation of angular frequency, wavelength, and logarithmically spaced scales. | Use as a secondary explanation for the frequency/wavelength section, not as the original specification. | Only the indexed lecture passage was inspected; the complete PDF and surrounding lecture context were not audited. |

## Technical reconciliation

1. The paper's standard formula is interleaved:
   \[
   PE(p,2i)=\sin(p/10000^{2i/d}),\qquad
   PE(p,2i+1)=\cos(p/10000^{2i/d}).
   \]
   Here \(d=d_{\text{model}}\), and the same \(i\) indexes one sine/cosine pair.

2. Define \(\omega_i=10000^{-2i/d}\). Then the wavelength is
   \[
   \lambda_i=2\pi/\omega_i=2\pi\,10000^{2i/d}.
   \]
   With \(i=0,\ldots,d/2-1\), the largest finite-dimension wavelength is \(2\pi\,10000^{1-2/d}\), not exactly \(2\pi\cdot10000\). The paper describes the upper endpoint approximately.

3. For a fixed offset \(k\), the pair \([\sin(\omega_i p),\cos(\omega_i p)]^\top\) is mapped to the pair at \(p+k\) by a 2-by-2 matrix depending on \(k\) and that pair's frequency, but not on \(p\). The full transformation is block diagonal across pairs.

4. The positional-only dot product is \(\sum_i\cos(\omega_i(p-q))\), so it depends on the relative offset. It is not itself the learned attention score: the content embeddings are added, projected, and transformed by the network.

5. The formula is evaluable for positions beyond training. This is not equivalent to a learned model generalizing reliably to those sequence lengths. The paper's stated extrapolation motivation must not be strengthened into a guarantee.

## Pedagogical synthesis adopted

The new page uses a progression not present in any one source in full:

1. Build the sine/cosine pair as a point on the unit circle.
2. Interpret the frequency schedule and wavelength as multiple timescales; calculate a small \(d_{\text{model}}=8\) example.
3. Derive the fixed-offset linear transformation with addition identities.
4. Derive the positional-only dot product and explicitly distinguish it from \(QK^\top\).
5. Locate the addition at the input and contrast it with RoPE's Q/K rotations.
6. Translate the equations into NumPy and PyTorch, then test the shift identity.
7. Separate formula extrapolation, representation behaviour, and model generalization.

The visual matrix reading from Alammar is a useful design direction for a future original figure. It is not necessary to reproduce the source image: the formula, table, derivation and tests provide an independently checkable explanation.

## Reuse and provenance

All four sources are linked, not reproduced. No source figure, paragraph, code block, dataset, or PDF page was copied. Rights remain unknown unless the source owner states otherwise. Machine-readable source records and item-level extractions are in data/sources.yml and data/extractions/; their scan status is partial because only the relevant passages were inspected.
