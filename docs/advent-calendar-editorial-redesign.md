# LLM Lab Advent Calendar — editorial redesign

**Status:** approved editorial direction; 2026 edition uses one permanent Deepen lesson per door  
**Date:** 2026-11-23

> **Production-order decision (2026-11-23):** draft, review and validate the stories in calendar order (Day 01, then Day 02, and so on). The earlier proposal to prepare non-adjacent pilots (Days 06, 17 and 23) is superseded as a production strategy. The stories remain independent for readers: chronological authoring does not create prerequisite dependencies.  
**Scope:** 24 independent, approximately 10-minute readings for December 1–24  
**Languages:** French and English  
**Audience:** curious readers, from mathematically literate beginners to LLM practitioners

## 1. Decision: change the product, not just the page template

The first calendar prototype is not sufficiently valuable in its current form:

- its entries summarize concepts that already have canonical lessons in the main learning path;
- the short 5–8 minute format produces shallow explanations rather than self-contained readings;
- the sequence follows the main curriculum so closely that it acts as a second, weaker navigation layer;
- the custom page presentation is fragile and has not passed a satisfactory visual review.

The calendar should therefore **stop being a compressed version of the main LLM Lab curriculum**.

### New editorial promise

> Every day, open an independent scientific story about one idea from mathematics, statistics, information theory, computer science, or modern language-model research. In about ten minutes, understand the question, follow a worked example, and leave with an experiment or a new way to think.

The calendar becomes a collection of 24 story-led Deepen lessons, not a prerequisite path or a duplicate curriculum. A reader can open day 17 before day 3 and still understand it. The entries are connected by a shared interest in mathematics and LLMs, not by a dependency chain.

The calendar should have value even for someone who has already completed the main learning path.

## 2. Relationship with the main LLM Lab

The two experiences have different jobs.

| Main learning path | Advent calendar |
|---|---|
| Teaches the complete LLM mechanism in a coherent progression | Explores selected ideas through independent stories |
| Establishes canonical definitions and dependencies | Builds intuition, historical context, mathematical connections, and critical perspective |
| Moves from foundations to implementation | Moves between mathematics, information theory, research findings, and practical consequences |
| Uses lessons and dedicated exercise pages | Uses one self-contained feature per day, with a small experiment or challenge |
| Is cumulative where prerequisites matter | Is deliberately non-cumulative |

### One permanent lesson behind every door

The calendar is a seasonal presentation layer over the permanent **Deepen** collection. Each of the 24 doors must lead to one identifiable, durable lesson in Deepen.

The relationship is:

`one door → one story-led lesson → one Deepen page`

The calendar and Deepen must not contain two copies of the same article. The page behind the door is the canonical lesson itself: it opens with the narrative hook that makes the door attractive, then develops the subject as a rigorous lesson. The calendar landing page presents the 24 doors; it does not reproduce their lesson content.

A door therefore has two complementary roles:

- **Seasonal role:** a short title, question, visual and teaser that create curiosity during December.
- **Learning role:** a permanent Deepen lesson with enough substance to remain useful after the calendar is archived.

The lesson must stand on its own. It should not require the reader to have opened earlier doors or completed the main learning path. Its placement in Deepen is based on its lasting intellectual subject, not on its December date.

### Deepen integration contract

Every door must resolve to a bilingual page identity (French and English) and a primary Deepen domain. The calendar manifest records this relationship explicitly.

For each lesson:

1. Reuse an existing Deepen page when its scope genuinely matches the story; audit and improve it rather than creating a duplicate.
2. If no suitable page exists, create a dedicated Deepen page. Do not point to a broad or only loosely related page merely to fill the calendar.
3. Keep the story and the lesson in the same page. The narrative is the entry point; the mathematical, conceptual and experimental development is the lesson.
4. Add the page to the appropriate thematic section of `site/fr/deepen.qmd` and its English counterpart, with the project's normal metadata and bilingual navigation.
5. Connect it to canonical concepts, domains, the knowledge map and relevant main-path pages. These are semantic links, not new prerequisites.
6. Keep exercises in the dedicated Practice & experiment area where they grow independently; the lesson may include one small challenge, but must link to the full exercise page when one exists.
7. Keep the calendar's seasonal presentation separate from the page's permanent identity. Archiving an edition must never archive, move or hide its Deepen lessons.

