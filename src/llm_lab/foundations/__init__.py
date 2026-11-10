"""Foundations package: numerical reference implementations for core LLM operations.

The reference decoder-only GPT is split into focused modules, in reading
order: ``gpt_config`` (dimensions), ``gpt_ops`` (building blocks),
``transformer_block`` (one block), ``gpt`` (the assembled model) and
``generate`` (the decoding loop). ``training_examples`` builds the
aligned input/target windows that pretraining consumes, and
``decoding_filters`` implements the optional top-k/top-p truncations of
the decoding deep dive, applied by ``generate`` in sampling mode.
``gpt2_weights`` maps GPT-2 checkpoint parameters onto the reference model,
for the reference-parity check and for inference with published weights.

This package re-exports that public surface so callers can import from
``llm_lab.foundations`` directly. Exports are resolved lazily: importing
the package does not eagerly load the GPT implementation or optional
decoding filters. The minimal model route can therefore remain independent
of advanced decoding algorithms until a caller explicitly requests them.
"""

from importlib import import_module
from typing import Any

_EXPORTS = {
    "GPT": "gpt",
    "GPT2_SMALL_CONFIG": "gpt2_weights",
    "GPTConfig": "gpt_config",
    "TransformerBlock": "transformer_block",
    "causal_mask": "attention",
    "cross_entropy_from_logits": "losses",
    "cross_entropy_gradient": "losses",
    "gelu": "gpt_ops",
    "generate": "generate",
    "layer_norm": "gpt_ops",
    "linear": "gpt_ops",
    "load_gpt2_state_dict": "gpt2_weights",
    "scaled_dot_product_attention": "attention",
    "sliding_input_target_pairs": "training_examples",
    "softmax_with_temperature": "attention",
    "top_k_filter": "decoding_filters",
    "top_p_filter": "decoding_filters",
}

__all__ = list(_EXPORTS)


def __getattr__(name: str) -> Any:
    """Resolve a public symbol only when a caller requests it."""
    try:
        module_name = _EXPORTS[name]
    except KeyError as exc:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from exc

    module = import_module(f"{__name__}.{module_name}")
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """Expose lazy public symbols to introspection tools."""
    return sorted(set(globals()) | set(__all__))
