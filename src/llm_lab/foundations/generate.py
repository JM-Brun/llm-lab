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
       from the temperature-scaled distribution;
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
        rng: Seeded generator used for sampling; required when ``greedy``
            is False. Sampling is reproducible only when this generator
            is seeded.

    Returns:
        A 1D int64 array of length ``prompt + max_new_tokens`` containing
        the prompt ids followed by the generated ids.

    Raises:
        ValueError: If the prompt is not a non-empty 1D integer array
            within range, if max_new_tokens is negative, if
            temperature <= 0, or if no rng is provided for sampling.
    """
    # Validate the prompt before touching the model: shape, dtype, range.
    ids = np.asarray(prompt_ids)
    if ids.ndim != 1 or ids.shape[0] == 0:
        raise ValueError("prompt_ids must be a non-empty 1D array of token ids")
    if not np.issubdtype(ids.dtype, np.integer):
        raise ValueError("prompt_ids must contain integer values")
    if ids.shape[0] > model.config.context_length:
        raise ValueError(
            f"prompt length {ids.shape[0]} exceeds context_length "
            f"{model.config.context_length}"
        )
    if np.any(ids < 0) or np.any(ids >= model.config.vocab_size):
        raise ValueError("prompt token ids are out of range [0, vocab_size)")
    if max_new_tokens < 0:
        raise ValueError("max_new_tokens must be >= 0")
    if temperature <= 0:
        raise ValueError("temperature must be strictly positive")
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
            # Temperature scales the logits before softmax: T < 1 sharpens
            # the distribution, T > 1 flattens it. rng.choice then draws
            # one id from that distribution.
            probs = softmax_with_temperature(logits, temperature=temperature)
            next_token = int(rng.choice(model.config.vocab_size, p=probs))
        # Append and loop: the generated token becomes context.
        context = np.append(context, np.int64(next_token))
    return np.asarray(context, dtype=np.int64)
