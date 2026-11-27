# LLM Lab visual design system

**Status:** adopted direction; implementation and rendered review are incremental.  
**Decision date:** 2026-10-30  
**Brand direction:** scientific learning environment, with green as the primary brand colour.

## Relationship to page templates

The visual system is implemented through the existing Quarto classes and site stylesheet. The [page-template guide](page-template-guide.md) provides reusable structures; the [page archetype implementation map](site-page-design-system.md) connects those structures to the metadata taxonomy and the editorial contract. Templates must reuse this system rather than introduce competing visual conventions.

## 1. Design intent

LLM Lab should feel like a scientific instrument for learning: precise, calm, legible, exploratory, and technically credible. The visual language may take inspiration from [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) for direct manipulation and visual explanation, but must not imitate its interface or imply equivalent model-specific capabilities.

The visual system serves five learning needs: orient the reader in the learning graph; distinguish intuition, formal claims, implementation, experiments, and limitations; make equations, tensor shapes, code, and diagrams readable; expose optional depth without hiding essential assumptions; and make implemented, planned, and illustrative material visibly distinct.

## 2. Brand palette

Green is the primary brand colour. It identifies the site, navigation, links, primary actions, selected states, and the main information flow in diagrams.

| Token | Hex | Intended use |
|---|---|---|
| Brand green | #16A34A | Main identity, borders, large accents and non-text interactive cues; not small text on pale surfaces |
| Deep green | #14532D | Navbar, dark hero surfaces, strong brand surfaces |
| Action green | #15803D | Text links, small emphasis labels on light surfaces, primary buttons and high-emphasis actions |
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

**Text-contrast rule:** on the reading surface `#F8FAFC`, brand green `#16A34A` has a calculated contrast ratio of 3.15:1 and must not be used for normal-size text. Action green `#15803D` reaches 4.79:1 and is the preferred green for links and small labels on light surfaces. This pairwise calculation is not a global WCAG conformance claim.

### Usage rules

- Keep long-form reading surfaces neutral. Do not turn every card, section, or page background green.
- Use deep green for global navigation and dark hero surfaces; use action green for primary controls and small text on light surfaces.
- Use pale green for low-emphasis fills. Do not put small white text on bright green.
- Green must not mean both brand and success by default. Success, warning, error, and informational states retain explicit semantic labels/icons and accessible contrast.
- In diagrams, define a stable legend. Green may identify the main data path, but tokens, tensor axes, masks, parameters, and outputs must not be distinguished by colour alone.
- Amber, blue, and violet are reserved for semantic or data-specific distinctions, not competing brand identities.

## Semantic colour layers for computation and data

The visual system distinguishes two independent questions:

- **Computational role:** what operation is being performed (generation, observed-target scoring, evaluation, or training)?
- **Data representation:** what kind of object is being manipulated (text, token, token ID, embedding, hidden state, logit, probability, etc.)?

These dimensions must never be collapsed into one colour taxonomy. An embedding remains an embedding during inference, scoring, and training. Conversely, a training operation may consume token IDs, hidden states, logits, and target labels; it is not represented by one data-type colour.

### Computational roles: a deliberately limited vocabulary

For diagrams whose instructional purpose is to compare the three uses of the shared prediction mechanism, the candidate mapping is:

| Role | Candidate visual accent | Meaning |
|---|---|---|
| Generation / inference | Green | Decode/select a token and feed it back into the context; model parameters remain fixed |
| Observed-target scoring / evaluation | Blue | Evaluate the probability or log-probability assigned to an observed target; no parameter update |
| Training | Violet | Derive an objective, gradients, and parameter updates |

This mapping is a **scoped proposal, not yet a site-wide implementation contract**. Before adoption, reconcile it with existing meanings in this design system: green is the brand and main information-flow colour; violet currently identifies explicit learning-stage transitions. Do not let training and stage-transition violet become indistinguishable. Either revise the stage-transition treatment to a neutral dashed connector, or keep the three-way comparison labelled and use a different, validated visual encoding. Do not silently reuse one colour for unrelated meanings.

The shared computational trunk (context, forward pass, logits, softmax and conditional distribution) remains neutral. The three branches receive an accent only after the distribution, where their operational purposes diverge. Keep explicit labels; do not colour every operation or every page. Likelihood, loss, gradients and parameter updates are not part of ordinary generation.

### Data representations: shape and notation before colour

Do **not** assign a unique hue to every representation. The text → tokens → token IDs → embeddings → contextualized hidden states progression is better taught through changes in form, notation and explicit labels:

