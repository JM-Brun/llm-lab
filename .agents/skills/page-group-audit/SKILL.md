---
name: page-group-audit
description: Audit a coherent group of LLM Lab documentation pages as a system rather than reviewing pages in isolation. Use for adjacent-page windows, pedagogical learning paths, concept families, documentation sections, and cross-cutting page sets. Evaluate project fit, group coherence, progression, coverage, level boundaries, terminology, navigation, and bilingual consistency; produce evidence-based findings and content-preserving actions.
---

# Page Group Audit

## Mission

Audit a set of related pages as a coherent unit. Determine whether the group has a clear role in LLM Lab, whether its pages fit together, whether their sequence makes sense for the intended reader, and whether the group contributes cleanly to the wider documentation architecture.

Do not reduce this task to proofreading or independent page reviews. A page can be locally correct while the group is redundant, incomplete, badly ordered, inconsistently scoped, or disconnected from the main learning path.

The audit is diagnostic first. Preserve existing knowledge: never recommend deleting, flattening, or moving material without identifying what information would be lost and where it should live instead.

## When to use

Use this skill when asked to audit a set of pages, a section, a chapter, a learning path, neighboring pages, a concept family, or the coherence and harmonization of a group.

Do not use it for a purely technical CI failure or a single-page copy edit unless the user explicitly asks for group-level implications.

## Inputs and group models

Resolve the target from the user's request. Do not force every group into a fixed-size window.

### 1. Local adjacency window

For a request such as "audit these 3 pages" or "review this page and its neighbors":
- Treat named or central pages as the audit core.
- Include the requested previous/next pages as context pages where relevant.
- State the counting convention: 3 pages total, 3 on each side, or central page plus N on either side.
- If the user asks for 3 previous and 3 next, include the central page plus up to 6 neighbors.
- Do not assume URL or file order equals pedagogical order. Verify actual navigation and learning-path references.

### 2. Pedagogical learning path

Treat the explicitly identified path as the audit core, even when its pages are not adjacent.
- Recover intended audience, prerequisites, outcomes, sequence, and depth from project documentation and page-level guidance.
- Inspect preceding/following learning steps where they establish prerequisites or hand-off.
- Evaluate the path as a learner journey, not merely a list of URLs.

### 3. Concept family

Group pages explaining the same or neighboring concepts from different angles: intuition, formal definition, implementation, experiment, application, glossary.
- Identify the canonical explanation and distinct role of each supporting page.
- Detect repeated explanations that should instead cross-reference one another.
- Do not force consolidation when different levels or purposes justify separate treatments.

### 4. Architectural or cross-cutting group

For pages grouped by section, theme, content type, or cross-cutting concern:
- Establish why these pages belong together.
- Check local coherence and links to other parts of the project.
- Identify whether the grouping itself is misleading or incomplete.

If the target is ambiguous and cannot be inferred safely, ask one concise question. Otherwise proceed with an explicit, revisable scope statement.

## Project context to recover

Before judging the pages, inspect the current repository guidance and the smallest useful set of project sources. Prefer:
1. AGENTS.md, contributor/editorial instructions, and skill/workflow documentation;
2. site map, navigation configuration, index, curriculum/learning-path definitions, and page templates;
3. relevant section landing page and neighboring pages;
4. target pages in both language versions when bilingual parity is in scope;
5. linked implementation/code pages and source references when needed to verify claims.

Use the current repository state, not assumptions from previous audits. Follow project-specific conventions over generic documentation conventions.

For LLM Lab, keep these project-level distinctions in view:
- The project is a self-contained pedagogical resource for understanding and experimenting with language models, from foundations to building a small GPT and deeper explorations.
- Distinguish learning paths, conceptual/reference pages, implementation/build material, experiments/labs, syntheses/glossaries, and project-level navigation. They may link to one another but should not be conflated.
- Support multiple depths: a high-level route, substantial intermediate explanations, and optional deep dives. Do not make every reader follow the deepest route.
- Keep theory/conceptual explanation distinct from implementation instructions when their purposes differ; connect them explicitly rather than mixing them indiscriminately.
- A page should have an identifiable pedagogical role, prerequisites, expected outcome, and appropriate depth.
- The public project must remain understandable on its own; do not rely on private wiki material as required context.
- Preserve useful information during restructuring. Prefer explicit links, scoped side lessons, and signposting over deleting content or duplicating entire explanations.
- In bilingual pages, check that EN and FR communicate equivalent concepts and navigation intent without requiring literal word-for-word translation.

