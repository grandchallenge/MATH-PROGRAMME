import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneColumnPower

/-! Explicit coordinates of first-quadrant total chains. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
namespace CMDG.CondensedCM5R0.BreenDeligneTotalCoordinates

def proj (K : BC) (n p q : ℕ) (h : p+q=n) :
    (K.total c).X n ⟶ (K.X p).X q :=
  K.totalDesc (fun a b hab => if ha : a=p then eqToHom (by
    change a+b=n at hab
    have hb : b=q := by omega
    subst a
    subst b
    rfl) else 0)

set_option backward.isDefEq.respectTransparency false in
@[reassoc]
theorem incl_proj_same (K : BC) (n p q : ℕ) (h : p+q=n) :
    K.ιTotal c p q n h ≫ proj K n p q h = 𝟙 _ := by
  unfold proj
  rw [HomologicalComplex₂.ι_totalDesc,dif_pos rfl]
  rfl

set_option backward.isDefEq.respectTransparency false in
@[reassoc]
theorem incl_proj_other (K : BC) (n p q a b : ℕ) (h : p+q=n) (hab : a+b=n) (ha : a≠p) :
    K.ιTotal c a b n hab ≫ proj K n p q h = 0 := by
  unfold proj
  rw [HomologicalComplex₂.ι_totalDesc,dif_neg ha]

def term (K : BC) (n : ℕ) (i : Fin (n+1)) : (K.total c).X n ⟶ (K.total c).X n :=
  proj K n i.val (n-i.val) (by omega) ≫ K.ιTotal c i.val (n-i.val) n (by
    change i.val+(n-i.val)=n
    omega)

set_option backward.isDefEq.respectTransparency false in
theorem sum_term (K : BC) (n : ℕ) :
    ∑ i : Fin (n+1), term K n i = 𝟙 _ := by
  apply HomologicalComplex₂.total.hom_ext
  intro p q h
  change p+q=n at h
  rw [Preadditive.comp_sum,Category.comp_id]
  let a : Fin (n+1) := ⟨p,by omega⟩
  rw [Finset.sum_eq_single a]
  · have he : n-p=q := by omega
    unfold term
    change K.ιTotal c p q n h ≫ proj K n p (n-p) _ ≫ K.ιTotal c p (n-p) n _ = _
    subst n
    have hh (r : ℕ) (hr : p+r=p+q) :
        K.ιTotal c p q (p+q) rfl ≫ proj K (p+q) p r hr ≫ K.ιTotal c p r (p+q) hr =
          K.ιTotal c p q (p+q) rfl := by
      have he' : r=q := by omega
      subst r
      rw [incl_proj_same_assoc]
    exact hh (p+q-p) (by omega)
  · intro i _ hi
    have hp : p≠i.val := by
      intro he
      apply hi
      exact Fin.ext he.symm
    unfold term
    rw [incl_proj_other_assoc K n i.val (n-i.val) p q (by omega) h hp,zero_comp]
  · intro ha; exact (ha (Finset.mem_univ a)).elim

theorem sum_elements (K : BC) (n : ℕ) (x : (K.total c).X n) :
    ∑ i : Fin (n+1), term K n i x = x := by
  have h := CategoryTheory.congr_fun (sum_term K n) x
  let E : ((K.total c).X n ⟶ (K.total c).X n) →+ (K.total c).X n :=
    { toFun := fun f => f x, map_zero' := rfl, map_add' := by intros; rfl }
  change E (∑ i : Fin (n+1), term K n i) = x at h
  rw [map_sum] at h
  exact h

theorem coord_ext (K : BC) (n : ℕ) (x y : (K.total c).X n)
    (h : ∀ (p q : ℕ) (hpq : p+q=n), proj K n p q hpq x = proj K n p q hpq y) : x=y := by
  rw [← sum_elements K n x,← sum_elements K n y]
  apply Finset.sum_congr rfl
  intro i _
  change K.ιTotal c i.val (n-i.val) n _ (proj K n i.val (n-i.val) _ x) =
    K.ιTotal c i.val (n-i.val) n _ (proj K n i.val (n-i.val) _ y)
  rw [h]

