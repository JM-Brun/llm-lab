# LLM Advent Calendar — project design

**Status:** 24-day editorial proposal; bilingual landing page and first three guided days implemented; learner validation pending  
**Date:** 2026-11-22  
**Owner:** LLM Lab editorial architecture  
**Scope:** a 24-day, bilingual, progressive introduction to the concepts already taught by LLM Lab

## 1. Purpose

Build a small, coherent learning experience that introduces one meaningful LLM concept, distinction, or operation per day. The calendar should make the existing lab easier to discover and understand; it must not become a parallel curriculum, a second concept registry, or a duplicate set of long-form lessons.

The intended learner outcome is cumulative: explain how a text context becomes a next-token probability distribution, how that distribution is used for generation and observed-target scoring, and how observed targets support parameter learning.

The initial format is **24 short daily units**, suitable for December 1–24, but the content should remain useful as an evergreen mini-course after the seasonal event.

### 1.1 Scope boundary

The 24 days focus on the **core autoregressive language-model mechanism**: supplied context, text/token representations, Transformer computation, next-token distributions, generation, observed-target scoring, the basic training objective, parameter updates, and held-out evaluation.

The calendar is not intended to cover the whole LLM application or research landscape. In particular, these topics remain outside the core 24-day sequence and should be reached through optional LLM Lab resources where useful:

- application-level context use and design (in-context learning, context engineering, retrieval, and memory);
- post-training, instruction tuning, preference optimization, and reinforcement learning;
- tool calling and agentic systems;
- alternative model families and multimodal architectures;
- scaling laws, emergent-ability claims, and research-frontier topics;
- production deployment, serving, and infrastructure optimization beyond the prefill/decode/KV-cache intuition.

This boundary is deliberate. It keeps the calendar focused on one coherent computational model rather than turning it into a compressed survey of every topic in the repository. Exclusion from the 24 days does not imply low importance; it means the topic belongs in a different route or an optional follow-up.

## 2. Architectural fit with LLM Lab

The calendar is a reader-facing editorial projection of canonical project knowledge. It does not own scientific definitions or dependency semantics.

| Concern | Canonical owner | Calendar responsibility |
|---|---|---|
| Scientific concepts and bilingual definitions | `data/concepts.yml` | Reference stable concept IDs |
| Concept definitions and semantic relations | `data/concepts.yml` | Reference stable concept IDs; do not redefine or flatten relations |
| Computational operations and dataflow | `data/computational-graph.yml` and [canonical computational spine](canonical-computational-spine.md) | Respect the shared prediction mechanism and its typed branches |
| Theory / Understand progression | `data/guided-route.yml` and [learning path](learning-path.md) | Select and compress a coherent subset; do not create prerequisite edges |
| Build implementation dependencies | Build route and implementation documentation | Link only where a hands-on implementation adds value |
| Long-form explanations | `site/**/*.qmd` | Link to authoritative lessons; avoid copying them |
| Exercises | Practice & experiment pages | Link to dedicated exercise material; do not move exercises into lesson prose |
| Calendar order and daily learning contract | `data/calendars/llm-advent-24.yml` | Own only day selection, editorial order, daily question, outcome, and resource pointers |

The calendar order is **not** a new prerequisite DAG. It is a carefully selected narrative path. The knowledge graph continues to represent conceptual relations; the computational graph represents operations and dataflow; the Understand and Build paths retain their distinct purposes.

### Shared computational spine

The calendar must preserve the central model:

`context → f_θ(context) → logits → softmax → p_θ(next token | context)`

This shared conditional distribution has sibling uses:

- **Generation:** a decoding policy selects a token, which is fed back into the next context.
- **Observed-target scoring:** the model assigns probability to a known target; target log-probabilities support sequence likelihood.
- **Evaluation:** observed-target scoring is applied to held-out data without updating parameters.
- **Training:** target-level negative log-likelihood / cross-entropy is aggregated into an objective, differentiated, and used by an optimizer to update parameters.

