# LOG-GCD-001: logarithmic GCD kernel

## Result-status box

| Field | Status |
|---|---|
| Object | `K(m,n) = log(gcd(m,n))` on positive natural numbers |
| Strongest supported claim | Every finite Gram quadratic form is nonnegative |
| Formal theorem | `logGcd_posSemidef` |
| Support route | Lean 4 + mathlib, pinned to `v4.33.0-rc1` and exact transitive revisions |
| Current certification state | **CERTIFIED** by repository-native Lean replay |
| Certification evidence | MATH-PROGRAMME workflow run `29984406250` |
| Computation class | `NONE` |
| Claims not made | novelty, strict positive definiteness, zero-input extension, formal ℓ² feature map |
| First executable step | Formalize the explicit finitely supported divisor feature map |

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

The certified declaration is `logGcd_posSemidef` in `LogGcd.lean`.

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
LOG-GCD-T01  logGcd_posSemidef                         [CERTIFIED]
      |
LOG-GCD-I01  positive-semidefinite-kernel interpretation [AUDITED]
```

The explicit Hilbert-space or finitely supported feature-map object is not yet
formalized as a separate declaration.

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

The upstream `lake-manifest.json` is pinned by Git blob
`99d43177d509c4ceb340c8b2e6330e9c75233169`; it resolves mathlib to commit
`79d0395a1825a6264ad5d269e35e60537518955e`.

The upstream repository is dedicated under CC0-1.0. The source lock records
the license blob, theorem blob, manifest blob, toolchain, and exact dependency
revision.

## Reproduction

From this fixture directory:

```bash
lake exe cache get
lake build
```

CI performs the same pinned replay. Workflow run `29984406250` completed
successfully.

## Trust quartet

1. **Proved and certified:** the finite quadratic-form inequality, conditional
   only on the displayed positivity hypotheses and pinned mathlib dependencies.
2. **Checked:** provenance lock, dependency manifest, claim ledger, Agent Council
   record, adversarial mutations, programme contracts, documentation, and Lean
   compilation.
3. **Open:** a first-class formal feature map, its Hilbert-space packaging, and
   optional corollaries such as coprimality-as-orthogonality.
4. **External verification:** novelty and prior-art assessment have not been
   performed.

## Next executable step

**Input:** `logGcd_posSemidef`, the von Mangoldt divisor identity, and the
finite support of the divisors of each positive integer.  
**Operation:** define a `Finsupp` divisor feature map weighted by
`sqrt (Λ d)` and prove its inner product equals `log (gcd m n)`.  
**Output:** `LogGcdFeature.lean` with a theorem such as
`logGcd_eq_feature_inner`.  
**Completion test:** the new theorem builds with no `sorry` and the existing PSD
theorem can be recovered as a corollary.  
**Debt advanced:** `LOG-GCD-001-O002`.
