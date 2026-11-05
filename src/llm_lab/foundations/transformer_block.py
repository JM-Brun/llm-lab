"""One pre-LN Transformer block of the reference decoder-only GPT.

A block is the repeated unit of the network. In the pre-LN order used by
GPT-2 it computes::

    x = x + attention(layer_norm_1(x))   # residual attention branch
    x = x + mlp(layer_norm_2(x))         # residual MLP branch

The normalization sits *inside* each residual branch, not on the trunk.
The trunk (``x + ...``) therefore always carries an unmodified copy of the
input towards the output: identity is the default, and each branch only
*adds* a correction. This keeps activations and gradients stable when many
blocks are stacked, which is why the post-LN order of the original
Transformer is no longer preferred in GPT-style models.

This module contains no training code: the parameters are drawn once in
``__init__`` and never updated.

Line-by-line walkthrough (bilingual site pages):
- https://jm-brun.github.io/llm-lab/fr/transformer-block-walkthrough/
- https://jm-brun.github.io/llm-lab/en/transformer-block-walkthrough/

Related concept pages:
- Q/K/V: https://jm-brun.github.io/llm-lab/fr/queries-keys-values/
- scaled dot-product attention:
  https://jm-brun.github.io/llm-lab/fr/scaled-dot-product-attention/
- causal masking: https://jm-brun.github.io/llm-lab/fr/causal-masking/
"""

import math

import numpy as np

from llm_lab.foundations.attention import (
    causal_mask,
    scaled_dot_product_attention,
)
from llm_lab.foundations.gpt_config import GPTConfig
from llm_lab.foundations.gpt_ops import (
    FloatArray,
    _init_linear,
    gelu,
    layer_norm,
    linear,
)


