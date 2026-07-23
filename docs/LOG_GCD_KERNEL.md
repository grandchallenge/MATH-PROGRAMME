# The logarithmic GCD kernel

`LOG-GCD-001` brings a compact Lean result into the programme as a
MATHCERT-oriented formal fixture.

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

## Why it works

The von Mangoldt divisor identity gives

```text
log(gcd(m,n)) = Σ_d Λ(d)[d|m][d|n].
```

Every divisor `d` contributes a rank-one positive semidefinite matrix, weighted
by `Λ(d) ≥ 0`. Summing those matrices preserves positive semidefiniteness.

## What entered the programme

The upstream formalization is pinned to:

```text
repository: irregular-rhomboid/log-gcd-lean
commit:     d2038c7b09fe849f236d6428d7159b5a40f9aed7
file:       Loggcd/Lean/loggcd.lean
blob:       fd5b136ed32c6d48f5f71381ccf4b69d1329088f
license:    CC0-1.0
toolchain:  leanprover/lean4:v4.33.0-rc1
mathlib:    v4.33.0-rc1
```

The CC0 source is vendored as a standalone Lake fixture, with exact provenance,
claim ledger, Agent Council review, adversarial metadata tests, and a dedicated
Lean CI replay.

## Claim boundary

The formal theorem proves positive semidefiniteness, not strict positive
definiteness. The value at `1` is zero:

```text
K(1,1) = log(1) = 0.
```

The divisor-feature formula suggests an explicit Hilbert-space embedding, but
that feature map is not yet packaged as a separate Lean object. No novelty or
priority claim is made.

## Certification route

```text
upstream Lean artifact
    ↓ provenance lock
vendored GCL Lake fixture
    ↓ metadata and adversarial validation
repository-native `lake build`
    ↓
MATHCERT promotion decision
```

The authoritative integrated artifact is
`fixtures/formal/LOG-GCD-001/README.md`.
