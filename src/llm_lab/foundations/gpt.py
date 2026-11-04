"""The assembled reference decoder-only GPT (inference only).

This module wires the model together. Reading order for the reference
implementation:

- ``gpt_config`` defines the dimensions (``GPTConfig``);
- ``gpt_ops`` provides the numerical building blocks;
- ``transformer_block`` implements one pre-LN block;
- **this file** stacks the blocks between the embeddings and the output
  projection;
- ``generate`` runs the autoregressive decoding loop on top of it.

Architecture implemented here: token and position embeddings, then
``num_layers`` pre-LN blocks, a final layer norm, and an untied output
projection to vocabulary logits. Parameters are drawn once from
``config.seed`` and never updated: this module implements the inference
branch only (milestones G4-G7 of the build path).

Scope and limitations:

- NumPy only, float64, educational clarity over speed.
- Inference and generation only: no backpropagation, no optimizer, no
  training loop.
- A randomly initialized model produces incoherent text. This is expected:
  it separates the mechanics of generation from the quality acquired by
  learning.

Line-by-line walkthrough (bilingual site pages):
- https://jm-brun.github.io/llm-lab/fr/gpt-model-walkthrough/
- https://jm-brun.github.io/llm-lab/en/gpt-model-walkthrough/

Related concept pages:
- Transformer overview: https://jm-brun.github.io/llm-lab/fr/transformer/
- Embedding space: https://jm-brun.github.io/llm-lab/fr/embedding-space/
- Positional information: https://jm-brun.github.io/llm-lab/fr/positional-encoding/
- Logits: https://jm-brun.github.io/llm-lab/fr/logits/
"""

import numpy as np
from numpy.typing import NDArray

from llm_lab.foundations.gpt_config import GPTConfig
from llm_lab.foundations.gpt_ops import (
    FloatArray,
    _init_linear,
    _init_matrix,
    layer_norm,
    linear,
)
from llm_lab.foundations.transformer_block import TransformerBlock


class GPT:
    """A minimal decoder-only GPT with learned absolute position embeddings.

    The model implements the inference branch only (milestones G4-G7):
    ``forward`` returns next-token logits for every position, and
    :func:`llm_lab.foundations.generate.generate` runs the autoregressive
    loop with fixed parameters.
    """

    def __init__(self, config: GPTConfig) -> None:
        """Draw all parameters of the model from one seeded generator.

        Why one generator for the whole model?
            A single ``default_rng(config.seed)`` walked in a fixed order
            (embeddings, blocks in stack order, head) makes every
            parameter a deterministic function of the configuration.
            Two models built from the same ``GPTConfig`` are identical.

        Args:
            config: Validated model configuration.
        """
        self.config = config
        rng = np.random.default_rng(config.seed)
        d = config.embedding_dim

        # Token embedding table: one learned vector per vocabulary entry.
        # Fancy indexing (token_embedding[ids]) performs the lookup.
        self.token_embedding: FloatArray = _init_matrix(rng, (config.vocab_size, d))
        # Learned absolute position embedding: one vector per position
        # slot 0..T-1, added to the token vector at the same position.
        self.position_embedding: FloatArray = _init_matrix(rng, (config.context_length, d))
        # The stack of identical blocks; each draws its parameters from
        # the same generator, in order, which keeps initialization
        # reproducible.
        self.blocks = [TransformerBlock(config, rng) for _ in range(config.num_layers)]
        # Final layer norm applied after the last block, before the head.
        self.ln_f_gamma: FloatArray = np.ones(d, dtype=np.float64)
        self.ln_f_beta: FloatArray = np.zeros(d, dtype=np.float64)
        # Output projection ("head"): d -> vocab_size, untied from the
        # token embedding (a separate matrix, unlike weight tying).
        self.w_head, self.b_head = _init_linear(rng, config.vocab_size, d, 0.02)

    def forward(self, token_ids: NDArray[np.integer]) -> FloatArray:
        """Return next-token logits for each position of a batch of sequences.

        Shape journey of one pass (B=batch, T=sequence length,
        V=vocabulary, d=embedding width)::

            (B, T) ids
              -> token_embedding[ids]              (B, T, d)
              -> + position_embedding[:T]          (B, T, d) broadcast
              -> num_layers x TransformerBlock     (B, T, d)
              -> final layer norm                  (B, T, d)
              -> output projection                 (B, T, V) logits

        Args:
            token_ids: Integer array of shape (batch, seq_len) with values
                in [0, vocab_size) and seq_len <= context_length.

        Returns:
            Logits of shape (batch, seq_len, vocab_size). Position t holds
            the scores for the token that may follow position t.

        Raises:
            ValueError: If token_ids is not a non-empty 2D integer array,
                if the sequence exceeds context_length, or if ids are out
                of range.
        """
        # Validate everything before computing: a clear, named error here
        # beats a NumPy indexing crash three lines later.
        ids = np.asarray(token_ids)
        if ids.ndim != 2:
            raise ValueError("token_ids must have shape (batch, seq_len)")
        if not np.issubdtype(ids.dtype, np.integer):
            raise ValueError("token_ids must contain integer values")
        if ids.shape[0] == 0 or ids.shape[1] == 0:
            raise ValueError("token_ids must have a non-empty batch and sequence")
        if ids.shape[1] > self.config.context_length:
            raise ValueError(
                f"seq_len {ids.shape[1]} exceeds context_length {self.config.context_length}"
            )
        if np.any(ids < 0) or np.any(ids >= self.config.vocab_size):
            raise ValueError("token ids are out of range [0, vocab_size)")

        seq_len = ids.shape[1]
        # Fancy indexing with (B, T) integer ids yields (B, T, d): each id
        # selects one row of the (V, d) table. Then the (T, d) position
        # table is sliced to the current length and broadcast over the
        # batch: every sequence shares the same absolute positions.
        x = self.token_embedding[ids] + self.position_embedding[:seq_len]
        # Each block rewrites x in place of the variable; the residual
        # paths inside the blocks guarantee x keeps a copy of its input.
        for block in self.blocks:
            x = block.forward(x)
        x = layer_norm(x, self.ln_f_gamma, self.ln_f_beta)
        # Untied head: a plain linear layer to V logits per position.
        return linear(x, self.w_head, self.b_head)

    def num_parameters(self) -> int:
        """Return the total number of scalar parameters of the model.

        The count is written as an explicit walk over every parameter
        array instead of a formula, so the test can compare it against the
        independent closed-form count derived from the configuration.
        """
        arrays = [
            self.token_embedding,
            self.position_embedding,
            self.ln_f_gamma,
            self.ln_f_beta,
            self.w_head,
            self.b_head,
        ]
        for block in self.blocks:
            arrays += [
                block.ln1_gamma,
                block.ln1_beta,
                block.w_q,
                block.b_q,
                block.w_k,
                block.b_k,
                block.w_v,
                block.b_v,
                block.w_o,
                block.b_o,
                block.ln2_gamma,
                block.ln2_beta,
                block.w_fc1,
                block.b_fc1,
                block.w_fc2,
                block.b_fc2,
            ]
        return int(sum(array.size for array in arrays))
