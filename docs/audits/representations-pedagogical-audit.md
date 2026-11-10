# Representations and embedding-lookup lessons — pedagogical audit and revision

**Date:** 2026-11-10  
**Scope:** French and English Understand lessons on token embeddings (`embedding-space.qmd`) and contextualized representations (`contextualized-representations.qmd`); the preceding text-data lessons (`text-data.qmd`, `tokenization-strategies.qmd`); and the following positional-encoding and Transformer overview lessons.  
**Comparison reference:** Rushang Chauhan, [*Embeddings: The Bridge Between Tokens and Context*](https://www.linkedin.com/pulse/embeddings-bridge-between-tokens-context-rushang-chauhan-oqpzf/); Ethayarajh (2019), [*How Contextual are Contextualized Word Representations?*](https://arxiv.org/abs/1909.00512).  
**Status:** Source-level audit and bilingual revision committed to the working branch; rendered and learner validation remain open.

## 1. Evidence level and method

The audit follows the repository's [Understand Path Audit](../../.agents/skills/understand-path-audit/SKILL.md) and the existing contracts for [page composition](../page-template-guide.md), [reader experience](../reader-experience-and-editorial-method.md), [content ownership](../content-section-mapping.md), and [page review status](../page-audit-inventory.md).

Inspected:

- `site/fr/embedding-space.qmd` and `site/en/embedding-space.qmd`;
- `site/fr/contextualized-representations.qmd` and `site/en/contextualized-representations.qmd`;
- `site/images/embedding-space-fr.svg`, `site/images/embedding-space-en.svg`, `site/images/contextualized-embeddings-fr.svg`, and `site/images/contextualized-embeddings-en.svg`;
- the French and English text-data and positional-encoding lessons;
- the bilingual page metadata and their stated learning objectives.

This is a **source-level review**. It establishes what the Quarto sources and SVGs specify. The published pages could not be inspected in a browser during this pass; no claim is made about rendered typography, responsive behavior, keyboard interaction, or actual learner comprehension. No learner study was conducted.

## 2. Reader journey and page boundaries

| Position | Reader's likely question | Knowledge brought in / added | Transition |
|---|---|---|---|
| Previous: `tokenization-strategies.qmd` / `text-data.qmd` | How does text become integers? | The reader knows text is split into tokens and mapped to integer IDs in a finite vocabulary $V$. | Token IDs are discrete integers, not differentiable vector representations. |
| Current 1: `embedding-space.qmd` | How does an integer ID become a vector, and what are its properties? | Explains the lookup as row indexing $E_i = E[i]$ in a learned table $E \in \mathbb{R}^{V \times d}$; establishes that two occurrences of the same ID retrieve the exact same initial vector; refutes integer proximity fallacies. | The lookup is purely static and non-contextual. Next question: how does sequence position and context change internal states? |
| Current 2: `contextualized-representations.qmd` | Why and how does the same token develop different hidden states in different sentences? | Demonstrates that identical initial embeddings diverge once position encodings and sequence attention mix surrounding context; distinguishes table lookup from contextualization. | Once the reader understands how contextual states emerge, the next question is the full Transformer forward pass and attention mechanisms. |
| Next: `positional-encoding.qmd` / `transformer.qmd` | How is position represented (absolute, relative, rotary), and how does attention compute contextual mixtures? | Follows the canonical route towards positional mechanisms and Transformer block operations. | The representations stage leaves score computation, causal masking, and projections to dedicated subsequent lessons. |

The route boundaries are clean and preserved.

## 3. Findings and decisions

| Priority | Finding and source evidence | Reader impact | Decision |
|---|---|---|---|
| **P1** | Neither lesson provided an executable, self-contained micro-workbench with shape assertions, making the row-selection invariant abstract. | Readers had to infer tensor shapes and row-indexing behavior purely from mathematical notation. | Add bilingual runnable Python/NumPy micro-workbenches with shape invariants and identity assertions ($E[\text{ID}_i] \equiv E[\text{ID}_i]$ and divergence $h_A \neq h_B$ after contextual mixing). |
| **P1** | Readers frequently confuse numerical integer ID proximity (e.g. 2 vs 3) with vector-space proximity, and confuse identical token IDs with inability to distinguish polysemy. | Common learner misconceptions were not explicitly countered with concrete refutations. | Add folded "Spot the Fallacy" counterexamples targeting consecutive-ID fallacies and tokenizer-versus-context confusions. |
| **P2** | Navigation between the lessons lacked clear pipeline breadcrumbs and direct links to the matching practice exercises in `exercises.qmd`. | Readers were told that practice was "planned" under `#transformer`, even though `Exercise TR-B` (lookup) and `Exercise TR-C` (contextualization) already exist in `exercises.qmd#donnees-textuelles`. | Add pipeline steppers, epistemic badges, route navigation cards, and direct links to `Exercise TR-B` and `Exercise TR-C`. |
| **P2** | The learning outcomes were not exposed in structured, collapsible format at the top of the lessons. | Readers did not have clear criteria for self-assessing their mastery before reading. | Add standardized collapsible `.callout-note .learning-outcomes` blocks to both lessons in FR and EN. |

## 4. Changes applied

The French and English concept pages now share an enhanced pedagogical structure:

1. Standard page-to-page orientation and lead paragraph.
2. Collapsible, observable learning outcomes.
3. Interactive pipeline stepper showing position in the LLM flow.
4. Epistemic status badges.
5. Qualitative and mathematical exposition of the lookup / contextualization mechanisms.
6. Self-contained NumPy micro-workbenches demonstrating tensor operations and testing invariants with assertions.
7. Folded "Spot the Fallacy" active-recall counterexamples.
8. Self-checks directly cross-linked to existing exercises `TR-B` and `TR-C`.
9. Bidirectional route navigation cards.

## 5. Preservation and scientific checks

- The page IDs, destination, level, suggested route, hierarchy, and related-page metadata were not changed.
- Existing project-owned SVGs and external illustrations under review were retained without alteration.
- The `tiktoken` reproducible trace in `embedding-space.qmd` was preserved intact to ensure compatibility with `site/tools/check_embedding_trace.py`.
- Numerical values in micro-workbenches are explicitly labelled synthetic and illustrative.
- The distinction between static token embeddings, contextualized states, and sentence embeddings remains strictly maintained.

## 6. Validation status

| Check | Status | Evidence / limitation |
|---|---|---|
| French and English concept parity | **Done at source level** | Both versions share identical learning outcomes, pipeline steppers, epistemic badges, micro-workbenches, fallacies, and navigation cards. |
| Micro-workbench execution | **Verified** | NumPy blocks verified with assertions in sandbox test runs. |
| Math delimiter compliance | **Verified** | `python3 site/tools/check_math_delimiters.py site` passed without errors. |
| Page metadata compliance | **Verified** | `python3 site/tools/check_page_metadata.py` passed without errors. |
| Test suite | **Verified** | 358 passed, 1 skipped, 99.20% coverage under `PYTHONPATH=src pytest`. |
| Ruff formatting and lint | **Verified** | `uv run ruff check .` and `uv run ruff format --check .` passed cleanly. |
