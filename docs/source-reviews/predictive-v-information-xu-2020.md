# Source review: predictive V-information — Xu et al. (ICLR 2020)

**Source:** Yilun Xu, Shengjia Zhao, Jiaming Song, Russell Stewart and Stefano Ermon, [A Theory of Usable Information under Computational Constraints](https://arxiv.org/abs/2002.10689).  
**Conference:** ICLR 2020.  
**Review date:** 16 November 2026.

## 1. Executive synthesis

The paper gives a formal, model-class-relative account of predictive information. Instead of asking only how statistically dependent \(X\) and \(Y\) are, it asks how much a specified family of predictors can improve its expected prediction of \(Y\) when it receives \(X\).

This is not a replacement for Shannon mutual information in all settings. The predictive family \(\mathcal V\), its loss, and the information supplied to the predictor are part of the quantity's definition. The framework is useful precisely because it makes the observer's predictive restrictions explicit.

## 2. Definitions

A predictive family is a set of probabilistic functions \(f:\mathcal X\cup\{\varnothing\}\to\mathcal P(\mathcal Y)\) satisfying **optional ignorance**: for every distribution \(P\) in the range of any family member, there is a family member that outputs \(P\) regardless of whether \(X\) is supplied.

With logarithmic loss:

\[
H_{\mathcal V}(Y\mid X)
=\inf_{f\in\mathcal V}\mathbb E_{(X,Y)}[-\log f[X](Y)]
\]

and the no-side-information baseline is:

\[
H_{\mathcal V}(Y\mid\varnothing)
=\inf_{f\in\mathcal V}\mathbb E_Y[-\log f[\varnothing](Y)].
\]

The predictive information is:

\[
I_{\mathcal V}(X\to Y)
=H_{\mathcal V}(Y\mid\varnothing)-H_{\mathcal V}(Y\mid X).
\]

Under optional ignorance, the population quantity is non-negative. If \(\mathcal V\) is unrestricted, it reduces to Shannon mutual information. Restricted families yield a class-relative predictive measure and can be directional.

## 3. What the paper establishes — and what must not be inferred

- **Established in the paper:** the formal definitions, elementary properties (including non-negativity and independence under the stated conditions), special cases such as Shannon mutual information and linear-regression \(R^2\), and PAC-style estimation bounds under bounded-log-loss and complexity assumptions.
- **Not assumption-free:** changing \(\mathcal V\) changes the question and potentially the numerical answer. Values from different families are not directly comparable unless their setup is made explicit.
- **Finite-sample caution:** the paper's empirical estimator and guarantees depend on the complexity of the function family. Too much capacity can overfit; too little capacity can miss a real dependency.
- **No automatic architecture ranking:** the definition does not prove that self-attention is more efficient than bag-of-words, nor that a particular Transformer extracts more V-information on an arbitrary dataset. That requires an explicit task, predictive families, held-out protocol and uncertainty analysis.
- **No synonymy with mutual information:** Shannon MI is recovered for an unrestricted family. A restricted family measures usable predictability relative to that observer, not the total statistical dependence.

## 4. LLM Lab's controlled example

LLM Lab implements a finite family of conditional categorical predictors and computes its population risks exactly on a known binary joint distribution. The family explicitly includes constant versions of every output distribution, enforcing optional ignorance.

For balanced binary variables with \(P(X=Y)=0.9\):

- a family containing the matching context-dependent predictor achieves \(1-h_2(0.1)\approx0.531\) bits;
- a constant-only family achieves zero predictive information on the same data;
- an independent feature also achieves zero.

This example isolates the role of the predictive family. It is deliberately small and exact: no model is fitted, no sample estimate is used, and no claim about neural architectures follows.

Run it with:

    uv run --locked python experiments/information-theory/v_information.py

## 5. Teaching decision

Add predictive \(\mathcal V\)-information as an advanced supporting concept, not as a core replacement for mutual information. The first learning resource is the bilingual controlled experiment guide. A future architecture-level study should compare pre-registered model families on held-out data, report log-loss baselines and confidence intervals, and account for model selection and computational budget.

## 6. Primary source

Xu, Y., Zhao, S., Song, J., Stewart, R. and Ermon, S. (2020). [A Theory of Usable Information under Computational Constraints](https://arxiv.org/abs/2002.10689). ICLR 2020.
