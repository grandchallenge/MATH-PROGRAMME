import Erdos27Period
open scoped BigOperators
namespace Erdos27Split

def Smooth (Q a : ℕ) : Prop := ∀ p : ℕ, Nat.Prime p → p ∣ a → p ≤ Q
def Rough (Q b : ℕ) : Prop := ∀ p : ℕ, Nat.Prime p → p ∣ b → Q < p

theorem smooth_one (Q : ℕ) : Smooth Q 1 := by
  intro p hp hd
  exact (hp.not_dvd_one hd).elim

theorem rough_one (Q : ℕ) : Rough Q 1 := by
  intro p hp hd
  exact (hp.not_dvd_one hd).elim

theorem smooth_mul {Q a b : ℕ} (ha : Smooth Q a) (hb : Smooth Q b) :
    Smooth Q (a*b) := by
  intro p hp hd
  rcases hp.dvd_mul.mp hd with h|h
  · exact ha p hp h
  · exact hb p hp h

theorem rough_mul {Q a b : ℕ} (ha : Rough Q a) (hb : Rough Q b) :
    Rough Q (a*b) := by
  intro p hp hd
  rcases hp.dvd_mul.mp hd with h|h
  · exact ha p hp h
  · exact hb p hp h

theorem smooth_prime {Q p : ℕ} (hp : Nat.Prime p) (h : p ≤ Q) : Smooth Q p := by
  intro q hq hd
  exact (Nat.le_of_dvd hp.pos hd).trans h

theorem rough_prime {Q p : ℕ} (hp : Nat.Prime p) (h : Q < p) : Rough Q p := by
  intro q hq hd
  have eq : q = p := by
    rcases (Nat.dvd_prime hp).mp hd with he|he
    · exact (hq.ne_one he).elim
    · exact he
  simpa [eq] using h

theorem cross_coprime {Q a b : ℕ} (ha : Smooth Q a) (hb : Rough Q b) :
    a.Coprime b := by
  apply Nat.coprime_of_dvd
  intro p hp hpa hpb
  exact (Nat.not_lt_of_ge (ha p hp hpa)) (hb p hp hpb)

theorem split_exists (Q n : ℕ) (hn : 0 < n) :
    ∃ a b : ℕ, 0 < a ∧ 0 < b ∧ a*b=n ∧ Smooth Q a ∧ Rough Q b := by
  induction n using Nat.strong_induction_on with
  | h n ih =>
    by_cases h1 : n = 1
    · subst n
      exact ⟨1,1,by decide,by decide,rfl,smooth_one Q,rough_one Q⟩
    · obtain ⟨p,hp,hd⟩ := Nat.exists_prime_and_dvd h1
      have hlt : n/p < n := Nat.div_lt_self hn hp.two_le
      have hpos : 0 < n/p := Nat.div_pos (Nat.le_of_dvd hn hd) hp.pos
      obtain ⟨a,b,ha,hb,hab,hs,hr⟩ := ih (n/p) hlt hpos
      have he : a*b*p=n := hab ▸ Nat.div_mul_cancel hd
      by_cases hq : p ≤ Q
      · refine ⟨a*p,b,Nat.mul_pos ha hp.pos,hb,?_,smooth_mul hs (smooth_prime hp hq),hr⟩
        rw [Nat.mul_assoc, Nat.mul_comm p b, ← Nat.mul_assoc,he]
      · exact ⟨a,b*p,ha,Nat.mul_pos hb hp.pos,by rw [← Nat.mul_assoc,he],hs,
          rough_mul hr (rough_prime hp (Nat.lt_of_not_ge hq))⟩

theorem split_unique {Q a b c d : ℕ} (ha : Smooth Q a) (hb : Rough Q b)
    (hc : Smooth Q c) (hd : Rough Q d) (he : a*b=c*d) (hpos : 0 < a) :
    a=c ∧ b=d := by
  have h1 : a ∣ c := (cross_coprime ha hd).dvd_of_dvd_mul_right
    (he ▸ Nat.dvd_mul_right a b)
  have h2 : c ∣ a := (cross_coprime hc hb).dvd_of_dvd_mul_right
    (he.symm ▸ Nat.dvd_mul_right c d)
  have h3 : a=c := Nat.dvd_antisymm h1 h2
  subst c
  exact ⟨rfl,Nat.eq_of_mul_eq_mul_left hpos he⟩

