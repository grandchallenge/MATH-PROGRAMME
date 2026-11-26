import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneStableAdditive
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneLatticeProjectives
import Mathlib.Algebra.Category.ModuleCat.Biproducts

/-! Finite lattice coordinates of the actual additive stable homology functor. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneLatticeProjectives
open CMDG.CondensedCM5R0.BreenDeligneStableAdditive
namespace CMDG.CondensedCM5R0.BreenDeligneStableLattice

abbrev Z : AGrp := AddCommGrpCat.of ℤ

def coordinate (r : ℕ) (i : Fin r) : lattice r ⟶ Z :=
  AddCommGrpCat.ofHom (Pi.evalAddMonoidHom (fun _ : Fin r => ℤ) i)

abbrev coordModule (M : ZMod) (r : ℕ) : ZMod :=
  @ModuleCat.of ℤ _ (Fin r → M) _ (Pi.module (Fin r) (fun _ => M) ℤ)

def coordinateIso (F : AGrp ⥤ ZMod) [F.Additive] (r : ℕ) :
    F.obj (lattice r) ≅ coordModule (F.obj Z) r :=
  F.mapIso (AddCommGrpCat.biproductIsoPi (fun _ : Fin r => Z)).symm ≪≫
    F.mapBiproduct (fun _ : Fin r => Z) ≪≫
    ModuleCat.biproductIsoPi (fun _ : Fin r => F.obj Z)

set_option backward.isDefEq.respectTransparency false in
theorem coordinateIso_apply (F : AGrp ⥤ ZMod) [F.Additive] (r : ℕ) (i : Fin r) (x : F.obj (lattice r)) :
    (coordinateIso F r).hom x i = F.map (coordinate r i) x := by
  let p := (ModuleCat.biproductIsoPi (fun _ : Fin r => F.obj Z)).inv ≫
    biproduct.π (fun _ : Fin r => F.obj Z) i
  have h : (coordinateIso F r).hom ≫ p = F.map (coordinate r i) := by
    unfold coordinateIso p
    simp only [Iso.trans_hom,Functor.mapIso_hom,Iso.symm_hom,Category.assoc,
      Iso.hom_inv_id_assoc,F.mapBiproduct_hom,biproduct.lift_π,← F.map_comp,
      AddCommGrpCat.biproductIsoPi_inv_comp_π]
    rfl
  have hp (y : coordModule (F.obj Z) r) : p y = y i := by
    unfold p
    have hh := ModuleCat.biproductIsoPi_inv_comp_π (fun _ : Fin r => F.obj Z) i
    exact CategoryTheory.congr_fun hh y
  have hh := CategoryTheory.congr_fun h x
  change p ((coordinateIso F r).hom x) = _ at hh
  rwa [hp] at hh

def stableLatticeIso (n k r : ℕ) (hk : k<n) :
    (stableFunctor n k).obj (lattice r) ≅
      coordModule ((stableFunctor n k).obj Z) r := by
  letI := stableFunctor_additive n k hk
  exact coordinateIso (stableFunctor n k) r

#print axioms coordinateIso_apply
#print axioms stableLatticeIso
end CMDG.CondensedCM5R0.BreenDeligneStableLattice
