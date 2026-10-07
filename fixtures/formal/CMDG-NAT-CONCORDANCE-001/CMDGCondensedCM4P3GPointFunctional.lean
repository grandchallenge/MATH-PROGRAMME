import CMDGCondensedCM4P3MFiniteQuotientBridge
import CMDGCondensedCM4P3E
import Mathlib.Condensed.Discrete.Characterization
import CMDGCondensedCM4P3G
import CMDGCondensedCM4P3GFiniteBooleanMeasureHom

/-!
# CMDG CM4-P3-G point-functional bridge

This successor module exposes the one-point component of the protected measure model as an
ordinary linear functional on locally constant coefficient functions. It adds no solidity claim:
the purpose is to give the subsequent Nöbeling/Boolean separation argument a concrete scalar
interface while preserving the certified P3-G reduction unchanged.
-/

namespace CMDG.CondensedCM4P3G.PointFunctional

universe u

open CategoryTheory Limits Opposite
open scoped CategoryTheory.MonoidalClosed

abbrev R := CMDG.CondensedCM4P3G.R.{u}
abbrev PresheafModule := CMDG.CondensedCM4P2D.PresheafModule.{u}

noncomputable abbrev measurePresheafObj (X : Profinite.{u}) : PresheafModule :=
  CMDG.CondensedCM4P2D.measurePresheafObj X

noncomputable abbrev sourcePresheaf (X : Profinite.{u}) : PresheafModule :=
  CMDG.CondensedCM4P2D.discreteContinuousPresheaf.obj (op X)

noncomputable abbrev coefficientPresheaf : PresheafModule :=
  CMDG.CondensedCM4P2D.coefficientPresheaf

noncomputable local instance : MonoidalClosed PresheafModule :=
  MonoidalClosed.FunctorCategory.monoidalClosed

abbrev Point := CompHaus.of PUnit.{u + 1}

noncomputable def pointIdentity : Under (op Point) :=
  Under.mk (𝟙 (op Point))

/-- Evaluate a one-point section of the measure internal-Hom at the identity object of the
under-category. The result is the corresponding module morphism between the one-point source
and coefficient sections. -/
noncomputable def measurePointProjection
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point)) :
    (Under.forget (op Point) ⋙ sourcePresheaf X).obj pointIdentity ⟶
      (Under.forget (op Point) ⋙ coefficientPresheaf).obj pointIdentity := by
  exact (ConcreteCategory.hom
    (CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
      (ModuleCat.{u + 1} R)
      (Under.forget (op Point) ⋙ sourcePresheaf X)
      (Under.forget (op Point) ⋙ coefficientPresheaf)
      pointIdentity)) μ

noncomputable def measurePointProjectionAt
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point))
    (k : Under (op Point)) :
    (Under.forget (op Point) ⋙ sourcePresheaf X).obj k ⟶
      (Under.forget (op Point) ⋙ coefficientPresheaf).obj k := by
  exact (ConcreteCategory.hom
    (CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
      (ModuleCat.{u + 1} R)
      (Under.forget (op Point) ⋙ sourcePresheaf X)
      (Under.forget (op Point) ⋙ coefficientPresheaf)
      k)) μ

lemma measurePointProjectionAt_identity
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point)) :
    measurePointProjectionAt X μ pointIdentity = measurePointProjection X μ := by
  rfl

lemma measurePointProjection_condition
    (X : Profinite.{u}) {i j : Under (op Point)} (f : i ⟶ j) :
    CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
          (ModuleCat.{u + 1} R)
          (Under.forget (op Point) ⋙ sourcePresheaf X)
          (Under.forget (op Point) ⋙ coefficientPresheaf)
          i ≫
        (ihom ((Under.forget (op Point) ⋙ sourcePresheaf X).obj i)).map
          ((Under.forget (op Point) ⋙ coefficientPresheaf).map f) =
      CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
          (ModuleCat.{u + 1} R)
          (Under.forget (op Point) ⋙ sourcePresheaf X)
          (Under.forget (op Point) ⋙ coefficientPresheaf)
          j ≫
        (MonoidalClosed.pre
          ((Under.forget (op Point) ⋙ sourcePresheaf X).map f)).app
            ((Under.forget (op Point) ⋙ coefficientPresheaf).obj j) := by
  simpa only [
      MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerLeft,
      MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerRight] using
    (CategoryTheory.Enriched.FunctorCategory.enrichedHom_condition
      (ModuleCat.{u + 1} R)
      (Under.forget (op Point) ⋙ sourcePresheaf X)
      (Under.forget (op Point) ⋙ coefficientPresheaf)
      f)

lemma measurePointProjectionAt_naturality
    (X : Profinite.{u}) {i j : Under (op Point)} (f : i ⟶ j)
    (μ : (measurePresheafObj X).obj (op Point)) :
    measurePointProjectionAt X μ i ≫
        (Under.forget (op Point) ⋙ coefficientPresheaf).map f =
      (Under.forget (op Point) ⋙ sourcePresheaf X).map f ≫
        measurePointProjectionAt X μ j := by
  have hcond := congrArg (fun q => q μ) (measurePointProjection_condition X f)
  change
    ((ihom ((Under.forget (op Point) ⋙ sourcePresheaf X).obj i)).map
      ((Under.forget (op Point) ⋙ coefficientPresheaf).map f))
        (measurePointProjectionAt X μ i) =
      ((MonoidalClosed.pre
        ((Under.forget (op Point) ⋙ sourcePresheaf X).map f)).app
          ((Under.forget (op Point) ⋙ coefficientPresheaf).obj j))
        (measurePointProjectionAt X μ j) at hcond
  rw [ModuleCat.ihom_map_apply,
    CMDG.CondensedCM4P2E.InternalHom.monoidalClosed_pre_apply] at hcond
  exact hcond

noncomputable def pointProbeToIdentity
    (k : Under (op Point)) (y : k.right.unop) :
    k ⟶ pointIdentity := by
  let p : Point ⟶ k.right.unop :=
    ConcreteCategory.ofHom
      { toFun := fun _ => y
        continuous_toFun := continuous_const }
  refine Under.homMk p.op ?_
  apply Quiver.Hom.unop_inj
  ext z

lemma coefficientPullback_pointProbeToIdentity
    (k : Under (op Point)) (y : k.right.unop)
    (h : coefficientPresheaf.obj k.right) :
    coefficientPresheaf.map (pointProbeToIdentity k y).right h =
      (show coefficientPresheaf.obj (op Point) from
        LocallyConstant.const Point
          ((show LocallyConstant k.right.unop R from h) y)) := by
  apply CMDG.CondensedCM4P2E.InternalHom.coefficientPullback_const_op
  intro z
  rfl

/-- The one-point enriched-Hom projection reflects zero: no nonzero one-point measure section is
lost by evaluation at the identity object of the under-category. -/
theorem measurePointProjection_zero_reflects
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point))
    (hμ : measurePointProjection X μ = 0) :
    μ = 0 := by
  let E := CategoryTheory.Enriched.FunctorCategory.enrichedHom
    (ModuleCat.{u + 1} R)
    (Under.forget (op Point) ⋙ sourcePresheaf X)
    (Under.forget (op Point) ⋙ coefficientPresheaf)
  have hproj :
      ∀ k : Under (op Point), measurePointProjectionAt X μ k = 0 := by
    intro k
    apply ModuleCat.hom_injective
    ext h
    change
      (show LocallyConstant k.right.unop R from
        measurePointProjectionAt X μ k h) = 0
    ext y
    let f : k ⟶ pointIdentity := pointProbeToIdentity k y
    have hnat := ConcreteCategory.congr_hom
      (measurePointProjectionAt_naturality X f μ) h
    change
      coefficientPresheaf.map f.right
          (measurePointProjectionAt X μ k h) =
        measurePointProjectionAt X μ pointIdentity
          (sourcePresheaf X |>.map f.right h) at hnat
    rw [measurePointProjectionAt_identity, hμ] at hnat
    have hnat0 :
        coefficientPresheaf.map f.right
            (measurePointProjectionAt X μ k h) = 0 := by
      exact hnat.trans (by rfl)
    have hnat0' :
        coefficientPresheaf.map (pointProbeToIdentity k y).right
            (measurePointProjectionAt X μ k h) = 0 := by
      simpa only [f] using hnat0
    have hp := coefficientPullback_pointProbeToIdentity k y
      (measurePointProjectionAt X μ k h)
    have hconst :
        (show coefficientPresheaf.obj (op Point) from
          LocallyConstant.const Point
            ((show LocallyConstant k.right.unop R from
              measurePointProjectionAt X μ k h) y)) = 0 :=
      hp.symm.trans hnat0'
    have hv := congrArg
      (fun q : LocallyConstant Point R => q PUnit.unit) hconst
    exact congrArg ULift.down hv
  let pack : ModuleCat.of R R ⟶ E :=
    ModuleCat.ofHom
      (LinearMap.toSpanSingleton R E
        (show E from μ))
  have hpack : pack = 0 := by
    apply CategoryTheory.Limits.end_.hom_ext
    intro k
    rw [zero_comp]
    apply ModuleCat.hom_injective
    let q :=
      CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op Point) ⋙ sourcePresheaf X)
        (Under.forget (op Point) ⋙ coefficientPresheaf)
        k
    change
      (ConcreteCategory.hom q).comp
          (LinearMap.toSpanSingleton R E (show E from μ)) = 0
    rw [LinearMap.comp_toSpanSingleton]
    change
      LinearMap.toSpanSingleton R
        ((Under.forget (op Point) ⋙ sourcePresheaf X).obj k ⟶
          (Under.forget (op Point) ⋙ coefficientPresheaf).obj k)
        (measurePointProjectionAt X μ k) = 0
    rw [hproj, LinearMap.toSpanSingleton_zero]
  have h1 := congrArg
    (fun q : ModuleCat.of R R ⟶ E => q.hom) hpack
  change LinearMap.toSpanSingleton R E (show E from μ) = 0 at h1
  exact (LinearMap.toSpanSingleton_eq_zero_iff R E).mp h1

/-- The projected one-point measure section, definitionally viewed as a linear map between
locally constant one-point families. -/
noncomputable def measurePointProjectionLinear
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point)) :
    LocallyConstant Point (LocallyConstant X R) →ₗ[R]
      LocallyConstant Point R := by
  exact (measurePointProjection X μ).hom

/-- Ordinary scalar functional represented by a one-point measure section: insert a continuous
coefficient function as a constant one-point family, apply the projected measure, then evaluate
at the unique point. -/
noncomputable def measurePointFunctional
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point)) :
    LocallyConstant X R →ₗ[R] R :=
  (LocallyConstant.evalₗ R PUnit.unit).comp
    ((measurePointProjectionLinear X μ).comp (LocallyConstant.constₗ R))

/-- Integral scalar functional attached to the same one-point measure section. This is the exact
input shape required by Nöbeling freeness. -/
noncomputable def measurePointIntegralFunctional
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point)) :
    LocallyConstant X ℤ →ₗ[ℤ] ℤ :=
  CMDG.CondensedCM4P3G.liftedIntFunctionalDown X
    (measurePointFunctional X μ)


/-- The lifted condensed measure functor has the P2-D presheaf map as its underlying
natural transformation. -/
lemma measureFunctor_map_hom
    {X Y : Profinite.{u}} (f : X ⟶ Y) :
    (CMDG.CondensedCM4P2D.measureFunctor.map f).hom =
      CMDG.CondensedCM4P2D.measurePresheafFunctor.map f := by
  rfl

set_option backward.isDefEq.respectTransparency false in
/-- The functor-category internal-Hom projection intertwines outer precomposition with
ordinary precomposition at the Point component. -/
lemma measurePointProjection_pre_naturality
    {X Y : Profinite.{u}} (f : X ⟶ Y) :
    (((MonoidalClosed.pre
        (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf).app (op Point)) ≫
      CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op Point) ⋙ sourcePresheaf Y)
        (Under.forget (op Point) ⋙ coefficientPresheaf)
        pointIdentity =
    CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op Point) ⋙ sourcePresheaf X)
        (Under.forget (op Point) ⋙ coefficientPresheaf)
        pointIdentity ≫
      (MonoidalClosed.pre
        ((CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op).app (op Point))).app
          ((Under.forget (op Point) ⋙ coefficientPresheaf).obj pointIdentity) := by
  let A := sourcePresheaf Y
  let B := sourcePresheaf X
  let T := coefficientPresheaf
  let η : A ⟶ B := CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op
  let U : CompHaus.{u}ᵒᵖ := op Point
  let πA :
      ((MonoidalClosed.internalHom.obj (op A)).obj T).obj U ⟶
      (MonoidalClosed.internalHom.obj (op (A.obj U))).obj (T.obj U) :=
    CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
      (ModuleCat.{u + 1} R)
      (Under.forget U ⋙ A) (Under.forget U ⋙ T) (Under.mk (𝟙 U))
  let πB :
      ((MonoidalClosed.internalHom.obj (op B)).obj T).obj U ⟶
      (MonoidalClosed.internalHom.obj (op (B.obj U))).obj (T.obj U) :=
    CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
      (ModuleCat.{u + 1} R)
      (Under.forget U ⋙ B) (Under.forget U ⋙ T) (Under.mk (𝟙 U))
  change (((MonoidalClosed.pre η).app T).app U) ≫ πA =
    πB ≫ (MonoidalClosed.pre (η.app U)).app (T.obj U)
  apply MonoidalClosed.uncurry_injective
  rw [MonoidalClosed.uncurry_natural_left, MonoidalClosed.uncurry_pre_app]
  have h := congrArg (fun α => α.app U)
    (MonoidalClosed.id_tensor_pre_app_comp_ev η T)
  change
      MonoidalCategory.whiskerLeft (A.obj U)
          (((MonoidalClosed.pre η).app T).app U) ≫ ((ihom.ev A).app T).app U =
        MonoidalCategory.whiskerRight (η.app U)
          (((ihom B).obj T).obj U) ≫
          ((ihom.ev B).app T).app U at h
  have hA :
      ((ihom.ev A).app T).app U = MonoidalClosed.uncurry πA := by
    rfl
  have hB :
      ((ihom.ev B).app T).app U = MonoidalClosed.uncurry πB := by
    rfl
  change _ ≫ MonoidalClosed.uncurry πA =
    _ ≫ MonoidalClosed.uncurry πB
  rw [← hA, ← hB]
  simpa only [Functor.id_obj] using h

