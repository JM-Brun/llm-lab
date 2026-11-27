# Cross-entropy lesson — intellectual-contribution pilot (#1739)

**Audit date:** 2026-11-27  
**Unit:** the canonical French/English pair (site/fr/cross-entropy.qmd and site/en/cross-entropy.qmd), with its advanced destination, practice companion and adjacent likelihood/loss pages.  
**Purpose:** test whether the issue #1739 contribution-inventory method transfers from an architectural lesson (Q/K/V) to a probabilistic/mathematical lesson.

## 1. Scope and page ownership

The core lesson owns the local penalty for a target at one token position: the relation between a target distribution \(q\), a predicted distribution \(p\), and the one-hot special case \(-\log p(y)\). It also owns the learner-facing distinctions needed to interpret that penalty correctly.

The lesson does **not** own the full derivation of the soft-target cross-entropy/KL identity, the constrained-optimization motivation for logarithmic loss, or the complete teacher/student distillation treatment. Those belong to the existing advanced page:

- [French — Formaliser mathématiquement la modélisation du langage](../../site/fr/language-modeling-math.qmd)
- [English — The mathematics of language modeling](../../site/en/language-modeling-math.qmd)

The neighbouring pages retain their own responsibilities:

- [Likelihood (FR)](../../site/fr/vraisemblance.qmd) / [Likelihood (EN)](../../site/en/likelihood.qmd): sequence scoring, autoregressive factorization and perplexity.
- [Loss (FR)](../../site/fr/loss.qmd) / [Loss (EN)](../../site/en/loss.qmd): aggregation over valid target positions, masks, reductions and training objective.
- [Practice hub (FR)](../../site/fr/exercises/cross-entropy.qmd) / [Practice hub (EN)](../../site/en/exercises/cross-entropy.qmd): retrieval questions and links to extended calculations.
- [Review sheet (FR)](../../site/fr/revision-cross-entropy.qmd) / [Review sheet (EN)](../../site/en/revision-cross-entropy.qmd): compact recall, not a replacement for derivation.

This separation is consistent with the page-map contract: scope and purpose define page ownership; route and related links express navigation; the concept graph remains separate from both.

## 2. Evidence corpus and inspection limits

| Source | Canonical record / extraction | What was used | Evidence boundary |
|---|---|---|---|
| Grant Sanderson / 3Blue1Brown, *But what is cross-entropy?* (Part 2, 2026) | 3blue1brown-cross-entropy-compression-intelligence-part-2-2026 | Cross-entropy as mismatched ideal code length; four-symbol distribution shift; pretraining NLL; constrained-optimization rationale; teacher/student soft targets; gzip language-tree analogy. | Creator-published captions accessed through a third-party transcript mirror and reconciled with official video metadata and upstream Manim source inspected statically. No frame-by-frame audiovisual review or code execution. Source remains partially scanned; reuse is link-only. |
| Grant Sanderson / 3Blue1Brown, *Reinventing Entropy* (Part 1, 2026) | 3blue1brown-reinventing-entropy-compression-intelligence-part-1-2026 | Prefix-free-code intuition, surprisal, entropy, conditional language probabilities and entropy rate; progression into cross-entropy. | Timestamped caption transcript and metadata reviewed; no frame-by-frame audiovisual review. Source remains partially scanned; reuse is link-only. |
| Wayland Zhang, *Information Theory Is All You Need (to Understand LLMs)* (2026) | wayland-zhang-information-theory-llm-2026 | Cross-entropy/KL statement and surrounding claims; useful counterexamples from the notebook and source review. | Complete article body inspected. All 18 English notebook cells inspected statically and five saved figures visually inspected; notebook not executed. Article figures, comments and remaining links not fully inspected. Source remains partially scanned. |
| Claude E. Shannon, *A Mathematical Theory of Communication* (1948) | shannon-mathematical-theory-communication-1948 | Conditional entropy, finite-state source entropy and the noiseless-channel coding theorem, as primary historical/theoretical context for source coding. | Primary paper §§6–9 and Theorems 3–6 and 9 inspected. Part II and appendices not exhaustively re-audited. It is not a modern autoregressive neural-LM specification and is not treated as the source of the modern cross-entropy training objective. |
| Xu et al., *A Theory of Usable Information under Computational Constraints* (ICLR 2020) | Linked from Wayland review; separately audited | Used only to validate the V-information discussion and the limits of the article's informal description. | Full paper inspected according to the existing Wayland review; authors' experiments were not independently rerun. Not a direct source for the core cross-entropy lesson. |

