# NS-CI-WP00 — Foundation, status, and equivalence audit

## Metadata

- Domain: Three-dimensional incompressible Navier–Stokes
- Campaign: `NS-CI-001`
- Work Package: `NS-CI-WP00`
- Canonical tracker: `MATH-PROGRAMME#55`
- Primary type: status spine and obstruction audit
- Global theorem-spine node advanced: `NS-CI-T011`
- Incoming dependencies: none; this package establishes the initial dependency set
- Claim status: mixed; local derivations proved, regularity implications literature-derived, universal estimate open
- Certification target: human audit followed by selective theorem-prover formalization
- Foundational profile: present
- Promotion state: draft

## 1. Result-status box

| Field | Value |
|---|---|
| Result status | `INITIALIZED / OPEN PROBLEM` |
| Conditional on | Standard definitions of Leray–Hopf and strong solutions; source-audited Ladyzhenskaya–Prodi–Serrin and weak–strong uniqueness theorems |
| Strongest supported claim | The standard energy class implies `L²_tL⁶_x`, does not abstractly imply `L⁴_tL⁶_x`, and the target norm is scaling-critical |
| Not claimed | Universal finiteness, global regularity, a new criterion, a novel reduction, or numerical evidence against singularity |
| Support-route class | `CONTINUUM_PROOF` for local derivations; `SOURCE_CITATION` for imported theorems |
| Foundational profile | Continuum PDE over `ℝ`; high pathology risk |
| Certification state | Not certified; source and formalization audits pending |
| First executable step | Audit the exact hypotheses of the implication chain and produce a theorem-by-theorem source ledger |

## 2. Foundational profile

```yaml
foundational_profile:
  carrier_type: continuum
  ambient_structure:
    - real_vector_spaces
    - measure_spaces
    - Banach_spaces
    - Sobolev_spaces
    - distributions
    - nonlinear_partial_differential_equations
  regularity:
    - weak_solution
    - energy_class
    - strong_solution
    - smooth_solution
  axiom_profile:
    base: classical_analysis
    choice_usage: standard_functional_analysis
    excluded_middle: used
    large_cardinal_usage: none
    determinacy_usage: none
  witness_policy:
    existence_claim: literature_derived
    witness_location: analytic_construction_or_source_theorem
  certification_target:
    - human_audit
    - Lean
  pathology_risk:
    level: high
    notes: Weak convergence, concentration, endpoint estimates, solution-class drift, and circular regularity arguments are principal risks.
```

## 3. Lay executive companion

### The object

The velocity field of an incompressible viscous fluid is governed by a diffusion term, which smooths, and a transport term, which can move and concentrate velocity gradients. The energy inequality controls the total kinetic energy and the time-integrated gradient energy.

### The obstruction

Those estimates control the `L⁶` size of velocity only with a square-integrable time exponent. The challenge needs fourth-power time integrability. This is not a minor strengthening: it is exactly invariant under the natural zooming transformation of the equation.

A useful image is a budget that controls the total area under a spike squared. It still permits spikes narrow enough that the area under the fourth power diverges. Navier–Stokes structure may forbid such spikes, but the energy budget alone does not.

### The restricted target

WP00 does not attempt the universal estimate. It establishes the exact logical gap, the theorem chain that would consume the missing estimate, and the obligations that any genuine route must discharge.

### What this package achieves

1. It fixes the equation, domain, norm convention, and initial-data class.
2. It proves the scaling invariance of the target integral.
3. It derives the available `L²_tL⁶_x` estimate from energy and Sobolev.
4. It gives an explicit divergence-free energy-class field showing that these abstract bounds do not imply `L⁴_tL⁶_x`.
5. It separates local proofs from literature-derived regularity theorems.

### What this package does not achieve

It gives no new control of an actual Navier–Stokes solution beyond the standard energy class. The obstruction witness is not a solution of the equation. It rules out an invalid functional-analytic shortcut, not the desired estimate.

## 4. Formal problem statement

### 4.1 Equation and data

Let `ν>0`, let `u₀ ∈ C_c^∞(ℝ³;ℝ³)` satisfy `div u₀=0`, and consider

```math
∂_t u - νΔu + (u·∇)u + ∇p = 0,
\qquad div u=0,
\qquad u|_{t=0}=u₀.
```

The primary campaign is unforced and posed on `ℝ³`. Forced, bounded-domain, and periodic variants require separate hypothesis profiles.

### 4.2 Leray–Hopf working interface

WP00 uses the standard interface:

```math
u ∈ L^∞(0,T;L²(ℝ³)) ∩ L²(0,T;H¹(ℝ³)),
```

with distributional satisfaction of the equation, divergence-free constraint, weak attainment of initial data, and the energy inequality. The exact convention for homogeneous versus inhomogeneous Sobolev spaces and the almost-everywhere form of the energy inequality remain source-audit items.

### 4.3 Target quantity

Define

```math
I_T(u)=∫₀ᵀ ‖u(t)‖_{L⁶(ℝ³)}⁴ dt.
```

The challenge is:

> For every admissible `u₀`, every finite `T>0`, and every Leray–Hopf solution `u` with initial datum `u₀`, is `I_T(u)<∞`?

The quantifier over every Leray–Hopf solution is deliberate. The equivalence to the positive global-regularity branch uses weak–strong uniqueness and must be audited as a bridge, not assumed silently.

### 4.4 Maximal strong-solution companion

Let `u` be the unique maximal strong solution on `[0,T_*)`. The conditional regularity/continuation route predicts:

```math
T_*<∞ \implies ∫₀^{T_*} ‖u(t)‖₆⁴dt=∞.
```

Thus universal finiteness through finite times would exclude finite `T_*`.

## 5. Object and obstruction

### 5.1 What energy gives

For a Leray–Hopf solution, the energy inequality yields, schematically,

```math
sup_{0≤t≤T} ‖u(t)‖₂²
+2ν∫₀ᵀ ‖∇u(t)‖₂²dt
≤ ‖u₀‖₂².
```

The three-dimensional Sobolev inequality gives

```math
‖u(t)‖₆ ≤ C_S ‖∇u(t)‖₂
```

for the appropriate homogeneous-space interpretation. Therefore

```math
∫₀ᵀ ‖u(t)‖₆²dt
≤ C_S²∫₀ᵀ ‖∇u(t)‖₂²dt
≤ C_S²‖u₀‖₂²/(2ν).
```

This proves `u∈L²_tL⁶_x`.

### 5.2 Why finite time does not upgrade the exponent

On a finite-measure interval,

```math
L⁴(0,T) ⊂ L²(0,T),
```

not the reverse inclusion. Hölder can lower an integrability exponent when the measure is finite; it cannot raise it without an additional bound.

### 5.3 Exact energy-space obstruction

Choose a nonzero divergence-free field `φ∈C_c^∞(ℝ³;ℝ³)`. For `0<t<1`, set

```math
λ(t)=t^{-1/3},
\qquad v(t,x)=λ(t)^{3/2}φ(λ(t)x).
```

Spatial rescaling gives

```math
‖v(t)‖₂=‖φ‖₂,
\qquad ‖∇v(t)‖₂=λ(t)‖∇φ‖₂,
\qquad ‖v(t)‖₆=λ(t)‖φ‖₆.
```

Hence

```math
v∈L^∞(0,1;L²_x),
```

and

```math
∫₀¹ ‖∇v(t)‖₂²dt
=‖∇φ‖₂²∫₀¹t^{-2/3}dt<∞.
```

But

```math
∫₀¹ ‖v(t)‖₆⁴dt
=‖φ‖₆⁴∫₀¹t^{-4/3}dt=∞.
```

Therefore

```math
L^∞_tL²_x ∩ L²_tH¹_x \not\subset L⁴_tL⁶_x.
```

This field is not asserted to solve Navier–Stokes. Its sole role is to prove that any successful argument must exploit more equation-specific structure than the energy-space membership itself.

### 5.4 Scaling calculation

For

```math
u_λ(x,t)=λu(λx,λ²t),
```

one has

```math
‖u_λ(t)‖₆
=λ^{1-3/6}‖u(λ²t)‖₆
=λ^{1/2}‖u(λ²t)‖₆.
```

Therefore

```math
∫₀ᵀ ‖u_λ(t)‖₆⁴dt
=∫₀ᵀ λ²‖u(λ²t)‖₆⁴dt
=∫₀^{λ²T} ‖u(s)‖₆⁴ds.
```

The norm is critical: zooming does not create a small prefactor.

## 6. Known terrain and source audit