| Representation | Preferred visual encoding | Important distinction |
|---|---|---|
| Text | Neutral text/string container | Human-readable source content |
| Tokens | Preserve the text, but segment it into visibly bounded spans | Token boundaries are tokenizer-dependent; a token is not necessarily a word or character |
| Token IDs | Compact integer labels in a monospace or numeric style, aligned one-to-one with the displayed tokens | IDs are vocabulary indices, not semantic coordinates or embeddings |
| Embeddings | Vector/matrix notation, visible dimensions and (when useful) a compact vector-cell depiction; one restrained shared data accent at most | Learned dense numerical vectors obtained through an embedding lookup |
| Contextualized hidden states | Reuse the vector/matrix visual grammar, with a clear contextualization/layer marker | Representations transformed by the Transformer; not the original token embeddings |
| Logits and probabilities | Keep distinct mathematical labels and scales; show logits as unconstrained scores and probabilities as normalized values | Do not imply that logits are probabilities |

The same representation should retain the same visual form wherever it appears. A token ID must not change colour because it is used as a target; a vector must not change its data-type encoding because it is processed by an attention block.

Use colour only when it adds a real discrimination that shape and notation cannot provide. In most prose pages, show these distinctions inline through typography, delimiters, labels and equations; reserve coloured data objects for diagrams where readers must track a representation across multiple transformations. Do not add a legend to a page when only one representation is present.

### Composing the two dimensions

When a diagram needs to show both an operation and the data it manipulates:

- Encode **data identity** through shape, notation, labels and (only if necessary) a restrained representation accent.
- Encode **operation identity** through the branch treatment and its explicit label.
- Keep arrows neutral unless their direction or role is itself the instructional focus.
- Never make a data object's fill inherit the colour of the operation currently processing it.
- Avoid stacking multiple saturated fills, badges and outlines on the same node. Prefer one accent plus a clear label.
- Provide a textual explanation or legend; colour is never the only carrier of meaning.

For example, a blue scoring branch may consume a neutral token-ID target and compare it with a probability selected from the model's output distribution. The target remains a token ID; blue identifies the scoring operation, not the target's data type.

### Application and restraint

Apply this grammar selectively, not as a mass restyling exercise:

1. Introduce the representation sequence in the tokenization/embedding lesson, where the learner needs to understand the successive changes of representation.
2. Reuse it in the embedding and Transformer lessons only when tracking the same object across operations improves comprehension.
3. Use the computational-role accents in the shared prediction overview and dedicated generation, scoring and training explanations, after resolving the violet stage-transition collision.
4. Do not add colour keys to the learning map, every lesson header, code listings, or concept cards merely for consistency.
5. Prefer the existing design tokens and reusable diagram classes. Do not scatter literal hex values through lesson content.

### Acceptance criteria

A visual change is justified only if it improves at least one of these tasks: identifying the current representation, following a transformation, distinguishing an operation from its input/output data, or comparing the three operational branches. Review each candidate in French and English, on light and dark themes, at desktop and narrow-mobile widths, and in grayscale or a colour-vision simulation. Keep labels, mathematical notation, shapes and line styles sufficient to recover the meaning without colour.

## 3. Typography and layout

- Use a readable sans-serif for prose and a monospace face for code, identifiers, and compact technical metadata.
- Keep paragraphs at a comfortable measure (approximately 65–80 characters per line); allow diagrams, tables, and code to use wider containers when necessary.
- Use a clear heading hierarchy and consistent vertical rhythm. Avoid oversized headings inside dense technical sections.
- Equations need whitespace; define symbols and tensor dimensions before use.
- Code blocks should support copying, preserve readable line lengths, and remain usable on narrow screens.
- Cards should encode a meaningful action or content grouping, not merely decorate every paragraph.

## Visual grammar for knowledge and navigation structures

LLM Lab contains several connected models, but they answer different reader questions. Their visual identities must make those differences apparent before a reader follows a link. They share the site design tokens and typography; they do **not** share one generic breadcrumb, stepper, graph or card treatment.

