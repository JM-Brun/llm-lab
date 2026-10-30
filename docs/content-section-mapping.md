# Content map: understanding, building, deepening, experimenting

**Status:** editorial classification baseline, 2026-10-30.  
**Purpose:** make the reader-facing boundary between the conceptual course, the guided build, optional depth, and practice explicit. This is a source inventory, not a claim that every mapped implementation or experiment exists.

## 1. The four destinations have different jobs

| Destination | Main learner question | Owns | Does not own |
|---|---|---|---|
| **Understand** | What happens in an LLM, why does the mechanism exist, and how does it fit into the whole? | System explanations, LLM-specific definitions, intuitions, essential equations, small worked examples, assumptions and limitations | Full software implementations, broad prerequisite textbooks, long derivations unrelated to the LLM question |
| **Build** | How do I turn these ideas into a working small GPT? | Ordered implementation milestones, Python/PyTorch code, interfaces, tensor contracts, tests, checkpoints, reproducibility and implementation evidence | A second explanation of every concept; general mathematical courses |
| **Deepen** | Why does the mechanism have these properties, and where do the assumptions or limits come from? | Detailed derivations, mathematical foundations, shape algebra, alternative formulations, variants, research discussions and critical analyses | Mandatory prerequisites for the first conceptual overview or first implementation |
| **Practice & experiment** | Can I calculate, implement, test, vary or falsify something? | Exercises, hidden solutions, interactive explorations, unit/property tests as learning activities, experiment protocols and reports | Untethered demonstrations, decorative widgets, or claims that a toy experiment establishes production-scale behavior |

**Classification is based on the primary learning objective, not on the presence of equations or code.** A concept lesson may contain a small equation or short illustrative snippet and remain in Understand. A Build milestone may explain only the local mathematics needed to implement the next component. A Deepen page may include runnable code as evidence without becoming an implementation tutorial.

## 2. Reader-facing page inventory

Paths are the canonical source files. French and English counterparts are listed together; a counterpart's existence does not establish semantic, scientific, or rendered parity.