theorem smooth_dvd {Q a b : ℕ} (h : a ∣ b) (hb : Smooth Q b) : Smooth Q a :=
  fun p hp hd => hb p hp (hd.trans h)

theorem rough_dvd {Q a b : ℕ} (h : a ∣ b) (hb : Rough Q b) : Rough Q a :=
  fun p hp hd => hb p hp (hd.trans h)

theorem smooth_lcm {ι : Type*} (Q : ℕ) (S : Finset ι) (a : ι → ℕ)
    (hs : ∀ i ∈ S, Smooth Q (a i)) : Smooth Q (S.lcm a) := by
  classical
  induction S using Finset.induction_on with
  | empty => simpa using smooth_one Q
  | @insert i S hi ih =>
    rw [Finset.lcm_insert]
    exact smooth_dvd (Nat.lcm_dvd (Nat.dvd_mul_right _ _) (Nat.dvd_mul_left _ _))
      (smooth_mul (hs i (Finset.mem_insert_self i S))
        (ih (fun j hj => hs j (Finset.mem_insert_of_mem hj))))

theorem rough_lcm {ι : Type*} (Q : ℕ) (S : Finset ι) (b : ι → ℕ)
    (hr : ∀ i ∈ S, Rough Q (b i)) : Rough Q (S.lcm b) := by
  classical
  induction S using Finset.induction_on with
  | empty => simpa using rough_one Q
  | @insert i S hi ih =>
    rw [Finset.lcm_insert]
    exact rough_dvd (Nat.lcm_dvd (Nat.dvd_mul_right _ _) (Nat.dvd_mul_left _ _))
      (rough_mul (hr i (Finset.mem_insert_self i S))
        (ih (fun j hj => hr j (Finset.mem_insert_of_mem hj))))

theorem lcm_split {ι : Type*} (Q : ℕ) (S : Finset ι) (a b : ι → ℕ)
    (hs : ∀ i ∈ S, Smooth Q (a i)) (hr : ∀ i ∈ S, Rough Q (b i)) :
    S.lcm (fun i => a i*b i) = S.lcm a * S.lcm b := by
  have hcop := cross_coprime (smooth_lcm Q S a hs) (rough_lcm Q S b hr)
  apply Nat.dvd_antisymm
  · exact Finset.lcm_dvd (fun i hi => Nat.mul_dvd_mul (Finset.dvd_lcm hi) (Finset.dvd_lcm hi))
  · apply hcop.mul_dvd_of_dvd_of_dvd
    · exact Finset.lcm_dvd (fun i hi => (Nat.dvd_mul_right (a i) (b i)).trans (Finset.dvd_lcm hi))
    · exact Finset.lcm_dvd (fun i hi => (Nat.dvd_mul_left (b i) (a i)).trans (Finset.dvd_lcm hi))

theorem family_split {ι : Type*} [Fintype ι] (Q : ℕ) (n : ι → ℕ) (hn : ∀ i, 0 < n i) :
    ∃ a b : ι → ℕ, (∀ i, 0 < a i ∧ 0 < b i ∧ a i*b i=n i ∧ Smooth Q (a i) ∧ Rough Q (b i)) ∧
      (Finset.univ.lcm a).Coprime (Finset.univ.lcm b) ∧
      Finset.univ.lcm n = Finset.univ.lcm a * Finset.univ.lcm b := by
  classical
  choose a b hab using fun i => split_exists Q (n i) (hn i)
  refine ⟨a,b,hab,?_,?_⟩
  · exact cross_coprime (smooth_lcm Q Finset.univ a (fun i _ => (hab i).2.2.2.1))
      (rough_lcm Q Finset.univ b (fun i _ => (hab i).2.2.2.2))
  · rw [← lcm_split Q Finset.univ a b (fun i _ => (hab i).2.2.2.1) (fun i _ => (hab i).2.2.2.2)]
    exact Finset.lcm_congr rfl (fun i _ => (hab i).2.2.1.symm)

theorem split_lcm_positive {ι : Type*} (S : Finset ι) (a : ι → ℕ)
    (ha : ∀ i ∈ S, 0 < a i) : 0 < S.lcm a := by
  exact Nat.pos_of_ne_zero (Finset.lcm_ne_zero_iff.mpr (fun i hi => Nat.ne_of_gt (ha i hi)))

theorem congruence_transport {T u v : ℕ} (eq : u = v) (hu : u ∣ T) (hv : v ∣ T)
    (x : ZMod T) (r : ℤ) :
    (ZMod.castHom hu (ZMod u) x ≠ (r : ZMod u)) ↔
      (ZMod.castHom hv (ZMod v) x ≠ (r : ZMod v)) := by
  subst v
  rfl

