# Knowledge-preservation ledger — LLM Lab math-page slice

**Status:** first-pass preservation inventory with a focused textual audit of the entropy and cross-entropy page pairs recorded below; not a full browser, external-link, or scientific sign-off.  
**Public branch under review:** `docs/llm-application-math-refactor` (PR #17).  
**Comparison baseline:** `main` as inspected on 2026-10-27.  
**Rule:** no item is considered “moved” merely because a similarly named Wiki page exists. The public page must still teach every prerequisite needed for its LLM-specific objective.

This ledger records section-level dispositions for the first four concepts. PR #17 has been integrated, but that does not certify every claim as scientifically reviewed. If a claim or useful teaching element is found missing, restore it to LLM Lab or explicitly decide—on pedagogical grounds—that it is not needed by the public book.

## Decision vocabulary

- **KEEP PUBLIC:** required for the standalone LLM Lab reader.
- **KEEP BOTH:** the general concept belongs in the Wiki, while its LLM-specific explanation is also needed in the public book.
- **WIKI DEEPER TREATMENT; PUBLIC APPLICATION RETAINED:** broad cross-domain treatment can live in the Wiki only after its scientific review, but the public page keeps the definitions/assumptions needed for the LLM lesson.
- **VERIFY:** inspect the exact equations, prose, citations, local links, or rendered result before marking complete.
- **NOT A DELETION AUTHORISATION:** an inventory finding does not by itself approve removing content.

## 1. Entropy — `site/fr/entropy.qmd`, `site/en/entropy.qmd`

### Baseline content inventoried

The original French and English pages include:
1. surprisal of an event, Shannon entropy of a discrete variable, and the (0\log 0=0) convention;
2. zero entropy, uniform distributions, the finite-alphabet upper bound, units (bits/nats), and a worked distribution example;
3. joint entropy, conditional entropy, chain rule, and mutual information, including the non-causality caveat;
4. connection between entropy and lossless/prefix coding;
5. relation and distinctions between Shannon and statistical-physics entropy;
6. differential entropy for continuous variables, including its possible negativity and scale dependence;
7. misconceptions about “disorder”, truth, intrinsic text complexity, thermodynamic equivalence, and differential entropy;
8. links to probabilities, likelihood, cross-entropy, and the mathematical chain;
9. Shannon, Cover–Thomas, Jaynes, and two 3Blue1Brown references.

### Proposed public disposition

| Baseline item | Disposition | Reason / verification |
|---|---|---|
| Event surprisal and discrete Shannon entropy | **KEEP BOTH** | Needed to derive and interpret next-token entropy; retain notation, log-base/unit convention, and the distinction between distribution entropy and observed-token surprisal locally. |
| (0\log 0=0), entropy zero, uniform case and maximum bound | **KEEP PUBLIC selectively** | These are useful sanity checks for a categorical vocabulary distribution. Verify that the new page retains enough boundary-case intuition; not every general theorem needs a full proof. |
| Joint/conditional entropy, chain rule, mutual information | **WIKI DEEPER TREATMENT; VERIFY public need** | General information-theory material belongs in the Wiki. Retain locally any conditional-distribution explanation needed to understand autoregressive next-token predictions. The public page must not rely on the Wiki for this. |
| Lossless/prefix coding interpretation | **WIKI DEEPER TREATMENT; public optional** | Useful general context but not required for the core LLM entropy application. Do not imply that this content was moved until the Wiki page and source coverage are checked. |
| Shannon vs statistical-physics entropy | **WIKI DEEPER TREATMENT** | Cross-domain comparison is outside the narrow LLM application path. Keep any short warning needed to prevent a misconception; the full comparison need not be taught here. |
| Differential entropy and continuous variables | **WIKI DEEPER TREATMENT** | The next-token output is categorical over a finite vocabulary. The continuous-variable caveat is not a prerequisite for this page, but the general knowledge and its caveats must not be lost from the overall knowledge system. |
| Misconceptions: entropy is truth, text complexity, disorder, or always positive | **KEEP BOTH selectively** | Preserve the LLM-relevant warnings: entropy does not establish truth, quality, calibration, or intrinsic text complexity. Domain-specific misconceptions can remain in the Wiki. |
| LLM-specific interpretation of next-token entropy, temperature, and model comparison | **KEEP PUBLIC** | This is the purpose of the public chapter. Explicitly distinguish predictive entropy, target-token surprisal/NLL, and corpus-level perplexity. |
| References | **KEEP PUBLIC** | Retain accessible sources that support the claims made in the public page. The Shannon and Cover–Thomas references remain; Jaynes can be Wiki-only if no statistical-physics claim remains public. |
| Navigation links and self-checks | **KEEP PUBLIC** | Update to current page names; ensure links work in both languages. |

**Follow-up changes on this branch:** added a numerical comparison — ‎(0.5, 0.5) versus (0.9, 0.1)‎ — and self-check questions to both language versions. The new page retains the key interpretation limits, temperature, and links to adjacent concepts. The broad information-theory sections are present in Wiki concept `CONCEPT-020`, which remains draft and is not a public dependency. Final rendered-page review is still required.

## 2. Cross-entropy and KL — `site/fr/cross-entropy.qmd`, `site/en/cross-entropy.qmd`

### Baseline content inventoried

The original pages include:
1. (H(q,p)=-\sum_i q_i\log p_i), normalization assumptions and log units;
2. one-hot target special case;
3. derivation of the softmax-cross-entropy derivative with respect to logits;
4. identity (D_{KL}(q\Vert p)=H(q,p)-H(q)), and the direction/asymmetry of KL;
5. coding interpretation and infinite cost if (q_i>0) while (p_i=0);
6. distinctions between cross-entropy, entropy, and KL;
7. one-hot and general soft target distributions;
8. perplexity relation, numerical example, misconceptions, self-checks;
9. Shannon, Cover–Thomas, 3Blue1Brown, and PyTorch CrossEntropyLoss references.

### Proposed public disposition

| Baseline item | Disposition | Reason / verification |
|---|---|---|
| Definition, normalization, logarithm base and units | **KEEP PUBLIC** | The token objective must be derivable locally; do not make a Wiki link the definition. |
| One-hot target and (-\log p_y) | **KEEP PUBLIC** | Essential for autoregressive next-token training. |
| Softmax-cross-entropy logit gradient | **KEEP PUBLIC** | Required bridge from token loss to backpropagation; state the assumptions (one-hot, unweighted, one position). |
| Cross-entropy/KL identity and KL direction | **KEEP BOTH / VERIFY** | Soft targets and distillation require this distinction. Check that the public page states the identity, conditions and direction correctly, rather than merely linking to a Wiki explanation. |
| Coding interpretation and infinite cost for unsupported targets | **WIKI DEEPER TREATMENT; public caveat retained if relevant** | General coding explanation can be deeper in the Wiki. The public page should retain the practical warning that assigning zero probability to a possible target gives infinite ideal NLL, or explain the relevant numerical analogue. |
| One-hot and soft targets | **KEEP PUBLIC** | Relevant to ordinary training, label smoothing and distillation. Clarify when formulas differ. |
| Causal target shift, padding/ignored positions, masks and reduction | **KEEP PUBLIC** | These are LLM implementation semantics and must remain explicit. |
| Perplexity and comparison conventions | **KEEP PUBLIC** | Define ΠPL from mean per-token NLL with natural logarithms and state tokenizer/mask/counting constraints. |
| Numerical example, misconceptions and exercises | **KEEP PUBLIC** | Keep a small independently checkable example and self-checks for the intended learner. |
| References | **KEEP PUBLIC** | PyTorch documentation supports API behaviour; public mathematical references support the definitions. |

**Follow-up changes on this branch:** the English and French pages now explicitly state normalized-distribution and log-base assumptions, zero-mass and zero-support conventions, and the distinction between target-position and input-position indexing. The algebraic derivation of the KL identity is restored locally, with the target entropy defined in the page; a concrete KL direction/support counterexample is included. The one-hot logit-gradient derivation and the direction of the resulting gradient-descent update are also explicit. The LLM-specific objective, target alignment, masking, reduction, perplexity, examples and practical misconceptions remain public. The rendered page and final line-by-line baseline comparison still require review.

## 3. Probabilities and softmax — `site/fr/probabilites.qmd`, `site/en/probabilities.qmd`

### Baseline content inventoried

The original bilingual pages include:
1. softmax definition and normalization over the vocabulary;
2. an explicit two-outcome numerical example;
3. temperature transformation and its effect on distribution concentration and ranking;
4. autoregressive conditional factorization;
5. distinction between normalization, calibration and factual truth;
6. local argmax vs sequence-level quality/search/sampling;
7. self-check questions and links to entropy, likelihood and cross-entropy.

### Proposed public disposition

| Baseline item | Disposition | Reason / verification |
|---|---|---|
| Softmax formula, vocabulary support, normalization | **KEEP PUBLIC** | Foundational to every downstream chapter. Explain the logit vector and vocabulary dimension locally. |
| Numerical example | **KEEP PUBLIC** | Useful hand-check of the formula; verify that the new example is correct and simple enough to reproduce. |
| Temperature and ordering/concentration | **KEEP PUBLIC** | LLM decoding application; distinguish the mathematical transformation from empirically measured calibration. |
| Autoregressive factorization | **KEEP PUBLIC** | Core language-model concept and dependency for likelihood/perplexity. |
| Normalization vs calibration vs truth | **KEEP PUBLIC** | Central misconception prevention; preserve all three as distinct concepts. |
| Local argmax vs sequence-level generation | **KEEP PUBLIC** | Keep the limitation if the new page discusses decoding strategies; verify that no stronger claim is introduced. |
| Self-checks and local navigation | **KEEP PUBLIC** | Preserve learning support and update links. |
| Public references | **KEEP PUBLIC** | New PyTorch references are appropriate for implementation details; the mathematical statement must remain understandable without them. |

**Follow-up changes on this branch:** the old two-logit example, conditional sequence factorization, temperature transformation, calibration caveat, normalization-versus-truth distinction, self-check answers, references, and exercise-space navigation are retained or strengthened. The calibration statement now explicitly calls for relevant held-out data; temperature is described as changing the decoding distribution, not model parameters. The old simplex terminology is not required for the application lesson; the page explicitly defines normalization and probability output locally.

## 4. Tensors and shapes — `site/fr/tensors.qmd`, `site/en/tensors.qmd`

### Baseline content inventoried

The original French page includes:
1. the three-axis (B\times T\times D) activation diagram and accessible alt text;
2. scalar/vector/matrix/rank-3 array examples and shapes;
3. distinction between a framework “tensor” and the stricter mathematical/physical tensor concept;
4. projection (XW) with shape reasoning;
5. variation in attention-axis conventions;
6. indexing, permutation, broadcasting, reshape, and masking pitfalls;
7. a worked example and misconceptions (tensor need not be a cube; same shape need not mean same semantics; compatible shapes do not prove correctness);
8. navigation to Q/K/V, attention, embeddings and the mathematical chain;
9. video, PyTorch, and Raschka references.

The baseline had no `site/en/tensors.qmd` counterpart. The proposed branch adds one and a translated figure.

### Proposed public disposition

| Baseline item / addition | Disposition | Reason / verification |
|---|---|---|
| (B\times T\times D) diagram and alt text | **KEEP PUBLIC** | Essential visual for the book; inspect both language variants and rendering. |
| Scalar/vector/matrix/rank-3 terminology and shape examples | **KEEP PUBLIC selectively** | Retain enough shape vocabulary for readers to follow the Transformer pages. The distinction between array rank and matrix rank should remain explicit where the term “rank” is used. |
| Framework-array vs mathematical-tensor distinction | **KEEP BOTH briefly** | Important caveat when using the word “tensor”; the general formal treatment may be in the Wiki, but a concise local warning avoids ambiguity. |
| (XW) projection and output-shape reasoning | **KEEP PUBLIC** | Directly prepares the reader for embeddings, attention and vocabulary logits. |
| (B,T,D,V,H,d_h) and attention shapes/axis conventions | **KEEP PUBLIC** | LLM-specific content; explicitly note conventions can differ by API. |
| Axis permutation, broadcasting, reshape, masks, dtype, gradient connectivity | **KEEP PUBLIC** | Practical failure modes that cannot be delegated to a private Wiki. |
| Worked example, misconceptions and navigation | **KEEP PUBLIC** | Keep a small shape trace and links to public LLM Lab pages. |
| New English page and translated SVG | **KEEP PUBLIC** | Fixes a pre-existing bilingual gap; verify equivalent technical coverage, links and alt text. |
| Video and Raschka reference | **KEEP PUBLIC** | Both references are retained in the French and English tensor lessons; PyTorch and NumPy docs support API-specific statements. External URL availability still needs a separate check. |

**Follow-up changes:** the new English page and translated SVG provide language parity; both pages retain scalar/vector/matrix examples, array-rank versus matrix-rank terminology, the mathematical-tensor caveat, shape semantics, axis permutation, indexing, broadcasting, reshape, masks, dtype, gradients, and misconceptions. Projection notation uses \(D'\) to avoid overloading \(H\), the number of attention heads. PyTorch, NumPy, Raschka, and the tensor-visualization reference are present in both language versions. The deployed tensor diagrams have now been visually inspected and are legible; their non-empty alt text and local asset paths were verified. External-reference availability remains open.

## 5. Contributor-guidance audit

- `llm-lab/CONTRIBUTING.md` previously said to include “only the concise general definition” and “do not duplicate a full Wiki chapter”. This wording could incorrectly encourage removal of teaching material needed by the public book. The PR branch now clarifies that LLM Lab is a self-contained book, that intentional overlap is allowed, and that no page may depend on private Wiki content. It now also explicitly keeps private Wiki URLs/IDs out of public lesson content and directs maintainer traceability to the private `career-knowledge` repository.
- `wiki-knowledge/CONTRIBUTING.md` previously said to link to one canonical page “instead of copying its definition into another page” without delimiting that rule to the Wiki. The merged Wiki contributor guidance in PR #24 clarifies that canonical uniqueness applies within the Wiki, not across independent books or applications.
- The Wiki concept pages added under `CONCEPT-020`–`CONCEPT-023` remain marked draft. Their existence is not evidence that their claims are scientifically reviewed, and they do not justify a public content deletion.
- The Wiki contributor-boundary change was merged via [wiki-knowledge PR #24](https://github.com/JM-Brun/wiki-knowledge/pull/24), and the corresponding public-book clarification was merged via [llm-lab PR #17](https://github.com/JM-Brun/llm-lab/pull/17), both on 2026-10-27.

## 6. Link-audit evidence

At commit `e3d80d65569afbc0e2c85b4e8fcb020ecb070497`, a path-existence check covered 50 local Markdown/image references across the eight affected French/English concept pages (entropy, cross-entropy, probabilities, tensors): all 25 unique targets existed in the branch tree. The four explicit fragment links to the planned exercise collections (`#foundations` and `#fondations`) were also checked against their target pages. The check exposed one invalid English tensor-page link to a not-yet-translated embedding-space page; it was changed to an explicit link to the existing French page with the translation gap labelled. These checks verify target paths/fragments only, not rendered appearance, accessibility, or external URL availability.

## 7. Post-merge validation and remaining checks

- [x] Complete a passage-level disposition review of all four affected concepts. The public pages retain the definitions, assumptions, derivations, numerical examples, interpretation limits, navigation, and references needed for the LLM application. Broad general entropy/coding/physics material is retained in Wiki concepts `CONCEPT-020`/`CONCEPT-021` (still draft); this is a content disposition, not scientific approval of the Wiki drafts.
- [x] Textual review: the entropy pages distinguish predictive entropy from observed-token surprisal and sequence NLL, state the finite-vocabulary bound in nats, include a numerical example/self-check, and state the convention 0 log 0 = 0. The deployed artifact contains the expected HTML and MathJax source; actual equation typesetting still needs a browser-level visual check.
- [x] Textual review: cross-entropy pages state and derive the KL identity, state its direction, cover one-hot/soft-target cases, zero-mass terms and zero-support caveat, distinguish target-position from input-position indexing, and derive the one-hot logit gradient. Rendered HTML contains the expected MathJax source and no missing local links; actual equation typesetting still needs a browser-level visual check.
- [x] Verify the probabilities/softmax old/new diff: numerical example, conditional factorization, temperature, calibration/truth distinctions, self-check answers, references, and exercise-space navigation are present. The general simplex term was replaced by a direct explanation of normalization.
- [x] Textual review: tensor pages distinguish output feature dimension (D') from attention-head count (H), explain array rank versus matrix rank, and preserve key misconceptions in both languages. Both deployed diagrams were visually inspected; alt text, local asset paths, FR/EN page structure, and local links/fragments were checked.
- [ ] Check the Wiki concept registry/generator synchronization, sources metadata, and draft lifecycle. The four pages exist in `main`, but all remain `status: draft`, with empty `sources` metadata; they are supplementary only and are not treated as scientifically approved destinations.
- [x] Path-existence audit for 50 local Markdown/image references and four explicit local fragments across the eight affected pages; all targets/fragments resolve at the recorded commit.
- [x] Inspect the deployed HTML artifact for the four affected cross-entropy/tensor pages: each has exactly one main H1, no duplicate HTML IDs, and no broken local file or fragment links. Both tensor diagrams were visually inspected and have meaningful non-empty alt text.
- [ ] Full-page browser review of the four pages and actual MathJax typesetting remains open: the available browser runtime blocked local HTTP/file navigation and could not load the external MathJax CDN. This limitation is not a Quarto build failure.
- [x] CI and Quarto site render passed on earlier reviewed heads after mathematical corrections. [CI](https://github.com/JM-Brun/llm-lab/actions/runs/40538171509) · [Quarto](https://github.com/JM-Brun/llm-lab/actions/runs/40538171519).
- [x] CI passes on reviewed head `b97475304533c76712dff180c68693d0482cb401`: [CI run](https://github.com/JM-Brun/llm-lab/actions/runs/40540506554).
- [x] Quarto bilingual site render passes on the same head: [site workflow](https://github.com/JM-Brun/llm-lab/actions/runs/40540504668). The render succeeded after the latest content, reference, navigation, and contributor-guidance changes.
- [x] Visually inspect both tensor SVG diagrams from the deployed artifact; they are legible, correctly labelled, and equivalent across languages. Check alt text and local links.
- [ ] Verify actual browser typesetting of the MathJax equations and full-page responsive layout in a normal browser.
- [x] PR #17 was merged on 2026-10-27; merge commit: `f215226bf995ab32d41fddf6a20e50979049cb96`. The merge records integration, not scientific approval of every claim.
- [x] CI, Quarto build, and GitHub Pages deployment succeeded on the merge commit: [CI](https://github.com/JM-Brun/llm-lab/actions/runs/40541155717) · [Quarto](https://github.com/JM-Brun/llm-lab/actions/runs/40541156190) · [Publish](https://github.com/JM-Brun/llm-lab/actions/runs/40541156248).
- [ ] Check external references for availability and relevance; no live external-URL validation was performed in this artifact audit.
- [ ] Review and merge this post-merge audit update separately.

## 8. Focused bilingual textual audit — 2026-10-27

**Scope:** current `main` versions of the four page files listed in sections 1–2. Compared French and English wording, formulas, assumptions, examples, limitations, and navigation. This pass did not execute Quarto, inspect a browser-rendered page, validate external URLs live, or assess the learner's mastery.

### Entropy

- **Parity:** the French and English pages cover the same core concepts and carry matching caveats.
- **Mathematical checks:** \(H(p)=-\sum_i p_i\log p_i\) is bounded by \(0\le H(p)\le\log V\) for a normalized categorical distribution on a finite vocabulary; the two-token examples are consistent in bits and nats; the sequence factorization and negative log-likelihood relation are aligned.
- **Interpretation checks:** predictive entropy is distinguished from observed-token surprisal; temperature is a transformation of logits for decoding, not a parameter update; low entropy is not evidence of truth or calibration.
- **Disposition:** no textual correction identified in this pass. Keep the chapter focused on the LLM application rather than restoring the broad general-information-theory sections.
- **Remaining verification:** browser-level equation/layout review and live external-reference check.

### Cross-entropy

- **Parity:** the French and English pages preserve the same equations, assumptions, practical cautions, and learning checks.
- **Mathematical checks:** the one-hot loss, soft-target cross-entropy, \(H(q,p)=H(q)+D_{\mathrm{KL}}(q\Vert p)\), directionality/support example, and one-hot logit gradient are internally consistent under the stated normalized-distribution and finite-value assumptions.
- **Implementation semantics:** both pages distinguish target-position and input-position indexing, and explicitly cover causal shifting, ignored/padding positions, reduction conventions, and perplexity from mean token NLL.
- **Disposition:** retain the local KL derivation for now: it directly explains the soft-target case and avoids making the public lesson depend on a private general-mathematics source. Do not remove it merely to reduce overlap. No textual correction identified in this pass.
- **Remaining verification:** browser-level equation/layout review, live external-reference check, and a follow-up check that the implementation page and tests support any code-specific wording.

### What this audit does not establish

This review does not mark either concept as mastered, prove every cited source supports every claim, or replace a full-site Quarto render and visual inspection. Update status only when those separate checks have evidence.

## 9. Focused bilingual textual audit — logits and probabilities (2026-10-27)

**Scope:** current French/English source pairs `site/fr/logits.qmd`, `site/en/logits.qmd`, `site/fr/probabilites.qmd`, and `site/en/probabilities.qmd`. Compared definitions, formulas, examples, caveats, self-checks, and local navigation. This was a source-text review, not a rendered-browser or external-link check.

### Logits

- **Mathematical checks:** the softmax definition, probability-ratio identity, translation invariance, two-class example, and max-subtraction stability explanation are consistent.
- **Defect found:** the English page repeated the same three self-check questions twice. The first copy had no answers and interrupted the exercise/tensor links; the second copy repeated the questions with answers.
- **Correction made on this branch:** consolidated the English page to one answered self-check, restored the exercise and tensor links before it, and kept the next-page links after it. This brings its structure closer to the French page without adding content.
- **Remaining verification:** render and inspect the page; confirm the local links and displayed equations in the deployed HTML.

### Probabilities

- **Parity:** French and English versions align on softmax normalization, the two-logit example, autoregressive factorization, tokenization caveat, temperature, decoding versus training, and the distinction between normalization, calibration, and factual truth.
- **Mathematical checks:** the example \(z=(0,\log 3)\) gives \(p=(0.25,0.75)\); for positive temperature, dividing logits by temperature preserves their order while changing their distribution.
- **Disposition:** no further source-text correction identified in this pass.
- **Remaining verification:** rendered-page review and live external-reference check.

### What this audit does not establish

The fix is not yet merged and this connector workflow did not run Quarto or CI. The review does not certify every source claim, live link availability, or learner mastery.

## 10. Focused bilingual textual audit — likelihood and loss (2026-10-27)

**Scope:** current French/English source pairs `site/fr/vraisemblance.qmd`, `site/en/likelihood.qmd`, `site/fr/loss.qmd`, and `site/en/loss.qmd`. Compared sequence factorization, examples, loss definitions, target alignment, masks/reduction, perplexity conventions, self-checks, and navigation.

### Likelihood

- **Parity:** both pages state the autoregressive chain-rule factorization, log-likelihood sum, NLL relationship, same-positions qualification, a numerical example, and tokenizer/model-fit caveats.
- **Mathematical check:** `0.5 × 0.25 × 0.8 = 0.1`, so the sequence NLL is `-ln(0.1) ≈ 2.303` nats when natural logarithms are used.
- **Disposition:** no source-text correction identified in this pass. The assumption of independent dataset sequences is stated for the product of sequence likelihoods; keep that qualification.

### Loss

- **Parity defect found:** the English page repeated its three self-check questions in a second section. It also lacked the explicit tensor-shape navigation present in French.
- **Correction made on this branch:** consolidated the English page to one answered self-check, restored a link to the tensor lesson, and kept the next-page navigation after the answers.
- **Notation clarification:** both language versions now define the predicted distribution `p[b,t,:]` and target-token ID `y[b,t]` before using them in the per-position loss.
- **Perplexity correction:** both pages now state explicitly that `PPL = exp(NLL_mean)` assumes natural-log NLL (nats), and give the base-2 equivalent `PPL = 2^NLL_mean` when NLL is measured in bits. The previous wording could be read as though the exponential formula applied regardless of log base.
- **Remaining verification:** render the modified equations, inspect the full bilingual pages, and run CI/Quarto. The edits are not yet merged.

### What this audit does not establish

This source-text audit does not replace a rendered-site review, test the implementation against the documented loss convention, or establish learner mastery.

## 11. Focused bilingual textual audit — gradients (2026-10-27)

**Scope:** current French/English pages `site/fr/gradients.qmd` and `site/en/gradients.qmd`. Compared equations, assumptions, numerical-check guidance, self-checks, and navigation.

- **Mathematical review:** the one-hot softmax-cross-entropy logit derivative, chain-rule relationship between logit and parameter gradients, SGD update, and central finite-difference expression are consistent under the stated conventions. The text appropriately limits what one finite-difference check establishes and notes the trade-off in choosing epsilon.
- **Defect found:** the English page presented the same three self-check questions twice, first without answers and then with answers.
- **Correction made on this branch:** consolidated the English page to one answered self-check, preserving the exercise link and return navigation.
- **Remaining verification:** compare the documented derivative and finite-difference convention with the implementation/tests, render the corrected equations, and run CI/Quarto. No implementation or new test was added in this audit.

### What this audit does not establish

The textual review does not prove that the current implementation tests all stated edge cases, and it does not establish learner mastery.

## 12. Scope of this ledger

This is a traceable first-pass preservation record, not a claim that every line has passed scientific review. It deliberately records several items as **VERIFY**. A future review must resolve those statuses using the actual text and rendered pages rather than treating the inventory as a rubber stamp.


## 13. Reference loss implementation correspondence — 2026-10-28

**Scope:** compared the current public cross-entropy lesson pair with `src/llm_lab/foundations/losses.py` and `tests/unit/test_losses.py`. This was a source-level audit; it did not execute tests locally or inspect the rendered site.

- **What the implementation does:** accepts logits of shape `(B, C)` and one integer class target per row; computes the unweighted mean multiclass cross-entropy using natural logarithms; returns the gradient of that same mean objective with respect to logits.
- **What the tests support:** a known loss value, central finite-difference agreement for the logit gradient, stability for large finite logits, invariance to row-wise constant shifts, zero-sum gradient rows, no mutation of the input logits, and rejection of invalid shapes/targets/non-finite logits.
- **Boundary made explicit in both public languages:** the reference is not a token-sequence loss. It does not implement target shifting, token masks or `ignore_index`, soft targets, class weighting, perplexity, or gradients with respect to model parameters. Those are conceptual concerns described by the lesson, but must not be inferred to exist in this small implementation.
- **Disposition:** add direct links to the implementation and tests and describe their scope in both cross-entropy pages. Keep token-level alignment/masking as caller responsibilities; do not expand the code until a separate, justified implementation task has validated prerequisites.
- **Still open:** Quarto/CI validation of these edits, rendered-browser review of equations and responsive layout, internal/external link checking, and learner transfer questions. The source audit alone does not establish those outcomes or learner mastery.

## 14. Rendered-site local link checker — 2026-10-28

**Scope:** verified the implementation and CI integration introduced by PR [#21](https://github.com/JM-Brun/llm-lab/pull/21), merged into `main` at commit `a641203c5df922bdd29007d26db6191fe9ee0f73`.

- **Behavior:** after `quarto render site`, CI runs `scripts/check_site_links.py site/_site`. The dependency-free checker validates local rendered-HTML targets and fragment identifiers. It supports root-relative links, directory `index.html` targets, extensionless `.html` targets, and URL decoding.
- **Unit coverage:** tests cover valid local files/fragments and external URLs, missing local targets, and missing fragments.
- **Scope boundary:** external URLs are intentionally ignored to keep CI deterministic and avoid third-party outages. A successful check establishes local link/fragment integrity for that rendered artifact; it does not establish external reference availability, visual equation rendering, responsive layout, accessibility, or learner mastery.
- **Post-merge evidence:** on merge commit `a641203c5df922bdd29007d26db6191fe9ee0f73`, the Python CI workflow and Quarto site workflow both completed successfully. The separate publish workflow was still running at the time of this record.
- **Focused external-reference spot-check (not a complete bibliography audit):** the Shannon 1948 PDF and Cover–Thomas Wiley book page are accessible and match their cited works; the Hugging Face perplexity documentation is accessible and discusses tokenization/context-window effects; the official PyTorch `CrossEntropyLoss` page is accessible and documents logits, targets, ignored labels, and reduction; the two linked 3Blue1Brown entropy/cross-entropy videos resolve with matching titles. The Deep Learning Book page could not be fetched by the browsing tool because its response exceeded the tool's content limit; this is inconclusive, not evidence of a broken link.
- **Remaining validation:** browser inspection of MathJax and responsive layouts, a broader external-reference audit beyond this focused core slice, and private transfer-question evidence remain open.

## 15. Bilingual link parity — cosine similarity lessons — 2026-10-28

**Scope:** compared the external URLs and section structure in `site/fr/cosine-similarity.qmd` and `site/en/cosine-similarity.qmd` on the reviewed `main` snapshot.

- **Finding:** the English lesson linked an interactive synthetic demonstration of nearest-neighbour hubness (`A Fifth of Your Corpus Is Unreachable. It Isn’t the Dimensions`) that was not linked from the French lesson. The scientific concept and the Nielsen & Hansen paper were already covered in both languages; the difference was a supplementary teaching resource, not a missing core claim.
- **Correction proposed:** add a French-language description of the same demonstration, including the limitation that its synthetic Gaussian corpus is illustrative and is not evidence of real retrieval-system performance.
- **Other parity check:** the extracted external URL sets now differ only by this newly identified item before the correction; the bilingual feature-linearity pages had matching extracted external URL sets. This is a source-level URL/heading comparison, not a full semantic translation review or a claim that every external resource has been validated.
- **Remaining verification:** render and run CI; manually verify the external page's continued availability and inspect the lessons in a browser. The link checker intentionally does not probe external hosts.


## 16. Bilingual parity — embedding-space lesson — 2026-10-28

**Finding:** `site/fr/embedding-space.qmd` had no English counterpart, and its language switch pointed to the English home page rather than an equivalent lesson. The Quarto render list and English sidebar also omitted the topic.

**Correction in this change:** translate the existing conceptual lesson into `site/en/embedding-space.qmd`, add a matching English-language schematic rather than reusing a French-labelled figure, include the page in the Quarto render list and English sidebar, and connect the two language versions directly. The translation preserves the original scope, caveats, references, and the explicit warning that the suggested video has not been independently verified. The positional-encoding page remains French-only and is identified as such rather than implying English parity.

**Limits / remaining validation:** this is a content and navigation parity repair, not independent scientific validation of every cited paper, a semantic line-by-line audit by a second reviewer, or browser-based visual/accessibility sign-off. Quarto rendering and local-link CI must pass before the change is considered validated.


## 17. Bilingual parity — positional encoding and RoPE — 2026-10-28

**Finding:** the positional-encoding lesson existed only in French, its language switch pointed to the English home page, and the English Transformer overview linked directly to the French lesson. The English Quarto render list and sidebar had no corresponding entry.

**Correction in this change:** translate the existing explanation into `site/en/positional-encoding.qmd`, create a matching English-labelled RoPE diagram, add the page to the render list and English navigation, connect both language versions, and update the English Transformer overview to link to the English lesson. The translation retains the source page's scope, caveats about long-context extrapolation, implementation checks, and the warning that the suggested video has not been independently verified. No RoPE implementation is added.

**Limits / remaining validation:** this is a bilingual content/navigation repair, not independent scientific review of all RoPE variants or a second-reviewer translation audit. Quarto rendering and local-link CI must pass; visual review of the diagram, equations, and mobile layout remains open.


## 18. Follow-up navigation check — English Transformer overview — 2026-10-28

**Finding:** after the English positional-encoding/RoPE lesson was added, the attention walkthrough in `site/en/transformer.qmd` still linked first to the French page (`../fr/positional-encoding.qmd`) and then to the English page. The English page was available, so the French link was a stale cross-language navigation choice rather than a missing target.

**Correction:** make the primary positional-information link point directly to `positional-encoding.qmd` and keep the explanation and language switch consistent with the English lesson. The French counterpart remains available through the page's language switch.

**Scope / limits:** this is a targeted source-level navigation correction discovered during the post-merge check of PR #26. It does not constitute a complete scan of all rendered pages, external URLs, translation semantics, or browser/mobile presentation. Validate the full Quarto render and local-link checker on this change.


## 19. Homepage bilingual parity — 2026-10-28

**Finding:** comparing the French root homepage (`site/index.qmd`) with `site/en/index.qmd` showed a small content-parity gap. The French homepage explicitly linked tensors, embedding space, and positional encoding/RoPE in its “further reading” section, while the English homepage omitted that cluster. The English suggested path also omitted the explicit mention of positional information present in the French attention/Transformer path.

**Correction:** add equivalent English links to the tensor, embedding-space, and positional-encoding lessons, and mention positional information (including RoPE) in the suggested attention path. This reuses existing pages and does not expand the scientific scope.

**Scope / limits:** this is a targeted homepage parity check, not a complete semantic translation audit. Quarto render and rendered-site local-link validation are required; external resource availability and responsive visual presentation are not established by those checks.
