# Agent Council Work Package Checklist

Use this checklist to make responsibility boundaries explicit: who checked what, what remains unresolved, what changed across revisions, and what prevents promotion. Apply Council offices according to the material boundary of the artifact; this is not a requirement to obtain every office's approval for every routine transaction.

`MP-STREAMLINED-EXECUTION-001` controls routine execution. Bounded administrative, documentation, engineering, workflow, maintenance, routing, synchronization, and campaign-execution work does not require a fresh Human Steward or generic independent-review approval when standing delegation covers the action and affected protected checks pass. Specialist non-author review remains reserved for substantive mathematical certification, source-semantic adjudication, constitutional authority expansion, security-sensitive protection weakening, and external claim promotion.

Certification-bound MATHSOLVE packages additionally require an explicit MATHCERT route.

## Artifact identity

- [ ] Work Package or governed artifact ID assigned where applicable.
- [ ] Domain and pillar ownership declared.
- [ ] Stable artifact type recorded.
- [ ] Canonical lifecycle status recorded.
- [ ] Campaign-specific disposition recorded separately when needed.
- [ ] Claim type recorded.
- [ ] Evidence or certification route identified.
- [ ] Material evidence closure identified well enough to determine affected checks and review jurisdiction.

## Council review — apply by jurisdiction

The following are review responsibilities, not a universal approval quorum. Mark an office applicable, not applicable, or satisfied by retained evidence as the governing contract permits.

- [ ] Axiomatist: carrier object, ambient structure, regularity, and foundation profile reviewed when foundational assumptions are material.
- [ ] Prospector: motivation, candidate generalizations, and related structures reviewed when discovery is material.
- [ ] Experimentalist: probes, examples, finite checks, and failed experiments recorded when computation is material.
- [ ] Cartographer: dependency graph, theorem inventory, and proof ordering reviewed when dependency structure is material.
- [ ] Verifier: hypotheses, proofs, quantifiers, and edge cases checked for mathematical claims.
- [ ] Adversary: counterexamples, hidden assumptions, and failure modes checked where claim or control risk warrants it.
- [ ] Formalist: formalization boundary and proof artifacts reviewed where formal evidence is claimed.
- [ ] Steward: reader contract and motivation reviewed where exposition is material.
- [ ] Composer: segmentation and transitions reviewed where editorial structure is material.
- [ ] Grammarian: notation and mathematical prose reviewed where language affects interpretation.
- [ ] Amanuensis: artifact continuity, decisions, terminology, applicable review provenance, consistency, and authoritative integration reviewed where continuity control applies.
- [ ] Archivist: prior art, attribution, and external provenance reviewed where provenance is material.
- [ ] Mechanist: implementation and reproducibility path reviewed where executable artifacts are material.
- [ ] Typesetter: presentation and navigation reviewed where publication presentation is material.
- [ ] Referee: independent specialist review completed only where the governing boundary requires it.

## Schema and CI binding

- [ ] Current-schema records validate against `schemas/agent_review.schema.json`.
- [ ] A review is added to `SCHEMA_BOUND_AGENT_REVIEWS` only after migration to the complete current schema.
- [ ] Legacy review formats are not described as schema-validated merely because they are committed.
- [ ] CI selection follows `ci/policy_impact.py` and `governance/policy_shard_registry.json`; `validate-json` is the aggregate context, not evidence that every shard ran.
- [ ] Expensive formal or computational replay is required only when the material closure invalidates it, on explicit dispatch, or on scheduled assurance; protected evidence reuse remains valid when its material identity is unchanged.
- [ ] Terminal lifecycle states are checked by `ci/validate_documentary_closure.py` where that control applies, even when `promotion.ready_for_next_stage` is false.

## Bounded-operation continuity gate

Use this gate only when the campaign is explicitly admitted in the registry.
Do not apply it to routine pull requests, ordinary CI waits, bounded repairs, or
ordinary drafting:

- [ ] The operation has a checkpoint registered in `governance/bounded_operation_checkpoint_registry.json`.
- [ ] The checkpoint validates with `ci/validate_bounded_operation_continuity.py`.
- [ ] Its recorded `freshness.verification_command` succeeds immediately before a permitted transition.
- [ ] Exact protected base and current candidate head are recorded when applicable.
- [ ] The current terminal condition is explicit and does not depend on conversational interpretation.
- [ ] `permitted_next_actions` are finite and the checkpoint names exactly one deterministic `next_action` while nonterminal.
- [ ] `resume.fresh_session_safe` is true and `resume.requires_chat_history` is false.
- [ ] Authoritative resume sources are repository/GitHub records, not a chat transcript or hand-carried summary.
- [ ] Pending external evidence names exact run/job/review/artifact/source identities and the next evidence-acquisition action; a vague `wait` is not used.
- [ ] A blocked operation uses only a recognized genuine boundary category and records the exact evidence for that boundary.
- [ ] The checkpoint is updated after a material phase, exact-head, external-evidence, next-action, or boundary transition.
- [ ] If an exact identity no longer matches, the operation is rebound before mutation; stale checkpoint evidence is not reused as current evidence.
- [ ] The checkpoint grants no merge, approval, certification, publication, protected-bypass, or mathematical-claim authority.

## Amanuensis continuity control

- [ ] Artifact-ledger reference recorded where the artifact class requires one.
- [ ] Artifact-ledger entry ID recorded.
- [ ] Relevant decision-record references recorded.
- [ ] Terminology-registry reference recorded when terminology is introduced or changed.
- [ ] Introduced or changed terms listed.
- [ ] Applicable review provenance is complete and evidence references are recorded.
- [ ] Cross-document consistency checked against materially relevant theorem spines, claim ledgers, Work Packages, schemas, documentation, implementation artifacts, and navigation entries.
- [ ] Conflicts are either resolved or entered as explicit unresolved obligations.
- [ ] Final editorial integration completed when required.
- [ ] Authoritative integrated artifact reference recorded.
- [ ] Ledger integration date reflects the most recent material editorial integration.

## Promotion gate

For a substantive promotion:

- [ ] No unresolved critical obligations remain.
- [ ] Claim ledger updated when the artifact carries mathematical claims.
- [ ] Evidence route declared.
- [ ] Certification handoff prepared when certification is the next stage.
- [ ] Required specialist review provenance is complete.
- [ ] Cross-document consistency is reviewed.
- [ ] Final editorial integration is reviewed where applicable.
- [ ] No promotion blockers remain.

For routine bounded integration without claim promotion, use the standing sequence:

`classify material closure -> run affected checks -> delegated disposition -> protected merge -> protected readback`.

Do not add an independent-review or Human Steward gate merely because a routine artifact received a new commit or protected `main` advanced.

## Terminal closure gate

Before using `completed`, `certified`, `published`, or `archived`, or before closing the canonical tracker for governed work:

- [ ] Operational success and documentary completion have been checked separately.
- [ ] Artifact-ledger identity is present where required and resolves to the governed artifact.
- [ ] Applicable review provenance is complete and evidence references are nonempty.
- [ ] Cross-document consistency has no unresolved hidden conflict.
- [ ] Final editorial integration names the authoritative artifact where required.
- [ ] No unresolved blocking documentary obligation remains.
- [ ] The authoritative artifact exists in the protected repository or is explicitly bound to the protected admission being reviewed.
- [ ] If the work is registered under the general documentary-closure control rather than a schema-bound Agent Council review, a conforming `closure_contract.json` exists under `governance/rebuild_evidence/<ID>/` and is registered in `governance/governed_closure_registry.json`.
- [ ] Before protected admission, that route-specific contract is `CANDIDATE_AWAITING_PROTECTED_ADMISSION`, contains no terminal-evidence claim, and keeps `protected_pr_admission_and_readback` explicitly unresolved.
- [ ] A contract is changed to `CANONICAL_ON_PROTECTED_MAIN` only when its current machine schema is satisfied and protected readback exists.
- [ ] Existing route-specific fields such as `exact_reviewed_head` and `independent_review_*` are treated as requirements of that registered closure contract, not as generic requirements for all routine programme work.
- [ ] Protected readback is not treated as a second approval cycle.
- [ ] A newly created rebuild-evidence package is not treated as legacy merely because its closure contract is absent. The only legacy exemption is the fixed baseline enforced by `ci/validate_documentary_closure.py`.
- [ ] Registry and filesystem agree: no unregistered contract, stale contract registration, uncontracted non-legacy evidence package, unauthorized legacy exemption, missing fixed baseline entry, or legacy/contract overlap remains.
- [ ] If operational work is complete but a genuinely applicable documentary item remains incomplete, the documentary obligation remains explicitly open.
