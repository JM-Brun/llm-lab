# Advent calendar — remaining work and session handoff

## Current operational snapshot — 2026-11-27 (supersedes earlier status paragraphs)

The 24-story calendar remains **implemented but not collection-validated or learner-validated**. Do not infer acceptance from merged implementation PRs, a published page, or green CI.

### Confirmed changes since the previous snapshot

- [PR #1695](https://github.com/JM-Brun/llm-lab/pull/1695) is merged: the first three stories were redistributed around the 15-minute editorial target. The Day 01 Zipf deep dive, Day 02 quantitative surprisal narrative, and Day 03 tokenizer trade-off narrative now have their intended ownership boundaries; exercises and guided experiments remain in Practice.
- [PR #1703](https://github.com/JM-Brun/llm-lab/pull/1703) is merged: Day 01's title/description and LLM caveats were aligned with its actual scope, all 24 bilingual door titles match the canonical manifest, and Practice ownership is explicit on the landing pages.
- [PR #1709](https://github.com/JM-Brun/llm-lab/pull/1709) is merged: the tokenizer story now distinguishes prompt/KV-cache cost, output-projection cost, and downstream quality; its numerical ratios are explicitly scoped to the constructed example.
- [PR #1663](https://github.com/JM-Brun/llm-lab/pull/1663) is merged: the text → position → contextualized-representation cluster and its synthesis sheets were refined. This is a prerequisite/context change for Day 05, not evidence that Day 05's reuse audit or learner review is complete.
- [PR #1691](https://github.com/JM-Brun/llm-lab/pull/1691) and the Day 01/03 editorial corrections #1692/#1693 are merged. The first-three-days pedagogical model exists; it does not replace the current rendered-page and learner checks.
- The 24 manifest entries have individual tracking issues (#1653 and #1666–#1689). Their ownership is deliberate: collection coherence stays here; page-level scientific and editorial changes stay with the day issues.

### Current page-level acceptance state

- **Day 01 — Zipf:** public FR/EN reading version; not accepted. The non-specialist timed read-through, comprehension evidence, and explicit accept/revise decision are still missing. #1653 also tracks source-by-source provenance follow-up and a decision on whether Heaps/hapax or lexical-diversity measures add value to the existing deep dive.
- **Day 02 — surprisal:** story implemented, but not accepted. Verify the final calculations and distinctions (observed surprisal vs predictive entropy; bits/nats; conditional vs marginal probability; sequence sum vs average), then perform the rendered and novice review in #1666.
- **Day 03 — tokenizer:** the narrative and cost boundaries are implemented, but the reuse/acceptance audit remains open. #1667 still requires current FR/EN desktop/mobile inspection, anchor/link and rights checks, reproducibility of the multilingual comparison protocol, and an independent novice reading focused on why shorter tokenization is not by itself better.
- **Days 04–05:** both remain reuse-audit, not accepted. #1668 must test whether the canonical linearity/embedding page supports the XOR-led story without overclaiming probing or feature use. #1669 must test the same-token/different-context contrast against the revised contextualized-representation page, distinguishing contextual change from complete disambiguation and probing from causal evidence.
- **Day 06:** the bilingual source draft/template/dossier exist, but the manifest remains in-progress; it is not an accepted or published story. The current issue #1671 still requires a complete bilingual draft, worked frequency/phase example, explicit distinction from learned/relative/RoPE methods, and scientific/render/learner validation.
- **Days 07–08:** reuse audits remain open. Day 07 must preserve the limits of the Q/K/V retrieval analogy; Day 08 must audit the variance derivation's assumptions rather than generalize from a Gaussian simulation.
- **Days 09–24:** each has an individual P2 issue and an explicit reuse/create decision. A manifest value create is a proposal, not proof that a page exists or is validated. Do not mass-create these pages. In particular, Day 09 (#1674) and Day 21 (#1686) are candidates for the deliberately varied content pilots, but require distinct-scope/source decisions and controlled examples before implementation.

### Execution order for the next session

1. Finish the **first-five cross-day quality review** in #1664 using the ten shared criteria, with a per-story pass / revise / not-applicable record and exact page evidence. Do not duplicate page-level edits already owned by #1653 and #1666–#1669.
2. Close the highest-value page-level evidence gaps in chronological order: Day 01 non-specialist read; Day 02 final scientific/render review; Day 03 reproducibility and mobile/novice review; then the explicit reuse decisions for Days 04–05.
3. Continue the varied scientific pilots only after the relevant page owner has established a distinct learner outcome and source basis. Day 03 is part of the existing tokenizer story; Day 09 and Day 21 remain candidates, not approved parallel production tracks.
4. Complete the collection crosswalk against canonical concepts and computational nodes. Preserve the three distinct uses of the conditional distribution (generation, observed-target scoring/evaluation, training); Q/K/V remains inside Transformer blocks. Do not infer prerequisites from calendar order.
5. Inspect the published archive/navigation, FR/EN responsive output, keyboard/screen-reader behavior, reduced motion, colour contrast, figure alternatives, source provenance and evergreen access. Record automated checks, manual rendered review, scientific review and learner evidence separately.

### Release gate

The collection cannot be called learner-validated or release-ready until (a) all 24 manifest references resolve to the intended canonical resources or an explicitly approved new story, (b) the first-five shared editorial bar and varied pilots have evidence, (c) the scientific crosswalk and boundaries are checked, (d) rendered accessibility/navigation is reviewed, and (e) actual novice observations are recorded for the stories claimed as learner-tested. One reader's evidence must not be generalized to all 24 stories.


> **Mise à jour de migration — 24 novembre 2026.** La PR [#1574](https://github.com/JM-Brun/llm-lab/pull/1574) est fusionnée et le rendu complet ainsi que le déploiement GitHub Pages post-fusion ont réussi. Les pages principales FR/EN pointent maintenant vers le calendrier scientifique. La PR de nettoyage remplace les huit anciennes pages du prototype par des redirections vers la nouvelle collection, retire leurs mini-leçons du graphe pédagogique et supprime le CSS spécifique devenu inutilisé. Les histoires indépendantes `advent-calendar-story-day-01` et `day-06` sont conservées. Cette mise à jour supersède les consignes de transition antérieures qui demandaient d'attendre le déploiement.

**Last updated:** 2026-11-26  
**Status:** PRs #1593 (Day 01 public reading release), #1594 (Zipf practice pages), #1596 (Day 02 preview) and #1695 (15-minute redistribution of the first three stories) are merged. Day 01 is public as a reading version, but its editorial acceptance remains pending a real non-specialist read-through. Day 02 remains a public preview, not an accepted story. PR #1703 is the current follow-up for Day 01 wording and bilingual calendar consistency. Production order is chronological; reader navigation remains non-linear.  
**Parent decision:** PR [#1551](https://github.com/JM-Brun/llm-lab/pull/1551) — merged into `main`.

This document is an operational handoff for future sessions. It records what is complete, what remains, the order of work, and the conditions for considering the calendar ready. The editorial rationale and approved 24-story slate remain in [advent-calendar-editorial-redesign.md](advent-calendar-editorial-redesign.md); this file should not duplicate that specification.

## Current snapshot — 2026-11-26

- **Day 01:** published in FR/EN for reading; the post-redistribution story targets about 15 minutes. The corpus counts and worked rank–frequency example remain intact. Its non-specialist review, observed reading time, comprehension record and explicit accept/revise decision are still missing.
- **Day 02:** the surprisal story is accessible as a preview. Its scientific and pedagogical acceptance remains pending; do not present the preview as a finished calendar story.
- **Day 03:** the tokenizer story has been redistributed around the vocabulary-size / sequence-length / cost trade-off. Its reuse audit and acceptance remain separate work.
- **PR #1695:** merged the first-three-story redistribution, the two companion deep dives, Practice ownership and related bilingual metadata/navigation updates.
- **PR #1703:** follow-up wording and collection-consistency pass. It aligns Day 01 metadata and LLM implications, clarifies that guided practice lives on dedicated pages, and synchronizes all 24 bilingual door titles with the canonical manifest. Its CI and rendered-page audit must pass before merge.

**Next actions:** validate PR #1703; then obtain a real non-specialist Day 01 read-through and record time, comprehension evidence and confusion points. Revise and retest only where observations warrant it. Do not treat source review, author self-review or CI as a substitute for learner validation.



## 2026-11-26 — first-three-story duration and redistribution pass

The editorial contract now targets **about 15 minutes per story**, with 10–20 minutes accepted only when the subject justifies the deviation. A story below 10 minutes triggers a structural diagnosis, not an automatic instruction to add words: determine whether the topic is too narrow or weak for an independent story, or whether the treatment omits reasoning steps, worked examples, explanatory visuals, or a meaningful conclusion. Restructure and deepen where the topic has real potential; combine closely related ideas only when they form one coherent investigation. Replace or fold in a topic that cannot sustain a substantive story. Any sub-10-minute exception requires explicit editorial justification. For stories above 20 minutes, redistribute secondary material. Keep exercises on dedicated practice pages and prefer redistribution to deletion, preserving citations, figures, anchors, and navigation.

A follow-up implementation is being prepared in the [PR #1695](https://github.com/JM-Brun/llm-lab/pull/1695). It redistributes the first three stories in FR/EN:

- **Day 01 — Zipf:** the main story is approximately 2,600 words in French (about 15 minutes including figures/tables). Detailed Zipf–Mandelbrot material, cross-linguistic data, history, and extended applications move to zipf-law-deep-dive.qmd; exercises remain in the existing Zipf exercise page.
- **Day 02 — Surprisal:** adds a context-sensitive worked example, the logits → softmax → probability → surprisal chain, sequence sum/average distinctions, an explicit entropy calculation, and guided experiments. The existing information-theory experiment remains the practical companion.
- **Day 03 — Tokenizer:** keeps the core vocabulary/sequence/cost decision in the story and adds a worked cost comparison. Research tables, multilingual metrics, and external resources move to tokenizer-multilingual-evaluation.qmd. Detailed WordPiece/Unigram mechanisms are integrated into the existing tokenization-strategies.qmd rather than duplicated.

The concept registry, computational graph, guided-route optional pages, page maps, calendar manifest, landing pages, and novice-review protocol have been updated to reflect the new ownership and 15-minute target.

**Validation status (2026-11-26):**
- The branch has been merged with the latest `main` history (#1696 and #1697); it is now up to date and GitHub reports the PR as mergeable.
- Python quality, page metadata, concept registry, and domain checks pass. The complete suite passed **834 tests, with 1 skipped and 1 warning** in [run #45817756001](https://github.com/JM-Brun/llm-lab/actions/runs/45817756001). The warning lists existing core lessons outside their 10–15 minute target; none of the three calendar stories is listed.
- The full Quarto render, interactive learning-map checks, computational-graph export, timeline parity, and local-link audit passed. The FR/EN browser audit reviewed 138 cases with no blocking failures in [run #45817755969](https://github.com/JM-Brun/llm-lab/actions/runs/45817755969). It nevertheless exposed one critical Axe `image-alt` issue on the surprisal distribution figure in both languages: Quarto had dropped the Markdown alt text from the rendered `img`. The source now sets `fig-alt` explicitly; the latest Quarto audit must confirm the rendered HTML has the alternative text.
- A scientific review of the tokenizer cost example identified a missing term: the output projection's training computation scales as `T × V × d`. The bilingual example now shows the factor `8/3` for the constructed A/B comparison and distinguishes tied parameter storage from the computation that remains necessary. The latest CI and Quarto runs must validate these final edits.
- The generated learning-map data now combines the revised bilingual page records with the latest 125 tokenization concepts and 147 typed relations from `main`; the two new calendar deep dives remain in the page map and navigation.
- No novice-reader timing or comprehension review has yet been performed. The advertised 15-minute durations remain editorial estimates, not observed measurements.
- [PR #1695](https://github.com/JM-Brun/llm-lab/pull/1695) remains open and mergeable. Do not merge until the latest CI and Quarto/browser runs pass and the novice review has an explicit acceptance decision.

The tracked generated fragments are committed. If a later source edit changes page-map metadata or section headings, regenerate the bilingual outputs with `uv run --no-project --with-requirements docs/requirements-history-validation.txt --python 3.12 python site/tools/build_learning_map.py`.
## Historical state snapshot — 2026-11-24 (superseded by the current snapshot above)

### Completed

- [x] The editorial direction, anti-duplication rules, proposed 24-story slate, source standards, rendering requirements and per-day acceptance gates are documented.
- [x] The former curriculum-summary design and manifest are marked historical/superseded.
- [x] The bilingual scientific-calendar landing pages are the current calendar entry points.
- [x] PR [#1565](https://github.com/JM-Brun/llm-lab/pull/1565) merged Day 01's French and English drafts, source dossier, original SVG, novice-review protocol and supporting language-switch/browser-review changes into `main`.
- [x] Day 01's PR-only Quarto preview and FR/EN desktop/mobile browser review passed (run [#45219428295](https://github.com/JM-Brun/llm-lab/actions/runs/45219428295)); at that stage, the pages were `status:planned` and excluded from the public render list.
- [x] PR [#1574](https://github.com/JM-Brun/llm-lab/pull/1574) corrected the bilingual homepage page maps to point to the scientific calendar.
- [x] PR [#1576](https://github.com/JM-Brun/llm-lab/pull/1576) retired the eight legacy prototype routes with redirects to the new calendar, retained no-JavaScript fallback links on old lesson routes, removed obsolete page-map entries and deleted the unused prototype CSS.
- [x] The cleanup PR's secret scan and Python quality/domain checks passed. Its test-suite and Quarto render checks were still running at the last status inspection; verify the completed results before treating the migration as fully validated.
- [x] The old Day 01–03 mini-lessons are no longer the calendar's content model. The new collection is intended to contain independent scientific stories, not a second curriculum sequence.

### Not completed

- [ ] No novice-reader review has been performed for Day 01.
- [ ] No observed reading time, comprehension record or final editorial acceptance has been recorded for Day 01.
- [x] PR #1593 prepares Day 01 for public reading; the release is not live until the PR is merged and deployed. Final editorial acceptance remains pending.
- [ ] Day 02 is not accepted for publication. A preview exists in stacked PR #1596; do not merge or publish it before the Day 01 acceptance gate.
- [ ] The story-oriented manifest and thematic-shelf redesign remain deferred until a small set of accepted stories establishes their actual metadata needs.
- [ ] The parked Day 06 draft remains unaccepted and must not cause the production sequence to skip ahead.

**Current blocker:** Day 01's public-reading release is prepared in PR #1593 but is not live until merge and deployment; editorial acceptance remains pending. A real non-specialist reader must complete [the review protocol](advent-calendar-pilots/day-01-novice-review.md). Record actual reading time, comprehension evidence and points of confusion; revise if needed and make an explicit accept/revise decision. Author self-review, source review and passing CI do not satisfy this gate. Keep the Day 02 preview in PR #1596 unmerged until this decision is recorded.

## 2. Execution order

Work in the following order. Do not start all 24 articles in parallel.

### Phase A — inventory and transition audit

- [x] Inspect the current Quarto project configuration, navigation, calendar landing page, day-page sources, and existing styles.
- [x] Identify the exact source and rendered paths: the landing page exists in FR/EN; only days 01–03 have dedicated rendered pages in each language; days 04–24 are cards linking to canonical lesson/exercise pages, not calendar story pages.
- [x] Inspect the PR-only rendered pages in French and English, including formulas, spacing, responsive layout and navigation. Desktop/mobile screenshots and accessibility review are recorded in the Day 01 source dossier; this was a preview-only render, not publication.
- [x] Classify existing content: days 01–03 are the old prototype mini-lessons; days 04–24 are canonical curriculum pointers; the old manifest is superseded historical input; canonical lessons remain in the main curriculum.
- [x] Decide the transition label: the old landing page is explicitly marked as an archived prototype in PR #1560. Preserve its content until the replacement experience is accepted.
- [x] Record the native Quarto article pattern in the reusable story template draft in PR #1560. Day 01 provides the first bilingual rendering validation of the article pattern.

**Deliverable:** source inventory, migration boundary and Day 01 rendering review completed; no mass rewrite or new story manifest.
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

**Current Day 01:** Zipf's rank-frequency relation and lexical frequency imbalance. PR #1565 merged the FR/EN drafts, source dossier, original SVG, novice-review protocol and bilingual language mapping into `main`. PR #1593 changes both story pages to `status:published`, adds them to the public render list and links them from the calendar landing pages. The release is not live until PR #1593 is merged and deployed. Fresh CI, Quarto and browser checks on the current PR head are required; novice review and editorial acceptance remain pending.

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
| Timing | Approximately 15 minutes, checked with a reader rather than estimated from word count alone |
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
- **Status at the time of this entry:** technical review passed; novice read-through and editorial acceptance remained pending. PR #1565 was subsequently merged; this did not publish the story or waive its novice-review gate.
- **Production rule:** proceed chronologically by day number. Do not draft Day 02 until Day 01 has passed scientific, editorial, bilingual, rendered-layout, accessibility, and novice-review gates. Chronological production does not imply prerequisite reading; stories remain independently understandable.
- **Next action:** obtain novice feedback and accept Day 01 before beginning Day 02.

## 10. Session completion log

- **Date:** 2026-11-23
- **Branch / PR:** `calendar/day01-zipfs-law` — PR #1565
- **Files changed:** bilingual Day 01 stories (including bibliography formatting correction), source dossier, original SVG, novice-reader review protocol, bilingual language-switch mapping, generic browser-review support for newly rendered pages, editorial/handoff documentation.
- **Work completed:** corrected page-map domain and canonical relation IDs; disambiguated lexical occurrences from tokenizer tokens; corrected the 2017 source attribution to Sander Lestrade; added Pilgrim and Hills (2021) on residual estimator bias; constrained the synthetic figure to integer counts; added descriptive figure alt text and local FR/EN links; added the slug to the global language-switch mapping; made the browser audit cover newly added pages only when they are included in Quarto rendering; restored Day 01 to planned status and removed it from the render list after preview.
- **Validation performed and results:** PR-only Quarto render and browser audit run [#45219428295](https://github.com/JM-Brun/llm-lab/actions/runs/45219428295) passed. Both pages returned HTTP 200 at desktop (1440 px) and mobile (390 px); MathJax rendered 2/2 expressions per page; the SVG loaded with its language-specific fig-alt; no horizontal overflow, console errors or page errors; desktop Axe reported zero violations in both languages. Final CI run [#45221807466](https://github.com/JM-Brun/llm-lab/actions/runs/45221807466) passed (812 tests, 1 skipped); Python quality/domain checks passed. Final Quarto run [#45221806910](https://github.com/JM-Brun/llm-lab/actions/runs/45221806910) passed, including full-site rendering, learning-map controls, knowledge-graph export, history timeline parity, local-link checks and browser review. Secret scanning [#45221807289](https://github.com/JM-Brun/llm-lab/actions/runs/45221807289) passed.
- **Open defects / decisions:** the literal escaped newline before the Pilgrim and Hills bibliography entry in both language versions has been corrected; the latest PR preview is running. A novice read-through, actual reading-time observation and final editorial acceptance are still required.
- **Exact next action:** re-run the PR preview after the bibliography correction; then conduct the novice review using [day-01-novice-review.md](advent-calendar-pilots/day-01-novice-review.md), revise if needed, and accept Day 01 before beginning Day 02.


## 11. Session completion log — pedagogical refinement

- **Date:** 2026-11-23
- **Branch / PR:** `calendar/day01-zipfs-law` — PR #1565
- **Files changed:** French and English Day 01 stories; French and English original rank-frequency SVGs; source dossier; novice-reader protocol.
- **Work completed:** added a small fictional count table in each language to make the construction of rank explicit before introducing Zipf's approximation; clarified that rank is corpus- and convention-dependent; updated the novice protocol to test whether a reader can explain why a form has rank 1; localized the French figure itself rather than leaving English axis labels in the French article.
- **Scientific boundary:** the count table is explicitly a constructed illustration, not an empirical corpus and not a fitted Zipf distribution. The separate (f(r)=C/r^\alpha) example remains the idealized model used for the arithmetic and log-log derivation.
- **Validation:** source edits committed; fresh Quarto, CI and secret-scanning checks are required for this new head. The previous browser preview does not validate these changes.
- **Open work:** inspect the new FR/EN render, especially the SVG labels and formula rendering; obtain novice feedback; record actual reading time; decide editorial acceptance.
- **Exact next action:** validate the latest PR head and inspect the bilingual preview before requesting the novice read-through. Do not start Day 02.

## 12. Session completion log — landing-page migration follow-up

- **Date:** 2026-11-24
- **Branch / PR:** `calendar/fix-primary-page-graph` — PR #1574
- **Files changed:** French and English homepage page-map declarations; this handoff.
- **Work completed:** verified that PR #1572 is merged and that the new bilingual `scientific-calendar.qmd` landing pages and navigation entries are present on `main`. Found that both homepage page maps still listed the archived `advent-calendar` as a child alongside `scientific-calendar`; removed the archived calendar from those two child lists in PR #1574. Confirmed that the new Day 01 Zipf story is merged as source material but remains `status:planned` and excluded from the public Quarto render list.
- **Deployment check:** the public search result still exposes the old `/en/advent-calendar.html` page, while direct access to the new `/fr/scientific-calendar.html` and `/en/scientific-calendar.html` could not be verified in this check. Treat the Pages replacement as unconfirmed; do not delete the old landing/day pages or their CSS yet.
- **Cleanup dependency:** the story page `advent-calendar-story-day-01.qmd` uses the shared language-switch mapping and story source assets, but does not import the prototype's custom calendar CSS. The prototype CSS may be removed only after repository-wide reference checks and after all remaining prototype pages are retired.
- **Validation:** source-level page-map replacement checked before committing; PR #1574 requires CI, Quarto rendering and graph checks. No novice-reader test has been performed; the Day 01 protocol explicitly requires a real non-specialist reader and must not be marked complete by author self-review.
- **Open work:** merge #1574 after checks pass; verify the actual GitHub Pages deployment and both language URLs; confirm navigation and redirects; then remove the archived prototype pages/resources in a separate cleanup PR. Obtain novice feedback and record actual reading time before publishing Day 01 or drafting Day 02.
- **Exact next action:** inspect PR #1574 checks; once merged, verify Pages deployment and then prepare a bounded cleanup PR only if the new calendar is live in both languages.


## 13. Session completion log — replacement and retirement of the old prototype

- **Date:** 2026-11-24
- **Branch / PR:** `chore/archive-legacy-advent-calendar` — cleanup PR prepared after merge of #1574.
- **Files changed:** eight legacy Quarto routes (two former landing pages and six mini-lessons); legacy calendar CSS; this handoff document.
- **Work completed:** verified that the post-#1574 full-site render and GitHub Pages deployment both succeeded. Replaced the old landing pages and mini-lessons with lightweight redirects to the bilingual scientific-calendar landing pages, retaining the old rendered URLs. The old lesson routes keep a fallback link to the corresponding canonical learning resource. Their former page-map metadata is retired from the source graph. The independent scientific stories for Days 01 and 06 remain untouched.
- **Validation required:** CI/domain checks must confirm that retired page-map entries are excluded cleanly; Quarto must render the eight redirect routes and pass link/browser checks; CSS reference checks must confirm that the prototype stylesheet is no longer used.
- **Editorial status:** Day 01 remains a planned draft awaiting an actual novice-reader review and editorial acceptance. Do not publish it or begin Day 02 on the basis of this migration.
- **Exact next action:** review the cleanup PR checks; fix any stale generated-map or navigation references before merging.


## 14. Session completion log — calendar migration verification and handoff correction

- **Date:** 2026-11-24
- **Branch / PR:** `docs/calendar-handoff-refresh`; intended PR after review.
- **Files changed:** `docs/advent-calendar-next-steps.md`.
- **Work completed:** rechecked the merged state of Day 01 and the legacy-calendar retirement. Corrected the operational handoff, which still described #1565 as open and the old 24-card prototype as the current calendar. Recorded the real remaining gate: a non-specialist reader must complete the Day 01 protocol before the story is accepted or Day 02 is drafted.
- **Validation performed and results:** confirmed #1565 and #1576 are merged. On merge commit `0fb77b2`, secret scanning and Python quality/domain checks passed; test-suite and Quarto-render jobs were still in progress at the last inspection. No claim is made that those two jobs or a post-cleanup deployment have completed.
- **Open decisions:** obtain an actual novice review; record reading time, comprehension evidence, observed confusion and an explicit accept/revise decision. Day 01 remains planned and unpublished.
- **Exact next action:** conduct the Day 01 novice read-through, update the decision record and revise the story if observations warrant it. Only after acceptance should Day 02 be researched and drafted.


## 15. Session completion log — transfer of investigative craft from Knowledge Stories

- **Date:** 2026-11-24
- **Branch:** `docs/calendar-story-craft-transfer`
- **Reference examined:** [Knowledge Stories — 2026 Data Science & Machine Learning calendar](https://jm-brun.github.io/knowledge-stories/calendar/), including its landing page and the five published investigations.
- **Files changed:** `docs/templates/advent-story-template.qmd`; this handoff.
- **Work completed:** compared the Knowledge Stories calendar's editorial practice with the LLM Lab story contract. The useful transferable principle is not to copy its topics or impose its page structure, but to vary the investigative device to fit the question. Its published examples demonstrate several distinct forms: measurement-profile comparison, sampling and representativeness, counterexamples to summary statistics, covariance derivation, and probabilistic calculation. The reusable LLM Lab template now makes this variation explicit and adds a clearer narrative arc, a specific limitation, a transfer-oriented challenge, an explained solution, and stronger distinctions between synthetic examples, empirical observations and theoretical claims.
- **Boundary preserved:** LLM Lab keeps its approved 24-story slate, anti-duplication rule, thematic shelves and chronological production order. The Knowledge Stories calendar remains an editorial reference, not a source of replacement topics or a prerequisite sequence. No landing-page redesign, new manifest, concept ontology or calendar dependency graph was introduced.
- **Validation performed:** inspected the source calendar's editorial framing and five published day pages; compared them with the current LLM Lab editorial redesign, reusable template, Day 01 bilingual draft and novice-review protocol. This is a documentation/template change only; no article content or public rendering configuration changed.
- **Open gate:** Day 01 remains `status:planned`. A real non-specialist reader must complete the existing protocol, with observed reading time and comprehension evidence, before Day 01 can be accepted or Day 02 can begin. This transfer does not waive or simulate that review.
- **Exact next action:** obtain the Day 01 novice read-through; revise and re-test only where observations justify it. After explicit acceptance, prepare Day 02 using the revised, deliberately non-rigid story template.


## 16. Session completion log — Day 01 public reading release

- **Date:** 2026-11-24
- **Branch / PR:** `calendar/day01-public-release-v3` — PR #1593 (prepared from current `main`).
- **Files changed:** bilingual scientific-calendar landing pages; bilingual Day 01 story pages; Quarto render/resource configuration; regenerated French and English learning-map data; this handoff.
- **Work completed:** exposed the French and English Day 01 stories as public reading versions, linked them from both calendar landing pages, and explicitly distinguished publication for reading from final editorial acceptance. The story remains open to feedback; no novice review is claimed.
- **Integration correction:** the first PR branch became one commit behind `main` after #1586 merged. Rebased the work onto current `main` rather than carrying stale generated artifacts forward. The learning-map generator assigns display ranks by traversing route/hierarchy reachability; the new story is not part of that route, so its record is appended after the existing published pages (rank 144). Existing page ranks are preserved. This is a display-order property, not a curricular dependency.
- **Validation state:** on the previous branch commit, the full Quarto build and secret scan passed; CI identified stale bilingual map data. The map payloads have now been regenerated from current `main` and include 145 records per language. The latest commit still requires fresh CI, Quarto, browser, responsive and accessibility validation.
- **Open gate:** merge and deployment only after required checks pass. Then obtain an actual non-specialist read-through and record reading time, comprehension evidence, observed confusion and an explicit accept/revise decision. Do not begin Day 02 before that editorial gate.
- **Exact next action:** finish the fresh CI, Quarto, browser, responsive and accessibility validation for PR #1593; merge only when required checks pass. After deployment, run the Day 01 novice-review protocol before advancing PR #1596.
