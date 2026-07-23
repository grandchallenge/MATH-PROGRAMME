# LOG-GCD-001: logarithmic GCD kernel

## Result-status box

| Field | Status |
|---|---|
| Object | `K(m,n) = log(gcd(m,n))` on positive natural numbers |
| Strongest certified claim | Every finite Gram quadratic form is nonnegative |
| Certified theorem | `logGcd_posSemidef` |
| Feature formalization | `logGcdFeature` and `logGcd_eq_feature_inner`; target-repository CI pending |
| Support route | Lean 4 + mathlib, pinned to `v4.33.0-rc1` and exact transitive revisions |
| Current certification state | Base PSD theorem **CERTIFIED**; feature extension `PENDING_TARGET_CI` |
| Prior-art determination | Mathematical novelty **NOT SUPPORTED**; Lean-artifact priority **NOT ESTABLISHED** |
| Computation class | `NONE` |
| Claims not made | novelty, priority, strict positive definiteness, zero-input extension, completed-space ℓ² packaging |
| First executable step | Build the expanded pinned Lake project in CI |

## Lay companion

The greatest common divisor records the prime-power structure shared by two
positive integers. Taking its logarithm turns that shared structure into an
additive similarity score. The certified theorem says that any finite matrix of
these scores behaves like a Gram matrix: every real weighted quadratic form is
nonnegative.

The feature module now makes that Gram picture literal. A positive integer is
mapped to one coordinate for each divisor. The coordinate at `d` is
`sqrt(Λ(d))` when `d` divides the integer and zero otherwise. Only finitely many
coordinates are nonzero, so Lean represents the vector as a `Finsupp` rather
than assuming convergence of an infinite series.

## Formal statements

For a finite type `ι`, values `x : ι → ℕ` satisfying `1 ≤ x i`, and real
coefficients `c : ι → ℝ`:

```lean
0 ≤ ∑ i, ∑ j, c i * c j * Real.log (Nat.gcd (x i) (x j))
```

The certified declaration is `logGcd_posSemidef` in `LogGcd.lean`.

For nonzero naturals `m,n`, the new module proves:

```lean
finsuppDot (logGcdFeature m) (logGcdFeature n)
  = Real.log (Nat.gcd m n)
```

The declaration is `logGcd_eq_feature_inner` in `LogGcdFeature.lean`.

## Theorem spine

```text
LOG-GCD-D01  von Mangoldt divisor-sum identity
      |
LOG-GCD-D02  nonnegativity of von Mangoldt weights
      |
LOG-GCD-F01  logGcdFeature : ℕ → (ℕ →₀ ℝ)               [FORMALIZED]
      |
LOG-GCD-F02  logGcd_eq_feature_inner                    [PENDING CI]
      |
LOG-GCD-T01  logGcd_posSemidef                          [CERTIFIED]
      |
LOG-GCD-I01  positive-semidefinite-kernel interpretation [AUDITED]
```

The feature theorem and the original quadratic-form theorem use the same
nonnegative divisor weights. The feature theorem exposes the Gram
factorization as a first-class formal object rather than leaving it only inside
the square-completion proof.

## Feature realization

The finitely supported feature map is

```text
φ(n)_d = sqrt(Λ(d)) [d | n].
```

In Lean:

```lean
noncomputable def logGcdFeature (n : ℕ) : ℕ →₀ ℝ :=
  Finsupp.indicator n.divisors fun d _ => Real.sqrt (Λ d)
```

Its support is contained in `n.divisors` by construction. The dot-product
identity follows because

```text
sqrt(Λ(d)) sqrt(Λ(d)) = Λ(d)
```

and a divisor contributes to both features exactly when it divides the gcd.
The von Mangoldt divisor identity then turns the finite sum into
`log(gcd(m,n))`.

This is a fully formal finitely supported realization. It is not presented as
a separate construction of the completed Hilbert space `ℓ²(ℕ)` because finite
support already suffices for the exact Gram identity and embeds canonically
into that completion.

## Prior-art determination

The mathematical theorem and the divisor feature factorization are not novel.
They are direct instances of the established theory of GCD matrices associated
with an arithmetical function `f`:

```text
[f(gcd(x_i,x_j))] = E diag((f * μ)(d)) Eᵀ.
```

The general positivity criterion requires the Möbius transform `f * μ` to be
nonnegative. For `f(n)=log n`,

```text
(log * μ)(d) = Λ(d) ≥ 0.
```

Therefore the present proof and feature coordinates specialize a classical
incidence factorization. The bounded audit located no earlier public exact Lean
artifact beyond the credited upstream repository, but this does not establish
first-formalization priority. The authoritative audit is
`PRIOR_ART_AUDIT.md`, with machine-readable policy in
`prior_art_audit.json`.

Permitted description:

> A GCL-certified Lean formalization and explicit `Finsupp` realization of a
> classical GCD-matrix positivity criterion.

Descriptions such as “new theorem,” “novel kernel,” “first proof,” or “first
Lean formalization” are prohibited.

## Claim boundary

The theorem proves positive **semidefiniteness**. It does not prove strict
positive definiteness. In particular, `K(1,1)=0`.

The feature theorem is stated for nonzero natural inputs. No extension over
zero inputs is claimed. No claim is made that primes form a complete
orthogonal basis of a separately specified Hilbert space.

## Provenance

The base formalization is adapted from
`irregular-rhomboid/log-gcd-lean`, pinned at commit
`d2038c7b09fe849f236d6428d7159b5a40f9aed7`. The upstream formal file is
`Loggcd/Lean/loggcd.lean`, Git blob
`fd5b136ed32c6d48f5f71381ccf4b69d1329088f`.

The upstream `lake-manifest.json` is pinned by Git blob
`99d43177d509c4ceb340c8b2e6330e9c75233169`; it resolves mathlib to commit
`79d0395a1825a6264ad5d269e35e60537518955e`.

The upstream repository is dedicated under CC0-1.0. The source lock records
the license blob, theorem blob, manifest blob, toolchain, and exact dependency
revision. `LogGcdFeature.lean` and the prior-art audit are GCL follow-on
artifacts and do not alter the upstream attribution.

## Reproduction

From this fixture directory:

```bash
lake exe cache get
lake build
```

CI performs the same pinned replay. The original theorem was certified by
workflow run `29984406250`; the expanded feature module awaits its own replay
before claim `LOG-GCD-001-C003` is promoted.

## Trust quartet

1. **Proved and certified:** the finite quadratic-form inequality, conditional
   only on the displayed positivity hypotheses and pinned mathlib dependencies.
2. **Formalized, pending replay:** the finitely supported divisor feature map
   and exact dot-product identity.
3. **Audited:** mathematical novelty and feature-factorization novelty are not
   supported; public Lean-artifact priority is not established.
4. **Still excluded:** strict positive definiteness, zero-input extension,
   completed-space packaging, and every first-or-novelty assertion.

## Next executable step

**Input:** `LogGcd.lean`, `LogGcdFeature.lean`, and the exact pinned Lake
manifest.  
**Operation:** run the repository-native Lean replay.  
**Output:** a checked build containing `logGcd_eq_feature_inner`.  
**Completion test:** the `Replay LOG-GCD-001 in Lean` CI job passes with no
`sorry` or local axioms.  
**Debt discharged on success:** `LOG-GCD-001-O002`; the prior-art debt
`LOG-GCD-001-O003` is already closed by the negative novelty audit.
