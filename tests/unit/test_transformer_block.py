"""Unit tests for one pre-LN Transformer block (src/llm_lab/foundations/transformer_block.py)."""

import numpy as np
import pytest

import llm_lab.foundations.transformer_block as transformer_block_module
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


def test_gpt2_scaled_initialization_applies_only_to_residual_output_projections(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed_stds: list[float] = []
    original_init_linear = transformer_block_module._init_linear

    def recording_init_linear(
        rng: np.random.Generator, out_features: int, in_features: int, std: float
    ) -> tuple[np.ndarray, np.ndarray]:
        observed_stds.append(std)
        return original_init_linear(rng, out_features, in_features, std)

    monkeypatch.setattr(transformer_block_module, "_init_linear", recording_init_linear)
    config = _small_config()
    TransformerBlock(config, np.random.default_rng(0))

    residual_std = 0.02 / np.sqrt(2.0 * config.num_layers)
    np.testing.assert_allclose(
        observed_stds,
        [0.02, 0.02, 0.02, residual_std, 0.02, residual_std],
        rtol=0.0,
        atol=1e-15,
    )
