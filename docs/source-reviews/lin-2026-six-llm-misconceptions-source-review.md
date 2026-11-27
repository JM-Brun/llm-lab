# Source review — Zhicheng Lin, “Six misconceptions about large language models”

**Source ID:** `lin-2026-six-llm-misconceptions`  
**Author:** Zhicheng Lin  
**Publisher:** PNAS Nexus / Oxford University Press  
**Publication/version:** 8 July 2026; corrected and typeset 17 July 2026  
**Canonical URL:** https://doi.org/10.1093/pnasnexus/pgag236  
**Review date:** 27 November 2026  
**Source type / language / audience:** paper (Perspective) / English / mixed technical and research audience

## 1. Scope, provenance and scan status

The publisher's full-text HTML was directly accessible. The pass inspected the bibliographic metadata, abstract, Table 1, the minimal working model, Misconceptions 1, 2, 4 and 6, the implications for evaluation/deployment and the conclusion. The publisher page explicitly identifies the article as open access under CC BY 4.0.

| Component | Status | Coverage and evidence | Limitations |
|---|---|---|---|
| Author-authored text | partial | Abstract, diagnostic matrix, four relevant misconceptions, implications and conclusion inspected directly on the publisher page | Other sections were not exhaustively audited for the current six-item pilot |
| Figures/media | partial | Figure 1 caption and textual description read | Actual figure bytes and other visual assets not inspected |
| Code/data | not-applicable / not-inspected | Article states that there are no data underlying this work | No code or supplementary dataset inspected |
| Comments/community | not-applicable | Journal Perspective; no discussion thread inspected | None claimed |
| Linked resources | not-inspected | DOI and publisher page verified | Cited primary studies, policies and external systems not independently inspected |
| Metadata/version | complete for this pass | DOI, journal, volume/issue, publication date, corrected/typeset date and licence statement | No separate version archive compared |
| Licence/reuse rights | verified for article | CC BY 4.0 statement on publisher page | No figures are reused; third-party material exceptions were not audited |

**Overall status: partially-scanned.** The text needed for the selected conceptual items was inspected, but figures and cited sources were not independently audited. This is not a full-paper visual or reference audit.

## 2. Atomic contribution inventory

The structured extraction is [`data/extractions/lin-2026-six-llm-misconceptions.yml`](../../data/extractions/lin-2026-six-llm-misconceptions.yml). It records six items:
- the four-distinction minimal working model;
- next-token objective versus deployed-system capability;
- learned distribution versus sampled output;
- parametric, contextual and external memory;
- task competence versus agency/human-like understanding;
- evaluation of the deployed configuration.

The paper's diagnostic matrix is the distinctive teaching contribution: each misconception is linked to a kernel truth, a conflated distinction, a downstream mistake, a diagnostic question and a practical correction.

## 3. Technical assessment

### Correct and useful within the stated scope
- Next-token prediction is a valid description of the base model's pretraining objective, but it does not by itself describe the full behavior of a deployed system.
- A learned conditional distribution and one sampled output are distinct; prompting and decoding policy influence the observed sample.
- During ordinary inference, model weights are fixed. Conversation history in the active context and external product memory are separate information layers.
- Observable task competence should be described with task, metric and protocol; it does not by itself establish human-like experience or agency.
- Evaluation claims should report the deployed configuration, including prompts, decoding, retrieval, tools, memory and workflow.

### Claims requiring qualification
- The four-distinction model and six-item taxonomy are the author's proposed diagnostic framework, not a consensus or exhaustive taxonomy.
- “The model does not learn from a chat during ordinary inference” must not be rewritten as “conversations are never retained or reused”: external logs and product memory may be stored, and some policies may permit later training reuse.
- The paper does not provide a detailed taxonomy of RAG retrieval, transmission or answer-faithfulness failures. Its memory distinctions can inform that discussion, but do not substantiate every RAG failure mode.
- The cited GeneGPT, FreshQA, PaperQA2 and workflow-comparison results were not independently reproduced or checked against primary sources in this pass.
- The article does not settle philosophical or empirical questions about understanding, consciousness or agency.

## 4. Source-local knowledge model

The source-local reconstruction is in the extraction YAML. Its central distinctions are:
1. training objective versus deployed system;
2. learned distribution versus sampled output;
3. parametric versus contextual versus external memory;
4. task competence versus agency/human-like understanding.

This is an editorial reconstruction of the article's framework, not an author-provided formal ontology or computational graph.

## 5. Source teaching route

The paper is not a course. Its inferred explanatory progression is:
1. introduce folk theories and their appeal;
2. propose a minimal working model;
3. lay out the diagnostic matrix;
4. apply it to selected misconceptions;
5. derive implications for evaluation and deployment;
6. apply the matrix to publisher AI policies;
7. synthesize the diagnostic questions.

Learning outcomes and prerequisites are therefore marked inferred in the structured record.

## 6. Differential comparison with LLM Lab

| Learner question | Current canonical treatment | Contribution / boundary |
|---|---|---|
| Does next-token prediction fully describe an assistant? | FR/EN LLM overview: transfer, model/system distinction and system components | Adds the diagnostic matrix; avoid duplicating the overview |
| Does temperature change model knowledge? | FR/EN advanced decoding and temperature exercise | Adds the broader distribution-versus-sample framing; the exact temperature calculation remains owned by the decoding lesson |
| Does a model learn from each conversation? | FR/EN overview, RAG/memory and training-loop pages | Adds a compact three-layer memory diagnosis; preserve the caveat about external retention and later training |
| Does RAG teach documents to the model or guarantee truth? | FR/EN RAG/memory page and dedicated exercises | The paper supports memory-layer distinctions only; the detailed retrieval/transmission failure chain is project-derived and must not be attributed to Lin |
| Does task performance establish human-like understanding? | FR/EN LLM limits page and its benchmark exercise | Adds a paired warning against both anthropomorphic over-attribution and deflationary dismissal |
| What must an evaluation report? | FR/EN experimental-evaluation page and existing protocol material | Adds a concise deployed-configuration checklist; primary empirical examples remain to be checked |

## 7. Integration decision

**Phase A only.** Register and extract the source. No page, concept, relation, computational-graph, route or visual change is made by this review. Phase B must compare each extracted item against the exact current page sections and decide whether the diagnostic matrix adds enough value to justify a bounded insertion or index reference.

## 8. Visual assets and rights

The article's CC BY 4.0 licence statement was verified on the publisher page. Figure 1 was only read through its caption and textual description; the image bytes were not inspected. No figure is copied, adapted or recreated. Any later visual use requires a separate exact-asset and attribution review.

## 9. Validation evidence

The source record and extraction are prepared on a dedicated Phase A branch. Source-catalogue validation, full tests and Quarto checks are pending CI; no validation success is claimed yet. Rendered learner-facing review and learner validation are outside this source-registration change.

## 10. Open questions and next actions

1. Independently inspect the primary references behind empirical examples before using their numerical results in a learner-facing claim.
2. Decide in Phase B whether the four-distinction diagnostic matrix should be linked from the six-item misconception pilot, and whether a compact visual adds value.
3. Keep the RAG failure chain attributed to LLM Lab's own page and exercises unless a separate primary/technical source is extracted.
4. If Figure 1 is ever considered for reuse, inspect the exact asset and any third-party credit lines first.
