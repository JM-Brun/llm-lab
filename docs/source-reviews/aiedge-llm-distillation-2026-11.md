# Source access and preliminary coverage review: AiEdge — LLM distillation

**Source:** [How LLM Distillation Trains Smaller Models](https://newsletter.theaiedge.io/p/how-llm-distillation-trains-smaller-models)  
**Source record:** `aiedge-how-llm-distillation-trains-smaller-models`  
**Review date:** 2026-11-27  
**Status:** article body inaccessible; metadata verified from newsletter listing; article-level integration deferred

## 1. Evidence boundary

The canonical URL was opened directly on 2026-11-06 and again on 2026-11-27; both attempts returned a cache miss. The newsletter homepage listing now exposes this article's title, a 2026-11-06 date, the byline Damien Benveniste and a one-sentence teaser (“From teacher-written answers to probability targets and feedback on the student's own output”). These listing fields support the source-record creator/date update, but the teaser is not the article body and does not establish its section structure, figures, references or detailed claims.

This review deliberately does **not** attribute claims from other articles or papers to the AiEdge article. No article-specific extraction file is created until its text can be inspected. The source remains `inaccessible`, not `partially-scanned` or `scanned`; its integration status is now `deferred` because the audit has made an explicit no-integration decision pending readable source text.

Unresolved: article text and structure, byline, publication/update date, figures, linked sources, code/data, comments and reuse rights.

## 2. Preliminary LLM Lab coverage check

A targeted inspection of the current canonical concept registry found:

- `teacher-forcing` already exists as a core concept, defined around using observed previous tokens as training context.
- `instruction-tuning` already exists as a supporting concept and is linked to the bilingual LLM-evolution lessons.
- Training examples, observed targets, cross-entropy and training objectives are represented in the existing training concepts and relations.
- The canonical concept `knowledge-distillation` already exists in `data/concepts.yml`, with bilingual definitions and links to the LLM-evolution, language-modeling-math and compression-revision lessons. It is also related to `model-compression` in the canonical graph.
- The AiEdge source record already points to the bilingual training-examples and LLM-evolution pages, but its `classification.concept_ids` was empty despite the explicit distillation topic in its title and tags. This is a metadata-link gap, not evidence that the inaccessible article's claims have been reviewed.

This is a coverage observation, not a claim about what the inaccessible article teaches. The source remains inaccessible and no article-specific extraction is justified. The title-level topic relation is now linked to the existing `knowledge-distillation` concept; no new concept, page or learning-route step is proposed.

## 3. Candidate comparison dimensions — pending article access

When the article text becomes available, extract and compare only the dimensions it actually covers:

1. **Teacher–student setup:** teacher and student roles, initialization, architecture constraints and whether the teacher is frozen.
2. **Transferred signal:** generated sequences / hard labels, token-level logits or soft targets, hidden states / intermediate features, attention maps, or rationale traces.
3. **Objective:** cross-entropy, KL divergence, temperature scaling, feature-matching losses, multi-task objectives and any weighting/combination of losses.
4. **Data protocol:** prompts, teacher-generated examples, filtering, teacher-forced versus student-generated trajectories, and on-policy versus off-policy supervision.
5. **Training and deployment:** what is paid during teacher inference/training versus what is saved during student inference; quality, latency, memory and cost trade-offs.
6. **Evaluation:** task quality, teacher–student agreement, calibration/distribution matching, robustness, efficiency and limitations.

These are an inspection checklist, not extracted claims or a proposed exhaustive taxonomy.

## 4. Independent technical anchors (not attributed to AiEdge)

The following primary/official materials can be used to verify concepts once the article is accessible:

- Hsieh et al., [Distilling Step-by-Step](https://arxiv.org/abs/2305.02301), ACL 2023: teacher-generated rationales are used as additional supervision in a multi-task framework. This is a specific rationale-distillation method, not a synonym for all knowledge distillation.
- Google Research, [Distilling Step-by-Step overview](https://research.google/blog/distilling-step-by-step-outperforming-larger-language-models-with-less-training-data-and-smaller-model-sizes/): describes rationale extraction and student training with separate task prefixes.
- Meta, [Llama distillation guide](https://dev.meta.ai/llama/docs/how-to-guides/distillation): describes synthetic response generation and student fine-tuning as a practical workflow.
- Modular, [LLM distillation handbook](https://handbook.modular.com/model-preparation/llm-distillation/): distinguishes response, feature and chain-of-thought distillation and discusses soft targets.

These sources are corroboration and candidate complementary perspectives. They require their own source records and extractions before their content is integrated as project knowledge.

## 5. Preliminary pedagogical hypothesis — not an editorial decision

A useful eventual learning progression may need to distinguish:

- why compress or specialize a model (deployment constraints and task scope);
- what knowledge/behaviour is transferred (outputs, distributions, internal representations, rationales);
- how the student is trained (data generation and loss);
- how teacher and student interact during data collection (offline/on-policy variants);
- how to evaluate both retained task capability and deployment efficiency.

This is only a hypothesis pending comparison with the article and the existing learning route. Do not create a new page or route step on this basis alone.

## 6. Integration decision

**Current decision: defer article-level integration** (source record `integration_status: deferred`, `scan_status: inaccessible`).

- Register the source and preserve its canonical URL and access history.
- Do not create an extraction containing guessed content.
- Do not create canonical concept IDs or graph relations based only on the URL slug or secondary sources.
- Reopen Phase A when the article body is available; then reconstruct its source-local graph and teaching route, extract atomic claims with exact locators, and assess complementarity against the canonical project.
- Only after that Phase A gate, perform Phase B dispositions and consider bilingual page/graph/route changes.

## 7. Next action

Obtain a readable copy of the article (pasted text, exported HTML/PDF, or a working canonical page). Then update this review rather than creating a competing dossier, complete the structured extraction, and validate the source catalogue and extraction against the repository schema.


## 8. Additional independent cross-check discovered during follow-up

A separate AiEdge article, [How To Deploy LLM Applications](https://newsletter.theaiedge.io/p/how-to-deploy-llm-applications) (2024-07-10), contains a short deployment-oriented taxonomy of knowledge distillation:
- response-based: the student learns to produce similar output responses;
- feature-based: the student learns to reproduce intermediate-layer representations;
- relation-based: the student learns to reproduce relationships/interactions between layers.

This is **not** the requested 2026 article and must not be attributed to it. It is a separately published source by the same newsletter author, surfaced during follow-up research. It offers a useful candidate cross-check for the extraction framework, but it is not yet registered or scanned as an independent source. In particular, this short taxonomy should not be treated as exhaustive: it does not by itself cover logit/soft-target objectives, rationale supervision, on-policy variants or detailed training losses.

The target article remains inaccessible and its source status is unchanged. If this 2024 article is later selected for ingestion, register it under its own canonical source ID and perform a separate scan rather than folding its claims into this record.


## 7. Correction — canonical concept already exists (2026-11-18)

A re-check of `data/concepts.yml` on main found that the earlier statement in §2 saying no knowledge-distillation concept existed was stale: `knowledge-distillation` is already a canonical bilingual concept, linked to `fr/en/llm-evolution`, `fr/en/language-modeling-math` and `fr/en/compression-revision`, and related to `model-compression`. The AiEdge source record's empty `classification.concept_ids` was therefore inconsistent with its explicit title/topic tag. The source record now links to `knowledge-distillation` at the topic/metadata level. This does not upgrade its inaccessible scan status, attribute claims to the article, or justify an extraction.


## 9. Revalidation — 2026-11-27

The current newsletter homepage listing resolves two metadata unknowns: the byline is Damien Benveniste and the publication date is 2026-11-06. These are recorded in `data/sources.yml` with a new append-only access-history entry.

The canonical article page still returns a cache miss. The homepage teaser is a discovery aid only; it is not sufficient to extract or attribute claims. The source remains inaccessible and no extraction file is warranted. The explicit no-integration decision is now reflected as `integration_status: deferred`. Reopen the review only when the article body becomes available.