open Erdos27CRT Erdos27Period in
theorem family_density {ι : Type*} [Fintype ι] (Q : ℕ) (n a b : ι → ℕ) (r : ι → ℤ)
    (ha : ∀ i, 0 < a i) (hb : ∀ i, 0 < b i)
    (he : ∀ i, a i*b i=n i)
    (hs : ∀ i, Smooth Q (a i)) (hr : ∀ i, Rough Q (b i)) :
    let M := Finset.univ.lcm a
    let B := Finset.univ.lcm b
    haveI : NeZero M := ⟨Nat.ne_of_gt (split_lcm_positive Finset.univ a (fun i _ => ha i))⟩
    haveI : NeZero B := ⟨Nat.ne_of_gt (split_lcm_positive Finset.univ b (fun i _ => hb i))⟩
    let da : ∀ i, a i ∣ M := fun i => Finset.dvd_lcm (Finset.mem_univ i)
    let db : ∀ i, b i ∣ B := fun i => Finset.dvd_lcm (Finset.mem_univ i)
    let dn : ∀ i, n i ∣ M*B := fun i => he i ▸ Nat.mul_dvd_mul (da i) (db i)
    density (fun x : ZMod (M*B) => ∀ i, ZMod.castHom (dn i) (ZMod (n i)) x ≠ (r i : ZMod (n i))) =
      (∑ h : ZMod M, density (fibreAvoid a b r da db h))/(M : ℚ) := by
  dsimp only
  have : NeZero (Finset.univ.lcm a) := ⟨Nat.ne_of_gt (split_lcm_positive Finset.univ a (fun i _ => ha i))⟩
  have : NeZero (Finset.univ.lcm b) := ⟨Nat.ne_of_gt (split_lcm_positive Finset.univ b (fun i _ => hb i))⟩
  have h := covering_density a b r
    (fun i => Finset.dvd_lcm (Finset.mem_univ i)) (fun i => Finset.dvd_lcm (Finset.mem_univ i))
    (fun i => cross_coprime (hs i) (hr i))
    (cross_coprime (smooth_lcm Q Finset.univ a (fun i _ => hs i))
      (rough_lcm Q Finset.univ b (fun i _ => hr i)))
  unfold density
  rw [← h]
  congr 1
  apply congrArg (fun P : ZMod (Finset.univ.lcm a * Finset.univ.lcm b) → Prop => (count P : ℚ))
  funext x
  apply propext
  unfold originalAvoid
  exact forall_congr' (fun i => (congruence_transport (he i) _ _ x (r i)).symm)

theorem smooth_power_allocation {Q a b p k : ℕ} (hp : Nat.Prime p) (hq : p ≤ Q)
    (hb : Rough Q b) : p^k ∣ a*b ↔ p^k ∣ a := by
  have hc : p.Coprime b := hp.coprime_iff_not_dvd.mpr
    (fun hd => (Nat.not_lt_of_ge hq) (hb p hp hd))
  exact ⟨(hc.pow_left k).dvd_of_dvd_mul_right,
    fun hd => hd.trans (Nat.dvd_mul_right a b)⟩

theorem rough_power_allocation {Q a b p k : ℕ} (hp : Nat.Prime p) (hq : Q < p)
    (ha : Smooth Q a) : p^k ∣ a*b ↔ p^k ∣ b := by
  have hc : p.Coprime a := hp.coprime_iff_not_dvd.mpr
    (fun hd => (Nat.not_le_of_gt hq) (ha p hp hd))
  exact ⟨(hc.pow_left k).dvd_of_dvd_mul_left,
    fun hd => hd.trans (Nat.dvd_mul_left b a)⟩

#print axioms smooth_power_allocation
#print axioms rough_power_allocation
#print axioms split_lcm_positive
#print axioms congruence_transport
#print axioms family_density
#check family_density
#print axioms smooth_one
#print axioms rough_one
#print axioms smooth_prime
#print axioms rough_prime
#print axioms smooth_dvd
#print axioms rough_dvd
#print axioms smooth_lcm
#print axioms rough_lcm
#print axioms lcm_split
#print axioms family_split
#print axioms smooth_mul
#print axioms rough_mul
#print axioms cross_coprime
#print axioms split_exists
#print axioms split_unique
end Erdos27Split
