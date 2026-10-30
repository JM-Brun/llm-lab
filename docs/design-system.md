# LLM Lab visual design system

**Status:** adopted direction; implementation and rendered review are incremental.  
**Decision date:** 2026-10-30  
**Brand direction:** scientific learning environment, with green as the primary brand colour.

## 1. Design intent

LLM Lab should feel like a scientific instrument for learning: precise, calm, legible, exploratory, and technically credible. The visual language may take inspiration from [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) for direct manipulation and visual explanation, but must not imitate its interface or imply equivalent model-specific capabilities.

The visual system serves five learning needs: orient the reader in the learning graph; distinguish intuition, formal claims, implementation, experiments, and limitations; make equations, tensor shapes, code, and diagrams readable; expose optional depth without hiding essential assumptions; and make implemented, planned, and illustrative material visibly distinct.

## 2. Brand palette

Green is the primary brand colour. It identifies the site, navigation, links, primary actions, selected states, and the main information flow in diagrams.

| Token | Hex | Intended use |
|---|---|---|
| Brand green | #16A34A | Main identity, links, interactive accents |
| Deep green | #14532D | Navbar, dark hero surfaces, strong brand surfaces |
| Action green | #15803D | Primary buttons and high-emphasis actions |
| Bright green | #22C55E | Small highlights; not body text on white |
| Pale green | #DCFCE7 | Selected states and subtle fills |
| Dark ink | #17212B | Main text on light surfaces |
| Slate | #475569 / #64748B | Secondary text and metadata, subject to contrast checks |
| Neutral paper | #F8FAFC | Main light reading surface |
| Neutral line | #D1D5DB | Borders, separators, table rules |
| Amber | #B45309 | Caution and attention states |
| Red | #DC2626 | Errors and negative states |
| Blue | #0EA5E9 | Distinct data category or external/system reference, not the brand |
| Violet | #8B5CF6 | Distinct data category only where a legend defines its meaning |

### Usage rules

- Keep long-form reading surfaces neutral. Do not turn every card, section, or page background green.
- Use deep green for global navigation and dark hero surfaces; use action green for primary controls.
- Use pale green for low-emphasis fills. Do not put small white text on bright green.
- Green must not mean both brand and success by default. Success, warning, error, and informational states retain explicit semantic labels/icons and accessible contrast.
- In diagrams, define a stable legend. Green may identify the main data path, but tokens, tensor axes, masks, parameters, and outputs must not be distinguished by colour alone.
- Amber, blue, and violet are reserved for semantic or data-specific distinctions, not competing brand identities.

## 3. Typography and layout

- Use a readable sans-serif for prose and a monospace face for code, identifiers, and compact technical metadata.
- Keep paragraphs at a comfortable measure (approximately 65–80 characters per line); allow diagrams, tables, and code to use wider containers when necessary.
- Use a clear heading hierarchy and consistent vertical rhythm. Avoid oversized headings inside dense technical sections.
- Equations need whitespace; define symbols and tensor dimensions before use.
- Code blocks should support copying, preserve readable line lengths, and remain usable on narrow screens.
- Cards should encode a meaningful action or content grouping, not merely decorate every paragraph.

## 4. Interaction and motion

- Interactive controls must identify the quantity they change and the output they affect.
- Show units, tensor shapes, parameter constraints, and relevant assumptions beside controls and results.
- A visualization must answer a stated learning question and support an interpretation; animation alone is not an interaction objective.
- Respect reduced-motion preferences. Motion must not be required to understand a state change.
- Provide keyboard operation, visible focus, accessible names, and a textual/static fallback for essential information.
- Do not make hover the only way to reveal information.

## 5. Content-state vocabulary

Use explicit labels where status could otherwise be ambiguous:

- **Implemented:** present and usable in the repository/site.
- **Tested:** covered by identified tests or a stated validation procedure; specify what tests establish.
- **Illustrative:** a conceptual diagram or synthetic example, not a live model result.
- **Planned:** intended work that is not yet available.
- **Research note:** a sourced interpretation or open question, not necessarily an established result.

Visual polish must not upgrade a planned feature to implemented, or an illustrative graphic to experimental evidence.

## 6. Accessibility and responsive acceptance

- Text contrast: WCAG 2.2 AA, normally at least 4.5:1 for body text and 3:1 for qualifying large text.
- Non-text UI components and meaningful graphical objects: at least 3:1 against adjacent colours where WCAG requires it.
- Never use colour as the only distinction; pair it with labels, shape, line style, or icons.
- All controls and navigation must be keyboard accessible with a visible focus indicator.
- Test desktop, tablet, and narrow mobile widths. Dense diagrams may scroll horizontally only when the scrolling region is obvious and information remains available in an accessible alternative.
- Verify both French and English layouts, including long labels and mathematical notation.

## 7. Implementation constraints

- Keep Quarto as the publishing framework and the existing SCSS design layer as the source of site styling.
- Prefer design tokens and reusable SCSS components over scattered one-off hex values.
- Keep the French/English content architecture and scientific review gates intact.
- Use SVG for diagrams that need crisp scaling and accessible labels. Use JavaScript only when it adds meaningful interaction.
- Python remains the reference implementation for numerical behavior where a Python implementation exists. Any browser-side equivalent must be checked against it or explicitly documented as an independent teaching approximation.
- Avoid introducing a front-end framework, large client-side dependencies, model downloads, or duplicate implementations merely to imitate another site.

## 8. UX delivery sequence

The authoritative sequence and acceptance criteria live in [the repository roadmap](roadmap.md), under **UX and visual-system track — Green identity**:

1. establish consistent green tokens and navbar identity;
2. refine homepage hierarchy and first-screen orientation;
3. improve navigation and wayfinding without discarding the detailed learning graph;
4. standardize page patterns by pedagogical purpose;
5. build and validate one interactive exemplar;
6. expand only after scientific, accessibility, responsive, performance, and maintenance review.

## 9. References

- [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) — reference for visual explanation and direct manipulation, not a template to copy.
- [Quarto website documentation](https://quarto.org/docs/websites/) — publishing and navigation constraints.
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) — accessibility requirements.
