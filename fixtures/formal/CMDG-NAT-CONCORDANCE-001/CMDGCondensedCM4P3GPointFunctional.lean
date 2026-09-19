import CMDGCondensedCM4P3MFiniteQuotientBridge
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

#check measurePointProjection
#check measurePointProjectionLinear
#check measurePointFunctional
#check measurePointIntegralFunctional

#print axioms measurePointProjection
#print axioms measurePointProjectionLinear
#print axioms measurePointFunctional
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
open CMDG.CondensedCM4P3J.WeightedBooleanMeasure
open CMDG.CondensedCM4P3L.KernelFunctional
open CMDG.CondensedCM4P2E.RightKanReconstruction

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
    have hlc :=
      CategoryTheory.Adjunction.homEquiv_leftAdjointUniq_hom_app
        (CondensedSet.LocallyConstant.iso.{u}.homAdjunction)
        (Condensed.discreteUnderlyingAdj (Type (u + 1)))
        (ULift.{u + 1, u} Q1.obj)
    have hlcPoint :=
      CategoryTheory.types_congr_hom hlc (ULift.up PUnit.unit)
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
      dsimp [Q1] at hlcPoint ⊢
      simpa [
        CMDG.CondensedCM4P2E.finiteRepresentableCondensedIso,
        CMDG.CondensedCM4P2E.compHausTopULiftNatIso,
        CMDG.CondensedCM4P2E.compHausTopULiftIso,
        CMDG.CondensedCM4P2E.compHausTopULiftPresheafIso,
        CMDG.CondensedCM4P2E.continuousULiftSectionEquiv,
        CMDG.CondensedCM4P2E.finiteDiscreteCondensedIso,
        CMDG.CondensedCM4P2E.finiteDiscreteULiftIso,
        CMDG.CondensedCM4P2E.discreteTopCondensedIso,
        CondensedSet.LocallyConstant.iso,
        CompHausLike.LocallyConstant.unit] using hlcPoint
    rw [hrep]
    have huniq :=
      CategoryTheory.Adjunction.unit_leftAdjointUniq_hom_app
        CMDG.CondensedCM4P2E.discreteSetFreeAdj
        CMDG.CondensedCM4P2E.freeDiscreteModuleAdj
        (ULift.{u + 1, u} Q1.obj)
    have huniqPoint :=
      CategoryTheory.types_congr_hom huniq (ULift.up PUnit.unit)
    dsimp [Q1, qx, D, eTail, freeHomSectionsEquiv]
    simpa [
      Q,
      CMDG.CondensedCM4P2E.finiteFreeDiscreteIso,
      CMDG.CondensedCM4P2E.finiteRepresentableCondensedIso,
      CMDG.CondensedCM4P2E.finiteDiscreteCondensedIso,
      CMDG.CondensedCM4P2E.compHausTopULiftNatIso,
      CMDG.CondensedCM4P2E.compHausTopULiftIso,
      CMDG.CondensedCM4P2E.compHausTopULiftPresheafIso,
      CMDG.CondensedCM4P2E.continuousULiftSectionEquiv,
      CMDG.CondensedCM4P2E.finiteDiscreteULiftIso,
      CMDG.CondensedCM4P2E.discreteTopCondensedIso,
      CMDG.CondensedCM4P2E.discreteFreeIso,
      CMDG.CondensedCM4P2E.discreteSetFreeAdj,
      CMDG.CondensedCM4P2E.freeDiscreteModuleAdj,
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedDiscreteNatIso,
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeDiscreteULiftNatIso,
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftNatIso,
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftIso,
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftLinearEquiv,
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCoordinateInclusion,
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCoordinateModuleMap,
      ModuleCat.freeMk,
      Equiv.coe_fn_mk,
      Functor.FullyFaithful.homEquiv_apply,
      Functor.map_comp,
      Functor.comp_map,
      NatTrans.comp_app,
      ConcreteCategory.comp_apply,
      Functor.map_id,
      Category.id_comp,
      Category.comp_id,
      Category.assoc,
      Adjunction.comp_unit_app,
      Adjunction.homEquiv_naturality_left,
      ModuleCat.adj_homEquiv] using huniqPoint

#check profinitePointProbe
#check weightedFiniteBooleanMeasureHom_measureSolidification_evaluationWeight_allTrue
#print axioms weightedFiniteBooleanMeasureHom_measureSolidification_evaluationWeight_allTrue

end CMDG.CondensedCM4P3M.KernelPointBridge
