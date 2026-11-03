"""Unit tests for the numerical building blocks (src/llm_lab/foundations/gpt_ops.py)."""

import math

import numpy as np

from llm_lab.foundations.gpt_ops import _init_linear, _init_matrix, gelu, layer_norm, linear


def test_linear_matches_manual_matmul_and_broadcasts_bias() -> None:
    rng = np.random.default_rng(0)
    x = rng.normal(size=(2, 5, 3))
    weight = rng.normal(size=(4, 3))
    bias = rng.normal(size=(4,))

    out = linear(x, weight, bias)

    assert out.shape == (2, 5, 4)
    np.testing.assert_allclose(out, x @ weight.T + bias)


def test_layer_norm_normalizes_then_rescales_last_axis() -> None:
    rng = np.random.default_rng(1)
    x = rng.normal(loc=5.0, scale=3.0, size=(2, 6, 4))
    gamma = np.full(4, 2.0)
    beta = np.full(4, 0.5)

    out = layer_norm(x, gamma, beta)

    assert out.shape == x.shape
    normalized = (x - x.mean(axis=-1, keepdims=True)) / np.sqrt(
        x.var(axis=-1, keepdims=True) + 1e-5
    )
    np.testing.assert_allclose(out, normalized * gamma + beta, atol=1e-12)


def test_layer_norm_with_identity_affine_yields_roughly_unit_variance() -> None:
    rng = np.random.default_rng(2)
    x = rng.normal(loc=-2.0, scale=0.5, size=(3, 7, 8))
    gamma = np.ones(8)
    beta = np.zeros(8)

    out = layer_norm(x, gamma, beta)

    assert out.shape == x.shape
    np.testing.assert_allclose(out.mean(axis=-1), 0.0, atol=1e-10)
    # Slightly below 1 because eps (1e-5) is added to the variance; the
    # shortfall is about eps / variance and stays well under 1e-3 here.
    np.testing.assert_allclose(out.var(axis=-1), 1.0, atol=1e-3)


def test_gelu_is_zero_at_zero_and_close_to_exact_erf_definition() -> None:
    x = np.linspace(-3.0, 3.0, 121)

    out = gelu(x)

    assert out.shape == x.shape
    assert gelu(np.array([0.0]))[0] == 0.0
    exact = 0.5 * x * (1.0 + np.array([math.erf(v / math.sqrt(2.0)) for v in x]))
    np.testing.assert_allclose(out, exact, atol=1e-3)


def test_init_linear_returns_weight_shape_and_zero_bias() -> None:
    rng = np.random.default_rng(3)

    weight, bias = _init_linear(rng, out_features=6, in_features=4, std=0.02)

    assert weight.shape == (6, 4)
    assert bias.shape == (6,)
    np.testing.assert_array_equal(bias, np.zeros(6))


def test_seeded_rng_makes_initialization_reproducible() -> None:
    w1, b1 = _init_linear(np.random.default_rng(42), 5, 5, 0.02)
    w2, b2 = _init_linear(np.random.default_rng(42), 5, 5, 0.02)

    np.testing.assert_array_equal(w1, w2)
    np.testing.assert_array_equal(b1, b2)


def test_init_matrix_draws_from_low_variance_normal() -> None:
    rng = np.random.default_rng(4)

    matrix = _init_matrix(rng, (200, 300), std=0.02)

    assert matrix.shape == (200, 300)
    # With 60000 draws, the sample mean stays very close to zero and the
    # sample standard deviation stays near the requested value.
    assert abs(float(matrix.mean())) < 0.005
    assert 0.01 < float(matrix.std()) < 0.03
