# Skill-system rationalization audit

**Audit date:** 2026-11-19  
**Scope:** repository skills under `.agents/skills/*/SKILL.md`, based on direct inspection of the 18 skill files listed below.  
**Status:** initial responsibility/overlap audit; not yet a verified exhaustive directory inventory.  
**Decision policy:** no skill is deleted, renamed, or merged on name similarity alone.

## Executive decision

The inspected skills mostly have distinct responsibilities. The immediate problem is not proven duplication but the risk of overlapping orchestration layers and unclear boundaries between broad and specialized audits.

Keep the specialist capabilities for now. Rationalize by making the router the only entry point for audit selection, keeping one canonical finding/evidence ledger per bounded task, and treating specialist skills as procedures rather than independent governance systems.

Do not add another skill or registry to manage this inventory. This report is a dated decision record, not a new live catalogue.

## Inventory and responsibility map

| Family | Skill | Primary responsibility | Initial disposition |
|---|---|---|---|
| Routing | `audit-skill-routing` | Select the smallest appropriate audit set and coordinate evidence/findings | **Keep as sole audit router** |
| Page and route audits | `page-content-audit` | Deep review of one page or close counterparts | Keep; narrow scope is distinct |
| Page and route audits | `page-group-audit` | Coherence of a page family, sequence, local window or cross-cutting group | Keep as general group-level audit |
| Page and route audits | `understand-path-audit` | Audit the conceptual Understand route and its continuity | Candidate to become a profile/extension of `page-group-audit`; compare procedures before merging |
| Page and route audits | `build-path-audit` | Audit the implementation Build route, dependency order and code teaching | Candidate to become a profile/extension of `page-group-audit`; retain Build-specific checks |
| Pedagogical standards | `learning-path-excellence` | Authoring/quality standard for depth, value and coherent learning design | Keep; normative design standard, not learner test |
| Pedagogical feedback | `learner-path-feedback` | Simulate a learner's journey and record experience-based feedback | Keep; validation perspective differs from authoring standard |
| Editorial ownership | `editorial-boundary-audit` | Detect overlap, misplaced explanations and canonical page ownership | Keep; distinct decision authority |
| Scientific verification | `scientific-content-audit` | Verify mathematical, scientific, algorithmic and empirical claims | Keep; distinct evidence method |
| Knowledge architecture | `knowledge-architecture-audit` | Validate canonical concepts, relations, metadata, routes and projections | Keep; structural source-of-truth owner |
| Rendered experience | `rendered-site-audit` | Verify actual rendered layout, interaction, navigation and accessibility | Keep; runtime evidence cannot be replaced by source inspection |
| Source intake | `source-extraction` | Register sources and extract traceable structured evidence/items | Keep; Phase A boundary |
| Asset rights | `visual-asset-audit` | Identify assets and review provenance, rights, accessibility and reuse | Keep; asset-specific rights work is not ordinary source extraction |
| External learning projects | `project-learning-resource-audit` | Audit a coherent external learning resource as a system | Keep; project-level comparative scope |
| Source orchestration | `source-to-learning-integration` | Coordinate source extraction and accepted integration across phases | Review for consolidation with the two phase skills; avoid duplicated checklists |
| Knowledge integration | `knowledge-and-learning-integration` | Apply validated items to graph, pages, references, visuals and experiments | Keep as Phase B procedure |
| Generic knowledge routing | `knowledge-change-workflow` | Route a proposed knowledge change to the correct existing workflow | Keep only as a short generic dispatcher; do not duplicate specialist procedures |
| New page creation | `new-learning-page` | Gate and create a genuinely necessary bilingual learning page | Keep; distinct creation lifecycle |

## Overlap findings

### 1. Build / Understand / page-group audits — strongest consolidation candidate

The three skills operate at different scopes but share the notion of a learner-facing route:
- `page-group-audit` is the general group/sequence method.
- `understand-path-audit` applies it to the conceptual route.
- `build-path-audit` applies it to the implementation route and adds dependency/code/verification checks.

**Provisional recommendation:** keep the two route-specific procedures until a line-by-line comparison proves that they can be represented as route profiles without losing required checks. If consolidated, the general group audit should own shared method; Build and Understand should become concise profiles or checklists, not competing full audit frameworks.

### 2. Learning-path-excellence / learner-path-feedback — apparent overlap, distinct lifecycle

One sets design expectations; the other tests the actual journey from a learner's perspective.

**Recommendation:** keep both. Make the handoff explicit: excellence is a design criterion; learner feedback is observed validation. Neither should claim the other's evidence.

