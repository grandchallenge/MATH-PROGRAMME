# MP-GOV-DOCUMENTARY-CLOSURE-INTEGRITY-001 — durable governance hardening record

This directory is the authoritative documentary record for MATH-PROGRAMME issue #655.

## Purpose

The operation closes a continuity gap exposed by `MP-ADMIN-LOW-FRICTION-001`: operational work could be genuinely complete while the repository still lacked the durable documentary package required by standing Council doctrine.

The enforced invariant is:

> Governed work is not complete merely because its operational objective succeeded. Terminal completion requires durable artifact continuity, review provenance, cross-document consistency, final editorial integration, and applicable ledger/Amanuensis registration; otherwise the documentary obligation remains explicitly open.

## Authority and policy basis

Issue #655 records the Human Steward execution instruction to make all requisite changes required for documentary integrity and consistency over time. This operation implements existing Council continuity doctrine in `docs/AGENT_COUNCIL_GOVERNANCE.md` and `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`; it does not create mathematical, certification, publication, bypass, direct-push, or external-claim authority.

## Layered enforcement

The repair deliberately does not rely on one prose reminder.

1. **Agent entry point.** Root `AGENTS.md` makes documentary closure a terminal execution invariant and points to the canonical Council policy.
2. **Council doctrine.** `docs/AGENT_COUNCIL_GOVERNANCE.md` defines a terminal documentary closure boundary. The checklist contains an explicit terminal closure gate.
3. **Schema-bound Council records.** `ci/validate_documentary_closure.py` treats `completed`, `certified`, `published`, and `archived` as terminal even when `promotion.ready_for_next_stage` is false. It requires complete Amanuensis continuity, core Council review, a resolving ledger entry and authoritative artifact, no hidden consistency conflict, and no blocking obligation.
4. **Other governed operations.** Non-Agent-Council operations use a direct-child `closure_contract.json` under their evidence package and register it in `governance/governed_closure_registry.json`.
5. **Two-phase governed closure.** A contract is first `CANDIDATE_AWAITING_PROTECTED_ADMISSION`; it carries no terminal-evidence claim and retains `protected_pr_admission_and_readback` as an unresolved obligation. Only a subsequent documentary readback seal may use `CANONICAL_ON_PROTECTED_MAIN`, with exact protected admission evidence.
6. **Exact canonical admission binding.** Canonical phase requires the exact reviewed head, independent review ID/reviewer, Programme policy run, protected merge, verified/valid signature, protected-main readback, and terminal receipt. The protected-main readback must equal the protected merge and terminal references must bind those exact identities.
7. **Omission-proof package coverage.** The validator enumerates every direct child of `governance/rebuild_evidence/`. Every package must be covered by a registered direct-child closure contract or by the fixed legacy baseline. A package cannot evade closure merely by omitting `closure_contract.json`.
8. **Fixed legacy baseline.** The sole grandfathered package is `governance/rebuild_evidence/MP-ADMIN-WORKFLOW-REBUILD-001`. Its exact membership is enforced in `ci/validate_documentary_closure.py` and mirrored in the registry. Registry-only expansion, deletion of the baseline entry, or legacy/contract overlap fails closed.
9. **Discovery and drift resistance.** The validator compares discovered closure contracts and evidence packages with the registry, validates schemas, resolves ledger entries and authoritative artifacts, verifies consistency-reference paths, and checks that the agent/Council instruction bindings remain present.
10. **CI reachability.** `governance/policy_shard_registry.json` runs the validator and adversarial regression suite in the existing contracts policy shard.
11. **Enforceable change ownership.** `.github/CODEOWNERS` binds the documentary instruction, governance, schema, validator, and regression surfaces to the requestable MATH-PROGRAMME Maintainers and Amanuensis teams; `.github/` additionally requires Security. The non-requestable `the-council` team is not used as a CODEOWNER.
12. **Self-application.** This hardening operation carries its own evidence package, closure contract, and administrative-ledger registration and remains open while its current contract is in candidate phase.

## Why the two-phase repair was necessary

PR #656 admitted the first hardening implementation at protected merge `93eaa1f035272e1125dcce9e418d89daf6d1ccf5`. Its exact reviewed head was `fb5ff5ce306fd094172b443c1f90d5b00948a976`, independent review `PRR_kwDOSuWV7M8AAAABKfDukg` was APPROVED by `jimsteeg`, Programme policy run `32542868995` succeeded, the merge signature was verified/valid, and protected-main readback matched the merge. Terminal issue comment `5377233642` recorded those facts.

A post-merge audit then found that the protected closure contract still contained prospective language saying readback was required before canonicality, while its binding status already said `CANONICAL_ON_PROTECTED_MAIN`. The validator allowed this because `terminal_evidence_refs` were checked only for presence, not for protected admission semantics.

That finding re-opened #655. The current repair makes candidate and canonical phases distinct and adversarially tests the distinction. Because this repair materially changes the validator and contract schema, its own closure contract is correctly back in candidate phase. The canonical tracker must remain open until this repair is protected and a final documentary-only readback seal records the repair PR's exact admission evidence.

## Legacy boundary

Historical artifacts are not silently reclassified. The only rebuild-evidence exception is the fixed `MP-ADMIN-WORKFLOW-REBUILD-001` baseline that predates the closure-contract mechanism. Every other rebuild-evidence package must carry a registered closure contract. Any intentional baseline change is itself a governance-control change requiring protected review.

## Regression cases

`ci/test_documentary_closure.py` exercises rejection paths including:

- incomplete terminal Agent Council provenance despite a terminal lifecycle state;
- missing or unresolved documentary artifacts and consistency references;
- a newly created evidence package with no closure contract;
- unauthorized legacy-baseline expansion or legacy/contract overlap;
- a canonical contract whose protected-main readback differs from its protected merge;
- canonical terminal references that do not bind the exact review/admission identities;
- a candidate contract attempting to carry terminal evidence;
- a candidate admission object presented under canonical status;
- loss of enforceable Maintainers/Amanuensis/Security CODEOWNERS bindings.

## Relevant artifacts

- tracker: MATH-PROGRAMME issue #655
- protected predecessor admission: MATH-PROGRAMME PR #656
- current material repair: MATH-PROGRAMME PR #658
- agent instructions: `AGENTS.md`
- ownership controls: `.github/CODEOWNERS`
- Council policy: `docs/AGENT_COUNCIL_GOVERNANCE.md`
- Council checklist: `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`
- governed closure contract schema: `schemas/governed_closure_contract.schema.json`
- governed closure registry: `governance/governed_closure_registry.json`
- validator: `ci/validate_documentary_closure.py`
- adversarial regressions: `ci/test_documentary_closure.py`
- policy reachability: `governance/policy_shard_registry.json`
- machine summary: `manifest.json`
- current continuity binding: `closure_contract.json`

## Current admission boundary

Current documentary state: `CANDIDATE_AWAITING_PROTECTED_ADMISSION`.

The material candidate-phase repair in PR #658 must pass exact-head policy/GCL/formal checks, independent non-author review, protected PR-only merge, and signed protected-main readback. A final documentary-only readback seal must then convert `closure_contract.json` to `CANONICAL_ON_PROTECTED_MAIN` using PR #658's exact admission evidence. Until that seal is protected, issue #655 remains open and this work is not described as fully closed.
