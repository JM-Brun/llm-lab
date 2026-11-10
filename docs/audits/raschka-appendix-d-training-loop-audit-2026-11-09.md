# Coverage audit — Raschka Appendix D: training-loop improvements

**Inspected:** 2026-11-09  
**Upstream repository:** [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch)  
**Inspected notebook:** [Appendix D — Adding Bells and Whistles to the Training Loop](https://github.com/rasbt/LLMs-from-scratch/blob/58f45ae5a7e330e234a7d4e4bba00752b236d9df/appendix-D/01_main-chapter-code/appendix-D.ipynb)  
**Inspected upstream commit:** `58f45ae5a7e330e234a7d4e4bba00752b236d9df`  
**Scope:** source coverage, current LLM Lab coverage and curriculum destination. This is not an implementation review or authorization for G8.

## 1. Inspection method and source boundary

Inspected the complete 39-cell notebook at the pinned commit, including its Markdown and code cells. The notebook is organised as:

- D.1 — learning-rate warmup;
- D.2 — cosine decay;
- D.3 — gradient clipping;
- D.4 — modified training function.

The notebook builds on previous chapters: GPT model, data loaders, loss calculation, evaluation helper and generation helper. It is a worked PyTorch training-loop extension, not a standalone training framework and not a derivation of reverse-mode differentiation or AdamW.

The source uses an example-specific configuration. Its warmup fraction, learning rates, clipping threshold, number of epochs, evaluation cadence and evaluation sample count are illustrative settings, not universal defaults.

## 2. Concept coverage and destination

| Concept | What Appendix D actually shows | When it matters / trade-off | LLM Lab destination and status |
|---|---|---|---|
| Linear learning-rate warmup | Raises LR from `initial_lr` to `peak_lr` over a configured number of steps | Can moderate early updates while optimization is settling. Adds schedule parameters and step-count assumptions; the example's 20% warmup is not a general prescription | G8 training-loop technique; optional Deepen, not a prerequisite for understanding gradients. No dedicated page or implementation currently evidenced |
| Cosine decay | After warmup, decreases LR along a half-cosine curve toward `min_lr` | Provides a smooth planned reduction during a finite run. Depends on a known training horizon; schedule shape and endpoint are experiment choices | G8 training-loop technique; optional Deepen. No dedicated page or implementation currently evidenced |
| Global gradient-norm clipping | Calls `torch.nn.utils.clip_grad_norm_(..., max_norm=1.0)` after backward and before optimizer step | Can bound the global gradient norm when gradients become unusually large. When clipping activates, it rescales the concatenated gradient vector without rotating that vector; the resulting parameter update still depends on the optimizer. The threshold is a hyperparameter, not a guarantee against instability | G8 optional gradient-handling technique. The current [Gradients lesson (FR)](../../site/fr/gradients.qmd) / [EN](../../site/en/gradients.qmd) mentions clipping only as an optimizer/training-dynamics choice; it does not yet explain the operation |
| Periodic train/validation evaluation | Calls an evaluation helper every `eval_freq` steps on train and validation loaders, with `eval_iter` limiting evaluation batches | Gives feedback on optimization and held-out behavior during training. More frequent/larger evaluation costs compute; validation monitoring must not be confused with final test-set assessment | G8 acceptance criterion and cross-cutting evaluation. Existing [learning path](../learning-path.md) and G8 issue #656 already specify separate train/validation curves; no standalone new page needed |
| Loss/LR/token monitoring | Stores train loss, validation loss, tokens seen and learning rates; prints periodic losses and plots curves | Makes a run inspectable and helps diagnose schedule/optimization behavior. Logging itself does not improve training; metrics need consistent definitions and sampling cadence | G8 acceptance criterion in #656. No additional concept or route stage |
| Epoch-level qualitative sample | Generates a sample after each epoch from a fixed starting context | Gives a qualitative signal complementary to scalar loss; samples are stochastic/context-dependent and cannot replace quantitative validation | Existing generation lesson plus G8 demonstration; optional monitoring hook, not a new module |
| Optimizer step | Reuses `torch.optim.AdamW`, calling `zero_grad`, `backward`, optional clipping and `step` | Separates gradient computation from the rule that updates parameters. Appendix D uses AdamW but does not derive or implement its internals | G8 already specifies an initial SGD update then AdamW; AdamW internals remain Deepen |
| Checkpointing / resume | No model or optimizer checkpoint save/load protocol is implemented in this notebook | Needed to preserve a run, resume training and hand trained weights to generation; correct resume also needs relevant optimizer/scheduler state, not only model weights | Explicit G8 acceptance requirement and #656. Appendix D is not evidence of this capability |
| Mixed precision, accumulation, distributed training | Not implemented in this Appendix D notebook | These are resource/performance techniques with additional numerical, synchronization and memory trade-offs | Not in this appendix's evidence; keep out of G8's minimal acceptance path unless separately justified |

## 3. Repository crosswalk

### Existing canonical explanations

- [Training examples — EN](../../site/en/training-examples.qmd) / [FR](../../site/fr/training-examples.qmd): shifted input/target sequences and teacher forcing. The lesson explicitly says its reference function only constructs windows; it does not run a trainable forward pass or update parameters.
- [Gradients — EN](../../site/en/gradients.qmd) / [FR](../../site/fr/gradients.qmd): gradient with respect to logits, chain rule, gradient-descent update, numerical checking. It distinguishes gradient calculation from optimizer dynamics and currently names clipping/scheduling only at a high level.
- [Learning path](../learning-path.md): training is one sibling branch after the shared predictor; schedulers, clipping and optimizer variants are classified as optional Deepen.
- [G8 specification, issue #656](https://github.com/JM-Brun/llm-lab/issues/656): owns backward through model parameters, optimizer, training loop, train/validation curves and checkpoint-to-generation handoff.

### Implementation evidence

The current public implementation audit records:
- shifted windows in `src/llm_lab/foundations/training_examples.py`;
- cross-entropy and its gradient with respect to logits in `src/llm_lab/foundations/losses.py`;
- forward operations in `src/llm_lab/foundations/gpt_ops.py`;
- no backward propagation through GPT parameters, optimizer, parameter-update loop, validation runner or checkpoint loader.

See [build-milestones evidence audit](build-milestones-evidence-audit-2026-11-06.md). The G8 status remains partial primitives only.

## 4. Technical qualifications from primary documentation

These references validate API semantics; they do not imply that LLM Lab uses PyTorch:

- [PyTorch `clip_grad_norm_`](https://docs.pytorch.org/docs/main/generated/torch.nn.utils.clip_grad_norm_.html): computes the norm over all parameter gradients as if concatenated into one vector and modifies gradients in place. The API default is an L2 norm (`norm_type=2.0`); the older non-underscore spelling is deprecated.
- [PyTorch `CosineAnnealingLR`](https://docs.pytorch.org/docs/main/generated/torch.optim.lr_scheduler.CosineAnnealingLR.html): documents the cosine schedule and its parameters. Appendix D instead writes its warmup-plus-cosine schedule explicitly inside the loop.
- [PyTorch optimizer scheduling guidance](https://docs.pytorch.org/docs/main/optim.html): recommends stepping the optimizer before stepping most learning-rate schedulers.
- [PyTorch AdamW](https://docs.pytorch.org/docs/stable/generated/torch.optim.AdamW): defines decoupled weight decay and exposes optimizer state serialization. Appendix D only instantiates AdamW; it does not teach its algorithm.

A useful distinction: clipping is applied to gradients before the parameter update; a learning-rate schedule changes the scale of the optimizer's update; neither changes the mathematical definition of the loss gradient. Validation is measurement, not an update operation.

## 5. Upstream code corrections noted by the notebook

The inspected notebook explicitly records differences from the printed book:
1. An unused `warmup_steps = 20` line is left over in the book and is not used.
2. The AdamW example in the book omitted the explicit learning-rate assignment; the notebook sets it.
3. The book's strict `global_step > warmup_steps` skips clipping at the first step after warmup; the notebook uses `>=`.

These are corrections to a particular example, not general algorithmic rules. Preserve the source version when reproducing its code.

## 6. Audit decision

- **No new concept IDs, computational graph nodes/edges, learning-route stages, pages or workflows.**
- Keep warmup, LR decay, clipping and monitoring as optional techniques attached to the existing G8 training-loop implementation, with concise explanations only when a learner needs to interpret the run.
- Keep manual backward through the model as the core mathematical/implementation gap. Appendix D relies on PyTorch autograd and does not close it.
- Keep checkpointing as a separate explicit G8 requirement; do not attribute it to Appendix D.
- No new issue is justified: #656 already owns the real implementation gaps and acceptance criteria. #105 remains the source-coverage audit, not a second implementation tracker.
- G8's private prerequisite gate remains unchanged. This audit does not authorize implementation.

## 7. Validation still required for closing #105

- Review rendered EN/FR pages in browser for visual/accessibility parity (source-level content parity has been checked for the two relevant lessons).
- Verify local links and Quarto output after the documentation change.
- Do not claim learner validation or reproduce the PyTorch notebook as part of this audit.
