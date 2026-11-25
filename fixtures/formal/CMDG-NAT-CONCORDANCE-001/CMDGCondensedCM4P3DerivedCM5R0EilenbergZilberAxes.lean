import CMDGCondensedCM4P3DerivedCM5R0EilenbergZilberZero

/-! The signed shuffle differential law on both boundary axes. -/
noncomputable section
open CategoryTheory Opposite AlgebraicTopology
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberAW
open CMDG.CondensedCM5R0.EilenbergZilberZero
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
namespace CMDG.CondensedCM5R0.EilenbergZilberAxes

def horizontalPath (p : ℕ) : Path p 0 :=
  ⟨(OrderHom.id,OrderHom.const _ 0),by intro i; simp⟩

def verticalPath (q : ℕ) : Path 0 q :=
  ⟨(OrderHom.const _ 0, {toFun := fun i => ⟨i.val,by omega⟩, monotone' := fun i j h => h}),
    by intro i; change 0+i.val=i.val; omega⟩

theorem horizontalPath_unique (p : ℕ) (u : Path p 0) : u = horizontalPath p := by
  apply Subtype.ext
  apply Prod.ext
  · apply OrderHom.ext
    funext i
    apply Fin.ext
    have h := u.property i
    have hv := (u.val.2 i).isLt
    change _ < 1 at hv
    change (u.val.1 i).val = i.val
    omega
  · apply OrderHom.ext
    funext i
    apply Fin.ext
    have hv := (u.val.2 i).isLt
    change _ < 1 at hv
    change (u.val.2 i).val = 0
    omega

theorem verticalPath_unique (q : ℕ) (u : Path 0 q) : u = verticalPath q := by
  apply Subtype.ext
  apply Prod.ext
  · apply OrderHom.ext
    funext i
    apply Fin.ext
    have hv := (u.val.1 i).isLt
    change _ < 1 at hv
    change (u.val.1 i).val = 0
    omega
  · apply OrderHom.ext
    funext i
    apply Fin.ext
    have h := u.property i
    have hv := (u.val.1 i).isLt
    change _ < 1 at hv
    change (u.val.2 i).val = i.val
    omega

theorem horizontalPath_sign (p : ℕ) : pathSign (horizontalPath p) = 1 := by
  unfold pathSign
  have h : (∑ i : Fin (p+0), if (horizontalPath p).val.1 i.castSucc <
      (horizontalPath p).val.1 i.succ then ((horizontalPath p).val.2 i.castSucc).val else 0) = 0 := by
    apply Finset.sum_eq_zero
    intro i _
    split_ifs <;> rfl
  rw [h,pow_zero]

theorem verticalPath_sign (q : ℕ) : pathSign (verticalPath q) = 1 := by
  unfold pathSign
  have h : (∑ i : Fin (0+q), if (verticalPath q).val.1 i.castSucc <
      (verticalPath q).val.1 i.succ then ((verticalPath q).val.2 i.castSucc).val else 0) = 0 := by
    apply Finset.sum_eq_zero
    intro i _
    change (if (0 : Fin 1) < 0 then _ else 0) = 0
    simp
  rw [h,pow_zero]

def constZero (n : ℕ) : SimplexCategory.mk n ⟶ SimplexCategory.mk 0 :=
  SimplexCategory.const _ _ 0

set_option backward.isDefEq.respectTransparency false in
theorem shufflePart_horizontal (B : Bi) (p : ℕ) :
    shufflePart B p 0 = B.map ((𝟙 (d p)) ×ₘ (constZero p).op) := by
  unfold shufflePart
  rw [Finset.sum_eq_single (horizontalPath p),horizontalPath_sign,one_smul]
  · rfl
  · intro u _ h
    exact (h (horizontalPath_unique p u)).elim
  · simp

set_option backward.isDefEq.respectTransparency false in
theorem shufflePart_vertical (B : Bi) (q : ℕ) :
    shufflePart B 0 q = B.map ((constZero (0+q)).op ×ₘ (SimplexCategory.mkHom (verticalPath q).val.2).op) := by
  unfold shufflePart
  rw [Finset.sum_eq_single (verticalPath q),verticalPath_sign,one_smul]
  · -- the arithmetic transport 0+q=q is supplied separately below
    rfl
  · intro u _ h
    exact (h (verticalPath_unique q u)).elim
  · simp

set_option backward.isDefEq.respectTransparency false in
theorem shuffleDegree_on (B : Bi) (p q n : ℕ) (h : p+q=n) :
    (double B).ιTotal c p q n h ≫ shuffleDegree B n =
      shufflePart B p q ≫ eqToHom (by rw [h]) := by
  subst n
  simpa using shuffleDegree_summand B p q

set_option backward.isDefEq.respectTransparency false in
theorem shuffleDegree_horizontal (B : Bi) (p : ℕ) :
    (double B).ιTotal c p 0 p rfl ≫ shuffleDegree B p =
      B.map ((𝟙 (d p)) ×ₘ (constZero p).op) := by
  exact (shuffleDegree_summand B p 0).trans (shufflePart_horizontal B p)

def castOrdinal (m n : ℕ) (h : m=n) : SimplexCategory.mk m ⟶ SimplexCategory.mk n :=
  SimplexCategory.mkHom {toFun := fun i => ⟨i.val,by omega⟩, monotone' := fun i j hij => hij}

theorem castOrdinal_eq (m n : ℕ) (h : m=n) :
    (castOrdinal m n h).op = eqToHom (congrArg d h).symm := by
  subst n
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem transportAxis (B : Bi) (m n : ℕ) (h : m=n) :
    B.map ((constZero m).op ×ₘ (castOrdinal m n h).op) ≫
      eqToHom (by rw [h] : (diagChains B).X m = (diagChains B).X n) =
    B.map ((constZero n).op ×ₘ 𝟙 (d n)) := by
  subst n
  change B.map ((constZero m).op ×ₘ (castOrdinal m m rfl).op) ≫ 𝟙 _ = _
  rw [Category.comp_id,castOrdinal_eq]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem shuffleDegree_vertical (B : Bi) (q : ℕ) :
    (double B).ιTotal c 0 q q (Nat.zero_add q) ≫ shuffleDegree B q =
      B.map ((constZero q).op ×ₘ 𝟙 (d q)) := by
  rw [shuffleDegree_on,shufflePart_vertical]
  exact transportAxis B (0+q) q (Nat.zero_add q)

theorem constZero_face (n : ℕ) (i : Fin (n+2)) :
    SimplexCategory.δ i ≫ constZero (n+1) = constZero n := by
  apply SimplexCategory.Hom.ext
  apply OrderHom.ext
  funext j
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem horizontal_chain (B : Bi) (n : ℕ) :
    (double B).ιTotal c (n+1) 0 (n+1) rfl ≫
      shuffleDegree B (n+1) ≫ (diagChains B).d (n+1) n =
    (double B).ιTotal c (n+1) 0 (n+1) rfl ≫
      (total B).d (n+1) n ≫ shuffleDegree B n := by
  rw [← Category.assoc,shuffleDegree_horizontal]
  change _ = (double B).ιTotal c (n+1) 0 (n+1) rfl ≫
    ((double B).D₁ c (n+1) n + (double B).D₂ c (n+1) n) ≫ shuffleDegree B n
  rw [← Category.assoc ( (double B).ιTotal c (n+1) 0 (n+1) rfl),
    Preadditive.comp_add,horizontal_succ (double B) n 0 (n+1) n rfl rfl,vertical_axis,add_zero,
    Category.assoc,shuffleDegree_horizontal,diag_d,hor_d,Preadditive.comp_sum,Preadditive.sum_comp]
  apply Finset.sum_congr rfl
  intro i _
  rw [Preadditive.comp_zsmul,Preadditive.zsmul_comp]
  congr 1
  rw [← B.map_comp,← B.map_comp]
  apply congrArg B.map
  apply CategoryTheory.Prod.hom_ext
  · simp
  · change (constZero (n+1)).op ≫ (SimplexCategory.δ i).op =
      𝟙 (d 0) ≫ (constZero n).op
    rw [Category.id_comp,← op_comp,constZero_face]

set_option backward.isDefEq.respectTransparency false in
theorem vertical_chain (B : Bi) (n : ℕ) :
    (double B).ιTotal c 0 (n+1) (n+1) (Nat.zero_add _) ≫
      shuffleDegree B (n+1) ≫ (diagChains B).d (n+1) n =
    (double B).ιTotal c 0 (n+1) (n+1) (Nat.zero_add _) ≫
      (total B).d (n+1) n ≫ shuffleDegree B n := by
  rw [← Category.assoc,shuffleDegree_vertical]
  change _ = (double B).ιTotal c 0 (n+1) (n+1) (Nat.zero_add _) ≫
    ((double B).D₁ c (n+1) n + (double B).D₂ c (n+1) n) ≫ shuffleDegree B n
  rw [← Category.assoc ( (double B).ιTotal c 0 (n+1) (n+1) (Nat.zero_add _)),
    Preadditive.comp_add,horizontal_axis,vertical_succ _ 0 n _ _ (Nat.zero_add _) (Nat.zero_add _),
    zero_add,pow_zero,one_smul,Category.assoc,shuffleDegree_vertical,diag_d,ver_d,
    Preadditive.comp_sum,Preadditive.sum_comp]
  apply Finset.sum_congr rfl
  intro i _
  rw [Preadditive.comp_zsmul,Preadditive.zsmul_comp]
  congr 1
  rw [← B.map_comp,← B.map_comp]
  apply congrArg B.map
  apply CategoryTheory.Prod.hom_ext
  · change (constZero (n+1)).op ≫ (SimplexCategory.δ i).op =
      𝟙 (d 0) ≫ (constZero n).op
    rw [Category.id_comp,← op_comp,constZero_face]
  · simp

set_option backward.isDefEq.respectTransparency false in
theorem shuffle_comm_one (B : Bi) :
    shuffleDegree B 1 ≫ (diagChains B).d 1 0 =
    (total B).d 1 0 ≫ shuffleDegree B 0 := by
  apply HomologicalComplex₂.total.hom_ext
  intro p q h
  change p+q=1 at h
  by_cases hp : p=0
  · have hq : q=1 := by omega
    subst p
    subst q
    exact vertical_chain B 0
  · have hp' : p=1 := by omega
    have hq : q=0 := by omega
    subst p
    subst q
    exact horizontal_chain B 0

#print axioms shufflePart_horizontal
#print axioms shufflePart_vertical
#print axioms shuffleDegree_vertical
#print axioms horizontal_chain
#print axioms vertical_chain
#print axioms shuffle_comm_one
end CMDG.CondensedCM5R0.EilenbergZilberAxes
