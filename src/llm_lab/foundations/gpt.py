"""Reference implementation of a small decoder-only GPT (inference only).

This module assembles the tested foundation components of
``llm_lab.foundations.attention`` into a complete, configurable, randomly
initialized decoder-only GPT. It is the first executable "lab artifact" of
the guided build path: it demonstrates the mechanics of inference and
generation with fixed parameters before any training exists.

Scope and limitations:

- NumPy only, float64, educational clarity over speed: attention uses
  explicit batch and head loops instead of batched tensor operations.
- Inference and generation only: there is no backpropagation, no optimizer
  and no training loop in this module.
- A randomly initialized model produces incoherent text. This is expected:
  it separates the mechanics of generation from the quality acquired by
  learning. A useful model requires training or pretrained weights.
- Learned absolute position embeddings; the context window slides over the
  last ``context_length`` tokens during generation (no KV cache).
"""

import math
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from llm_lab.foundations.attention import (
    causal_mask,
    scaled_dot_product_attention,
    softmax_with_temperature,
)

FloatArray = NDArray[np.float64]
IntArray = NDArray[np.int64]


@dataclass(frozen=True)
class GPTConfig:
    """Immutable configuration of the reference decoder-only GPT.

    Attributes:
        vocab_size: Number of vocabulary entries V.
        context_length: Maximum number of positions T the model can process.
        embedding_dim: Embedding and residual width d.
        num_heads: Number of attention heads H; d must be divisible by H.
        num_layers: Number of stacked pre-LN Transformer blocks.
        mlp_hidden_dim: Hidden width of the position-wise MLP.
        seed: Seed of the random initialization. Inference is deterministic.

    Raises:
        ValueError: If a dimension is not a positive integer, or if
            embedding_dim is not divisible by num_heads.
    """

    vocab_size: int
    context_length: int
    embedding_dim: int
    num_heads: int
    num_layers: int
    mlp_hidden_dim: int
    seed: int = 0

    def __post_init__(self) -> None:
        dimensions = {
            "vocab_size": self.vocab_size,
            "context_length": self.context_length,
            "embedding_dim": self.embedding_dim,
            "num_heads": self.num_heads,
            "num_layers": self.num_layers,
            "mlp_hidden_dim": self.mlp_hidden_dim,
        }
        for name, value in dimensions.items():
            if value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        if self.embedding_dim % self.num_heads != 0:
            raise ValueError("embedding_dim must be divisible by num_heads")


def _init_matrix(
    rng: np.random.Generator,
    shape: tuple[int, int],
    std: float = 0.02,
) -> FloatArray:
    """Draw a weight matrix from a zero-mean normal distribution."""
    return np.asarray(rng.normal(0.0, std, shape), dtype=np.float64)


def _init_linear(
    rng: np.random.Generator,
    out_features: int,
    in_features: int,
    std: float,
) -> tuple[FloatArray, FloatArray]:
    """Initialize a linear layer: weight (out_features, in_features) + zero bias."""
    weight = _init_matrix(rng, (out_features, in_features), std)
    bias = np.zeros(out_features, dtype=np.float64)
    return weight, bias


def linear(x: FloatArray, weight: FloatArray, bias: FloatArray) -> FloatArray:
    """Apply y = x @ W^T + b with weight of shape (out_features, in_features).

    Args:
        x: Input activations of shape (..., in_features).
        weight: Weight matrix of shape (out_features, in_features).
        bias: Bias vector of shape (out_features,).

    Returns:
        Output activations of shape (..., out_features).
    """
    return np.asarray(x @ weight.T + bias, dtype=np.float64)


def layer_norm(
    x: FloatArray,
    gamma: FloatArray,
    beta: FloatArray,
    eps: float = 1e-5,
) -> FloatArray:
    """Normalize the last dimension of x, then scale by gamma and shift by beta.

    Args:
        x: Activations of shape (..., embedding_dim).
        gamma: Learned scale of shape (embedding_dim,).
        beta: Learned shift of shape (embedding_dim,).
        eps: Numerical-stability constant added to the variance.

    Returns:
        Normalized activations with the same shape as x.
    """
    mean = x.mean(axis=-1, keepdims=True)
    variance = x.var(axis=-1, keepdims=True)
    normalized = (x - mean) / np.sqrt(variance + eps)
    return np.asarray(normalized * gamma + beta, dtype=np.float64)


def gelu(x: FloatArray) -> FloatArray:
    """Apply the GELU activation (tanh approximation, as in GPT-2)."""
    inner = math.sqrt(2.0 / math.pi) * (x + 0.044715 * x**3)
    return np.asarray(0.5 * x * (1.0 + np.tanh(inner)), dtype=np.float64)


