# Agent Council Governance

The Agent Council is the review-governance layer for Grand Challenge MATH-PROGRAMME artifacts.

Every Work Package records council participation through `templates/agent_review.yaml` and is checked against `docs/AGENT_COUNCIL_WORK_PACKAGE_CHECKLIST.md`.

The council preserves separation of concerns:

- Discovery is not proof.
- Computation is not certification.
- Exposition is not evidence.
- Formalization is not understanding.
- Archival provenance is not internal editorial continuity.

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

Promotion requires explicit council review state, unresolved-obligation tracking, a declared route toward MATHCERT, and Amanuensis continuity control.

A Work Package cannot be marked ready for its next stage unless:

1. its artifact-ledger reference and entry ID are present;
2. review provenance is complete;
3. cross-document consistency is reviewed;
4. final editorial integration is reviewed;
5. an authoritative integrated artifact is identified;
6. no promotion blockers remain.
