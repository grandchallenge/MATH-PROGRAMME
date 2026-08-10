import CMDGCondensedCM4P2D
import Mathlib.Condensed.Solid
import Mathlib.Condensed.Discrete.Colimit
import Mathlib.Condensed.Discrete.Basic
import Mathlib.CategoryTheory.Adjunction.Unique
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Algebra.Category.ModuleCat.Adjunctions
import Mathlib.CategoryTheory.Functor.KanExtension.Basic
import Mathlib.CategoryTheory.Functor.KanExtension.Pointwise
import Mathlib.LinearAlgebra.Finsupp.Pi
import Mathlib.Algebra.BigOperators.Pi
import Mathlib.Topology.Category.TopCat.ULift

/-!
# CMDG CM4-P2-E comparison reconstruction

This fixture freezes the exact P2-E theorem target after protected admission of P2-D and develops
the basis-free finite algebraic duality core needed for the finite comparison.

No natural equivalence with `Condensed.profiniteSolid` is asserted until the finite condensed
comparison and the measure-side right-Kan-extension property are both constructed.
-/

namespace CMDG.CondensedCM4P2E

universe u

open CategoryTheory
open scoped BigOperators

abbrev R := CMDG.CondensedCM4P2D.R

noncomputable abbrev measureFunctor : Profinite.{u} ⥤ CondensedMod.{u} R :=
  CMDG.CondensedCM4P2D.measureFunctor

noncomputable abbrev solidFunctor : Profinite.{u} ⥤ CondensedMod.{u} R :=
  Condensed.profiniteSolid R

noncomputable abbrev finiteMeasure : FintypeCat.{u} ⥤ CondensedMod.{u} R :=
  FintypeCat.toProfinite ⋙ measureFunctor

noncomputable abbrev finiteFree : FintypeCat.{u} ⥤ CondensedMod.{u} R :=
  Condensed.finFree R

abbrev FiniteComparisonTarget := finiteMeasure ≅ finiteFree
abbrev ComparisonTarget := measureFunctor ≅ solidFunctor

