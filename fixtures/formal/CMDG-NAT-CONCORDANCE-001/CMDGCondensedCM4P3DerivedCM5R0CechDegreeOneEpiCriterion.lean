import CMDGCondensedCM4P3DerivedCM5R0CechPresheafFaceComparison
import Mathlib.CategoryTheory.Abelian.Exact

/-!
# CMDG CM5 — exact degree-one Čech criterion for the ACTUAL second syzygy

For arbitrary profinite T, let d₂ : F_Q → F_R be the true triple
alternating differential and d₁ : F_R → F_P be the true difference.
Let r : F_R → K_T be the already-protected genuine Čech relation epi,
and let i : K_T ↪ F_P be the presentation kernel inclusion.

Since d₁ = r ≫ i, and i is mono, the short complexes
  (F_Q --d₂--> F_R --r--> K_T)
  (F_Q --d₂--> F_R --d₁--> F_P)
have equivalent exactness at their shared middle term.

The first complex's canonical kernel lift is exactly the genuine
map F_Q → L_T. Hence we prove the genuine equivalence:

  Exact(F_Q → F_R → F_P)
    IFF Epi(F_Q → L_T).

This is a non-vacuous bridge: the first side is the degree-one
homological exactness to be proved by Stonean presheaf descent;
the second side is the actual CM5 arbitrary-profinite target,
not a new abstract kernel or an assumed epimorphism.

The present file does NOT assert the first side without a proof.
Consequently no unconditional global epi, Ext² vanishing or
derived solidity is claimed. No new axioms or sorry are used.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The genuine degree-one Čech complex at the free presheaf
sheafification target, using actual first and second differentials. -/
noncomputable abbrev stoneanCechDegreeOneComplex (T : Profinite.{u}) :
    ShortComplex Ambient :=
  ShortComplex.mk (stoneanCechTripleBoundary T)
    (stoneanCechDifference T) (by
      rw [← stoneanCechRelationToKernel_comp_ι, ← Category.assoc,
        stoneanCechTripleBoundary_comp_relation_zero]
      simp)

/-- The same source/degree-one relation, with true kernel K_T as
its right term. This is not the second-syzygy kernel L_T. -/
noncomputable abbrev stoneanCechDegreeOneKernelComplex (T : Profinite.{u}) :
    ShortComplex Ambient :=
  ShortComplex.mk (stoneanCechTripleBoundary T)
    (stoneanCechRelationToKernel T)
    (stoneanCechTripleBoundary_comp_relation_zero T)

/-- The factorization of genuine degree-one complexes along
the original monomorphism K_T → F_{P(T)}. -/
noncomputable abbrev stoneanCechKernelComplexComparison (T : Profinite.{u}) :
    stoneanCechDegreeOneKernelComplex T ⟶
      stoneanCechDegreeOneComplex T :=
  ShortComplex.homMk
    (𝟙 _) (𝟙 _) (kernel.ι (freeStoneanPresentationMap T))
    (by simp)
    (by simpa only [Category.id_comp]
      using (stoneanCechRelationToKernel_comp_ι T).symm)

/-- Exactness of d₂,d₁ in the **real condensed module category**
is equivalent to exactness of d₂,r, because r factors d₁ through
a monic K_T ↪ F_P. -/
theorem stoneanCechDegreeOneExact_iff_kernelComplexExact
    (T : Profinite.{u}) :
    (stoneanCechDegreeOneComplex T).Exact ↔
      (stoneanCechDegreeOneKernelComplex T).Exact := by
  haveI : Epi (stoneanCechKernelComplexComparison T).τ₁ := by
    change Epi (𝟙 ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)))
    infer_instance
  haveI : IsIso (stoneanCechKernelComplexComparison T).τ₂ := by
    change IsIso (𝟙 ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechPairs T)))
    infer_instance
  haveI : Mono (stoneanCechKernelComplexComparison T).τ₃ := by
    change Mono (kernel.ι (freeStoneanPresentationMap T))
    infer_instance
  exact (ShortComplex.exact_iff_of_epi_of_isIso_of_mono
    (stoneanCechKernelComplexComparison T)).symm

/-- The exact non-conditional algebraic criterion for global
Čech relation generation. On its RHS is the actual protected
F_triples → L_T map. The remaining research obligation is to
derive the LHS from sheafified Stonean-probe exactness. -/
theorem stoneanCechTripleToSecondRelation_epi_iff_degreeOneExact
    (T : Profinite.{u}) :
    Epi (stoneanCechTripleToSecondRelation T) ↔
      (stoneanCechDegreeOneComplex T).Exact := by
  rw [stoneanCechDegreeOneExact_iff_kernelComplexExact]
  exact (stoneanCechDegreeOneKernelComplex T).exact_iff_epi_kernel_lift.symm

/-- Forward direction explicitly establishes the genuine target
from a proof of global degree-one Čech exactness. -/
theorem stoneanCechTripleToSecondRelation_epi_of_degreeOneExact
    (T : Profinite.{u}) (h : (stoneanCechDegreeOneComplex T).Exact) :
    Epi (stoneanCechTripleToSecondRelation T) :=
  (stoneanCechTripleToSecondRelation_epi_iff_degreeOneExact T).2 h

#check stoneanCechTripleToSecondRelation_epi_iff_degreeOneExact
#print axioms stoneanCechDegreeOneExact_iff_kernelComplexExact
#print axioms stoneanCechTripleToSecondRelation_epi_iff_degreeOneExact
#print axioms stoneanCechTripleToSecondRelation_epi_of_degreeOneExact

end CMDG.CondensedCM5R0
