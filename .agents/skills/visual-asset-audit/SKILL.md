---
name: visual-asset-audit
description: Audit the provenance, exact identity, accessibility evidence, licensing and proposed reuse of external visual assets in LLM Lab without silently removing or replacing existing material.
---

# Visual asset audit

## Mission

Establish what an image or other visual asset actually is, where it came from, what evidence exists for its creator and licence, how LLM Lab currently uses it, and whether a proposed new use is permitted.

This skill owns **asset-level provenance and reuse decisions**. It does not replace rendered-site checks, pedagogical review, or scientific verification of what a diagram claims.

## When to use

Use when:
- an existing project asset or proposed external image, diagram, screenshot, chart, SVG or other visual asset needs a focused provenance/rights/reuse decision;
- the project needs to establish exact asset identity, creator/rightsholder, licence or permission;
- an existing asset's accessibility text, caption, attribution or reuse status is uncertain;
- a full source scan has already identified an asset-specific question that needs a separate rights or reuse decision;
- a proposed crop, adaptation, recreation, local copy, redistribution or replacement needs review.

Use `rendered-site-audit` for how an asset appears and behaves in the rendered site. Use `scientific-content-audit` to verify the technical claims represented by a diagram. Use `page-content-audit` or `page-group-audit` for its teaching role.

## Required project guidance

Read and follow:
- `docs/workflows/templates/visual-asset-audit-template.md`;
- relevant source-review records and project asset/licensing instructions;
- the exact source page and exact asset URL/path;
- the page(s), language variants, caption and surrounding explanation that use the asset.

Do not infer a general asset policy from one previous audit. Treat the current template and explicit owner decisions as authoritative.

## Audit procedure

### 1. Inventory each asset separately

For every figure or asset, record:
- stable figure ID;
- page path(s), language(s), section and source locator;
- exact URL or repository path;
- whether it is embedded, linked, locally stored or generated;
- intended use: display/hosting, reproduction, adaptation/cropping, redistribution or proposed future use;
- retrieval date and method.

Do not combine several figures into one row merely because they appear in the same article.

### 2. Verify exact identity and inspect the bytes

Distinguish the source page from the asset itself:
- retrieve the exact asset URL or repository file where possible;
- record whether the exact bytes were retrieved;
- visually inspect the actual asset when available;
- record format, dimensions and embedded labels where relevant;
- compare the inspected asset with the page caption and surrounding text.

A caption, thumbnail, placeholder, alt-text string, filename or search snippet is not visual inspection. If bytes cannot be retrieved, state the limitation and do not describe unseen content.

### 3. Establish provenance and rights evidence

Record separately:
- creator/rightsholder evidence;
- asset-level licence or permission evidence;
- licence version, scope and relevant conditions;
- required attribution;
- whether modifications are allowed;
- whether commercial use, redistribution, hosting or derivative works are covered.

Do not equate attribution with permission. A website's terms, article licence or repository licence do not automatically establish the licence of every embedded image. Record conflicting, missing or ambiguous evidence as unknown; do not resolve it by assumption.

### 4. Separate existing use from proposed new use

Make two independent decisions.

**Existing use**
- Default to `preserve-existing-use`.
- If a concern exists, use `escalate-to-owner` and describe the evidence.
- Never remove, replace, hide, disable, crop, rehost, redraw or convert an existing embedded asset to link-only as part of an audit.

**Proposed new use**
- Use `verified-compatible` only when exact asset-level permission covers the intended use.
- Use `permission-required` when permission is needed but not established.
- Use `defer-new-use` when identity, bytes, rights or scope remain uncertain.
- Use `link-to-original-only` only when the proposal is a new link rather than an existing embed.

An audit is not authorization to modify existing material. Any exceptional action affecting an existing asset requires a separate explicit instruction from the project owner.

### 5. Assess accessibility independently

Inspect and record:
- meaningful alt text for informative images;
- empty alt text for purely decorative images where appropriate;
- SVG `title`, `desc`, accessible name and role;
- whether labels embedded in an image are also available as text;
- caption and nearby explanation;
- whether the asset's purpose is understandable without relying on color alone.

Source inspection can establish that attributes exist, not that assistive technology exposes them correctly. Use `rendered-site-audit` for browser accessibility-tree, keyboard and responsive checks.

### 6. Assess pedagogical and scientific role without conflating them with rights

Record whether the visual is:
- conceptual schematic;
- quantitative chart;
- implementation diagram;
- screenshot/UI evidence;
- decorative illustration;
- external teaching resource.

Check whether its caption and nearby prose accurately describe the inspected asset. If the diagram makes scientific or algorithmic claims, route those claims to `scientific-content-audit`. If the visual is redundant, confusing or poorly placed, route the pedagogical question to the page or group audit.

### 7. Report evidence and decisions

Use the project template's asset-level table and inspection record. Each substantive finding includes:
- stable ID (`VAA-01`, ...);
- exact asset URL/path and page locator;
- what was actually retrieved and inspected;
- evidence source and confidence;
- existing-use decision;
- proposed-new-use decision, if applicable;
- accessibility status;
- unresolved rights or owner question.

Required report:
1. Scope, date, pages and assets covered.
2. Asset-level inventory.
3. Exact-byte and visual-inspection status.
4. Provenance/licence/permission evidence.
5. Existing-use and proposed-use decisions.
6. Accessibility findings.
7. Pedagogical/scientific hand-offs.
8. Unavailable evidence and owner follow-ups.

## Quality gates

- Every asset has its own exact URL or repository path.
- Source page and asset-level licence are treated separately.
- Exact bytes and visual inspection are explicitly marked as done or not done.
- Attribution is not presented as a licence.
- Existing-use and proposed-new-use decisions are separate.
- Unknown rights never trigger silent deletion or replacement.
- No unseen visual is described, compared or recreated.
- Accessibility, scientific correctness and rights are separate verdicts.
- Every proposed use is assessed against its actual intended action.

## Change control

Diagnostic by default. Do not modify existing assets during an audit. If the user separately requests a new asset use, verify the exact asset and permission first, document attribution and accessibility requirements, and make the smallest permitted change. If rights remain uncertain, defer the new use and retain the existing project content unchanged. Never merge without explicit authorization.
