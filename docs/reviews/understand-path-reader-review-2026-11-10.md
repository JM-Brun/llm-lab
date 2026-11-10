# Understand path — reader review, problems and suggestions (2026-11-10)

**Status:** review only. Nothing here is fixed yet; repairs are meant for a later session. It
proposes and changes no priority: decisions stay with the maintainer, the current handoff and
GitHub issues.

**What was done.** The 17 core pages of the Understand path were read in route order, in French,
as a learner would: title, lead, one-minute box, the opening of every section, the self-check and
the end of each page. The body of long sections was skimmed, not read word for word. Structure,
wording variants and French/English parity were then measured with scripts.

**Reviewed at:** `origin/main` `5d412b2`. Line numbers below are from that commit and will drift.

**Question asked:** is the path coherent and consistent, pleasant to read, are the pages
harmonised, and is everything organised sensibly?

**Short answer:** yes for the progression and for how pages open; no for how pages end, for a
handful of wording conventions, for two notes that are now false, and for the three different
groupings applied to the same pages.

## 1. Read this first

Repairs must follow the project's own contracts. An earlier review on this topic made
recommendations that contradicted them; see §1.4 of the
[learning-path adversarial review](learning-path-adversarial-review-2026-11-09.md).

- [Contributor guiding principles](../contributor-guiding-principles.md) — editorial economy, soft
  page patterns, French terminology rule (principle 8), bilingual parity.
- [Page-navigation contract](../pedagogical-breadcrumb-and-page-navigation-contract.md) — one
  rendering per navigation dimension; a next step only when useful.
- [Reader-experience and editorial method](../reader-experience-and-editorial-method.md).

Consequences for this document:

- **Harmonise cues, not headings.** No universal lesson template, no empty section added to make
  pages look alike.
- **Every change is made in both languages** in the same pull request.
- **Do not add navigation.** Several suggestions below remove or merge end-of-page sections.
- Items marked **Decision** need the maintainer's choice before any edit.

## 2. What works and should be kept

- **A stable opening.** 15 of 17 pages open the same way: path badge, lead paragraph, "L'idée à
  retenir en une minute". It is the strongest harmonising element of the path.
- **A continuous chain.** Previous/next cards follow `data/guided-route.yml` with no gap.
- **A self-check on 16 of 17 pages**, with collapsed answers.
- **Bilingual parity of structure**: the same cues in the same order in French and English on
  every core page.
- **A clear conceptual thread**: text → IDs → vectors → attention → logits → probabilities →
  scoring → loss → gradient, with the key distinctions repeated where they matter (generating is
  not learning; a logit is not a probability; entropy is not the surprise of the observed token).

## 3. Problems and suggestions

Each item gives the evidence, why it matters to a reader, a suggestion and a check that the repair
is complete. Paths are under `site/`; `fr/x` implies the same place in `en/x` unless stated.

### A. Statements that are false for the reader

