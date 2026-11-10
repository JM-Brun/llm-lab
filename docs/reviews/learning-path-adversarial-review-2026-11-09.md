# Learning-path adversarial review and fix handoff — 2026-11-09

This document is written so that a new session can fix everything without the original
conversation. It has four parts:

1. [Start here](#1-start-here) — state of the repository, traps, and what is already done.
2. [Findings](#2-findings) — what is wrong, with evidence, including a check of the four declared
   purposes (§2.5).
3. [Target design](#3-target-design-for-the-learning-path) — what the learning path and navigation
   should become. §3.6 records the maintainer's two-track model, which takes precedence where it
   differs from §3.1–§3.3.
4. [Work packages](#4-work-packages) — ordered, self-contained tasks with files, acceptance criteria
   and checks.

Scope reviewed: `JM-Brun/llm-lab` at `origin/main` (`56d30b4`, then `d2bcbcd`) and the published
site <https://jm-brun.github.io/llm-lab/>.

**Status:** this review proposes; it changes no priority. Decisions stay with the maintainer, the
current handoff and GitHub issues.

**Relation to other reviews of the same day:** it was written independently of the
[project review](adversarial-project-review-2026-11-09.md) and the
[navigation and ergonomics audit](navigation-ergonomics-audit-2026-11-09.md), and was not
reconciled with them. Where they overlap (sidebar, transitions, local orientation), compare before
acting; the navigation audit already defines validation tasks N1–N8 and a pilot decision that
work packages in group B should respect or explicitly supersede.

---

## 1. Start here

### 1.1 State of the repository

| Item | State |
|---|---|
| Anchor fix | Merged: PR [JM-Brun/llm-lab#812](https://github.com/JM-Brun/llm-lab/pull/812), `a5de714` on `main`. |
| This review | Merged: PR [JM-Brun/llm-lab#813](https://github.com/JM-Brun/llm-lab/pull/813), `5572868` on `main`. §2.5, §3.6 and group D were added afterwards, measured on `5572868`. |
| Leftover worktree | `.worktrees/fix-learning-map-anchor` removed on 2026-11-09, local branch deleted. |
| Main checkout | On `codex/check-guided-route-freshness`, **256+ commits behind `origin/main`**, with uncommitted edits in `src/llm_lab/foundations/` (the `FloatArray` consolidation, see WP-C2) and `.serena/project.yml`. Do not build on this branch. |
| This document | `docs/reviews/learning-path-adversarial-review-2026-11-09.md`. The older untracked copy in the main checkout was deleted. |

### 1.2 Traps met during the review

- **Always branch from `origin/main`**, in a worktree (`git worktree add .worktrees/<name> -b <branch> origin/main`). `.worktrees/` is git-ignored.
- **`git add` through rtk can stage everything.** Use `rtk proxy git add <paths>` and check `git diff --cached --name-only`.
- **`gh` has two accounts.** Only `JM-Brun` can open PRs on this repository (`gh auth switch --user JM-Brun`; it was switched on 2026-11-09).
- **Generated files.** `site/includes/learning-map.html` is generated from `site/tools/learning_map_renderers.py`; edit the renderer, then run `uv run python site/tools/build_learning_map.py`. That command also rewrites `site/includes/generated-map-data-{en,fr}.qmd` (committed as placeholders — restore them with `git checkout --`) and creates untracked `site/knowledge-graph.jsonld`. Guided-route partials (`site/includes/generated-guided-*.qmd`) are tracked and must be regenerated and committed when `data/guided-route.yml` changes.
- **Quarto version.** CI pins 1.11.9. Local 1.9.38 prints a fatal error on `includes/learning-map-hreflang.html` but still renders single pages. Trust CI for full renders.
- **Local setup** needs three installs: `uv sync --locked --dev`, then `uv pip install --python .venv/bin/python -r docs/requirements-tokenizer-example.txt -r docs/requirements-history-validation.txt`. The GPT-2 parity test also needs `docs/requirements-gpt2-reference.txt`; without it the test skips silently.
- **zsh**: `echo =====` fails (`=` expansion). Quote separators.

### 1.3 Baseline checks (all pass on `main`)

```bash
uv run ruff format --check . && uv run ruff check . && uv run mypy src && uv run pytest
```

Expected: about 350 passed, 1 skipped, coverage about 98 % (342 when first written; the count grows).

### 1.4 What this review must yield to (added 2026-11-10)

This review was written from the outside, before reading the project's own contracts. The
maintainer then restated the goal and asked for the editorial principles and constraints to be
respected. Where this document disagrees with the items below, **they win**.

**Goal, as stated by the maintainer (2026-11-10).** A complete panorama to learn and understand
LLMs and to build one: a main learning path and a Build path, comparable to the best
learn-and-build projects; separate resources to deepen; others to practise, exercise and question,
which keep growing over time. The project compiles the best of the field — pedagogical approaches,
sites and resources, differing and complementary viewpoints — and adds its own extensions.

**Contracts to read before any work package:**
[contributor guiding principles](../contributor-guiding-principles.md),
[page-navigation contract](../pedagogical-breadcrumb-and-page-navigation-contract.md),
[reader-experience and editorial method](../reader-experience-and-editorial-method.md),
[guided-route membership projection](../guided-route-membership-projection.md),
[comparable projects](../comparable-projects-landscape.md) and the
[source syntheses](../source-syntheses/README.md).

**Corrections to this review.**

| Where | What it said | Why it is wrong here | What to do instead |
|---|---|---|---|
| §2.5, Deepen | "It is larger than Understand, so the optional layer outweighs the core." | Deepen and Practice are meant to grow; size is not a defect. | Judge them by attachment and discoverability (§3.6, WP-D3), not by size. |
| §2.3, §2.4, §3.5 | Too many internal links; one running example everywhere, as in a single-author course. | The project's value is synthesis of several sources and viewpoints. | Keep multiple perspectives; make their role explicit on the page. Link density is a problem only where a link does not say which question it answers. |
| §3.1 item 4, §3.4, WP-B5, WP-B7 | One lesson template with eight fixed sections, checked by a test. | The principles require soft page patterns: "never add empty headings to satisfy a template"; the navigation contract "does not impose a universal lesson template". | Use the existing page patterns; align cues (question, outcome, self-check), not headings. No test on section order. |
| §3.3, WP-A5 | Remove the pipeline stepper on `text-data`. | The navigation contract (§3.4) allows a local process stepper when it describes the page's process. | Keep it; check only its label and placement against the contract. |
| §3.3, WP-A2 | "Path complete" card with three exits; "Back to stage N" card on optional pages. | End-of-page lists that duplicate menus are excluded; the badge already gives the way back, and one navigation dimension must not be rendered twice. | Done differently in PR 847: one forward card from the last core page to the Build path, nothing on optional pages. |
| §3.3, WP-B2 | Position line with reading time (`N min`), numbers in the sidebar. | Reading time is an unvalidated claim about effort. | Done differently in PR 849: position only, core pages only, inside the existing badge. Renumbering stays open and needs the maintainer's decision. |
| §3.2 | Fold the code tours into the lessons. | Concept teaching and implementation teaching stay separate and linked (principle 5). | Already superseded by §3.6: two paired tracks. |
| §2.5, Build; WP-D6 | "The name oversells"; rename the track until training exists. | The Build path is a stated goal, with status made visible (principle 14), not a naming problem. | Keep the name; keep the status column honest; prioritise G8 (WP-C5) so the path earns it. |

**Still valid and not affected:** the confirmed defects of §2.2, the measurements, the
verification of what runs (§2.5), group C, WP-A3, WP-A4, WP-D1 to WP-D5.

**Method for new work.** A change to the paths should name the source or comparable project whose
approach it adopts, say what it keeps and what it changes, and go through the source-synthesis
workflow when it adds or reshapes teaching content.

---

## 2. Findings

### 2.1 Whole project

**Verdict.** The code is small and correct; the site is honest and works on mobile. The weakness is
proportion: a large governance apparatus surrounds about 380 statements of NumPy, and the "lab"
trains nothing.

| Measure | Value |
|---|---|
| Library code | 382 statements, 13 files |
| Internal documentation (`docs/`) | about 203,000 words |
| Site prose (English) | about 90,000 words, 55 pages |
| Site tooling (`site/tools/`) | about 270 KB of Python |
| Commits by type | 281 `docs`, 47 `fix`, 18 `feat` |
| Experiments | 1 (softmax on four hard-coded logits) |
| Trained models | 0 |

- No training loop: no backward pass, optimizer, tokenizer pipeline or checkpoint.
- The build path teaches reading existing code, not building.
- About 17 open issues audit other people's projects; training (G8) is one issue.
- Nearly every paragraph ends with a "this does not prove…" qualifier.
- 4 of 10 exercise collections are published as "Structure to be filled".
- The "Verified Concept" badge overclaims: `docs/project-status.md` records no independent review.

**Code.**

- `GPTConfig` accepts `vocab_size=10.5` and `vocab_size=True`; failure comes later as a `TypeError` in `GPT()`. `generate(max_new_tokens=2.5)` likewise.
- `FloatArray` is defined in four modules.
- The GPT-2 parity test skips silently in the documented local setup.
- Walkthrough snippets drift from source (`residual_std = 0.02 / …` on the site, `base_std / …` in code). None of the Python blocks on the site is executed at build time.
- `softmax_with_temperature` carries an overflow-recovery branch for ±1e308 logits, at odds with "readable teaching implementation".

**Site.**

- English pages have a French footer (`site/_quarto.yml`, `page-footer`).
- No `hreflang` on most pages and no canonical link.
- The root URL is French; the README is English; there is no language choice at `/`.

### 2.2 Learning path — confirmed defects

| # | Defect | Evidence |
|---|---|---|
| D1 | Stage badges link to an anchor the map script strips | Fixed and merged (PR 812) |
| D2 | The route ends in a dead end | `en/gradients.html` shows only "Previous step" |
| D3 | Stage 06 cannot be reached with "Next" | Its only core page, `generation`, is read in stage 01; cards go entropy → likelihood |
| D4 | Optional pages have no way back to their stage | `en/rope.html`: previous/next are cross-attention and hybrid Nemotron architectures |
| D5 | The home page sends learners to maintainer documents | `site/en/index.qmd` line 180 links to `docs/full-curriculum-plan.md` (106 KB) and `docs/learning-path.md` (59 KB) |
| D6 | `generation` badge missing or inconsistent with `cross-entropy` | Verify on current `main`; an include now exists for it |

### 2.3 Learning path — why it feels unclear

Measured on the 17 core pages of the published English site:

| Measure | Value | Reading |
|---|---|---|
| Words | 21,400 (about 1 h 45) | Reasonable |
| Internal links inside lesson text | 310 (18 per page, one every 70 words) | Every paragraph offers an exit |
| Words before the first section heading | 145–306 | Badge, lead, "one-minute model", outcomes, sometimes a stepper |
| Code blocks | 6 in 17 pages | Not "code-first" |
| Figures | 15 | Adequate |
| Distinct example sentences | 4 (report/concentration, river bank, ice cream, animal/road) | No running example |

Structural causes:

1. **Five numbering schemes.** Home doors 01–03; stages 01–08; build steps 0–8; milestones G0–G9
   (displayed G0, G1, G3–G7, G1b, G2, G8, G9) plus E1 and A1; exercise codes TR-A, AT-A, CA-A, TF-A,
   GE-A. "03" means Deepen on the home page and "From IDs to representations" one click later.
2. **One object, five names.** "Guided route and resource map", "concept map", "resource and concept
   map", "Resource map" (`site/404.html`), "Learning path" (badge); URL `learning-map`. Units:
   stage, step, stop, tour, milestone.
3. **Four navigation widgets compete.** Sidebar, stage badge, bottom route cards, and on
   `text-data` an extra in-page "pipeline stepper" (1. Text → IDs, 2. Vectors, 3. Position,
   4. Context) that numbers the same pages differently again.
4. **No lesson template.** Section names and order differ on almost every page: numbered headings
   on three pages only; "Check your understanding" is last, in the middle, renamed ("Check the
   essential idea") or absent; closing sections are "References", "Further reading", both, or
   neither; some pages expose internal bookkeeping as sections ("Boundaries between pages",
   "Where does this step sit in the route?", "Provenance and purpose").
5. **Order of ideas.** The whole-model diagram (`transformer`) is page 7, after three detail pages
   on embeddings and position. Residual connections, layer normalization, the MLP and multi-head
   attention have no core page of their own, although the reference code implements all four.
6. **The route is not the front door.** The primary home button opens `llm-overview`; a learner can
   finish the route without seeing the route page.
7. **No position or progress.** No "page 9 of 17", no reading time, no completion state.
8. **The route page is three tools in one** (route, territory map, concept registry): 7,720 px on
   desktop, 12,279 px on mobile, and its introduction explains URL mechanics before stage 01.
9. **Sidebar and stages disagree.** Stages 02–05 are grouped under "How the model computes a
   prediction" with other sub-titles; stage 01's optional pages are listed after stage 08's core
   pages; breadcrumbs go four levels deep on a 17-page route; labels wrap to three lines.
10. **Build path is a separate island.** No badge, no "tour 2 of 5"; prose "Previous stop / Next
    stop" duplicates Quarto's previous/next links.
11. **The navbar is empty** (language, GitHub, search). The sidebar is collapsed by default
    (2 of 55 links visible) and hidden on mobile.

### 2.4 How comparable projects handle the same problem

Checked live on 2026-11-09: Hugging Face LLM Course, Dive into Deep Learning, Transformer Explainer.
From general knowledge, not re-checked: Raschka's book repository, Karpathy's Zero to Hero.

| Project | Path shape | Numbering | Per-page navigation | Lesson shape | Running example |
|---|---|---|---|---|---|
| Hugging Face LLM Course | One linear course | `chapter1/4` in the URL | One previous and one next link | Prose, then quiz at chapter end | Per chapter |
| Dive into Deep Learning | One linear book | `11.1`, `11.1.1` everywhere | Previous / Next with section numbers | Fixed: content, Summary, Exercises; "Open in Colab" on every page | Code carried across sections |
| Raschka, LLMs from Scratch | Seven chapters | `ch01`–`ch07` | Chapter order | Code first, each chapter extends the last | One model grown chapter by chapter |
| Karpathy, Zero to Hero | One playlist | Video order | Next video | Live coding | One codebase |
| Transformer Explainer | One screen | None needed | None | Interactive | One sentence ("Data visualization empowers users to") |
| **LLM Lab today** | Route + map + sidebar + build path + deepen | Five schemes | Badge + cards + sidebar + stepper | Different on each page | Four different sentences |

What all five have and LLM Lab lacks: **one spine, one numbering, one next button, one lesson
shape, one example carried from start to finish.** None of them asks the learner to choose between
routes before the first lesson.

LLM Lab's real differences are worth keeping: bilingual parity, the separation of generation,
scoring and training, the explicit evidence levels, and the misconception lists. They do not
require the present navigation complexity.

### 2.5 The four declared purposes, verified

The home page and both sidebars promise four things: **Understand**, **Build**, **Deepen**, and
**Practice and experiment**. Each was checked against `main` at `5572868`, English pages only.
Counts come from the sidebar sections of `site/_quarto.yml`; words exclude code blocks and the
page-map comment.

| Purpose | Promise on the home page | Delivered | Verdict |
|---|---|---|---|
| Understand | A system-level picture: data, representations, Transformer, prediction, generation | 19 pages, 25,504 words, 17 of 19 with a self-check | Holds, with gaps |
| Build | "Implement a small GPT" | 8 pages, 9,367 words, touring code that already exists | The name oversells |
| Deepen | Optional derivations and references, not prerequisites | 21 pages, 29,655 words, all listed in the hub | Reachable, uneven |
| Practice and experiment | "Verify through calculation and experiment" | 3 pages; 31 paper exercises; no experiment a learner can run from the site | Half delivered |

The `destination:` tag matches the sidebar section on all 53 pages. The classification is clean;
the problems are in what each section contains.

**Understand**

- Reading only: 6 static Python blocks, none executed at build time, one interactive widget
  (`probabilities`).
- The inside of a block has no lesson of its own. Multi-head attention, the MLP, residual
  connections and layer normalization appear only in the `transformer` overview; layer
  normalization is mentioned in 1 Understand page and 5 Build pages.
- Learning stops at one section, "Gradient-descent update" in `gradients`. There is no lesson on a
  training loop or an optimizer.
- No page covers chat templates or instruction tuning. The site explains a raw GPT, not how one
  becomes an assistant.
- `llm-overview` and `queries-keys-values` (the longest lesson, 2,338 words) have no self-check.

**Build**

- What works: the quick-start example on `build-path` runs as printed (21,426 parameters, greedy
  and sampled token IDs); the 140 unit tests pass with 97.6 % coverage.
- The learner writes no code. There is no skeleton and no "implement this, then make the test
  pass". Each tour ends with about 100 words of predict-the-shape questions.
- Milestone table: G0 and G1 are conceptual, G3–G7 are reference code, G2 is partial, G8 (train)
  and G9 (verify against a reference) do not exist.
- The output is random token IDs: no tokenizer, no text, no trained weights. The learner never
  sees the model produce language.
- `uv sync --locked --dev` followed by `uv run --locked pytest` fails with 6 collection errors
  (`No module named 'pydantic'`). The two extra installs are documented only in a footnote of
  `build-path` and in the README (see WP-C3).

**Deepen**

- It is larger than Understand, so the optional layer outweighs the core.
- Three pages have no inbound link from any Understand or Build page: `next-concept-modeling`,
  `score-centering`, `llm-evolution`. Ten more have exactly one.
- 12 of 20 pages state no prerequisite; 12 of 20 have no self-check.
- `tensors` (8 inbound links from core pages) and `mathematical-foundations` (5) act as
  prerequisites but are tagged `level:advanced`.
- Where the core is thin, Deepen is empty too: no deep dive on layer normalization, the MLP or
  multi-head attention.

**Practice and experiment**

- The exercises are real: 31 exercises with 63 collapsed answers, in 5 collections.
- The other 5 of 10 collections are placeholders ("Structure to be filled"): pretraining,
  fine-tuning, evaluation, efficiency, advanced topics.
- Almost all are pen-and-paper: one Python block and one `pytest` command in 12,555 words.
- The repository has one experiment, `experiments/decoding-distribution`. It is reproducible: a
  fresh run is byte-identical to `reports/decoding-distribution.json`. No site page links to it.
- "Experimental evaluation" is one written case with a checklist. "Transformer Explainer" embeds a
  third-party tool. `notebooks/` contains only a README.

**Across the four**

- The home page orders them 01 Understand, 02 Build, 03 Deepen, with Practice "at any time". The
  sidebar orders them Understand, Build, Practice, Deepen.
- `data/guided-route.yml` contains only the Understand path: all 18 core entries are
  `destination:understand`. Seven of the 8 Build pages, 12 of the 21 Deepen pages and all 3
  Practice pages are outside the route. The Build progression G0–G9 exists only as a table in
  `build-path.qmd`.

---

## 3. Target design for the learning path

### 3.1 Principles

1. One spine. Everything else is a side room reached from a lesson and returning to it.
2. One number per lesson, shown identically in the sidebar, the title, the badge and the cards.
3. One name: **Learning path** (FR: *Parcours*). One unit: **lesson** inside a **stage**.
4. One lesson template.
5. One running example, the same sentence and the same tiny model from lesson 1.1 to the last.
6. The reference code appears in the lesson that explains it.

### 3.2 Proposed spine (7 stages, 20 lessons)

Existing pages keep their URLs; only order, numbering and titles change. New lessons are marked.

| # | Lesson | Source page | Reference code shown |
|---|---|---|---|
| **1** | **The big picture** | | |
| 1.1 | What an LLM is | `llm-overview` | — |
| 1.2 | Generating text, step by step | `generation` | `generate.py` (10 lines) |
| 1.3 | The whole model in one diagram | `transformer` (moved up) | `gpt.py` `forward` shape journey |
| **2** | **From text to vectors** | | |
| 2.1 | Text, tokens and IDs | `text-data` | — |
| 2.2 | Embeddings | `embedding-space` | `token_embedding[ids]` |
| 2.3 | Position | `positional-encoding` | `position_embedding[:T]` |
| **3** | **Attention** | | |
| 3.1 | Queries, keys and values | `queries-keys-values` | `linear` projections |
| 3.2 | Scaled dot-product attention | `scaled-dot-product-attention` | `scaled_dot_product_attention` |
| 3.3 | Causal masking | `causal-masking` | `causal_mask` |
| 3.4 | Several heads | **new** (from block walkthrough) | `_attention` loop |
| **4** | **The Transformer block** | | |
| 4.1 | Residuals, normalization and the MLP | **new** (from ops and block walkthroughs) | `layer_norm`, `gelu`, `forward` |
| 4.2 | Contextualized representations | `contextualized-representations` (moved after attention) | — |
| **5** | **From vectors to a prediction** | | |
| 5.1 | Logits | `logits` | `w_head` |
| 5.2 | Probabilities | `probabilities` | `softmax_with_temperature` |
| 5.3 | Entropy | `entropy` | — |
| 5.4 | Choosing the next token | `decoding-strategies` (trimmed) or new short page | `top_k_filter`, `top_p_filter` |
| **6** | **Scoring a known text** | | |
| 6.1 | Likelihood | `likelihood` | — |
| 6.2 | Cross-entropy | `cross-entropy` | `cross_entropy_from_logits` |
| **7** | **Learning** | | |
| 7.1 | Loss over a batch | `loss` + `training-examples` | `sliding_input_target_pairs` |
| 7.2 | Gradients and the update | `gradients` | `cross_entropy_gradient` |

Changes from today: stage 06 (a repeat of `generation`) disappears and its content becomes lesson
5.4; the whole-model diagram moves to 1.3; contextualized representations move after attention,
where they can be explained; two lessons fill the block-component gap; the five code tours stop
being a parallel path and become the "In the code" section of lessons, with the tours kept as
reference pages.

When training (G8) exists, stage 7 gains 7.3 "A training loop" and 7.4 "Train a tiny model".

### 3.3 Navigation

- **Navbar:** Learning path · Build · Practice · Reference · FR/EN · search.
- **Sidebar:** the 7 stages and 20 numbered lessons, expanded for the current stage. A separate
  "Go deeper" group holds the optional pages; "Reference" holds glossary, history, references.
- **Top of each lesson:** one line — `Stage 3 of 7 · Lesson 3.2 · 6 min` — linking to the path page.
- **Bottom of each lesson:** one previous and one next card. The last lesson's next card is
  "Path complete" with three exits: Build, Practice, Go deeper.
- **Optional pages:** one card "Back to lesson N.M" instead of sidebar-order previous/next.
- **Remove:** the pipeline stepper on `text-data`, prose "Previous stop / Next stop", home door
  numbers 01–03, G-identifiers from reader-facing text.
- **Path page (`learning-map.html`):** the 7 stages with their lessons and a "Start" button. The
  territory map and concept registry move to a separate "Explore" page.
- **Home page:** one primary button, "Start the learning path" → lesson 1.1; secondary: "See the
  path".

### 3.4 Lesson template

1. Title: `N.M  Short noun phrase` (no colon subtitle; sidebar label ≤ 4 words).
2. One sentence: what you will be able to do.
3. The idea (intuition with the running example; one figure).
4. The computation (formula, then a worked example by hand with the running example's numbers).
5. In the code (the reference function, 10–25 lines, with a link to its test).
6. Common mistakes (at most three).
7. Check your understanding (three questions, collapsed answers).
8. Go deeper (at most three links) and Sources.

Rules: at most 8 internal links in sections 3–6; no section about the site's own organisation; one
"Limits" box per page instead of sentence-level qualifiers.

### 3.5 Running example

One sentence used in every lesson (suggestion: "The cat sat on the" → " mat"), one tiny
configuration (`vocab_size=50, context_length=8, embedding_dim=8, num_heads=2, num_layers=2`,
`seed=0`), and the same five token IDs. Every worked number on the path comes from this model, and
a test asserts each number printed on a page.

### 3.6 Maintainer's model: two paired tracks on a shared corpus

After §3.1–§3.5 were written, the maintainer stated the intended structure (2026-11-09, quoted as
given):

> **Corpus de connaissances partagé** — Concepts · Sources · Relations · Mathématiques ·
> Architectures · Méthodes
>
> **Theory / Understand** — Progression conceptuelle et scientifique
>
> **Build (from scratch)** — Progression d'implémentation et de validation
>
> **Deepen · Practice & experiment** — Ressources facultatives et activités transversales,
> rattachées à l'un ou aux deux parcours.

This is the target. It **supersedes** two points above: principle 1 of §3.1 ("one spine") and the
last sentence of the "Changes from today" paragraph of §3.2 (code tours folded into lessons). The
target is two parallel tracks whose stages are paired, not one spine. The rest of §3.1–§3.5 still
applies to each track: one numbering, one name, one lesson template, one running example.

How the project compares with the model today (evidence in §2.5):

| Layer of the model | Today | Gap |
|---|---|---|
| Shared corpus | Exists: `data/concepts.yml`, `sources.yml`, `resources.yml`, `domains.yml`, `computational-graph.yml` | Sound, but the reader sees a "map", not the base that both tracks draw from |
| Theory / Understand | A real track: `data/guided-route.yml`, 8 stages, core pages all `destination:understand` | None structural |
| Build (from scratch) | Not a track in the data: no stages, no stage badge, no generated next link; G0–G9 is a table | The second track is missing |
| Deepen, Practice and experiment, attached to one or both tracks | 9 Deepen pages are optional pages of an Understand stage; 12 Deepen pages and all Practice pages are attached to nothing; nothing is attached to Build | Attachment is partial and one-sided |

What the model requires:

1. **Two tracks in the route data.** `data/guided-route.yml` gains a `tracks` level with
   `understand` and `build`. Build stages are G0–G9, each with its pages, the result to verify and
   the test that checks it.
2. **Paired stages.** Each stage may name its counterpart in the other track (`pairs_with`). The
   generator renders the cross-link in both directions: "Build this" on an Understand lesson,
   "The idea behind this" on a Build step. In the lesson template (§3.4), section 5 "In the code"
   keeps a short excerpt and links to the paired Build step.
3. **Declared attachment.** Every Deepen page, exercise collection and experiment declares
   `attached_to` with one or more `track/stage` values. The generator renders a "Go deeper" block
   and a "Practice" block per stage from these declarations. A page with no attachment fails the
   build.
4. **The corpus shown as the base.** The home page replaces the 01/02/03 doors with the four-layer
   diagram. The concept registry and territory map (the "Explore" page of WP-B4) are presented as
   the shared corpus.
5. **Build keeps its promise.** "Implementation and validation" means the learner implements and
   the result is validated: stub functions with failing tests per step, training (G8) and
   comparison with a reference (G9). Until then the track's title should say what it is.

Navigation under this model, replacing the first two bullets of §3.3: the navbar is
Understand · Build · Practice · Explore · FR/EN · search; the sidebar shows the current track's
numbered stages, with that stage's attached Deepen and Practice items beneath it.

---

## 4. Work packages

Order matters within a group; groups A and C are independent of B. Each package is one PR. Before starting group B, read the navigation audit named above.

### Group A — small fixes (do first)

**WP-A1 Anchor fix.** Done (PR 812 merged). After the next deployment, confirm on the live site that
`en/learning-map.html#guided-stage-training` scrolls to stage 08.

**WP-A2 Route ending and way back.**
Files: `site/tools/build_learning_map.py` (`render_suggested_route_markdown`,
`render_guided_page_context_markdown`), `site/styles.scss`, generated partials.
Do: last core page gets a "Path complete" card linking to build path, exercises and the path page;
optional pages get a "Back to stage N" card linking to that stage's first core page.
Accept: `en/gradients.html` and `fr/gradients.html` show the completion card; `en/rope.html` shows
the back card; tests in `tests/knowledge/test_suggested_route_navigation.py` cover both.

**WP-A3 Home page links.**
Files: `site/en/index.qmd` (lines 35, 41, 180), `site/index.qmd` (French home), `site/404.html`.
Do: replace the two GitHub planning links with the path page; use "Learning path" / "Parcours" for
every link to `learning-map`; make "Start the learning path" the primary button.
Accept: no link from a rendered page to `docs/full-curriculum-plan.md` or `docs/learning-path.md`;
`grep -ri "concept map\|resource map" site/*.qmd site/en site/fr site/404.html` returns nothing.

**WP-A4 Footer and language metadata.**
Files: `site/_quarto.yml` (`page-footer`), language includes.
Do: language-neutral or per-language footer; `hreflang` alternates and a canonical link on every
page.
Accept: `en/*.html` contains no French footer text; each page has two `link rel="alternate"`.

**WP-A5 Remove duplicate navigation.**
Files: `site/en/text-data.qmd`, `site/fr/text-data.qmd` (pipeline stepper), the five
`*-walkthrough.qmd` pairs ("Previous stop / Next stop" lines).
Accept: `grep -r "pipeline-stepper\|Previous stop\|Arrêt précédent" site/en site/fr` returns nothing.

### Group B — learning path redesign (the main work)

**WP-B1 Decide and record the spine.** Edit `data/guided-route.yml` to the 7 stages of §3.2 using
existing pages only (no new lessons yet); remove stage `inference`; move `transformer` to stage 1
and `contextualized-representations` after attention. Regenerate partials. Update
`docs/learning-path.md` in the same PR (short note, not a rewrite).
Accept: every core page appears exactly once; "Next" from each core page reaches the last page in
18 clicks; `tests/knowledge/` pass.

**WP-B2 Numbering and position line.** Generator emits `Stage S of 7 · Lesson S.L · N min` (reading
time = words / 200, rounded up) in the badge; sidebar entries and route cards show `S.L`.
Files: `site/tools/build_learning_map.py`, `site/_quarto.yml` (sidebar text), `site/styles.scss`.
Accept: the same number appears in sidebar, badge and cards for all core pages (add a rendered-site
test).

**WP-B3 Sidebar and navbar.** Rewrite both language sidebars in `site/_quarto.yml` to mirror the
route (stage titles identical to `data/guided-route.yml`), with "Go deeper" and "Reference" groups;
add four navbar entries. Prefer generating the sidebar from the route file so they cannot diverge.
Accept: a test asserts sidebar order equals route order; breadcrumbs at most two levels on core
pages.

**WP-B4 Split the path page.** `learning-map.qmd` keeps the route only; move the territory map and
concept registry to new `explore.qmd` (both languages). Keep map-state URLs working with a redirect
note.
Accept: path page under 2,500 px at 1024 px width; stage anchors still work (test from PR 812).

**WP-B5 Lesson template, three pilot pages.** Apply §3.4 to `queries-keys-values`,
`scaled-dot-product-attention`, `causal-masking` in both languages, including the "In the code"
section. Write the template into `docs/concept-page-template.md` (replace, do not add a document).
Accept: identical section headings in the three pages; at most 8 internal links in sections 3–6;
a test checks section order for pages tagged `type:lesson`.

**WP-B6 Running example.** Add `site/tools/running_example.py` producing every number used on the
path from the tiny configuration of §3.5; add a test that the numbers quoted in the three pilot
pages match. Then use the example in the pilot pages.

**WP-B7 Roll the template out** to the remaining core pages, one stage per PR (five PRs).

**WP-B8 New lessons 3.4 and 4.1**, built from the existing block and ops walkthroughs.

**WP-B9 Names and numbers clean-up.** Remove 01–03 from home doors and G-identifiers from
reader-facing pages (keep them in `docs/`); replace "stop", "step", "milestone" with "lesson" or
"tour" as defined in §3.1.

### Group C — code and substance

**WP-C1 `GPTConfig` integer validation.** `src/llm_lab/foundations/gpt_config.py`: reject non-`int`
and `bool` for the six dimensions and `seed`; `generate`: same for `max_new_tokens`.
Tests in `tests/unit/test_gpt_config.py`, `test_generate.py`.

**WP-C2 Single `FloatArray`.** Import from `foundations/types.py` in `attention.py`,
`decoding_filters.py`, `gpt_ops.py`, `gpt.py`, `transformer_block.py`, `gpt2_weights.py`. The
uncommitted edits in the main checkout do this on a stale base; redo on `main`.

**WP-C3 Setup.** Move the three requirements files into `pyproject.toml` dependency groups
(`docs`, `parity`); one command in README; make the parity test's skip visible (`-rs` in
`addopts`).

**WP-C4 Snippet drift.** Either execute site code at build time or add a test that every fenced
Python block in `*-walkthrough.qmd` is a verbatim substring of its source file.

**WP-C5 Training (G8).** Manual backward pass for the existing blocks, finite-difference gradient
check, AdamW, character-level corpus, loss curve in `reports/`. This is the highest-value item in
the project; it unlocks lessons 7.3–7.4 and a real experiment.

**WP-C6 Published GPT-2 weights.** Tokenizer plus one script using the existing loader; generate
real text.

**WP-C7 Housekeeping.** Hide empty exercise collections; rename or justify the "Verified Concept"
badge; stop tracking `.serena/`; archive dated audit and handoff documents under `docs/archive/`.

### Group D — the two-track model (§3.6)

Group D changes the shape that group B works on. Do D1 before B1; B1 then orders the Understand
track only, and B3 builds the sidebar per track.

**WP-D1 Two tracks in the route data.** Files: `data/guided-route.yml` (schema version 2),
`site/tools/build_learning_map.py`, `site/tools/learning_map_renderers.py`, tests under
`tests/knowledge/`. Add `tracks: {understand, build}`; move the existing 8 stages under
`understand` unchanged; add Build stages G0–G9 using the existing Build pages, each with
`verify` (text) and `test` (path, optional). Generate badge and route cards for Build pages.
Accept: every Build page shows a stage badge and one next card; `build-path` renders its milestone
table from the data; existing Understand output is unchanged byte for byte.

**WP-D2 Paired stages.** Add `pairs_with` to stages; render the cross-link in both directions in
the generated context partial.
Accept: a test asserts pairing is symmetric; `en/scaled-dot-product-attention.html` links to the
attention Build step and back.

**WP-D3 Declared attachment.** Add `attached_to: ["track/stage", …]` to the page-map comment of
every Deepen and Practice page, to each exercise collection and to each experiment in
`data/resources.yml`. Replace `optional_pages` in the route file with this declaration. Generate
per-stage "Go deeper" and "Practice" blocks.
Accept: `site/tools/check_page_metadata.py` fails on a `destination:deepen` or
`destination:practice` page without `attached_to`; the three pages with no inbound core link
(`next-concept-modeling`, `score-centering`, `llm-evolution`) are attached or moved to Reference.

**WP-D4 Home page and names.** Replace the three doors and the practice strip on both home pages
with the four-layer diagram of §3.6; make the sidebar order match it; retag `tensors` and
`mathematical-foundations` as prerequisites rather than `level:advanced`.
Accept: the same four names, in the same order, on the home page, navbar and sidebar in both
languages.

**WP-D5 First learner-run experiment.** Link `experiments/decoding-distribution` from
`decoding-strategies` and from the Practice hub with a task: change the temperature, predict the
entropy, run, compare with the report. Attach it to the prediction stage.
Accept: at least one site page gives the run command and the expected output.

**WP-D6 Build tasks.** For each of the five tours, add one stub function and its failing test
under `exercises/` (solutions are the reference code); the tour's exercise section points to it.
Until D6 and C5 are done, title the track "Read and run a small GPT" in both languages.
Accept: `uv run pytest exercises/` fails before the learner's work and passes with the reference
implementation substituted.

**WP-D7 Fill the gaps the verification found.** Block-internals lessons are WP-B8. Add a self-check
to `llm-overview` and `queries-keys-values`; add a prerequisite line and a self-check to the 12
Deepen pages that lack them; hide the five empty exercise collections (same as WP-C7).

### Suggested sequence

A1 → A3 → A5 → A2 → A4 → D1 → B1 → D2 → D3 → B2 → B3 → D4 → B5 → B6 → B4 → B7 → B8 → B9, with
C1–C4, D5 and D7 in parallel, C5 started as soon as B1 is merged, and D6 after C5.

### Not verified in this review

- French pages beyond the home page and `fr/gradients.html`.
- Colour contrast and keyboard operation of the interactive map.
- The prose of most "Deepen" pages and the correctness of the exercise solutions (§2.5 measured
  structure and reachability, not content).
- §2.5 and §3.6 measured English pages only; the French side is assumed symmetric because the
  route file declares both languages.
- The full test suite with the two extra requirement files installed was not re-run for §2.5; only
  the 140 unit tests were.
- Raschka's and Karpathy's material was described from general knowledge, not re-read.
- The proposed spine has not been tested with a learner.