set_option backward.isDefEq.respectTransparency false in
/-- Projection of a pushed measure section is precomposition by pullback of source
functions. -/
theorem measurePointProjection_map
    {X Y : Profinite.{u}} (f : X ⟶ Y)
    (μ : (measurePresheafObj X).obj (op Point)) :
    measurePointProjection Y
        (((CMDG.CondensedCM4P2D.measureFunctor.map f).hom.app (op Point)) μ) =
      (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op).app (op Point) ≫
        measurePointProjection X μ := by
  rw [measureFunctor_map_hom f]
  unfold measurePointProjection
  have happ := ConcreteCategory.congr_hom
    (measurePointProjection_pre_naturality f) μ
  rw [ConcreteCategory.comp_apply, ConcreteCategory.comp_apply] at happ
  change
    (ConcreteCategory.hom
      (CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op Point) ⋙ sourcePresheaf Y)
        (Under.forget (op Point) ⋙ coefficientPresheaf)
        pointIdentity))
      ((ConcreteCategory.hom
        (((MonoidalClosed.pre
          (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op)).app
            CMDG.CondensedCM4P2D.coefficientPresheaf).app (op Point))) μ) =
      ((MonoidalClosed.pre
        ((CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op).app
          (op Point))).app
        ((Under.forget (op Point) ⋙ coefficientPresheaf).obj pointIdentity))
          ((ConcreteCategory.hom
            (CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
              (ModuleCat.{u + 1} R)
              (Under.forget (op Point) ⋙ sourcePresheaf X)
              (Under.forget (op Point) ⋙ coefficientPresheaf)
              pointIdentity)) μ) at happ
  rw [CMDG.CondensedCM4P2E.InternalHom.monoidalClosed_pre_apply] at happ
  change
    (ConcreteCategory.hom
      (CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
        (ModuleCat.{u + 1} R)
        (Under.forget (op Point) ⋙ sourcePresheaf Y)
        (Under.forget (op Point) ⋙ coefficientPresheaf)
        pointIdentity))
      ((ConcreteCategory.hom
        (((MonoidalClosed.pre
          (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op)).app
            CMDG.CondensedCM4P2D.coefficientPresheaf).app (op Point))) μ) =
      (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op).app (op Point) ≫
        (ConcreteCategory.hom
          (CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
            (ModuleCat.{u + 1} R)
            (Under.forget (op Point) ⋙ sourcePresheaf X)
            (Under.forget (op Point) ⋙ coefficientPresheaf)
            pointIdentity)) μ
  exact happ

set_option backward.isDefEq.respectTransparency false in
/-- Pushing a one-point measure section forward along a profinite map and then evaluating
the induced scalar functional is the same as evaluating the original measure on the pulled-back
locally constant function. -/
theorem measurePointFunctional_map
    {X Y : Profinite.{u}} (f : X ⟶ Y)
    (μ : (measurePresheafObj X).obj (op Point))
    (v : LocallyConstant Y R) :
    measurePointFunctional Y
        (((CMDG.CondensedCM4P2D.measureFunctor.map f).hom.app (op Point)) μ) v =
      measurePointFunctional X μ (LocallyConstant.comap f.hom.hom v) := by
  unfold measurePointFunctional
  change
    (LocallyConstant.evalₗ R PUnit.unit)
      (measurePointProjectionLinear Y
        (((CMDG.CondensedCM4P2D.measureFunctor.map f).hom.app (op Point)) μ)
        (LocallyConstant.const Point v)) =
      (LocallyConstant.evalₗ R PUnit.unit)
        (measurePointProjectionLinear X μ
          (LocallyConstant.const Point (LocallyConstant.comap f.hom.hom v)))
  unfold measurePointProjectionLinear
  rw [measurePointProjection_map]
  rfl


