-- Finite semantic witness only; not a proof or refutation of Erdős #41.
-- Uses only Lean core, no mathlib or axioms.
import Init

namespace GCL.Erdos41

def distinctTriple : Nat × Nat × Nat := (1, 2, 3)
def repeatedTripleA : Nat × Nat × Nat := (1, 1, 3)
def repeatedTripleB : Nat × Nat × Nat := (1, 2, 2)

theorem distinct_sum : 1 + 2 + 3 = 6 := by decide
theorem collision_left : 1 + 1 + 3 = 5 := by decide
theorem collision_right : 1 + 2 + 2 = 5 := by decide
theorem collision_distinct : repeatedTripleA ≠ repeatedTripleB := by decide
theorem finite_collision :
    (1 + 1 + 3 = 1 + 2 + 2) ∧ repeatedTripleA ≠ repeatedTripleB := by
  constructor <;> decide

end GCL.Erdos41
