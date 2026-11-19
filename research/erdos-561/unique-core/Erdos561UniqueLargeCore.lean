import Lean.Elab.Tactic.Omega

/-!
Erdos #561: general Nat consequences of the one-large-tight-component
ordinary Lovasz factor obstruction, including slack threshold.
The Lovasz factor theorem itself and its graph component semantics are
external paper-level inputs, not formalized by this source.
No user axioms, sorry, admit, or native_decide.
-/
namespace Erdos561UniqueLargeCore

/-- With fewer than two groups of D+1 saturated vertices, there can
be at most one component of that minimum size. -/
theorem at_most_one_large (D k h : Nat)
    (hk : k ≤ 2 * D + 1)
    (hcover : h * (D + 1) ≤ k) : h ≤ 1 := by
  apply Classical.byContradiction
  intro hnot
  have htwo : 2 ≤ h := by omega
  have hmul : 2 * (D + 1) ≤ h * (D + 1) :=
    Nat.mul_le_mul_right (D + 1) htwo
  omega

/-- If every small counted component contributes at least D and the
ordinary factor cut has defect A<q, the unique large component must
have zero weighted boundary. -/
theorem isolated_large_weighted_boundary (D q A b : Nat)
    (hq : 1 ≤ q)
    (hbad : A < q)
    (hbound : D * (q - 1) + b ≤ D * A) : b = 0 := by
  have hle : A ≤ q - 1 := by omega
  have hmul : D * A ≤ D * (q - 1) := Nat.mul_le_mul_left D hle
  omega

/-- Numerical small-slack condition ensuring at most 2D+1
maximum-degree vertices, when (D-1)k is bounded by the degree-excess
budget. -/
theorem low_slack_caps_saturated_count (D k s : Nat)
    (_hD : 2 ≤ D)
    (hbudget : (D - 1) * k ≤ (D - 1) * (D + 1) + s)
    (hsmall : s < (D - 1) * (D + 1)) : k ≤ 2 * D + 1 := by
  apply Classical.byContradiction
  intro hnot
  have hk : 2 * D + 2 ≤ k := by omega
  have hmul : (D - 1) * (2 * D + 2) ≤ (D - 1) * k :=
    Nat.mul_le_mul_left (D - 1) hk
  have htwice : (D - 1) * (2 * D + 2) =
      (D - 1) * (D + 1) + (D - 1) * (D + 1) := by
    have hsum : 2 * D + 2 = (D + 1) + (D + 1) := by omega
    rw [hsum, Nat.mul_add]
  omega

private theorem plus_square (m : Nat) :
    m * (m + 2) + 1 = (m + 1) * (m + 1) := by
  simp only [Nat.mul_add, Nat.add_mul]
  omega

/-- Exact identity converting our degree-excess threshold to D²-1. -/
theorem slack_product_square (D : Nat) (hD : 1 ≤ D) :
    (D - 1) * (D + 1) + 1 = D * D := by
  have hplus : (D - 1) + 1 = D := Nat.sub_add_cancel hD
  have htwo : (D - 1) + 2 = D + 1 := by omega
  calc
    (D - 1) * (D + 1) + 1 = (D - 1) * ((D - 1) + 2) + 1 := by rw [htwo]
    _ = ((D - 1) + 1) * ((D - 1) + 1) := plus_square (D - 1)
    _ = D * D := by rw [hplus]

#print axioms Erdos561UniqueLargeCore.at_most_one_large
#print axioms Erdos561UniqueLargeCore.slack_product_square
#print axioms Erdos561UniqueLargeCore.isolated_large_weighted_boundary
#print axioms Erdos561UniqueLargeCore.low_slack_caps_saturated_count
end Erdos561UniqueLargeCore
