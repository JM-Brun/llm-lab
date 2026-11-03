"""Unit tests for the reference decoder-only GPT (inference and generation only)."""

import numpy as np
import pytest

from llm_lab.foundations.gpt import GPT, GPTConfig, generate


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


def test_config_rejects_non_positive_dimensions() -> None:
    with pytest.raises(ValueError, match="vocab_size must be a positive integer"):
        GPTConfig(
            vocab_size=0,
            context_length=8,
            embedding_dim=8,
            num_heads=2,
            num_layers=1,
            mlp_hidden_dim=16,
        )
    with pytest.raises(ValueError, match="mlp_hidden_dim must be a positive integer"):
        GPTConfig(
            vocab_size=10,
            context_length=0,
            embedding_dim=8,
            num_heads=2,
            num_layers=1,
            mlp_hidden_dim=0,
        )


def test_config_requires_divisible_head_count() -> None:
    with pytest.raises(ValueError, match="embedding_dim must be divisible by num_heads"):
        GPTConfig(
            vocab_size=10,
            context_length=8,
            embedding_dim=10,
            num_heads=3,
            num_layers=1,
            mlp_hidden_dim=16,
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


def test_same_seed_reproduces_identical_parameters_and_logits() -> None:
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
    per_block = 4 * d * d + 4 * d + 2 * hidden * d + hidden + d + 4 * d
    expected = (
        2 * config.vocab_size * d  # token embedding + untied output weight
        + config.context_length * d  # position embedding
        + config.num_layers * per_block
        + 2 * d  # final layer norm
        + config.vocab_size  # output bias
    )

    assert model.num_parameters() == expected


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
