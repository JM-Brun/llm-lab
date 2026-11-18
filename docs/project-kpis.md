# Project KPIs — definitions, evidence and implementation plan

**Status:** proposed measurement contract, 2026-11-18  
**Purpose:** measure learning outcomes, scientific quality, documentation integrity, software reliability, knowledge traceability and maintainability without rewarding content volume.  
**Authority:** this document defines KPI semantics. Existing registries and reports remain canonical; this is not a new content registry.

> **Interpretation:** targets below are provisional hypotheses, not measured results. Missing evidence is reported as *not measured*, never as zero or success. Calibrate targets after baseline and pilot cycles.

## 1. Measurement principles

1. Measure outcomes and evidence, not activity volume (pages, concepts, commits, tests or closed issues).
2. Keep pedagogical mastery, scientific validity, implementation correctness and operational health separate.
3. Publish numerator, denominator, scope, timestamp, repository commit and method for every computed rate.
4. Distinguish automated checks from human-reviewed judgments.
5. Use representative samples where exhaustive review is impractical; record sampling frame, sample size and reviewer agreement where feasible.
6. Do not aggregate dimensions into one health score.
7. Preserve reproducibility and trends without duplicating canonical project data.

## 2. Core KPI catalogue

### 2.1 Learning outcomes

| ID | KPI | Definition | Initial target | Evidence |
|---|---|---|---:|---|
| EDU-01 | Objective mastery | Learner-objective assessments meeting a predeclared mastery rubric / valid assessments | ≥80% | Learner-validation pilot; human-reviewed |
| EDU-02 | Learning gain | Mean post-test minus pre-test score, in percentage points, for matched participants and equivalent assessments | ≥20 pp (pilot hypothesis) | Pilot; report sample size and uncertainty |
| EDU-03 | Independent transfer | Participants completing a novel task without solution-level guidance / participants attempting it | ≥70% (pilot hypothesis) | Understand/Build transfer tasks; human rubric |
| EDU-04 | Path progression | Participants reaching the next defined milestone / participants who began the path and had sufficient follow-up | Baseline first | Learning path and pilot |

Understand and Build have distinct evidence requirements. Do not merge their milestones or infer mastery from page/path completion. Report by path and topic where sample sizes permit. Do not publish learner-level personal data.

### 2.2 Scientific and experimental quality

| ID | KPI | Definition | Initial target | Evidence |
|---|---|---|---:|---|
| SCI-01 | Claim evidence coverage | Audited substantive scientific claims with traceable, relevant source or documented derivation / claims audited | ≥95% | Page/source audit; human review |
| SCI-02 | Experiment reproducibility | Published experiments independently rerun within declared tolerance / experiments sampled for reproduction | 100% of those labelled reproducible | Experiment protocol and reproduction reports |
| SCI-03 | Experimental completeness | Experiments satisfying all applicable protocol fields (question, baseline, data, method, controls, metrics, uncertainty, results, error analysis, limitations) / experiments audited | 100% | Experiment protocol; automated checks + review |
| SCI-04 | Limitation disclosure | Audited claims with material scope/limitations stated / claims for which limitations are material | ≥95% | Human review |

A passing unit test, correct formula, successful execution or lower training loss is not by itself evidence of a scientifically valid conclusion.

### 2.3 Documentation and bilingual quality

| ID | KPI | Definition | Initial target | Evidence |
|---|---|---|---:|---|
| DOC-01 | FR/EN semantic parity | Audited bilingual pairs preserving equivalent claims, assumptions, examples, caveats and exercises / pairs audited | 100% | Rendered bilingual review |
| DOC-02 | Editorial acceptance | Audited pages satisfying criteria for their declared page role / pages audited | ≥90% | Page metadata and editorial review |
| DOC-03 | Internal reference integrity | Valid internal links and anchors / links and anchors checked | ≥99%; CI target 100% | Rendered-site link/fragment checks |
| DOC-04 | Critical editorial debt | Open high-impact editorial defects, segmented by severity and age | Downward trend | GitHub issues |

### 2.4 Software and operational reliability

