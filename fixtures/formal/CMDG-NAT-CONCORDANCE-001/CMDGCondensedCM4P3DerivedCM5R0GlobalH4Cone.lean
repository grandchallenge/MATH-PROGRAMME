import CMDGCondensedCM4P3DerivedCM5R0FiniteClosedCoverH3CocycleInduction

/-!
# CMDG CM5 Ext⁴: exact global integer Čech degree-four cone contraction

Given a nonempty (not necessarily finite) index type I, a locally
constant global 4-cochain c : I^5 -> LC(X,Z) satisfying the 6-face
five-cocycle equation has a *global* continuous 3-cochain primitive.
The primitive is c(a,-,-,-,-) for any fixed a : I, not an approximation.

This is the honest base case for a forthcoming finite closed-family
H⁴ induction. It does NOT imply acyclicity for arbitrary finite closed
families, closed fivefold fibres, or Ext⁴.
-/

noncomputable section
universe u v
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem integerGlobalFourCocycle_cone_potential
    (X : Profinite.{u}) {I : Type v} [Nonempty I]
    (c : I → I → I → I → I → LocallyConstant X ℤ)
    (hc : ∀ (i j k l m n : I) (x : X),
      c j k l m n x - c i k l m n x + c i j l m n x -
        c i j k m n x + c i j k l n x -
          c i j k l m x = 0) :
    ∃ b : I → I → I → I → LocallyConstant X ℤ,
      ∀ (i j k l m : I) (x : X),
        c i j k l m x =
          b j k l m x - b i k l m x + b i j l m x -
            b i j k m x + b i j k l x := by
  classical
  let a : I := Classical.choice inferInstance
  refine ⟨fun i j k l => c a i j k l, ?_⟩
  intro i j k l m x
  have h := hc a i j k l m x
  dsimp
  omega

#print axioms integerGlobalFourCocycle_cone_potential
end CMDG.CondensedCM5R0
