"""Unit tests for the autoregressive generation loop (src/llm_lab/foundations/generate.py)."""

import numpy as np
import pytest

from llm_lab.foundations.gpt import GPT
from llm_lab.foundations.gpt_config import GPTConfig
from llm_lab.foundations.generate import generate


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


def test_generate_greedy_is_deterministic_and_matches_manual_argmax_chain() -> None:
    model = GPT(_small_config())
    prompt = np.array([3, 1, 4, 1, 5], dtype=np.int64)

    generated_a = generate(model, prompt, 6)
    generated_b = generate(model, prompt, 6)

    assert generated_a.shape == (9,)
    assert np.array_equal(generated_a, generated_b)
    assert np.array_equal(generated_a[:5], prompt)

    # Independent recomputation: greedy decoding must follow the argmax chain.
    manual = prompt.copy()
    for _ in range(6):
        window = manual[-model.config.context_length :]
        step_logits = model.forward(window[None, :])[0, -1, :]
        manual = np.append(manual, np.int64(np.argmax(step_logits)))
    assert np.array_equal(generated_a, manual)


def test_generate_sampled_tokens_are_reproducible_with_seeded_rng() -> None:
    model = GPT(_small_config())
    prompt = np.array([3, 1, 4], dtype=np.int64)

    sampled_a = generate(
        model, prompt, 5, temperature=1.5, greedy=False, rng=np.random.default_rng(123)
    )
    sampled_b = generate(
        model, prompt, 5, temperature=1.5, greedy=False, rng=np.random.default_rng(123)
    )

    assert sampled_a.shape == (8,)
    assert np.array_equal(sampled_a, sampled_b)
    assert np.all(sampled_a >= 0)
    assert np.all(sampled_a < model.config.vocab_size)


def test_generate_slides_the_context_window() -> None:
    config = _small_config()
    model = GPT(config)
    # Prompt fills the whole context window; generation must still work by
    # reprocessing only the last context_length tokens at each step.
    prompt = np.arange(1, 17, dtype=np.int64)
    assert prompt.shape[0] == config.context_length

    generated = generate(model, prompt, 4)

    assert generated.shape == (16 + 4,)
    assert np.all(generated < config.vocab_size)


def test_generate_without_new_tokens_returns_prompt_unchanged() -> None:
    model = GPT(_small_config())
    prompt = np.array([3, 1, 4, 1, 5, 9, 2, 6], dtype=np.int64)

    result = generate(model, prompt, 0)

    assert np.array_equal(result, prompt)
    assert result.dtype == np.int64


def test_generate_validation_errors() -> None:
    model = GPT(_small_config())

    with pytest.raises(ValueError, match="non-empty 1D array"):
        generate(model, np.empty(0, dtype=np.int64), 3)
    with pytest.raises(ValueError, match="non-empty 1D array"):
        generate(model, np.array([[1, 2]], dtype=np.int64), 3)
    with pytest.raises(ValueError, match="prompt_ids must contain integer values"):
        generate(model, np.array([1.5, 2.0]), 3)
    with pytest.raises(ValueError, match="exceeds context_length"):
        generate(model, np.ones(17, dtype=np.int64), 3)
    with pytest.raises(ValueError, match="out of range"):
        generate(model, np.array([1, 50], dtype=np.int64), 3)
    with pytest.raises(ValueError, match="max_new_tokens must be >= 0"):
        generate(model, np.array([1, 2], dtype=np.int64), -1)
    with pytest.raises(ValueError, match="temperature must be strictly positive"):
        generate(
            model,
            np.array([1, 2], dtype=np.int64),
            3,
            greedy=False,
            temperature=0.0,
            rng=np.random.default_rng(0),
        )
    with pytest.raises(ValueError, match="rng is required"):
        generate(model, np.array([1, 2], dtype=np.int64), 3, greedy=False)
