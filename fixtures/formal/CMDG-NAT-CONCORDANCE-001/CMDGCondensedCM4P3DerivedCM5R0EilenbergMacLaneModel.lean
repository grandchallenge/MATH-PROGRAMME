import Mathlib.AlgebraicTopology.DoldKan.FunctorGamma
import Mathlib.AlgebraicTopology.AlternatingFaceMapComplex
import Mathlib.Algebra.Category.Grp.Adjunctions
import Mathlib.Algebra.Category.Grp.Abelian
import Mathlib.Algebra.Homology.Single

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

theorem reducedEMChains_below (A : Ab) (n m : ℕ) (h : m < n) :
    IsZero (((reducedEMChains n).obj A).X m) := by
  change IsZero (reducedFree.obj (((em n).obj A).obj (op (SimplexCategory.mk m))))
  exact reducedFree_zero _ (emBelow_isZero A n m h)

#print axioms emTermIso
#print axioms emBelow_isZero
#print axioms reducedRetract_eq
#print axioms reducedFree_zero
#print axioms reducedEMChains_below
end CMDG.CondensedCM5R0.EilenbergMacLaneModel
