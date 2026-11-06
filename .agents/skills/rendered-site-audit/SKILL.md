---
name: rendered-site-audit
description: Audit the rendered LLM Lab site for visual, responsive, navigation, interaction, keyboard and accessibility behavior using the existing browser-review tooling and explicit evidence limits.
---

# Rendered site audit

## Mission

Verify what a reader actually sees and can operate in the rendered bilingual site. This skill owns browser-observed presentation and interaction behavior, not source-only editorial diagnosis or scientific correctness.

## When to use

Use when the request concerns:
- duplicate, missing or misleading breadcrumbs and route cues;
- rendered navigation, next/previous links, language switching or page context;
- desktop/mobile layout, horizontal overflow, clipped content, figures or equations;
- light/dark theme behavior;
- keyboard focus, disclosure controls, interactive diagrams or learning-map controls;
- accessibility findings from rendered DOM inspection;
- whether a source-level fix actually appears correctly on the published/rendered page.

Use `page-content-audit` for the page's teaching contract, `page-group-audit` for group-level sequence, and `knowledge-architecture-audit` for canonical route or graph semantics. A rendered defect does not by itself prove that the underlying metadata model is wrong.

## Current project tooling

The primary existing browser harness is `scripts/site-browser-review.mjs`. It uses Playwright and Axe and writes evidence under `artifacts/site-browser-review/`.

Before running it:
1. Read the current script and workflow; do not assume its case inventory or assertions remain unchanged.
2. Inspect the relevant workflow conditions. The Quarto workflow currently runs the browser harness only for selected branch-name patterns, not every pull request.
3. Determine whether the target page is included in the harness. A successful run over a fixed inventory does not validate an unlisted page.
4. Prefer testing the exact PR render served locally when the workflow supports it; otherwise state whether the audit used the deployed site and its possible staleness.

Do not claim that a browser harness ran unless its workflow result or local output was observed.

## Audit procedure

### 1. Declare the test matrix

Record:
- target page(s) and both language paths;
- source commit and rendered site revision/URL;
- viewport classes, theme, browser and device emulation;
- interaction profile and controls tested;
- whether the page is in the existing harness inventory;
- known exclusions and unavailable environments.

Use representative desktop and mobile viewports, light and dark themes when supported, and both FR/EN counterparts. Do not imply exhaustive coverage from a small matrix.

### 2. Inspect rendered structure and layout

Check:
- page title and one clear primary heading;
- breadcrumb hierarchy and distinct pedagogical context cues;
- route stepper and local previous/next controls;
- language switch and counterpart destination;
- content width, horizontal overflow, clipping and unexpected overlays;
- loaded images, alt text, SVG labels/descriptions and math rendering;
- disclosure states, code blocks, tables and long equations;
- responsive navigation and content order.

Capture screenshots for material visual findings. Describe the viewport and theme so the observation can be reproduced.

### 3. Test interactions and keyboard use

For relevant controls:
- verify pointer operation and expected state change;
- traverse with keyboard and record visible focus;
- test Enter/Space/Escape behavior where appropriate;
- confirm disclosures and dialogs can be operated and dismissed;
- check that labels, accessible names and roles match the control's function;
- check that focus order follows the visible reading order.

Do not treat the presence of ARIA attributes as proof of accessible behavior. Test actual interaction.

### 4. Review accessibility evidence

Use the repository's Axe/Playwright integration when available. Record:
- rule and affected element;
- impact/severity reported by the tool;
- whether the issue is reproducible;
- whether a manual keyboard or screen-reader-relevant check is needed.

Automated accessibility scans are partial. Do not claim WCAG conformance from an Axe pass or a keyboard smoke test.

### 5. Verify navigation against canonical intent

Compare the rendered controls with the appropriate source of truth:
- Quarto hierarchy for site location;
- guided-route data and narrative curriculum for learning stage/order;
- page metadata for suggested route and conceptual relations;
- Build route for implementation sequence.

A visual breadcrumb must not impersonate a learning path. A rendered route cue can be visually correct but semantically wrong; escalate such cases to the architecture or group-audit skill.

### 6. Report findings

Each finding includes:
- ID (`RSA-01`, ...);
- exact URL/path, viewport, theme and browser;
- screenshot/artifact or DOM/interaction evidence;
- expected versus observed behavior;
- reader impact and severity;
- source-of-truth owner if a canonical data change is needed;
- reproducible acceptance criterion.

Required report:
1. Revision, URL and test matrix.
2. Pages and interactions actually covered.
3. Visual/layout findings.
4. Navigation and route findings.
5. Keyboard/accessibility findings.
6. Screenshots/artifact references.
7. Known coverage gaps and untested cases.
8. Validation state and residual risks.

## Quality gates

- Source inspection and rendered observation are clearly separated.
- Every reported visual issue names its viewport and theme.
- A harness pass is not generalized beyond its tested inventory.
- Automated accessibility checks are not described as conformance certification.
- A screenshot supports an observation but does not prove interaction behavior.
- Navigation appearance is checked against the correct canonical projection.
- Both FR and EN are checked where the change is bilingual.
- No claim of CI or browser execution is made without an observed result.

## Change control

This skill is diagnostic by default. If implementation is requested, fix the canonical source responsible for the defect, not only the rendered artifact; add or update a focused browser assertion when the behavior is important and stable; keep the test bounded; and verify the exact PR render. Do not add a new browser workflow when an existing workflow can be extended safely. Never merge without explicit authorization.
