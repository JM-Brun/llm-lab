"""Unit tests for the assembled reference GPT model (src/llm_lab/foundations/gpt.py)."""

import numpy as np
import pytest

from llm_lab.foundations.gpt import GPT
from llm_lab.foundations.gpt_config import GPTConfig


def _small_config(seed: int = 0) -> GPTConfig:
    return GPTConfig(
        vocab_size=50,
        context_length=16,
        embedding_dim=16,
        num_heads=2,
        num_layers=2,
        mlp_hidden_dim=32,
        seed=seed,
    )


def test_forward_returns_expected_logit_shape() -> None:
    model = GPT(_small_config())
    ids = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int64)

    logits = model.forward(ids)

    assert logits.shape == (2, 3, 50)
    assert np.all(np.isfinite(logits))


def test_forward_validation_errors() -> None:
    model = GPT(_small_config())

    with pytest.raises(ValueError, match="token_ids must have shape"):
        model.forward(np.array([1, 2, 3], dtype=np.int64))
    with pytest.raises(ValueError, match="token_ids must contain integer values"):
        model.forward(np.array([[1.5, 2.0]], dtype=np.float64))
    with pytest.raises(ValueError, match="non-empty batch and sequence"):
        model.forward(np.empty((0, 3), dtype=np.int64))
    with pytest.raises(ValueError, match="exceeds context_length"):
        model.forward(np.ones((1, 17), dtype=np.int64))
    with pytest.raises(ValueError, match="out of range"):
        model.forward(np.array([[1, 50]], dtype=np.int64))
    with pytest.raises(ValueError, match="out of range"):
        model.forward(np.array([[1, -1]], dtype=np.int64))


def test_same_seed_reproduces_identical_logits() -> None:
    ids = np.array([[1, 2, 3, 4]], dtype=np.int64)
    logits_a = GPT(_small_config(seed=7)).forward(ids)
    logits_b = GPT(_small_config(seed=7)).forward(ids)

    assert np.allclose(logits_a, logits_b)

    logits_c = GPT(_small_config(seed=8)).forward(ids)
    assert not np.allclose(logits_a, logits_c)


def test_prefix_invariance_future_tokens_do_not_change_earlier_logits() -> None:
    model = GPT(_small_config())
    prefix = np.array([[1, 2, 3, 4]], dtype=np.int64)
    extended = np.array([[1, 2, 3, 4, 5, 6, 7, 8]], dtype=np.int64)

    prefix_logits = model.forward(prefix)
    extended_logits = model.forward(extended)

    assert np.allclose(prefix_logits[0], extended_logits[0, :4])
    assert not np.allclose(extended_logits[0, 3], extended_logits[0, 7])


def test_num_parameters_matches_configuration_formula() -> None:
    config = _small_config()
    model = GPT(config)

    d = config.embedding_dim
    hidden = config.mlp_hidden_dim
    # One block owns: 4 attention matrices (d, d) + their biases, an MLP
    # made of (hidden, d) and (d, hidden) + biases, and 2 layer norms.
    per_block = 4 * d * d + 4 * d + 2 * hidden * d + hidden + d + 4 * d
    expected = (
        2 * config.vocab_size * d  # token embedding + untied output weight
        + config.context_length * d  # position embedding
        + config.num_layers * per_block
        + 2 * d  # final layer norm
        + config.vocab_size  # output bias
    )

    assert model.num_parameters() == expected
