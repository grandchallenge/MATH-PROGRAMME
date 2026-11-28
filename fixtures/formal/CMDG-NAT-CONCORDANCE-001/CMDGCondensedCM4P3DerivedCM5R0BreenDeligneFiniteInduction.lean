import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFiniteTensor

/-! All Eilenberg–Mac Lane stages inherit finite homology from
the rank-one circle base. The base is still a separate input. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory Opposite
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneReducedBasis
open CMDG.CondensedCM5R0.BreenDeligneFiniteTensor
open CMDG.CondensedCM5R0.BreenDeligneFiniteBar
namespace CMDG.CondensedCM5R0.BreenDeligneFiniteInduction

theorem reducedChainFree (A : AddCommGrpCat.{0}) (n j : ℕ) :
    Module.Free ℤ ((reducedChainsZ A n).X j) := by
  let B := ((em n).obj A).obj (op (SimplexCategory.mk j))
  exact Module.Free.of_basis (reducedBasis B)

theorem finite_succ (A : AddCommGrpCat.{0}) (n : ℕ)
    (h : ∀ j, Module.Finite ℤ ((reducedChainsZ A n).homology j)) :
    ∀ j, Module.Finite ℤ ((reducedChainsZ A (n+1)).homology j) := by
  intro j
  exact finite_next A n j (fun p q _ _ =>
    finitePowerHomology _ h (reducedChainFree A n) p q)

theorem finite_positive (A : AddCommGrpCat.{0})
    (base : ∀ j, Module.Finite ℤ ((reducedChainsZ A 1).homology j)) (n : ℕ) :
    ∀ j, Module.Finite ℤ ((reducedChainsZ A (n+1)).homology j) := by
  induction n with
  | zero => exact base
  | succ n ih => exact finite_succ A (n+1) ih

#print axioms reducedChainFree
#print axioms finite_positive
end CMDG.CondensedCM5R0.BreenDeligneFiniteInduction
