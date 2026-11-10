---
name: understand-path-audit
description: >
  Audit and improve the LLM Lab Theory / Understand learning experience from the
  perspective of a real reader. Use when asked to review the learning path, check
  whether pages flow naturally, harmonize page structure or style, assess
  readability, inspect a sequence or group of pages, or verify that the conceptual
  course is coherent and pleasant to read. Distinct from build-path-audit: this
  skill evaluates conceptual understanding and reader experience, not implementation
  dependency order or code correctness.
---

# Understand Path Audit

## Mission

Act as a critical reader moving through LLM Lab's **Theory / Understand** route. Determine whether a learner can form, refine, and retain a correct mental model of how an LLM works, with a progression that feels coherent, readable, and intentional.

This is an evidence-based editorial and pedagogical audit, not a generic proofreading pass, a link checker, or a demand to make every page identical.

The output must answer:

1. Can a reader understand why this page appears here?
2. Does it build on what has already been established without assuming unexplained knowledge?
3. Does it prepare the reader for what follows?
4. Is the explanation scientifically correct and at the right depth?
5. Does the rendered experience feel consistent and easy to navigate?
6. Are the page's structure and visual choices aligned with its teaching purpose?

## Canonical project contracts

Read the relevant current versions before auditing; do not reproduce their rules as a competing system:

- `docs/learning-path.md`: authoritative distinction and curriculum for Theory / Understand and Build.
- `data/guided-route.yml`: canonical eight-stage Understand route and its bilingual stage/page assignments.
- `docs/understand-path-overview.md`: concise reader-facing route overview, if present.
- `docs/content-section-mapping.md`: page ownership, destination boundaries, cross-page content ownership.
- `docs/information-architecture.md`: canonical data ownership and relationship semantics.
- `docs/page-metadata-schema.md`: page IDs, tags, language parity and navigation metadata.
- `docs/page-template-system.md`, `docs/page-template-guide.md`: soft composition targets, not mandatory outlines.
- `docs/design-system.md`: shared visual and interaction rules.
- `docs/reader-experience-and-editorial-method.md`: progressive disclosure, page roles, meaningful links, editorial economy and self-checks.
- `docs/pedagogical-breadcrumb-and-page-navigation-contract.md`: breadcrumb and navigation behavior.
- `docs/roadmap.md` and `docs/project-status.md`: planned versus implemented content.

If a referenced document has moved, locate its current canonical owner. Do not silently invent a replacement contract.

## Non-negotiable architecture

- Theory / Understand and Build are **distinct pathways**. Do not turn Understand into a prerequisite chain for Build, or Build milestones into theory chapters.
- Understand is a conceptual progression, not a rigid linear textbook. Respect the canonical route while allowing meaningful non-linear entry points and optional depth.
- The eight stages in `data/guided-route.yml` are authoritative. Do not add, remove, reorder, or rename stages merely to make a local sequence look neater. Propose a curriculum change separately and justify it with learner evidence.
- Keep page navigation, conceptual hierarchy, semantic concept relations, curriculum prerequisites and implementation dependencies distinct. A suggested next page is not automatically a prerequisite or a parent-child relation.
- Each concept has a canonical explanatory home. A reminder or overview may repeat a small amount of context; do not duplicate the full explanation or worked example without a distinct learning objective.
- A page must remain self-contained for its LLM-specific learning objective. A link cannot replace a definition, assumption or derivation needed to follow the argument.
- Templates are soft targets. Harmonization means a recognizably shared reader experience, not identical headings, length, section count or visual density.
- Preserve substantive information, examples, references, caveats and useful illustrations. Never remove an existing external illustration solely because its licence is unknown; record the unresolved asset in `docs/visual-assets-register.md` and escalate without hiding or replacing it.
- Never present planned pages, exercises, code or experiments as available evidence.

## When to run

Choose an audit scope from the user's request:

- **Whole route:** all eight canonical stages and their core pages.
- **Stage / topic:** one stage, its core pages and immediately relevant context.
- **Page group:** an explicitly supplied group, a navigation-neighbour group (for example three consecutive pages), or a pedagogically meaningful group (for example five related pages).
- **Rendered experience:** visual, responsive, keyboard, navigation and readability review of the rendered pages.

For a group audit, inspect the pages before and after the group where needed to understand entry and exit transitions. A group is not judged in isolation if its context determines whether the sequence works.

### Default unit: a three-page continuity window

For an audit focused on one page in the Understand route, use a **three-page window** by default:

- **Previous page (incoming context):** establishes the learner's expected starting knowledge and the question or unresolved tension handed to the current page.
- **Current page (audit target):** must make its own contribution explicit, explain what it needs locally, and avoid re-teaching the previous page's canonical content.
- **Next page (outgoing context):** reveals what the current page needs to prepare, which concepts can safely be deferred, and whether the hand-off is explicit and usable.