These branches must not be presented as one operational sequence. In particular, likelihood and loss are not steps in ordinary generation.

The Transformer computation must also remain correctly nested: Q/K/V projections, attention scores, causal masking, normalization of attention weights, and value aggregation occur inside each Transformer block. They do not follow the final contextualized representation.

## 3. Learning design

### 3.1 Intended audience and level

- Curious readers with basic familiarity with text and vectors; no assumption that they have implemented a Transformer.
- The core explanation should be accessible without advanced mathematics.
- Mathematical details, code, architecture variants, and implementation caveats belong in linked deeper resources.
- A day should be useful on its own, while making its place in the overall story visible.

### 3.2 Daily learning contract

Each day should contain:

1. **One central question** — a concrete question, not a broad topic label.
2. **One concise explanation** — enough to answer that question without duplicating the canonical lesson.
3. **One intuition or worked example** — visual, numerical, geometric, or textual as appropriate.
4. **One active check** — predict, distinguish, calculate, trace, or explain something.
5. **One takeaway** — a short statement of what the learner should now be able to explain.
6. **A path onward** — one primary LLM Lab lesson and, where useful, a separate exercise or experiment.

Target duration: approximately 5–8 minutes. This is a design target to test, not a guaranteed reading time.

Not every day needs code or an interactive widget. Use an interaction only when it materially improves reasoning or feedback. A hand-checkable numerical example may be more valuable than a custom widget.

### 3.3 Daily formats

Use a small controlled set of activity formats:

- `conceptual-check`: distinguish concepts or explain a mechanism.
- `trace`: follow values through a computation.
- `numerical`: calculate a small result by hand or with a reproducible example.
- `visual`: inspect or manipulate a diagram.
- `code`: run or modify a small implementation.

A day can use one primary format and optionally one secondary format. Do not force identical interaction patterns onto every concept.

### 3.4 Difficulty and progression

The proposed four acts are editorial groupings, not new curriculum stages:

1. **Days 1–7 — Context and representations:** what conditions the prediction, then how text becomes numerical input.
2. **Days 8–12 — Transformer computation:** how representations are transformed and contextualized.
3. **Days 13–18 — Prediction and generation:** how logits become a distribution and how inference uses it.
4. **Days 19–24 — Scoring and learning:** how observed targets support likelihood and loss, then how training updates parameters while evaluation measures held-out data without updates.

The progression should be checked against actual conceptual dependencies. A topic must not appear early merely because it is popular or easy to illustrate.

### Relationship to the nine-stage guided route

The calendar is a **selective short-form projection**, not a compressed copy of every guided-route stage:

| Guided-route stage | Calendar coverage | Decision |
|---|---|---|
| Orientation | Day 1 | Introduce the conditional next-token prediction mechanism. |
| Text input | Days 2–4 | Cover context/prefix, tokenization, and vocabulary-local IDs. |
| Representations | Days 5–7 | Cover embeddings, positional information, and contextualized representations. |
| Transformer computation | Days 8–12 | Cover the block, Q/K/V, attention, causal masking, and the non-attention sublayers. |
| Prediction | Days 13–15 | Cover logits, the vocabulary distribution, and predictive entropy. |
| Inference | Days 16–18 | Cover decoding, autoregressive feedback, prefill, decode, and KV cache. |
| Context use and design | Not included | Deliberately excluded from this core calendar; retrieval, memory, in-context learning, and context engineering remain optional follow-up resources. Day 2 covers the immediate prefix available to the model, not application-level context engineering. |
| Observed-target scoring | Days 19–21 | Cover teacher-forced observed targets, sequence likelihood, and token-level cross-entropy. |
| Training | Days 22–24 | Cover loss aggregation, gradients, optimizer updates, and held-out evaluation. |

This mapping preserves the distinction between the immediate model context (needed to explain next-token prediction) and the broader system-level work of designing, retrieving, or managing context. The omitted guided-route stage is an explicit scope decision, not a missing day to be filled automatically.

