import Mathlib.Data.Finset.Sum
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Set.Finite.Basic
import Lean.Elab.Tactic.Omega

/-!
Independent Lean verification of the nontrivial E3-to-E2 step.
All statements concern infinite sets of natural numbers.
-/
namespace GCLErdos41.DensityTransfer

def E3 (A : Set ℕ) : Prop :=
  ∀ I J : Finset ℕ, (∀ a ∈ I, a ∈ A) → (∀ a ∈ J, a ∈ A) →
    I.card = 3 → J.card = 3 → I.sum id = J.sum id → I = J

def FixedTwo (A : Set ℕ) : Prop :=
  ∀ I J : Finset ℕ, (∀ a ∈ I, a ∈ A) → (∀ a ∈ J, a ∈ A) →
    I.card = 2 → J.card = 2 → I.sum id = J.sum id → I = J

theorem e3_implies_fixed_two {A : Set ℕ} (hA : A.Infinite)
    (h3 : E3 A) : FixedTwo A := by
  intro I J hI hJ hcI hcJ hsum
  obtain ⟨x, hx, hxn⟩ := hA.exists_notMem_finset (I ∪ J)
  have hxnI : x ∉ I := by
    intro hi
    exact hxn (Finset.mem_union.mpr (Or.inl hi))
  have hxnJ : x ∉ J := by
    intro hj
    exact hxn (Finset.mem_union.mpr (Or.inr hj))
  have hi3 : (insert x I).card = 3 := by
    simp [hxnI, hcI]
  have hj3 : (insert x J).card = 3 := by
    simp [hxnJ, hcJ]
  have hiA : ∀ a ∈ insert x I, a ∈ A := by
    intro a ha
    rcases Finset.mem_insert.mp ha with rfl | ha
    · exact hx
    · exact hI a ha
  have hjA : ∀ a ∈ insert x J, a ∈ A := by
    intro a ha
    rcases Finset.mem_insert.mp ha with rfl | ha
    · exact hx
    · exact hJ a ha
  have heqsum : (insert x I).sum id = (insert x J).sum id := by
    simpa [Finset.sum_insert, hxnI, hxnJ] using congrArg (fun n : ℕ => x + n) hsum
  have heq := h3 (insert x I) (insert x J) hiA hjA hi3 hj3 heqsum
  have heqerase := congrArg (fun s : Finset ℕ => s.erase x) heq
  simpa [Finset.erase_insert, hxnI, hxnJ] using heqerase

/-- The encoded sum has the card as the residue modulo four. -/
theorem code_sum (I : Finset ℕ) :
    I.sum (fun x => 4*x+1) = 4*(I.sum id)+I.card := by
  classical
  induction I using Finset.induction_on with
  | empty => simp
  | @insert a s has ih =>
    simp [Finset.sum_insert, has, ih, Nat.mul_add]
    omega

/-- Source-index formulation of the affine H3 property. No need for a
    choice of inverse representation for the coded image. -/
def CodedH3 (A : Set ℕ) : Prop :=
  ∀ I J : Finset ℕ, (∀ a ∈ I, a ∈ A) → (∀ a ∈ J, a ∈ A) →
    I.card ≤ 3 → J.card ≤ 3 →
    I.sum (fun x => 4*x+1) = J.sum (fun x => 4*x+1) → I = J

theorem e3_implies_coded_h3 {A : Set ℕ}
    (hA : A.Infinite) (h3 : E3 A) : CodedH3 A := by
  intro I J hI hJ hcI hcJ hcode
  rw [code_sum I, code_sum J] at hcode
  have hc : I.card = J.card := by omega
  have hs : I.sum id = J.sum id := by omega
  have h2 := e3_implies_fixed_two hA h3
  have hcases : I.card = 0 ∨ I.card = 1 ∨ I.card = 2 ∨ I.card = 3 := by omega
  rcases hcases with h0 | h1 | h2c | h3c
  · have hI0 : I = ∅ := Finset.card_eq_zero.mp h0
    have hJ0 : J = ∅ := Finset.card_eq_zero.mp (hc.symm.trans h0)
    exact hI0.trans hJ0.symm
  · obtain ⟨a, ha⟩ := Finset.card_eq_one.mp h1
    obtain ⟨b, hb⟩ := Finset.card_eq_one.mp (hc.symm.trans h1)
    subst I
    subst J
    simp only [Finset.sum_singleton] at hs
    change a = b at hs
    simpa [hs]
  · exact h2 I J hI hJ h2c (hc.symm.trans h2c) hs
  · exact h3 I J hI hJ h3c (hc.symm.trans h3c) hs


end GCLErdos41.DensityTransfer
