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