A page can be linked from several annual editions if it remains the right canonical lesson. A later edition may also point to a substantially revised lesson, but the historical manifest must preserve which page each edition originally featured.

The 2026 mapping is maintained in `data/calendars/advent-2026.yml`. Each entry records the door, the permanent page ID, its primary Deepen domain, whether the page is reused or still needs to be created, and its FR/EN counterparts. A planned page is not considered published until its content, metadata, navigation and Deepen placement have been validated.

## 3. The daily reading contract

**Target: approximately 10 minutes per language version**, excluding optional links.

A typical entry should contain 1,000–1,400 words in French (adjust after testing), with mathematical and visual material contributing to understanding rather than padding the word count.

Every entry must include:

1. **A narrative hook** — a puzzle, historical episode, counter-intuitive result, concrete failure, or practical dilemma.
2. **The question** — one precise question the reader will be able to answer.
3. **The story** — explain why the problem arose, what idea addressed it, and what changed.
4. **The mathematics** — derive or interpret at least one relevant equation when the subject permits it; define symbols and assumptions.
5. **A worked example** — numerical, geometric, textual, or computational, small enough to follow.
6. **A limitation or counterexample** — explain what the idea does not establish and where the analogy breaks.
7. **A small challenge or experiment** — something the reader can calculate, predict, inspect, or modify in a few minutes, with a worked answer or feedback.
8. **A closing insight** — one precise takeaway, not a generic recap.
9. **Optional further reading** — sources and, where genuinely useful, one canonical LLM Lab lesson.

A story is not an excuse for imprecision. Historical claims, empirical results, equations, and model-specific claims must be sourced and checked. Clearly label toy examples, empirical observations, hypotheses, and analogies.

### Editorial voice

- Explain the problem before naming the technique.
- Prefer one concrete example developed carefully over a catalogue of terms.
- Make the mathematical reasoning visible; do not hide it behind metaphors.
- Use diagrams only when they explain structure, geometry, a process, or a comparison that prose cannot show as clearly.
- Avoid generic AI hype, claims of human-like understanding, and unsupported claims about emergent abilities.
- Use a narrative arc, but do not force all 24 entries into the same fictional storyline.

## 4. Proposed collection of 24 independent stories

The four groups below are **editorial shelves**, not acts in a learning sequence. No group or day is a prerequisite for another.

