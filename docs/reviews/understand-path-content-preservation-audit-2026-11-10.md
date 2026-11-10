# Understand path content-preservation audit (PR #932)

**Date:** 2026-11-10  
**Scope:** The four lesson pages changed by PR #932, compared with its base commit `0a22f646d6906a6cdbca43ec8f13e1877b1c5100` and the current `main`. The two generation-process SVGs were checked for consistency with the new running example. This is a semantic and navigation audit, not a line-by-line proof of every sentence or a full rendered-site accessibility review.

## Overall result

**No substantive loss was identified in the central teaching mechanisms or the important generation limitations.** The rewrite changes the running example and teaching order, but the principal ideas remain in the current French and English pages. The main residual regression is navigational: several useful links present in the old overview were removed without equivalent contextual destinations. The linked pages themselves were not deleted.

## Traceability

| Previous material | Decision in the rewrite | Current destination / evidence | Result |
|---|---|---|---|
| Definition of a language model; LLM scale and the absence of a single parameter-count threshold | Rephrased and reordered | Overview: “What the model predicts” / “LLM, Transformer, GPT…”; scaling-law and survey references remain | Preserved |
| Distinction between LLM, GPT and Transformer; encoder-only, encoder-decoder and decoder-only families | Rephrased; comparison retained | Overview architecture section and Transformer architecture comparison link | Preserved |
| Tokenizer, token IDs, context, parameters, conditional next-token prediction | Rephrased around the new running example | Overview: “From text to a distribution”; links to text/data, Transformer and generation | Preserved |
| Logits, softmax, probability distribution; generation, scoring and learning as distinct uses | Reorganized and illustrated | Overview: “One computation, three uses”; figures and links to likelihood, training examples, loss and gradients | Preserved |
| Teacher forcing; evaluation is distinct from scoring; held-out test data | Condensed into the architecture/learning/use explanation | Overview: learning and evaluation paragraphs in both languages | Preserved; the test-data qualification remains in the overview |
| Pretraining, base model, foundation model, fine-tuning/SFT/preference optimization; in-context learning and RAG | Rephrased and grouped | Overview: “Architecture, learning, use” and “Choosing an approach” | Preserved |
| Choosing between a general model, RAG and parameter adaptation; measured quality, errors, robustness, cost, latency, privacy, provenance and maintenance | Rephrased into a clearer three-option comparison | Overview: “Choosing an approach” | Preserved |
| Generation as predict → select → append → repeat; model parameters fixed during inference | Rebuilt as a worked three-turn loop | Generation: “The loop on an example”, in French and English | Preserved; more explicit |
| Forward pass vs decoding rule vs full generation loop | Rephrased and formalized | Generation: “One step, in notation” | Preserved |
| Prefill, incremental decode, KV cache and its role as an optimization rather than a correctness requirement | Reorganized; technical detail retained | Generation: “From the prompt…” and collapsed latency deep dive | Preserved |
| TTFT, ITL, KV-cache memory estimate, compute-/bandwidth-bound tendencies, GQA and speculative decoding | Kept in the optional latency deep dive | Generation: “Why can inference feel slow?” | Preserved |
| Greedy selection, sampling, temperature, top-k/top-p, beam search and contrastive decoding | Reorganized around one shared distribution and temperature table | Generation: “How is the next token chosen?” plus decoding-strategies link | Preserved |
| Reproducibility and seed; local greedy choice can lead to repetitions | Rephrased in the selection explanation | Generation selection section | Preserved |
| Stopping conditions (EOS, maximum length, application rule) | Integrated into the loop explanation and stepper | Generation: “The loop on an example” | Preserved |
| Context-window budget, truncation/history selection, no intrinsic memory between generations | Rephrased as explicit limits | Generation: “What generation does not do” | Preserved |
| Generation does not improve an untrained model; generation is not learning | Rephrased | Generation: “What generation does not do” | Preserved |
| Fluent or executable SQL does not establish business correctness; check schema, definitions, assumptions and results | Rephrased | Generation: “What generation does not do” | Preserved |
| Exercises, answers, and links to practice pages | Reorganized; practice destinations remain | Both overview and generation pages link to their dedicated exercise pages; generation retains the GE-A exercise link | Preserved |
| Original running example (“The report indicates…”) and old probability distribution | Replaced intentionally | New Otis / *Life of Brian* running examples and clearly labelled illustrative probabilities | Intentional pedagogical replacement, not a lost concept |
| Four overview links: GPT configuration walkthrough, mathematical foundations, tokenization strategies, Transformer block walkthrough | Removed from the overview | The destination pages remain in the repository, but equivalent links are not present in the current overview | **Discoverability regression** |
| Overview link to the Build path | Removed from the overview's old link set | The Build path page remains; the current overview still links to the general Build path in at least one locale only if explicitly present—verify bilingual parity before considering restored | **Navigation should be checked** |

## SVG review

Both generation-process illustrations now use the new running example and the same illustrative 60 / 20 / 10 / 10 distribution as the lesson. Their bar widths were subsequently corrected in PR #945 to be proportional to those percentages. This audit does not treat the SVG as an independent source of explanatory detail; the surrounding lesson supplies the explanation.

## Follow-up recommended

Restore the four removed overview destinations as a compact, contextual **“Go further / Pour approfondir”** group in both languages. They are not missing lesson content—the target pages still exist—but removing their entry points makes useful implementation and mathematical material harder to discover. Keep the group short and describe what each destination adds; do not reinstate a long undifferentiated link list.

Before closing the audit, verify the Build-path link and equivalent French/English destinations, then run the page metadata, link, and Quarto checks. The audit rule in `docs/reader-experience-and-editorial-method.md` should be used for subsequent multi-page refactors.

## Limits of this audit

- The comparison is scoped to the four QMD files changed by PR #932; it does not audit every downstream destination page.
- A retained link is not proof that its destination is complete or current.
- The current page content was inspected structurally and semantically; this report does not claim a full visual review of all four rendered pages.
