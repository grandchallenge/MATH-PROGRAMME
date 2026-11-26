import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFirstColumnRange

/-! Concrete cycle and boundary criteria for the actual Mathlib homology. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
namespace CMDG.CondensedCM5R0.BreenDeligneHomologyElements

theorem prev_degree (n : ℕ) : c.prev n=n+1 :=
  c.prev_eq' (show c.Rel (n+1) n by rfl)

theorem next_degree (n : ℕ) : c.next n=n-1 := by
  cases n with
  | zero => exact c.next_eq_self' 0 (fun k hk => by change k+1=0 at hk; omega)
  | succ n => exact c.next_eq' (show c.Rel (n+1) n by rfl)

def cycleOf (K : Ch) (n : ℕ) (x : K.X n) (hx : K.d n (n-1) x=0) : K.cycles n :=
  (K.sc n).moduleCatCyclesIso.inv ⟨x,by
    change K.d n (c.next n) x=0
    rw [next_degree]
    exact hx⟩

set_option backward.isDefEq.respectTransparency false in
theorem cycleOf_i (K : Ch) (n : ℕ) (x : K.X n) (hx : K.d n (n-1) x=0) :
    K.iCycles n (cycleOf K n x hx)=x := by
  exact CategoryTheory.congr_fun ((K.sc n).moduleCatCyclesIso_inv_iCycles)
    (⟨x,by change K.d n (c.next n) x=0; rw [next_degree]; exact hx⟩ :
      (K.sc n).moduleCatLeftHomologyData.K)

theorem cycle_closed (K : Ch) (n : ℕ) (z : K.cycles n) :
    K.d n (n-1) (K.iCycles n z)=0 :=
  CategoryTheory.congr_fun (K.iCycles_d n (n-1)) z

theorem iCycles_injective (K : Ch) (n : ℕ) : Function.Injective (K.iCycles n) :=
  (ModuleCat.mono_iff_injective _).mp inferInstance

theorem class_surj (K : Ch) (n : ℕ) : Function.Surjective (K.homologyπ n) :=
  (ModuleCat.epi_iff_surjective _).mp inferInstance

theorem class_pOpcycles (K : Ch) (n : ℕ) (z : K.cycles n) :
    K.homologyπ n z=0 ↔ K.pOpcycles n (K.iCycles n z)=0 := by
  have he := CategoryTheory.congr_fun (K.homology_π_ι n) z
  change K.homologyι n (K.homologyπ n z) = K.pOpcycles n (K.iCycles n z) at he
  constructor
  · intro h
    rw [← he,h,map_zero]
  · intro h
    apply (ModuleCat.mono_iff_injective (K.homologyι n)).mp inferInstance
    rw [he,h,map_zero]

set_option backward.isDefEq.respectTransparency false in
theorem class_zero_iff (K : Ch) (n : ℕ) (z : K.cycles n) :
    K.homologyπ n z=0 ↔ ∃ y : K.X (n+1), K.d (n+1) n y=K.iCycles n z := by
  rw [class_pOpcycles]
  change (K.sc n).pOpcycles (K.iCycles n z)=0 ↔ _
  rw [ShortComplex.moduleCat_pOpcycles_eq_zero_iff]
  change (∃ y : K.X (c.prev n), K.d (c.prev n) n y=K.iCycles n z) ↔ _
  have hp := prev_degree n
  rw [hp]

theorem class_eq_of_boundary_diff (K : Ch) (n : ℕ) (z w : K.cycles n)
    (y : K.X (n+1)) (h : K.d (n+1) n y=K.iCycles n z-K.iCycles n w) :
    K.homologyπ n z=K.homologyπ n w := by
  have hz : K.homologyπ n (z-w)=0 :=
    (class_zero_iff K n (z-w)).mpr ⟨y,by rw [map_sub]; exact h⟩
  rw [map_sub] at hz
  exact sub_eq_zero.mp hz

theorem map_cycle_i {K L : Ch} (f : K ⟶ L) (n : ℕ) (z : K.cycles n) :
    L.iCycles n (cyclesMap f n z) = f.f n (K.iCycles n z) :=
  CategoryTheory.congr_fun (cyclesMap_i f n) z

theorem map_class {K L : Ch} (f : K ⟶ L) (n : ℕ) (z : K.cycles n) :
    homologyMap f n (K.homologyπ n z)=L.homologyπ n (cyclesMap f n z) :=
  CategoryTheory.congr_fun (homologyπ_naturality f n) z

#print axioms cycleOf_i
#print axioms class_zero_iff
#print axioms class_eq_of_boundary_diff
end CMDG.CondensedCM5R0.BreenDeligneHomologyElements
