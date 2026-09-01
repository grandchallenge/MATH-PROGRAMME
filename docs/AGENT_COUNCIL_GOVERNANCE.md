# Agent Council Governance

The Agent Council is the review-governance layer for Grand Challenge MATH-PROGRAMME artifacts.

Every governed Work Package, regardless of pillar, records council participation through an Agent Council review record and is checked against `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`.

The current machine schema is `schemas/agent_review.schema.json`. CI validates only review records explicitly registered in `SCHEMA_BOUND_AGENT_REVIEWS` in `ci/validate_programme.py`. Legacy campaign reviews remain governed evidence, but they are not represented as schema-conformant until migrated and registered.

The council preserves separation of concerns:

- Discovery is not proof.
- Computation is not certification.
- Exposition is not evidence.
- Formalization is not understanding.
- Archival provenance is not internal editorial continuity.

## Review-record scope

The review contract applies across:

- `MATHFORGE` discovery and experimental Work Packages;
- `MATHSOLVE` theorem and reconstruction Work Packages;
- `MATHCERT` certificate and formalization Work Packages;
- `MATH-PROGRAMME` integration, governance, and archival Work Packages.

A record may use the current schema only when its complete field structure has been migrated. CI registration is explicit so that legacy formats cannot be mistaken for validated current-schema records.

## Lifecycle and disposition

A schema-bound review record separates:

- `artifact.status`: a canonical lifecycle token such as `draft`, `active`, `completed`, or `certified`;
- `artifact.disposition`: an optional campaign-specific description such as `referee_promoted_conditional`.

The artifact ledger may retain detailed human-readable dispositions. They do not silently extend the schema's lifecycle vocabulary.

## Issue and tracker housekeeping

A duplicate operational issue must be closed with GitHub `state_reason: duplicate` and must link to the canonical tracker that retains the work. The canonical tracker remains open unless its own success condition is satisfied.

A superseded implementation issue or pull request is not necessarily a duplicate. Close it with the disposition that matches the record, and identify the replacement issue, pull request, Work Package, or governing artifact. Closure must preserve the reason that downstream readers should follow the canonical record rather than the retired one.

## Amanuensis authority

The Amanuensis is the council office responsible for continuity of the programme's own record. It owns the artifact ledger, decision-record references, terminology registry, review provenance, cross-document consistency, and final editorial integration.

Each governed artifact therefore carries an `amanuensis_control` record. This record identifies:

- the artifact-ledger location and entry;
- decision records relevant to the current version;
- the terminology registry and changed terms;
- review-evidence references;
- documents and artifacts checked for consistency;
- unresolved conflicts;
- the authoritative integrated artifact.

The Amanuensis does not certify mathematical truth. It certifies that the reviewed reasoning and obligations have been faithfully carried into the authoritative artifact and that no known blocking conflict has been hidden by revision.

## Terminal documentary closure boundary

Operational success is necessary but not sufficient for governed completion. A canonical tracker, Work Package, governance operation, or archival operation must not be represented as terminal while its required documentary continuity remains incomplete.

Two closure routes are recognized and machine-checked:

1. **Schema-bound Agent Council route.** A Work Package or other schema-bound review record uses `amanuensis_control`. The lifecycle states `completed`, `certified`, `published`, and `archived` are terminal. Those states require the same continuity conditions as promotion even when `promotion.ready_for_next_stage` is false: artifact-ledger identity, complete review provenance, reviewed cross-document consistency, reviewed final editorial integration, an authoritative integrated artifact, no hidden blocking conflict, and no unresolved blocking documentary obligation.
2. **Registered governed-operation route.** A governed operation that does not use a schema-bound Agent Council review must provide `governance/rebuild_evidence/<ID>/closure_contract.json`, validate against `schemas/governed_closure_contract.schema.json`, and register that contract in `governance/governed_closure_registry.json`. The contract records the authoritative artifact, ledger identity, review provenance, consistency review, final editorial integration, authority references, terminal evidence, and unresolved documentary obligations.

The registered governed-operation route has two explicit phases. A contract proposed before protected admission uses `CANDIDATE_AWAITING_PROTECTED_ADMISSION`. Candidate phase carries no terminal-evidence claim and must retain `protected_pr_admission_and_readback` as an unresolved documentary obligation. It may pass CI as a valid candidate continuity record, but it is not terminal documentary closure and must not justify closing the canonical tracker.

After the implementation/evidence PR has passed exact-head checks, independent review, protected merge, signature verification, and protected-main readback, a subsequent readback-seal change may switch the contract to `CANONICAL_ON_PROTECTED_MAIN`. Canonical phase requires `admission.phase=protected` together with the exact reviewed head, independent review ID and reviewer, exact-head Programme policy run, protected merge SHA, verified/valid signature state, protected-main readback, and terminal receipt. The protected-main readback must equal the protected merge, and the contract's terminal-evidence references must bind those exact admission identities.

This two-phase rule prevents a candidate artifact from calling itself canonical merely because it contains prospective text saying that merge or readback will occur later.

`ci/validate_documentary_closure.py` enforces these two routes and the candidate/canonical admission distinction in the contracts policy shard. It rejects unregistered closure contracts, stale registry entries, and any rebuild-evidence package that omits a registered closure contract unless that exact package is in the fixed legacy baseline.

The fixed legacy baseline is deliberately closed rather than extensible by ordinary registry editing. Its exact membership is enforced in code and mirrored in `governance/governed_closure_registry.json`. Adding a new legacy exemption, deleting the required baseline entry, or classifying one package as both legacy and contract-bound is a validation failure. Any intentional change to the baseline is therefore a governance-control change and must pass the same protected review path as the validator itself.

Historical artifacts are not silently reclassified by this rule. Legacy records remain governed by their existing evidence until individually migrated. Any newly created rebuild-evidence package outside the fixed baseline, and any newly completed or materially revised governed work, must use one of the two machine-enforced closure routes before it is described as complete.

If the operational objective has succeeded but documentary closure is incomplete, the correct state is **operationally complete, documentary obligation open**. The canonical tracker or an explicitly linked documentary obligation remains open until the continuity record is admitted and, for the registered governed-operation route, sealed in protected canonical phase.

## Promotion boundary

Promotion requires explicit council review state, unresolved-obligation tracking, a declared evidence or certification route, and Amanuensis continuity control.

A Work Package cannot be marked ready for its next stage unless:

1. its artifact-ledger reference and entry ID are present;
2. review provenance is complete;
3. cross-document consistency is reviewed;
4. final editorial integration is reviewed;
5. an authoritative integrated artifact is identified;
6. no promotion blockers remain.
