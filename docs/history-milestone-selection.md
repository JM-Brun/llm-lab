# LLM history: first-release selection matrix

**Status:** editorial proposal, 2026-10-31  
**Owner:** [issue #197](https://github.com/JM-Brun/llm-lab/issues/197)  
**Parent design:** [history-data-model.md](history-data-model.md)  
**Evidence inventory:** [history-pilot-sources.md](history-pilot-sources.md) · [relation audit](history-relation-audit.md)

This matrix turns the source-discovery shortlist into a proposed first release. It is a decision aid, not a quantitative measurement of historical importance. It deliberately prioritizes the scope of issue #197: attention, Transformers, and selected developments that explain modern LLMs. It does not claim to be an exhaustive history of language modelling or AI.

## 1. Selection method

Rate each candidate on four ordinal dimensions:

| Criterion | 1 | 2 | 3 |
|---|---|---|---|
| **Scope relevance** | Peripheral to attention/Transformers/modern LLMs | Useful context or adjacent development | Directly explains a major step in the issue's scope |
| **Pedagogical value** | Hard to connect to the site's learning objectives | Adds useful context or contrast | Explains a concept, design choice, or misconception central to the site |
| **Evidence readiness** | Source/date/attribution needs substantial additional work | A credible primary source exists, but details need normalization | Primary/authoritative evidence and editorial caveats are already identified |
| **Coverage contribution** | Mostly duplicates a selected event | Adds a distinct dimension | Fills a currently underrepresented technical dimension or research line |

Do **not** sum these scores into a pseudo-objective ranking. Scope relevance and pedagogical value drive the main-timeline decision; evidence readiness is a publication gate; coverage contribution helps avoid selecting a narrow sequence of similar model releases.

Selection labels:

- **Core:** proposed for the first visual chronology.
- **Context:** useful as a short precursor/context marker or a thematic side track, not a main milestone.
- **Supplement:** retain in the research inventory and link from a later expanded view or bibliography; not required for the first release.
- **Defer:** do not publish until the named evidence or coverage gap is resolved.

## 2. Proposed core chronology

The first view contains 16 selected core milestone entries. Because the GPT-2 research announcement/report and staged model releases are distinct events, this selection expands to **17 underlying event records**. Keep both counts explicit in implementation and review; do not merge the GPT-2 records merely to preserve a round milestone count. Same-year events must not be artificially ordered when the available date precision does not justify it. The chronology can use parallel thematic lanes (architecture, training/scaling, systems, ecosystem) rather than a single causal chain.

| Candidate | Relevance | Pedagogy | Evidence | Coverage | Decision | Reason / caveat |
|---|---:|---:|---:|---:|---|---|
| Bahdanau et al. learned attention (2014) | 3 | 3 | 3 | 3 | **Core** | Explains the move beyond a single fixed encoder vector and provides a carefully scoped attention precursor. Do not imply it is identical to Transformer self-attention. |
| Transformer (2017) | 3 | 3 | 3 | 3 | **Core** | Central architectural milestone and anchor for the site's canonical Transformer explanation. It did not invent attention. |
| GPT generative pretraining (2018) | 3 | 3 | 3 | 3 | **Core** | Makes the autoregressive pretrained language-model path explicit. Label the research announcement/report date convention accurately. |
| BERT (2018 arXiv; 2019 conference) | 3 | 3 | 3 | 3 | **Core** | Important contrasting branch: bidirectional encoder pretraining, not a left-to-right text generator. Display submission and conference dates distinctly. |
| GPT-2 research announcement and staged releases (2019; separate event records) | 3 | 3 | 3 | 3 | **Core** | Needed to explain the GPT progression and public discussion of scaling/zero-shot behavior. Keep the 14 February research announcement/report distinct from the staged 124M→1.5B model releases; describe zero-shot results with benchmark-specific limits. |
| T5 (2019) | 2 | 3 | 3 | 2 | **Core** | Demonstrates the encoder–decoder/text-to-text branch; prevents a misleading decoder-only account. |
| Scaling laws (2020) | 3 | 3 | 3 | 3 | **Core** | Introduces an empirical lens on model/data/compute trade-offs. Present as a research finding, not a universal law or a causal explanation of GPT-3. |
| GPT-3 (2020) | 3 | 3 | 3 | 3 | **Core** | Landmark example for few-shot in-context learning. Keep distinct from parameter fine-tuning and from scaling-law claims. |
| Retrieval-Augmented Generation (2020) | 2 | 3 | 3 | 3 | **Core** | Adds a non-parametric retrieval path alongside model parameters. Explain the original paper's formulation; do not imply modern RAG systems are identical or hallucination-free. |
| LoRA (2021) | 2 | 3 | 3 | 3 | **Core** | Important adaptation dimension: efficient parameter updates without changing the base architecture. Do not confuse it with QLoRA. |
| Chinchilla (2022) | 3 | 3 | 3 | 3 | **Core** | Essential counterpoint to simplistic parameter-count scaling: compute allocation depends on both model size and training tokens. Avoid a universal ratio. |
| InstructGPT / RLHF (2022) | 3 | 3 | 3 | 3 | **Core** | Explains a major post-training path from pretrained models to instruction-following behavior. Separate the paper's method from the ChatGPT product launch. |
| FlashAttention (2022) | 3 | 3 | 3 | 3 | **Core** | Connects attention theory to GPU memory hierarchy and implementation efficiency. It is an exact IO-aware algorithm, not a new architecture or an asymptotic removal of quadratic attention computation. |
| ChatGPT public launch (2022-11-30) | 2 | 2 | 3 | 3 | **Core — ecosystem lane** | A major deployment/distribution milestone. Visually distinguish product/ecosystem events from research contributions. |
| DPO (2023) | 2 | 3 | 3 | 2 | **Core** | Shows a different preference-optimization formulation. Do not say it removes preference data or all RLHF-related ideas; no unsupported direct InstructGPT → DPO lineage. |
| Mamba (2023) | 2 | 3 | 3 | 3 | **Core** | Represents a distinct state-space sequence-model research line and a useful contrast with attention-based backbones. Not a universal Transformer replacement. |

**Editorial note:** GPT-2 has separate official research-announcement/report and staged-release records. The source audit now documents two retrospective date conflicts (January/February for the 124M release; April/May for the 355M release) and OpenAI's correction of the original parameter counts. Use 14 February 2019 for the dated research announcement, month-level precision for the early checkpoint releases, 20 August for 774M, and 5 November for 1.5B. Retain separate `research` and `model_release` events; the core label does not permit combining them.



**Date convention:** where the source is an arXiv paper, the research-event date is its first-version submission date unless the event explicitly uses a different convention (for example, GPT's official announcement or GPT-2's dated announcement). The source inventory records exact dates and the distinction between submission, conference publication, announcement and release. The visual matrix intentionally groups many entries by year; do not infer same-year ordering from that display.

## 3. Context and supplementary candidates

| Candidate | Relevance | Pedagogy | Evidence | Coverage | Decision | Why it is not in the core chronology yet |
|---|---:|---:|---:|---:|---|---|
| LSTM (1997) | 2 | 2 | 3 | 2 | **Context** | Useful recurrent-model background, but not specifically an NLP milestone and too early for the focused attention/Transformer story. |
| Class-based n-gram models (1992) | 1 | 2 | 3 | 2 | **Context** | A representative statistical-language-modelling marker, not the origin of n-grams. A fuller Shannon/Markov/smoothing/perplexity account is still missing. |
| Seq2Seq LSTM (2014) | 3 | 3 | 3 | 2 | **Context** | Directly motivates the encoder–decoder bottleneck discussed by Bahdanau et al.; can be shown as a nearby precursor, without asserting an unsupported directed lineage. |
| BPE subword units in NMT (2016) | 2 | 3 | 3 | 3 | **Context** | Important tokenization branch, but the NMT adaptation of BPE is not the invention of BPE. Better shown in a tokenizer lane or companion explainer. |
| Sparse Mixture-of-Experts (2017) | 2 | 2 | 3 | 3 | **Supplement** | Important conditional-computation line, but the cited work is not a Transformer MoE and requires careful comparison with later MoE systems. |
| Flamingo (2022) | 2 | 2 | 3 | 3 | **Supplement** | A useful multimodal milestone, but one model cannot represent the breadth of vision-language, speech, audio and video research. |
| Chain-of-thought prompting (2022) | 2 | 3 | 3 | 2 | **Supplement** | Relevant to prompting and reasoning, but a timeline entry risks implying generated rationales faithfully expose internal reasoning. Needs a broader reasoning/test-time-compute context. |
| Toolformer (2023) | 2 | 3 | 3 | 3 | **Supplement** | Useful tool-use research example; not the origin of tool calling or agent systems. Better placed in a tools/agents side track with other work. |

## 4. Existing internal destinations: verified page inventory

The current branch contains the following bilingual concept pages relevant to the proposed history. These are real paths in the repository at the time of this audit; no destination should be inferred for concepts that do not have a page.

| Historical topic | English page | French page | Link policy |
|---|---|---|---|
| Attention mechanism / Q, K, V | `site/en/queries-keys-values.qmd` | `site/fr/queries-keys-values.qmd` | Link where the milestone explains attention inputs. |
| Scaled dot-product attention | `site/en/scaled-dot-product-attention.qmd` | `site/fr/scaled-dot-product-attention.qmd` | Primary internal destination for attention mechanics. |
| Transformer architecture | `site/en/transformer.qmd` | `site/fr/transformer.qmd` | Canonical architecture destination. |
| Positional encoding | `site/en/positional-encoding.qmd` | `site/fr/positional-encoding.qmd` | Link only when the milestone summary discusses positional information. |
| Causal masking | `site/en/causal-masking.qmd` | `site/fr/causal-masking.qmd` | Link for autoregressive/causal masking, not for BERT. |
| Contextualized representations | `site/en/contextualized-representations.qmd` | `site/fr/contextualized-representations.qmd` | Relevant to ELMo/BERT context, but verify the page's exact scope before linking. |
| Tokenization strategies | `site/en/tokenization-strategies.qmd` | `site/fr/tokenization-strategies.qmd` | Destination for BPE/subword context. |
| Embedding space | `site/en/embedding-space.qmd` | `site/fr/embedding-space.qmd` | Relevant to representation history; not a substitute for a word2vec-specific lesson. |

The branch also contains the existing history pair `site/en/transformer-history.qmd` and `site/fr/transformer-history.qmd`. The current issue requires evolving those pages, not creating a parallel history page.

No current bilingual canonical pages were found in the branch inventory for GPT/GPT-2, BERT, T5, scaling laws, GPT-3, RAG, LoRA, Chinchilla, RLHF, FlashAttention, DPO, Mamba, Flamingo or Toolformer. For these events:
- link to the primary/authoritative external source;
- do not fabricate an internal “Explore the concept” link;
- optionally add a clearly labelled “Concept page not yet available” state only if that is useful to readers;
- do not create new concept lessons under this history issue.

## 5. Coverage gaps that block claims of completeness

The candidate set is now broad enough for a focused first prototype, but not for a balanced general history of modern LLMs. In particular:

1. **Early statistical foundations:** Shannon's information-theoretic treatment, Markov language models, smoothing, perplexity and the transition from count-based to neural models.
2. **GPT lineage:** GPT-2 primary/official record and later release milestones; distinguish paper, announcement, checkpoint and API dates.
3. **Tokenization:** pre-NLP BPE history, WordPiece, SentencePiece and multilingual segmentation trade-offs.
4. **Efficient inference:** multi-query/grouped-query attention, KV cache, speculative decoding, quantization and serving systems.
5. **Multimodality:** speech/audio and video, not just image-text examples.
6. **Reasoning and tool use:** broader tool-augmented models, external memory, planning and test-time compute.
7. **Research diversity:** deliberate coverage of multilingual and non-Western research communities, not token inclusion without historical context.

These are explicit limitations of the first release, not items to squeeze into the core timeline without source work.

## 6. Proposed visual organization

Use one chronological axis with optional thematic lanes, not multiple independent timelines that fragment chronology:

- **Architecture and sequence modelling:** Seq2Seq context → learned attention → Transformer → BERT/T5/GPT branches → Mamba contrast.
- **Pretraining, scaling and adaptation:** GPT, scaling laws, GPT-3, Chinchilla, LoRA.
- **Retrieval and post-training:** RAG, InstructGPT/RLHF, DPO; later extend with tools and reasoning.
- **Systems and deployment:** FlashAttention; ChatGPT launch in a clearly different ecosystem style.

The core timeline should remain readable without opening every lane. A selected milestone can open a compact detail panel with: date kind, one-sentence significance, one caution/limitation, primary source, and (only when verified) the matching EN/FR concept link.

Do not encode the proposed lanes as causal relations. The sparse relation decisions remain those in [history-relation-audit.md](history-relation-audit.md).

## 7. Decision and implementation gates

**Recommended decision:** accept the 16-event core as a working editorial target, subject to final GPT-2 date-semantics review and the broader coverage caveat. Keep context and supplementary candidates available without putting all of them on the first visual axis.

Before implementing the bilingual timeline:

- [ ] Final-check GPT-2 announcement, report and staged-release date semantics against the linked official records.
- [ ] Verify the full text of every core paper used for a substantive historical claim; abstracts alone are not enough for relation claims.
- [ ] Decide whether Seq2Seq and BPE appear as contextual side markers or remain in the expandable detail/reference layer.
- [ ] Draft equivalent EN/FR titles and concise descriptions with stable event IDs.
- [ ] Add only the internal links listed in section 4, and only when the milestone's content warrants them.
- [ ] Keep research, model-release and ecosystem event streams visually distinct.
- [ ] Render the existing FR/EN history pages as a static-first prototype and inspect desktop/mobile, keyboard focus, zoom/reflow and color-independent meaning.
- [ ] Record actual rendered/accessibility checks; a successful Quarto build alone is not visual or accessibility validation.

**Out of scope for this selection document:** creating detailed concept lessons, adding a new JavaScript framework, changing the public navigation, or publishing a supposedly complete history of LLMs.