## 4. Initial 24-day editorial proposal

This sequence is a **candidate for review**, not an approved syllabus. The machine-readable proposal is in `data/calendars/llm-advent-24.yml`. Three bilingual content pilots (days 03, 09, and 21) are drafted in [advent-calendar-pilot-content.md](advent-calendar-pilot-content.md); they are not yet learner-tested.

| Day | Act | Candidate topic | Core question |
|---:|---|---|---|
| 01 | Text and representations | Next-token prediction | What does a language model predict? |
| 02 | Text and representations | Context and prefix | What information can the model use for its next prediction? |
| 03 | Text and representations | Tokenization | How does text become discrete tokens? |
| 04 | Text and representations | Vocabulary and token IDs | How does the model identify each token? |
| 05 | Text and representations | Token embeddings | How does an ID select a vector? |
| 06 | Text and representations | Positional information | Why does token order matter? |
| 07 | Context and representations | Contextualized representations | Why can the same token have different representations in different contexts? |
| 08 | Transformer computation | Transformer block | What transformations happen inside a block? |
| 09 | Transformer computation | Queries, Keys, Values | What distinct roles do Q, K, and V play? |
| 10 | Transformer computation | Scaled dot-product attention | How do scores become a weighted combination of values? |
| 11 | Transformer computation | Causal masking | How is access to future positions prevented? |
| 12 | Transformer computation | MLP, residual connections, normalization | How does a block transform and preserve information? |
| 13 | Prediction and generation | Logits | What does the output projection produce? |
| 14 | Prediction and generation | Softmax and conditional probabilities | How do scores define a probability distribution? |
| 15 | Prediction and generation | Entropy and uncertainty | What does the distribution tell us about uncertainty? |
| 16 | Prediction and generation | Decoding policies | How is a token selected from the distribution? |
| 17 | Prediction and generation | Autoregressive generation | How does a selected token become part of the next context? |
| 18 | Prediction and generation | Prefill, decode, and KV cache | How is inference organized and accelerated? |
| 19 | Scoring and learning | Observed targets and teacher forcing | How does the model receive the correct prefix while scoring a target? |
| 20 | Scoring and learning | Sequence likelihood | How do conditional target probabilities combine across a sequence? |
| 21 | Scoring and learning | NLL and cross-entropy | How is a prediction error expressed as a probabilistic cost? |
| 22 | Scoring and learning | Training objective and loss aggregation | How do token-level costs become one objective? |
| 23 | Scoring and learning | Gradients and backpropagation | How do we determine how parameters should change? |
| 24 | Scoring and learning | Optimizer and parameter update | How does the training step change the model? |

### Important editorial checks before approval

- Day 2 must explain context/prefix without conflating prompt construction with the broader topic of context engineering.
- Day 4 must distinguish token strings, vocabulary entries, and token IDs.
- Day 8 and day 12 need a clean boundary: day 8 introduces the block as a whole; day 12 explains the non-attention sublayers and residual/normalization flow. Avoid teaching the same diagram twice.
- Days 9–11 must preserve the exact Q/K/V and masking computation; changing V while Q, K, and the mask are fixed is a useful intervention.
- Day 15 must distinguish entropy of the predictive distribution from uncertainty about correctness or calibration.
- Day 18 must distinguish prefill from autoregressive decode and explain KV cache as an optional inference optimization, not a new prediction mechanism.
- Day 19 must distinguish the observed prefix/target shift from generation feedback. Teacher forcing is a context policy for scoring/training, not a separate forward mechanism.
- Days 20–22 must distinguish sequence likelihood, log-likelihood, per-token NLL/cross-entropy, and the reduction/masking used to form an objective.
- Days 23–24 must distinguish gradients from optimizer updates. Day 24 must also show held-out evaluation as a sibling measurement of the current model: it uses fixed parameters and must not be drawn as a mandatory step after the optimizer update.
- The current NumPy implementation and project status must be represented honestly: documentation of training concepts does not imply a complete trained-model pipeline or demonstrated language quality.

