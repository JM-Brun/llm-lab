# Source-to-knowledge workflow: validation protocol

**Status:** reusable validation protocol · **Version:** 0.1 · **Pilot:** Q/K/V

## 1. Purpose and claim boundary

This protocol validates two coupled products:

1. **The knowledge product:** a coherent, technically defensible learning resource combining the strongest useful contributions of multiple sources.
2. **The production method:** a repeatable process for discovering, inspecting, extracting, comparing, synthesizing, integrating and maintaining that resource as new sources arrive.

The target is a **traceable, purpose-relative synthesis** whose coverage, precision, pedagogical usefulness and limitations are demonstrably stronger than any one inspected source for the declared learner question. This is not a universal ranking of sources.

"More complete" means broader coverage of relevant dimensions within a declared scope while preserving accuracy and navigability. It does not mean longer, exhaustive across all research, or superior for every audience.

This protocol complements:
- [Source catalogue and extraction data contract](../source-catalogue-schema.md);
- [Normative source-to-learning workflow](source-to-learning-system-integration.md);
- [Source synthesis method](../source-synthesis-method.md);
- [Source extraction skill](../../.agents/skills/source-extraction/SKILL.md);
- [Source-to-learning integration skill](../../.agents/skills/source-to-learning-integration/SKILL.md);
- [Knowledge and learning integration skill](../../.agents/skills/knowledge-and-learning-integration/SKILL.md).

It does not define new source registries, concepts, controlled vocabularies or a parallel skill system. Reuse the canonical schemas, taxonomies and artifacts.

## 2. Independent completion states

Never compress these into one "done" flag:

| Object | Question | Evidence required |
|---|---|---|
| Source inspection | What was actually accessed and inspected? | Version, retrieval channel, scope, locators, missing parts, media/comments/rights status |
| Extraction | Were relevant contributions captured faithfully and atomically? | Extraction records, exact locators, evidence types, caveats, source-local teaching model |
| Cross-source synthesis | Were complementary views, convergence and disagreement compared correctly? | Contribution map, comparison dossier, primary-source checks, explicit decisions |
| Project integration | Did selected contributions improve the canonical learning system? | Page/graph/route diff, item dispositions, bilingual parity, preserved content |
| Resource validation | Is the resulting resource correct, usable and maintainable? | Technical review, tests/build, rendered/accessibility review, navigation |
| Learner validation | Can intended learners use and transfer the ideas? | Independent formative observations and task evidence, with limitations |

A source can be partially scanned while some items are extracted and integrated. Complete extraction does not imply complete synthesis. Complete synthesis does not imply a page edit. A passing build does not establish browser accessibility or learner outcomes.

## 3. Units of analysis

Use the smallest unit that can receive an independent decision:

- **Source component:** article section, paper equation, figure, code path, comment, course activity, dataset or linked resource.
- **Extraction item:** one independently assessable claim, definition, mechanism, derivation, assumption, result, limitation, counterexample, analogy, mental model, teaching move, visual or experiment.
- **Pedagogical contribution:** a learner question plus explanatory lens, form/example/sequence and limitations.
- **Synthesis decision:** how one or more items affect a specific canonical page, concept, route, visual, exercise, experiment or reference.
- **Learner task:** a question or action that reveals understanding, misconception or transfer.

Do not treat a whole article as one contribution. Do not create a concept node for every extracted item.

## 4. Validation dimensions

Evaluate dimensions independently. Use existing evidence-confidence and pedagogical-assessment vocabularies; do not invent a composite score or rank sources by one number.

| Dimension | Core question | Minimum evidence |
|---|---|---|
| Identity and provenance | Can another maintainer identify the exact source/version and retrieval path? | Canonical ID/URL, creator, version/date, access route, locator |
| Inspection coverage | Is it clear what was and was not inspected? | Component-level scope, scan history, missingness and access limitations |
| Extraction fidelity | Does each item represent what the source actually says? | Exact locator, paraphrase, voice, evidence kind, caveats |
| Technical validity | Is the claim correct within its stated scope? | Primary/official evidence, equations/API/code/tests, assumptions, counterexamples |
| Evidence independence | Are repeated claims independent corroboration or copied consensus? | Citation lineage, source type, primary-source chain |
| Pedagogical reconstruction | Does the source model/route reflect its instructional design? | Source-local graph, ordered route, declared/inferred outcomes and prerequisites |
| Complementarity | Does a contribution illuminate a distinct learner difficulty or explanatory aspect? | Comparison with exact canonical section and other contributions |
| Synthesis coherence | Does the compiled explanation preserve distinctions without becoming a collage? | Core narrative, optional depth, disagreement/caveat handling, attribution |
| Integration value | Does the change improve learning enough to justify its cost? | Before/after rationale, bounded diff, no-op alternatives tested |
| Resource quality | Is the lesson accurate, teachable, navigable and bilingual? | Content/formal review, EN/FR comparison, exercises, links, page checks |
| Maintainability | Can a new source be added without rewriting or duplicating the system? | Stable IDs, schema validation, incremental diff, bounded dossiers |
| Learner evidence | Do independent learners understand and transfer the intended ideas? | Pilot tasks, observations, scoring rubric, limitations |

