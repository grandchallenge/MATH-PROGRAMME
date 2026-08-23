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
    rfl
  have hv := congrArg (fun f : LocallyConstant X ℤ →ₗ[ℤ] ℤ => f v) hlhs
  simpa [lhs] using hv

#check integralBasisEvaluationWeight
#check weightedBasisBooleanPairing_evaluationWeight_allTrue
#print axioms weightedBasisBooleanPairing_evaluationWeight_allTrue

end CMDG.CondensedCM4P3M.KernelPointBridge
