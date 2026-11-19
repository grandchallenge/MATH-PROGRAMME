import Lean.Elab.Tactic.Omega

/-!
  GCL Erdős #561 — checked NATURAL-NUMBER degree-core arithmetic.
  Preconditions are explicitly numerical; the graph handshake lemma and
  the Lovász-factor obstruction remain external proof obligations.
  No sorry, axiom, admit or native_decide.
-/
namespace Erdos561

/-- A degree-sum budget with k vertices of degree D gives the
    familiar D(D+1) lower bound if k≥D+1. -/
theorem saturated_edge_budget
    (D k E : Nat) (hk : D + 1 ≤ k)
    (h_sum : D * k ≤ 2 * E) :
    D * (D + 1) ≤ 2 * E := by
  calc
    D * (D + 1) ≤ D * k := Nat.mul_le_mul_left D hk
    _ ≤ 2 * E := h_sum

/-- The vertex budget from k saturated vertices, expressed in terms
    of the positive-degree vertex count v. -/
theorem saturated_vertex_budget
    (D k v E : Nat) (hk : D + 1 ≤ k)
    (h_sum : (D - 1) * k + v ≤ 2 * E) :
    (D - 1) * (D + 1) + v ≤ 2 * E := by
  calc
    (D - 1) * (D + 1) + v ≤ (D - 1) * k + v :=
      Nat.add_le_add_right (Nat.mul_le_mul_left (D - 1) hk) v
    _ ≤ 2 * E := h_sum

/-- If the allowed excess above the D+1 saturated core is less
    than D-1, there CANNOT be D+2 saturated vertices. -/
theorem saturation_low_slack
    (D k slack : Nat) ( _hD : 2 ≤ D) (hk : D + 1 ≤ k)
    (h_sum : (D - 1) * k ≤ (D - 1) * (D + 1) + slack)
    (hsmall : slack < D - 1) : k = D + 1 := by
  apply Classical.byContradiction
  intro hne
  have hk2 : D + 2 ≤ k := by omega
  have hmul : (D - 1) * (D + 2) ≤ (D - 1) * k :=
    Nat.mul_le_mul_left (D - 1) hk2
  have hstep : (D - 1) * (D + 2) = (D - 1) * (D + 1) + (D - 1) := by
    have ha : D + 2 = D + 1 + 1 := by omega
    rw [ha, Nat.mul_add]
    simp
  omega

/-- Degree-excess alone proves the same stability conclusion after
    transferring a valid graph degree-sum estimate. -/
theorem saturation_low_slack_from_sum
    (D k v E slack : Nat) (hD : 2 ≤ D) (hk : D + 1 ≤ k)
    (h_sum : (D - 1) * k + v ≤ 2 * E)
    (h_budget : 2 * E ≤ (D - 1) * (D + 1) + v + slack)
    (hsmall : slack < D - 1) : k = D + 1 := by
  have hcore : (D - 1) * k ≤ (D - 1) * (D + 1) + slack := by omega
  exact saturation_low_slack D k slack hD hk hcore hsmall

end Erdos561

#print axioms Erdos561.saturated_edge_budget
#print axioms Erdos561.saturated_vertex_budget
#print axioms Erdos561.saturation_low_slack
#print axioms Erdos561.saturation_low_slack_from_sum