The current page is the primary target; its neighbors are context, not automatically equal-scope audit targets. Inspect all three in FR and EN when available. Check both transitions (previous → current and current → next), not just the current page's local quality. Also inspect route metadata and rendered previous/next navigation: conceptual sequence, metadata relations and UI navigation are related evidence, not interchangeable sources of truth.

Use a rolling window when progressing through a route: after auditing A–B–C, the next focused audit is B–C–D. Reuse findings and evidence from the overlap instead of repeating the full audit, but re-check them if the source revision or route changed. This makes each page appear as incoming context, target, then outgoing context and reduces blind spots at hand-offs.

**Route boundaries are asymmetric by design:**
- At the first page, there is no previous page. Audit the entry contract instead: what the route promises, what prior knowledge it assumes, how the reader arrives, and whether the page establishes a clear first question. Include the next page to test the first hand-off.
- At the last page, there is no next page. Audit the exit contract instead: what the route has enabled the learner to explain or do, whether the page closes or signposts the route appropriately, and whether it points to a meaningful continuation without implying a nonexistent required step. Include the previous page to test the final hand-off.
- If route metadata has no previous/next neighbor, do not invent one from filename order. Use the canonical route and explain the boundary or branching structure.

For a user-requested group of more than one target page, expand the window to include one immediate predecessor and one immediate successor where they exist. State clearly which pages are targets and which are context. For a whole-route audit, every page is in scope and the first/last-page boundary rules apply.

## Procedure

### 1. Establish the actual route and scope

1. Read the canonical route data and curriculum narrative.
2. Resolve stable page IDs to the actual French and English Quarto sources and published pages.
3. Identify each page's role, destination, level, topic, status, canonical concept ownership and route position from the metadata—not from its filename alone.
4. Build a compact route table: preceding learner knowledge, current page contribution, next learner question, essential links, optional links, and status.
5. Note discrepancies between route data, page metadata, navigation and rendered output. Do not fix one representation by editing a generated projection.

### 2. Simulate the learner's reading

Read each page in route order, not just its headings or metadata. For each page, record:

- **Entry state:** what a reader can reasonably know at this point.
- **Learner question:** the concrete question that motivates this page.
- **Core answer:** the new mental model or distinction it establishes.
- **Prerequisite load:** terms, equations, shapes, conventions or mechanisms used before explanation.
- **Cognitive work:** what the reader must infer, calculate, compare or remember.
- **Exit state:** what the reader can now explain or predict.
- **Next question:** why the next page is a sensible continuation.
- **Friction:** ambiguity, repetition, abrupt depth shift, excessive density, missing bridge, broken expectation or navigation dead end.

Do not assume that a link was read. The page must provide enough local context for its main argument.

### 3. Audit sequence and transitions

Evaluate the route as a chain of justified conceptual steps:

- Is the overall progression from system-level orientation to input, representations, Transformer computation, prediction, inference, scoring and learning understandable?
- Is the early generation overview clearly framed as a preview with fixed parameters, rather than implying that every internal detail has already been taught?
- Are initial embeddings distinguished from contextualized hidden states?
- Are Q/K/V projections placed inside Transformer-block computation, not after final contextual representations?
- Are logits, softmax probabilities, observed-target scoring, loss and parameter updates distinguished correctly?
- Are prefill, iterative decoding and autoregressive feedback introduced at the point where they resolve a real learner question?
- Is teacher forcing explained as use of observed prefixes/targets in training, without turning corpus preparation or batch construction into prerequisites for conceptual understanding?
- Are evaluation and held-out test concepts introduced without confusing validation, test and training roles?
- Are optional mathematics, history, architecture variants and implementation detail discoverable without blocking the core explanation?

These are checks against the project's canonical scientific model, not a license to force every listed term into every page.

For every adjacent pair, write the transition in one sentence: **"After page A, the learner can ask question B; page B answers it by adding C."** If this sentence cannot be written precisely, investigate the transition.

### 4. Audit page-level pedagogy and readability

For each page, assess:

- The first screen establishes a specific question, relevance to LLMs and a useful mental model.
- Intuition is distinguishable from definitions, mathematical claims and empirical observations.
- Terms, symbols, tensor shapes, axes, masks, dimensions and assumptions are defined before use.
- Equations are motivated and interpreted; notation is stable across neighbouring pages.
- Examples are small enough to follow and sufficiently explicit to verify.
- Figures answer a concrete question, have captions and useful alt text, and agree with the prose and equations.
- Limitations and caveats that change the conclusion remain visible.
- Optional detail is progressively disclosed; the core mechanism is not buried in nested callouts.
- Self-checks test stated outcomes with increasing reasoning demand where appropriate; answers explain reasoning.
- References support the claims and are accessible to the public reader.
- The page avoids generic meta-discourse, repeated navigation dumps and redundant "continue learning" endings.
- The language is precise and readable in both French and English, without unnecessary jargon or unexplained acronyms.