| ID | KPI | Definition | Initial target | Evidence |
|---|---|---|---:|---|
| ENG-01 | Relevant CI success | Successful relevant completed CI runs / all relevant completed runs in the window; exclude cancellations and separately classify infrastructure failures | ≥98% | GitHub Actions; workflow/branch scope |
| ENG-02 | Critical invariant coverage | Identified critical invariants with executable tests / critical invariants in reviewed inventory | ≥95% | Invariant inventory and tests |
| ENG-03 | Clean-environment reproducibility | Successful clean setup and required checks / documented clean-environment attempts | 100% | Reproduction workflow |
| ENG-04 | Validation scalability | Runtime and peak memory by workload shape and size, with commit/runner/runtime metadata | Baseline first | Existing benchmark reports |

Code coverage is not a substitute for invariant coverage. Report flaky failures and runner variation separately.

### 2.5 Knowledge provenance and graph quality

| ID | KPI | Definition | Initial target | Evidence |
|---|---|---|---:|---|
| KNO-01 | Provenance completeness | Audited evidence-bearing records with valid source/locator lineage appropriate to their type / records sampled that require provenance | ≥98% | Source catalogue, extractions and lineage audit |
| KNO-02 | Claim-to-source traceability | Audited substantive claims traceable to a specific source and relevant location or derivation / claims sampled | ≥95% | Page/extraction/source crosswalk |
| KNO-03 | Relation evidence quality | Audited semantic relations with valid type/endpoints and supporting rationale/evidence / relations sampled | ≥90% initially | Concept graph human review |
| KNO-04 | Source review freshness | Priority sources reviewed within declared interval / priority sources due for review | ≥95% | Source inspection history |

Graph density or edge count is not knowledge quality. A syntactically valid edge is not automatically scientifically justified. Keep source lineage, semantic concept relations and pedagogical routes distinct.

### 2.6 Maintainability and delivery flow

| ID | KPI | Definition | Initial target | Evidence |
|---|---|---|---:|---|
| OPS-01 | Issue resolution time | Median elapsed time from issue creation to closure, segmented by priority and type | Baseline first | GitHub issues |
| OPS-02 | Overdue backlog rate | Open actionable issues past explicit target date / open actionable issues with target date | ≤10% after dates are maintained consistently | GitHub issues |
| OPS-03 | Reopen rate | Issues reopened after closure / issues closed in reporting cohort | ≤5% | GitHub issue history |
| OPS-04 | Maintenance effort share | Maintenance/repair time / total recorded project effort in same period | Baseline first; do not minimize blindly | Voluntary time log or estimates |

Use issue age and blocked status alongside resolution time. Avoid optimizing for rapid closure at the expense of correctness.

## 3. Risk and control indicators

| KPI at risk | KRI (risk signal) | KCI (control effectiveness) |
|---|---|---|
| SCI-01 / KNO-02 | High-impact claims with missing, stale or irrelevant evidence | Sampled claims passing source/locator review |
| DOC-01 | Material FR/EN divergence in claims or caveats | Bilingual changes receiving parity review |
| ENG-01 | Repeated failures, flaky tests and recovery time | Failures triaged/classified within agreed window |
| ENG-04 | Runtime/memory growth or widening run variance | Benchmark runs retaining reproducibility metadata |
| EDU-01 / EDU-03 | Ambiguous learner-task rubrics or insufficient observations | Pilot tasks reviewed/calibrated before use |
| KNO-03 | Unsupported, ambiguous or contradictory relations | Sampled relations reviewed with evidence/rationale |

## 4. Measurement contract

Every KPI observation should expose:

- `kpi_id`: stable ID from this catalogue;
- `period_start`, `period_end`, and `measured_at` (ISO 8601 UTC);
- `repository_commit`: exact commit SHA;
- `value`, `unit`, and `numerator`/`denominator` where applicable;
- `scope`: paths, workflows, population, sample or issue filters;
- `method_version`: calculation or rubric version;
- `evidence`: paths/URLs to reports or source records;
- `measurement_type`: automated, human-reviewed or mixed;
- `limitations` and `status`: measured, not-measured, insufficient-sample or invalid.

