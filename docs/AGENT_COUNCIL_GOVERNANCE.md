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

## Promotion boundary

Promotion requires explicit council review state, unresolved-obligation tracking, a declared evidence or certification route, and Amanuensis continuity control.

A Work Package cannot be marked ready for its next stage unless:

1. its artifact-ledger reference and entry ID are present;
2. review provenance is complete;
3. cross-document consistency is reviewed;
4. final editorial integration is reviewed;
5. an authoritative integrated artifact is identified;
6. no promotion blockers remain.
