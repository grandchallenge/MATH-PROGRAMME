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

/-- For any profinite T, the actual free condensed-module presentation
is the cokernel of its explicit Čech difference map. The proof uses
the effective-epi structure of this *specific* Stonean cover, not
a typeclass claim about preserving every effective epimorphism. -/
noncomputable def stoneanCechFreeCokernel
    (T : Profinite.{u}) :
    IsColimit (CokernelCofork.ofπ
      (freeStoneanPresentationMap T)
      (stoneanCechDifference_comp_zero T)) := by
  let f := Profinite.presentation.π T
  let c : PullbackCone f f := pullback.cone f f
  have hc : IsLimit c := pullback.isLimit _ _
  letI : EffectiveEpi (profiniteToCondensed.map f) :=
    stoneanPresentation_effectiveEpi_condensed T
  haveI : PreservesLimitsOfShape WalkingCospan compHausToCondensed := by
    change PreservesLimitsOfShape WalkingCospan
      ((coherentTopology CompHaus).uliftYoneda)
    infer_instance
  haveI : PreservesLimitsOfShape WalkingCospan profiniteToCondensed := by
    change PreservesLimitsOfShape WalkingCospan
      (profiniteToCompHaus ⋙ compHausToCondensed)
    infer_instance
  let cp : PullbackCone (profiniteToCondensed.map f)
      (profiniteToCondensed.map f) :=
    PullbackCone.mk (profiniteToCondensed.map c.fst)
      (profiniteToCondensed.map c.snd)
      (by simp [← Functor.map_comp, c.condition])
  have hcp : IsLimit cp := by
    refine IsLimit.equivOfNatIsoOfIso ?_ _ _ ?_
      (isLimitOfPreserves profiniteToCondensed hc)
    · exact cospanIsoMk (Iso.refl _) (Iso.refl _) (Iso.refl _)
    · exact Cone.ext (Iso.refl _) <| by
        rintro (_ | _ | _) <;> cat_disch
  have hco : IsColimit (Cofork.ofπ
      (profiniteToCondensed.map f) cp.condition) :=
    isColimitCoforkOfEffectiveEpi (profiniteToCondensed.map f) cp hcp
  letI := (Condensed.freeForgetAdjunction Coeff).leftAdjoint_preservesColimits
  have hfree := isColimitCoforkMapOfIsColimit
    (Condensed.free Coeff) cp.condition hco
  have hfree' : IsColimit (Cofork.ofπ
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
    simpa [f, c, cp, PullbackCone.mk_fst, PullbackCone.mk_snd,
      freeStoneanPresentationMap, Condensed.profiniteFree,
      Functor.comp_map] using hfree
  have hck := Preadditive.isColimitCokernelCoforkOfCofork hfree'
  simpa only [Preadditive.cokernelCoforkOfCofork_ofπ,
    stoneanCechDifference] using hck

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

#print axioms stoneanCechFreeCokernel
#print axioms stoneanCechRelationToKernel_epi

end CMDG.CondensedCM5R0
