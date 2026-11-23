# Practice activity model pilot: Q/K/V and attention

**Status:** bounded pilot based on existing bilingual pages; no activity registry introduced.  
**Date:** 2026-11-23  
**Scope:** test whether LLM Lab can identify, relate and maintain practical activities using page-local anchors and existing page metadata.

## 1. Why Q/K/V is a useful pilot

The Q/K/V topic has three existing layers:

1. The Understand lesson explains the mechanism.
2. A dedicated FR/EN exercise hub in **site/<lang>/exercises/queries-keys-values.qmd** contains a focused self-check and links back to the lesson.
3. The shared Attention collection contains extended calculations, projection exercises, parameter interventions, gradient reasoning and transfer to cross-attention.

This tests both the per-lesson companion rule and the legitimate grouping of multi-lesson exercises in a topic collection.

## 2. Observed activity inventory

The Q/K/V part of the Attention collection contains eight activities. Their explicit heading anchors are identical in French and English.

| Stable page anchor | Activity kind | Observable outcome |
|---|---|---|
| ex-attention-scores-to-output | Calculation | Compute Q/K scores, scaling, softmax weights and the weighted output; interpret the weights correctly |
| ex-attention-manual-aggregation | Calculation | Calculate a weighted sum and predict the effect of swapping values |
| ex-attention-weighted-mixture-vs-selection | Conceptual discrimination | Distinguish a weighted mixture from discrete selection, including the softmax limiting case |
| ex-attention-project-qkv | Shape inference + code | Infer Q/K/V dimensions and verify the projections with NumPy |
| ex-attention-calculate-qkv-isolate-values | Matrix calculation + intervention | Calculate Q/K/V by hand and isolate the consequences of changing only $W_V$ |
| ex-attention-predict-projection-change | Controlled intervention | Predict which tensors, scores, weights and outputs may change when $W_Q$, $W_K$ or $W_V$ changes |
| ex-attention-connect-projections-learning | Gradient derivation | Explain indirect learning through the final loss and derive local projection gradients |
| ex-attention-cross-attention-transfer | Transfer | Transfer Q/K/V reasoning to distinct decoder and encoder streams and distinguish MQA/GQA sharing |

The same collection continues with CA-A for causal masking, AT-A–AT-C for multi-head attention, and AT-D for score variance. These remain separate activities with their own anchors and learning targets.

The per-lesson Q/K/V hub contains one concise self-check. It does not duplicate the extended calculations; it directs the learner to the Attention collection. The main lesson exposes one link to this dedicated hub and no direct links to the shared collection.

## 3. Minimal identity and relationship model

For this pilot, the canonical activity identity is:

**activity_id = page_id + "#" + explicit heading anchor**

Examples:

- fr/exercises-attention#ex-attention-project-qkv
- en/exercises-attention#ex-attention-project-qkv

The anchor is shared across languages; the page ID carries the language-specific identity. Labels such as AT-A are useful learner-facing exercise codes, but are not required as a second global identifier.

| Concern | Pilot representation | Decision |
|---|---|---|
| Page identity | Existing page-map ID | Keep canonical |
| Activity identity | Explicit heading anchor | Reuse; no separate ID registry |
| Language | Page language | Keep at page level |
| Activity kind | Explicit classification in this inventory | Do not yet encode in YAML |
| Observable outcome | Activity prompt and success criterion | Keep beside the activity |
| Lesson association | Page-level related links plus explicit preparation text | Sufficient for this grouped collection |
| Prerequisites | Authored preparation section | Do not infer from heading order |
| Hints and solutions | Collapsed details blocks | Keep in the activity |
| Code evidence | Code block and stated expected output | Execution status must be tracked separately |
| Publication state | Existing page status | No activity-level lifecycle needed for this pilot |

## 4. Metadata and navigation adjustment

The bilingual Attention collection explicitly prepares learners with Q/K/V, scaled dot-product attention, causal masking and score scaling, and includes transfer tasks for cross-attention and multi-head attention. Its page metadata previously listed only attention-score scaling as a related page.

The pilot therefore adds the relevant lesson relationships to the collection's existing related field and adds the collection to the Q/K/V companion hub's related pages. The companion hub now links directly to the Attention collection rather than routing through the general exercise catalogue first.

This is a page-level relation improvement. It does **not** claim that every activity in the collection is individually mapped to every related lesson.

## 5. What the pilot demonstrates

- A dedicated practice companion can remain concise while the larger exercises grow in a separate Practice collection.
- A shared collection is justified when its exercises deliberately integrate adjacent lessons and the relationship is explicit.
- Existing heading anchors already provide stable, bilingual activity identities for this pilot.
- Page-level metadata can express the collection's lesson neighborhood without introducing a new graph.
- The activity itself remains the source of truth for its prompt, hints, solution and success criterion.

## 6. Limits and next decision

This pilot does not yet provide machine-readable activity kinds, per-activity concept mappings, automated grading, learner progress or a cross-page activity query API. Those are not needed to publish and navigate the current exercise set.

A page-local structured activity list should be considered only if a concrete use case requires reliable machine queries such as:

- coverage of each concept by activity type;
- identification of lessons with no calculation, transfer or implementation task;
- extraction of activities for a generated quiz or learning dashboard;
- separate lifecycle or validation status per activity.

If one of these use cases becomes necessary, extend the existing page metadata contract or a page-local manifest and derive indexes from it. Do not create a hand-maintained global activities.yml merely to duplicate headings, links and page content.

Code execution, mathematical review, bilingual rendering and learner testing remain separate evidence states. A published page or a passing metadata validator does not prove that an activity is scientifically correct or pedagogically effective.

## 7. Pilot acceptance criteria

- [x] A dedicated FR/EN Q/K/V practice hub exists.
- [x] The hub links back to its lesson and directly to the shared extended collection.
- [x] The main Q/K/V lesson has one link to its dedicated hub and no direct links to the shared collection.
- [ ] A regression test locks bilingual anchor parity and the lesson → hub → collection navigation boundary.
- [x] The extended Q/K/V activity anchors are identical across languages.
- [x] The collection's page-level lesson relationships reflect its declared scope.
- [x] Questions for recall remain distinct from multi-step practice.
- [x] No new global activity registry or graph is introduced.
- [ ] The updated pages pass the repository metadata checks and bilingual Quarto render.
- [ ] The NumPy example is executed in a controlled environment and its expected output is verified.
- [ ] A learner review checks whether the activity progression makes the intended transfer explicit.