### Evidence classes

Keep evidence type and confidence separate:

- **Primary technical evidence:** original paper, formal specification, official API, source code, tests, dataset/protocol.
- **Secondary technical interpretation:** textbook, review, expert tutorial, engineering explanation.
- **Pedagogical evidence:** observed instructional sequence, worked example, visual, exercise, learner study.
- **Project evidence:** canonical page, graph, tests, build output, issue/PR history.
- **Learner evidence:** independent participant task observations and responses.

A tutorial can be a strong pedagogical source and weak evidence for a technical claim. A paper can be strong technical evidence and a poor beginner explanation.

## 5. Gates and failure handling

### Gate A — source is inspectable enough for its intended use

Pass when identity, version/revision where applicable, retrieval route and inspected scope are recorded. Uninspected media, comments, code or appendices remain explicit gaps.

**Fail / partial:** keep the source partial, narrow claims extracted, use a verified mirror/API where appropriate, or defer the affected component. Never infer absent material.

### Gate B — extraction is faithful and reusable

Pass when relevant items are atomic, source-grounded, precisely located, voice-attributed, caveated and assigned an evidence kind/confidence. Instructional sources have a source-local model/route or a justified not-applicable status.

**Fail:** correct/remove unsupported extraction, restore missing provenance, split conflated claims, or retain as an unverified lead.

### Gate C — synthesis is genuinely comparative

Pass when the dossier compares contributions with the existing canonical treatment by learner question, explanatory lens, mental model, example phenomenon, abstraction level, assumptions, teaching move and caveats. It records convergence, complementarity, disagreement and source independence.

**Fail:** do not publish a composite claim. Return to extraction, consult primary evidence, preserve disagreement or defer the unresolved point.

### Gate D — integration is justified

Pass when each accepted contribution has an item-level disposition and destination/rationale. At least one plausible integration candidate must be tested before declaring no learner-facing change for a pedagogical source.

**Fail:** avoid an unnecessary page addition; move useful material to optional depth/reference, or document an explicit no-op. Never integrate for source-count completeness.

### Gate E — resource is validated at the right level

Pass only for checks applicable to the change: schema/graph/tests, Quarto, FR/EN parity, rendered browser review, keyboard/accessibility, link/media/rights checks.

**Fail:** report the precise failed gate. Do not substitute CI success for visual review, source inspection for rights clearance, or content review for learner evaluation.

### Gate F — learning claims are appropriately bounded

Pass when outcomes are reported as content review, automated validation, expert review, formative learner observation or controlled study—whichever actually occurred.

**Fail:** remove claims of measured effectiveness or general superiority unsupported by evidence. One learner pilot is formative, not a general efficacy result.

## 6. The best-of-sources synthesis test

For every candidate contribution, ask:

1. What exact learner question or cognitive obstacle does it address?
2. What does it add: technical fact, distinction, derivation, intuition, example, visual, teaching sequence, practice, empirical result or limitation?
3. Is that contribution already present? Compare its function, not merely its topic or wording.
4. If present, does it improve precision, intuition, transfer, accessibility or optional depth?
5. What is the source's valid scope, and where does its model/analogy fail?
6. Is its technical claim supported independently of the tutorial's own explanation?
7. Can it be integrated without duplicating the core explanation or increasing cognitive load?
8. What is intentionally not integrated, and why?

A strong synthesis normally has one stable core explanation; complementary perspectives only where they resolve different difficulties; formal definitions/equations and dimensions where required; examples selected for distinct purpose; counterexamples, boundary conditions and misconceptions; clearly separated optional depth, variants, implementation and empirical findings; claim-level provenance; explicit unresolved questions and inspection gaps.

### Non-regression rule

Every integration diff identifies the existing knowledge it preserves. A move or deletion requires a destination and rationale. A new source must not erase a prior source's unique useful contribution or silently strengthen a claim by blending it with a weaker source.

## 7. Incremental source-addition protocol

When a new source arrives for an already-covered concept:

1. Resolve identity and deduplicate against canonical URL, DOI, repository/revision and known aliases.
2. Register a new inspection event; never overwrite historical scan evidence.
3. Extract new or materially useful atomic items, while preserving relevant overlap and corrections.
4. Compare items with the existing contribution map and canonical page at exact section level.
5. Update the dossier's contribution map and coverage matrix; do not create a second registry.
6. Re-evaluate only affected claims, examples, route edges and media; avoid full rescans of unrelated sources.
7. Select item dispositions using the canonical taxonomy.
8. Integrate the smallest coherent change or document why no change is justified.
9. Run validators and targeted content/build checks; expand to full checks when shared schemas, registries or templates change.
10. Record before/after coverage, regressions, unresolved gaps and the trigger for future review.

A new source may be reinforcing, complementary, corrective, variant-specific, contradictory, redundant or out of scope. These are descriptive analysis labels, not new controlled dispositions. Record the actual item decision using the canonical taxonomy.

## 8. Q/K/V pilot: baseline coverage matrix

This is a pilot evaluation frame, not a claim that every dimension is closed. Exact page/section mapping and source-item IDs remain in the linked Q/K/V dossiers and extraction records.

| Learning dimension | Expected treatment in a reference Q/K/V resource | Current project evidence | Validation boundary |
|---|---|---|---|
| Role separation | Q selects/asks, K supplies matchable representations, V supplies aggregated content | Bilingual Q/K/V lesson and diagram | Review mathematical wording; avoid anthropomorphic literalism |
| Projection mechanics | Learned, separately parameterized linear projections from input hidden states | Lesson; Vaswani primary source | Clarify joint optimization and dimensions |
| Tensor contracts | Distinguish sequence, feature, head and batch dimensions; allow key/value widths to differ where relevant | Lesson and attention implementation/tests | Do not imply one universal shape convention |
| Scores vs weights vs output | Separate compatibility scores, normalized weights and weighted value aggregation | Q/K/V and scaled-attention lessons | Check formulas, axes and worked values |
| Dot product vs cosine | Explain why standard attention uses scaled dot products, not nearest-neighbour cosine retrieval | Lesson, exercises and #489 fixtures | Include counterexample and state what is held fixed |
| Contextual representations | Inputs are contextual hidden states at the relevant layer, not necessarily raw token embeddings | Q/K/V lesson | Preserve distinction between embedding lookup and later hidden states |
| Self- vs cross-attention | Identify source of Q separately from source of K/V | Lesson and adjacent attention material | Avoid overgeneralizing self-attention |
| Position information | Explain positional information as part of representations/attention design; distinguish RoPE details | Q/K/V lesson and linked positional material | Keep RoPE a bounded extension |
| Multi-head variants | Explain standard heads and distinguish GQA/MQA sharing patterns | Scope note and primary GQA reference | Do not conflate KV-head sharing with parameter tying |
| KV cache | Explain cached keys/values during autoregressive decoding | Official HF documentation linked as extension | Keep inference optimization distinct from core mechanism |
| Interpretability limits | Attention weights are not automatically causal explanations | Lesson caveats | Avoid stronger claims than evidence supports |
| Learner transfer | Predict what changes when W_V changes while Q/K are fixed | Exercise and pilot protocol in #447 | Protocol exists; no independent outcome claimed |
| Media and accessibility | Figures are legible, accessible and rights-cleared or link-only | Project SVGs and #483 | Browser/accessibility and third-party asset evidence remain open |
| Citation/reproducibility | Immutable version, citations, licence/provenance | #488 | Not release-ready until release gates close |

### Q/K/V source roles

| Source family | Primary role in synthesis | Do not use it as |
|---|---|---|
| Nishanthan K (DEV/Medium mirror) | Concise intuition and visual framing candidate | Primary technical authority or two independent sources when mirror duplicates article |
| Neha KK (Medium) | Motivation for three projections; matching/payload distinction; linguistic examples | Evidence that parallelism alone explains architecture design |
| Codefinity | Geometric intuition and distractor-style questions | Fully inspected course assessment; runtime/deeper course material remains unverified |
| Vaswani et al. (2017) | Primary formulation of learned projections and scaled dot-product attention | Complete beginner teaching sequence |
| GQA/MQA paper (Ainslie et al.) | Evidence for grouped/shared KV-head architectural variants | Proof that projection parameter tying is the same design decision |
| Hugging Face KV-cache documentation | Implementation-oriented explanation of cached keys/values in autoregressive generation | General proof of every model's cache layout |

The project synthesis should be stronger than each tutorial for the declared scope by combining precise definitions, equations/dimensions, complementary intuition, distinct examples, counterexamples, caveats, exercises and implementation links. This is a reasoned editorial assessment, not a measured universal ranking.

## 9. Adversarial regression suite

Reuse these checks when a source is added or the synthesis changes.

