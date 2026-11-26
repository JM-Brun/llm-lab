# Visual audit pilot — four core Understand lessons (2026-11-26)

**Scope:** French and English lessons for likelihood, loss, gradients and context engineering.  
**Purpose:** apply the [pedagogical visual design and review process](pedagogical-visual-design-process.md) to the four highest-priority gaps identified in the source-level route audit.  
**Status:** figures integrated in source; Quarto build and browser rendering have not yet been verified.

## Decision summary

The audit selected four figures because each addresses a distinct learner difficulty not adequately resolved by the existing visual inventory. The decision was not to add a generic illustration to every page.

| Lesson | Observed gap before this change | Chosen visual | Exact placement | Why it earns its place |
|---|---|---|---|---|
| Likelihood / Vraisemblance | The page had a stepper and equations, but no visual trace showing that each target is scored under a longer observed prefix. | Three-step conditional-scoring trace: prefix → observed target → conditional probability, followed by product and sum of log-probabilities. | Immediately after the three-token worked probability product, before the transition to NLL. | Makes the chain-rule structure concrete and prevents the common but incorrect reading that token probabilities are independent or that scoring feeds model-generated tokens back into the prefix. |
| Loss | The page explained target alignment, causal visibility, ignored positions and the valid-token denominator in prose, but had no visual comparison of the two masks. | Two-panel comparison: triangular causal attention mask versus a separate target-inclusion mask; the latter feeds a mean over valid positions only. | After the section explaining causal masking, shifted targets and the distinction between attention and loss masks; before teacher forcing. | Makes the two masks' different jobs visually explicit and shows why ignored positions leave both numerator and denominator. It complements, rather than repeats, the one-token cross-entropy figure. |
| Gradients | The page had the relevant equations and an SGD worked example, but no representation connecting the forward computation, backward derivative flow and optimizer update. | Forward path from parameters to loss; backward path from loss to logit gradients and parameter gradients; optimizer update in a separately labelled final stage. | After the chain-rule explanation and before “From gradient to parameter update”. | Exposes the dependency graph and the direction of derivative propagation while preventing the conceptual conflation of gradient computation with parameter mutation. |
| Context engineering | A useful three-row table already distinguished system context, input sequence/window and position-accessible context, but the distinctions were not spatially connected. | Four-stage diagram: available application sources → selection/organization → supplied input sequence → causal access at position t. | Immediately after the three-level context table and before the contextualized-representations link. | Turns the table's three levels into a traceable construction, while retaining the critical facts that stored data need not be sent and future positions remain inaccessible to a causal query. |

## Design decisions and constraints

### Likelihood

- Reuse the page's existing illustrative conditional probabilities: 0.6, 0.5 and 0.8 (French decimal comma in the FR asset).
- Label each probability with its own observed prefix: c; (c, x₁); (c, x₁, x₂).
- Show both equivalent views: product for likelihood and sum for log-likelihood.
- State that the prefix is extended with reference tokens and parameters remain fixed.
- Do not depict sampling, a generated-token feedback loop, or an independence assumption.

### Loss

- Use a small 3×3 causal visibility matrix and a distinct four-position target mask with three valid targets and one ignored PAD position.
- Show the valid-position mean explicitly: (ℓ₁ + ℓ₂ + ℓ₃) / 3.
- State that the loss mask excludes an ignored target from the numerator and denominator.
- Preserve the page's scientific caveat: a zero/directly ignored loss contribution does not by itself prove that the token's representation cannot influence another valid position. Attention visibility is a separate dependency.
- Do not reproduce the cross-entropy page's existing comparison of −log p(y) at p(y)=0.9 and p(y)=0.1.

### Gradients

- Use separate visual directions for the forward values and backward derivatives.
- Show the chain-rule stage between logit gradients and parameter gradients.
- Keep the optimizer/update in a separate box, explicitly labelled as a distinct operation.
- The displayed SGD expression is an example update rule, not a claim that all optimizers use plain SGD.
- Do not imply that a gradient guarantees a globally decreasing objective for an arbitrary step.

### Context engineering

