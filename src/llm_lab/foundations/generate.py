"""Autoregressive generation with the reference decoder-only GPT.

This module implements the decoding loop that turns next-token logits
into a sequence: at each step the model reprocesses the current context,
reads the logits at the final position, selects one token (greedy argmax
or a sample from the temperature-scaled distribution), appends it, and
repeats. There is no training and no early-stopping rule here.

Deliberate limitations, documented rather than hidden:

- **No KV cache.** Each step recomputes attention over the whole window.
  This is O(T^2) work per generated token where a cache would make the
  incremental step much cheaper. The reference chooses inspectability
  first; caching is an optimization topic, not a conceptual one.
- **No early stopping.** Production decoders stop at an end-of-text
  token; that rule belongs to the tokenizer/vocabulary layer, which this
  milestone does not include.
- **No configurable processor chain.** The optional ``top_k``/``top_p``
  truncations apply to the sampling path only, in the fixed order
  temperature -> top-k -> top-p; there is no beam search, contrastive
  decoding or repetition penalty.

Line-by-line walkthrough (bilingual site pages):
- https://jm-brun.github.io/llm-lab/fr/gpt-generation-walkthrough/
- https://jm-brun.github.io/llm-lab/en/gpt-generation-walkthrough/

Related concept pages:
- Generation step by step:
  https://jm-brun.github.io/llm-lab/fr/generation/
- Logits: https://jm-brun.github.io/llm-lab/fr/logits/
- Probabilities: https://jm-brun.github.io/llm-lab/fr/probabilites/
"""

import numpy as np
from numpy.typing import NDArray

from llm_lab.foundations.attention import softmax_with_temperature
from llm_lab.foundations.decoding_filters import top_k_filter, top_p_filter
from llm_lab.foundations.gpt import GPT

# Token ids are int64 throughout the reference implementation.
IntArray = NDArray[np.int64]


def generate(
    model: GPT,
    prompt_ids: NDArray[np.integer],
    max_new_tokens: int,
    *,
    temperature: float = 1.0,
    greedy: bool = True,
    top_k: int | None = None,
    top_p: float | None = None,
    rng: np.random.Generator | None = None,
) -> IntArray:
    """Generate token ids autoregressively with fixed parameters.

    One step of the loop, in order:

    1. take the last ``context_length`` tokens of the current sequence
       (the sliding window);
    2. run one forward pass on that window as a batch of one sequence;
    3. read the logits at the final position -- position T-1 predicts
       the token that follows position T-1;
    4. select one token: ``argmax`` when ``greedy``, otherwise a sample
       from the temperature-scaled distribution, optionally truncated to
       its top-k entries and/or its top-p nucleus (then renormalized);
    5. append the token and repeat, until ``max_new_tokens`` are produced.

    Args:
        model: A decoder-only GPT with fixed parameters.
        prompt_ids: 1D integer array of prompt ids, with
            1 <= length <= context_length and values in [0, vocab_size).
        max_new_tokens: Number of tokens to generate (>= 0).
        temperature: Sampling temperature (> 0); it only affects sampling,
            but is validated in both modes so that a latent invalid value
            cannot hide behind greedy decoding.
        greedy: If True, select the argmax token at each step.
        top_k: Optional per-step truncation for sampling: keep only the
            ``k`` most probable tokens (integer >= 1). Validated in both
            modes but ignored when ``greedy`` is True.
        top_p: Optional nucleus truncation for sampling: keep the smallest
            set whose cumulative mass reaches ``p`` (0 < p <= 1).
            Validated in both modes but ignored when ``greedy`` is True.
        rng: Seeded generator used for sampling; required when ``greedy``
            is False. Sampling is reproducible only when this generator
            is seeded.

    Returns:
        A 1D int64 array of length ``prompt + max_new_tokens`` containing
        the prompt ids followed by the generated ids.

    Raises:
        ValueError: If the prompt is not a non-empty 1D integer array
            within range, if max_new_tokens is negative, if
            temperature <= 0, if top_k is provided and is not an integer
            >= 1, if top_p is provided and lies outside (0, 1], or if
            no rng is provided for sampling.
    """
    # Validate the prompt before touching the model: shape, dtype, range.
    ids = np.asarray(prompt_ids)
    if ids.ndim != 1 or ids.shape[0] == 0:
        raise ValueError("prompt_ids must be a non-empty 1D array of token ids")
    if not np.issubdtype(ids.dtype, np.integer):
        raise ValueError("prompt_ids must contain integer values")
    if ids.shape[0] > model.config.context_length:
        raise ValueError(
            f"prompt length {ids.shape[0]} exceeds context_length {model.config.context_length}"
        )
    if np.any(ids < 0) or np.any(ids >= model.config.vocab_size):
        raise ValueError("prompt token ids are out of range [0, vocab_size)")
    if max_new_tokens < 0:
        raise ValueError("max_new_tokens must be >= 0")
    if temperature <= 0:
        raise ValueError("temperature must be strictly positive")
    if top_k is not None and (top_k < 1 or not np.issubdtype(np.asarray(top_k).dtype, np.integer)):
        raise ValueError("top_k must be an integer >= 1 when provided")
    if top_p is not None and not 0.0 < top_p <= 1.0:
        raise ValueError("top_p must be in the interval (0, 1] when provided")
    if not greedy and rng is None:
        raise ValueError("rng is required when greedy is False")

    # Copy and normalize to int64 so that appending never mutates the
    # caller's array and the returned dtype is stable.
    context = ids.astype(np.int64, copy=True)
    for _ in range(max_new_tokens):
        # Sliding window: once the sequence exceeds context_length, only
        # the last context_length tokens fit -- and matter -- for the
        # next prediction.
        window = context[-model.config.context_length :]
        # Batch of one sequence: forward expects (batch, seq_len).
        # [0, -1, :] selects batch 0, last position, all logits.
        logits = model.forward(window[None, :])[0, -1, :]
        if greedy:
            # Deterministic: the most probable token under the current
            # logits. Ties resolve to the lowest index (NumPy argmax).
            next_token = int(np.argmax(logits))
        else:
            # rng was validated before the loop; the assert only narrows
            # the Optional type for mypy.
            assert rng is not None
            # Temperature scales the logits before softmax: T < 1 sharpens
            # the distribution, T > 1 flattens it. Optional truncation then
            # zeroes the tail and renormalizes; the fixed temperature ->
            # top-k -> top-p order is a teaching convention. rng.choice
            # finally draws one id from the retained distribution.
            probs = softmax_with_temperature(logits, temperature=temperature)
            if top_k is not None:
                probs = top_k_filter(probs, k=top_k)
            if top_p is not None:
                probs = top_p_filter(probs, p=top_p)
            next_token = int(rng.choice(model.config.vocab_size, p=probs))
        # Append and loop: the generated token becomes context.
        context = np.append(context, np.int64(next_token))
    return np.asarray(context, dtype=np.int64)
