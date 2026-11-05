# Visual route continuity audit — steppers, route context, and nested routes

**Audit date:** 2026-11-05  
**Status:** continuity scan complete on the deployed site and current `main`; corrective slice proposed in this PR; rendered browser, accessibility, and learner validation remain open.  
**Contract:** [Pedagogical breadcrumb and page-navigation contract](pedagogical-breadcrumb-and-page-navigation-contract.md)  
**Coordination:** #337, #368, #415; implementation PRs #522, #524, #528, #531, #534.

## 1. Method and evidence boundary

- Text-level scrape of every published French page (51 pages; one fetch was blocked by an extraction filter and that page was inspected at source level instead), plus targeted English parity checks on the source tree.
- Source inspection of every page referenced by `data/guided-route.yml` (18 core members plus optional members), both languages, for the three page-level navigation treatments: the generated guided-route context include, the legacy `pipeline-stepper` block, and the `route-nav-cards` block.
- The deployed site matched `main` at `d6c5f9f`: the steppers retired by #524 are absent in production, the generated multi-membership context on `generation` renders, and every remaining stepper is present in both places.
- Limit: the single-membership context renders inside a `<nav>` landmark that text-only extraction does not expose; rendered evidence for the chip comes from the Chromium review (#531/#534), which this PR extends. This scan validates source structure and deployment alignment, not accessibility or learner comprehension.

## 2. Cue coverage before this correction

18 core route pages; FR = EN throughout.

| Treatment | Pages |
|---|---|
| Generated guided-route context | llm-overview; generation (two labelled contexts); embedding-space; queries-keys-values |
| Legacy five-stop stepper | scaled-dot-product-attention; causal-masking; logits; cross-entropy |
| Local stepper, retained (§12.1) | text-data |
| No page-level cue | tokenization-strategies; positional-encoding; contextualized-representations; transformer; probabilites; vraisemblance; loss; gradients; evaluation-experimentale |

`route-nav-cards` exist only on queries-keys-values, scaled-dot-product-attention, causal-masking and logits (plus the guided-build pages). cross-entropy carried a stepper but no cards, and the whole prediction → learning tail (probabilites → vraisemblance → cross-entropy → loss → gradients) showed no visual transition cue, although every page carries `suggested_route` metadata. The visual thread therefore appeared and disappeared four times along the route.

## 3. Complete pipeline-stepper inventory

The §8 inventory of the pilot audit was a bounded four-occurrence sample (embedding-space and queries-keys-values, FR/EN, retired by #524). The exhaustive scan found ten remaining occurrences on `main`:

1. `site/fr/text-data.qmd`, `site/en/text-data.qmd` — the local four-stop text-to-representation stepper; **retained** per the §12.1 decision (no generated cue stacked above it).
2. `site/{fr,en}/scaled-dot-product-attention.qmd`, `site/{fr,en}/causal-masking.qmd`, `site/{fr,en}/logits.qmd`, `site/{fr,en}/cross-entropy.qmd` — the same five-stop chain condemned in §8, with identical defects:
   - from `logits` and `cross-entropy`, the step-3 link points to `queries-keys-values`, silently skipping scaled dot-product attention and causal masking;
   - the step-5 link points to `cross-entropy`, silently skipping probabilities and likelihood;
   - the step-3 label differs across pages for what the chain presents as the same step (étape 3 libellée «Attention à produit scalaire», «Masque causal & Attention» ou «Attention (Q, K, V)» selon la page).

## 4. What the cues must express: nested routes

The guided route is not a five-step pipeline. It is a six-stage sequence in which each stage holds several pages, and nesting is legitimate in exactly two sanctioned forms:

- a page that carries its own local sub-pipeline nested inside the route — text-data and its four-stop input sequence is the one retained example (§12.1);
- a page with several stage memberships — generation appears first in orientation as a black-box preview and again in prediction as a deliberate return; it is shown as labelled contexts, never as a single fabricated parent.

The Build path (G0–G9 milestones) and the Practice sequence are separate routes and deliberately receive no conceptual cue. The retired five-stop stepper flattened this nested structure into one false linear chain; the generated cue expresses the real structure.

```mermaid
flowchart TB
  subgraph ROUTE['Parcours guidé — six étapes (data/guided-route.yml)']
    direction TB
    subgraph S1['01 · Situer le système']
      A['llm-overview — cue généré']
      B['generation — cue généré, deux contextes']
    end
    subgraph S2['02 · Du texte aux tokens']
      direction LR
      subgraph LOC['Sous-pipeline local de text-data (conservé, §12.1)']
        direction LR
        C1['Texte, tokens et IDs'] --> C2['Embeddings'] --> C3['Information positionnelle'] --> C4['Représentations contextualisées']
      end
      D['tokenization-strategies — aucun repère']
    end
    subgraph S3['03 · Des identifiants aux représentations']
      E['embedding-space — cue généré']
      F['positional-encoding — aucun repère']
      G['contextualized-representations — aucun repère']
    end
    subgraph S4['04 · Comprendre le calcul du Transformer']
      H['transformer — aucun repère']
      I['queries-keys-values — cue généré']
      J['scaled-dot-product-attention — stepper remplacé par cue (cette PR)']
      K['causal-masking — stepper remplacé par cue (cette PR)']
    end
    subgraph S5['05 · Des états aux prédictions']
      L['logits — stepper remplacé par cue (cette PR)']
      M['probabilites — aucun repère']
      N['vraisemblance — aucun repère']
      B2['generation (retour) — cue généré, deux contextes']
    end
    subgraph S6['06 · Apprentissage et évaluation']
      O['cross-entropy — stepper remplacé par cue (cette PR)']
      P['loss — aucun repère']
      Q['gradients — aucun repère']
      R2['evaluation-experimentale — aucun repère']
    end
    S1 --> S2 --> S3 --> S4 --> S5 --> S6
  end
```

Optional stage members (transformer-architectures, llm-limits, unicode-text, tokenizer-design-evaluation, tensors, rope, cross-attention, decoding-strategies, scaling-laws) are omitted from the diagram for readability; none currently carries a cue.

## 5. Decision applied in this PR

- Retire the eight remaining five-stop steppers: removal only, no relabelling — the §8 rationale (omission is less misleading than a false curriculum).
- Add the generated single-membership guided-route context to the four affected lessons, FR and EN, mirroring the #524 + #528 sequence.
- Extend `scripts/site-browser-review.mjs` so the Chromium route-context audit covers all ten guided-context pages and asserts zero legacy steppers on the four corrected lessons.
- Record this audit; add §14 to the pilot audit; close the §5 and §11 stepper-inventory checkboxes at source level; correct the dangling references to PR #532 (the corrective change merged as #534).

## 6. Remaining rollout (owner decisions)

- Generated cue for the nine still-silent core pages and for optional members, after the rendered review of this correction.
- Route cards for the prediction → learning tail so suggested transitions stay visible after `logits`.
- §11 rendered/accessibility/learner validation; #535 accessibility follow-up.

## 7. Honest limits

- No local render, CI, or browser execution in the audit environment: CI (local links, Quarto render, membership tests) must run on this branch, and the extended browser review needs the deployed site.
- FR/EN parity verified at source level for the eight modified pages; no other content changed.
- This scan does not establish that the cue helps learners; the contract requires an external learner check before the pilot is declared complete.