| Existing page pair (FR / EN) | Primary destination | Editorial role and boundary | Recommended treatment |
|---|---|---|---|
| `index.qmd` / `en/index.qmd` | Entry point | Help readers choose a route; explain the project's scope and current status | Present the four destinations clearly; avoid implying that math/tensor mastery precedes building |
| `transformer.qmd` / `transformer.qmd` | Understand | System-level GPT/Transformer explanation | Keep concise and system-oriented; link to build milestones and optional details |
| `transformer-history.qmd` / `transformer-history.qmd` | Understand (context) | Historical and architectural context | Keep as supporting context, not a prerequisite |
| `text-data.qmd` / `text-data.qmd` | Understand | Explain how raw text becomes usable model input | Keep concept-first; link to tokenizer/data preparation in Build |
| `unicode-text.qmd` / `unicode-text.qmd` | Understand (supporting concept) | Explain text representation issues that affect preprocessing | Keep only the Unicode detail needed to reason about real text; deeper encoding detail optional |
| `tokenization-strategies.qmd` / `tokenization-strategies.qmd` | Understand | Explain tokenization choices and their consequences | Keep the conceptual comparison; implementation belongs to Build |
| `training-examples.qmd` / `training-examples.qmd` | Understand + Build bridge | Explain context windows, shifted targets, document boundaries and masks | Keep as the canonical explanation; Build should link here and add executable data-pipeline work only when it exists |
| `embedding-space.qmd` / `embedding-space.qmd` | Understand | Explain token embeddings and their role | Keep LLM-specific intuition and interpretation; link to shape details |
| `positional-encoding.qmd` / `positional-encoding.qmd` | Understand + Deepen | Explain why position matters and compare positional mechanisms | Keep first-pass role/intuitions in Understand; make RoPE derivations and variant details optional |
| `contextualized-representations.qmd` / `contextualized-representations.qmd` | Understand | Explain how representations become context-dependent | Keep as a conceptual bridge between input representations and Transformer computation |
| `queries-keys-values.qmd` / `queries-keys-values.qmd` | Understand | Explain the roles of Q, K and V in attention | Keep intuition and data flow; link tensor layouts to Deepen and code to Build when available |
| `scaled-dot-product-attention.qmd` / `scaled-dot-product-attention.qmd` | Understand + Deepen | Explain attention's computation and why it is scaled | Keep the essential mechanism; move extended derivations/variance analysis to optional depth within the page or a justified companion |
| `causal-masking.qmd` / `causal-masking.qmd` | Understand | Explain the no-future-information constraint | Keep the causal invariant and a minimal counterexample; implementation/tests belong to Build and Practice |
| `logits.qmd` / `logits.qmd` | Understand | Explain the model's vocabulary scores | Keep output shape and interpretation in the LLM context; avoid general score-function theory |
| `probabilites.qmd` / `probabilities.qmd` | Understand | Explain next-token categorical distributions | Keep softmax and decoding interpretation; distinguish confidence from truth and calibration |
| `vraisemblance.qmd` / `likelihood.qmd` | Understand + Deepen | Explain autoregressive sequence likelihood and token probabilities | Keep chain-rule factorization and teacher-forcing context; link general maximum-likelihood theory as optional depth |
| `entropy.qmd` / `entropy.qmd` | Understand (focused concept) | Explain uncertainty in a next-token distribution | Keep the current LLM-specific scope; do not restore a broad general information-theory chapter |
| `cross-entropy.qmd` / `cross-entropy.qmd` | Understand + Build bridge | Explain token-level negative log-likelihood and the training objective | Keep the identities needed for the LLM objective; Build owns PyTorch use, reduction and tests |
| `loss.qmd` / `loss.qmd` | Understand + Build bridge | Explain target alignment, masking and objective aggregation | Keep conceptual objective and pitfalls; implementation claims must match actual code/tests |
| `gradients.qmd` / `gradients.qmd` | Understand + Deepen | Explain how loss changes flow toward model parameters | Keep the LLM-specific gradient-flow story; detailed chain-rule/optimization theory remains optional |
| `mathematical-foundations.qmd` / `mathematical-foundations.qmd` | Understand (orientation map) | Compact map from logits to probabilities, likelihood, loss and gradients | Keep as an applied map, not a general prerequisite syllabus; its existing framing already says this is not a prerequisite course |
| `tensors.qmd` / `tensors.qmd` | Deepen (with Build links) | Reference for tensor shapes, axes, projections and common LLM operations | Keep Transformer-specific shape semantics; state explicitly that advanced tensor theory is not a prerequisite; Build teaches only operations as needed |
| `cosine-similarity.qmd` / `cosine-similarity.qmd` | Deepen / critical case study | Examine a geometric measure and its limitations in representation analysis | Keep optional and link from embedding concepts; do not make it part of the minimum GPT build |
| `linearite-embeddings.qmd` / `embedding-linearity.qmd` | Deepen / critical case study | Examine and challenge linearity claims about embeddings | Keep as optional research-oriented reading, not a core construction step |
| `evaluation-experimentale.qmd` / `experimental-evaluation.qmd` | Practice & experiment (method) | Explain experimental evaluation, evidence and limits | Keep as the shared evaluation-method reference; link from concept and build milestones |
| `exercises.qmd` / `exercises.qmd` | Practice & experiment | Entry point for conceptual and practical exercises | Keep exercises separate from lesson prose; label exercise type and link back to canonical concepts |
| `glossary.qmd` / `glossary.qmd` | Reference | Concise definitions and navigation | Keep concise; definitions point to canonical concept pages |
| `references.qmd` | Reference | Curated sources and provenance | Keep as a cross-cutting reference, not a learning stage |

## 3. What belongs in the guided build

The Build route is a **sequence of implementation checkpoints**, not a parallel concept catalogue. It reuses the canonical pages above.

