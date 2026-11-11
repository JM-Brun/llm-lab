

## Transition projection and page rendering — proposed in #977

The transition view is a second, read-only projection of the canonical `transitions` records. It is indexed by the explicitly declared page IDs and does not modify or merge the page-to-stage membership index.

- The existing membership context remains first and unchanged: one membership keeps its compact stage cue; multiple memberships keep the separate all-stages section and each stage's core/optional role.
- A page with one or more declared transitions receives a separate, initially collapsed disclosure below that membership context.
- Each disclosure links the localized source and target stage titles to their stable learning-map anchors and shows the localized purpose when expanded.
- Directed transitions use `→`; symmetric transitions use `↔`. Neither presentation denotes a prerequisite.
- Pages with no declared transition receive no transition disclosure. No relationship is inferred from mentions, sidebar adjacency, concepts, or Build content.
- Technical transition IDs are implementation keys only and are never rendered. Authored titles and purpose are HTML-escaped.
- The generated fragment remains a Quarto partial; site-wide insertion is intentionally deferred to #831.

The projection must remain deterministic in canonical registry order. Regression fixtures cover `generation`, `cross-entropy`, a page with membership but no transition (`text-data`), multiple pages per transition, multiple transitions per page, bilingual copy and escaping.
