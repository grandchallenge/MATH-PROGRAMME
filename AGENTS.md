# Agent instructions

MATH-PROGRAMME owns mathematics-specific policy and pins adopted
cross-programme standards. Agents may propose changes by branch and pull
request, but may not approve or merge their own work, write to protected
branches, or promote a mathematical claim.

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
