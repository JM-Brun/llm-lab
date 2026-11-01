# LLM history: editorial model and data contract

**Status:** design proposal, 2026-10-31  
**Owner:** [issue #197](https://github.com/JM-Brun/llm-lab/issues/197)  
**Purpose:** define a source-backed, bilingual historical dataset that can support a chronology, a concept-genealogy view, and concise milestone pages without duplicating content or creating a second curriculum.

This document defines the historical content model and editorial rules. It is not yet the implementation of the public timeline or an exhaustive history of language modelling.

## 1. Product boundary

The history page is an optional reference resource. It answers:

- What problems and research traditions preceded modern LLMs?
- Which contributions changed the available modelling, training, or inference approaches?
- Which developments happened in parallel?
- How are research contributions, model releases, and ecosystem events different?
- Where can a reader study a concept in more detail?

It does **not** replace the conceptual course, the guided GPT build, or the deep-dive pages. The canonical concept page remains the explanation of a mechanism; the history page explains its historical context and links to that page.

### Three event streams

Keep these event types distinct in the data and in the visual design:

| Stream | Includes | Does not imply |
|---|---|---|
| **research** | Papers, methods, architectures, training objectives, empirical findings | A production model or product was released |
| **model_release** | Public model/checkpoint/API releases and major version milestones | The underlying method was invented at release time |
| **ecosystem** | Products, infrastructure, standards, policy, adoption milestones | A scientific contribution or proof of technical priority |

A milestone may be linked to another stream, but must have one primary type. For example, the 2022 ChatGPT launch is an ecosystem/product event; InstructGPT is a research/model-training contribution. They should not be collapsed into one event.

## 2. Core entities

The first version needs only four entity types:

1. **Event** — something that happened at a date or interval.
2. **Concept** — a reusable technical idea or method, linked to canonical LLM Lab lessons when available.
3. **Source** — a paper, technical report, official announcement, standard, or carefully selected secondary source.
4. **Relation** — an explicitly typed, evidence-backed relationship between events or concepts.

People, laboratories, products and model families can initially be plain metadata on events. Do not create a separate entity catalogue until a real navigation use case requires it.

## 3. Event record

Each event has a stable, language-neutral ID. Translated text lives side-by-side in the same record so that French and English cannot silently drift into different event inventories.

| Field | Required | Meaning |
|---|---:|---|
| **id** | yes | Stable kebab-case identifier; never derive from translated title |
| **type** | yes | research, model_release, or ecosystem |
| **date** | yes | Structured date with precision and semantic type |
| **era** | yes | Broad editorial grouping, not a claim of a clean historical break |
| **title.fr**, **title.en** | yes | Concise bilingual title |
| **summary.fr**, **summary.en** | yes | One or two sentences explaining what changed and why it matters |
| **significance** | yes | Controlled tag(s): architecture, objective, data, scaling, efficiency, alignment, inference, multimodal, ecosystem, etc. |
| **concept_ids** | no | Concepts materially involved in the event |
| **internal_links.fr**, **internal_links.en** | no | Existing canonical pages only; omit if no page exists |
| **source_ids** | yes | At least one source supporting the event and its date |
| **people**, **organizations**, **model_families** | no | Names, not an implied attribution of sole invention |
| **editorial_note** | no | Dating ambiguity, parallel work, contested attribution, or scope caveat |
| **confidence** | yes | high, medium, or provisional, with rationale for non-high values |

### Date semantics

A date is not just a string. Use:

- **value**: ISO date (YYYY-MM-DD), year-month (YYYY-MM), or year (YYYY);
- **end_value**: optional inclusive end date/month/year, using the same precision, for events spanning an interval;
- **precision**: day, month, or year;
- **kind**: proposal, submission, publication, announcement, release, adoption, or other;
- **note**: optional explanation when multiple dates matter.

Do not invent a day when only a year or month is supported. For a staged release or other interval, use `end_value` rather than presenting the first date as if it described the whole interval. If proposal, publication and release dates differ, either represent distinct events or explain the distinction in the date note.

## 4. Concept record

A concept is a technical idea that can recur across several events and model families.

| Field | Required | Meaning |
|---|---:|---|
| **id** | yes | Stable language-neutral identifier |
| **name.fr**, **name.en** | yes | Bilingual canonical name |
| **description.fr**, **description.en** | yes | Short historical/technical definition, not a duplicate lesson |
| **domain** | yes | Controlled domain such as architecture, representation, objective, optimization, alignment, inference, efficiency |
| **internal_page.fr**, **internal_page.en** | no | Existing canonical lesson path only |
| **source_ids** | yes | Sources establishing the concept and/or its historical introduction |

A concept without an internal page is still valid. The UI should link to its strongest source and must not render a fake “learn more” destination.

## 5. Relation record: genealogy without false causality

Relations must be explicit and typed. Avoid a generic arrow labelled “led to”.

Initial relation vocabulary:

| Relation | Meaning | Evidence standard |
|---|---|---|
| **precursor_to** | Earlier work established a relevant component or problem formulation | Explain the shared mechanism/problem; do not imply direct citation or influence |
| **influenced** | Later work explicitly builds on or cites earlier work | Direct citation, author statement, or documented technical lineage |
| **extends** | Later work generalizes or modifies a prior method | Compare the specific technical change |
| **parallel_to** | Similar problem/idea developed independently or contemporaneously | Evidence for temporal/conceptual parallelism; do not draw a parent-child tree |
| **combines** | Work combines multiple previously available ideas | Cite the combination and identify its components |
| **alternative_to** | Competing approach to a similar problem | State the shared problem and material difference |
| **supersedes_in_context** | Later method replaces an earlier one for a stated use case | Name the context and evidence; never imply universal replacement |
| **applied_in** | Concept/method appears in a named model or system | Primary model paper or official technical report |

Each relation requires:

- **from** and **to** stable IDs;
- **type**;
- **rationale.fr** and **rationale.en** (short, factual);
- **source_ids** supporting the relationship;
- optional **confidence** and **editorial_note**.

**Important:** chronological order alone supports neither influenced nor extends. Use precursor_to only when a genuine technical antecedent can be explained. If the relationship is merely contextual, omit the edge.

## 6. Source record and evidence policy

| Field | Required | Meaning |
|---|---:|---|
| **id** | yes | Stable source identifier |
| **kind** | yes | primary_paper, technical_report, official_announcement, standard, or secondary_review |
| **title** | yes | Original title |
| **authors_or_organization** | yes | Authors or issuing organization |
| **date** | yes | Source publication/announcement date when known |
| **url** | yes | Stable DOI, arXiv, proceedings, official paper or announcement URL |
| **supports** | yes | Claim(s) supported: event date, contribution, relation, release, etc. |
| **accessed** | no | Date checked for mutable web sources |

Evidence hierarchy:

1. Original paper/proceedings or primary technical report for a research contribution.
2. Official release note/model card/announcement for a release.
3. Institutional or standards source for infrastructure/policy facts.
4. Scholarly review for context, discovery of candidate sources, and historiographical framing.

Secondary timelines and AI-generated catalogues are **discovery aids**, not evidence of historical facts. Verify each selected event against primary sources. A citation must support the claim beside it, not merely mention the same topic.

## 7. Illustrative record shape

The following is a schema illustration, not a complete or validated production dataset:

~~~yaml
events:
  - id: transformer-attention-is-all-you-need
    type: research
    date:
      value: "2017"
      precision: year
      kind: publication
      note: "Use a more precise date only if the chosen source and editorial convention justify it."
    era: transformer-and-pretraining
    title:
      fr: "Architecture Transformer"
      en: "Transformer architecture"
    summary:
      fr: "Propose une architecture encodeur-décodeur fondée sur l'attention pour la traduction automatique."
      en: "Proposes an attention-based encoder-decoder architecture for machine translation."
    significance: [architecture, attention]
    concept_ids: [self-attention, multi-head-attention]
    internal_links:
      fr: [fr/transformer.qmd, fr/scaled-dot-product-attention.qmd]
      en: [en/transformer.qmd, en/scaled-dot-product-attention.qmd]
    source_ids: [vaswani-2017-attention-is-all-you-need]
    confidence: high

relations:
  - from: bahdanau-2014-neural-machine-translation
    to: transformer-attention-is-all-you-need
    type: precursor_to
    rationale:
      fr: "Les mécanismes d'attention pour l'encodeur-décodeur récurrent constituent un antécédent pertinent, sans être l'architecture Transformer."
      en: "Attention for recurrent encoder-decoder models is a relevant antecedent, but is not the Transformer architecture."
    source_ids:
      - bahdanau-2014-neural-machine-translation
      - vaswani-2017-attention-is-all-you-need
    confidence: high
~~~

The example intentionally uses year-level precision and a cautious relation. The production dataset must verify exact bibliographic metadata and all internal destinations before publication.

## 8. Editorial eras and candidate coverage

Use eras as scan-friendly groupings, not rigid periodization:

1. **Statistical language modelling and information theory** — n-gram/Markov language models, probabilistic foundations, evaluation/perplexity.
2. **Neural language modelling and distributed representations** — neural probabilistic LMs, word embeddings, recurrent networks and LSTM.
3. **Neural sequence transduction and attention** — encoder-decoder, Seq2Seq, attention, subword methods.
4. **Transformer and pretraining families** — Transformer, ELMo, GPT, BERT, T5; distinguish decoder-only, encoder-only and encoder-decoder objectives.
5. **Scaling and post-training** — GPT-2/3, scaling-law studies, compute-optimal training, in-context learning, instruction tuning and preference optimization.
6. **Efficiency and architectural alternatives** — quantization, LoRA/QLoRA, FlashAttention, KV cache/GQA, MoE, state-space and hybrid sequence models.
7. **Multimodal, reasoning and tool-using systems** — multimodal models, retrieval/tool use, test-time compute and agentic workflows.

These are coverage areas to investigate, not a pre-approved event list. Each candidate must pass the source and significance criteria. Include parallel approaches and failed/limited ideas where they explain a genuine research trade-off; do not force every topic into one linear progression.

## 9. Visualisation requirements derived from the model

The same data should support three views:

- **Timeline:** filter by event stream, era and domain; display date semantics and primary-source links.
- **Concept genealogy:** show only evidence-backed typed relations; distinguish influence from precursor, parallel and alternative relations visually and textually.
- **Milestone detail:** explain the contribution, the problem it addressed, what it did not solve, and links to internal lessons and primary sources.

The first release should be static-first and accessible. A semantic HTML chronology is the baseline; a relationship view may use a lightweight SVG or a textual adjacency/list alternative. No essential information may depend on animation, hover, colour, or a JavaScript graph framework. Respect reduced-motion preferences.

## 10. Quality gates before publication

- [ ] Every event has a stable ID, primary type, date precision/type, bilingual title/summary, and at least one relevant source.
- [ ] Research contribution, model release and ecosystem event are not conflated.
- [ ] Every relation has a type, bilingual rationale and supporting sources; unsupported causal edges are rejected.
- [ ] Every internal link resolves to an existing page in the matching language.
- [ ] Missing internal pages fall back to a primary source without implying that a lesson exists.
- [ ] Dates, authorship, model sizes and release claims are checked against primary sources; unknown values remain unknown.
- [ ] Parallel work, attribution uncertainty and material limitations are represented where relevant.
- [ ] EN/FR records share stable IDs and equivalent factual scope.
- [ ] Chronology remains understandable without JavaScript; genealogy has a keyboard-accessible textual equivalent.
- [ ] The resource remains optional and does not add a learning-path milestone.

## 11. Benchmark references

These references informed the product/design requirements; they are not accepted as sources for individual historical claims:

- [Origin of Models](https://originofmodels.com/) — rich idea/model genealogy, typed evolutionary relationships, dead ends and source/uncertainty presentation. Its evolutionary metaphor is useful, but its edges require independent verification before reuse.
- [Language Model Timeline, 2000–2026](https://iwatobipen.github.io/llm_list/) — separate tracks for technical innovations, commercial releases and open-weight releases; useful chronological scan pattern.
- [LLM Timeline](https://llmtimeline.org/about) — model-release catalogue with lab, date, modality and licensing metadata; a release tracker, not a conceptual history.
- [The evolution of language models: From N-Grams to LLMs, and beyond](https://doi.org/10.1016/j.nlp.2025.100168) — secondary review useful for discovering historical coverage and primary references; verify claims in original sources.

## 12. Implementation sequence

1. Review this model against #197 and the existing bilingual page pair.
2. Build a small, verified pilot dataset spanning pre-Transformer foundations, attention, Transformer/pretraining, scaling, post-training and one or two alternative/efficiency lines. Report both the number of visible milestone groupings and underlying event records; the current selection matrix contains 16 core milestone entries and 17 records because GPT-2 research and staged releases are distinct events.
3. Check every source, date, relation and internal destination; record omissions and uncertainty.
4. Render the pilot as a bilingual chronology and assess whether the genealogy adds explanatory value. Do not build a large graph before the records justify it.
5. Only then implement the complete page integration and responsive/accessibility review.


## 13. Canonical pilot rendering

The first public timeline is rendered from `data/history-pilot.yml`; the French and English pages must not maintain separate milestone lists. The build script `scripts/render_history_pilot.py` generates the two Quarto fragments included by the existing page pair.

- Edit event content, dates, sources, caveats and verified internal destinations in the dataset, not in the generated fragments.
- Keep titles, summaries and editorial caveats bilingual under the same stable event ID.
- The generator sorts by the ISO date value, groups adjacent events by editorial era, and renders the event stream, date semantics, source links and available internal concept links.
- The generator escapes text and attributes before emitting HTML. The rendered chronology uses semantic headings, ordered lists, `time` elements and visible text labels; event type is never conveyed by colour alone.
- CI generates the fragments before Quarto rendering. For a local render, run:

```bash
uv run --with-requirements docs/requirements-history-validation.txt python scripts/render_history_pilot.py
quarto render site
```

Generated files are build artifacts and must not be edited manually. The data validator checks their inputs and references; the Quarto workflow checks rendered event count, FR/EN ID parity, date-range visibility, source links, accessible section labels and local rendered links. Neither check substitutes for manual responsive and accessibility review.
