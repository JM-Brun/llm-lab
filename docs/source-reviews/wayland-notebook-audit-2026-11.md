# Audit of the companion notebook — Wayland Zhang (2026)

**Audit date:** 16 November 2026  
**Notebook:** [English notebook](https://github.com/waylandzhang/information-theory-and-language-models/blob/main/information-theory-and-llm-en.ipynb)  
**Companion article:** https://waylandz.com/blog/information-theory-and-llm/  
**Audit mode:** static inspection of all 18 notebook cells, including code and saved textual outputs; the notebook was not executed in this review.

## Executive synthesis

The notebook is useful as a visual introduction to surprisal, binary entropy, mutual information and cross-entropy. It is not a reliable source of experimental evidence for the stronger claims made around attention, thermodynamics, V-information or compression. Several code cells produce illustrative visualizations, but some labels and interpretations overstate what the calculations measure.

The notebook should be linked as an optional visual companion, not copied into LLM Lab or treated as a validated experiment. The project-owned experiments now provide small deterministic checks with explicit assumptions.

## Cell-by-cell technical findings

| Notebook cells | What they do | Assessment and disposition |
|---|---|---|
| 0–3 | Introduce logarithms and binary entropy; plot \(\log_2 p\) and the binary entropy curve | Useful intuition. The plotted logarithm is \(\log_2 p\), whereas surprisal is \(-\log_2 p\); keep the sign distinction explicit. |
| 4–6 | Define Shannon mutual information and compute a weather/umbrella joint-distribution example | The discrete joint-distribution calculation is a suitable illustration. A Venn diagram is a mnemonic, not a literal geometric decomposition of random variables. |
| 7–9 | Introduce ML applications and compare target, good, bad and uniform categorical predictions | The cross-entropy/KL identity is appropriate. Adding \(10^{-10}\) inside every logarithm is an unnecessary smoothing approximation and slightly perturbs exact identities; the displayed distributions have positive support, so exact masked logarithms are preferable. “True English letter distribution” should be read as a hand-entered illustrative frequency vector, not a universal or context-independent language distribution. |
| 10–11 | Visualize attention and label a second heatmap “MI Approximation from Attention” | The right-hand matrix is **not mutual information**. For each query row, the code computes \(a_{ij}\log_2(a_{ij}/u_j)\), where \(u\) is uniform. Summing a row would give \(D_{KL}(a_i\|u)\), the divergence of that attention row from uniform; the plotted cells are only the individual summands. No joint distribution \(p(X,Y)\), marginal distributions or conditional entropy are estimated. |
| 11 | Optionally loads bert-base-uncased, otherwise uses a hand-authored attention matrix | use_model is initialized to False, so the default run always takes the simulated branch. If enabled, BERT is an encoder with bidirectional attention, not an autoregressive GPT. Its attention weights still do not estimate mutual information. The broad exception handler can also hide model-loading or runtime errors by silently switching to simulated data. |
| 12 | Describes predictive V-information and links the Xu et al. paper | The motivation is broadly right but incomplete. The formal object is defined relative to a predictive family \(\mathcal V\), logarithmic prediction risk and the optional-ignorance condition. It is not simply “a finite set of probes” in every formulation, and it is not a generic measure of computational efficiency. The paper's guarantees depend on assumptions about bounded log-probabilities and function-class complexity. |
| 13 | Connects thermodynamics to information extraction and gives an electron-ionization analogy | This does not explain Landauer's principle. Ionizing an atom is not the logically irreversible erasure operation in Landauer's bound. The subsequent claim that all information learnable from a training set is bounded by the erasure-energy argument is not established by the cited physics principle. |
| 14–16 | Connect entropy and compression; propose comparing strings with different entropy levels | The source-coding connection is valid under the relevant assumptions, but the notebook's phrase “compression is intelligence” is not a scientific equivalence. |
| 17 | Computes empirical marginal character entropy and compresses strings with zlib | This is not a fair direct test of the entropy lower bound. The entropy calculation uses only single-character frequencies (a zero-order marginal model); DEFLATE/zlib also exploits repeated substrings and sequential dependencies. The units and objects differ: bits per character versus compressed bytes for finite strings, including framing/overhead. The random string uses an unseeded global NumPy RNG, so the result is not reproducible. The text examples are short and highly repetitive. |

## The attention calculation: exact interpretation

For a query row \(i\), the notebook first normalizes the restricted attention row \(a_i\), then computes each cell:

\[
c_{ij}=a_{ij}\log_2\frac{a_{ij}}{1/n}.
\]

The row sum is:

\[
\sum_j c_{ij}=D_{KL}(a_i\|U_n),
\]

where \(U_n\) is the uniform distribution over the selected content-token positions. This measures how far one attention row is from uniform. It does **not** measure dependence between random variables, and an individual cell is not an information contribution in a mutual-information decomposition.

A valid mutual-information experiment would define a joint sampling process for variables \(X\) and \(Y\), estimate the joint and marginal distributions (or use a justified estimator), and report estimator bias, sample size and uncertainty. If the goal is to relate attention to dependence, attention should be treated as a model feature or intervention, not silently substituted for a joint distribution.

## Predictive V-information: formal correction

Xu et al. (ICLR 2020) define predictive conditional \(\mathcal V\)-entropy as the minimum expected negative log-likelihood over a predictive family:

\[
H_{\mathcal V}(Y\mid X)
=\inf_{f\in\mathcal V}\mathbb E[-\log f[X](Y)].
\]

Predictive information is the difference between the best achievable log-loss without and with side information:

\[
I_{\mathcal V}(X\to Y)
=H_{\mathcal V}(Y\mid\varnothing)-H_{\mathcal V}(Y\mid X).
\]

The predictive family must satisfy **optional ignorance**: if a predictor can output a distribution \(P\), the family also contains a predictor that outputs \(P\) regardless of whether \(X\) is supplied. This is essential to the non-negativity result. With the unrestricted family, the quantity reduces to Shannon mutual information; with a restricted family, it measures predictive usefulness relative to that family. It is directional and class-dependent.

The paper's PAC-style estimation result is not automatic: it requires bounded log-probabilities and a complexity control for the function family. The authors explicitly note the trade-off: a family that is too complex can overfit, while one that is too simple cannot represent the relationship of interest.

## Reproducible LLM Lab replacement

The project adds:

- src/llm_lab/foundations/predictive_information.py: exact finite-family calculation with validation of optional ignorance.
- tests/unit/test_predictive_information.py: tests for correlated and independent variables, a constant-only family, and invalid families.
- experiments/information-theory/v_information.py: deterministic binary example.
- experiments/information-theory/compression.py: fixed-seed, equal-length constant, IID and Markov sources; compares marginal entropy, known source entropy rate and zlib size with container overhead included.
- A bilingual section in the information-theory experiment guide and revision sheet.

The controlled distribution has \(P(X=Y)=0.9\), with balanced binary \(X\) and \(Y\). A finite family that includes a context-dependent rule obtains about \(0.531\) bits; a constant-only family obtains zero on the very same correlated distribution. An independent feature also gives zero. This is an exact population-risk calculation for a small, hand-specified family, not a trained-model benchmark or a replication of Xu et al.'s experiments.

## Operational decisions

1. Keep the notebook linked as a visual companion; do not copy its code or figures.
2. Do not label attention-to-uniform KL contributions as mutual information.
3. Do not reuse the thermodynamic argument as a statistical-learning bound.
4. Do not use marginal character entropy as a direct prediction of zlib's finite-file compression ratio; use entropy rate for dependent sources and state finite-code overhead. The deterministic replacement experiment illustrates this distinction.
5. Teach predictive V-information only with its predictive family, optional ignorance, loss, direction and estimation assumptions stated.
6. Do not infer that self-attention extracts more predictive information than bag-of-words without a controlled, held-out comparison using explicitly defined model families.

## Sources

- Wayland Zhang, [Information Theory Is All You Need (to Understand LLMs)](https://waylandz.com/blog/information-theory-and-llm/), 17 February 2026.
- Yilun Xu et al., [A Theory of Usable Information under Computational Constraints](https://arxiv.org/abs/2002.10689), ICLR 2020.
- Companion [English notebook](https://github.com/waylandzhang/information-theory-and-language-models/blob/main/information-theory-and-llm-en.ipynb).
