import CMDGCondensedCM4P3DerivedCM5R0PointwiseShortExactTransfer
import CMDGCondensedCM4P3DerivedCM5R0RealCircleCondensedComplex
import CMDGCondensedCM4P3DerivedCM5R0RealCircleStoneanExact
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat

noncomputable section
universe u
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.RealCircleStonean
open CMDG.CondensedCM5R0.RealCircleStoneanPresheaf

namespace CMDG.CondensedCM5R0.RealCircleSheafExact

variable (I : Type u)
local instance (I : Type u) : IsTopologicalAddGroup (ULift.{u+1,u} (I → UnitAddCircle)) := ⟨⟩

def presheafSeq :
    ShortComplex (Stonean.{u}ᵒᵖ ⥤ ModuleCat.{u+1} (ULift.{u+1} ℤ)) :=
  ShortComplex.mk
    (postcomposeNatTrans (ULift.{u+1,u} (I → ℤ))
      (intProductTopHom I) (intProductTopHom_continuous I))
    (postcomposeNatTrans (ULift.{u+1,u} (I → ℝ))
      (realProductTopHom I) (realProductTopHom_continuous I))
    (postcomposeNatTrans_comp_zero
      (ULift.{u+1,u} (I → ℤ))
      (intProductTopHom I) (intProductTopHom_continuous I)
      (realProductTopHom I) (realProductTopHom_continuous I)
      (realProductTopHom_comp_intProductTopHom I))

theorem realToCircle_probe_surjective (S : Stonean.{u}) :
    Function.Surjective
      (postcomposeAddHom (ULift.{u+1,u} (I → ℝ))
        (realProductTopHom I) (realProductTopHom_continuous I) S) := by
  intro f
  let f0 : C(S,I→UnitAddCircle) :=
    ⟨fun x => (f x).down, continuous_uliftDown.comp f.continuous⟩
  obtain ⟨g0,hg0⟩ := torus_map_has_continuous_real_lift S I f0
  let g : C(S,ULift.{u+1,u} (I→ℝ)) :=
    ⟨fun x => ⟨g0 x⟩,continuous_uliftUp.comp g0.continuous⟩
  refine ⟨g, ?_⟩
  apply ContinuousMap.ext
  intro x
  apply ULift.ext
  funext i
  exact hg0 x i

#print axioms realToCircle_probe_surjective

theorem intToReal_probe_injective (S : Stonean.{u}) :
    Function.Injective
      (postcomposeAddHom (ULift.{u+1,u} (I → ℤ))
        (intProductTopHom I) (intProductTopHom_continuous I) S) := by
  intro f g h
  apply ContinuousMap.ext
  intro x
  apply ULift.ext
  funext i
  have hi := congrArg
    (fun k : C(S,ULift.{u+1,u} (I → ℝ)) => (k x).down i) h
  change (((f x).down i : ℤ) : ℝ) =
    (((g x).down i : ℤ) : ℝ) at hi
  exact_mod_cast hi

#print axioms intToReal_probe_injective

theorem realToCircle_probe_kernel_lifts_integer (S : Stonean.{u})
    (g : C(S, ULift.{u+1,u} (I → ℝ)))
    (hg : postcomposeAddHom (ULift.{u+1,u} (I → ℝ))
        (realProductTopHom I) (realProductTopHom_continuous I) S g = 0) :
    ∃ z : C(S,ULift.{u+1,u} (I→ℤ)),
      postcomposeAddHom (ULift.{u+1,u} (I → ℤ))
        (intProductTopHom I) (intProductTopHom_continuous I) S z = g := by
  let g0 : C(S,I→ℝ) :=
    ⟨fun x => (g x).down,continuous_uliftDown.comp g.continuous⟩
  have h0 : realToCircle S I g0 = 0 := by
    apply ContinuousMap.ext
    intro x
    funext i
    have hi := congrArg
      (fun k : C(S,ULift.{u+1,u} (I → UnitAddCircle)) => (k x).down i) hg
    exact hi
  obtain ⟨z0,hz0⟩ := realToCircle_kernel_lifts_integer S I g0 h0
  let z : C(S,ULift.{u+1,u} (I→ℤ)) :=
    ⟨fun x => ⟨z0 x⟩,continuous_uliftUp.comp z0.continuous⟩
  refine ⟨z, ?_⟩
  apply ContinuousMap.ext
  intro x
  apply ULift.ext
  funext i
  have hi := congrArg (fun k : C(S,I→ℝ) => k x i) hz0
  exact hi

#print axioms realToCircle_probe_kernel_lifts_integer

theorem presheafSeq_pointwise_shortExact (S : Stonean.{u}ᵒᵖ) :
    ((presheafSeq I).map
      ((evaluation Stonean.{u}ᵒᵖ
        (ModuleCat.{u+1} (ULift.{u+1} ℤ))).obj S)).ShortExact := by
  apply ShortComplex.ShortExact.mk'
  · apply (ShortComplex.moduleCat_exact_iff _).2
    intro g hg
    change postcomposeAddHom (ULift.{u+1,u} (I → ℝ))
        (realProductTopHom I) (realProductTopHom_continuous I)
        S.unop g = 0 at hg
    obtain ⟨z,hz⟩ :=
      realToCircle_probe_kernel_lifts_integer I S.unop g hg
    exact ⟨z,hz⟩
  · apply (ModuleCat.mono_iff_injective _).2
    exact intToReal_probe_injective I S.unop
  · apply (ModuleCat.epi_iff_surjective _).2
    exact realToCircle_probe_surjective I S.unop

theorem presheafSeq_shortExact :
    (presheafSeq I).ShortExact :=
  CMDG.CondensedCM5R0.CategoryExactness.shortExact_of_pointwise
    (presheafSeq I) (presheafSeq_pointwise_shortExact I)

#print axioms presheafSeq_pointwise_shortExact
#print axioms presheafSeq_shortExact

#check presheafSeq
end CMDG.CondensedCM5R0.RealCircleSheafExact
