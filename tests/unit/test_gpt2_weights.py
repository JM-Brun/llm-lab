"""Tests for loading GPT-2 checkpoint parameters into the reference NumPy GPT."""

import numpy as np
import pytest

from llm_lab.foundations.gpt import GPT
from llm_lab.foundations.gpt2_weights import GPT2_SMALL_CONFIG, load_gpt2_state_dict
from llm_lab.foundations.gpt_config import GPTConfig

TINY = GPTConfig(
    vocab_size=11,
    context_length=8,
    embedding_dim=6,
    num_heads=2,
    num_layers=2,
    mlp_hidden_dim=24,
    seed=0,
)


def _gpt2_state_dict(config: GPTConfig, seed: int = 1) -> dict[str, np.ndarray]:
    """Build a random state dict with Hugging Face GPT-2 names and shapes.

    GPT-2 stores its projections as ``Conv1D`` weights of shape ``(in, out)``
    and fuses the Q/K/V projections into one ``c_attn`` matrix. Every value
    is distinct, so a misplaced or untransposed array cannot pass by chance.
    """
    rng = np.random.default_rng(seed)
    d, hidden = config.embedding_dim, config.mlp_hidden_dim

    def draw(*shape: int) -> np.ndarray:
        return rng.normal(0.0, 0.5, shape).astype(np.float32)

    state = {
        "wte.weight": draw(config.vocab_size, d),
        "wpe.weight": draw(config.context_length, d),
        "ln_f.weight": draw(d),
        "ln_f.bias": draw(d),
    }
    for i in range(config.num_layers):
        state |= {
            f"h.{i}.ln_1.weight": draw(d),
            f"h.{i}.ln_1.bias": draw(d),
            f"h.{i}.attn.c_attn.weight": draw(d, 3 * d),
            f"h.{i}.attn.c_attn.bias": draw(3 * d),
            f"h.{i}.attn.c_proj.weight": draw(d, d),
            f"h.{i}.attn.c_proj.bias": draw(d),
            f"h.{i}.ln_2.weight": draw(d),
            f"h.{i}.ln_2.bias": draw(d),
            f"h.{i}.mlp.c_fc.weight": draw(d, hidden),
            f"h.{i}.mlp.c_fc.bias": draw(hidden),
            f"h.{i}.mlp.c_proj.weight": draw(hidden, d),
            f"h.{i}.mlp.c_proj.bias": draw(d),
        }
    return state


def _loaded(state: dict[str, np.ndarray], config: GPTConfig = TINY) -> GPT:
    model = GPT(config)
    load_gpt2_state_dict(model, state)
    return model


def test_copies_embeddings_and_ties_output_head_to_token_table() -> None:
    state = _gpt2_state_dict(TINY)
    model = _loaded(state)

    np.testing.assert_array_equal(model.token_embedding, state["wte.weight"])
    np.testing.assert_array_equal(model.position_embedding, state["wpe.weight"])
    np.testing.assert_array_equal(model.w_head, state["wte.weight"])
    np.testing.assert_array_equal(model.b_head, np.zeros(TINY.vocab_size))
    np.testing.assert_array_equal(model.ln_f_gamma, state["ln_f.weight"])
    np.testing.assert_array_equal(model.ln_f_beta, state["ln_f.bias"])


