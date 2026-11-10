"""Reference parity (milestone G9): the NumPy GPT against Hugging Face GPT-2.

Both implementations receive the *same* parameter values, so any output
difference measures an architectural or numerical mismatch, never a
difference in learning. The reference is a small, randomly initialized
``GPT2LMHeadModel`` built locally: no checkpoint is downloaded.

Compatibility contract checked here: identical dimensions, tied output head,
tanh GELU (``gelu_new``), layer-norm ``eps = 1e-5``, eager attention and no
dropout (evaluation mode). Stated tolerances:

- float64 on both sides: ``atol = 1e-10``; agreement is then structural,
  limited only by the order of floating-point operations;
- float32 reference (the dtype of the published checkpoint): ``atol = 1e-5``.
"""

import numpy as np
import pytest

from llm_lab.foundations.generate import generate
from llm_lab.foundations.gpt import GPT
from llm_lab.foundations.gpt2_weights import load_gpt2_state_dict
from llm_lab.foundations.gpt_config import GPTConfig
from llm_lab.foundations.gpt_ops import layer_norm

torch = pytest.importorskip("torch")
transformers = pytest.importorskip("transformers")

CONFIG = GPTConfig(
    vocab_size=37,
    context_length=12,
    embedding_dim=16,
    num_heads=4,
    num_layers=3,
    mlp_hidden_dim=64,
)


def _reference(config: GPTConfig, dtype: object) -> object:
    """Build a Hugging Face GPT-2 with random, distinct parameter values."""
    hf_config = transformers.GPT2Config(
        vocab_size=config.vocab_size,
        n_positions=config.context_length,
        n_embd=config.embedding_dim,
        n_layer=config.num_layers,
        n_head=config.num_heads,
        n_inner=config.mlp_hidden_dim,
        activation_function="gelu_new",
        layer_norm_epsilon=1e-5,
        resid_pdrop=0.0,
        embd_pdrop=0.0,
        attn_pdrop=0.0,
        bos_token_id=0,
        eos_token_id=0,
        pad_token_id=0,
        attn_implementation="eager",
    )
    torch.manual_seed(0)
    reference = transformers.GPT2LMHeadModel(hf_config).eval().to(dtype)
    # Default initialization sets layer-norm weights to 1 and biases to 0,
    # which would hide a swapped or misplaced vector. Redraw everything.
    with torch.no_grad():
        for parameter in reference.parameters():
            parameter.normal_(0.0, 0.3)
    assert reference.lm_head.weight is reference.transformer.wte.weight
    return reference


def _numpy_model(reference: object) -> GPT:
    model = GPT(CONFIG)
    state = {name: value.numpy() for name, value in reference.state_dict().items()}
    load_gpt2_state_dict(model, state)
    return model


def _token_ids() -> np.ndarray:
    rng = np.random.default_rng(3)
    return rng.integers(0, CONFIG.vocab_size, size=(2, CONFIG.context_length))


def test_logits_match_reference_in_float64() -> None:
    reference = _reference(CONFIG, torch.float64)
    model = _numpy_model(reference)
    ids = _token_ids()

    with torch.no_grad():
        expected = reference(torch.from_numpy(ids)).logits.numpy()

    np.testing.assert_allclose(model.forward(ids), expected, rtol=0.0, atol=1e-10)


def test_hidden_states_match_reference_layer_by_layer() -> None:
    reference = _reference(CONFIG, torch.float64)
    model = _numpy_model(reference)
    ids = _token_ids()

    with torch.no_grad():
        hidden = reference(torch.from_numpy(ids), output_hidden_states=True).hidden_states
    # Hugging Face returns the embeddings, then each block output; its last
    # entry already includes the final layer norm.
    x = model.token_embedding[ids] + model.position_embedding[: ids.shape[1]]
    np.testing.assert_allclose(x, hidden[0].numpy(), rtol=0.0, atol=1e-12)
    for i, block in enumerate(model.blocks):
        x = block.forward(x)
        if i == len(model.blocks) - 1:
            x = layer_norm(x, model.ln_f_gamma, model.ln_f_beta)
        np.testing.assert_allclose(x, hidden[i + 1].numpy(), rtol=0.0, atol=1e-10)


def test_logits_match_float32_reference_within_stated_tolerance() -> None:
    reference = _reference(CONFIG, torch.float32)
    model = _numpy_model(reference)
    ids = _token_ids()

    with torch.no_grad():
        expected = reference(torch.from_numpy(ids)).logits.numpy()

    np.testing.assert_allclose(model.forward(ids), expected, rtol=0.0, atol=1e-5)


def test_greedy_generation_matches_reference() -> None:
    reference = _reference(CONFIG, torch.float64)
    model = _numpy_model(reference)
    prompt = np.array([5, 1, 30], dtype=np.int64)
    new_tokens = CONFIG.context_length - prompt.size

    with torch.no_grad():
        expected = reference.generate(
            torch.from_numpy(prompt[None]),
            attention_mask=torch.ones((1, prompt.size), dtype=torch.long),
            max_new_tokens=new_tokens,
            min_new_tokens=new_tokens,
            do_sample=False,
        )[0].numpy()

    np.testing.assert_array_equal(generate(model, prompt, new_tokens), expected)