| Day | Working title | Narrative hook / story | Main mathematical or LLM connection | Distinct value beyond the main path |
|---:|---|---|---|---|
| 01 | **Why does the word “the” appear everywhere?** | A journey through word-frequency rankings and the surprising regularity of natural language. | Zipf's law, rank-frequency distributions, heavy tails, token-frequency imbalance. | Explains why language data are statistically uneven and why rare tokens are difficult; not a tokenization lesson. |
| 02 | **How many bits does a sentence surprise us with?** | Shannon's information problem: how to quantify uncertainty before knowing the outcome. | Self-information, entropy, conditional entropy, surprisal. | Builds an information-theoretic lens for language, not a softmax/probability walkthrough. |
| 03 | **The tokenizer as a compression engineer** | Why a vocabulary must balance reusable chunks against sequence length; how pair-merging became a practical strategy. | Byte-pair encoding, greedy merges, compression trade-offs, vocabulary size. | A design trade-off and miniature tokenizer experiment, not a basic segmentation tutorial. |
| 04 | **Can meaning have a direction?** | The geometric surprise of vector representations and the famous analogy experiments, followed by their limits. | Vector spaces, cosine similarity, linear offsets, distributional semantics. | Critical geometric interpretation rather than embedding lookup. |
| 05 | **The same word, two different worlds** | “Bank” in a river sentence and a finance sentence: why a static vector is not enough. | Polysemy, contextual representations, representation geometry. | Explores ambiguity and context through a case study rather than explaining the Transformer pipeline. |
| 06 | **What does a sine wave have to do with word order?** | The use of multiple frequencies to give a sequence a sense of position. | Sinusoidal positional encodings, Fourier features, frequency scales, relative phase. | A mathematical connection to signal processing, not a catalogue of positional methods. |
| 07 | **Attention as a learned retrieval system** | A query seeks relevant records; keys determine match and values carry retrieved content. | Q/K/V as query–index–payload, dot-product retrieval, weighted aggregation. | Uses an information-retrieval/database lens and a concrete counterexample; not a second QKV lesson. |
| 08 | **Why divide by the square root of the dimension?** | As vector dimension grows, unscaled dot products become numerically awkward. | Variance of dot products, concentration, scaling by \(\sqrt{d_k}\). | Derives a design choice from assumptions and checks what changes when they fail. |
| 09 | **Softmax and the physics of a crowd** | A system distributes probability among competing states; temperature changes concentration. | Partition functions, Boltzmann distributions, temperature, softmax invariances. | Connects ML to statistical mechanics; not a routine softmax calculation. |
| 10 | **The triangular wall: preventing information leaks** | A model that can peek at the answer key appears brilliant until the test is run properly. | Causal masks, information flow, leakage, triangular dependency constraints. | Frames causality as an information-access rule and compares it with data leakage. |
| 11 | **Why do deep networks keep a residual stream?** | A sequence of transformations can destroy useful information; an identity path offers a stable route. | Residual mappings \(x + F(x)\), iterative refinement, Jacobian intuition. | Explains residual connections through optimization and signal preservation, beyond block anatomy. |
| 12 | **Normalization: changing coordinates to make learning easier** | Why scale and shift intermediate activations, and what normalization does not guarantee. | Mean/variance, LayerNorm, RMSNorm, scale invariance, conditioning. | Compares normalization choices and their assumptions rather than listing sublayers. |
| 13 | **Perplexity: how surprised was the model?** | Two models predict the same text; how can we compare their predictive performance? | Geometric mean probability, cross-entropy, perplexity, tokenization dependence. | Critical interpretation of a metric: what it measures, what it does not, and why comparisons can mislead. |
| 14 | **Temperature: creativity or just a flatter distribution?** | The same logits produce different sampling behaviour when the temperature changes. | Logit scaling, entropy, softmax, sampling variance. | An experimental investigation of a decoding parameter, not a general decoding tutorial. |
| 15 | **Top-k and top-p: where should the probability tail end?** | A long tail of low-probability candidates raises a practical selection problem. | Truncation, cumulative mass, discrete distributions, diversity. | Compares two policies on a hand-built distribution and identifies edge cases. |
| 16 | **Why the most likely next word can make a worse sentence** | Local greedy choices can block a better global sequence; search and sampling make different compromises. | Greedy decoding, beam search, sequence scores, length bias. | Studies local-vs-global optimization and its failure modes. |
| 17 | **Cross-entropy as a code length** | If a message is encoded with the wrong probability model, how many extra bits are paid? | Shannon coding intuition, cross-entropy, KL divergence, coding regret. | A deeper information-theoretic meaning of the training objective, not a loss-function recipe. |
| 18 | **Why multiply probabilities when we can add log-probabilities?** | A long sequence produces tiny products; logarithms turn the calculation into a stable sum. | Chain rule, likelihood, log-likelihood, numerical underflow. | A numerical and probabilistic story distinct from teacher forcing or training-loop mechanics. |
| 19 | **The chain rule: how does an error reach an early layer?** | A final prediction depends on many nested transformations; how can its loss inform earlier parameters? | Derivatives of compositions, chain rule, computational graphs, backpropagation. | A worked mathematical derivation with a tiny network, not a generic backpropagation overview. |
| 20 | **The learning-rate cliff** | One optimizer step barely moves; another overshoots. What determines a useful step size? | Gradient descent, curvature, conditioning, stability, learning-rate schedules. | Explains optimization geometry and practical failure rather than the optimizer API. |
| 21 | **When a model gets worse before it gets better** | The double-descent phenomenon challenges the simplest picture of model complexity. | Bias–variance intuition, interpolation threshold, double descent, generalization. | A research-story about empirical generalization; requires careful qualifications and sources. |
| 22 | **Do bigger models become predictable?** | Empirical scaling curves invite extrapolation — and can be misused. | Scaling laws, power laws, compute/data/parameter trade-offs, uncertainty in extrapolation. | Teaches how to read empirical laws and their limits, not a Transformer architecture lesson. |
| 23 | **What if the model could look things up?** | A model answers from parameters alone, then is given an external library it can search. | Retrieval-augmented generation, nearest-neighbour search, external memory, grounding. | Introduces a complementary system-level design beyond the core model computation. |
| 24 | **Making a model smaller without retraining everything** | Memory and bandwidth limits motivate lower-precision representations. | Quantization, rounding error, dynamic range, calibration, memory/quality trade-offs. | A practical numerical-computing story beyond the main conceptual training path. |