These are audit lenses, not a substitute for reading current project instructions.

## Audit procedure

### Step 1 — Declare scope and map the group

Create a compact inventory with:
- title and path/URL;
- core or context status;
- language/version;
- page type and intended role;
- apparent depth (overview, intermediate, deep dive, implementation, reference, experiment);
- prerequisites and expected learner outcome;
- incoming/outgoing links and position in the relevant path.

Record missing evidence as unknown. Do not infer a page's role solely from its filename.

### Step 2 — Reconstruct the intended group logic

Explain briefly:
- why these pages belong together;
- what the reader should gain from the group;
- the intended order or navigation pattern;
- what should be learned before and after the group.

If no coherent rationale can be found, treat that as a finding rather than inventing one.

### Step 3 — Audit each page's contribution

For each core page, assess:
- role clarity: is its purpose distinct and visible?
- scope discipline: does it stay within that purpose?
- prerequisites and outcome: can readers tell what is assumed and what they will gain?
- depth fit: is the level appropriate for its position and audience?
- conceptual reliability: are definitions, notation, claims, examples, and caveats precise and consistent with linked pages?
- pedagogical usability: does the explanation build understanding rather than merely list facts?
- connection: does it point to the right next step, prerequisite, deeper treatment, or implementation?

Avoid rewriting page content during this diagnostic pass.

### Step 4 — Audit group-level coherence

Evaluate the group on these dimensions:

| Dimension | Questions |
|---|---|
| Project fit | Does the group serve the project's purpose and editorial architecture? Is it in the right section and connected to the main experience? |
| Group identity | Is there a clear reason these pages form a group? Is the boundary sensible? |
| Sequence and progression | Does each step prepare for the next? Are transitions explicit? Is the order pedagogically justified? |
| Complementarity | Does each page add a distinct contribution? Are explanations repeated, fragmented, or contradictory? |
| Coverage | Are essential concepts, transitions, prerequisites, examples, or applications missing? Are there unnecessary detours? |
| Level consistency | Are overview, intermediate, deep-dive, and implementation layers clearly signposted and appropriately separated? |
| Terminology and notation | Are terms, symbols, translations, and naming conventions stable? Are differences intentional and explained? |
| Theory / implementation | Is conceptual learning distinguishable from code/build instructions while retaining useful links? |
| Navigation | Do breadcrumbs, previous/next links, section navigation, anchors, and learning-path links communicate distinct and accurate relationships? |
| Cross-project connections | Are links to foundations, experiments, code, glossaries, and external sources appropriate and non-circular? |
| Bilingual parity | Do language versions preserve equivalent scope, sequence, examples, and navigation? Is missing or stale translation visible? |
| Maintenance | Are claims and external assets traceable where needed? Are outdated or fragile dependencies apparent? |

Not every dimension needs equal weight. Explain why a dimension is not applicable rather than silently skipping it.

### Step 5 — Inspect transitions explicitly

For each adjacent pair in the intended sequence, record:
- what knowledge the first page establishes;
- what the next page assumes;
- the conceptual bridge between them;
- whether the hand-off is explicit;
- whether the next page arrives too early, repeats material, or leaves a gap.

For groups of at least three steps, use a transition matrix:

| From → To | Established by previous page | Assumed by next page | Bridge quality | Action |
|---|---|---|---|---|

A transition can be sound without being linear, provided optional or branching structure is clear. For non-adjacent groups, inspect the links that make the relationship discoverable.

### Step 6 — Diagnose overlap and gaps

Classify overlap as:
- **Necessary reinforcement:** repetition intentionally supports learning.
- **Useful recap:** a short recap helps readers enter a page independently.
- **Unclear duplication:** similar material appears without a distinct purpose.
- **Contradiction:** pages make incompatible claims or use incompatible definitions.
- **Misplaced content:** material belongs to another conceptual or instructional layer.

For each important gap, state what the learner needs, where the gap occurs, and whether it needs a new explanation, short bridge, link, example, or prerequisite. Choose the lightest intervention that closes it.

Do not label every repeated term or example as duplication. Distinguish deliberate scaffolding from redundant exposition.

### Step 7 — Assess navigation as information architecture

Check that navigation labels the relationship being represented:
- hierarchy/breadcrumbs: where this page sits;
- pedagogical path: where the learner is in a sequence;
- local previous/next: what comes before/after in this sequence;
- conceptual references: related ideas, not necessarily sequential;
- implementation links: where the idea is used in code or experiments.

