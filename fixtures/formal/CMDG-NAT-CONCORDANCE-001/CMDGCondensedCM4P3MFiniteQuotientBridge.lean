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
open CMDG.CondensedCM4P3L.KernelFunctional

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

/-- A finite-coordinate kernel witness for the P3-L product functional identifies the finite
truncation of the basis-evaluation weight with the full evaluation-weight vector after applying
that functional.  No solidification-kernel hypothesis is used here. -/
theorem kernelProductFunctional_finiteTruncation_evaluationWeight
    (X : Profinite.{u})
    (d : (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X ⟶ coefficientObject)
    (I : Finset (IntegralBasisIndex X))
    (hI :
      ∀ a : IntegralBasisIndex X → ℤ,
        (∀ i ∈ I, a i = 0) →
        kernelProductFunctional X d a = 0)
    (x : X) :
    kernelProductFunctional X d
        (finiteTruncation (integralBasisEvaluationWeight X x) I) =
      kernelProductFunctional X d (integralBasisEvaluationWeight X x) := by
  have hzero :
      kernelProductFunctional X d
          (finiteTruncation (integralBasisEvaluationWeight X x) I -
            integralBasisEvaluationWeight X x) = 0 := by
    apply hI
    intro i hi
    simp [finiteTruncation, hi]
  rw [map_sub] at hzero
  exact sub_eq_zero.mp hzero

/-- Under the same P3-L finite-coordinate kernel witness, the concrete finite Nöbeling
combination is exactly the product functional evaluated on the full vector of basis values at the
point.  The remaining P3-M question is therefore whether the solidification-kernel hypothesis
forces this full evaluation-weight value to vanish. -/
theorem basisCombination_kernelProductFunctional_finiteCoefficients_apply
    (X : Profinite.{u})
    (d : (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).obj X ⟶ coefficientObject)
    (I : Finset (IntegralBasisIndex X))
    (hI :
      ∀ a : IntegralBasisIndex X → ℤ,
        (∀ i ∈ I, a i = 0) →
        kernelProductFunctional X d a = 0)
    (x : X) :
    basisCombination X
        (finiteFunctionalCoefficients X (kernelProductFunctional X d) I) x =
      kernelProductFunctional X d (integralBasisEvaluationWeight X x) := by
  rw [basisCombination_finiteFunctionalCoefficients_apply]
  exact kernelProductFunctional_finiteTruncation_evaluationWeight X d I hI x

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
      (1 : LocallyConstant (Profinite.of PUnit.{u + 1}) CMDG.CondensedCM4P3G.R.{u}) := by
  classical
  funext q
  apply LocallyConstant.ext
  intro z
  calc
    ((ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf
        (FiniteQuotientObject X j)).map
        ((profiniteToCompHaus).map
          (CMDG.CondensedCM4P3L.KernelFunctional.basisBooleanPointProbe X
            (fun _ => true))).op))
      (weightedFiniteBooleanCoefficientFamily X (integralBasisEvaluationWeight X x) j) q) z =
        weightedFiniteBooleanCoefficient X (integralBasisEvaluationWeight X x) j q
          (fun _ => true) := by
            rfl
    _ = finiteDeltaPullbackR X j q x := by
      rw [weightedFiniteBooleanCoefficient_evaluationWeight_allTrue]
    _ = if q = j.proj x then 1 else 0 := by
      let qx : (FiniteQuotientObject X j).obj := j.proj x
      change
        (if qx = q then 1 else 0) =
          (if q = qx then 1 else 0)
      by_cases hq : q = qx
      · rw [if_pos hq.symm, if_pos hq]
      · have hxq : qx ≠ q := by
          intro h
          exact hq h.symm
        rw [if_neg hxq, if_neg hq]
    _ =
      ((ConcreteCategory.hom
        ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion
          (X.fintypeDiagram.obj j) (j.proj x)).app
          (Opposite.op
            ((profiniteToCompHaus).obj (Profinite.of PUnit.{u + 1})))))
        (1 : LocallyConstant (Profinite.of PUnit.{u + 1}) CMDG.CondensedCM4P3G.R.{u}) q) z := by
      by_cases hq : q = j.proj x
      · rw [if_pos hq, hq]
        have hself :=
          CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion_apply_self
            (X.fintypeDiagram.obj j) (j.proj x)
            (Opposite.op
              ((profiniteToCompHaus).obj (Profinite.of PUnit.{u + 1})))
            (1 : LocallyConstant (Profinite.of PUnit.{u + 1}) CMDG.CondensedCM4P3G.R.{u}) z
        exact hself.symm
      · rw [if_neg hq]
        have hne :=
          CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion_apply_ne
            (X.fintypeDiagram.obj j) hq
            (Opposite.op
              ((profiniteToCompHaus).obj (Profinite.of PUnit.{u + 1})))
            (1 : LocallyConstant (Profinite.of PUnit.{u + 1}) CMDG.CondensedCM4P3G.R.{u}) z
        exact hne.symm

