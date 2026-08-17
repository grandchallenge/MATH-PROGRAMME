import CMDGCondensedCM4P3GBasisBooleanPairingR
import CMDGCondensedCM4P2EFiniteMeasureTransport
import CMDGCondensedCM4P2EFiniteDualFamilyIso

/-!
# CMDG CM4-P3-G finite-stage Boolean measure family

For each finite quotient of `X`, this fixture constructs the `0/1` Nöbeling-coordinate measure
family over the Boolean basis cube. The construction is entirely finite-stage: finite deltas are
pulled back to `X`, paired against the chosen Nöbeling basis, and transported through the
already-certified finite measure/family isomorphisms.
-/

namespace CMDG.CondensedCM4P3G.FiniteBooleanMeasure

universe u

open CategoryTheory Opposite

open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BasisBooleanPairing
open CMDG.CondensedCM4P3G.BasisBooleanPairingR

abbrev R := CMDG.CondensedCM4P3G.R.{u}

abbrev FiniteQuotientObject (X : Profinite.{u}) (j : DiscreteQuotient X) :=
  X.fintypeDiagram.obj j

/-- Pull the delta at a finite-quotient point directly back to `X`. This avoids re-exposing the
packaged quotient topology: `j.proj` is already certified locally constant by `DiscreteQuotient`. -/
noncomputable def finiteDeltaPullbackR
    (X : Profinite.{u}) (j : DiscreteQuotient X)
    (q : (FiniteQuotientObject X j).obj) :
    LocallyConstant X R.{u} := by
  classical
  exact
    { toFun := fun x => if j.proj x = q then 1 else 0
      isLocallyConstant :=
        j.proj_isLocallyConstant.comp
          (fun y => if y = q then (1 : R.{u}) else 0) }

/-- The Boolean basis-coordinate function attached to one finite-quotient point: pull the finite
delta back to `X` and apply the already-certified lifted Nöbeling Boolean pairing. -/
noncomputable def finiteBooleanCoefficient
    (X : Profinite.{u}) (j : DiscreteQuotient X)
    (q : (FiniteQuotientObject X j).obj) :
    LocallyConstant (basisBooleanCube X) R.{u} := by
  change LocallyConstant (IntegralBasisIndex X → Bool) R.{u}
  exact
    (basisBooleanPairingR X :
      LocallyConstant X R.{u} →ₗ[R.{u}]
        LocallyConstant (IntegralBasisIndex X → Bool) R.{u})
      (finiteDeltaPullbackR X j q)

/-- The whole finite family of Boolean coefficient functions at one finite quotient. -/
noncomputable def finiteBooleanCoefficientFamily
    (X : Profinite.{u}) (j : DiscreteQuotient X) :
    (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf
      (FiniteQuotientObject X j)).obj
      (op ((profiniteToCompHaus).obj (basisBooleanCube X))) := by
  exact fun q => finiteBooleanCoefficient X j q

/-- Transport the concrete coefficient family to a section of the actual finite P2-D measure
presheaf. -/
noncomputable def finiteBooleanMeasureSection
    (X : Profinite.{u}) (j : DiscreteQuotient X) :
    (CMDG.CondensedCM4P2D.measurePresheafObj (X.diagram.obj j)).obj
      (op ((profiniteToCompHaus).obj (basisBooleanCube X))) := by
  let Q := FiniteQuotientObject X j
  let S := op ((profiniteToCompHaus).obj (basisBooleanCube X))
  let a := finiteBooleanCoefficientFamily X j
  let b :=
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteFamilyInternalHomIso Q).inv.app S)) a
  exact
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFamilyIso Q).inv.app S)) b

#print finiteDeltaPullbackR
#print finiteBooleanCoefficient
#print finiteBooleanCoefficientFamily
#print finiteBooleanMeasureSection
#print axioms finiteBooleanMeasureSection

end CMDG.CondensedCM4P3G.FiniteBooleanMeasure