class TransformerBlock:
    """One pre-LN Transformer block: attention and MLP with residual paths.

    The block computes ``x + attention(ln(x))`` followed by
    ``x + mlp(ln(x))``, matching the GPT-2 decoder-only component order.
    Parameters are randomly initialized once and never updated here.
    """

    def __init__(self, config: GPTConfig, rng: np.random.Generator) -> None:
        """Draw all parameters of the block from the caller's generator.

        Why take ``rng`` as an argument instead of creating one?
            The model creates one generator from ``config.seed`` and hands
            it to each block in order. Parameter values then depend only
            on the configuration, which is what makes two identically
            configured models bitwise-identical.

        Args:
            config: Validated model configuration.
            rng: Seeded NumPy generator owned by the caller.
        """
        d = config.embedding_dim
        # GPT-2 uses the base std for internal projections and a smaller
        # std only for the two output projections added to the residual
        # stream: attention W_o and the MLP's second linear layer.
        # This depth-scaled scheme controls their initial contribution; it
        # does not guarantee constant residual-stream variance.
        base_std = 0.02
        residual_std = base_std / math.sqrt(2.0 * config.num_layers)
        # Each head owns a contiguous slice of head_dim columns; the slice
        # boundaries are recomputed in _attention from these two numbers.
        self.num_heads = config.num_heads
        self.head_dim = d // config.num_heads

        # --- Attention branch ------------------------------------------
        # LayerNorm starts as the identity (gamma=1, beta=0): at
        # initialization the block behaves like a plain normalization.
        self.ln1_gamma: FloatArray = np.ones(d, dtype=np.float64)
        self.ln1_beta: FloatArray = np.zeros(d, dtype=np.float64)
        # Three projections Q, K, V from the same input x, then an output
        # projection W_o that merges the per-head results back into d
        # columns. All four matrices are (d, d).
        self.w_q, self.b_q = _init_linear(rng, d, d, base_std)
        self.w_k, self.b_k = _init_linear(rng, d, d, base_std)
        self.w_v, self.b_v = _init_linear(rng, d, d, base_std)
        self.w_o, self.b_o = _init_linear(rng, d, d, residual_std)

        # --- MLP branch ------------------------------------------------
        self.ln2_gamma: FloatArray = np.ones(d, dtype=np.float64)
        self.ln2_beta: FloatArray = np.zeros(d, dtype=np.float64)
        # Position-wise MLP: d -> mlp_hidden_dim -> d. Each position goes
        # through the same two matrices, independently of its neighbours.
        self.w_fc1, self.b_fc1 = _init_linear(rng, config.mlp_hidden_dim, d, base_std)
        self.w_fc2, self.b_fc2 = _init_linear(rng, d, config.mlp_hidden_dim, residual_std)

    def _attention(self, x: FloatArray) -> FloatArray:
        """Compute multi-head causal self-attention over normalized input ``x``.

        Why loops over batch and heads?
            A production kernel would batch all heads into one tensor
            product. Here, explicit loops make every intermediate shape
            inspectable: the learner can print ``q[b, :, columns]`` and
            see a single (T, head_dim) attention problem, exactly the one
            solved by the tested ``scaled_dot_product_attention`` function.
            Clarity is chosen over speed (milestone G4 of the build path).

        Args:
            x: Normalized activations of shape (batch, seq_len, embedding_dim).

        Returns:
            Attention output of the same shape as ``x``.

        Raises:
            ValueError: If ``x`` is not 3D or if the head parameters are
                inconsistent with the embedding width.
        """
        if x.ndim != 3:
            raise ValueError("x must have shape (batch, seq_len, embedding_dim)")
        batch, seq_len, d = x.shape
        # Re-check the head split even when the block is used outside the
        # assembled model (defensive when attributes are mutated in tests).
        if self.num_heads <= 0 or d % self.num_heads != 0:
            raise ValueError("num_heads must be positive and divide embedding_dim")

        # One shared projection step for Q, K and V: shapes go from
        # (batch, seq_len, d) to (batch, seq_len, d) for each of them.
        q = linear(x, self.w_q, self.b_q)
        k = linear(x, self.w_k, self.b_k)
        v = linear(x, self.w_v, self.b_v)

        # One causal mask per sequence length: position i may attend to
        # positions j <= i; later positions receive -inf scores.
        mask = causal_mask(seq_len)
        attended = np.empty_like(x)
        for b in range(batch):
            for h in range(self.num_heads):
                # Head h owns columns [h*head_dim, (h+1)*head_dim) of the
                # projected matrices -- a *slice*, not a copy: the split
                # is purely a bookkeeping convention over the same d
                # columns.
                columns = slice(h * self.head_dim, (h + 1) * self.head_dim)
                head_out, _ = scaled_dot_product_attention(
                    q[b, :, columns], k[b, :, columns], v[b, :, columns], mask=mask
                )
                # Write the head's result back into its own slice; the
                # heads never mix until the output projection.
                attended[b, :, columns] = head_out
        # W_o mixes information across heads and projects back to width d.
        return linear(attended, self.w_o, self.b_o)

    def _mlp(self, x: FloatArray) -> FloatArray:
        """Apply the position-wise feed-forward network.

        Expand to ``mlp_hidden_dim`` (typically 4*d), pass through GELU,
        project back to ``d``. The intermediate widening gives each
        position a larger space in which to compute its non-linear
        transformation.
        """
        hidden = gelu(linear(x, self.w_fc1, self.b_fc1))
        return linear(hidden, self.w_fc2, self.b_fc2)

    def forward(self, x: FloatArray) -> FloatArray:
        """Run one block: residual attention, then residual MLP.

        Args:
            x: Activations of shape (batch, seq_len, embedding_dim).

        Returns:
            Activations with the same shape as ``x``.
        """
        # Pre-LN: normalize inside the branch; the trunk x stays intact.
        x = x + self._attention(layer_norm(x, self.ln1_gamma, self.ln1_beta))
        return x + self._mlp(layer_norm(x, self.ln2_gamma, self.ln2_beta))
