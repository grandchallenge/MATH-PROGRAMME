import CMDGCondensedCM4P3GBasisSeparation
import Mathlib.LinearAlgebra.Finsupp.LinearCombination

/-!
# CMDG CM4-P3-G Nöbeling Boolean pairing

This fixture builds the linear Boolean-coordinate family associated to the chosen Nöbeling basis.
For a basis-coordinate vector `t : B → Bool`, evaluating the resulting locally constant function
implements the `0/1` pairing with the finite basis representation of an element of `C(X, ℤ)`.
-/

namespace CMDG.CondensedCM4P3G.BasisBooleanPairing

universe u

open scoped Topology

open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.FiniteSupport

/-- The locally constant `0/1` coordinate function on the Boolean basis cube. -/
def basisBooleanCoordinate (X : Profinite.{u}) (b : IntegralBasisIndex X) :
    LocallyConstant (IntegralBasisIndex X → Bool) ℤ where
  toFun t := if t b then 1 else 0
  isLocallyConstant := by
    rw [IsLocallyConstant.iff_continuous]
    exact
      (continuous_of_discreteTopology
        (f := fun a : Bool => if a then (1 : ℤ) else 0)).comp
        (continuous_apply b)

/-- Interpret a finite integral basis-coordinate vector as the corresponding locally constant
linear combination of Boolean coordinate functions. -/
noncomputable def basisBooleanCombination (X : Profinite.{u}) :
    (IntegralBasisIndex X →₀ ℤ) →ₗ[ℤ]
      LocallyConstant (IntegralBasisIndex X → Bool) ℤ :=
  Finsupp.linearCombination ℤ (basisBooleanCoordinate X)

/-- The universal Boolean pairing attached to the chosen Nöbeling basis. -/
noncomputable def basisBooleanPairing (X : Profinite.{u}) :
    LocallyConstant X ℤ →ₗ[ℤ]
      LocallyConstant (IntegralBasisIndex X → Bool) ℤ :=
  (basisBooleanCombination X).comp (integralBasis X).repr.toLinearMap

theorem basisBooleanPairing_apply (X : Profinite.{u})
    (v : LocallyConstant X ℤ) :
    basisBooleanPairing X v =
      basisBooleanCombination X ((integralBasis X).repr v) := by
  rfl

#print basisBooleanCoordinate
#print basisBooleanCombination
#print basisBooleanPairing
#print axioms basisBooleanPairing

end CMDG.CondensedCM4P3G.BasisBooleanPairing
