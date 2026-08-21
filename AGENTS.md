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

Do not close a canonical tracker while a required documentary obligation is
missing. If operational work is complete but documentary closure is not, keep
the documentary obligation explicitly open.

Historical artifacts are not silently reclassified. Newly completed or
materially revised governed work must use one of the two closure routes above.

Canonical policy: `docs/AGENT_COUNCIL_GOVERNANCE.md` and
`docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`.