### Selection and balance notes

For the wider set of scientific, historical, linguistic, mathematical, experimental, philosophical and sociotechnical perspectives that may inform later editions, see the [thematic landscape and future story candidates](advent-calendar-thematic-landscape.md). That document is a discovery backlog only: it does not change this approved 2026 slate, add days, or alter chronological production.

- The list deliberately alternates between information theory, probability, geometry, numerical analysis, optimization, and LLM system design.
- Some subjects (attention, normalization, cross-entropy, backpropagation) exist in the main curriculum. Their calendar angle must be materially different as specified above; if the pilot reveals duplication, replace the story.
- Day 21 (double descent) and day 22 (scaling laws) require careful primary-source review and must not be presented as universal laws.
- Day 23 is the only strongly system/application-oriented entry; it is included to widen the view beyond the internal Transformer.
- The proposed titles and hooks are editorial hypotheses, not final copy. Each story needs a source dossier and scientific review before publication.

## 5. Page design: prioritize reliable rendering and reading

The current custom HTML/CSS day pages have not met the quality bar. Do not scale this implementation to 24 pages.

### New page layout

Use a restrained, readable Quarto article layout:

1. A compact calendar breadcrumb and day number.
2. A title, one-sentence hook, reading-time estimate, and small topic label.
3. A narrow main reading column with consistent heading hierarchy.
4. Equations using standard Quarto/MathJax delimiters.
5. Figures with captions, source, alt text, and responsive sizing.
6. Small callouts only for a real distinction, warning, or result.
7. One challenge with a visible answer/solution.
8. Sources and optional further reading.
9. A compact previous/next navigation, explicitly labelled as browsing rather than prerequisites.

### Visual rules

- Reuse the existing LLM Lab typography and restrained forest-green palette.
- Do not wrap all article content in custom grid/flex containers.
- Avoid hand-authored inline CSS for layout.
- Avoid nested custom HTML blocks around Markdown headings, lists, equations, and tables; they are a common source of Quarto rendering surprises.
- Use native Markdown and Quarto features first. Add a custom component only when its output is tested in the rendered site.
- Equations must be checked in the actual rendered FR and EN pages, not only in source.
- Tables must remain readable on mobile; replace wide tables with structured subsections where necessary.
- Figures must retain their aspect ratio and never overflow the reading column.
- Keyboard focus, link contrast, reduced motion, and screen-reader semantics are release requirements.

### Required visual QA for every pilot

- Render the full Quarto site locally.
- Inspect FR and EN pages on desktop and mobile widths.
- Check headings, equations, code, figures, captions, tables, callouts, and answer disclosures.
- Check navigation and every internal link.
- Run the repository's accessibility/browser audit.
- Capture screenshots for review; do not treat CI success as proof of editorial or visual quality.

