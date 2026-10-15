import Init

namespace Erdos41HistoricalSource

def historicalB3 (A : Nat → Prop) : Prop :=
  ∀ xs ys : List Nat,
    xs.length ≤ 3 → ys.length ≤ 3 →
    xs.Nodup → ys.Nodup →
    (∀ x ∈ xs, A x) → (∀ y ∈ ys, A y) →
    xs ≠ [] → ys ≠ [] →
    xs.sum = ys.sum → xs.Perm ys

def modernMultisetB3 (A : Nat → Prop) : Prop :=
  ∀ xs ys : List Nat,
    xs.length = 3 → ys.length = 3 →
    (∀ x ∈ xs, A x) → (∀ y ∈ ys, A y) →
    xs.sum = ys.sum → xs.Perm ys

def fixedDistinctTripleB3 (A : Nat → Prop) : Prop :=
  ∀ xs ys : List Nat,
    xs.length = 3 → ys.length = 3 →
    xs.Nodup → ys.Nodup →
    (∀ x ∈ xs, A x) → (∀ y ∈ ys, A y) →
    xs.sum = ys.sum → xs.Perm ys

theorem historical_implies_fixed (A : Nat → Prop)
    (h : historicalB3 A) : fixedDistinctTripleB3 A := by
  intro xs ys hxs hys ndxs ndys memxs memys hsum
  exact h xs ys (by simp [hxs]) (by simp [hys]) ndxs ndys memxs memys
    (by intro hn; simp [hn] at hxs) (by intro hn; simp [hn] at hys) hsum

theorem modern_implies_fixed (A : Nat → Prop)
    (h : modernMultisetB3 A) : fixedDistinctTripleB3 A := by
  intro xs ys hxs hys _ _ memxs memys hsum
  exact h xs ys hxs hys memxs memys hsum

#print axioms historical_implies_fixed
#print axioms modern_implies_fixed
end Erdos41HistoricalSource
