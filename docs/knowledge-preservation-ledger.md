# Knowledge-preservation ledger — LLM Lab math-page slice

**Status:** first-pass inventory; not yet a final approval to merge.  
**Public branch under review:** `docs/llm-application-math-refactor` (PR #17).  
**Comparison baseline:** `main` as inspected on 2026-10-27.  
**Rule:** no item is considered “moved” merely because a similarly named Wiki page exists. The public page must still teach every prerequisite needed for its LLM-specific objective.

This ledger records section-level dispositions for the first four concepts. A final content review must check the actual diff, equations, links, and rendered output before PR #17 is mergeable in substance. If a claim or useful teaching element is found missing, restore it to LLM Lab or explicitly decide—on pedagogical grounds—that it is not needed by the public book.

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

**Follow-up changes on this branch:** the English and French pages now explicitly state the support condition for the identity and that cross-entropy/KL are infinite when (q_i>0) but (p_i=0). The LLM-specific objective, target alignment, masking, reduction, perplexity, gradient, examples and practical misconceptions remain public. The final check must still verify the exact formula, target assumptions, and rendered page.

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

**Initial assessment:** this page was already LLM-specific in the baseline. It should be an application-focused refinement, not a removal of the core probability explanation. No Wiki dependency is necessary for this page.

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
| Video and Raschka reference | **VERIFY** | Keep if they provide distinct value; do not remove provenance without checking. PyTorch and NumPy docs support API-specific statements. |

**Initial assessment:** this is a strong application-focused improvement and fixes English parity. The new page adds LLM-specific shape semantics such as the vocabulary axis (V), attention heads, softmax axis, causal masks and logits/label alignment. Ensure that the basic scalar/vector/matrix explanation and the distinction between array rank and algebraic rank are still taught somewhere in the public book before considering them redundant.

## 5. Contributor-guidance audit

- `llm-lab/CONTRIBUTING.md` previously said to include “only the concise general definition” and “do not duplicate a full Wiki chapter”. This wording could incorrectly encourage removal of teaching material needed by the public book. The PR branch now clarifies that LLM Lab is a self-contained book, that intentional overlap is allowed, and that no page may depend on private Wiki content.
- `wiki-knowledge/CONTRIBUTING.md` previously said to link to one canonical page “instead of copying its definition into another page” without delimiting that rule to the Wiki. The proposed Wiki contributor-doc change clarifies that canonical uniqueness applies within the Wiki, not across independent books or applications.
- The Wiki concept pages added under `CONCEPT-020`–`CONCEPT-023` are marked draft per PR #23. Their existence is not evidence that their claims are scientifically reviewed, and they do not justify a public content deletion.
- Both contributor-doc changes require their own review and merge. They should not be treated as already merged into either repository's `main`.

## 6. Link-audit evidence

At commit `39d439078b585802b926c52681e6cd0d87dcfa3b`, a path-existence check covered 44 local Markdown/image references across the eight affected French/English concept pages (entropy, cross-entropy, probabilities, tensors): all targets existed in the branch tree. The check exposed one invalid English tensor-page link to a not-yet-translated embedding-space page; it was changed to an explicit link to the existing French page with the translation gap labelled. This check verifies target paths only, not anchors, rendered appearance, accessibility, or external URL availability.

## 7. Open checks before PR #17 can be approved

- [x] Inspect key equations and content for entropy, cross-entropy and tensors; review identified and corrected the target-indexing ambiguity and added explicit zero-probability conventions. [ ] Complete a passage-level comparison against the full baseline diff for all four concepts, including probabilities/softmax.
- [x] Textual review: the new entropy pages distinguish predictive entropy from observed-token surprisal and sequence NLL, state the finite-vocabulary bound in nats, include a numerical example/self-check, and state the (0\log 0=0) convention. [ ] Verify the rendered page and ensure any perplexity statements remain convention-aware.
- [x] Textual review: cross-entropy pages state the KL identity/direction, one-hot/soft-target cases, zero-mass-term convention, and zero-support caveat. A review found ambiguity between target-position and input-position indexing; both language pages now explicitly distinguish the conventions and require consistent logit/label shifting. [ ] Verify rendered output and the exact formulas/assumptions.
- [ ] Verify softmax examples, temperature claims, and normalization/calibration/truth distinctions.
- [x] Textual review: tensor pages distinguish output feature dimension (D') from attention-head count (H), explain array rank versus matrix rank, and preserve key misconceptions in both languages. [ ] Verify tensor shapes, diagram rendering/alt text, links, and FR/EN parity.
- [ ] Check the new Wiki concepts and their draft lifecycle, registry synchronization and links; treat them as supplementary only.
- [x] Path-existence audit for 44 local Markdown/image references across the eight affected pages; all targets exist at the recorded commit.
- [ ] Inspect rendered Quarto pages in both languages, including anchors, figures, alt text, navigation, and visual quality.
- [ ] Re-run CI and Quarto workflows on the latest head after the latest mathematical clarification commits.
- [ ] Review the final PR diff against this ledger; update this document if a disposition changes.
- [ ] Do not merge PR #17 until the checks above are completed.

## 8. Scope of this ledger

This is a traceable first-pass preservation record, not a claim that every line has passed scientific review. It deliberately records several items as **VERIFY**. A future review must resolve those statuses using the actual text and rendered pages rather than treating the inventory as a rubber stamp.
