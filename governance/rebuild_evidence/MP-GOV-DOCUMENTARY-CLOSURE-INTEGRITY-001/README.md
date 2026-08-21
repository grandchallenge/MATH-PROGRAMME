# MP-GOV-DOCUMENTARY-CLOSURE-INTEGRITY-001 — durable governance hardening record

This directory is the authoritative documentary record for MATH-PROGRAMME issue #655 and PR #656.

## Purpose

The operation closes a continuity gap exposed by `MP-ADMIN-LOW-FRICTION-001`: operational work could be genuinely complete while the repository still lacked the durable documentary package required by standing Council doctrine.

The enforced invariant is:

> Governed work is not complete merely because its operational objective succeeded. Terminal completion requires durable artifact continuity, review provenance, cross-document consistency, final editorial integration, and applicable ledger/Amanuensis registration; otherwise the documentary obligation remains explicitly open.

## Authority and policy basis

Issue #655 records the Human Steward execution instruction to make all requisite changes required for documentary integrity and consistency over time. This operation implements existing Council continuity doctrine in `docs/AGENT_COUNCIL_GOVERNANCE.md` and `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`; it does not create mathematical, certification, publication, bypass, direct-push, or external-claim authority.

## Layered enforcement

The repair deliberately does not rely on one prose reminder.

1. **Agent entry point.** Root `AGENTS.md` now makes documentary closure a terminal execution invariant and points to the canonical Council policy.
2. **Council doctrine.** `docs/AGENT_COUNCIL_GOVERNANCE.md` defines a terminal documentary closure boundary. The checklist contains an explicit terminal closure gate.
3. **Schema-bound Council records.** `ci/validate_documentary_closure.py` treats `completed`, `certified`, `published`, and `archived` as terminal even when `promotion.ready_for_next_stage` is false. It requires complete Amanuensis continuity, core Council review, a resolving ledger entry and authoritative artifact, no hidden consistency conflict, and no blocking obligation.
4. **Other governed operations.** Non-Agent-Council terminal operations use `closure_contract.json` under their evidence package and register it in `governance/governed_closure_registry.json`.
5. **Discovery and drift resistance.** The validator compares discovered closure contracts with the registry, validates contract schemas, resolves ledger entries and authoritative artifacts, verifies consistency-reference paths, and checks that the agent/Council instruction bindings remain present.
6. **CI reachability.** `governance/policy_shard_registry.json` runs the validator and adversarial regression suite in the existing contracts policy shard.
7. **Change ownership.** `.github/CODEOWNERS` binds `AGENTS.md`, Council governance documents, and the documentary-closure validator/tests to Council and Amanuensis review, while governance/schema paths retain their existing Council/Amanuensis ownership.
8. **Self-application.** This hardening operation carries its own evidence package, closure contract, and administrative-ledger registration in PR #656.

## Legacy boundary

The new machine route is prospective rather than a silent reinterpretation of history. Historical artifacts retain their existing governance evidence until individually migrated. Newly completed or materially revised governed work must use one of the two machine-enforced routes.

This mirrors the repository's existing explicit migration boundary for schema-bound Agent Council records.

## Regression cases

`ci/test_documentary_closure.py` exercises at least the following rejection paths:

- a published record with `promotion.ready_for_next_stage: false` but incomplete review provenance;
- missing review-evidence references;
- unresolved cross-document conflicts;
- a missing authoritative integrated artifact;
- a bad artifact-ledger entry;
- a missing consistency reference;
- registry/discovery consistency on the protected candidate tree;
- preservation of nonterminal working states, which may legitimately retain pending continuity while they remain nonterminal.

## Relevant artifacts

- tracker: MATH-PROGRAMME issue #655
- admission PR: MATH-PROGRAMME PR #656
- agent instructions: `AGENTS.md`
- ownership controls: `.github/CODEOWNERS`
- Council policy: `docs/AGENT_COUNCIL_GOVERNANCE.md`
- Council checklist: `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`
- Agent-review semantic description: `schemas/agent_review.schema.yaml`
- governed closure contract schema: `schemas/governed_closure_contract.schema.json`
- governed closure registry schema: `schemas/governed_closure_registry.schema.json`
- closure registry: `governance/governed_closure_registry.json`
- validator: `ci/validate_documentary_closure.py`
- adversarial regressions: `ci/test_documentary_closure.py`
- policy reachability: `governance/policy_shard_registry.json`
- machine summary: `manifest.json`
- terminal continuity binding: `closure_contract.json`

## Admission boundary

This record becomes canonical only through PR #656 after exact-head policy checks, independent non-author review, protected PR-only merge, and protected-main readback. Until then it is candidate documentary evidence on the control branch.
