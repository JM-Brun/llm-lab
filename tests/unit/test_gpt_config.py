"""Unit tests for the GPTConfig object (src/llm_lab/foundations/gpt_config.py)."""

import dataclasses

import pytest

from llm_lab.foundations.gpt_config import GPTConfig


def _config(**overrides: int) -> GPTConfig:
    """Return a valid configuration, with optional field overrides."""
    values = {
        "vocab_size": 50,
        "context_length": 16,
        "embedding_dim": 16,
        "num_heads": 2,
        "num_layers": 2,
        "mlp_hidden_dim": 32,
    }
    values.update(overrides)
    return GPTConfig(**values)


def test_config_rejects_non_positive_dimensions() -> None:
    with pytest.raises(ValueError, match="vocab_size must be a positive integer"):
        _config(vocab_size=0)
    with pytest.raises(ValueError, match="mlp_hidden_dim must be a positive integer"):
        _config(mlp_hidden_dim=0)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("vocab_size", 50.5),
        ("context_length", 16.0),
        ("embedding_dim", 16.0),
        ("num_heads", True),
        ("mlp_hidden_dim", 32.0),
    ],
)
def test_config_rejects_non_integer_dimensions(field: str, value: object) -> None:
    with pytest.raises(ValueError, match=f"{field} must be a positive integer"):
        _config(**{field: value})


@pytest.mark.parametrize("seed", [-1, 1.5, True])
def test_config_rejects_invalid_seed(seed: object) -> None:
    with pytest.raises(ValueError, match="seed must be a non-negative integer"):
        _config(seed=seed)


def test_config_requires_divisible_head_count() -> None:
    with pytest.raises(ValueError, match="embedding_dim must be divisible by num_heads"):
        _config(embedding_dim=10, num_heads=3)


def test_config_is_immutable() -> None:
    config = _config()
    with pytest.raises(dataclasses.FrozenInstanceError):
        config.vocab_size = 20


def test_config_defaults_seed_to_zero() -> None:
    assert _config().seed == 0