Do not store personal learner-level data in public reports. Aggregate small samples cautiously and suppress potentially identifying breakdowns.

## 5. Existing data sources and ownership

Reuse canonical data; do not create duplicate registries.

| Existing source | Measurements supported |
|---|---|
| `docs/learning-path.md`, `data/guided-route.yml`, Build path | Learning objectives and milestones |
| `docs/learner-validation-pilot.md` | Learner assessment protocol |
| `docs/experiment-protocol.md`, `experiments/`, `reports/` | Experimental completeness and reproducibility |
| `docs/project-status.md` | Implemented / tested / demonstrated / planned distinctions |
| Page metadata and rendered Quarto site | Bilingual parity sampling, editorial role, link integrity |
| `data/sources.yml`, `data/extractions/`, source lineage | Provenance, locators and review history |
| `data/concepts.yml`, `data/domains.yml`, `data/resources.yml` | Typed relations and graph review |
| GitHub Actions | CI reliability and benchmark artifacts |
| GitHub Issues | Defect debt, issue age, resolution and reopening |

## 6. Reporting cadence

- **Per PR:** tests, metadata validation, rendered local-link/anchor checks and relevant bilingual checks.
- **Weekly:** CI trend, priority backlog ageing, regressions and high-impact open defects.
- **Monthly:** source provenance/freshness, concept-relation sample, documentation parity sample and technical benchmark trend.
- **Per learner pilot:** pre/post evidence, transfer tasks, sample size, rubric and uncertainty.
- **Quarterly:** target calibration, KPI usefulness, architecture/maintenance burden and perverse incentives.

## 7. Phased implementation

### Phase 1 — baseline and feasibility
- Map each KPI to existing data and determine whether it is computable today.
- Compute only metrics with defensible numerator, denominator and scope.
- Mark learner outcomes and human-review measures as not measured until observations exist.
- Record commit, environment, method and raw evidence for each baseline.

### Phase 2 — reproducible machine-readable report
- Agree a versioned JSON observation schema.
- Add a small report generator only after source contracts are clear.
- Test calculations, missing data, empty denominators and invalid inputs.
- Emit evidence, limitations and measurement type; do not add a database.

### Phase 3 — human-reviewed measures
- Define sampling frames/rubrics for claims, FR/EN parity, provenance and concept relations.
- Calibrate reviewers and report agreement/uncertainty where feasible.
- Run the learner-validation pilot; do not infer outcomes from page analytics.

### Phase 4 — dashboard and alerts
- Publish trends only after comparable observations exist.
- Alert on meaningful regressions and missing evidence, not arbitrary one-off thresholds.
- Keep noisy performance budgets advisory until runner variance is understood.

## 8. Initial baseline status

No comprehensive KPI baseline has been computed at document creation. The repository contains measurement foundations—a learner-validation pilot protocol, experiment protocol, CI checks, source/concept registries and repeated concept-validator benchmark reports—but these instruments are not proof that the corresponding outcomes have been achieved.

The 2026-11-18 scalability audit says the architecture is directionally scalable but target-scale capacity is not demonstrated. The concept-validator benchmark covers synthetic chains of 500, 2,000 and 10,000 concepts across two hosted-runner executions; it does not establish performance for all graph shapes, source/extraction pipelines or rendered graph interfaces. Preserve these caveats for ENG-04.

## 9. Acceptance criteria

- [ ] Stable KPI IDs, unambiguous formulas and denominators.
- [ ] Targets visibly distinguished from observations.
- [ ] Every observation tied to commit, period, method and evidence.
- [ ] Missing/insufficient evidence represented explicitly.
- [ ] Automated and human-reviewed measurements distinguished.
- [ ] Understand and Build outcomes remain separate.
- [ ] Graph validity is not confused with semantic truth or evidence quality.
- [ ] No duplicate canonical registry introduced.
- [ ] Baseline report reproducible and tested before dashboard/alerts.
- [ ] Targets reviewed after baseline and pilot cycles.

## 10. Related contracts