Do not reward shorter pages by default. Optimize for comprehension and information density, not word count.

### 5. Audit harmonization across the group

Compare pages side by side for consistency in:

- Title conventions and opening orientation.
- Definition / intuition / mechanism / mathematics / example balance, as appropriate to each page role.
- Notation, symbol names, tensor shape conventions and terminology.
- Heading hierarchy and section granularity.
- Figure sizing, captions, alt text, callout semantics and disclosure behavior.
- Learning outcomes and self-check visual patterns.
- References and source attribution.
- Contextual links, breadcrumbs, previous/next behavior and language switch.
- French/English structural and substantive parity.

Classify differences as:
1. **Intentional and justified** by the learner question or page type.
2. **Acceptable variation** with no reader cost.
3. **Inconsistency with reader cost** that should be harmonized.

Never standardize away a useful page-specific explanatory form just to make outlines match.

### 6. Verify the actual reader experience

Use the strongest available evidence and label it precisely:

- Source inspection: establishes authored content and metadata only.
- Generator / validator / unit tests: establish the contracts they explicitly test.
- Quarto render: establishes that the site can be generated, not that it is pleasant or correct in a browser.
- Browser inspection: required for claims about rendered hierarchy, responsive layout, navigation, visual rhythm, focus, keyboard and touch interaction.
- Learner observation or task-based testing: required for claims about actual comprehension or usability.

When browser access is available, inspect at least one representative page per distinct pattern and every page with a suspected rendering issue. Check desktop and narrow/mobile widths, keyboard navigation, visible focus, links, disclosures, figures, equations and language switching. For a full-route audit, sample every stage's entry page and all pages with high-risk interactions; inspect the full set where practical.

If browser evidence is unavailable, say so and produce a source-level audit only. Never claim to have visually reviewed the site from Markdown or Quarto source.

### 7. Prioritize findings and decide what to change

For each finding, record:

- Page IDs and FR/EN paths.
- Evidence (specific heading, passage, transition, metadata relation, figure, rendering behavior or test).
- Reader impact and likely misconception/friction.
- Severity: **P0** scientific/navigation blocker; **P1** major comprehension or route break; **P2** meaningful consistency/readability improvement; **P3** polish.
- Proposed action and canonical owner.
- Preservation risk: information, source, figure, exercise, code or metadata that must survive.
- Validation required and whether it has actually run.

Prefer the smallest coherent change that resolves the reader problem. Reuse existing canonical pages and shared design components. Do not add a new page, taxonomy, relation type, template, workflow or validation script unless a concrete gap cannot be handled by existing structures.

When editing is requested, work in small coherent groups. Preserve content before moving it; update links and bilingual counterparts; update only canonical metadata sources; regenerate generated projections with their documented tools.

### 8. Re-read as a reader

After changes, repeat the learner simulation across the affected group from its entry point to its exit point. Verify that the revision improved the transition and did not create a new gap, duplicate explanation or orphaned page.

## Expected output

Use this structure; omit empty sections rather than padding the report.

1. **Scope and evidence level** — route/stage/group, pages and language versions inspected; source, test, render, browser and learner evidence distinguished.
2. **Reader journey** — concise page-by-page table with learner question, new understanding, entry/exit state and transition.
3. **Findings** — prioritized, evidence-linked issues with reader impact.
4. **Harmonization matrix** — shared patterns, justified differences and inconsistencies with reader cost.
5. **Recommended changes** — smallest coherent set, canonical files to edit, preservation notes.
6. **Validation** — exact commands/tests/render/browser checks run and results; unavailable checks stated explicitly.
7. **Residual risks and next audit boundary** — only concrete unresolved items.

Do not output a generic score without evidence. A compact verdict may be **coherent**, **coherent with friction**, or **not yet coherent**, with the reasons stated.

## Completion criteria

An audit is complete when:

- The requested scope and its surrounding transitions have been read.
- Every finding is tied to concrete evidence and a learner consequence.
- Scientific correctness and pedagogical sequencing have been checked separately.
- Differences between page roles are distinguished from accidental inconsistency.
- French/English parity and navigation are considered.
- The rendered-evidence level is honestly reported.
- No information has been silently discarded.
- The report proposes a bounded, actionable improvement sequence.
- If changes were made, the affected group has been re-read and relevant checks rerun.
