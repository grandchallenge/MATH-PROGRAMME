import Init

/-!
Independently kernel-checked arithmetic tables for the small seeds used
in the explicit infinite-set lifting theorem in INFINITE_FIDELITY.md.
The positional-expansion lift is separately proved in that manuscript.
-/
namespace GCLErdos41.InfiniteSeeds

/-- Index 0..7 enumerates all subsets of {1,2,3}, by size. -/
def exactCard (i : Fin 8) : Nat :=
  match i.val with
  | 0 => 0 | 1 => 1 | 2 => 1 | 3 => 1
  | 4 => 2 | 5 => 2 | 6 => 2 | _ => 3

def exactSum (i : Fin 8) : Nat :=
  match i.val with
  | 0 => 0 | 1 => 1 | 2 => 2 | 3 => 3
  | 4 => 3 | 5 => 4 | 6 => 5 | _ => 6

theorem exact_same_card_table :
    ∀ i j : Fin 8, exactCard i = exactCard j →
      exactSum i = exactSum j → i = j := by decide

/-- All eight subset sums of {1,3,5} are distinct. -/
def historicalSubsetSum (i : Fin 8) : Nat :=
  match i.val with
  | 0 => 0 | 1 => 1 | 2 => 3 | 3 => 5
  | 4 => 4 | 5 => 6 | 6 => 8 | _ => 9

theorem historical_seed_injective :
    ∀ i j : Fin 8, historicalSubsetSum i = historicalSubsetSum j →
      i = j := by decide

/-- All size-two multiset sums of {1,4,5} are distinct. -/
def multisetSumTwo (i : Fin 6) : Nat :=
  match i.val with
  | 0 => 2 | 1 => 5 | 2 => 6 | 3 => 8 | 4 => 9 | _ => 10

theorem multiset_two_injective :
    ∀ i j : Fin 6, multisetSumTwo i = multisetSumTwo j →
      i = j := by decide

/-- All size-three multiset sums of {1,4,5} are distinct. -/
def multisetSumThree (i : Fin 10) : Nat :=
  match i.val with
  | 0 => 3 | 1 => 6 | 2 => 7 | 3 => 9 | 4 => 10
  | 5 => 11 | 6 => 12 | 7 => 13 | 8 => 14 | _ => 15

theorem multiset_three_injective :
    ∀ i j : Fin 10, multisetSumThree i = multisetSumThree j →
      i = j := by decide

/-- Distinct source semantics exhibit explicit small collisions. -/
theorem original_cross_card_collision : 1 + 2 = 3 := by decide
theorem original_repetition_collision : 1 + 1 + 3 = 1 + 2 + 2 := by decide
theorem historical_repetition_collision : 1 + 1 + 5 = 1 + 3 + 3 := by decide
theorem multiset_cross_card_collision : 1 + 4 = 5 := by decide

end GCLErdos41.InfiniteSeeds