The sources are not four independent proofs of one claim. The 3Blue1Brown materials are strong pedagogical reconstructions; Wayland is a secondary conceptual map whose claims require qualification; Shannon is primary evidence for source entropy/coding results; the canonical equations and their assumptions are checked mathematically. Repetition across tutorials is not counted as independent corroboration.

## 3. Aggregated contribution inventory

The identifiers below are stable **within this dossier**. They aggregate source-level extraction items and project-derived teaching moves. They are not canonical concepts, page tags, computational nodes or a global contribution registry.

| Local ID | Learner question / distinctive contribution | Evidence and current location | Decision |
|---|---|---|---|
| ce-ic-01-target-versus-prediction | **What is being compared?** Keep target distribution \(q\) and model prediction \(p\) conceptually distinct. Cross-entropy is target-weighted surprisal under the prediction; predictive entropy \(H(p)\) asks a different question. | Core lesson: “Objective for one token” and the one-minute mental model; advanced page generalizes to soft targets. | **Keep in the core lesson.** This is the central conceptual distinction, not a second definition of entropy. |
| ce-ic-02-one-hot-as-special-case | **Why does token NLL appear?** When the target is one-hot, all target mass is concentrated on \(y\), so \(H(q,p)\) reduces to \(-\log p(y)\). | Core lesson: one-token equation and worked running example; linked to likelihood. | **Keep in the core lesson.** The one-hot reduction is the bridge from distributions to observed tokens. |
| ce-ic-03-same-p-different-target | **Can the same prediction have different losses?** Yes. Holding the predictive distribution fixed leaves predictive entropy unchanged, but changing the observed target changes the loss. The generation/scoring comparison makes the distinction operational. | Core lesson: “When the selected token and target differ”; links to the likelihood exercise comparing generation and scoring. | **Keep in the core lesson.** This is one of its strongest counterfactual teaching moves. It prevents the learner from treating the model-selected token as the training target. |
| ce-ic-04-non-target-probabilities-still-matter | **If only the target term appears, do other classes matter?** They still affect softmax normalization, the target probability and the gradient with respect to logits. | Core lesson: worked one-hot example immediately after \(H(q,p)=-\log p(y)\). | **Keep in the core lesson.** This is a compact but important mathematical correction to a likely misreading. |
| ce-ic-05-loss-is-not-truth | **Does a large penalty prove that the observed token is false or useless?** No. It measures probability assigned by a particular model to a target under a specified context/data convention. | Core lesson: interpretation of the one-token visual and misconception section; likelihood page further qualifies corpus/tokenizer dependence. | **Keep the qualification at the point of interpretation.** Do not turn predictive score into factual validation. |
| ce-ic-06-confidence-penalty | **Why are confident errors costly?** The \(-\log p(y)\) curve strongly penalizes assigning very low probability to the observed target; the 0.9 versus 0.1 visual gives a concrete scale contrast. | Core lesson: “Intuition visuelle” and explanation of the same-target comparison. | **Keep in the core lesson.** It is a useful quantitative intuition, not evidence of calibration or truth. |
| ce-ic-07-local-penalty-versus-batch-objective | **Is one token's cross-entropy already the training loss?** No. It is a local term; sequence/batch aggregation, valid positions, reduction and weighting are separate choices. | Core lesson: “Several positions”; Loss page owns the full mask/reduction contract; implementation notes distinguish local reference code from a complete LLM objective. | **Keep a concise boundary in the core lesson; link to Loss.** Avoid duplicating the batch derivation. |
| ce-ic-08-mismatched-codebook-cost | **What does cross-entropy mean operationally?** Data follow \(q\), but ideal code lengths are built from \(p\); the average cost is \(H(q,p)\). In the source's four-symbol example, the old code costs 2.625 bits under the shifted data distribution, versus \(H(q)=1.75\) bits; the excess is \(D_{KL}(q\Vert p)=0.875\) bit/symbol. | 3Blue1Brown Part 2 extraction mismatched-codebook-cost; present in both language-modeling-math pages, section “From probabilistic coding to distillation”, and the compression revision material. | **Keep in Deepen / compression bridge.** Do not insert the full coding example into the core token-loss lesson. |
| ce-ic-09-log-loss-under-explicit-assumptions | **Why the logarithm?** Under a separable expected per-event loss, normalized predictions, differentiability and the requirement that \(p=q\) minimize expected loss for every interior \(q\), the Lagrange first-order condition yields a logarithmic penalty (with the negative sign for a minimum). | 3Blue1Brown Part 2 extraction logarithmic-loss-rationale; present in both language-modeling-math pages, section “Why the logarithm?”. | **Keep in Deepen.** The assumptions and non-universality caveat are essential; this is not a theorem that all useful ML objectives must be log loss. |
| ce-ic-10-soft-target-distillation | **What changes when the target is a distribution rather than one observed token?** A teacher can provide a full next-token distribution; the student is trained against that soft target. This can carry richer per-example information, but the teacher is not ground truth. | 3Blue1Brown Part 2 extraction teacher-distribution-distillation; present in both language-modeling-math pages and linked to LLM evolution. | **Keep in Deepen / distillation.** Do not conflate teacher supervision with ordinary observed-token targets or predictive data compression. |
| ce-ic-11-kl-direction-and-support | **Is KL a symmetric distance?** No. Its direction matters; if \(q_i>0\) where \(p_i=0\), cross-entropy and \(D_{KL}(q\Vert p)\) are infinite under the extended-value convention. | Both language-modeling-math pages, section “Soft targets and KL divergence”, including a boundary example. | **Keep in Deepen.** This is a mathematically important qualification; the core lesson links to the derivation. |
| ce-ic-12-entropy-rate-context | **Why is language not a fixed bag of independent symbols?** The relevant source-coding view uses context-dependent probabilities and conditional entropy/entropy rate. | 3Blue1Brown Part 1 extraction entropy-rate-language; Shannon §§7–9; canonical entropy and compression revision pages. | **Keep with Entropy / compression.** Cross-link only; do not re-explain entropy rate on the cross-entropy page. |
| ce-ic-13-gzip-analogy-boundary | **Can cross-compressing text with gzip be treated as an exact cross-entropy measurement?** No. gzip is a practical dictionary/repetition compressor with finite-sample and framing effects, not an ideal probability coder. | 3Blue1Brown Part 2 extraction language-tree-gzip-analogy; the source synthesis explicitly records the analogy's limits. | **Optional case study only.** Do not use as a definition, benchmark or proof of language understanding. |
| ce-ic-14-reject-landauer-learning-ceiling | **Does Landauer's erasure bound prove a universal limit on what a model can learn?** No; that inference is not established by the physical principle. | Wayland extraction landauer-data-ceiling, source review and notebook audit. | **Keep as a source-review correction, not a cross-entropy lesson section.** It is outside this page's scope. |
| ce-ic-15-reject-attention-as-mutual-information | **Are attention weights mutual information?** No; attention rows are input-dependent normalized aggregation weights, whereas MI is defined from a joint distribution. | Wayland extraction attention-mutual-information; review and notebook audit. | **Keep with Attention.** It is a useful cross-domain counterpoint, but belongs on the attention page, not here. |

