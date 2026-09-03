# LOG-GCD-001 — GCL-TCS mathematical communication map

**Pilot artifact:** `LOG-GCD-001-TCS-PILOT-001`  
**Subject mathematical artifact:** `LOG-GCD-001` / certificate artifact `CERT-LOG-GCD-001`  
**Authoritative fixture:** `fixtures/formal/LOG-GCD-001/`  
**Protected baseline:** `20c4796ccd6d1e9d4fd8578ffc7c3f7847b40eb6`  
**Primary profile:** `GCL-TCS-P03`  
**Secondary profile:** `GCL-TCS-P02`  
**Impact class:** `IC-2`  
**Pilot authority:** candidate / in review

## Purpose

This supplement evaluates whether the existing LOG-GCD mathematical package exposes exact theorem identity, domains and quantifiers, formal/informal boundaries, dependency and evidence structure, counterexamples, prior-art limits, replay provenance, and certification status without changing any mathematical or canonical state.

The source fixture remains authoritative. This pilot is a communication mapping over frozen protected evidence. It is not a proof, proof repair, MATHCERT recertification, Claim Ledger promotion, publication event, or MATH-CORE migration.

## Exact source lock

The protected source lock records the upstream source as `irregular-rhomboid/log-gcd-lean` at commit `d2038c7b09fe849f236d6428d7159b5a40f9aed7`, formal-file blob `fd5b136ed32c6d48f5f71381ccf4b69d1329088f`, CC0-1.0 licensing, Lean `v4.33.0-rc1`, and mathlib commit `79d0395a1825a6264ad5d269e35e60537518955e`.

Protected GCL fixture identities used by this pilot include:

- `LogGcd.lean` — blob `06c3678d63021cf6fbb90b7c7f6b1a36e7f176a0`;
- `LogGcdFeature.lean` — blob `41429debd75ceed1da718ea629cbde3769cebdba`;
- `claim_ledger.json` — blob `525ac6eb321726627032968aa93b7f530e50c206`;
- `source_lock.json` — blob `42f500020ec7019d6390b717b6d1c6b3867fd844`;
- `agent_review.yaml` — blob `3de21489f09653c6a2f941cb163933b022c827b9`;
- `lake-manifest.json` — blob `99d43177d509c4ceb340c8b2e6330e9c75233169`;
- `lean-toolchain` — blob `fd85b262bf1c734663aa8292b0101f672168788f`.

## Certified theorem T01 — finite-Gram positive semidefiniteness

The protected Lean declaration is:

```lean
theorem logGcd_posSemidef
    (x : ι → ℕ) (hx : ∀ i, 1 ≤ x i) (c : ι → ℝ) :
    0 ≤ ∑ i, ∑ j, c i * c j * Real.log (Nat.gcd (x i) (x j))
```

The quantifier and domain lock is material:

- `ι` is a finite type;
- `x` maps each index to a natural number;
- `hx` requires every `x i` to satisfy `1 ≤ x i`;
- `c` is an arbitrary real coefficient family;
- the conclusion is nonnegativity of the finite quadratic form.

This establishes positive semidefiniteness in the finite-Gram sense. It does not establish strict positive definiteness.

## Certified theorem F02 — exact finitely supported feature identity

The protected feature definition is:

```lean
noncomputable def logGcdFeature (n : ℕ) : ℕ →₀ ℝ :=
  Finsupp.indicator n.divisors fun d _ => Real.sqrt (Λ d)
```

The protected feature theorem is:

```lean
theorem logGcd_eq_feature_inner
    (m n : ℕ) (hm : m ≠ 0) (hn : n ≠ 0) :
    finsuppDot (logGcdFeature m) (logGcdFeature n) =
      Real.log (Nat.gcd m n)
```

The nonzero hypotheses are part of the certified statement. `ℕ →₀ ℝ` makes finite support part of the formal type. The theorem does not separately construct or certify a completed `ℓ²(ℕ)` Hilbert space.

## Dependency and implication structure

The package exposes two formal views of the same divisor decomposition:

```text
von Mangoldt divisor identity + Λ(d) ≥ 0
             |
             +--> logGcd_posSemidef                 [CERTIFIED]
             |
             +--> logGcdFeature
                    |
                    +--> logGcd_eq_feature_inner    [CERTIFIED]
```

