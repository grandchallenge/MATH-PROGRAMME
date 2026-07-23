# DOMAIN_02_NAVIER_STOKES_CRITICAL_INTEGRABILITY_MASTER_PLAN.md

## Domain

**Domain 02: Three-Dimensional Incompressible Navier–Stokes / Critical Integrability**

- Campaign identifier: `NS-CI-001`
- Canonical tracker: `MATH-PROGRAMME#55`
- Primary domain: the unforced Cauchy problem on `ℝ³`
- Secondary domain: the periodic problem on `𝕋³`, tracked as a separate hypothesis profile
- Initial result status: `OPEN`
- Initial programme state: `CAMPAIGN_INITIALIZATION`

## Challenge statement

Fix viscosity `ν > 0`. Let `u₀ ∈ C_c^∞(ℝ³;ℝ³)` satisfy `∇·u₀ = 0`, and let `u` be a Leray–Hopf weak solution of

```math
∂_t u + (u·∇)u + ∇p = νΔu,
\qquad ∇·u = 0,
\qquad u(0)=u₀.
```

Determine whether, for every finite `T > 0`,

```math
I_T(u) := ∫₀ᵀ ‖u(t)‖_{L⁶(ℝ³)}⁴\,dt < ∞.
```

This is the critical Ladyzhenskaya–Prodi–Serrin pair `(q,p)=(4,6)`, since

```math
2/q + 3/p = 2/4 + 3/6 = 1.
```

## Exact campaign posture

The programme does **not** begin by claiming a new a priori estimate. It begins by separating four logically distinct objects:

1. the energy-class estimate actually available;
2. the missing critical time-integrability estimate;
3. the conditional regularity theorem that would consume that estimate;
4. the bridge from universal critical integrability to global smoothness.

The campaign must not confuse a criterion for regularity with a proof that the criterion always holds.

## Why this formulation is useful

The usual Leray–Hopf bounds give

```math
u ∈ L^∞(0,T;L²_x) ∩ L²(0,T;H¹_x).
```

Sobolev embedding in three dimensions gives

```math
u ∈ L²(0,T;L⁶_x),
```

but the challenge asks for `L⁴(0,T;L⁶_x)`. The exponent gap is exact and cannot be repaired by finite-interval inclusion: `L⁴(0,T) ⊂ L²(0,T)`, not conversely.

Under the Navier–Stokes scaling

```math
u_λ(x,t)=λu(λx,λ²t),
```

one has `I_T(u_λ)=I_{λ²T}(u)`. The quantity therefore sits exactly at the scale-invariant boundary where the energy estimate no longer gains control under concentration.

## Equivalent and adjacent formulations requiring audit

### A. Leray–Hopf formulation

Every Leray–Hopf solution arising from smooth, compactly supported, divergence-free data belongs to `L⁴(0,T;L⁶)` on every finite interval.

### B. Maximal strong-solution formulation

For the unique maximal strong solution on `[0,T_*)`, a finite maximal time requires

```math
∫₀^{T_*} ‖u(t)‖₆⁴\,dt = ∞.
```

Thus a universal finite bound rules out finite-time breakdown.

### C. Quantitative continuation formulation

Find a function `Φ` such that control of `I_T(u)` and the initial-data norm yields a controlled strong norm at time `T` or an explicit continuation interval beyond `T`.

### D. Restricted-target formulation

Establish the estimate under a checkable additional hypothesis that is not merely a restatement of regularity, such as a small critical norm, a frequency-envelope condition, a geometric depletion condition, or a quantitatively stable symmetry class.

The equivalence of A and B uses standard local strong existence, the Ladyzhenskaya–Prodi–Serrin criterion, and weak–strong uniqueness. Each hypothesis must be recorded explicitly; no equivalence may be promoted by slogan.

## Initial theorem spine

```text
NS-CI-D000  Equation, viscosity, domain, forcing convention, and solution classes
NS-CI-D001  Mixed-norm convention and endpoint policy
NS-CI-L002  Leray–Hopf energy inequality
NS-CI-L003  Homogeneous/inhomogeneous Sobolev bridge to L⁶
NS-CI-C004  Energy-class consequence u ∈ L²_tL⁶_x
NS-CI-O005  Abstract L²_t ↛ L⁴_t obstruction
NS-CI-L006  Navier–Stokes scaling law
NS-CI-C007  Scale invariance of I_T
NS-CI-L008  Ladyzhenskaya–Prodi–Serrin regularity at (4,6)
NS-CI-L009  Weak–strong uniqueness bridge
NS-CI-L010  Blow-up/continuation alternative expressed through I_T
NS-CI-T011  Universal critical-integrability challenge
NS-CI-R012  Restricted theorem target, to be selected after audit
```

## Dependency architecture

```text
D000 ─┬─> L002 ─> L003 ─> C004 ─> O005
      ├─> D001 ────────────────┐
      └─> L006 ─> C007 ────────┼─> T011
                                │
L008 ─> L009 ─> L010 ──────────┘

source audit + adversarial review ─> R012
```

