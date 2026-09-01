# MP-GOV-DOCUMENTARY-CLOSURE-INTEGRITY-001 — durable governance hardening record

This directory is the authoritative documentary record for MATH-PROGRAMME issue #655.

## Purpose

This operation closes the continuity gap exposed by `MP-ADMIN-LOW-FRICTION-001`: governed work could be operationally complete while its durable documentary package remained incomplete.

The enforced invariant is:

> Governed work is not complete merely because its operational objective succeeded. Terminal completion requires durable artifact continuity, review provenance, cross-document consistency, final editorial integration, applicable ledger/Amanuensis registration, and protected-admission evidence.

## Authority and policy basis

Issue #655 records the Human Steward instruction to make all requisite changes required for documentary integrity and consistency over time. The implementation applies existing Council doctrine in `docs/AGENT_COUNCIL_GOVERNANCE.md` and `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`; it creates no mathematical, certification, publication, bypass, direct-push, ruleset, or external-claim authority.

## Enforced architecture

The protection is layered rather than dependent on memory:

1. Root `AGENTS.md` states documentary completion as a terminal execution invariant.
2. Council governance and the Work Package checklist define the same terminal boundary.
3. Schema-bound Agent Council records cannot use terminal lifecycle states with incomplete Amanuensis continuity.
4. Other governed operations use a registered direct-child `closure_contract.json` under `governance/rebuild_evidence/<ID>/`.
5. Evidence-package discovery is authoritative: every non-legacy package must have a registered closure contract.
6. The sole fixed legacy package is `MP-ADMIN-WORKFLOW-REBUILD-001`; registry-only expansion, baseline deletion, or legacy/contract overlap fails closed.
7. Closure contracts have two distinct phases:
   - `CANDIDATE_AWAITING_PROTECTED_ADMISSION`: no terminal-evidence claim; `protected_pr_admission_and_readback` remains unresolved.
   - `CANONICAL_ON_PROTECTED_MAIN`: exact reviewed head, independent review, successful Programme policy run, protected merge, valid signature, protected-main readback, and terminal receipt are all required and cross-bound.
8. Canonical readback must equal the protected merge; terminal references must contain the exact structured admission identities.
9. `ci/test_documentary_closure.py` adversarially tests omission, legacy drift, premature canonicality, readback mismatch, missing evidence binding, and enforceable ownership.
10. `.github/CODEOWNERS` binds the relevant instruction, governance, schema, validator, and evidence surfaces to requestable Maintainers/Amanuensis ownership, with Security additionally protecting `.github/`.

## Why the second repair was necessary

PR #656 admitted the first hardening implementation at protected merge `93eaa1f035272e1125dcce9e418d89daf6d1ccf5`. A post-merge audit then found that its closure contract said `CANONICAL_ON_PROTECTED_MAIN` while still describing protected admission/readback as future work. The validator checked only that terminal-evidence strings existed; it did not distinguish a candidate continuity record from a genuinely protected canonical closure.

Issue #655 was therefore reopened. PR #658 repaired the model rather than merely editing the stale prose.

## Protected two-phase repair admission

PR #658 is the material repair that established the final two-phase rule.

- exact reviewed head: `e5ec255122a37dbfbe651854ebca8cfb81bfca8b`
- independent APPROVED review: `PRR_kwDOSuWV7M8AAAABKfHXPQ` by `jimsteeg`
- exact-head Programme policy run: `32545953635`, success
- protected merge: `369b0453198cd31411b75375d04f0a08b0be34df`
- merge signature: verified=true, reason=valid
- exact reviewed head is the second merge parent
- protected-main readback: `369b0453198cd31411b75375d04f0a08b0be34df`
- protected admission receipt: issue #655 comment `5379296345`

The material repair was admitted from protected predecessor `fc40dd732116445e17f9cc3fed8e0b62be88bac1`. The independently protected Construction Gate instructions introduced by PR #657 were preserved during synchronization.

## Final readback seal

This final documentary-only seal converts the registered #655 contract from candidate phase to `CANONICAL_ON_PROTECTED_MAIN` using the already-protected #658 evidence above. It changes no validator, schema, policy, runtime, workflow, registry, authority, or operational behavior.

The seal is not a new governed operation requiring recursive self-certification. It is the deterministic recording step authorized by the two-phase model: the protected operational/governance admission already exists, and the seal makes the durable contract state agree with that protected fact.

## Relevant artifacts

- tracker: MATH-PROGRAMME issue #655
- initial hardening admission: PR #656
- material phase-model repair: PR #658
- agent instructions: `AGENTS.md`
- Council policy: `docs/AGENT_COUNCIL_GOVERNANCE.md`
- Council checklist: `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`
- closure-contract schema: `schemas/governed_closure_contract.schema.json`
- closure registry: `governance/governed_closure_registry.json`
- validator: `ci/validate_documentary_closure.py`
- adversarial regressions: `ci/test_documentary_closure.py`
- machine summary: `manifest.json`
- canonical continuity binding: `closure_contract.json`

## Closure state

Documentary state represented by this seal: `CANONICAL_ON_PROTECTED_MAIN`.

No unresolved documentary obligation remains in the registered contract. Once this seal itself is admitted through the ordinary exact-head review and protected PR path, issue #655 may be closed as completed and the final issue comment may record the seal merge/readback for navigational completeness.
