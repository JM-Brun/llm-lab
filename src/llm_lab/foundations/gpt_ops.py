"""Numerical building blocks of the reference decoder-only GPT.

This module gathers the small, self-contained operations that every
Transformer block repeats: weight initialization, linear projections,
layer normalization and the GELU activation. Keeping them here, away
from the model classes, has two benefits:

1. **Each operation is testable alone.** A bug in ``layer_norm`` is caught
   by a two-line unit test, not by debugging a full model forward pass.
2. **The model files read like architecture.** ``transformer_block``
   states *that* a block applies attention then an MLP; the *how* of each
   elementary operation lives in this file.

All functions exchange float64 NumPy arrays (alias :data:`FloatArray`).
float64, not float32, keeps results exact enough to hand-check on paper;
the cost in speed is irrelevant at reference scale.

Line-by-line walkthrough (bilingual site pages):
- https://jm-brun.github.io/llm-lab/fr/gpt-ops-walkthrough/
- https://jm-brun.github.io/llm-lab/en/gpt-ops-walkthrough/

Related concept pages (architecture and tensor shapes):
- https://jm-brun.github.io/llm-lab/fr/transformer/
- https://jm-brun.github.io/llm-lab/en/transformer/
"""

import math

import numpy as np
from numpy.typing import NDArray

# Shared type alias for the whole reference implementation: every
# operation takes and returns float64 arrays.
FloatArray = NDArray[np.float64]


def _init_matrix(
    rng: np.random.Generator,
    shape: tuple[int, int],
    std: float = 0.02,
) -> FloatArray:
    """Draw a weight matrix from a zero-mean normal distribution.

    Why small values?
        With ``std=0.02`` (the GPT-2 convention), initial activations stay
        close to the scale of the embeddings, so a randomly initialized
        model neither saturates nor explodes on its first pass. The value
        is a convention, not a law: training could tune it, or use a
        scaled scheme (``transformer_block`` applies exactly such a
        variant to weights that feed a residual path).

    Args:
        rng: Seeded NumPy generator. The caller owns the generator, which
            is what makes whole-model initialization reproducible from a
            single seed.
        shape: Target ``(rows, columns)`` of the matrix.
        std: Standard deviation of the normal draw.

    Returns:
        A float64 array of the requested shape.
    """
    return np.asarray(rng.normal(0.0, std, shape), dtype=np.float64)


def _init_linear(
    rng: np.random.Generator,
    out_features: int,
    in_features: int,
    std: float,
) -> tuple[FloatArray, FloatArray]:
    """Initialize one linear layer: weight ``(out, in)`` and zero bias.

    Why a zero bias?
        At initialization the layer should be a pure (small) linear map:
        a non-zero bias would shift every activation by a constant before
        the model has learned anything. Zero biases also keep the
        parameter count honest in ``GPT.num_parameters``.

    Args:
        rng: Seeded NumPy generator, owned by the caller.
        out_features: Output width of the layer.
        in_features: Input width of the layer.
        std: Standard deviation used for the weight draw.

    Returns:
        A ``(weight, bias)`` pair with shapes ``(out_features, in_features)``
        and ``(out_features,)``.
    """
    weight = _init_matrix(rng, (out_features, in_features), std)
    bias = np.zeros(out_features, dtype=np.float64)
    return weight, bias


def linear(x: FloatArray, weight: FloatArray, bias: FloatArray) -> FloatArray:
    """Apply ``y = x @ W^T + b`` with weight of shape ``(out, in)``.

    Why store the weight as ``(out_features, in_features)`` and transpose
    it here?
        This matches the ``torch.nn.Linear`` convention, so learners can
        carry the layout between this reference code and PyTorch. It also
        makes the two widths explicit in every weight's shape.

    Why does the bias broadcast?
        ``bias`` has shape ``(out_features,)``; NumPy adds it to the last
        axis of ``x @ weight.T``, which is exactly the output axis. The
        same line therefore works for ``(in,)``, ``(B, T, in)`` or any
        number of leading batch dimensions.

    Args:
        x: Input activations of shape ``(..., in_features)``.
        weight: Weight matrix of shape ``(out_features, in_features)``.
        bias: Bias vector of shape ``(out_features,)``.

    Returns:
        Output activations of shape ``(..., out_features)``.
    """
    return np.asarray(x @ weight.T + bias, dtype=np.float64)


def layer_norm(
    x: FloatArray,
    gamma: FloatArray,
    beta: FloatArray,
    eps: float = 1e-5,
) -> FloatArray:
    """Normalize the last axis of ``x``, then scale by ``gamma`` and shift by ``beta``.

    Why the last axis?
        Layer normalization acts on each position's ``d``-dimensional
        vector independently of the batch and sequence dimensions. Taking
        the statistics over ``axis=-1`` is what makes the operation
        *per-token* rather than *per-batch* (unlike batch normalization).

    Why ``keepdims=True``?
        The mean and variance keep shape ``(..., 1)`` so the subtraction
        and division broadcast back over the embedding axis without any
        reshaping.

    Why add ``eps`` inside the square root?
        If a position's activations were exactly constant, the variance
        would be zero and the division would explode. ``eps`` caps the
        denominator at ``sqrt(eps)``; it is a numerical guard, not a
        modelling choice.

    Why learnable ``gamma`` and ``beta``?
        Normalization forces each vector to zero mean and unit variance;
        the affine pair gives the model back the freedom to undo or temper
        that constraint. Both start as identity (ones and zeros), so the
        operation is a pure normalization at initialization.

    Args:
        x: Activations of shape ``(..., embedding_dim)``.
        gamma: Learned scale of shape ``(embedding_dim,)``.
        beta: Learned shift of shape ``(embedding_dim,)``.
        eps: Numerical-stability constant added to the variance.

    Returns:
        Normalized activations with the same shape as ``x``.
    """
    # Statistics over the embedding axis only, kept broadcastable.
    mean = x.mean(axis=-1, keepdims=True)
    variance = x.var(axis=-1, keepdims=True)
    # eps inside the sqrt guards against a zero-variance position.
    normalized = (x - mean) / np.sqrt(variance + eps)
    # Affine transform restores expressiveness after normalization.
    return np.asarray(normalized * gamma + beta, dtype=np.float64)


def gelu(x: FloatArray) -> FloatArray:
    """Apply the GELU activation (tanh approximation, as in GPT-2).

    The exact definition is ``x * Phi(x)`` where ``Phi`` is the standard
    normal CDF, which requires ``erf``. Base NumPy does not provide
    ``erf`` (SciPy would), so this module uses the tanh approximation:

    ``0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))``

    The approximation differs from the exact function by a small amount
    (order 1e-4 for moderate inputs) and is the variant GPT-2 used, which
    is why it is chosen here: learners meet the same formula they will see
    in real GPT-2 source code.

    Why not ReLU?
        GELU is smooth: near zero it lets a small negative input pass with
        a small weight instead of clipping it to exactly zero. The choice
        is a convention of GPT-style models, not a law.

    Args:
        x: Input activations of any shape.

    Returns:
        Activations of the same shape.
    """
    inner = math.sqrt(2.0 / math.pi) * (x + 0.044715 * x**3)
    return np.asarray(0.5 * x * (1.0 + np.tanh(inner)), dtype=np.float64)