### 3. Source-extraction / source-to-learning-integration / knowledge-and-learning-integration

These form an intake → orchestration → integration chain. The orchestration skill is justified only if it coordinates work without copying the phase procedures.

**Recommendation:** retain the phase boundaries; inspect the orchestration document for duplicated mandatory steps. If it mostly repeats the two phase skills, reduce it to a short workflow index and decision gate.

### 4. Knowledge-change-workflow / audit-skill-routing

These are not interchangeable: one routes changes to canonical knowledge; the other routes audits. Their scope must remain explicit. Neither should become a universal router for all project work.

### 5. Specialist audit skills

Scientific, rendered-site, visual-asset, editorial and architecture audits have distinct evidence types and acceptance criteria. Combining them into one generic audit skill would obscure important validation boundaries.

## System-level rules to retain

1. `audit-skill-routing` is the only entry point for choosing audit skills.
2. Select one primary skill; add a secondary skill only for a distinct question.
3. One canonical finding ID and owner per finding; other skills reference it rather than opening duplicates.
4. One evidence ledger per bounded audit; do not create per-skill parallel ledgers.
5. Distinguish diagnosis, implementation and validation.
6. Distinguish source inspection, code/tests, rendered observation, scientific correctness and learner evidence.
7. No new skill unless it has a durable, non-overlapping trigger, procedure and output.

## Completeness and evidence limits

- 18 skill files were fetched and inspected by exact path on the default branch on 2026-11-19.
- This is not yet proof that `.agents/skills/` contains exactly 18 directories; the repository tree was not enumerated exhaustively in this pass.
- The audit is a responsibility/overlap review, not a full line-by-line duplication analysis of every procedure and reference file.
- No skill has been deleted, renamed or edited as part of this audit.
- No conclusion about skill runtime invocation frequency or effectiveness is made; that requires usage evidence, not file contents alone.

## Ordered next steps

1. Obtain an exhaustive `.agents/skills/` tree inventory and reconcile it with this 18-file sample.
2. Compare `build-path-audit` and `understand-path-audit` against `page-group-audit` section by section; propose a profile-based consolidation only if all unique checks remain represented.
3. Compare `source-to-learning-integration` with its Phase A and Phase B procedures; remove repeated normative text only after confirming cross-links and callers.
4. Inspect all skill cross-references and router coverage for orphaned, unreachable or multiply-routed skills.
5. Only then propose a minimal patch and run repository-specific validation.

## Change control

This report is a dated audit artifact. Update it only when a new evidence pass changes a disposition. Do not turn it into a second canonical skills registry; the skill files and the router remain authoritative for their own instructions.


## Focused overlap verification — 2026-11-19

A second pass inspected the full text of the three route/group skills and the three source-phase skills.

### Build / Understand / page-group: retain separate skills

The overlap is smaller than the initial trigger wording suggests:
- `build-path-audit` explicitly owns implementation dependency order, executable artifacts, tests, expected outputs, failure modes and reproducibility.
- `understand-path-audit` explicitly owns conceptual progression, reader comprehension, readability, route continuity and rendered reading experience.
- `page-group-audit` owns the generic method for arbitrary page groups, families and sequences; it does not replace the Build-specific implementation contract or the eight-stage Understand route contract.

**Revised disposition:** do not merge these three. Tighten routing so Build requests select Build, Understand requests select Understand, and page-group is used for other page families or as a supporting lens only when a separate group-level question exists. The distinct canonical inputs and acceptance evidence justify separate skills.

### Source orchestration: keep, but avoid procedural duplication

The three phase responsibilities are clear:
- `source-extraction` is Phase A and prohibits page/graph mutation.
- `knowledge-and-learning-integration` is Phase B and consumes persistent reviewed records.
- `source-to-learning-integration` coordinates both phases and defines their hand-off, ordering and project-level routing.

**Disposition:** keep the orchestrator because it owns cross-phase sequencing and hand-off. In future edits, prefer concise links to the Phase A/B procedures over repeating their detailed output checklists. Do not collapse the two phase skills.

### Routing consequence

The router should make the distinctions operational:
- Whole Build route → `build-path-audit`, not automatically `page-group-audit`.
- Theory / Understand route → `understand-path-audit`, not automatically `page-group-audit`.
- Arbitrary page family / adjacency window → `page-group-audit`.
- External source through to accepted project changes → `source-to-learning-integration`; Phase A only → `source-extraction`; Phase B against existing reviewed records → `knowledge-and-learning-integration`.

This is a routing clarification, not a reason to add another skill. The router already contains the principle to select one primary skill and add specialists only for distinct questions.
