# Understand path — readability rewrite (design)

**Status:** approved by the maintainer on 2026-11-10, then revised the same day (see “Revision” below). Implemented so far: `llm-overview` and `generation`, French and English.
**Date:** 2026-11-10
**Scope:** the 19 pages of the "Comprendre les LLM" sidebar section, French and English.
**Related:** [reader review of 2026-11-10](../../reviews/understand-path-reader-review-2026-11-10.md),
[editorial method](../../reader-experience-and-editorial-method.md),
[contributor principles](../../contributor-guiding-principles.md),
[navigation contract](../../pedagogical-breadcrumb-and-page-navigation-contract.md).

## Revision of 2026-11-10 (after main moved)

While this design was being written, `main` gained 55 commits that change its premises. Where
this section and the rest of the document disagree, this section wins.

- **Anchor example.** `docs/meta/learning-example-otis.md` is now the source of truth for the
  running example: the prefix « C'est une bonne situation, ça, scribe ? » in French, the *Life
  of Brian* question in English, each with an original continuation for calculations. The
  maintainer chose to align on it. The "avocat" / "bank" pair of sections 3 and 4 is dropped,
  except as a possible declared variant where a page needs an ambiguous word
  (`contextualized-representations`).
- **Number chain.** Section 5 keeps its structure and its values; only the tokens change. After
  the prefix, the made-up candidates are « Être » 0.6, « Vous » 0.2, « Oui » 0.1, « Non » 0.1
  (English: “They”, “Aqueducts”, “Nothing”, “Well”). The three observed tokens used for
  scoring are « Être », « scribe », « , » with probabilities 0.6, 0.5, 0.8 (English: “They”,
  “built”, “roads”): product 0.24, NLL about 1.43 nats, mean about 0.48 nat per token. Values
  are labelled as made up, as rule 5 of the Otis document requires.
- **Exercises.** Lesson questions now live on dedicated pages under
  `site/<language>/exercises/`. Cue 7 of section 7 becomes: a lesson links to its exercise
  page; an embedded check is kept only where the page already has one, placed before the
  generated route block, never after the language switch.
- **Steppers.** The flow steppers added at the top of path pages are kept as they are.
- **Content added on main** (inference latency, context budget, result validity, and so on) is
  preserved; it is re-voiced, not removed.
- **Math delimiters** are `$…$` and `$$…$$` site-wide.
- **Way of working.** Several sessions edit these pages in parallel. Each batch is therefore
  one or two pages, started from the `main` of the moment, and offered as a small pull request.
  Pages with an open pull request are left alone until it is merged. The order of section 10 is
  indicative only.
- **Conventions batch** ("la softmax", "entropie croisée", "perte") is not applied yet on
  `main`; it needs its own small pull request because it touches about twenty pages.

## 1. Intent

The maintainer's judgement: the path holds very good information but reads as less coherent,
consistent, harmonious and teachable than comparable explainers. Some elements and some
transitions do not feel natural. The goal is a path that is more pleasant and more logical to
read, with the same rigour and the same organisation (Understand, Build, Deepen, Practice).

The diagnosis after reading the pages:

1. **No running example.** The overview opens on one sentence and drops it. Every later page
   brings its own toy (`chat` / ID 17, English `bank`, `it` / `the animal`, anonymous NumPy
   matrices, tokens A to D).
2. **No shared numbers.** `probabilites` uses (0.25, 0.75), `entropy` uses (0.5, 0.5) and
   (0.9, 0.1), `vraisemblance` uses (0.5, 0.25, 0.8). Nothing computed on one page is reused on
   the next. `logits` and `scaled-dot-product-attention` have no worked number at all.
3. **Defensive voice.** Leads and summaries state what a thing does not guarantee before the
   reader knows what it does. The same warning (normalised is not calibrated is not true; a
   weight is not a cause) is repeated on five or more pages.
4. **Pages that describe themselves.** "Cette page apparaît une première fois…", "Frontières
   entre les pages", "Où se situe cette étape dans le parcours ?", "Liens avec les autres
   concepts", "Complément côté Build". These break the project's own editorial-economy rule.
5. **Uneven cues.** Opening blocks, learning outcomes, self-checks and endings differ page to
   page without a reason (items C and D of the reader review).
6. **Broken joins.** `generation` is page 2 and uses logits, softmax and the KV cache before a
   token has been shown. `text-data` never shows a sentence actually split into tokens.

What the readable explainers have in common (Understanding AI, Transformer Explainer, Google ML
Crash Course, Hugging Face, madewithlove, IBM; two Medium pages and llm-visualized could not be
read): one anchor sentence reused at every stage; a problem or limit before each mechanism; a
caveat said once, where it applies; an explicit "you can skip this"; one analogy per concept.

## 2. Goals, non-goals, anti-goals

