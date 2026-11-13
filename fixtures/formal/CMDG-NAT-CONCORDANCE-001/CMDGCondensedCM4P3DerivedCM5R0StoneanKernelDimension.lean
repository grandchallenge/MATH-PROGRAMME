import CMDGCondensedCM4P3DerivedCM5R0StoneanPresentation
import Mathlib.CategoryTheory.Abelian.Projective.Dimension

/-!
# CM5: exact Stonean presentation and the remaining kernel obstruction

Every profinite T admits a canonical Stonean projective epimorphism
P_T → F_T, established in the preceding module. Its kernel K_T
gives a short exact sequence in the actual condensed-module category.

We isolate a conditional but nontrivial consequence: projectivity of
K_T would bound the projective dimension of F_T by one, hence force
vanishing of Ext in degrees ≥ 2. Neither projectivity of K_T nor the
degree-one Ext vanishing is assumed or claimed for arbitrary profinite T.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The kernel of the actual Stonean free-module presentation. -/
noncomputable abbrev stoneanPresentationKernel (T : Profinite.{u}) : Ambient :=
  kernel (freeStoneanPresentationMap T)

/-- Canonical kernel-to-projective-to-free short complex. -/
noncomputable abbrev stoneanPresentationShortComplex (T : Profinite.{u}) :
    ShortComplex Ambient :=
  ShortComplex.mk
    (kernel.ι (freeStoneanPresentationMap T))
    (freeStoneanPresentationMap T)
    (kernel.condition (freeStoneanPresentationMap T))

/-- This is a genuine short exact sequence for every profinite T,
with no finite or Stonean restriction on T. -/
theorem stoneanPresentationShortExact (T : Profinite.{u}) :
    (stoneanPresentationShortComplex T).ShortExact := by
  letI : Epi (freeStoneanPresentationMap T) :=
    freeStoneanPresentationMap_epi T
  exact { exact := ShortComplex.exact_kernel _ }

/-- The next mathematical hypothesis is precisely the projectivity
of the Stonean presentation kernel. If it holds, the free object has
projective dimension at most one in condensed modules. -/
theorem freeProfinite_projectiveDimensionLE_one_of_kernel_projective
    (T : Profinite.{u})
    [Projective (stoneanPresentationKernel T)] :
    HasProjectiveDimensionLE ((Condensed.profiniteFree Coeff).obj T) 1 := by
  have h : (stoneanPresentationShortComplex T).ShortExact :=
    stoneanPresentationShortExact T
  have hK : HasProjectiveDimensionLT (stoneanPresentationKernel T) 1 := by
    infer_instance
  have hP : HasProjectiveDimensionLT
      ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) 2 := by
    letI := freeStoneanPresentation_source_projective T
    infer_instance
  exact h.hasProjectiveDimensionLT_X₃ 1 hK hP

/-- Under that *explicit* kernel-projectivity hypothesis, all
ordinary positive-degree-2-and-up Ext groups in the condensed
category vanish. No degree-one claim is made. -/
theorem freeProfinite_extHigher_eq_zero_of_kernel_projective
    (T : Profinite.{u}) (A : Ambient) (n : ℕ)
    [Projective (stoneanPresentationKernel T)]
    (e : Abelian.Ext ((Condensed.profiniteFree Coeff).obj T) A (n + 2)) :
    e = 0 := by
  letI : HasProjectiveDimensionLE ((Condensed.profiniteFree Coeff).obj T) 1 :=
    freeProfinite_projectiveDimensionLE_one_of_kernel_projective T
  exact e.eq_zero_of_hasProjectiveDimensionLT 2 (by omega)

#print axioms stoneanPresentationShortExact
#print axioms freeProfinite_projectiveDimensionLE_one_of_kernel_projective
#print axioms freeProfinite_extHigher_eq_zero_of_kernel_projective

end CMDG.CondensedCM5R0
