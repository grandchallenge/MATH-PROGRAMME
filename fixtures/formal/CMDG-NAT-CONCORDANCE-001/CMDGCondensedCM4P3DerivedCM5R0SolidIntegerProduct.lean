import CMDGCondensedCM4P3DerivedCM5R0IntegerProductBridge
import CMDGCondensedCM4P3DerivedCM5R0GSCondensedProduct
import Mathlib.Logic.Small.Basic

/-! Reindex the genuine protected free-solid coefficient fan into the
small universe of the real/circle sequence. The resulting isomorphism
uses the actual coordinate maps, not a bare group equivalence. -/
noncomputable section
universe u
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.RealCircleStoneanPresheaf
open CMDG.CondensedCM5R0.IntegerProductBridge
namespace CMDG.CondensedCM5R0.SolidIntegerProduct

theorem basisSmall (T : Profinite.{u}) : Small.{u} (LiftedSourceBasisIndex T) :=
  small_of_injective ((integralToLiftedLocallyConstantSemilinearEquiv T).symm.injective.comp
    (liftedSourceBasis T).injective)

local instance (T : Profinite.{u}) : Small.{u} (LiftedSourceBasisIndex T) := basisSmall T

abbrev Index (T : Profinite.{u}) : Type u := Shrink.{u} (LiftedSourceBasisIndex T)
def indexEquiv (T : Profinite.{u}) : Index T ≃ LiftedSourceBasisIndex T :=
  (equivShrink (LiftedSourceBasisIndex T)).symm

def reindexedBasisFan (T : Profinite.{u}) : Fan (fun _ : Index T => Zdisc.{u}) :=
  Fan.mk (gsBasisInternalHomCondensed T)
    (fun i => (gsBasisCondensedCoefficientFan T).proj (indexEquiv T i))

def reindexedBasisFanIsLimit (T : Profinite.{u}) : IsLimit (reindexedBasisFan T) :=
  (Fan.isLimitEquivOfEquiv (indexEquiv T) (gsBasisCondensedCoefficientFan T)).toFun
    (gsBasisCondensedCoefficientFanIsLimit T)

def solidIntegerIso (T : Profinite.{u}) :
    underivedObject T ≅ (realCircleCondensedSequence (Index T)).X₁ :=
  freeSolidToBasisInternalHomCondensedIso T ≪≫
    (reindexedBasisFanIsLimit T).conePointUniqueUpToIso (integerFanIsLimit (Index T))

set_option backward.isDefEq.respectTransparency false in
/-- The forward isomorphism matches the protected coordinate morphisms. -/
theorem solidIntegerIso_projection (T : Profinite.{u}) (i : Index T) :
    (solidIntegerIso T).hom ≫ (integerFan (Index T)).proj i =
      gsFreeSolidCoefficientCoordinate T (indexEquiv T i) := by
  change ((freeSolidToBasisInternalHomCondensedIso T).hom ≫
      ((reindexedBasisFanIsLimit T).conePointUniqueUpToIso
        (integerFanIsLimit (Index T))).hom) ≫
      (integerFan (Index T)).proj i = _
  rw [Category.assoc]
  have h := (reindexedBasisFanIsLimit T).conePointUniqueUpToIso_hom_comp
    (integerFanIsLimit (Index T)) (Discrete.mk i)
  change ((reindexedBasisFanIsLimit T).conePointUniqueUpToIso
        (integerFanIsLimit (Index T))).hom ≫ (integerFan (Index T)).proj i =
          (reindexedBasisFan T).proj i at h
  rw [h]
  rfl

#print axioms basisSmall
#print axioms solidIntegerIso
#print axioms solidIntegerIso_projection
end CMDG.CondensedCM5R0.SolidIntegerProduct
