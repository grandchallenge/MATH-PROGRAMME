# PUB-LOG-GCD-001 — GCL-TCS public communication map

**Pilot artifact:** `PUB-LOG-GCD-001-TCS-PILOT-001`  
**Subject publication:** `PUB-LOG-GCD-001`  
**Canonical public page:** `docs/LOG_GCD_PUBLICATION.md`  
**Public-page blob:** `f52b6e0d08520de2c4d263a58acee06468d1770c`  
**Publication-manifest blob:** `24f76b494b74a51f2949171b8380cc08f1458156`  
**Primary profile:** `GCL-TCS-P06`  
**Secondary profiles:** `GCL-TCS-P03`, `GCL-TCS-P02`  
**Impact class:** `IC-2`  
**Pilot authority:** candidate / in review

## Purpose

This supplement evaluates whether the already-published LOG-GCD public note preserves the exact certified mathematical claims, audited negative boundaries, source provenance, replay path, and publication authority that support it. It does not edit, republish, recertify, or canonically promote the subject publication or its mathematics.

The existing public page remains the canonical public exposition. This supplement is an internal governance layer over that fixed artifact.

## Authority chain

The public note is downstream of distinct authority objects:

1. `LOG-GCD-001-C001` — `CERTIFIED`: finite Gram quadratic-form nonnegativity for positive natural inputs, formal theorem `logGcd_posSemidef`.
2. `LOG-GCD-001-C003` — `CERTIFIED`: exact finitely supported divisor-feature Gram identity for nonzero natural inputs, formal theorem `logGcd_eq_feature_inner` and definition `logGcdFeature`.
3. `LOG-GCD-001-C004` — `AUDITED`: strict positive definiteness on the full positive-natural domain is false; `K(1,1)=0` is the exact boundary example.
4. `LOG-GCD-001-C005` — `AUDITED`: mathematical novelty is not supported and public Lean-artifact priority is not established.
5. `PUB-LOG-GCD-001` — `PUBLISHED`: the public visibility node binds only the permitted claims and boundaries above; publication changes visibility, not mathematical status.

GCL-TCS evaluates how those states are communicated. It is not a replacement proof system, MATHCERT route, canonical Claim Ledger, publication gate, or MATH-CORE mathematical-state plane.

## Public claim lock

The publication manifest fixes the published claim set to exactly:

- `LOG-GCD-001-C001`;
- `LOG-GCD-001-C003`.

It fixes the public boundary set to exactly:

- `LOG-GCD-001-C004`;
- `LOG-GCD-001-C005`.

The permitted description is:

> A GCL-certified Lean formalization and explicit Finsupp realization of a classical GCD-matrix positivity criterion.

This pilot does not authorize a replacement or stronger description.

## Mathematical content exposed to the public

For positive natural inputs, the public note defines

```text
K(m,n) = log(gcd(m,n)).
```

and states the certified finite-Gram nonnegativity result. It also explains the finitely supported divisor feature map

```text
phi(n)_d = sqrt(Lambda(d)) when d divides n, and 0 otherwise,
```

whose certified dot-product identity is `log(gcd(m,n))` for nonzero inputs.

The public exposition may explain the divisor-incidence mechanism, but explanatory prose cannot widen theorem quantifiers, erase positivity/nonzero-input hypotheses, convert a finite-support construction into a separately established completed-space theorem, or turn an audited interpretation into a certified theorem.

## Negative and novelty boundaries

The public note correctly exposes the principal falsifier of strict positive definiteness:

```text
K(1,1) = log(gcd(1,1)) = 0.
```

It also states that the theorem and divisor-incidence factorization belong to established GCD-matrix theory. The prior-art audit therefore forbids descriptions such as:

- new theorem;
- novel kernel;
- first proof;
- first feature representation;
- first Lean formalization.

A bounded search that failed to locate an earlier exact public Lean artifact does not establish priority. Public indexing limitations remain material negative evidence.

## Provenance and replay

The public note points to the authoritative fixture `fixtures/formal/LOG-GCD-001`. Its protected result-status record identifies the certified declarations, pinned Lean/mathlib route, upstream provenance, prior-art determination, and publication gate.

The publication manifest binds the page to publication workflow `29997559180` and certification evidence runs `29984406250`, `29993578051`, and `29994235171`. The publication validator fail-closes drift in the published claim set, boundary set, permitted/prohibited descriptions, certification evidence, and public-page integration.

The underlying fixture documents reproduction from its directory with:

```text
lake exe cache get
lake build
```

This GCL-TCS supplement inherits that replay provenance as source evidence. It does not issue a new mathematical replay or certificate.

## MATH-CORE and trusted-acceptance firewall

ADR-0021 and `MATH_CORE_INTEGRITY.md` keep mathematical coordination, proof/replay checking, independent assurance, certification state, canonical Claim Ledger recording, and policy/publication disposition distinct.

No new MATH-CORE event or migration is needed to review this public artifact. This pilot therefore creates no blackboard claim, certificate event, cross-domain bridge, canonical promotion, or C04-C07 capability transition. Existing mathematical authority remains where the source records place it.

## Public accessibility and interpretation

The canonical page gives a plain-language description, exact formulas, a concrete `12`/`18` example, a finite-support explanation, explicit novelty/priority exclusions, certification evidence, and reproduction pointers. These features support public comprehension without replacing the formal source.

The principal interpretation hazard is authority inflation by paraphrase. A shorter or more accessible explanation must continue to preserve:

- positive semidefinite, not strict positive definite;
- positive/nonzero input boundaries as applicable to the exact theorem;
- certified versus audited status;
- classical-result / negative-novelty determination;
- no first-formalization priority;
- no completed `l2(N)` construction claim;
- no claim that prime coordinates form a formally specified complete orthogonal basis.

## Pilot observations

The existing public page already exhibits strong source-to-public claim discipline: status, theorem names, exclusions, prior-art conclusion, replay route, and publication gate are visible together. The publication validator converts several of those communication boundaries into machine-enforced invariants.

The remaining burden is maintenance: future public edits must remain synchronized with the fixed certified/audited claim set. This pilot does not measure reader comprehension, accessibility outcomes, or the probability of future paraphrase drift.

## What this pilot does not establish

This pilot does not prove or recertify LOG-GCD mathematics; alter the canonical claim ledger; establish mathematical novelty, priority, strict positive definiteness, zero-input extension, completed-space packaging, or basis completeness; migrate LOG-GCD into MATH-CORE; authorize a new publication; change publication status; or authorize any downstream commercial, patentability, or external claim.

G0-G7 in the candidate package are same-system internal checks only. They do not establish independent `CHECKED` or `ASSURED` GCL-TCS status. G8 and G9 remain separate promotion/admission boundaries.