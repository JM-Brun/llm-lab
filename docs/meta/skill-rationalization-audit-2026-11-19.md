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


## Exhaustive inventory and routing-boundary correction — 2026-11-19

The repository Git tree was enumerated recursively from `main` (tree response `truncated=false`). It contains exactly **19** files matching `.agents/skills/*/SKILL.md`. The earlier count of 18 was incomplete: it omitted `llm-learning-explorer`. This section supersedes the earlier 18-file completeness caveat and corrects the inventory count; it does not claim that every supporting file inside every skill directory has been reviewed.

### Complete skill inventory

| Skill | Primary responsibility | Routing boundary |
|---|---|---|
| `audit-skill-routing` | Select and coordinate audit specialists | Sole router for audit selection, not all project tasks |
| `build-path-audit` | Implementation route, dependencies, executable artifacts and reproducibility | Build-specific audit |
| `editorial-boundary-audit` | Explanatory ownership, duplication and relocation | Editorial decisions |
| `knowledge-and-learning-integration` | Apply reviewed source items to canonical knowledge and learning content | Phase B integration |
| `knowledge-architecture-audit` | Formal information architecture, graph and metadata invariants | Structural correctness |
| `knowledge-change-workflow` | Dispatch knowledge changes to existing workflows | Change orchestration, not audit selection |
| `learner-path-feedback` | Evaluate the public journey from a learner perspective | Experience feedback, not authoring standard |
| `learning-path-excellence` | Set learning-design ambition and value criteria | Normative design standard |
| `llm-learning-explorer` | Discover and assess external ideas, projects, analogies and teaching perspectives | Exploration/discovery; intentionally outside the audit router |
| `new-learning-page` | Gate and create a genuinely necessary bilingual learning page | Page creation lifecycle |
| `page-content-audit` | Deep pedagogical/editorial review of one page | Page-level audit |
| `page-group-audit` | Review coherence of page families, sequences and groups | Generic group-level audit |
| `project-learning-resource-audit` | Audit a coherent external learning resource as a system | External project-level audit |
| `rendered-site-audit` | Verify rendered behavior, layout, navigation and accessibility | Runtime/render evidence |
| `scientific-content-audit` | Verify scientific, mathematical, algorithmic and empirical claims | Scientific evidence |
| `source-extraction` | Inspect sources and extract traceable evidence/items | Phase A intake; no page/graph mutation |
| `source-to-learning-integration` | Coordinate source intake and accepted integration | Cross-phase orchestration |
| `understand-path-audit` | Audit conceptual progression and reader comprehension | Understand-specific audit |
| `visual-asset-audit` | Verify asset identity, provenance, rights and reuse | Asset-specific evidence |

### What the count establishes — and what it does not

- The recursive Git tree response was complete (`truncated=false`); the 19-path inventory above is exhaustive for tracked files matching `.agents/skills/*/SKILL.md` on the inspected `main` tree.
- The inventory does not assert that each directory contains only `SKILL.md`; supporting files and nested references require a separate directory-level review.
- `llm-learning-explorer` is not a missing audit-router entry. Its activation contract is discovery and external-idea evaluation, whereas `audit-skill-routing` explicitly selects audit procedures. Keep the distinction; do not turn the audit router into a universal dispatcher.
- The earlier statement that the audit had not enumerated the tree is superseded. The earlier 18-file list and its omission of `llm-learning-explorer` should be read as a first-pass sample, not the final inventory.

### Routing and overlap review status

The router directly names the audit specialists relevant to its scope. Skills with different task lifecycles—`llm-learning-explorer`, `learning-path-excellence`, `learner-path-feedback`, `new-learning-page`, and the knowledge/source workflow skills—must be reached through their own activation contracts or the knowledge-change dispatcher where appropriate, not forced into an audit-only matrix. This is a boundary decision, not proof of complete reachability across every agent entry point.

No skill has been deleted, renamed or merged. The evidence supports preserving the 19 distinct activation contracts while continuing to simplify duplicated orchestration text only where exact procedure comparison demonstrates safe delegation.


## Cross-reference and workflow-ownership pass — 2026-11-19

### Skill-to-skill references

A direct full-text scan of all 19 `SKILL.md` files found the following intended routing/hand-off pattern:

