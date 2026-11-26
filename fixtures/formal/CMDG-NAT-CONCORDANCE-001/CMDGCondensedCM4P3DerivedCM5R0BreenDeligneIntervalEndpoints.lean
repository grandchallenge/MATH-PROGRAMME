import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneIntervalChain

/-! The interval filler composed with Alexander–Whitney has the exact
prescribed endpoint chain maps. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology HomologicalComplex
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberAW
open CMDG.CondensedCM5R0.BreenDeligneInterval
open CMDG.CondensedCM5R0.BreenDeligneIntervalFill
open CMDG.CondensedCM5R0.BreenDeligneIntervalChain
namespace CMDG.CondensedCM5R0.BreenDeligneIntervalEndpoints
variable {X Y : SimplicialObject ZMod} {f g : alt X ⟶ alt Y}

def fill (H : Homotopy f g) : total (cylinderBi X) ⟶ alt Y :=
  ChainComplex.ofHom (fillDegree H) (fun n => (fill_comm H n).symm)

def diagFill (H : Homotopy f g) : alt (cyl X) ⟶ alt Y :=
  aw (cylinderBi X) ≫ fill H

set_option backward.isDefEq.respectTransparency false in
theorem endpoint_term (H : Homotopy f g) (v : Fin 2) (n : ℕ) (i : Fin (n+1)) :
    (endpoint X v).app (d n) ≫ awTerm (cylinderBi X) n i ≫ fillDegree H n =
      X.map (SimplexCategory.subinterval i.val (n-i.val)
        (by omega : i.val+(n-i.val)≤n)).op ≫
        part H i.val (n-i.val) n (by omega) (vertex (d i.val) v) := by
  unfold endpoint awTerm
  dsimp only [NatTrans.app]
  rw [Category.assoc,inj_map_assoc,vertex_comp,fill_summand]

set_option backward.isDefEq.respectTransparency false in
theorem endpoint_term_zero (H : Homotopy f g) (v : Fin 2) (n : ℕ) :
    (endpoint X v).app (d n) ≫ awTerm (cylinderBi X) n 0 ≫ fillDegree H n =
      if v=0 then f.f n else g.f n := by
  rw [endpoint_term]
  have he : SimplexCategory.subinterval 0 n (by omega : 0+n≤n) =
      𝟙 (SimplexCategory.mk n) := by
    apply SimplexCategory.Hom.ext
    apply OrderHom.ext
    funext j
    apply Fin.ext
    rfl
  simp only [Fin.val_zero,Nat.sub_zero,part_zero,firstValue,vertex]
  rw [show (SimplexCategory.subinterval 0 n (by omega : 0+n≤n)).op =
    𝟙 (d n) by rw [he]; rfl,X.map_id,Category.id_comp]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem endpoint_term_other (H : Homotopy f g) (v : Fin 2) (n : ℕ) (i : Fin (n+1)) (hi : i ≠ 0) :
    (endpoint X v).app (d n) ≫ awTerm (cylinderBi X) n i ≫ fillDegree H n = 0 := by
  rw [endpoint_term]
  have hp : i.val ≠ 0 := by
    intro he
    apply hi
    exact Fin.ext he
  have he (p q k : ℕ) (h : p+q=k) (hp : p≠0) :
      part H p q k h (vertex (d p) v) = 0 := by
    cases p with
    | zero => contradiction
    | succ p =>
      cases p with
      | zero =>
        have hk : k=q+1 := by omega
        subst k
        simp [part,vertex_ne_id]
      | succ p => rw [part_high]
  rw [he _ _ _ _ hp,comp_zero]


set_option backward.isDefEq.respectTransparency false in
theorem endpoint_fill (H : Homotopy f g) (v : Fin 2) :
    (alternatingFaceMapComplex ZMod).map (endpoint X v) ≫ diagFill H =
      if v=0 then f else g := by
  apply HomologicalComplex.Hom.ext
  funext n
  change (endpoint X v).app (d n) ≫ awDegree (cylinderBi X) n ≫ fillDegree H n = _
  unfold awDegree
  rw [Preadditive.sum_comp,Preadditive.comp_sum,Finset.sum_eq_single (0 : Fin (n+1))]
  · rw [endpoint_term_zero]
    split_ifs <;> rfl
  · intro i _ hi
    exact endpoint_term_other H v n i hi
  · simp

#print axioms fill
#print axioms endpoint_fill
end CMDG.CondensedCM5R0.BreenDeligneIntervalEndpoints
