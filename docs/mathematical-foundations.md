# Mathematical foundations

This document is a working checklist. Derivations should be added alongside implementations and numerical tests.

## Tensor shapes first

For a batch of token sequences, a common shape convention is:

- token IDs: `(batch, sequence_length)`
- token embeddings: `(batch, sequence_length, d_model)`
- query/key/value projections: commonly `(batch, heads, sequence_length, head_dim)`
- vocabulary logits: `(batch, sequence_length, vocabulary_size)`

State the convention at each function boundary; do not rely on shape intuition alone.

## Softmax and cross-entropy

For logits (z \in \mathbb{R}^C), softmax maps logits to probabilities:

\[
p_i = \frac{\exp(z_i)}{\sum_{j=1}^{C}\exp(z_j)}.
\]

For a target class (y), cross-entropy is:

\[
\mathcal{L}(z,y) = -\log p_y.
\]

A numerically stable implementation subtracts the maximum logit before exponentiation. For a single example, the derivative with respect to logits is:

\[
\frac{\partial \mathcal{L}}{\partial z_i} = p_i - \mathbb{1}[i=y].
\]

For a batch, explicitly define whether the loss is summed or averaged; gradient scale depends on that choice.

## Gradient verification

For parameter (\theta_i), a central finite-difference approximation is:

\[
g_i^{\mathrm{num}} = \frac{\mathcal{L}(\theta_i + \epsilon) - \mathcal{L}(\theta_i - \epsilon)}{2\epsilon}.
\]

Compare numerical and analytical gradients with absolute and relative tolerances. Finite differences are a diagnostic, not a substitute for derivation; results depend on scale, precision, and the chosen (\epsilon).

## Attention

Scaled dot-product attention is:

\[
\operatorname{Attention}(Q,K,V) =
\operatorname{softmax}\left(\frac{QK^\top}{\sqrt{d_k}} + M\right)V,
\]

where (M) masks positions that must not be attended to. For causal language modeling, future positions must be inaccessible. Test this behavior directly by changing future tokens and checking that earlier-position outputs remain unchanged.

## Optimization checklist

Before trusting a training curve, check:

- the loss is finite and the reduction is understood;
- gradients are finite and have expected shapes;
- a tiny batch can be overfit as a pipeline sanity check;
- train and validation sets are separated before learned preprocessing;
- validation is not repeatedly used as an unbiased final test;
- the seed, optimizer, schedule, batch size, and stopping rule are recorded.
