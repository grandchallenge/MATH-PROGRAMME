import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneAdditiveBoundary
import Mathlib.GroupTheory.FreeGroup.GeneratorEquiv
import Mathlib.LinearAlgebra.TensorProduct.Basis

/-! The actual reduced free group has the free basis of nonbasepoint
generators. Tensoring these bases describes the normalized smash terms. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Module
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneAdditiveBoundary
namespace CMDG.CondensedCM5R0.BreenDeligneReducedBasis

abbrev NZ (A : AGrp) := {a : A // a ≠ 0}
abbrev freeNZ (A : AGrp) := AddCommGrpCat.free.obj (NZ A)

def ofNZ (A : AGrp) : freeNZ A ⟶ reducedFree.obj A :=
  AddCommGrpCat.ofHom (FreeAbelianGroup.lift (fun x : NZ A => reducedGenerator A x.val))

def nzGen (A : AGrp) (x : A) : freeNZ A := by
  classical
  exact if h : x = 0 then 0 else FreeAbelianGroup.of ⟨x,h⟩

def freeToNZ (A : AGrp) : forgetFree.obj A ⟶ freeNZ A :=
  AddCommGrpCat.ofHom (FreeAbelianGroup.lift (nzGen A))

def toNZ (A : AGrp) : reducedFree.obj A ⟶ freeNZ A :=
  kernel.ι (augmentation A) ≫ freeToNZ A

set_option backward.isDefEq.respectTransparency false in
theorem toNZ_generator (A : AGrp) (x : A) :
    toNZ A (reducedGenerator A x) = nzGen A x := by
  have h := CategoryTheory.congr_fun (reducedProjectionApp_ι A) (FreeAbelianGroup.of x)
  change kernel.ι (augmentation A) (reducedProjectionApp A (FreeAbelianGroup.of x)) =
    (𝟙 (forgetFree.obj A) - augmentation A ≫ basepoint A) (FreeAbelianGroup.of x) at h
  change freeToNZ A (kernel.ι (augmentation A) (reducedProjectionApp A (FreeAbelianGroup.of x))) = _
  rw [h]
  change FreeAbelianGroup.lift (nzGen A) (FreeAbelianGroup.of x - FreeAbelianGroup.of (0 : A)) = _
  rw [map_sub, FreeAbelianGroup.lift_apply_of, FreeAbelianGroup.lift_apply_of]
  simp [nzGen]

set_option backward.isDefEq.respectTransparency false in
theorem ofNZ_nzGen (A : AGrp) (x : A) :
    ofNZ A (nzGen A x) = reducedGenerator A x := by
  classical
  by_cases h : x = 0
  · subst x
    rw [generator_zero]
    change (ofNZ A).hom (nzGen A 0) = 0
    simp [nzGen]
  · change (FreeAbelianGroup.lift (fun z : NZ A => reducedGenerator A z.val)) (nzGen A x) = _
    simp [nzGen, h]

set_option backward.isDefEq.respectTransparency false in
def reducedFreeIso (A : AGrp) : freeNZ A ≅ reducedFree.obj A where
  hom := ofNZ A
  inv := toNZ A
  hom_inv_id := by
    apply AddCommGrpCat.hom_ext
    apply FreeAbelianGroup.lift_ext
    intro x
    change toNZ A ((FreeAbelianGroup.lift (fun z : NZ A => reducedGenerator A z.val)) (FreeAbelianGroup.of x)) = _
    rw [FreeAbelianGroup.lift_apply_of, toNZ_generator]
    change nzGen A x.val = FreeAbelianGroup.of x
    simp [nzGen, x.property]
  inv_hom_id := by
    have hp : reducedInclusion.app A ≫ reducedProjectionApp A = 𝟙 _ :=
      congrArg (fun t => t.app A) reducedRetract_eq
    letI : Epi (reducedProjectionApp A) := epi_of_epi_fac hp
    apply (cancel_epi (reducedProjectionApp A)).mp
    apply AddCommGrpCat.hom_ext
    apply FreeAbelianGroup.lift_ext
    intro x
    change ofNZ A (toNZ A (reducedGenerator A x)) = reducedGenerator A x
    rw [toNZ_generator, ofNZ_nzGen]

def reducedAddEquiv (A : AGrp) : FreeAbelianGroup (NZ A) ≃+ reducedFree.obj A where
  toFun := ofNZ A
  invFun := toNZ A
  left_inv x := CategoryTheory.congr_fun (reducedFreeIso A).hom_inv_id x
  right_inv x := CategoryTheory.congr_fun (reducedFreeIso A).inv_hom_id x
  map_add' := map_add (ofNZ A).hom

def reducedBasis (A : AGrp) : Basis (NZ A) ℤ (reducedFree.obj A) :=
  (FreeAbelianGroup.basis (NZ A)).map (reducedAddEquiv A).toIntLinearEquiv

#print axioms reducedFreeIso
#print axioms reducedBasis
end CMDG.CondensedCM5R0.BreenDeligneReducedBasis
