import CMDGCondensedCM4P3JWeightedBooleanMeasure
import CMDGCondensedCM4P2EE3

/-!
# CMDG CM4-P3-K — kernel functional and weighted finite dependence

This successor isolates the algebraic bridge from the protected P3-J weighted Boolean measure
families to the protected weighted finite-coordinate-dependence theorem.  The first layer records
the two identities needed downstream: additivity in the arbitrary integer weight vector and
selector reweighting on the Boolean basis cube.

No mapping-out injectivity, coefficient-object solidity, or P3 completion is asserted here.
-/

namespace CMDG.CondensedCM4P3K.KernelFiniteDependence

universe u

open CategoryTheory Limits Opposite
open scoped BigOperators

open CMDG.CondensedCM4P3G
open CMDG.CondensedCM4P3G.FiniteSupport
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BasisBooleanPairing
open CMDG.CondensedCM4P3G.BasisBooleanPairingR
open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3J.WeightedBooleanMeasure
open CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness

abbrev R := CMDG.CondensedCM4P3G.R.{u}

/-- The weighted Boolean coordinate family is additive in the external weight vector. -/
theorem weightedBasisBooleanCoordinate_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ) (i : IntegralBasisIndex X) :
    weightedBasisBooleanCoordinate X (a + b) i =
      weightedBasisBooleanCoordinate X a i +
        weightedBasisBooleanCoordinate X b i := by
  ext t
  simp [weightedBasisBooleanCoordinate, basisBooleanCoordinate, add_smul]

/-- Finite weighted Boolean combinations are additive in the external weight vector. -/
theorem weightedBasisBooleanCombination_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ)
    (c : IntegralBasisIndex X →₀ ℤ) :
    weightedBasisBooleanCombination X (a + b) c =
      weightedBasisBooleanCombination X a c +
        weightedBasisBooleanCombination X b c := by
  classical
  apply LocallyConstant.ext
  intro t
  simp [weightedBasisBooleanCombination, Finsupp.linearCombination_apply,
    weightedBasisBooleanCoordinate, basisBooleanCoordinate, add_smul, smul_add,
    Finset.sum_add_distrib]

/-- Evaluating at a Boolean selector is the same as absorbing that selector into the weights and
then evaluating at the all-true selector. -/
theorem weightedBasisBooleanCombination_reweight_eval
    (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ)
    (c : IntegralBasisIndex X →₀ ℤ)
    (t : IntegralBasisIndex X → Bool) :
    weightedBasisBooleanCombination X a c t =
      weightedBasisBooleanCombination X (weightedBoolToInt a t) c
        (fun _ => true) := by
  classical
  let evalAt (s : IntegralBasisIndex X → Bool) :
      LocallyConstant (IntegralBasisIndex X → Bool) ℤ →+ ℤ :=
    { toFun := fun f => f s
      map_zero' := rfl
      map_add' := by intro f g; rfl }
  change
    evalAt t (weightedBasisBooleanCombination X a c) =
      evalAt (fun _ => true)
        (weightedBasisBooleanCombination X (weightedBoolToInt a t) c)
  simp only [weightedBasisBooleanCombination, Finsupp.linearCombination_apply,
    Finsupp.sum, map_sum]
  apply Finset.sum_congr rfl
  intro i hi
  cases h : t i <;>
    simp [evalAt, weightedBasisBooleanCoordinate, basisBooleanCoordinate,
      weightedBoolToInt, h]

/-- The integral weighted Nöbeling pairing is additive in its external weight vector. -/
theorem weightedBasisBooleanPairing_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ)
    (v : LocallyConstant X ℤ) :
    weightedBasisBooleanPairing X (a + b) v =
      weightedBasisBooleanPairing X a v +
        weightedBasisBooleanPairing X b v := by
  change
    weightedBasisBooleanCombination X (a + b) ((integralBasis X).repr v) =
      weightedBasisBooleanCombination X a ((integralBasis X).repr v) +
        weightedBasisBooleanCombination X b ((integralBasis X).repr v)
  exact weightedBasisBooleanCombination_add X a b ((integralBasis X).repr v)

/-- Selector reweighting for the integral weighted Nöbeling pairing. -/
theorem weightedBasisBooleanPairing_reweight_eval
    (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ)
    (v : LocallyConstant X ℤ)
    (t : IntegralBasisIndex X → Bool) :
    weightedBasisBooleanPairing X a v t =
      weightedBasisBooleanPairing X (weightedBoolToInt a t) v
        (fun _ => true) := by
  change
    weightedBasisBooleanCombination X a ((integralBasis X).repr v) t =
      weightedBasisBooleanCombination X (weightedBoolToInt a t)
        ((integralBasis X).repr v) (fun _ => true)
  exact weightedBasisBooleanCombination_reweight_eval X a ((integralBasis X).repr v) t

