import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneReducedBasis
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneTensorComparison
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneBarTupleQuotient

/-! The failure of reduced free chains to be additive factors through
the quadratic tensor term. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits CategoryTheory.MonoidalCategory
open Module
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneAdditiveBoundary
open CMDG.CondensedCM5R0.BreenDeligneReducedBasis
open CMDG.CondensedCM5R0.BreenDeligneBarTupleQuotient
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
namespace CMDG.CondensedCM5R0.BreenDeligneCrossEffect
abbrev R := reducedFree ⋙ toZModule
abbrev gen (A : AGrp) (x : A) : R.obj A := reducedGenerator A x

def quadratic (A : AGrp) : R.obj A ⟶ R.obj A ⊗ R.obj A :=
  ModuleCat.ofHom ((reducedBasis A).constr ℤ (fun x => gen A x.val ⊗ₜ[ℤ] gen A x.val))

def cross (A : AGrp) : R.obj A ⊗ R.obj A ⟶ R.obj A :=
  ModuleCat.ofHom (((reducedBasis A).tensorProduct (reducedBasis A)).constr ℤ
    (fun x => gen A (x.1.val+x.2.val) - gen A x.1.val - gen A x.2.val))

theorem gen_map {A B : AGrp} (f : A ⟶ B) (x : A) :
    R.map f (gen A x) = gen B (f x) := generator_natural f x

set_option backward.isDefEq.respectTransparency false in
theorem quadratic_gen (A : AGrp) (x : A) :
    quadratic A (gen A x) = gen A x ⊗ₜ[ℤ] gen A x := by
  by_cases h : x=0
  · subst x
    simp [gen,generator_zero]; exact map_zero (quadratic A).hom
  · have hx : reducedBasis A ⟨x,h⟩ = gen A x := reducedBasis_generator A ⟨x,h⟩
    rw [← hx]
    change (reducedBasis A).constr ℤ _ (reducedBasis A ⟨x,h⟩) = _
    rw [Basis.constr_basis,hx]

set_option backward.isDefEq.respectTransparency false in
theorem cross_gen (A : AGrp) (x y : A) :
    cross A (gen A x ⊗ₜ[ℤ] gen A y) = gen A (x+y)-gen A x-gen A y := by
  by_cases hx : x=0
  · subst x
    simp [gen,generator_zero]; exact map_zero (cross A).hom
  by_cases hy : y=0
  · subst y
    simp [gen,generator_zero]; exact map_zero (cross A).hom
  let i : NZ A := ⟨x,hx⟩
  let j : NZ A := ⟨y,hy⟩
  have h : ((reducedBasis A).tensorProduct (reducedBasis A)) (i,j) =
      gen A x ⊗ₜ[ℤ] gen A y := by
    rw [Basis.tensorProduct_apply',reducedBasis_generator,reducedBasis_generator]
  rw [← h]
  change ((reducedBasis A).tensorProduct (reducedBasis A)).constr ℤ _
      (((reducedBasis A).tensorProduct (reducedBasis A)) (i,j)) = _
  rw [Basis.constr_basis]

set_option backward.isDefEq.respectTransparency false in
theorem gen_ext {A : AGrp} {B : ZMod} {f g : R.obj A ⟶ B}
    (h : ∀ x : A, f (gen A x)=g (gen A x)) : f=g := by
  apply ModuleCat.hom_ext
  apply (reducedBasis A).ext
  intro i
  rw [reducedBasis_generator]
  exact h i.val

set_option backward.isDefEq.respectTransparency false in
theorem cross_ext {A : AGrp} {B : ZMod} {f g : R.obj A ⊗ R.obj A ⟶ B}
    (h : ∀ x y : A, f (gen A x ⊗ₜ[ℤ] gen A y)=g (gen A x ⊗ₜ[ℤ] gen A y)) : f=g := by
  apply ModuleCat.hom_ext
  apply ((reducedBasis A).tensorProduct (reducedBasis A)).ext
  intro i
  rw [Basis.tensorProduct_apply',reducedBasis_generator,reducedBasis_generator]
  exact h i.1.val i.2.val

set_option backward.isDefEq.respectTransparency false in
theorem quadratic_natural {A B : AGrp} (f : A ⟶ B) :
    R.map f ≫ quadratic B = quadratic A ≫ (R.map f ⊗ₘ R.map f) := by
  apply gen_ext
  intro x
  change quadratic B (R.map f (gen A x)) =
    (R.map f ⊗ₘ R.map f) (quadratic A (gen A x))
  rw [gen_map,quadratic_gen,quadratic_gen]
  change _ = R.map f (gen A x) ⊗ₜ[ℤ] R.map f (gen A x)
  rw [gen_map]

set_option backward.isDefEq.respectTransparency false in
theorem cross_natural {A B : AGrp} (f : A ⟶ B) :
    (R.map f ⊗ₘ R.map f) ≫ cross B = cross A ≫ R.map f := by
  apply cross_ext
  intro x y
  change cross B (R.map f (gen A x) ⊗ₜ[ℤ] R.map f (gen A y)) =
    R.map f (cross A (gen A x ⊗ₜ[ℤ] gen A y))
  rw [gen_map,gen_map,cross_gen,cross_gen,map_sub,map_sub,gen_map,gen_map,gen_map,map_add]

set_option backward.isDefEq.respectTransparency false in
theorem additive_defect {A B : AGrp} (f g : A ⟶ B) :
    R.map (f+g) - R.map f - R.map g =
      quadratic A ≫ (R.map f ⊗ₘ R.map g) ≫ cross B := by
  apply gen_ext
  intro x
  change _ = cross B ((R.map f ⊗ₘ R.map g) (quadratic A (gen A x)))
  rw [quadratic_gen]
  change _ = cross B (R.map f (gen A x) ⊗ₜ[ℤ] R.map g (gen A x))
  rw [gen_map,gen_map,cross_gen]
  change R.map (f+g) (gen A x) - R.map f (gen A x) - R.map g (gen A x) = _
  rw [gen_map,gen_map,gen_map]
  rfl

#print axioms additive_defect
end CMDG.CondensedCM5R0.BreenDeligneCrossEffect
