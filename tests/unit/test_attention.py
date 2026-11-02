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