/-- At a fixed finite quotient, transporting the weighted measure section forward through the
protected finite measure/family and finite internal-dual/family isomorphisms recovers exactly its
coefficient family.  This is only a cancellation statement for already-protected isomorphisms; it
does not introduce any global measure or solidification comparison. -/
theorem weightedFiniteBooleanMeasureSection_coefficientFamily_transport
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) :
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteFamilyInternalHomIso
        (FiniteQuotientObject X j)).hom.app
        (Opposite.op ((profiniteToCompHaus).obj
          (CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X)))))
      ((ConcreteCategory.hom
        ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFamilyIso
          (FiniteQuotientObject X j)).hom.app
          (Opposite.op ((profiniteToCompHaus).obj
            (CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X)))))
        (weightedFiniteBooleanMeasureSection X a j)) =
      weightedFiniteBooleanCoefficientFamily X a j := by
  let Q := FiniteQuotientObject X j
  let S := Opposite.op ((profiniteToCompHaus).obj
    (CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X))
  let c := weightedFiniteBooleanCoefficientFamily X a j
  let iM := CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFamilyIso Q
  let iF := CMDG.CondensedCM4P2E.FiniteDualTransport.finiteFamilyInternalHomIso Q
  change
    (ConcreteCategory.hom (iF.hom.app S))
      ((ConcreteCategory.hom (iM.hom.app S))
        ((ConcreteCategory.hom (iM.inv.app S))
          ((ConcreteCategory.hom (iF.inv.app S)) c))) = c
  have hMpoint :
      (ConcreteCategory.hom (iM.hom.app S))
          ((ConcreteCategory.hom (iM.inv.app S))
            ((ConcreteCategory.hom (iF.inv.app S)) c)) =
        (ConcreteCategory.hom (iF.inv.app S)) c := by
    exact ConcreteCategory.congr_hom (iM.app S).inv_hom_id
      ((ConcreteCategory.hom (iF.inv.app S)) c)
  rw [hMpoint]
  exact ConcreteCategory.congr_hom (iF.app S).inv_hom_id c

/-- At a fixed finite quotient, the protected finite measure-to-small-free comparison sends the
weighted measure section to the canonical finite free image of its coefficient family.  This is
still purely finite-stage transport; it does not assert any global measure, Dirac, or solid-side
comparison. -/
theorem weightedFiniteBooleanMeasureSection_smallFree_transport
    (X : Profinite.{u}) (a : IntegralBasisIndex X → ℤ)
    (j : DiscreteQuotient X) :
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasureSmallFreePresheafNatIso.app
        (FiniteQuotientObject X j)).hom.app
        (Opposite.op ((profiniteToCompHaus).obj
          (CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X)))))
      (weightedFiniteBooleanMeasureSection X a j) =
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyFreeIso
        (FiniteQuotientObject X j)).hom.app
        (Opposite.op ((profiniteToCompHaus).obj
          (CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X)))))
      (weightedFiniteBooleanCoefficientFamily X a j) := by
  let Q := FiniteQuotientObject X j
  let S := Opposite.op ((profiniteToCompHaus).obj
    (CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X))
  let m := weightedFiniteBooleanMeasureSection X a j
  let c := weightedFiniteBooleanCoefficientFamily X a j
  change
    (ConcreteCategory.hom
      (((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasurePresheafFamilyIso Q).hom ≫
        (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteFamilyInternalHomIso Q).hom ≫
        (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyFreeIso Q).hom).app S)) m =
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyFreeIso Q).hom.app S)) c
  simp only [NatTrans.comp_app, ConcreteCategory.comp_apply]
  exact congrArg
    (fun t =>
      (ConcreteCategory.hom
        ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyFreeIso Q).hom.app S)) t)
    (weightedFiniteBooleanMeasureSection_coefficientFamily_transport X a j)