These relationships must not be presented as interchangeable or duplicated under identical labels. Check that breadcrumb levels are semantically distinct, links resolve, and previous/next links follow the intended sequence rather than raw file order.

### Step 8 — Form evidence-based findings

Every substantive finding must include:
- ID (GPA-01, GPA-02, ...);
- severity: blocker, high, medium, low, or observation;
- scope: page, transition, group, architecture, or bilingual;
- evidence: exact path, heading, link, or short excerpt;
- impact on comprehension, navigation, correctness, or maintenance;
- concrete and testable recommendation;
- preservation note when content is moved, merged, shortened, or replaced.

Prioritize systemic problems over cosmetic inconsistencies. Do not elevate a stylistic preference without demonstrating learner or architectural impact.

### Step 9 — Produce a coordinated action plan

Group recommendations into:
1. Structural — boundaries, sequence, page roles, missing/extra pages.
2. Pedagogical — prerequisites, bridges, outcomes, depth, examples.
3. Editorial — terminology, notation, consistency, language parity.
4. Navigation — breadcrumbs, path links, previous/next, cross-references.
5. Technical/maintenance — broken links, metadata, source/asset traceability.

Use priorities:
- P0: blocks understanding, correctness, or access to the group;
- P1: materially damages progression or architecture;
- P2: meaningful coherence/usability improvement;
- P3: polish or optional enhancement.

For each action include dependencies, affected pages, expected result, and a verification criterion. Prefer a small number of coherent changes over many isolated edits. Identify actions that can be done independently and those that must be coordinated.

Do not modify pages, create issues, or open a pull request unless the user asks for implementation or task creation. When implementation is requested, work in a branch, preserve content, and verify rendered/navigation results where tooling permits.

## Required report format

# Group audit — [group name]

## 1. Scope
Group model and selection rule; core and context pages; languages and repository revision/date; exclusions and evidence limitations.

## 2. Group purpose and intended reader journey
Explain the group's role in the wider project and its expected learning outcome.

## 3. Group map
A compact table of page, role, depth, prerequisites, outcome, and position.

## 4. Overall assessment
Choose and justify: coherent; coherent with friction; structurally inconsistent; or not yet a meaningful group. Do not invent a numeric score unless requested.

## 5. Page-level observations
Include only observations that affect group coherence or explain a systemic issue. Keep isolated proofreading issues out.

## 6. Group-level findings
Prioritized findings with evidence, impact, recommendation, and preservation notes.

## 7. Sequence and transition analysis
Include the transition matrix or equivalent explicit analysis. Explain branching and optional deep dives.

## 8. Coverage, overlap, and level boundaries
Identify useful reinforcement, duplication, contradictions, gaps, and misplaced content.

## 9. Navigation and project integration
Assess hierarchy, learning path, local sequence, related concepts, implementation links, and language parity.

## 10. Prioritized action plan
List P0–P3 actions, dependencies, affected pages, and acceptance criteria.

## 11. What is already working
Record sound decisions and structures to preserve. This reduces regression risk.

## 12. Open questions and confidence
Separate facts from interpretations; state missing evidence and confidence (high/medium/low).

## Quality gates

Before delivering the audit, verify:
- group boundary and selection rule are explicit;
- core pages are distinguished from context pages;
- wider project architecture was consulted;
- group rationale is stated, not assumed;
- page roles and intended depths are distinguishable;
- key transitions were examined explicitly;
- overlap is classified rather than merely counted;
- gaps are described from the learner's perspective;
- navigation relationships are semantically distinguished;
- recommendations are evidence-based, prioritized, and content-preserving;
- existing strengths and uncertainties are documented;
- local page defects are not confused with group-level defects.

## Operating principles

- Be precise, critical, and constructive.
- Prefer repository evidence over memory or generic best practices.
- Do not infer pedagogical intent from URL order alone.
- Do not optimize for uniformity at the expense of legitimate differences in page purpose.
- Do not force linearity where branching, optional depth, or reference-style navigation is more appropriate.
- Do not duplicate a full explanation merely to make every page standalone; use orientation and a clear link when appropriate.
- Never delete information to make pages shorter. Any consolidation proposal must include a content-preservation map.
- Recommend the smallest useful intervention that resolves the underlying problem.
- Make findings actionable and verifiable.


## Applied calibration protocol (added after the 2026-11-06 pilot)

The first four pilot cases exposed a recurring failure mode: a flat page inventory can accidentally imply that every member is a mandatory, sequential lesson. Apply the following protocol in every future audit.

