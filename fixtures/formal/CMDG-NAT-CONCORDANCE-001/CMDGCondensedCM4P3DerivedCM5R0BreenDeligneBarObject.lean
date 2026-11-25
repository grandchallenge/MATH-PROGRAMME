import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneBarTupleQuotient
import Mathlib.Algebra.BigOperators.Fin

/-! The actual additive group bar object, in edge coordinates.
Every ordinal map pulls back vertex potentials and takes adjacent
differences. Composition is telescoping, not an assumed simplicial identity. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBarTupleQuotient
namespace CMDG.CondensedCM5R0.BreenDeligneBarObject

def edges {A : Type} [AddCommGroup A] {n : ℕ} (v : Fin (n+1) → A) : Fin n → A :=
  fun i => v i.succ - v i.castSucc

theorem edges_partialSum {A : Type} [AddCommGroup A] {n : ℕ} (x : Fin n → A) :
    edges (Fin.partialSum x) = x := by
  funext i
  unfold edges
  rw [Fin.partialSum_succ]
  abel

theorem partialSum_edges {A : Type} [AddCommGroup A] {n : ℕ} (v : Fin (n+1) → A) (i : Fin (n+1)) :
    Fin.partialSum (edges v) i = v i - v 0 := by
  induction i using Fin.inductionOn with
  | zero => simp
  | succ i hi =>
    rw [Fin.partialSum_succ, hi]
    unfold edges
    abel

theorem partialSum_hom {A B : Type} [AddCommGroup A] [AddCommGroup B]
    (f : A →+ B) {n : ℕ} (x : Fin n → A) (i : Fin (n+1)) :
    Fin.partialSum (fun j => f (x j)) i = f (Fin.partialSum x i) := by
  induction i using Fin.inductionOn with
  | zero => simp
  | succ i hi => rw [Fin.partialSum_succ, Fin.partialSum_succ, hi, map_add]

theorem partialSum_add {A : Type} [AddCommGroup A] {n : ℕ} (x y : Fin n → A) (i : Fin (n+1)) :
    Fin.partialSum (x+y) i = Fin.partialSum x i + Fin.partialSum y i := by
  induction i using Fin.inductionOn with
  | zero => simp
  | succ i hi =>
    rw [Fin.partialSum_succ, Fin.partialSum_succ, Fin.partialSum_succ, hi]
    change _ + (x i + y i) = _
    abel

theorem partialSum_zero {A : Type} [AddCommGroup A] {n : ℕ} (i : Fin (n+1)) :
    Fin.partialSum (0 : Fin n → A) i = 0 := by
  induction i using Fin.inductionOn with
  | zero => simp
  | succ i hi => rw [Fin.partialSum_succ,hi]; simp

abbrev barTerm (A : AGrp) (Δ : SimplexCategoryᵒᵖ) : AGrp :=
  AddCommGrpCat.of (Tuples A Δ.unop.len)

def barMap (A : AGrp) {Δ Δ' : SimplexCategoryᵒᵖ} (f : Δ ⟶ Δ') :
    barTerm A Δ ⟶ barTerm A Δ' :=
  AddCommGrpCat.ofHom {
    toFun x := edges (Fin.partialSum x ∘ f.unop.toOrderHom)
    map_zero' := by
      funext i
      unfold edges Function.comp
      rw [partialSum_zero,partialSum_zero,sub_self]
      rfl
    map_add' x y := by
      funext i
      unfold edges Function.comp
      rw [partialSum_add,partialSum_add]
      change (Fin.partialSum x (f.unop.toOrderHom i.succ) +
          Fin.partialSum y (f.unop.toOrderHom i.succ)) -
        (Fin.partialSum x (f.unop.toOrderHom i.castSucc) +
          Fin.partialSum y (f.unop.toOrderHom i.castSucc)) =
        (Fin.partialSum x (f.unop.toOrderHom i.succ) - Fin.partialSum x (f.unop.toOrderHom i.castSucc)) +
        (Fin.partialSum y (f.unop.toOrderHom i.succ) - Fin.partialSum y (f.unop.toOrderHom i.castSucc))
      abel }