**A1. Two self-checks say their exercise collection does not exist yet.**
Evidence: `fr/text-data.qmd:106` and `en/text-data.qmd:106` ("La collection approfondie sur les
données textuelles est prévue ; utilisez les vérifications ci-dessous en attendant" / "is planned;
use the checks below for now"); `fr/embedding-space.qmd:171` and `en/embedding-space.qmd:170`
(same sentence for the Transformer collection). Both collections are published:
`fr/exercises.qmd` has six exercises TR-A to TR-F under `#donnees-textuelles` and three, TF-A to
TF-C, under `#transformer`.
Why it matters: the reader is told not to look for exercises that are there.
Suggestion: replace with the neutral link line used on other pages (see C3).
Check: `grep -rn "est prévue ; utilisez\|is planned; use the checks" site/fr site/en` returns
nothing.

**A2. "Four steps" announced, five listed.**
Evidence: `fr/scaled-dot-product-attention.qmd:38` and `:43` ("suivez les quatre étapes", heading
"Calcul en quatre étapes"); the one-minute box on the same page gives the chain as
"scores → mise à l'échelle → masque éventuel → softmax → agrégation". Same in English (`:38`).
Suggestion: either number the mask as an optional step inside the four, and say so in the box, or
say five. Keep the heading, the box and the first-reading line in agreement.
Check: the count stated in the heading equals the number of items in the box and in the list.

### B. Language and tone

**B1. Grammatical gender of "softmax" changes between pages.**
Evidence (French core pages): "le/du softmax" 17 times — `positional-encoding` 1,
`queries-keys-values` 1, `scaled-dot-product-attention` 5, `causal-masking` 9, `gradients` 1;
"la softmax" 7 times — `logits` 2, `probabilites` 4, `loss` 1.
**Decision:** choose one. Then apply it to all French pages, not only the core path, and record it
in the glossary.
Check: `grep -rniE "\b(la|une) softmax" site/fr` or its masculine counterpart returns nothing.

**B2. "cross-entropie" and "entropie croisée" alternate.**
Evidence: "cross-entropie" 14 times (`cross-entropy` 8, `gradients` 3, `logits` 1,
`vraisemblance` 1, `loss` 1); "entropie croisée" 5 times (`cross-entropy` 3, `loss` 2). The page
title is "Entropie croisée".
Suggestion: principle 8 applies — French term in explanatory prose, English term where it is the
name of an API or established expression (`CrossEntropyLoss`). Use "entropie croisée" in prose.
Check: "cross-entropie" no longer appears in French prose.

**B3. "Loss" in French titles and menu labels while the prose says "perte".**
Evidence: title "Loss : de la perte par token à l'objectif" (`fr/loss.qmd`); sidebar labels
"Scoring des tokens observés" and "Loss et gradients" (`site/_quarto.yml:171`, `:175`). In the 17
pages "perte" appears 51 times and "loss" 46 times, 20 of them on `loss` itself.
**Decision:** keep "loss" as an accepted technical borrowing, or prefer "perte" in titles and
labels with "loss" introduced once. Either is defensible; mixing both in one title is the problem.

**B4. One informal imperative.**
Evidence: `fr/queries-keys-values.qmd:47`, "Imagine une collection de fiches". Every other page
addresses the reader as "vous".
Suggestion: "Imaginez".
Check: `grep -rnE "^(Imagine|Pense|Regarde|Suppose|Considère) " site/fr` returns nothing.

**B5. The French/English pair of a term is repeated at every mention.**
Evidence: `fr/contextualized-representations.qmd` — "matrice d'embeddings (ou table de
plongements)", "table de plongements (table d'embeddings)", "vecteur de plongement initial
(embedding)" within one page; `fr/embedding-space.qmd` uses "embedding" 26 times and "plongement"
7 times, alternating.
Why it matters: the doubled form slows reading and suggests two objects. Principle 8 asks to
introduce the pair at first mention, then reuse one naturally.
Suggestion: one introduction per page, then a single term; the same choice across the three pages
of stage 03.

**B6. English example sentences on a French page.**
Evidence: `fr/contextualized-representations.qmd:49-50` — "The river bank eroded." / "The
financial bank collapsed."
Suggestion: a French pair with the same property, one written form and two senses (for instance
"avocat"), or keep the English pair and say why (a tokenizer trained on English). Check that the
chosen word is plausibly a single token, or keep the page's existing hypothesis explicit.

### C. Page cues that differ without a reason

**C1. `generation` is the only core page without the path badge, and names its box differently.**
Evidence: no `generated-guided-context` include in `fr/generation.qmd` (removed in PR 787); box
titled "Le modèle mental" (`:37`) where the other 16 pages say "L'idée à retenir en une minute".
It is the second page of the path, so the reader loses the position cue just after starting.
Note: the page belongs to two stages, so its badge is the longer multi-stage variant; that is
probably why it was removed.
**Decision:** restore the badge in a compact form for multi-stage pages, or accept the exception.
The box title can be aligned in either case.

**C2. The one-minute box has a varying set of sub-labels.**
Evidence: "Première lecture" on 8 pages, "Pour approfondir" on 4, "Question de contrôle" on 8,
none on the rest; combinations differ page to page.
Suggestion: keep the box as the summary only. If a first-reading hint is useful, use the same
label everywhere it appears. "Question de contrôle" duplicates the self-check section and can go.

**C3. The self-check varies in heading, opening line and answer label.**
Evidence: heading "Vérifier l'idée essentielle" on `queries-keys-values:206`, "Vérifier sa
compréhension" on the 15 others. Opening lines: "Répondez aux questions suivantes sans consulter
immédiatement les réponses", "[Exercices approfondis sur ce thème].", "Des exercices formatifs
mobilisent cette page dans la collection Transformer", "Pour des exercices complémentaires séparés
du cours, voir…", and the two stale lines of A1. Answer labels: "Afficher la réponse" 16,
"Afficher les réponses" 5, "Afficher le raisonnement" 7, and three "Piège fréquent : …".
Suggestion: one heading; one opening line of the form "Exercices associés : [collection]"; two
answer labels at most ("Afficher la réponse" for a result, "Afficher le raisonnement" for a worked
answer). "Piège fréquent" disclosures belong with misconceptions, not with the self-check.

**C4. Learning outcomes appear on 4 pages, in two places.**
Evidence: collapsed "Objectifs d'apprentissage" on `generation`, `text-data`, `transformer`,
`logits`; on `queries-keys-values` the outcomes are a section near the end, "Opérations à
maîtriser" (`:183`).
Note: principle 7 says outcomes only when they help, so their absence elsewhere is acceptable.
Suggestion: where they exist, use the same collapsed block near the top.

**C5. "Concept vérifié · Architecture" chips on 3 pages only.**
Evidence: `queries-keys-values`, `scaled-dot-product-attention`, `causal-masking`. Nothing on the
page says what was verified or by whom, and a reader may conclude the other 14 pages are not.
**Decision:** explain the chip where it appears (link to the evidence), extend it, or remove it.

**C6. Section numbering is mixed.**
Evidence: all sections numbered on `llm-overview` and `generation`; partly on `text-data` ("1.",
unnumbered, "2.") and `transformer` (unnumbered, "1.", "2.", "3.", then unnumbered); none on the
other 13.
Suggestion: number only where the sections are steps of one process, and then number all of them.

### D. Page endings

**D1. Seven different closing sections, in varying order.**
Evidence (French headings after the main explanation): "Références" (5 pages), "Pour approfondir"
(3), "Pour poursuivre" (2), "Liens avec les autres concepts" (2), "Exercices complémentaires"
(1), "Frontières entre les pages" (1), "Où se situe cette étape dans le parcours ?" (1).
"Références" comes before the self-check on `positional-encoding` and after it elsewhere. On
`transformer`, three content sections follow the self-check.
Why it matters: the reader cannot predict where a page ends or where sources are. Several of these
lists restate the route or the menu, which editorial economy excludes.
Suggestion:
- Keep at most two closing blocks, in this order: self-check, then sources ("Références").
- Move a link to where the concept is used in the text instead of listing it at the end
  ("Liens avec les autres concepts", "Pour poursuivre").
- Remove sections that describe the site rather than the subject ("Où se situe cette étape dans
  le parcours ?" on `positional-encoding:97`; "Frontières entre les pages" on `text-data:127`
  could become one sentence in the lead about what the page leaves to others).
- Put the self-check after the last content section on `transformer`.
Check: on every core page the self-check is the last section before sources, and no closing
section lists the previous or next page.

**D2. Only one page links to its Build counterpart.**
Evidence: "Complément côté Build (facultatif)" on `scaled-dot-product-attention:137`. Its first
sentence describes the site ("Cette page appartient au parcours conceptuel…").
Why it matters: the project is two paths; a reader of Understand has no consistent way to see the
same mechanism as code.
Suggestion: this is the paired-stage link of WP-D2 in the adversarial review. Until it is
generated, either add the same short link to the pages that have a matching tour or leave this
one, without the sentence about the site.

### E. Organisation

**E1. Three groupings of the same pages, with different names.**
Evidence: the route has 8 stages; the path page groups them under 3 questions; the sidebar has 7
groups (`site/_quarto.yml:152-175` for French, `:253-276` for English).

| Route stage | Sidebar group |
|---|---|
| 01 Situer le système | (two pages listed directly) |
| 02 Du texte aux tokens | (one page inside "Comment le modèle calcule sa prédiction") |
| 03 Des identifiants aux représentations | Des identifiants aux représentations |
| 04 Comprendre le calcul du Transformer | Transformer les représentations |
| 05 Des états à la distribution prédictive | Des scores aux probabilités |
| 06 Exécuter l'inférence et générer du texte | — |
| 07 Attribuer un score aux tokens observés | Scoring des tokens observés |
| 08 Apprendre et mettre à jour les paramètres | Loss et gradients |

The badge on a page says "04 · Comprendre le calcul du Transformer" while the menu beside it says
"Transformer les représentations".
**Decision:** align sidebar group names with stage titles, or state that the sidebar is the site
map and deliberately different. The navigation contract keeps the two dimensions distinct, so
different *structures* are allowed; different *names for the same group* are what confuses.

**E2. `generation` asks too much as the second page.**
Evidence: its learning outcomes include "expliquer le rôle du prefill, du decode incrémental et du
cache KV" (`:32`), and section 3 covers them (`:106`). A note explains that the page is used twice
and that the first visit can stop at the mental model (`:44-48`), but it is collapsed by default,
and the next cards never bring the reader back: from `entropy` the next card goes to
`vraisemblance`, skipping stage 06.
Suggestion: show the two-visits note open, split the outcomes into "first visit" and "second
visit", and make stage 06 reachable on the way (a contextual link from `entropy` or `probabilites`
where decoding is discussed). Splitting the page in two is the larger alternative.
**Decision** if the page is split.

