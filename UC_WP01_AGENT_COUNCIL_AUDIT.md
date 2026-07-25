# UC_WP01_AGENT_COUNCIL_AUDIT.md

## Purpose

This is the first operational test of the MATH-PROGRAMME Agent Council against a real mathematical campaign artifact.

The test is deliberately narrow: govern `WP01_UNION_CLOSED_STATUS_SPINE.md` without rewriting its mathematics, duplicating its claim ledger, or creating ceremonial review work.

## Pilot verdict

WP01 is fit as a completed status spine and certification entry point. It is not a theorem package and does not support any claim that Frankl's conjecture is close to resolution.

The governing review record is:

`reviews/union_closed/UC-WP01.agent_review.yaml`

The governing dependency graph is:

`reviews/union_closed/UC-WP01.dependency_dag.yaml`

The pilot decision is `ADR-0002`. The post-pilot contract normalization and consistency repair is `ADR-0007`.

## Axiomatist profile

```yaml
foundational_profile:
  carrier_type: finite
  ambient_structure:
    - set_system
    - finite_combinatorial_structure
    - computable_presentation
  regularity:
    - finite
    - decidable
    - computable
  axiom_profile:
    base: finite
    choice_usage: none
    excluded_middle: local
    large_cardinal_usage: none
    determinacy_usage: none
  witness_policy:
    existence_claim: explicit_witness
    witness_location: certificate_artifact
  certification_target:
    - Lean
    - exact_replay
    - human_audit
  pathology_risk:
    level: low
    notes: The main risk is semantic ambiguity or combinatorial overclaiming, not set-theoretic pathology.
```

The nontriviality convention is binding: the family has nonempty support, equivalently at least one nonempty member.

## Cartographer dependency graph

The critical path is:

```text
finite definitions
  -> nontriviality convention
  -> Frankl target statement
  -> bounded computation contract
  -> exact n <= 4 enumeration
  -> independent MATHCERT replay
  -> typed claim ledger
  -> WP02 formalization handoff
```

The source-status audit is a parallel dependency into the claim ledger. It does not certify the conjecture or the bounded computation.

The path through WP02 is discharged. Later WP04 and WP05 work is downstream of this baseline and does not retroactively turn WP01 into a theorem package.

## Verifier obligations

The Verifier accepts only the following claims from WP01:

1. The conjecture is stated under an explicit finite nontriviality convention.
2. The package claims no new theorem.
3. The `n <= 4` result is exact, bounded, and independently replayed.
4. Raw family counts and Frankl-facing nontrivial counts remain distinct.
5. Any larger finite range requires a new source artifact, replay artifact, hash, ledger entry, and review record.

The Verifier does not infer general evidence from the absence of bounded counterexamples.

## Adversary failure register

| Failure mode | Rejection rule |
|---|---|
| False simplicity | Reject any averaging proof that does not expose where union-closure enforces the claimed frequency inequality. |
| Finite-range overreach | Reject any general statement inferred from enumeration on bounded universes. |
| Constant-bound inflation | Reject language treating a lower bound below `1/2` as equivalent to, or nearly proving, the conjecture. |
| Convention drift | Reject counts or claims that change the empty-family or nonempty-support convention without a new ledger entry. |
| Representation drift | Reject transfer between finite-set and lattice formulations without an explicit correspondence argument. |
| Source freshness failure | Reject date-sensitive status language that has not undergone a current literature refresh. |
| Temporal handoff drift | Reject baseline language that presents a completed downstream handoff as future work. |
| CI-scope inflation | Reject language claiming schema validation for legacy review records not registered in `SCHEMA_BOUND_AGENT_REVIEWS`. |

## Formalist boundary

WP01 authorizes the following formal work:

- Lean definitions for finite set families, union-closure, support, frequency, nontriviality, abundance, and the conjecture statement;
- checked elementary lemmas such as powerset sharpness, top-union membership, and the singleton case;
- independently replayed exact certificates for bounded finite audits.

WP01 does not authorize a formal claim of the full conjecture, nor does it treat Python output as kernel-checked proof.

The authorized WP02 substrate and local lemmas have been implemented. Their status is governed by WP02 and MATHCERT artifacts.

## Amanuensis continuity record

Authoritative integrated artifact:

`WP01_UNION_CLOSED_STATUS_SPINE.md`

Continuity bundle:

```text
WP01_UNION_CLOSED_STATUS_SPINE.md
UC_WP01_AGENT_COUNCIL_AUDIT.md
reviews/union_closed/UC-WP01.agent_review.yaml
reviews/union_closed/UC-WP01.dependency_dag.yaml
templates/union_closed_claim_ledger_wp01.yaml
DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md
WP02_UNION_CLOSED_LEAN_HANDOFF.md
docs/AGENT_COUNCIL_ARTIFACT_LEDGER.md
docs/AGENT_COUNCIL_DECISION_RECORDS.md
docs/decisions/ADR-0002_UNION_CLOSED_AGENT_COUNCIL_PILOT.md
docs/decisions/ADR-0007_AGENT_COUNCIL_CONTRACT_NORMALIZATION.md
schemas/agent_review.schema.json
schemas/agent_review.schema.yaml
ci/validate_programme.py
ci/test_validate_programme.py
mkdocs.yml
```

The Agent Council artifact ledger identifies `UC-WP01`. ADR-0002 records why this campaign was selected as the first council pilot and how review overhead is bounded. ADR-0007 records the subsequent decision-storage, schema-scope, lifecycle, and temporal consistency repairs.

## Referee acceptance criteria

WP01 is acceptable only when a reviewer can verify that:

1. the object and nontriviality convention are precise;
2. the general conjecture is clearly marked open;
3. every claim is typed by support route;
4. the bounded audit is reproducible and independently replayed;
5. false-proof and overclaiming risks are explicit;
6. the formalization boundary is concrete;
7. unresolved obligations are visible;
8. downstream packages consume named dependencies rather than narrative momentum;
9. completed downstream work is not described as future work;
10. CI scope is stated as explicit schema binding rather than repository-wide inference.

## Anti-bureaucracy budget

The council pilot is constrained by four rules:

1. The review record references proofs, ledgers, and certificates; it does not copy them.
2. The dependency DAG contains only nodes needed to explain promotion.
3. Nonblocking obligations remain visible without preventing useful work.
4. New review artifacts are required only when mathematical status, dependency structure, representation, promotion state, or governing contract materially changes.

The measure of success is not document count. It is whether a reader or agent can identify the exact claim boundary, current debt, and next permitted move without reconstructing the campaign from repository history.

## 2026-07-24 consistency disposition

The post-merge audit found and repaired stale ADR reservation language, overstated CI scope, mixed ADR storage, schema/checklist scope mismatch, stale WP01 temporal language, obsolete handoff paths, and incomplete consistency evidence. After those repairs, the review record may retain `cross_document_consistency.status: reviewed` and `conflicts: []`.