class TransformerBlock:
    """One pre-LN Transformer block: attention and MLP with residual paths.

    The block computes ``x + attention(ln(x))`` followed by
    ``x + mlp(ln(x))``, matching the GPT-2 decoder-only component order.
    Parameters are randomly initialized and never updated in this module.
    """

    def __init__(self, config: GPTConfig, rng: np.random.Generator) -> None:
        d = config.embedding_dim
        residual_std = 0.02 / math.sqrt(2.0 * config.num_layers)
        self.num_heads = config.num_heads
        self.head_dim = d // config.num_heads

        self.ln1_gamma: FloatArray = np.ones(d, dtype=np.float64)
        self.ln1_beta: FloatArray = np.zeros(d, dtype=np.float64)
        self.w_q, self.b_q = _init_linear(rng, d, d, residual_std)
        self.w_k, self.b_k = _init_linear(rng, d, d, residual_std)
        self.w_v, self.b_v = _init_linear(rng, d, d, residual_std)
        self.w_o, self.b_o = _init_linear(rng, d, d, residual_std)

        self.ln2_gamma: FloatArray = np.ones(d, dtype=np.float64)
        self.ln2_beta: FloatArray = np.zeros(d, dtype=np.float64)
        self.w_fc1, self.b_fc1 = _init_linear(rng, config.mlp_hidden_dim, d, residual_std)
        self.w_fc2, self.b_fc2 = _init_linear(rng, d, config.mlp_hidden_dim, residual_std)

    def _attention(self, x: FloatArray) -> FloatArray:
        """Compute multi-head causal self-attention over normalized input x.

        Args:
            x: Normalized activations of shape (batch, seq_len, embedding_dim).

        Returns:
            Attention output of the same shape as x.

        Raises:
            ValueError: If x is not 3D or head parameters are inconsistent.
        """
        if x.ndim != 3:
            raise ValueError("x must have shape (batch, seq_len, embedding_dim)")
        batch, seq_len, d = x.shape
        if self.num_heads <= 0 or d % self.num_heads != 0:
            raise ValueError("num_heads must be positive and divide embedding_dim")

        q = linear(x, self.w_q, self.b_q)
        k = linear(x, self.w_k, self.b_k)
        v = linear(x, self.w_v, self.b_v)

        # Per-head split and merge: head h uses columns [h*hd, (h+1)*hd).
        # Explicit loops keep the split/merge shapes inspectable (milestone G4).
        mask = causal_mask(seq_len)
        attended = np.empty_like(x)
        for b in range(batch):
            for h in range(self.num_heads):
                columns = slice(h * self.head_dim, (h + 1) * self.head_dim)
                head_out, _ = scaled_dot_product_attention(
                    q[b, :, columns], k[b, :, columns], v[b, :, columns], mask=mask
                )
                attended[b, :, columns] = head_out
        return linear(attended, self.w_o, self.b_o)

    def _mlp(self, x: FloatArray) -> FloatArray:
        """Apply the position-wise feed-forward network."""
        hidden = gelu(linear(x, self.w_fc1, self.b_fc1))
        return linear(hidden, self.w_fc2, self.b_fc2)

    def forward(self, x: FloatArray) -> FloatArray:
        """Run one block: residual attention, then residual MLP.

        Args:
            x: Activations of shape (batch, seq_len, embedding_dim).

        Returns:
            Activations with the same shape as x.
        """
        x = x + self._attention(layer_norm(x, self.ln1_gamma, self.ln1_beta))
        return x + self._mlp(layer_norm(x, self.ln2_gamma, self.ln2_beta))


