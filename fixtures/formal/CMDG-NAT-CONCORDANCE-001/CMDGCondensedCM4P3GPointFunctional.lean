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
        (profinitePointProbe (X.diagram.obj j) (j.proj x)) ≫
      measureSolidification.app (X.diagram.obj j) := by
  let P := Profinite.of PUnit.{u + 1}
  let T := CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X
  let Q := FiniteQuotientObject X j
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
  rw [measureSolidification_fac]
  simp only [Category.comp_id]
  apply (cancel_mono eFree).1
  simp only [Category.assoc]
  let e := eComp ≫ eFree
  have hpost :
      freeHomSectionsEquiv T D
          (weightedFiniteBooleanMeasureHom X (integralBasisEvaluationWeight X x) j ≫ e) =
        (ConcreteCategory.hom (((Condensed.forget CMDG.CondensedCM4P3G.R.{u}).map e).hom.app S))
          (freeHomSectionsEquiv T A
            (weightedFiniteBooleanMeasureHom X (integralBasisEvaluationWeight X x) j)) := by
    change
      (coherentTopology CompHaus.{u}).uliftYonedaEquiv
        ((Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv
          ((profiniteToCondensed).obj T) D
          (weightedFiniteBooleanMeasureHom X (integralBasisEvaluationWeight X x) j ≫ e)) = _
    rw [(Condensed.freeForgetAdjunction CMDG.CondensedCM4P3G.R.{u}).homEquiv_naturality_right]
    rfl
  have hsection :
      freeHomSectionsEquiv T A
          (weightedFiniteBooleanMeasureHom X (integralBasisEvaluationWeight X x) j) =
        weightedFiniteBooleanMeasureSection X (integralBasisEvaluationWeight X x) j := by
    exact Equiv.apply_symm_apply _ _
  apply (freeHomSectionsEquiv P D).injective
  rw [Category.assoc]
  rw [freeHomSectionsEquiv_precomp]
  rw [hpost, hsection]
  trace_state
  exact weightedFiniteBooleanMeasureSection_smallFree_evaluationWeight_allTrue X x j

#check profinitePointProbe
#check weightedFiniteBooleanMeasureHom_measureSolidification_evaluationWeight_allTrue
#print axioms weightedFiniteBooleanMeasureHom_measureSolidification_evaluationWeight_allTrue

end CMDG.CondensedCM4P3M.KernelPointBridge