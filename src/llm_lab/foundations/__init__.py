"""Foundations module: numerical reference implementations for core LLM operations."""

from llm_lab.foundations.attention import (
    causal_mask,
    scaled_dot_product_attention,
    softmax_with_temperature,
)
from llm_lab.foundations.gpt import GPT, GPTConfig, generate
from llm_lab.foundations.losses import (
    cross_entropy_from_logits,
    cross_entropy_gradient,
)

__all__ = [
    "GPT",
    "GPTConfig",
    "causal_mask",
    "cross_entropy_from_logits",
    "cross_entropy_gradient",
    "generate",
    "scaled_dot_product_attention",
    "softmax_with_temperature",
]
