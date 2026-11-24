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
    · simp [hi, Category.assoc]
    · have hz : IsZero (B i) :=
        HomologicalComplex.isZero_single_obj_X (ComplexShape.down ℕ) n A _ hi
      exact hz.eq_of_src _ _
  · apply Sigma.hom_ext
    intro i
    have hi := i.property
    simp [hi, Category.assoc]

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

def forgetFree : Ab ⥤ Ab := forget Ab ⋙ AddCommGrpCat.free

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
def reducedFree : Ab ⥤ Ab where
  obj A := kernel (augmentation A)
  map f := kernel.map _ _ (forgetFree.map f) (𝟙 _)
    (by rw [Category.comp_id, augmentation_natural])
  map_id A := by
    apply (cancel_mono (kernel.ι (augmentation A))).mp
    simp
  map_comp f g := by
    apply (cancel_mono (kernel.ι (augmentation _))).mp
    simp [Category.assoc, Functor.map_comp]

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
#print axioms reducedFree_zero
#print axioms reducedEMChains_below
end CMDG.CondensedCM5R0.EilenbergMacLaneModel
