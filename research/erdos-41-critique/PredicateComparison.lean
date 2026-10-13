import Mathlib.Data.Finset.Basic
import Mathlib.Data.Multiset.Sum
import Mathlib.Data.Finset.Sum
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.BigOperators.Group.Multiset.Basic
import Lean.Elab.Tactic.Omega

/-!
Finite semantic comparison for Erdős #41, zero sorry or additional axioms.
The original problem remains open. This file does not address an infinite density limit.
-/
namespace GCLErdos41

def B : Finset ℕ := {1, 2, 3}

/-- Literal finite restriction of the pinned provider's NtupleCondition (n = 3).
    Distinct elements, exactly three, no comparison across cardinalities. -/
def FrozenExactThree (A : Finset ℕ) : Prop :=
  ∀ I J : Finset ℕ,
    I ⊆ A → J ⊆ A → I.card = 3 → J.card = 3 →
    I.sum id = J.sum id → I = J

/-- Erdős 1980, p.98: sums with εᵢ ∈ {0,1}, with at most three selected
    entries, are unique. The empty selection is included. -/
def OriginalAtMostThree (A : Finset ℕ) : Prop :=
  ∀ I J : Finset ℕ,
    I ⊆ A → J ⊆ A → I.card ≤ 3 → J.card ≤ 3 →
    I.sum id = J.sum id → I = J

/-- Distinct triple multisets, repetition of summands permitted. -/
def RepetitionThree (A : Finset ℕ) : Prop :=
  ∀ U V : Multiset ℕ,
    U.card = 3 → V.card = 3 →
    (∀ x ∈ U, x ∈ A) → (∀ x ∈ V, x ∈ A) →
    U.sum = V.sum → U = V

/-- Frozen provider quantifier form, preserving its conjunction and Set carrier. -/
def ProviderNtupleCondition (A : Set ℕ) (n : ℕ) : Prop :=
  ∀ I J : Finset ℕ,
    (↑I : Set ℕ) ⊆ A ∧ (↑J : Set ℕ) ⊆ A ∧
    I.card = n ∧ J.card = n ∧ I.sum id = J.sum id → I = J

/-- The finite predicate is precisely the n=3 provider predicate on the carrier. -/
theorem finite_provider_equivalence (A : Finset ℕ) :
    ProviderNtupleCondition (↑A : Set ℕ) 3 ↔ FrozenExactThree A := by
  constructor
  · intro h I J hI hJ hcI hcJ hs
    apply h I J
    exact ⟨by simpa using hI, by simpa using hJ, hcI, hcJ, hs⟩
  · intro h I J hconds
    rcases hconds with ⟨hI, hJ, hcI, hcJ, hs⟩
    exact h I J (by simpa using hI) (by simpa using hJ) hcI hcJ hs

theorem historical_implies_frozen (A : Finset ℕ)
    (h : OriginalAtMostThree A) : FrozenExactThree A := by
  intro I J hI hJ hIc hJc hs
  exact h I J hI hJ (by omega) (by omega) hs

theorem repeated_implies_frozen (A : Finset ℕ)
    (h : RepetitionThree A) : FrozenExactThree A := by
  intro I J hI hJ hIc hJc hs
  have hh : (I.val : Multiset ℕ) = (J.val : Multiset ℕ) := by
    apply h I.val J.val
    · simpa using hIc
    · simpa using hJc
    · intro x hx; exact hI (by simpa using hx)
    · intro x hx; exact hJ (by simpa using hx)
    · simpa using hs
  exact Finset.val_inj.mp hh

theorem b_frozen : FrozenExactThree B := by
  intro I J hI hJ hIc hJc hs
  have hB : B.card = 3 := by decide
  have eqI : I = B := Finset.eq_of_subset_of_card_le hI (by omega)
  have eqJ : J = B := Finset.eq_of_subset_of_card_le hJ (by omega)
  exact eqI.trans eqJ.symm

theorem b_not_historical : ¬ OriginalAtMostThree B := by
  intro h
  have q : ({1, 2} : Finset ℕ) = ({3} : Finset ℕ) := by
    apply h
    all_goals decide
  have ne : ({1, 2} : Finset ℕ) ≠ ({3} : Finset ℕ) := by decide
  exact ne q

theorem b_not_repetition : ¬ RepetitionThree B := by
  intro h
  let U : Multiset ℕ := ([(1 : ℕ),1,3] : List ℕ)
  let V : Multiset ℕ := ([(1 : ℕ),2,2] : List ℕ)
  have hh : U = V := by
    apply h U V
    all_goals decide
  have ne : U ≠ V := by decide
  exact ne hh

theorem b_separates_exact_historical :
    FrozenExactThree B ∧ ¬ OriginalAtMostThree B :=
  ⟨b_frozen, b_not_historical⟩

theorem b_separates_exact_repetition :
    FrozenExactThree B ∧ ¬ RepetitionThree B :=
  ⟨b_frozen, b_not_repetition⟩

end GCLErdos41
