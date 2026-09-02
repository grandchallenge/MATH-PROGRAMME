# Agent instructions

MATH-PROGRAMME owns mathematics-specific policy and pins adopted cross-programme standards. Agents work through ordinary branches and protected pull requests. Standing delegated authority permits routine bounded administrative, documentation, engineering, workflow, maintenance, routing, synchronization, and campaign-execution transactions to proceed through protected merge and readback when their affected checks pass. Agents may not manufacture mathematical independence, self-certify substantive mathematical claims, bypass protected controls, or promote claims outside their granted authority.

Current routine execution is governed by [`docs/governance/STREAMLINED_EXECUTION_AMENDMENT.md`](docs/governance/STREAMLINED_EXECUTION_AMENDMENT.md), [`docs/WORKFLOW_COVERAGE.md`](docs/WORKFLOW_COVERAGE.md), and [`docs/governance/AGENT_CADENCE_OPERATING_DESIGN.md`](docs/governance/AGENT_CADENCE_OPERATING_DESIGN.md).

## Routine execution rule

For bounded work within already-authorized scope:

1. classify the material evidence closure;
2. run the affected checks selected by current policy;
3. exercise the standing delegated disposition;
4. merge through protected controls when the candidate remains mergeable and its relevant dependencies and authority boundary are unchanged;
5. read back protected state.

Do not request a fresh Human Steward approval or generic independent review for routine work. Do not manufacture a synchronization commit, update a branch, rerun unaffected checks, or invalidate a prior disposition merely because protected `main` moved. Specialist non-author review remains appropriate for substantive mathematical certification, source-semantic adjudication, constitutional authority expansion, security-sensitive protection weakening, and external claim promotion.

## Mandatory execution routing

Every direct workflow under `.github/workflows/` must be registered in `.ghos-routing/workflows.json`. Workflow bytes determine observed execution features and topology; registry prose cannot downgrade them. Any workflow that is autonomous, opaque, credential-bearing, waiting, or write-capable must use the exact admitted persistent controller with compatible capabilities.

Do not add, remove, or change a workflow without updating the routing registry and passing `routing-enforcement`. A bounded conversational agent may perform individual authorized transactions, but it may not serve as the sole persistent controller for unattended campaign execution.

Control maintenance and emergency recovery follow [`docs/governance/GHOS_ROUTING_CONTROL_RUNBOOK.md`](docs/governance/GHOS_ROUTING_CONTROL_RUNBOOK.md).

## Terminal documentary integrity

Governed work is not complete merely because its operational objective succeeded. Before describing, closing, or marking governed work as complete, agents must verify that the applicable durable continuity record is complete:

- authoritative artifact identified;
- artifact-ledger reference and entry recorded;
- applicable review provenance and evidence references retained;
- cross-document consistency reviewed with no hidden blocking conflict;
- final editorial integration reviewed;
- unresolved documentary obligations either cleared or explicitly kept open.

There are two machine-enforced closure routes:

1. Schema-bound Agent Council records use `amanuensis_control`. Lifecycle states `completed`, `certified`, `published`, and `archived` are terminal and must satisfy the continuity gate even when `promotion.ready_for_next_stage` is false.
2. Other governed operations that are explicitly registered under the documentary-closure control carry `governance/rebuild_evidence/<ID>/closure_contract.json` conforming to `schemas/governed_closure_contract.schema.json` and listed in `governance/governed_closure_registry.json`.

The registered governed-operation route is explicitly two-phase. Before protected admission, the contract uses `CANDIDATE_AWAITING_PROTECTED_ADMISSION`, carries no terminal-evidence claim, and retains `protected_pr_admission_and_readback` as unresolved. A later protected canonical record may use `CANONICAL_ON_PROTECTED_MAIN` only when that route's machine contract is satisfied.

Those route-specific schema fields are not a generic programme-wide approval ceremony. In particular, a legacy closure schema's `exact_reviewed_head` or `independent_review_*` fields do not create a fresh reviewer requirement for unrelated routine work. Where a registered closure contract still requires such fields, satisfy that exact machine contract or reconcile the control through a separately governed change; do not generalize it into a universal execution rule.

Protected readback is evidence that the admitted result exists on protected state. It does not create a second Human Steward or independent-review cycle.

Do not close a canonical tracker while a genuinely required documentary obligation is missing. Historical artifacts are not silently reclassified. The only rebuild-evidence package exempt from a closure contract is the fixed legacy baseline enforced by `ci/validate_documentary_closure.py` and declared in `governance/governed_closure_registry.json`. Agents must not create a new legacy exemption merely to avoid documentary closure.

Canonical continuity policy: `docs/AGENT_COUNCIL_GOVERNANCE.md` and `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`.

## Construction Gate routing

For work that may enter `gcl/dev/*` or `gcl/candidate/*`, follow [`docs/governance/CONSTRUCTION_GATE_OPERATING_GUIDE.md`](docs/governance/CONSTRUCTION_GATE_OPERATING_GUIDE.md).

- Do not require the user to know or say `CREATE_DEVELOPMENT`, `UPDATE_DEVELOPMENT`, `FREEZE_CANDIDATE`, "advance", or "freeze".
- Keep ordinary drafting and revision on an ordinary working branch. The Gate is a one-way admission lane for an exact prepared commit, not the normal editing workflow.
- Interpret a request to prepare an exact version for governed or formal review as a possible Gate admission. State that interpretation, check whether the target is registered on protected `main`, and stop for protected target registration when it is not.
- Treat a clear request to lock, finalize, or submit the exact review candidate as authorization to attempt `FREEZE_CANDIDATE`. If finality is ambiguous, ask before freezing because the candidate cannot be updated or replaced in place.
- A Gate operation itself grants no mathematical certification, publication authority, external-claim authority, or protected bypass. Routine merge authority, where applicable, comes from standing delegation and repository protection rather than from the Gate command.

## Recoverable diagnostic and tooling failure

For an already authorized bounded MATH operation, follow [`docs/governance/EXECUTION_RECOVERY_OPERATING_GUIDE.md`](docs/governance/EXECUTION_RECOVERY_OPERATING_GUIDE.md) when ordinary logs, check surfaces, connectors, compiler diagnostics, environments, CI, or replay tooling fail.

- Recoverable operational/tooling failure is not by itself an authority boundary. Continue through the applicable bounded recovery routes.
- Bind diagnostics to the exact run/job/artifact and the candidate bytes they actually describe. Do not patch from stale diagnostics.
- A repository-head change matters only when it changes the material evidence closure, relevant protected dependency, mergeability, scope, or authority boundary. Unrelated `main` movement does not invalidate diagnostic or review evidence.
- Repair only the demonstrated failing theorem/module/validator/scope, then rerun the affected replay or checks required by that repair. Do not rerun unrelated expensive lanes merely to obtain a numerically fresh repository head.
- If connected diagnostic surfaces remain unavailable, use the guide's authenticated local extraction route rather than declaring missing logs a terminal blocker.
- Stop or escalate only at a named governance, authority, authentication, safety, protected-state, materially changed-state, substantive evidentiary, or actual recovery-exhaustion boundary.
- Fail closed on claims, certification, promotion, publication, protected-state mutation, and authority; do not fail closed merely on authorized evidence gathering and bounded repair.
