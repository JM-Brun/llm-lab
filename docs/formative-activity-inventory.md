# Minimal formative activity inventory — text to representations

> **Status: design inventory; not learner-release ready.** This document satisfies the inventory stage of [#313](https://github.com/JM-Brun/llm-lab/issues/313) and coordinates the existing detailed draft in [formative-sequence-text-to-representations.md](formative-sequence-text-to-representations.md). It does not publish exercises, establish learner mastery, or replace the canonical lessons.

## Design decision

The first sequence contains **three substantial activity bundles**, not six independent exercises. The six existing draft sections TR-01–TR-06 are retained as subparts, scaffolds, and optional extensions; no mathematical content or misconception feedback is discarded.

- TR-01 remains the pipeline reconstruction.
- TR-02, TR-05 and TR-03 become one progressive lookup-and-shape activity: calculate first, complete a scaffold, then generalize to a batch.
- TR-04 and TR-06 become one diagnosis-and-prediction activity: classify claims, then predict which representation can change under controlled changes to identity, position or context.

Suggested order: **TR-A → TR-B → TR-C**. This is a first formative sequence, not a delayed transfer test or a mastery assessment.

## Activity inventory

| Stable ID (FR/EN) | Observable outcome | Prerequisites and canonical lesson | Response format | G milestone | Success criterion |
|---|---|---|---|---|---|
| **TR-A — Reconstruct the representation pipeline** / **Reconstruire la chaîne des représentations** | Reconstruct source text → tokenizer units → integer IDs → embedding lookup → initial token vectors → architecture-dependent position handling/network computation → contextualized hidden states; explain what each transition does. | First pass through [Text and data](../site/en/text-data.qmd) / [Texte et données](../site/fr/text-data.qmd) and [Embedding space](../site/en/embedding-space.qmd) / [Espace des embeddings](../site/fr/embedding-space.qmd). | Ordered sequence plus one-sentence explanation per transition; short justification of where positional handling belongs. | **G1–G3** (input representation and transition into G3). | All objects are correctly ordered and distinguished; IDs are discrete indices, lookup does not contextualize, and positional handling is not described as universal. |
| **TR-B — Calculate lookup and trace tensor shapes** / **Calculer un lookup et suivre les formes des tenseurs** | Select the correct rows from a synthetic embedding matrix; compute the resulting vectors; infer single-sequence and batched shapes; explain why the vocabulary axis is not retained after lookup. | [Embedding space](../site/en/embedding-space.qmd) / [Espace des embeddings](../site/fr/embedding-space.qmd); [Tensors](../site/en/tensors.qmd) / [Tenseurs](../site/fr/tensors.qmd) as an optional notation reference, not a prerequisite gate. | Hand calculation of selected rows, matrix result, shape table with named axes, and a short explanation. | **G3 — Represent tokens.** | Exact selected rows and output; correct shapes (L,d), (B,L) and (B,L,d) with axes named; no confusion between vocabulary size and embedding dimension; no claim that lookup mixes positions. |
| **TR-C — Diagnose identity, position and context** / **Distinguer identité, position et contexte** | Evaluate claims about fixed IDs, initial lookup vectors and contextualized states; predict what can change when a token moves, its identity changes, or visible preceding context changes. | [Contextualized representations](../site/en/contextualized-representations.qmd) / [Représentations contextualisées](../site/fr/contextualized-representations.qmd), [Positional encoding](../site/en/positional-encoding.qmd) / [Position et RoPE](../site/fr/positional-encoding.qmd); TR-A and TR-B. | Classification (valid / invalid / architecture-dependent) with justification, followed by a compact prediction table. | **G3 — Represent tokens.** | Distinguishes fixed-table lookup invariants from position/context-dependent computations; qualifies absolute position embeddings versus RoPE; respects causal masking; makes no unsupported claim about the magnitude or propagation of numerical changes. |

## Traceability to the six existing draft sections

| Inventory activity | Existing detailed draft sections | Treatment |
|---|---|---|
| TR-A | TR-01 | Retain as the core reconstruction task. |
| TR-B | TR-02 + TR-05 + TR-03 | Merge into one progressive activity: explicit lookup calculation → scaffolded axis completion → batch-shape generalization. Keep each existing hint, worked value and misconception as a stage or feedback item; remove repeated instructions only during later editorial integration. |
| TR-C | TR-04 + TR-06 | Merge claim classification and controlled prediction into one diagnosis activity. Preserve architecture qualifications, causal-mask condition, and the distinction between qualitative dependency and guaranteed nonzero numerical change. |

The existing six-section draft remains the detailed answer-key source until the consolidated FR/EN artifact is edited and reviewed. This inventory does not silently delete or supersede it.

## Scope and release boundaries

- No question bank, quiz engine, learner tracking, or new concept page.
- No transfer/retention assessment at this stage. TR-C is a within-sequence prediction and misconception-diagnosis task, not evidence of durable learning.
- Toy embedding values remain explicitly synthetic; IDs are not metric coordinates.
- FR/EN versions must preserve mathematical content, difficulty, hints, solutions, and feedback.
- A separate reviewer is still required for independent scientific/mathematical review. Author self-review is not independent review.
- Rendered desktop/mobile inspection remains deferred to [#320](https://github.com/JM-Brun/llm-lab/issues/320); this inventory does not claim browser validation.
- Publication remains subject to the release gates in [#220](https://github.com/JM-Brun/llm-lab/issues/220), including independent review, bilingual parity, integration with the G3 route, and rendered validation.

## Next bounded work

1. Independently review the TR-02 matrix lookup and every TR-B shape/axis statement.
2. Compare TR-C's absolute-position and RoPE claims against the canonical FR/EN lessons and primary sources.
3. Integrate the three-bundle structure into the detailed answer-key document without losing the existing hints, worked solutions, or misconception feedback.
4. Link the activities from the G3 evidence field and the relevant existing pages only after the #220/#87 coordination check.

## Notation note

The lookup exercise uses `d` for the embedding width in its small matrix example. The optional tensor reference uses `D` for the model feature width and `d_h` for a per-head width. In this G3 example, `d` and `D` denote the same feature-axis role; they are local notation choices, not different dimensions. Keep the mapping explicit when integrating the exercise into the tensor lesson. Do not infer that `d` and `D` are interchangeable in every formula or architecture.