**E3. `contextualized-representations` comes before the page that introduces Transformer blocks.**
Evidence: stage 03 ends with it; `transformer` opens stage 04. The page relies on "les blocs
Transformer" and "états cachés" before either is presented.
Assessment: readable as a bridge, and the page states its dependency. Not a defect by itself; note
it if the route order is revisited.

**E4. The first lead of the path is its densest.**
Evidence: `fr/llm-overview.qmd` lead — a definition qualified by a debate on parameter thresholds
with three citations, before the reader knows what a token is.
Suggestion: open with the plain definition; move the threshold discussion and its citations to
section 1, where the three notions are distinguished.

**E5. File names mix languages in French URLs.**
Evidence: `fr/probabilites`, `fr/vraisemblance` beside `fr/entropy`, `fr/loss`, `fr/gradients`,
`fr/cross-entropy`.
Assessment: visible only in the address bar; renaming breaks links. Record, do not fix, unless a
redirect mechanism is added.

## 4. Decisions needed from the maintainer

1. Gender of "softmax" in French (B1).
2. "loss" or "perte" in titles and menu labels (B3).
3. Badge on `generation`: restore in compact form or keep the exception (C1).
4. "Concept vérifié" chips: explain, extend or remove (C5).
5. Sidebar group names: align with stage titles or keep distinct (E1).
6. `generation`: restructure in place or split (E2).