/-- The ordinary scalar Point functional loses no information about a one-point measure section. -/
theorem measurePointFunctional_zero_reflects
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point))
    (hμ : measurePointFunctional X μ = 0) :
    μ = 0 := by
  have hlin : measurePointProjectionLinear X μ = 0 := by
    apply LinearMap.ext
    intro f
    let f' : LocallyConstant Point (LocallyConstant X R) := f
    change measurePointProjectionLinear X μ f' = 0
    apply LocallyConstant.ext
    intro z
    have hf :
        f' = LocallyConstant.const Point (f' PUnit.unit) := by
      apply LocallyConstant.ext
      intro y
      cases y
      rfl
    have hfun := congrArg
      (fun F : LocallyConstant X R →ₗ[R] R => F (f' PUnit.unit)) hμ
    have hfun0 : measurePointFunctional X μ (f' PUnit.unit) = 0 := by
      simpa using hfun
    rw [measurePointFunctional] at hfun0
    change
      (measurePointProjectionLinear X μ
        (LocallyConstant.const Point (f' PUnit.unit))) PUnit.unit = 0 at hfun0
    rw [hf]
    cases z
    exact hfun0
  apply measurePointProjection_zero_reflects X μ
  apply ModuleCat.hom_injective
  change measurePointProjectionLinear X μ = 0
  exact hlin

/-- The integral scalar functional also reflects zero.  The lifted/integral equivalence is
lossless, so vanishing after descent forces the full Point functional, hence the Point measure,
to vanish. -/
theorem measurePointIntegralFunctional_zero_reflects
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point))
    (hμ : measurePointIntegralFunctional X μ = 0) :
    μ = 0 := by
  apply measurePointFunctional_zero_reflects X μ
  apply LinearMap.ext
  intro v
  have hdown := congrArg
    (fun F : LocallyConstant X ℤ →ₗ[ℤ] ℤ =>
      F ((CMDG.CondensedCM4P3G.locallyConstantIntegralLiftEquiv X).symm v)) hμ
  have hinv :=
    CMDG.CondensedCM4P3G.liftedIntFunctionalDown_apply_inverse X
      (measurePointFunctional X μ) v
  rw [measurePointIntegralFunctional] at hdown
  rw [hdown] at hinv
  change (measurePointFunctional X μ) v = ULift.up (0 : ℤ)
  exact hinv.symm

#check measurePointProjection
#check measurePointProjectionAt
#check measurePointProjectionAt_identity
#check measurePointProjection_condition
#check measurePointProjectionAt_naturality
#check pointProbeToIdentity
#check coefficientPullback_pointProbeToIdentity
#check measurePointProjection_zero_reflects
#check measurePointProjectionLinear
#check measurePointFunctional
#check measureFunctor_map_hom
#check measurePointProjection_pre_naturality
#check measurePointProjection_map
#check measurePointFunctional_map
#check measurePointIntegralFunctional
#check measurePointFunctional_zero_reflects
#check measurePointIntegralFunctional_zero_reflects

#print axioms measurePointProjection
#print axioms measurePointProjection_condition
#print axioms measurePointProjectionAt_naturality
#print axioms pointProbeToIdentity
#print axioms coefficientPullback_pointProbeToIdentity
#print axioms measurePointProjection_zero_reflects
#print axioms measurePointProjectionLinear
#print axioms measurePointFunctional
#print axioms measureFunctor_map_hom
#print axioms measurePointProjection_pre_naturality
#print axioms measurePointProjection_map
#print axioms measurePointFunctional_map
#print axioms measurePointIntegralFunctional
#print axioms measurePointFunctional_zero_reflects
#print axioms measurePointIntegralFunctional_zero_reflects

end CMDG.CondensedCM4P3G.PointFunctional

/-!
## Branch-local P3-M diagnostic

The declarations below test only the next finite point/measure comparison required by #664.
They preserve the protected point-functional module above unchanged in substance.
-/

namespace CMDG.CondensedCM4P3M.KernelPointBridge

universe u

open CategoryTheory Limits Opposite
open CMDG.CondensedCM4P3G
open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.FreeSections
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BasisBooleanPairing
open CMDG.CondensedCM4P3G.BasisBooleanPairingR
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3G.PointFunctional
open CMDG.CondensedCM4P3J.WeightedBooleanMeasure
open CMDG.CondensedCM4P3L.KernelFunctional
open CMDG.CondensedCM4P2E.RightKanReconstruction
open CMDG.CondensedCM4P2E.FiniteDualTransport
open scoped CategoryTheory.MonoidalClosed BigOperators
attribute [local instance] FintypeCat.fintype

abbrev N4PM := CMDG.CondensedCM4P2D.PresheafModule.{u}
abbrev N4RR := CMDG.CondensedCM4P2D.R.{u}
noncomputable local instance : MonoidalClosed N4PM :=
  MonoidalClosed.FunctorCategory.monoidalClosed

/-- The all-true weighted finite coefficient attached to an arbitrary Point measure
section recovers the corresponding scalar point functional on each finite delta pullback. -/
theorem weightedFiniteBooleanCoefficient_measurePoint_allTrue
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point))
    (j : DiscreteQuotient X)
    (q : (FiniteQuotientObject X j).obj) :
    weightedFiniteBooleanCoefficient X
        (fun i => measurePointIntegralFunctional X μ (integralBasis X i))
        j q (fun _ => true) =
      measurePointFunctional X μ (finiteDeltaPullbackR X j q) := by
  change
    ULift.up
      (weightedBasisBooleanPairing X
        (fun i => measurePointIntegralFunctional X μ (integralBasis X i))
        (locallyConstantIntegralDownEquiv X (finiteDeltaPullbackR X j q))
        (fun _ => true)) =
      measurePointFunctional X μ (finiteDeltaPullbackR X j q)
  rw [weightedBasisBooleanPairing_functionalWeight_allTrue]
  simpa [measurePointIntegralFunctional, locallyConstantIntegralDownEquiv] using
    liftedIntFunctionalDown_apply_inverse X
      (measurePointFunctional X μ) (finiteDeltaPullbackR X j q)

noncomputable def finiteDeltaFamilyAt
    (Q : FintypeCat.{u}) (q : Q.obj) :
    Q.obj → CMDG.CondensedCM4P3G.R.{u} := by
  classical
  exact fun y => if y = q then 1 else 0

noncomputable def finiteDeltaAt
    (Q : FintypeCat.{u}) (q : Q.obj) :
    LocallyConstant (FintypeCat.toProfinite.obj Q) CMDG.CondensedCM4P3G.R.{u} :=
  (ConcreteCategory.hom
    (CMDG.CondensedCM4P2E.finiteContinuousFunctionsIso Q).inv)
      (finiteDeltaFamilyAt Q q)

set_option backward.isDefEq.respectTransparency false in
lemma family_inv_coordinate_one
    (Q : FintypeCat.{u}) (q : Q.obj) :
    (ConcreteCategory.hom
      (((CMDG.CondensedCM4P2E.FiniteTransport.finiteFunctionPresheafFamilyNatIso.app
        (op Q)).inv).app (op Point)))
      ((ConcreteCategory.hom
        ((finiteCoordinateInclusion Q q).app (op Point)))
        (1 : LocallyConstant Point CMDG.CondensedCM4P3G.R.{u})) =
      LocallyConstant.const Point (finiteDeltaFamilyAt Q q) := by
  classical
  change
    LocallyConstant.unflip
      (fun y : Q.obj =>
        if y = q then (1 : LocallyConstant Point CMDG.CondensedCM4P3G.R.{u}) else 0) =
      LocallyConstant.const Point (finiteDeltaFamilyAt Q q)
  apply LocallyConstant.ext
  intro z
  funext y
  by_cases h : y = q <;> simp [LocallyConstant.unflip, finiteDeltaFamilyAt, h]

set_option backward.isDefEq.respectTransparency false in
lemma continuous_inv_delta_family
    (Q : FintypeCat.{u}) (q : Q.obj) :
    (ConcreteCategory.hom
      (((CMDG.CondensedCM4P2E.FiniteTransport.finiteDiscreteContinuousPresheafNatIso.app
        (op Q)).inv).app (op Point)))
      (LocallyConstant.const Point (finiteDeltaFamilyAt Q q)) =
      LocallyConstant.const Point (finiteDeltaAt Q q) := by
  apply LocallyConstant.ext
  intro z
  change
    (ConcreteCategory.hom (CMDG.CondensedCM4P2E.finiteContinuousFunctionsIso Q).inv)
      (finiteDeltaFamilyAt Q q) =
      finiteDeltaAt Q q
  rfl

set_option backward.isDefEq.respectTransparency false in
lemma sourceFamily_inv_coordinate_one
    (Q : FintypeCat.{u}) (q : Q.obj) :
    (ConcreteCategory.hom
      ((finiteMeasureSourceFamilyIso Q).inv.app (op Point)))
      ((ConcreteCategory.hom
        ((finiteCoordinateInclusion Q q).app (op Point)))
        (1 : LocallyConstant Point CMDG.CondensedCM4P3G.R.{u})) =
      LocallyConstant.const Point (finiteDeltaAt Q q) := by
  change
    (ConcreteCategory.hom
      (((CMDG.CondensedCM4P2E.FiniteTransport.finiteDiscreteContinuousPresheafNatIso.app
        (op Q)).inv).app (op Point)))
      ((ConcreteCategory.hom
        (((CMDG.CondensedCM4P2E.FiniteTransport.finiteFunctionPresheafFamilyNatIso.app
          (op Q)).inv).app (op Point)))
        ((ConcreteCategory.hom
          ((finiteCoordinateInclusion Q q).app (op Point)))
          (1 : LocallyConstant Point CMDG.CondensedCM4P3G.R.{u}))) =
      LocallyConstant.const Point (finiteDeltaAt Q q)
  rw [family_inv_coordinate_one, continuous_inv_delta_family]

set_option backward.isDefEq.respectTransparency false in
lemma finiteDeltaAt_pullback
    (X : Profinite.{u}) (j : DiscreteQuotient X)
    (q : (FiniteQuotientObject X j).obj) :
    LocallyConstant.comap (finiteQuotientMap X j).hom.hom
        (finiteDeltaAt (FiniteQuotientObject X j) q) =
      finiteDeltaPullbackR X j q := by
  classical
  apply LocallyConstant.ext
  intro x
  have hleft :
      (LocallyConstant.comap (finiteQuotientMap X j).hom.hom
        (finiteDeltaAt (FiniteQuotientObject X j) q)) x =
      finiteDeltaAt (FiniteQuotientObject X j) q
        ((finiteQuotientMap X j).hom.hom x) := by
    rfl
  rw [hleft]
  have hmap : (finiteQuotientMap X j).hom.hom x = j.proj x := by
    rfl
  rw [hmap]
  have h := ConcreteCategory.congr_hom
    (CMDG.CondensedCM4P2E.finiteContinuousFunctionsIso
      (FiniteQuotientObject X j)).inv_hom_id
    (finiteDeltaFamilyAt (FiniteQuotientObject X j) q)
  have hx := congrArg (fun g => g (j.proj x)) h
  change
    finiteDeltaAt (FiniteQuotientObject X j) q (j.proj x) =
      finiteDeltaFamilyAt (FiniteQuotientObject X j) q (j.proj x)
    at hx
  unfold finiteDeltaPullbackR
  by_cases hp : j.proj x = q
  · simp [finiteDeltaFamilyAt, hp] at hx ⊢
    exact hx
  · simp [finiteDeltaFamilyAt, hp] at hx ⊢
    exact hx

set_option backward.isDefEq.respectTransparency false in
lemma enrichedHomProjection_pre_naturality
    {A B T : N4PM} (eta : A ⟶ B) :
    (((MonoidalClosed.pre eta).app T).app (op Point)) ≫
      CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
        (ModuleCat.{u + 1} N4RR)
        (Under.forget (op Point) ⋙ A)
        (Under.forget (op Point) ⋙ T)
        pointIdentity =
    CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
        (ModuleCat.{u + 1} N4RR)
        (Under.forget (op Point) ⋙ B)
        (Under.forget (op Point) ⋙ T)
        pointIdentity ≫
      (MonoidalClosed.pre (eta.app (op Point))).app
        ((Under.forget (op Point) ⋙ T).obj pointIdentity) := by
  let U : CompHaus.{u}ᵒᵖ := op Point
  let piA :
      ((MonoidalClosed.internalHom.obj (op A)).obj T).obj U ⟶
      (MonoidalClosed.internalHom.obj (op (A.obj U))).obj (T.obj U) :=
    CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
      (ModuleCat.{u + 1} N4RR)
      (Under.forget U ⋙ A) (Under.forget U ⋙ T) (Under.mk (𝟙 U))
  let piB :
      ((MonoidalClosed.internalHom.obj (op B)).obj T).obj U ⟶
      (MonoidalClosed.internalHom.obj (op (B.obj U))).obj (T.obj U) :=
    CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
      (ModuleCat.{u + 1} N4RR)
      (Under.forget U ⋙ B) (Under.forget U ⋙ T) (Under.mk (𝟙 U))
  change (((MonoidalClosed.pre eta).app T).app U) ≫ piA =
    piB ≫ (MonoidalClosed.pre (eta.app U)).app (T.obj U)
  apply MonoidalClosed.uncurry_injective
  rw [MonoidalClosed.uncurry_natural_left, MonoidalClosed.uncurry_pre_app]
  have h := congrArg (fun alpha => alpha.app U)
    (MonoidalClosed.id_tensor_pre_app_comp_ev eta T)
  change
      MonoidalCategory.whiskerLeft (A.obj U)
          (((MonoidalClosed.pre eta).app T).app U) ≫ ((ihom.ev A).app T).app U =
        MonoidalCategory.whiskerRight (eta.app U)
          (((ihom B).obj T).obj U) ≫
          ((ihom.ev B).app T).app U at h
  have hA : ((ihom.ev A).app T).app U = MonoidalClosed.uncurry piA := by rfl
  have hB : ((ihom.ev B).app T).app U = MonoidalClosed.uncurry piB := by rfl
  change _ ≫ MonoidalClosed.uncurry piA = _ ≫ MonoidalClosed.uncurry piB
  rw [← hA, ← hB]
  simpa only [Functor.id_obj] using h

set_option backward.isDefEq.respectTransparency false in
lemma finiteMeasureFamily_coordinate_pre
    (Q : FintypeCat.{u}) (q : Q.obj) :
    (finiteMeasurePresheafFamilyIso Q).hom ≫
        (MonoidalClosed.pre (finiteCoordinateInclusion Q q)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf =
      (MonoidalClosed.pre
        (finiteCoordinateInclusion Q q ≫ (finiteMeasureSourceFamilyIso Q).inv)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf := by
  rw [finiteMeasurePresheafFamilyIso_hom]
  change
    (MonoidalClosed.pre (finiteMeasureSourceFamilyIso Q).inv).app
          CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre (finiteCoordinateInclusion Q q)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf =
      _
  have hp := congrArg
    (fun eta => eta.app CMDG.CondensedCM4P2D.coefficientPresheaf)
    (MonoidalClosed.pre_map
      (finiteCoordinateInclusion Q q) (finiteMeasureSourceFamilyIso Q).inv)
  simpa only [NatTrans.comp_app] using hp.symm

set_option maxHeartbeats 3000000 in
set_option backward.isDefEq.respectTransparency false in
lemma finiteCoordinateEvaluation_measureFamily
    (Q : FintypeCat.{u})
    (mu : (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFunctor.obj Q).obj
      (op Point))
    (q : Q.obj) :
    (ConcreteCategory.hom
      ((finiteCoordinateEvaluation Q q).app (op Point)))
      ((ConcreteCategory.hom
        ((finiteMeasurePresheafFamilyIso Q).hom.app (op Point))) mu) =
      LocallyConstant.const Point
        (measurePointFunctional (FintypeCat.toProfinite.obj Q)
          (show (measurePresheafObj (FintypeCat.toProfinite.obj Q)).obj (op Point) from mu)
          (finiteDeltaAt Q q)) := by
  let T := CMDG.CondensedCM4P2D.coefficientPresheaf
  let i := finiteMeasureSourceFamilyIso Q
  let inc := finiteCoordinateInclusion Q q
  let eta := inc ≫ i.inv
  let phi : CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom.obj (op Point) :=
    (ConcreteCategory.hom (((MonoidalClosed.pre eta).app T).app (op Point))) mu
  let one : CMDG.CondensedCM4P2E.InternalHom.coefficientAt Point :=
    LocallyConstant.const Point (1 : CMDG.CondensedCM4P2E.InternalHom.R)
  have hcomp := finiteMeasureFamily_coordinate_pre Q q
  have hfull := congrArg
    (fun k => k ≫ CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.hom) hcomp
  change
    (finiteMeasurePresheafFamilyIso Q).hom ≫ finiteCoordinateEvaluation Q q =
      (MonoidalClosed.pre eta).app T ≫
        CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.hom at hfull
  have happ := congrArg (fun k => k.app (op Point)) hfull
  have hval := ConcreteCategory.congr_hom happ mu
  simp only [NatTrans.comp_app, ConcreteCategory.comp_apply] at hval
  change
    (ConcreteCategory.hom ((finiteCoordinateEvaluation Q q).app (op Point)))
      ((ConcreteCategory.hom ((finiteMeasurePresheafFamilyIso Q).hom.app (op Point))) mu) =
      CMDG.CondensedCM4P2E.InternalHom.rankOneEvaluationApp Point phi at hval
  have hproj := enrichedHomProjection_pre_naturality (T := T) eta
  have hprojVal := ConcreteCategory.congr_hom hproj mu
  simp only [ConcreteCategory.comp_apply] at hprojVal
  have hprojExact :
      CMDG.CondensedCM4P2E.InternalHom.rankOneProjectionEndomorphism
          Point pointIdentity phi =
        (ConcreteCategory.hom
          ((MonoidalClosed.pre (eta.app (op Point))).app
            ((Under.forget (op Point) ⋙ T).obj pointIdentity)))
          ((ConcreteCategory.hom
            (CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
              (ModuleCat.{u + 1} N4RR)
              (Under.forget (op Point) ⋙
                CMDG.CondensedCM4P2E.FiniteTransport.finiteDiscreteContinuousPresheafFunctor.obj
                  (op Q))
              (Under.forget (op Point) ⋙ T)
              pointIdentity)) mu) := by
    unfold CMDG.CondensedCM4P2E.InternalHom.rankOneProjectionEndomorphism
    exact hprojVal
  rw [CMDG.CondensedCM4P2E.InternalHom.monoidalClosed_pre_apply] at hprojExact
  have hprojOne := congrArg
    (fun k : CMDG.CondensedCM4P2E.InternalHom.coefficientAt Point ⟶
        CMDG.CondensedCM4P2E.InternalHom.coefficientAt Point =>
      (ConcreteCategory.hom k) one) hprojExact
  refine hval.trans ?_
  rw [CMDG.CondensedCM4P2E.InternalHom.rankOneEvaluationApp_apply]
  change (ConcreteCategory.hom
    (CMDG.CondensedCM4P2E.InternalHom.rankOneProjectionEndomorphism
      Point pointIdentity phi)) one = _
  refine hprojOne.trans ?_
  change
    (ConcreteCategory.hom
      (measurePointProjection (FintypeCat.toProfinite.obj Q)
        (show (measurePresheafObj (FintypeCat.toProfinite.obj Q)).obj (op Point) from mu)))
      ((ConcreteCategory.hom (i.inv.app (op Point)))
        ((ConcreteCategory.hom (inc.app (op Point)))
          (1 : LocallyConstant Point N4RR))) =
      LocallyConstant.const Point
        (measurePointFunctional (FintypeCat.toProfinite.obj Q)
          (show (measurePresheafObj (FintypeCat.toProfinite.obj Q)).obj (op Point) from mu)
          (finiteDeltaAt Q q))
  rw [sourceFamily_inv_coordinate_one Q q]
  change
    measurePointProjectionLinear (FintypeCat.toProfinite.obj Q)
        (show (measurePresheafObj (FintypeCat.toProfinite.obj Q)).obj (op Point) from mu)
        (LocallyConstant.const Point (finiteDeltaAt Q q)) =
      LocallyConstant.const Point
        (measurePointFunctional (FintypeCat.toProfinite.obj Q)
          (show (measurePresheafObj (FintypeCat.toProfinite.obj Q)).obj (op Point) from mu)
          (finiteDeltaAt Q q))
  apply LocallyConstant.ext
  intro z
  cases z
  rfl

lemma finiteFamilyEvaluation_coordinate
    (Q : FintypeCat.{u}) (q : Q.obj) :
    finiteFamilyEvaluation Q ≫ finiteCoordinateProjection Q q =
      finiteCoordinateEvaluation Q q := by
  classical
  unfold finiteFamilyEvaluation
  rw [Preadditive.sum_comp Finset.univ]
  rw [Finset.sum_eq_single q]
  · rw [Category.assoc, finiteCoordinateInclusion_projection_self]
    simp
  · intro b _ hb
    rw [Category.assoc, finiteCoordinateInclusion_projection_ne Q hb]
    simp
  · simp

theorem weightedFiniteBooleanMeasureSection_allTrue_realizes_pushforward
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point))
    (j : DiscreteQuotient X) :
    (ConcreteCategory.hom
      ((measurePresheafObj (X.diagram.obj j)).map
        ((profiniteToCompHaus).map
          (basisBooleanPointProbe X (fun _ => true))).op))
      (weightedFiniteBooleanMeasureSection X
        (fun i => measurePointIntegralFunctional X μ (integralBasis X i)) j) =
    ((CMDG.CondensedCM4P2D.measureFunctor.map
      (finiteQuotientMap X j)).hom.app (op Point)) μ := by
  classical
  let Q := FiniteQuotientObject X j
  let S := op ((profiniteToCompHaus).obj (basisBooleanCube X))
  let U : CompHaus.{u}ᵒᵖ := op Point
  let ftrue := ((profiniteToCompHaus).map
    (basisBooleanPointProbe X (fun _ => true))).op
  let a : IntegralBasisIndex X → ℤ :=
    fun i => measurePointIntegralFunctional X μ (integralBasis X i)
  let sec :
      (finiteMeasurePresheafFunctor.obj Q).obj S :=
    weightedFiniteBooleanMeasureSection X a j
  let μj :
      (finiteMeasurePresheafFunctor.obj Q).obj U :=
    ((CMDG.CondensedCM4P2D.measureFunctor.map
      (finiteQuotientMap X j)).hom.app (op Point)) μ
  let e := finiteMeasurePresheafFamilyIso Q ≪≫ finiteFamilyInternalHomIso Q
  apply_fun (ConcreteCategory.hom (e.hom.app U))
  · have hnat := ConcreteCategory.congr_hom (e.hom.naturality ftrue) sec
    simp only [NatTrans.comp_app, ConcreteCategory.comp_apply] at hnat
    have hsec := weightedFiniteBooleanMeasureSection_coefficientFamily_transport X a j
    have hsec' :
        (ConcreteCategory.hom (e.hom.app S)) sec =
          weightedFiniteBooleanCoefficientFamily X a j := by
      change
        (ConcreteCategory.hom ((finiteFamilyInternalHomIso Q).hom.app S))
          ((ConcreteCategory.hom ((finiteMeasurePresheafFamilyIso Q).hom.app S)) sec) =
        weightedFiniteBooleanCoefficientFamily X a j
      simpa [Q, S, sec] using hsec
    have hlhs :
        (ConcreteCategory.hom (e.hom.app U))
          ((ConcreteCategory.hom ((measurePresheafObj (X.diagram.obj j)).map ftrue)) sec) =
        (ConcreteCategory.hom
          ((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf Q).map ftrue))
          (weightedFiniteBooleanCoefficientFamily X a j) := by
      exact hnat.trans (congrArg
        (fun t => (ConcreteCategory.hom
          ((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf Q).map ftrue)) t)
        hsec')
    rw [hlhs]
    change _ = (ConcreteCategory.hom (e.hom.app U)) μj
    funext q
    let iM := finiteMeasurePresheafFamilyIso Q
    have hcoord := finiteFamilyEvaluation_coordinate Q q
    have hcoordApp := congrArg (fun η => η.app U) hcoord
    have hcoordVal := ConcreteCategory.congr_hom hcoordApp
      ((ConcreteCategory.hom (iM.hom.app U)) μj)
    simp only [NatTrans.comp_app, ConcreteCategory.comp_apply] at hcoordVal
    have hrhs :
        ((ConcreteCategory.hom (e.hom.app U)) μj) q =
          (ConcreteCategory.hom ((finiteCoordinateEvaluation Q q).app U))
            ((ConcreteCategory.hom (iM.hom.app U)) μj) := by
      change
        (ConcreteCategory.hom ((finiteCoordinateProjection Q q).app U))
          ((ConcreteCategory.hom ((finiteFamilyEvaluation Q).app U))
            ((ConcreteCategory.hom (iM.hom.app U)) μj)) =
        (ConcreteCategory.hom ((finiteCoordinateEvaluation Q q).app U))
          ((ConcreteCategory.hom (iM.hom.app U)) μj)
      exact hcoordVal
    rw [hrhs]
    have hmeasure :=
      finiteCoordinateEvaluation_measureFamily Q μj q
    rw [hmeasure]
    apply LocallyConstant.ext
    intro z
    change weightedFiniteBooleanCoefficient X a j q (fun _ => true) =
      measurePointFunctional (X.diagram.obj j)
        (((CMDG.CondensedCM4P2D.measureFunctor.map
          (finiteQuotientMap X j)).hom.app (op Point)) μ)
        (finiteDeltaAt (FiniteQuotientObject X j) q)
    rw [weightedFiniteBooleanCoefficient_measurePoint_allTrue]
    rw [measurePointFunctional_map (finiteQuotientMap X j) μ]
    rw [finiteDeltaAt_pullback X j q]
  · intro x y h
    have h' := congrArg (ConcreteCategory.hom (e.inv.app U)) h
    simpa [ConcreteCategory.comp_apply] using h'

#check finiteDeltaAt_pullback
#check finiteCoordinateEvaluation_measureFamily
#check weightedFiniteBooleanMeasureSection_allTrue_realizes_pushforward

#print axioms finiteDeltaAt_pullback
#print axioms finiteCoordinateEvaluation_measureFamily
#print axioms weightedFiniteBooleanMeasureSection_allTrue_realizes_pushforward

/-- The arbitrary Point measure section is recovered globally by evaluating the
weighted Boolean limit at the all-true selector. -/
theorem weightedFiniteBooleanMeasureLimitLift_measurePoint_allTrue
    (X : Profinite.{u})
    (μ : (measurePresheafObj X).obj (op Point)) :
    (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map
        (basisBooleanPointProbe X (fun _ => true)) ≫
      weightedFiniteBooleanMeasureLimitLift X
        (fun i => measurePointIntegralFunctional X μ (integralBasis X i)) =
    (freeHomSectionsEquiv (Profinite.of PUnit.{u + 1})
      (CMDG.CondensedCM4P2D.measureFunctor.obj X)).symm μ := by
  let P := Profinite.of PUnit.{u + 1}
  let T := basisBooleanCube X
  let qtrue := basisBooleanPointProbe X (fun _ => true)
  let a : IntegralBasisIndex X → ℤ :=
    fun i => measurePointIntegralFunctional X μ (integralBasis X i)
  let μHom :
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).obj P ⟶
        CMDG.CondensedCM4P2D.measureFunctor.obj X :=
    (freeHomSectionsEquiv P
      (CMDG.CondensedCM4P2D.measureFunctor.obj X)).symm μ
  let S := op ((profiniteToCompHaus).obj P)
  have hpost :
      ∀ {A B : CondensedMod.{u} CMDG.CondensedCM4P3G.R.{u}}
        (g : (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).obj P ⟶ A)
        (h : A ⟶ B),
        freeHomSectionsEquiv P B (g ≫ h) =
          (ConcreteCategory.hom
            (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map h).hom.app S))
            (freeHomSectionsEquiv P A g) := by
    intro A B g h
    change
      (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
          ((profiniteToCondensed).obj P) B (g ≫ h)) = _
    rw [Adjunction.homEquiv_naturality_right]
    rfl
  apply (measureFunctorMapConeIsLimit X).hom_ext
  intro j
  let q := finiteQuotientMap X j
  have hleft := congrArg
    (fun g =>
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫ g)
    (weightedFiniteBooleanMeasureLimitLift_fac X a j)
  have hfinite :
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
          weightedFiniteBooleanMeasureHom X a j =
        μHom ≫ CMDG.CondensedCM4P2D.measureFunctor.map q := by
    apply
      (freeHomSectionsEquiv P
        (CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j))).injective
    rw [freeHomSectionsEquiv_precomp]
    rw [hpost
      (g := μHom)
      (h := CMDG.CondensedCM4P2D.measureFunctor.map q)]
    have hsec :
        freeHomSectionsEquiv T
            (CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j))
            (weightedFiniteBooleanMeasureHom X a j) =
          weightedFiniteBooleanMeasureSection X a j := by
      exact Equiv.apply_symm_apply _ _
    have hμ :
        freeHomSectionsEquiv P
            (CMDG.CondensedCM4P2D.measureFunctor.obj X) μHom = μ := by
      exact Equiv.apply_symm_apply _ _
    rw [hsec, hμ]
    change
      (ConcreteCategory.hom
        ((measurePresheafObj (X.diagram.obj j)).map
          ((profiniteToCompHaus).map qtrue).op))
        (weightedFiniteBooleanMeasureSection X a j) =
      (ConcreteCategory.hom
        ((CMDG.CondensedCM4P2D.measureFunctor.map q).hom.app (op Point))) μ
    simpa [qtrue, a, q] using
      weightedFiniteBooleanMeasureSection_allTrue_realizes_pushforward X μ j
  have h := hleft.trans hfinite
  set_option backward.defeqAttrib.useBackward true in
  set_option backward.isDefEq.respectTransparency false in
    simpa [P, q, finiteQuotientMap, qtrue, a, μHom, Category.assoc] using h