### A. Assign a membership role to every page

Use one primary role per page in the group map:
- **Core:** part of the intended main sequence or central scope.
- **Optional:** useful extension or advanced depth; not required for the core outcome.
- **Branch:** belongs to a different but connected route, such as Build or training-data preparation.
- **Context:** inspected to understand prerequisites, hand-offs, or boundaries, but not part of the audit core.
- **Excluded related page:** relevant enough to mention, but outside the declared group boundary.

A page may have secondary roles, but do not let that obscure its primary reader-facing purpose. Record destination (Understand, Build, Deepen, Practice, Reference) separately from membership role. Membership does not automatically imply order, prerequisite, or hierarchy.

### B. Normalize the group boundary before auditing

For local windows, state whether N means N pages total or N neighbors on each side. List core and context pages separately.

For a route or concept family, do not force a page count. Record:
- inclusion rationale;
- primary membership role;
- intended order, if any;
- relevant but excluded neighbors;
- the boundary at which the next group or destination begins.

Do not silently expand the group whenever a related page is discovered. Add it as context or an excluded related page unless it changes the group's identity.

### C. Inspect canonical projections separately

For LLM Lab, consult only the projections relevant to the group, but do not treat them as interchangeable:
- narrative curriculum in docs/learning-path.md;
- guided stages and optional resources in data/guided-route.yml;
- practical implementation order in the Build path;
- published destination and sidebar order in site/_quarto.yml;
- page-level suggested_route, hierarchy, related, type, destination and level metadata;
- concept/resource relations where they materially explain the group.

Record agreement and disagreement between projections. A sidebar order is not proof of pedagogical sequence; a hierarchy edge is not proof of prerequisite; a related link is not proof of group membership.

### D. Classify transition types

For every important hand-off, identify its type:
- concept → concept;
- concept → optional deep dive;
- concept → Build implementation;
- concept → Practice/experiment;
- stage → stage;
- overview → detailed mechanism;
- mechanism → output or application.

Judge the bridge against that transition type. A Build hand-off needs to explain what is implemented and what concepts it reuses; a deep-dive hand-off needs to explain why it is optional; an experiment hand-off must state what observation can and cannot establish. Do not demand the same transition wording everywhere.

### E. Use an evidence ledger

Before writing findings, maintain a compact internal ledger with:
- claim or question;
- exact source path and relevant field/heading/link;
- evidence type: canonical documentation, page metadata, page body, navigation configuration, rendered observation, or inferred interpretation;
- confidence;
- whether the claim was verified in the rendered site.

Never describe a rendered behavior as verified when only source files were inspected. Separate file/counterpart existence from semantic bilingual equivalence. Cite source paths in the report so a future maintainer can reproduce the audit.

### F. Apply a two-stage bilingual check

1. **Structural parity:** counterpart exists; page ID, destination, type, level, route membership and major links are aligned or intentionally different.
2. **Semantic parity:** scope, learner outcomes, examples, terminology, caveats, transitions and references communicate equivalent teaching intent.

Report these as separate results. A missing counterpart is a finding; a deliberate language-specific adaptation is not automatically a defect. Do not claim full parity after checking filenames alone.

### G. Calibrate against regression cases

When changing this skill, test the revised procedure against representative cases from docs/audits/page-group-audit-pilot-2026-11-06.md:
- Group A: concept family with optional depth and a Build branch;
- Group B: guided-route stage with optional deep dives;
- Group C: heterogeneous cross-destination family;
- Group D: five-page local sequential window.

A skill refinement is acceptable only if it improves repeatability without flattening these different structures into one template. If a new project pattern is not represented, add a new regression case rather than weakening a useful distinction.

### H. Keep diagnosis and implementation separate

The audit report is diagnostic by default. When implementation is explicitly requested:
- convert accepted findings into a coordinated change set;
- identify canonical sources before editing generated projections;
- update the source of truth, not generated files, unless project instructions say otherwise;
- preserve content and explain any relocation;
- verify metadata, route resolution, links, render output and CI as appropriate;
- update the audit report with implemented, deferred and rejected decisions.

Do not silently turn a recommendation into a canonical curriculum or navigation change.

### I. Record lessons without bloating every audit

The full audit report is the evidence record. The skill should contain reusable method rules, not copy every project's findings into its permanent instructions. Add a new rule only when a pilot reveals a repeatable methodological failure or ambiguity. Keep project-specific findings in dated audit reports and link them as calibration examples.