- `audit-skill-routing` names the audit specialists and the knowledge/source workflows needed when an audit request crosses into implementation. It includes Build, Understand, page/group/page-content, editorial, scientific, architecture, rendered, visual, source intake/integration, knowledge change and new-page routes.
- `knowledge-change-workflow` routes knowledge changes to the source integration, Phase B integration, page, group, editorial, architecture and rendered specialists. It is a change dispatcher, not a replacement for the audit router.
- `source-to-learning-integration` explicitly coordinates Phase A `source-extraction` and Phase B `knowledge-and-learning-integration`, and delegates coherent external learning-project reviews to `project-learning-resource-audit`.
- `page-content-audit`, `page-group-audit`, `editorial-boundary-audit`, `knowledge-architecture-audit`, `scientific-content-audit`, `rendered-site-audit` and `visual-asset-audit` refer to one another only for distinct evidence/decision boundaries.
- `learner-path-feedback`, `learning-path-excellence` and `llm-learning-explorer` have their own activation contracts and point to route audits or canonical project contracts where useful. They are not audit-router omissions: learner feedback, design criteria and external discovery are different task types.
- `build-path-audit` and `understand-path-audit` have no need to route to other skills by default; they are bounded specialist procedures. Their absence of outgoing skill links is not evidence of orphan status.

**Finding:** no obvious orphan or circular delegation was established by the direct references in the 19 skill files. This is a static link audit, not evidence of runtime invocation frequency or proof that every natural-language user request activates the intended skill.

### Canonical workflow versus skill instruction

The knowledge-change skill explicitly declares itself an orchestration skill and delegates its normative procedure to `docs/workflows/knowledge-change-workflow.md`. The source-to-learning skill similarly coordinates Phase A/B and references the specialist procedures. This is the desired ownership pattern: skill files provide activation and delegation; workflow documents provide durable step-by-step contracts; schemas and registries own data.

However, the repository has several adjacent source/knowledge workflow documents with distinct but overlapping scopes:

- `docs/workflows/knowledge-change-workflow.md` — general change-mode selection, ownership, evidence, integration and closure;
- `docs/workflows/source-to-learning-system-integration.md` — source/topic intake and integration lifecycle;
- `docs/workflows/source-to-knowledge-validation.md` — validation gates, evidence classes, synthesis quality and regression protocol;
- `docs/workflows/project-learning-resource-audit.md` — coherent external-project-level comparison.

The documents explicitly cross-link and declare complementary scopes. Their existence alone does not prove duplication. The remaining useful review is a section-level responsibility matrix, especially for repeated baseline, source inspection, bilingual parity, validation and completion-report requirements. Do not merge these documents or copy their checklists into skills without a line-level proof that one canonical owner can retain every distinct gate.

### Rationalization decision

No additional skill merge or deletion is justified by this pass. The highest-value next change, if needed, is to remove duplicated normative prose from orchestration skills only where a stable workflow link already owns the requirement. Preserve separate activation contracts and evidence gates.

## Section-level workflow ownership matrix — 2026-11-19

This pass inspected the four canonical workflow documents and their five coordinating/specialist skills. The matrix assigns ownership by decision, not by repeated vocabulary.