#check weightedFiniteBooleanMeasureLimitLift_measurePoint_allTrue
#print axioms weightedFiniteBooleanMeasureLimitLift_measurePoint_allTrue

/-- The one-point profinite probe selecting `x`. -/
noncomputable def profinitePointProbe
    (X : Profinite.{u}) (x : X) : Profinite.of PUnit.{u + 1} ⟶ X :=
  ConcreteCategory.ofHom
    { toFun := fun _ => x
      continuous_toFun := continuous_const }

/-- Finite-stage measure/Dirac identity.  The large finite comparison is kept inside the proof so
that its four canonical factors can be cancelled explicitly rather than normalized definitionally
in the theorem statement. -/
theorem weightedFiniteBooleanMeasureHom_measureSolidification_evaluationWeight_allTrue
    (X : Profinite.{u}) (x : X) (j : DiscreteQuotient X) :
    (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map
        (basisBooleanPointProbe X (fun _ => true)) ≫
      weightedFiniteBooleanMeasureHom X (integralBasisEvaluationWeight X x) j =
    (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map
        (profinitePointProbe (X.diagram.obj j) ((finiteQuotientMap X j).hom.hom x)) ≫
      measureSolidification.app (X.diagram.obj j) := by
  let P := Profinite.of PUnit.{u + 1}
  let T := CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X
  let Q := CMDG.CondensedCM4P3G.FiniteBooleanMeasure.FiniteQuotientObject X j
  let A := CMDG.CondensedCM4P2D.measureFunctor.obj (X.diagram.obj j)
  let D :=
    (CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
      ModuleCat.free CMDG.CondensedCM4P3G.R.{u} ⋙
      Condensed.discrete (ModuleCat.{u + 1} CMDG.CondensedCM4P3G.R.{u})).obj Q
  let S := op ((profiniteToCompHaus).obj T)
  let eComp :=
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom.app Q
  let eFree := CMDG.CondensedCM4P2E.finiteFreeDiscreteIso.hom.app Q
  apply (cancel_mono eComp).1
  simp only [Category.assoc]
  have hfac :
      measureSolidification.app (X.diagram.obj j) ≫ eComp =
        𝟙 ((Condensed.finFree CMDG.CondensedCM4P3G.R.{u}).obj Q) := by
    dsimp [eComp, Q]
    simpa only [Functor.comp_obj] using
      (measureSolidification_fac (X.fintypeDiagram.obj j))
  rw [hfac]
  apply (cancel_mono eFree).1
  simp only [Category.assoc]
  let e := eComp ≫ eFree
  have hpost :
      ∀ {B C : CondensedMod.{u} CMDG.CondensedCM4P3G.R.{u}}
        (g : (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).obj T ⟶ B)
        (h : B ⟶ C),
        freeHomSectionsEquiv T C (g ≫ h) =
          (ConcreteCategory.hom
            (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map h).hom.app S))
            (freeHomSectionsEquiv T B g) := by
    intro B C g h
    change
      (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
          ((profiniteToCondensed).obj T) C (g ≫ h)) = _
    rw [Adjunction.homEquiv_naturality_right]
    rfl
  have hsection :
      freeHomSectionsEquiv T (CMDG.CondensedCM4P2E.finiteMeasure.obj Q)
          (weightedFiniteBooleanMeasureHom X (integralBasisEvaluationWeight X x) j) =
        weightedFiniteBooleanMeasureSection X (integralBasisEvaluationWeight X x) j := by
    change
      freeHomSectionsEquiv T A
          (weightedFiniteBooleanMeasureHom X (integralBasisEvaluationWeight X x) j) =
        weightedFiniteBooleanMeasureSection X (integralBasisEvaluationWeight X x) j
    exact Equiv.apply_symm_apply _ _
  apply (freeHomSectionsEquiv P D).injective
  rw [freeHomSectionsEquiv_precomp]
  rw [hpost, hsection]
  rw [freeHomSectionsEquiv_precomp]
  simp only [Category.id_comp]
  have he :
      eComp ≫ eFree =
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasureSmallFreeCondensedNatIso.hom.app Q ≫
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedDiscreteNatIso.hom.app Q ≫
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeDiscreteULiftNatIso.hom.app Q := by
    dsimp [eComp, eFree]
    simp [CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso,
      Category.assoc]
  rw [he]
  let eTail :=
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedDiscreteNatIso.hom.app Q ≫
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeDiscreteULiftNatIso.hom.app Q
  have hbridge :=
    weightedFiniteBooleanMeasureSection_smallFree_evaluationWeight_allTrue X x j
  have hbridgeTail := congrArg
    (fun t =>
      (ConcreteCategory.hom
        (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map eTail).hom.app
          (op ((profiniteToCompHaus).obj P)))) t)
    hbridge
  simp [eTail, eFree, freeHomSectionsEquiv,
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasureSmallFreeCondensedNatIso,
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasureSmallFreeCondensedIso,
    CMDG.CondensedCM4P2E.finiteFreeDiscreteIso,
    CMDG.CondensedCM4P2E.finiteRepresentableCondensedIso,
    CMDG.CondensedCM4P2E.discreteFreeIso,
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedDiscreteNatIso,
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeDiscreteULiftNatIso,
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftNatIso,
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftIso,
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftLinearEquiv,
    Adjunction.homEquiv_naturality_left,
    CategoryTheory.Adjunction.homEquiv_leftAdjointUniq_hom_app] at hbridgeTail
  convert hbridgeTail using 1
  · rfl
  ·
    let U := op ((profiniteToCompHaus).obj P)
    let ftrue := ((profiniteToCompHaus).map
      (basisBooleanPointProbe X (fun _ => true))).op
    let z :=
      (ConcreteCategory.hom
        ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasureSmallFreePresheafNatIso.app Q).hom.app S))
        (weightedFiniteBooleanMeasureSection X (integralBasisEvaluationWeight X x) j)
    have hnat :=
      ConcreteCategory.congr_hom
        (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map eTail).hom.naturality ftrue) z
    change
      (ConcreteCategory.hom
        (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).obj D).obj.map ftrue))
          ((ConcreteCategory.hom
            (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map eTail).hom.app S)) z) =
        (ConcreteCategory.hom
          (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map eTail).hom.app U))
          ((ConcreteCategory.hom
            ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreePresheafFunctor.obj Q).map ftrue)) z)
    exact hnat.symm
  ·
    rw [← freeHomSectionsEquiv_precomp]
    let Q1 : FintypeCat.{u} := FintypeCat.of PUnit.{u + 1}
    let qx : Q1 ⟶ Q := FintypeCat.homMk (fun _ => j.proj x)
    have hpoint :
        profinitePointProbe (X.diagram.obj j) ((finiteQuotientMap X j).hom.hom x) =
          FintypeCat.toProfinite.map qx := by
      ext y
      rfl
    rw [hpoint]
    change
      freeHomSectionsEquiv (FintypeCat.toProfinite.obj Q1) D
        ((Condensed.finFree CMDG.CondensedCM4P3G.R.{u}).map qx ≫ eFree) = _
    rw [CMDG.CondensedCM4P2E.finiteFreeDiscreteIso.hom.naturality qx]
    have heQ1 :
        CMDG.CondensedCM4P2E.finiteFreeDiscreteIso.hom.app Q1 =
          (Condensed.free CMDG.CondensedCM4P3G.R.{u}).map
              (CMDG.CondensedCM4P2E.finiteRepresentableCondensedIso.hom.app Q1) ≫
            CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
              (CMDG.CondensedCM4P2E.finiteUnderlyingULift.obj Q1) := by
      rfl
    rw [heQ1, Category.assoc]
    unfold freeHomSectionsEquiv
    simp only [Equiv.trans_apply, id_eq]
    rw [Adjunction.homEquiv_naturality_left]
    dsimp only [id]
    set_option backward.isDefEq.respectTransparency false in
      unfold GrothendieckTopology.uliftYonedaEquiv
      simp only [Equiv.trans_apply]
      change
        CategoryTheory.uliftYonedaEquiv
          ((sheafToPresheaf (coherentTopology CompHaus.{u}) (Type (u + 1))).map
            (CMDG.CondensedCM4P2E.finiteRepresentableCondensedIso.hom.app Q1 ≫
              (Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
                ((CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙ Condensed.discrete (Type (u + 1))).obj Q1)
                D
                (CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
                    (CMDG.CondensedCM4P2E.finiteUnderlyingULift.obj Q1) ≫
                  (CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
                    ModuleCat.free CMDG.CondensedCM4P3G.R.{u} ⋙
                    Condensed.discrete (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map qx))) = _
      rw [CategoryTheory.uliftYonedaEquiv_apply]
      simp only [Functor.map_comp, NatTrans.comp_app, ConcreteCategory.comp_apply]
    have hrep :
        (ConcreteCategory.hom
          (((sheafToPresheaf (coherentTopology CompHaus.{u}) (Type (u + 1))).map
            (CMDG.CondensedCM4P2E.finiteRepresentableCondensedIso.hom.app Q1)).app
              (op (profiniteToCompHaus.obj (FintypeCat.toProfinite.obj Q1)))))
          (ULift.up
            (𝟙 (profiniteToCompHaus.obj (FintypeCat.toProfinite.obj Q1)))) =
          (ConcreteCategory.hom
            ((Condensed.discreteUnderlyingAdj (Type (u + 1))).unit.app
              (ULift.{u + 1, u} Q1.obj)))
            (ULift.up PUnit.unit) := by
      have hlcUnit :=
        CategoryTheory.Adjunction.unit_leftAdjointUniq_hom_app
          CondensedSet.LocallyConstant.adjunction
          (Condensed.discreteUnderlyingAdj (Type (u + 1)))
          (ULift.{u + 1, u} Q1.obj)
      have hlcUnitPoint :=
        CategoryTheory.types_congr_hom hlcUnit (ULift.up PUnit.unit)
      let frontIso :=
        Functor.isoWhiskerLeft
            (FintypeCat.toProfinite ⋙ profiniteToCompHaus)
            CMDG.CondensedCM4P2E.compHausTopULiftNatIso ≪≫
          Functor.isoWhiskerRight
              CMDG.CondensedCM4P2E.finiteDiscreteULiftIso
              topCatToCondensedSet ≪≫
            Functor.isoWhiskerLeft
              CMDG.CondensedCM4P2E.finiteUnderlyingULift
              (CompHausLike.LocallyConstant.functorIso
                (fun _ : TopCat.{u} => True)
                (fun _ _ _ => ((CompHaus.effectiveEpi_tfae _).out 0 2).mp)).symm
      have hdecomp :
          CMDG.CondensedCM4P2E.finiteRepresentableCondensedIso.hom.app Q1 =
            frontIso.hom.app Q1 ≫
              (Functor.isoWhiskerLeft
                CMDG.CondensedCM4P2E.finiteUnderlyingULift
                CondensedSet.LocallyConstant.iso).hom.app Q1 := by
        set_option backward.defeqAttrib.useBackward true in
        set_option backward.isDefEq.respectTransparency false in
          rfl
      have hfront :
          (ConcreteCategory.hom
            (((sheafToPresheaf (coherentTopology CompHaus.{u}) (Type (u + 1))).map
              (frontIso.hom.app Q1)).app
                (op (profiniteToCompHaus.obj (FintypeCat.toProfinite.obj Q1)))))
            (ULift.up
              (𝟙 (profiniteToCompHaus.obj (FintypeCat.toProfinite.obj Q1)))) =
            (ConcreteCategory.hom
              (CondensedSet.LocallyConstant.adjunction.unit.app
                (ULift.{u + 1, u} Q1.obj)))
              (ULift.up PUnit.unit) := by
        dsimp [Q1]
        apply LocallyConstant.ext
        intro s
        apply ULift.ext
        exact Subsingleton.elim _ _
      set_option backward.defeqAttrib.useBackward true in
      set_option backward.isDefEq.respectTransparency false in
        rw [hdecomp]
        simp only [Functor.map_comp, NatTrans.comp_app, ConcreteCategory.comp_apply]
        let post :=
          ConcreteCategory.hom
            (((sheafToPresheaf (coherentTopology CompHaus.{u}) (Type (u + 1))).map
              ((Functor.isoWhiskerLeft
                CMDG.CondensedCM4P2E.finiteUnderlyingULift
                CondensedSet.LocallyConstant.iso).hom.app Q1)).app
                  (op (profiniteToCompHaus.obj (FintypeCat.toProfinite.obj Q1))))
        calc
          _ = post
              ((ConcreteCategory.hom
                (CondensedSet.LocallyConstant.adjunction.unit.app
                  (ULift.{u + 1, u} Q1.obj)))
                (ULift.up PUnit.unit)) := congrArg post hfront
          _ = _ := hlcUnitPoint
    have hrepPost :
        (ConcreteCategory.hom
          (((sheafToPresheaf (coherentTopology CompHaus.{u}) (Type (u + 1))).map
            ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
              ((CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
                Condensed.discrete (Type (u + 1))).obj Q1)
              D
              (CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
                  (CMDG.CondensedCM4P2E.finiteUnderlyingULift.obj Q1) ≫
                (CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
                  ModuleCat.free CMDG.CondensedCM4P3G.R.{u} ⋙
                  Condensed.discrete (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map qx))).app
                (op (profiniteToCompHaus.obj (FintypeCat.toProfinite.obj Q1)))))
          ((ConcreteCategory.hom
            (((sheafToPresheaf (coherentTopology CompHaus.{u}) (Type (u + 1))).map
              (CMDG.CondensedCM4P2E.finiteRepresentableCondensedIso.hom.app Q1)).app
                (op (profiniteToCompHaus.obj (FintypeCat.toProfinite.obj Q1)))))
            (ULift.up
              (𝟙 (profiniteToCompHaus.obj (FintypeCat.toProfinite.obj Q1))))) =
        (ConcreteCategory.hom
          (((sheafToPresheaf (coherentTopology CompHaus.{u}) (Type (u + 1))).map
            ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
              ((CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
                Condensed.discrete (Type (u + 1))).obj Q1)
              D
              (CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
                  (CMDG.CondensedCM4P2E.finiteUnderlyingULift.obj Q1) ≫
                (CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
                  ModuleCat.free CMDG.CondensedCM4P3G.R.{u} ⋙
                  Condensed.discrete (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map qx))).app
                (op (profiniteToCompHaus.obj (FintypeCat.toProfinite.obj Q1)))))
          ((ConcreteCategory.hom
            ((Condensed.discreteUnderlyingAdj (Type (u + 1))).unit.app
              (ULift.{u + 1, u} Q1.obj)))
            (ULift.up PUnit.unit)) := by
      exact congrArg
        (ConcreteCategory.hom
          (((sheafToPresheaf (coherentTopology CompHaus.{u}) (Type (u + 1))).map
            ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
              ((CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
                Condensed.discrete (Type (u + 1))).obj Q1)
              D
              (CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
                  (CMDG.CondensedCM4P2E.finiteUnderlyingULift.obj Q1) ≫
                (CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
                  ModuleCat.free CMDG.CondensedCM4P3G.R.{u} ⋙
                  Condensed.discrete (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map qx))).app
                (op (profiniteToCompHaus.obj (FintypeCat.toProfinite.obj Q1)))))
        hrep
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      refine hrepPost.trans ?_
    have huniqQ :=
      CategoryTheory.Adjunction.unit_leftAdjointUniq_hom_app
        CMDG.CondensedCM4P2E.discreteSetFreeAdj
        CMDG.CondensedCM4P2E.freeDiscreteModuleAdj
        (ULift.{u + 1, u} Q.obj)
    have huniqQPoint :=
      CategoryTheory.types_congr_hom huniqQ (ULift.up (j.proj x))
    have huniqQHomEquiv :=
      CategoryTheory.Adjunction.homEquiv_leftAdjointUniq_hom_app
        CMDG.CondensedCM4P2E.discreteSetFreeAdj
        CMDG.CondensedCM4P2E.freeDiscreteModuleAdj
        (ULift.{u + 1, u} Q.obj)
    have huniqQHomEquivExpanded :
        (Condensed.discreteUnderlyingAdj (Type (u + 1))).homEquiv
          (ULift.{u + 1, u} Q.obj)
          ((Condensed.forget CMDG.CondensedCM4P2E.R.{u}).obj
            ((ModuleCat.free CMDG.CondensedCM4P2E.R.{u} ⋙
              Condensed.discrete (ModuleCat CMDG.CondensedCM4P2E.R.{u})).obj
                (ULift.{u + 1, u} Q.obj)))
          (((Condensed.freeForgetAdjunction CMDG.CondensedCM4P2E.R.{u}).homEquiv
            ((Condensed.discrete (Type (u + 1))).obj
              (ULift.{u + 1, u} Q.obj))
            ((ModuleCat.free CMDG.CondensedCM4P2E.R.{u} ⋙
              Condensed.discrete (ModuleCat CMDG.CondensedCM4P2E.R.{u})).obj
                (ULift.{u + 1, u} Q.obj)))
            (CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
              (ULift.{u + 1, u} Q.obj))) =
        CMDG.CondensedCM4P2E.freeDiscreteModuleAdj.unit.app
          (ULift.{u + 1, u} Q.obj) := by
      simpa only [
        Functor.comp_obj,
        CMDG.CondensedCM4P2E.discreteFreeIso,
        CMDG.CondensedCM4P2E.discreteSetFreeAdj,
        Adjunction.comp_homEquiv,
        Equiv.trans_apply] using huniqQHomEquiv
    have huniqQUnitExpanded := huniqQHomEquivExpanded
    rw [Adjunction.homEquiv_unit] at huniqQUnitExpanded
    have huniqQUnitPoint :=
      CategoryTheory.types_congr_hom huniqQUnitExpanded (ULift.up (j.proj x))
    have hdiscNat :=
      CMDG.CondensedCM4P2E.discreteFreeIso.hom.naturality
        (CMDG.CondensedCM4P2E.finiteUnderlyingULift.map qx)
    have hdiscNatTarget :
        CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
              (CMDG.CondensedCM4P2E.finiteUnderlyingULift.obj Q1) ≫
            (CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
              ModuleCat.free CMDG.CondensedCM4P3G.R.{u} ⋙
              Condensed.discrete (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map qx =
          (CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
              Condensed.discrete (Type (u + 1)) ⋙
              Condensed.free CMDG.CondensedCM4P3G.R.{u}).map qx ≫
            CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
              (CMDG.CondensedCM4P2E.finiteUnderlyingULift.obj Q) := by
      simpa only [Functor.comp_map] using hdiscNat.symm
    have hfreeNat :=
      (Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv_naturality_left
        ((Condensed.discrete (Type (u + 1))).map
          (CMDG.CondensedCM4P2E.finiteUnderlyingULift.map qx))
        (CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
          (CMDG.CondensedCM4P2E.finiteUnderlyingULift.obj Q))
    have hfreeNatTarget :
        ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
          ((CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
            Condensed.discrete (Type (u + 1))).obj Q1)
          ((CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
            ModuleCat.free CMDG.CondensedCM4P3G.R.{u} ⋙
            Condensed.discrete (ModuleCat CMDG.CondensedCM4P3G.R.{u})).obj Q))
          ((CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
              Condensed.discrete (Type (u + 1)) ⋙
              Condensed.free CMDG.CondensedCM4P3G.R.{u}).map qx ≫
            CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
              (CMDG.CondensedCM4P2E.finiteUnderlyingULift.obj Q)) =
        (Condensed.discrete (Type (u + 1))).map
            (CMDG.CondensedCM4P2E.finiteUnderlyingULift.map qx) ≫
          ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
            ((CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
              Condensed.discrete (Type (u + 1))).obj Q)
            ((CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
            ModuleCat.free CMDG.CondensedCM4P3G.R.{u} ⋙
            Condensed.discrete (ModuleCat CMDG.CondensedCM4P3G.R.{u})).obj Q))
            (CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
              (CMDG.CondensedCM4P2E.finiteUnderlyingULift.obj Q)) := by
      simpa only [Functor.comp_obj, Functor.comp_map] using hfreeNat
    have hunitNat :=
      (Condensed.discreteUnderlyingAdj (Type (u + 1))).unit.naturality
        (CMDG.CondensedCM4P2E.finiteUnderlyingULift.map qx)
    have hunitPoint :=
      CategoryTheory.types_congr_hom hunitNat (ULift.up PUnit.unit)
    have hunitSection :
        (ConcreteCategory.hom
          (((sheafToPresheaf (coherentTopology CompHaus.{u}) (Type (u + 1))).map
            ((Condensed.discrete (Type (u + 1))).map
              (CMDG.CondensedCM4P2E.finiteUnderlyingULift.map qx))).app
                (op (CompHaus.of PUnit.{u + 1}))))
          ((ConcreteCategory.hom
            ((Condensed.discreteUnderlyingAdj (Type (u + 1))).unit.app
              (ULift.{u + 1, u} Q1.obj)))
            (ULift.up PUnit.unit)) =
        (ConcreteCategory.hom
          ((Condensed.discreteUnderlyingAdj (Type (u + 1))).unit.app
            (ULift.{u + 1, u} Q.obj)))
          (ULift.up ((ConcreteCategory.hom qx.hom) PUnit.unit)) := by
      set_option backward.defeqAttrib.useBackward true in
      set_option backward.isDefEq.respectTransparency false in
        exact hunitPoint.symm
    let postUnit :=
      ConcreteCategory.hom
        (((sheafToPresheaf (coherentTopology CompHaus.{u}) (Type (u + 1))).map
          ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
            ((CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
              Condensed.discrete (Type (u + 1))).obj Q)
            ((CMDG.CondensedCM4P2E.finiteUnderlyingULift ⋙
              ModuleCat.free CMDG.CondensedCM4P3G.R.{u} ⋙
              Condensed.discrete (ModuleCat CMDG.CondensedCM4P3G.R.{u})).obj Q)
            (CMDG.CondensedCM4P2E.discreteFreeIso.hom.app
              (CMDG.CondensedCM4P2E.finiteUnderlyingULift.obj Q)))).app
                (op (CompHaus.of PUnit.{u + 1})))
    have hunitPost := congrArg postUnit hunitSection
    rw [hdiscNatTarget]
    dsimp only [D]
    rw [hfreeNatTarget]
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      refine hunitPost.trans ?_
    dsimp [postUnit, Q1, qx, eTail, freeHomSectionsEquiv]
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      refine huniqQUnitPoint.trans ?_
    let M : ModuleCat.{u + 1} CMDG.CondensedCM4P3G.R.{u} :=
      (ModuleCat.free CMDG.CondensedCM4P3G.R.{u}).obj
        (ULift.{u + 1, u} Q.obj)
    have hlcUnitMap :
        (CondensedMod.LocallyConstant.adjunction CMDG.CondensedCM4P3G.R.{u}).unit.app M =
          (CondensedMod.LocallyConstant.functorIsoDiscreteAux₁
            CMDG.CondensedCM4P3G.R.{u} M).hom := by
      set_option backward.defeqAttrib.useBackward true in
      set_option backward.isDefEq.respectTransparency false in
        change
          (Condensed.discreteUnderlyingAdj
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.app M ≫
              (Condensed.underlying
                (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
                ((CondensedMod.LocallyConstant.functorIsoDiscreteComponents
                  CMDG.CondensedCM4P3G.R.{u} M).hom) =
            (CondensedMod.LocallyConstant.functorIsoDiscreteAux₁
              CMDG.CondensedCM4P3G.R.{u} M).hom
      rw [show
        (CondensedMod.LocallyConstant.functorIsoDiscreteComponents
            CMDG.CondensedCM4P3G.R.{u} M).hom =
          (Condensed.discrete (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
              (CondensedMod.LocallyConstant.functorIsoDiscreteAux₁
                CMDG.CondensedCM4P3G.R.{u} M).hom ≫
            (Condensed.discreteUnderlyingAdj
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).counit.app
              ((CondensedMod.LocallyConstant.functor
                CMDG.CondensedCM4P3G.R.{u}).obj M) by
          rfl]
      have hmapComp :=
        (Condensed.underlying
          (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map_comp
          ((Condensed.discrete
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
            (CondensedMod.LocallyConstant.functorIsoDiscreteAux₁
              CMDG.CondensedCM4P3G.R.{u} M).hom)
          ((Condensed.discreteUnderlyingAdj
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).counit.app
            ((CondensedMod.LocallyConstant.functor
              CMDG.CondensedCM4P3G.R.{u}).obj M))
      rw [hmapComp]
      have hunitNat :=
        ((Condensed.discreteUnderlyingAdj
          (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.naturality
            (CondensedMod.LocallyConstant.functorIsoDiscreteAux₁
              CMDG.CondensedCM4P3G.R.{u} M).hom).symm
      simp only [Functor.comp_map, Functor.id_map] at hunitNat
      rw [← Category.assoc, hunitNat]
      have htriangle :=
        (Condensed.discreteUnderlyingAdj
          (ModuleCat CMDG.CondensedCM4P3G.R.{u})).right_triangle_components
          ((CondensedMod.LocallyConstant.functor
            CMDG.CondensedCM4P3G.R.{u}).obj M)
      set_option backward.defeqAttrib.useBackward true in
      set_option backward.isDefEq.respectTransparency false in
        change
          (CondensedMod.LocallyConstant.functorIsoDiscreteAux₁
              CMDG.CondensedCM4P3G.R.{u} M).hom ≫
              ((Condensed.discreteUnderlyingAdj
                (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.app
                  ((Condensed.underlying
                    (ModuleCat CMDG.CondensedCM4P3G.R.{u})).obj
                    ((CondensedMod.LocallyConstant.functor
                      CMDG.CondensedCM4P3G.R.{u}).obj M)) ≫
                (Condensed.underlying
                  (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
                  ((Condensed.discreteUnderlyingAdj
                    (ModuleCat CMDG.CondensedCM4P3G.R.{u})).counit.app
                    ((CondensedMod.LocallyConstant.functor
                      CMDG.CondensedCM4P3G.R.{u}).obj M))) =
            (CondensedMod.LocallyConstant.functorIsoDiscreteAux₁
              CMDG.CondensedCM4P3G.R.{u} M).hom
      have htrianglePost :=
        congrArg
          (fun k =>
            (CondensedMod.LocallyConstant.functorIsoDiscreteAux₁
              CMDG.CondensedCM4P3G.R.{u} M).hom ≫ k)
          htriangle
      exact htrianglePost.trans (Category.comp_id _)
    have hdiscreteUnitFactor :
        (Condensed.discreteUnderlyingAdj
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.app M =
          (CondensedMod.LocallyConstant.adjunction CMDG.CondensedCM4P3G.R.{u}).unit.app M ≫
            (Condensed.underlying
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
              ((CondensedMod.LocallyConstant.functorIsoDiscrete
                CMDG.CondensedCM4P3G.R.{u}).hom.app M) := by
      have htransport :
          (CondensedMod.LocallyConstant.adjunction CMDG.CondensedCM4P3G.R.{u}).unit.app M =
            (Condensed.discreteUnderlyingAdj
                (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.app M ≫
              (Condensed.underlying
                (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
                ((CondensedMod.LocallyConstant.functorIsoDiscrete
                  CMDG.CondensedCM4P3G.R.{u}).inv.app M) := by
        rfl
      rw [htransport, Category.assoc, ← Functor.map_comp,
        Iso.inv_hom_id_app]
      have hmapId :=
        (Condensed.underlying
          (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map_id
          ((Condensed.discrete
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).obj M)
      rw [hmapId]
      exact (Category.comp_id _).symm
    let mx : M := ModuleCat.freeMk (ULift.up (j.proj x))
    have hlcUnitPoint :
        (ConcreteCategory.hom
          ((CondensedMod.LocallyConstant.adjunction CMDG.CondensedCM4P3G.R.{u}).unit.app M))
          mx =
        LocallyConstant.const (CompHaus.of PUnit.{u + 1}) mx := by
      dsimp [mx]
      rw [hlcUnitMap]
      rfl
    have hmoduleUnit :=
      (ModuleCat.adj CMDG.CondensedCM4P3G.R.{u}).homEquiv_id
        (ULift.{u + 1, u} Q.obj)
    rw [ModuleCat.adj_homEquiv] at hmoduleUnit
    have hmoduleUnitPoint :=
      CategoryTheory.types_congr_hom hmoduleUnit.symm
        (ULift.up (j.proj x))
    have hfreeHomIdentity :
        (ConcreteCategory.hom
          (ModuleCat.freeHomEquiv
            (𝟙 ((ModuleCat.free CMDG.CondensedCM4P3G.R.{u}).obj
              (ULift.{u + 1, u} Q.obj)))))
          (ULift.up (j.proj x)) =
        ModuleCat.freeMk (ULift.up (j.proj x)) := by
      rfl
    have hmoduleUnitPointMx :
        (ConcreteCategory.hom
          ((ModuleCat.adj CMDG.CondensedCM4P3G.R.{u}).unit.app
            (ULift.{u + 1, u} Q.obj)))
          (ULift.up (j.proj x)) = mx := by
      dsimp [mx]
      exact hmoduleUnitPoint.trans hfreeHomIdentity
    have hdiscreteUnitFactorForget :=
      congrArg
        (fun k =>
          (CategoryTheory.forget
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map k)
        hdiscreteUnitFactor
    rw [show
      CMDG.CondensedCM4P2E.freeDiscreteModuleAdj.unit.app
          (ULift.{u + 1, u} Q.obj) =
        (ModuleCat.adj CMDG.CondensedCM4P3G.R.{u}).unit.app
            (ULift.{u + 1, u} Q.obj) ≫
          (CategoryTheory.forget (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
            ((Condensed.discreteUnderlyingAdj
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.app M) by
      rfl]
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      change
        (ConcreteCategory.hom
          ((CategoryTheory.forget
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
            ((Condensed.discreteUnderlyingAdj
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.app M)))
          ((ConcreteCategory.hom
            ((ModuleCat.adj CMDG.CondensedCM4P3G.R.{u}).unit.app
              (ULift.{u + 1, u} Q.obj)))
            (ULift.up (j.proj x))) = _
    rw [hmoduleUnitPointMx]
    have hdiscreteUnitFactorMx :=
      CategoryTheory.types_congr_hom hdiscreteUnitFactorForget mx
    rw [hdiscreteUnitFactorMx]
    have hlcUnitPointForget :
        (ConcreteCategory.hom
          ((CategoryTheory.forget
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
            ((CondensedMod.LocallyConstant.adjunction
              CMDG.CondensedCM4P3G.R.{u}).unit.app M)))
          mx =
        LocallyConstant.const (CompHaus.of PUnit.{u + 1}) mx := by
      exact hlcUnitPoint
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      change
        (ConcreteCategory.hom
          ((CategoryTheory.forget
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
            ((Condensed.underlying
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
              ((CondensedMod.LocallyConstant.functorIsoDiscrete
                CMDG.CondensedCM4P3G.R.{u}).hom.app M))))
          ((ConcreteCategory.hom
            ((CategoryTheory.forget
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
              ((CondensedMod.LocallyConstant.adjunction
                CMDG.CondensedCM4P3G.R.{u}).unit.app M)))
            mx) = _
    have hfunctorIsoConst :
        (ConcreteCategory.hom
          ((CategoryTheory.forget
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
            ((Condensed.underlying
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
              ((CondensedMod.LocallyConstant.functorIsoDiscrete
                CMDG.CondensedCM4P3G.R.{u}).hom.app M))))
          (LocallyConstant.const (CompHaus.of PUnit.{u + 1}) mx) =
        (ConcreteCategory.hom
          ((CategoryTheory.forget
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
            ((Condensed.discreteUnderlyingAdj
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.app M)))
          mx := by
      have h := hdiscreteUnitFactorMx
      set_option backward.defeqAttrib.useBackward true in
      set_option backward.isDefEq.respectTransparency false in
        change
          (ConcreteCategory.hom
            ((CategoryTheory.forget
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
              ((Condensed.discreteUnderlyingAdj
                (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.app M)))
            mx =
          (ConcreteCategory.hom
            ((CategoryTheory.forget
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
              ((Condensed.underlying
                (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
                ((CondensedMod.LocallyConstant.functorIsoDiscrete
                  CMDG.CondensedCM4P3G.R.{u}).hom.app M))))
            ((ConcreteCategory.hom
              ((CategoryTheory.forget
                (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
                ((CondensedMod.LocallyConstant.adjunction
                  CMDG.CondensedCM4P3G.R.{u}).unit.app M)))
              mx) at h
      rw [hlcUnitPointForget] at h
      exact h.symm
    rw [hlcUnitPointForget, hfunctorIsoConst]
    let U := op ((profiniteToCompHaus).obj P)
    let q : Q.obj := by
      set_option backward.isDefEq.respectTransparency false in
        exact (finiteQuotientMap X j).hom.hom x
    let fU :
        CMDG.CondensedCM4P2E.Algebraic.finiteSmallFreeModule.obj Q ⟶ M :=
      (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftIso Q).hom
    let c : LocallyConstant P (Q.obj →₀ CMDG.CondensedCM4P3G.R.{u}) :=
      (ConcreteCategory.hom
        ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCoordinateInclusion
          Q q).app U))
        (1 : LocallyConstant P CMDG.CondensedCM4P3G.R.{u})
    have hc :
        c =
          LocallyConstant.const (CompHaus.of PUnit.{u + 1})
            (Finsupp.single q (1 : CMDG.CondensedCM4P3G.R.{u})) := by
      apply LocallyConstant.ext
      intro p
      change c p = Finsupp.single q (1 : CMDG.CondensedCM4P3G.R.{u})
      have hp :=
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCoordinateInclusion_apply
          Q q U
          (1 : LocallyConstant P
            CMDG.CondensedCM4P2E.FiniteDualTransport.R.{u}) p
      set_option backward.defeqAttrib.useBackward true in
      set_option backward.isDefEq.respectTransparency false in
        exact hp
    have hfU :
        fU (Finsupp.single q (1 : CMDG.CondensedCM4P3G.R.{u})) = mx := by
      change
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftLinearEquiv Q
            (Finsupp.single q (1 : CMDG.CondensedCM4P3G.R.{u})) =
          ModuleCat.freeMk (ULift.up (j.proj x))
      rw [CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftLinearEquiv_single]
      set_option backward.defeqAttrib.useBackward true in
      set_option backward.isDefEq.respectTransparency false in
        dsimp [q, Q]
        rfl
    have hmap :
        (ConcreteCategory.hom
          (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map
            ((CondensedMod.LocallyConstant.functor CMDG.CondensedCM4P3G.R.{u}).map fU)).hom.app U))
          c =
        LocallyConstant.const (CompHaus.of PUnit.{u + 1}) mx := by
      rw [hc]
      apply LocallyConstant.ext
      intro p
      set_option backward.isDefEq.respectTransparency false in
        change fU (Finsupp.single q (1 : CMDG.CondensedCM4P3G.R.{u})) = mx
      exact hfU
    have hIsoNat :=
      (CondensedMod.LocallyConstant.functorIsoDiscrete
        CMDG.CondensedCM4P3G.R.{u}).hom.naturality fU
    have htail :
        eTail =
          (CondensedMod.LocallyConstant.functor CMDG.CondensedCM4P3G.R.{u}).map fU ≫
            (CondensedMod.LocallyConstant.functorIsoDiscrete
              CMDG.CondensedCM4P3G.R.{u}).hom.app M := by
      dsimp [eTail, fU,
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedDiscreteNatIso,
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeDiscreteULiftNatIso,
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftNatIso,
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftIso]
      set_option backward.isDefEq.respectTransparency false in
        exact hIsoNat.symm
    change
      (ConcreteCategory.hom
        ((CategoryTheory.forget
          (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
          ((Condensed.discreteUnderlyingAdj
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.app M)))
        mx =
      (ConcreteCategory.hom
        (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map eTail).hom.app U)) c
    rw [htail]
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      change
        (ConcreteCategory.hom
          ((CategoryTheory.forget
            (ModuleCat CMDG.CondensedCM4P3G.R.{u})).map
            ((Condensed.discreteUnderlyingAdj
              (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.app M)))
          mx =
        (ConcreteCategory.hom
          (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map
            ((CondensedMod.LocallyConstant.functorIsoDiscrete
              CMDG.CondensedCM4P3G.R.{u}).hom.app M)).hom.app U))
          ((ConcreteCategory.hom
            (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map
              ((CondensedMod.LocallyConstant.functor
                CMDG.CondensedCM4P3G.R.{u}).map fU)).hom.app U)) c)
    rw [hmap]
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      exact hfunctorIsoConst.symm

/-- The finite evaluation-weight/Dirac identity assembles through the protected
finite-quotient limit to the global measure object. -/
theorem weightedFiniteBooleanMeasureLimitLift_measureSolidification_evaluationWeight_allTrue
    (X : Profinite.{u}) (x : X) :
    (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map
        (basisBooleanPointProbe X (fun _ => true)) ≫
      weightedFiniteBooleanMeasureLimitLift X (integralBasisEvaluationWeight X x) =
    (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map
        (profinitePointProbe X x) ≫
      measureSolidification.app X := by
  apply (measureFunctorMapConeIsLimit X).hom_ext
  intro j
  let q := finiteQuotientMap X j
  let px :=
    profinitePointProbe (X.diagram.obj j) ((finiteQuotientMap X j).hom.hom x)
  have hleft := congrArg
    (fun g =>
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map
          (basisBooleanPointProbe X (fun _ => true)) ≫ g)
    (weightedFiniteBooleanMeasureLimitLift_fac
      X (integralBasisEvaluationWeight X x) j)
  have hpoint :
      profinitePointProbe X x ≫ q = px := by
    ext y
    rfl
  have hnat := measureSolidification.naturality q
  have hfinite :=
    weightedFiniteBooleanMeasureHom_measureSolidification_evaluationWeight_allTrue X x j
  calc
    ((Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map
        (basisBooleanPointProbe X (fun _ => true)) ≫
      weightedFiniteBooleanMeasureLimitLift X (integralBasisEvaluationWeight X x)) ≫
        (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j =
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map
          (basisBooleanPointProbe X (fun _ => true)) ≫
        weightedFiniteBooleanMeasureHom X (integralBasisEvaluationWeight X x) j := by
          set_option backward.defeqAttrib.useBackward true in
          set_option backward.isDefEq.respectTransparency false in
            simpa only [Category.assoc] using hleft
    _ =
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map px ≫
        measureSolidification.app (X.diagram.obj j) := hfinite
    _ =
      ((Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map
          (profinitePointProbe X x) ≫ measureSolidification.app X) ≫
        (CMDG.CondensedCM4P2D.measureFunctor.mapCone X.asLimitCone).π.app j := by
          change
            (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map px ≫
                measureSolidification.app (X.diagram.obj j) =
              ((Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map
                  (profinitePointProbe X x) ≫ measureSolidification.app X) ≫
                CMDG.CondensedCM4P2D.measureFunctor.map q
          rw [Category.assoc, ← hnat]
          rw [← Category.assoc, ← Functor.map_comp, hpoint]

/-- A morphism in the kernel of profinite solidification annihilates the full
basis-evaluation weight at every point.  This is the first direct use of the #664 kernel
hypothesis after the finite Dirac identity has been assembled globally. -/
theorem kernelProductFunctional_evaluationWeight_eq_zero_of_solidification_kernel
    (X : Profinite.{u})
    (d :
      (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X ⟶
        coefficientObject)
    (hd :
      (Condensed.profiniteSolidification CMDG.CondensedCM4P3G.R.{u}).app X ≫ d = 0)
    (x : X) :
    kernelProductFunctional X d (integralBasisEvaluationWeight X x) = 0 := by
  let P := Profinite.of PUnit.{u + 1}
  let U := op ((profiniteToCompHaus).obj P)
  let qtrue := basisBooleanPointProbe X (fun _ => true)
  let qx := profinitePointProbe X x
  let e :=
    CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.hom.app X
  have hsolid :
      measureSolidification.app X ≫ e =
        (Condensed.profiniteSolidification CMDG.CondensedCM4P3G.R.{u}).app X := by
    simpa [e] using
      congrArg (fun η => η.app X)
        measureSolidification_comp_measureProfiniteSolidNatIso
  have hlimit :=
    weightedFiniteBooleanMeasureLimitLift_measureSolidification_evaluationWeight_allTrue X x
  have hmor :
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
          (weightedFiniteBooleanMeasureLimitLift X
              (integralBasisEvaluationWeight X x) ≫ e ≫ d) =
        0 := by
    calc
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
          (weightedFiniteBooleanMeasureLimitLift X
              (integralBasisEvaluationWeight X x) ≫ e ≫ d) =
        ((Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
          weightedFiniteBooleanMeasureLimitLift X
            (integralBasisEvaluationWeight X x)) ≫ e ≫ d := by
              simp only [Category.assoc]
      _ =
        ((Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qx ≫
          measureSolidification.app X) ≫ e ≫ d := by
            rw [hlimit]
      _ =
        (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qx ≫
          (measureSolidification.app X ≫ e) ≫ d := by
            simp only [Category.assoc]
      _ =
        (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qx ≫
          (Condensed.profiniteSolidification CMDG.CondensedCM4P3G.R.{u}).app X ≫ d := by
            rw [hsolid]
      _ =
        (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qx ≫ 0 := by
            rw [hd]
      _ = 0 := by simp
  have hzadd :=
    freeHomSectionsEquiv_add P coefficientObject
      (0 : FreeHom P coefficientObject) (0 : FreeHom P coefficientObject)
  have hz :
      freeHomSectionsEquiv P coefficientObject
          (0 : FreeHom P coefficientObject) =
        (0 : ↑(coefficientObject.obj.obj U)) := by
    let z : ↑(coefficientObject.obj.obj U) :=
      freeHomSectionsEquiv P coefficientObject
        (0 : FreeHom P coefficientObject)
    change z = 0
    have hzz : z = z + z := by
      simpa [z] using hzadd
    have hsub := congrArg
      (fun w : ↑(coefficientObject.obj.obj U) => w - z) hzz
    have hz0 : (0 : ↑(coefficientObject.obj.obj U)) = z := by
      simpa using hsub
    exact hz0.symm
  have hs0 :
      freeHomSectionsEquiv P coefficientObject
          ((Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
            (weightedFiniteBooleanMeasureLimitLift X
                (integralBasisEvaluationWeight X x) ≫ e ≫ d)) =
        (0 : ↑(coefficientObject.obj.obj U)) := by
    rw [hmor]
    exact hz
  rw [freeHomSectionsEquiv_precomp] at hs0
  have hsPoint := congrArg
    (fun f : LocallyConstant P CMDG.CondensedCM4P3G.R.{u} => f PUnit.unit) hs0
  have hsection :
      kernelProductSection X d (integralBasisEvaluationWeight X x)
          (fun _ => true) = 0 := by
    set_option backward.defeqAttrib.useBackward true in
    set_option backward.isDefEq.respectTransparency false in
      change
        (show LocallyConstant
            (CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X)
            CMDG.CondensedCM4P3G.R.{u} from
          freeHomSectionsEquiv
            (CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X)
            coefficientObject
            (weightedFiniteBooleanMeasureLimitLift X
                (integralBasisEvaluationWeight X x) ≫ e ≫ d))
              (fun _ => true) = 0 at hsPoint
    exact hsPoint
  rw [kernelProductFunctional_apply]
  simpa using congrArg ULift.down hsection

/-- The #664 finite-coordinate witness and the solidification-kernel hypothesis force the
finite Nöbeling coefficient combination to vanish pointwise. -/
theorem basisCombination_kernelProductFunctional_eq_zero_of_solidification_kernel
    (X : Profinite.{u})
    (d :
      (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X ⟶
        coefficientObject)
    (hd :
      (Condensed.profiniteSolidification CMDG.CondensedCM4P3G.R.{u}).app X ≫ d = 0)
    (I : Finset (IntegralBasisIndex X))
    (hI :
      ∀ a : IntegralBasisIndex X → ℤ,
        (∀ i ∈ I, a i = 0) →
        kernelProductFunctional X d a = 0) :
    ∀ x : X,
      basisCombination X
        (finiteFunctionalCoefficients X (kernelProductFunctional X d) I) x = 0 := by
  intro x
  rw [basisCombination_kernelProductFunctional_finiteCoefficients_apply X d I hI x]
  exact
    kernelProductFunctional_evaluationWeight_eq_zero_of_solidification_kernel
      X d hd x

/-- Immediate #664 endpoint: a solidification-kernel morphism has zero P3-L product
functional.  This uses only the protected finite-coordinate dependence theorem, the pointwise
Nöbeling separation theorem, and the kernel/evaluation bridge above. -/
theorem kernelProductFunctional_eq_zero_of_solidification_kernel
    (X : Profinite.{u})
    (d :
      (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X ⟶
        coefficientObject)
    (hd :
      (Condensed.profiniteSolidification CMDG.CondensedCM4P3G.R.{u}).app X ≫ d = 0) :
    kernelProductFunctional X d = 0 := by
  obtain ⟨I, hI⟩ :=
    kernelProductFunctional_finite_coordinate_kernel X d
  apply
    additiveFunctional_eq_zero_of_finiteDependence_and_basisCombination
      X (kernelProductFunctional X d) I hI
  exact
    basisCombination_kernelProductFunctional_eq_zero_of_solidification_kernel
      X d hd I hI

/-- Evaluating an arbitrary solid-side coefficient morphism on a transported Point measure is
exactly the P3-L product functional applied to the measure's Nöbeling coefficient vector. -/
theorem applied_d_point_kernelProductFunctional
    (X : Profinite.{u})
    (d :
      (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X ⟶
        coefficientObject)
    (μ : (measurePresheafObj X).obj (op Point)) :
    ((show LocallyConstant Point CMDG.CondensedCM4P3G.R.{u} from
      (d.hom.app (op Point))
        ((CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.hom.app X).hom.app
          (op Point) μ)) PUnit.unit).down =
      kernelProductFunctional X d
        (fun i => measurePointIntegralFunctional X μ (integralBasis X i)) := by
  let P := Profinite.of PUnit.{u + 1}
  let T := basisBooleanCube X
  let qtrue := basisBooleanPointProbe X (fun _ => true)
  let a : IntegralBasisIndex X → ℤ :=
    fun i => measurePointIntegralFunctional X μ (integralBasis X i)
  let e :=
    CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.hom.app X
  let μHom :
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).obj P ⟶
        CMDG.CondensedCM4P2D.measureFunctor.obj X :=
    (freeHomSectionsEquiv P
      (CMDG.CondensedCM4P2D.measureFunctor.obj X)).symm μ
  have hrec := weightedFiniteBooleanMeasureLimitLift_measurePoint_allTrue X μ
  have hcomp := congrArg (fun g => g ≫ e ≫ d) hrec
  have hcomp' :
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).map qtrue ≫
          weightedFiniteBooleanMeasureLimitLift X a ≫ e ≫ d =
        μHom ≫ e ≫ d := by
    simpa [P, qtrue, a, e, μHom, Category.assoc] using hcomp
  have hs := congrArg (freeHomSectionsEquiv P coefficientObject) hcomp'
  rw [freeHomSectionsEquiv_precomp] at hs
  let U := op ((profiniteToCompHaus).obj P)
  have hpost :
      ∀ {A B : CondensedMod.{u} CMDG.CondensedCM4P3G.R.{u}}
        (g : (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u}).obj P ⟶ A)
        (h : A ⟶ B),
        freeHomSectionsEquiv P B (g ≫ h) =
          (ConcreteCategory.hom
            (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map h).hom.app U))
            (freeHomSectionsEquiv P A g) := by
    intro A B g h
    change
      (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
          ((profiniteToCondensed).obj P) B (g ≫ h)) = _
    rw [Adjunction.homEquiv_naturality_right]
    rfl
  have hμ :
      freeHomSectionsEquiv P
          (CMDG.CondensedCM4P2D.measureFunctor.obj X) μHom = μ := by
    exact Equiv.apply_symm_apply _ _
  have hright := hpost (g := μHom) (h := e ≫ d)
  rw [hμ] at hright
  rw [hright] at hs
  have hsPoint := congrArg
    (fun f : LocallyConstant P CMDG.CondensedCM4P3G.R.{u} => f PUnit.unit) hs
  have hsPoint' := hsPoint
  change kernelProductSection X d a (fun _ => true) = _ at hsPoint'
  set_option backward.defeqAttrib.useBackward true in
  set_option backward.isDefEq.respectTransparency false in
    change kernelProductSection X d a (fun _ => true) =
      (show LocallyConstant Point CMDG.CondensedCM4P3G.R.{u} from
        (d.hom.app (op Point)) ((e.hom.app (op Point)) μ)) PUnit.unit at hsPoint'
  rw [kernelProductFunctional_apply]
  change
    ((show LocallyConstant Point CMDG.CondensedCM4P3G.R.{u} from
      (d.hom.app (op Point)) ((e.hom.app (op Point)) μ)) PUnit.unit).down =
      (kernelProductSection X d a (fun _ => true)).down
  exact congrArg ULift.down hsPoint'.symm

/-- The product-functional zero theorem is faithful enough at Point to kill the original
solid-side coefficient morphism. -/
theorem coefficient_eq_zero_of_solidification_kernel
    (X : Profinite.{u})
    (d :
      (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X ⟶
        coefficientObject)
    (hd :
      (Condensed.profiniteSolidification CMDG.CondensedCM4P3G.R.{u}).app X ≫ d = 0) :
    d = 0 := by
  have hk :=
    kernelProductFunctional_eq_zero_of_solidification_kernel X d hd
  apply coefficient_hom_ext_point
  change d.hom.app (op Point) = 0
  apply ModuleCat.hom_ext
  apply LinearMap.ext
  intro s
  let E :=
    CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.app X
  let μ : (measurePresheafObj X).obj (op Point) :=
    (E.inv.hom.app (op Point)) s
  have hE : (E.hom.hom.app (op Point)) μ = s := by
    dsimp [μ]
    change
      (ConcreteCategory.hom (E.hom.hom.app (op Point)))
        ((ConcreteCategory.hom (E.inv.hom.app (op Point))) s) = s
    rw [← ConcreteCategory.comp_apply]
    change
      (ConcreteCategory.hom ((E.inv ≫ E.hom).hom.app (op Point))) s = s
    rw [E.inv_hom_id]
    rfl
  have hc := applied_d_point_kernelProductFunctional X d μ
  let aμ : IntegralBasisIndex X → ℤ :=
    fun i => measurePointIntegralFunctional X μ (integralBasis X i)
  have hkμ := congrArg
    (fun F : (IntegralBasisIndex X → ℤ) →+ ℤ => F aμ) hk
  have hzero : kernelProductFunctional X d aμ = 0 := by
    simpa using hkμ
  have hdown :
      ((show LocallyConstant Point CMDG.CondensedCM4P3G.R.{u} from
        (d.hom.app (op Point)) ((E.hom.hom.app (op Point)) μ))
          PUnit.unit).down = 0 := by
    exact hc.trans hzero
  rw [← hE]
  apply LocallyConstant.ext
  intro z
  cases z
  apply ULift.ext
  exact hdown

/-- Point-functional faithfulness closes the remaining coefficient mapping-out injectivity
boundary directly, without first constructing a finite-stage factorization. -/
theorem coefficientMappingOutInjectivity_of_pointFunctional :
    CoefficientMappingOutInjectivity.{u} := by
  intro X h₁ h₂ hh
  change
    (Condensed.profiniteSolidification CMDG.CondensedCM4P3G.R.{u}).app X ≫ h₁ =
      (Condensed.profiniteSolidification CMDG.CondensedCM4P3G.R.{u}).app X ≫ h₂ at hh
  have hd :
      (Condensed.profiniteSolidification CMDG.CondensedCM4P3G.R.{u}).app X ≫
        (h₁ - h₂) = 0 := by
    rw [Preadditive.comp_sub, hh, sub_self]
  have hzero :=
    coefficient_eq_zero_of_solidification_kernel X (h₁ - h₂) hd
  exact sub_eq_zero.mp hzero

/-- Terminal coefficient-solidity theorem obtained from the Point-functional route. -/
theorem coefficientObject_isSolid_via_pointFunctional :
    CondensedMod.IsSolid.{u} CMDG.CondensedCM4P3G.R.{u} coefficientObject := by
  have hinj : CoefficientMappingOutInjectivity.{u} :=
    coefficientMappingOutInjectivity_of_pointFunctional
  have hstage : CoefficientFiniteStageMappingOut.{u} :=
    coefficientFiniteStageMappingOut_of_injectivity hinj
  exact coefficientFiniteStageMappingOut_iff_isSolid.mp hstage

#check applied_d_point_kernelProductFunctional
#check coefficient_eq_zero_of_solidification_kernel
#check coefficientMappingOutInjectivity_of_pointFunctional
#check coefficientObject_isSolid_via_pointFunctional
#print axioms applied_d_point_kernelProductFunctional
#print axioms coefficient_eq_zero_of_solidification_kernel
#print axioms coefficientMappingOutInjectivity_of_pointFunctional
#print axioms coefficientObject_isSolid_via_pointFunctional

/-- Immediate propagation of the Point-functional coefficient theorem through protected P3-E:
every profinite solid value is solid. -/
theorem profiniteSolid_isSolid_via_pointFunctional
    (S : Profinite.{u}) :
    CondensedMod.IsSolid CMDG.CondensedCM4P3G.R.{u}
      ((Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj S) := by
  exact CMDG.CondensedCM4P3E.profiniteSolid_isSolid_of_coefficient S
    coefficientObject_isSolid_via_pointFunctional

/-- Terminal P3 residual theorem obtained by composing protected P3-E with the
Point-functional coefficient-solidity closure. -/
theorem residualHomTheorem_via_pointFunctional
    (S : Profinite.{u}) :
    CMDG.CondensedCM4P3C.ResidualHomTheorem S := by
  exact CMDG.CondensedCM4P3E.residualHomTheorem_of_coefficientSolid S
    coefficientObject_isSolid_via_pointFunctional

#check profiniteSolid_isSolid_via_pointFunctional
#check residualHomTheorem_via_pointFunctional
#print axioms profiniteSolid_isSolid_via_pointFunctional
#print axioms residualHomTheorem_via_pointFunctional

#check weightedFiniteBooleanCoefficient_measurePoint_allTrue
#check profinitePointProbe
#check weightedFiniteBooleanMeasureHom_measureSolidification_evaluationWeight_allTrue
#check weightedFiniteBooleanMeasureLimitLift_measureSolidification_evaluationWeight_allTrue
#print axioms weightedFiniteBooleanCoefficient_measurePoint_allTrue
#print axioms weightedFiniteBooleanMeasureHom_measureSolidification_evaluationWeight_allTrue
#print axioms weightedFiniteBooleanMeasureLimitLift_measureSolidification_evaluationWeight_allTrue
#print axioms kernelProductFunctional_evaluationWeight_eq_zero_of_solidification_kernel
#print axioms basisCombination_kernelProductFunctional_eq_zero_of_solidification_kernel
#print axioms kernelProductFunctional_eq_zero_of_solidification_kernel

end CMDG.CondensedCM4P3M.KernelPointBridge
