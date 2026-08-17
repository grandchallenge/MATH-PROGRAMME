# OTP-CURRENT-STATE-SYNC-002

Tracker: `MATH-PROGRAMME#538`

## Purpose

Synchronize the Programme-owned navigation state for `OPENAI-TEN-PROOFS-001` to the live protected Forge/Solve/Cert state without rewriting predecessor Programme records or importing execution authority from another repository.

## Protected inputs

- Programme base: `df4e81fb254ccc585c8ffad80a99798507579863`.
- Forge formal-source successor merge: `48e8bf8e0fd157688ae83a8110d63b1e500ee688`.
- Forge successor record blob: `6993ce9fac2c65ffae7f2a0c7d728aab828ed532`.
- Current unresolved-family formal root/tree: `94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6` / `174289e4d4958cb0509874e6e53400e098213de7`.
- Solve main: `7d1f9edf16558ba4c4396126e24fd2c9ae4826f7`.
- Permanent full-formula producer merge: `bebc35818c6d3b79ddc7e348c9bffd328279cd24`.
- Permanent circuit producer merge: `7d1f9edf16558ba4c4396126e24fd2c9ae4826f7`.
- Cert main: `5a69fd897f69cc3871f2138d162fb6ec897ef393`.
- Cert route-registry blob: `2d17473b4731aa9d9c630b1e7777ad4bd794d993`.

## Corrected current state

Restricted qualified Cert surfaces are exactly:

1. `OTP-F-EHRHART` — `qualified_encoded_targets_only`;
2. `OTP-J1-COMPACTNESS` — `qualified_encoded_targets_only`;
3. `OTP-J2-TWO-DEGENERATE` — `qualified_source_faithful_targets_only`;
4. `OTP-C-PERMANENT` variable-leaf formula surface — `qualified_encoded_targets_only`.

The two newer Permanent producer surfaces are protected in Solve but remain independently unrouted in Cert:

- full formula consequences — two targets;
- Theorem 1.1 circuit surface — three targets.

They do not inherit the existing variable-leaf certificate.

## Unresolved-family current-root queue

The protected source successor applies prospectively only to:

- `OTP-A-SPHERE-PACKING`;
- `OTP-B1-BINARY-CODES`;
- `OTP-B2-SPHERICAL-CODES`;
- `OTP-D-NON-SOFIC`;
- `OTP-E-CONNES-RIGIDITY`;
- `OTP-G-QUANTUM-PARALLEL-REPETITION`;
- `OTP-H-GAPCVP`;
- `OTP-I-RAMSEY`.

Execution order remains:

`Sphere Packing + GapCVP`
→ `Binary Codes`
→ `Spherical Codes`
→ `Ramsey`
→ `Quantum Parallel Repetition`
→ `Non-sofic`
→ `Connes Rigidity`.

### Sphere Packing

The exact current-root solution carrier has now been located. `SpherePacking.lean`, blob `e6117934a80142a8249356fdafa797eba030e920`, is a substantive proof-bearing module rather than an empty carrier. It contains the four configured Comparator targets, including the full/radial bridge for the exact limit and binary exponent, the packing upper-bound theorem, and the assembled manuscript-conclusion structure.

Accordingly, Forge #89 is no longer a proof-carrier recovery problem. Its remaining boundary is the explicit source-locus and declaration-level dependency-concordance audit: source theorem/revision, dimensions and normalizations, asymptotic quantifiers, log/exponent conventions, bridge strength, nonvacuity, and target-by-target source relation.

### GapCVP

The exact current-root solution carrier has likewise been located. `GapCVP.lean`, blob `47f3a395e4d9ec3e2892664860f26ed63421b0c9`, is substantive and contains explicit promise-disjointness proofs and the four Comparator-facing NP-hardness theorems. Challenge-side `by sorry` declarations are interface placeholders and must not be read as absence of the solution proofs.

The predecessor's four missing-definition diagnosis remains historical only. The remaining Forge #90 boundary is semantic/reduction/nonvacuity concordance: exact source problem definitions and theorem loci, YES/NO semantics, malformed and out-of-promise behavior, the promise-problem hardness notion, reduction direction/type, dimension-dependent gap-factor transport, finite-`p` scope, and explicit nonvacuity. In particular, `400`, `200`, and `200p` are exponent denominators in dimension/block-length-dependent gap factors rather than constant approximation factors.

B2 target-surface drift and Connes declaration-identity drift remain explicit governed differences, not inferred equivalences.

## Files

- `governance/openai_ten_proofs_current_state_sync_002.json`
- `schemas/openai_ten_proofs_current_state_sync_002.schema.json`
- `governance/validators/openai_ten_proofs_current_state_sync_002.py`
- `tests/test_openai_ten_proofs_current_state_sync_002.py`

## Validation

Required before review:

```text
python governance/validators/openai_ten_proofs_current_state_sync_002.py
python ci/validate_programme.py
python -m unittest discover -s tests -v
git diff --check
```

The mutation suite must reject predecessor-record drift, authority collapse, current-root substitution, restricted-certificate inflation or removal, aggregate output, proof promotion, premature Permanent routing, Sphere/GapCVP state inflation or removal, execution-order drift, and whole-document-equivalence inflation.

## Publication boundary

This branch is a Programme synchronization candidate only. Protected publication requires exact-head Programme/GCL/security checks, fresh non-author approval bound to the exact head, and the repository's normal protected-merge/readback procedure. No review or merge authority is inferred by this work package.

## Claim boundary

This work package does not establish source-semantic equivalence, nonvacuity, mathematical truth, proof correctness, a new Solve handoff, a new MATHCERT route, adjudication, certificate output, aggregate Ten Proofs authority, whole-document equivalence, novelty, priority, publication, patentability, product, or commercial claims.
