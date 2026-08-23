import CMDGCondensedCM4P3MFiniteQuotientBridge

/-!
# CMDG CM4 P3-M — pointwise Nöbeling kernel bridge

This file implements only the first concrete lemma under
`CMDG-CM4-P3-M-KERNEL-POINT-002`.

The immediate question is whether the arbitrary-weight Nöbeling Boolean pairing already contains
ordinary point evaluation as a special weight vector.  This is a prerequisite for converting the
P3-L scalar kernel functional into the pointwise Nöbeling combination required by the protected
basis-separation theorem.

No solidification-kernel separation, mapping-out injectivity, solidity, or P3 completion is asserted
here.
-/

namespace CMDG.CondensedCM4P3M.KernelPointBridge

universe u

open CMDG.CondensedCM4P3G
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BasisBooleanPairing

/-- At a point `x`, use the values of the chosen Nöbeling basis functions as the external weight
vector. -/
noncomputable def integralBasisEvaluationWeight
    (X : Profinite.{u}) (x : X) : IntegralBasisIndex X → ℤ :=
  fun i => integralBasis X i x

/-- The weighted Boolean pairing at the all-true selector, with weights obtained by evaluating the
basis at `x`, is exactly ordinary evaluation at `x`.

The proof compares the two linear functionals on the chosen basis, avoiding any global finite-sum
normal-form argument. -/
theorem weightedBasisBooleanPairing_evaluationWeight_allTrue
    (X : Profinite.{u}) (x : X) (v : LocallyConstant X ℤ) :
    weightedBasisBooleanPairing X (integralBasisEvaluationWeight X x) v
        (fun _ => true) =
      v x := by
  let lhs : LocallyConstant X ℤ →ₗ[ℤ] ℤ :=
    (LocallyConstant.evalₗ ℤ (fun _ => true)).comp
      (weightedBasisBooleanPairing X (integralBasisEvaluationWeight X x))
  have hlhs : lhs = LocallyConstant.evalₗ ℤ x := by
    apply (integralBasis X).ext
    intro i
    change
      weightedBasisBooleanPairing X (integralBasisEvaluationWeight X x)
          (integralBasis X i) (fun _ => true) =
        integralBasis X i x
    rw [weightedBasisBooleanPairing_apply, Module.Basis.repr_self]
    simp [weightedBasisBooleanCombination, weightedBasisBooleanCoordinate,
      basisBooleanCoordinate, integralBasisEvaluationWeight]
  have hv := congrArg (fun f : LocallyConstant X ℤ →ₗ[ℤ] ℤ => f v) hlhs
  simpa [lhs] using hv

#check integralBasisEvaluationWeight
#check weightedBasisBooleanPairing_evaluationWeight_allTrue
#print axioms weightedBasisBooleanPairing_evaluationWeight_allTrue

end CMDG.CondensedCM4P3M.KernelPointBridge
