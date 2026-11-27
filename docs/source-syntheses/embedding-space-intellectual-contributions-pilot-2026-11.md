# Embedding-space lesson — intellectual-contribution pilot (#1739)

**Audit date:** 2026-11-27  
**Unit:** canonical French/English pair (site/fr/embedding-space.qmd and site/en/embedding-space.qmd), its dedicated Practice hubs and review sheets, with adjacent contextualized-representation and cosine-similarity pages.  
**Purpose:** test the contribution-inventory method on a core representation lesson with a mixed corpus of tutorials, API documentation and primary research.

## 1. Page ownership

The core lesson owns the **input embedding lookup**:

- sequence position, token ID, row address and stored vector are distinct objects;
- an ordered ID sequence selects an ordered sequence of matrix rows;
- repeated occurrences of the same ID retrieve the same initial vector for a fixed table;
- the tokenizer defines the vocabulary/ID mapping, while the embedding matrix contains learned model parameters;
- positional processing and contextualization occur after the initial lookup, with architecture-specific mechanisms.

It does not own:
- the mathematical and empirical analysis of contextualization across layers (contextualized-representations);
- sentence/document embedding geometry, anisotropy, cosine similarity, hubness or retrieval metrics (cosine-similarity);
- the implementation-specific API contract of PyTorch Embedding (reference only unless the implementation uses it);
- the full GPT implementation path (Build).

The page's original purpose also explicitly promises that the learner can predict the effect of coordinated ID renumbering. The full invariance was already explained in the preceding text-data lesson, but the embedding-space page did not link directly to it and its dedicated Practice hub had no corresponding exercise. The correct repair is therefore a short bilingual cross-reference (not a duplicated derivation), a matching exercise on the dedicated Practice page, and the corresponding recall explanation.

## 2. Evidence corpus and limits

| Source | Canonical record / extraction or review | Relevance to this page | Inspection boundary |
|---|---|---|---|
| Hesam Sheikh Hessani, *LLM Embeddings Explained: A Visual and Intuitive Guide* (2025) | hesam-sheikh-hessani-llm-embeddings-explained-2025 ([extraction](../../data/extractions/hesam-sheikh-hessani-llm-embeddings-explained-2025.yml); [source review](../source-reviews/hesam-sheikh-hessani-llm-embeddings-explained-2026-11.md)) | Token ID lookup, fixed input-table vectors versus contextual hidden states, Word2Vec/BERT/LLM progression, real-model embedding atlas. | Complete article text inspected; interactive atlas was not manually operated; repository code, model weights, runtime, image bytes and reuse permissions not inspected. Source remains partially scanned. |
| Sebastian Raschka, *Build a Large Language Model (From Scratch)*, Chapter 2 | sebastian-raschka-llms-from-scratch-ch02 ([extraction](../../data/extractions/sebastian-raschka-llms-from-scratch-ch02.yml)) | Vocabulary and integer token IDs as the upstream input contract. | Chapter source and selected companion notebooks/tests inspected; extraction items are about tokenization/vocabulary, not a separate embedding-lookup derivation. Do not attribute the page's full lookup explanation to this source. |
| PyTorch, torch.nn.Embedding documentation | pytorch-embedding-api ([focused source review](../source-reviews/pytorch-embedding-api-2026-11-19.md); intentionally no extraction) | Confirms the API-specific contract: integer indices select rows; input shape gains an embedding-dimension axis. | Stable documentation page, no immutable version pin; focused API semantics only. No code execution. The review explicitly says these options are not used by the project's NumPy GPT path. |
| Kawin Ethayarajh, *How Contextual are Contextualized Word Representations?* (EMNLP 2019) | ethayarajh-contextualized-representations-2019 ([primary-paper extraction](../../data/extractions/ethayarajh-contextualized-representations-2019.yml)) | Measures context dependence and anisotropy of contextualized representations in evaluated ELMo/BERT/GPT-2 settings. | Primary paper definitions and reported results inspected; claims remain scoped to the studied models, layers, datasets and metrics. |
| Li et al., *On the Sentence Embeddings from Pre-trained Language Models* (EMNLP 2020) | li-bert-flow-sentence-embeddings-2020 ([primary-paper extraction](../../data/extractions/li-bert-flow-sentence-embeddings-2020.yml)) | Sentence-level embedding anisotropy and its impact on cosine similarity; boundary between token embeddings and pooled sentence embeddings. | Primary paper methodology and seven STS benchmark results inspected; target-split flow setup is transductive and the paper is not about all token embeddings. |
| Steck, Ekanadham & Kallus, *Is Cosine-Similarity of Embeddings Really About Similarity?* (2024) | steck-cosine-similarity-embeddings-2024 ([primary-paper extraction](../../data/extractions/steck-cosine-similarity-embeddings-2024.yml)) | Shows that cosine geometry can depend on regularization and may be non-unique in specified matrix-factorization families. | Analytic result and simulated-data experiment inspected; not a theorem about all LLM embedding spaces. |

