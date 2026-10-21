# Repository roadmap

This roadmap prioritizes **validating and improving the knowledge already present**. Do not add implementations, modules, pages, or experiments merely to advance a roadmap. A topic is not complete because it is documented, because tests pass, or because an experiment runs: it requires accurate explanations, explicit assumptions and counterexamples, and demonstrated understanding recorded in the private `career-knowledge` inventory. Code is justified only when it resolves a specific conceptual gap and the prerequisite knowledge has been validated.

## Current state (reviewed 2026-10-20)

### Implemented in the repository
- A Quarto site in French and English, with a chapter on causal attention and notes on cosine similarity and the linearity hypothesis.
- A small NumPy cross-entropy implementation and analytical gradient, with unit tests including finite-difference comparison.
- CI checks for Ruff formatting/lint, mypy, pytest, and a separate Quarto render workflow.
- Written conventions for the learning path, experiment protocol, mathematical foundations, and reference provenance.

### Not yet demonstrated
- A complete tokenizer, Transformer block, or tiny GPT implementation in `src/llm_lab`.
- A training run with a saved configuration, validation curves, generated examples, and error analysis.
- End-to-end invariance tests for causal attention.
- Reproducible experiments behind the cosine-similarity and feature-linearity articles.
- Browser-based visual/accessibility review and automated link checking for the site.
- A committed `uv.lock` at the reviewed base snapshot; the current setup can resolve dependencies during CI, but it does not yet guarantee the same locked dependency graph across runs.
- An explicit repository licence. Do not infer permission to reuse the code or content.

## Prioritized plan

### P0 — Audit and validate existing knowledge (current priority)
**Goal:** improve the quality and teachability of existing material without increasing the repository's scope.

Tasks:
1. Review each existing explanation for factual accuracy, hidden assumptions, scope conditions, and claims stronger than the cited evidence supports.
2. Identify the most plausible misconception for each core concept and correct it in the existing explanation rather than adding a separate page.
3. Add or sharpen a counterexample only where it distinguishes two explanations that otherwise sound equally plausible.
4. Check whether French and English versions preserve the same qualifications and limits.
5. Use short, unfamiliar transfer questions to assess understanding; record mastery evidence privately in `career-knowledge`, not in the public portfolio.
6. Fix only defects found by this audit. Do not start new implementation work while relevant prerequisite knowledge remains unvalidated.

**Exit criteria**
- Important claims have a clear scope and support from relevant sources.
- Common misconceptions and at least one discriminating counterexample are addressed where useful.
- The learner can explain the concept, identify when it does not apply, and transfer it to a new case.
- `career-knowledge` records the evidence needed for mastery; a passing test or a polished page alone is insufficient.

### P1 — Keep the existing learning experience dependable
**Goal:** ensure the existing site and numerical exercise are correct, navigable, and easy to reproduce.

Tasks:
1. Render the full Quarto site and inspect both languages at desktop and mobile widths.
2. Check internal links, external source links, image loading, alternative text, headings, and rendered mathematics.
3. Fix notation inconsistencies in the mathematical foundations and attention self-checks.
4. Link the website, learning path, reference list, and this roadmap consistently.
5. Record reproducibility and accessibility defects found during review, but defer dependency-locking changes and new test helpers until the knowledge-validation gate is met.
6. Do not add a causal-mask helper or attention implementation as part of this priority; first validate the existing explanation of causality and its failure cases.

**Acceptance criteria**
- `quarto render site` succeeds from a clean checkout.
- `uv sync --locked --dev`, Ruff, mypy, and pytest pass.
- No known broken internal links; externally hosted images have a text alternative and source attribution.
- The site distinguishes existing implementations from planned work.

### Deferred — Mathematical and numerical foundations
**Goal:** build a small reference implementation with reliable numerical checks before model complexity grows.

Tasks:
1. Consolidate validation shared by loss and gradient functions without obscuring the mathematics.
2. Test invariance of cross-entropy to adding a constant to every logit in a row.
3. Test gradient row sums, expected shapes, finite outputs, and extreme but valid logits.
4. Add a small gradient-check utility or a clearly documented test helper.
5. Document dtype, reduction convention, numerical tolerances, and finite-difference limitations.

**Acceptance criteria**
- Known-value, edge-case, property, and gradient tests pass.
- Tests explain what each property establishes and what it does not.
- The implementation remains NumPy-only and CPU-friendly.

### Deferred — Causal attention implementation
**Goal:** turn the current explanatory chapter into an executable, tested component.

Tasks:
1. Add a NumPy reference for causal masking and scaled dot-product attention, keeping it deliberately small.
2. Specify tensor shapes and whether masks are boolean or additive.
3. Test shape errors, finite outputs, row normalization, and masked probability mass.
4. Test the defining causal invariant: changing a future token must not change earlier-position outputs.
5. Compare the reference against PyTorch scaled dot-product attention on matching inputs and tolerances.
6. Extend the chapter in French and English with links to the implementation and tests.

**Acceptance criteria**
- Tests demonstrate both local mask behavior and end-to-end causality.
- Reference-vs-framework differences are explained, not hidden behind loose tolerances.
- No performance claim is made without a benchmark.

### Deferred — Tokenization, data windows, and a tiny Transformer
**Goal:** build the smallest end-to-end autoregressive model whose data flow can be inspected.

