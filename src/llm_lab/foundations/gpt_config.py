"""Configuration of the reference decoder-only GPT: the ``GPTConfig`` object.

This module is the entry point of the reference implementation: it defines
*what the model is* -- named, validated dimensions -- before any other
module defines *what the model does*. Isolating configuration in one small
immutable object has three pedagogical benefits:

1. **One definition site.** Every dimension used later (embedding width,
   number of heads, context length...) has a name here. When a tensor
   shape looks surprising in the model code, the answer lives in this
   file.
2. **Fail fast.** Invalid combinations are rejected at construction time
   with a precise message, instead of producing a confusing NumPy
   broadcasting error deep inside a forward pass.
3. **Reproducibility.** The ``seed`` field makes random initialization
   deterministic: two models built from the same configuration have
   identical parameters, so an observation can be replayed exactly.

Module family of the reference implementation:

- ``llm_lab.foundations.gpt_config`` (this file): dimensions, names,
  validation;
- ``llm_lab.foundations.gpt_ops``: numerical building blocks
  (initialization, linear projection, layer normalization, GELU);
- ``llm_lab.foundations.transformer_block``: one pre-LN Transformer block;
- ``llm_lab.foundations.gpt``: the assembled model (embeddings, blocks,
  final normalization, output projection);
- ``llm_lab.foundations.generate``: the autoregressive decoding loop.

Line-by-line walkthrough (bilingual site pages):
- https://jm-brun.github.io/llm-lab/fr/gpt-config-walkthrough/
- https://jm-brun.github.io/llm-lab/en/gpt-config-walkthrough/

Related concept pages (decoder-only architecture):
- https://jm-brun.github.io/llm-lab/fr/transformer/
- https://jm-brun.github.io/llm-lab/en/transformer/
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class GPTConfig:
    """Immutable, validated dimensions of the reference decoder-only GPT.

    Why a *frozen* dataclass?
        The configuration is read everywhere and written nowhere. Making
        it frozen turns "did something mutate the config mid-run?" into a
        guarantee instead of a debugging session: any accidental
        assignment raises ``FrozenInstanceError`` immediately.

    Why validate in ``__post_init__``?
        The constructor is the last moment when the caller still knows
        exactly which value is wrong. Checking constraints here converts
        a distant crash ("shapes not aligned") into an immediate, named
        error ("num_heads must be positive").

    Attributes:
        vocab_size: Number of vocabulary entries ``V``. It fixes the number
            of rows of the token embedding table and the number of logits
            the model outputs at every position.
        context_length: Maximum number of positions ``T`` the model can
            process in one pass. It fixes the number of rows of the
            learned position embedding table and the width of the sliding
            window used during generation.
        embedding_dim: Width ``d`` of the embedding and residual stream.
            Every block reads and writes vectors of this width; it must be
            divisible by ``num_heads`` because each attention head owns a
            contiguous slice of ``embedding_dim / num_heads`` columns.
        num_heads: Number ``H`` of attention heads. Multi-head attention is
            implemented as ``H`` independent single-head attentions over
            slices of the residual stream.
        num_layers: Number of stacked pre-LN Transformer blocks. It sets
            the depth used to scale the initialization standard deviation
            of the two residual-output projections in each block: attention
            ``w_o`` and MLP ``w_fc2`` (see ``transformer_block``). The other
            projections retain the base initialization standard deviation.
        mlp_hidden_dim: Hidden width of the position-wise MLP. GPT-2 uses
            ``4 * embedding_dim``; the value is explicit here instead of
            implied, so learners can see and change it.
        seed: Seed of the random initialization. Inference itself is
            deterministic; the seed controls only which random numbers
            initialize the parameters.

    Raises:
        ValueError: If a dimension is not a positive integer, or if
            ``embedding_dim`` is not divisible by ``num_heads``.
    """

    vocab_size: int
    context_length: int
    embedding_dim: int
    num_heads: int
    num_layers: int
    mlp_hidden_dim: int
    seed: int = 0

    def __post_init__(self) -> None:
        """Validate the configuration at construction time (fail fast)."""
        # A plain dict ties each value to its field name, so the error
        # message can name the culprit instead of repeating six
        # near-identical checks.
        dimensions = {
            "vocab_size": self.vocab_size,
            "context_length": self.context_length,
            "embedding_dim": self.embedding_dim,
            "num_heads": self.num_heads,
            "num_layers": self.num_layers,
            "mlp_hidden_dim": self.mlp_hidden_dim,
        }
        for name, value in dimensions.items():
            # A zero or negative dimension would create empty arrays or
            # degenerate loops much later; rejecting it here keeps the
            # error message next to its cause.
            if value <= 0:
                raise ValueError(f"{name} must be a positive integer")
        # Multi-head attention splits the residual stream into H equal
        # slices of d/H columns. A width not divisible by H makes the
        # split impossible; catching it here avoids a shape error in the
        # middle of the first forward pass.
        if self.embedding_dim % self.num_heads != 0:
            raise ValueError("embedding_dim must be divisible by num_heads")
