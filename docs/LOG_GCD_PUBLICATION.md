# The logarithmic GCD kernel

<p class="page-deck">A certified arithmetic kernel, an explicit finite feature map, and a publication boundary that distinguishes a new formal artifact from classical mathematics.</p>

## Publication record

| Field | Status |
| --- | --- |
| Publication ID | `PUB-LOG-GCD-001` |
| Publication status | **CANDIDATE** |
| Mathematical status | Classical result; mathematical novelty **not claimed** |
| Formal status | Lean declarations **CERTIFIED** by pinned repository-native replay |
| Public claim | Positive semidefiniteness and exact divisor-feature Gram identity |
| Inputs | Positive natural numbers; the feature theorem is stated for nonzero naturals |
| Priority | First-proof and first-formalization priority **not claimed** |
| Strictness | Positive semidefinite, not strictly positive definite on the full domain |

> A GCL-certified Lean formalization and explicit `Finsupp` realization of a classical GCD-matrix positivity criterion.

## The claim

For positive natural numbers, define

```text
K(m,n) = log(gcd(m,n)).
```

For every finite family `xᵢ` and every real coefficient family `cᵢ`,

```text
Σᵢ Σⱼ cᵢ cⱼ K(xᵢ,xⱼ) ≥ 0.
```

Equivalently, every finite matrix with entries `log(gcd(xᵢ,xⱼ))` is positive semidefinite. The certified Lean declaration is `logGcd_posSemidef`.

The companion feature theorem makes the Gram representation explicit. Define

```text
φ(n)_d = sqrt(Λ(d)) when d divides n,
         0            otherwise,
```

where `Λ` is the von Mangoldt function. Lean represents `φ(n)` as a finitely supported function `ℕ →₀ ℝ` and certifies

```lean
finsuppDot (logGcdFeature m) (logGcdFeature n)
  = Real.log (Nat.gcd m n)
```

for nonzero `m,n`. The declaration is `logGcd_eq_feature_inner`.

## A concrete calculation

Take `m = 12` and `n = 18`. Their greatest common divisor is `6`. The positive-weight divisor coordinates common to both feature vectors are the prime powers `2` and `3`:

```text
⟨φ(12), φ(18)⟩
  = Λ(2) + Λ(3)
  = log 2 + log 3
  = log 6
  = log(gcd(12,18)).
```

The construction includes every divisor coordinate, but `Λ(d)` is zero unless `d` is a prime power. Finite support is therefore built into the formal object; no convergence argument is being hidden.

## Why the quadratic form is nonnegative

The von Mangoldt divisor identity gives

```text
log(gcd(m,n)) = Σ_d Λ(d)[d|m][d|n].
```

Substituting this into a finite quadratic form and changing the order of summation gives

```text
ΣᵢΣⱼ cᵢcⱼ log(gcd(xᵢ,xⱼ))
  = Σ_d Λ(d) (Σ_{i : d|xᵢ} cᵢ)².
```

Every term on the right is nonnegative because `Λ(d) ≥ 0`. The feature theorem packages the same decomposition as an exact finite Gram factorization.

## What is new here—and what is not

The mathematics belongs to the established theory of GCD matrices. For an arithmetical function `f`, classical incidence factorizations express

```text
[f(gcd(x_i,x_j))] = E diag((f * μ)(d)) Eᵀ,
```

and positivity is governed by nonnegativity of the Möbius transform `f * μ`. For `f(n)=log n`, the transform is the von Mangoldt function:

```text
(log * μ)(d) = Λ(d) ≥ 0.
```

Accordingly:

- mathematical novelty is **not supported**;
- novelty of the divisor-feature factorization is **not supported**;
- no first-public-Lean-formalization priority is established;
- the programme contribution is a pinned, replayable Lean artifact, explicit `Finsupp` packaging, claim governance, and public exposition.

The governing literature audit is recorded in [LOG-GCD prior-art audit](LOG_GCD_PRIOR_ART_AUDIT.md).

## Claim boundary

The publication does **not** claim any of the following:

- a new theorem or novel kernel;
- a first proof, first feature representation, or first Lean formalization;
- strict positive definiteness on all positive natural numbers;
- a theorem over inputs containing zero;
- a separately completed `ℓ²(ℕ)` construction;
- that prime coordinates form a formally specified complete orthogonal basis.

The strict-positive-definiteness claim already fails at `1`:

```text
K(1,1) = log(gcd(1,1)) = log 1 = 0.
```

## Certification record

| Artifact | Status | Evidence |
| --- | --- | --- |
| `logGcd_posSemidef` | `CERTIFIED` | workflow `29984406250` |
| `logGcdFeature` and `logGcd_eq_feature_inner` | `CERTIFIED` | workflow `29993578051` |
| promoted governance state | `CHECKED` | workflow `29994235171` |
| prior-art determination | `AUDITED` | `PRIOR_ART_AUDIT.md` and `prior_art_audit.json` |

All Lean builds use `leanprover/lean4:v4.33.0-rc1`, mathlib release `v4.33.0-rc1`, and the exact pinned dependency graph. The fixture contains no `sorry` and introduces no local axioms.

## Inspect and reproduce

The authoritative certificate fixture is [`fixtures/formal/LOG-GCD-001`](https://github.com/grandchallenge/MATH-PROGRAMME/tree/main/fixtures/formal/LOG-GCD-001).

From that directory:

```bash
lake exe cache get
lake build
```

The publication manifest is `publication_manifest.json`. It binds this page to the certified claim IDs, the negative novelty determination, the permanent claim boundary, and the repository publication gate.