No new external source was needed for this pilot. The selected corpus already covers lookup, contextualization and adjacent geometry. The sources are not interchangeable: Hesam is primarily pedagogical, PyTorch documents one API, and the papers make model-/objective-/task-scoped empirical or mathematical claims.

## 3. Aggregated contribution inventory

The IDs below are stable within this dossier. They are not canonical concepts or a global registry.

| Local ID | Learner question / contribution | Current treatment | Decision |
|---|---|---|---|
| emb-ic-01-id-as-row-address | **What does an ID mean?** It is an integer index/address into a table, not a vector, coordinate or semantic measurement. | Core lesson: “Lookup: select a row, not a coordinate”; object comparison table and figure. | **Keep in the core lesson.** This is the central mental-model correction. |
| emb-ic-02-position-id-vector | **Why distinguish position, ID and vector?** Position identifies an occurrence in the sequence; ID selects a vocabulary row; the vector is the learned content stored there. | Core lesson: ordered toy sequence [17,42,8,17], table of positions/IDs/rows/vectors, and matrix equation. | **Keep in the core lesson.** It prevents confusion between sequence order and vocabulary indexing. |
| emb-ic-03-ordered-lookup | **Does lookup preserve sequence order and repetition?** Yes: it applies the same row lookup independently at every sequence position and returns a T×d matrix in the original order. | Core lesson: sequence lookup equation and worked row table. | **Keep in the core lesson.** The table is more useful than an abstract lookup definition alone. |
| emb-ic-04-fixed-table-repeated-id | **Do repeated IDs retrieve different vectors?** Not at the initial lookup when the table is fixed; the same ID selects the same row. | Core lesson: repeated ID 17 in the worked sequence; revision sheet and exercise. | **Keep in the core lesson.** Contrast explicitly with later contextualized states. |
| emb-ic-05-lookup-does-not-contextualize | **Does lookup read neighbouring tokens or disambiguate meaning?** No. Contextualization occurs in later network computations. | Core lesson: “From the initial vector to a contextualized representation”; contextualized-representations owns the deeper analysis. | **Keep a concise boundary and link.** Do not import layer-wise contextuality metrics here. |
| emb-ic-06-tokenizer-does-not-learn-the-table | **Who supplies the vector values?** The tokenizer fixes token strings/IDs; the embedding table contains learned model parameters adjusted during training. | Core lesson: matrix-parameter paragraph; Build page owns the code and training details. | **Keep in the core lesson.** This distinguishes preprocessing from model parameters. |
| emb-ic-07-coordinated-id-renumbering | **Are numerical ID values intrinsic?** No. If IDs are permuted and the corresponding rows are permuted consistently, lookup vectors remain unchanged. Renumbering without moving rows changes the selected vectors. | New short bilingual cross-reference to the existing text-data explanation, matching Practice exercise and review-sheet explanation. The upstream page owns the full tokenizer/model-contract explanation; this page avoids duplicating it. | **Integrate in the core lesson and Practice.** This directly fulfils the page's stated purpose without turning the page into an implementation tutorial. |
| emb-ic-08-api-contract-not-universal | **Does every embedding implementation behave exactly like PyTorch's module?** The row-lookup contract is common, but padding_idx, max_norm, sparse gradients, freezing and in-place behavior are API-specific options. | Focused PyTorch source review; not needed in the generic core lesson or current NumPy Build path. | **Keep as a technical reference only.** No extraction or API-options callout until the project uses those features. |
| emb-ic-09-static-vs-contextualized | **Are input embeddings and contextualized states the same object?** No; contextualized representations depend on the model layer and accessible context. | Core lesson gives the boundary; contextualized-representations owns definitions, layer-wise analysis and source evidence. | **Integrate by reference.** No duplicate chapter or source-derived metric here. |
| emb-ic-10-sentence-geometry-is-task-dependent | **Does a nearby vector prove semantic equivalence?** No. Similarity depends on model, representation type, normalization, metric and task; anisotropy/hubness can affect neighbourhoods. | Cosine-similarity lesson and Practice hub; the embedding Practice hub includes a bounded atlas exploration. | **Keep outside the core lookup lesson.** Preserve the short warning in Practice, not a long geometry detour in the main page. |
| emb-ic-11-dimensionality-is-not-quality | **Does a larger embedding dimension guarantee a better representation?** No; dimensionality is a capacity/resource choice whose usefulness depends on training and evaluation. | Hesam source review qualifies the tutorial's dimensionality claims; Build/deep-dive treatment is the appropriate owner if a concrete comparison is added. | **Do not add a generic quality claim to the core lesson.** Keep the source correction in the review. |
| emb-ic-12-tfidf-is-a-different-representation | **Is TF-IDF the same kind of object as a learned LLM token embedding?** No; it is a count-based document-term representation with vocabulary-indexed features, not the learned token lookup table used by a Transformer. | Hesam review identifies a dimensionality conflation in the source's TF-IDF example; history/deepen pages own the comparison. | **Keep as optional historical context.** No TF-IDF detour on the lookup lesson. |