- [Learning path](learning-path.md)
- [Learner validation pilot](learner-validation-pilot.md)
- [Experiment protocol](experiment-protocol.md)
- [Project status](project-status.md)
- [Information architecture](information-architecture.md)
- [Scalability and capacity audit (2026-11-18)](scalability-capacity-audit-2026-11-18.md)
- [Concept registry validation benchmark (2026-11-18)](concept-registry-validation-benchmark-2026-11-18.md)
- [Roadmap](roadmap.md)

## 11. Quality-driving KPI hierarchy

The 24 KPIs above form the full measurement catalogue. They are not all dashboard headline metrics. Use the following hierarchy to focus decisions while retaining the detailed catalogue as the source of definitions.

### 11.1 Twelve headline indicators

| Priority | Headline KPI | Catalogue mapping | Why it drives quality |
|---|---|---|---|
| Strategic | Learning Outcome Success | EDU-01 | Checks whether learners reach declared objectives |
| Strategic | Learning Gain | EDU-02 | Measures improvement rather than activity or completion |
| Strategic | Autonomous Transfer Rate | EDU-03 | Tests whether understanding transfers to unfamiliar tasks |
| Scientific | Evidence Coverage | SCI-01 | Makes unsupported substantive claims visible |
| Scientific | Experiment Reproducibility | SCI-02 | Tests whether published results can be independently checked |
| Scientific | Scientific Completeness | SCI-03 | Detects missing experimental controls, metrics or limitations |
| Knowledge | Concept Integrity | KNO-03 plus registry validation checks | Separates valid structure from meaningful, justified relations |
| Knowledge | Knowledge Traceability | KNO-01 and KNO-02 | Connects claims and knowledge records to evidence |
| Documentation | FR/EN Semantic Parity | DOC-01 | Protects conceptual equivalence across languages |
| Engineering | Regression Escape Rate | Supplementary metric; see §12 | Reveals defects escaping pre-merge controls |
| Engineering | Clean Build Reliability | ENG-03 | Measures reproducibility from a clean environment |
| Engineering | Validation Scalability | ENG-04 | Checks whether quality controls remain affordable as the corpus grows |

These headline indicators are a decision-oriented view, not a replacement for the stable KPI IDs. Concept Integrity must not be interpreted as a count of valid YAML records alone: its human-reviewed semantic component must assess definitions, endpoints, relation types and evidence.

### 11.2 Three strategic outcomes

Use these three questions in quarterly project reviews:

1. **Learning transfer:** can learners explain and apply mechanisms in a new situation without solution-level guidance?
2. **Evidence and reproducibility:** can an independent reader trace and verify important claims and experimental results?
3. **Quality preservation at scale:** can the project add sources, concepts, experiments, pages and learning paths without degrading correctness, discoverability, performance or maintainability?

Do not calculate a weighted composite score from these outcomes. Report each dimension with its evidence and uncertainty.

## 12. Supplementary diagnostic KPIs

These measures complement the core catalogue. Promote one to the headline set only when its definition, data source and decision use are stable.

| ID | KPI | Operational definition | Measurement / caveat |
|---|---|---|---|
| EDU-05 | Misconception Rate | Recurring target misconceptions observed / misconception opportunities assessed | Requires a reviewed misconception taxonomy and learner-task rubric; segment by concept |
| EDU-06 | Concept Prerequisite Coverage | Audited concepts with necessary prerequisites identified and pedagogically ordered / concepts audited that require prerequisites | Human review required; absence of a prerequisite is not always a defect |
| EDU-07 | Time to Understand | Median elapsed learner time to meet a predefined mastery criterion | Use only with a consistent task and opt-in, privacy-preserving observations; do not equate time spent with learning |
| PATH-01 | Broken Learning Path Rate | Audited path steps with missing, inaccessible or unsatisfied prerequisites / path steps audited | Combine automated link/metadata checks with manual pedagogical review |
| SRC-01 | Priority Source Freshness | Priority sources reviewed within their declared review interval / priority sources due for review | Complements KNO-04; use one canonical source-review history |
| DOC-05 | Documentation Debt | Open editorial/scientific documentation defects weighted by severity and age | Complements DOC-04; publish weighting rules and raw counts to avoid hiding severe defects |
| ENG-05 | Flaky Test Rate | Tests with inconsistent outcomes under unchanged inputs/environment / tests rerun for flakiness assessment | Separate product failures, runner/infrastructure failures and nondeterminism |
| ENG-06 | Regression Escape Rate | Defects first detected after integration / all defects detected in the same mature cohort | Define cohort, detection window and severity; attribution is often imperfect |
| OPS-05 | Issue Recurrence Rate | Defects recurring after a fix / fixed defects observed over a defined follow-up window | Define recurrence links and follow-up window; issue closure alone is not success |
| OPS-06 | Maintenance Cost Ratio | Maintenance and repair effort / total recorded project effort | Use only if effort data are consistently captured; never optimize by suppressing maintenance |
| SCI-05 | Evidence Gap Rate | High-impact audited claims with absent, stale or insufficient evidence / high-impact claims audited | A risk-oriented complement to SCI-01; publish severity and evidence-gap categories |