## 4. Page-level assessment

### Core lesson

The core page already offers more than the target two or three distinctive contributions:

1. the distinction between a predictive distribution and the observed target;
2. the counterfactual in which the predictive distribution remains fixed while the observed target changes, so entropy is unchanged but loss changes;
3. the explanation that non-target probabilities still matter through softmax normalization and the gradient;
4. the interpretation boundary that a low probability is a model score, not a truth judgement;
5. the separation between a one-position penalty and a sequence/batch objective.

The visual comparison of \(p(y)=0.9\) and \(p(y)=0.1\) adds quantitative intuition. The page does not need another generic definition, another one-hot derivation, or the full coding-theory detour.

### Advanced destination

The advanced bilingual page already contains the three high-value additions from 3Blue1Brown Part 2:

- mismatched-codebook cost and the numerical 2.625 / 1.75 / 0.875-bit example;
- the Lagrange-multiplier motivation for logarithmic loss, with explicit assumptions and limitations;
- teacher/student soft-target distillation, including the warning that the teacher distribution is not ground truth.

It also contains the KL identity, directionality and support boundary cases. The core page links to this destination in its “Soft targets and KL divergence” section. This is an intentional by-reference relationship, not a missing core-page contribution.

### Bilingual and curriculum coherence

The FR/EN page-map contracts agree on the page's local purpose, scope and route (likelihood → cross-entropy → loss). The main explanations, equations, caveats and links have bilingual counterparts. The advanced page is classified as type:deep-dive, destination:deepen, level:advanced; it is not a hidden prerequisite for the core lesson. The separate exercise hubs remain in Practice and do not duplicate the main explanation.

