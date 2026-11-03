"""Unit tests for one pre-LN Transformer block (src/llm_lab/foundations/transformer_block.py)."""

import numpy as np
import pytest

from llm_lab.foundations.gpt_config import GPTConfig
from llm_lab.foundations.transformer_block import TransformerBlock


def _small_config() -> GPTConfig:
    return GPTConfig(
        vocab_size=50,
        context_length=16,
        embedding_dim=16,
        num_heads=2,
        num_layers=2,
        mlp_hidden_dim=32,
        seed=0,
    )


def test_block_forward_preserves_shape_and_stays_finite() -> None:
    block = TransformerBlock(_small_config(), np.random.default_rng(0))
    x = np.random.default_rng(1).normal(size=(2, 5, 16))

    out = block.forward(x)

    assert out.shape == x.shape
    assert np.all(np.isfinite(out))


def test_block_attention_rejects_non_3d_input() -> None:
    block = TransformerBlock(_small_config(), np.random.default_rng(0))

    with pytest.raises(ValueError, match="x must have shape"):
        block._attention(np.zeros((5, 16)))


def test_block_attention_rejects_inconsistent_head_count() -> None:
    block = TransformerBlock(_small_config(), np.random.default_rng(0))
    block.num_heads = 3  # 16 is not divisible by 3

    with pytest.raises(ValueError, match="num_heads must be positive"):
        block._attention(np.zeros((1, 5, 16)))