/-- Pull the evaluation-weight measure section to the all-true Boolean point and then apply the
protected measure-to-small-free comparison.  The result is exactly the canonical small-free delta
at the quotient point represented by `x`.  This is entirely finite-stage. -/
theorem weightedFiniteBooleanMeasureSection_smallFree_evaluationWeight_allTrue
    (X : Profinite.{u}) (x : X) (j : DiscreteQuotient X) :
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreePresheafFunctor
        (FiniteQuotientObject X j)).map
        ((profiniteToCompHaus).map
          (CMDG.CondensedCM4P3L.KernelFunctional.basisBooleanPointProbe X
            (fun _ => true))).op))
      ((ConcreteCategory.hom
        ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasureSmallFreePresheafNatIso.app
          (FiniteQuotientObject X j)).hom.app
          (Opposite.op ((profiniteToCompHaus).obj
            (CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X)))))
        (weightedFiniteBooleanMeasureSection X (integralBasisEvaluationWeight X x) j)) =
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCoordinateInclusion
        (FiniteQuotientObject X j) (j.proj x)).app
        (Opposite.op
          ((profiniteToCompHaus).obj (Profinite.of PUnit.{u + 1})))))
      (1 : LocallyConstant (Profinite.of PUnit.{u + 1}) CMDG.CondensedCM4P3G.R.{u}) := by
  let Q := FiniteQuotientObject X j
  let P := Profinite.of PUnit.{u + 1}
  let S := Opposite.op ((profiniteToCompHaus).obj
    (CMDG.CondensedCM4P3G.BooleanCube.basisBooleanCube X))
  let U := Opposite.op ((profiniteToCompHaus).obj P)
  let ftrue := ((profiniteToCompHaus).map
    (CMDG.CondensedCM4P3L.KernelFunctional.basisBooleanPointProbe X
      (fun _ => true))).op
  let c := weightedFiniteBooleanCoefficientFamily X (integralBasisEvaluationWeight X x) j
  let iF := CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyFreeIso Q
  have htransport :=
    weightedFiniteBooleanMeasureSection_smallFree_transport
      X (integralBasisEvaluationWeight X x) j
  have hnat := ConcreteCategory.congr_hom (iF.hom.naturality ftrue) c
  simp only [ConcreteCategory.comp_apply] at hnat
  have hdelta :
      (ConcreteCategory.hom
        ((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf Q).map ftrue)) c =
        (ConcreteCategory.hom
          ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion
            Q (j.proj x)).app U))
          (1 : LocallyConstant P CMDG.CondensedCM4P3G.R.{u}) := by
    simpa [Q, P, U, ftrue, c] using
      weightedFiniteBooleanCoefficientFamily_evaluationWeight_allTrue X x j
  have hdeltaFree := congrArg
    (fun t => (ConcreteCategory.hom (iF.hom.app U)) t) hdelta
  have hcoord :=
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion_freeIso
      Q (j.proj x)
  have hcoordU := congrArg (fun η => η.app U) hcoord
  simp only [NatTrans.comp_app] at hcoordU
  have hcoordPoint := ConcreteCategory.congr_hom hcoordU
    (1 : LocallyConstant P CMDG.CondensedCM4P3G.R.{u})
  simp only [ConcreteCategory.comp_apply] at hcoordPoint
  rw [htransport]
  exact hnat.symm.trans (hdeltaFree.trans hcoordPoint)

/-- The measure-side analogue of profinite solidification: lift the identity finite-free
transformation through the protected measure right-Kan extension.  This is uniquely determined by
P2-E and introduces no new comparison assumption. -/
noncomputable def measureSolidification :
    Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u} ⟶
      CMDG.CondensedCM4P2D.measureFunctor := by
  letI :
      CMDG.CondensedCM4P2D.measureFunctor.IsRightKanExtension
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom :=
    CMDG.CondensedCM4P2E.RightKanReconstruction.measureFunctorIsRightKanExtension
  exact
    CMDG.CondensedCM4P2D.measureFunctor.liftOfIsRightKanExtension
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u})
      (𝟙 (Condensed.finFree CMDG.CondensedCM4P3G.R.{u}))