Avoid double-counting: SRC-01 may be implemented as a view of KNO-04; DOC-05 may be a severity/age-weighted view of DOC-04. Do not create separate registries or duplicate observations when the same canonical evidence can support both.

## 13. Quality gates, drivers and strategic outcomes

Classify measures by the decisions they support. A KPI can be both a trend measure and a gate only when its scope and evidence are suitable.

### 13.1 Quality gates

Quality gates are release/merge conditions for the relevant change scope, not global claims that the whole project is perfect.

| Gate | Proposed rule | Scope and exception handling |
|---|---|---|
| Data and metadata validity | All applicable required validators pass | Run validators affected by changed data and required global checks |
| Critical regression | No unresolved critical regression introduced by the change | Severity and evidence must be recorded; flaky/infrastructure failures are triaged separately |
| Internal references | No broken internal links/anchors in the affected rendered scope | Full-site check where feasible; explain exclusions |
| Experiment reproducibility | Do not label an experiment reproducible unless its declared reproduction procedure passes | Gate only experiments changed or newly labelled; retain environment/tolerance metadata |
| Bilingual parity | Material claims, assumptions, caveats and exercises are equivalent for changed bilingual content | Human review for semantic equivalence; automated presence checks are insufficient |

A gate must have a named check, a defined scope, an actionable failure message and a documented exception path. Do not block unrelated changes on a measure that has not yet been instrumented reliably.

### 13.2 Quality drivers

Use these to prioritize work and evaluate trends: EDU-01–04, SCI-01–04, DOC-01–04, ENG-01–04, KNO-01–04 and selected supplementary indicators. They should normally trigger investigation and corrective work rather than automatic rejection on a single noisy observation.

### 13.3 Strategic outcomes

Review learning transfer, evidence/reproducibility and quality preservation at scale quarterly. These outcomes require multiple indicators and qualitative interpretation; they are not individual pass/fail checks.

## 14. KPI-to-action decision rules

The dashboard must make the next useful action clear. The following are default playbook mappings; thresholds and escalation windows are calibrated after baselines.