| Structure | Reader question | Visual identity | Semantic boundary |
|---|---|---|---|
| **Document breadcrumb** | Where am I in the site? | Quiet, neutral hierarchy with compact chevron separators; derived from the Quarto sidebar. | Information architecture only; no learning order or prerequisite claim. |
| **Learning-stage membership** | Which learning stage(s) does this page serve? | Green, rounded stage labels grouped as a compact context/list; multiple memberships remain visible. No connecting arrows. | Membership is not a parent/child relation, transition or primary-stage assignment. |
| **Explicit stage transition** | What conceptual connection does this page explain between stages? | A separately labelled relationship, using a violet dashed connector and an explicit direction marker (`→` or `↔`) wherever a diagram is appropriate. Its purpose remains available as text. | An explanatory relation, never a prerequisite or an inferred next step. Violet is valid here only with a visible legend. |
| **Preferred next page** | What is the recommended next reading action? | A clear, solid-green action link/card with a forward cue; visually stronger than contextual metadata. | An editorial recommendation, not a required transition and not the only available route. |
| **Build walkthrough sequence** | Which implementation visit am I in, and what comes next locally? | Dark-green numbered connected stepper, with a stable local count and explicit previous/next actions. | Local implementation order only; never reuse Understand stage numbers or memberships. |
| **Canonical concept** | What is this notion, independently of a particular lesson? | Stable concept identity with a bilingual label/definition and visible domain context when useful; link to its canonical resources. | A concept is not a page: one concept may be explained by several resources and belong to several domains. |
| **Conceptual relation** | How are two canonical concepts related, and in which direction? | Typed relation vocabulary with a persistent legend, explicit arrow/direction and relation-family filtering. Keep the current domain-grouped concept browser as the default; do not force a global linear or DAG layout. | A typed knowledge relation, not a page link, curriculum membership or automatically inferred learning dependency. |
| **Page hierarchy** | How is this page structurally grouped within the documentation? | Neutral nested tree/indentation derived from the authored page hierarchy and reflected in the sidebar where applicable. | A parent/child page relation is structural; it does not by itself establish a conceptual relation or prerequisite. |
| **Curated related-page link** | Which other page is relevant alongside this one? | Quiet secondary text link, grouped as a related resource rather than a step or node in a sequence. | Relevance/association only; no direction, prerequisite or next-step claim unless separately declared. |
| **Preferred previous/next route** | What is the recommended continuation or return point? | Explicit directional navigation; the preferred next action receives the solid-green emphasis, while previous/secondary links remain quieter. | An editorial route edge, not a conceptual relation or mandatory curriculum transition. |
| **Exploratory resource map** | What pages and resources can I explore across the site? | Neutral, hierarchical or branching overview with a clear distinction between navigation areas and page resources. | The map supports discovery; its layout/order does not imply conceptual relations or prerequisites. |
| **Page-local process / meta-flow** | What happens to the data or computation inside this explanation? | Explicit source → operation → result nodes; use branches, comparisons or loops when the process actually has that topology. | A domain-specific computational/process model, not a site breadcrumb or universal learning sequence. |
| **Inline concept link** | Where can I understand this term more deeply? | Subtle dotted underline on the first useful contextual occurrence. | A contextual affordance to a canonical explanation, not a metadata badge or graph edge displayed inline. |

### Shared rules

- **Meaning before colour.** Every structure must retain a textual label and a recognisable shape/connector convention. Colour reinforces meaning; it never carries the distinction alone.
- **One source of truth per model.** Render each projection from its existing canonical source (`data/concepts.yml`, `data/guided-route.yml`, page metadata and Quarto sidebar as appropriate). Do not create a second registry to drive styling.
- **No semantic promotion by presentation.** A stronger colour, arrow, number or position must not turn membership into sequence, a link into a prerequisite, or an explanatory transition into a required route.
- **Keep the layers composable.** A page may legitimately show its document location, several learning-stage memberships, an explained stage transition and a preferred next page together. Give each its own label and visual treatment rather than merging them into a synthetic breadcrumb.
- **Use diagrams only when topology matters.** A list or compact relationship panel is preferable when a spatial graph adds no useful task. Do not draw connectors merely to make a model look more graph-like.
- **Progressive disclosure.** Show the smallest useful context by default; reveal relation descriptions, optional branches and detailed inventories on demand. Preserve a textual alternative.
- **Bilingual parity.** Labels, direction markers, legends and explanatory purpose must remain equivalent in French and English, including long-label wrapping.
- **Validation is model-specific.** Test source semantics, generated projection, rendered appearance and learner interpretation separately. A successful build does not prove that readers distinguish these structures.

This grammar is a contract for future refinements, not an instruction to restyle every existing component in one pass. Apply it incrementally in the owning navigation, concept-graph and process-diagram work; preserve already validated behaviours unless a concrete defect is demonstrated.

## Navigation hierarchy