No new concept, graph edge, route step, lesson, visual asset or exercise is justified by this corpus.

## 5. Metadata traceability issue found and corrected in this pilot

The Wayland extraction item cross-entropy-kl-decomposition had:

- candidate_destinations.pages: [fr/cross-entropy, en/cross-entropy];
- a rationale saying to add the KL identity and worked example to the core cross-entropy lesson.

That destination is inaccurate for the actual integration. The core page links to the advanced math page; the full soft-target identity, derivation, support conditions and worked distribution example are in fr/language-modeling-math and en/language-modeling-math.

**Correction:** point the extraction item to the two advanced math pages and revise its disposition rationale to say that the contribution is integrated there and linked from the core page. Keep the item disposition integrate: the material is genuinely integrated, but in the correct canonical destination.

This is a second concrete traceability failure mode after the Q/K/V pilot: an extraction can be technically sound and have an accepted disposition while its proposed page destination is wrong or too coarse. The audit therefore needs to verify the actual destination, not just whether similar material exists somewhere in the site.

## 6. Meta-model fit

The existing architecture is sufficient for this case:

- data/sources.yml owns source identity, version, scan history, rights and source-to-page associations.
- data/extractions/<source-id>.yml owns source-scoped atomic items, locators, evidence, assumptions, limitations, pedagogical profiles/assessments and item dispositions.
- docs/source-reviews/ owns source-specific technical/pedagogical critique.
- docs/source-syntheses/ owns cross-source comparison and editorial decisions.
- Hidden page-map metadata owns page scope, purpose, route, hierarchy and related links.
- data/concepts.yml owns durable scientific concepts and typed relations.
- The guided route owns the learner progression; Practice pages own extended exercises.

Do not add a global contribution registry, a new page-map field, or a concept for each explanatory lens. This dossier uses local aggregate IDs to connect source items to actual page sections. As in the Q/K/V pilot, reconsider typed page-anchor metadata only after repeated evidence across materially different page types shows that dossier-level traceability is insufficient.

## 7. Reusable task sequence and deliverables for this page family

1. **Resolve page ownership:** read the FR/EN page maps and identify the core lesson, adjacent pages, Deepen destination, revision sheet and Practice hub.
2. **Close the existing corpus:** resolve source IDs, extractions, reviews and synthesis dossiers; distinguish source text, notebook/code, figures and primary sources.
3. **Extract/aggregate contributions:** group by learner question and cognitive obstacle, not by repeated terminology; preserve source locators and evidence limits.
4. **Cross-check technical claims:** use primary definitions/papers for information-theoretic claims; check assumptions, logarithm base, support and direction; do not promote tutorial wording into a theorem.
5. **Verify actual integration:** search both language page bodies and metadata; classify as explicit, implicit, linked by reference, elsewhere, absent or unverified.
6. **Decide placement:** core, short caveat, Deepen, Practice, adjacent page, reference, case study, defer or reject. Record why adding it would improve learning and why alternatives would overload or duplicate the page.
7. **Repair provenance:** correct source extraction destinations and rationales when the actual canonical owner differs; retain source records and prior evidence boundaries.
8. **Validate proportionately:** source catalogue/schema validation when extraction records change; FR/EN rendering and link checks when page content changes; concept/route validation only when those models change. Report automated, source, expert, visual/accessibility and learner checks separately.

