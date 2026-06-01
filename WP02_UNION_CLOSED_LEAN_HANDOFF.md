# WP02_UNION_CLOSED_LEAN_HANDOFF.md

## Work Package 02

**Title:** Union-Closed Sets: Lean Handoff and First Checked Lemmas

**Primary type:** FORMALIZATION_HANDOFF

**Claim status:** WP02 substrate implemented; local lemmas require CI replay in each environment

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

## 3. Implemented Lean files

```text
MathCert/Domains/UnionClosed/Basic.lean
  Core definitions: family, union-closed, support, nontrivial.

MathCert/Domains/UnionClosed/Frequency.lean
  Frequency function and elementary counting lemmas.

MathCert/Domains/UnionClosed/FranklStatement.lean
  Frankl-abundant and full conjecture statement.

MathCert/Domains/UnionClosed/SingletonCase.lean
  First meaningful checked lemma.

MATHCERT/ci/replay_certificates.py
  Independent bounded certificate replay for finite ledgers.
```

## 4. First theorem targets

### Lemma 1: powerset sharpness

For a finite universe `U` and element `x ∈ U`, exactly half of the subsets of `U` contain `x`. This shows the `1/2` bound is sharp.

Certification status: checked as `UC-WP02-L004`.

### Lemma 2: singleton case

If `F` is union-closed and `{a} ∈ F`, then `a` belongs to at least half of the sets in `F`.

Proof idea: map every set `S` not containing `a` to `S ∪ {a}`. Union-closure ensures the image is in `F`; the image contains `a`; the map is injective because `a ∉ S` allows recovery by deleting `a`.

Certification status: checked as `UC-WP02-L002` and promoted to abundance witness `UC-WP02-L006`.

### Lemma 3: top union belongs to the family

If `F` is nonempty and union-closed, then the union of all sets in `F` belongs to `F`.

Proof idea: finite induction over the family.

Certification status: checked as `UC-WP02-L003`.

### Lemma 4: finite certificate replay

An independently implemented MATHCERT replay verifier recomputes all union-closed families for `n <= 4`, verifies the source audit hash, and checks that every nontrivial family is Frankl-abundant.

Certification status: implemented as bounded exact replay in `MATHCERT/ci/replay_certificates.py`.

## 5. Lean scaffold

The checked formal layer is included in:

```text
MATHCERT/MathCert/Domains/UnionClosed/Basic.lean
MATHCERT/MathCert/Domains/UnionClosed/FranklStatement.lean
MATHCERT/MathCert/Domains/UnionClosed/SingletonCase.lean
```

The initial singleton placeholder has been replaced by a checked injection proof. CI rejects any reintroduced `sorry`.

## 6. Certification blockers

Resolved blockers:

1. WP02 fixes `Finset (Finset α)` as the local representation.
2. Filtered-family comparisons use explicit injective maps.
3. The bounded certificate schema records convention, counts, version, and hash.
4. MATHCERT independently replays the Python-generated bounded audit.

## 7. MATHFORGE dependencies

WP02 depends on exact finite-family enumerator outputs only as test cases. The formal definitions should not depend on Python semantics.

## 8. MATHCERT acceptance criteria

WP02 is accepted when:

- definitions compile;
- Frankl's conjecture is stated cleanly;
- at least one nontrivial lemma is checked;
- CI rejects every `sorry`;
- a human theorem statement accompanies every Lean theorem;
- the claim ledger distinguishes statements from proofs.

## 9. First CI target

A CI job runs:

```bash
lake build
python3 ci/validate_ledgers.py
python3 ci/test_validate_ledgers.py
python3 ci/replay_certificates.py
python3 ci/check_sorries.py
```

If Lean is not available, the CI should fail honestly rather than marking formal claims checked.

## 10. Next target

The two-element-member special case is checked in `TwoElementCase.lean`. Before beginning original restricted-theorem work, compare the programme representation with the 2025 Lean-verified ideal-family work and choose a chain-constrained or lattice-minimal-counterexample corridor.