Tasks:
1. Define a deterministic tokenizer/data interface and document any simplifications.
2. Create next-token windows with explicit input/target shifting and split-before-fitting rules.
3. Implement embeddings, positional information, attention, residual connections, normalization, and feed-forward layers in small modules.
4. Add shape, gradient, causal-leakage, and tiny-batch overfit tests.
5. Run a CPU-friendly training smoke test and save a configuration plus a small report.

**Acceptance criteria**
- Data windows and targets can be inspected by hand.
- No train/validation overlap is introduced by windowing.
- A tiny batch can be overfit as a pipeline check; this is not presented as evidence of language quality.
- A clean command reproduces the smoke test.

### Deferred — Controlled experiments on representation geometry
**Goal:** move the cosine and linearity notes from literature review to evidence-producing investigations.

**Experiment A — Embedding metrics**
- Choose a documented sentence-embedding model and a fixed dataset/split such as STS Benchmark.
- Compare cosine, dot product, and Euclidean distance under explicit normalization conditions.
- Report Spearman/Pearson correlation for similarity prediction and Recall@k/MRR/nDCG for retrieval where relevant.
- Measure vector norms, similarity distributions, anisotropy diagnostics, and neighbour hubness.
- Inspect false positives/negatives and repeat across at least one model or data slice.
- Do not conclude that one metric is universally best from one dataset.

**Experiment B — Geometry and linear probes**
- Use a synthetic dataset first: linearly separable data, XOR, and a periodic/circular feature.
- Compare linear and nonlinear probes under controlled sample size, regularization, and held-out compositions.
- If a pretrained language model is added, pin its revision and tokenizer, define the activation layer and feature label, and separate training, validation, and test examples.
- Include control tasks and intervention tests where feasible; probe accuracy alone is not evidence of causal use.
- Report uncertainty and failure cases, not only headline accuracy.

**Acceptance criteria**
- Each experiment has a fixed config/seed, data provenance, baseline, metrics, machine-readable output, and report.
- The report distinguishes observed results, interpretation, and hypotheses.
- Data/model download requirements and compute costs are explicit.

### P5 — Training, fine-tuning, and evaluation
**Goal:** add model training only after the foundational tests and data contracts are stable.

Order:
1. Tiny GPT pre-training with train/validation curves and generation examples.
2. Reference comparison against a trusted implementation with matching tokenizer, architecture, weights, and numerical conditions.
3. Small SFT run with held-out evaluation and example-level error analysis.
4. LoRA and quantization comparisons, keeping adapter rank, target modules, quantization, memory, latency, and quality distinct.
5. Preference optimization as a controlled experiment or simulation if realistic compute/data are unavailable.
6. Robustness evaluation: leakage, distribution shift, calibration where relevant, prompt sensitivity, contamination, and failure slices.

**Acceptance criteria**
- Every run records model/tokenizer revisions, data provenance, config, seed, device, package versions, runtime, peak memory where available, and evaluation protocol.
- Baselines and selection criteria are defined before inspecting final-test results.
- Quality/cost trade-offs and regressions are reported.

### P6 — Portfolio quality and maintenance
**Goal:** make the repository legible to a technical reviewer or hiring team.

Tasks:
1. Add a concise project status page and one-command quick-start for each completed experiment.
2. Add a CI link checker or equivalent internal-link validation, while treating external-site outages separately.
3. Perform an accessibility and mobile visual pass on the rendered site.
4. Choose and add an explicit licence only after deciding the intended reuse terms for code and content.
5. Publish reports with plots, exact commands, source links, and known limitations.
6. Keep the roadmap honest: mark items complete only after acceptance criteria are satisfied.

**Acceptance criteria**
- A reviewer can reproduce the core numerical tests and at least one experiment from a clean checkout.
- Every claimed feature is either implemented or labelled planned.
- The repository clearly states licence and external asset provenance.

## Suggested sequence at 10 hours per week

| Timebox | Focus | Deliverable |
| --- | --- | --- |
| Week 1 | P0 site and documentation QA | Clean render, checked navigation, notation fixes |
| Weeks 2–3 | P1 numerical foundations | Property tests and gradient diagnostics |
| Weeks 4–5 | P2 causal attention | Tested NumPy reference and framework comparison |
| Weeks 6–7 | P3 tokenization and tiny Transformer | Deterministic data path and CPU smoke test |
| Weeks 8–9 | P4 representation experiments | Reproducible metric and geometry reports |
| Weeks 10–11 | P5 choose one: pre-training or SFT/LoRA | One bounded, well-evaluated run |
| Week 12 | P6 portfolio review | Final report, limitations, reproducibility check |

This schedule is a prioritization aid, not a guarantee. If acceptance criteria fail, extend the module instead of advancing on calendar time.

## Definition of done for any new chapter

- [ ] A precise question and scope statement.
- [ ] Equations with defined symbols, dimensions, and assumptions.
- [ ] A small illustrative example or diagram with provenance.
- [ ] A primary paper or official technical source plus accessible explanation.
- [ ] Runnable code or a clear reason why the page is literature-only.
- [ ] Tests or a reproducible protocol linked from the page.
- [ ] Counterexamples, limitations, and common misinterpretations.
- [ ] French and English versions reviewed for equivalent meaning.
- [ ] Internal links and rendered mathematics checked.