## 4. Page-level judgement and actual change

Before the pilot, the core lesson already had at least five distinctive teaching contributions: row-address versus coordinate, position/ID/vector separation, ordered lookup, repeated-ID invariance at fixed table, and the boundary between initial lookup and contextualized states. The source corpus did not justify another generic analogy or a historical survey on this page.

A narrower inconsistency did justify a change: the page-map purpose promised prediction of coordinated renumbering, but the embedding-space page did not point learners to the existing explanation in text-data and the dedicated Practice page did not test it. The revision sheet referred to renumbering as a follow-up without explaining the result.

**Bounded correction made in this pilot:**
- add a short bilingual cross-reference to the existing text-data explanation of consistent ID/row permutation;
- add a dedicated Practice exercise that distinguishes coordinated renumbering from changing IDs without moving rows;
- retain the full-model vocabulary-indexed-parameter caveat at the upstream tokenizer/model-contract level;
- add a worked bilingual exercise and matching recall explanation;
- preserve the existing page route, concept graph, Build ownership and geometry ownership.

No new concept, page-map field, concept edge, route step, global contribution registry or source extraction is required.

## 5. Meta-model fit

The existing model is sufficient:

- source identity, scan status, rights and inspection history remain in data/sources.yml;
- source-specific atomic items and pedagogical profiles remain in data/extractions/;
- source reviews can intentionally remain the representation of record without a new extraction (as with PyTorch API documentation);
- the living tokenization/embeddings source dossier compares the wider heterogeneous source family;
- this page-centred dossier aggregates learner-facing contributions and exact destinations;
- hidden page-map metadata continues to own page scope, purpose and route;
- data/concepts.yml remains the owner of scientific concepts, not explanatory lenses.

The pilot reinforces that not every useful source needs an extraction, not every extracted item needs a page edit, and not every page improvement creates a new concept. Do not add a page-level contributions field or another registry.

## 6. Validation and remaining evidence

