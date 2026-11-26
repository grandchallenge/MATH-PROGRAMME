import Erdos27Period

open scoped BigOperators
namespace Erdos27Sequence
open Erdos27Period Erdos27Weighted

variable (T : ℕ) [NeZero T] (m : ℕ → ℕ) (r : ℕ → ℤ) (hm : ∀ i, m i ∣ T)

def residueEvent (i : ℕ) (x : ZMod T) : Prop :=
  ZMod.castHom (hm i) (ZMod (m i)) x = (r i : ZMod (m i))

noncomputable def A (i : ℕ) : Finset (ZMod T) :=
  predSet (residueEvent T m r hm i)

noncomputable def U (j : ℕ) : Finset (ZMod T) :=
  predSet (fun x => ∀ i < j, ¬ residueEvent T m r hm i x)

noncomputable def I (j : ℕ) : Finset (ZMod T) :=
  predSet (fun x => ∀ i < j, (m j).Coprime (m i) → ¬ residueEvent T m r hm i x)

def bad (j : ℕ) : Finset ℕ :=
  (Finset.range j).filter (fun i => ¬ (m j).Coprime (m i))

noncomputable def D (j : ℕ) : Finset (ZMod T) :=
  (bad m j).biUnion (A T m r hm)

def p (i : ℕ) : ℚ := 1 / (m i : ℚ)

def err (j : ℕ) : ℚ :=
  p m j * ∑ i ∈ bad m j, p m i

theorem residue_mass (i : ℕ) :
    mass T (A T m r hm i) = p m i := by
  have : NeZero (m i) := ⟨Nat.ne_of_gt (Nat.pos_of_dvd_of_pos (hm i) (Nat.pos_of_ne_zero (NeZero.ne T)))⟩
  rw [A, predSet_mass]
  exact common_residue_mass (m i) T (hm i) (r i : ZMod (m i))

theorem U_zero : mass T (U T m r hm 0) = 1 := by
  classical
  have h : U T m r hm 0 = Finset.univ := by
    ext x
    simp [U,predSet]
  rw [h,mass,Finset.card_univ,ZMod.card]
  exact div_self (by exact_mod_cast NeZero.ne T)

theorem U_succ (j : ℕ) :
    U T m r hm (j+1) = U T m r hm j \ A T m r hm j := by
  classical
  ext x
  simp only [U,A,predSet,Finset.mem_filter,Finset.mem_univ,true_and,Finset.mem_sdiff]
  constructor
  · intro h
    exact ⟨fun i hi => h i (Nat.lt_succ_of_lt hi), h j (Nat.lt_succ_self j)⟩
  · rintro ⟨h,hj⟩ i hi
    rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ hi) with hlt|heq
    · exact h i hlt
    · subst i
      exact hj

theorem U_split (j : ℕ) :
    U T m r hm j = I T m r hm j \ D T m r hm j := by
  classical
  ext x
  simp only [U,I,D,bad,A,predSet,Finset.mem_filter,Finset.mem_univ,true_and,
    Finset.mem_sdiff,Finset.mem_biUnion,Finset.mem_range]
  constructor
  · intro h
    exact ⟨fun i hi _ => h i hi, fun ⟨i,hi,hx⟩ => h i hi.1 hx⟩
  · rintro ⟨h,hd⟩ i hi
    by_cases hc : (m j).Coprime (m i)
    · exact h i hi hc
    · intro hx
      exact hd ⟨i,⟨hi,hc⟩,hx⟩

theorem D_bound (j : ℕ) :
    mass T (D T m r hm j) ≤ ∑ i ∈ bad m j, p m i := by
  classical
  calc
    mass T (D T m r hm j) ≤ ∑ i ∈ bad m j, mass T (A T m r hm i) := by
      unfold mass D
      rw [← Finset.sum_div, ← Nat.cast_sum]
      exact div_le_div_of_nonneg_right (by exact_mod_cast Finset.card_biUnion_le) (Nat.cast_nonneg T)
    _ = _ := Finset.sum_congr rfl (fun i _ => residue_mass T m r hm i)

