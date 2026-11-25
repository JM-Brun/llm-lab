# Training-example practice: remaining pedagogical gaps

**Date:** 2026-11-25  
**Scope:** FR/EN source-level audit of the existing text-data extended exercises (TR-D–TR-F in the inventory's shorthand), the canonical training-examples lesson and its dedicated Practice companions, plus the reference window-construction implementation and tests.

**Purpose:** continue from the existing exercise inventory without re-authoring validated TR-A–TR-C, repeating the BPE/tokenization science audit, or duplicating the completed causal-mask work. This document records what already exists, what was checked in this pass, and the next bounded work.

## 1. Existing material — do not recreate

The bilingual `site/{en,fr}/exercises-text-data.qmd` collection already contains six progressive exercises, with descriptive stable anchors rather than visible TR-A–TR-F labels:

| Inventory shorthand | Published anchor | Existing coverage |
|---|---|---|
| TR-A | `ex-text-data-representation-pipeline` | Reconstruct text → token strings → IDs → initial embeddings → architecture-dependent position handling → contextualized states. |
| TR-B | `ex-text-data-embedding-lookup` | Embedding lookup and tensor-shape calculation. |
| TR-C | `ex-text-data-representation-context` | Distinguish token identity, position and context. |
| TR-D | `ex-text-data-training-windows` | Build shifted input/target windows, reason about stride and the corpus tail, derive the window-count formula, diagnose a copied-target bug. |
| TR-E | `ex-text-data-bpe-merges` | Count BPE pair occurrences, apply successive merges, encode an unseen word using the learned merge order. |
| TR-F | `ex-text-data-data-leakage` | Diagnose overlap leakage after windowing, near-duplicate documents, temporal continuation protocols, and tokenizer fitting on held-out data. |

The text/data lesson links to its short dedicated companion; that companion links onward to the longer collection. This separation is intentional. The broad collection should remain the owner of the extended tokenization, representation, window, BPE and split-leakage tasks.

**Naming clarification:** TR-A–TR-F are editorial shorthand used by the audit/inventory. The exercise pages use descriptive stable anchors; do not rename anchors or add redundant visible IDs merely to make the shorthand appear in the page.

## 2. Independent checks completed in this pass

### TR-D — shifted windows and stride

For the published stream (s=[11,4,4,9,2,7,5]), context length (L=3), stride (S=2):

[
X=egin{bmatrix}11&4&4\\4&9&2end{bmatrix},qquad
Y=egin{bmatrix}4&4&9\\9&2&7end{bmatrix}.
]

Both arrays have shape ((2,3)). Start (a=4) is invalid because the final input token has no successor. With (N=7,L=3), the documented count (1+\lfloor(N-L-1)/S\rfloor) gives 4 windows for (S=1), 2 for (S=2), and 2 for (S=3). The explanation correctly distinguishes stride (window-start displacement) from the one-token target shift.

The code-backed reference `sliding_input_target_pairs` implements this exact contract: one-dimensional integer stream, positive integer context length/stride, complete shifted targets only, no invented padding or EOS. The unit tests cover the worked example, target alignment, non-copied targets, overlap/no-overlap, the minimum complete stream, the count formula, determinism/non-mutation and invalid inputs. The source and tests do not claim to implement packing, padding, loss masks or corpus loading.

### TR-E — BPE merge trace

Under the explicitly stated word-level teaching convention (characters plus `</w>`), the initial pair counts are correct:

- (o+w): 4 occurrences;
- (l+o): 3;
- (w+</w>): 2;
- the remaining listed pairs: 1 each.

After (o+w\to ow), the pair (l+ow) occurs 3 times and (ow+</w>) twice, so the second merge (l+ow\to low) is correct. Applying those two learned merges to unseen `lowest` gives `low · e · s · t · </w>`. The exercise correctly states that encoding reuses the learned merge order rather than retraining/recounting on the request text. It explicitly disclaims being a production byte-level BPE specification. No correction is justified.

### TR-F — split and tokenizer leakage

The three protocols are correctly distinguished:

- Randomly splitting overlapping windows from one source document can share source tokens across train/validation; split independent source units first, then construct windows within each partition.
- Splitting only by document ID does not prevent near-duplicate content crossing partitions; grouping/deduplication and a documented cross-partition overlap audit are required for the intended independence claim.
- A temporal continuation split can legitimately supply the earlier prefix as validation context if the operational task is continuation of a known stream, while keeping post-cutoff targets out of training. It does not measure generalization to independent documents.

For the conventional held-out protocol, fitting BPE on train + validation is correctly identified as leakage; fit on train, freeze the tokenizer revision, then encode all partitions. The exercise also correctly avoids claiming that every industrial pretraining protocol must use this exact convention.

### FR/EN comparison

The inspected TR-D, TR-E and TR-F prompts, numerical matrices/counts, formulas, solutions, limitations and success criteria match in substance across English and French. The bilingual pages retain the same descriptive anchors. No mathematical or pedagogical correction was justified in this pass.

## 3. Training-examples lesson and Practice companion

The FR/EN `training-examples` lessons already explain:

- one-token input/target shift and teacher forcing as observed-prefix conditioning (not the objective, loss or optimizer);
- stride and overlapping windows, including the corpus-tail requirement;
- document packing, boundary markers and the separate decision whether attention may cross document boundaries;
- padding, attention masks and loss masks as distinct mechanisms;
- dynamic padding and its collator boundary;
- ([B,L]), ([B,L,V]) shapes and alignment through loss reduction;
- limitations: no universal packing, cross-document masking, padding or loss-reduction policy.

The dedicated `site/{en,fr}/exercises/training-examples.qmd` companions currently contain four short checks: shift alignment, teacher forcing/causality, attention-mask versus loss-mask roles, and logits axes. They do not yet ask the learner to solve a complete document-boundary/packing or padded-batch scenario.

The lesson's worked padding example is arithmetically correct: valid-token mean ((0.2+1.1+0.7)/3=2/3\approx0.667); naive mean over all five illustrative positions is (9/5=1.8). The text correctly warns that the denominator convention must be specified and that an attention-mask value alone does not guarantee that a target is excluded from loss.

## 4. Remaining work — bounded and non-duplicative

### P1 — Extend the training-examples Practice companion with transfer tasks

Create a small number of progressive tasks on the existing FR/EN dedicated Practice pages, not a new collection:

1. **Document boundary and packing scenario.** Give two short documents and a packed stream with a boundary/EOS marker. Ask learners to distinguish (a) target shift, (b) whether cross-document attention is allowed, and (c) whether the boundary marker itself enforces that policy. Require the learner to state the intended objective before choosing a mask. Do not present one masking policy as universal.
2. **Padding and loss-reduction scenario.** Start from unequal-length examples in a batch; construct padded inputs/targets, identify valid context positions and valid target positions separately, and calculate a stated valid-token mean. Include a counterexample where the attention mask is correct but PAD labels are still included in the loss.
3. **Transfer/debug prompt (optional if it adds value).** Diagnose a faulty collator that changes target alignment after left/right padding, or an implementation that uses a classification attention mask as if it were a causal-LM loss mask. Keep this as a reasoning task unless a real implementation exists to test.

Use prediction → worked answer → transfer/counterexample, stable descriptive anchors, matching FR/EN reasoning and an explicit success criterion. Reuse the existing lesson examples; do not duplicate TR-D's window-count derivation or TR-F's split-leakage scenarios.

### P2 — Decide whether code should expand

Do not extend `sliding_input_target_pairs` into a general corpus/packing/collation implementation merely to support the exercises. Its documented narrow contract is coherent and its tests match that contract. If the project later adds a concrete packer/collator, define its semantics first (EOS insertion, cross-document visibility, left/right padding, target shifting after padding, loss-mask construction, reduction denominator), then add implementation and tests as a separate bounded change.

### P2 — Rendered validation

After any Practice-page changes, use the existing Quarto and browser-review workflows. Verify both language companions, all answer disclosures, stable links back to the lesson, mobile overflow, math rendering and keyboard operation. Do not create a new workflow for this concept.

### P3 — Learner validation

The source-level audit does not establish comprehension. Include these tasks in the existing learner pilot only after the manual accessibility gate in #483 is closed; record where learners confuse EOS/boundary markers, causal attention masks, padding masks and loss masks. Do not treat correct answer disclosure or green CI as evidence of mastery.

## 5. Explicitly out of scope

- Rewriting TR-A–TR-C or the already validated representation/embedding exercises.
- Repeating the BPE, tokenizer, corpus-splitting or scientific audits.
- Re-deriving the existing TR-D/E/F calculations after this pass.
- Implementing a production tokenizer, corpus loader, packer, collator or training loop.
- Adding another exercise registry, new page-map concepts, or per-concept GitHub Actions.
- Treating the current four-question companion as defective merely because it is short; the gap is specifically the absence of transfer scenarios for packing/boundaries and padding/loss reduction.

## 6. Integration dependency: causal-masking Practice

The separate CA-A ownership migration is still represented by open PRs #1622 (lesson-side Practice entry points) and #1623 (expanded dedicated causal-masking companions). Their Quarto/browser checks have passed, but the Test suite jobs were cancelled by workflow concurrency and have not yet produced a successful final result. Do not treat the CA-A migration as integrated until the final PR heads have a successful CI result and the PRs are merged. This report does not include or duplicate those changes.

## 7. Evidence boundary

This is a source-level audit of the published bilingual exercises, the lesson's worked example, and the reference implementation/tests. It does not certify rendered screenshots, screen-reader behavior, touch usability or learner outcomes. Existing manual accessibility work remains tracked under #483; the learner pilot remains gated under #447.