| Source or result | Claim used here | Audit state | Spine dependency |
|---|---|---|---|
| Leray weak-solution theory | Global energy-class weak solutions exist for finite-energy divergence-free data | `PRIMARY_SOURCE_REQUIRED` | `NS-CI-L002` |
| Prodi 1959 | Conditional uniqueness under a mixed-norm hypothesis | `BIBLIOGRAPHY_IDENTIFIED; THEOREM_TEXT_PENDING` | `NS-CI-L008`, `NS-CI-L009` |
| Serrin 1962 | Interior/conditional regularity in the Ladyzhenskaya–Prodi–Serrin range | `BIBLIOGRAPHY_IDENTIFIED; THEOREM_TEXT_PENDING` | `NS-CI-L008` |
| Ladyzhenskaya 1967 | Smoothness and uniqueness of weak solutions under appropriate integrability | `PRIMARY_TEXT_IDENTIFIED; TRANSLATION_AND_HYPOTHESES_PENDING` | `NS-CI-L008` |
| Fefferman / Clay official statement | Canonical global existence and smoothness problem on `ℝ³` and periodic setting | `OFFICIAL_SOURCE_IDENTIFIED; CORRESPONDENCE_AUDIT_PENDING` | `NS-CI-T011` |
| Standard local strong theory | Smooth data admit a unique local strong solution and maximal-time alternative | `SOURCE_PENDING` | `NS-CI-L010` |
| Weak–strong uniqueness | A Leray–Hopf solution agrees with a strong solution while the latter exists | `SOURCE_PENDING` | `NS-CI-L009` |

No current literature survey is complete at WP00 initialization. In particular, modern quantitative versions, endpoint criteria, Lorentz-space refinements, and domain-dependent statements must not be imported until their exact hypotheses are logged.

## 7. Claim ledger summary and trust quartet

### Claim ledger summary

| Claim ID | Statement | Status | Evidence | Certification state |
|---|---|---|---|---|
| `NS-CI-WP00-C001` | Energy plus Sobolev yields `L²_tL⁶_x` | `PROVED_IN_PACKAGE` | Section 5.1 | Human review pending |
| `NS-CI-WP00-C002` | The energy space is not embedded in `L⁴_tL⁶_x` | `PROVED_IN_PACKAGE` | Section 5.3 | Human review pending |
| `NS-CI-WP00-C003` | `I_T` is invariant under Navier–Stokes scaling | `PROVED_IN_PACKAGE` | Section 5.4 | Human review pending |
| `NS-CI-WP00-C004` | `L⁴_tL⁶_x` control implies regularity/uniqueness | `LITERATURE_DERIVED` | Prodi–Serrin–Ladyzhenskaya source chain | Primary theorem audit pending |
| `NS-CI-WP00-C005` | Universal finiteness resolves the positive global-regularity branch | `NEEDS_AUDIT` | Local theory + C004 + weak–strong uniqueness | Bridge audit pending |
| `NS-CI-WP00-C006` | Universal finiteness is presently open | `LITERATURE_DERIVED` | Official Clay status plus criterion correspondence | Correspondence audit pending |

### What is proved?

The three local calculations C001–C003 are proved directly in this package.

### What is checked?

The bibliography and expected theorem chain have been identified, but exact primary-source hypotheses have not yet been checked line by line.

### What remains open?

The universal estimate `I_T(u)<∞`, any mechanism producing it, and the selection of a nontrivial restricted theorem target.

### What requires external verification?

The precise historical attribution, modern theorem formulation, domain and endpoint assumptions, weak–strong uniqueness bridge, and exact correspondence with the official Millennium formulation.

## 8. Theorem-spine slice and dependency DAG

| Node ID | Role | Statement | Status | Dependencies | Discharge criterion |
|---|---|---|---|---|---|
| `NS-CI-D000` | definition | Equation, data, domain, solution classes | draft | none | source-audited definitions |
| `NS-CI-D001` | definition | Mixed-norm and endpoint convention | draft | D000 | notation audit |
| `NS-CI-L002` | imported lemma | Leray–Hopf energy inequality | needs audit | D000 | primary-source statement logged |
| `NS-CI-L003` | lemma | Sobolev bridge `Ḣ¹→L⁶` | proved locally | D000 | formal or specialist review |
| `NS-CI-C004` | consequence | Energy class implies `L²_tL⁶_x` | proved locally | L002,L003 | review C001 |
| `NS-CI-O005` | obstruction | Energy space does not imply target space | proved locally | D001 | review explicit witness |
| `NS-CI-L006` | lemma | Scaling law | proved locally | D000 | review change of variables |
| `NS-CI-C007` | consequence | Criticality of `I_T` | proved locally | L006,D001 | review C003 |
| `NS-CI-L008` | imported theorem | LPS regularity at `(4,6)` | needs audit | D000,D001 | exact source theorem |
| `NS-CI-L009` | imported theorem | Weak–strong uniqueness | needs audit | D000 | exact source theorem |
| `NS-CI-L010` | bridge | Critical integral blow-up alternative | needs audit | L008,L009,local theory | written proof with hypotheses |
| `NS-CI-T011` | open target | Universal critical integrability | open | C004,O005,C007,L010 | proof or counterexample |
| `NS-CI-R012` | restricted target | First selected tractable theorem | unopened | source audit | scored target-selection record |