### Deliverables from this pilot

- This page-centred contribution inventory and FR/EN coverage assessment.
- A corrected source-item destination for Wayland's cross-entropy/KL contribution.
- A precise ownership decision: core token-level penalty vs advanced KL/log-loss/distillation treatment.
- A reusable rule: a contribution is not “integrated” until its real bilingual destination is verified.
- No unnecessary page rewrite or model/schema extension.

## 8. What remains open

- Run the source-catalogue validator against the corrected extraction in the PR branch; do not claim it passed until run output is available.
- Run bilingual Quarto build/render and link checks if page content changes later; this pilot does not change page bodies.
- Browser, keyboard/accessibility and independent learner checks have not been performed for this pilot.
- A third pilot on a non-probabilistic mathematical page is still needed before finalizing issue-wide model-extension decisions.
- The issue-wide page inventory and audit of the complete canonical Understand route remain open.

**Pilot conclusion:** the existing cross-entropy lesson meets the distinctive-contribution quality heuristic without being lengthened. The most important improvement from this pilot is not a new explanation but better evidence-to-destination traceability and a more exact separation between core and advanced ownership.


## 9. Current source-to-page destination verification — 2026-11-27

This matrix checks the current bilingual Quarto files. The local ce-ic identifiers remain dossier-scoped aggregation IDs, not canonical concepts or a global contribution register. “Explicit” means the current destination teaches the contribution; the core-page link to an advanced destination is recorded separately from the advanced content itself.

