import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneHomologyElements

/-! For a total cycle, including column zero, a zero top-column
homology class can be removed by an actual total boundary. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
open CMDG.CondensedCM5R0.BreenDeligneTotalCoordinates
open CMDG.CondensedCM5R0.BreenDeligneColumnElimination
open CMDG.CondensedCM5R0.BreenDeligneHomologyElements
namespace CMDG.CondensedCM5R0.BreenDeligneFiniteColumnRemoval

theorem top_closed (K : BC) (r q : ℕ) (z : (K.total c).cycles (r+q))
    (hz : SupportedThrough K (r+q) r ((K.total c).iCycles (r+q) z)) :
    (K.X r).d q (q-1) (proj K (r+q) r q rfl ((K.total c).iCycles (r+q) z))=0 := by
  cases q with
  | zero =>
    rw [(K.X r).shape 0 0 (by decide)]
    rfl
  | succ q =>
    change (K.X r).d (q+1) q (proj K (r+q+1) r (q+1) (by omega) ((K.total c).iCycles (r+q+1) z))=0
    let x := (K.total c).iCycles (r+q+1) z
    have h := diff_proj_apply K (r+q) r q rfl x
    have hzero : (K.total c).d (r+q+1) (r+q) x=0 := cycle_closed _ _ z
    have htop : proj K (r+q+1) (r+1) q (by omega) x=0 := hz (r+1) q (by omega) (by omega)
    rw [hzero,map_zero,htop,map_zero,zero_add] at h
    have hs : (-1:ℤ)^r * (-1:ℤ)^r=1 := by
      rw [← pow_two,← pow_mul,Nat.mul_comm,pow_mul]
      norm_num
    have he := congrArg (fun a : (K.X r).X q => (-1:ℤ)^r • a) h
    simp only [zsmul_zero,smul_smul,hs,one_smul] at he
    exact he.symm

def topCycle (K : BC) (r q : ℕ) (z : (K.total c).cycles (r+q))
    (hz : SupportedThrough K (r+q) r ((K.total c).iCycles (r+q) z)) :
    (K.X r).cycles q :=
  cycleOf (K.X r) q _ (top_closed K r q z hz)

theorem topCycle_i (K : BC) (r q : ℕ) (z : (K.total c).cycles (r+q)) (hz) :
    (K.X r).iCycles q (topCycle K r q z hz) =
      proj K (r+q) r q rfl ((K.total c).iCycles (r+q) z) :=
  cycleOf_i _ _ _ _

set_option backward.isDefEq.respectTransparency false in
theorem remove_top_class (K : BC) (r q : ℕ) (z : (K.total c).cycles (r+q))
    (hz : SupportedThrough K (r+q) r ((K.total c).iCycles (r+q) z))
    (hc : (K.X r).homologyπ q (topCycle K r q z hz)=0) :
    ∃ w : (K.total c).cycles (r+q),
      (K.total c).homologyπ (r+q) z=(K.total c).homologyπ (r+q) w ∧
      ∀ p t (h : p+t=r+q), r≤p →
        proj K (r+q) p t h ((K.total c).iCycles (r+q) w)=0 := by
  obtain ⟨v,hv⟩ := (class_zero_iff (K.X r) q _).mp hc
  rw [topCycle_i] at hv
  let x := (K.total c).iCycles (r+q) z
  let y := K.ιTotal c r (q+1) (r+q+1) (by change r+(q+1)=r+q+1; omega) (((-1:ℤ)^r) • v)
  let x' := x-(K.total c).d (r+q+1) (r+q) y
  have hx' : (K.total c).d (r+q) (r+q-1) x'=0 := by
    change (K.total c).d (r+q) (r+q-1) (x-(K.total c).d (r+q+1) (r+q) y)=0
    rw [boundary_unchanged]
    exact cycle_closed _ _ z
  let w := cycleOf (K.total c) (r+q) x' hx'
  have hw : (K.total c).iCycles (r+q) w=x' := cycleOf_i _ _ _ _
  refine ⟨w,class_eq_of_boundary_diff _ _ z w y (by rw [hw]; change _ = x-(x-_); abel),?_⟩
  intro p t ht hp
  rw [hw]
  change proj K (r+q) p t ht (x-(K.total c).d (r+q+1) (r+q) y)=0
  rw [map_sub,diff_proj_apply]
  have hhor : proj K (r+q+1) (p+1) t (by omega) y=0 :=
    incl_coord_other K _ _ _ _ _ _ _ (by omega) _
  rw [hhor,map_zero,zero_add]
  by_cases he : p=r
  · subst p
    have ht' : t=q := by omega
    subst t
    have hver : proj K (r+q+1) r (q+1) (by omega) y = ((-1:ℤ)^r) • v :=
      incl_coord_same K _ _ _ _ _
    rw [hver,map_zsmul,hv,smul_smul]
    have hs : (-1:ℤ)^r * (-1:ℤ)^r=1 := by
      rw [← pow_two,← pow_mul,Nat.mul_comm,pow_mul]
      norm_num
    rw [hs,one_smul,sub_self]
  · have hver : proj K (r+q+1) p (t+1) (by omega) y=0 :=
      incl_coord_other K _ _ _ _ _ _ _ (Ne.symm he) _
    rw [hver,map_zero]
    change proj K (r+q) p t ht x - ((-1:ℤ)^p • (0 : (K.X p).X t))=0
    simp only [zsmul_zero,sub_zero]
    exact hz p t ht (by omega)

#print axioms top_closed
#print axioms remove_top_class
end CMDG.CondensedCM5R0.BreenDeligneFiniteColumnRemoval
