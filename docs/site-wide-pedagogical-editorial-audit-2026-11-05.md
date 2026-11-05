# Site-wide pedagogical and editorial audit — 2026-11-05

**Status:** initial cross-site audit documented; remediation is incremental. This is not a certification of scientific correctness, accessibility, or learning effectiveness.
**Scope:** published bilingual LLM Lab, its navigation projections, and the source contracts that generate them.
**Coordination:** [#337 rendered navigation review](https://github.com/JM-Brun/llm-lab/issues/337), [#320 canonical text-to-representation review](https://github.com/JM-Brun/llm-lab/issues/320), [#329 exercise review](https://github.com/JM-Brun/llm-lab/issues/329), [#341 homepage review](https://github.com/JM-Brun/llm-lab/issues/341), [#347 prediction-to-learning review](https://github.com/JM-Brun/llm-lab/issues/347), [#368 bilingual lesson template](https://github.com/JM-Brun/llm-lab/issues/368).

## 1. Purpose and evidence boundary

This audit treats the website as one learning environment rather than a set of independent pages. It checks four dimensions:

1. **Information architecture:** site navigation, pedagogical context, local process sequences, conceptual relations, and suggested reading transitions.
2. **Learning progression:** purpose, prerequisites, core/optional depth, continuity between explanations, and links to implementation or practice.
3. **Scientific/editorial quality:** definitions, notation, assumptions, examples, caveats, misconceptions, evidence, and source attribution.
4. **Published experience:** bilingual parity, responsive layout, interaction, keyboard access, contrast, and correspondence between source and rendered pages.

Evidence must be labelled accurately:
- Source inspection establishes what is authored and configured.
- Quarto render and static checks establish that the site can be generated and that tested structural constraints hold.
- Browser tests establish only the tested interactions, viewports, and pages.
- Axe establishes detected accessibility violations for the tested DOM and rules, not WCAG conformance.
- Learner studies are required for claims about comprehension, usability, or learning effectiveness.

The initial review was a cross-cutting inspection informed by published entry points, canonical lesson pages, current repository contracts, route audit, and recent PR/issue evidence. It was not a page-by-page scientific peer review or a manual inspection of every viewport.

## 2. Architecture: preserve distinct navigation semantics

The site must preserve these separate questions:

| Dimension | Reader question | Source of truth |
|---|---|---|
| Site location | Where am I in the published site? | Quarto sidebar and native title breadcrumb |
| Pedagogical context | Which guided stage does this page serve? | data/guided-route.yml and generated context |
| Local process | Which steps make up the process explained here? | Page-authored local sequence, only when justified |
| Suggested transition | What is a useful next or previous reading? | suggested_route metadata and route cards |
| Conceptual hierarchy | Which concepts contain or decompose this topic? | Typed page/concept hierarchy |
| Concept relations | Which concepts are semantically connected? | Typed concept graph |
| Build dependency | What implementation milestone depends on this? | Guided-build sequence |
| Exploratory discovery | What else can I explore? | Page/resource/concept browser |

These dimensions may link to one another but must not be merged into one synthetic path. A page may legitimately show the native Quarto breadcrumb, one or more guided-stage contexts, and a local process sequence only when each adds distinct information.

The canonical contract is [pedagogical-breadcrumb-and-page-navigation-contract.md](pedagogical-breadcrumb-and-page-navigation-contract.md). Recent merged work supersedes parts of the initial visual-route audit:
- #535 repaired targeted Quarto callout semantics and contrast findings; its 40-case browser/Axe run passed.
- #537 retired misleading legacy five-stop steppers on attention, causal masking, logits, and cross-entropy.
- #539/#540 retained route transitions and reconciled nested text-data context with its local representation sequence.
- #541 added generated guided-route context to remaining core and optional route members in FR/EN.

Do not reopen those source changes without a reproducible regression. The remaining review is deployed rendering and reader experience.

## 3. Positive design decisions to preserve

- The four destinations **Understand / Build / Deepen / Practice & experiment** are complementary entry points, not four competing curricula. Practice remains transversal.
- The guided conceptual route and guided GPT build are distinct sequences; neither should be inferred from the other.
- Deep dives are optional unless a real conceptual dependency is documented.
- Canonical concept pages should own definitions; companion pages should explain their particular connection without duplicating canonical exposition.
- The page template is a soft target, not a mandatory checklist. Page archetypes should differ where the learner question differs.
- Scientific claims should be distinguished from intuition, illustrations, numerical examples, formal derivations, tests, and empirical experiments.
- Status labels must distinguish implemented, tested, illustrative, and planned work.
- The public site must remain self-contained for its LLM-specific learning objectives; links to the separate knowledge wiki are not substitutes for essential explanations.

## 4. Initial findings and risk register

### F1 — Navigation dimensions were liable to be duplicated or conflated
**Severity:** high reader-experience risk.
**Status:** source-level remediation substantially integrated by #535–#541; deployed review remains necessary.

The native site breadcrumb, generated guided-stage context, and local process stepper answer different questions. Earlier implementations duplicated site breadcrumbs and used a five-stop stepper that skipped important conceptual stages. The current contract and merged changes separate these dimensions. Verify the deployed FR/EN result, especially title blocks, text-data, Q/K/V, scaled attention, causal masking, logits, cross-entropy, and multi-membership pages.

### F2 — Route continuity was uneven across the prediction-to-learning sequence
**Severity:** medium.
**Status:** source-level route context coverage expanded by #541; review rendered route cards and transitions.

Check that the suggested sequence from logits through probabilities, likelihood, cross-entropy, loss, gradients, and evaluation is understandable without presenting every transition as a strict prerequisite. Confirm previous/next links, labels, and return paths in both languages.

### F3 — Core explanation and optional depth need consistent reader cues
**Severity:** medium.
**Status:** editorial review required; do not solve with boilerplate.

For each page, verify that the central mental model and necessary caveats are in the main reading flow. Extended derivations, implementation details, historical context, and optional variants may be disclosed progressively, but assumptions that alter a claim must remain visible. Avoid adding identical headings or metadata panels to every page.

### F4 — Scientific quality has not yet been established page by page
**Severity:** high epistemic risk.
**Status:** not yet audited exhaustively; coordinate with existing page-family reviews.

Prioritize:
- text, Unicode, tokenization, and representation distinctions (#320);
- attention, Q/K/V, masking, and Transformer architecture;
- logits, probabilities, likelihood, cross-entropy, loss, and gradients (#347);
- evaluation protocols and claims about model quality;
- mathematical notation, tensor shapes, axis conventions, numerical examples, and limiting cases.

For each substantive claim, identify its scope, assumptions, source, and appropriate evidence. Check that examples are reproducible by hand or test, and that counterexamples address likely misconceptions. Do not label a page scientifically validated merely because Quarto or Python CI passes.

### F5 — Accessibility evidence is improving but incomplete
**Severity:** medium/high.
**Status:** automated targeted findings fixed; manual evidence gaps remain.

The #535 browser/Axe run passed 40 tested cases and removed targeted blocking aria-allowed-attr and color-contrast findings. This is not a WCAG conformance claim. Real touchscreen interaction and manual screen-reader review remain separate checks in #337/#417. Check zoom/reflow, focus order, meaningful accessible names, keyboard operation, and non-colour state cues.

### F6 — Learner effectiveness is not measured
**Severity:** medium.
**Status:** future validation.

Navigation and source quality cannot establish learning outcomes. After content and route stabilization, test representative tasks: explain a concept, trace a numerical example, distinguish a misconception, and transfer the idea to an unfamiliar case. Record participant/task/context and avoid generalizing from informal feedback.

## 5. Page-family review matrix

This is a review queue, not a claim that unreviewed pages are defective.

| Family | Primary audit question | Existing coordination |
|---|---|---|
| Homepage and orientation | Are purpose, entry points, system overview, and status immediately clear? | #341 |
| Text and tokenization | Are characters, code points, tokens, IDs, and vectors clearly distinguished? | #320 |
| Embeddings and representations | Are lookup vectors, positional information, and contextual states distinguished? | #320 |
| Tensors and mathematical foundations | Are shape, axis, broadcasting, and operation conventions explicit? | Existing canonical pages; add findings to relevant review |
| Transformer architecture | Are data flow, block components, and variants separated without false universality? | #337/#368 as applicable |
| Q/K/V and attention | Are projections, score computation, scaling, masking, softmax, and aggregation correctly related? | #337 and canonical page reviews |
| Prediction and learning | Are logits, probabilities, likelihood, cross-entropy, loss, and gradients distinguished? | #347 |
| Evaluation | Are task, dataset, split, metric, baseline, uncertainty, and limitations explicit? | #347 and evaluation page |
| Build path | Does each milestone correspond to real code, tests, and a verifiable artifact? | docs/learning-path.md and docs/content-section-mapping.md |
| Exercises and experiments | Does each activity have a clear objective, expected reasoning, feedback, and scope? | #329 |
| Glossary and reference | Are definitions concise, canonical, bilingual, and linked to substantive explanations? | Existing glossary and concept registry |

## 6. Remediation sequence

### Immediate — verify merged navigation in the published site
- Inspect the current deployed commit, not cached or older snapshots.
- Compare FR and EN for homepage, text-data, tokenization, embeddings, contextual representations, Q/K/V, attention, causal masking, logits, cross-entropy, generation, and evaluation.
- Record browser, viewport, page, visible cue types, link destinations, keyboard behavior, and screenshots/artifact references.
- Confirm exactly one site-location breadcrumb; guided context and local stepper appear only where semantically justified.
- Verify route-card labels and targets and confirm no misleading legacy stepper remains.

### Next — scientific/editorial page-family audits
- Reuse #320, #329, #341, and #347 rather than creating duplicate issues.
- Review one coherent family at a time in both languages.
- Record each finding with page, exact claim or element, evidence, severity, correction, and test.
- Prefer minimal corrections to canonical content; preserve useful detail and provenance.

### Then — validation and learning evidence
- Complete touch and screen-reader checks under #337/#417.
- Add targeted scientific regression tests where a mathematical or implementation claim is testable.
- Conduct small learner-task evaluations after route and content are stable.
- Update project status and roadmap only when evidence supports the status change.

## 7. Definition of done

- [ ] Current published deployment commit is recorded and corresponds to intended main commit.
- [ ] FR/EN page-family coverage is recorded with reproducible page and viewport details.
- [ ] Site breadcrumb, guided context, local process sequence, and suggested transitions are checked independently.
- [ ] Existing issue coverage is reconciled; no duplicate issue is created for an existing finding.
- [ ] Scientific findings cite a page location and supporting source or derivation.
- [ ] Corrections have appropriate static, unit, browser, or numerical regression tests.
- [ ] Touch and screen-reader limitations are reported honestly.
- [ ] No claim of learner effectiveness or WCAG conformance is made without corresponding evidence.

## 8. Continuation protocol

A future session should:
1. Read this audit and the canonical navigation contract.
2. Check current main, open PRs, existing issue state, and deployed Pages commit before acting; this document records a point-in-time state.
3. Resume with immediate deployed navigation verification, then take the next page-family review from existing coordination issues.
4. Update this document with dated evidence and links. Do not repeat completed work or infer that a merged source change is deployed.
5. Keep this audit as a coordination document; detailed findings belong in the existing family issue or a focused new issue only when no suitable issue exists.