class GPT:
    """A minimal decoder-only GPT with learned absolute position embeddings.

    Architecture: token + position embeddings, then ``num_layers`` pre-LN
    Transformer blocks, a final layer norm, and an untied output projection
    to vocabulary logits. Parameters are randomly initialized from
    ``config.seed`` and are never updated in this module.

    The model implements the inference branch only (milestones G4–G7):
    ``forward`` returns next-token logits for every position, and
    :func:`generate` runs the autoregressive loop with fixed parameters.
    """

    def __init__(self, config: GPTConfig) -> None:
        self.config = config
        rng = np.random.default_rng(config.seed)
        d = config.embedding_dim

        self.token_embedding: FloatArray = _init_matrix(rng, (config.vocab_size, d))
        self.position_embedding: FloatArray = _init_matrix(rng, (config.context_length, d))
        self.blocks = [TransformerBlock(config, rng) for _ in range(config.num_layers)]
        self.ln_f_gamma: FloatArray = np.ones(d, dtype=np.float64)
        self.ln_f_beta: FloatArray = np.zeros(d, dtype=np.float64)
        self.w_head, self.b_head = _init_linear(rng, config.vocab_size, d, 0.02)

    def forward(self, token_ids: NDArray[np.integer]) -> FloatArray:
        """Return next-token logits for each position of a batch of sequences.

        Args:
            token_ids: Integer array of shape (batch, seq_len) with values in
                [0, vocab_size) and seq_len <= context_length.

        Returns:
            Logits of shape (batch, seq_len, vocab_size).

        Raises:
            ValueError: If token_ids is not a non-empty 2D integer array, if
                the sequence exceeds context_length, or if ids are out of
                range.
        """
        ids = np.asarray(token_ids)
        if ids.ndim != 2:
            raise ValueError("token_ids must have shape (batch, seq_len)")
        if not np.issubdtype(ids.dtype, np.integer):
            raise ValueError("token_ids must contain integer values")
        if ids.shape[0] == 0 or ids.shape[1] == 0:
            raise ValueError("token_ids must have a non-empty batch and sequence")
        if ids.shape[1] > self.config.context_length:
            raise ValueError(
                f"seq_len {ids.shape[1]} exceeds context_length {self.config.context_length}"
            )
        if np.any(ids < 0) or np.any(ids >= self.config.vocab_size):
            raise ValueError("token ids are out of range [0, vocab_size)")

        seq_len = ids.shape[1]
        x = self.token_embedding[ids] + self.position_embedding[:seq_len]
        for block in self.blocks:
            x = block.forward(x)
        x = layer_norm(x, self.ln_f_gamma, self.ln_f_beta)
        return linear(x, self.w_head, self.b_head)

    def num_parameters(self) -> int:
        """Return the total number of scalar parameters of the model."""
        arrays = [
            self.token_embedding,
            self.position_embedding,
            self.ln_f_gamma,
            self.ln_f_beta,
            self.w_head,
            self.b_head,
        ]
        for block in self.blocks:
            arrays += [
                block.ln1_gamma,
                block.ln1_beta,
                block.w_q,
                block.b_q,
                block.w_k,
                block.b_k,
                block.w_v,
                block.b_v,
                block.w_o,
                block.b_o,
                block.ln2_gamma,
                block.ln2_beta,
                block.w_fc1,
                block.b_fc1,
                block.w_fc2,
                block.b_fc2,
            ]
        return int(sum(array.size for array in arrays))


def generate(
    model: GPT,
    prompt_ids: NDArray[np.integer],
    max_new_tokens: int,
    *,
    temperature: float = 1.0,
    greedy: bool = True,
    rng: np.random.Generator | None = None,
) -> IntArray:
    """Generate token ids autoregressively with fixed parameters.

    At each step the model reprocesses the last ``context_length`` tokens of
    the current sequence (sliding window), computes next-token logits at the
    final position, and selects one token: argmax when ``greedy`` is True,
    otherwise a sample from the temperature-scaled distribution. The selected
    token is appended and the loop repeats until ``max_new_tokens`` tokens
    have been produced. There is no early-stopping rule in this reference.

    Args:
        model: A decoder-only GPT with fixed parameters.
        prompt_ids: 1D integer array of prompt ids, with
            1 <= length <= context_length and values in [0, vocab_size).
        max_new_tokens: Number of tokens to generate (>= 0).
        temperature: Sampling temperature (> 0); it only affects sampling,
            but is validated in both modes.
        greedy: If True, select the argmax token at each step.
        rng: Seeded generator used for sampling; required when greedy is
            False. Sampling is reproducible only when this generator is
            seeded.

    Returns:
        A 1D int64 array of length ``prompt + max_new_tokens`` containing the
        prompt ids followed by the generated ids.

    Raises:
        ValueError: If the prompt is not a non-empty 1D integer array within
            range, if max_new_tokens is negative, if temperature <= 0, or if
            no rng is provided for sampling.
    """
    ids = np.asarray(prompt_ids)
    if ids.ndim != 1 or ids.shape[0] == 0:
        raise ValueError("prompt_ids must be a non-empty 1D array of token ids")
    if not np.issubdtype(ids.dtype, np.integer):
        raise ValueError("prompt_ids must contain integer values")
    if ids.shape[0] > model.config.context_length:
        raise ValueError(
            f"prompt length {ids.shape[0]} exceeds context_length "
            f"{model.config.context_length}"
        )
    if np.any(ids < 0) or np.any(ids >= model.config.vocab_size):
        raise ValueError("prompt token ids are out of range [0, vocab_size)")
    if max_new_tokens < 0:
        raise ValueError("max_new_tokens must be >= 0")
    if temperature <= 0:
        raise ValueError("temperature must be strictly positive")
    if not greedy and rng is None:
        raise ValueError("rng is required when greedy is False")

    context = ids.astype(np.int64, copy=True)
    for _ in range(max_new_tokens):
        window = context[-model.config.context_length :]
        logits = model.forward(window[None, :])[0, -1, :]
        if greedy:
            next_token = int(np.argmax(logits))
        else:
            probs = softmax_with_temperature(logits, temperature=temperature)
            next_token = int(rng.choice(model.config.vocab_size, p=probs))
        context = np.append(context, np.int64(next_token))
    return np.asarray(context, dtype=np.int64)
