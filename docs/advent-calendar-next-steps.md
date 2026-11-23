# Advent calendar — remaining work and session handoff

**Last updated:** 2026-11-23  
**Status:** Day 01 (Zipf's law) has bilingual drafts, an original SVG and a source dossier in PR #1565. The Quarto preview and FR/EN desktop/mobile browser review passed (run #45219428295); the pages remain status:planned and outside the public render list. Scientific and technical review is complete; novice review and editorial acceptance remain pending. Production proceeds strictly from Day 01 to Day 02, then Day 03, etc.  
**Parent decision:** PR [#1551](https://github.com/JM-Brun/llm-lab/pull/1551) — merged into `main`.

This document is an operational handoff for future sessions. It records what is complete, what remains, the order of work, and the conditions for considering the calendar ready. The editorial rationale and proposed 24-story slate remain in [advent-calendar-editorial-redesign.md](advent-calendar-editorial-redesign.md); this file should not duplicate that specification.

## 1. Current state — verified

### Completed

- [x] The calendar's editorial direction was changed from a compressed second learning path to a collection of 24 independent scientific stories.
- [x] The new editorial contract, anti-duplication rules, proposed 24-story slate, source standards, rendering requirements, and pilot acceptance gates were documented.
- [x] The former curriculum-summary design was marked historical/superseded.
- [x] The former 24-day manifest was marked superseded and retained as historical material.
- [x] Source-level inventory completed: the Quarto render list contains the landing page and only days 01–03 in each language; it does not contain 24 day-story pages.
- [x] The current landing page has 24 cards: days 01–03 link to the old guided mini-lessons; days 04–24 link to canonical lessons and exercise pages rather than independent calendar stories.
- [x] The old landing page uses the custom advent-calendar CSS and the former four-movement curriculum-summary design; it is explicitly labelled as a historical prototype in PR #1560.
- [x] The canonical positional-encoding lesson already contains the sinusoidal formula and fixed-offset rotation derivation. The Day 06 story is refocused on Fourier feature mappings and spectral bias to avoid duplication.
- [x] PR [#1551](https://github.com/JM-Brun/llm-lab/pull/1551) was merged on 2026-11-23.
- [x] Day 01 rendered successfully in a PR-only Quarto preview; FR/EN desktop and mobile browser review passed. MathJax, local links, image loading, keyboard focus and desktop Axe checks were verified.

### Not completed

- [ ] An earlier Day 06 FR/EN draft exists in PR #1560 but remains parked and unaccepted; it will be reviewed when chronological production reaches Day 06. No later-day story is an active target.
- [ ] A native Quarto story-template draft exists in PR #1560. Day 01 validates its standard article layout; broader template reuse remains to be assessed as later days are produced.
- [x] Day 01 source-level, Quarto-render, link, FR/EN desktop/mobile and accessibility checks are complete.
- [ ] No new story-oriented manifest has been approved or created.
- [ ] The 24 existing entries have not been migrated; they remain prototype/historical material.
- [ ] No novice-reader review has been performed.
- [x] Day 01 has FR/EN desktop/mobile visual evidence; novice-reader acceptance is still pending.

**Important:** merging #1551 means the editorial decision is recorded. It does not mean the calendar implementation is complete or ready to publish.

## 2. Execution order

Work in the following order. Do not start all 24 articles in parallel.

### Phase A — inventory and transition audit

- [x] Inspect the current Quarto project configuration, navigation, calendar landing page, day-page sources, and existing styles.
- [x] Identify the exact source and rendered paths: the landing page exists in FR/EN; only days 01–03 have dedicated rendered pages in each language; days 04–24 are cards linking to canonical lesson/exercise pages, not calendar story pages.
- [ ] Inspect the published/rendered pages in French and English, including formula, spacing, responsive-layout and navigation behavior. Source inspection is complete; visual inspection and screenshots remain pending.
- [x] Classify existing content: days 01–03 are the old prototype mini-lessons; days 04–24 are canonical curriculum pointers; the old manifest is superseded historical input; canonical lessons remain in the main curriculum.
- [x] Decide the transition label: the old landing page is explicitly marked as an archived prototype in PR #1560. Preserve its content until the replacement experience is accepted.
- [x] Record the native Quarto article pattern in the reusable story template draft in PR #1560. Visual validation remains pending.

**Deliverable:** source-level inventory and migration boundary completed; no mass rewrite or new story manifest.
### Phase B — article template and rendering proof

- [x] Implement a reusable story template using native Quarto/Markdown and standard MathJax delimiters in docs/templates/advent-story-template.qmd.
- [x] Keep the new article pages on the site's standard typography and layout; use clear headings, a worked example, a figure with alternative text, sources, a challenge/solution and optional further reading.
- [x] Avoid custom nested HTML/CSS wrappers and bespoke layout systems.
- [x] Validate the source structure with representative content containing equations, lists, a figure, a table and a solution disclosure.
- [x] Rendered Day 01 in French and English; inspected desktop (1440 px) and mobile (390 px), including formulas, figure, caption, links and overflow.
- [x] Captured browser-review screenshots; fixed the missing figure alt text and added page-aware bilingual language switching.

**Deliverable:** the source template and a bilingual Day 01 rendering proof exist. The PR-only preview passed; novice acceptance remains a separate gate.

### Phase C — Chronological story production (current: Day 01)

The production sequence is Day 01, Day 02, Day 03, and so on. The previously drafted Day 06 story is retained as an unaccepted draft; it is not the active production target and must not cause work to skip ahead.

For each day:
- [x] Confirm the day's distinct editorial question and boundary against the main curriculum.
- [x] Prepare a source dossier and claim-to-source ledger before finalizing the story.
- [x] Draft French and English versions with equivalent reasoning, examples, equations and caveats.
- [x] Include a worked example, one limitation or counterexample, and a short challenge with a worked solution.
- [x] Check mathematical derivations and numerical values independently.
- [x] Render both language versions in Quarto and inspect desktop/mobile output.
- [x] Verify figure provenance, alt text, captions, internal/external links and keyboard accessibility.
- [ ] Obtain a novice read-through and record observed reading time and points of confusion.
- [x] Record defects and fixes in the handoff document.
- [ ] Do not start the next numbered day until the current day passes its acceptance gates.

**Current Day 01:** Zipf's rank-frequency relation and lexical frequency imbalance. PR #1565 contains the FR/EN drafts, source dossier, original SVG, bilingual language mapping and generic new-page browser-review support. The PR is open and ready for review; the story pages remain status:planned and outside the render list. Technical gates passed; novice review remains pending.

### Phase D — Next days after acceptance

After Day 01 is accepted, continue with Day 02, then Day 03, following the approved story slate. Do not jump to the former non-adjacent pilots (Days 17 and 23) as a production shortcut. Reuse their proposed angles only when their calendar days are reached and the source review supports them.

### Phase E — collection architecture and landing page

- [ ] Only after a small chronological set of stories has passed acceptance and its metadata needs are understood, design a new story manifest. It should describe story metadata, language variants, themes, sources, and optional canonical links.
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
- Create a new manifest or generator before the first chronological stories establish the necessary metadata.
- Build custom interactive widgets or bespoke diagrams for every article.
- Add prerequisite edges between days.
- Change the main LLM Lab curriculum to accommodate the calendar.
- Delete the old prototype pages before their content has been inventoried and the replacement experience is ready.
- Treat the proposed titles as immutable.

## 5. Suggested next session

Continue with **Day 01 only**:

1. Obtain a novice read-through of the French or English story; record actual reading time and points of confusion.
2. Ask the reader to explain the rank-frequency relation and solve the challenge without assistance.
3. Review whether the LLM-training implication is clear and appropriately qualified.
4. Revise from that feedback and obtain explicit editorial acceptance.
5. Draft Day 02 only after Day 01 is accepted.

The Quarto preview, source metadata, bilingual mapping, links, MathJax, desktop/mobile layout and desktop Axe checks have already passed. Do not repeat those checks unless the relevant source changes.

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

## 7. Session completion log

- **Date:** 2026-11-23
- **Branch / PR:** calendar/day06-independent-story-pilot — PR #1560
- **Files changed:** bilingual calendar landing pages, Quarto render list, bilingual Day 06 story drafts, language-switch mapping, reusable story template, Day 06 source dossier, original frequency-scale SVG, editorial redesign and this handoff.
- **Work completed:** verified the old 24-card prototype structure; marked it as an archive; drafted a distinct Day 06 story focused on Fourier features and spectral bias rather than repeating the canonical positional-encoding derivation.
- **Validation performed and results:** source paths and bilingual canonical lesson content inspected; primary references checked. No Quarto render of the Day 06 draft, browser screenshot, numerical-table verification or novice review has yet been performed. The first CI run also exposed the explicit language-switch mapping requirement for planned source pages; the bilingual mapping entry is now included.
- **Open defects / decisions:** PR checks and visual rendering; verify the page metadata and the PR-only published preview status; run FR/EN desktop/mobile and accessibility review; verify the numerical table and SVG in the rendered pages; obtain novice feedback.
- **Exact next action:** inspect the PR render and metadata checks, revise the Day 06 draft, then decide whether to proceed with Days 17 and 23. Do not create the story manifest yet.

## 8. Session completion log

- **Date:** 2026-11-23
- **Branch / PR:** `calendar/day06-spectral-bias-revision` — PR #1562 merged; follow-up math-render correction in PR #1563
- **Files changed:** French and English Day 06 drafts; Day 06 source dossier; this handoff.
- **Work completed:** strengthened the distinction between expressivity and learning dynamics; added a qualified account of spectral bias grounded in Rahaman et al. (2019); clarified the frequency-bandwidth trade-off from Tancik et al. (2020); replaced the recall-style challenge with a two-frequency transfer example; defined frequency units and the ReLU scope; repaired FR math delimiters and dossier display equations; aligned the source dossier with the revised claims.
- **Validation performed and results:** primary-source abstracts and paper descriptions checked; numerical examples and the linear-readout argument checked analytically; QMD math delimiters and dossier display blocks inspected at source level. No Quarto render, screenshot review, accessibility audit or novice review was performed in this session.
- **Open defects / decisions:** the draft still needs word-count/timing validation with readers, rendered FR/EN desktop/mobile review, SVG verification, and scientific/editorial acceptance. It remains `status:planned` and outside the render list.
- **Exact next action:** run the repository's Quarto and metadata checks on the revision branch; if they pass, inspect rendered FR/EN previews at desktop and mobile widths before deciding whether to publish Pilot A. Do not start Pilots B and C until this gate passes.
 
## 9. Chronological production decision — Day 01

- **Date:** 2026-11-23
- **Branch:** `calendar/day01-zipfs-law`
- **Files added:** French and English Day 01 story drafts; Day 01 source dossier; original synthetic rank-frequency SVG.
- **Editorial subject:** “Why does the word ‘the’ appear everywhere?” / “Pourquoi le mot « de » revient-il si souvent ?”
- **Angle:** Zipf's rank-frequency regularity, long-tailed lexical frequencies, the limits of power-law claims, and a carefully qualified implication for language-model training data.
- **Anti-duplication:** this is a statistical-linguistics story, not a tokenization lesson. It distinguishes lexical word types/tokens from tokenizer tokens and links to canonical pages only as optional further reading.
- **Validation performed:** arithmetic and source claims checked; canonical QMD paths, metadata, relative image path and bilingual page mapping verified. PR-only Quarto render and browser audit run #45219428295 passed: FR/EN pages returned HTTP 200 at desktop (1440 px) and mobile (390 px); MathJax rendered 2/2 expressions on each page; no console/page errors or horizontal overflow; the SVG loaded with its descriptive fig-alt; desktop Axe reported zero violations; local links and the full site render passed.
- **Defects found and fixed during review:** the first browser audit exposed missing figure alternative text (image-alt); added fig-alt. The test suite exposed a missing language-switch mapping; added the FR/EN slug mapping. Added generic browser cases for changed Quarto pages, limited to pages present in project.render.
- **Preview-only configuration:** the two pages were temporarily marked published and added to the PR render list to exercise metadata validation and browser review. They have now been restored to status:planned and removed from the render list; they are not part of the public build.
- **Status:** technical review passed; novice read-through and editorial acceptance remain pending. PR #1565 is open and ready for review, not merged.
- **Production rule:** proceed chronologically by day number. Do not draft Day 02 until Day 01 has passed scientific, editorial, bilingual, rendered-layout, accessibility, and novice-review gates. Chronological production does not imply prerequisite reading; stories remain independently understandable.
- **Next action:** obtain novice feedback and accept Day 01 before beginning Day 02.

## 10. Session completion log

- **Date:** 2026-11-23
- **Branch / PR:** `calendar/day01-zipfs-law` — PR #1565
- **Files changed:** bilingual Day 01 stories, Day 01 source dossier, original Zipf SVG, and this handoff document.
- **Work completed:** corrected page-map domain and canonical relation IDs; distinguished lexical occurrences from tokenizer units; corrected the attribution of *Unzipping Zipf's law* to Sander Lestrade (2017); added Pilgrim and Hills (2021) to qualify the limitations of corpus splitting and residual estimator bias; restricted the synthetic plot to integer occurrence counts; updated the production handoff to make Day 01 the sole active target.
- **Validation performed and results:** reviewed repository metadata rules and controlled domain registry; checked canonical target IDs against configured pages; verified the 2014 and 2017 source attributions and the 2021 estimator caveat against the papers. Quarto and browser workflows were skipped because the PR is still a draft; no rendered preview, screenshots, accessibility audit or novice review has been completed.
- **Open defects / decisions:** rendered preview and page metadata validation remain pending; review the new source note's wording and the SVG in actual page context; obtain novice feedback and acceptance.
- **Exact next action:** validate and accept Day 01 before beginning Day 02.
