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
      simp only [Functor.map_comp, Category.assoc]
      have hunitNat :=
        ((Condensed.discreteUnderlyingAdj
          (ModuleCat CMDG.CondensedCM4P3G.R.{u})).unit.naturality
            (CondensedMod.LocallyConstant.functorIsoDiscreteAux₁
              CMDG.CondensedCM4P3G.R.{u} M).hom).symm
      simp only [Functor.comp_map, Functor.id_map] at hunitNat
      rw [hunitNat]
      simp only [Category.assoc,
        (Condensed.discreteUnderlyingAdj
          (ModuleCat CMDG.CondensedCM4P3G.R.{u})).right_triangle_components,
        Category.comp_id]
    have hlcUnitPoint :
        (ConcreteCategory.hom
          ((CondensedMod.LocallyConstant.adjunction CMDG.CondensedCM4P3G.R.{u}).unit.app M))
          (ModuleCat.freeMk (ULift.up (j.proj x))) =
        LocallyConstant.const (CompHaus.of PUnit.{u + 1})
          (ModuleCat.freeMk (ULift.up (j.proj x))) := by
      rw [hlcUnitMap]
      rfl
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
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeULiftLinearEquiv_single,
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCoordinateInclusion_apply,
      CondensedMod.LocallyConstant.functorIsoDiscrete,
      CondensedMod.LocallyConstant.functorIsoDiscreteComponents,
      CondensedMod.LocallyConstant.functorIsoDiscreteAux₂,
      CondensedMod.LocallyConstant.functorIsoDiscreteAux₁,
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
      Adjunction.comp_homEquiv,
      Equiv.trans_apply,
      Adjunction.homEquiv_unit,
      Adjunction.homEquiv_naturality_left,
      ModuleCat.adj_homEquiv]

#check profinitePointProbe
#check weightedFiniteBooleanMeasureHom_measureSolidification_evaluationWeight_allTrue
#print axioms weightedFiniteBooleanMeasureHom_measureSolidification_evaluationWeight_allTrue

end CMDG.CondensedCM4P3M.KernelPointBridge
