# Issue backlog governance

This policy defines the operational meaning of issue metadata and the repeatable audit used to keep the open backlog actionable.

## Canonical metadata

Every open issue must carry exactly one priority label (`P0`–`P3`), one domain label (`area:*`) and one work-type label (`type:*`). The label is canonical; a priority repeated in the title is for scanning and must agree. Preserve all other labels.

| Label | Meaning |
|---|---|
| `P0` | Exceptional immediate blocker with demonstrated critical security, integrity or release impact; state the escalation rationale. |
| `P1` | Structural near-term work or a dependency blocking several important deliverables. |
| `P2` | Important, bounded work sequenced after current structural dependencies. |
| `P3` | Optional experiment, polish or improvement with no near-term blocking effect. |

Do not populate P0 for symmetry. Priority is not age, effort, status or visibility. Reassess it when dependencies, evidence, gates or objectives change. A P1 label never authorizes bypassing an explicit prerequisite.

### Domain and type

- `area:*` identifies the primary project domain that owns the work. Choose one.
- `type:*` identifies the principal deliverable (research, audit, documentation, feature, architecture, chore, etc.). Choose one.
- `internal` marks repository/process maintenance that is not itself a learner-facing deliverable.
- `meta` marks genuine coordination, governance or cross-cutting policy work; it does not replace area or type.
- Facet labels such as `documentation` or `research` do not replace the controlled dimensions.

Do not create taxonomy values merely to avoid choosing the closest existing category. Change the controlled vocabulary only with an explicit rationale and corresponding documentation/tests.

## Issue structure and closure

- Keep one canonical issue per coherent deliverable. Split only when acceptance criteria can be independently completed and reviewed.
- Express sequencing through parent/child or blocking relationships. A child owns a bounded output and handoff, not a duplicate parent plan.
- State the evidence required for closure and what that evidence does not establish.
- Close only when mandatory acceptance criteria are met, or when explicitly superseded, duplicate, rejected or no longer applicable with a recorded rationale and destination.
- A merged PR, green CI, documentation update or completed subtask does not by itself satisfy unrelated criteria.
- Preserve unresolved work as open checkboxes. Structural validation does not establish human review, scientific reproduction, rights clearance or external-source inspection.

## Repeatable audit

Run from a checkout with GitHub CLI authenticated and repository access:

```bash
python scripts/audit_issue_metadata.py JM-Brun/llm-lab
```

The script paginates through all open issues, excludes pull requests, and reports priority distribution, missing/multiple priority/area/type labels and title/priority disagreements. It exits non-zero on metadata defects. Rerun after issue creation, label changes or backlog triage.

The audit is a snapshot, not a semantic priority decision or completion review; those remain maintainer judgments.

## Baseline — 2026-11-19

The complete inventory contained 85 open issues: P0 0, P1 13, P2 58 and P3 14. All 85 had exactly one priority, area and type label after normalization; no title/priority disagreement was found. This is a dated snapshot, not a permanent assertion.
