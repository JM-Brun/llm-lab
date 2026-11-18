# Tokenizer compression and downstream quality — primary-source comparison

**Review date:** 2026-11-18  
**Owning issue:** [#1211](https://github.com/JM-Brun/llm-lab/issues/1211)  
**Canonical destination:** `en/tokenizer-design-evaluation` / `fr/tokenizer-design-evaluation`  
**Audit type:** focused primary-source review of the published ACL Anthology PDFs. No independent reproduction, code execution, checkpoint inspection or data audit is claimed.

## Executive synthesis

The two papers test related but non-identical hypotheses and should not be flattened into a single verdict.

- **Goldman et al. (Findings of ACL 2024)** vary the amount of corpus support used to train BPE tokenizers. In their English experiments, better compression generally tracks better downstream results, particularly for generation tasks and smaller models. The evidence is a correlation under a specific intervention and small set of tokenizer-support conditions.
- **Schmidt et al. (EMNLP 2024)** build PathPiece to obtain minimum-token segmentations for a fixed vocabulary and vary multiple stages of tokenization. Across their English experiments they find no clear general relationship between corpus token count and downstream accuracy. They instead report important effects from pre-tokenization and vocabulary initialization.

**Operational conclusion:** corpus token count / compression is an inexpensive intrinsic descriptor, but not a universal stand-alone quality score. Interpret it beside tokenizer family, pre-tokenization, vocabulary construction, segmentation, language, model size, training budget and downstream task. Neither paper establishes a universal ranking.

## 1. Goldman et al. (2024)

**Source:** Omer Goldman, Avi Caciularu, Matan Eyal, Kris Cao, Idan Szpektor and Reut Tsarfaty, *Unpacking Tokenization: Evaluating Text Compression and its Correlation with Model Performance*, Findings of ACL 2024, pp. 2274–2286. [ACL Anthology](https://aclanthology.org/2024.findings-acl.134/) · [PDF](https://aclanthology.org/2024.findings-acl.134.pdf) · DOI: 10.18653/v1/2024.findings-acl.134.

### Question and method

The paper asks whether an intrinsic compression measure tracks downstream model performance. It varies BPE tokenizer support from one million documents through 1,000, 100, 10 and one document, down to a character-level baseline. For English, decoder-only models have 1B, 128M and 10M parameters; pretraining uses the C4 training split. Four downstream tasks are used: QQP and MultiNLI classification, plus XSum and question generation. Results are averaged over five fine-tunes.

The authors report that the 1-document tokenizer produces 121% more tokens than the 1M-document tokenizer on the aggregated English development sets; the character baseline produces 323% more. Downstream performance generally improves with better-supported tokenizers. The correlation is stronger for generation than classification and more pronounced for smaller models. Spearman correlations are calculated over the six tokenizer-support conditions; for the 1B English model, the classification-task correlations are not statistically significant.

### Language extension

The Turkish experiment uses six tokenizer conditions for intrinsic evaluation, but only three conditions (1M-DOC, 10-DOC and CHAR) for downstream training, because of compute cost. It evaluates XNLI, XL-Sum and Turkish question generation. This is a useful non-English extension, not a full replication of the English experiment.

### Limits and interpretation

- The small number of tokenizer-support conditions constrains the correlation analysis.
- The intervention changes tokenizer-training support; it does not isolate every possible design dimension.
- Turkish receives a reduced downstream treatment; no broad multilingual generalization follows.
- The authors identify the cost of repeating large-model pretraining and the limited non-English experiments as key limitations.

**Safe claim:** in this particular BPE-support intervention, compression correlates with downstream performance, especially for generation and smaller models.  
**Unsafe claim:** minimizing token count is always sufficient to improve a language model.

## 2. Schmidt et al. (2024)

**Source:** Craig W. Schmidt, Varshini Reddy, Haoran Zhang, Alec Alameddine, Omri Uzan, Yuval Pinter and Chris Tanner, *Tokenization Is More Than Compression*, EMNLP 2024, pp. 678–702. [ACL Anthology](https://aclanthology.org/2024.emnlp-main.40/) · [PDF](https://aclanthology.org/2024.emnlp-main.40.pdf) · DOI: 10.18653/v1/2024.emnlp-main.40.

### Analytical decomposition

The authors distinguish three sequential stages:

1. **Pre-tokenization:** initial rules that constrain where tokens may begin/end.
2. **Vocabulary construction:** choosing the token vocabulary from a corpus.
3. **Segmentation:** splitting a document using that vocabulary.

They define corpus token count (CTC) as the sum of the token counts over the documents in a corpus. This decomposition is useful because two systems can have similar CTC while differing in pre-tokenization, vocabulary construction or segmentation.

### PathPiece and experimental design

PathPiece uses shortest-path dynamic programming over byte positions to find a minimum-token segmentation for a fixed vocabulary (with a maximum token width of 16 bytes in the described algorithm). Its top-down vocabulary-construction procedure is heuristic: it starts from a larger vocabulary and removes tokens to reduce corpus token count.

The experiments use English text from The Pile for language-model pretraining and MiniPile for tokenizer-vocabulary construction. The MPT decoder-only architecture is used. The paper reports 64 language models: 54 at 350M parameters, six at 1.3B and four at 2.4B. The 350M comparisons use ten multiple-choice benchmarks with five-shot prompting; larger models are evaluated with a narrower vocabulary-size setup for compute reasons.

### Findings

- Across the reported settings, the authors find no clear relationship between CTC and downstream accuracy; the summarized Pearson correlation between CTC and average accuracy is 0.241.
- No tokenizer algorithm is statistically superior to all the others in the principal 350M comparison; several top systems are statistically indistinguishable.
- Pre-tokenization materially affects results in the PathPiece experiments. The authors caution that this particular finding may be specific to PathPiece.
- BPE-initialized vocabularies perform better than the tested unigram and n-gram initializations for the specified top-down construction comparison.
- Relative tokenizer performance changes with model size; rankings should not be treated as stable across model scales.

### Limits and interpretation

- All experiments use English; the authors explicitly warn against transferring whitespace-pretokenization findings to languages without space-delimited words.
- The findings depend on selected models, vocabulary sizes and a finite set of downstream tasks.
- The authors note possible noise and task-selection sensitivity.
- The study challenges compression as a sufficient explanation; it does not establish that compression has no value.

**Safe claim:** CTC alone did not explain downstream accuracy across this paper's English tokenizer-design experiments; other design choices mattered.  
**Unsafe claim:** compression is irrelevant to all tokenizers, languages or tasks.

## 3. Reconciliation

| Dimension | Goldman et al. | Schmidt et al. | Synthesis |
|---|---|---|---|
| Main intervention | Amount of BPE tokenizer training support | Tokenizer stages and segmentation/vocabulary alternatives | Different causal questions |
| Compression result | Positive correlation in tested conditions | No clear general CTC–accuracy relationship | Context- and intervention-dependent |
| Languages | English + reduced Turkish subset | English only | Neither is a broad multilingual benchmark |
| Model scale | 10M, 128M, 1B | 350M, 1.3B, 2.4B | Model size may alter sensitivity/rankings |
| Key design insight | Support corpus quality affects BPE compression and downstream results | Pre-tokenization and vocabulary construction can matter beyond CTC | Tokenizer quality is multi-dimensional |
| Reproduction status here | Not reproduced | Not reproduced | Source inspection only |

The apparent disagreement is not a direct contradiction: Goldman varies support for BPE while Schmidt varies several tokenizer stages and studies a broader set of tokenizer families/designs. Their findings should be presented as complementary evidence about the limits of a one-number quality metric.

## 4. Integration decision for LLM Lab

- Retain both papers on the existing bilingual advanced tokenizer-evaluation pages.
- Present compression/CTC as a measurable intrinsic property, not as a project KPI or universal proxy for downstream quality.
- Keep pre-tokenization, vocabulary construction and segmentation conceptually distinct.
- Put language, model-size, task and compute scope directly beside every quantitative result.
- Do not create a new concept ID or curriculum step: the existing `token` concept and bilingual tokenizer-design pages are sufficient.
- Do not copy source figures. The extraction files contain paraphrases and locators only.

## 5. Validation and remaining work

- Primary PDF text, publication metadata, key result tables/plots and author-stated limitations were inspected.
- The extraction records are structured documentation, not independent reproduction.
- The linked repositories, model weights, tokenizer artifacts, raw data and training/evaluation code were not audited or executed.
- Next review in the source queue: continue with the next explicitly prioritized paper (Sentence-BERT), while preserving the distinction between sentence-embedding similarity and retrieval/ranking systems.


## Synchronisation de branche — 2026-11-18

La branche de cette revue a été réintégrée à `main` par un commit de fusion à deux parents. Les mises à jour principales de `main` sont conservées, notamment les audits RoPE et les corrections GPT-2/embeddings ; les ajouts de cette revue restent limités aux deux extractions Goldman/Schmidt, à leurs métadonnées dans le catalogue et à ce dossier.

La fusion de `data/sources.yml` a conservé les deux ensembles de modifications : les ajouts Goldman/Schmidt ont été appliqués à leurs entrées respectives sans écraser la mise à jour RoPE de `main`. Cette note décrit la réconciliation du contenu ; elle ne remplace pas la validation CI du nouveau head.


### Synchronisation complémentaire — 2026-11-18

Une seconde synchronisation a intégré le HEAD `cb7e3c859591b954188bb435a7b888ae2949875f` de `main`, qui inclut la documentation ENG-02 fusionnée par la PR #1300. Le diff propre de la PR reste limité aux deux extractions, au catalogue des sources et à ce dossier. Les validations doivent être lues sur le nouveau head de branche.
