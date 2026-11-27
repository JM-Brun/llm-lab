# Scaled dot-product attention — learning-page workflow pilot

**Review date:** 2026-11-26  
**Canonical pages:** [FR lesson](../../site/fr/scaled-dot-product-attention.qmd) · [EN lesson](../../site/en/scaled-dot-product-attention.qmd) · [FR Practice](../../site/fr/exercises/scaled-dot-product-attention.qmd) · [EN Practice](../../site/en/exercises/scaled-dot-product-attention.qmd)  
**Workflow:** seven-stage page-production sequence in [knowledge-change-workflow](../workflows/knowledge-change-workflow.md)  
**Pilot type:** mathematical / computational mechanism lesson (second archetype after Q/K/V)

## 1. Learner question and current coverage

**Learner question:** Given queries, keys, values and an optional mask, what exactly does scaled dot-product attention compute, in what order, over which tensor axes, and what does the resulting output mean?

The current bilingual lesson already presents the five-step operation, tensor shapes, additive hard-mask convention, row-wise softmax, weighted value aggregation, a distinction between position-level attention softmax and vocabulary-level output softmax, and interpretive limits. It links to the score-scaling derivation, causal masking, Q/K/V, probabilities, the Transformer overview and optional FlashAttention/Build material.

The dedicated Practice page contains focused self-checks and a weighted-mixture-vs-selection exercise. The complete one-query numerical trace already exists in the larger Attention exercise collection; it should be reached through the dedicated Practice page rather than duplicated in the core lesson.

## 2. Source contribution map

