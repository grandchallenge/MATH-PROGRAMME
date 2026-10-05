import CMDGCondensedCM4P3MFiniteQuotientBridge
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

/-- Projection of a pushed measure section is precomposition by pullback of source
functions. -/
theorem measurePointProjection_map
    {X Y : Profinite.{u}} (f : X ⟶ Y)
    (μ : (measurePresheafObj X).obj (op Point)) :
    measurePointProjection Y
        (((CMDG.CondensedCM4P2D.measureFunctor.map f).hom.app (op Point)) μ) =
      (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.map f.op).app (op Point) ≫
        measurePointProjection X μ := by
  simp only [measurePointProjection, CMDG.CondensedCM4P2D.measureFunctor,
    CMDG.CondensedCM4P2D.measurePresheafFunctor]
  rw [← MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerRight]
  simp [CategoryTheory.eHomWhiskerRight,
    MonoidalClosed.enrichedOrdinaryCategorySelf_homEquiv,
    CategoryTheory.Enriched.FunctorCategory.functorHomEquiv,
    CategoryTheory.Enriched.FunctorCategory.functorEnrichedComp,
    CategoryTheory.Enriched.FunctorCategory.homEquiv_apply_π,
    CMDG.CondensedCM4P2E.InternalHom.monoidalClosed_pre_apply]

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
  rw [measurePointFunctional, measurePointFunctional]
  change
    ((measurePointProjection Y
      (((CMDG.CondensedCM4P2D.measureFunctor.map f).hom.app (op Point)) μ)).hom
        (LocallyConstant.const Point v)) PUnit.unit =
      ((measurePointProjection X μ).hom
        (LocallyConstant.const Point (LocallyConstant.comap f.hom.hom v))) PUnit.unit
  rw [measurePointProjection_map]
  rfl

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
#check measurePointProjection_map
#check measurePointFunctional_map
#check measurePointIntegralFunctional

#print axioms measurePointProjection
#print axioms measurePointProjection_condition
#print axioms measurePointProjectionAt_naturality
#print axioms pointProbeToIdentity
#print axioms coefficientPullback_pointProbeToIdentity
#print axioms measurePointProjection_zero_reflects
#print axioms measurePointProjectionLinear
#print axioms measurePointFunctional
#print axioms measurePointProjection_map
#print axioms measurePointFunctional_map
#print axioms measurePointIntegralFunctional

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
open CMDG.CondensedCM4P3G.FreeSections
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BasisBooleanPairing
open CMDG.CondensedCM4P3G.BasisBooleanPairingR
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3G.PointFunctional
open CMDG.CondensedCM4P3J.WeightedBooleanMeasure
open CMDG.CondensedCM4P3L.KernelFunctional
open CMDG.CondensedCM4P2E.RightKanReconstruction

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
