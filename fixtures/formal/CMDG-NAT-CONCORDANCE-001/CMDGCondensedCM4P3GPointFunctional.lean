import CMDGCondensedCM4P3G
import CMDGCondensedCM4P3GBasisBooleanPairingR

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