# Source review — “Intelligence and compression” (lewish.io)

**Source:** [Canonical article](https://lewish.io/posts/intelligence-and-compression) · [structured extraction](../../data/extractions/lewish-intelligence-and-compression-2025.yml)  
**Displayed publication date:** 2025-05-28 · **Accessed:** 2026-11-17  
**Attribution:** the page/site identity is lewish.io; a fuller author identity was not independently verified.  
**Scan boundary:** article text and visible footnotes were retrieved from the canonical HTML. Figures, code/data, comments, outbound links, revision history and reuse rights were not fully inspected. Text and media remain link-only.

## Executive synthesis

This is a useful conceptual bridge from predictive compression to model selection and agent-level accounts of intelligence. Its strongest contribution is the **two-part description-length framing**: a model helps compress observations, but the model itself also has a cost. This makes the connection to Minimum Description Length (MDL) explicit and prevents the model from being treated as free.

The article then extends the picture in three directions: temporal/causal prediction, the efficiency of updating a model, and action-oriented frameworks (AIXI and active inference). These extensions are valuable as optional perspectives, not as proof that compression is equivalent to intelligence.

## 1. Contribution map and integration decisions

| Contribution | Assessment | Decision |
|---|---|---|
| Musician chunks notes into learned structures | Strong intuition for priors and domain expertise; analogy, not a measurement | Keep as optional analogy in synthesis |
| Conditional data cost + model description cost | Standard two-part MDL perspective; clarifies why memorization is not free | Integrate into living synthesis |
| Predictive probabilities → variable-length code | Correct principle; article's unary-like code is illustrative, not an efficient general coder | Link to canonical entropy/coding material |
| Past-to-future ordering | Important for online prediction in temporally generated environments | Clarify alongside sequential likelihood |
| Forward/reverse enwik8 table | Interesting source-reported empirical result | Mark unverified; design controlled experiment rather than repeat as established evidence |
| MDL and generalization | Useful regularization intuition, but not a guarantee or a proof of truth | Clarify assumptions and limits |
| Chollet's skill-acquisition efficiency | Adds adaptation/data/computation efficiency to static model fit | Retain as an advanced perspective |
| AIXI | Formalizes universal prediction plus reward-oriented action in an idealized agent | Link-only advanced comparison; intractability explicit |
| FEP / active inference | Offers a broader perception-action framing | Retain as an explicitly speculative/high-level perspective; do not equate surprise, variational free energy and reward |

## 2. Technical audit

### 2.1 Two-part compression and MDL

The useful formal target is a total description length such as

\[
L(M) + L(D\mid M),
\]

where the first term encodes the model and the second encodes the data under that model. The exact expression depends on the model class, coding scheme, parameters, prior and whether the formulation is batch, prequential or Bayesian. A practical account may also need to state computational and update costs; they are not automatically represented by the two terms.

This is not the same as choosing the numerically smallest neural network. A model that memorizes the sample may have a small residual but an expensive description. Conversely, a compact model can underfit. MDL is a model-selection principle relative to a specified representation and code, not a guarantee that the selected model is the one true mechanism.

### 2.2 Prediction and coding

For a sequential model, the idealized cumulative code cost is

\[
-\sum_{t=1}^{T}\log_2 q(x_t\mid x_{<t}),
\]

in bits when base-2 logarithms are used. Natural logarithms yield nats. A practical loss scalar is not automatically bits per token unless its logarithm base and averaging convention are known.

A predictor can drive arithmetic or other entropy coding, but a usable compressor also needs a synchronized decoder/model, a valid coding protocol and accounting for model/side-information overhead. The article's short prefix-style example is illustrative; its footnote correctly warns that it is not a generally efficient code and that incompressible data cannot be shortened.

### 2.3 Temporal order and the reported enwik8 comparison

The author reports smaller forward than reversed files for gzip, ppmd and zpaq. The difference is modest. The article text does not establish exact versions, options, checksums, reverse transformation details or scripts, so the numbers are source-reported rather than independently reproduced.

The interpretation should be narrow: a sequential compressor may exploit directional regularities in a corpus generated by a forward process. Reversing a file changes local contexts and boundary conditions; the result does not prove a universal causal law or that all useful structure is forward-only. A stronger experiment would use synthetic sources with known causal structure, matched non-causal controls, multiple compressors and repeated settings.

### 2.4 MDL, Kolmogorov complexity and generalization

Keep these related ideas distinct:
- practical MDL minimizes a code length within a chosen model/coding family;
- Kolmogorov complexity is the length of the shortest program for a universal description language and is uncomputable in general;
- Solomonoff induction weights computable hypotheses by description length in an idealized Bayesian mixture.

The counting argument is an intuition about model capacity and overfitting, not a standalone guarantee that every shorter model generalizes better. Generalization depends on the model class, data distribution, sample size, inductive bias, optimization and the relationship between training and deployment data.

### 2.5 Updating, AIXI and active inference

Chollet's definition concerns skill-acquisition efficiency relative to priors, experience and generalization difficulty. It adds data and computational efficiency of learning to the discussion; it is not reducible to model size or compression ratio.

AIXI combines a Solomonoff-style universal mixture over computable environment models with reward maximization. It is a theoretical idealization and is generally computationally intractable; do not present it as an implementable recipe.

The article explicitly labels its Free Energy Principle discussion as a lay interpretation. Distinguish:
- surprisal: negative log probability of an observation;
- variational free energy: a bound/objective used in approximate Bayesian inference;
- prediction error: a model-dependent residual or mismatch;
- reward/preferences: criteria that shape action selection.

Active inference is not simply an agent making the world conform to a fixed expectation. Formal accounts involve generative models, beliefs, policies, uncertainty and preferred outcomes. The proposed unification of intelligence and compression remains an interpretive thesis, not a consensus result.

## 3. Complementarity with the existing LLM Lab corpus

This source should be compared, not merged, with:
- Sourav Mukherjee's inference-efficiency article: entropy signals, KV-cache decisions and an unvalidated token-pruning hypothesis;
- 3Blue1Brown's entropy videos: visual/derivational treatment of surprisal, entropy and cross-entropy;
- Wayland Zhang: information-theoretic framing and explicit cautions about mutual information, attention and physical analogies;
- Karthik Shashidhar: LZW/predictive-compression analogies;
- David Chen: feature selection, compact representations and generation-as-decompression analogy;
- Mingdi Fan: philosophical accounts of compression and intelligence.

Distinctive contribution here: model cost plus data cost, causal ordering, adaptation efficiency, and the contrast between AIXI and active inference. The source does not warrant a new mandatory lesson or duplicate entropy concepts.

## 4. Visuals, code and provenance

The article contains a musical-score visual placement, but its actual image bytes have not been retrieved or inspected. No description, recreation or reuse is claimed. A new LLM Lab diagram may later be justified to show the two-part MDL objective or the contrast between batch compression, prequential prediction and model update, but it should be original and should not imitate or copy the article's visual.

No code or data artifact was independently inspected or executed. The forward/reverse table remains an unverified reported result. Rights are unknown.

## 5. Recommended project integration

1. Add the two-part MDL explanation to the existing comparative synthesis, not a new core page.
2. Cross-link canonical entropy, cross-entropy, predictive-compression and generalization lessons.
3. Keep the music analogy as optional pedagogy and explicitly label it as an analogy.
4. Design a reproducible synthetic forward/reverse experiment only after defining causal and non-causal generators and reporting the compressor configuration.
5. Keep AIXI and active inference in advanced comparative material; verify against primary references before any learner-facing claim.
6. Do not change the guided route or canonical concept registry on the basis of this article alone.

## Conclusion

The article adds a useful **model-plus-data** view of compression and a broader bridge from prediction to adaptation and action. Its most valuable use is to enrich the existing compression synthesis and motivate controlled experiments. The stronger thesis that intelligence is fundamentally compression, the generalization argument, the enwik8 causal interpretation and the FEP unification all require explicit qualifications. The ingestion remains partially scanned until figures, outbound resources, code/data, creator attribution and rights are checked.