Every page reached through the Quarto sidebar should expose a compact **breadcrumb** above its title. It is generated from the active sidebar hierarchy, so the labels and nesting remain aligned with the actual site navigation in both languages. The breadcrumb answers “where am I?”; it is not a claim that readers must follow every parent page in sequence.

The global navbar is the **primary task-oriented wayfinding layer**, limited to four stable learner intents: learning paths, understanding, building, and practice. It is language-aware (FR/EN) and should remain compact. The sidebar is the **secondary detailed information architecture** for topic-level navigation; it may be rich and hierarchical because it serves readers who already have a subject in mind. Do not duplicate the full sidebar in the navbar, and do not make references the only global entry point. Search and the language switch remain utility actions.

Keep navigation patterns distinct:

- **Breadcrumb:** the page's location in the site's information architecture; generated globally from the sidebar.
- **Sidebar:** the wider topic map and alternative entry points.
- **Previous / next navigation:** a suggested local continuation, where the metadata defines a useful route.
- **Pipeline stepper:** a domain-specific process or data-flow sequence inside a lesson. Use it only when the stages form a meaningful process; it is not a substitute for the breadcrumb and must not imply a universal learning order.

Do not manually reproduce breadcrumb markup in individual pages. If the sidebar hierarchy changes, the breadcrumb should follow it automatically. Pages that are not represented in the sidebar (for example, a standalone reference page) may legitimately have no breadcrumb.

## Reader-facing metadata and concept emphasis

Page-classification metadata is not part of the reading interface. The controlled `type`, `destination`, `topic`, `level`, `language`, `status`, and `domain` values remain in the source and generated data for tools, filters, search, and graph construction. Do not display their raw identifiers as chips, badges, a metadata strip, or a tag cloud. This is a presentation rule, not a reason to delete or weaken the metadata contract. The Quarto `keywords` field currently mirrors these controlled tags for machine-readable HTML metadata, but Quarto also renders it in the title block by default. The site therefore overrides the version-pinned `title-metadata.html` partial to omit only the visible keywords section; keep the front-matter keywords and page-map tags synchronized. The HTML `<meta name="keywords">` element remains available to machines.

Show reader-facing orientation only when it has a concrete pedagogical purpose. Use natural language (for example, “Prerequisites”, “What you will learn”, or “Optional deep dive”) rather than exposing internal field names. Reuse existing callouts and page patterns; do not add a uniform metadata panel to every page.

Scientific and technical terms may be highlighted in the prose when they help readers recognize an important concept. Prefer a contextual inline link to the canonical explanation, with emphasis at the first useful occurrence. Use the existing `concept-link` class for a subtle, consistent treatment where a distinction from ordinary navigation links is useful:

```markdown
[attention croisée](cross-attention.qmd){.concept-link}
```

The link should resolve to a useful explanation, not merely to a page that happens to mention the term. Keep the definition or essential qualification in the current page when needed for comprehension. Avoid repeated highlighting, keyword clouds, decorative pills, and links on every occurrence. The bilingual concept registry in `data/concepts.yml` is the vocabulary reference; it does not require every associated concept to be displayed on every page.

The goal is to make concepts easier to recognize and explore without turning the prose into an index.

## Callout semantics

Use the same Quarto callout types for the same reader need, but do not require every page to contain the same number of callouts.

- **Tip:** a compact mental model or the essential point to retain. The recurring “one-minute” callout belongs here when it genuinely helps the reader orient.
- **Note:** a clarification, distinction, assumption, or contextual qualification that should remain visible without interrupting the main explanation.
- **Warning / caution:** a likely error, limitation, or condition that could materially change the reader's interpretation.
- **Important:** a constraint or consequence that must not be missed.
- **Collapsed note:** genuinely supplementary material such as implementation references, extended derivations, or optional detail—not an essential definition or caveat.
- **Learning outcomes:** use the shared `.callout-note.learning-outcomes` pattern only when explicit outcomes help the reader; keep it collapsed by default.
- **Comprehension check:** use the dedicated `.self-check` structure, not a generic callout, and keep answer disclosures collapsed.

A chapter lead states the page's central answer; it is not interchangeable with a callout. Avoid stacking multiple boxes that repeat the same idea. The target is consistent semantics and visual treatment, not identical page composition.

## 4. Interaction and motion

For the composition of a complete explanatory lesson that combines a motivating question, worked example, meaningful learner action, mechanism visualization and evidence-aware synthesis, use the [interactive explanatory lesson pattern](interactive-explanatory-lesson-pattern.md). It composes this design system; it does not define a new visual language or require every page to become interactive.

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
