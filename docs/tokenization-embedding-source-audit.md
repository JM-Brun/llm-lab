# Source-by-source audit: tokenization and embeddings

**Tracking issue:** [#114](https://github.com/JM-Brun/llm-lab/issues/114)  
**Scope inspected:** `site/{fr,en}/text-data.qmd`, `site/{fr,en}/tokenization-strategies.qmd`, `site/{fr,en}/embedding-space.qmd`, and the public references page.  
**Audit type:** source/content and visual-value review. This is not a rendered-browser review; licensing is not assumed from public availability.

## How to read this audit

- **Explained:** the concept is substantively explained on the named page.
- **Partial:** mentioned or explained at an introductory level; source-specific nuance or worked evidence is missing.
- **Elsewhere:** deliberately owned by another concept page.
- **Gap / action:** a bounded correction or follow-up.
- **Visual decision:** whether to integrate a visual, create an original one, link externally, or omit it.

The two language versions should remain structurally and conceptually equivalent. A link to a resource is not itself evidence that its concepts are covered.

## 1. Explanatory, interactive, and course sources

### 1.1 Andrej Karpathy — [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE)

**Concepts in the source**
- Python strings and Unicode code points; UTF-8 bytes and why visible characters do not map one-to-one to bytes.
- Tokenization as a separate stage from the neural network; encode/decode and vocabulary/IDs.
- BPE training: count adjacent pairs, merge a selected pair, repeat; distinction between training and applying learned merges.
- Practical tokenizer inspection; special tokens and implementation details.
- Tokenization-related failure modes, including spelling, numbers, whitespace, code, and multilingual inputs.

**LLM Lab coverage**
- Unicode/UTF-8, IDs, tokenizer/model compatibility, BPE training versus encoding, and a tokenization mini-lab: **explained** in `text-data.qmd`.
- Normalization/pre-tokenization and BPE/WordPiece/unigram differences: **partial**, expanded in `tokenization-strategies.qmd`.
- Concrete failure examples tied to real model outputs: **partial**; the current mini-lab poses tests but does not report measured outputs.

**Gap / action**
- Keep the video as the main long-form walkthrough, not as a substitute for the local concise explanation.
- Consider adding one reproducible byte-level example showing a Unicode character's UTF-8 bytes and resulting tokenizer fragments. Do not claim that every tokenizer exposes byte fragments in the same way.

**Visual decision:** link to the original video. Do not copy frames; no need to reproduce the entire video visually. The local pipeline diagram already provides the system-level map.

### 1.2 Sebastian Raschka — [Build an LLM from Scratch](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch02)

**Concepts in the source**
- Chapter 2's data preparation: raw text, tokenizer interface, encoding to IDs, decoding, and the connection to model input.
- The surrounding implementation path connects token IDs to embeddings and later to input-target sequences.

**LLM Lab coverage**
- Text → tokens → IDs → embedding lookup: **explained** in `text-data.qmd`.
- The later input-target shift, windows and batches are owned by `training-examples.qmd`: **elsewhere by design**.
- Exact chapter-specific implementation choices are not comprehensively compared with LLM Lab: **partial**.

**Gap / action**
- Link to the chapter as a code companion. Add a small explicit cross-reference to the code location only where the corresponding concept is explained locally; do not mirror the book's code or chapter structure.

**Visual decision:** no copied book figures. Use the original local pipeline diagram and the repository's runnable code as the implementation companion.

### 1.3 Sebastian Raschka — [BPE from scratch](https://sebastianraschka.com/blog/2025/bpe-from-scratch.html)

**Concepts in the source**
- A small, inspectable BPE implementation and the sequence of operations needed to learn and apply merges.
- Relationship between merge rules, vocabulary, encoding, and decoding.

**LLM Lab coverage**
- A toy merge trace is **explained** in `text-data.qmd`; the implementation resources are linked.
- Implementation-specific details and reproducible code output are **partial** in the lesson.

**Gap / action**
- Use it as a second implementation perspective, not another conceptual overview. If a code example is added, compare only a small behavior that reveals a convention or implementation choice.

**Visual decision:** link to the article/code. Do not embed a screenshot of code or create another flowchart.

### 1.4 Hugging Face — [LLM Course: tokenizers](https://huggingface.co/learn/llm-course/fr/chapter6/1)

**Concepts in the source**
- Tokenizer components and pipeline: normalization, pre-tokenization, model, post-processing and decoding.
- BPE, WordPiece and Unigram; training a tokenizer and applying a trained tokenizer.
- Special capabilities of fast tokenizers and integration into model pipelines.

**LLM Lab coverage**
- Normalization, pre-tokenization, model family, special tokens and algorithm distinctions: **explained at overview level** in `tokenization-strategies.qmd`.
- Fast-tokenizer offsets/alignment and pipeline component details: **partial / not a core objective** of the current LLM Lab build path.

**Gap / action**
- Make the resource link point to the course overview and to the relevant specific chapters, rather than implying that one page covers all components.
- Add a deep dive on offsets/alignment only if a downstream task (e.g. token classification) enters the project's scope.

**Visual decision:** link externally. The course is long-form and interactive; reproducing its diagrams would add little and reuse rights have not been checked.

### 1.5 Müller & Steinbach — [BPE Explainer](https://philipmueller.dev/bpe-visualization/)

**Concepts in the source**
- Word-level versus character-level/subword trade-offs and vocabulary-size intuition.
- BPE's origin in compression and its adaptation to tokenizer construction.
- Step-by-step pair frequencies, merge selection, vocabulary growth and stopping criteria.
- Contrasts between compression-oriented and byte-level variants, including base units and coverage.
- Encoding with learned merge rules and token IDs.

**LLM Lab coverage**
- Vocabulary/sequence-length trade-offs, simplified BPE merges, and training-versus-encoding: **explained** in `text-data.qmd`.
- Character/byte/subword categories and algorithm comparison: **explained at overview level** in `tokenization-strategies.qmd`.
- More detailed contrasts between historical compression BPE and production tokenizer conventions: **partial**.

**Gap / action**
- Keep this as the primary interactive exploration resource. Add a short local note that the historical compression algorithm and an LLM tokenizer share a core merge intuition but can differ in base units, pre-tokenization, stopping criteria and special-token handling.
- Review strong generalizations on the external page against primary/official sources before adopting them as local claims.

**Visual decision:** **link, do not copy**. The interactive visualization exposes state changes (candidate pair → merge → vocabulary update) better than a static screenshot. The exact reuse terms for its figures were not established in this audit. A local original static figure is only warranted if an offline, self-contained merge trace is needed.

### 1.6 Cornell CS4782 — [Interactive Tokenization Visualizer](https://www.cs.cornell.edu/courses/cs4782/2026sp/demos/bytepair/)

**Concepts in the source**
- Interactive comparison of BPE and WordPiece.
- BPE's frequent-pair merging, token-boundary evolution, and vocabulary.
- Applying the current vocabulary to a new input.

**LLM Lab coverage**
- BPE versus WordPiece is **explained** in `tokenization-strategies.qmd`; the local table states their distinct selection ideas and caveats.
- An interactive side-by-side comparison is **not reproduced locally**.

**Gap / action**
- Recheck the live tool before presenting it as a dependable learning aid: the inspected page exposed a “Frequency: undefined” value in the UI. This may be a demo/data issue rather than a conceptual error, but it degrades trust.
- Keep it as an optional comparison only after confirming the UI behaves correctly.

**Visual decision:** link only, with a caveat until the displayed value is checked. Do not embed screenshots of an unstable state. The BPE Explainer is the stronger first-stop visual resource.

### 1.7 Saurav Prateek — [Visualizing BPE encoding with Hugging Face](https://huggingface.co/blog/SauravP97/bpe-tokenizer-visualize)

**Concepts in the source**
- Visual inspection of the encoding path and token/merge behavior using Hugging Face tooling.
- Implementation-oriented demonstration rather than a general algorithm specification.

**LLM Lab coverage**
- The general encode path and BPE behavior are **explained**; exact library/API behavior is **partial**.

**Gap / action**
- Check the current article code, dependencies and API versions before asking learners to execute it. Label it as a community tutorial rather than authoritative specification.

**Visual decision:** external link only. No copy; no unique concept has yet been identified that requires a local figure.

## 2. Educational implementations and technical references

### 2.1 OpenAI — [tiktoken educational implementation](https://github.com/openai/tiktoken/blob/main/tiktoken/_educational.py)

**Concepts in the source**
- UTF-8 byte units, regex pre-tokenization, merge ranks, iterative BPE encoding, decode/decode-bytes and optional visualization of intermediate merges.
- Difference between an educational implementation and the optimized library path.

**LLM Lab coverage**
- BPE intuition, pre-tokenization and encode/decode: **explained**; implementation details are **partial**.

**Gap / action**
- Cite this as the best small implementation to inspect for byte-level merge mechanics. If adding code, show the merge trace and explicitly distinguish merge rank from token ID where the implementation makes that distinction relevant.

**Visual decision:** link to source code. The code's console colorization is useful for a live walkthrough but is not a reusable static illustration; do not screenshot it.

### 2.2 OpenAI — [tiktoken library](https://github.com/openai/tiktoken)

**Concepts in the source**
- Production-oriented BPE encodings for specific OpenAI models, practical encode/decode APIs, and the fact that tokenizer choice/encoding is model-specific.
- Approximate bytes-per-token intuition and educational submodule.

**LLM Lab coverage**
- Compatibility and token count as representation cost: **explained**.
- Exact encoding names, version pinning and model-specific usage: **partial**, intentionally not a tutorial on the library API.

**Gap / action**
- Add a short reproducibility checklist to the mini-lab: package version, encoding name, input string, token IDs/tokens and decoding round trip.

**Visual decision:** no external image needed; the API output is more useful as a code example than a figure.

### 2.3 Karpathy — [minbpe](https://github.com/karpathy/minbpe)

**Concepts in the source**
- Minimal implementations for training, encoding, decoding and saving/loading tokenizers.
- Basic text BPE versus regex-pre-tokenized byte-level BPE.
- Special-token handling and implementation details required to reproduce a specific GPT tokenizer.

**LLM Lab coverage**
- The difference between training and encoding is **explained**.
- Regex pre-tokenization, byte-level base vocabulary and special-token conventions are **partially explained**; production compatibility is not yet demonstrated by a local test.

**Gap / action**
- Treat `minbpe` as the clearest source for implementation-level inspection. Make no claim that a toy BPE implementation is compatible with GPT-2/GPT-4 unless a tested round-trip/compatibility claim identifies the exact tokenizer.

**Visual decision:** link to code and its toy example. No copied screenshots.

### 2.4 Hugging Face — [Tokenizers](https://github.com/huggingface/tokenizers)

**Concepts in the source**
- Library architecture and components, multiple model algorithms, normalizers, pre-tokenizers, post-processors, decoders and alignment/offset APIs.

**LLM Lab coverage**
- Main pipeline stages are **explained at overview level**.
- Component APIs, offsets and alignment are **partial / out of current core scope**.

**Gap / action**
- Preserve the distinction between a tokenizer *algorithm* and a tokenizer *library/pipeline*. Add API-level material only when it supports a concrete downstream exercise.

**Visual decision:** official documentation/code link; no copied figures needed.

### 2.5 Google — [SentencePiece](https://github.com/google/sentencepiece)

**Concepts in the source**
- Text-first tokenizer training without requiring whitespace-separated words.
- BPE and Unigram models, normalization, special symbols, vocabulary and encoding/decoding conventions.

**LLM Lab coverage**
- SentencePiece as a library supporting BPE and Unigram is **explained**.
- Whitespace marker conventions and exact normalization/configuration behavior are **partial**.

**Gap / action**
- Add one example of a visible whitespace marker (e.g. `▁`) only with a clear note that it is a representation convention, not a literal space in every tokenizer. Avoid implying SentencePiece is itself one algorithm.

**Visual decision:** official docs and repository link. An original short text example is clearer and easier to maintain than a copied diagram.

### 2.6 Gage (1994) — [A New Algorithm for Data Compression](https://dl.acm.org/doi/10.5555/177910.177914)

**Concepts in the source**
- Historical byte-pair compression: identify repeated adjacent byte sequences and replace them using a dictionary/table.
- It is a compression algorithm paper, not a specification for modern GPT tokenizer pipelines.

**LLM Lab coverage**
- Historical origin and the caveat that modern LLM tokenizers add conventions: **mentioned and appropriately caveated** in `text-data.qmd`.

**Gap / action**
- Preserve the historical distinction. Do not attribute byte-level GPT tokenization, regex pre-tokenization or modern special-token behavior to Gage.

**Visual decision:** no need to copy the original paper's figures; a small original merge example suffices.

### 2.7 Raschka — [Chapter 2 repository and notebooks](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch02)

**Concepts in the source**
- Tokenizer interfaces, text-to-ID conversion, data preparation, and the bridge from IDs to embeddings and training samples.

**LLM Lab coverage**
- The high-level bridge is **explained** across `text-data.qmd`, `embedding-space.qmd`, and `training-examples.qmd`.

**Gap / action**
- Keep the chapter as a code companion and ensure links target the relevant directory/notebook, not just the repository root.

**Visual decision:** no external figure integration; the local pipeline plus executable code is sufficient.

## 3. Research on tokenization costs and linguistic variation

For the research papers below, the lesson currently captures the high-level principle that token count is a cost measure, not a sufficient quality metric. That is sound as a synthesis, but it does not replace reading each paper's methods, languages, baselines and uncertainty.

### 3.1 Ahia et al. (2023) — [Do All Languages Cost the Same?](https://aclanthology.org/2023.emnlp-main.614/)

**Concepts in the source:** language-dependent tokenization costs; implications for token-based API billing and resource use; empirical comparison across languages.  
**LLM Lab coverage:** **explained at synthesis level** in the language-equity section.  
**Gap / action:** if adding quantitative claims, record the exact tokenizer, language sample, corpus and metric used by the paper. Do not generalize its measured languages/results to every model or task.  
**Visual decision:** do not copy paper figures without license review. A local original plot is justified only if the source data/method can be faithfully reproduced and the caption states its scope.

### 3.2 Ali et al. (2024) — [Tokenizer Choice for LLM Training: Negligible or Crucial?](https://aclanthology.org/2024.findings-naacl.247/)

**Concepts in the source:** tokenizer selection can influence training cost and downstream performance; intrinsic tokenizer metrics do not necessarily predict downstream results.  
**LLM Lab coverage:** **explained at synthesis level**; the lesson explicitly rejects “fewer tokens = better model.”  
**Gap / action:** do not reduce the paper to a universal claim that tokenizer choice is always decisive. Summarize experimental conditions and distinguish tokenization effects from training-budget/model differences before adding detail.  
**Visual decision:** link to the paper. No figure integration unless a specific experimental comparison is essential to a worked lesson.

### 3.3 Wegmann et al. (2025) — [Tokenization is Sensitive to Language Variation](https://aclanthology.org/2025.findings-acl.572/)

**Concepts in the source:** sensitivity to language variation and the role of tokenizer/pre-tokenizer design.  
**LLM Lab coverage:** **mentioned and summarized**, but the precise dimensions of variation and the paper's operational definitions are not fully taught.  
**Gap / action:** inspect the full paper before expanding the claim; distinguish language, dialect/register, orthographic variation and tokenizer-specific preprocessing rather than collapsing them into “multilingual fairness.”  
**Visual decision:** link to original paper. Consider an original schematic only if it clarifies the dimensions of variation without implying results not reported by the authors.

### 3.4 Arnett et al. (2025) — [Explaining and Mitigating Crosslingual Tokenizer Inequities](https://proceedings.neurips.cc/paper_files/paper/2025/hash/5b91cefbfa52340af2f16f249572dc76-Abstract-Conference.html)

**Concepts in the source:** unequal tokenization costs across languages and design factors such as vocabulary size and pre-tokenization; analysis/mitigation of crosslingual inequity.  
**LLM Lab coverage:** **summarized at high level**.  
**Gap / action:** verify paper-specific claims and distinguish observed cost differences from demonstrated downstream capability gaps. Keep token count, compute budget, and task performance as separate quantities.  
**Visual decision:** link to the paper. A reproduction of a paper plot would require a faithful method/data trail and rights review.

### 3.5 TokLens — [ACL 2026 SRW](https://aclanthology.org/2026.acl-srw.18/)

**Concepts in the source:** a toolkit for comparative multilingual tokenizer measurement.  
**LLM Lab coverage:** **mentioned as a tool**, with an appropriate warning that one intrinsic metric is not enough.  
**Gap / action:** verify the current toolkit's supported metrics, language coverage, dependencies and maintenance before recommending it as an executable lab. Do not present the existence of a toolkit as validation of its metrics.  
**Visual decision:** link to the paper/tool. No copied figures required.

## 4. Embeddings: conceptual and research sources

### 4.1 Mikolov et al. (2013) — [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781)

**Concepts in the source**
- Learning vector representations of words from context/co-occurrence objectives.
- Geometric relations between learned word vectors and the limits of treating a vector as a literal definition.

**LLM Lab coverage**
- The embedding page explains learned vectors and similarity measures: **explained at introductory level**.
- Historical Word2Vec objectives and the distinction between static word embeddings and modern token embeddings: **partial**.

**Gap / action**
- Add a short contrast: Word2Vec-style static word vectors are not the same object as a Transformer token embedding table or a contextualized hidden state.

**Visual decision:** the local original 2D embedding sketch is appropriate for intuition, provided it continues to label itself as schematic and warns that projection can distort distances. Do not copy paper figures.

### 4.2 Ethayarajh (2019) — [How Contextual are Contextualized Word Representations?](https://arxiv.org/abs/1909.00512)

**Concepts in the source**
- Contextualized representations vary with context; the degree of contextualization differs by model/layer and is measurable.
- Hidden representations should not be treated as static word types.

**LLM Lab coverage**
- Token embeddings versus contextualized representations are **explicitly distinguished** in `embedding-space.qmd`.
- The paper's quantitative analysis and model/layer-specific findings are **not deeply covered**.

**Gap / action**
- Cite it as evidence that contextual representations vary with context, not as proof that all models/layers contextualize equally.

**Visual decision:** no copied paper chart. An original same-token/different-context diagram could be useful if the current embedding page does not already make this distinction visually.

### 4.3 Li et al. (2020) — [On the Sentence Embeddings from Pre-trained Language Models](https://aclanthology.org/2020.emnlp-main.733/)

**Concepts in the source**
- Sentence embeddings derived from pretrained language models; properties and limitations of pooling/representing whole sentences.
- Sentence-level vectors are a different target from token-level contextual states.

**LLM Lab coverage**
- Token, contextualized, and sentence/document embeddings are **explicitly distinguished**.
- Pooling choices and empirical comparisons are **partial**.

**Gap / action**
- Keep sentence embeddings out of the main token-embedding lookup diagram. Add a link to a dedicated sentence-embedding resource only where semantic search/retrieval is taught.

**Visual decision:** no figure integration needed for the current tokenization scope. A pooling diagram belongs in a future sentence-embedding deep dive.

### 4.4 Steck, Ekanadham & Kallus (2024) — [Is Cosine-Similarity of Embeddings Really About Similarity?](https://arxiv.org/abs/2403.05440)

**Concepts in the source**
- A critical analysis of interpreting cosine similarity as semantic similarity; the score's meaning depends on representation geometry and task context.

**LLM Lab coverage**
- The embedding page states that a high cosine score does not prove textual equivalence or answer correctness: **explained at high level**.
- The paper's formal argument and conditions are **partial**, owned by the related cosine-similarity deep dive.

**Gap / action**
- Keep the overview cautious and link to the dedicated cosine-similarity page. Do not summarize the paper as “cosine is useless”; its result is a warning against unqualified interpretation.

**Visual decision:** use the existing original conceptual embedding-space illustration only as orientation. Do not use a 2D scatterplot to claim that cosine scores correspond to human semantic judgments.

### 4.5 Sentence Transformers — [Semantic Textual Similarity](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html)

**Concepts in the source**
- Practical computation of sentence embeddings and similarity scores using a purpose-built library/model.
- API usage and task-level interpretation of similarity.

**LLM Lab coverage**
- Sentence/document embeddings and the limits of cosine similarity are **explained conceptually**.
- Concrete Sentence Transformers API usage is **not a core part of the tokenization lesson**.

**Gap / action**
- Keep it as a practical reference for sentence-level embeddings, not evidence that raw token embeddings are directly suitable for semantic search.

**Visual decision:** documentation link/code example, not an imported figure.

## 5. Current coverage map

| Concept | Current owner | Assessment | Follow-up |
|---|---|---|---|
| Unicode code points vs UTF-8 bytes | `text-data.qmd` | Explained, but no byte-level worked trace | Add one small verified example if it adds value |
| Tokens vs token IDs vs embeddings | `text-data.qmd`, `embedding-space.qmd` | Explained | Preserve distinction and cross-links |
| Embedding lookup matrix (E\in\mathbb{R}^{V\times d}) | `text-data.qmd` | Explained | Keep shape and ID semantics explicit |
| Token embedding vs contextualized state vs sentence embedding | `embedding-space.qmd` | Explained | Avoid conflating their evaluation methods |
| Word/character/byte/subword trade-offs | `tokenization-strategies.qmd` | Explained at overview level | Do not add more diagrams unless needed |
| BPE merge procedure | `text-data.qmd` | Explained with text table | Keep FR/EN examples aligned and validate rendering |
| BPE vs WordPiece vs Unigram | `tokenization-strategies.qmd` | Explained at overview level | Keep algorithm/library distinctions |
| Normalization and pre-tokenization | `tokenization-strategies.qmd` | Mentioned/explained briefly | Expand only with an example that changes output |
| Special tokens and compatibility | `text-data.qmd` | Partial | Clarify special-token handling is implementation/API-specific |
| Multilingual tokenization cost | `text-data.qmd` | Synthesized, paper details not reproduced | Retain metric/task caveat; avoid unsupported quantitative claims |
| Cosine similarity limits | `embedding-space.qmd` and dedicated page | Overview + deep dive | Cross-link, do not duplicate derivation |
| Tokenizer code-level behavior | External code resources | Linked, not validated locally | Pin version and run a reproducible mini-lab before asserting outputs |

## 6. Visual asset inventory and decisions

| Visual / interaction | Learning value | Decision | Rights / quality status |
|---|---|---|---|
| Original text → normalization/pre-tokenization → tokens → IDs → embedding lookup → contextualized states diagram | Establishes system-level pipeline and boundaries between stages | **Keep as canonical local figure** | Original Mermaid diagram; ensure both languages remain equivalent |
| Müller & Steinbach BPE interactive | Shows merge frequency, state changes and vocabulary growth | **Link as primary interactive visual** | No local copy; exact figure reuse terms not verified |
| Cornell BPE/WordPiece interactive | Useful side-by-side algorithm comparison | **Optional link only after recheck** | UI surfaced “Frequency: undefined” during inspection |
| Karpathy tokenizer video | Combines code, visual token inspection and edge cases | **Link** | No frames copied |
| Hugging Face course | Structured sequence of explanations and components | **Link to relevant chapter(s)** | No copied figures |
| tiktoken/minbpe code visualization | Exposes actual implementation steps | **Use code/output in a reproducible lab, not screenshots** | External code evolves; pin versions for any exact claim |
| Original embedding-space SVG | Shows abstract geometry and introduces projection caveat | **Keep as a conceptual figure** | Local asset; maintain clear alt text and projection caveat |
| External paper plots | Evidence for study-specific empirical results | **Do not copy by default** | Rights and reproducibility need individual verification |
| More Mermaid diagrams for each algorithm | Likely repetitive; low incremental value relative to tables and external interactions | **Do not add by default** | Add only for a distinct learning objective |

## 7. Concrete corrections and next steps

1. **Completed in PR #115:** removed the repeated sentence in the English BPE introduction.
2. Verify FR/EN parity after edits; the pages should share concepts and caveats, not necessarily word-for-word translation.
3. Recheck Cornell's live demo before recommending it as a dependable comparison tool.
4. Clarify the distinction between historical compression BPE, byte-level BPE, and a complete production tokenizer pipeline (normalization, pre-tokenization, learned ranks/merges, special tokens and decoding).
5. Consider a tiny reproducible Unicode/UTF-8 byte example only if it adds a concept not already communicated by the existing text and video.
6. Do not integrate external figures until the reuse terms for the exact asset are verified. Link to the original interactive resources in the meantime.
7. Validate the Quarto render and local links after changes. A successful render does not replace a rendered-browser visual review.

## Scope and limits

This is a first source-by-source content map based on the cited source pages and the current repository files. It does not claim that every research paper has undergone a full methods/statistics replication, that every external link has been exhaustively tested, or that browser-level visual inspection has occurred. Before adding detailed quantitative claims from research papers, verify the paper's methods, datasets, baselines, metrics and stated limitations directly.


## 8. Follow-up implemented in PR #117

The first audit's actionable gaps have been addressed in the bilingual lessons:

- **Unicode / UTF-8 worked example:** added an original FR/EN SVG comparing precomposed `é` (U+00E9, UTF-8 `C3 A9`) with decomposed `e` + combining acute (U+0065 U+0301, UTF-8 `65 CC 81`). The accompanying Python example verifies code points, byte sequences and NFC normalization. Sources: [RFC 3629](https://www.rfc-editor.org/rfc/rfc3629) and [Unicode UAX #15](https://www.unicode.org/reports/tr15/). The lesson explicitly states that the figure does not predict tokenizer output.
- **Tokenizer components:** added a bilingual table separating normalization, pre-tokenization, tokenization model, post-processing and decoding. Added a caution on SentencePiece's visible whitespace marker `▁`, with links to the [Hugging Face Tokenizers component documentation](https://huggingface.co/docs/tokenizers/python/latest/components.html) and [SentencePiece](https://github.com/google/sentencepiece).
- **Embedding vs contextualization:** added an original FR/EN SVG showing the same assumed token ID in two contexts and the possible difference between the initial embedding and contextualized states. The caption links to [Ethayarajh (2019)](https://arxiv.org/abs/1909.00512), and explicitly says the vectors are illustrative rather than measured.
- **Tokenizer evaluation metrics:** defined token count, fertility, characters/bytes per token, vocabulary coverage and downstream quality, with caveats about denominators and comparability. Linked to [Ahia et al. (2023)](https://aclanthology.org/2023.emnlp-main.614/) and [TokLens (ACL 2026 SRW)](https://aclanthology.org/2026.acl-srw.18/).

### Visual decisions after implementation

| Asset | Status | Reason |
|---|---|---|
| Unicode/UTF-8 SVG | Added locally in FR/EN | Explains a hidden encoding difference that is difficult to infer from prose alone; cites normative technical references |
| Contextualized-embedding SVG | Added locally in FR/EN | Clarifies the difference between lookup and context-dependent states; cites the research motivating the concept |
| BPE merge visualization | Remains an external link | Interactive state changes are more informative than a copied static image; reuse rights are not verified |
| Existing 2D embedding-space SVG | Retained | Useful conceptual overview with explicit warning about projection distortion |

**Validation still required:** render the bilingual Quarto site, run the repository's link checks and inspect the rendered pages in a browser. CI has not yet returned a run/status for the current PR head; this is not evidence of a successful render.


## Follow-up: complementary tokenizer-evaluation perspectives (2026-10-29)

**Learner problem:** the existing overview correctly warns that fewer tokens do not automatically mean a better tokenizer, but offers little structured framework for interpreting competing claims and newer multilingual evaluation work.

**New sources checked against repository search:**
- Goldman et al. (2024), [Unpacking Tokenization](https://aclanthology.org/2024.findings-acl.134/): compression and downstream-task association in the paper's experiments.
- Schmidt et al. (2024), [Tokenization Is More Than Compression](https://aclanthology.org/2024.emnlp-main.40/): evidence against treating minimum token count as a sufficient objective.
- Arnett et al. (NeurIPS 2025), [Explaining and Mitigating Crosslingual Tokenizer Inequities](https://proceedings.neurips.cc/paper_files/paper/2025/hash/5b91cefbfa52340af2f16f249572dc76-Abstract-Conference.html): design factors associated with cross-lingual token premiums.
- Chiu (ACL 2026), [TokLens](https://aclanthology.org/2026.acl-srw.18/): multi-metric tokenizer evaluation across languages. Treat reported relationships with downstream performance as empirical associations, not universal causal guarantees.

**Design decision:** add a short bilingual section distinguishing representation efficiency, downstream task performance, multilingual variation, and reproducibility. Add original bilingual SVGs as conceptual frameworks, not as data figures. Keep the existing pipeline and segmentation illustration; avoid copying figures from papers or interactive sites.

**Validation status:** source files were inspected and the source list was checked for existing matches in repository search; new figure source is authored locally. Quarto rendering, HTML/image rendering, link checking, mobile layout, and bilingual rendered-page comparison still need to be run on the PR head. No validation is claimed as passed here.


## Editorial integration decision: tokenizer evaluation literature (2026-10-29)

**Decision:** do not create a standalone page at this stage. The learner question—how to evaluate tokenizers beyond token count—belongs in the existing tokenization-strategies page, which already owns representation trade-offs, metrics, and reproducible comparisons. A separate page would fragment a coherent concept and duplicate the current measurement/protocol sections.

**Page responsibilities:**
- `text-data`: retain the introductory pipeline and a short signpost to the evaluation deep dive; do not carry the paper-by-paper discussion.
- `tokenization-strategies`: own the substantive evaluation framework, study comparison, limitations, and protocol.
- `references.qmd`: provide a concise bibliography/provenance index, not repeat the analysis.

**Integration:** Goldman et al. (2024) and Schmidt et al. (2024) are contextualized with distinct roles (empirical compression/performance association versus limits of compression-only objectives); Arnett et al. (2025) and Chiu (ACL 2026) are contextualized for cross-lingual disparities and multi-metric evaluation. Ahia et al. (2023) and Wegmann et al. (2025), already linked in the strategy page, are retained as related work rather than presented as new discoveries.

**Visual placement:** relocate the use of the original four-dimension conceptual SVG from the introductory overview to the evaluation section of the strategy page. It is a framework, not empirical data. Keep the overview pipeline diagram and token-segmentation illustration focused on their own learning questions.

**Validation still required:** Quarto render; verify generated anchor IDs and local links; check both SVGs and image paths; compare FR/EN scope and tables; run link checker; inspect responsive layout. No render/browser/CI pass is claimed by this source edit.


## 3. Candidate-source review: tokenization and embedding visuals (2026-10-29)

### 3.1 Chitransha Agarwal — [Tokenization in Large Language Models (LLMs): A Complete Guide from Beginner to Advanced](https://medium.com/@chitranshaagarwal/tokenization-in-large-language-models-llms-a-complete-guide-from-beginner-to-advanced-47d0c013c2f4)

**Decision: do not use as a technical authority or copy its figures.**

The article is a secondary overview and can be useful for discovering beginner questions, but several formulations are too broad to reuse as written:

- The claim that tokenizers always select the longest possible vocabulary token is not a general description of tokenization. Actual behavior depends on the tokenizer family, pre-tokenization, normalization, merge ranks or learned segmentation procedure, and configuration.
- A larger vocabulary can reduce token count in some settings, but does not guarantee universally shorter encodings, lower end-to-end cost, or better model quality.
- Saying that an LLM reasons purely on token IDs skips the learned embedding lookup and subsequent contextual transformations. IDs are discrete indices, not semantic coordinates.

The article's figures have no reuse license established by this review. Link only if a future learner-facing resource list has a clear reason to include it; otherwise omit it to avoid elevating a weak secondary source.

### 3.2 Search candidates for the text → token → ID → embedding pipeline

The image search surfaced the following candidates. None is currently approved for direct incorporation:

| Candidate | Potential instructional value | Decision / unresolved issue |
|---|---|---|
| [Raschka / Manning — tokenization and vocabulary figure](https://drek4537l1klr.cloudfront.net/raschka/v-8/Figures/ch02__image013.png) | A compact view of text fragments and vocabulary IDs; closely aligned with the book used as a project reference | Do not copy without explicit reuse permission. Prefer linking to the book/chapter and retain the repository's own explanation. |
| [Stanford / Jurafsky — Speech and Language Processing, Chapter 10](https://web.stanford.edu/~jurafsky/slp3/ed3bookfeb3_2024.pdf) | Figure 10.10 illustrates a one-hot vector selecting a row from an embedding matrix; Figure 10.11 extends the idea to sequences | Strong technical teaching source. Check the book's current license and figure-specific terms before reproducing. The existing embedding-space page already provides a worked lookup, so a second static figure may be redundant. |
| [Novamai — Embeddings summary](https://novamai.com/1Concepts/Embeddings/Embeddings_summary.png) | A compact text-to-embedding overview | Provenance, technical precision, and reuse terms have not been established. Do not embed pending review. |
| [DigitalOcean — tokenizer overview figure](https://doimages.nyc3.cdn.digitaloceanspaces.com/010AI-ML/2026/Shaoni/Adrien/31-mar/Image_1.png) | May help introduce the tokenizer pipeline | Verify the source article, accuracy, and image reuse terms before considering it. |
| Medium-hosted diagrams returned by image search | Potentially accessible summaries of embedding lookup and tokenization | Author ownership and reuse terms are unclear; no demonstrated advantage over the original diagrams in this repository. |

### 3.3 Placement decision

The existing pages already provide distinct visual explanations:

- `text-data.qmd`: a pipeline diagram and an original segmentation illustration. Keep this page focused on the conceptual sequence and avoid adding another generic end-to-end infographic.
- `embedding-space.qmd`: a hand-checkable matrix lookup, a reproducible tokenizer-to-ID trace, and original illustrations of contextualization and embedding geometry. These explain the ID-to-vector operation more precisely than a generic external infographic.
- `tokenization-strategies.qmd`: reserve external empirical figures for evaluation questions such as multilingual tokenization costs, tokenizer fertility, and downstream performance. These are the visuals with the greatest potential to add evidence rather than repeat the pipeline.

**Conclusion:** no new third-party image is integrated from this search. This is an intentional editorial decision, not an unfinished image insertion. The candidate figures either have unresolved reuse terms or duplicate explanations already supplied by original, version-controlled diagrams and worked examples. If a future page needs a visual for embedding lookup, create a small original diagram from the repository's own mathematical example, or obtain explicit permission for a source figure.

### 3.4 Image-integration acceptance checklist

Before adding an external figure, record:

1. The exact concept it teaches and the gap in the current page it fills.
2. The original source page and direct image URL, with author/rights holder.
3. An explicit reuse license or written permission covering the intended use; public accessibility alone is insufficient.
4. Whether modification, local hosting, and bilingual captions are allowed.
5. A technically accurate alt text and a caption that distinguishes illustration from measured result.
6. Successful loading in the built site, including narrow-screen layout and both language versions.
7. A fallback or local copy strategy if the remote host is unstable, but only where the license permits copying.