## 5. Daily content template

Use a common editorial template, while allowing the activity to vary:

- Day number, short title, and estimated duration.
- Central question.
- Short answer / intuition.
- Worked example or visual.
- One active question or manipulation, with feedback or a worked answer.
- Key takeaway (one or two sentences).
- **Understand more:** link to the canonical lesson.
- **Practice & experiment:** link to a dedicated exercise where one exists.
- Optional **Deepen / Build** links, clearly marked as optional.

The calendar unit is a short entry point, not a replacement for the canonical page. Do not duplicate long-form definitions, detailed proofs, or code that already has an authoritative home.

## 6. Interface and interaction principles

### Visual direction

- Reuse the LLM Lab visual system: restrained green as the dominant accent, neutral reading surfaces, and the existing typography and spacing.
- Use a 24-door grid with clear numbering and compact titles.
- Provide an accessible text list of all days in addition to the visual grid.
- Use subtle opening/transition effects only when they do not impair accessibility or performance.
- Keep the main learning content readable and avoid decorative clutter.

### Calendar behavior

- During the December event, the interface may visually distinguish today's door and future doors.
- The evergreen archive must make all 24 entries available after the event.
- Do not require an account, leaderboard, streak, or social competition.
- Do not make completion streaks a proxy for learning.
- If progress is persisted, prefer a transparent, local-only mechanism and make the calendar fully usable without it.
- Support keyboard navigation, visible focus, screen readers, reduced motion, sufficient contrast, and meaningful image alternatives.
- Preserve the site's FR/EN switch; do not create parallel language-specific calendar implementations.

### No premature interface implementation

Do not build the visual calendar before the 24-day selection and three-day content pilot are reviewed. The content model and rendered reader experience should be validated first.

## 7. Data and implementation architecture

The proposed manifest is `data/calendars/llm-advent-24.yml`. It should own only:

- calendar identity and status;
- day number and stable day ID;
- bilingual title, question, and learning outcome;
- editorial act and activity type;
- references to existing concept IDs and page/resource IDs;
- estimated duration and optional exercise references.

It must not duplicate concept definitions, page content, source bibliographies, or computational edges.

### 7.1 Reuse the existing metadata model

The manifest is an editorial index, not a metadata registry. Its references must resolve through the existing sources of truth:

| Calendar field | Canonical metadata owner | Contract |
|---|---|---|
| `concepts` | `data/concepts.yml` | Stable language-independent concept IDs only. Keep the list focused on concepts actually taught or explicitly contrasted that day. |
| `computational_nodes` | `data/computational-graph.yml` | Stable node IDs for computational states and operations that are not necessarily concepts. Do not put branch IDs or edge IDs here. An empty list is valid when a day is about a quantity not represented as a computational node. |
| `lesson_pages` | Page-map metadata in `site/**/*.qmd` | Existing FR/EN page IDs. Resolve their `type`, `destination`, `topic`, `level`, `language`, and `status` from the page metadata; do not repeat those tags in the calendar manifest. |
| `build_pages` | Page-map metadata in `site/**/*.qmd` | Optional Build companions, kept separate from the main lesson and exercises. Each must resolve to a published `destination:build` page (currently `type:guided-build` or `type:concept-bridge`) in the matching language. |
| `deepening_pages` | Page-map metadata in `site/**/*.qmd` | Optional deeper reading. Each must resolve to a published `type:deep-dive`, `destination:deepen` page in the matching language. |
| `practice_pages` | Page-map metadata in `site/**/*.qmd` | Optional existing exercise-page IDs. Each must resolve to a published `type:exercise-hub`, `destination:practice` page in the matching language. Omit the field when no sufficiently relevant exercise page exists; do not create artificial links to fill all 24 days. |
| Concept domains and importance | `data/concepts.yml` and `data/domains.yml` | Derive domain facets from referenced concepts when needed (the day-level domain view may be the union, retaining concept provenance). Keep importance attached to each concept; do not collapse several importance values into a synthetic day-level rank. Never copy `domains` or `importance` into each day, because that would drift from the concept registry. |
| Computational branch membership | `data/computational-graph.yml` | Derive branch membership from the referenced nodes. It is not a calendar act or a prerequisite edge. |
| Daily question, micro-outcome, activity, duration, day number, act | Calendar manifest | Calendar-specific editorial information. The micro-outcome is deliberately narrower than a page's `purpose`; it is not a replacement for the page learning contract. |

