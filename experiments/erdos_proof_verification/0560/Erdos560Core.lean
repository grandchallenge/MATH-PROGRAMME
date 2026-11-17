import Init

/-!
Erdos-PV-0560-C: independently checked finite-graph semantic invariants
and the exact integer-cleared factor bound from the primary Proposition 2.2.
This is *not* a formal proof of the full size-Ramsey proposition.
No external libraries are imported.
-/

namespace ErdosPV0560

/-- A loopless undirected graph. No induced-subgraph condition is imposed. -/
structure SimpleAdj (V : Type) where
  adj : V → V → Prop
  symm : ∀ ⦃v w : V⦄, adj v w → adj w v
  loopless : ∀ v : V, ¬ adj v v

/-- Every required cross-edge exists, whether or not intra-side edges exist. -/
def CompleteBetween {V : Type} (G : SimpleAdj V)
    (S T : V → Prop) : Prop :=
  ∀ ⦃v : V⦄, S v → ∀ ⦃w : V⦄, T w → G.adj v w

/-- Source-semantic lemma: the cross-edge condition forces disjoint sides. -/
theorem completeBetween_disjoint {V : Type} (G : SimpleAdj V)
    {S T : V → Prop} (h : CompleteBetween G S T) :
    ∀ v : V, ¬ (S v ∧ T v) := by
  intro v hv
  exact G.loopless v (h hv.1 hv.2)

/-- The left-side vertex must be adjacent to every right-side vertex. -/
theorem right_subset_neighbors {V : Type} (G : SimpleAdj V)
    {S T : V → Prop} (h : CompleteBetween G S T)
    {v : V} (hv : S v) :
    ∀ w : V, T w → G.adj v w := by
  intro w hw
  exact h hv hw

/-- Cross-completeness is symmetric, but the sides are not identified. -/
theorem completeBetween_symm {V : Type} (G : SimpleAdj V)
    {S T : V → Prop} (h : CompleteBetween G S T) :
    CompleteBetween G T S := by
  intro v hv w hw
  exact G.symm (h hw hv)

/-- A non-induced copy remains a copy when host edges are added. -/
theorem completeBetween_mono {V : Type}
    (G H : SimpleAdj V)
    (hle : ∀ ⦃v w : V⦄, G.adj v w → H.adj v w)
    {S T : V → Prop}
    (h : CompleteBetween G S T) :
    CompleteBetween H S T := by
  intro v hv w hw
  exact hle (h hv hw)

/-- Arithmetic bound needed to clear the analytic integral factor. -/
theorem n_le_two_pow (n : Nat) : n ≤ 2 ^ n := by
  induction n with
  | zero =>
      decide
  | succ n ih =>
      have hp : 1 ≤ 2 ^ n := Nat.one_le_pow n 2 (by decide)
      calc
        n.succ ≤ 2 * (2 ^ n) := by omega
        _ = 2 ^ n.succ := by
          simp [Nat.pow_succ, Nat.mul_comm]

/--
For s>=2, a>=2, the exact nonnegative-integer clearing of
 (s-1)/(a-1) * (s/(s-1))^a <= 2^(s+a).
The denominators a-1 and (s-1)^a are positive in this regime.
-/
theorem integral_factor_cleared (s a : Nat)
    (hs : 2 ≤ s) (ha : 2 ≤ a) :
    (s - 1) * s ^ a ≤ (a - 1) * (2 ^ (s + a)) * (s - 1) ^ a := by
  have hbase : s ≤ 2 * (s - 1) := by omega
  have hpow : s ^ a ≤ (2 ^ a) * ((s - 1) ^ a) := by
    calc
      s ^ a ≤ (2 * (s - 1)) ^ a := Nat.pow_le_pow_left hbase a
      _ = (2 ^ a) * ((s - 1) ^ a) := Nat.mul_pow 2 (s - 1) a
  have hsub : s - 1 ≤ 2 ^ s :=
    Nat.le_trans (Nat.sub_le s 1) (n_le_two_pow s)
  calc
    (s - 1) * s ^ a
        ≤ (s - 1) * ((2 ^ a) * ((s - 1) ^ a)) :=
          Nat.mul_le_mul_left (s - 1) hpow
    _ ≤ (2 ^ s) * ((2 ^ a) * ((s - 1) ^ a)) :=
          Nat.mul_le_mul_right ((2 ^ a) * ((s - 1) ^ a)) hsub
    _ = (2 ^ (s + a)) * (s - 1) ^ a := by
          simp [Nat.pow_add, Nat.mul_assoc]
    _ ≤ (a - 1) * ((2 ^ (s + a)) * ((s - 1) ^ a)) := by
          exact Nat.le_mul_of_pos_left _ (by omega)
    _ = (a - 1) * (2 ^ (s + a)) * (s - 1) ^ a := by
          simp [Nat.mul_assoc]

