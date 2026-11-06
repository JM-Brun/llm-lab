---
name: editorial-boundary-audit
description: Audit editorial boundaries in the LLM Lab learning site. Use when reviewing overlapping page scopes, duplicated explanations, learning objectives, canonical concept ownership, page moves or merges, the core learning route, or the distinction between prerequisites and optional advanced material.
---

# Editorial boundary audit

## Mission

Improve the conceptual ownership and pedagogical organization of the LLM Lab site without reducing the explanations a reader needs, breaking the bilingual site, or turning a flexible learning graph into a rigid linear course.

This skill is for **evidence-based editorial diagnosis and proposed reorganization**. It does not authorize automatic page deletion, merging, shortening, route changes, or scientific rewrites.

## Required project context

Before auditing, read the current versions of:

- `docs/reader-experience-and-editorial-method.md`
- `docs/page-metadata-schema.md`
- `docs/learning-path.md`
- `docs/content-section-mapping.md`
- `docs/contributor-guiding-principles.md`
- `docs/page-audit-inventory.md`, when it covers the pages in scope
- Relevant page templates or archetype guidance in `docs/page-template-guide.md` and `docs/site-page-design-system.md`

Inspect the source pages in both `site/fr/` and `site/en/`, their metadata comments, Quarto navigation, and any linked exercises, implementations, tests, experiments, or references that establish their role. Treat the current repository state as authoritative; older audit reports are leads, not proof that a proposed action is still needed.

The project has four distinct destinations: **Understand**, **Build**, **Deepen**, and **Practice & experiment**. The canonical learning path in `docs/learning-path.md` governs module order and prerequisites. Do not infer the teaching sequence from sidebar order or from a processing pipeline alone.

## Non-negotiable editorial principles

1. **Reader comprehension outranks deduplication.** Repetition is a defect only when it repeats the same explanatory job without adding a new context, representation, level, example, or prerequisite.
2. **A link is not a substitute for a necessary explanation.** Every public lesson must remain independently understandable for its stated LLM learning objective. This is especially important because the general-purpose Wiki is private.
3. **Separate conceptual ownership from pedagogical reuse.** A concept has one canonical home for its full treatment, but several lessons may legitimately restate a compact definition or apply it in different contexts.
4. **Keep the core route lean, not incomplete.** Move optional derivations, variants, research debates, and implementation edge cases to Deepen or Practice only when a first-pass reader can understand the core claim without them.
5. **Do not confuse sequence with prerequisite.** “Read next”, “used by”, “computed after”, and “is a kind of” are different relations. Use `suggested_route`, `related`, and `hierarchy` according to the metadata contract.
6. **Preserve page purpose.** Overview, concept lesson, bridge, guided build, deep dive, exercise, experiment, glossary, and reference pages have different jobs. Do not force them into one template.
7. **Maintain French/English parity.** Audit corresponding pages as a pair. Equivalent scope, learning outcomes, depth, claims, examples, caveats, links, and editorial disposition are required; literal translation is not.
8. **Do not manufacture certainty.** Similar wording, shared tags, a graph edge, or an audit score is a signal for human review, not proof of semantic duplication or a reason to merge pages.

## Audit workflow

### 1. Establish the audit boundary

Record:
- audit date and commit;
- exact page IDs and language counterparts in scope;
- reason for the audit (new content growth, suspected overlap, route confusion, canonical gap, or an earlier finding);
- exclusions and known constraints.

Start with a bounded cluster of related pages, not an indiscriminate whole-repository rewrite. Expand the boundary only when source evidence reveals a necessary dependency or competing ownership claim.

### 2. Build a page evidence matrix

For every page, inspect the actual body, not metadata alone. Capture:

| Evidence | What to record |
|---|---|
| Identity | Stable page ID, path, language, topic tag, page type, status |
| Editorial contract | `scope`, `purpose`, destination, level |
| Learner outcome | What a reader should be able to explain, distinguish, calculate, trace, or decide |
| Actual content | Definitions, claims, mechanisms, equations, assumptions, examples, caveats, exercises |
| Boundaries | What the page explicitly excludes and which neighbouring pages own it |
| Contextual value | What this page adds that another page does not: viewpoint, application, representation, evidence, activity, or depth |
| Graph role | Suggested route, conceptual parents/children, related links |
| Support | References, implementation, tests, experiments, diagrams, and their actual status |
| Bilingual parity | Matching counterpart and substantive differences |

Quote or pinpoint the relevant headings/sections when reporting overlap. Do not infer body content from `scope`, `purpose`, filenames, keywords, sidebar labels, or page titles.

### 3. Identify scope overlap

Compare pages pairwise within a coherent topic cluster. Ask:

- Do they claim the same conceptual object or mechanism?
- Do they cover the same level of abstraction and the same reader question?
- Are the same definitions, derivations, explanations, examples, and caveats repeated?
- Does each page add a distinct application, representation, prerequisite, worked example, implementation contract, experiment, or critical perspective?
- Is one page an overview that should summarize and link to a deeper canonical treatment?
- Is the apparent overlap intentional because the reader needs a local explanation before applying the concept?

Classify each overlap as one of:

- **Intentional reuse:** a concise reminder or local explanation needed for comprehension.
- **Complementary coverage:** related pages with distinct questions, contexts, or depth.
- **Boundary ambiguity:** both pages appear to claim ownership; clarify scope and links.
- **Substantive duplication:** substantially the same explanatory work is performed twice with no material pedagogical gain.
- **Potential gap:** a concept is used or named, but no page owns its explanation.

A lexical similarity score, shared vocabulary, or matching headings may prioritize inspection. Never use it as a semantic verdict. Record false-positive explanations where similar terms mean different things.

### 4. Verify learning objectives against actual explanations

For each candidate overlap, compare the stated `purpose` with what the page actually teaches.

- Rewrite objectives as observable learner outcomes, not descriptions of page contents.
- Identify objectives that are duplicates, overly broad, missing, or unsupported by the body.
- Check whether each claimed outcome has an explanation, example, exercise, or other appropriate evidence.
- Distinguish a repeated definition from a repeated teaching sequence. Repeating a short definition may be necessary; repeating the same full derivation and worked example may not be.
- Check whether an explanation is merely mentioned or genuinely taught.
- Verify whether a page's content has drifted beyond its declared `scope`.

Do not mark an objective as covered just because another page links to it. A cross-link can support a route, but the reader may need a local bridge or recap.

### 5. Decide canonical concept ownership

A concept is a candidate for a canonical page when at least one of these is true:

- multiple pages independently explain its definition or mechanism;
- the concept is reused across several topics and needs stable terminology, notation, assumptions, and boundaries;
- readers need a dedicated explanation to understand several downstream pages;
- variants, misconceptions, limitations, or implementation conventions require a coherent reference point.

Before proposing a new page, check for an existing page that can own the concept after a scope clarification. Prefer improving and linking to an existing canonical page over creating near-duplicate pages.

For each proposed canonical concept, record:

- canonical page ID (existing or proposed);
- definition and exact scope owned by that page;
- what remains in each applied/overview page;
- what is linked rather than retaught;
- minimum local explanation required for standalone comprehension;
- reciprocal links and metadata relations to update;
- French/English counterpart status.

A canonical page is not a dumping ground. Keep application-specific consequences, worked examples, implementation contracts, and experiments in the pages where they answer a distinct question.

### 6. Classify prerequisites versus optional depth

Use a counterfactual test:

> If a first-time reader skips this material, can they still understand the next core learning objective and the central claim of the page, without relying on unexplained terminology?

Classify the material:

- **Core prerequisite:** skipping it makes a core explanation unintelligible or invalid. Keep it in the main route or provide a sufficient local bridge.
- **Core explanation:** directly teaches the stated central objective. Keep it in the main route.
- **Optional deepening:** enriches understanding but is not needed for the next core objective: full derivation, advanced variant, edge case, research debate, optimization, or extended proof. Place in Deepen or an optional disclosure, with a clear link.
- **Practice/evidence:** develops skill or tests a claim through an exercise, implementation, or experiment. Keep in Practice & experiment or Build as appropriate.
- **Reference/context:** supports lookup or historical understanding but is not a conceptual prerequisite.

Do not classify material as advanced merely because it contains equations or technical vocabulary. A short equation may be essential; an intuitive mechanism may be advanced. Classify by its role in the learning dependency, not by apparent difficulty.

For a proposed move, state:
- source section and destination page;
- why it is optional or belongs elsewhere;
- what summary/bridge remains at the source;
- how the reader discovers the destination;
- which core route transition remains valid.

### 7. Propose moves, splits, merges, or boundary changes

Choose the smallest change that resolves the demonstrated problem. For every proposal, specify:

- **Evidence:** exact pages and sections involved;
- **Problem:** duplicated explanation, ambiguous ownership, misplaced depth, missing canonical home, or route break;
- **Action:** keep, clarify scope, shorten repeated exposition, move a section, split a page, merge pages, create a canonical page, or add links;
- **Destination:** exact page/section and language counterpart;
- **Preservation:** definitions, assumptions, examples, caveats, references, exercises, and implementation evidence that must survive;
- **Learning-path impact:** prerequisites and next steps before/after;
- **Metadata impact:** `scope`, `purpose`, tags, `suggested_route`, `hierarchy`, `related`, and render/sidebar entries;
- **Risk and confidence:** what could become harder to understand and what remains unverified.