theorem step_independence (j : ℕ) :
    mass T (A T m r hm j ∩ I T m r hm j) = p m j * mass T (I T m r hm j) := by
  classical
  have : NeZero (m j) := ⟨Nat.ne_of_gt (Nat.pos_of_dvd_of_pos (hm j) (Nat.pos_of_ne_zero (NeZero.ne T)))⟩
  let J := {i : Fin j // (m j).Coprime (m i.val)}
  let a : J → ℕ := fun i => m i.val.val
  let s : J → ℤ := fun i => r i.val.val
  let ha : ∀ i : J, a i ∣ T := fun i => hm i.val.val
  have hc : ∀ i : J, (m j).Coprime (a i) := fun i => i.property
  have hI : I T m r hm j = predSet (fun x : ZMod T =>
      ∀ i : J, ZMod.castHom (ha i) (ZMod (a i)) x ≠ (s i : ZMod (a i))) := by
    ext x
    simp only [I,predSet,Finset.mem_filter,Finset.mem_univ,true_and]
    constructor
    · intro h i
      exact h i.val.val i.val.isLt i.property
    · intro h i hi hcop
      exact h ⟨⟨i,hi⟩,hcop⟩
  rw [A,hI,predSet_inter,predSet_mass,predSet_mass]
  exact finite_family_independent (m j) T (hm j) (r j : ZMod (m j)) a s ha hc

theorem p_nonneg (i : ℕ) : 0 ≤ p m i :=
  div_nonneg zero_le_one (Nat.cast_nonneg _)

theorem p_le_one (hdiv : ∀ i, m i ∣ T) (i : ℕ) : p m i ≤ 1 := by
  have h : 0 < m i := Nat.pos_of_dvd_of_pos (hdiv i) (Nat.pos_of_ne_zero (NeZero.ne T))
  have hq : (0 : ℚ) < m i := by exact_mod_cast h
  unfold p
  apply (div_le_iff₀ hq).2
  rw [one_mul]
  exact_mod_cast h

theorem err_nonneg (j : ℕ) : 0 ≤ err m j :=
  mul_nonneg (p_nonneg m j) (Finset.sum_nonneg (fun i _ => p_nonneg m i))

theorem sequence_step (j : ℕ) :
    (1-p m j)*mass T (U T m r hm j) - err m j ≤ mass T (U T m r hm (j+1)) := by
  have h := finite_step T (I T m r hm j) (D T m r hm j) (A T m r hm j)
    (p m j) (∑ i ∈ bad m j, p m i) (p_nonneg m j) (D_bound T m r hm j)
    (step_independence T m r hm j)
  rw [← U_split T m r hm j, ← U_succ T m r hm j] at h
  exact h

theorem arithmetic_weighted (n : ℕ) :
    ideal (p m) n - weightedError (p m) (err m) n ≤ mass T (U T m r hm n) :=
  weighted_recurrence (p m) (err m) (fun j => mass T (U T m r hm j))
    (U_zero T m r hm) (p_le_one T m hm) (sequence_step T m r hm) n

theorem ideal_product (p' : ℕ → ℚ) (n : ℕ) :
    ideal p' n = ∏ i ∈ Finset.range n, (1-p' i) := by
  induction n with
  | zero => simp [ideal]
  | succ n ih => rw [ideal,Finset.prod_range_succ,ih,mul_comm]

theorem plain_sum (e : ℕ → ℚ) (n : ℕ) :
    plainError e n = ∑ j ∈ Finset.range n, e j := by
  induction n with
  | zero => simp [plainError]
  | succ n ih => rw [plainError,Finset.sum_range_succ,ih]

theorem arithmetic_lemma21 (n : ℕ) :
    (∏ i ∈ Finset.range n, (1 - 1/(m i : ℚ))) -
      (∑ j ∈ Finset.range n, ∑ i ∈ bad m j, 1/((m i : ℚ)*(m j : ℚ))) ≤
      mass T (U T m r hm n) := by
  have h := unweighted_bound (p m) (err m) (fun j => mass T (U T m r hm j))
    (U_zero T m r hm) (p_nonneg m) (p_le_one T m hm) (err_nonneg m)
    (sequence_step T m r hm) n
  rw [ideal_product,plain_sum] at h
  have he (j : ℕ) : err m j = ∑ i ∈ bad m j, 1/((m i : ℚ)*(m j : ℚ)) := by
    unfold err p
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    rw [div_mul_div_comm,one_mul,mul_comm (m j : ℚ)]
  simpa only [p,he] using h

theorem bad_mem (j i : ℕ) :
    i ∈ bad m j ↔ i < j ∧ ¬ (m j).Coprime (m i) := by
  simp [bad]

omit [NeZero T] in
theorem residue_congr {a b : ℕ} (eq : a = b) (ha : a ∣ T) (hb : b ∣ T)
    (x : ZMod T) (z : ℤ) :
    (ZMod.castHom ha (ZMod a) x ≠ (z : ZMod a)) ↔
    (ZMod.castHom hb (ZMod b) x ≠ (z : ZMod b)) := by
  subst b
  rfl

theorem mem_predSet {Q : ZMod T → Prop} (x : ZMod T) :
    x ∈ predSet Q ↔ Q x := by
  classical
  simp [predSet]

theorem finite_lemma21 (n : ℕ) (hd : ∀ i < n, m i ∣ T) :
    (∏ i ∈ Finset.range n, (1 - 1/(m i : ℚ))) -
      (∑ j ∈ Finset.range n, ∑ i ∈ bad m j, 1/((m i : ℚ)*(m j : ℚ))) ≤
      density (fun x : ZMod T => ∀ i : Fin n,
        ZMod.castHom (hd i.val i.isLt) (ZMod (m i.val)) x ≠ (r i.val : ZMod (m i.val))) := by
  classical
  let m' : ℕ → ℕ := fun i => if i < n then m i else 1
  have ha (i : ℕ) : m' i ∣ T := by
    by_cases hi : i < n
    · simpa [m',hi] using hd i hi
    · simp [m',hi]
  have he (i : ℕ) (hi : i < n) : m' i = m i := if_pos hi
  have h := arithmetic_lemma21 T m' r ha n
  have hp : (∏ i ∈ Finset.range n, (1 - 1/(m' i : ℚ))) =
      ∏ i ∈ Finset.range n, (1 - 1/(m i : ℚ)) := by
    apply Finset.prod_congr rfl
    intro i hi
    rw [he i (Finset.mem_range.mp hi)]
  have hs : (∑ j ∈ Finset.range n, ∑ i ∈ bad m' j, 1/((m' i : ℚ)*(m' j : ℚ))) =
      ∑ j ∈ Finset.range n, ∑ i ∈ bad m j, 1/((m i : ℚ)*(m j : ℚ)) := by
    apply Finset.sum_congr rfl
    intro j hj
    have hj' := Finset.mem_range.mp hj
    have hb : bad m' j = bad m j := by
      ext i
      simp only [bad_mem]
      by_cases hi : i < j
      · simp [hi,he j hj',he i (hi.trans hj')]
      · simp [hi]
    rw [hb]
    apply Finset.sum_congr rfl
    intro i hi
    rw [he j hj',he i (((bad_mem m j i).mp hi).1.trans hj')]
  have hU : U T m' r ha n = predSet (fun x : ZMod T => ∀ i : Fin n,
        ZMod.castHom (hd i.val i.isLt) (ZMod (m i.val)) x ≠ (r i.val : ZMod (m i.val))) := by
    apply Finset.ext
    intro x
    unfold U
    rw [mem_predSet T,mem_predSet T]
    unfold residueEvent
    constructor
    · intro H i
      exact (residue_congr T (he i.val i.isLt) (ha i.val) (hd i.val i.isLt) x (r i.val)).mp
        (H i.val i.isLt)
    · intro H i hi
      exact (residue_congr T (he i hi) (ha i) (hd i hi) x (r i)).mpr (H ⟨i,hi⟩)
  rw [hp,hs,hU,predSet_mass] at h
  exact h

theorem bad_mem_gcd (j i : ℕ) (hi : 0 < m i) (_hj : 0 < m j) :
    i ∈ bad m j ↔ i < j ∧ 1 < Nat.gcd (m i) (m j) := by
  rw [bad_mem]
  have hpos : 0 < Nat.gcd (m i) (m j) := Nat.gcd_pos_of_pos_left _ hi
  rw [Nat.Coprime, Nat.gcd_comm (m j) (m i)]
  omega

theorem common_period_exists (n : ℕ) (hpos : ∀ i < n, 0 < m i) :
    ∃ T : ℕ, 0 < T ∧ ∀ i < n, m i ∣ T := by
  classical
  let T := (Finset.range n).lcm m
  have hT : T ≠ 0 := by
    unfold T
    rw [Finset.lcm_ne_zero_iff]
    intro i hi
    exact Nat.ne_of_gt (hpos i (Finset.mem_range.mp hi))
  exact ⟨T,Nat.pos_of_ne_zero hT,fun i hi => Finset.dvd_lcm (Finset.mem_range.mpr hi)⟩

#print axioms bad_mem_gcd
#print axioms common_period_exists
#print axioms mem_predSet
#print axioms residue_congr
#print axioms bad_mem
#print axioms finite_lemma21
#check finite_lemma21
#print axioms step_independence
#print axioms p_nonneg
#print axioms p_le_one
#print axioms err_nonneg
#print axioms sequence_step
#print axioms arithmetic_weighted
#print axioms ideal_product
#print axioms plain_sum
#print axioms arithmetic_lemma21
#check arithmetic_lemma21
#print axioms residue_mass
#print axioms U_zero
#print axioms U_succ
#print axioms U_split
#print axioms D_bound
end Erdos27Sequence
