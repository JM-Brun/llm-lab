# Guided-route pattern coherence — page-by-page re-walk

**Date:** 2026-11-09  
**Scope:** source-level re-walk of the eight-stage guided route (18 core page pairs) on `main` (24bf1ead), after #717 and #722. This pass verified the continuity of the FR/EN suggested-route chains, the membership of every stage page, FR/EN parity of outgoing links, and the presence of shared page-contract cues (chapter lead, one-minute model callout, self-check closure, in-body connections). It is a pattern-coherence pass: scientific content correctness evidence remains in the existing inventory slices and is not repeated or re-certified here.

## Confirmed before this change

1. The FR and EN suggested-route chains are continuous from the landing pages to `gradients`, with no gap, cycle or cross-language divergence, and agree with the stage membership declared in `data/guided-route.yml`.
2. Every core and optional route page exists in both languages; the generation and cross-entropy membership overlaps (orientation/inference, scoring/training) are intentional and rendered as multiple stage contexts.
3. Sixteen of the eighteen core pairs carry a self-check closure. `positional-encoding` and `tokenization-strategies` are the only two without one, and also the only two whose in-body links do not connect to their route neighbours: positional-encoding links only to the RoPE deep dive; tokenization-strategies links back to text-data but not forward to embedding-space.
4. The EN generation page titles its one-minute callout "The idea to remember in one minute", while the eight other EN pages that carry the cue use "The one-minute mental model"; the FR title is uniform ("L'idée à retenir en une minute").
5. `.gitignore` ignores `site/includes/generated-guided-context-*.qmd` but not the sibling `generated-suggested-route-*.qmd` fragments emitted by the same build step.
6. Pattern-drift observation recorded for a decision, not changed here: the one-minute model callout appears on 9 of 18 core pairs; entropy, likelihood (vraisemblance) and cross-entropy currently lack it, while loss and gradients carry it.

## Changes in the accompanying pull request

- Added an in-body route-connections section and a self-check closure to positional-encoding (FR/EN), linking the embedding-space predecessor, the contextualized-representations successor, the causal-masking structural constraint and the Transformer exercise collection.
- Added an in-body route-connections section and a self-check closure to tokenization-strategies (FR/EN), linking the text-data predecessor, the embedding-space successor, the two optional deep dives and the text-data exercise collection (which already contains the TR-E BPE merge-trace exercise based on this page).
- Harmonized the EN generation one-minute callout title with the eight other EN pages.
- Added the missing `site/includes/generated-suggested-route-*.qmd` pattern to `.gitignore`.

## Validation status and limits

- All question and answer statements are derived from each page's own audited content (counterexamples section, tokenizer-training versus inference encoding, RoPE insertion point, causal-mask visibility constraint); no new claim, figure, or external dependency is introduced.
- Delegated to CI on the pull request: page metadata checks, `check_site_links`, Quarto render including guided-context and suggested-route fragment generation.
- Not established by this pass: rendered inspection of the new sections at desktop/mobile widths, manual screen-reader behaviour, learner validation. The rendered review remains owned by #337 and the page-group source audit by #584; the learner pilot by #447.
## Follow-up: pattern closure (2026-11-09, later same day)

The drift recorded in point 6 above was resolved in two steps. First, #754 added the one-minute callout to entropy, likelihood (vraisemblance) and cross-entropy, bringing coverage to 16/18 core pairs. Then #790 closed the last two pairs: `llm-overview` gained the standard callout after its chapter lead, and `tokenization-strategies` had its "À retenir"/"Key takeaways" section converted into the standard callout (same five bullets, uniform title, added self-check question). The one-minute mental model cue now covers 18 of 18 core page pairs in both languages. The audit above remains a dated snapshot of `main` at 24bf1ead and was not rewritten.