| ID | Adversarial input | Expected safe behavior | Failure signal |
|---|---|---|---|
| A1 | Analogy implies literal database lookup or hard retrieval | State mapping and failure boundary; retain formal mechanism | Analogy presented as mechanism |
| A2 | Tutorial says Q, K and V "learn independently" | Distinguish separate parameters from joint optimization | Wording implies independent training |
| A3 | Tutorials repeat a claim through one upstream source | Preserve pedagogical utility but count evidence lineage once | Repetition reported as independent corroboration |
| A4 | Media caption exists but original bytes are unavailable | Mark not visually inspected; link-only/defer rights | Visual content inferred from caption |
| A5 | Example mixes coreference and lexical polysemy | Keep phenomena distinct and explain the relation illustrated | Different phenomena collapse into vague "context" |
| A6 | New source has low topical novelty but a distinct explanatory lens | Run complementarity test; integrate only if learner benefit is real | Rejected solely because topic already exists |
| A7 | Source describes GQA/MQA; another discusses projection tying | Distinguish shared KV heads from shared projection parameters | Architecture variants conflated |
| A8 | Source section order suggests a prerequisite | Treat as pedagogical sequence unless dependency is justified | Section order becomes canonical graph edge |
| A9 | Source contradicts a popular secondary explanation | Inspect primary evidence; preserve uncertainty if unresolved | Consensus wording hides disagreement |
| A10 | Partial source yields one valuable item | Integrate item while keeping source scan partial | Item integration upgrades scan completeness |
| A11 | New contribution would add a duplicate paragraph | Prefer link/reference or no-op with rationale | Page length/source count optimized over learning |
| A12 | Page changes in English only | Block publication or record explicit translation follow-up | Bilingual parity assumed from one page's build |

For each check, record pass/fail/not-applicable, evidence pointer and reviewer/date. A checklist pass is not a substitute for technical judgement.

## 10. Compact reusable regression checklist

- [ ] Source identity, revision, retrieval route and inspected scope are reproducible.
- [ ] Text, media, comments, linked resources, code/data and rights have separate inspection states.
- [ ] Extraction items are atomic, located, source-faithful and caveated.
- [ ] Source voice and independent verification are distinct.
- [ ] Source-local graph/route is reconstructed or explicitly partial/not applicable.
- [ ] Primary technical evidence and tutorial-derived pedagogy are distinguished.
- [ ] Source dependence/citation lineage is assessed before claiming convergence.
- [ ] Existing canonical coverage is mapped at section level.
- [ ] Complementarity is assessed independently of novelty.
- [ ] At least one plausible candidate integration is tested before a pedagogical no-op.
- [ ] Disagreements, assumptions, counterexamples and failure boundaries remain visible.
- [ ] Every accepted/deferred/rejected item has a canonical disposition and rationale.
- [ ] Graph, page, route, navigation, asset, experiment and reference decisions are independent.
- [ ] Existing knowledge is preserved or has a traceable destination.
- [ ] EN/FR content and navigation are substantively aligned.
- [ ] Schema/tests/build/render/browser/accessibility checks are reported separately.
- [ ] Learner evidence is reported only if actually collected.
- [ ] Incremental addition creates no duplicate registries, concepts, explanations or workflow vocabularies.

## 11. Validation report format

For each pilot or concept collection, report:

1. **Scope:** learner question, canonical pages, sources and versions.
2. **Coverage:** dimensions covered, partial, missing or intentionally out of scope.
3. **Evidence:** primary/secondary lineage, confidence and unresolved disagreements.
4. **Synthesis:** complementary perspectives retained, rejected, linked or deferred, with item IDs.
5. **Integration:** before/after page, graph, route, asset, experiment and reference changes.
6. **Quality gates:** automated, technical, editorial, bilingual, rendered/accessibility and learner checks—each with status and evidence.
7. **Method defects:** extraction omissions, taxonomy/schema drift, template ambiguity, skill failure or non-scalable manual work.
8. **Next iteration:** actionable gaps with owner/trigger; avoid duplicating existing issues.

## 12. Revision policy

Treat this protocol as versioned project method. Change it only when a pilot reveals a real ambiguity, missed failure mode or excessive cost. For every change:
- cite the observed failure or maintenance problem;
- identify affected skills, templates, schema, validators and existing records;
- add/update a regression fixture;
- avoid new controlled vocabulary when a descriptive label or existing field is sufficient;
- validate the protocol on a second concept collection before claiming general transfer.

Q/K/V is the first calibration case, not proof of scalability. Tokenization/embeddings or another concept collection should be the next transfer test after the Q/K/V benchmark and the existing #475 vocabulary/validator reconciliation are complete.
