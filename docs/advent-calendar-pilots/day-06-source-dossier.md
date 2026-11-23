# Day 06 source dossier — sine waves, Fourier features and word order

**Status:** revised source dossier for Pilot A  
**Date:** 2026-11-23

## Editorial question

What does a sine wave have to do with word order?

The story's center is a shared representation idea: map a scalar coordinate to a vector of sinusoidal features at multiple frequencies. Transformer positional encoding is one application; Fourier feature mappings for coordinate-based MLPs are the adjacent mathematical connection.

## Primary sources and supported claims

### 1. Vaswani et al. (2017)

**Reference:** Ashish Vaswani et al., *Attention Is All You Need*, arXiv:1706.03762, Section 3.5.  
https://arxiv.org/abs/1706.03762

Supports:
- the original Transformer adds positional encodings to token embeddings;
- the encoding uses sine and cosine functions at different frequencies;
- the wavelengths form a geometric progression;
- the authors hypothesize that fixed offsets may be represented by linear transformations of the encoding;
- the authors state that sinusoidal encodings may allow extrapolation to longer sequence lengths.

Editorial constraint:
- the paper states a motivation/hypothesis, not a universal guarantee of extrapolation;
- the current canonical positional-encoding lesson already derives the formula and fixed-offset rotation property. The story must not repeat that derivation.

### 2. Rahaman et al. (2019)

**Reference:** Nasim Rahaman et al., *On the Spectral Bias of Neural Networks*, Proceedings of the 36th International Conference on Machine Learning, PMLR 97, 5301–5310, 2019.  
https://proceedings.mlr.press/v97/rahaman19a.html

Supports:
- Fourier analysis reveals a learning bias toward low-frequency functions in the deep ReLU networks studied;
- the bias appears as frequency-dependent learning speed: lower-frequency components are learned earlier;
- the paper also studies the interaction between spectral bias and data-manifold geometry.

Editorial constraint:
- describe a learning preference/speed, not an inability to represent high frequencies;
- qualify the result by the network families and settings studied;
- do not present spectral bias as a universal law for every architecture, dataset or optimizer.

### 3. Tancik et al. (2020)

**Reference:** Matthew Tancik et al., *Fourier Features Let Networks Learn High Frequency Functions in Low Dimensional Domains*, NeurIPS 2020.  
https://proceedings.neurips.cc/paper/2020/hash/55053683268957697aa39fba6f231c68-Abstract.html  
https://arxiv.org/abs/2006.10739

Supports:
- sinusoidal/Fourier feature mappings can be applied to low-dimensional input coordinates;
- in the settings studied, the mapping changes the effective neural tangent kernel and helps MLPs learn high-frequency functions;
- frequency scale/bandwidth is an important design choice;
- the choice of frequency distribution scale influences the resulting learning behaviour.

Editorial constraint:
- this paper studies Fourier feature mappings for coordinate-based MLPs, not the original Transformer's positional-encoding scheme;
- the Transformer uses a deterministic geometric frequency schedule; Tancik et al. study random Fourier feature mappings. Do not present them as the same algorithm;
- do not simplify the result to “more frequencies are always better”; the mapping bandwidth must be matched to the target problem.

## Claims used in the draft

| Claim | Evidence | Wording constraint |
|---|---|---|
| A scalar coordinate can be mapped to several sinusoidal features | Tancik et al.; elementary construction | Present the one-dimensional map as a simplified example, not the exact full paper implementation |
| Explicit frequency features make selected oscillations directly available to a linear readout | Direct derivation in the article | State the limitation applies to a linear readout over the stated feature bank, not to every nonlinear MLP |
| Deep ReLU networks in the studied settings tend to learn lower frequencies earlier | Rahaman et al. | Describe frequency-dependent learning speed and qualify architecture/problem scope |
| Fourier features can mitigate spectral bias in the studied coordinate-based MLP settings | Tancik et al. | Use “can help” and preserve the paper's task/domain scope |
| Transformer positional encoding uses fixed sinusoidal frequencies added to token embeddings | Vaswani et al. | Do not call it a Fourier transform of the sentence |
| The original sinusoidal design may help with longer positions | Vaswani et al. | Say “the authors hypothesized/motivated”; do not claim guaranteed extrapolation |

## Worked-example verification

Use:

$$
f(x)=\sin(16\pi x), \qquad x\in[0,1].
$$

This has eight cycles on [0,1]. The exact values are:

| x | 16πx | sin(16πx) |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1/32 | π/2 | 1 |
| 1/16 | π | 0 |
| 3/32 | 3π/2 | -1 |
| 1/8 | 2π | 0 |

The revised transfer challenge uses:

$$
g(x)=\sin(2\pi x)+0.2\sin(16\pi x).
$$

A linear readout with only the pair $\sin(2\pi x),\cos(2\pi x)$ cannot represent the eight-cycle component. Adding $\sin(16\pi x)$ makes both components directly accessible. This remains a statement about the specified feature bank and linear readout, not a general impossibility result for nonlinear networks.

## Visual provenance

The frequency-scale figure is an original SVG generated for this story. It contains no external image or third-party asset. Its two panels show one and eight oscillations over the same interval.

## Explicit non-claims

- The Transformer positional encoding is not a Fourier transform of a sentence.
- The fixed Transformer frequency schedule is not identical to random Fourier features.
- A sinusoidal feature bank does not guarantee that a model learns the desired relative-position rule.
- A sinusoidal feature bank does not guarantee extrapolation to arbitrary sequence lengths.
- Spectral bias is not a universal law for every architecture, dataset or training regime.
- A nonlinear MLP is not mathematically incapable of representing high-frequency functions from raw coordinates.