## 6. Source and scientific quality

Each day must have a source dossier with:

- one or more primary or authoritative sources for central claims;
- publication details and stable links;
- license/provenance notes for figures and adapted material;
- claims that need qualification;
- a short list of facts or analogies explicitly excluded because evidence is weak.

Preferred sources include original research papers, textbooks, author documentation, reputable technical articles, and reproducible demonstrations. Secondary explainers may help with pedagogy but should not be the sole source for a scientific claim.

For research phenomena (double descent, scaling laws, representation analogies), distinguish:
- mathematical results under stated assumptions;
- empirical observations on specific models/datasets;
- proposed explanations;
- open questions and limits to generalization.

## 7. Chronological production with per-day validation

Produce the new edition in calendar order: Day 01, then Day 02, continuing through Day 24. Do not skip ahead to later stories during normal content production.

This is a production and quality-control rule, **not a prerequisite sequence for readers**. Each story must remain understandable on its own, without requiring the previous day or a canonical lesson.

For every day, follow the same controlled cycle:

1. Confirm the day's question, distinct editorial angle and boundary against the main curriculum.
2. Prepare a source dossier before drafting: primary sources, claim-to-source mapping, caveats, excluded claims and visual provenance.
3. Draft the French and English versions together, preserving conceptual parity rather than translating mechanically.
4. Include a worked example and a meaningful challenge with a solution.
5. Review mathematical/scientific correctness and the anti-duplication boundary.
6. Render both languages and inspect equations, figures, tables, links and responsive layout.
7. Run accessibility checks and obtain a novice read-through; record actual reading time and points of confusion.
8. Revise and accept the day before starting the next day.

A day passes only if it is a complete independent reading, adds a distinct perspective, has a complete source dossier, renders correctly in both languages, and passes the novice and accessibility reviews. If it fails, revise that day; do not work around the failure by moving on to later days.

The previous non-adjacent pilot proposal (Days 06, 17 and 23) was useful for considering topic diversity, but is no longer the production plan. Day 06 is retained as reference material for comparison, not as a template to copy. Days 17 and 23 will be reached in their chronological turn.

## 8. Migration and implementation plan

1. **Freeze the current day pages as prototype material.** Do not extend their short-form template.
2. Keep the current 24-day curriculum-summary manifest as historical/prototype input; mark it superseded once the new manifest is approved. Do not silently reinterpret its entries.
3. Approve the new editorial promise and story slate.
4. Build one article template using standard Quarto rendering and validate it with Day 01.
5. Add a new story-oriented manifest once the initial template and Day 01 pass review. It should reference concepts and optional lessons but not own canonical definitions or prerequisite edges.
6. Replace the calendar landing page's curriculum-like four acts with thematic shelves that communicate independent reading.
7. Produce and validate Days 01–24 in chronological order, applying the per-day acceptance gate before proceeding.
8. Publish only accepted stories; keep drafts out of the public calendar until their content, source, visual, accessibility and novice-review gates pass.

The old pages should not be deleted until the new experience is ready. Their useful content can be mined for source leads or linked back to canonical lessons, but duplicated short explanations should not be carried over automatically.

## 9. Explicit non-goals

- A second guided route through the canonical Transformer pipeline.
- A sequence that requires reading days in numerical order.
- Twenty-four miniature textbook chapters that merely paraphrase existing pages.
- A story format that sacrifices mathematical correctness.
- A bespoke interaction or diagram on every page.
- A new parallel concept ontology, computational graph, or prerequisite system.
- Treating calendar completion as evidence of mastery.

## 10. Immediate next actions

- Review and approve this new editorial direction.
- Audit the existing calendar landing page and current day pages for rendering defects; keep the old experience clearly marked as a prototype during transition.
- Build and visually test the article template before migrating content.
- Continue with Day 01 only: complete its scientific, editorial, bilingual, rendered, accessibility and novice-review gates.
- Draft Day 02 only after Day 01 is accepted, then continue in numerical order; retain the same per-day acceptance gate throughout.