| Source / review | Material actually inspected | Distinct contribution | Evidence class and boundary | Decision |
|---|---|---|---|---|
| Vaswani et al. (2017), [primary paper](https://arxiv.org/abs/1706.03762), §3.2.1 Eq. (1), Fig. 2; [focused review](../source-reviews/vaswani-attention-formulation-2026-11.md); [extraction item](../../data/extractions/vaswani-et-al-attention-is-all-you-need-2017.yml) | Focused review of the formal definition, prose and figure; not a full-paper re-audit | Canonical operator: $\operatorname{softmax}(QK^\top/\sqrt{d_k})V$; scores, scale, softmax and weighted values; optional mask shown in Fig. 2 | Primary formal specification. The paper's Eq. (1) omits an explicit mask term; the mask is optional and shown in the figure. It does not support interpreting weights as MI, semantic importance or causal influence. | Technical anchor; preserve the equation and distinguish paper notation from the project's explicit masked form. |
| Jay Joshi, *The Mathematics of a Transformer Explained With Numbers You Can Check by Hand With Geometric Intuitions*, Part 2; [source review](../source-reviews/jay-joshi-transformer-mathematics-attention-2026-11.md) | Full article text from an indexed Medium snapshot; direct retrieval failed. Figures and PyTorch code were not inspectable. | Four-stage teaching sequence from position-encoded input through Q/K/V, scaled scores, softmax, weighted values and output projection | Secondary pedagogical source. The promised numerical values and visual/code trace were not available for verification. Its geometric language requires qualifications; its “convex cone” terminology is not interchangeable with convex hull. | Retain as a reference for sequencing only. Do not import unverified numbers, figures or code. |
| 3Blue1Brown, *Attention in Transformers, step by step*, via [comparative pedagogical review](../source-reviews/transformer-attention-pedagogical-comparison-2026-11.md) | Full text adaptation, lesson structure, embedded questions, YouTube description/timestamps and scene source; the rendered video itself was not independently watched | Contextual ambiguity before formalism; geometric Q/K intuition; staged scores → softmax → V aggregation; retrieval questions at transitions | Pedagogical evidence, not a primary mathematical source. Its column-vector/column-wise-softmax convention is compatible with the row-oriented convention used here after transposition; the axis must be stated explicitly. Animation pacing and visual legibility remain unverified. | Use the staged explanation and retrieval-question pattern as design references; state the project's row/column convention explicitly. |
| Jay Alammar, *The Illustrated GPT-2*, via the same comparative review | Full article text; asset-level rights review not refreshed | Architecture bridge to decoder-only GPT, causal masking, weighted aggregation, head splitting and training/inference distinctions | Secondary explanatory resource; historical GPT-2 details are not universal architecture rules. | Keep as a linked architecture reference; do not reproduce third-party figures. |

Convergence on the standard operator is explanatory convergence, not independent experimental validation. The primary paper anchors the mathematics; tutorial sources inform sequencing and examples only.

## 3. Pre-draft page blueprint

| Dimension | Decision |
|---|---|
| Learner problem and value | Learners may conflate raw compatibility scores, scaled scores, masked scores, normalized attention weights and the final weighted output. The lesson must make each object and transformation inspectable. |
| Observable outcomes | Reconstruct the five-step operation; state the shape of every intermediate; identify the softmax axis; explain why scaling precedes softmax; compute a one-query output in the companion Practice material; bound interpretations of attention weights. |
| Scope and ownership | Core lesson owns the standard one-head mathematical operation and its tensor flow. Q/K/V owns projection provenance and roles. Causal masking owns construction and invariants of the causal mask, including fully masked-row handling. Attention-score-scaling owns the variance derivation and simulation. |
| Prerequisites and route | Q/K/V is the previous conceptual lesson; causal masking follows. Tensor conventions and probabilities are useful references, not extra mandatory route steps. |
| Mathematical contract | $Q,K\in\mathbb{R}^{T\times d_k}$, $V\in\mathbb{R}^{T\times d_v}$; $S=QK^\top\in\mathbb{R}^{T\times T}$; $S'=S/\sqrt{d_k}$; $S''=S'+M$ for additive mask $M\in\mathbb{R}^{T\times T}$; $A=\operatorname{softmax}_{\text{keys}}(S'')$; $O=AV\in\mathbb{R}^{T\times d_v}$. The row index is the query position; the column index is the key position. Each non-empty row is normalized over accessible keys. |
| Worked-example decision | Do not add a second full numerical trace to the core lesson. The existing AT-0 one-query calculation already checks scores, scaling, softmax and weighted output; the dedicated Practice page will link to it. The core lesson keeps the symbolic matrix derivation and explicit shape trace. |
| Visual support | Keep the original project flow diagram and matrix-shape diagrams. Their role is to distinguish score, weight and output matrices, not to imply empirically observed attention patterns. |
| Source synthesis | Vaswani is the mathematical anchor; Jay Joshi contributes a pedagogical sequence but its promised numeric assets are unverified; 3Blue1Brown contributes geometric intuition and staged retrieval questions, with a different vector convention; Alammar provides a GPT-2 architecture bridge. |
| Misconceptions and limits | Softmax weights are relative within a query row, not absolute similarity or semantic relevance; high weight is not causal importance; convex-hull claims apply only to the normalized weighted sum before output projection/residual/MLP; a fully masked row is not a probability distribution and is handled by the causal-masking page. |
| Companions and transfer | Dedicated Practice page owns learner calculations; attention-score-scaling owns variance derivation; causal masking owns allowed-position construction; Build owns implementation; FlashAttention remains optional Deepen. Do not create a new page, route step, graph node or exercise collection. |
| Validation evidence | Check FR/EN parity, equation and shape consistency, row/column semantics, Practice link routing, source attribution and Quarto rendering. Browser accessibility and learner transfer remain separate validation gates. |

## 4. Seven-stage workflow evaluation

| Stage | Existing evidence and action | Result |
|---|---|---|
| 1. Ingest sources | Reuse the Vaswani primary-source review/extraction, Jay Joshi review and the comparative pedagogical review. | No re-ingestion. Inspection limits remain explicit; no claim that the 3Blue1Brown video or Jay Joshi figures/code were independently inspected. |
| 2. Model source knowledge | Vaswani extraction item is attached to existing canonical concepts and attention operations. The two pedagogical reviews retain source-local teaching sequences and limitations. | Sufficient for this bounded page decision. Do not create concepts from pedagogical labels or import unverified assets. |
| 3. Compile and synthesize | Compare formal definition, geometric intuition, staged retrieval and numerical-example claims against existing canonical lesson and Practice coverage. | Complementary roles are clear; no mathematical disagreement with the primary operator. The column/row convention is a representational difference, not a contradiction. |
| 4. Blueprint | The table above fixes learner contract, scope, mathematical contract, worked-example decision and companion ownership. | Complete for this revision. This dossier is the working record; no separate blueprint file or new registry. |
| 5. Write | Retain the existing five-step explanation and diagrams. Clarify the row/column axis convention and correct the page's stated purpose so it matches the actual lesson (reconstruct/explain the operator; numerical calculation is assessed in Practice). | Targeted FR/EN changes only; no unnecessary expansion of the core lesson. |
| 6. Derive companions | Route the inline calculation link through the dedicated Practice page; from there link to the existing AT-0 full calculation in the broader exercise collection. | No duplicated exercise or new page. |
| 7. Validate | Inspect source text, metadata, FR/EN equivalence, equations, anchors and local links; run Quarto/CI and inspect rendered pages. | Textual checks are performed in this change. CI/Quarto rendering, live browser/accessibility and learner validation must be reported separately and are not claimed complete until executed. |

## 5. Findings and integration decisions

1. **Metadata contract:** the old `purpose` promised a small numerical calculation on the core lesson, but the lesson deliberately delegates learner calculations to Practice. The new purpose describes the explanatory outcome and matrix reconstruction instead.
2. **Softmax axis:** the lesson already says “row-wise” and “per query”; the revision makes the mapping explicit: row $i$ is query $i$, column $j$ is key $j$, and normalization is over the key axis. This prevents confusion with column-vector presentations without introducing a competing convention.
3. **Practice navigation:** the core lesson's inline calculation link previously bypassed its dedicated Practice page. It now points to a named section on that page, which in turn links to the existing AT-0 worked calculation. The exercise remains in one canonical location.
4. **Mask edge case:** the causal-masking lesson already explains that a fully masked row makes ordinary softmax undefined and documents the reference implementation's zero-output convention. The core attention page should link to that owner rather than duplicate the caveat.
5. **No graph or route change:** no new concept, computational operation, semantic relation, route stage or page is justified.

## 6. Remaining work

- Run the repository's relevant CI and Quarto render against the final PR head; inspect both rendered language versions and verify the new anchors.
- Complete the live-host keyboard, touch and screen-reader checks tracked in #483; the source-review browser checks are not a substitute for a project-site accessibility audit.
- Run the learner pilot in #447 only after the accessibility/deployment gate; test transfer from Q/K/V to the full attention operator and distinguish score, weight and output matrices.
- Revisit the worked-example strategy only if learners cannot reconstruct the five operations from the symbolic page plus the existing Practice calculation.
- Keep third-party visual asset rights and uninspected source modalities explicit.

This second pilot tests a mathematical/computational page archetype. It does not establish that the seven-stage workflow is effective for all page types; an implementation-heavy Build page would be a distinct future test.

## 7. Page-level source diversity and claim-evidence audit — 2026-11-27

**Audit method:** distinguish the page's external citations, internal project artefacts, construction sources and the broad set of `related.pages` associations. The latter is a discovery index, not evidence that a source was used to construct or support a claim.

### 7.1 Reconciled source sets

| Source set | Inventory | What it means |
|---|---|---|
| External references visible in both published-language source files | Vaswani et al. (2017); Dao et al. (2022); PyTorch SDPA API | Three external references, all English: two primary research papers and one official API reference |
| Internal project artefacts linked by the page | FlashAttention source review; FlashAttention benchmark protocol | Repository documentation and a measurement plan, not independent external sources |
| Construction sources named in this pilot's source contribution map | Vaswani; Jay Joshi; 3Blue1Brown; Jay Alammar, *The Illustrated GPT-2* | A bounded editorial corpus: primary mathematical anchor plus complementary sequencing, geometry and architecture explanations |
| FlashAttention implementation bridge | Dao et al.; The AI Edge excerpt; PyTorch SDPA documentation | A distinct subtopic: algorithmic IO efficiency, secondary teaching explanation and framework API contract |
| Catalogue associations through `related.pages` | 16 source records currently point to the bilingual scaled-attention pages | Candidate discovery set only; do not count these 16 as sources used or cited by the page |

The three external references are not interchangeable:
- **Vaswani et al.** is primary evidence for the mathematical attention operator and its original formulation.
- **Dao et al.** is primary evidence for the IO-aware exact attention algorithm, its online-softmax tiling and its stated IO/compute analysis. It is not a second independent derivation of the base operator.
- **PyTorch SDPA** is authoritative for the documented PyTorch function contract. It is not a mathematical research source and does not prove which backend ran in a particular environment.

The two internal links are useful traceability artefacts, but must not inflate the external source count or be presented as independent evidence.

### 7.2 Diversity profile — visible bibliography versus discovery set

| Dimension | Visible external references (n=3) | `related.pages` candidate set (n=16) |
|---|---|---|
| Source type | 2 papers, 1 official documentation page | 9 blogs, 2 courses, 2 tutorials, 1 video, 2 papers |
| Language | 3 English | 15 English, 1 French |
| Technical role | Mathematical specification, algorithmic implementation research, framework API contract | Mixed: Q/K/V tutorials, Transformer visual explanations, attention mathematics, FlashAttention, information theory and positional-embedding resources |
| Origin | Vaswani et al./NeurIPS; Dao et al./NeurIPS; PyTorch project | Multiple creators/platforms; several are shared with the upstream Q/K/V page |
| Inspection | Focused primary reviews for both papers; PyTorch API reference inspected on 2026-11-27 | Heterogeneous and partial; association alone does not establish inspection for this page |
| Independence | Distinct sources, but their claims are not all the same claim | Unknown; no independence claim is made |

The visible bibliography is concentrated in English and in formal/technical references. For this mathematical/computational page, that is defensible: the primary paper anchors the operator, the second paper anchors an implementation algorithm, and the official API anchors framework behavior. The bilingual LLM Lab lesson is the learner-facing explanation. A French source should be added only if it contributes a distinct mathematical derivation, counterexample or implementation perspective; language quotas would be artificial.

The 16 associated records are not a coherent 16-source corpus. They include resources whose primary scope is Q/K/V or general Transformer architecture, plus an apparent outlier association to the Karatsuba multiplication article. The outlier and the broader associations should be reviewed individually before changing `related.pages`; no automatic cleanup is justified from association counts alone.

### 7.3 Provenance gap found and repaired: PyTorch SDPA

The page cited the official PyTorch SDPA API, but the matching source was absent from `data/sources.yml`. The stable documentation URL redirected to the versioned PyTorch 2.15 page during the 2026-11-27 inspection.

The missing provenance has now been added in this branch:
- `data/sources.yml`: `pytorch-scaled-dot-product-attention-api`, with the observed version and scan boundary;
- `data/extractions/pytorch-scaled-dot-product-attention-api.yml`: atomic API claims;
- `docs/source-reviews/pytorch-sdpa-api-reference-2026-11.md`: focused review and implementation decision.

The extraction separates six distinct API concerns:
1. reference operator and default scale;
2. boolean mask polarity (`True` means participate, opposite to `MultiheadAttention.key_padding_mask`);
3. causal-mask argument contract, including the `attn_mask` / `is_causal` exclusivity and non-square alignment;
4. caller-controlled dropout, including explicit zero during evaluation;
5. automatic backend dispatch, eligibility constraints and floating-point output differences;
6. version-specific experimental GQA support.

The review records a strict boundary: the API reference documents the function contract; it does not establish runtime backend selection, GPU speed, exact numerical parity or a general mathematical proof. The stable alias's redirect is a version/freshness risk; the inspected PyTorch 2.15 page also labels the function beta and subject to change. Recheck before version-sensitive Build guidance.

### 7.4 Claim-to-evidence map

| Page claim / learner need | Best supporting source | Evidence class | Boundary / non-claim |
|---|---|---|---|
| Standard operator `softmax(QKᵀ / √dₖ)V` | Vaswani et al., §3.2.1, Eq. (1) | Primary mathematical definition | Do not attribute the full masked implementation contract to Eq. (1); the optional mask is shown in Fig. 2 |
| Scale rationale and dimension dependence | Vaswani et al., §3.2.1; Brenndoerfer source review as a secondary derivation | Primary theory plus secondary explanation | The variance argument depends on assumptions; it is not a universal claim that every high-dimensional row saturates |
| Softmax normalization axis | Vaswani notation and the page's row-query/column-key convention; PyTorch pseudocode uses the final/key dimension | Mathematical convention plus API implementation reference | 3Blue1Brown uses a column-vector convention; it is compatible after transposition, not a contradiction |
| Mask placement and allowed positions | Vaswani Fig. 2; canonical causal-masking lesson; PyTorch SDPA for API-specific mask semantics | Primary figure, canonical project derivation and official API contract | Boolean mask polarity is API-specific; do not transfer it to other PyTorch APIs |
| Weighted aggregation of values | Vaswani et al., §3.2.1, Eq. (1) | Primary mathematical operator | The equation establishes weighted aggregation; the convex-hull consequence additionally requires nonnegative normalized weights |
| Convex-hull consequence (candidate, not a current page claim) | Brenndoerfer extraction item mbrenndoerfer-qkv-attention-mechanism:convex-hull; direct mathematical derivation from nonnegative normalized weights | Source-derived mathematical property | Applies only to a non-empty normalized row's weighted sum before output projection, residual addition or later transformations; it is absent from the current FR/EN lesson files |
| Exact IO-aware FlashAttention and online softmax | Dao et al. (2022), §§3.1–3.3 and Theorems 1–2 | Primary algorithm and complexity analysis | Exact dense attention retains quadratic arithmetic; IO complexity is not wall-clock performance |
| FlashAttention empirical speed/memory claims | Dao et al. (2022), §4 and appendices | Primary empirical results | Results are tied to the paper's hardware, shapes, dtype, workloads and baselines |
| PyTorch API backend dispatch and numerical differences | PyTorch SDPA API reference | Official API documentation | An SDPA call does not prove that FlashAttention ran; actual backend must be observed |
| Attention weights as semantic or causal explanations | No source in this page corpus establishes such a general interpretation | Explicit epistemic limit | Keep the page's interpretive caveat; do not convert mathematical weights into claims about causal importance or human-readable meaning |

### 7.5 Findings and decisions

1. **The cited bibliography is appropriately specialized, not generically diverse.** Two papers and one official API reference serve three different evidence functions. Adding another generic attention tutorial would not improve the technical evidence.
2. **The construction corpus is pedagogically more diverse than the visible bibliography.** Jay Joshi, 3Blue1Brown and Jay Alammar contribute alternative teaching sequences, geometric intuition and an architecture bridge; their inspection boundaries remain explicit.
3. **The PyTorch source-register omission was a real provenance defect.** It is repaired in this branch with a source record, extraction and review.
4. **The `related.pages` set is not a valid denominator for source diversity.** It includes 16 records with mixed scope and at least one association requiring scrutiny. Keep it as discovery metadata until each association is justified.
5. **No additional language, video or blog source is required at this stage.** The relevant question is whether each mathematical/API claim has the correct evidence class, not whether every source type is represented.
6. **No change to the public lesson is justified by this audit.** Keep the core page mathematical; route API-specific dropout, boolean-mask polarity and backend constraints to Build/Deepen material.

### 7.6 Remaining work and validation gates

- [x] Reconcile visible external citations in FR and EN; the same three external URLs and two internal artefact URLs occur in the same order.
- [x] Separate page-visible citations, construction sources, internal project artefacts and thematic associations.
- [x] Record the visible bibliography's source-type, language and evidence-role profile.
- [x] Register the PyTorch SDPA API and record the observed 2.15 documentation redirect.
- [x] Create a source extraction for the PyTorch API's operator, boolean and causal mask contracts, dropout, dispatch and GQA contract.
- [x] Create a focused PyTorch API review and distinguish API evidence from mathematical and algorithmic primary sources.
- [x] Add a claim-to-evidence map for the page's mathematical, masking, FlashAttention and API claims.
- [ ] Review the 16 `related.pages` associations individually; correct only demonstrably stale or over-broad links.
- [ ] Run source-catalogue and extraction schema validators on the final branch head.
- [ ] Run Quarto render and relevant CI for both language versions.
- [ ] Inspect the rendered equations, links, code/API callouts and mobile layout.
- [ ] Complete the live accessibility checks tracked in #483.
- [ ] Run the learner transfer pilot tracked in #447 after deployment/accessibility gates.

**Second-pilot conclusion:** the scaled-attention page has good evidence-role diversity for its actual mathematical/computational scope, but its visible references are English-only and its `related.pages` candidate set is broader than the page's real source corpus. The highest-value fix was not adding another tutorial; it was registering the already-cited PyTorch API and tracing each claim to the correct evidence class.


### 7.7 Current source-to-page destination verification — 2026-11-27

The FR and EN lesson sources were inspected directly. This is a source-file verification, not a fresh rendered-site, mobile or accessibility audit.

| Contribution and source item | Claim / teaching point | FR destination | EN destination | Current presence | Source role and decision |
|---|---|---|---|---|---|
| Vaswani et al. — [extraction](../../data/extractions/vaswani-et-al-attention-is-all-you-need-2017.yml), scaled-dot-product-attention | Standard scaled dot-product operator, scaling, softmax and weighted aggregation | [Five-step computation](../../site/fr/scaled-dot-product-attention.qmd#calcul-en-cinq-étapes) and [source attribution](../../site/fr/scaled-dot-product-attention.qmd#origine-et-role) | [Five computation steps](../../site/en/scaled-dot-product-attention.qmd#five-computation-steps) and [source attribution](../../site/en/scaled-dot-product-attention.qmd#provenance-and-purpose) | explicit | Primary claim evidence and construction source for the standard operator. The mask extension is separately qualified; do not attribute every implementation detail to Eq. (1). |
| Brenndoerfer — [extraction](../../data/extractions/mbrenndoerfer-qkv-attention-mechanism.yml), scaling-variance | Assumption-led derivation of the score-variance scale | [Scaling deep dive](../../site/fr/attention-score-scaling.qmd#deriver-variance) | [Scaling deep dive](../../site/en/attention-score-scaling.qmd#derive-variance) | implicit | The derivation is present in the advanced lesson, but the current page does not explicitly attribute that derivation to Brenndoerfer. Treat the source as a construction/reference resource, not as a currently cited claim source. |
| Brenndoerfer — same extraction, message-passing | Attention as content-dependent message passing | [Scaled attention](../../site/fr/scaled-dot-product-attention.qmd#calcul-en-cinq-étapes) | [Scaled attention](../../site/en/scaled-dot-product-attention.qmd#five-computation-steps) | absent | Weighted aggregation is taught; the message-passing analogy is not. Defer unless learner evidence justifies it. |
| Brenndoerfer — same extraction, convex-hull | Convex-hull consequence of normalized value aggregation | [Scaled attention](../../site/fr/scaled-dot-product-attention.qmd#calcul-en-cinq-étapes) | [Scaled attention](../../site/en/scaled-dot-product-attention.qmd#five-computation-steps) | absent | Mathematically valid under the stated assumptions, but not present in the current bilingual lesson. Defer; no new content is added by this audit. |

**Presence semantics:** explicit means the current page states the contribution; implicit means related teaching content exists but the source-specific contribution is not attributed or named; absent means the current page does not teach the contribution. These are dossier-level verification labels, not canonical extraction statuses.
