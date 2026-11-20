import Mathlib.Data.Fin.Tuple.Basic
import Mathlib.AlgebraicTopology.ExtraDegeneracy
import Mathlib.Condensed.Module

noncomputable section
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

universe u v
def splitCechTuple (A : Type u) (B : Type v) (p : A → B)
    (n : ℕ) : Type u :=
  {xs : Fin (n + 1) → A // ∀ i : Fin (n + 1), p (xs i) = p (xs 0)}

def splitCechFace (A : Type u) (B : Type v) (p : A → B)
    (n : ℕ) (k : Fin (n + 2)) :
    splitCechTuple A B p (n + 1) → splitCechTuple A B p n :=
  fun xs => ⟨k.removeNth xs.val, by
    intro i
    exact (xs.property (k.succAbove i)).trans
      (xs.property (k.succAbove 0)).symm⟩

def splitCechExtra (A : Type u) (B : Type v) (p : A → B)
    (s : B → A) (hs : ∀ b, p (s b) = b) (n : ℕ) :
    splitCechTuple A B p n → splitCechTuple A B p (n + 1) :=
  fun xs => ⟨Fin.cons (s (p (xs.val 0))) xs.val, by
    intro i
    refine Fin.cases ?_ ?_ i
    · rfl
    · intro j
      change p (xs.val j) = p (s (p (xs.val 0)))
      exact (xs.property j).trans (hs _).symm⟩

theorem splitCechFace_zero_extra (A : Type u) (B : Type v)
    (p : A → B) (s : B → A) (hs : ∀ b, p (s b) = b)
    (n : ℕ) (xs : splitCechTuple A B p n) :
    splitCechFace A B p n 0
      (splitCechExtra A B p s hs n xs) = xs := by
  apply Subtype.ext
  funext i
  rfl

theorem splitCechFace_succ_extra (A : Type u) (B : Type v)
    (p : A → B) (s : B → A) (hs : ∀ b, p (s b) = b)
    (n : ℕ) (k : Fin (n + 2))
    (xs : splitCechTuple A B p (n + 1)) :
    splitCechFace A B p (n + 1) k.succ
      (splitCechExtra A B p s hs (n + 1) xs) =
    splitCechExtra A B p s hs n
      (splitCechFace A B p n k xs) := by
  apply Subtype.ext
  funext i
  refine Fin.cases ?_ ?_ i
  · change s (p (xs.val 0)) =
      s (p (xs.val (k.succAbove 0)))
    rw [xs.property (k.succAbove 0)]
  · intro j
    change (Fin.cons (s (p (xs.val 0))) xs.val : Fin (n + 3) → A)
      ((k.succ).succAbove j.succ) = xs.val (k.succAbove j)
    rw [Fin.succ_succAbove_succ]
    rfl

#print axioms splitCechFace_succ_extra

end CMDG.CondensedCM5R0