noncomputable def finiteFunctionDualEquiv (X : Type u) [Fintype X] :
    ((X → R) →ₗ[R] R) ≃ₗ[R] (X → R) where
  toFun φ := by
    classical
    exact fun x => φ (Pi.single x (1 : R))
  invFun a :=
    { toFun := fun h => ∑ x, h x * a x
      map_add' := by
        intro f g
        simp [add_mul, Finset.sum_add_distrib]
      map_smul' := by
        intro c f
        simp [Finset.mul_sum, mul_assoc] }
  left_inv φ := by
    classical
    apply LinearMap.ext
    intro h
    change (∑ x, h x * φ (Pi.single x (1 : R))) = φ h
    calc
      (∑ x, h x * φ (Pi.single x (1 : R))) =
          ∑ x, φ (h x • (Pi.single x (1 : R) : X → R)) := by
            apply Finset.sum_congr rfl
            intro x _
            simpa using (φ.map_smul (h x) (Pi.single x (1 : R) : X → R)).symm
      _ = φ (∑ x, h x • (Pi.single x (1 : R) : X → R)) := by
            rw [map_sum]
      _ = φ h := by
            rw [← pi_eq_sum_univ' h]
  right_inv a := by
    classical
    funext x
    change (∑ y, (Pi.single x (1 : R) : X → R) y * a y) = a x
    rw [Fintype.sum_eq_single x (fun y hy => by simp [Pi.single, hy])]
    simp
  map_add' φ ψ := by
    classical
    funext x
    simp
  map_smul' c φ := by
    classical
    funext x
    simp

noncomputable def finiteFunctionDualFreeEquiv (X : Type u) [Fintype X] :
    ((X → R) →ₗ[R] R) ≃ₗ[R] (X →₀ R) :=
  (finiteFunctionDualEquiv X).trans (Finsupp.linearEquivFunOnFinite R R X).symm

noncomputable def discreteSetFreeAdj :
    (Condensed.discrete (Type (u + 1)) ⋙ Condensed.free R) ⊣
      (Condensed.forget R ⋙ Condensed.underlying (Type (u + 1))) :=
  (Condensed.discreteUnderlyingAdj (Type (u + 1))).comp
    (Condensed.freeForgetAdjunction R)

noncomputable def freeDiscreteModuleAdj :
    (ModuleCat.free R ⋙ Condensed.discrete (ModuleCat.{u + 1} R)) ⊣
      (Condensed.underlying (ModuleCat.{u + 1} R) ⋙
        CategoryTheory.forget (ModuleCat.{u + 1} R)) :=
  (ModuleCat.adj R).comp
    (Condensed.discreteUnderlyingAdj (ModuleCat.{u + 1} R))

example :
    Condensed.forget R ⋙ Condensed.underlying (Type (u + 1)) =
      Condensed.underlying (ModuleCat.{u + 1} R) ⋙
        CategoryTheory.forget (ModuleCat.{u + 1} R) := rfl

noncomputable def discreteFreeIso :
    (Condensed.discrete (Type (u + 1)) ⋙ Condensed.free R) ≅
      (ModuleCat.free R ⋙ Condensed.discrete (ModuleCat.{u + 1} R)) :=
  discreteSetFreeAdj.leftAdjointUniq freeDiscreteModuleAdj

noncomputable abbrev finiteUnderlyingULift : FintypeCat.{u} ⥤ Type (u + 1) :=
  FintypeCat.incl ⋙ CategoryTheory.uliftFunctor.{u + 1, u}

example :
    FintypeCat.toProfinite ⋙ Profinite.toTopCat =
      FintypeCat.incl ⋙ TopCat.discrete := rfl

noncomputable def finiteDiscreteULiftIso :
    FintypeCat.toProfinite ⋙ Profinite.toTopCat ⋙ TopCat.uliftFunctor.{u + 1, u} ≅
      finiteUnderlyingULift ⋙ TopCat.discrete :=
  NatIso.ofComponents
    (fun X => by
      letI : DiscreteTopology ↑((finiteUnderlyingULift ⋙ TopCat.discrete).obj X) := ⟨rfl⟩
      exact TopCat.isoOfHomeo
        ((TopCat.uliftFunctorObjHomeo (TopCat.discrete.obj X)).symm.trans
          (Homeomorph.ofDiscrete Equiv.ulift.symm)))
    (by
      intro X Y f
      ext x
      rfl)

noncomputable def discreteTopCondensedIso :
    TopCat.discrete.{u + 1} ⋙ topCatToCondensedSet ≅
      Condensed.discrete (Type (u + 1)) :=
  (CompHausLike.LocallyConstant.functorIso
      (fun _ : TopCat.{u} => True)
      (fun _ _ _ => ((CompHaus.effectiveEpi_tfae _).out 0 2).mp)).symm ≪≫
    CondensedSet.LocallyConstant.iso

noncomputable def finiteDiscreteCondensedIso :
    (FintypeCat.toProfinite ⋙ Profinite.toTopCat ⋙ TopCat.uliftFunctor.{u + 1, u} ⋙
        topCatToCondensedSet) ≅
      (finiteUnderlyingULift ⋙ Condensed.discrete (Type (u + 1))) :=
  Functor.isoWhiskerRight finiteDiscreteULiftIso topCatToCondensedSet ≪≫
    Functor.isoWhiskerLeft finiteUnderlyingULift discreteTopCondensedIso

noncomputable def continuousULiftSectionEquiv (S X : CompHaus.{u}) :
    ULift.{u + 1} (S ⟶ X) ≃ C(S, ↑(TopCat.uliftFunctor.{u + 1, u}.obj X.toTop)) where
  toFun f :=
    { toFun := fun s => (TopCat.uliftFunctorObjHomeo X.toTop) ((ConcreteCategory.hom f.down) s)
      continuous_toFun :=
        (TopCat.uliftFunctorObjHomeo X.toTop).continuous.comp
          (ConcreteCategory.hom f.down).continuous }
  invFun g :=
    ULift.up (ConcreteCategory.ofHom
      { toFun := fun s => (TopCat.uliftFunctorObjHomeo X.toTop).symm (g s)
        continuous_toFun :=
          (TopCat.uliftFunctorObjHomeo X.toTop).symm.continuous.comp g.continuous })
  left_inv f := by
    apply ULift.ext
    apply ConcreteCategory.hom_ext
    intro s
    simp
  right_inv g := by
    ext s
    simp

noncomputable def compHausTopULiftPresheafIso (X : CompHaus.{u}) :
    (compHausToCondensed.obj X).obj ≅
      (topCatToCondensedSet.obj (TopCat.uliftFunctor.{u + 1, u}.obj X.toTop)).obj :=
  NatIso.ofComponents
    (fun (S : CompHaus.{u}ᵒᵖ) =>
      equivEquivIso.{u + 1} (continuousULiftSectionEquiv S.unop X))
    (by
      intro S T f
      ext g s
      rfl)

#check finiteUnderlyingULift
#check finiteDiscreteULiftIso
#check discreteTopCondensedIso
#check finiteDiscreteCondensedIso
#check continuousULiftSectionEquiv
#check compHausTopULiftPresheafIso
#check TopCat.uliftFunctor
#check TopCat.uliftFunctorObjHomeo
#check CompHausLike.LocallyConstant.functorIso
#check CondensedSet.LocallyConstant.iso
#check CMDG.CondensedCM4P2D.measureFunctor
#check CMDG.CondensedCM4P2D.dualityHomEquiv
#check finiteFunctionDualEquiv
#check finiteFunctionDualFreeEquiv
#check discreteSetFreeAdj
#check freeDiscreteModuleAdj
#check discreteFreeIso
#check Condensed.finFree
#check Condensed.profiniteSolid
#check Condensed.profiniteSolidCounit
#check Condensed.profiniteSolidIsPointwiseRightKanExtension
#check Functor.rightKanExtensionUniqueOfIso
#check Functor.rightKanExtensionUnique
#check Condensed.isColimitLocallyConstantPresheafDiagram
#check Condensed.lanPresheafNatIso

#print axioms finiteFunctionDualEquiv
#print axioms finiteFunctionDualFreeEquiv
#print axioms discreteFreeIso
#print axioms finiteDiscreteULiftIso
#print axioms discreteTopCondensedIso
#print axioms finiteDiscreteCondensedIso
#print axioms continuousULiftSectionEquiv
#print axioms compHausTopULiftPresheafIso

end CMDG.CondensedCM4P2E