| Signal | First investigation | Likely corrective action |
|---|---|---|
| EDU-02 learning gain falls | Check cohort comparability, assessment equivalence, sample size and uncertainty | Revise explanations, exercises, examples or prerequisites; rerun the pilot |
| EDU-03 transfer falls or EDU-05 misconceptions rise | Inspect failed tasks and misconception patterns by concept | Add contrastive examples, mechanism-level explanations and novel transfer exercises |
| SCI-01 evidence coverage falls / SCI-05 gaps rise | Identify high-impact unsupported claims and source relevance | Source, qualify, test or remove claims; record unresolved uncertainty |
| SCI-02 reproducibility fails | Compare commit, environment, data, seeds, dependencies and tolerance | Repair protocol or implementation; withdraw reproducibility label until rerun |
| SCI-03 completeness falls | Identify missing protocol elements | Complete controls, baselines, metrics, uncertainty, error analysis or limitations |
| KNO-01/02 traceability falls | Trace records to source locators and extraction lineage | Repair lineage and locators at the canonical source; regenerate dependent outputs |
| KNO-03 relation quality falls | Review relation semantics, endpoints, rationale and contradictory edges | Correct or remove unsupported relations; add explicit relation evidence |
| DOC-01 parity falls | Compare claims, caveats, examples and exercises in both languages | Update the incomplete language version and require bilingual review |
| PATH-01 broken path rate rises | Locate inaccessible steps, missing prerequisites or dead ends | Repair path metadata, navigation and pedagogical ordering |
| ENG-01 CI reliability falls / ENG-05 flakiness rises | Classify product, test, runner and infrastructure failures | Fix root cause, quarantine only with an issue and expiry, improve deterministic setup |
| ENG-03 clean build reliability falls | Reproduce from documented clean environment | Fix hidden dependencies, setup instructions, lockfiles or environment assumptions |
| ENG-04 scalability degrades | Compare runtime/memory by workload shape, size, runner and commit | Profile bottlenecks, optimize incremental processing and set evidence-based budgets |
| OPS-03 reopen / OPS-05 recurrence rises | Check whether fixes addressed root causes and acceptance criteria | Improve issue diagnosis, regression tests and definition of done |
| DOC-04 / DOC-05 debt grows | Segment by severity, age, affected learning path and scientific risk | Prioritize high-impact debt; avoid optimizing raw issue count |

Escalation should consider severity, persistence and confidence. A small-sample learner result or noisy benchmark should trigger review, not a false claim of regression.

## 15. Dashboard and measurement architecture

### 15.1 Recommended layers

1. **Canonical project data:** existing source, extraction, concept, domain, resource, page, experiment, issue and workflow records remain authoritative.
2. **Measurement adapters:** small scripts or queries read canonical data and expose explicit, versioned calculations. Adapters must not silently repair or rewrite source records.
3. **Observation output:** emit immutable, commit-pinned KPI observations using the contract in §4. Store generated reports as build artifacts or versioned reports only where they have durable project value.
4. **Human review records:** store sampling frame, rubric version, reviewer role, sample size, agreement and evidence references. Avoid learner personal data and unnecessary reviewer data.
5. **Presentation:** dashboard views group by strategic dimension, headline KPI, trend, confidence/status, evidence and recommended action. It is a view over observations, not another source of truth.
6. **Alerts:** alert on sustained, material changes, critical evidence gaps and failed gates. Include the affected scope and a link to the evidence.

### 15.2 Dashboard minimum fields

For each displayed KPI show:
- stable KPI ID and human-readable name;
- current value, unit, numerator and denominator where applicable;
- baseline and previous comparable period;
- target or threshold, explicitly labelled provisional or calibrated;
- trend and sample size;
- measurement status (measured, not-measured, insufficient-sample, invalid);
- measurement type (automated, human-reviewed or mixed);
- commit, period, method version and evidence link;
- limitations and next action.

Do not render missing data as zero, green, or success. Do not compare observations with different scopes or method versions without an explicit comparability warning.

### 15.3 Automation boundaries

**Good automation candidates:** schema/metadata validity, internal links, workflow outcomes, benchmark runtime/memory, clean-build checks, source-locator presence and mechanical lineage integrity.

**Human or mixed assessment required:** conceptual correctness, claim relevance, scientific interpretation, relation quality, bilingual semantic parity, editorial acceptance, misconception analysis and learner transfer.

Automation can prioritize samples and detect anomalies, but must not claim to establish scientific truth or learner understanding by itself.

### 15.4 Anti-gaming and quality safeguards

- Publish numerator and denominator; do not report percentages alone.
- Keep raw counts and severity distributions beside weighted scores.
- Never reward page, concept, relation, commit, test or issue volume as a proxy for quality.
- Do not improve resolution time by closing issues prematurely.
- Do not improve test success by deleting difficult tests or silently quarantining flaky tests.
- Do not improve evidence coverage by attaching irrelevant citations.
- Do not improve bilingual parity by reducing the richer language version without editorial justification.
- Keep failed, excluded and insufficient-sample observations visible.
- Version rubrics and calculation methods; preserve historical observations rather than rewriting them.
- Review incentives and thresholds quarterly for unintended consequences.

