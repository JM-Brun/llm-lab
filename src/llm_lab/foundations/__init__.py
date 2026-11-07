"""Foundations package with lazy, compatibility-preserving public exports.

Importing the package itself does not import the GPT implementation or optional
extensions. Public names are resolved on first access, so the minimal model
route can depend on the package namespace without eagerly loading advanced
decoding algorithms. Existing package-level imports remain supported.
"""

from importlib import import_module
from typing import Any

_EXPORTS = {
    "GPT": "gpt",
    "GPTConfig": "gpt_config",
    "TransformerBlock": "transformer_block",
    "causal_mask": "attention",
    "cross_entropy_from_logits": "losses",
    "cross_entropy_gradient": "losses",
    "gelu": "gpt_ops",
    "generate": "generate",
    "layer_norm": "gpt_ops",
    "linear": "gpt_ops",
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
