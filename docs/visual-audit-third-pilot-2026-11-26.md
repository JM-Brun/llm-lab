# Visual audit pilot — representations and Transformer architecture (2026-11-26)

**Scope:** EN/FR Understand lessons for embedding lookup, contextualized representations and the Transformer architecture.  
**Status:** source-level review and responsive source changes completed; Quarto build and browser rendering remain unverified.

## Decisions

| Lesson | Existing support | Decision | Why |
|---|---|---|---|
| Embedding space | Ordered ID/row/vector table, an illustrative lookup figure, matrix dimensions and a worked lookup exercise | **Keep the figure; add a mobile composition** | The visual makes the crucial distinction between an integer row address and the vector stored in that row. Its wide 1120 px layout would make labels too small when scaled to a phone. The mobile version stacks prefix → ID → selected matrix row → vector → point in vector space. |
| Contextualized representations | A core comparison of two occurrences with one assumed shared ID and different accessible contexts; a separate pipeline figure hidden in a collapsed callout | **Keep the semantic contrast; add a mobile composition; remove the redundant collapsed pipeline** | The two-context figure explains the page's actual learning objective: same lookup, different context, potentially different hidden states. The collapsed text→IDs→lookup→position→Transformer pipeline repeats the preceding/following lessons and the Transformer architecture page, without adding a distinct claim. Its external article reference is preserved as a text resource; the local pipeline asset is not deleted. |
| Transformer architecture | A detailed 900×1500 architecture/block diagram and a separate 1200×560 end-to-end GPT generation flow | **Keep both; add mobile compositions** | They answer different questions: the first shows the network and one common pre-LN block; the second locates that network in the complete autoregressive loop. The wide second diagram would become unreadable on a narrow viewport. Mobile variants preserve the distinction. |
| Cross-page position semantics | The desktop GPT flow used the shorthand “embeddings + position” | **Clarify wording** | The shorthand could imply that all architectures add a position vector to embeddings. The label now says “positional mechanism”; the page's explanation that RoPE acts on Q/K remains consistent. |

## Changes made

### Embedding lookup

- Added EN/FR mobile variants and responsive `picture` embeds.
- Preserved the original desktop figure and its central distinction: ID = row address; vector = contents of the row; point = geometric interpretation of that vector.
- The mobile diagram makes the selected row explicit and keeps the row address distinct from the vector-space point.

### Contextualized representations

- Added EN/FR mobile variants for the existing same-lookup/different-context figure.
- The mobile layout shows two context examples converging on the same assumed lookup, then branching into separate Transformer computations and potentially different hidden states.
- Corrected the diagram so the two context paths enter the shared lookup without crossing the second context card; after lookup, the two computations are shown as parallel branches.
- Removed the collapsed pipeline image from the lesson because it repeated the conceptual path already established across the text-data, embedding and Transformer lessons. The optional external article reference remains as text.
- No existing SVG was deleted; the now-unembedded pipeline assets remain in the repository pending the normal asset lifecycle review.

### Transformer architecture

- Added EN/FR mobile variants for the detailed decoder-only GPT / pre-LN block diagram.
- Added EN/FR mobile variants for the end-to-end GPT data-flow diagram.
- Preserved the distinction between architecture and generation process.
- Mobile block labels state the residual additions explicitly: input plus attention output gives the intermediate state H′, then H′ plus MLP output gives the block output.
- Clarified the input stage as “initial representations” and added an explicit note that positional handling depends on the architecture. This avoids implying that positional information is always added at the input; the exact injection point remains architecture-dependent.

## New assets

- `embedding-lookup-en-mobile.svg`
- `embedding-lookup-fr-mobile.svg`
- `contextualized-embeddings-en-mobile.svg`
- `contextualized-embeddings-fr-mobile.svg`
- `gpt-data-flow-en-mobile.svg`
- `gpt-data-flow-fr-mobile.svg`
- `transformer-stack-en-mobile.svg`
- `transformer-stack-fr-mobile.svg`

All eight files were authored for this contribution and include SVG `title` and `desc` elements. They contain no embedded raster image, script, foreignObject or external href. These source checks do not establish XML conformance, rendered accessibility, owner provenance confirmation or a licence. Owner confirmation and asset-level licensing remain pending under the existing #156/#163 contracts.

## Source-level validation completed

- EN/FR source pages inspected and paired.
- All eight mobile assets are referenced from the matching language page through `picture` elements.
- Each affected figure has one page-level alternative text and one caption.
- The mobile contextualization figure shows two separate computation branches from one shared lookup.
- The mobile Transformer block labels both residual additions explicitly.
- The mobile Transformer and GPT-flow diagrams use “initial representations” and separately state that positional handling depends on the architecture.
- The redundant collapsed context pipeline is no longer embedded in the core lesson; its source asset is retained.

## Not yet validated

1. Run the normal Quarto build and resolve any source, HTML or asset-path issues.
2. Inspect all six EN/FR pages at desktop and narrow mobile widths, including SVG text size, French wrapping, diagram height, line breaks and caption wrapping.
3. Inspect the accessibility tree; verify that the page alt text, SVG title/description and caption are not announced redundantly.
4. Verify that the two contextualized branches and both residual additions are legible and unambiguous in the rendered mobile diagrams.
5. Confirm owner provenance for all eight new SVGs and record the separate asset-level licence decision.
6. Decide through the normal asset lifecycle process whether the now-unembedded contextualization-pipeline SVGs should remain as reusable reference assets or be marked as retired; do not delete them merely because one embed was removed.

## Remaining route-wide work

This pilot covers three lesson groups only. It does not close #1729. Continue with the remaining prediction and inference lessons (logits, probabilities, entropy, generation, in-context learning), then revisit the training-loop figures. The review must consider both the individual diagram and the page/route sequence: repeated examples, notation, visual grammar, figure placement, desktop/mobile legibility and whether each visual contributes something the adjacent prose, equation or table does not already teach.