def bar (A : AGrp) : SimplicialObject AGrp where
  obj := barTerm A
  map := barMap A
  map_id Δ := by
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    change edges (Fin.partialSum x) i = x i
    exact congrFun (edges_partialSum x) i
  map_comp {Δ Δ' Δ''} f g := by
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    change edges (Fin.partialSum x ∘ (g.unop ≫ f.unop).toOrderHom) i =
      edges (Fin.partialSum (edges (Fin.partialSum x ∘ f.unop.toOrderHom)) ∘ g.unop.toOrderHom) i
    -- The intermediate base vertex cancels from both endpoint potentials.
    change Fin.partialSum x (f.unop.toOrderHom (g.unop.toOrderHom i.succ)) -
      Fin.partialSum x (f.unop.toOrderHom (g.unop.toOrderHom i.castSucc)) =
      Fin.partialSum (edges (Fin.partialSum x ∘ f.unop.toOrderHom)) (g.unop.toOrderHom i.succ) -
      Fin.partialSum (edges (Fin.partialSum x ∘ f.unop.toOrderHom)) (g.unop.toOrderHom i.castSucc)
    rw [partialSum_edges,partialSum_edges]
    simp only [Function.comp_apply]
    abel

set_option backward.isDefEq.respectTransparency false in
def barNat {A B : AGrp} (f : A ⟶ B) : bar A ⟶ bar B where
  app Δ := AddCommGrpCat.ofHom {
    toFun x i := f (x i)
    map_zero' := by funext i; exact map_zero f.hom
    map_add' x y := by funext i; exact map_add f.hom (x i) (y i) }
  naturality {Δ Δ'} g := by
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    change f (edges (Fin.partialSum x ∘ g.unop.toOrderHom) i) =
      edges (Fin.partialSum (fun j => f (x j)) ∘ g.unop.toOrderHom) i
    unfold edges Function.comp
    have h (j : Fin (Δ.unop.len+1)) :=
      partialSum_hom f.hom (show Fin Δ.unop.len → A from x) j
    rw [h,h]
    exact map_sub f.hom _ _

def barFunctor : AGrp ⥤ SimplicialObject AGrp where
  obj := bar
  map := barNat
  map_id A := by ext Δ x; rfl
  map_comp f g := by ext Δ x; rfl

/-- The actual i-th degeneracy has a zero i-th edge. -/
theorem barDegeneracy_zero (A : AGrp) (p : ℕ) (i : Fin (p+1))
    (x : Tuples A p) : ((bar A).σ i x) i = 0 := by
  change edges (Fin.partialSum x ∘ i.predAboveOrderHom) i = 0
  unfold edges Function.comp
  change Fin.partialSum x (i.predAbove i.succ) -
    Fin.partialSum x (i.predAbove i.castSucc) = 0
  rw [Fin.predAbove_succ_self,Fin.predAbove_castSucc_self,sub_self]

theorem barDegeneracy_other (A : AGrp) (p : ℕ) (i : Fin (p+1))
    (x : Tuples A p) (j : Fin p) :
    ((bar A).σ i x) (i.succAbove j) = x j := by
  change Fin.partialSum x (i.predAbove (i.succAbove j).succ) -
    Fin.partialSum x (i.predAbove (i.succAbove j).castSucc) = x j
  have h₀ : i.predAbove (i.succAbove j).castSucc = j.castSucc := by
    by_cases h : j.castSucc < i
    · rw [Fin.succAbove_of_castSucc_lt _ _ h, Fin.predAbove_castSucc_of_le _ _ h.le]
    · rw [Fin.succAbove_of_le_castSucc _ _ (le_of_not_gt h),
        Fin.predAbove_castSucc_of_lt _ _ (lt_of_le_of_lt (le_of_not_gt h) (Fin.castSucc_lt_succ))]
      ext
      simp
  have h₁ : i.predAbove (i.succAbove j).succ = j.succ := by
    by_cases h : j.castSucc < i
    · rw [Fin.succAbove_of_castSucc_lt _ _ h, Fin.predAbove_succ_of_lt _ _ h]
      ext
      simp
    · rw [Fin.succAbove_of_le_castSucc _ _ (le_of_not_gt h),
        Fin.predAbove_succ_of_le _ _ (le_trans (le_of_not_gt h) (Fin.castSucc_le_succ j))]
  rw [h₀,h₁,Fin.partialSum_succ]
  abel

theorem barDegeneracy_insert (A : AGrp) (p : ℕ) (i : Fin (p+1)) (x : Tuples A p) :
    (bar A).σ i x = i.insertNth 0 x := by
  funext j
  refine Fin.succAboveCases i ?_ (fun k => ?_) j
  · rw [barDegeneracy_zero,Fin.insertNth_apply_same]
  · rw [barDegeneracy_other,Fin.insertNth_apply_succAbove]

/-- Exact equality between the actual degeneracy-generated subgroup
and the kernel of the normalized bar quotient. -/
def actualDegenerateSubgroup (A : AGrp) (p : ℕ) : AddSubgroup (Raw A (p+1)) :=
  AddSubgroup.closure {z | ∃ (i : Fin (p+1)) (x : Tuples A p),
    z = FreeAbelianGroup.of ((bar A).σ i x)}

theorem actualDegenerate_eq (A : AGrp) (p : ℕ) :
    actualDegenerateSubgroup A p = degenerateSubgroup A (p+1) := by
  unfold actualDegenerateSubgroup degenerateSubgroup
  congr 1
  ext z
  constructor
  · rintro ⟨i,x,rfl⟩
    exact ⟨_,⟨i,barDegeneracy_zero A p i x⟩,rfl⟩
  · rintro ⟨x,h,rfl⟩
    obtain ⟨i,y,hy⟩ := (degenerate_iff_insert A p x).mp h
    refine ⟨i,y,?_⟩
    rw [barDegeneracy_insert,← hy]; rfl

theorem actualBarQuotient_ker (A : AGrp) (p : ℕ) :
    (quotientMap A (p+1)).ker = actualDegenerateSubgroup A p := by
  rw [quotient_ker,actualDegenerate_eq]

#print axioms bar
#print axioms barFunctor
#print axioms barDegeneracy_zero
#print axioms barDegeneracy_insert
#print axioms actualBarQuotient_ker
end CMDG.CondensedCM5R0.BreenDeligneBarObject
