import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneReducedNext
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneHomologyElements

/-! Degree shift for the actual horizontal-single total, including its
negative differential, and the full stable suspension isomorphism. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneFirstColumnInclusion
open CMDG.CondensedCM5R0.BreenDeligneReducedNext
open CMDG.CondensedCM5R0.BreenDeligneHomologyElements
open CMDG.CondensedCM5R0.BreenDeligneTotalCoordinates
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
namespace CMDG.CondensedCM5R0.BreenDeligneSuspensionDegree

abbrev S (V : Ch) : BC := (HomologicalComplex.single Ch c 1).obj V
abbrev SV (V : Ch) : Ch := (S V).total c

def selfIso (V : Ch) : (S V).X 1 ≅ V :=
  HomologicalComplex.singleObjXSelf c 1 V

theorem offZero (V : Ch) (p q : ℕ) (hp : p≠1) : IsZero (((S V).X p).X q) :=
  (HomologicalComplex.eval ZMod c q).map_isZero
    (HomologicalComplex.isZero_single_obj_X c 1 V p hp)

def incl (V : Ch) (q : ℕ) : V.X q ⟶ (SV V).X (q+1) :=
  (selfIso V).inv.f q ≫ (S V).ιTotal c 1 q (q+1) (by change 1+q=q+1; omega)

def prj (V : Ch) (q : ℕ) : (SV V).X (q+1) ⟶ V.X q :=
  proj (S V) (q+1) 1 q (by omega) ≫ (selfIso V).hom.f q

set_option backward.isDefEq.respectTransparency false in
def termIso (V : Ch) (q : ℕ) : V.X q ≅ (SV V).X (q+1) where
  hom := incl V q
  inv := prj V q
  hom_inv_id := by
    unfold incl prj
    rw [Category.assoc,incl_proj_same_assoc]
    exact congrArg (fun k => k.f q) (selfIso V).inv_hom_id
  inv_hom_id := by
    apply HomologicalComplex₂.total.hom_ext
    intro p r h
    change p+r=q+1 at h
    by_cases hp : p=1
    · subst p
      have hr : r=q := by omega
      subst r
      unfold incl prj
      rw [← Category.assoc,incl_proj_same_assoc]
      rw [← Category.assoc ((selfIso V).hom.f q) ((selfIso V).inv.f q)]
      have he := congrArg (fun k => k.f q) (selfIso V).hom_inv_id
      change (selfIso V).hom.f q ≫ (selfIso V).inv.f q = 𝟙 _ at he
      rw [he,Category.id_comp,Category.comp_id]
    · exact (offZero V p r hp).eq_of_src _ _

set_option backward.isDefEq.respectTransparency false in
theorem incl_diff (V : Ch) (q : ℕ) :
    incl V (q+1) ≫ (SV V).d (q+2) (q+1) =
      -(V.d (q+1) q ≫ incl V q) := by
  unfold incl
  rw [Category.assoc]
  change _ ≫ (S V).ιTotal c 1 (q+1) (q+2) _ ≫
    ((S V).D₁ c (q+2) (q+1) + (S V).D₂ c (q+2) (q+1)) = _
  rw [Preadditive.comp_add,horizontal_succ _ 0 (q+1) (q+2) (q+1) _ (by omega),
    vertical_succ _ 1 q (q+2) (q+1) _ (by omega)]
  have he : ((S V).d 1 0).f (q+1)=0 :=
    (offZero V 0 (q+1) (by decide)).eq_of_tgt _ _
  rw [he,zero_comp,zero_add,pow_one,neg_smul,one_smul,Preadditive.comp_neg,
    ← Category.assoc,(selfIso V).inv.comm,Category.assoc]

def negIso {A B : ZMod} (e : A ≅ B) : A ≅ B where
  hom := -e.hom
  inv := -e.inv
  hom_inv_id := by rw [Preadditive.neg_comp,Preadditive.comp_neg,neg_neg,e.hom_inv_id]
  inv_hom_id := by rw [Preadditive.neg_comp,Preadditive.comp_neg,neg_neg,e.inv_hom_id]

set_option backward.isDefEq.respectTransparency false in
def suspensionScIso (V : Ch) (q : ℕ) :
    V.sc' (q+2) (q+1) q ≅ (SV V).sc' (q+3) (q+2) (q+1) :=
  ShortComplex.isoMk (negIso (termIso V (q+2))) (termIso V (q+1)) (negIso (termIso V q))
    (by
      change (-incl V (q+2)) ≫ (SV V).d (q+3) (q+2) = V.d (q+2) (q+1) ≫ incl V (q+1)
      rw [Preadditive.neg_comp,incl_diff,neg_neg])
    (by
      change incl V (q+1) ≫ (SV V).d (q+2) (q+1) = V.d (q+1) q ≫ (-incl V q)
      rw [incl_diff,Preadditive.comp_neg])

def suspensionHomologyIso (V : Ch) (q : ℕ) : V.homology (q+1) ≅ (SV V).homology (q+2) :=
  V.homologyIsoSc' (q+2) (q+1) q (prev_degree _) (next_degree _) ≪≫
    ShortComplex.homologyMapIso (suspensionScIso V q) ≪≫
    ((SV V).homologyIsoSc' (q+3) (q+2) (q+1) (prev_degree _) (next_degree _)).symm

def stableSuspension (A : AGrp) (n k : ℕ) (hk : k<n) :
    (reducedChainsZ A n).homology (n+k) ≅ (reducedChainsZ A (n+1)).homology (n+k+1) := by
  have hp : n+k>0 := by omega
  let q := n+k-1
  have hq : n+k=q+1 := by dsimp [q]; omega
  refine eqToIso (congrArg (fun i : ℕ => (reducedChainsZ A n).homology i) hq) ≪≫
    suspensionHomologyIso (reducedChainsZ A n) q ≪≫ ?_
  change (suspendedReduced A n).homology (q+2) ≅ _
  exact fullSuspensionIso A n (q+2) (by omega) ≪≫
    eqToIso (congrArg (fun i : ℕ => (reducedChainsZ A (n+1)).homology i) (by omega : q+2=n+k+1))

#print axioms suspensionHomologyIso
#print axioms stableSuspension
end CMDG.CondensedCM5R0.BreenDeligneSuspensionDegree
