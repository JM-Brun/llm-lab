"""Load GPT-2 checkpoint parameters into the reference NumPy GPT.

The reference model and OpenAI's GPT-2 share one architecture: learned
absolute positions, pre-LN blocks, tanh-approximated GELU, biases on every
projection, layer norm with ``eps = 1e-5`` and an output head tied to the
token embedding. Only the *storage layout* differs, so a checkpoint can be
loaded by renaming and reshaping arrays, without changing any model code.
The mapping is the compatibility contract checked by the reference-parity
tests (milestone G9) and reused to load the published GPT-2 small weights
(milestone A1):

==================================  ===============================  ==========================
GPT-2 name (Hugging Face)           Reference attribute              Transformation
==================================  ===============================  ==========================
``wte.weight``  (V, d)              ``token_embedding``, ``w_head``  copy; head bias is zero
``wpe.weight``  (T, d)              ``position_embedding``           copy
``h.i.ln_1.weight`` / ``.bias``     ``ln1_gamma`` / ``ln1_beta``     copy
``h.i.attn.c_attn.weight`` (d, 3d)  ``w_q``, ``w_k``, ``w_v``        split columns, transpose
``h.i.attn.c_attn.bias``   (3d,)    ``b_q``, ``b_k``, ``b_v``        split
``h.i.attn.c_proj.weight`` (d, d)   ``w_o``                          transpose
``h.i.ln_2.weight`` / ``.bias``     ``ln2_gamma`` / ``ln2_beta``     copy
``h.i.mlp.c_fc.weight``   (d, 4d)   ``w_fc1``                        transpose
``h.i.mlp.c_proj.weight`` (4d, d)   ``w_fc2``                        transpose
``ln_f.weight`` / ``.bias``         ``ln_f_gamma`` / ``ln_f_beta``   copy
==================================  ===============================  ==========================

Why transpose? GPT-2 stores its projections as ``Conv1D`` weights of shape
``(in, out)`` and computes ``x @ W + b``. The reference ``linear`` keeps
the ``(out, in)`` convention of most textbooks and computes
``x @ W.T + b``. The same numbers therefore enter the model transposed.

This module reads no file and depends only on NumPy: the caller provides
the state dict (for example ``safetensors.numpy.load_file`` on the
published checkpoint, or ``state_dict()`` of a PyTorch model). Loading
changes parameter *values* only; the model stays inference-only.

Line-by-line walkthrough of the model receiving the weights:
- https://jm-brun.github.io/llm-lab/fr/gpt-model-walkthrough.html
- https://jm-brun.github.io/llm-lab/en/gpt-model-walkthrough.html
"""

from collections.abc import Mapping

import numpy as np
from numpy.typing import ArrayLike

from llm_lab.foundations.gpt import GPT
from llm_lab.foundations.gpt_config import GPTConfig
from llm_lab.foundations.gpt_ops import FloatArray

GPT2_SMALL_CONFIG = GPTConfig(
    vocab_size=50257,
    context_length=1024,
    embedding_dim=768,
    num_heads=12,
    num_layers=12,
    mlp_hidden_dim=3072,
)
"""Dimensions of the published 124M-parameter GPT-2 small checkpoint.

The number of heads cannot be read from the weights (the fused ``c_attn``
matrix has the same shape for any head count), so it is stated here.
"""

# Prefix used by ``GPT2LMHeadModel.state_dict()``; the published
# checkpoint file stores the same names without it.
_PREFIX = "transformer."
# Causal-mask buffers saved by older checkpoints. They are constants, not
# learned parameters; the reference model builds its own mask.
_MASK_BUFFER_SUFFIXES = (".attn.bias", ".attn.masked_bias")


def _parameter_tensors(state_dict: Mapping[str, ArrayLike]) -> dict[str, ArrayLike]:
    """Return the learned parameters under their unprefixed GPT-2 names.

    Raises:
        ValueError: If ``lm_head.weight`` is present but differs from
            ``wte.weight``: the reference head can only be loaded tied.
    """
    tensors = {name.removeprefix(_PREFIX): value for name, value in state_dict.items()}
    tensors = {
        name: value for name, value in tensors.items() if not name.endswith(_MASK_BUFFER_SUFFIXES)
    }
    head = tensors.pop("lm_head.weight", None)
    if (
        head is not None
        and "wte.weight" in tensors
        and not np.array_equal(np.asarray(head), np.asarray(tensors["wte.weight"]))
    ):
        raise ValueError("lm_head.weight differs from wte.weight; GPT-2 ties its output head")
    return tensors


