import CMDGCondensedCM4P3DerivedCM5R0CechKernelRelation
import CMDGCondensedCM4P3DerivedCM5R0StoneanEffectiveDescent
import Mathlib.CategoryTheory.EffectiveEpi.Preserves
import Mathlib.CategoryTheory.Preadditive.Basic
import Mathlib.Algebra.Homology.ShortComplex.Exact

/-!
# CM5: Čech relations generate the actual Stonean presentation kernel

For any (possibly infinite) profinite T, the canonical Stonean cover
P(T) → T is an effective epi. The profinite Yoneda embedding
preserves both effective epis and pullbacks. Consequently the
resulting diagram from P(T)×_T P(T) coequalizes onto T in
CondensedSet. The free condensed-module functor, being left
adjoint to forgetting the module structure, preserves that
coequalizer. In the abelian category CondensedMod ZLift it
is a cokernel of the difference of the two Čech arrows, hence
the exactness condition implies that the canonical relation-to-
kernel map is an epimorphism.

No finite-profinite restriction, no statement that every cocycle
admits a potential, and no Ext¹ vanishing are used here.
-/

noncomputable section

universe u

open CategoryTheory Limits CategoryTheory.Functor

namespace CMDG.CondensedCM5R0

/-- The actual Yoneda image of the Stonean presentation has the
canonical regular epi diagram from the genuine profinite Čech
fiber product. -/
noncomputable def stoneanCechRegularEpiCondensed
    (T : Profinite.{u}) :
    RegularEpi (profiniteToCondensed.map (Profinite.presentation.π T)) := by
  letI : EffectiveEpi (Profinite.presentation.π T) :=
    stoneanPresentation_effectiveEpi_profinite T
  letI : PreservesEffectiveEpis profiniteToCondensed := inferInstance
  exact regularEpiOfPreserves
    (Profinite.presentation.π T) profiniteToCondensed
    (pullback.cone _ _) (pullback.isLimit _ _)

/-- The free condensed-module presentation is the cokernel of
the actual difference of the two free Čech arrows. -/
noncomputable def stoneanCechFreeCokernel
    (T : Profinite.{u}) :
    IsColimit (CokernelCofork.ofπ
      (freeStoneanPresentationMap T)
      (stoneanCechDifference_comp_zero T)) := by
  let h := stoneanCechRegularEpiCondensed T
  letI := (Condensed.freeForgetAdjunction Coeff).leftAdjoint_preservesColimits
  have hco' : IsColimit (Cofork.ofπ
      (freeStoneanPresentationMap T)
      (by
        change ((Condensed.profiniteFree Coeff).map
            (pullback.fst (Profinite.presentation.π T) (Profinite.presentation.π T))) ≫
          freeStoneanPresentationMap T =
          ((Condensed.profiniteFree Coeff).map
            (pullback.snd (Profinite.presentation.π T) (Profinite.presentation.π T))) ≫
          freeStoneanPresentationMap T
        have hh := stoneanCechDifference_comp_zero T
        unfold stoneanCechDifference at hh
        simpa only [Preadditive.sub_comp, sub_eq_zero] using hh)) := by
    exact isColimitCoforkMapOfIsColimit
      (Condensed.free Coeff) h.w h.isColimit
  have hck := Preadditive.isColimitCokernelCoforkOfCofork hco'
  simpa only [Preadditive.cokernelCoforkOfCofork_ofπ] using hck

/-- **Unconditional**: for every profinite T the canonical map
from the actual free Čech relation object to the kernel K_T
is epic in CondensedMod ZLift. -/
theorem stoneanCechRelationToKernel_epi
    (T : Profinite.{u}) :
    Epi (stoneanCechRelationToKernel T) := by
  let sc : ShortComplex Ambient :=
    ShortComplex.mk (stoneanCechDifference T)
      (freeStoneanPresentationMap T)
      (stoneanCechDifference_comp_zero T)
  have hx : sc.Exact :=
    sc.exact_of_g_is_cokernel (stoneanCechFreeCokernel T)
  exact (sc.exact_iff_epi_kernel_lift).mp hx

#print axioms stoneanCechRegularEpiCondensed
#print axioms stoneanCechFreeCokernel
#print axioms stoneanCechRelationToKernel_epi

end CMDG.CondensedCM5R0