The machine-readable form is in `06_DEPENDENCY_DAG.json`.

## 9. Proofs and classified computations

WP00 contains continuum calculations only. It contains no numerical experiment.

- Scaling identity: `CONTINUUM_PROOF`; exact algebra and change of variables.
- Energy-to-mixed-norm estimate: `CONTINUUM_PROOF`; conditional on the standard energy inequality and Sobolev theorem.
- Energy-space non-embedding witness: `NEGATIVE_RESULT`; exact scaling construction.

No floating-point computation supports any claim in this package.

## 10. Failure and negative-result analysis

### Attempted route

Upgrade `L²_tL⁶_x` to `L⁴_tL⁶_x` because the time interval is finite.

### Why it was plausible

Finite-measure spaces do admit inclusions between `L^p` spaces, and it is easy to reverse the direction mentally.

### Smallest exact obstruction

The explicit concentrating field in Section 5.3 lies in the full abstract energy space but not in the target space.

### What the obstruction rules out

Any proof using only membership in `L^∞_tL²_x∩L²_tH¹_x` and generic Banach-space interpolation.

### What it does not rule out

Equation-specific cancellations, pressure–velocity structure, local energy inequalities, vorticity geometry, frequency-localized mechanisms, or a new monotone quantity.

### Next viable restricted problem

Reconstruct the conditional regularity proof at `(4,6)` quantitatively and identify the exact nonlinear estimate whose direction would need to be reversed or closed by new structure.

## 11. Proof-debt register

The machine-readable register is `09_PROOF_DEBT.json`. Principal debts are:

- exact Leray–Hopf convention and source;
- exact LPS theorem at `(4,6)`;
- weak–strong uniqueness hypotheses;
- maximal strong-solution continuation theorem;
- equivalence with the positive Clay branch;
- domain transfer between `ℝ³` and `𝕋³`;
- selection of a non-circular restricted theorem.

## 12. Certification boundary and MATHCERT handoff

### Pencil-and-paper claims suitable for early checking

1. spatial scaling of `L^p` norms;
2. time-change formula for mixed norms;
3. criticality relation `2/q+3/p=1` at `(4,6)`;
4. the energy-space non-embedding witness;
5. implication graph syntax without asserting imported theorem bodies.

### Machine-checked or replayed claims

None yet.

### Exact certificate candidates

Symbolic exponent checks and finite-dimensional Galerkin energy identities may be replayable, but they are infrastructure checks only.

### Formalization blockers

- function-space and Bochner-integral infrastructure;
- divergence-free distributional formulation;
- Sobolev inequalities on `ℝ³`;
- weak-solution semantics;
- imported PDE regularity theorems far beyond initial formal scope.

### First item for MATHCERT

Formalize a generic mixed-norm scaling lemma for smooth compactly supported vector fields and instantiate it at `(q,p)=(4,6)`.

## 13. First executable step

- Input: the primary texts and standard modern references for Leray–Hopf theory, LPS regularity, local strong existence, and weak–strong uniqueness.
- Operation: extract theorem statements verbatim into a source ledger, normalize notation, and prove every arrow in the equivalence diagram with explicit hypotheses.
- Output artifact: `WP00_SOURCE_AND_EQUIVALENCE_AUDIT.md` plus updated claim and debt ledgers.
- Completion test: every imported theorem has a primary or authoritative source, every hypothesis is represented, and the Referee can trace `universal I_T finiteness → global regularity` without an implicit step.
- Spine node advanced: `NS-CI-L010`; debt discharged: `NS-CI-D005`.

## 14. Escalation gate

- [ ] The theorem-spine slice has been externally audited.
- [x] All currently known dependencies are named.
- [x] The initial proof-debt register is present.
- [x] The trust quartet is complete.
- [x] The foundational profile is present.
- [x] The first executable step is explicit.
- [x] The proposed next package names the spine node it advances.

WP01 may be drafted, but it may not be promoted until WP00's source and equivalence audit is complete.