def test_splits_fused_qkv_and_transposes_conv1d_weights() -> None:
    state = _gpt2_state_dict(TINY)
    model = _loaded(state)
    d = TINY.embedding_dim

    for i, block in enumerate(model.blocks):
        c_attn_w = state[f"h.{i}.attn.c_attn.weight"]
        c_attn_b = state[f"h.{i}.attn.c_attn.bias"]
        np.testing.assert_array_equal(block.w_q, c_attn_w[:, :d].T)
        np.testing.assert_array_equal(block.w_k, c_attn_w[:, d : 2 * d].T)
        np.testing.assert_array_equal(block.w_v, c_attn_w[:, 2 * d :].T)
        np.testing.assert_array_equal(block.b_q, c_attn_b[:d])
        np.testing.assert_array_equal(block.b_k, c_attn_b[d : 2 * d])
        np.testing.assert_array_equal(block.b_v, c_attn_b[2 * d :])
        np.testing.assert_array_equal(block.w_o, state[f"h.{i}.attn.c_proj.weight"].T)
        np.testing.assert_array_equal(block.b_o, state[f"h.{i}.attn.c_proj.bias"])
        np.testing.assert_array_equal(block.w_fc1, state[f"h.{i}.mlp.c_fc.weight"].T)
        np.testing.assert_array_equal(block.b_fc1, state[f"h.{i}.mlp.c_fc.bias"])
        np.testing.assert_array_equal(block.w_fc2, state[f"h.{i}.mlp.c_proj.weight"].T)
        np.testing.assert_array_equal(block.b_fc2, state[f"h.{i}.mlp.c_proj.bias"])
        np.testing.assert_array_equal(block.ln1_gamma, state[f"h.{i}.ln_1.weight"])
        np.testing.assert_array_equal(block.ln1_beta, state[f"h.{i}.ln_1.bias"])
        np.testing.assert_array_equal(block.ln2_gamma, state[f"h.{i}.ln_2.weight"])
        np.testing.assert_array_equal(block.ln2_beta, state[f"h.{i}.ln_2.bias"])


def test_loaded_parameters_are_independent_float64_copies() -> None:
    state = _gpt2_state_dict(TINY)
    model = _loaded(state)
    original = model.token_embedding.copy()

    state["wte.weight"][0, 0] += 1.0

    assert model.token_embedding.dtype == np.float64
    assert model.blocks[0].w_q.dtype == np.float64
    np.testing.assert_array_equal(model.token_embedding, original)


def test_accepts_transformer_prefix_tied_head_and_mask_buffers() -> None:
    plain = _gpt2_state_dict(TINY)
    state = {f"transformer.{name}": value for name, value in plain.items()}
    state["lm_head.weight"] = plain["wte.weight"].copy()
    for i in range(TINY.num_layers):
        # Older checkpoints store the causal mask as non-parameter buffers.
        mask = np.tril(np.ones((TINY.context_length, TINY.context_length)))
        state[f"transformer.h.{i}.attn.bias"] = mask[None, None]
        state[f"transformer.h.{i}.attn.masked_bias"] = np.array(-1e4)

    model = _loaded(state)

    np.testing.assert_array_equal(model.token_embedding, plain["wte.weight"])


def test_rejects_untied_output_head() -> None:
    state = _gpt2_state_dict(TINY)
    state["lm_head.weight"] = state["wte.weight"] + 1.0

    with pytest.raises(ValueError, match=r"lm_head\.weight"):
        _loaded(state)


def test_rejects_missing_parameter_without_modifying_model() -> None:
    state = _gpt2_state_dict(TINY)
    del state["h.1.mlp.c_fc.bias"]
    model = GPT(TINY)
    before = model.token_embedding.copy()

    with pytest.raises(ValueError, match=r"h\.1\.mlp\.c_fc\.bias"):
        load_gpt2_state_dict(model, state)

    np.testing.assert_array_equal(model.token_embedding, before)


def test_rejects_unexpected_parameter() -> None:
    state = _gpt2_state_dict(TINY)
    state["h.2.ln_1.weight"] = np.ones(TINY.embedding_dim, dtype=np.float32)

    with pytest.raises(ValueError, match=r"h\.2\.ln_1\.weight"):
        _loaded(state)


def test_rejects_shape_that_does_not_match_config() -> None:
    state = _gpt2_state_dict(TINY)
    state["wpe.weight"] = np.zeros((TINY.context_length + 1, TINY.embedding_dim))

    with pytest.raises(ValueError, match=r"wpe\.weight.*\(9, 6\).*\(8, 6\)"):
        _loaded(state)


def test_gpt2_small_config_matches_published_dimensions() -> None:
    assert GPT2_SMALL_CONFIG.vocab_size == 50257
    assert GPT2_SMALL_CONFIG.context_length == 1024
    assert GPT2_SMALL_CONFIG.embedding_dim == 768
    assert GPT2_SMALL_CONFIG.num_heads == 12
    assert GPT2_SMALL_CONFIG.num_layers == 12
    assert GPT2_SMALL_CONFIG.mlp_hidden_dim == 3072
