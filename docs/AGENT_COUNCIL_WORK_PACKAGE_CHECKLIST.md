# Agent Council Work Package Checklist

Every governed Work Package across MATHFORGE, MATHSOLVE, MATHCERT, and MATH-PROGRAMME should carry an Agent Council review record before promotion to its next governed stage. Certification-bound MATHSOLVE packages additionally require an explicit MATHCERT route.

The purpose is not to replace mathematical judgment. The purpose is to make responsibility boundaries explicit: who checked what, what remains unresolved, what changed across revisions, and what prevents promotion.

## Artifact identity

- [ ] Work Package ID assigned.
- [ ] Domain and pillar ownership declared.
- [ ] Stable snake-case artifact type recorded.
- [ ] Canonical lifecycle status recorded.
- [ ] Campaign-specific disposition recorded separately when needed.
- [ ] Claim type recorded.
- [ ] Evidence or certification route identified.

## Council review

- [ ] Axiomatist: carrier object, ambient structure, regularity, and foundation profile reviewed.
- [ ] Prospector: motivation, candidate generalizations, and related structures reviewed.
- [ ] Experimentalist: probes, examples, finite checks, and failed experiments recorded.
- [ ] Cartographer: dependency graph, theorem inventory, and proof ordering reviewed.
- [ ] Verifier: hypotheses, proofs, quantifiers, and edge cases checked.
- [ ] Adversary: counterexamples, hidden assumptions, and failure modes checked.
- [ ] Formalist: formalization boundary and proof artifacts reviewed.
- [ ] Steward: reader contract and motivation reviewed.
- [ ] Composer: segmentation and transitions reviewed.
- [ ] Grammarian: notation and mathematical prose reviewed.
- [ ] Amanuensis: artifact continuity, decision records, terminology, review provenance, consistency, and authoritative integration reviewed.
- [ ] Archivist: prior art, attribution, and external provenance reviewed.
- [ ] Mechanist: implementation and reproducibility path reviewed.
- [ ] Typesetter: presentation and navigation reviewed.
- [ ] Referee: contribution boundary and external objections reviewed.

## Schema and CI binding

- [ ] Current-schema records validate against `schemas/agent_review.schema.json`.
- [ ] A review is added to `SCHEMA_BOUND_AGENT_REVIEWS` only after migration to the complete current schema.
- [ ] Legacy review formats are not described as schema-validated merely because they are committed.
- [ ] Terminal lifecycle states are checked by `ci/validate_documentary_closure.py` even when `promotion.ready_for_next_stage` is false.

## Amanuensis continuity control

- [ ] Artifact-ledger reference recorded.
- [ ] Artifact-ledger entry ID recorded.
- [ ] Relevant decision-record references recorded.
- [ ] Terminology-registry reference recorded when terminology is introduced or changed.
- [ ] Introduced or changed terms listed.
- [ ] Review provenance is complete and evidence references are recorded.
- [ ] Cross-document consistency checked against relevant theorem spines, claim ledgers, Work Packages, schemas, documentation, implementation artifacts, and navigation entries.
- [ ] Conflicts are either resolved or entered as explicit unresolved obligations.
- [ ] Final editorial integration completed after specialist reviews.
- [ ] Authoritative integrated artifact reference recorded.
- [ ] Ledger integration date reflects the most recent material editorial integration.

## Promotion gate

- [ ] No unresolved critical obligations remain.
- [ ] Claim ledger updated when the artifact carries mathematical claims.
- [ ] Evidence route declared.
- [ ] Certification handoff prepared when certification is the next stage.
- [ ] Review provenance marked complete.
- [ ] Cross-document consistency marked reviewed.
- [ ] Final editorial integration marked reviewed.
- [ ] No promotion blockers remain.

## Terminal closure gate

Before using `completed`, `certified`, `published`, or `archived`, or before closing the canonical tracker for the governed work:

- [ ] Operational success and documentary completion have been checked separately.
- [ ] Artifact-ledger identity is present and resolves to the governed artifact.
- [ ] Review provenance is complete and evidence references are nonempty.
- [ ] Cross-document consistency is reviewed and has no unresolved hidden conflict.
- [ ] Final editorial integration is reviewed and names the authoritative artifact.
- [ ] No unresolved blocking documentary obligation remains.
- [ ] The authoritative artifact exists in the protected repository or is explicitly bound to the protected admission being reviewed.
- [ ] If the work does not use a schema-bound Agent Council review, a conforming `closure_contract.json` exists under `governance/rebuild_evidence/<ID>/` and is registered in `governance/governed_closure_registry.json`.
- [ ] If operational work is complete but any documentary item above is incomplete, the documentary obligation remains explicitly open and the work is not described as fully closed.
