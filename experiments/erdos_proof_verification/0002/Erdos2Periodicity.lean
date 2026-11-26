import Std

namespace Erdos2
abbrev Class := Int × Nat
def period : List Class → Nat
  | [] => 1
  | c :: cs => Nat.lcm c.2 (period cs)
abbrev Covered (cs : List Class) (z : Int) : Prop :=
  cs.any (fun c => z % (c.2 : Int) == c.1 % (c.2 : Int)) = true

theorem period_dvd (cs : List Class) (c : Class) (hc : c ∈ cs) : c.2 ∣ period cs := by
  induction cs with
  | nil => simp at hc
  | cons a as ih =>
    simp only [List.mem_cons] at hc
    rcases hc with rfl | h
    · exact Nat.dvd_lcm_left _ _
    · exact Nat.dvd_trans (ih h) (Nat.dvd_lcm_right _ _)

theorem period_pos (cs : List Class) (h : ∀ c ∈ cs, 2 ≤ c.2) : 0 < period cs := by
  induction cs with
  | nil => decide
  | cons a as ih =>
    have ha : 0 < a.2 := Nat.lt_of_lt_of_le (by decide : 0 < 2) (h a (by simp))
    have hb : 0 < period as := ih (fun c hc => h c (by simp [hc]))
    exact Nat.lcm_pos ha hb

theorem covered_iff_exists (cs : List Class) (z : Int) :
    Covered cs z ↔ ∃ c ∈ cs, (c.2 : Int) ∣ z - c.1 := by
  simp only [Covered, List.any_eq_true, beq_iff_eq, Int.dvd_iff_emod_eq_zero,
    Int.emod_eq_emod_iff_emod_sub_eq_zero]

theorem covered_period (cs : List Class) (z : Int) :
    Covered cs z ↔ Covered cs (z % (period cs : Int)) := by
  simp only [Covered, List.any_eq_true, beq_iff_eq]
  constructor <;> intro h <;> obtain ⟨c, hc, he⟩ := h
  · exact ⟨c, hc, (Int.emod_emod_of_dvd z (Int.ofNat_dvd.mpr (period_dvd cs c hc))).trans he⟩
  · exact ⟨c, hc, (Int.emod_emod_of_dvd z (Int.ofNat_dvd.mpr (period_dvd cs c hc))).symm.trans he⟩

theorem covers_all_iff (cs : List Class) (h : ∀ c ∈ cs, 2 ≤ c.2) :
    (∀ z : Int, Covered cs z) ↔ ∀ r : Int, 0 ≤ r → r < (period cs : Int) → Covered cs r := by
  constructor
  · intro H r _ _; exact H r
  · intro H z
    have hp : 0 < (period cs : Int) := by exact_mod_cast period_pos cs h
    exact (covered_period cs z).mpr (H _ (Int.emod_nonneg _ (Int.ne_of_gt hp)) (Int.emod_lt_of_pos _ hp))

theorem covered_shift (cs : List Class) (z : Int) :
    Covered cs (z + (period cs : Int)) ↔ Covered cs z := by
  have e : (z + (period cs : Int)) % (period cs : Int) = z % (period cs : Int) := by
    rw [Int.add_emod]; simp
  exact (covered_period cs _).trans (e ▸ (covered_period cs z).symm)

theorem uncovered_residue (cs : List Class) (z : Int)
    (h : ¬ Covered cs (z % (period cs : Int))) : ¬ Covered cs z :=
  fun hz => h ((covered_period cs z).mp hz)

theorem empty_period : period [] = 1 := by decide
theorem empty_uncovered (z : Int) : ¬ Covered [] z := by simp [Covered]

def exampleClasses : List Class := [(0,2),(0,3),(1,4),(3,8),(7,12),(23,24)]
def hostileClasses : List Class := [(0,2),(0,3),(1,4),(3,8),(7,12),(24,24)]
theorem example_period : period exampleClasses = 24 := by decide
theorem example_moduli : ∀ c ∈ exampleClasses, 2 ≤ c.2 := by decide
theorem example_distinct : (exampleClasses.map Prod.snd).Nodup := by decide
theorem example_finite : ∀ r : Fin 24, Covered exampleClasses (r.val : Int) := by decide
theorem example_cover : ∀ z : Int, Covered exampleClasses z := by
  apply (covers_all_iff exampleClasses example_moduli).mpr
  intro r hr hlt
  rw [example_period] at hlt
  have hnat : r.toNat < 24 := by omega
  have he : (r.toNat : Int) = r := by omega
  simpa only [he] using example_finite ⟨r.toNat, hnat⟩
theorem hostile_miss : ¬ Covered hostileClasses 23 := by decide
theorem repeated_cover : ∀ z : Int, Covered [(0,2),(1,2)] z := by
  intro z
  have h := (covered_period [(0,2),(1,2)] z)
  apply h.mpr
  have h0 : 0 ≤ z % 2 := Int.emod_nonneg _ (by decide)
  have h1 : z % 2 < 2 := Int.emod_lt_of_pos _ (by decide)
  have e : z % 2 = 0 ∨ z % 2 = 1 := by omega
  change Covered [(0,2),(1,2)] (z % 2)
  rcases e with e | e <;> rw [e] <;> decide
theorem repeated_not_distinct : ¬ (([(0,2),(1,2)] : List Class).map Prod.snd).Nodup := by decide
#print axioms period_dvd
#print axioms period_pos
#print axioms covered_iff_exists
#print axioms covered_period
#print axioms covers_all_iff
#print axioms covered_shift
#print axioms uncovered_residue
#print axioms empty_period
#print axioms empty_uncovered
#print axioms example_period
#print axioms example_moduli
#print axioms example_distinct
#print axioms example_finite
#print axioms example_cover
#print axioms hostile_miss
#print axioms repeated_cover
#print axioms repeated_not_distinct
#check period_dvd
#check period_pos
#check covered_iff_exists
#check covered_period
#check covers_all_iff
#check covered_shift
#check uncovered_residue
#check example_cover
#check hostile_miss
#check repeated_cover
#check repeated_not_distinct
end Erdos2
