# Agent instructions

MATH-PROGRAMME owns mathematics-specific policy and pins adopted
cross-programme standards. Agents may propose changes by branch and pull
request, but may not approve or merge their own work, write to protected
branches, or promote a mathematical claim.

## Mandatory execution routing

Every direct workflow under `.github/workflows/` must be registered in
`.ghos-routing/workflows.json`. Workflow bytes determine observed execution
features and topology; registry prose cannot downgrade them. Any workflow that
is autonomous, opaque, credential-bearing, waiting, or write-capable must use
the exact admitted persistent controller with compatible capabilities.

Do not add, remove, or change a workflow without updating the routing registry
and passing `routing-enforcement`. A bounded conversational agent may perform
individual authorized transactions, but it may not serve as the sole
persistent controller for unattended campaign execution.

Control maintenance and emergency recovery follow
[`docs/governance/GHOS_ROUTING_CONTROL_RUNBOOK.md`](docs/governance/GHOS_ROUTING_CONTROL_RUNBOOK.md).

## Terminal documentary integrity

Governed work is not complete merely because its operational objective
succeeded. Before describing, closing, or marking governed work as complete,
agents must verify that the applicable durable continuity record is complete:

- authoritative artifact identified;
- artifact-ledger reference and entry recorded;
- review provenance and evidence references retained;
- cross-document consistency reviewed with no hidden blocking conflict;
- final editorial integration reviewed;
- unresolved documentary obligations either cleared or explicitly kept open.

There are two machine-enforced closure routes:

1. Schema-bound Agent Council records use `amanuensis_control`. Lifecycle states
   `completed`, `certified`, `published`, and `archived` are terminal and must
   satisfy the continuity gate even when `promotion.ready_for_next_stage` is
   false.
2. Other governed operations must carry a registered
   `governance/rebuild_evidence/<ID>/closure_contract.json` conforming to
   `schemas/governed_closure_contract.schema.json` and listed in
   `governance/governed_closure_registry.json`.

The registered governed-operation route is explicitly two-phase. Before
protected admission, the contract must use
`CANDIDATE_AWAITING_PROTECTED_ADMISSION`, carry no terminal-evidence claim, and
retain `protected_pr_admission_and_readback` as an unresolved documentary
obligation. Only a subsequent protected readback seal may use
`CANONICAL_ON_PROTECTED_MAIN`; that state requires `admission.phase=protected`
and exact reviewed-head, independent-review, policy-run, protected-merge,
signature, protected-main-readback, and terminal-receipt evidence. A candidate
contract is not documentary completion.

Do not close a canonical tracker while a required documentary obligation is
missing. If operational work is complete but documentary closure is not, keep
the documentary obligation explicitly open. In particular, merging the primary
implementation/evidence PR does not by itself permit tracker closure when the
registered closure contract is still in candidate phase; the protected
readback seal must be admitted first.

Historical artifacts are not silently reclassified. The only rebuild-evidence
package exempt from a closure contract is the fixed legacy baseline enforced by
`ci/validate_documentary_closure.py` and declared in
`governance/governed_closure_registry.json`. Agents must not create a new legacy
exemption merely to avoid documentary closure. Any change to that fixed
baseline is itself a governance-control change requiring the same protected
review path. Every newly created rebuild-evidence package outside that baseline
must carry a registered closure contract; omission is a CI failure.

Newly completed or materially revised governed work must use one of the two
closure routes above.

Canonical policy: `docs/AGENT_COUNCIL_GOVERNANCE.md` and
`docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`.

## Construction Gate routing

For work that may enter `gcl/dev/*` or `gcl/candidate/*`, follow
[`docs/governance/CONSTRUCTION_GATE_OPERATING_GUIDE.md`](docs/governance/CONSTRUCTION_GATE_OPERATING_GUIDE.md).

- Do not require the user to know or say `CREATE_DEVELOPMENT`,
  `UPDATE_DEVELOPMENT`, `FREEZE_CANDIDATE`, "advance", or "freeze".
- Keep ordinary drafting and revision on an ordinary working branch. The Gate
  is a one-way admission lane for an exact prepared commit, not the normal
  editing workflow.
- Interpret a request to prepare an exact version for governed or formal review
  as a possible Gate admission. State that interpretation, check whether the
  target is registered on protected `main`, and stop for protected target
  registration when it is not.
- Treat a clear request to lock, finalize, or submit the exact review candidate
  as authorization to attempt `FREEZE_CANDIDATE`. If finality is ambiguous, ask
  before freezing because the candidate cannot be updated or replaced in place.
- Never infer approval, merge authority, mathematical certification,
  publication authority, or external-claim authority from a Gate operation.

## Recoverable diagnostic and tooling failure

For an already authorized bounded MATH operation, follow
[`docs/governance/EXECUTION_RECOVERY_OPERATING_GUIDE.md`](docs/governance/EXECUTION_RECOVERY_OPERATING_GUIDE.md)
when ordinary logs, check surfaces, connectors, compiler diagnostics,
environments, CI, or replay tooling fail.

- Recoverable operational/tooling failure is not by itself an authority
  boundary. Continue through the applicable bounded recovery routes.
- Bind recovery, repair, and replay to the current exact head/run/job/artifact
  whenever those identities matter. Do not patch from stale diagnostics or
  reuse superseded evidence as current evidence.
- Repair only the demonstrated failing theorem/module/validator/scope, then
  require a fresh exact-head replay before relying on the repair.
- If connected diagnostic surfaces remain unavailable, use the guide's
  authenticated local extraction route rather than declaring missing logs a
  terminal blocker.
- Stop or escalate only at a named governance, authority, authentication,
  safety, protected-state, materially changed-state, substantive evidentiary,
  or actual recovery-exhaustion boundary.
- Fail closed on claims, certification, promotion, publication, protected-state
  mutation, and authority; do not fail closed merely on authorized evidence
  gathering and bounded repair.

## Durable bounded-operation continuity

For substantial governed work that can span more than one agent/session or can
wait on CI, review, external evidence, or another asynchronous GitHub surface,
the repository state, not conversational memory, owns the operational resume
point.

- Read `governance/bounded_operation_checkpoint_registry.json` before resuming a
  registered operation. Re-read the named authoritative issue/PR and exact
  material identities before mutation.
- A live checkpoint must validate with
  `ci/validate_bounded_operation_continuity.py`, name one deterministic
  `next_action`, and set `resume.fresh_session_safe=true` and
  `resume.requires_chat_history=false`.
- Update the registered checkpoint after every material transition that changes
  phase, candidate head, external-evidence state, permitted next action, or
  genuine blocking boundary. Git history is the durable transition history.
- Never use a vague `wait` as the resume instruction. If an external object is
  pending, record its exact run/job/review/artifact identity and the exact
  evidence-acquisition action to perform next.
- An agent/session interruption is not a workflow boundary. A fresh agent must
  be able to continue from protected policy plus the registered checkpoint
  without a chat transcript or hand-carried prose summary.
- If a registered exact identity has changed, do not continue from the stale
  checkpoint. Rebind the operation to current authoritative state and record a
  fresh checkpoint before mutation.
- A checkpoint is continuity metadata only. It never grants approval, merge,
  certification, publication, protected bypass, or mathematical-claim
  authority.
