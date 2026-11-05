"""Unit tests for scaled dot-product attention, causal masking, and temperature scaling."""

import numpy as np
import pytest

from llm_lab.foundations.attention import (
    causal_mask,
    scaled_dot_product_attention,
    softmax_with_temperature,
)


def test_causal_mask_structure() -> None:
    mask = causal_mask(4)
    assert mask.shape == (4, 4)

    # Lower triangular and diagonal must be 0.0
    for i in range(4):
        for j in range(4):
            if j <= i:
                assert mask[i, j] == 0.0
            else:
                assert mask[i, j] == -np.inf


def test_causal_mask_invalid_length() -> None:
    with pytest.raises(ValueError, match="seq_len must be a positive integer"):
        causal_mask(0)
    with pytest.raises(ValueError, match="seq_len must be a positive integer"):
        causal_mask(-3)


def test_softmax_with_temperature_properties() -> None:
    logits = np.array([[1.0, 2.0, 3.0], [0.5, 0.5, 0.5]])

    # Sum along axis must be 1.0
    probs = softmax_with_temperature(logits, temperature=1.0)
    assert probs.shape == logits.shape
    assert np.allclose(probs.sum(axis=-1), 1.0)

    # Translation invariance
    shifted_logits = logits + 10.0
    shifted_probs = softmax_with_temperature(shifted_logits, temperature=1.0)
    assert np.allclose(probs, shifted_probs)

    # High temperature approaches uniform
    hot_probs = softmax_with_temperature(logits, temperature=1000.0)
    assert np.allclose(hot_probs[0], 1.0 / 3.0, atol=1e-3)

    # Low temperature approaches one-hot argmax
    cold_probs = softmax_with_temperature(logits, temperature=0.01)
    assert np.allclose(cold_probs[0], [0.0, 0.0, 1.0], atol=1e-3)


def test_softmax_with_temperature_invalid() -> None:
    with pytest.raises(ValueError, match="temperature must be strictly positive"):
        softmax_with_temperature(np.array([1.0, 2.0]), temperature=0.0)
    with pytest.raises(ValueError, match="temperature must be strictly positive"):
        softmax_with_temperature(np.array([1.0, 2.0]), temperature=-1.0)
    with pytest.raises(ValueError, match="logits must contain only finite values"):
        softmax_with_temperature(np.array([1.0, np.nan]))


def test_softmax_extreme_finite_logits_stays_normalized() -> None:
    with np.errstate(over="raise", invalid="raise"):
        result = softmax_with_temperature(np.array([1e308, 0.0]), temperature=0.1)
        wide_result = softmax_with_temperature(np.array([-1e308, 1e308]), temperature=0.1)
    np.testing.assert_array_equal(result, [1.0, 0.0])
    np.testing.assert_array_equal(wide_result, [0.0, 1.0])


def test_softmax_extreme_logits_with_high_temperature_preserves_relative_mass() -> None:
    # Scaling first yields [1, -1]; subtracting the unscaled extremes overflows.
    with np.errstate(over="raise", invalid="raise"):
        result = softmax_with_temperature(np.array([1e308, -1e308]), temperature=1e308)
    np.testing.assert_allclose(result, [1 / (1 + np.exp(-2)), 1 / (1 + np.exp(2))])


def test_softmax_preserves_close_large_logits_before_scaling() -> None:
    largest = 1e308
    next_logit = np.nextafter(largest, -np.inf)
    temperature = 1e292
    difference = (largest - next_logit) / temperature
    expected_first = 1 / (1 + np.exp(-difference))
    result = softmax_with_temperature(np.array([largest, next_logit]), temperature=temperature)
    np.testing.assert_allclose(result, [expected_first, 1 - expected_first], rtol=1e-12)


def test_softmax_mixes_overflow_and_close_values_along_axis() -> None:
    largest = 1e308
    close = np.nextafter(largest, -np.inf)
    temperature = 1e292
    expected_first = 1 / (1 + np.exp(-(largest - close) / temperature))
    logits = np.array([[largest, largest], [-largest, close]])
    with np.errstate(over="raise", invalid="raise"):
        result = softmax_with_temperature(logits, temperature=temperature, axis=0)
    np.testing.assert_allclose(result[:, 0], [1.0, 0.0])
    np.testing.assert_allclose(result[:, 1], [expected_first, 1 - expected_first], rtol=1e-12)


