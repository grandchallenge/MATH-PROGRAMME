# OPENAI-TEN-PROOFS-WP00 — Governed external-formalization intake

## Status

Candidate-only implementation under Programme issue #198. This work package does not modify the active campaign registry.

## Subject lock

The candidate subject is `openai/ten-proofs` at exact root commit `6fefffdbab0dfa726fcfde6cefae23aa7a1888f3`, tree `79e6a50b1e391bdddb18b42be3e886c1d9784ed3`.

The deterministic source archive recorded by MATHFORGE has SHA-256 `630e10ec7f8b08ce3416fba967e6d1e4c7599677e38fd4af24fc0c68a9a5bac2`. MATHFORGE pull request #36 reviewed head `f4283c59571a43be23d07700b4cfddafc2bcda8d` is protected at merge commit `89f3853f697450261cb76a638b5282c3bfa96770`; the Programme intake pins that merge and the Git blob identities of its provider manifest, source lock, theorem matrix, and provider-coverage registry.

## Admission unit

The upstream repository groups its material into ten lettered packages but advertises twelve main-result families. GCL admission is result-family-specific. Neither an aggregate build nor upstream branding can admit the corpus as one object.

## Orthogonal gates

1. **Source identity** establishes the exact external bytes and dependency identities.
2. **Kernel correctness** requires a trusted exact-head build, all declared Comparator checks, and theorem-level axiom reports.
3. **Statement fidelity** requires source-paper, theorem-revision, Lean-declaration, and Comparator-target concordance plus nonvacuity review.
4. **Independent adjudication** belongs exclusively to MATHCERT and occurs per result family.

A positive disposition at one gate does not imply a positive disposition at another.

## Current evidence

- Exact Git identity and deterministic archive identity are independently reproduced.
- The source-identity gate is provider-verified at the protected Forge merge; this does not satisfy any other gate.
- The textual solution-source scan outside the challenge modules found no `sorry`, `admit`, custom `axiom`, `unsafe`, or `opaque` declarations.
- Upstream `formalization.yaml` has `sources: []` and records only `agent-reviewed` status.
- Default `lake build` fails because `defaultTargets` names undeclared target `ConnesRigidity2`.
- The Comparator library roots name missing module `ComparatorChallenges.C_PermanentSuperquadraticStandalone`.
- Trusted elaboration, Comparator replay, and theorem-level axiom reports are incomplete.

The scan result is reconnaissance only. Textual absence of proof holes is not kernel verification.

## Governed route

- MATHFORGE #35 and merged PR #36 own the protected source lock, provider manifest, and twelve-result intake matrix.
- MATHSOLVE #90 is blocked and may not open or emit a result-level handoff before trusted Lean/Comparator replay and source-theorem acquisition for that result family.
- MATHCERT #43 remains `pre_route_candidate`, with `may_adjudicate: false` and `cert_output: null`.

## Promotion boundary

No mathematical, source-equivalence, novelty, priority, patentability, mechanical, manufacturing, or commercial claim is promoted. Passing CI on a GCL governance proposal would validate that proposal's structure, not any upstream theorem.
