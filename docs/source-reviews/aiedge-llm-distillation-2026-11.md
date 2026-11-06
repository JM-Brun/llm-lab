# Source access and preliminary coverage review: AiEdge — LLM distillation

**Source:** [How LLM Distillation Trains Smaller Models](https://newsletter.theaiedge.io/p/how-llm-distillation-trains-smaller-models)  
**Source record:** `aiedge-how-llm-distillation-trains-smaller-models`  
**Review date:** 2026-11-06  
**Status:** access blocked; article-specific extraction not yet possible

## 1. Evidence boundary

The canonical URL was opened directly; retrieval returned a cache miss. Searches for the exact title and slug did not expose the article body, section headings, figures or references. The newsletter homepage identifies The AiEdge Newsletter as a publication by Damien Benveniste, but that does not establish the byline of this specific article; the source record therefore leaves `creators` empty.

This review deliberately does **not** attribute claims from other articles or papers to the AiEdge article. No article-specific extraction file is created until its text can be inspected. The source remains `inaccessible`, not `partially-scanned` or `scanned`.

Unresolved: article text and structure, byline, publication/update date, figures, linked sources, code/data, comments and reuse rights.

## 2. Preliminary LLM Lab coverage check

A targeted inspection of the current canonical concept registry found:

- `teacher-forcing` already exists as a core concept, defined around using observed previous tokens as training context.
- `instruction-tuning` already exists as a supporting concept and is linked to the bilingual LLM-evolution lessons.
- Training examples, observed targets, cross-entropy and training objectives are represented in the existing training concepts and relations.
- No canonical concept explicitly named knowledge distillation, teacher model, student model, response/logit distillation or feature distillation was found in the inspected concept registry.
- The current source registry and bibliography do not yet provide an inspected AiEdge article record.

This is a coverage observation, not a claim about what the inaccessible article teaches. It suggests a potentially useful topic gap, but does not yet justify adding concepts, changing the graph or modifying the learning route.

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

**Current decision: defer article-level integration.**

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