- FR/EN page bodies, page-map purpose, review sheets and dedicated Practice pages were inspected.
- Source-specific review/extraction evidence was reused; the inspection limits above remain in force.
- The new renumbering explanation is a direct consequence of the lookup equation, not an empirical claim from an external tutorial.
- The full model permutation caveat is stated explicitly; the pilot does not claim that permuting only the input table preserves a trained model.
- Quarto build, rendered browser inspection, keyboard/accessibility checks and independent learner validation must be reported from their own evidence. They are not inferred from the source review or from the content edit.

**Pilot conclusion:** the core embedding-space lesson has distinctive value already. The useful change was to close a mismatch between its declared learning purpose and its actual explanation/practice, not to add more source material or length for its own sake.


## 7. Current source-to-page destination verification — 2026-11-27

This pass distinguishes source-derived contributions from project-derived mathematical consequences. The coordinated-renumbering result is a project-owned consequence of the lookup equation and tokenizer/model contract; it must not be attributed to a tutorial merely because sources discuss IDs or embeddings.

| Contribution / source item | Learner claim | FR destination | EN destination | Current presence | Source role and decision |
|---|---|---|---|---|---|
| emb-ic-07 — coordinated ID renumbering (project-derived; no external extraction item) | A consistent permutation of vocabulary IDs and embedding rows preserves lookup outputs; renumbering without moving rows changes the selected vectors. Preserving a full model additionally requires consistent permutation of all vocabulary-indexed parameters. | [Embedding lookup and renumbering](../../site/fr/embedding-space.qmd#embedding-matrix-lookup); [tokenizer/model contract](../../site/fr/text-data.qmd#experience-texte-ids); [Practice exercise](../../site/fr/exercises/embedding-space.qmd#inspecter-matrice-embeddings); [recall sheet](../../site/fr/revision-embedding-space.qmd#revision-check) | [Embedding lookup and renumbering](../../site/en/embedding-space.qmd#embedding-matrix-lookup); [tokenizer/model contract](../../site/en/text-data.qmd#text-id-experiment); [Practice exercise](../../site/en/exercises/embedding-space.qmd#inspect-input-embedding-table); [recall sheet](../../site/en/revision-embedding-space.qmd#revision-check) | explicit in all four destinations | Project-derived mathematical invariant; integrated in core, Practice and review. Lookup-level invariance is not by itself invariance of the complete trained model. |
| Hesam Sheikh Hessani — [extraction](../../data/extractions/hesam-sheikh-hessani-llm-embeddings-explained-2025.yml), static-and-contextualized | The same ID retrieves the same initial input row, while later Transformer states can vary with context. | [Initial vector to contextualized representation](../../site/fr/embedding-space.qmd#du-lookup-a-la-representation-contextualisee); [context effects](../../site/fr/contextualized-representations.qmd#effets-position-contexte) | [Initial vector to contextualized representation](../../site/en/embedding-space.qmd#from-lookup-to-contextualized-representation); [context effects](../../site/en/contextualized-representations.qmd#position-and-context-effects) | explicit | Already covered in the project lesson; Hesam is a pedagogical corroborating source, not the technical definition or sole origin of the distinction. |
| Hesam Sheikh Hessani — same extraction, deepseek-token-atlas | A real model's input embedding matrix can be inspected by token ID; cosine neighbours and graph structure depend on checkpoint, normalization and graph-construction choices. | [Embedding families and case-study context](../../site/fr/embeddings-deep-dive.qmd#familles-embeddings); [Embedding Atlas exploration](../../site/fr/embeddings-deep-dive.qmd#explorer-embedding-atlas) | [Embedding families and case-study context](../../site/en/embeddings-deep-dive.qmd#embedding-families); [Embedding Atlas exploration](../../site/en/embeddings-deep-dive.qmd#explore-embedding-atlas) | explicit link by reference | The Deepen dossier links to the original Space and the Embedding Atlas tool. It does not reproduce the source's DeepSeek checkpoint, code, graph or quantitative results. The source item destination is corrected to the Deepen dossier, not the core lookup page. |
| Hesam Sheikh Hessani — same extraction, historical-method-comparison | TF-IDF, Word2Vec, contextualized representations and modern LLM input embeddings are different representation families with different learning targets. | [Embedding families](../../site/fr/embeddings-deep-dive.qmd#familles-embeddings) | [Embedding families](../../site/en/embeddings-deep-dive.qmd#embedding-families) | explicit | Integrated in the autonomous Deepen survey; not a historical detour in the core lookup lesson. |
| Raschka, Chapter 2 — [extraction](../../data/extractions/sebastian-raschka-llms-from-scratch-ch02.yml), vocabulary-and-token-ids | Token strings map to integer IDs local to a tokenizer vocabulary; IDs are indices, not semantic measurements. | [Text to token IDs](../../site/fr/text-data.qmd#le-parcours-du-texte-au-modèle) | [Text to token IDs](../../site/en/text-data.qmd#the-path-from-text-to-model) | explicit | Already covered; use Raschka for tokenization/vocabulary context, not as evidence for the full embedding-lookup derivation. |
| PyTorch — [focused source review](../source-reviews/pytorch-embedding-api-2026-11-19.md), torch.nn.Embedding contract | PyTorch indices select rows and append an embedding-dimension axis; options such as padding_idx/max_norm are API-specific. | — | — | absent by editorial decision | Keep as a technical reference only. The project path audited here uses NumPy; do not import unused PyTorch API options into the generic lesson. |
| Ethayarajh (2019) — [extraction](../../data/extractions/ethayarajh-contextualized-representations-2019.yml), contextuality-measures / layerwise-contextuality / static-explainability-bound | Contextuality can be operationalized with self-similarity, intra-sentence similarity and MEV; the paper reports a below-5% average MEV for the evaluated models/layers after its anisotropy adjustment. | [Contextuality measurement and geometric limits](../../site/fr/contextualized-representations-advanced.qmd#mesure-contextualite-limites-geometriques) | [Measuring contextuality and its geometric limits](../../site/en/contextualized-representations-advanced.qmd#measuring-contextuality-geometric-limits) | explicit | Primary research evidence in the advanced contextualized-representations destination. Scope the result to the paper's evaluated ELMo/BERT/GPT-2 models, layers, data and metric; do not generalize it to all embeddings. |
| Ethayarajh (2019) — same extraction, anisotropy-baselines | Anisotropy can inflate cosine similarity; the paper uses layer- and metric-specific baselines in its contextuality measurements. | [Anisotropy and score concentration](../../site/fr/cosine-similarity.qmd#anisotropie-concentration-scores) | [Anisotropy and score concentration](../../site/en/cosine-similarity.qmd#anisotropy-concentrated-scores) | explicit | Already covered in the advanced cosine-similarity destination; primary evidence remains scoped to the studied models, layers, datasets and metrics. |
| emb-ic-10 — task-dependent sentence geometry; project synthesis | A nearby vector does not prove semantic equivalence or task relevance; metric choice depends on model, representation, normalization and objective. | [Metric and model dependence](../../site/fr/cosine-similarity.qmd#metrique-modele-objectif) | [Metric and model dependence](../../site/en/cosine-similarity.qmd#metric-model-objective) | explicit | Keep the long geometry discussion in Deepen/Practice, not the core lookup lesson. |
| Hesam Sheikh Hessani — same extraction, embedding-quality-and-dimension | Higher dimensionality does not by itself guarantee better semantic structure or prevent overfitting. | — | — | absent by editorial decision | Retain the source-review correction; do not turn the tutorial's dimensionality claim into a generic page rule without a concrete model/task comparison. |

**Other dispositions remain local to the inventory:** the TF-IDF dimensionality correction is deferred as a source-review finding; the TF-IDF versus learned-embedding distinction belongs in the broader Deepen survey, not the core lookup page. The source's historical and visual material does not justify a new core concept or route step.

**Verification boundary:** this is a source-file inspection on 2026-11-27. The exercise hub, review sheet, and bilingual lesson files were checked separately. It does not claim fresh browser rendering, accessibility testing or independent learner validation.
