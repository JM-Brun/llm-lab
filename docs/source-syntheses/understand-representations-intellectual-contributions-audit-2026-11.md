# Understand representations — intellectual-contribution audit

**Issue:** [#1739 — Guarantee distinctive intellectual value for every lesson](https://github.com/JM-Brun/llm-lab/issues/1739)  
**Review date:** 2026-11-27  
**Status:** bounded source and page audit; no lesson edits proposed in this pass.  
**Scope:** the canonical Understand lessons `positional-encoding` and `contextualized-representations`, their FR/EN counterparts, revision sheets, dedicated Practice hubs, the contextualized-representations Deepen page, and the existing positional-encoding source synthesis.

This is one coherent batch of the exhaustive page-by-page audit. It does not certify the whole Understand route, the visual rendering, accessibility, or learner outcomes.

## 1. Method and evidence boundary

The audit followed the canonical `representations` stage in `data/guided-route.yml`; it did not create a competing page inventory. For each lesson, it inspected:

- the FR/EN Quarto source and hidden `LLM-LAB-PAGE-MAP v1` metadata;
- the linked revision sheet and dedicated Practice page in both languages;
- the page's actual source references and existing extraction records;
- the current ownership boundary with adjacent Understand and Deepen pages.

The source corpus was reused. No new source was ingested, and no claim of complete re-scanning is made. In particular, the positional-encoding source compilation records its own inspection limits; Ethayarajh (2019) is represented by a focused extraction, not a reproduction of the paper's experiments.

The evidence categories below are deliberately separate:

- **Observed:** directly present in the inspected page, companion, metadata, source dossier or extraction.
- **Interpretation:** editorial assessment of why the observed material helps learning.
- **Candidate action:** a proposed change, not a statement that it has been implemented.

## 2. Page-by-page matrix

### 2.1 Positional encoding — FR/EN

**Canonical pages:** `site/fr/positional-encoding.qmd`, `site/en/positional-encoding.qmd`  
**Route:** Understand → Representations; previous: Embedding space; next: Contextualized representations.  
**Declared learner outcome:** explain why token content alone is insufficient, compare where positional mechanisms act, and distinguish explicit information, implicit order and causal visibility.

| Distinctive contribution | Observed evidence and provenance | Why it matters | Placement decision |
|---|---|---|---|
| **1. A precise reason order must enter the computation: content-only self-attention is permutation equivariant.** | The core lesson motivates the issue with reordered sentences. The optional section derives \(\operatorname{Attention}(PX)=P\operatorname{Attention}(X)\) from the Q/K/V and row-wise softmax equations, with its assumptions stated. | Replaces the vague statement that “Transformers need position” with a testable mathematical reason: content-only attention reorders its outputs with its inputs and cannot by itself distinguish sequence order. | Keep the intuition and conclusion in the core lesson; retain the derivation in the optional mathematical section. No new concept or page is needed. |
| **2. Positional information is defined by its insertion point, not by one universal positional vector.** | The page compares absolute input addition, Shaw-style relative vectors, T5 bucketed score bias, ALiBi fixed score bias and RoPE rotations of projected Q/K. Provenance is consolidated in `docs/source-reviews/positional-encoding-source-synthesis-2026-11-26.md`; primary extractions include Vaswani (2017), Shaw et al. (2018), Raffel et al. (2020), Press et al. (2022) and Su et al. (2021). | The learner can locate a mechanism in the computation and predict which objects it changes. This is more transferable than memorizing a list of architecture names. It also prevents the false taxonomy in which RoPE is treated as a family disjoint from relative-position methods. | Keep the compact comparison in the core lesson. Keep frequency derivations, rotary algebra, implementation layouts and configuration details in the existing sinusoidal/RoPE deep dives. |
| **3. Causal visibility is not the same object as positional information; NoPE makes the distinction more subtle.** | The core page states that a causal mask restricts accessible positions, while NoPE may exploit nested causal prefixes as an implicit order signal. It explicitly says this supplies neither an absolute coordinate nor an explicit relative distance, and gives no long-context guarantee. The same distinction appears in the positional synthesis and the bilingual revision sheets. | Prevents two common errors: assuming the causal mask is an ordinary position embedding, and assuming the absence of an explicit positional transform means the model has no possible order signal. | Keep in the core lesson and revision sheet. Do not create a separate NoPE lesson from this observation alone. |
| **4. A computable positional signal does not prove length generalization.** | The bilingual Practice pages ask whether a sinusoidal vector being computable at an unseen position guarantees model generalization; the worked answer says no and identifies training length, data, architecture and context adaptation as relevant conditions. | Separates a mathematical property of an encoding function from an empirical capability of a trained model. | Keep as a Practice check and a short caveat; no additional core paragraph is necessary. |

**Existing value assessment:** the page already contains at least three substantial, mutually reinforcing contributions. The strongest distinctive feature is the insertion-point comparison joined to the separation of positional information, causal access and implicit order. The permutation-equivariance derivation supplies a formal foundation without burdening the main exposition.

**Potential risk:** the mechanism table is necessarily information-dense. Adding further positional variants or their detailed hyperparameters to the core lesson would weaken its purpose. The current boundary—conceptual comparison in Understand, derivations and implementation in Deepen—is appropriate.

**Source qualifications to preserve:**

- Vaswani et al.'s sinusoidal construction does not prove that a trained model generalizes to arbitrary sequence lengths.
- T5's bucket count and distance boundary are configuration-specific, not universal constants.
- ALiBi's reported extrapolation results remain tied to the paper's model, data and evaluation protocol.
- RoPE's relative-offset property concerns the Q/K score contribution; the score still depends on content-derived Q/K.
- The NoPE statement is an architectural possibility, not a universal property of every causal Transformer.

### 2.2 Contextualized representations — FR/EN

**Canonical pages:** `site/fr/contextualized-representations.qmd`, `site/en/contextualized-representations.qmd`  
**Route:** Understand → Representations; previous: Positional encoding; next: Transformer.  
**Declared learner outcome:** predict what can change an occurrence's state by separating token ID, position, accessible prefix and network transformations.

| Distinctive contribution | Observed evidence and provenance | Why it matters | Placement decision |
|---|---|---|---|
| **1. The same token ID can produce the same initial lookup while later states differ.** | The page uses two context-dependent readings of a word, explicitly assumes a shared token ID, and distinguishes table lookup from context processing. The figure is labelled as an illustration, not measured vectors. The source corpus includes Mikolov (2013), Ethayarajh (2019), 3Blue1Brown and other pedagogical references. | Makes the boundary between a static lookup and contextual computation concrete. The controlled shared-ID assumption prevents a tokenizer segmentation difference from being mistaken for contextualization. | Keep as the opening mental model. Preserve the qualification that a visible word need not correspond to one token. |
| **2. Context dependence is constrained by causal access, not by the full text displayed to an evaluator.** | The page explains that each position uses its accessible context. The dedicated Practice page tests three sequences, \([A,X,U]\), \([B,X,U]\), and \([A,X,V]\), at the fixed position of \(X\): changing the accessible past may change its state; changing the inaccessible future must not. | Converts “context matters” into a falsifiable dependency statement. It also makes the causal mask operational rather than merely descriptive. | Keep the compact principle in the core lesson and the controlled perturbation in Practice. The complete exercise correctly delays its scoring/loss sub-question until those lessons have been studied. |
| **3. Computational contextualization does not guarantee a clean semantic geometry or a single interpretable attention head.** | The page explicitly warns that contextualization does not guarantee human-interpretable sense clusters. Its linguistic examples are labelled as illustrations, not evidence that a particular head resolves coreference. The Practice hub repeats the limit. | Distinguishes a property of the forward computation from a stronger claim about what a representation means or what a component causally computes. This is a valuable scientific guardrail. | Keep in the core lesson. Do not replace it with a broad claim about semantic spaces or mechanistic interpretability. |
| **4. Empirical contextuality measurements are useful, but belong at the advanced level with their model and metric scope attached.** | The Ethayarajh (2019) extraction records three measures, anisotropy-adjusted baselines, layer-wise findings for ELMo/BERT/GPT-2 and the study-specific MEV result. The bilingual Deepen page discusses the results and qualifications. The core page only credits the illustrative motivation. | Shows how to move from a conceptual claim (“representations vary with context”) to an operational measurement, while preventing a study-specific result from becoming a universal law. | Keep the measurement framework and numerical findings in `contextualized-representations-advanced`; link to Deepen rather than importing its technical detail into the core lesson. |

**Existing value assessment:** the core page has at least three substantive contributions: shared lookup versus context-dependent states, a causal perturbation boundary, and a disciplined separation between computational contextualization and semantic interpretation. The fourth contribution is intentionally developed in Deepen rather than duplicated.

**Practice ownership check:** the dedicated Practice hub contains both the core causal-boundary exercise and a guided SAE/Neuronpedia investigation. The latter is explicitly linked from the Deepen page's section on inspecting features, so its presence is not an accidental claim that SAE analysis is a core prerequisite. Keep it optional and clearly separated from the basic comprehension questions. A future metadata pass may consider recording the existing Deepen-to-Practice relationship in the Practice page's `related` field; no change is required to validate the current learning content.

**Source qualifications to preserve:**

- Ethayarajh's metrics are geometric diagnostics, not direct measures of semantic correctness or task quality.
- The paper's layer-wise results and MEV figure are scoped to its evaluated models and procedure.
- A linguistic example motivates a possible contextual dependency; it does not demonstrate a learned circuit or a single-head explanation.
- A same-ID example is conditional on the tokenizer actually assigning the same ID to both occurrences.

## 3. Companion and bilingual alignment

| Artifact | Positional encoding | Contextualized representations |
|---|---|---|
| Core FR/EN pages | Same conceptual distinctions and mechanism taxonomy; language-specific examples and phrasing | Same lookup/context/causality argument; language-specific running examples |
| Revision FR/EN | Recalls absolute/relative insertion points, causal visibility, NoPE and permutation reasoning | Recalls lookup, position-wise hidden states and the causal boundary |
| Practice FR/EN | Four self-check questions, a prefix-permutation transfer exercise and five recall cards | Shared-ID/context questions, four recall cards, a controlled causal-boundary exercise and optional SAE investigation |
| Deepen destination | Existing sinusoidal and RoPE pages own derivations and implementation | Advanced contextualized-representations page owns sublayers, empirical measures and interpretability material |

The inspected source files show semantic FR/EN parity for these learning objectives. This is not a claim of rendered visual parity: browser, responsive, keyboard, screen-reader and learner checks are not part of this source audit.

## 4. Meta-model fit and preservation decision

The current model is sufficient for these two pages:

- `data/sources.yml` owns source identity, classification, scan history and page associations.
- `data/extractions/<source-id>.yml` owns atomic source contributions, locators, evidence, pedagogical profiles, assessments and item dispositions.
- Source-review/synthesis dossiers own cross-source comparison and editorial reasoning.
- `data/concepts.yml` owns canonical scientific concepts.
- `data/guided-route.yml` owns the core learning sequence and outcomes.
- `LLM-LAB-PAGE-MAP v1` owns page scope, purpose, routes and page relations.

**No new page metadata field, contribution registry, concept node, computation node or route step is justified by this batch.** The distinctive contributions can be traced through existing extraction items and the source synthesis to their actual destinations.

Preservation rule for this batch: do not remove or rewrite the NoPE/causal-visibility distinction, the insertion-point taxonomy, the shared-ID assumption, the causal future-perturbation invariant, or the semantic-geometry caveat during future page refactors without an explicit replacement destination and a bilingual verification.

## 5. Decisions and follow-up

| Priority | Decision / action | Status |
|---|---|---|
| P0 | Preserve the four positional distinctions and their source qualifications | Retain; no lesson edit proposed |
| P0 | Preserve the contextualization causal-boundary experiment and its separation of distribution from observed target/loss | Retain; no lesson edit proposed |
| P1 | Keep Ethayarajh's metric definitions and empirical findings in the existing Deepen destination | Correct placement already observed |
| P1 | Consider a typed `related` link from the contextualized-representations Practice hub to its existing Deepen page, since the advanced page links to the SAE investigation there | Candidate metadata refinement; defer until the broader metadata audit |
| P2 | Perform rendered FR/EN desktop/mobile and keyboard/accessibility review of both page groups and their companions | Not performed in this audit |
| P2 | Seek learner evidence only if later feedback or assessment results reveal a concrete comprehension failure | Not performed; no learner validation claimed |

## 6. Transferability conclusion

These pages confirm that the contribution method is not limited to the three earlier pilots:

- Q/K/V tests a mechanism and parameter-role distinction.
- Cross-entropy tests a mathematical objective and its interpretation.
- Embedding space tests a representation and lookup invariant.
- Positional encoding tests a family of mechanisms and their distinct computational insertion points.
- Contextualized representations tests a causal dependency and the epistemic boundary between computation and semantic interpretation.

Across these cases, the most reliable distinctive contributions are not “extra facts”. They are **invariants, discriminating counterfactuals, carefully bounded mathematical properties, and explicit limits on what an observation proves**.

This supports continuing the audit with the next Understand batch. It does not yet establish exhaustive coverage of the route or justify freezing a project-wide contribution schema. The next batch should follow the canonical route order and inspect the Transformer system-overview page and the attention/computation lessons, while reusing the already merged Q/K/V pilot rather than auditing that page again from scratch.
