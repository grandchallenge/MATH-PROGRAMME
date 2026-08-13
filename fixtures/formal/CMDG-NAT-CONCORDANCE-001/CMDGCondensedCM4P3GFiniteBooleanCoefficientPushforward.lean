import CMDGCondensedCM4P3GKernelWeightedLocalConstancy
import CMDGCondensedCM4P2EFiniteDualPushforward

/-!
# CMDG CM4-P3-G finite Boolean coefficient pushforward

This fixture is the stage-22 successor to finite quotient coefficient compatibility. It proves
that the concrete Boolean coefficient family is carried along a quotient refinement by the
already-certified P2-E canonical finite coefficient-family pushforward.

The proof first exposes the pointwise fiber-sum action of the existing pushforward map, then
identifies the finite-set map with the certified quotient transition and discharges the result by
`finiteBooleanCoefficient_fiber_sum`.

No finite-measure compatibility, right-Kan cone assembly, kernel-local-constancy, injectivity,
coefficient-solidity, or broader P3 closure claim is asserted here.
-/

namespace CMDG.CondensedCM4P3G.FiniteBooleanCoefficientPushforward

universe u

open CategoryTheory Opposite
open scoped BigOperators

open CMDG.CondensedCM4P3G.BooleanCube
open CMDG.CondensedCM4P3G.FiniteBooleanMeasure
open CMDG.CondensedCM4P3G.KernelWeightedLocalConstancy

abbrev R := CMDG.CondensedCM4P3G.R.{u}

attribute [local instance] FintypeCat.fintype

/-- The finite-set map used by the profinite quotient diagram is definitionally the certified
quotient transition from stage 21. -/
theorem fintypeDiagram_map_eq_finiteQuotientTransition
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) (p : j) :
    (X.fintypeDiagram.map f) p = finiteQuotientTransition X f p := by
  rfl

/-- Pointwise action of the existing P2-E canonical coefficient-family pushforward: the target
coordinate `y` is the sum of all source coordinates in its fiber. -/
theorem finiteCoefficientFamilyPushforwardMap_apply
    {A B : FintypeCat.{u}} (g : A ⟶ B) (S : CompHaus.{u}ᵒᵖ)
    (a :
      (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf A).obj S)
    (y : B.obj) :
    ((ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap g).app S))
      a) y =
      ∑ x : A.obj, if g x = y then a x else 0 := by
  classical
  unfold CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap
  rw [NatTrans.app_sum, ModuleCat.hom_sum]
  let evalAtA :
      (↑((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf A).obj S) →ₗ[
          R.{u}]
        ↑((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf B).obj S)) →+
        ↑((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf B).obj S) :=
    { toFun := fun h => h a
      map_zero' := rfl
      map_add' := by intro h k; rfl }
  change
    (evalAtA
      (∑ x : A.obj,
        ModuleCat.Hom.hom
          (((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateProjection A x) ≫
            CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion B (g x)).app S))) y =
      ∑ x : A.obj, if g x = y then a x else 0
  rw [map_sum]
  let evalAtY :
      ↑((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf B).obj S) →+
        LocallyConstant S.unop R.{u} :=
    { toFun := fun b => b y
      map_zero' := rfl
      map_add' := by intro b c; rfl }
  change
    evalAtY
      (∑ x : A.obj,
        (ModuleCat.Hom.hom
          ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateInclusion B (g x)).app S))
          ((ModuleCat.Hom.hom
            ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateProjection A x).app S)) a)) =
      ∑ x : A.obj, if g x = y then a x else 0
  rw [map_sum]
  change (∑ x : A.obj, if y = g x then a x else 0) =
    ∑ x : A.obj, if g x = y then a x else 0
  apply Finset.sum_congr rfl
  intro x _
  by_cases hxy : g x = y
  · simp [hxy]
  · have hyx : y ≠ g x := fun h => hxy h.symm
    simp [hxy, hyx]

/-- Stage-22 terminal theorem. The Boolean coefficient family is covariantly compatible with a
refinement of finite quotients under the already-certified P2-E pushforward map. -/
theorem finiteBooleanCoefficientFamily_pushforward
    (X : Profinite.{u}) {j k : DiscreteQuotient X} (f : j ⟶ k) :
    (ConcreteCategory.hom
      ((CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyPushforwardMap
        (X.fintypeDiagram.map f)).app
        (op ((profiniteToCompHaus).obj (basisBooleanCube X)))))
      (finiteBooleanCoefficientFamily X j) =
      finiteBooleanCoefficientFamily X k := by
  funext q
  rw [finiteCoefficientFamilyPushforwardMap_apply]
  change
    (∑ p : j,
      if (X.fintypeDiagram.map f) p = q then
        finiteBooleanCoefficient X j p
      else 0) =
      finiteBooleanCoefficient X k q
  simpa only [fintypeDiagram_map_eq_finiteQuotientTransition] using
    (finiteBooleanCoefficient_fiber_sum X f q)

#check fintypeDiagram_map_eq_finiteQuotientTransition
#check finiteCoefficientFamilyPushforwardMap_apply
#check finiteBooleanCoefficientFamily_pushforward

#print axioms fintypeDiagram_map_eq_finiteQuotientTransition
#print axioms finiteCoefficientFamilyPushforwardMap_apply
#print axioms finiteBooleanCoefficientFamily_pushforward

end CMDG.CondensedCM4P3G.FiniteBooleanCoefficientPushforward
