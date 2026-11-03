"""Unit tests for the autoregressive generation loop (src/llm_lab/foundations/generate.py)."""

import numpy as np
import pytest

from llm_lab.foundations.attention import softmax_with_temperature
from llm_lab.foundations.decoding_filters import top_k_filter, top_p_filter
from llm_lab.foundations.generate import generate
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


def test_generate_greedy_is_deterministic_and_matches_manual_argmax_chain() -> None:
    model = GPT(_small_config())
    prompt = np.array([3, 1, 4, 1, 5], dtype=np.int64)

    generated_a = generate(model, prompt, 6)
    generated_b = generate(model, prompt, 6)

    assert generated_a.shape == (11,)
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


def test_generate_top_k_one_sampling_matches_greedy_chain() -> None:
    model = GPT(_small_config())
    prompt = np.array([3, 1, 4, 1, 5], dtype=np.int64)

    greedy_chain = generate(model, prompt, 6)
    sampled = generate(model, prompt, 6, greedy=False, top_k=1, rng=np.random.default_rng(7))

    # With a single candidate left, the draw is forced: sampling with
    # top_k=1 must reproduce the greedy argmax chain exactly.
    assert np.array_equal(sampled, greedy_chain)


def test_generate_tight_top_p_nucleus_matches_greedy_chain() -> None:
    model = GPT(_small_config())
    prompt = np.array([3, 1, 4], dtype=np.int64)

    greedy_chain = generate(model, prompt, 5)
    sampled = generate(
        model,
        prompt,
        5,
        greedy=False,
        temperature=1.7,
        top_p=1e-9,
        rng=np.random.default_rng(7),
    )

    # A nucleus smaller than any single token's mass keeps only the most
    # probable token; argmax is temperature-invariant, so the chains agree.
    assert np.array_equal(sampled, greedy_chain)


def test_generate_sampling_with_truncation_matches_manual_chain() -> None:
    model = GPT(_small_config())
    prompt = np.array([3, 1, 4, 1, 5], dtype=np.int64)

    result = generate(
        model,
        prompt,
        6,
        greedy=False,
        temperature=1.3,
        top_k=5,
        top_p=0.9,
        rng=np.random.default_rng(42),
    )

    # Independent recomputation of the applied order:
    # temperature -> top-k -> top-p -> draw, with the same seeded rng.
    manual = prompt.copy().astype(np.int64)
    rng = np.random.default_rng(42)
    for _ in range(6):
        window = manual[-model.config.context_length :]
        step_logits = model.forward(window[None, :])[0, -1, :]
        probs = softmax_with_temperature(step_logits, temperature=1.3)
        probs = top_k_filter(probs, k=5)
        probs = top_p_filter(probs, p=0.9)
        manual = np.append(manual, np.int64(rng.choice(model.config.vocab_size, p=probs)))

    assert np.array_equal(result, manual)


def test_generate_top_k_at_vocabulary_equivalent_to_plain_sampling() -> None:
    model = GPT(_small_config())
    prompt = np.array([3, 1, 4], dtype=np.int64)

    plain = generate(model, prompt, 5, greedy=False, temperature=1.2, rng=np.random.default_rng(9))
    truncated = generate(
        model,
        prompt,
        5,
        greedy=False,
        temperature=1.2,
        top_k=model.config.vocab_size,
        rng=np.random.default_rng(9),
    )

    # k >= vocabulary keeps every candidate: the draws must coincide.
    assert np.array_equal(plain, truncated)


def test_generate_greedy_ignores_valid_filters() -> None:
    model = GPT(_small_config())
    prompt = np.array([3, 1, 4], dtype=np.int64)

    plain = generate(model, prompt, 4)
    with_filters = generate(model, prompt, 4, top_k=3, top_p=0.8)

    assert np.array_equal(plain, with_filters)


def test_generate_truncation_validation_errors() -> None:
    model = GPT(_small_config())
    prompt = np.array([1, 2], dtype=np.int64)
    rng = np.random.default_rng(0)

    with pytest.raises(ValueError, match="top_k must be an integer >= 1"):
        generate(model, prompt, 2, greedy=False, top_k=0, rng=rng)
    with pytest.raises(ValueError, match="top_k must be an integer >= 1"):
        generate(model, prompt, 2, greedy=False, top_k=-3, rng=rng)
    with pytest.raises(ValueError, match="top_k must be an integer >= 1"):
        generate(model, prompt, 2, greedy=False, top_k=2.5, rng=rng)
    with pytest.raises(ValueError, match="top_p must be in the interval"):
        generate(model, prompt, 2, greedy=False, top_p=0.0, rng=rng)
    with pytest.raises(ValueError, match="top_p must be in the interval"):
        generate(model, prompt, 2, greedy=False, top_p=1.5, rng=rng)
    # Hidden invalid values must not wait for a switch to sampling: the
    # truncation parameters are validated in greedy mode too.
    with pytest.raises(ValueError, match="top_k must be an integer >= 1"):
        generate(model, prompt, 2, top_k=0)
    with pytest.raises(ValueError, match="top_p must be in the interval"):
        generate(model, prompt, 2, top_p=0.0)
