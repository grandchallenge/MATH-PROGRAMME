# 15. Review roles and separation of duties

Roles identify review functions. They do not confer authority without a review record.

| Role | Primary function |
|---|---|
| Owner | Accountable scope, maintenance, and response to findings |
| Steward | Standards selection, impact class, and lifecycle governance |
| Cartographer | Structure, dependency map, navigation, and cross-document integration |
| Grammarian | Controlled language, terminology, notation, and reader clarity |
| Axiomatist | Definitions, assumptions, ambient setting, and source normalization |
| Formalist | Proof structure, formalization boundary, and logical obligations |
| Verifier | Calculations, tests, experiments, implementation, and reproducibility |
| Adversary | Counterexamples, omitted cases, claim inflation, and failure search |
| Amanuensis | Registry, manifests, provenance, terminology records, and review history |
| Referee | Independent final judgment and promotion scope |

One person or agent MAY hold more than one role for IC-0 or IC-1 work. IC-2 and IC-3 artifacts MUST record material role overlap.

For IC-3 artifacts:

- the author MUST NOT be the sole G5 reviewer;
- the authoring team MUST NOT supply the only G6 review;
- the owner MUST NOT be the sole referee;
- the release steward MUST verify the exact promoted revision.

Automated checks MAY satisfy part of a gate. They MUST NOT impersonate an independent human or institutional decision. The review record MUST identify automated and judgment-based checks separately.

# 16. Fail-closed controls

A conforming implementation of this charter MUST block promotion when any of these conditions occurs:

- a required claim ledger is absent or undiscoverable;
- a required review is absent or references another revision;
- an authority status is missing;
- a candidate source is used as authoritative without admission;
- a required exception is absent, expired, or revoked;
- a mandatory metadata field is omitted;
- a public claim has no authoritative source;
- an artifact manifest omits a required governed file;
- a required asset, source record, or static file is orphaned;
- a machine-readable status conflicts with display text;
- a hash or immutable revision does not match the reviewed artifact.

A warning is not sufficient for a fail-closed condition.

# 17. Change control

GCL-TCS-00 uses semantic versioning:

- A major version changes normative meaning or compatibility.
- A minor version adds a backward-compatible requirement, profile, or field.
- A patch version corrects wording, examples, formatting, or an unambiguous defect without changing normative meaning.

Each release MUST include:

- a change log;
- a migration note for changed fields or gate requirements;
- a statement of compatibility;
- the previous and new standard identifiers;
- a review and promotion record.

A project MUST review active exceptions after a major version change.

A superseded standard remains available for provenance. It MUST NOT remain the default for new artifacts unless an approved project annex locks it.