## 5. Suggested batches for the repair session

Each batch is one pull request, both languages together.

| Batch | Items | Needs a decision | Risk |
|---|---|---|---|
| 1. Facts | A1, A2 | No | Low |
| 2. Wording | B4, B2, B5, B6 | No | Low |
| 3. Conventions | B1, B3 | Yes (1, 2) | Low once decided; touches many pages |
| 4. Self-check | C3, C2 | No | Low |
| 5. Page cues | C1, C4, C5, C6 | Yes (3, 4) | Medium |
| 6. Endings | D1, D2 | No | Medium: moves links into the text |
| 7. Organisation | E1, E2, E4 | Yes (5, 6) | Medium to high |

Before each batch: read the contracts in §1, run the baseline checks
(`uv run ruff check . && uv run pytest`), and update `docs/page-audit-inventory.md` if a page's
structure changes. After each batch: render the changed pages and read them once in a browser.

## 6. Not checked

- Mathematical and scientific correctness of the pages.
- The body of long sections, word for word.
- English prose quality; only English structure was compared.
- Optional pages, the Build path, exercises and Deepen pages.
- Rendering beyond the top of three pages on the published site.
- Whether any of the above is already tracked in an open issue.

## 7. Reference: cues per page

French core pages in route order. `x` present, `.` absent.

| Page | Words | Badge | One-minute box | Outcomes | Self-check | Misconceptions | Closing sections |
|---|---|---|---|---|---|---|---|
| `llm-overview` | 2,024 | x | x | . | . | . | — |
| `generation` | 2,173 | . | "Le modèle mental" | x | x | x | — |
| `text-data` | 1,301 | x | x | x | x | . | Frontières entre les pages |
| `embedding-space` | 1,737 | x | x | . | x | . | Références |
| `positional-encoding` | 1,414 | x | x | . | x | x | Où se situe…, Références (before self-check) |
| `contextualized-representations` | 1,422 | x | x | . | x | . | — |
| `transformer` | 2,061 | x | x | x | x | x | three content sections after self-check |
| `queries-keys-values` | 2,665 | x | x | at end | "Vérifier l'idée essentielle" | . | — |
| `scaled-dot-product-attention` | 1,517 | x | x | . | x | x | Liens…, Complément côté Build |
| `causal-masking` | 1,832 | x | x | . | x | x | Liens… |
| `logits` | 706 | x | x | x | x | . | — |
| `probabilites` | 1,245 | x | x | . | x | x | Pour poursuivre, Références |
| `entropy` | 990 | x | x | . | x | . | Pour poursuivre, Références |
| `vraisemblance` | 1,145 | x | x | . | x | x | Pour approfondir |
| `cross-entropy` | 2,086 | x | x | . | x | x | Exercices complémentaires, Références |
| `loss` | 1,323 | x | x | . | x | x | Pour approfondir |
| `gradients` | 1,128 | x | x | . | x | x | Pour approfondir |

Word counts exclude code blocks and inline figures, and include markup words; treat them as
relative sizes.
