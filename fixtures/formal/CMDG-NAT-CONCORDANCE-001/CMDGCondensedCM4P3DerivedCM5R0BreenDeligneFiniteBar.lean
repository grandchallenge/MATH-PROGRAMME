import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFiniteTotal
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneReducedNext

/-! Finite generation transfer from actual tensor-power homology
to the next Eilenberg–MacLane model. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.BreenDeligneColumnPower
open CMDG.CondensedCM5R0.BreenDeligneBarDiagonalComparison
open CMDG.CondensedCM5R0.BreenDeligneReducedNext
open CMDG.CondensedCM5R0.BreenDeligneFiniteTotal
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneFiniteBar

theorem finiteOfIso {M N : ZMod} (e : M ≅ N) [Module.Finite ℤ N] :
    Module.Finite ℤ M :=
  Module.Finite.of_surjective e.inv.hom (by
    intro x
    exact ⟨e.hom x, CategoryTheory.congr_fun e.hom_inv_id x⟩)

theorem finiteOfZero (M : ZMod) (h : IsZero M) : Module.Finite ℤ M := by
  have he : 𝟙 M = 0 := h.eq_of_src _ _
  haveI : Subsingleton M := ⟨fun x y => by
    have hx := CategoryTheory.congr_fun he x
    have hy := CategoryTheory.congr_fun he y
    change x=0 at hx
    change y=0 at hy
    exact hx.trans hy.symm⟩
  infer_instance

theorem finite_bar_total (A : AGrp) (n j : ℕ)
    (h : ∀ p q, 1 ≤ p → p+q=j →
      Module.Finite ℤ ((tensorPower (reducedChainsZ A n) p).homology q)) :
    Module.Finite ℤ ((barTotal ((em n).obj A)).homology j) := by
  apply total_finite
  intro p q hpq
  cases p with
  | zero =>
    exact finiteOfZero _ (ShortComplex.isZero_homology_of_isZero_X₂ _
      (zeroColumn ((em n).obj A) q))
  | succ p =>
    letI := h (p+1) q (by omega) hpq
    exact finiteOfIso ((columnPowerEquiv A n p).toHomologyIso q)

theorem finite_next (A : AGrp) (n j : ℕ)
    (h : ∀ p q, 1 ≤ p → p+q=j →
      Module.Finite ℤ ((tensorPower (reducedChainsZ A n) p).homology q)) :
    Module.Finite ℤ ((reducedChainsZ A (n+1)).homology j) := by
  letI := finite_bar_total A n j h
  let e := (diagonalComparison ((em n).obj A)).trans (HomotopyEquiv.refl _)
  let e' := ((reducedNextEquiv A n).trans (HomotopyEquiv.ofIso (reducedEMChainIso A (n+1))))
  exact finiteOfIso ((e'.symm.trans e).toHomologyIso j)

#print axioms finite_bar_total
#print axioms finite_next
end CMDG.CondensedCM5R0.BreenDeligneFiniteBar
