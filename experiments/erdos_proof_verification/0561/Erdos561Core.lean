import Init

/-!
Erdős #561 Phase C, Lean 4.33.0 source-typed *arithmetic* bridge.
No Mathlib and no imported Lovász graph-factor theorem.
These are auxiliary conditions from Chunlin You, arXiv:2610.25958v1,
Corollary 2.6 and Claims 3.9–3.10, NOT the whole graph proof.
-/

namespace ErdosPV0561

/-- Lovász's g(v) specializes to the truncated natural subtraction. -/
def factorLower (d beta : Nat) : Nat := d - beta

/-- The exact d-g = min(d,beta) identity in the cut criterion. -/
theorem degree_minus_lower_eq_min (d beta : Nat) :
    d - factorLower d beta = min d beta := by
  unfold factorLower
  omega

/-- If d<=D=alpha+beta and alpha>0, g=f iff ambient degree reaches D. -/
theorem tight_degree_iff (d alpha beta : Nat)
    (ha : 0 < alpha) (_hd : d ≤ alpha + beta) :
    factorLower d beta = alpha ↔ d = alpha + beta := by
  unfold factorLower
  omega

/-- The (g,f) bounds exactly constrain each vertex's blue complement. -/
theorem split_budget_iff (d j alpha beta : Nat) (hjd : j ≤ d) :
    (factorLower d beta ≤ j ∧ j ≤ alpha) ↔
      (j ≤ alpha ∧ d - j ≤ beta) := by
  unfold factorLower
  omega

/-- The nonnegative parameter condition ensures g<=f. -/
theorem factor_bounds (d alpha beta : Nat) (h : d ≤ alpha + beta) :
    factorLower d beta ≤ alpha := by
  unfold factorLower
  omega

/-- Clear the source's beta/D degree-ratio term by integer multiplication. -/
theorem min_degree_ratio (d D beta : Nat)
    (hd : d ≤ D) (hb : beta ≤ D) :
    beta * d ≤ D * min d beta := by
  rcases Nat.le_total d beta with h | h
  · rw [Nat.min_eq_left h]
    exact Nat.mul_le_mul_right d hb
  · rw [Nat.min_eq_right h]
    simpa [Nat.mul_comm] using Nat.mul_le_mul_right beta hd

/-- The weighted Claim 3.9 boundary estimate implies the unweighted one. -/
theorem weighted_to_unweighted (alpha beta D A eSY eTY : Nat)
    (hbeta : alpha ≤ beta)
    (hw : alpha * eSY + beta * eTY ≤ D * A) :
    alpha * (eSY + eTY) ≤ D * A := by
  calc
    alpha * (eSY + eTY) = alpha * eSY + alpha * eTY := by
      simp [Nat.mul_add]
    _ ≤ alpha * eSY + beta * eTY :=
      Nat.add_le_add_left (Nat.mul_le_mul_right eTY hbeta) _
    _ ≤ D * A := hw

/-- With r counted components each sending >=D edges, an obstructing
    cut with A<r contradicts the weighted upper-bound. -/
theorem all_small_components_impossible (alpha D A B r : Nat)
    (ha : 1 ≤ alpha) (hD : 0 < D) (hA : A < r)
    (hupper : alpha * B ≤ D * A)
    (hsmall : r * D ≤ B) : False := by
  have hBlow : B ≤ alpha * B := Nat.le_mul_of_pos_left B (by omega)
  have hstrict : D * A < D * r := Nat.mul_lt_mul_of_pos_left hA hD
  have hsmallcomm : D * r ≤ B := by simpa [Nat.mul_comm] using hsmall
  omega

/-- The reduced counterexample parameters satisfy the strict slope gap. -/
theorem strict_factor_slope (alpha beta D : Nat)
    (ha : 2 ≤ alpha) (hb : 2 * (alpha + 1) ≤ beta)
    (hD : D = alpha + beta) : D < alpha * beta := by
  have hmult : 2 * beta ≤ alpha * beta := Nat.mul_le_mul_right beta ha
  omega

/-- The opposite (large-component) boundary inequalities are incompatible.
    This is the *numeric* final Claim 3.10 contradiction; the structural
    existence and counting of large star-centers remain unformalized. -/
theorem large_component_impossible
    (alpha beta D A B r : Nat)
    (ha : 2 ≤ alpha) (hb : 2 * (alpha + 1) ≤ beta)
    (hD : D = alpha + beta) (hr : 1 ≤ r)
    (hA : A < r) (hupper : alpha * B ≤ D * A)
    (hlarge : beta * (D + r - 2) + 2 ≤ B) : False := by
  have hDpos : 1 ≤ D := by omega
  have hDelta : r - 1 ≤ D + r - 2 := by omega
  have hbmult : beta * (r - 1) ≤ beta * (D + r - 2) :=
    Nat.mul_le_mul_left beta hDelta
  have hBlt : beta * (r - 1) < B := by omega
  have hAstr : A ≤ r - 1 := by omega
  have hleft : D * A ≤ D * (r - 1) :=
    Nat.mul_le_mul_left D hAstr
  have hDlt : D ≤ alpha * beta :=
    Nat.le_of_lt (strict_factor_slope alpha beta D ha hb hD)
  have hright : D * (r - 1) ≤ (alpha * beta) * (r - 1) :=
    Nat.mul_le_mul_right (r - 1) hDlt
  have hbottom : alpha * (beta * (r - 1)) < alpha * B :=
    Nat.mul_lt_mul_of_pos_left hBlt (by omega)
  have hassoc : (alpha * beta) * (r - 1) =
      alpha * (beta * (r - 1)) := by simp [Nat.mul_assoc]
  omega

/-- An odd number of vertices cannot support a spanning odd-regular
    graph, by the handshaking parity condition. Numeric obstruction only. -/
theorem odd_odd_product_odd (a b : Nat)
    (ha : a % 2 = 1) (hb : b % 2 = 1) :
    (a * b) % 2 = 1 := by
  simp [Nat.mul_mod, ha, hb]

/-- A unit of edge-to-T parity changes an odd obstruction into even. -/
theorem component_parity_flips (m alpha e : Nat)
    (hodd : (alpha * m + e) % 2 = 1) :
    (alpha * m + (e + 1)) % 2 = 0 := by
  omega

#check ErdosPV0561.degree_minus_lower_eq_min
#check ErdosPV0561.tight_degree_iff
#check ErdosPV0561.split_budget_iff
#check ErdosPV0561.factor_bounds
#check ErdosPV0561.min_degree_ratio
#check ErdosPV0561.weighted_to_unweighted
#check ErdosPV0561.all_small_components_impossible
#check ErdosPV0561.strict_factor_slope
#check ErdosPV0561.large_component_impossible
#check ErdosPV0561.odd_odd_product_odd
#check ErdosPV0561.component_parity_flips

#print axioms degree_minus_lower_eq_min
#print axioms tight_degree_iff
#print axioms split_budget_iff
#print axioms factor_bounds
#print axioms min_degree_ratio
#print axioms weighted_to_unweighted
#print axioms all_small_components_impossible
#print axioms strict_factor_slope
#print axioms large_component_impossible
#print axioms odd_odd_product_odd
#print axioms component_parity_flips

end ErdosPV0561