def load_gpt2_state_dict(model: GPT, state_dict: Mapping[str, ArrayLike]) -> None:
    """Replace the parameters of ``model`` with those of a GPT-2 checkpoint.

    Every array is checked before any is assigned, so a rejected checkpoint
    leaves the model unchanged. Values are copied to float64: later edits
    of the source arrays do not leak into the model.

    Args:
        model: Reference GPT whose configuration matches the checkpoint
            (for the published weights, ``GPT(GPT2_SMALL_CONFIG)``).
        state_dict: Mapping from GPT-2 parameter names, with or without the
            ``transformer.`` prefix, to array-like values.

    Raises:
        ValueError: If a parameter is missing, unexpected, of the wrong
            shape for ``model.config``, or if the output head is untied.
    """
    config = model.config
    d = config.embedding_dim
    tensors = _parameter_tensors(state_dict)
    used: set[str] = set()

    def take(name: str, shape: tuple[int, ...]) -> FloatArray:
        if name not in tensors:
            raise ValueError(f"missing GPT-2 parameter {name!r}")
        array = np.array(tensors[name], dtype=np.float64)
        if array.shape != shape:
            raise ValueError(
                f"{name!r} has shape {array.shape}, expected {shape} for this GPTConfig"
            )
        used.add(name)
        return array

    wte = take("wte.weight", (config.vocab_size, d))
    # Collect every new value first; assign only once all checks passed.
    updates: list[tuple[object, str, FloatArray]] = [
        (model, "token_embedding", wte),
        # Tied head: the same matrix scores the output vocabulary. A copy
        # keeps the two attributes independent, as in the untied reference.
        (model, "w_head", wte.copy()),
        (model, "b_head", np.zeros(config.vocab_size, dtype=np.float64)),
        (model, "position_embedding", take("wpe.weight", (config.context_length, d))),
        (model, "ln_f_gamma", take("ln_f.weight", (d,))),
        (model, "ln_f_beta", take("ln_f.bias", (d,))),
    ]
    for i, block in enumerate(model.blocks):
        p = f"h.{i}."
        # Fused projection: columns [0, d) are Q, [d, 2d) K, [2d, 3d) V.
        c_attn_w = take(p + "attn.c_attn.weight", (d, 3 * d))
        c_attn_b = take(p + "attn.c_attn.bias", (3 * d,))
        hidden = config.mlp_hidden_dim
        updates += [
            (block, "ln1_gamma", take(p + "ln_1.weight", (d,))),
            (block, "ln1_beta", take(p + "ln_1.bias", (d,))),
            (block, "w_q", c_attn_w[:, :d].T.copy()),
            (block, "w_k", c_attn_w[:, d : 2 * d].T.copy()),
            (block, "w_v", c_attn_w[:, 2 * d :].T.copy()),
            (block, "b_q", c_attn_b[:d].copy()),
            (block, "b_k", c_attn_b[d : 2 * d].copy()),
            (block, "b_v", c_attn_b[2 * d :].copy()),
            (block, "w_o", take(p + "attn.c_proj.weight", (d, d)).T.copy()),
            (block, "b_o", take(p + "attn.c_proj.bias", (d,))),
            (block, "ln2_gamma", take(p + "ln_2.weight", (d,))),
            (block, "ln2_beta", take(p + "ln_2.bias", (d,))),
            (block, "w_fc1", take(p + "mlp.c_fc.weight", (d, hidden)).T.copy()),
            (block, "b_fc1", take(p + "mlp.c_fc.bias", (hidden,))),
            (block, "w_fc2", take(p + "mlp.c_proj.weight", (hidden, d)).T.copy()),
            (block, "b_fc2", take(p + "mlp.c_proj.bias", (d,))),
        ]

    unexpected = sorted(set(tensors) - used)
    if unexpected:
        raise ValueError(f"unexpected GPT-2 parameters for this GPTConfig: {unexpected}")
    for owner, attribute, value in updates:
        setattr(owner, attribute, value)
