# GCL Negative-Knowledge Registry

## Current status

`GCL-NEGATIVE-KNOWLEDGE-WP00` Tranche 1 is `TRANCHE_1_PROTECTED_COMPLETE`.

It completed through PR #206 from reviewed candidate `f440f62506b046784720f072716bdba8c25f5738` and protected merge `b3c092c18fa8d6521a7c49d0663d277487d3c9de`. The historical admission record includes successful hosted checks, delegated review, Human Steward release, and protected merge. Those facts establish the original admission; they are not current generic gates for routine record maintenance.

The protected registry's `active_pilot` state is therefore effective on protected `main` within its bounded tranche.

## Purpose

The negative-knowledge registry preserves bounded failures, obstructions, exhausted searches, counterexamples, and superseded implementation routes as durable institutional records.

It prevents three recurrent errors:

1. a failed route silently returning without its prior blocker;
2. a finite or assumption-dependent negative result being widened into a universal claim;
3. an issue comment being treated as authority after the underlying protected evidence changes.

The protected truth-spine record class is `negative_knowledge_record`. Issue #189 records the Tranche 1 admission.

## Authority

The authoritative pilot is:

```text
negative_knowledge/pilot_registry.json
```

Its closed schema is:

```text
schemas/negative_knowledge_registry.schema.json
```

Validation runs through:

```text
python3 ci/validate_negative_knowledge.py
```

The validator is reached from Programme policy reachability. A repository with no negative-knowledge surface is unaffected. Once any surface component appears, the complete schema, registry, and validator are required; partial adoption fails closed.

Routine semantic-preserving maintenance of the protected pilot uses the standing delegated execution rule and affected checks. A theorem-level refutation, materially widened negative claim, source-semantic change, or other substantive claim-boundary transition still receives the independent specialist review appropriate to that object.

## Record boundary

Every record binds:

- the exact attempted claim or mechanism;
- assumptions and included scope;
- explicitly excluded variants;
- method and execution identity;
- immutable evidence paths, commits, and Git blob identities where applicable;
- result and smallest known witness where applicable;
- what the result does not establish;
- present disposition;
- structured reopening requirements;
- supersession lineage;
- review jurisdiction and claim-boundary fields.

The scope and evidence sections each receive a canonical SHA-256 digest. Changing either section without updating the corresponding digest is rejected.

## Pilot records

### Mathematical route obstruction

`NK-NS-CI-A2-L4-001` records that the Navier–Stokes L4 weighted active-diagonal route is exhausted under its audited interfaces. It does not refute the restricted A2 target, the independent L5 route, or any future route based on a genuinely new PDE theorem.

### Bounded computational exhaustion

`NK-UC-N4-SCREEN-001` records exact exhaustion of the Union-Closed search on universes `n <= 4`, with no violation found. It does not establish Frankl's conjecture for larger universes or universally.

### Superseded systems defect

`NK-GCL-TOOLING-PARTIAL-SURFACE-001` records the exact policy-reachability integration defect found during tooling Tranche 1 and binds its protected repair. It prevents reintroduction of unconditional validation that treats absent and partial control surfaces identically.

## Fail-closed rules

The pilot rejects:

- unknown or duplicate record identities;
- malformed or mutable-only evidence;
- scope or evidence digest drift;
- missing or mismatched reopening triggers;
- broken, self-referential, or cyclic lineage;
- superseded records without an exact successor identity;
- finite-search records widened beyond their finite scope;
- incompatible status and failure-kind combinations;
- silent route reactivation;
- embedded review self-attestation;
- theorem-level refutation without appropriate Referee jurisdiction;
- any mathematical, certification, novelty, priority, publication, patentability, product, or commercial promotion flag.

## Ongoing operating boundary

A protected record remains valid by its material identity; unrelated `main` movement does not require ceremonial repinning or reapproval. A material scope/evidence change is revalidated for the affected closure. Scheduled/manual assurance may replay broader coverage without converting that sentinel into a per-change requirement.

Validation proves only that the registry satisfies its declared contract. It does not prove the recorded mathematical targets, issue certificates, or establish broader impossibility claims.