/-- The lifted weighted pairing remains additive in its external weight vector. -/
theorem weightedBasisBooleanPairingR_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ)
    (v : LocallyConstant X R.{u}) :
    weightedBasisBooleanPairingR.{u, u, u, u} X (a + b) v =
      weightedBasisBooleanPairingR.{u, u, u, u} X a v +
        weightedBasisBooleanPairingR.{u, u, u, u} X b v := by
  apply LocallyConstant.ext
  intro t
  change
    ULift.up
        (weightedBasisBooleanPairing X (a + b)
          (locallyConstantIntegralDownEquiv X v) t) =
      ULift.up
          (weightedBasisBooleanPairing X a
            (locallyConstantIntegralDownEquiv X v) t) +
        ULift.up
          (weightedBasisBooleanPairing X b
            (locallyConstantIntegralDownEquiv X v) t)
  rw [weightedBasisBooleanPairing_add X a b]
  rfl

/-- Selector reweighting survives scalar extension to the lifted coefficient ring. -/
theorem weightedBasisBooleanPairingR_reweight_eval
    (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ)
    (v : LocallyConstant X R.{u})
    (t : IntegralBasisIndex X → Bool) :
    weightedBasisBooleanPairingR.{u, u, u, u} X a v t =
      weightedBasisBooleanPairingR.{u, u, u, u} X (weightedBoolToInt a t) v
        (fun _ => true) := by
  change
    ULift.up
        (weightedBasisBooleanPairing X a
          (locallyConstantIntegralDownEquiv X v) t) =
      ULift.up
        (weightedBasisBooleanPairing X (weightedBoolToInt a t)
          (locallyConstantIntegralDownEquiv X v) (fun _ => true))
  exact congrArg ULift.up
    (weightedBasisBooleanPairing_reweight_eval X a
      (locallyConstantIntegralDownEquiv X v) t)

/-- Weighted finite Boolean coefficients are additive in the weight vector. -/
theorem weightedFiniteBooleanCoefficient_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) (q : j) :
    weightedFiniteBooleanCoefficient X (a + b) j q =
      weightedFiniteBooleanCoefficient X a j q +
        weightedFiniteBooleanCoefficient X b j q := by
  change
    weightedBasisBooleanPairingR.{u, u, u, u} X (a + b)
        (finiteDeltaPullbackR X j q) =
      weightedBasisBooleanPairingR.{u, u, u, u} X a
          (finiteDeltaPullbackR X j q) +
        weightedBasisBooleanPairingR.{u, u, u, u} X b
          (finiteDeltaPullbackR X j q)
  exact weightedBasisBooleanPairingR_add X a b (finiteDeltaPullbackR X j q)

/-- Weighted finite Boolean coefficients obey selector reweighting pointwise. -/
theorem weightedFiniteBooleanCoefficient_reweight_eval
    (X : Profinite.{u})
    (a : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) (q : j)
    (t : IntegralBasisIndex X → Bool) :
    weightedFiniteBooleanCoefficient X a j q t =
      weightedFiniteBooleanCoefficient X (weightedBoolToInt a t) j q
        (fun _ => true) := by
  change
    weightedBasisBooleanPairingR.{u, u, u, u} X a
        (finiteDeltaPullbackR X j q) t =
      weightedBasisBooleanPairingR.{u, u, u, u} X (weightedBoolToInt a t)
        (finiteDeltaPullbackR X j q) (fun _ => true)
  exact weightedBasisBooleanPairingR_reweight_eval X a
    (finiteDeltaPullbackR X j q) t

/-- The finite coefficient family is additive in the weight vector. -/
theorem weightedFiniteBooleanCoefficientFamily_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) :
    weightedFiniteBooleanCoefficientFamily X (a + b) j =
      weightedFiniteBooleanCoefficientFamily X a j +
        weightedFiniteBooleanCoefficientFamily X b j := by
  funext q
  exact weightedFiniteBooleanCoefficient_add X a b j q

/-- Additivity transports through the protected finite coefficient-to-measure equivalences. -/
theorem weightedFiniteBooleanMeasureSection_add
    (X : Profinite.{u})
    (a b : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) :
    weightedFiniteBooleanMeasureSection X (a + b) j =
      weightedFiniteBooleanMeasureSection X a j +
        weightedFiniteBooleanMeasureSection X b j := by
  change
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFamilyIso
        (FiniteQuotientObject X j)).inv.app
        (op ((profiniteToCompHaus).obj (basisBooleanCube X)))))
      ((ConcreteCategory.hom
        ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteFamilyInternalHomIso
          (FiniteQuotientObject X j)).inv.app
          (op ((profiniteToCompHaus).obj (basisBooleanCube X)))))
        (weightedFiniteBooleanCoefficientFamily X (a + b) j)) = _
  rw [weightedFiniteBooleanCoefficientFamily_add X a b j, map_add, map_add]

#check weightedBasisBooleanPairing_add
#check weightedBasisBooleanPairing_reweight_eval
#check weightedBasisBooleanPairingR_add
#check weightedBasisBooleanPairingR_reweight_eval
#check weightedFiniteBooleanCoefficient_add
#check weightedFiniteBooleanCoefficient_reweight_eval
#check weightedFiniteBooleanCoefficientFamily_add
#check weightedFiniteBooleanMeasureSection_add

#print axioms weightedBasisBooleanPairing_add
#print axioms weightedBasisBooleanPairing_reweight_eval
#print axioms weightedBasisBooleanPairingR_add
#print axioms weightedBasisBooleanPairingR_reweight_eval
#print axioms weightedFiniteBooleanMeasureSection_add

end CMDG.CondensedCM4P3K.KernelFiniteDependence