| Build milestone | Conceptual source pages | Minimum practical learning | Current repository evidence |
|---|---|---|---|
| G0 — Define the target | Transformer overview, history, glossary | State what a decoder-only GPT does and distinguish it from other model families | Conceptual overview exists; a broader LLM panorama remains tracked by #108 |
| G1 — Prepare text and tokenizer | Text/data, Unicode, tokenization | Load a licensed corpus, tokenize/decode, document provenance and deterministic splits | Conceptual pages exist; no complete end-to-end corpus/tokenizer pipeline is established by this audit |
| G2 — Create training examples | Training examples | Build context windows, shifted targets, batches and masks; test alignment and leakage boundaries | Detailed conceptual explanation exists; production-ready data pipeline is not established |
| G3 — Represent tokens | Embedding space, positional encoding; tensors as needed | Use embedding lookup and positional information; inspect only the shapes required by the implementation | Conceptual pages exist; no complete GPT embedding stack is established |
| G4 — Implement attention | Q/K/V, scaled attention, causal masking | Implement and test causal self-attention; verify shape and no-future-information invariants | Conceptual pages exist; full tested attention module is not established |
| G5 — Assemble a GPT block/model | Transformer overview; tensor reference as needed | Compose attention, residual paths, normalization, MLP and output projection into a configured model | Overview exists; full GPT implementation is not established |
| G6 — Compute the objective | Logits, probabilities, likelihood, cross-entropy, loss | Align logits/targets, apply valid-position masking and reduction | A small NumPy loss/gradient reference and tests exist; this is not a GPT training implementation |
| G7 — Train and validate | Gradients, loss, experimental evaluation | Use autograd, optimizer updates, validation, checkpoints and reproducible configuration | No end-to-end GPT training run is established |
| G8 — Generate | Transformer, logits, probabilities | Implement autoregressive decoding, stopping and sampling with fixed trained parameters | Conceptual explanation is partial; complete generation implementation is not established |
| G9 — Evaluate | Experimental evaluation and relevant concept pages | Compare against baselines, analyze errors and state limits | Evaluation-method content exists; no complete evaluation of a locally trained GPT is established |

A milestone may use a short local explanation of a tensor operation, derivative, or probability calculation. That does **not** make a full mathematics course a prerequisite. The implementation should teach the smallest useful operation at the point of use, with a link to Deepen for readers who want the derivation.

## 4. Prerequisite policy: minimum viable knowledge, then optional depth

Use three explicit levels:

1. **Must know now:** a small fact or operation without which the next step cannot be performed or interpreted safely.
2. **Learn in context:** the local explanation supplied immediately before or during the relevant build step.
3. **Optional depth:** a derivation, generalization, proof, variant, or advanced treatment that is not required to complete the first small GPT.

Examples:

- Before using `nn.Embedding`, the learner needs to know that token IDs index a learned lookup table and what input/output shapes mean. They do not need a course in vector spaces.
- Before using attention, the learner needs to understand the roles of Q/K/V, softmax over the key positions, and the causal constraint. They do not need to derive every property of matrix multiplication.
- Before calling `loss.backward()`, the learner needs to understand that the loss is a scalar objective and gradients indicate local sensitivity. They do not need a full course in multivariable calculus.
- Before sampling, the learner needs to understand that logits define a categorical distribution and that decoding transforms or samples from it. They do not need general information theory.

Never label a concept as a mandatory prerequisite merely because it is mathematically related. State the specific operation or claim that requires it.

## 5. Editorial rules for page changes

- **Do not split by subject name alone.** “Attention” can have a conceptual lesson, a tested implementation checkpoint, and a mathematical deep dive because these answer different questions.
- **Do not duplicate canonical explanations.** Build pages link to Understand; Deepen links back to the applied concept; exercises link to both.
- **Do not hide essential mathematics.** A public LLM lesson must remain independently understandable without private repositories. Keep the definitions and derivations needed for its stated learning objective.
- **Do not front-load prerequisites.** Introduce tensor operations, probability and gradients when the learner encounters them.
- **Do not overstate implementation status.** A code snippet is illustrative unless it is part of the maintained package and covered by relevant tests. A test suite does not establish model quality.
- **Do not advertise absent practical content.** Build milestones must carry explicit status until code, tests and evidence exist.
- **Keep bilingual parity.** Every reader-facing route and major lesson must have equivalent FR/EN learning objectives, caveats, status and links.

## 6. Relationship to existing planning documents

- This file owns the **page-by-page editorial classification**.
- [Learning path](learning-path.md) owns the dependency-aware build sequence and evidence criteria.
- [Full curriculum plan](full-curriculum-plan.md) owns broad topic coverage against Raschka and complementary sources.
- [Reader experience and editorial method](reader-experience-and-editorial-method.md) owns page types, progressive disclosure and link behavior.
- [Editorial boundary audit](editorial-boundary-audit.md) owns the separate public-LLM-course versus general-mathematics-wiki boundary.
- [Page audit inventory](page-audit-inventory.md) records what has actually been reviewed and what remains to validate.

Do not create a new issue for every row. Route changes to existing owners: #130 (high-level architecture), #87 (curriculum relationships), #61 (page-level progressive disclosure), #78 (concept-to-code), #82 (current foundational content gate), and #108 (broad LLM panorama).
