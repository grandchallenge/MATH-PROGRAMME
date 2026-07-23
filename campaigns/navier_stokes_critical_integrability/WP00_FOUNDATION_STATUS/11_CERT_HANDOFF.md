# NS-CI-WP00 MATHCERT handoff

## Purpose

This handoff isolates statements that can be checked without pretending to formalize the open global-regularity problem. The initial certification substrate should verify the geometry of the norms and the campaign's implication interfaces, not the universal estimate.

## Certification boundary

### In scope for the first formal slice

1. Spatial scaling of `L^p` norms in dimension three.
2. Scaling of a first spatial derivative in `L²`.
3. Mixed-norm scaling under

   ```math
   u_λ(x,t)=λu(λx,λ²t).
   ```

4. The exponent identity

   ```math
   2/4+3/6=1.
   ```

5. Invariance of

   ```math
   ∫₀ᵀ ‖u_λ(t)‖₆⁴dt
   =∫₀^{λ²T} ‖u(s)‖₆⁴ds.
   ```

6. The abstract concentrating witness showing

   ```math
   L^∞_tL²_x∩L²_tH¹_x \not\subset L⁴_tL⁶_x.
   ```

7. A data structure representing the implication graph:

   ```text
   target estimate
      + imported LPS theorem
      + imported local theory
      + imported weak-strong uniqueness
      -> continuation/global regularity consequence.
   ```

   The imported theorems must remain assumptions or named interfaces until actually formalized.

### Explicitly out of scope

- a proof of universal `L⁴_tL⁶_x` integrability;
- a formalization badge implying the Millennium problem has been reduced or solved;
- encoding a literature theorem as an axiom without visible provenance;
- using a Galerkin trajectory as a witness for a continuum universal statement;
- replacing a weak-solution theorem with a smooth-function theorem while preserving the same public claim.

## Proposed theorem interfaces

The names below are placeholders for a dedicated MATHCERT issue and may change after library reconnaissance.

```lean
-- Schematic only; not asserted to compile.

def NSSpaceTimeScale (λ : ℝ) (u : ℝ → ℝ³ → ℝ³) : ℝ → ℝ³ → ℝ³ :=
  fun t x => λ • u (λ^2 * t) (λ • x)

 theorem lp_space_scaling_dim3
    (p : ℝ) (hp : 0 < p) ... :
    ‖fun x => λ • f (λ • x)‖_{L^p} = |λ|^(1 - 3/p) * ‖f‖_{L^p} := ...

 theorem critical_L4_L6_scaling ... :
    criticalIntegral (NSSpaceTimeScale λ u) T
      = criticalIntegral u (λ^2 * T) := ...

 theorem energy_space_not_embedded_in_critical_space :
    ∃ v,
      v ∈ L∞_tL2_x ∧
      v ∈ L2_tH1_x ∧
      v ∉ L4_tL6_x := ...
```

## Formalization risks

1. Bochner measurability and almost-everywhere equivalence classes can dominate the proof cost.
2. Whole-space Sobolev infrastructure may use conventions that differ from the analytic statement.
3. Real powers and changes of variables require careful positivity hypotheses on `λ`.
4. The explicit witness uses a time-dependent dilation; proving strong measurability may be more costly than the norm calculations.
5. A finite-dimensional surrogate is easier but would certify a different statement. Such a surrogate must not be substituted silently.

## Recommended implementation order

### Stage C0 — library reconnaissance

Record available definitions for:

- `L^p` and Bochner spaces;
- vector-valued integration;
- linear changes of variables in Lebesgue measure;
- divergence and compactly supported smooth vector fields;
- Sobolev spaces on Euclidean space.

Output: `NS_CI_LIBRARY_AUDIT.md` with exact module names and blockers.

### Stage C1 — scalar scaling lemma

Prove a generic scalar `L^p` scaling statement for smooth compactly supported functions and positive `λ`.

Completion test: kernel-checked proof with no placeholders and a regression example at `p=2` and `p=6`.

### Stage C2 — mixed-norm criticality

Add time rescaling and instantiate at `(q,p)=(4,6)`.

Completion test: the final exponent reduces exactly to zero and the theorem states interval rescaling explicitly.

### Stage C3 — obstruction witness

Attempt the continuum witness. If library cost is excessive, write an ADR that keeps C002 human-audited and explains why a weaker finite-dimensional statement would not certify it.

### Stage C4 — imported theorem interface

Represent the LPS criterion, local theory, and weak–strong uniqueness as provenance-bearing assumptions in an implication theorem. The resulting theorem may certify the logic of the bridge while leaving the imported analytic theorems unformalized.

## Acceptance criteria

- Every formal theorem has a claim-ledger identifier.
- Every assumption representing literature has a source identifier and visible `UNFORMALIZED_IMPORT` status.
- No `axiom` or unchecked placeholder is hidden by generated code.
- Build and theorem-prover versions are pinned.
- Negative tests detect exponent, dimension, and interval-scaling errors.
- Public wording remains within claim `NS-CI-WP00-C007`.

## First MATHCERT task

Formalize and test the mixed-norm scaling identity for smooth compactly supported fields under positive dilation, ending with the exact `(4,6)` critical case. This advances `NS-CI-C007` and does not depend on solving any PDE.