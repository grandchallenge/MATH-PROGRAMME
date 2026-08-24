import CMDGCondensedCM4P3LKernelFunctional

/-!
# CMDG CM4 P3-M — finite-stage recovery bridges

The first protected P3-M operation proves that an arbitrary finite family of chosen Nöbeling basis
functions descends through one common finite discrete quotient.  The second bounded operation,
`CMDG-CM4-P3-M-KERNEL-POINT-002`, begins the passage from the P3-L scalar kernel functional to the
pointwise Nöbeling combination required by the protected basis-separation theorem.

No lower-side recovery theorem, mapping-out injectivity, coefficient-object solidity, or P3
completion is asserted here.
-/

namespace CMDG.CondensedCM4P3M.FiniteQuotientBridge

universe u

open CMDG.CondensedCM4P3G
open CMDG.CondensedCM4P3G.BasisSeparation

/-- Package a finite family of chosen integral Nöbeling basis functions as one locally constant
map.  Finiteness of the subtype `I` is exactly what allows `LocallyConstant.unflip` to form the
joint observation. -/
noncomputable def finiteBasisFamily
    (X : Profinite.{u}) (I : Finset (IntegralBasisIndex X)) :
    LocallyConstant X (I → ℤ) :=
  LocallyConstant.unflip (fun i : I => integralBasis X i.1)

/-- Any finite family of chosen integral Nöbeling basis functions descends jointly through one
finite discrete quotient of `X`.

The proof deliberately uses only the existing cofiltered-limit factorization theorem already used
by protected P3-G: first package the family as one locally constant map, then factor that single
map through one stage. -/
theorem finiteBasisFamily_factors_common_discreteQuotient
    (X : Profinite.{u}) (I : Finset (IntegralBasisIndex X)) :
    ∃ (j : DiscreteQuotient X)
      (fQ : LocallyConstant (X.diagram.obj j) (I → ℤ)),
      finiteBasisFamily X I =
        fQ.comap (finiteQuotientMap X j).hom.hom := by
  exact
    Profinite.exists_locallyConstant X.asLimitCone X.asLimit
      (finiteBasisFamily X I)

/-- Coordinate form of `finiteBasisFamily_factors_common_discreteQuotient`: the same quotient
works simultaneously for every basis index in the finite set. -/
theorem integralBasis_factors_common_discreteQuotient
    (X : Profinite.{u}) (I : Finset (IntegralBasisIndex X)) :
    ∃ j : DiscreteQuotient X,
      ∀ i : I,
        ∃ fQ : LocallyConstant (X.diagram.obj j) ℤ,
          integralBasis X i.1 =
            fQ.comap (finiteQuotientMap X j).hom.hom := by
  obtain ⟨j, fQ, hf⟩ := finiteBasisFamily_factors_common_discreteQuotient X I
  refine ⟨j, ?_⟩
  intro i
  refine ⟨fQ.flip i, ?_⟩
  ext x
  change
    (finiteBasisFamily X I) x i =
      (fQ.comap (finiteQuotientMap X j).hom.hom) x i
  exact congrFun (LocallyConstant.congr_fun hf x) i

#check finiteBasisFamily_factors_common_discreteQuotient
#check integralBasis_factors_common_discreteQuotient
#print axioms finiteBasisFamily_factors_common_discreteQuotient
#print axioms integralBasis_factors_common_discreteQuotient

end CMDG.CondensedCM4P3M.FiniteQuotientBridge

namespace CMDG.CondensedCM4P3M.KernelPointBridge

universe u

open CategoryTheory
open CMDG.CondensedCM4P3G
open CMDG.CondensedCM4P3G.BasisSeparation
open CMDG.CondensedCM4P3G.BasisBooleanPairing
open CMDG.CondensedCM4P3G.BasisBooleanPairingR
open CMDG.CondensedCM4P3G.FiniteSupport
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3J.WeightedBooleanMeasure

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
    rfl
  have hv := congrArg (fun f : LocallyConstant X ℤ →ₗ[ℤ] ℤ => f v) hlhs
  simpa [lhs] using hv

/-- Evaluating the finite Nöbeling coefficient combination associated to an additive
functional `L` at `x` is the same as applying `L` to the finite truncation of the vector of
basis values at `x`.

