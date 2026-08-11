import CMDGCondensedCM4P2EFiniteFreeTransport
import Mathlib.LinearAlgebra.Finsupp.LSum

/-!
# CMDG CM4-P2-E E1 — canonical finite natural comparison

This fixture closes E1 by lifting the certified finite presheaf comparison to condensed modules,
identifying locally-constant modules with discrete modules, and transporting the canonical small
finite free module across the universe lift. The terminal declaration has exactly the frozen E1
target

`FintypeCat.toProfinite ⋙ measureFunctor ≅ Condensed.finFree R`.

No E2 right-Kan-extension statement or global P2-E equivalence is asserted here.
-/

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
attribute [local instance] FintypeCat.fintype

abbrev R := CMDG.CondensedCM4P2D.R.{u}

/-- The canonical small finite free module, realized directly as a condensed module of locally
constant sections. -/
noncomputable abbrev finiteSmallFreeCondensedFunctor :
    FintypeCat.{u} ⥤ CondensedMod.{u} R :=
  CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule ⋙
    CondensedMod.LocallyConstant.functor R

/-- Objectwise lift of the certified finite presheaf comparison to the full subcategory of sheaves. -/
noncomputable def finiteMeasureSmallFreeCondensedIso (X : FintypeCat.{u}) :
    CMDG.CondensedCM4P2E.finiteMeasure.obj X ≅
      finiteSmallFreeCondensedFunctor.obj X :=
  ObjectProperty.isoMk
    (Presheaf.IsSheaf (coherentTopology CompHaus.{u}))
    (finiteMeasureSmallFreePresheafNatIso.app X)

/-- The presheaf-level finite comparison lifts naturally to condensed modules. -/
noncomputable def finiteMeasureSmallFreeCondensedNatIso :
    CMDG.CondensedCM4P2E.finiteMeasure ≅ finiteSmallFreeCondensedFunctor :=
  NatIso.ofComponents
    (fun X => finiteMeasureSmallFreeCondensedIso X)
    (by
      intro X Y f
      apply ObjectProperty.hom_ext
      change
        finiteMeasurePresheafFunctor.map f ≫
            (finiteMeasureSmallFreePresheafNatIso.app Y).hom =
          (finiteMeasureSmallFreePresheafNatIso.app X).hom ≫
            finiteSmallFreePresheafFunctor.map f
      exact finiteMeasureSmallFreePresheafNatIso.hom.naturality f)

/-- Replace locally-constant condensed modules by the canonically isomorphic discrete condensed
modules. -/
noncomputable def finiteSmallFreeCondensedDiscreteNatIso :
    finiteSmallFreeCondensedFunctor ≅
      (CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule ⋙
        Condensed.discrete (ModuleCat.{u + 1} R)) :=
  Functor.isoWhiskerLeft
    CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule
    (CondensedMod.LocallyConstant.functorIsoDiscrete R)

/-- Canonical universe transport on the free module: relabel a finitely-supported function by
`X ≃ ULift X`. -/
noncomputable def finiteSmallFreeULiftLinearEquiv (X : FintypeCat.{u}) :
    (X.obj →₀ R) ≃ₗ[R] (ULift.{u + 1, u} X.obj →₀ R) :=
  Finsupp.domLCongr Equiv.ulift.symm

/-- The corresponding module isomorphism. -/
noncomputable def finiteSmallFreeULiftIso (X : FintypeCat.{u}) :
    CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule.obj X ≅
      (CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙ ModuleCat.free R).obj X :=
  (finiteSmallFreeULiftLinearEquiv X).toModuleIso

@[simp]
lemma finiteSmallFreeULiftLinearEquiv_single
    (X : FintypeCat.{u}) (x : X.obj) (r : R) :
    finiteSmallFreeULiftLinearEquiv X (Finsupp.single x r) =
      Finsupp.single (ULift.up x) r := by
  exact Finsupp.domLCongr_single Equiv.ulift.symm x r

/-- The universe transport is natural in finite maps. -/
noncomputable def finiteSmallFreeULiftNatIso :
    CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule ≅
      (CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙ ModuleCat.free R) :=
  NatIso.ofComponents
    (fun X => finiteSmallFreeULiftIso X)
    (by
      intro X Y f
      apply ModuleCat.hom_ext
      apply Finsupp.lhom_ext
      intro x r
      change
        finiteSmallFreeULiftLinearEquiv Y
            (Finsupp.lmapDomain R R (fun z => f z) (Finsupp.single x r)) =
          Finsupp.lmapDomain R R (fun z => ULift.map f z)
            (finiteSmallFreeULiftLinearEquiv X (Finsupp.single x r))
      simp only [Finsupp.lmapDomain_apply, Finsupp.mapDomain_single,
        finiteSmallFreeULiftLinearEquiv_single]
      rfl)

/-- Apply the canonical universe transport under the discrete condensed-module functor. -/
noncomputable def finiteSmallFreeDiscreteULiftNatIso :
    (CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule ⋙
      Condensed.discrete (ModuleCat.{u + 1} R)) ≅
      (CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙ ModuleCat.free R ⋙
        Condensed.discrete (ModuleCat.{u + 1} R)) :=
  Functor.isoWhiskerRight
    finiteSmallFreeULiftNatIso
    (Condensed.discrete (ModuleCat.{u + 1} R))

/-- E1: the protected P2-D finite restriction is canonically and naturally the pinned finite-free
condensed-module functor. -/
noncomputable def finiteComparisonNatIso :
    CMDG.CondensedCM4P2E.FiniteComparisonTarget :=
  finiteMeasureSmallFreeCondensedNatIso ≪≫
    finiteSmallFreeCondensedDiscreteNatIso ≪≫
    finiteSmallFreeDiscreteULiftNatIso ≪≫
    CMDG.CondensedCM4P2E.finiteFreeDiscreteIso.symm

example :
    FintypeCat.toProfinite ⋙ CMDG.CondensedCM4P2D.measureFunctor ≅
      Condensed.finFree R :=
  finiteComparisonNatIso

#check finiteSmallFreeCondensedFunctor
#check finiteMeasureSmallFreeCondensedIso
#check finiteMeasureSmallFreeCondensedNatIso
#check finiteSmallFreeCondensedDiscreteNatIso
#check finiteSmallFreeULiftLinearEquiv
#check finiteSmallFreeULiftIso
#check finiteSmallFreeULiftNatIso
#check finiteSmallFreeDiscreteULiftNatIso
#check finiteComparisonNatIso

#print axioms finiteMeasureSmallFreeCondensedIso
#print axioms finiteMeasureSmallFreeCondensedNatIso
#print axioms finiteSmallFreeCondensedDiscreteNatIso
#print axioms finiteSmallFreeULiftLinearEquiv
#print axioms finiteSmallFreeULiftIso
#print axioms finiteSmallFreeULiftNatIso
#print axioms finiteSmallFreeDiscreteULiftNatIso
#print axioms finiteComparisonNatIso

end CMDG.CondensedCM4P2E.FiniteDualTransport