def SupportedThrough (K : BC) (n r : ℕ) (x : (K.total c).X n) : Prop :=
  ∀ (p q : ℕ) (h : p+q=n), r<p → proj K n p q h x=0

theorem supported_all (K : BC) (n : ℕ) (x : (K.total c).X n) :
    SupportedThrough K n n x := by
  intro p q h hp
  omega

set_option backward.isDefEq.respectTransparency false in
theorem D1_proj (K : BC) (n p q : ℕ) (h : p+q=n) :
    K.D₁ c (n+1) n ≫ proj K n p q h =
      proj K (n+1) (p+1) q (by omega) ≫ (K.d (p+1) p).f q := by
  apply HomologicalComplex₂.total.hom_ext
  intro a b hab
  change a+b=n+1 at hab
  rw [← Category.assoc]
  cases a with
  | zero =>
    rw [horizontal_axis,zero_comp,incl_proj_other_assoc K (n+1) (p+1) q 0 b (by omega) hab (by omega),zero_comp]
  | succ a =>
    rw [horizontal_succ K a b (n+1) n hab (by omega),Category.assoc]
    by_cases ha : a=p
    · subst a
      have hb : b=q := by omega
      subst b
      rw [incl_proj_same,Category.comp_id,incl_proj_same_assoc]
    · rw [incl_proj_other K n p q a b h (by omega) ha,comp_zero,
        incl_proj_other_assoc K (n+1) (p+1) q (a+1) b (by omega) hab (by omega),zero_comp]

set_option backward.isDefEq.respectTransparency false in
theorem D2_proj (K : BC) (n p q : ℕ) (h : p+q=n) :
    K.D₂ c (n+1) n ≫ proj K n p q h =
      (-1 : ℤ)^p • (proj K (n+1) p (q+1) (by omega) ≫ (K.X p).d (q+1) q) := by
  apply HomologicalComplex₂.total.hom_ext
  intro a b hab
  change a+b=n+1 at hab
  rw [Preadditive.comp_zsmul,← Category.assoc]
  cases b with
  | zero =>
    rw [vertical_axis,zero_comp,incl_proj_other_assoc K (n+1) p (q+1) a 0 (by omega) hab (by omega),
      zero_comp,smul_zero]
  | succ b =>
    rw [vertical_succ K a b (n+1) n hab (by omega),Preadditive.zsmul_comp,Category.assoc]
    by_cases ha : a=p
    · subst a
      have hb : b=q := by omega
      subst b
      rw [incl_proj_same,Category.comp_id,incl_proj_same_assoc]
    · rw [incl_proj_other K n p q a b h (by omega) ha,comp_zero,smul_zero,
        incl_proj_other_assoc K (n+1) p (q+1) a (b+1) (by omega) hab ha,zero_comp,smul_zero]

set_option backward.isDefEq.respectTransparency false in
theorem diff_proj (K : BC) (n p q : ℕ) (h : p+q=n) :
    (K.total c).d (n+1) n ≫ proj K n p q h =
      proj K (n+1) (p+1) q (by omega) ≫ (K.d (p+1) p).f q +
      (-1 : ℤ)^p • (proj K (n+1) p (q+1) (by omega) ≫ (K.X p).d (q+1) q) := by
  change (K.D₁ c (n+1) n + K.D₂ c (n+1) n) ≫ _ = _
  rw [Preadditive.add_comp,D1_proj,D2_proj]

theorem diff_proj_apply (K : BC) (n p q : ℕ) (h : p+q=n) (x : (K.total c).X (n+1)) :
    proj K n p q h ((K.total c).d (n+1) n x) =
      (K.d (p+1) p).f q (proj K (n+1) (p+1) q (by omega) x) +
      (-1 : ℤ)^p • ((K.X p).d (q+1) q (proj K (n+1) p (q+1) (by omega) x)) :=
  CategoryTheory.congr_fun (diff_proj K n p q h) x

#print axioms sum_term
#print axioms coord_ext
#print axioms diff_proj_apply
end CMDG.CondensedCM5R0.BreenDeligneTotalCoordinates