The feature module imports `LogGcd`; the feature identity is an exact Gram realization, while the PSD theorem is the certified quadratic-form statement. Publication and explanatory interpretations sit downstream and do not strengthen these formal declarations.

## Claim-state lock

The protected claim ledger records:

- `LOG-GCD-001-C001` — `CERTIFIED`: finite-Gram quadratic-form nonnegativity;
- `LOG-GCD-001-C002` — `AUDITED`: positive-semidefinite-kernel interpretation, dependent on C001;
- `LOG-GCD-001-C003` — `CERTIFIED`: exact finitely supported feature identity;
- `LOG-GCD-001-C004` — `AUDITED`: strict positive definiteness on all positive naturals is false;
- `LOG-GCD-001-C005` — `AUDITED`: mathematical novelty is not supported and first-formalization priority is not established.

This pilot inherits those statuses exactly. It does not create a new claim status or promote an audited interpretation into a formal theorem.

## Boundary cases and falsifiers

The principal exact counterexample to strict positive definiteness is:

```text
K(1,1) = log(gcd(1,1)) = log 1 = 0.
```

Additional boundaries that must remain visible are:

- no theorem over inputs containing zero beyond the exact source statements;
- no first-proof, first-feature-representation, or first-Lean-formalization claim;
- no mathematical novelty claim;
- no completed-space `ℓ²(ℕ)` construction claim;
- no formally specified complete orthogonal prime-basis claim.

A bounded search that did not locate an earlier exact public Lean artifact is negative search evidence only; it cannot establish priority.

## Formal/informal boundary

`LogGcd.lean` and `LogGcdFeature.lean` are the mechanized theorem sources. The fixture README, prior-art audit, public note, and this communication supplement explain and classify those results but do not become proof support merely by describing them.

The prior-art discussion is literature-derived and audited, not a Lean theorem. The positive-semidefinite-kernel interpretation is audited against the finite-Gram convention, not a separate certified declaration. Public exposition is downstream visibility, not mathematical promotion.

## Replay and certification provenance

The protected package fixes Lean `leanprover/lean4:v4.33.0-rc1` and the pinned Lake dependency graph. Existing certification evidence records:

- workflow `29984406250` — certified `logGcd_posSemidef`;
- workflow `29993578051` — certified the expanded feature package;
- workflow `29994235171` — checked the completed certification-governance state;
- workflow `29997559180` — publication candidate policy/adversarial/docs/unchanged Lean evidence.

The fixture documents reproduction with:

```text
lake exe cache get
lake build
```

For this Stage-A pilot, CI may validate that the relevant formal identity is unchanged and reuse a protected attestation. Such reuse is evidence preservation, not recertification. This supplement does not emit a new MATHCERT certificate or claim that an independent clean replay was performed by the authoring assistant.

## MATH-CORE and trusted-acceptance firewall

Protected ADR-0021 and `MATH_CORE_INTEGRITY.md` distinguish live reasoning coordination from proof/replay checking, independent assurance, certification, canonical Claim Ledger recording, and policy disposition.

LOG-GCD need not be migrated into MATH-CORE merely to satisfy this communication pilot. This package creates no blackboard event, certificate event, cross-domain evidence bridge, canonical promotion, or C04-C07 capability transition.

## Research communication layer

Under secondary profile P02, the canonical question is narrow: can `K(m,n)=log(gcd(m,n))` be represented as a positive-semidefinite finite Gram kernel with an explicit finite-support divisor feature map, and what exactly has been certified?

The answer is bounded by the protected declarations and claim ledger. The package also preserves its strongest counterevidence and prior-art result: strict positive definiteness fails at `1`, and mathematical novelty is not supported by the literature audit.

## What this pilot does not establish

This pilot does not prove a new theorem; repair or alter Lean; recertify LOG-GCD; independently reproduce the literature audit; promote C002, C004, or C005; change canonical Claim Ledger state; create MATH-CORE state; cross C04-C07; alter publication status; establish novelty or priority; or authorize patentability, commercial, or other external claims.

G0-G7 in this candidate package are same-system internal communication checks only. They do not satisfy independent G8 review. G8 and G9 remain separate authority gates.
