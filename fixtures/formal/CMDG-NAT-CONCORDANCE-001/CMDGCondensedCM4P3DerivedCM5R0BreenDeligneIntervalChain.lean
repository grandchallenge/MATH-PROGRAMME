import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneIntervalFill

/-! The interval filler commutes with the signed total differential. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology HomologicalComplex
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberAW
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
open CMDG.CondensedCM5R0.BreenDeligneInterval
open CMDG.CondensedCM5R0.BreenDeligneIntervalFill
namespace CMDG.CondensedCM5R0.BreenDeligneIntervalChain
variable {X Y : SimplicialObject ZMod} {f g : alt X ⟶ alt Y}

set_option backward.isDefEq.respectTransparency false in
theorem h_eval (H : Homotopy f g) (p q n : ℕ) (h : p+1+q=n+1)
    (t : I (d (p+1))) :
    inj X (d (p+1)) (d q) t ≫ (double (cylinderBi X)).ιTotal c (p+1) q (n+1) h ≫
      (double (cylinderBi X)).D₁ c (n+1) n ≫ fillDegree H n =
    ∑ i : Fin (p+2), (-1:ℤ)^i.val • part H p q n (by omega) (SimplexCategory.δ i ≫ t) := by
  rw [horizontal_succ_assoc _ p q (n+1) n h (by omega),hor_d,Preadditive.sum_comp,
    Preadditive.comp_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [Preadditive.zsmul_comp,Preadditive.comp_zsmul,inj_map_assoc,X.map_id,Category.id_comp,fill_summand]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem v_eval (H : Homotopy f g) (p q n : ℕ) (h : p+(q+1)=n+1)
    (t : I (d p)) :
    inj X (d p) (d (q+1)) t ≫ (double (cylinderBi X)).ιTotal c p (q+1) (n+1) h ≫
      (double (cylinderBi X)).D₂ c (n+1) n ≫ fillDegree H n =
    (-1:ℤ)^p • ((alt X).d (q+1) q ≫ part H p q n (by omega) t) := by
  rw [vertical_succ_assoc _ p q (n+1) n h (by omega),Preadditive.zsmul_comp,Preadditive.comp_zsmul,ver_d]
  rw [Preadditive.sum_comp,alternatingFaceMapComplex_obj_d]
  unfold AlternatingFaceMapComplex.objD
  congr 1
  rw [← Category.assoc,Preadditive.sum_comp,Preadditive.comp_sum,Preadditive.sum_comp]
  apply Finset.sum_congr rfl
  intro i _
  rw [Preadditive.zsmul_comp,Preadditive.comp_zsmul,inj_map_assoc]
  simp only [unop_id,Category.id_comp,Preadditive.zsmul_comp,Category.assoc,fill_summand]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem fill_comm (H : Homotopy f g) (n : ℕ) :
    (total (cylinderBi X)).d (n+1) n ≫ fillDegree H n =
      fillDegree H (n+1) ≫ (alt Y).d (n+1) n := by
  apply HomologicalComplex₂.total.hom_ext
  intro p q h
  change p+q=n+1 at h
  apply Sigma.hom_ext
  intro t
  change inj X (d p) (d q) t ≫ (double (cylinderBi X)).ιTotal c p q (n+1) h ≫
      ((double (cylinderBi X)).D₁ c (n+1) n + (double (cylinderBi X)).D₂ c (n+1) n) ≫ fillDegree H n =
    inj X (d p) (d q) t ≫ (double (cylinderBi X)).ιTotal c p q (n+1) h ≫
      fillDegree H (n+1) ≫ (alt Y).d (n+1) n
  rw [fill_summand_assoc,Preadditive.add_comp,Preadditive.comp_add,Preadditive.comp_add]
  cases p with
  | zero =>
    have hq : q=n+1 := by omega
    subst q
    rw [horizontal_axis_assoc,zero_comp,comp_zero,zero_add,v_eval,pow_zero,one_smul,part_zero,part_zero]
    split_ifs
    · exact (f.comm (n+1) n).symm
    · exact (g.comm (n+1) n).symm
  | succ p =>
    cases p with
    | zero =>
      have hq : q=n := by omega
      subst q
      rw [h_eval,Fin.sum_univ_two,part_one]
      simp only [Fin.val_zero,Fin.val_one,pow_zero,pow_one,one_smul,neg_smul,part_zero]
      rcases one_const_or_id t with ht | ht | ht
      · subst t
        simp only [face_zero_vertex,if_pos rfl,add_neg_cancel,if_neg (vertex_ne_id _),zero_comp,zero_add]
        cases n with
        | zero => rw [vertical_axis_assoc,zero_comp,comp_zero]
        | succ n => rw [v_eval,part_one,if_neg (vertex_ne_id _),comp_zero,smul_zero]
      · subst t
        simp only [face_zero_vertex,if_neg (by decide : (1:Fin 2)≠0),add_neg_cancel,if_neg (vertex_ne_id _),zero_comp,zero_add]
        cases n with
        | zero => rw [vertical_axis_assoc,zero_comp,comp_zero]
        | succ n => rw [v_eval,part_one,if_neg (vertex_ne_id _),comp_zero,smul_zero]
      · subst t
        simp only [face_zero_id,if_true,if_pos rfl,if_neg (by decide : (1:Fin 2)≠0)]
        cases n with
        | zero =>
          rw [vertical_axis_assoc,zero_comp,comp_zero,add_zero,Preadditive.neg_comp]
          have he := H.comm 0
          rw [Homotopy.dNext_zero_chainComplex,Homotopy.prevD_chainComplex,zero_add] at he
          change f.f 0 = _ ≫ _ + g.f 0 at he
          rw [he]
          abel
        | succ n =>
          rw [v_eval,part_one,if_pos rfl,pow_one,Preadditive.comp_neg,neg_smul,one_smul,neg_neg,Preadditive.neg_comp]
          have he := H.comm (n+1)
          rw [Homotopy.dNext_succ_chainComplex,Homotopy.prevD_chainComplex] at he
          rw [he]
          abel
    | succ p =>
      rw [part_high,zero_comp,h_eval]
      have hv : inj X (d (p+2)) (d q) t ≫
          (double (cylinderBi X)).ιTotal c (p+2) q (n+1) h ≫
          (double (cylinderBi X)).D₂ c (n+1) n ≫ fillDegree H n = 0 := by
        cases q with
        | zero => rw [vertical_axis_assoc,zero_comp,comp_zero]
        | succ q => rw [v_eval,part_high,comp_zero,smul_zero]
      rw [hv,add_zero]
      cases p with
      | zero =>
        have hn : n=q+1 := by omega
        subst n
        rw [Fin.sum_univ_three]
        have hpart (u : I (d 1)) : part H 1 q (q+1) (by omega) u =
            (if u=𝟙 (SimplexCategory.mk 1) then -H.hom q (q+1) else 0) := part_one H q u
        rw [hpart,hpart,hpart]
        simp only [Fin.val_zero,Fin.val_one,Fin.val_two,pow_zero,pow_one,one_smul,neg_smul]
        have he := face_two_coeff t
        split_ifs at he ⊢ <;> (try norm_num at he) <;> (try norm_num) <;> (try omega) <;> (try abel)
      | succ p =>
        simp only [part_high,smul_zero,Finset.sum_const_zero]

#print axioms h_eval
#print axioms v_eval
#print axioms fill_comm
end CMDG.CondensedCM5R0.BreenDeligneIntervalChain
