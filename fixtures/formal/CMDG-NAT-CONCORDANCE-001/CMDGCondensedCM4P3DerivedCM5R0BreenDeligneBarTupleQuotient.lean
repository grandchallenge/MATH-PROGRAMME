import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneReducedBasis
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneTensorSupport
import Mathlib.Data.Fin.Tuple.Basic

/-! Horizontal normalized bar terms: quotient by exactly the
zero-insertion degeneracies, and pointwise tensor basis. -/
noncomputable section
open scoped TensorProduct
open CategoryTheory CategoryTheory.Limits CategoryTheory.MonoidalCategory Module
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneReducedBasis
open CMDG.CondensedCM5R0.BreenDeligneAdditiveBoundary
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
namespace CMDG.CondensedCM5R0.BreenDeligneBarTupleQuotient

abbrev Tuples (A : AGrp) (p : ℕ) := Fin p → A
abbrev Good (A : AGrp) (p : ℕ) := {x : Tuples A p // ∀ i, x i ≠ 0}
abbrev Raw (A : AGrp) (p : ℕ) := FreeAbelianGroup (Tuples A p)
abbrev Smash (A : AGrp) (p : ℕ) := FreeAbelianGroup (Good A p)

def quotientGen (A : AGrp) (p : ℕ) (x : Tuples A p) : Smash A p := by
  classical
  exact if h : ∀ i, x i ≠ 0 then FreeAbelianGroup.of ⟨x,h⟩ else 0

def quotientMap (A : AGrp) (p : ℕ) : Raw A p →+ Smash A p :=
  FreeAbelianGroup.lift (quotientGen A p)

def sectionMap (A : AGrp) (p : ℕ) : Smash A p →+ Raw A p :=
  FreeAbelianGroup.map Subtype.val

theorem quotient_section (A : AGrp) (p : ℕ) :
    (quotientMap A p).comp (sectionMap A p) = AddMonoidHom.id _ := by
  apply FreeAbelianGroup.lift_ext
  intro x
  simp [quotientMap, sectionMap, quotientGen, x.property, FreeAbelianGroup.map_of_apply]

def degenerateSubgroup (A : AGrp) (p : ℕ) : AddSubgroup (Raw A p) :=
  AddSubgroup.closure {z | ∃ x : Tuples A p, (∃ i, x i = 0) ∧ z = FreeAbelianGroup.of x}

theorem degenerate_iff_insert (A : AGrp) (p : ℕ) (x : Tuples A (p+1)) :
    (∃ i, x i = 0) ↔ ∃ (i : Fin (p+1)) (y : Tuples A p), x = i.insertNth 0 y := by
  constructor
  · rintro ⟨i,hi⟩
    refine ⟨i,i.removeNth x,?_⟩
    rw [← hi, Fin.insertNth_self_removeNth]
  · rintro ⟨i,y,rfl⟩
    exact ⟨i,by simp⟩

theorem degenerate_le_ker (A : AGrp) (p : ℕ) :
    degenerateSubgroup A p ≤ (quotientMap A p).ker := by
  apply (AddSubgroup.closure_le _).2
  rintro z ⟨x,⟨i,hi⟩,rfl⟩
  have h : ¬ ∀ j, x j ≠ 0 := fun h => h i hi
  change quotientMap A p (FreeAbelianGroup.of x) = 0
  simp [quotientMap, quotientGen,h]

/-- Every element differs from its canonical nondegenerate representative
by a sum of degenerate generators. -/
theorem difference_mem_degenerate (A : AGrp) (p : ℕ) (z : Raw A p) :
    z - sectionMap A p (quotientMap A p z) ∈ degenerateSubgroup A p := by
  classical
  let D := degenerateSubgroup A p
  let f : Raw A p →+ Raw A p := AddMonoidHom.id _ - (sectionMap A p).comp (quotientMap A p)
  change f z ∈ D
  induction z using FreeAbelianGroup.induction_on with
  | zero => rw [map_zero]; exact D.zero_mem
  | of x =>
    change FreeAbelianGroup.of x - sectionMap A p (quotientMap A p (FreeAbelianGroup.of x)) ∈ D
    rw [quotientMap, FreeAbelianGroup.lift_apply_of]
    by_cases h : ∀ i, x i ≠ 0
    · simp [quotientGen,h,sectionMap,FreeAbelianGroup.map_of_apply]
    · have hz : ∃ i, x i = 0 := by push Not at h; exact h
      simp only [quotientGen,dif_neg h,map_zero,sub_zero]
      exact AddSubgroup.subset_closure ⟨x,hz,rfl⟩
  | neg x hx =>
    rw [map_neg]; exact D.neg_mem hx
  | add x y hx hy =>
    rw [map_add]; exact D.add_mem hx hy

theorem quotient_ker (A : AGrp) (p : ℕ) :
    (quotientMap A p).ker = degenerateSubgroup A p := by
  apply le_antisymm
  · intro z hz
    have h := difference_mem_degenerate A p z
    change quotientMap A p z = 0 at hz
    simpa only [hz,map_zero,sub_zero] using h
  · exact degenerate_le_ker A p

theorem quotient_surjective (A : AGrp) (p : ℕ) :
    Function.Surjective (quotientMap A p) := by
  intro z
  exact ⟨sectionMap A p z, congrArg (fun f : Smash A p →+ Smash A p => f z) (quotient_section A p)⟩

def pointTensor (A : AGrp) : ℕ → ZMod
  | 0 => ModuleCat.of ℤ ℤ
  | p+1 => ModuleCat.of ℤ (reducedFree.obj A) ⊗ pointTensor A p

def pointTensorBasis (A : AGrp) : (p : ℕ) → Basis (Fin p → NZ A) ℤ (pointTensor A p)
  | 0 => Basis.singleton _ _
  | p+1 => ((reducedBasis A).tensorProduct (pointTensorBasis A p)).reindex (Fin.consEquiv (fun _ => NZ A))

def smashTensorIso (A : AGrp) (p : ℕ) : Smash A p ≃ₗ[ℤ] pointTensor A p :=
  (FreeAbelianGroup.basis (Good A p)).equiv (pointTensorBasis A p) (Equiv.subtypePiEquivPi (β := fun _ : Fin p => A) (p := fun _ x => x ≠ 0))

theorem freeBasis_generator (T : Type) (x : T) :
    FreeAbelianGroup.basis T x = FreeAbelianGroup.of x := by
  apply (FreeAbelianGroup.basis T).repr.injective
  rw [Basis.repr_self]
  change Finsupp.single x 1 = FreeAbelianGroup.toFinsupp (FreeAbelianGroup.of x)
  simp

theorem reducedBasis_generator (A : AGrp) (x : NZ A) :
    reducedBasis A x = reducedGenerator A x.val := by
  rw [reducedBasis, Basis.map_apply, freeBasis_generator]
  change FreeAbelianGroup.lift (fun z : NZ A => reducedGenerator A z.val)
    (FreeAbelianGroup.of x) = _
  exact FreeAbelianGroup.lift_apply_of _ _

def pureTuple (A : AGrp) : (p : ℕ) → Tuples A p → pointTensor A p
  | 0, _ => (1 : ℤ)
  | p+1, x => reducedGenerator A (x 0) ⊗ₜ[ℤ] pureTuple A p (Fin.tail x)

theorem pureTuple_degenerate (A : AGrp) (p : ℕ) (x : Tuples A p)
    (h : ∃ i, x i = 0) : pureTuple A p x = 0 := by
  induction p with
  | zero => obtain ⟨i,_⟩ := h; exact Fin.elim0 i
  | succ p hp =>
    obtain ⟨i,hi⟩ := h
    refine Fin.cases ?_ (fun j => ?_) i hi
    · intro h0
      change reducedGenerator A (x 0) ⊗ₜ[ℤ] pureTuple A p (Fin.tail x) = 0
      rw [h0, generator_zero, TensorProduct.zero_tmul]
    · intro hj
      change reducedGenerator A (x 0) ⊗ₜ[ℤ] pureTuple A p (Fin.tail x) = 0
      rw [hp (Fin.tail x) ⟨j,hj⟩, TensorProduct.tmul_zero]

theorem pointBasis_pure (A : AGrp) (p : ℕ) (x : Fin p → NZ A) :
    pointTensorBasis A p x = pureTuple A p (fun i => (x i).val) := by
  induction p with
  | zero => exact Basis.singleton_apply (Fin 0 → NZ A) ℤ x
  | succ p hp =>
    change (((reducedBasis A).tensorProduct (pointTensorBasis A p)).reindex
      (Fin.consEquiv (fun _ => NZ A))) x = _
    rw [Basis.reindex_apply, Basis.tensorProduct_apply']
    change reducedBasis A (x 0) ⊗ₜ[ℤ] pointTensorBasis A p (Fin.tail x) = _
    rw [reducedBasis_generator, hp]
    rfl

/-- The tensor comparison sends the actual quotient generator to the
ordered tensor of reduced generators, including degenerate tuples. -/
theorem smashTensor_generator (A : AGrp) (p : ℕ) (x : Tuples A p) :
    smashTensorIso A p (quotientGen A p x) = pureTuple A p x := by
  classical
  by_cases h : ∀ i, x i ≠ 0
  · rw [quotientGen, dif_pos h]
    unfold smashTensorIso
    rw [← freeBasis_generator, Basis.equiv_apply, pointBasis_pure]
    rfl
  · rw [quotientGen, dif_neg h, map_zero]
    apply (pureTuple_degenerate A p x _).symm
    push Not at h
    exact h

def tupleMap {A B : AGrp} (f : A ⟶ B) (p : ℕ) (x : Tuples A p) : Tuples B p :=
  fun i => f (x i)

def smashMap {A B : AGrp} (f : A ⟶ B) (p : ℕ) : Smash A p →+ Smash B p :=
  FreeAbelianGroup.lift (fun x : Good A p => quotientGen B p (tupleMap f p x.val))

theorem smashMap_generator {A B : AGrp} (f : A ⟶ B) (p : ℕ) (x : Tuples A p) :
    smashMap f p (quotientGen A p x) = quotientGen B p (tupleMap f p x) := by
  classical
  by_cases h : ∀ i, x i ≠ 0
  · rw [quotientGen, dif_pos h, smashMap, FreeAbelianGroup.lift_apply_of]
  · have hb : ¬ ∀ i, tupleMap f p x i ≠ 0 := by
      intro hb
      apply h
      intro i hi
      apply hb i
      change f (x i) = 0
      rw [hi]
      exact map_zero f.hom
    rw [quotientGen, dif_neg h, map_zero, quotientGen, dif_neg hb]

def pointTensorMap {A B : AGrp} (f : A ⟶ B) : (p : ℕ) → pointTensor A p ⟶ pointTensor B p
  | 0 => 𝟙 _
  | p+1 => toZModule.map (reducedFree.map f) ⊗ₘ pointTensorMap f p

theorem pointTensorMap_pure {A B : AGrp} (f : A ⟶ B) (p : ℕ) (x : Tuples A p) :
    pointTensorMap f p (pureTuple A p x) = pureTuple B p (tupleMap f p x) := by
  induction p with
  | zero => rfl
  | succ p hp =>
    change (toZModule.map (reducedFree.map f) ⊗ₘ pointTensorMap f p)
      (reducedGenerator A (x 0) ⊗ₜ[ℤ] pureTuple A p (Fin.tail x)) = _
    have ht := ModuleCat.MonoidalCategory.tensorHom_tmul
      (toZModule.map (reducedFree.map f)) (pointTensorMap f p)
      (reducedGenerator A (x 0)) (pureTuple A p (Fin.tail x))
    rw [ht]
    change reducedFree.map f (reducedGenerator A (x 0)) ⊗ₜ[ℤ]
      pointTensorMap f p (pureTuple A p (Fin.tail x)) = _
    rw [generator_natural, hp]
    rfl

/-- The actual pointwise comparison commutes with all group maps,
in particular the vertical faces and degeneracies. -/
theorem smashTensor_natural {A B : AGrp} (f : A ⟶ B) (p : ℕ) (z : Smash A p) :
    smashTensorIso B p (smashMap f p z) = pointTensorMap f p (smashTensorIso A p z) := by
  induction z using FreeAbelianGroup.induction_on with
  | zero => simp
  | of x =>
    have h : quotientGen A p x.val = FreeAbelianGroup.of x := by
      simp [quotientGen,x.property]
    rw [← h, smashMap_generator, smashTensor_generator, smashTensor_generator, pointTensorMap_pure]
  | neg x hx => simp only [map_neg, hx]
  | add x y hx hy => simp only [map_add, hx, hy]

def smashFunctor (p : ℕ) : AGrp ⥤ ZMod where
  obj A := ModuleCat.of ℤ (Smash A p)
  map f := ModuleCat.ofHom (smashMap f p).toIntLinearMap
  map_id A := by
    apply ModuleCat.hom_ext
    apply LinearMap.toAddMonoidHom_injective
    apply FreeAbelianGroup.lift_ext
    intro x
    change smashMap (𝟙 A) p (FreeAbelianGroup.of x) = FreeAbelianGroup.of x
    rw [smashMap, FreeAbelianGroup.lift_apply_of]
    have h : tupleMap (𝟙 A) p x.val = x.val := rfl
    rw [h]
    simp [quotientGen,x.property]
  map_comp {A B C} f g := by
    apply ModuleCat.hom_ext
    apply LinearMap.toAddMonoidHom_injective
    apply FreeAbelianGroup.lift_ext
    intro x
    change smashMap (f ≫ g) p (FreeAbelianGroup.of x) =
      smashMap g p (smashMap f p (FreeAbelianGroup.of x))
    have hx : quotientGen A p x.val = FreeAbelianGroup.of x := by simp [quotientGen,x.property]
    rw [← hx, smashMap_generator, smashMap_generator, smashMap_generator]
    rfl

set_option backward.isDefEq.respectTransparency false in
def pointTensorFunctor (p : ℕ) : AGrp ⥤ ZMod where
  obj A := pointTensor A p
  map f := pointTensorMap f p
  map_id A := by
    ext x
    obtain ⟨z,rfl⟩ := (smashTensorIso A p).surjective x
    rw [← smashTensor_natural]
    have h := CategoryTheory.congr_fun ((smashFunctor p).map_id A) z
    change smashMap (𝟙 A) p z = z at h
    rw [h]
    rfl
  map_comp {A B C} f g := by
    ext x
    obtain ⟨z,rfl⟩ := (smashTensorIso A p).surjective x
    change pointTensorMap (f ≫ g) p (smashTensorIso A p z) =
      pointTensorMap g p (pointTensorMap f p (smashTensorIso A p z))
    rw [← smashTensor_natural, ← smashTensor_natural, ← smashTensor_natural]
    have h := CategoryTheory.congr_fun ((smashFunctor p).map_comp f g) z
    change smashMap (f ≫ g) p z = smashMap g p (smashMap f p z) at h
    rw [h]

set_option backward.isDefEq.respectTransparency false in
def smashNatIso (p : ℕ) : smashFunctor p ≅ pointTensorFunctor p :=
  NatIso.ofComponents (fun A => (smashTensorIso A p).toModuleIso) (fun {A B} f => by
    ext x
    exact smashTensor_natural f p x)

def verticalSmashChains (X : SimplicialObject AGrp) (p : ℕ) : Ch :=
  (AlgebraicTopology.alternatingFaceMapComplex ZMod).obj (X ⋙ smashFunctor p)

def verticalPointTensorChains (X : SimplicialObject AGrp) (p : ℕ) : Ch :=
  (AlgebraicTopology.alternatingFaceMapComplex ZMod).obj (X ⋙ pointTensorFunctor p)

/-- This compares the true degreewise normalized tuple quotient and
pointwise tensor chains, not yet the total tensor complex. -/
def verticalSmashIso (X : SimplicialObject AGrp) (p : ℕ) :
    verticalSmashChains X p ≅ verticalPointTensorChains X p :=
  (AlgebraicTopology.alternatingFaceMapComplex ZMod).mapIso
    (Functor.isoWhiskerLeft X (smashNatIso p))

set_option backward.isDefEq.respectTransparency false in
def pointTensorOneIso : pointTensorFunctor 1 ≅ reducedFree ⋙ toZModule :=
  NatIso.ofComponents (fun A => ρ_ (toZModule.obj (reducedFree.obj A))) (fun {A B} f => by
    change (toZModule.map (reducedFree.map f) ⊗ₘ 𝟙 (𝟙_ ZMod)) ≫
        (ρ_ (toZModule.obj (reducedFree.obj B))).hom =
      (ρ_ (toZModule.obj (reducedFree.obj A))).hom ≫ toZModule.map (reducedFree.map f)
    simpa only [tensorHom_id] using rightUnitor_naturality (toZModule.map (reducedFree.map f)))

/-- The length-one column is exactly the original reduced chain complex,
via the unit constraint and additive change of category. -/
def firstColumnIso (A : AGrp) (n : ℕ) :
    verticalSmashChains ((EilenbergMacLaneModel.em n).obj A) 1 ≅ reducedChainsZ A n := by
  let X := (EilenbergMacLaneModel.em n).obj A
  refine verticalSmashIso X 1 ≪≫
    (AlgebraicTopology.alternatingFaceMapComplex ZMod).mapIso
      (Functor.isoWhiskerLeft X pointTensorOneIso) ≪≫ ?_
  apply eqToIso
  let Y := X ⋙ reducedFree
  have h := congrArg (fun F => F.obj Y)
    (AlgebraicTopology.map_alternatingFaceMapComplex toZModule)
  exact h.symm

#print axioms degenerate_iff_insert
#print axioms quotient_ker
#print axioms quotient_surjective
#print axioms smashTensorIso
#print axioms smashTensor_generator
#print axioms smashTensor_natural
#print axioms verticalSmashIso
#print axioms firstColumnIso
end CMDG.CondensedCM5R0.BreenDeligneBarTupleQuotient