@pytest.mark.parametrize(
    ("query", "key", "mask"),
    [
        (1e308, 2.0, None),
        (1e308, 1.0, np.array([[1e308]])),
        (-1e308, 1.0, np.array([[-1e308]])),
    ],
)
def test_attention_rejects_overflowed_scores(
    query: float, key: float, mask: np.ndarray | None
) -> None:
    with np.errstate(over="raise", invalid="raise"), pytest.raises(ValueError, match="scores"):
        scaled_dot_product_attention(
            np.array([[query]]), np.array([[key]]), np.ones((1, 1)), mask=mask
        )


@pytest.mark.parametrize("temperature", [np.nan, np.inf, -np.inf])
def test_softmax_rejects_nonfinite_temperature(temperature: float) -> None:
    with pytest.raises(ValueError, match="temperature must be"):
        softmax_with_temperature(np.array([1.0, 0.0]), temperature=temperature)


@pytest.mark.parametrize("bad_mask", [np.nan, np.inf])
def test_attention_rejects_invalid_mask_entries(bad_mask: float) -> None:
    with pytest.raises(ValueError, match="mask"):
        scaled_dot_product_attention(
            np.ones((1, 1)),
            np.ones((2, 1)),
            np.ones((2, 1)),
            mask=np.array([[bad_mask, 0.0]]),
        )


def test_fully_masked_attention_row_returns_zeros_without_warning() -> None:
    with np.errstate(invalid="raise"):
        output, weights = scaled_dot_product_attention(
            np.ones((1, 1)),
            np.ones((2, 1)),
            np.ones((2, 1)),
            mask=np.full((1, 2), -np.inf),
        )
    np.testing.assert_array_equal(weights, [[0.0, 0.0]])
    np.testing.assert_array_equal(output, [[0.0]])


def test_scaled_dot_product_attention_matches_hand_computable_weighted_sum() -> None:
    # One query, two keys, and values with a different width from Q/K.
    q = np.array([[1.0, 0.0]])
    k = np.array([[1.0, 0.0], [0.0, 1.0]])
    v = np.array([[10.0, 0.0, 1.0], [0.0, 20.0, 3.0]])

    output, weights = scaled_dot_product_attention(q, k, v)

    scaled_scores = np.array([1.0 / np.sqrt(2.0), 0.0])
    expected_weights = np.exp(scaled_scores) / np.exp(scaled_scores).sum()
    expected_output = expected_weights @ v

    assert weights.shape == (1, 2)
    assert output.shape == (1, 3)
    np.testing.assert_allclose(weights[0], expected_weights, rtol=1e-12)
    np.testing.assert_allclose(output[0], expected_output, rtol=1e-12)


def test_attention_weights_normalize_only_over_allowed_keys() -> None:
    q = np.array([[1.0, 0.0]])
    k = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    v = np.array([[2.0, 0.0], [100.0, 100.0], [0.0, 4.0]])
    mask = np.array([[0.0, -np.inf, 0.0]])

    output, weights = scaled_dot_product_attention(q, k, v, mask=mask)

    assert weights[0, 1] == 0.0
    np.testing.assert_allclose(weights[0, [0, 2]].sum(), 1.0, rtol=1e-12)
    np.testing.assert_allclose(output[0], weights[0] @ v, rtol=1e-12)


def test_single_position_attention_returns_its_only_value() -> None:
    q = np.array([[2.0, -1.0]])
    k = np.array([[0.5, 3.0]])
    v = np.array([[4.0, -2.0, 7.0]])

    output, weights = scaled_dot_product_attention(q, k, v)

    np.testing.assert_array_equal(weights, [[1.0]])
    np.testing.assert_array_equal(output, v)


