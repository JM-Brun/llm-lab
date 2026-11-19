# Issue governance and metadata contract

**Status:** active governance policy  
**Operational source of truth:** GitHub Issues and Pull Requests  
**Scope:** issue classification, prioritisation, dependencies and generated reporting

This document defines how issue metadata is interpreted and checked. It does not create a second backlog or authorize automated changes to issue labels, titles, state, assignees or dependencies.

## 1. Canonical fields

Every open issue (pull requests excluded) must carry exactly:

- one priority label: `P0`, `P1`, `P2` or `P3`;
- one area label from the repository's existing `area:*` vocabulary;
- one work-type label from the repository's existing `type:*` vocabulary.

GitHub labels are canonical. Titles may repeat a priority for readability, but labels take precedence and the two must not contradict one another. An issue title without a priority is acceptable; a title containing more than one distinct priority is ambiguous and must be reviewed.

The allowed area and type values are discovered from labels currently defined in the repository. Do not create a new value merely to make one issue fit. Propose taxonomy changes separately, with examples, migration impact and an explicit rationale.

## 2. Priority semantics

| Label | Meaning | Assignment test |
|---|---|---|
| `P0` | Exceptional immediate critical blocker | Demonstrable security, data/integrity, release or foundational failure requiring immediate intervention |
| `P1` | Near-term structural priority | Blocks several important deliverables, resolves a foundational dependency, or has a time-critical project impact |
| `P2` | Important, bounded work | Valuable and actionable, but sequenced after current structural priorities or prerequisites |
| `P3` | Optional/deferred improvement | Polish, exploration or enhancement without a near-term blocking effect |

P0 is not a synonym for "important". An empty P0 queue is valid. Priority expresses sequencing and impact, not current status, effort, age, ownership or technical certainty.

## 3. Orthogonal metadata

- `area:*` identifies the principal project domain affected.
- `type:*` identifies the nature of the work (for example, audit, documentation, feature, maintenance or test, using only existing repository labels).
- Do not assume `internal` or `meta` are canonical labels. Searches of the current issue set found no issues using either label; their existence in the repository label catalogue and any intended semantics still require a separate taxonomy check. Do not introduce either label without an explicit decision.
- Assignees express explicit ownership, not priority. Do not assign people without a clear basis.
- Milestones express a real delivery grouping, not a substitute for a due date.
- Dependencies must be represented by issue relationships or explicit links, not merely by ordering in a handoff.

An issue can be well classified while still needing semantic review. Passing metadata validation does not prove that its priority is correct, that its work is complete, or that its dependencies are exhaustive.

## 4. Dependency and lifecycle rules

1. Prefer one parent/coordinating issue with linked, independently deliverable child issues over duplicated plans.
2. A child issue must retain its own acceptance criteria and evidence; parent completion must not imply child completion.
3. Record blockers explicitly and remove them when the dependency is resolved.
4. Close an issue only when its acceptance criteria are met and evidence is linked, or use the appropriate GitHub close reason when work is intentionally not planned or is a duplicate.
5. A draft PR, a green check on an outdated commit, or a documentation-only status statement is not proof of completion.
6. Do not close or re-scope issues during metadata cleanup.

## 5. Validation and reporting

Run the read-only audit locally:

```bash
python scripts/issue_metadata_audit.py --repo JM-Brun/llm-lab
```

For deterministic offline validation, pass a JSON fixture containing an object with `issues` and `labels` arrays:

```bash
python scripts/issue_metadata_audit.py --input tests/fixtures/issue-metadata-valid.json
```

The report checks all pages of open issues (excluding pull requests), exactly-one priority/area/type labels, title/label priority contradictions and ambiguous multiple priorities. It prints a Markdown summary and exits non-zero for classification errors. It never writes to GitHub.

A scheduled GitHub Actions workflow runs the audit with a read-only token and publishes the report as a job summary. Treat that report as a timestamped observation, not as a stored backlog or durable KPI. The GitHub issue list remains authoritative.

## 6. Review cadence and ownership

- On issue creation: apply the three canonical classifications before work is queued.
- During triage: review priority against impact, dependencies, current delivery gates and project status.
- Weekly: inspect unclassified issues, stale blockers and priority drift.
- When taxonomy changes: update this contract, existing labels/issues and tests in the same reviewed change.
- When the audit fails: fix the underlying issue metadata after human review; do not weaken the validator to make the report green.

## 7. Non-goals and safeguards

- No automatic priority assignment or issue closure.
- No automatic label mutation.
- No global health score derived from issue counts.
- No requirement to assign every issue or invent due dates.
- No new taxonomy values without an explicit decision.
- No inference that a metadata pass is a technical or scientific review.

## 8. Acceptance criteria for this governance layer

- [x] Priority, area and type are distinct, canonical fields.
- [x] Priority semantics and P0 guardrail are documented.
- [x] A read-only, paginated audit checks the complete open-issue collection.
- [x] Offline fixtures exercise valid and invalid metadata.
- [x] A scheduled/manual workflow reports findings without mutating GitHub.
- [ ] Semantic review of every priority assignment remains a human task.
- [ ] Saved GitHub searches and dependency relationships still require explicit verification.