## 16. Rollout priorities and definition of done

### Immediate — establish trustworthy baselines
- [ ] Map the 12 headline KPIs to concrete repository paths, workflows or pilot instruments.
- [ ] Mark each as automatable, human-reviewed, mixed or currently unmeasurable.
- [ ] Calculate only values with defensible numerator, denominator and scope.
- [ ] Add regression-escape and flaky-test definitions only after agreeing on defect/test cohort semantics.
- [ ] Publish a baseline report with commit, method, limitations and explicit missing-data statuses.

### Next — make measurements repeatable
- [ ] Implement a minimal versioned observation schema and report generator.
- [ ] Add unit tests for denominators of zero, missing fields, exclusions, cohort filters and method changes.
- [ ] Add CI reporting for technical gates without duplicating existing validators.
- [ ] Define review samples and rubrics for claims, relations, bilingual parity and editorial quality.

### Then — measure learner outcomes
- [ ] Run the learner-validation pilot with pre/post assessments and independent transfer tasks.
- [ ] Record sample size, attrition, assessment equivalence, rubric and uncertainty.
- [ ] Add misconception analysis only after defining a reviewed taxonomy.
- [ ] Protect learner privacy and do not publish identifiable individual-level data.

### Finally — dashboard and governance
- [ ] Build a read-only dashboard from observation outputs.
- [ ] Add trend alerts only after comparable baselines exist.
- [ ] Review targets, cost, usefulness and unintended incentives quarterly.
- [ ] Retire indicators that do not change decisions or cannot be measured reliably.

The KPI system is considered operational only when a reviewer can reproduce a displayed value from its cited evidence and commit, understand its limitations, and identify the decision it is intended to inform.


## 17. Focused quality-measurement and test-strengthening work (2026-11-18)

### 17.1 Decision: replace CI Reliability in the four-KPI dashboard

CI Reliability remains useful operational telemetry, but it is generic delivery health. Keep it outside the four primary project-quality KPIs. Use **Critical Invariant Coverage** (existing catalogue KPI ENG-02) as the fourth KPI; *Mathematical Invariant Protection* may be used as its explanatory label. This reuses ENG-02 rather than creating a duplicate KPI.

Operational definition:
- Numerator: critical, reviewed invariants with at least one executable test whose assertion can detect a violation.
- Denominator: all critical invariants in the reviewed inventory for the declared scope.
- Report numerator/denominator, scope, inventory revision, test paths and commit. Do not infer invariant coverage from line coverage or test count.
- Initial status: **not measured** until the inventory and mapping are reviewed. The existing 90% code-coverage threshold is not an invariant-coverage baseline or target.
- Mutation testing is a supplementary diagnostic of test strength, not the KPI denominator and not a substitute for reviewing inventory completeness.

The four-KPI dashboard is therefore Source-to-Knowledge Coverage, Knowledge Validation Status, Learning Page Metadata Coverage and Critical Invariant Coverage. CI Reliability remains a secondary operational indicator.

### 17.2 Test audit — first scope

Before adding tests, inspect existing tests and implementations in this order:
1. **attention:** softmax normalization and shift invariance; causal-mask orientation and future-token exclusion; attention shape and numerical edge cases.
2. **losses:** cross-entropy reference values, gradient finite-difference checks, extreme logits and documented input/target conventions.
3. **gpt_ops:** layer-normalization convention and epsilon, GELU reference points, linear projection dimensions and deterministic behavior.
4. **transformer_block and gpt:** residual/normalization ordering, shape propagation, causal behavior and small deterministic end-to-end outputs.
5. **training_examples:** exact input/target one-token shift, window boundaries, stride and short-sequence behavior.
6. **generate and decoding_filters:** deterministic decoding, stopping conditions, top-k/top-p boundaries and probability validity.
7. **embedding_inspection and GPT-2 weight mapping:** index bounds, dimensions, mapping completeness and independent reference parity where practical.

For each candidate invariant, record its statement, implementation location, existing tests, missing case, proposed minimal test and whether the assertion is independent of the implementation. Do not create a permanent second invariant registry unless the audit demonstrates a concrete need; begin with a small reviewed table in the audit report or this document.