def test_attention_dot_product_ranking_is_not_cosine_ranking() -> None:
    q = np.array([[1.0, 0.0]])
    k = np.array([[0.1, 0.0], [10.0, 10.0]])
    v = np.eye(2)

    dot_products = (q @ k.T)[0]
    cosine_similarities = (q @ k.T)[0] / (np.linalg.norm(q, axis=1)[0] * np.linalg.norm(k, axis=1))
    output, weights = scaled_dot_product_attention(q, k, v)

    assert dot_products[1] > dot_products[0]
    assert cosine_similarities[0] > cosine_similarities[1]
    assert weights[0, 1] > weights[0, 0]
    np.testing.assert_allclose(output, weights, rtol=1e-12)


def test_wrong_softmax_axis_fails_per_query_normalization_invariant() -> None:
    scores = np.array([[2.0, 0.0], [1.0, 0.0]])

    wrong_axis_weights = softmax_with_temperature(scores, axis=0)

    np.testing.assert_allclose(wrong_axis_weights.sum(axis=0), [1.0, 1.0])
    assert not np.allclose(wrong_axis_weights.sum(axis=-1), [1.0, 1.0])


def test_scaled_dot_product_attention_shapes_and_invariants() -> None:
    t_q, t_k, d_k, d_v = 3, 4, 8, 12
    q = np.random.randn(t_q, d_k)
    k = np.random.randn(t_k, d_k)
    v = np.random.randn(t_k, d_v)

    out, weights = scaled_dot_product_attention(q, k, v)

    assert out.shape == (t_q, d_v)
    assert weights.shape == (t_q, t_k)
    assert np.allclose(weights.sum(axis=-1), 1.0)
    assert np.all(weights >= 0.0)


def test_scaled_dot_product_attention_causal_invariance() -> None:
    seq_len, d_k, d_v = 4, 6, 6
    np.random.seed(42)
    q = np.random.randn(seq_len, d_k)
    k = np.random.randn(seq_len, d_k)
    v = np.random.randn(seq_len, d_v)

    mask = causal_mask(seq_len)
    out1, weights1 = scaled_dot_product_attention(q, k, v, mask=mask)

    # Check future weights are strictly zero
    for i in range(seq_len):
        for j in range(i + 1, seq_len):
            assert weights1[i, j] == 0.0

    # Modify future keys and values for token at position 3
    k_modified = k.copy()
    v_modified = v.copy()
    k_modified[3] += 50.0
    v_modified[3] += 100.0

    out2, _ = scaled_dot_product_attention(q, k_modified, v_modified, mask=mask)

    # Invariance check: positions 0, 1, and 2 MUST BE COMPLETELY UNCHANGED
    assert np.allclose(out1[:3], out2[:3])
    # Position 3 can change
    assert not np.allclose(out1[3], out2[3])


def test_scaled_dot_product_attention_validation_errors() -> None:
    q = np.ones((3, 4))
    k = np.ones((3, 5))  # Mismatched d_k
    v = np.ones((3, 6))

    with pytest.raises(ValueError, match="identical key dimension"):
        scaled_dot_product_attention(q, k, v)

    k_len = np.ones((4, 4))  # Mismatched T_k with v (3, 6)
    with pytest.raises(ValueError, match="identical sequence length"):
        scaled_dot_product_attention(q, k_len, v)

    with pytest.raises(ValueError, match="2D arrays"):
        scaled_dot_product_attention(np.ones(4), np.ones(4), np.ones(4))

    with pytest.raises(ValueError, match="mask shape"):
        scaled_dot_product_attention(q, np.ones((3, 4)), v, mask=np.ones((2, 2)))

    with pytest.raises(ValueError, match="must contain finite numbers"):
        scaled_dot_product_attention(np.array([[np.nan]]), np.ones((1, 1)), np.ones((1, 1)))

    with pytest.raises(ValueError, match="dimensions cannot be empty"):
        scaled_dot_product_attention(np.empty((0, 4)), np.empty((0, 4)), np.empty((0, 4)))


def test_softmax_equal_large_logits_remain_uniform() -> None:
    logits = np.array([[1e308, 1e308]])
    with np.errstate(over="raise", invalid="raise"):
        probabilities = softmax_with_temperature(logits, temperature=0.1)
    np.testing.assert_allclose(probabilities, [[0.5, 0.5]])
