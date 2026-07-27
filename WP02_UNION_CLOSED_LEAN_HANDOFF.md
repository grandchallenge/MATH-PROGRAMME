# WP02_UNION_CLOSED_LEAN_HANDOFF.md

## Work Package 02

**Title:** Union-Closed Sets: Lean Handoff and First Checked Lemmas

**Primary type:** FORMALIZATION_HANDOFF

**Claim status:** external MATHCERT substrate implemented and replayed at a pinned commit; no proof of Frankl's conjecture

## 1. Purpose

WP02 translates the Union-Closed Sets status spine into a Lean/equivalent certification plan. The aim is not to prove Frankl's conjecture. The aim is to build a precise formal layer that can support later exact finite certificates and restricted theorem targets.

## 2. Informal-to-formal dictionary

| Informal object | Lean-oriented representation | Notes |
|---|---|---|
| Finite universe `U` | `Finset α` or finite type `[Fintype α]` | Prefer finite type for theorem statements; finite support for examples. |
| Set in the family | `Finset α` | Membership decidable under `[DecidableEq α]`. |
| Family of sets | `Finset (Finset α)` | Natural for finite combinatorics. |
| Union-closed | `∀ A ∈ F, ∀ B ∈ F, A ∪ B ∈ F` | Direct Finset formulation. |
| Frequency of `x` | `(F.filter (fun A => x ∈ A)).card` | Exact cardinality. |
| Nontrivial family | `(support F).Nonempty` | Checked equivalent to `∃ A ∈ F, A.Nonempty`. |
| Frankl-abundant | `∃ x, 2 * freq F x ≥ F.card` | May restrict `x` to support. |
| Frankl conjecture | universally quantified theorem statement | Leave as theorem statement, not proof. |

## 3. Authoritative implementation location

The proof-bearing Lean package and bounded certificate replay are maintained in the separate [`grandchallenge/MATHCERT`](https://github.com/grandchallenge/MATHCERT) repository. They are not local paths in this repository.

The current governed evidence is pinned by [`evidence/UC-WP02-MATHCERT.json`](evidence/UC-WP02-MATHCERT.json) to MATHCERT commit `d59173899dcd1a67dbe8f31de0b9f0917cd1459a`.

```text
MathCert/Domains/UnionClosed/Basic.lean
  Core definitions: family, union-closed, support, nontrivial.

MathCert/Domains/UnionClosed/Frequency.lean
  Frequency function and elementary counting lemmas.

MathCert/Domains/UnionClosed/FranklStatement.lean
  Frankl-abundant and full conjecture statement.

MathCert/Domains/UnionClosed/SingletonCase.lean
  First meaningful checked lemma.

certificates/exact/union_closed_n_le_4.json
  Bounded exact certificate for universes of size at most four.

ci/replay_certificates.py
  Independent bounded certificate replay.

ci/check_lean.sh
  Complete MATHCERT certification gate.
```

## 4. First theorem targets

### Lemma 1: powerset sharpness

For a finite universe `U` and element `x ∈ U`, exactly half of the subsets of `U` contain `x`. This shows the `1/2` bound is sharp.

Certification status: checked in the external MATHCERT package.

### Lemma 2: singleton case

If `F` is union-closed and `{a} ∈ F`, then `a` belongs to at least half of the sets in `F`.

Proof idea: map every set `S` not containing `a` to `S ∪ {a}`. Union-closure ensures the image is in `F`; the image contains `a`; the map is injective because `a ∉ S` allows recovery by deleting `a`.

Certification status: checked in the external MATHCERT package.

### Lemma 3: top union belongs to the family

If `F` is nonempty and union-closed, then the union of all sets in `F` belongs to `F`.

Proof idea: finite induction over the family.

Certification status: checked in the external MATHCERT package.

### Lemma 4: finite certificate replay

An independently implemented MATHCERT replay verifier recomputes all union-closed families for `n <= 4`, verifies the source-audit hash or governed snapshot hash, and checks that every nontrivial family is Frankl-abundant.

Certification status: bounded exact replay in external `grandchallenge/MATHCERT/ci/replay_certificates.py`.

## 5. Trust and repository boundary

The MATH-PROGRAMME policy workflow checks out the exact external MATHCERT commit recorded in `evidence/UC-WP02-MATHCERT.json`, sets up the pinned Lean toolchain, and runs:

```bash
bash ci/check_lean.sh
```

That external gate performs `lake build`, ledger validation, certificate validation, bounded replay, and `sorry` rejection. A moving branch name is not accepted as certification evidence.

## 6. Certification blockers

Resolved substrate obligations:

1. WP02 fixes `Finset (Finset α)` as the local representation.
2. Filtered-family comparisons use explicit injective maps.
3. The bounded certificate schema records convention, counts, version, and hash.
4. MATHCERT independently replays the bounded audit.
5. MATH-PROGRAMME now records and replays the external dependency at an exact commit.

Retained boundary:

- neither the checked local lemmas nor the `n <= 4` replay proves Frankl's conjecture;
- changes in MATHCERT require an explicit evidence-pin update and a fresh MATH-PROGRAMME policy run.

## 7. MATHFORGE dependencies

WP02 depends on exact finite-family enumerator outputs only as test cases. The formal definitions do not depend on Python semantics.

## 8. MATHCERT acceptance criteria

WP02 is accepted as a certification substrate when:

- definitions compile;
- Frankl's conjecture is stated cleanly;
- at least one nontrivial lemma is checked;
- CI rejects every `sorry`;
- a human theorem statement accompanies every Lean theorem;
- the claim ledger distinguishes statements from proofs;
- the external repository and commit are pinned and replayed by programme policy.

## 9. Workflow coverage

The global `Programme policy checks` workflow runs on every pull request, every push to `main`, and manual audit. Its `union-closed-mathcert` job checks out the evidence-pinned MATHCERT commit and executes the complete external certification gate. GitHub Pages deployment is downstream of successful completion of that global policy workflow.

## 10. Next target

The two-element-member special case is checked in the external package. Before beginning original restricted-theorem work, compare the programme representation with the 2025 Lean-verified ideal-family work and choose a chain-constrained or lattice-minimal-counterexample corridor.
