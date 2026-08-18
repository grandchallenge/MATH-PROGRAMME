import CMDGCondensedCM4P3GBasisSeparation
import Mathlib.LinearAlgebra.Finsupp.LinearCombination

/-!
# CMDG CM4-P3-G Nöbeling Boolean pairing

This fixture builds the linear Boolean-coordinate family associated to the chosen Nöbeling basis.
For a basis-coordinate vector `t : B → Bool`, evaluating the resulting locally constant function
implements the `0/1` pairing with the finite basis representation of an element of `C(X, ℤ)`.
The weighted variant scales each Boolean coordinate by an arbitrary integer weight vector; this is
the family required for the full finite-coordinate-dependence argument.
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

/-- Boolean coordinate `b`, scaled by the arbitrary integer weight `a b`. -/
def weightedBasisBooleanCoordinate (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ) (b : IntegralBasisIndex X) :
    LocallyConstant (IntegralBasisIndex X → Bool) ℤ :=
  (a b) • basisBooleanCoordinate X b

/-- Interpret finite basis coordinates using the weighted Boolean coordinate family. -/
noncomputable def weightedBasisBooleanCombination (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ) :
    (IntegralBasisIndex X →₀ ℤ) →ₗ[ℤ]
      LocallyConstant (IntegralBasisIndex X → Bool) ℤ :=
  Finsupp.linearCombination ℤ (weightedBasisBooleanCoordinate X a)

/-- The weighted Boolean pairing. For weight vector `a`, its Boolean restriction records the
basis-coordinate functional with coordinate `b` multiplied by `a b`. -/
noncomputable def weightedBasisBooleanPairing (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ) :
    LocallyConstant X ℤ →ₗ[ℤ]
      LocallyConstant (IntegralBasisIndex X → Bool) ℤ :=
  (weightedBasisBooleanCombination X a).comp (integralBasis X).repr.toLinearMap

theorem weightedBasisBooleanPairing_apply (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ) (v : LocallyConstant X ℤ) :
    weightedBasisBooleanPairing X a v =
      weightedBasisBooleanCombination X a ((integralBasis X).repr v) := by
  rfl

#print basisBooleanCoordinate
#print basisBooleanCombination
#print basisBooleanPairing
#print weightedBasisBooleanCoordinate
#print weightedBasisBooleanCombination
#print weightedBasisBooleanPairing
#print axioms basisBooleanPairing
#print axioms weightedBasisBooleanPairing

end CMDG.CondensedCM4P3G.BasisBooleanPairing
