import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneTotalCoordinates
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat

/-! Remove the highest nonzero column of a total chain by an actual
boundary, when its boundary is supported in the first column. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
open CMDG.CondensedCM5R0.BreenDeligneTotalCoordinates
namespace CMDG.CondensedCM5R0.BreenDeligneColumnElimination

theorem fill_cycle (L : Ch) (q : ℕ) (h : IsZero (L.homology q))
    (z : L.X q) (hz : L.d q (q-1) z=0) :
    ∃ y : L.X (q+1), L.d (q+1) q y=z := by
  have he := (L.exactAt_iff_isZero_homology q).mpr h
  have hs : (L.sc' (q+1) q (q-1)).Exact :=
    (L.exactAt_iff' (q+1) q (q-1) (c.prev_eq' (show c.Rel (q+1) q by rfl))
      (show c.next q=q-1 by
        cases q with
        | zero => exact c.next_eq_self' 0 (fun k hk => by change k+1=0 at hk; omega)
        | succ q => exact c.next_eq' (show c.Rel (q+1) q by rfl))).mp he
  exact (ShortComplex.moduleCat_exact_iff _).mp hs z hz

theorem incl_coord_same (K : BC) (n p q : ℕ) (h : p+q=n) (x : (K.X p).X q) :
    proj K n p q h (K.ιTotal c p q n h x)=x :=
  CategoryTheory.congr_fun (incl_proj_same K n p q h) x

theorem incl_coord_other (K : BC) (n p q a b : ℕ) (h : p+q=n) (hab : a+b=n)
    (ha : a≠p) (x : (K.X a).X b) :
    proj K n p q h (K.ιTotal c a b n hab x)=0 :=
  CategoryTheory.congr_fun (incl_proj_other K n p q a b h hab ha) x

theorem top_cycle (K : BC) (r q : ℕ) (hr : 2≤r)
    (x : (K.total c).X (r+q))
    (hx : SupportedThrough K (r+q) r x)
    (hd : SupportedThrough K (r+q-1) 1 ((K.total c).d (r+q) (r+q-1) x)) :
    (K.X r).d q (q-1) (proj K (r+q) r q rfl x)=0 := by
  cases q with
  | zero =>
    rw [(K.X r).shape 0 0 (by decide)]
    rfl
  | succ q =>
    -- use the equality of degree indices without transporting the chain
    change (K.X r).d (q+1) q (proj K (r+q+1) r (q+1) (by omega) x)=0
    have he : proj K (r+q) r q rfl ((K.total c).d (r+q+1) (r+q) x)=0 := by
      have h' : r+(q+1)-1=r+q := by omega
      exact hd r q (by omega) (by omega)
    have hf := diff_proj_apply K (r+q) r q rfl x
    have hzero : proj K (r+q+1) (r+1) q (by omega) x=0 :=
      hx (r+1) q (by omega) (by omega)
    rw [he,hzero,map_zero,zero_add] at hf
    have hs : (-1 : ℤ)^r * (-1 : ℤ)^r = 1 := by
      rw [← pow_two,← pow_mul,Nat.mul_comm,pow_mul]
      norm_num
    have hf' := congrArg (fun z : (K.X r).X q => (-1 : ℤ)^r • z) hf
    simp only [zsmul_zero,smul_smul,hs,one_smul] at hf'
    exact hf'.symm

set_option backward.isDefEq.respectTransparency false in
theorem remove_top (K : BC) (r q : ℕ) (hr : 2≤r)
    (x : (K.total c).X (r+q))
    (hx : SupportedThrough K (r+q) r x)
    (hd : SupportedThrough K (r+q-1) 1 ((K.total c).d (r+q) (r+q-1) x))
    (hc : IsZero ((K.X r).homology q)) :
    ∃ y : (K.total c).X (r+q+1),
      SupportedThrough K (r+q) (r-1) (x - (K.total c).d (r+q+1) (r+q) y) := by
  obtain ⟨w,hw⟩ := fill_cycle (K.X r) q hc _ (top_cycle K r q hr x hx hd)
  let y := K.ιTotal c r (q+1) (r+q+1) (by change r+(q+1)=r+q+1; omega) (((-1 : ℤ)^r) • w)
  refine ⟨y,?_⟩
  intro p t ht hp
  rw [map_sub,diff_proj_apply K (r+q) p t ht]
  have hpr : r≤p := by omega
  have hh : proj K (r+q+1) (p+1) t (by omega) y=0 :=
    incl_coord_other K _ _ _ _ _ _ _ (by omega) _
  rw [hh,map_zero,zero_add]
  by_cases he : p=r
  · subst p
    have ht' : t=q := by omega
    subst t
    have hv : proj K (r+q+1) r (q+1) (by omega) y = ((-1 : ℤ)^r) • w :=
      incl_coord_same K _ _ _ _ _
    rw [hv,map_zsmul,hw,smul_smul]
    have hs : (-1 : ℤ)^r * (-1 : ℤ)^r = 1 := by
      rw [← pow_two,← pow_mul,Nat.mul_comm,pow_mul]
      norm_num
    rw [hs,one_smul,sub_self]
  · have hv : proj K (r+q+1) p (t+1) (by omega) y=0 :=
      incl_coord_other K _ _ _ _ _ _ _ (Ne.symm he) _
    rw [hv,map_zero]
    change proj K (r+q) p t ht x - ((-1 : ℤ)^p • (0 : (K.X p).X t))=0
    simp only [zsmul_zero,sub_zero]
    exact hx p t ht (by omega)

theorem boundary_unchanged (K : BC) (n : ℕ) (x : (K.total c).X n)
    (y : (K.total c).X (n+1)) :
    (K.total c).d n (n-1) (x-(K.total c).d (n+1) n y) =
      (K.total c).d n (n-1) x := by
  rw [map_sub]
  have hz : (K.total c).d n (n-1) ((K.total c).d (n+1) n y)=0 :=
    CategoryTheory.congr_fun ((K.total c).d_comp_d (n+1) n (n-1)) y
  rw [hz,sub_zero]

theorem reduce_support (K : BC) (n r : ℕ) (hr : r≤n)
    (x : (K.total c).X n) (hx : SupportedThrough K n r x)
    (hd : SupportedThrough K (n-1) 1 ((K.total c).d n (n-1) x))
    (hc : ∀ p q : ℕ, p+q=n → 2≤p → IsZero ((K.X p).homology q)) :
    ∃ y : (K.total c).X (n+1),
      SupportedThrough K n 1 (x - (K.total c).d (n+1) n y) := by
  induction r generalizing x with
  | zero =>
    refine ⟨0,?_⟩
    rw [map_zero,sub_zero]
    intro p q h hp
    exact hx p q h (by omega)
  | succ r ih =>
    by_cases hr' : r=0
    · subst r
      refine ⟨0,?_⟩
      rw [map_zero,sub_zero]
      exact hx
    · obtain ⟨q,hq⟩ : ∃ q, r+1+q=n := ⟨n-(r+1),by omega⟩
      subst n
      obtain ⟨y,hy⟩ := remove_top K (r+1) q (by omega) x hx hd (hc (r+1) q rfl (by omega))
      let x' := x - (K.total c).d (r+1+q+1) (r+1+q) y
      have hx' : SupportedThrough K (r+1+q) r x' := hy
      have hd' : SupportedThrough K (r+1+q-1) 1 ((K.total c).d (r+1+q) (r+1+q-1) x') := by
        change SupportedThrough K (r+1+q-1) 1
          ((K.total c).d (r+1+q) (r+1+q-1) (x-(K.total c).d (r+1+q+1) (r+1+q) y))
        rw [boundary_unchanged]
        exact hd
      obtain ⟨z,hz⟩ := ih (by omega) x' hx' hd'
      refine ⟨y+z,?_⟩
      rw [map_add,← sub_sub]
      exact hz

theorem reduce_to_first (K : BC) (n : ℕ) (x : (K.total c).X n)
    (hd : SupportedThrough K (n-1) 1 ((K.total c).d n (n-1) x))
    (hc : ∀ p q : ℕ, p+q=n → 2≤p → IsZero ((K.X p).homology q)) :
    ∃ y : (K.total c).X (n+1),
      SupportedThrough K n 1 (x - (K.total c).d (n+1) n y) :=
  reduce_support K n n (le_refl _) x (supported_all K n x) hd hc

#print axioms fill_cycle
#print axioms top_cycle
#print axioms remove_top
#print axioms reduce_to_first
end CMDG.CondensedCM5R0.BreenDeligneColumnElimination