| Concern / requirement | Canonical owner | Other documents: permitted treatment | Disposition |
|---|---|---|---|
| Select change mode, state learner problem, choose the smallest intervention | `docs/workflows/knowledge-change-workflow.md` | Source workflow may restate its source-specific entry boundary; project audit may state its project-level trigger | Keep general decision gate in one owner |
| Establish repository baseline, find existing owner/issues/PRs, inspect canonical contracts | Knowledge-change workflow for general changes; source workflow Stage 0 for source intake; project-audit workflow §3 for project-owner reconciliation | Validation protocol may require traceability evidence but should not repeat repository reconnaissance steps | Context-specific baseline checks are valid; avoid copy/paste checklists |
| Register source identity, scan scope, provenance, rights and source status | Source-to-learning-system integration workflow; source schema/records remain data authority | Validation protocol defines inspectability evidence; Phase A skill performs the operational scan | Keep source workflow as lifecycle owner; validation owns acceptance criteria |
| Extract atomic items and preserve source-faithful evidence | Source-to-learning-system integration workflow Stages 1–2; `source-extraction` skill is procedural Phase A owner | Validation protocol defines extraction fidelity gate; Phase B skill consumes records, not re-extracts | Distinct procedure vs gate; do not duplicate extraction checklist |
| Reconstruct source-local pedagogy, graph and route | Source-to-learning-system integration workflow Stages 3–4; source-extraction skill captures evidence | Project audit reconstructs the aggregate project model; validation checks claims and boundaries | Keep source-local and project-level models separate |
| Compare evidence across sources and assess synthesis quality | Source-to-knowledge validation protocol §§4–8 | Source integration workflow defines when and where comparison occurs; Phase B uses approved dispositions | Validation protocol owns quality test; integration owns execution point |
| Decide whether accepted evidence changes LLM Lab concepts/pages/resources | Knowledge-change workflow for general ownership; source integration workflow Stage 5 for source-derived decisions; Phase B skill for item disposition and implementation | Project audit produces project-level differential findings and delegates accepted changes | Keep distinct levels; avoid a second project disposition vocabulary |
| Canonical graph, relation semantics, page ownership, routes and projections | Existing registries/schemas and information-architecture documentation; knowledge-change workflow §5 routes to them | Source integration and project audit describe impact and delegate implementation | Workflows must not supersede data/schema authority |
| Bilingual parity and preservation/conservation | Knowledge-change workflow §§6 and 9 for general changes; source integration Stage 6 for source-derived publication | Project audit requires semantic parity; validation protocol may treat parity as a validation dimension | Retain contextual checks; use one shared template/checklist only if an existing canonical template can own it |
| Validation evidence classes, independent completion states, gates and failure handling | Source-to-knowledge validation protocol | Source integration Stage 7 selects relevant checks; knowledge-change workflow §10 provides a high-level validation-layer map; project audit §9 reports project-level validation | Validation protocol owns normative gate semantics; others link and report scoped outcomes |
| Project audit depth, coverage bias, project-local model and cross-project comparison | Project-level learning resource audit workflow | Source integration and validation protocol only identify when it applies and preserve source-level boundaries | Project-specific requirements; no duplication |
| Completion report and maintenance/revisit triggers | Each workflow owns its own deliverable, limited to its unit of work | Skills summarize required output and point to workflow | Similar report headings are justified because units and evidence differ; avoid a universal mega-report |

### Exact duplication versus useful repetition

**No proven wholesale workflow duplication.** The four workflows describe nested units (change request, source/topic, validation protocol, coherent external project). Their repeated references to baseline, evidence, bilingual checks and validation are mostly contextual hand-offs rather than substitutable procedures.

Three areas merit a future narrow cleanup, but not a speculative merge:

1. **Validation language:** the general knowledge-change workflow §10 lists validation layers, while source integration Stage 7 and project audit §9 describe their scoped checks. Keep the general layer map as a summary; make the validation protocol the sole owner of evidence classes, gate definitions, failure handling and claims about learner validation. Replace any copied gate details with links if a future diff demonstrates exact repetition.
2. **Baseline/reconciliation:** retain the general repository baseline in knowledge-change workflow §3, source-owner reconciliation in source workflow Stage 0, and project-owner reconciliation in project-audit workflow §3. These have different target entities. Do not collapse them into one generic checklist.
3. **Bilingual/preservation checks:** retain the general conservation ledger in knowledge-change workflow §9 and source-derived publication checks in source workflow Stage 6. They share principles but apply to different transformations. A future common template could reduce repeated table structure, but should not erase source-specific provenance or move/merge preservation evidence.

### Skill-to-workflow delegation check

- `knowledge-change-workflow` skill is a short dispatcher to the canonical knowledge-change workflow; it does not reproduce the workflow's gates.
- `source-to-learning-integration` skill coordinates Phase A and Phase B, states their hand-off and routes whole-project requests. Its cross-phase role is distinct from the detailed source-extraction and knowledge-integration procedures.
- `source-extraction` owns Phase A execution and source-faithful capture; `knowledge-and-learning-integration` owns Phase B disposition and project changes. Their procedural depth is appropriate and should not be copied into the orchestrator.
- `project-learning-resource-audit` skill activates the project-level audit and delegates to its workflow/template; it does not replace source records or Phase A/B.

### Additional inspection note

The source-to-learning workflow's scope-boundary heading currently contains literal escaped newline sequences in the fetched Markdown content rather than normal line breaks. This is a formatting defect in that file, not a responsibility overlap. It should be corrected in a separate, tightly scoped documentation patch after checking the raw file and rendered result; it is intentionally not mixed into this dated audit update.

### Decision

No workflow merge, skill merge or deletion is justified. Keep all four workflow documents and five skills. Treat the validation protocol as the sole normative owner for evidence classes and gate semantics; keep workflow-specific execution and completion criteria in their respective documents. Any future deduplication must identify exact duplicated requirements and preserve the local context and evidence outputs.

