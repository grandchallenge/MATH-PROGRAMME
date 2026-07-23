# The logarithmic GCD kernel

`LOG-GCD-001` is a certified MATHCERT fixture for the logarithmic GCD kernel,
including an explicit finitely supported feature realization.

## The result

For positive natural numbers, define

```text
K(m,n) = log(gcd(m,n)).
```

For any finite collection `xᵢ` and real coefficients `cᵢ`,

```text
ΣᵢΣⱼ cᵢcⱼ K(xᵢ,xⱼ) ≥ 0.
```

Thus `K` is a positive semidefinite kernel in the finite-Gram-matrix sense.
The Lean theorem `logGcd_posSemidef` is certified by MATH-PROGRAMME workflow
run `29984406250`.

## Explicit feature realization

The follow-on module defines a finitely supported vector

```text
φ(n)_d = sqrt(Λ(d)) [d | n]
```

as `logGcdFeature n : ℕ →₀ ℝ`. It proves the exact Gram identity

```lean
finsuppDot (logGcdFeature m) (logGcdFeature n)
  = Real.log (Nat.gcd m n)
```

for nonzero natural inputs. The declaration
`logGcd_eq_feature_inner` in `LogGcdFeature.lean` is certified by the expanded
repository-native replay in workflow run `29993578051`.

Finite support is part of the type: the vector is supported on the divisors of
`n`. No convergence assumption is hidden in the construction.

## Why it works

The von Mangoldt divisor identity gives

```text
log(gcd(m,n)) = Σ_d Λ(d)[d|m][d|n].
```

Every divisor `d` contributes one coordinate. When `d` divides both numbers,
the coordinate product is

```text
sqrt(Λ(d)) sqrt(Λ(d)) = Λ(d).
```

Summing the coordinate products recovers the logarithm of the gcd. The
quadratic-form theorem and feature theorem are two certified views of the same
nonnegative divisor decomposition.

## Prior-art determination

The mathematical theorem and feature factorization are classical, not novel.
General GCD-matrix theory factors matrices of the form

```text
[f(gcd(x_i,x_j))] = E diag((f * μ)(d)) Eᵀ
```

and characterizes positivity through nonnegativity of the Möbius transform
`f * μ`. For `f(n)=log n`, this transform is the nonnegative von Mangoldt
function.

The programme therefore permits the description:

> A GCL-certified Lean formalization and explicit `Finsupp` realization of a
> classical GCD-matrix positivity criterion.

It prohibits “new theorem,” “novel kernel,” “first proof,” “first feature
representation,” and “first Lean formalization.” The bounded search did not
locate an earlier exact public Lean artifact beyond the credited upstream
source, but this does not establish priority. See **LOG-GCD prior-art audit**
for the governing literature and complete determination.

## What entered the programme

The upstream base formalization is pinned to:

```text
repository:      irregular-rhomboid/log-gcd-lean
commit:          d2038c7b09fe849f236d6428d7159b5a40f9aed7
formal file:     Loggcd/Lean/loggcd.lean
formal blob:     fd5b136ed32c6d48f5f71381ccf4b69d1329088f
manifest blob:   99d43177d509c4ceb340c8b2e6330e9c75233169
license:         CC0-1.0
toolchain:       leanprover/lean4:v4.33.0-rc1
mathlib release: v4.33.0-rc1
mathlib commit:  79d0395a1825a6264ad5d269e35e60537518955e
```

The CC0 source is vendored as a standalone Lake fixture. The feature module,
prior-art audit, claim-ledger promotion, Agent Council review, adversarial
tests, and documentation are GCL follow-on artifacts.

## Claim boundary

The formal theorem proves positive semidefiniteness, not strict positive
definiteness. The value at `1` is zero:

```text
K(1,1) = log(1) = 0.
```

The feature map is a formal `Finsupp` realization. It is not advertised as a
novel embedding or as a separately developed completed-space `ℓ²`
construction. Zero inputs remain outside the theorem statement.

## Certification record

```text
classical GCD-matrix factorization
    ↓ formalized divisor features
LogGcdFeature.lean
    ↓ provenance, audit, and adversarial policy checks
repository-native pinned lake build: workflow 29993578051
    ↓
C003 CERTIFIED; O002 and O003 CLOSED
```

The authoritative integrated artifact is
`fixtures/formal/LOG-GCD-001/README.md`.