### 17.3 Test design rules

- Prefer deterministic examples, parametrized boundary cases and mathematical properties over duplicated examples.
- Use finite-difference gradient checks only on tiny arrays, with documented tolerances and numerically stable points.
- Use metamorphic tests when a reliable relation is known (for example, softmax invariance to adding a constant to every logit).
- Use independent reference values or implementations for high-value checks; avoid tests that merely reproduce production formulas line-for-line.
- Keep tests offline, CPU-only, seeded and small. No model downloads, large checkpoints, network calls or benchmark-sized fixtures in the fast path.
- Test error handling only where the function contract promises validation.
- Make pedagogical conventions explicit: tensor shapes, axis meanings, normalization convention, epsilon, masking polarity and tolerance.

### 17.4 CI integration without duplicate work

The current CI already runs the full pytest suite with two workers, uses path-scoped domain validation, and keeps benchmark and locator-inventory jobs opt-in. Preserve this architecture:
1. Add missing tests to the existing pytest suite; do not add a second pytest invocation that repeats them.
2. Keep tiny deterministic invariant tests in the ordinary suite.
3. Reuse existing path-scope logic for expensive reference dependencies; extend it only when a new test genuinely needs an optional dependency.
4. Do not split fast tests into another CI job unless measurements show a net feedback-time benefit without duplicate setup or execution.
5. Run mutation testing only on a small allowlist of critical modules, on a schedule or manual dispatch. Publish its report as an artifact and keep it advisory initially.
6. Keep large benchmarks, full-corpus audits and clean-environment reproduction outside the per-PR fast path unless a change specifically requires them.
7. Record wall-clock duration before and after CI changes. Revert or redesign additions that materially increase routine feedback time without commensurate risk reduction.

### 17.5 Remaining work and acceptance criteria

**A — Inventory existing tests**
- [ ] Locate the actual test modules and map them to the seven implementation areas above.
- [ ] Record current test commands, coverage configuration and existing property/reference tests.
- [ ] Identify duplicates and gaps; do not infer missing tests from filenames alone.

**B — Build the invariant-to-test map**
- [ ] Select a small first batch of high-impact invariants: attention causality, softmax stability, cross-entropy gradient, input/target alignment and deterministic generation.
- [ ] Review each invariant against the implementation contract and an independent mathematical/reference expectation.
- [ ] Map each selected invariant to meaningful assertions and identify untested boundaries.
- [ ] Establish a reviewed denominator for ENG-02 and calculate its first baseline.

**C — Add only justified tests**
- [ ] Add the highest-value missing tests to existing test modules.
- [ ] Use deterministic, tiny fixtures and explicit tolerances.
- [ ] Verify that tests fail under a deliberate local fault or equivalent mutation where practical.
- [ ] Run relevant tests and the complete existing suite; retain failure diagnostics.

**D — Add optional mutation diagnostics**
- [ ] Evaluate a mutation-testing tool on one or two small modules before adding a dependency or workflow.
- [ ] Check runtime, mutation equivalence/noise, reproducibility and report usefulness.
- [ ] If worthwhile, add a scheduled/manual workflow with pinned dependencies and a narrow module allowlist.
- [ ] Keep the result advisory until a stable baseline and actionable threshold exist.

**E — Update KPI and CI documentation**
- [ ] Promote ENG-02 / Critical Invariant Coverage to the fourth primary KPI.
- [ ] Retain CI Reliability as a secondary operational measure.
- [ ] Document inventory scope, numerator, denominator, evidence and review date.
- [ ] Compare CI duration before/after; confirm that the PR fast path has no redundant test run.
- [ ] Update the KPI PR and tracking issue with actual findings and measured results.

**Definition of done:** every counted invariant traces to a documented property and executable test; the first ENG-02 value is reproducible from that mapping; tests run in the existing fast suite without a duplicate invocation; and mutation analysis, if adopted, is separately scoped, measured and non-blocking until proven reliable.

No test additions, mutation tooling or CI workflow changes are claimed by this plan. Those changes remain pending the audit and evidence above.