/-- On each finite object, the measure-side solidification lift followed by the protected E1
finite comparison is the identity finite-free map. -/
theorem measureSolidification_fac (Q : FintypeCat.{u}) :
    measureSolidification.app (FintypeCat.toProfinite.obj Q) ≫
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom.app Q =
      𝟙 ((Condensed.finFree CMDG.CondensedCM4P3G.R.{u}).obj Q) := by
  letI :
      CMDG.CondensedCM4P2D.measureFunctor.IsRightKanExtension
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom :=
    CMDG.CondensedCM4P2E.RightKanReconstruction.measureFunctorIsRightKanExtension
  exact
    CMDG.CondensedCM4P2D.measureFunctor.liftOfIsRightKanExtension_fac_app
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom
      (Condensed.profiniteFree CMDG.CondensedCM4P3G.R.{u})
      (𝟙 (Condensed.finFree CMDG.CondensedCM4P3G.R.{u})) Q

/-- The measure-side lift is the protected profinite solidification after passage through the
P2-E canonical right-Kan uniqueness isomorphism.  This is a uniqueness statement for two lifts of
the same finite identity transformation. -/
theorem measureSolidification_comp_measureProfiniteSolidNatIso :
    measureSolidification ≫
        CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.hom =
      Condensed.profiniteSolidification CMDG.CondensedCM4P3G.R.{u} := by
  letI :
      CMDG.CondensedCM4P2D.measureFunctor.IsRightKanExtension
        CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom :=
    CMDG.CondensedCM4P2E.RightKanReconstruction.measureFunctorIsRightKanExtension
  letI :
      (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).IsRightKanExtension
        (Condensed.profiniteSolidCounit CMDG.CondensedCM4P3G.R.{u}) :=
    CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.profiniteSolidIsRightKanExtension
  apply
    (Condensed.profiniteSolid CMDG.CondensedCM4P3G.R.{u}).hom_ext_of_isRightKanExtension
      (Condensed.profiniteSolidCounit CMDG.CondensedCM4P3G.R.{u})
  simp [measureSolidification,
    CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso,
    Condensed.profiniteSolidification]

#check integralBasisEvaluationWeight
#check weightedBasisBooleanPairing_evaluationWeight_allTrue
#check basisCombination_finiteFunctionalCoefficients_apply
#check kernelProductFunctional_finiteTruncation_evaluationWeight
#check basisCombination_kernelProductFunctional_finiteCoefficients_apply
#check weightedFiniteBooleanCoefficient_evaluationWeight_allTrue
#check weightedFiniteBooleanCoefficientFamily_evaluationWeight_allTrue
#check weightedFiniteBooleanMeasureSection_coefficientFamily_transport
#check weightedFiniteBooleanMeasureSection_smallFree_transport
#check weightedFiniteBooleanMeasureSection_smallFree_evaluationWeight_allTrue
#check measureSolidification
#check measureSolidification_fac
#check measureSolidification_comp_measureProfiniteSolidNatIso
#print axioms weightedBasisBooleanPairing_evaluationWeight_allTrue
#print axioms basisCombination_finiteFunctionalCoefficients_apply
#print axioms kernelProductFunctional_finiteTruncation_evaluationWeight
#print axioms basisCombination_kernelProductFunctional_finiteCoefficients_apply
#print axioms weightedFiniteBooleanCoefficient_evaluationWeight_allTrue
#print axioms weightedFiniteBooleanCoefficientFamily_evaluationWeight_allTrue
#print axioms weightedFiniteBooleanMeasureSection_coefficientFamily_transport
#print axioms weightedFiniteBooleanMeasureSection_smallFree_transport
#print axioms weightedFiniteBooleanMeasureSection_smallFree_evaluationWeight_allTrue
#print axioms measureSolidification
#print axioms measureSolidification_fac
#print axioms measureSolidification_comp_measureProfiniteSolidNatIso

end CMDG.CondensedCM4P3M.KernelPointBridge