`O005` is an obstruction node, not a negative result about Navier–Stokes. It proves only that the standard energy-class information is logically insufficient by itself.

## Work Package sequence

### WP00: Foundation, status, and equivalence audit

Goal: establish a trustworthy statement of the campaign.

Deliverables:

- solution-class and domain dictionary;
- exact scaling calculation;
- energy-to-`L²_tL⁶_x` derivation;
- abstract exponent-gap witness;
- primary-source ledger;
- theorem spine and dependency DAG;
- claim ledger and proof-debt register;
- MATHCERT handoff;
- Agent Council review record.

### WP01: Energy-gap obstruction and false-proof atlas

Goal: catalogue every tempting but invalid route from the energy inequality to the critical estimate.

Required failures include:

- reversed finite-measure embedding;
- illegal interpolation in time;
- hidden use of `L^∞_tH¹_x`;
- circular invocation of regularity;
- unjustified pressure estimates;
- scale-breaking truncations whose constants diverge;
- numerical boundedness presented as continuum proof.

### WP02: Conditional regularity and continuation ledger

Goal: reconstruct the exact theorem chain consuming `L⁴_tL⁶_x` control, including constants and continuation hypotheses where available.

### WP03: Quantitative concentration observatory

Goal: build reproducible diagnostics for concentration in shell models, Galerkin truncations, and verified smooth benchmark flows.

Boundary: computations may test mechanisms and implementations. They cannot certify global regularity or rule out singularity in the continuum equation.

### WP04: Restricted theorem target

Goal: select one theorem-grade restricted target after the source audit. Candidate families must be ranked by mathematical leverage, non-circularity, formalizability, and falsifiability.

### WP05: Certification substrate

Goal: formalize safe local statements and interfaces: scaling identities, mixed-norm algebra, energy/Sobolev consequences, implication structure, and explicit hypotheses of any imported regularity theorem.

## Three-pillar split

### MATHFORGE

- primary-source and current-status audit;
- taxonomy of regularity criteria;
- false-proof and claimed-proof triage;
- exact scaling fixtures;
- restricted-regime candidate generation;
- non-probative computational diagnostics.

### MATHSOLVE

- theorem spine and proof-debt ownership;
- analytic derivations and obstruction proofs;
- continuation and equivalence map;
- restricted-target selection;
- explicit route termination when a mechanism fails.

### MATHCERT

- formal statement hygiene;
- mixed-norm and scaling identities;
- energy/Sobolev bridge where library support permits;
- conditional implication interfaces;
- proof objects only for closed lemmas, never for the open universal estimate.

## Foundational profile

- Carrier: real-valued vector fields and distributions on `ℝ³ × [0,T]`.
- Ambient structures: measure spaces, Banach/Sobolev spaces, distributions, nonlinear PDE, weak and strong solution classes.
- Classical base: standard classical mathematics with excluded middle and ordinary choice as used in analysis.
- Witness policy: existential weak solutions are literature-derived until reconstructed; computational trajectories are not witnesses for the continuum universal claim.
- Pathology risk: high, due to weak convergence, concentration, endpoint estimates, nonuniqueness outside the Leray–Hopf/regularity classes, and semantic drift between solution concepts.

Registry promotion is deferred until MSC/arXiv mappings and knowledge-graph nodes are independently audited.

## Source-audit seed

1. Charles L. Fefferman, *Existence and Smoothness of the Navier–Stokes Equation*, Clay Mathematics Institute, official problem description.
2. Giovanni Prodi, *Un teorema di unicità per le equazioni di Navier–Stokes*, 1959, DOI `10.1007/BF02410664`.
3. James Serrin, *On the Interior Regularity of Weak Solutions of the Navier–Stokes Equations*, 1962, DOI `10.1007/BF00253344`.
4. O. A. Ladyzhenskaya, *On the uniqueness and on the smoothness of weak solutions of the Navier–Stokes equations*, 1967.
5. Jean Leray's original weak-solution construction and energy framework: exact edition, theorem statement, and translation source pending audit.

These sources seed the ledger; they do not complete it.

## Claim boundary

This initialization establishes no new Navier–Stokes theorem. In particular, it does not claim:

- universal finiteness of `I_T`;
- a new regularity criterion;
- a reduction that weakens the Millennium problem;
- evidence against finite-time singularity from numerical experiments;
- novelty for the challenge formulation itself.

## First executable step

Complete WP00 by independently auditing the exact hypotheses and logical arrows in

```text
energy class → L²_tL⁶_x,
L⁴_tL⁶_x → regularity,
regularity + local theory → continuation,
universal L⁴_tL⁶_x → global regularity.
```

The completion test is a reviewed source ledger, a machine-readable dependency DAG, a complete trust quartet, and zero unrecorded assumptions.