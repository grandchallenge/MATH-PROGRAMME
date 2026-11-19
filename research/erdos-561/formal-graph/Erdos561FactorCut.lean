import Lean.Elab.Tactic.Omega

/-! Numerical part of the Lovasz (g,f)-factor obstruction argument,
without assuming that factor theorem is formalized. -/
namespace Erdos561FactorCut

/-- A connected simple D-regular induced set of r vertices, r≤D,
    has at least D edges leaving it: count incidences and at most
    r(r−1) internal incidences. This lemma checks the key polynomial. -/
theorem small_core_boundary (D r : Nat)
    (hr : 1 ≤ r) (hle : r ≤ D) :
    D ≤ r * (D - r + 1) := by
  have hleft : D - r ≤ r * (D - r) := by
    calc
      D - r = 1 * (D - r) := by simp
      _ ≤ r * (D - r) := Nat.mul_le_mul_right (D - r) hr
  have hstep : r * (D - r + 1) = r * (D - r) + r := by
    simp [Nat.mul_add]
  omega

/-- α and β are positive. Therefore a core component with at least D
    boundary edges contributes at least D in weighted S/T crossing. -/
theorem weighted_boundary (α β D s t : Nat)
    (ha : 1 ≤ α) (hb : 1 ≤ β)
    (hsum : D ≤ s + t) :
    D ≤ α * s + β * t := by
  have hs : s ≤ α * s := by
    calc
      s = 1 * s := by simp
      _ ≤ α * s := Nat.mul_le_mul_right s ha
  have ht : t ≤ β * t := by
    calc
      t = 1 * t := by simp
      _ ≤ β * t := Nat.mul_le_mul_right t hb
  omega

/-- Disjoint tight parity components each paying D boundary units
    imply their collective weighted cut budget is at least D per component.
    The edges disjointness and actual component extraction remain separate
    graph-theoretic semantic inputs. -/
theorem weighted_boundary_sum (α β D : Nat) (xs : List (Nat × Nat))
    (hα : 1 ≤ α) (hβ : 1 ≤ β)
    (h : ∀ x ∈ xs, D ≤ x.1 + x.2) :
    D * xs.length ≤
      α * ((xs.map fun x => x.1).sum) +
      β * ((xs.map fun x => x.2).sum) := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
      have hx : D ≤ x.1 + x.2 := h x (by simp)
      have htail : ∀ y ∈ xs, D ≤ y.1 + y.2 := by
        intro y hy
        exact h y (by simp [hy])
      have hhead := weighted_boundary α β D x.1 x.2 hα hβ hx
      have hrest := ih htail
      simp only [List.length_cons, List.map_cons, List.sum_cons,
        Nat.mul_add] at *
      omega

/-- At every vertex with degree at most D=alpha+beta, the upper
    red-degree bound f=min(alpha,d) is above the proportional target. -/
theorem local_upper_envelope (α β d : Nat)
    (hd : d ≤ α + β) :
    α * d ≤ (α + β) * min α d := by
  by_cases h : d ≤ α
  · rw [Nat.min_eq_right h]
    have hx : α * d ≤ (α + β) * d :=
      Nat.mul_le_mul_right d (Nat.le_add_right α β)
    exact hx
  · have ha : α ≤ d := by omega
    rw [Nat.min_eq_left ha]
    have hx : α * d ≤ α * (α + β) := Nat.mul_le_mul_left α hd
    simpa [Nat.mul_comm] using hx

/-- At every vertex of degree at most D=alpha+beta, the red lower
    bound g=d-beta stays below the proportional target. -/
theorem local_lower_envelope (α β d : Nat)
    (hd : d ≤ α + β) :
    (α + β) * (d - β) ≤ α * d := by
  by_cases h : d ≤ β
  · have hz : d - β = 0 := Nat.sub_eq_zero_of_le h
    simp [hz]
  · have hβ : β ≤ d := by omega
    have heq : d - β + β = d := Nat.sub_add_cancel hβ
    have ht : d - β ≤ α := by omega
    have hmul : β * (d - β) ≤ β * α := Nat.mul_le_mul_left β ht
    have hright : α * d = α * (d - β) + α * β := by
      calc
        α * d = α * (d - β + β) := by rw [heq]
        _ = α * (d - β) + α * β := by simp [Nat.mul_add]
    have hleft : (α + β) * (d - β) =
        α * (d - β) + β * (d - β) := by simp [Nat.add_mul]
    calc
      (α + β) * (d - β) = α * (d - β) + β * (d - β) := hleft
      _ ≤ α * (d - β) + β * α := Nat.add_le_add_left hmul _
      _ = α * d := by simp [hright, Nat.mul_comm]

/-- A scaled (g,f)-factor cut certificate. Bound on q encodes
    disjoint small tight components; the actual component counting and
    Lovasz theorem are separately unformalized dependencies. -/
theorem cut_certificate
    (α β fS gT eSS eTT eST eSU eTU q : Nat)
    (hα : 1 ≤ α) (hβ : 1 ≤ β)
    (hf : (α + β) * fS ≥ α * (2 * eSS + eST + eSU))
    (hg : (α + β) * gT ≤ α * (2 * eTT + eST + eTU))
    (hq : (α + β) * q ≤ α * eSU + β * eTU) :
    gT + eST + q ≤ fS + (2 * eTT + eST + eTU) := by
  have hscale : (α + β) * (gT + eST + q) ≤
      (α + β) * (fS + (2 * eTT + eST + eTU)) := by
    simp only [Nat.mul_add, Nat.add_mul] at hf hg hq ⊢
    omega
  have hp : 0 < α + β := by omega
  exact Nat.le_of_mul_le_mul_left hscale hp

#print axioms Erdos561FactorCut.small_core_boundary
#print axioms Erdos561FactorCut.weighted_boundary
#print axioms Erdos561FactorCut.weighted_boundary_sum
#print axioms Erdos561FactorCut.cut_certificate
#print axioms Erdos561FactorCut.local_upper_envelope
#print axioms Erdos561FactorCut.local_lower_envelope
end Erdos561FactorCut
