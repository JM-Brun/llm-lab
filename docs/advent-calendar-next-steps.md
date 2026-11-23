# Advent calendar — remaining work and session handoff

**Last updated:** 2026-11-23  
**Status:** editorial redesign documented and merged; implementation of the new experience has not started.  
**Parent decision:** PR [#1551](https://github.com/JM-Brun/llm-lab/pull/1551) — merged into `main`.

This document is an operational handoff for future sessions. It records what is complete, what remains, the order of work, and the conditions for considering the calendar ready. The editorial rationale and proposed 24-story slate remain in [advent-calendar-editorial-redesign.md](advent-calendar-editorial-redesign.md); this file should not duplicate that specification.

## 1. Current state — verified

### Completed

- [x] The calendar's editorial direction was changed from a compressed second learning path to a collection of 24 independent scientific stories.
- [x] The new editorial contract, anti-duplication rules, proposed 24-story slate, source standards, rendering requirements, and pilot acceptance gates were documented.
- [x] The former curriculum-summary design was marked historical/superseded.
- [x] The former 24-day manifest was marked superseded and retained as historical material.
- [x] PR [#1551](https://github.com/JM-Brun/llm-lab/pull/1551) was merged on 2026-11-23.

### Not completed

- [ ] No new story pilot has been written or accepted.
- [ ] No new Quarto article template has been implemented and visually validated.
- [ ] The existing landing page and day pages have not yet been fully audited against the new direction.
- [ ] No new story-oriented manifest has been approved or created.
- [ ] The 24 existing entries have not been migrated; they remain prototype/historical material.
- [ ] No novice-reader review has been performed.
- [ ] No FR/EN desktop/mobile visual acceptance has been recorded for a new story.

**Important:** merging #1551 means the editorial decision is recorded. It does not mean the calendar implementation is complete or ready to publish.

## 2. Execution order

Work in the following order. Do not start all 24 articles in parallel.

### Phase A — inventory and transition audit

- [ ] Inspect the current Quarto project configuration, navigation, calendar landing page, day-page sources, and existing styles.
- [ ] Identify the exact source and rendered paths for the landing page and all 24 current entries. Record them in an inventory; do not infer paths from URL patterns.
- [ ] Inspect the published/rendered pages in French and English, including the known formula, spacing, responsive-layout, and navigation defects.
- [ ] Classify each existing page as: reusable source material, canonical lesson content that should remain in the main curriculum, obsolete duplicate, or content needing source verification.
- [ ] Decide how the prototype is labelled and reached during transition. Avoid presenting the old pages as the new calendar.
- [ ] Record the existing Quarto conventions and identify the simplest native Markdown/Quarto article pattern compatible with the project.

**Deliverable:** a concise inventory and migration map, with no mass content rewrite.

### Phase B — article template and rendering proof

- [ ] Implement one minimal article template using native Quarto/Markdown and standard MathJax delimiters.
- [ ] Keep the layout restrained: readable article width, existing typography and forest-green palette, compact metadata, clear headings, captions, sources, challenge/solution, and optional further reading.
- [ ] Avoid custom nested HTML/CSS wrappers and bespoke layout systems unless a demonstrated rendering requirement justifies them.
- [ ] Validate the template with representative content containing equations, lists, a figure with caption/alt text, a table or its mobile-friendly alternative, and a solution disclosure.
- [ ] Render FR and EN; inspect desktop and mobile widths; verify keyboard navigation, focus visibility, contrast, link destinations, and overflow.
- [ ] Capture review screenshots and record defects and fixes.

**Deliverable:** one reusable article pattern whose rendered output—not just source or CI status—has passed review.

### Phase C — Pilot A: Day 06, sinusoidal position encodings and Fourier ideas

This is the first article to write. It tests whether a mathematical story can be self-contained without turning into another Transformer lesson.

- [ ] Create a source dossier for the pilot. Start with the original *Attention Is All You Need* paper and verify the exact positional-encoding equations and the authors' stated motivation.
- [ ] Explain the connection to multiple sinusoidal frequencies and relative phase in accessible terms.
- [ ] Derive the two-dimensional rotation identity for a fixed positional offset, defining every symbol and stating the assumptions.
- [ ] Include one small numerical or geometric worked example that a reader can follow without implementing a Transformer.
- [ ] Include a challenge and worked solution.
- [ ] Explain the limits: distinguish the authors' motivation/hypothesis about relative positions and extrapolation from a general guarantee; do not imply that sinusoidal encodings solve every length-generalization problem.
- [ ] Make the story useful even if the reader has never opened the canonical positional-encoding lesson.
- [ ] Add at most one optional link to the canonical lesson, after the story is complete.
- [ ] Produce FR and EN versions with equivalent mathematical content and terminology.
- [ ] Run scientific review, independent novice review, and the complete visual/accessibility checks.

**Pilot A acceptance:** all criteria in section 7 of the editorial redesign document pass. If the angle duplicates the canonical lesson, change the angle or replace the pilot; do not merely shorten the canonical explanation.

### Phase D — Pilots B and C

Only start these after the template has been validated and Pilot A has exposed any structural problems.

- [ ] **Pilot B / Day 17 — Cross-entropy as a code length:** build the story around coding regret and the cost of using a mismatched probability model. Include a derivation, hand-worked example, challenge, limits of the coding analogy, and primary/authoritative sources.
- [ ] **Pilot C / Day 23 — Retrieval as external memory:** build a concrete retrieval example that shows what is stored in parameters versus retrieved from an external collection. Distinguish retrieval, grounding, and generation; discuss failure modes and evaluation. Do not turn this into a generic RAG implementation tutorial.
- [ ] For each pilot, complete FR/EN parity, scientific/source review, novice review, and rendered visual QA.
- [ ] Compare the three pilots for actual reading time, distinctness from canonical lessons, usefulness, and template suitability.

**Decision gate:** decide whether the format and editorial promise work across all three pilots before committing to the full collection.

### Phase E — collection architecture and landing page

- [ ] Only after the pilots pass, design a new story manifest. It should describe story metadata, language variants, themes, sources, and optional canonical links.
- [ ] Do not create a parallel concept ontology, prerequisite graph, or second guided curriculum.
- [ ] Rework the calendar landing page as a collection of thematic shelves. The shelves are browsing groupings, not a sequence or prerequisite structure.
- [ ] Make independence explicit: any day can be read first; previous/next links are browsing aids only.
- [ ] Keep the calendar distinct from the main LLM Lab learning path and from the dedicated exercise area.
- [ ] Decide migration/reuse for old pages only after the inventory; preserve useful sources and unique content, but do not carry duplicate summaries forward automatically.
- [ ] Verify that FR/EN switching and all day links work.

### Phase F — controlled expansion and release

- [ ] Expand in small batches, not all 24 at once.
- [ ] For every story, require a source dossier, mathematical/scientific review, distinct editorial angle, worked example, challenge with solution, FR/EN parity, and rendered visual QA.
- [ ] Re-check the collection's balance across mathematics, statistics, information theory, numerical methods, optimization, and LLM systems.
- [ ] Treat the 24-title slate as a proposal: replace weak or duplicative topics rather than forcing them into the calendar.
- [ ] Publish only entries that have passed the acceptance criteria.
- [ ] Keep a short release checklist and record unresolved issues explicitly.

## 3. Cross-cutting quality gates

A story is not ready merely because it renders or the CI passes.

| Dimension | Required evidence |
|---|---|
| Independence | Understandable without prerequisite days or canonical lessons |
| Editorial distinctness | Answers a different question from the corresponding main-path lesson |
| Scientific quality | Equations, assumptions, terminology, and claims checked |
| Sources | Primary/authoritative references for central claims; provenance/licence notes for reused visuals |
| Pedagogy | Narrative hook, one central question, worked example, limitation/counterexample, challenge and solution |
| Timing | Approximately 10 minutes, checked with a reader rather than estimated from word count alone |
| Language parity | FR and EN carry the same ideas, equations, caveats, and examples |
| Rendering | Actual Quarto output inspected on desktop and mobile |
| Accessibility | Semantic structure, keyboard operation, visible focus, contrast, alt text, no horizontal overflow |
| Navigation | Links resolve; previous/next are not presented as prerequisites |

For empirical topics (for example double descent and scaling laws), explicitly distinguish mathematical results, observations on particular datasets/models, hypotheses, and open questions.

## 4. Explicitly deferred

Do not do these before the relevant decision gate:

- Rewrite all 24 pages in one batch.
- Create a new manifest or generator before the three pilots establish the necessary metadata.
- Build custom interactive widgets or bespoke diagrams for every article.
- Add prerequisite edges between days.
- Change the main LLM Lab curriculum to accommodate the calendar.
- Delete the old prototype pages before their content has been inventoried and the replacement experience is ready.
- Treat the proposed titles as immutable.

## 5. Suggested next session

Start with **Phase A**, not with drafting all 24 stories:

1. Inspect the merged state of the calendar-related files on `main`.
2. Inventory the actual Quarto sources and rendered routes for the landing page and current day pages.
3. Inspect the current published FR/EN experience and record concrete defects with paths/screenshots.
4. Identify the smallest implementation path for a native Quarto article template.
5. Then implement the template and write **Day 06** as the first full pilot.

If the current session cannot inspect the rendered site or run Quarto, record that limitation and leave visual acceptance pending. Do not claim that a page has passed visual review based only on source inspection or CI.

## 6. Session completion log

Append a dated entry here at the end of each substantial work session:

- **Date:**
- **Branch / PR:**
- **Files changed:**
- **Work completed:**
- **Validation performed and results:**
- **Open defects / decisions:**
- **Exact next action:**

This log should record outcomes, not merely activity.