**Goals**

- One anchor example carried through all 19 pages.
- One chain of numbers from `logits` to `gradients`, each page starting from the previous
  page's result.
- Each page opens on the question the previous page left open.
- Affirmative explanation first; each scientific reservation kept, stated once, at the point
  where it applies.
- No sentence about the page or the site. Links sit where the concept is used.
- The same reader cues on every page, in the same order.
- French and English changed together, equivalent in substance.

**Non-goals**

- No change to the four destinations, the route order in `data/guided-route.yml`, the sidebar,
  file names or URLs.
- No new page, no split page, no deleted page.
- No rewrite of Build, Deepen or Practice pages. They are touched only where a rename
  (softmax gender, "perte") or a changed anchor forces it.
- No new component, no page-specific styling.
- No new scientific claim. Existing claims, sources and formulas stay.

**Anti-goals** (failure even if the result reads well)

- Rigour traded for fluency: a dropped assumption, a caveat removed rather than moved, a
  number that does not recompute.
- A universal lesson template with empty or forced sections.
- New meta-discourse replacing the old ("In this section we will…").
- An end-of-page list that repeats the menu or the route.
- FR and EN drifting apart.

## 3. Decisions taken by the maintainer

| Decision | Choice |
|---|---|
| Anchor example | The "avocat" pair (section 4) |
| `generation`, used at stages 01 and 06 | Restructure in place; do not split |
| Gender of "softmax" in French | Feminine: "la softmax" |
| "loss" or "perte" in French titles and prose | "perte"; "loss" introduced once, then kept for code and API names |

## 4. The anchor example

**French.** Two prompts with the same ending and a different left context:

- « Dans la salade, l'avocat est bien » → expected continuation « mûr »
- « Au tribunal, l'avocat est bien » → expected continuation « préparé »

Why this pair: "avocat" is one written form with two senses; the disambiguating word comes
*before* it, so a causal model can use it; the last three words are identical, so every
difference in the output distribution comes from the left context.

**English.** "avocat" does not translate. The English pages use a pair with the same
structure — one form, two senses, the cue on the left, an identical ending — and the same
numbers. Proposed: "By the river, the bank was" → "steep" and "After the crash, the bank was"
→ "closed". This is a builder's call, to be confirmed while writing; the constraint is the
structure, not the words.

**What each stage does with it**

| Stage | Pages | Use of the anchor |
|---|---|---|
| 01 Orientation | `llm-overview`, `generation` | The prompt and its continuation; the loop adds « mûr », then the next token |
| 02 Text input | `text-data` | The prompt split into tokens and IDs; "avocat" has the same ID in both prompts |
| 03 Representations | `embedding-space`, `positional-encoding`, `contextualized-representations` | Same ID → same row; swapping two words changes the meaning; same row, two different hidden states |
| 04 Computation | `transformer`, `queries-keys-values`, `scaled-dot-product-attention`, `causal-masking` | The last position gathers information from « salade »; a small worked attention; « avocat » cannot read « mûr » |
| 05 Prediction | `logits`, `probabilites`, `entropy` | The number chain (section 5) |
| 06 Inference | `generation` (second visit) | Greedy picks « mûr »; sampling sometimes picks another |
| 07 Scoring | `vraisemblance`, `cross-entropy` | Scoring the observed sentence « … est bien mûr. » |
| 08 Training | `loss`, `gradients` | Averaging over positions; the gradient pushes the logit of « mûr » up |
| Complements | `transformer-architectures`, `llm-limits` | Why a decoder-only model suits this prompt; « mûr » is plausible, not verified |

**Rules for the anchor**

- All numbers attached to it are illustrative and are labelled so, once per page, at first use.
  They do not come from a trained model.
- The token split shown in `text-data` either comes from a named real tokenizer, run and
  recorded, or is labelled illustrative. The hypothesis "« avocat » is a single token" is
  stated wherever the same-ID argument relies on it.
- The anchor replaces local toys where it can do the same job. A local example stays when it
  shows something the anchor cannot (for instance the pronoun example in
  `queries-keys-values`), and is then introduced as a second case, not a restart.
- Existing NumPy micro-workbenches keep their assertions; their comments and labels switch to
  the anchor's tokens where the mapping is direct.
- The existing figures `contextualized-embeddings-fr.svg` and its English twin show "bank".
  The French figure needs French labels; the builder edits the SVG text or, if that is not
  clean, keeps the figure and says in the caption that it uses the English counterpart.

## 5. The number chain

One small candidate set after « Dans la salade, l'avocat est bien », with probabilities chosen
so that every step can be checked by hand. Proposed values, to be recomputed by the builder
before use:

