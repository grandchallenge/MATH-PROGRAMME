# Agent Council Governance

The Agent Council is the review-governance layer for Grand Challenge MATH-PROGRAMME artifacts. Its offices define responsibility and evidentiary jurisdiction; they are not a requirement to collect every office's approval on every routine transaction.

Current execution is subject to `MP-STREAMLINED-EXECUTION-001`. Routine bounded administrative, documentation, engineering, workflow, maintenance, routing, synchronization, and campaign-execution work proceeds under standing delegated authority after affected checks pass. Specialist non-author review is reserved for substantive mathematical certification, source-semantic adjudication, constitutional authority expansion, security-sensitive protection weakening, and external claim promotion.

The current machine schema is `schemas/agent_review.schema.json`. CI validates only review records explicitly registered in `SCHEMA_BOUND_AGENT_REVIEWS` in `ci/validate_programme.py`. Legacy campaign reviews remain governed evidence, but they are not represented as schema-conformant until migrated and registered.

The council preserves separation of concerns:

- Discovery is not proof.
- Computation is not certification.
- Exposition is not evidence.
- Formalization is not understanding.
- Archival provenance is not internal editorial continuity.
- Review jurisdiction is not universal approval authority.

## Review-record scope

The review contract can apply across:

- `MATHFORGE` discovery and experimental Work Packages;
- `MATHSOLVE` theorem and reconstruction Work Packages;
- `MATHCERT` certificate and formalization Work Packages;
- `MATH-PROGRAMME` integration, governance, and archival Work Packages.

A record may use the current schema only when its complete field structure has been migrated. CI registration is explicit so that legacy formats cannot be mistaken for validated current-schema records.

The material boundary determines which offices are required. A mathematical certification package may require Verifier, Formalist, Adversary, Referee, and MATHCERT-specific separation. A routine documentation correction generally does not. Review evidence should be complete for the offices that actually have jurisdiction; completeness does not mean ceremonial participation by every named office.

## Lifecycle and disposition

A schema-bound review record separates:

- `artifact.status`: a canonical lifecycle token such as `draft`, `active`, `completed`, or `certified`;
- `artifact.disposition`: an optional campaign-specific description such as `referee_promoted_conditional`.

The artifact ledger may retain detailed human-readable dispositions. They do not silently extend the schema's lifecycle vocabulary.

## Issue and tracker housekeeping

A duplicate operational issue must be closed with GitHub `state_reason: duplicate` and must link to the canonical tracker that retains the work. The canonical tracker remains open unless its own success condition is satisfied.

A superseded implementation issue or pull request is not necessarily a duplicate. Close it with the disposition that matches the record, and identify the replacement issue, pull request, Work Package, or governing artifact. Closure must preserve the reason that downstream readers should follow the canonical record rather than the retired one.

Issue and PR text are navigation surfaces. They do not become authoritative merely because protected records have moved, and they do not force branch synchronization merely to keep a numerical head current.

## Amanuensis authority

The Amanuensis is the council office responsible for continuity of the programme's own record. It owns the artifact ledger, decision-record references, terminology registry, review provenance, cross-document consistency, and final editorial integration.

Where an artifact uses `amanuensis_control`, the record identifies:

- the artifact-ledger location and entry;
- decision records relevant to the current version;
- the terminology registry and changed terms;
- applicable review-evidence references;
- documents and artifacts checked for consistency;
- unresolved conflicts;
- the authoritative integrated artifact.

The Amanuensis does not certify mathematical truth. It certifies that the relevant reasoning and obligations have been faithfully carried into the authoritative artifact and that no known blocking conflict has been hidden by revision.

## Terminal documentary closure boundary

Operational success and documentary completion are separate facts. A canonical tracker, Work Package, governance operation, or archival operation must not be represented as terminal while a genuinely applicable documentary continuity obligation remains incomplete.

Two machine-checked closure routes exist:

1. **Schema-bound Agent Council route.** A Work Package or other schema-bound review record uses `amanuensis_control`. Terminal lifecycle states require artifact-ledger identity, applicable review provenance, reviewed cross-document consistency, reviewed final editorial integration, an authoritative integrated artifact, no hidden blocking conflict, and no unresolved blocking documentary obligation.
2. **Registered governed-operation route.** A governed operation explicitly registered under the documentary-closure control provides `governance/rebuild_evidence/<ID>/closure_contract.json`, validates against `schemas/governed_closure_contract.schema.json`, and registers that contract in `governance/governed_closure_registry.json`.

The registered governed-operation route has candidate and protected-canonical phases. Candidate phase uses `CANDIDATE_AWAITING_PROTECTED_ADMISSION`, carries no terminal-evidence claim, and keeps `protected_pr_admission_and_readback` unresolved. Protected canonical phase uses `CANONICAL_ON_PROTECTED_MAIN` only after the exact machine contract for that route is satisfied.

Some existing closure schemas preserve historical fields such as `exact_reviewed_head`, `independent_review_id`, and `independent_reviewer`. Those fields are requirements of that registered machine contract until the control itself is changed; they are not a general requirement that all routine work obtain fresh independent review or reapproval. `MP-STREAMLINED-EXECUTION-001` controls the general routine execution rule.

A protected readback establishes that the admitted result exists on protected state. It does not create a second approval cycle. If a dedicated closure contract requires a separate readback seal, that is a route-specific documentary operation and should remain bounded to the exact closure record rather than being generalized to unrelated work.

`ci/validate_documentary_closure.py` enforces the registered routes and the fixed legacy baseline. Historical artifacts are not silently reclassified. Any newly created rebuild-evidence package outside the fixed baseline, and any newly completed or materially revised governed work that is actually in scope for that control, must satisfy its applicable closure route before being described as complete.

If the operational objective has succeeded but documentary closure is incomplete, the correct state is **operationally complete, documentary obligation open**.

## Review proportionality and evidence identity

Reviews and checks bind to their material subject, not indiscriminately to repository-head freshness.

- Unrelated movement of protected `main` does not invalidate review evidence.
- Byte-identical synchronization or an unrelated campaign transition does not require a new review.
- A changed material object, relevant dependency, authority boundary, or claim scope does require renewed validation or specialist review for the affected closure.
- Routine bounded work does not receive a generic Referee or Human Steward gate.
- Mathematical independence cannot be manufactured by relabeling the same authoring actor as a specialist reviewer.

## Promotion boundary

Promotion requires the evidence, review, and authority appropriate to the claim being promoted. For mathematical or certification promotion, this can include explicit specialist review, unresolved-obligation tracking, a declared evidence or certification route, and Amanuensis continuity control. For routine administrative integration, the standing delegated sequence is sufficient when the work remains within authorized scope and affected protected checks pass.

No review record, workflow success, issue comment, or delegated administrative disposition can by itself promote a mathematical claim beyond its declared support route.