The distinction between concept and computational-node references is intentional. For example, token IDs are represented as nodes in the computational graph, while the broader token concept is in the concept registry. Likewise, the Transformer-block computation is represented in the computational graph; it must not be invented as a concept merely to populate a calendar field. Days 2, 4, 8, and 12 therefore include computational-node references for important aspects that do not currently have matching first-class concept records. Day 12 currently resolves to the aggregate `block-update` node: this anchors the block-level transformation but does not claim that MLP, residual connections, and normalization are separately represented in the graph. If those operations later need first-class nodes or concepts, that should be justified by the wider computational/knowledge model, not by the calendar alone.

Do not copy page tags into the manifest. In particular:

- `topic` is a page-grouping identifier, not a concept ID or calendar-day ID.
- `level` describes editorial depth, not calendar difficulty or mandatory status.
- `destination` and `type` classify the linked page, not the calendar entry.
- `domain` is a primary classification for eligible Deepen pages; it is not a field to add to calendar days. Concept domains remain multi-valued in the concept registry.
- `status` and `language` belong to the linked page record. The calendar itself has its own lifecycle status and bilingual content.

This avoids creating a competing taxonomy while preserving useful derived views. A future calendar renderer may filter days by concept domain or show concept-level importance, or show “Understand” / “Build” / “Deepen” / “Practice” links. It must resolve those labels from the canonical registries and render localized human-readable text rather than exposing raw IDs. Days with no concept references have no derived concept domain or importance; do not infer them from a computational node.

### 7.2 Validation expectations for metadata links

In addition to the checks above, validate:

1. Every `concepts` entry resolves to a concept ID in `data/concepts.yml`.
2. Every `computational_nodes` entry resolves to a node ID (not merely a branch or edge) in `data/computational-graph.yml`.
3. Every `lesson_pages` entry resolves to a published page with `destination:understand` or `destination:orient` and the correct language; FR and EN counterparts must be semantically aligned.
4. Every `practice_pages` entry resolves to a published `exercise-hub` in `practice`, with the correct language. Where an exercise companion follows the established convention, its topic should be the topic of the corresponding lesson or Build page plus `-exercises`.
5. Every `build_pages` entry resolves to a published page in `build` with the correct language; its type must be one of the existing Build-capable types (`guided-build` or `concept-bridge`). It must remain separate from the conceptual lesson.
6. Every `deepening_pages` entry resolves to a published `deep-dive` page in `deepen`, with the correct language. It must remain optional and must not become a hidden prerequisite.
7. Do not require every day to have a concept, computational node, exercise link, Build companion, or deepening link if the knowledge model does not currently represent one. Record a genuine registry gap for review rather than fabricating a reference.
8. If a derived view needs concept importance, domains, or computational branches, compute them from their canonical owner; do not persist a copied value in the calendar manifest.
9. Calendar order must not be translated into `prerequisite` concept relations, `hierarchy` page relations, or computational edges.

The manifest uses `lesson_pages`, `computational_nodes`, and optional `build_pages`, `deepening_pages`, and `practice_pages` to make these ownership boundaries explicit. The previous generic `resources` field is intentionally avoided because the repository now distinguishes page resources from first-class non-page resources in `data/resources.yml`.

### Manifest-level validation expectations

In addition to the metadata-reference checks in §7.2, a future validator should check:

1. Exactly 24 unique day numbers, with no gaps.
2. Unique, stable day IDs and valid act references.
3. Both FR and EN titles, questions, and outcomes.
4. Activity types belong to the controlled set and duration estimates are positive, bounded values.
5. No duplicate primary topic without an explicit pedagogical rationale.
6. No calendar ordering is accidentally exported as hard prerequisite edges.
7. No reader-facing YAML metadata is rendered as lesson prose.

Do not add a new CI workflow for this feature. Extend an existing validation/build entry point only when the data model and acceptance rules are stable and the check provides real value.

## 8. Comparable projects and lessons

The following projects were checked on 2026-11-22. They are format references, not content sources to copy. Their current editions may change.

| Project | Format | Useful lesson for LLM Lab | Boundary / caution |
|---|---|---|---|
| [Advent of Code](https://adventofcode.com/about) | Daily programming puzzles with examples, testable answers, and a generally increasing challenge | A daily problem should require reasoning; examples and hand-checkable tests help learners diagnose misunderstandings | Do not copy its text, visual identity, or distinctive calendar design. Its official page explicitly restricts copying and replication of its design |
| [DFKI/RPTU AI Advent Calendar](https://www.ki-adventskalender.de/en/) | 24 doors and interactive AI tasks, aimed at school learners | A clear daily challenge can introduce AI concepts without assuming programming expertise | Different audience and scope; use its low-threshold approach, not its contest/prize model |
| [Advent ML](https://mlatlas.org/en/advent/) | 12 reproducible ML tasks with fixed settings and numerical answers | Explicit seeds, parameters, tolerances, and worked solutions make small experiments verifiable | Twelve tasks, not a 24-day conceptual LLM curriculum; its numerical checking model is not suitable for every concept |
| [Santa has Everything under Control](https://www.research.unipd.it/handle/11577/3542097) | Research paper describing a 24-problem control-engineering advent calendar and feedback from university students | Collaborative question design and learner feedback are useful for evaluating educational value | Different technical domain; consult the paper for design/assessment lessons rather than borrowing exercises |
| [LLM Daily](https://llmdaily.org/) | A growing set of short lessons on training, inference, and LLM systems | Strong reference for technical granularity and concise explanations of topics such as prefill/decode and tensor shapes | It is a daily lesson collection, not an advent calendar or the canonical syllabus for this project |
| [The AI-dvent Calendar — Context Jamming](https://www.contextjamming.com/AI-dventCalendar) | 25 mixed-format entries behind a visual grid, openable in any order | Useful reference for visual discovery, mixed media, and an accessible plain-link index | Its intentionally non-linear collection differs from LLM Lab's progressive sequence; the current edition is not a vetted LLM curriculum |

### Synthesis

Combine:
- Advent of Code's problem-solving and worked-example discipline;
- DFKI/RPTU's approachable daily discovery;
- Advent ML's reproducibility and answer verification;
- the control-calendar paper's attention to collaborative design and learner feedback;
- LLM Daily's short technical lessons;
- Context Jamming's visual discovery and alternative text index.

Do **not** combine them into a competition or a generic link collection. LLM Lab's differentiator is a carefully justified conceptual progression grounded in its own knowledge model.

## 9. Evaluation and acceptance criteria

Evaluate more than clicks or completed doors.

### Content-level checks

- A learner can state the day's central idea in their own words.
- The active check tests the stated outcome rather than trivia.
- The day does not introduce an unmarked prerequisite.
- The explanation agrees with the canonical page and computational graph.
- The example is reproducible and includes assumptions, shapes, or parameter settings when relevant.
- FR and EN preserve the same technical claims and caveats.

### Pilot evaluation

Before producing all 24 days, pilot three deliberately different topics:

1. **Tokenization:** accessible input concept.
2. **Q/K/V:** internal computational mechanism.
3. **Cross-entropy:** mathematical/probabilistic concept.

For each, record:
- actual completion time;
- points where a novice hesitates or misinterprets a term;
- whether the learner can answer the active check without guessing;
- whether they can transfer the idea to a changed example;
- whether the canonical follow-up page is useful and discoverable;
- editorial/implementation effort.

Revise the template based on this evidence before scaling to 24 entries.

### Release gate

Do not publish the calendar as a finished learning product until:
- the 24-day sequence has passed a dependency and coverage review;
- all referenced resources are valid;
- the three-day pilot has been reviewed;
- FR/EN parity is checked;
- keyboard, screen-reader, reduced-motion, and responsive behavior are reviewed;
- scientific claims and provenance are checked;
- the public project status accurately describes what exists and what remains planned.

## 10. Phased delivery

1. **Design and inventory:** audit concepts, computation nodes, route stages, published pages, and exercise resources; resolve gaps and day boundaries.
2. **Sequence review:** score candidate topics for importance, readiness, prerequisite fit, teachability in 5–8 minutes, activity potential, coverage, and complementarity. Record why each topic is included or deferred.
3. **Three-day pilot:** author tokenization, Q/K/V, and cross-entropy entries; run a novice review and revise the content contract.

   The reader-facing calendar now contains guided orientation pages for days 01–03. The selected content-validation pilot remains days 03, 09 and 21: these are three deliberately different concepts, not necessarily three consecutive doors. The adjacent drafts for days 04–06 remain in `docs/advent-calendar-pilot-content.md` to support continuity review.
4. **Manifest and validation:** stabilize the YAML schema, then add a small validator to an existing build/test path.
5. **Content production:** author the remaining entries and review bilingual parity.
6. **Interface:** bilingual 24-door view implemented using the existing site design system and navigation; responsive and interaction review remains part of the release gate.
7. **Release and maintenance:** publish the evergreen archive, check links and content yearly, and review whether the calendar remains aligned with the canonical concepts and routes.

The calendar is successful if it helps a reader build and transfer a correct mental model of LLM computation—not merely if all 24 doors are opened.


## 11. First reader-facing implementation

The calendar landing page is implemented in French and English at `site/fr/advent-calendar.qmd` and `site/en/advent-calendar.qmd`, with shared responsive styling in `site/styles/advent-calendar.css`. It presents all 24 days in four editorial acts. The first three doors receive a distinct visual treatment and open dedicated short-form learning pages; the remaining days continue to point to canonical LLM Lab lessons and their separate practice resources.

The first three daily pages are implemented in both languages:

| Day | Daily page | Learning boundary |
|---:|---|---|
| 01 | `advent-calendar-day-01.qmd` | Conditional next-token distribution; distinguish prediction from decoding selection |
| 02 | `advent-calendar-day-02.qmd` | Immediate supplied prefix; distinguish context from continuation and from application-level context design |
| 03 | `advent-calendar-day-03.qmd` | Text segmentation into ordered tokens; token IDs and embedding lookup remain for days 4 and 5 |

Each daily page contains one question, a concise explanation, a worked example or trace, one self-check with a disclosed answer, a takeaway, and links to the canonical lesson and exercise hub. The sequence follows the shared computation `context → f_θ(context) → logits → softmax → conditional distribution`; it does not imply that decoding selection is part of the model's probability calculation.

The first three daily page IDs are also recorded in the YAML manifest and in the landing page's hidden page-map metadata. The six daily pages are classified as `destination:orient`, `level:overview`, and `type:concept-bridge`: they are short guided introductions, not duplicate canonical lessons. This keeps them out of the Understand/Build revision-coverage inventory while retaining them in the bilingual learning-map data. The manifest remains an editorial proposal and is **not yet consumed by Quarto or CI**. The bilingual landing pages and daily pages are currently maintained as QMD files. A later change should add a lightweight consistency validator or generator rather than introducing a second registry or a dedicated workflow.

**Validation status:** the full Quarto render and local-link audit have passed on an earlier revision. CI now checks the calendar landing page and the three guided days in both languages at desktop and mobile widths, including the 24-door sequence, first-three-day targets, keyboard-operated self-checks, and canonical resource links. The final CI run and screenshot review are still required. The entries remain editorial drafts, not learner-validated content.