/-- Exact rational first-moment numerical gate, cleared of denominators. -/
theorem strict_gate_base : 2 * 18 ^ 4 < 25 ^ 4 := by decide

/-- The strict gate propagates from t=4 to every larger integer exponent. -/
theorem strict_gate_step (n : Nat)
    (hn : 2 * 18 ^ n < 25 ^ n) :
    2 * 18 ^ (n + 1) < 25 ^ (n + 1) := by
  have hlt : (2 * 18 ^ n) * 18 < (25 ^ n) * 18 :=
    Nat.mul_lt_mul_of_pos_right hn (by decide)
  have hle : (25 ^ n) * 18 ≤ (25 ^ n) * 25 :=
    Nat.mul_le_mul_left (25 ^ n) (by decide)
  calc
    2 * 18 ^ (n + 1) = (2 * 18 ^ n) * 18 := by
      simp [Nat.pow_succ, Nat.mul_assoc]
    _ < (25 ^ n) * 18 := hlt
    _ ≤ (25 ^ n) * 25 := hle
    _ = 25 ^ (n + 1) := by simp [Nat.pow_succ]

/-- Exactly the t>=4 numerator/denominator inequality used after e<3. -/
theorem strict_gate_all (t : Nat) (ht : 4 ≤ t) :
    2 * 18 ^ t < 25 ^ t := by
  have hfamily (k : Nat) : 2 * 18 ^ (4 + k) < 25 ^ (4 + k) := by
    induction k with
    | zero =>
        exact strict_gate_base
    | succ k ih =>
        have hsucc : 4 + k.succ = (4 + k) + 1 := by omega
        rw [hsucc]
        exact strict_gate_step (4 + k) ih
  have heq : t = 4 + (t - 4) := by omega
  rw [heq]
  exact hfamily (t - 4)

/-- Positivity makes the cleared factor inequality faithful. -/
theorem integral_denominators_positive (s a : Nat)
    (hs : 2 ≤ s) (ha : 2 ≤ a) :
    0 < (a - 1) * (s - 1) ^ a := by
  have h1 : 0 < a - 1 := by omega
  have h2 : 0 < s - 1 := by omega
  exact Nat.mul_pos h1 (Nat.pow_pos h2)

/-- Published parameter conditions force a convergent tail exponent. -/
theorem gap_ge_two (s t : Nat) (hst : s + 2 ≤ t) :
    2 ≤ t - s := by omega

/-- Published parameter conditions force the numerical t>=4 gate. -/
theorem t_ge_four (s t : Nat)
    (hs : 2 ≤ s) (hst : s + 2 ≤ t) : 4 ≤ t := by omega

#print ErdosPV0560.CompleteBetween
#check ErdosPV0560.integral_factor_cleared
#check ErdosPV0560.strict_gate_all
#check ErdosPV0560.completeBetween_disjoint

#print axioms completeBetween_disjoint
#print axioms right_subset_neighbors
#print axioms completeBetween_symm
#print axioms completeBetween_mono
#print axioms n_le_two_pow
#print axioms integral_factor_cleared
#print axioms strict_gate_base
#print axioms strict_gate_step
#print axioms strict_gate_all
#print axioms integral_denominators_positive
#print axioms gap_ge_two
#print axioms t_ge_four

end ErdosPV0560