Do not recommend a merge solely to reduce page count. Do not move a necessary prerequisite behind an advanced link. Do not remove a local explanation until the replacement is present and usable. If a proposed split creates a navigation fragment with no independent learning purpose, do not split.

### 8. Validate the bilingual graph and reader experience

Before considering an editorial reorganization complete:

- update FR and EN pages in the same change, preserving equivalent substance;
- update stable `topic` tags and language-specific IDs as required;
- check metadata against `docs/page-metadata-schema.md`;
- preserve reciprocal parent/child relations and use `related` when a connection is useful but not hierarchical;
- keep `suggested_route` acyclic and aligned with `docs/learning-path.md`;
- update Quarto render lists, sidebars, language switch mappings, and incoming links for renamed/moved pages;
- check every referenced section anchor and local link;
- ensure overview pages remain concise and do not become competing canonical treatments;
- ensure advanced pages remain discoverable but optional;
- inspect the rendered French and English pages, not only their source.

Run the repository's documented validators and tests, then the bilingual Quarto render and local-link checks. Use the current workflow definitions as the authority for exact commands. A passing metadata test or text search does not prove pedagogical quality or visual rendering.

## Expected audit deliverables

Produce a concise report with these sections:

1. **Scope and method** — commit, pages, languages, evidence inspected, exclusions.
2. **Findings matrix** — page pair/cluster, overlap classification, exact sections, learning objectives, evidence, confidence.
3. **Canonical ownership map** — concept → canonical page → applied uses → local explanation required.
4. **Core versus optional map** — prerequisite rationale, main-route placement, Deepen/Build/Practice destination.
5. **Proposed changes** — ordered by priority, smallest safe action first, with FR/EN and metadata impact.
6. **Preservation ledger** — knowledge, equations, examples, caveats, exercises, sources, and implementation evidence that must not be lost.
7. **Validation status** — metadata, tests, Quarto, links, rendered FR/EN review; distinguish passed, failed, pending, and not run.
8. **Open questions** — only decisions that genuinely require editorial judgement.

Use explicit confidence labels:
- **High:** directly supported by page-body evidence and aligned metadata.
- **Medium:** evidence supports the diagnosis, but a boundary or learner dependency needs review.
- **Low:** based mainly on metadata, lexical similarity, or incomplete rendering; do not implement destructive changes on this basis.

## Safety rails for repository edits

- Begin with an audit report or a small, reversible change. Do not combine broad content migration with unrelated refactors.
- Preserve the original explanatory content in a ledger before moving or deleting it.
- Make changes in a dedicated branch and a focused PR; never merge without explicit authorization.
- Do not rewrite scientific claims, equations, or implementation status as a side effect of editorial restructuring. Flag scientific questions separately.
- Do not claim a page is redundant until the body-level comparison is complete.
- Do not claim bilingual parity from file existence alone.
- If evidence is insufficient, report the uncertainty and leave the page unchanged.

## Useful commands

Adapt paths to the current repository layout and inspect the available scripts before assuming a command exists.

```bash
# Inspect metadata and learning graph
uv run python scripts/check_page_metadata.py

# Generate the advisory metadata audit, if present
uv run python scripts/audit_page_metadata.py

# Run focused metadata tests
uv run pytest tests/unit/test_page_metadata.py

# Render the bilingual site (requires Quarto CLI)
quarto render site
```

The metadata audit is a triage aid only. The final editorial decision must be grounded in the page bodies, learner objectives, and the actual core learning route.


## Specialist boundaries and delegation

This skill owns **conceptual ownership, scope overlap and editorial disposition**. It does not replace specialist verification.

- Use `page-content-audit` for the internal quality of a single page's teaching sequence.
- Use `page-group-audit` for coherence across a defined set of pages or transitions.
- Use `scientific-content-audit` for mathematical, statistical, algorithmic, empirical or code-level correctness. Do not settle a factual dispute as an editorial decision.
- Use `knowledge-architecture-audit` for canonical concept IDs, relation semantics, graph projections, route registries or schema integrity.
- Use `rendered-site-audit` for browser-observed layout, navigation and interaction behavior.
- Use `visual-asset-audit` for external visual provenance, exact-byte inspection, licence and reuse decisions.

When a boundary audit discovers a correctness, rendering or rights concern, record it as a linked question with exact evidence and hand it to the owning skill. Do not silently rewrite scientific content or alter existing assets as an editorial cleanup. Keep one canonical finding record and reference it from related audits.
