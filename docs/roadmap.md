# Repository roadmap

This roadmap prioritizes **validating and improving the knowledge already present**. Do not add implementations, modules, pages, or experiments merely to advance a roadmap. A topic is not complete because it is documented, because tests pass, or because an experiment runs: it requires accurate explanations, explicit assumptions and counterexamples, and demonstrated understanding recorded in the private `career-knowledge` inventory. Code is justified only when it resolves a specific conceptual gap and the prerequisite knowledge has been validated.

## Current state (reviewed 2026-10-28)

The learning budget is capped at **five focused hours per week, with no session longer than 60 minutes**. Calendar estimates below are sequencing aids, not deadlines; a module remains open until its evidence criteria are met. Do not compensate for missed sessions by extending another day.

### Implemented in the repository
- A Quarto site in French and English, with canonical pages for mathematical foundations, entropy/cross-entropy, attention, cosine similarity, embedding-space geometry, positional encoding/RoPE, and the embedding-linearity hypothesis.
- A bilingual glossary and a sourced, selective history of the Transformer architecture.
- Control questions in the core probability/loss/gradient pages with answers hidden behind native disclosure controls.
- A small NumPy cross-entropy implementation and analytical gradient, with unit tests including finite-difference comparison.
- CI checks for Ruff formatting/lint, mypy, pytest, and a separate Quarto render workflow; the rendered-site workflow also checks local HTML links and fragment identifiers.
- Written conventions for the learning path, experiment protocol, mathematical foundations, and reference provenance.

### Not yet demonstrated
- A complete tokenizer, Transformer block, or tiny GPT implementation in `src/llm_lab`.
- A training run with a saved configuration, validation curves, generated examples, and error analysis.
- End-to-end invariance tests for causal attention.
- Reproducible experiments behind the cosine-similarity and feature-linearity articles.
- Browser-based visual/accessibility review and external-reference availability/relevance checks. Local rendered-site file and fragment links are now checked in CI.
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

#### Latest focused audit — core probability and loss chain (2026-10-27)

A textual, bilingual review of `site/fr/entropy.qmd`, `site/en/entropy.qmd`, `site/fr/cross-entropy.qmd`, and `site/en/cross-entropy.qmd` has been completed against the current public files. This is not a browser-render, external-link, or mastery review.

- **Entropy:** the two language versions preserve the same core claims: finite-vocabulary bound in nats, the \(0\log 0=0\) convention, a checkable numerical example, predictive entropy versus observed-token surprisal, sequence NLL, temperature, and limits concerning truth/calibration and tokenizer-dependent comparisons.
- **Cross-entropy:** the two versions preserve the one-hot token objective, normalized soft-target formulation, KL identity and direction, zero-support caveat, target/logit alignment, masking and reduction semantics, perplexity convention, and the one-hot logit-gradient derivation.
- **Logits/probabilities:** a duplicated set of self-check questions in the English logits page was removed on this branch; no mathematical correction was identified in those page pairs.
- **Likelihood/loss:** the likelihood pages remain aligned. The loss pages had duplicated English self-checks, a missing tensor-navigation link, and an ambiguous perplexity/log-base caveat. The branch consolidates the self-check, restores the link, defines the loss notation, and states the natural-log and base-2 perplexity formulas explicitly.
- **Gradients:** the English page also duplicated its self-check. The branch consolidates it; the textual review found no justified change to the chain-rule or finite-difference equations.
- **Corrections so far are editorial/mathematical clarification, not mastery evidence.** In particular, the KL derivation remains because the page uses it to explain soft targets and the relationship between cross-entropy and KL; this is not a claim that the entire treatment has passed independent scientific review.
- **Still open:** actual browser review of MathJax and responsive layout; external-reference availability/relevance; private knowledge-transfer questions and evidence. Do not mark these concepts acquired from this audit alone.

**Next step:** the English embedding-space and positional-encoding/RoPE lessons are included in Quarto's render list and English sidebar; the main-branch Quarto render and local-link checks passed after the recent navigation corrections. This closes the build-level check for those pages, not their browser-rendered visual review or semantic equivalence. The local rendered-site link checker is part of CI, and a focused spot-check of the core entropy/loss references is recorded in the ledger. The bilingual cosine-similarity pages both describe the hubness illustration and preserve its synthetic-data limitation. The public cross-entropy pages distinguish the row-wise NumPy reference from token-level shifting/masking, and the English Transformer overview and homepage have had their identified navigation gaps corrected. Remaining work: inspect the published pages in a browser at desktop and mobile widths; verify external references for availability, relevance, and accurate attribution; continue the semantic FR/EN audit; then collect private transfer-question evidence. Do not mark content mastery or overall page quality complete until those checks have evidence.

### P1 — Keep the existing learning experience dependable
**Goal:** ensure the existing site and numerical exercise are correct, navigable, and easy to reproduce.

Tasks:
1. Render the full Quarto site and inspect both languages at desktop and mobile widths.
2. Rely on the rendered-site CI checker for local file/fragment links; manually inspect external references, image loading, alternative text, headings, and rendered mathematics.
3. Fix notation inconsistencies in the mathematical foundations and attention self-checks.
4. Link the website, learning path, reference list, and this roadmap consistently.
5. Record reproducibility and accessibility defects found during review, but defer dependency-locking changes and new test helpers until the knowledge-validation gate is met.
6. Do not add a causal-mask helper or attention implementation as part of this priority; first validate the existing explanation of causality and its failure cases.