- Represent source availability, system-side selection/organization, the sequence actually supplied, and per-position causal access as distinct levels.
- Include selection, filtering/verification, prioritization, summarization/updating and role structuring.
- Mention that the context window is a token budget, not an instruction to fill it.
- Do not present RAG, memory or tools as synonymous with context engineering, and do not depict every stored source as automatically transmitted.

## Asset and page integration

Each figure is authored as a project SVG, with French and English variants and separate desktop/mobile layouts:

- `likelihood-en.svg`, `likelihood-en-mobile.svg`, `likelihood-fr.svg`, `likelihood-fr-mobile.svg`
- `loss-en.svg`, `loss-en-mobile.svg`, `loss-fr.svg`, `loss-fr-mobile.svg`
- `gradients-en.svg`, `gradients-en-mobile.svg`, `gradients-fr.svg`, `gradients-fr-mobile.svg`
- `context-engineering-en.svg`, `context-engineering-en-mobile.svg`, `context-engineering-fr.svg`, `context-engineering-fr-mobile.svg`

The page embeds each desktop SVG through a `picture` element with a mobile source selected at 600 px. Every page has a page-level alternative text and a caption stating the main takeaway and a relevant caveat. The SVGs include `title` and `desc` elements.

No external illustration was copied. The artwork is newly authored for these lessons from the concepts, examples and equations already present in the pages. This contribution record is evidence of how the diagrams were designed; it is not an asset-level licence grant. Owner provenance confirmation and a separate asset-licensing decision remain governed by the existing project contracts (#156 and #163).

## Validation completed

- Source pages inspected in both languages.
- Existing figures and visual register inspected to avoid duplicating the one-token cross-entropy illustration or the existing training-loop optimizer visual.
- Each diagram checked against the relevant page's formulas and terminology at source level.
- Desktop and mobile SVG variants created for all four lessons.
- Page references, captions and alternative text added to all eight FR/EN lesson pages.
- English decimal notation checked in the likelihood figure.
- The gradient diagram's backward arrow was corrected to flow from the loss to the logit gradient before the chain-rule and parameter-gradient stages.

## Validation still required

This is not yet a rendered visual audit. Before treating the work as complete:

1. Run the project's normal Quarto/site build and resolve any Markdown/HTML or asset-path issues.
2. Inspect all eight rendered lesson pages at desktop and narrow mobile widths; confirm the `picture` source switch, text legibility, clipping, whitespace, figure scaling and caption wrapping.
3. Inspect the rendered DOM and accessibility tree; verify that the image alternative text is exposed once, captions are associated correctly and no duplicate title/description is announced undesirably.
4. Check the diagrams against the surrounding equations and prose in the rendered page, not only the SVG source.
5. Check FR/EN visual parity and long-label wrapping.
6. Confirm authorship/provenance with the repository owner and decide an explicit asset-level licence under the existing asset policy.
7. Record build, browser, viewport and accessibility evidence in the PR before marking the issue complete.

## Remaining route-wide work

This pilot closes only four source-level figure gaps; it does not close the route-wide visual audit in [#1729](https://github.com/JM-Brun/llm-lab/issues/1729).

- Audit every remaining core Understand page and its immediate route neighbours in FR and EN, including whether the existing visual is the right form, placed at the right point and doing work the prose/equations do not already do.
- Revisit the visual priorities from the initial audit: text → token → ID trace; whether absolute-position/RoPE comparison belongs in the main lesson rather than only optional material; the distinction between mathematical dense attention and IO-aware FlashAttention; and whether the cross-entropy curve or training-loop optimizer comparison adds value at its current level of prominence.
- Inspect visual continuity across page groups, not only individual pages: repeated token examples, notation, color semantics, mask semantics, and the separation of conceptual maps, computation diagrams, architecture diagrams and curriculum navigation.
- Complete rendered desktop/mobile inspection for the entire canonical route.
- Reconcile all new SVGs with the recursive asset inventory and provenance/licensing register.

A figure should be revised or removed if rendered inspection shows that it adds no distinct explanatory value, is too small to read, conflicts with the prose, or makes an unsupported scientific claim. The existence of a newly authored asset is not a reason to keep it.
