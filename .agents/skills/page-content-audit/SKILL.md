---
name: page-content-audit
description: Audit the internal pedagogical and editorial quality of one LLM Lab page or a small set of directly related page counterparts, without turning the review into a site-wide or graph audit.
---

# Page content audit

## Mission

Evaluate whether a page fulfils its own reader-facing contract: a clear learner question, appropriate scope, observable outcome, understandable explanation, suitable examples, explicit assumptions, useful transitions and a coherent next action.

This is an internal page audit. It is not a generic copy-editing pass, a scientific peer review, a group-sequence audit, or a knowledge-graph redesign.

## When to use

Use when the request concerns:
- one page's pedagogical quality, structure, completeness or readability;
- one FR/EN page pair and whether they teach equivalent content;
- whether a page mixes too many levels or purposes;
- whether a page's declared scope, purpose and learner outcomes match its actual body.

Use `page-group-audit` when the main question concerns multiple pages as a system or their transitions. Use `editorial-boundary-audit` when ownership or duplication across pages is central.

## Required baseline

Inspect the current repository guidance and the smallest useful set of evidence:
- `docs/reader-experience-and-editorial-method.md`;
- `docs/page-metadata-schema.md`;
- `docs/page-template-guide.md` and relevant archetype/template;
- `docs/learning-path.md` and relevant guided-route/build definitions;
- the target page's metadata and complete body;
- its FR/EN counterpart when applicable;
- immediate prerequisite and next-step pages only where needed to verify assumptions and hand-offs.

Use current source files as authority. A previous audit report is a lead, not proof.

## Audit procedure

### 1. Establish the page contract

Record path, stable page ID, language, type, destination, level, declared scope, purpose, prerequisites, expected outcome, suggested route and repository revision.

Rewrite the expected outcome as an observable capability (explain, distinguish, derive, calculate, implement, inspect, compare or decide). Mark absent or ambiguous contract elements as unknown rather than inventing them.

### 2. Inspect the actual teaching structure

Map the page's sections in order. For each substantial section, record:
- learner question answered;
- concept or operation introduced;
- prerequisite assumed;
- explanatory mode (intuition, formalism, worked example, code, experiment, reference);
- evidence or source supporting factual claims;
- hand-off to the next section or destination.

Identify abrupt level changes, repeated explanations, unexplained notation, orphan sections, premature implementation details, and content that does not serve the declared outcome.

### 3. Evaluate the explanation

Check:
- whether the opening establishes the problem and motivation;
- whether intuition is bounded and followed by a precise definition where needed;
- whether notation is introduced before use and remains consistent;
- whether equations, diagrams, examples and prose explain the same mechanism;
- whether assumptions, limitations, counterexamples and common misconceptions are visible;
- whether a reader can connect the explanation to a concrete input, operation and output;
- whether the conclusion consolidates the key idea without merely repeating the introduction.

Do not certify scientific correctness here. Flag claims, derivations, dimensions, complexity statements or implementation assertions that need `scientific-content-audit`.

### 4. Check scope and level discipline

Determine whether the page is primarily an overview, concept lesson, guided build, deep dive, practice/experiment, synthesis, glossary or reference. Check whether its actual sections match that role.

Distinguish:
- essential content needed for the stated outcome;
- useful local recap needed for standalone comprehension;
- optional depth that can be signposted without becoming a prerequisite;
- material that belongs to another reader task or page.

Do not recommend removal merely because a section is advanced or long. Any proposed relocation needs a preservation map and a working destination.

### 5. Check learner usability

Assess whether the reader can answer:
- Why am I reading this?
- What should I know first?
- What will I understand or be able to do afterwards?
- Which parts are essential versus optional?
- Where should I go next, and why?

Inspect headings, summaries, callouts, figures, exercises, code blocks, links, glossary references and page navigation for their actual contribution. Do not treat visual polish as evidence of comprehension.

### 6. Check bilingual equivalence

For FR/EN pairs, perform two separate checks:
1. Structural parity: counterpart, stable topic identity, page type, destination, level, section roles and major links.
2. Semantic parity: scope, learning outcomes, claims, equations, examples, assumptions, caveats and next-step intent.

Natural language-specific phrasing is expected. Literal translation is not. File existence or matching headings alone do not establish parity.

### 7. Check evidence and implementation status

Classify evidence as:
- canonical documentation;
- page metadata;
- page body;
- source/reference;
- implementation or test;
- rendered observation;
- inference.

State whether rendered output, mobile behavior, accessibility and links were actually inspected. Distinguish proposed code from executable code, documented behavior from tested behavior, and source results from project results.

## Findings and report

Each substantive finding must include:
- ID (`PCA-01`, ...);
- severity (blocker/high/medium/low/observation);
- exact path and heading/section;
- evidence and confidence;
- impact on the learner;
- smallest concrete recommendation;
- preservation note for any move, merge, shortening or replacement;
- specialist hand-off, if required.

Required report:
1. Scope, revision and evidence limitations.
2. Page contract and intended learner outcome.
3. Section-by-section teaching map.
4. Overall assessment: fulfils contract / fulfils with friction / contract mismatch / insufficient evidence.
5. Findings, prioritized by learner impact.
6. What works and should be preserved.
7. FR/EN parity status, when applicable.
8. Validation status and open questions.

## Quality gates

Before finalizing:
- read the full page body, not metadata alone;
- distinguish declared scope from actual teaching;
- tie each finding to a learner consequence;
- separate essential, recap and optional content;
- do not label a scientific claim correct without appropriate verification;
- do not claim rendered, responsive or accessible behavior unless observed;
- do not confuse a page-level issue with group-level or architecture-level issues;
- preserve useful content and cite exact evidence.

## Change control

This skill is diagnostic by default. If implementation is explicitly requested, use a focused branch and change set, preserve the original content, update FR/EN together when applicable, run the relevant validators and render checks, and report observed results. Never merge without explicit authorization.


## Rendered behavior hand-off

This skill may identify a likely layout or navigation concern from source structure. For actual desktop/mobile, theme, keyboard, interaction and accessibility verification, use `rendered-site-audit`. State explicitly when a page was reviewed only at source level; do not imply rendered usability from a successful content audit.
