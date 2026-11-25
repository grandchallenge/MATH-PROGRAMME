import Mathlib.AlgebraicTopology.DoldKan.FunctorGamma
import Mathlib.AlgebraicTopology.AlternatingFaceMapComplex
import Mathlib.Algebra.Category.Grp.Adjunctions
import Mathlib.Algebra.Category.Grp.Abelian
import Mathlib.Algebra.Homology.Single
import Mathlib.Algebra.Category.Grp.Biproducts
import Mathlib.LinearAlgebra.StdBasis
import Mathlib.CategoryTheory.Whiskering
import Mathlib.CategoryTheory.Adjunction.Whiskering
import Mathlib.CategoryTheory.Limits.FunctorCategory.EpiMono
import Mathlib.CategoryTheory.Preadditive.Projective.Basic
import Mathlib.Algebra.Category.Grp.EpiMono

/-! The actual Dold-Kan Eilenberg-MacLane model on abelian groups.
This constructs the reduced integral chain functor and proves the
low-degree support constraint. It is not the stable homology theorem. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite
open AlgebraicTopology AlgebraicTopology.DoldKan
namespace CMDG.CondensedCM5R0.EilenbergMacLaneModel

abbrev Ab := AddCommGrpCat.{0}
def singleDegree (n : ℕ) : Ab ⥤ ChainComplex Ab ℕ :=
  HomologicalComplex.single Ab (ComplexShape.down ℕ) n

def em (n : ℕ) : Ab ⥤ SimplicialObject Ab :=
  singleDegree n ⋙ Γ₀

abbrev Indices (m : ℕ) :=
  SimplicialObject.Splitting.IndexSet (op (SimplexCategory.mk m))

