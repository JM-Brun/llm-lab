# Training-example Practice transfer exercises — 2026-11-25

## Scope

Extend the existing bilingual Practice companions for the Build lesson on training examples. This implements the bounded follow-up identified by the source audit `training-example-practice-gaps-2026-11-25.md`.

Files changed:
- `site/fr/exercises/training-examples.qmd`
- `site/en/exercises/training-examples.qmd`

The lesson pages and the NumPy reference implementation are intentionally unchanged.

## Changes

The four existing checks are retained and made slightly more diagnostic with hints. Two transfer scenarios are added in both languages:

1. **Packed document boundaries.** Learners derive the mechanically shifted input/target pair for two concatenated documents, identify the visibility permitted by an ordinary causal mask, and distinguish an EOS marker from an attention policy. The solution also surfaces a subtle boundary condition: the output at the previous document's EOS position predicts the first token of the next document under mechanical shifting. If that transition is not part of the objective, target/loss construction must handle it explicitly in addition to any block-diagonal attention mask.
2. **Padded batch and loss reduction.** Learners construct separate attention and loss masks for unequal-length examples, calculate the valid-token mean (5/8 = 0.625), compare it with the naive padded-position mean (12/10 = 1.2), and diagnose why an attention mask alone does not exclude PAD labels from cross-entropy.

## Pedagogical and technical boundaries

- Preserve the separation between Understand/Build explanation and Practice questions.
- Keep the existing six-stage Text data collection and its TR-D window arithmetic / TR-F leakage exercises as the owners of those topics; do not duplicate them.
- Do not expand `sliding_input_target_pairs`: the exercises do not claim that the repository implements packing, padding, collators, cross-document masks or loss masks.
- Do not prescribe one universal packing or reduction policy. State the objective and boundary semantics before choosing masks.
- Keep the FR/EN task structure, numerical data, calculations and conclusions equivalent.
- No concept registry, guided-route, knowledge-graph or generated map change is required: the page identities and lesson-to-companion relationship are unchanged.

## Validation required

Run the existing Python and Quarto/site workflows on the final PR head. Inspect both rendered companions for:
- all six questions and their answer disclosures;
- correct inline/block math rendering;
- valid lesson and language-switch links;
- desktop/mobile layout without horizontal overflow;
- keyboard operation of native disclosures.

These checks do not constitute manual screen-reader testing or learner validation. The former remains with the accessibility workstream; the latter remains owned by issue #447.
