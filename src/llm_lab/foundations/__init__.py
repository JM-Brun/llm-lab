"""Foundations module: numerical reference implementations for core LLM operations.

The reference decoder-only GPT is split into focused modules, in reading
order: ``gpt_config`` (dimensions), ``gpt_ops`` (building blocks),
``transformer_block`` (one block), ``gpt`` (the assembled model) and
``generate`` (the decoding loop). This package-level module re-exports
the public surface so callers can import from ``llm_lab.foundations``
directly.
"""

from llm_lab.foundations.attention import (
    causal_mask,
    scaled_dot_product_attention,
    softmax_with_temperature,
)
from llm_lab.foundations.generate import generate
from llm_lab.foundations.gpt import GPT
from llm_lab.foundations.gpt_config import GPTConfig
from llm_lab.foundations.gpt_ops import gelu, layer_norm, linear
from llm_lab.foundations.losses import (
    cross_entropy_from_logits,
    cross_entropy_gradient,
)
from llm_lab.foundations.transformer_block import TransformerBlock

__all__ = [
    "GPT",
    "GPTConfig",
    "TransformerBlock",
    "causal_mask",
    "cross_entropy_from_logits",
    "cross_entropy_gradient",
    "gelu",
    "generate",
    "layer_norm",
    "linear",
    "scaled_dot_product_attention",
    "softmax_with_temperature",
]