This is the explicit finite-support expression required before any kernel/measure comparison:
it is purely algebraic and introduces no vanishing or separation claim. -/
theorem basisCombination_finiteFunctionalCoefficients_apply
    (X : Profinite.{u})
    (L : (IntegralBasisIndex X → ℤ) →+ ℤ)
    (I : Finset (IntegralBasisIndex X))
    (x : X) :
    basisCombination X (finiteFunctionalCoefficients X L I) x =
      L (finiteTruncation (integralBasisEvaluationWeight X x) I) := by
  classical
  rw [← weightedBasisBooleanPairing_evaluationWeight_allTrue X x
    (basisCombination X (finiteFunctionalCoefficients X L I))]
  rw [weightedBasisBooleanPairing_apply]
  rw [finiteTruncation_eq_sum, map_sum]
  simp_rw [map_zsmul]
  simp only [basisCombination, LinearEquiv.apply_symm_apply,
    weightedBasisBooleanCombination, finiteFunctionalCoefficients]
  rw [Finsupp.linearCombination_onFinset]
  simp [weightedBasisBooleanCoordinate, basisBooleanCoordinate,
    integralBasisEvaluationWeight, mul_comm]
  change (LocallyConstant.evalRingHom (fun _ => true)) _ = _
  rw [map_sum]
  simp [LocallyConstant.evalRingHom, basisBooleanCoordinate]

/-- At every finite quotient, the full basis-evaluation weight turns the weighted Boolean
coefficient at the all-true selector into the literal pulled-back finite delta evaluated at `x`.
This is the finite-stage Dirac identity needed before any global measure/solid comparison. -/
theorem weightedFiniteBooleanCoefficient_evaluationWeight_allTrue
    (X : Profinite.{u}) (x : X)
    (j : DiscreteQuotient X)
    (q : (FiniteQuotientObject X j).obj) :
    weightedFiniteBooleanCoefficient X (integralBasisEvaluationWeight X x) j q
        (fun _ => true) =
      finiteDeltaPullbackR X j q x := by
  change
    ULift.up
      (weightedBasisBooleanPairing X (integralBasisEvaluationWeight X x)
        (locallyConstantIntegralDownEquiv X (finiteDeltaPullbackR X j q))
        (fun _ => true)) =
      finiteDeltaPullbackR X j q x
  rw [weightedBasisBooleanPairing_evaluationWeight_allTrue]
  rfl

/-- Pulling the finite weighted coefficient family for the full evaluation weight to the all-true
one-point probe gives exactly the canonical coefficient-family coordinate delta at the quotient
point represented by `x`. -/
theorem weightedFiniteBooleanCoefficientFamily_evaluationWeight_allTrue
    (X : Profinite.{u}) (x : X)
    (j : DiscreteQuotient X) :
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf
        (FiniteQuotientObject X j)).map
        ((profiniteToCompHaus).map
          (CMDG.CondensedCM4P3L.KernelFunctional.basisBooleanPointProbe X
            (fun _ => true))).op))
      (weightedFiniteBooleanCoefficientFamily X (integralBasisEvaluationWeight X x) j) =
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion
        (X.fintypeDiagram.obj j) (j.proj x)).app
        (Opposite.op
          ((profiniteToCompHaus).obj (Profinite.of PUnit.{u + 1})))))
      (1 : LocallyConstant (Profinite.of PUnit.{u + 1}) R) := by
  funext q
  apply LocallyConstant.ext
  intro z
  change
    weightedFiniteBooleanCoefficient X (integralBasisEvaluationWeight X x) j q
        (fun _ => true) =
      if q = j.proj x then 1 else 0
  rw [weightedFiniteBooleanCoefficient_evaluationWeight_allTrue]
  simp [finiteDeltaPullbackR, eq_comm]

#check integralBasisEvaluationWeight
#check weightedBasisBooleanPairing_evaluationWeight_allTrue
#check basisCombination_finiteFunctionalCoefficients_apply
#check weightedFiniteBooleanCoefficient_evaluationWeight_allTrue
#check weightedFiniteBooleanCoefficientFamily_evaluationWeight_allTrue
#print axioms weightedBasisBooleanPairing_evaluationWeight_allTrue
#print axioms basisCombination_finiteFunctionalCoefficients_apply
#print axioms weightedFiniteBooleanCoefficient_evaluationWeight_allTrue
#print axioms weightedFiniteBooleanCoefficientFamily_evaluationWeight_allTrue

end CMDG.CondensedCM4P3M.KernelPointBridge
