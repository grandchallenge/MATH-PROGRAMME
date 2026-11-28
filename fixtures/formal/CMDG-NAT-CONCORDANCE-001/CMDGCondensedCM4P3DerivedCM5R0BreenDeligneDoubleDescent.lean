import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFreeExactness

/-! Elementary exactness descent for an augmented commuting double
complex. Both augmentation positions are numbered zero. The proof
uses simultaneous cycles and induction on vertical degree, not
convergence of a spectral sequence. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
open BreenDeligneProbe

structure DoubleAugmented where
  obj : ℕ → ℕ → Mod.{u}
  v : ∀ n j, obj (n+1) j ⟶ obj n j
  h : ∀ n j, obj n (j+1) ⟶ obj n j
  vv : ∀ n j, v (n+1) j ≫ v n j = 0
  hh : ∀ n j, h n (j+1) ≫ h n j = 0
  commute : ∀ n j, h (n+1) j ≫ v n j = v n (j+1) ≫ h n j

namespace DoubleAugmented
variable (D : DoubleAugmented.{u})

def VCycle : (n j : ℕ) → D.obj n j → Prop
  | 0, _, _ => True
  | n+1, j, x => D.v n j x = 0

def HCycle : (n j : ℕ) → D.obj n j → Prop
  | _, 0, _ => True
  | n, j+1, x => D.h n j x = 0

abbrev HExact : Prop := ∀ n j (x : D.obj n j), D.HCycle n j x →
  ∃ y : D.obj n (j+1), D.h n j y = x

abbrev VExactPositive : Prop := ∀ n j (x : D.obj n (j+1)), D.VCycle n (j+1) x →
  ∃ y : D.obj (n+1) (j+1), D.v n (j+1) y = x

theorem h_commute_apply (n j : ℕ) (x : D.obj (n+1) (j+1)) :
    D.v n j (D.h (n+1) j x) = D.h n j (D.v n (j+1) x) :=
  CategoryTheory.congr_fun (D.commute n j) x

theorem v_cycle (n j : ℕ) (x : D.obj (n+1) j) :
    D.VCycle n j (D.v n j x) := by
  cases n with
  | zero => trivial
  | succ n =>
    exact CategoryTheory.congr_fun (D.vv n j) x

theorem h_cycle (n j : ℕ) (x : D.obj n (j+1)) :
    D.HCycle n j (D.h n j x) := by
  cases j with
  | zero => trivial
  | succ j =>
    exact CategoryTheory.congr_fun (D.hh n j) x

/-- Simultaneous cycles lift vertically while retaining the horizontal
cycle condition, even in the augmentation column. -/
theorem simultaneous_lift (hH : D.HExact) (hV : D.VExactPositive) :
    ∀ n j (x : D.obj n j), D.VCycle n j x → D.HCycle n j x →
      ∃ y : D.obj (n+1) j, D.v n j y = x ∧ D.HCycle (n+1) j y := by
  intro n
  induction n with
  | zero =>
    intro j x _ hx
    obtain ⟨z,hz⟩ := hH 0 j x hx
    obtain ⟨w,hw⟩ := hV 0 j z trivial
    exact ⟨D.h 1 j w, by rw [D.h_commute_apply,hw,hz], D.h_cycle 1 j w⟩
  | succ n ih =>
    intro j x hxv hxh
    obtain ⟨z,hz⟩ := hH (n+1) j x hxh
    have hv : D.VCycle n (j+1) (D.v n (j+1) z) := D.v_cycle n (j+1) z
    have hh : D.HCycle n (j+1) (D.v n (j+1) z) := by
      change D.h n j (D.v n (j+1) z) = 0
      rw [← D.h_commute_apply,hz]
      exact hxv
    obtain ⟨w,hw,hwh⟩ := ih (j+1) (D.v n (j+1) z) hv hh
    have hzw : D.VCycle (n+1) (j+1) (z-w) := by
      change D.v n (j+1) (z-w) = 0
      rw [map_sub,hw,sub_self]
    obtain ⟨t,ht⟩ := hV (n+1) j (z-w) hzw
    refine ⟨D.h (n+2) j t,?_,D.h_cycle (n+2) j t⟩
    rw [D.h_commute_apply,ht,map_sub,hz]
    change D.h (n+1) j w = 0 at hwh
    rw [hwh,sub_zero]

theorem augmentation_exact (hH : D.HExact) (hV : D.VExactPositive) :
    ∀ n (x : D.obj n 0), D.VCycle n 0 x →
      ∃ y : D.obj (n+1) 0, D.v n 0 y = x := by
  intro n x hx
  obtain ⟨y,hy,_⟩ := D.simultaneous_lift hH hV n 0 x hx trivial
  exact ⟨y,hy⟩

#print axioms simultaneous_lift
#print axioms augmentation_exact
end DoubleAugmented
end CMDG.CondensedCM5R0.BreenDeligneProbe.UniversalExtension