**Acceptance criteria**
- `quarto render site` succeeds from a clean checkout.
- `uv sync --locked --dev`, Ruff, mypy, and pytest pass.
- The rendered-site local-link check passes with no known broken local file or fragment links; externally hosted images have a text alternative and source attribution.
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
2. **Implemented:** CI checks local file and fragment links in rendered HTML. Continue reviewing external-reference availability/relevance separately; external URLs are intentionally excluded from this deterministic check.
3. Perform an accessibility and mobile visual pass on the rendered site.
4. Choose and add an explicit licence only after deciding the intended reuse terms for code and content.
5. Publish reports with plots, exact commands, source links, and known limitations.
6. Keep the roadmap honest: mark items complete only after acceptance criteria are satisfied.

**Acceptance criteria**
- A reviewer can reproduce the core numerical tests and at least one experiment from a clean checkout.
- Every claimed feature is either implemented or labelled planned.
- The repository clearly states licence and external asset provenance.

## Suggested sequence at five hours per week

Use five sessions of at most 60 minutes. A missed session is skipped or rescheduled into another available day; never exceed the daily cap. Keep the audit/retrieval loop active throughout rather than treating it as a one-time first week.

| Approximate timebox | Focus | Deliverable |
| --- | --- | --- |
| Weeks 1–2 | P0 audit existing explanations and bilingual parity | Corrections to existing pages only, source/caveat review, unfamiliar transfer questions |
| Weeks 3–4 | P1 numerical foundations, only where the audit exposes a real gap | Reviewed derivation or property-test plan; implementation only after the prerequisite knowledge gate |
| Weeks 5–6 | Causal attention concepts and invariance reasoning | Written causal-invariance argument and counterexample; no implementation unless mastery evidence warrants it |
| Weeks 7–8 | Representation geometry: critically audit existing cosine/linearity claims | Source-backed claim review and explicit limitations; no experiment until its question and protocol are justified |
| Weeks 9–10 | Select one bounded experiment or one existing-page gap | One protocol with baseline, metrics, split policy, uncertainty and stop criteria |
| Weeks 11–12 | Reproducibility, report, transfer test and public-site review | Reviewed evidence report, limitations, links and accessibility/render check |

At five hours per week, the plan intentionally narrows throughput rather than weakening quality gates. Tokenizer, Transformer, pretraining, SFT/LoRA, preference optimization, and advanced architecture work remain deferred until the relevant concepts and the chosen project justify them. If acceptance criteria fail, extend the module instead of advancing on calendar time.

## Content architecture and definition of done

Use the same hierarchy as the site grows:

- **Home page:** orientation, learning path, current status, and how to navigate; do not repeat chapter content.
- **Synthesis page:** explain how multiple concepts interact and link to their canonical concept pages. Keep only the equations needed to understand the relationship.
- **Concept page:** one canonical explanation of one concept. Other pages should link to it instead of copying its full definition.
- **Code and evidence:** link to the existing implementation, tests, and experiment/report where they exist. If none exists, say so explicitly and link to the planned acceptance criteria. Never imply that illustrative pseudocode is production code or that planned work already exists.

Every new or substantially revised concept page should meet these criteria:

- [ ] State the question, scope, prerequisites, and an intuitive explanation before formal notation.
- [ ] Explain the concept's provenance: original paper or technical source, historical context where known, and distinguish it from later variants.
- [ ] Explain what problem it solves and why it is useful; state assumptions and trade-offs.
- [ ] Define symbols, tensor dimensions, conventions, and equations precisely.
- [ ] Give a small worked example or diagram with clear provenance.
- [ ] Explain misconceptions and at least one discriminating counterexample where it improves understanding.
- [ ] Link to related concepts and other disciplines when the connection is substantive; explain the mapping and its limits instead of adding a bare link. For example, an entropy connection should distinguish Shannon information entropy, statistical mechanics, and informal uses of the word.
- [ ] Link to code, tests, and experiments when present, or explicitly state that they do not yet exist.
- [ ] Include a primary paper or official technical source plus an accessible explanation where useful.
- [ ] Keep French and English versions equivalent in claims, caveats, notation, and references.
- [ ] Check internal links, rendered equations, mobile readability, and source attribution.
- [ ] Use Quarto-supported inline math (`$...$`) and display math (`$$...$$`) delimiters consistently; check that display delimiters are paired and inspect the rendered output in both languages.

Passing a render or test establishes only the property that was checked. It does not by itself establish conceptual mastery, general model quality, or an empirical claim.


### Focused audit — causal-mask API semantics (2026-10-28)

A source-level review of the English and French causal-masking pages found that both correctly described the additive causal mask and stated that no reusable attention implementation or end-to-end invariance test exists. One practical caveat was missing: boolean-mask polarity is not uniform across attention APIs. The official PyTorch `scaled_dot_product_attention` API treats `True` as allowed, while `MultiheadAttention.attn_mask` treats `True` as masked out. The proposed correction adds matching warnings and links to both official references. This does not establish end-to-end causality or replace rendered/browser review; Quarto and local-link CI must pass.


### Focused bilingual audit — cosine-similarity navigation (2026-10-28)

The source comparison found one small parity gap: the French cosine-similarity lesson linked to the embedding-space concept from its takeaway, while the English lesson did not. The English link has been added. This is a targeted navigation fix, not completion of the full semantic bilingual audit; rendered-site, external-reference, and responsive visual checks remain open.
