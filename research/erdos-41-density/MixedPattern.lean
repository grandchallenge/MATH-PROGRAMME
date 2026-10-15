import Mathlib.Tactic.Ring
import Lean.Elab.Tactic.Omega

/-! Elementary polynomial and interval arithmetic for two adjacent M3 shells.
The universal shell-pattern injection is established in CROSS_PATTERN_HALL.md
and is not asserted to be fully kernel-formalized in this file. -/
namespace GCLErdos41.CrossPattern

theorem mixed_pattern_double_count (x y : Nat) :
    x*(x+1)*y + x*y*(y+1) = x*y*(x+y+2) := by ring

theorem union_interval_cardinality (L : Nat) (hL : 1 ≤ L) :
    (10*L-3)-(4*L)+1 = 6*L-2 := by omega

theorem isolated_xxy_range_cardinality (L : Nat) (hL : 1 ≤ L) :
    (8*L-3)-(4*L)+1 = 4*L-2 := by omega

theorem isolated_xyy_range_cardinality (L : Nat) (hL : 1 ≤ L) :
    (10*L-3)-(5*L)+1 = 5*L-2 := by omega

end GCLErdos41.CrossPattern