| Candidate | Logit | Probability |
|---|---|---|
| mûr | ln 6 ≈ 1.79 | 0.6 |
| préparé | ln 2 ≈ 0.69 | 0.2 |
| vert | 0 | 0.1 |
| frais | 0 | 0.1 |

- `logits`: the four scores; what can and cannot be read from them.
- `probabilites`: softmax turns them into (0.6, 0.2, 0.1, 0.1); temperature reshapes them.
  The tribunal prompt gives a different distribution over the same candidates.
- `entropy`: about 1.09 nats, against a maximum of ln 4 ≈ 1.39 for four candidates.
- `generation`: greedy selects « mûr »; sampling selects it six times in ten on average.
- `vraisemblance`: three observed tokens with probabilities (0.5, 0.6, 0.8), the middle one
  being « mûr »; product 0.24, NLL ≈ 1.43 nats, mean ≈ 0.48 nat per token.
- `cross-entropy`: the term for « mûr » is −ln 0.6 ≈ 0.51 nat.
- `loss`: the mean of the three terms; perplexity ≈ e^0.48 ≈ 1.61.
- `gradients`: p − one-hot = (−0.4, 0.2, 0.1, 0.1); one small step raises the logit of « mûr ».

The four-candidate vocabulary is a deliberate reduction of a real vocabulary of size V; each
page says so once. The current interactive temperature explorer and its micro-workbench keep
working; their logits are replaced by the chain's values if the rendered result stays readable.

## 6. Voice

- Address the reader as "vous". Short to medium sentences. One idea per sentence.
- Open a page with the question left by the previous one, phrased from the anchor
  ("« avocat » a le même identifiant dans les deux phrases. Comment le modèle les distingue-t-il ?").
- Say what the thing is and does, then what it does not establish. A reservation appears once
  per page, next to the claim it limits. The full treatment of a recurring reservation lives
  on one page and the others link to it at the point of use:
  normalisation vs calibration vs truth → `probabilites`; attention weight vs cause →
  `scaled-dot-product-attention`; objective vs guarantees → `llm-limits`.
- No sentence that would fit unchanged on another page.
- One analogy per concept at most, dropped as soon as it stops being exact, and said to be an
  analogy.
- French term in prose, English term once at first mention, then only in code and API names
  (principle 8). "la softmax", "perte", "entropie croisée", "plongement" / "embedding" per the
  glossary; one introduction per page, not at every mention.
- Formulas stay. Each is preceded by one sentence saying what it computes, in words.

## 7. Reader cues, the same on every page

A soft pattern, not a template: a cue is omitted when it has nothing to say.

1. Generated guided-route context (restored on `generation`, in its multi-stage form).
2. Lead: the question, then the answer in two or three sentences.
3. "L'idée à retenir en une minute": the summary only. No "Question de contrôle" (it
   duplicates the self-check). At most one "Première lecture" line saying what can be skipped.
4. Learning outcomes: collapsed block, kept only where it already exists and helps, always in
   this position.
5. Body. Sections numbered only when they are steps of one process, and then all numbered.
6. Misconceptions: at most one block per page, holding the "Idées reçues" list and any
   "Piège fréquent" disclosure.
7. "Vérifier sa compréhension" in a `.self-check` div: one line "Exercices associés :" with
   the matching collection anchor; numbered questions; one collapsed answer per question;
   "Afficher la réponse" for a result, "Afficher le raisonnement" for a worked answer.
8. "Références", only when the page cites sources that are not already linked in the text.
9. Generated suggested-route include, then the language switch.

Removed everywhere: hand-written `route-nav-cards` blocks (they render the suggested route a
second time, which the navigation contract forbids), "Pour poursuivre", "Pour aller plus loin",
"Liens avec les autres concepts", "Frontières entre les pages", "Où se situe cette étape…",
"Complément côté Build". A link from such a list survives only if it is moved to the sentence
where the concept is used and says what question it answers.

"Concept vérifié" badges: nothing on the page says what was verified. Builder's call: remove
them from the path pages unless the maintainer wants them explained instead.

## 8. Page-by-page plan

Listed in route order. "Keep" means the content stays and is only re-voiced.