| Contribution / source item | Learner claim | FR core reference | EN core reference | FR content destination | EN content destination | Presence and decision |
|---|---|---|---|---|---|---|
| ce-ic-01 — target versus prediction; project synthesis | Cross-entropy weights model-assigned surprisal by the target distribution; do not conflate target q with prediction p | [Objective for one token](../../site/fr/cross-entropy.qmd#objectif-pour-un-token) | [Objective for one token](../../site/en/cross-entropy.qmd#objective-for-one-token) | Same core section | Same core section | explicit; keep as the central core distinction |
| ce-ic-05 / ce-ic-06 — local penalty and confidence penalty; project synthesis | A token-level penalty measures assigned probability, not factual truth; low probability for the observed target incurs a large penalty | [Visual intuition](../../site/fr/cross-entropy.qmd#intuition-visuelle) and [misconceptions](../../site/fr/cross-entropy.qmd#idees-recues) | [Visual intuition](../../site/en/cross-entropy.qmd#visual-intuition) and [misconceptions](../../site/en/cross-entropy.qmd#misconceptions) | Same core sections | Same core sections | explicit; retain the caveat at the point of interpretation |
| ce-ic-07 — local term versus batch objective; project synthesis | One token's cross-entropy is a local term; sequence/batch aggregation and valid-position reduction are separate choices | [Several positions](../../site/fr/cross-entropy.qmd#plusieurs-positions) | [Multiple positions](../../site/en/cross-entropy.qmd#multiple-positions) | Same core section; full reduction contract remains on Loss | Same core section; full reduction contract remains on Loss | explicit; preserve the boundary and link to Loss |
| ce-ic-08 — [3Blue1Brown Part 2 extraction](../../data/extractions/3blue1brown-cross-entropy-compression-intelligence-part-2-2026.yml), mismatched-codebook-cost | Data follow q while ideal code lengths are derived from p; expected cost is H(q,p) | [Soft targets and KL](../../site/fr/cross-entropy.qmd#cibles-souples-kl) | [Soft targets and KL](../../site/en/cross-entropy.qmd#soft-targets-kl) | [Probabilistic coding and distillation](../../site/fr/language-modeling-math.qmd#probabilistic-coding-distillation) | [Probabilistic coding and distillation](../../site/en/language-modeling-math.qmd#probabilistic-coding-distillation) | explicit in Deepen; core page links by reference; keep the full codebook example out of the core lesson |
| ce-ic-09 — same extraction, logarithmic-loss-rationale | Under explicit separability, normalization, differentiability and minimization assumptions, logarithmic loss follows; this is not a universal theorem about all losses | — | — | [Explicit-assumption derivation](../../site/fr/language-modeling-math.qmd#why-logarithm-explicit-assumptions) | [Explicit-assumption derivation](../../site/en/language-modeling-math.qmd#why-logarithm-explicit-assumptions) | explicit in Deepen; retain assumptions and non-universality caveat |
| ce-ic-10 — same extraction, teacher-distribution-distillation | A teacher supplies a soft target distribution; a student is trained against it, without treating the teacher as ground truth | [Soft targets and KL](../../site/fr/cross-entropy.qmd#cibles-souples-kl) | [Soft targets and KL](../../site/en/cross-entropy.qmd#soft-targets-kl) | [Observed target to teacher distribution](../../site/fr/language-modeling-math.qmd#observed-target-teacher-distribution) | [Observed target to teacher distribution](../../site/en/language-modeling-math.qmd#observed-target-teacher-distribution) | explicit in Deepen; core page links by reference; keep distillation separate from ordinary one-hot pretraining targets |
| ce-ic-11 — [Wayland extraction](../../data/extractions/wayland-zhang-information-theory-llm-2026.yml), cross-entropy-kl-decomposition | H(q,p)=H(q)+D_KL(q||p); minimizing over p is equivalent to minimizing forward KL only for fixed q and compatible support | [Soft targets and KL](../../site/fr/cross-entropy.qmd#cibles-souples-kl) | [Soft targets and KL](../../site/en/cross-entropy.qmd#soft-targets-kl) | [Soft-target KL derivation](../../site/fr/language-modeling-math.qmd#soft-targets-kl-derivation) | [Soft-target KL derivation](../../site/en/language-modeling-math.qmd#soft-targets-kl-derivation) | explicit in Deepen; core page links by reference; extraction destination is correctly set to language-modeling-math |
| ce-ic-13 — same 3Blue1Brown Part 2 extraction, language-tree-gzip-analogy | gzip cross-compression is an empirical analogy, not exact cross-entropy or a measure of intelligence | — | — | — | — | absent from the core/advanced cross-entropy pages as a learner-facing case study; retain as an optional source-review/case-study candidate only |
| ce-ic-14 — Wayland extraction, landauer-data-ceiling | Landauer's erasure bound does not establish a general statistical-learning ceiling | — | — | — | — | absent by editorial decision; keep as a source-review correction, not learner-facing cross-entropy content |
| ce-ic-15 — Wayland extraction, attention-mutual-information | Attention weights are not mutual information: the former are input-dependent normalized compatibility coefficients, the latter depends on a joint distribution | — | — | [Attention and mutual information](../../site/fr/scaled-dot-product-attention.qmd#attention-information-mutuelle) | [Attention and mutual information](../../site/en/scaled-dot-product-attention.qmd#attention-mutual-information) | explicit in the attention lesson; outside the cross-entropy page's ownership and not duplicated here |

**Out-of-scope contributions:** ce-ic-12 (entropy-rate context) remains owned by the entropy/compression pages; ce-ic-14 remains a source-review correction; ce-ic-15 is routed to Attention rather than cross-entropy. These dispositions do not create a new page or route step.

**Source-role distinction:** 3Blue1Brown is a pedagogical reconstruction; Wayland is a secondary conceptual map whose claims are qualified; Shannon remains primary historical/theoretical evidence for source entropy and coding, not for the modern neural-LM training objective. An extraction item is not itself proof of a page claim: the current destination and the claim's mathematical assumptions are checked separately.

**Verification boundary:** this is a source-file inspection on 2026-11-27. It does not claim a new browser/rendered-page, visual, accessibility or learner validation. The core/advanced ownership and FR/EN destinations were checked separately.
