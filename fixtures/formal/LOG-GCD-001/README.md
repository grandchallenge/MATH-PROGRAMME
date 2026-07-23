# LOG-GCD-001: logarithmic GCD kernel

## Result-status box

| Field | Status |
|---|---|
| Object | `K(m,n) = log(gcd(m,n))` on positive natural numbers |
| Strongest supported claim | Every finite Gram quadratic form is nonnegative |
| Formal theorem | `logGcd_posSemidef` |
| Support route | Lean 4 + mathlib, pinned to `v4.33.0-rc1` |
| Current certification state | Formal artifact imported; MATH-PROGRAMME CI replay required |
| Computation class | `NONE` |
| Claims not made | novelty, strict positive definiteness, zero-input extension, formal ℓ² feature map |
| First executable step | Build the vendored Lake project in CI |

## Lay companion

The greatest common divisor records the prime-power structure shared by two
positive integers. Taking its logarithm turns that shared structure into an
additive similarity score. The theorem says that any finite matrix of these
scores behaves like a Gram matrix: every real weighted quadratic form is
nonnegative.

The proof decomposes the score into nonnegative contributions indexed by
divisors. Each divisor contributes a rank-one positive semidefinite matrix.
Their weighted sum is therefore positive semidefinite.

## Formal statement

For a finite type `ι`, values `x : ι → ℕ` satisfying `1 ≤ x i`, and real
coefficients `c : ι → ℝ`:

```lean
0 ≤ ∑ i, ∑ j, c i * c j * Real.log (Nat.gcd (x i) (x j))
```

The checked declaration is `logGcd_posSemidef` in `LogGcd.lean`.

## Theorem spine

```text
LOG-GCD-D01  von Mangoldt divisor-sum identity
      |
LOG-GCD-D02  nonnegativity of von Mangoldt weights
      |
LOG-GCD-B01  log(gcd) as weighted divisor-indicator products
      |
LOG-GCD-B02  finite-sum interchange and square completion
      |
LOG-GCD-T01  logGcd_posSemidef
      |
LOG-GCD-I01  positive-semidefinite-kernel interpretation
```

`LOG-GCD-T01` is formalized. The explicit Hilbert-space feature-map object is
not yet formalized.

## Proof idea

For positive `m,n`,

```text
log(gcd(m,n))
  = Σ_{d | gcd(m,n)} Λ(d)
  = Σ_d Λ(d) [d|m][d|n].
```

Thus

```text
ΣᵢΣⱼ cᵢcⱼ log(gcd(xᵢ,xⱼ))
  = Σ_d Λ(d) (Σᵢ cᵢ[d|xᵢ])²
  ≥ 0.
```

The Lean proof uses a finite common divisor pool: the divisors of the product
of all sampled values.

## Claim boundary

The theorem proves positive **semidefiniteness**. It does not prove strict
positive definiteness. In particular, `K(1,1)=0`.

The source repository also discusses an infinite feature map

```text
φ(n)_d = sqrt(Λ(d)) [d|n].
```

This fixture treats that as an audited mathematical interpretation, not as a
separately formalized Lean object.

## Provenance

The formalization is adapted from
`irregular-rhomboid/log-gcd-lean`, pinned at commit
`d2038c7b09fe849f236d6428d7159b5a40f9aed7`. The upstream formal file is
`Loggcd/Lean/loggcd.lean`, Git blob
`fd5b136ed32c6d48f5f71381ccf4b69d1329088f`.

The upstream repository is dedicated under CC0-1.0. The source lock records
the license blob, theorem file blob, toolchain, and mathlib revision.

## Reproduction

From this fixture directory:

```bash
lake build
```

CI executes the same build through `leanprover/lean-action`.

## Trust quartet

1. **Proved:** the finite quadratic-form inequality, conditional only on the
   displayed positivity hypotheses and mathlib dependencies.
2. **Checked:** source identity, provenance lock, claim ledger, Agent Council
   record, and—after the CI gate—the Lean build.
3. **Open:** a first-class formal feature map, its ℓ² packaging, and optional
   corollaries such as coprimality-as-orthogonality.
4. **External verification:** novelty and prior-art assessment have not been
   performed.

## Next executable step

**Input:** the vendored pinned Lake package.  
**Operation:** run `lake build` in GitHub Actions.  
**Output:** a repository-native Lean replay result.  
**Completion test:** the `log-gcd-lean` CI job passes.  
**Debt discharged:** `LOG-GCD-001-O001`.
