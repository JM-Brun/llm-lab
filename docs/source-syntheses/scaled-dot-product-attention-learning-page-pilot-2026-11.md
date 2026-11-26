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