| Page | Main changes |
|---|---|
| `llm-overview` | Plain lead on the anchor; the parameter-threshold debate and its citations move to section 1. Link-only paragraphs in sections 2 and 3 become explanation with links in place. Self-check gets collapsed answers. |
| `generation` | First screen: the loop as a black box on the anchor, no formula, readable at stage 01. Then the detailed lesson (notation, prefill, decode, KV cache, decoding rules) for stage 06. Drop the sentence about the page appearing twice and the duplicated paragraph on probabilities summing to one. Restore the route context. |
| `text-data` | Show the anchor split into tokens and IDs. Drop "Frontières entre les pages" and the stale "collection prévue" line. Corpus preparation shrinks to the one distinction the reader needs. |
| `embedding-space` | Open on the IDs from the previous page. Fix the duplicated heading. Word2Vec history shortened to what distinguishes a static vector from a lookup row. One term per concept. |
| `positional-encoding` | Open on the problem: the lookup gives the same vectors whatever the order. Self-check moves after the last content section. Drop the "where does this step sit" section. |
| `contextualized-representations` | The anchor replaces the English `bank` sentences. The externally hosted figure with unverified reuse rights (issue 156) is left as is and flagged in section 11. Drop the route recap. |
| `transformer` | Lead says what the network does to the anchor's vectors. Self-check wrapped and moved to the end. One "three levels" block kept here; the one in `generation` goes. |
| `queries-keys-values` | Opening question on the anchor: how does the last position get information from « salade »? Outcomes move to the top. "Imagine" → "Imaginez". Self-check heading aligned. |
| `scaled-dot-product-attention` | A hand-checkable worked example on three or four positions of the anchor. Heading, box and list agree on the number of steps. A real self-check. Drop the Build paragraph and the links list. |
| `causal-masking` | Open on the anchor: « avocat » must not read « mûr ». The API-version note joins the collapsed API block. Drop the links list. A real self-check. |
| `logits` | Add the four scores of the chain. Otherwise keep. |
| `probabilites` | The chain replaces (0, ln 3). One home for normalisation vs calibration vs truth. Drop "Pour poursuivre". |
| `entropy` | The chain replaces the two-token examples, which may stay as a second, contrasting case. The repeated temperature formula becomes one sentence and a link. Drop "Pour poursuivre". |
| `vraisemblance` | The anchor sentence scored token by token. The self-check stops carrying navigation links. |
| `cross-entropy` | The term for « mûr ». Keep the collapsed implementation blocks. "entropie croisée" in prose. |
| `loss` | Title in French ("Perte : …"). Mean of the three terms from the chain. The prefill vs teacher-forcing distinction is stated once here and linked from `generation`. |
| `gradients` | The gradient of the chain's distribution; one update step. End of the path: no "Retour" line. |
| `transformer-architectures` | Re-voice; tie the three families to what each would do with the anchor. |
| `llm-limits` | The one-minute box moves to the top. Each limit attached to a concrete case from the anchor. "Sources principales et rôle" becomes "Références". |

`cross-entropy` and `transformer-architectures` have been outlined but not yet read line by
line; their rows may gain items.

## 9. Constraints

- Read the four contract documents before editing; check each page against the quality
  contract in section 6 of the editorial method.
- French and English in the same commit, page by page.
- Page-map comments (`LLM-LAB-PAGE-MAP`) are updated when a page's scope or summary changes.
- Anchors referenced from `exercises.qmd` and from other pages are preserved or their
  referrers updated in the same commit.
- Every number is recomputed before it is written; the recomputation is kept as a short script
  in the pull request description or a test, not on the page.
- Governing documents updated in the same change: the editorial method gains a short section
  on the shared anchor and number chain; the glossary records "la softmax" and "perte";
  `docs/page-audit-inventory.md` is updated where a page's structure changes.
- Baseline checks before and after: `uv run ruff check .`, `uv run pytest`,
  `python site/tools/build_learning_map.py`, `quarto render site`, then a read of each changed
  page in a browser.

## 10. Order of work

Each batch is one commit covering both languages, and leaves the site buildable.

0. Conventions across the French site: "la softmax", "perte", "entropie croisée"; glossary.
1. Stage 01: `llm-overview`, `generation`. The anchor and the voice are set here; the
   maintainer reads these two pages before the rest proceeds.
2. Stages 02 and 03: `text-data`, `embedding-space`, `positional-encoding`,
   `contextualized-representations`.
3. Stage 04: `transformer`, `queries-keys-values`, `scaled-dot-product-attention`,
   `causal-masking`.
4. Stage 05: `logits`, `probabilites`, `entropy`.
5. Stages 07 and 08: `vraisemblance`, `cross-entropy`, `loss`, `gradients`.
6. Complements: `transformer-architectures`, `llm-limits`. Governing documents and inventory.

## 11. Left to the builder, and open points

- Exact wording of the English anchor pair.
- Whether the token split in `text-data` comes from a real tokenizer or is illustrative.
- Final values of the number chain, provided they stay hand-checkable and consistent across
  pages.
- Whether the French "bank" figure is relabelled or captioned.
- "Concept vérifié" badges: removed by default (section 7).
- Not addressed here, recorded for the maintainer: sidebar group names differ from stage titles
  (review item E1); French URLs mix languages (E5); the externally hosted figure in
  `contextualized-representations` still awaits its rights check.
- Not verified by this design: the mathematical correctness of the existing pages beyond the
  examples recomputed in the review of 2026-11-09.