abbrev Active (n m : ℕ) := {i : Indices m // i.1.unop.len = n}

def summandIso (A : Ab) (n m : ℕ) (i : Active n m) :
    Γ₀.Obj.summand ((singleDegree n).obj A)
      (op (SimplexCategory.mk m)) i.val ≅ A :=
  HomologicalComplex.singleObjXIsoOfEq (ComplexShape.down ℕ) n A _ i.property

/-- Each actual simplex object is a finite coproduct of copies of A,
indexed by surjections [m]→[n], with zero summands removed. -/
def emTermIso (A : Ab) (n m : ℕ) :
    ((em n).obj A).obj (op (SimplexCategory.mk m)) ≅
      (∐ fun _ : Active n m => A) := by
  classical
  change (∐ fun i : Indices m => Γ₀.Obj.summand
    ((singleDegree n).obj A) (op (SimplexCategory.mk m)) i) ≅ _
  let B := fun i : Indices m => Γ₀.Obj.summand
    ((singleDegree n).obj A) (op (SimplexCategory.mk m)) i
  refine {
    hom := Sigma.desc (fun i => if hi : i.1.unop.len = n then
      (summandIso A n m ⟨i,hi⟩).hom ≫
        Sigma.ι (fun _ : Active n m => A) ⟨i,hi⟩ else 0)
    inv := Sigma.desc (fun i => (summandIso A n m i).inv ≫ Sigma.ι B i.val)
    hom_inv_id := ?_
    inv_hom_id := ?_ }
  · apply Sigma.hom_ext
    intro i
    by_cases hi : i.1.unop.len = n
    · simp [B, hi, Category.assoc]
    · have hz : IsZero (B i) :=
        HomologicalComplex.isZero_single_obj_X (ComplexShape.down ℕ) n A _ hi
      exact hz.eq_of_src _ _
  · apply Sigma.hom_ext
    intro i
    have hi := i.property
    simp [B, hi, Category.assoc]

def emDegree (n m : ℕ) : Ab ⥤ Ab :=
  em n ⋙ (evaluation SimplexCategoryᵒᵖ Ab).obj (op (SimplexCategory.mk m))

def activePower (n m : ℕ) : Ab ⥤ Ab where
  obj A := ∐ fun _ : Active n m => A
  map f := Limits.Sigma.map (fun _ => f)
  map_id _A := Limits.Sigma.map_id
  map_comp f g := (Limits.Sigma.map_comp_map (fun _ => f) (fun _ => g)).symm

set_option backward.isDefEq.respectTransparency false in
private theorem splitting_inj_eq (K : ChainComplex Ab ℕ)
    (m : ℕ) (i : Indices m) :
    ((Γ₀.splitting K).cofan (op (SimplexCategory.mk m))).inj i =
      Sigma.ι (Γ₀.Obj.summand K (op (SimplexCategory.mk m))) i := by
  change Sigma.ι (Γ₀.Obj.summand K i.1) (SimplicialObject.Splitting.IndexSet.id i.1) ≫
    Γ₀.Obj.map K i.e.op = _
  letI : Mono (𝟙 i.1.unop) := inferInstance
  rw [Γ₀.Obj.map_on_summand₀ K (SimplicialObject.Splitting.IndexSet.id i.1)
    (show i.e ≫ 𝟙 _ = i.e.op.unop ≫ 𝟙 _ by rfl),
    Γ₀.Obj.Termwise.mapMono_id]
  change 𝟙 (Γ₀.Obj.summand K (op (SimplexCategory.mk m)) i) ≫
      Sigma.ι (Γ₀.Obj.summand K (op (SimplexCategory.mk m))) i = _
  exact Category.id_comp _

private theorem emMap_inj {A B : Ab} (f : A ⟶ B) (n m : ℕ) (i : Indices m) :
    Sigma.ι (Γ₀.Obj.summand ((singleDegree n).obj A) (op (SimplexCategory.mk m))) i ≫
      (emDegree n m).map f =
    ((singleDegree n).map f).f i.1.unop.len ≫
      Sigma.ι (Γ₀.Obj.summand ((singleDegree n).obj B) (op (SimplexCategory.mk m))) i := by
  change _ ≫ (Γ₀.map ((singleDegree n).map f)).app (op (SimplexCategory.mk m)) = _
  rw [← splitting_inj_eq, ← splitting_inj_eq]
  exact (Γ₀.splitting ((singleDegree n).obj A)).ι_desc _ _ i

private theorem singleIso_inv_naturality {A B : Ab} (f : A ⟶ B)
    (n k : ℕ) (hk : k = n) :
    f ≫ (HomologicalComplex.singleObjXIsoOfEq (ComplexShape.down ℕ) n B k hk).inv =
      (HomologicalComplex.singleObjXIsoOfEq (ComplexShape.down ℕ) n A k hk).inv ≫
        ((singleDegree n).map f).f k := by
  subst k
  change _ = _ ≫ ((HomologicalComplex.single Ab (ComplexShape.down ℕ) n).map f).f n
  rw [HomologicalComplex.single_map_f_self]
  simp [HomologicalComplex.singleObjXSelf]

set_option backward.isDefEq.respectTransparency false in
/-- The finite simplex decomposition commutes with every homomorphism of groups. -/
def emDegreeIso (n m : ℕ) : activePower n m ≅ emDegree n m :=
  NatIso.ofComponents (fun A => (emTermIso A n m).symm) (fun {A B} f => by
    apply Sigma.hom_ext
    intro i
    change Sigma.ι (fun _ : Active n m => A) i ≫
      Limits.Sigma.map (fun _ : Active n m => f) ≫ (emTermIso B n m).inv =
        Sigma.ι (fun _ : Active n m => A) i ≫
          (emTermIso A n m).inv ≫ (emDegree n m).map f
    rw [Limits.Sigma.ι_map_assoc]
    have ha : Sigma.ι (fun _ : Active n m => A) i ≫ (emTermIso A n m).inv =
        (summandIso A n m i).inv ≫
          Sigma.ι (Γ₀.Obj.summand ((singleDegree n).obj A) (op (SimplexCategory.mk m))) i.val := by
      unfold emTermIso
      exact Sigma.ι_desc _ _
    have hb : Sigma.ι (fun _ : Active n m => B) i ≫ (emTermIso B n m).inv =
        (summandIso B n m i).inv ≫
          Sigma.ι (Γ₀.Obj.summand ((singleDegree n).obj B) (op (SimplexCategory.mk m))) i.val := by
      unfold emTermIso
      exact Sigma.ι_desc _ _
    rw [hb, ← Category.assoc (Sigma.ι (fun _ : Active n m => A) i), ha,
      Category.assoc, emMap_inj, ← Category.assoc, ← Category.assoc]
    exact congrArg (fun x => x ≫ Sigma.ι
      (Γ₀.Obj.summand ((singleDegree n).obj B) (op (SimplexCategory.mk m))) i.val)
      (singleIso_inv_naturality f n i.val.1.unop.len i.property))

def activePi (n m : ℕ) : Ab ⥤ Ab where
  obj A := AddCommGrpCat.of (Active n m → A)
  map f := AddCommGrpCat.ofHom {
    toFun x i := f (x i)
    map_zero' := by funext i; exact map_zero f.hom
    map_add' x y := by funext i; exact map_add f.hom (x i) (y i) }
  map_id _ := by ext x i; rfl
  map_comp _ _ := by ext x i; rfl

set_option backward.isDefEq.respectTransparency false in
private theorem piToBiproduct_natural {A B : Ab} (f : A ⟶ B) (n m : ℕ) :
    (activePi n m).map f ≫
      (AddCommGrpCat.biproductIsoPi (fun _ : Active n m => B)).inv =
    (AddCommGrpCat.biproductIsoPi (fun _ : Active n m => A)).inv ≫
      biproduct.map (fun _ : Active n m => f) := by
  apply biproduct.hom_ext
  intro j
  simp only [Category.assoc, AddCommGrpCat.biproductIsoPi_inv_comp_π,
    biproduct.map_π]
  rw [← Category.assoc (AddCommGrpCat.biproductIsoPi (fun _ : Active n m => A)).inv,
    AddCommGrpCat.biproductIsoPi_inv_comp_π]
  ext x
  rfl

set_option backward.isDefEq.respectTransparency false in
private theorem biproductToPower_natural {A B : Ab} (f : A ⟶ B) (n m : ℕ) :
    biproduct.map (fun _ : Active n m => f) ≫
      (biproduct.isoCoproduct (fun _ : Active n m => B)).hom =
    (biproduct.isoCoproduct (fun _ : Active n m => A)).hom ≫
      (activePower n m).map f := by
  apply biproduct.hom_ext'
  intro j
  change _ = _ ≫ _ ≫ Limits.Sigma.map (fun _ : Active n m => f)
  simp [biproduct.isoCoproduct_hom]

set_option backward.isDefEq.respectTransparency false in
/-- Finite direct sums are finite products, naturally in the group. -/
def activePiIso (n m : ℕ) : activePi n m ≅ activePower n m :=
  NatIso.ofComponents (fun A =>
    (AddCommGrpCat.biproductIsoPi (fun _ : Active n m => A)).symm ≪≫
      biproduct.isoCoproduct (fun _ : Active n m => A)) (fun {A B} f => by
    change (activePi n m).map f ≫
      ((AddCommGrpCat.biproductIsoPi (fun _ : Active n m => B)).inv ≫
        (biproduct.isoCoproduct (fun _ : Active n m => B)).hom) =
      ((AddCommGrpCat.biproductIsoPi (fun _ : Active n m => A)).inv ≫
        (biproduct.isoCoproduct (fun _ : Active n m => A)).hom) ≫
        (activePower n m).map f
    rw [← Category.assoc, piToBiproduct_natural, Category.assoc,
      biproductToPower_natural, Category.assoc])

/-- The finite free group representing the underlying set of each simplex. -/
def activeLattice (n m : ℕ) : Ab := AddCommGrpCat.of (Active n m → ℤ)

def activeHomEquiv (n m : ℕ) (A : Ab) :
    (activeLattice n m ⟶ A) ≃ (Active n m → A) where
  toFun f i := f ((Pi.basisFun ℤ (Active n m)) i)
  invFun x := AddCommGrpCat.ofHom
    (((Pi.basisFun ℤ (Active n m)).constr ℤ x).toAddMonoidHom)
  left_inv f := by
    ext x
    have h := (Pi.basisFun ℤ (Active n m)).constr_self ℤ f.hom.toIntLinearMap
    exact LinearMap.congr_fun h x
  right_inv x := by
    funext i
    exact (Pi.basisFun ℤ (Active n m)).constr_basis ℤ x i

set_option backward.isDefEq.respectTransparency false in
def activeHomIso (n m : ℕ) :
    coyoneda.obj (op (activeLattice n m)) ≅ activePi n m ⋙ forget Ab :=
  NatIso.ofComponents (fun A => (activeHomEquiv n m A).toIso) (fun {A B} f => by
    ext g
    rfl)

/-- Rank of the finite free lattice representing an actual simplex. -/
def activeRank (n m : ℕ) : ℕ := Fintype.card (Active n m)

def rankLattice (n m : ℕ) : Ab := AddCommGrpCat.of (Fin (activeRank n m) → ℤ)

def activeRankIso (n m : ℕ) : activeLattice n m ≅ rankLattice n m := by
  classical
  let e : Active n m ≃ Fin (activeRank n m) := Fintype.equivFin _
  refine {
    hom := AddCommGrpCat.ofHom {
      toFun x i := x (e.symm i)
      map_zero' := rfl
      map_add' _ _ := rfl }
    inv := AddCommGrpCat.ofHom {
      toFun x i := x (e i)
      map_zero' := rfl
      map_add' _ _ := rfl }
    hom_inv_id := ?_
    inv_hom_id := ?_ }
  · ext x
    funext i
    change x (e.symm (e i)) = x i
    rw [Equiv.symm_apply_apply]
  · ext x
    funext i
    change x (e (e.symm i)) = x i
    rw [Equiv.apply_symm_apply]

def rankHomIso (n m : ℕ) :
    coyoneda.obj (op (rankLattice n m)) ≅ activePi n m ⋙ forget Ab :=
  coyoneda.mapIso (activeRankIso n m).op ≪≫ activeHomIso n m

theorem emBelow_isZero (A : Ab) (n m : ℕ) (h : m < n) :
    IsZero (((em n).obj A).obj (op (SimplexCategory.mk m))) := by
  apply (emTermIso A n m).isZero_iff.mpr
  rw [IsZero.iff_id_eq_zero]
  apply Sigma.hom_ext
  intro i
  have hh := SimplexCategory.len_le_of_epi i.val.e
  exact (False.elim (by
    change i.val.1.unop.len ≤ m at hh
    rw [i.property] at hh
    omega))

abbrev forgetFree : Ab ⥤ Ab := forget Ab ⋙ AddCommGrpCat.free

def augmentation (A : Ab) :
    forgetFree.obj A ⟶ AddCommGrpCat.free.obj PUnit :=
  AddCommGrpCat.free.map (↾fun _ : A => PUnit.unit)

theorem augmentation_natural {A B : Ab} (f : A ⟶ B) :
    forgetFree.map f ≫ augmentation B = augmentation A := by
  change AddCommGrpCat.free.map ((forget Ab).map f) ≫
    AddCommGrpCat.free.map (↾fun _ : B => PUnit.unit) = _
  rw [← Functor.map_comp]
  rfl

/-- Reduced free integral chains are the actual augmentation kernels. -/
abbrev reducedFree : Ab ⥤ Ab where
  obj A := kernel (augmentation A)
  map f := kernel.map _ _ (forgetFree.map f) (𝟙 _)
    (by rw [Category.comp_id, augmentation_natural])
  map_id A := by
    apply (cancel_mono (kernel.ι (augmentation A))).mp
    rw [kernel.lift_ι, forgetFree.map_id, Category.comp_id, Category.id_comp]
  map_comp f g := by
    apply (cancel_mono (kernel.ι (augmentation _))).mp
    rw [kernel.lift_ι, forgetFree.map_comp, Category.assoc, kernel.lift_ι]
    simp only [kernel.map, kernel.lift_ι_assoc, Category.assoc]

/-- The natural basepoint section of the free integral augmentation. -/
def basepoint (A : Ab) :
    AddCommGrpCat.free.obj PUnit ⟶ forgetFree.obj A :=
  AddCommGrpCat.free.map (↾fun _ : PUnit => (0 : A))

theorem basepoint_natural {A B : Ab} (f : A ⟶ B) :
    basepoint A ≫ forgetFree.map f = basepoint B := by
  change AddCommGrpCat.free.map (↾fun _ : PUnit => (0 : A)) ≫
    AddCommGrpCat.free.map ((forget Ab).map f) = _
  rw [← Functor.map_comp]
  congr 1
  ext x
  exact map_zero f.hom

theorem basepoint_section (A : Ab) :
    basepoint A ≫ augmentation A = 𝟙 _ := by
  change AddCommGrpCat.free.map (↾fun _ : PUnit => (0 : A)) ≫
    AddCommGrpCat.free.map (↾fun _ : A => PUnit.unit) = 𝟙 _
  rw [← Functor.map_comp]
  have h : (↾fun _ : PUnit => (0 : A)) ≫ (↾fun _ : A => PUnit.unit) =
      𝟙 (PUnit : Type) := by ext x
  rw [h, AddCommGrpCat.free.map_id]

def reducedInclusion : reducedFree ⟶ forgetFree where
  app A := kernel.ι (augmentation A)
  naturality f := by simp [reducedFree]

def reducedProjectionApp (A : Ab) : forgetFree.obj A ⟶ reducedFree.obj A :=
  kernel.lift (augmentation A) (𝟙 _ - augmentation A ≫ basepoint A) (by
    rw [Preadditive.sub_comp, Category.id_comp, Category.assoc, basepoint_section,
      Category.comp_id, sub_self])

@[reassoc (attr := simp)]
theorem reducedProjectionApp_ι (A : Ab) :
    reducedProjectionApp A ≫ kernel.ι (augmentation A) =
      𝟙 _ - augmentation A ≫ basepoint A := by
  exact kernel.lift_ι _ _ _

def reducedProjection : forgetFree ⟶ reducedFree where
  app := reducedProjectionApp
  naturality {A B} f := by
    apply (cancel_mono (kernel.ι (augmentation B))).mp
    change (forgetFree.map f ≫ reducedProjectionApp B) ≫ kernel.ι (augmentation B) =
      (reducedProjectionApp A ≫ reducedFree.map f) ≫ kernel.ι (augmentation B)
    have hm : reducedFree.map f ≫ kernel.ι (augmentation B) =
        kernel.ι (augmentation A) ≫ forgetFree.map f :=
      kernel.lift_ι _ _ _
    rw [Category.assoc, reducedProjectionApp_ι, Category.assoc, hm,
      ← Category.assoc (reducedProjectionApp A), reducedProjectionApp_ι,
      Preadditive.comp_sub, Preadditive.sub_comp, Category.comp_id,
      Category.id_comp, ← Category.assoc, augmentation_natural, Category.assoc,
      basepoint_natural]

/-- Reduction is a genuine natural retract, not an objectwise choice. -/
theorem reducedRetract_eq : reducedInclusion ≫ reducedProjection = 𝟙 reducedFree := by
  apply NatTrans.ext
  funext A
  apply (cancel_mono (kernel.ι (augmentation A))).mp
  change (kernel.ι (augmentation A) ≫ reducedProjectionApp A) ≫
    kernel.ι (augmentation A) = 𝟙 _ ≫ kernel.ι (augmentation A)
  rw [Category.assoc, reducedProjectionApp_ι, Preadditive.comp_sub,
    Category.comp_id, ← Category.assoc, kernel.condition, zero_comp, sub_zero,
    Category.id_comp]

def reducedRetract : Retract reducedFree forgetFree :=
  ⟨reducedInclusion, reducedProjection, reducedRetract_eq⟩

theorem reducedFree_zero (A : Ab) (h : IsZero A) :
    IsZero (reducedFree.obj A) := by
  have hz : 𝟙 A = 0 := (IsZero.iff_id_eq_zero A).mp h
  let e : A ≃ PUnit :=
    { toFun := fun _ => PUnit.unit
      invFun := fun _ => 0
      left_inv := fun x => by
        have hx := congrArg (fun f : A ⟶ A => f x) hz
        exact hx.symm
      right_inv := fun _ => rfl }
  have hi : IsIso (augmentation A) := by
    change IsIso (AddCommGrpCat.free.map e.toIso.hom)
    infer_instance
  exact isZero_kernel_of_mono (augmentation A)

def reducedEMChains (n : ℕ) : Ab ⥤ ChainComplex Ab ℕ :=
  em n ⋙ (SimplicialObject.whiskering Ab Ab).obj reducedFree ⋙
    alternatingFaceMapComplex Ab

/-- The actual unreduced degree functor is a free representable of finite rank. -/
def rankFreeIso (n m : ℕ) :
    coyoneda.obj (op (rankLattice n m)) ⋙ AddCommGrpCat.free ≅
      emDegree n m ⋙ forgetFree :=
  Functor.isoWhiskerRight (rankHomIso n m) AddCommGrpCat.free ≪≫
    Functor.associator (activePi n m) (forget Ab) AddCommGrpCat.free ≪≫
    Functor.isoWhiskerRight (activePiIso n m ≪≫ emDegreeIso n m) forgetFree

def reducedChainDegree (n m : ℕ) : Ab ⥤ Ab :=
  reducedEMChains n ⋙ HomologicalComplex.eval Ab (ComplexShape.down ℕ) m

/-- Each genuine reduced chain term is a natural retract of a single
finite-rank free representable; no finite-type homology claim is made here. -/
def reducedChainDegreeRetract (n m : ℕ) :
    Retract (reducedChainDegree n m)
      (coyoneda.obj (op (rankLattice n m)) ⋙ AddCommGrpCat.free) := by
  change Retract (emDegree n m ⋙ reducedFree) _
  exact (reducedRetract.map ((Functor.whiskeringLeft Ab Ab Ab).obj (emDegree n m))).trans
    (Retract.ofIso (rankFreeIso n m).symm)

section Restriction

variable {C : Type} [Category.{0} C]

def restrictedHomEquiv (F : C ⥤ Ab) (hF : F.FullyFaithful)
    (c : C) (n m : ℕ) (h : F.obj c ≅ rankLattice n m) (X : C) :
    (c ⟶ X) ≃ (rankLattice n m ⟶ F.obj X) where
  toFun g := h.inv ≫ F.map g
  invFun g := hF.preimage (h.hom ≫ g)
  left_inv g := by
    apply hF.map_injective
    simp
  right_inv g := by simp

def restrictedHomIso (F : C ⥤ Ab) (hF : F.FullyFaithful)
    (c : C) (n m : ℕ) (h : F.obj c ≅ rankLattice n m) :
    coyoneda.obj (op c) ≅ F ⋙ coyoneda.obj (op (rankLattice n m)) :=
  NatIso.ofComponents (fun X => (restrictedHomEquiv F hF c n m h X).toIso)
    (fun {X Y} f => by
      ext g
      change h.inv ≫ F.map (g ≫ f) = (h.inv ≫ F.map g) ≫ F.map f
      rw [F.map_comp, Category.assoc])

def restrictedFreeIso (F : C ⥤ Ab) (hF : F.FullyFaithful)
    (c : C) (n m : ℕ) (h : F.obj c ≅ rankLattice n m) :
    coyoneda.obj (op c) ⋙ AddCommGrpCat.free ≅
      F ⋙ (coyoneda.obj (op (rankLattice n m)) ⋙ AddCommGrpCat.free) :=
  Functor.isoWhiskerRight (restrictedHomIso F hF c n m h) AddCommGrpCat.free ≪≫
    Functor.associator F (coyoneda.obj (op (rankLattice n m))) AddCommGrpCat.free

def restrictedChainRetract (F : C ⥤ Ab) (hF : F.FullyFaithful)
    (c : C) (n m : ℕ) (h : F.obj c ≅ rankLattice n m) :
    Retract (F ⋙ reducedChainDegree n m)
      (coyoneda.obj (op c) ⋙ AddCommGrpCat.free) :=
  ((reducedChainDegreeRetract n m).map ((Functor.whiskeringLeft C Ab Ab).obj F)).trans
    (Retract.ofIso (restrictedFreeIso F hF c n m h).symm)

/-- General free representable projectivity via the actual free-forgetful
adjunction and evaluation; applies in particular to the lattice skeleton. -/
theorem freeRepresentableProjective (c : C) :
    Projective (coyoneda.obj (op c) ⋙ AddCommGrpCat.free) := by
  let adj := AddCommGrpCat.adj.whiskerRight C
  let e (G : C ⥤ Ab) :
      (coyoneda.obj (op c) ⋙ AddCommGrpCat.free ⟶ G) ≃ G.obj c :=
    (adj.homEquiv (coyoneda.obj (op c)) G).trans coyonedaEquiv
  have hn {G H : C ⥤ Ab} (f : coyoneda.obj (op c) ⋙ AddCommGrpCat.free ⟶ G)
      (g : G ⟶ H) : e H (f ≫ g) = g.app c (e G f) := by
    change coyonedaEquiv (adj.homEquiv (coyoneda.obj (op c)) H (f ≫ g)) =
      g.app c (coyonedaEquiv (adj.homEquiv (coyoneda.obj (op c)) G f))
    exact (congrArg coyonedaEquiv
      (adj.homEquiv_naturality_right (X := coyoneda.obj (op c)) f g)).trans
      (coyonedaEquiv_comp _ _)
  refine ⟨fun {E X} f p hp => ?_⟩
  have hE : Epi (p.app c) := (NatTrans.epi_iff_epi_app p).mp hp c
  obtain ⟨x, hx⟩ := (AddCommGrpCat.epi_iff_surjective (p.app c)).mp hE (e X f)
  refine ⟨(e E).symm x, ?_⟩
  apply (e X).injective
  rw [hn, Equiv.apply_symm_apply, hx]

theorem restrictedChainProjective (F : C ⥤ Ab) (hF : F.FullyFaithful)
    (c : C) (n m : ℕ) (h : F.obj c ≅ rankLattice n m) :
    Projective (F ⋙ reducedChainDegree n m) := by
  letI : Projective (coyoneda.obj (op c) ⋙ AddCommGrpCat.free) :=
    freeRepresentableProjective c
  exact (restrictedChainRetract F hF c n m h).projective

end Restriction

theorem reducedEMChains_below (A : Ab) (n m : ℕ) (h : m < n) :
    IsZero (((reducedEMChains n).obj A).X m) := by
  change IsZero (reducedFree.obj (((em n).obj A).obj (op (SimplexCategory.mk m))))
  exact reducedFree_zero _ (emBelow_isZero A n m h)

#print axioms emTermIso
#print axioms emDegreeIso
#print axioms activePiIso
#print axioms activeHomIso
#print axioms rankFreeIso
#print axioms reducedChainDegreeRetract
#print axioms restrictedChainProjective
#print axioms emBelow_isZero
#print axioms reducedRetract_eq
#print axioms reducedFree_zero
#print axioms reducedEMChains_below
end CMDG.CondensedCM5R0.EilenbergMacLaneModel
