# Project status

This is a high-level inventory; the [learning path](learning-path.md) owns curriculum order, module-level status, and evidence, while the [roadmap](roadmap.md) owns priorities. Update this summary when the underlying evidence or scope changes. A historical snapshot in either document is not a replacement for the current inventory.

| Area | Implemented and tested | Demonstrated | Still planned or incomplete |
|---|---|---|---|
| Learning site | Bilingual Quarto lessons, metadata and local-link checks | Site builds in CI; source-level reviews and worked checks exist | Independent learner validation and full visual/accessibility review |
| Inference | NumPy GPT configuration, attention, Transformer block, model, generation and decoding filters; unit and causal-invariance tests | Seeded, random-weight inference; mechanics only, not useful language generation | Comparison with a matched independent reference or trained checkpoint |
| Data and learning | Sliding input/target windows; cross-entropy and gradient helpers | Small hand-checkable windows and numerical tests | Complete corpus/tokenizer pipeline, optimizer, training loop and held-out evaluation |
| Experiments | Small synthetic decoding-distribution investigation | [Recorded configuration, result and limitations](../reports/decoding-distribution.md) | Model-level evaluation, data-backed experiments and claims about language quality |
| Reproduction | Python lockfile and automated quality checks; Quarto version pinned in CI | CI checks the configured properties | Clean-environment results depend on platform and external documentation dependencies; browser review remains separate |
| Reuse | Terms for project-owned code and prose in [LICENSE.md](../LICENSE.md) | Scope and exceptions documented | Rights and provenance of visual assets and externally sourced material remain under review |

The inference implementation does not train its parameters. Tests check the cases and properties they exercise, not full model quality, general numerical safety, or learner mastery.

A [learner-validation pilot protocol](learner-validation-pilot.md) is ready to run; it is not evidence that a participant has been observed.
