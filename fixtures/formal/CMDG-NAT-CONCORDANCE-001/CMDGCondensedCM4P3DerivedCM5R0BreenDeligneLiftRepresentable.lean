import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneUniverseLift

/-! Identify the lifted free representable with the actual one-arity
polynomial functor, naturally in the lattice. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
set_option maxHeartbeats 800000
universe u
open CategoryTheory CategoryTheory.Limits Opposite
open CMDG.CondensedCM5R0.BreenDeligneProbe
open CMDG.CondensedCM5R0.BreenDeligneUniverseLift
namespace CMDG.CondensedCM5R0.BreenDeligneLiftRepresentable
open UniversalExtension (rank generic tupleMap tupleMap_generic tupleMap_generic_id tupleMap_comp)

def homEquiv (r s : Big.{u}) :
    (r ⟶ s) ≃ (shrink.{u}.obj r ⟶ shrink.{u}.obj s) where
  toFun f := shrink.map f
  invFun g := InducedCategory.homMk (bigLinear
    ((rankCoords.{u} s).symm.toAddMonoidHom.comp
      ((BreenDeligneLatticeProjectives.valueFunctor.map g).hom.comp
        (rankCoords.{u} r).toAddMonoidHom)))
  left_inv f := by
    apply InducedCategory.homEquiv.injective
    apply ConcreteCategory.hom_ext
    intro x
    change (rankCoords.{u} s).symm (rankCoords.{u} s (UniversalExtension.incl.map f
      ((rankCoords.{u} r).symm (rankCoords.{u} r x)))) = _
    rw [AddEquiv.symm_apply_apply,AddEquiv.symm_apply_apply]
    rfl
  right_inv g := by
    apply InducedCategory.homEquiv.injective
    apply AddCommGrpCat.hom_ext
    ext x
    change rankCoords.{u} s ((rankCoords.{u} s).symm (BreenDeligneLatticeProjectives.valueFunctor.map g
      (rankCoords.{u} r ((rankCoords.{u} r).symm x)))) = _
    rw [AddEquiv.apply_symm_apply,AddEquiv.apply_symm_apply]
    rfl

def tupleEquiv (r s : Big.{u}) : (r ⟶ s) ≃ (Fin r → rank.{u} s) where
  toFun f i := UniversalExtension.incl.map f (generic r i)
  invFun x := InducedCategory.homMk (tupleMap x)
  left_inv f := by
    apply InducedCategory.homEquiv.injective
    apply ModuleCat.free_hom_ext
    intro i
    change tupleMap (fun j => UniversalExtension.incl.map f (generic r j)) (generic r i.down) = UniversalExtension.incl.map f (generic r i.down)
    exact tupleMap_generic _ i.down
  right_inv x := by
    funext i
    exact tupleMap_generic x i

def singleArity (r : ℕ) : Fin 1 → ℕ := fun _ => r

def generatorEquiv (r : ℕ) (s : Big.{u}) :
    (Quiver.Hom (V:=Small) r (shrink.{u}.obj s)) ≃ (tupleSet (singleArity r)).obj (rank.{u} s) :=
  (homEquiv (r : Big.{u}) s).symm.trans ((tupleEquiv (r : Big.{u}) s).trans {
    toFun x := ⟨0,x⟩
    invFun x := x.2
    left_inv _ := rfl
    right_inv x := by
      obtain ⟨j,x⟩ := x
      have hj : j = 0 := Subsingleton.elim _ _
      subst j
      rfl })

theorem generator_natural (r : ℕ) {s t : Big.{u}} (f : s ⟶ t)
    (g : Quiver.Hom (V:=Small) r (shrink.{u}.obj s)) :
    generatorEquiv r t (g ≫ shrink.map f) =
      (tupleSet (singleArity r)).map (UniversalExtension.incl.map f) (generatorEquiv r s g) := by
  let h := (homEquiv (r : Big.{u}) s).symm g
  have he : (homEquiv (r : Big.{u}) t).symm (g ≫ shrink.map f) = h ≫ f := by
    apply (homEquiv (r : Big.{u}) t).injective
    rw [Equiv.apply_symm_apply]
    change g ≫ shrink.map f = shrink.map (h ≫ f)
    rw [Functor.map_comp]
    have hh : shrink.map h = g := (homEquiv (r : Big.{u}) s).apply_symm_apply g
    rw [hh]
  change (⟨0,tupleEquiv _ _ ((homEquiv (r : Big.{u}) t).symm (g ≫ shrink.map f))⟩ : (tupleSet (singleArity r)).obj (rank t)) = _
  rw [he]
  rfl

def freeLiftIso {X : Type} {Y : Type (u+1)} (e : X ≃ Y) :
    lift.{u}.obj ((ModuleCat.free ℤ).obj X) ≅ (ModuleCat.free Coeff.{u}).obj Y :=
  bigIso ((liftAdd ((ModuleCat.free ℤ).obj X)).symm.trans
    ((Finsupp.domCongr e).trans (Finsupp.mapRange.addEquiv
      (ULift.ringEquiv : Coeff.{u} ≃+* ℤ).symm.toAddEquiv)))

theorem freeLift_gen {X : Type} {Y : Type (u+1)} (e : X ≃ Y) (x : X) :
    (freeLiftIso e).hom (liftAdd ((ModuleCat.free ℤ).obj X) (ModuleCat.freeMk x)) =
      ModuleCat.freeMk (e x) := by
  change Finsupp.mapRange (ULift.ringEquiv : Coeff.{u} ≃+* ℤ).symm (map_zero _) (Finsupp.equivMapDomain e (Finsupp.single x (1:ℤ))) =
    Finsupp.single (e x) (1:Coeff.{u})
  rw [Finsupp.equivMapDomain_single,Finsupp.mapRange_single]
  rfl

theorem freeLift_inv_gen {X : Type} {Y : Type (u+1)} (e : X ≃ Y) (y : Y) :
    (freeLiftIso e).inv (ModuleCat.freeMk y) =
      liftAdd ((ModuleCat.free ℤ).obj X) (ModuleCat.freeMk (e.symm y)) := by
  apply (ConcreteCategory.bijective_of_isIso (freeLiftIso e).hom).injective
  rw [freeLift_gen,Equiv.apply_symm_apply]
  exact CategoryTheory.congr_fun (freeLiftIso e).inv_hom_id _

def repIso (r : ℕ) : transport.{u}.obj (BreenDeligneLatticeFP.poly r) ≅
    UniversalExtension.incl ⋙ polynomial (singleArity r) :=
  (NatIso.ofComponents (fun s => (freeLiftIso (generatorEquiv r s)).symm)
    (fun {s t} f => by
      apply ModuleCat.free_hom_ext
      intro y
      let e := generatorEquiv r s
      let e' := generatorEquiv r t
      change (freeLiftIso e').inv ((ModuleCat.free Coeff.{u}).map
        ((tupleSet (singleArity r)).map (UniversalExtension.incl.map f)) (ModuleCat.freeMk y)) =
        lift.map ((ModuleCat.free ℤ).map (↾fun g : Quiver.Hom (V:=Small) r (shrink.{u}.obj s) => g ≫ shrink.map f))
          ((freeLiftIso e).inv (ModuleCat.freeMk y))
      rw [ModuleCat.free_map_apply,freeLift_inv_gen,freeLift_inv_gen,lift_apply,ModuleCat.free_map_apply]
      have he := generator_natural r f (e.symm y)
      change e' (e.symm y ≫ shrink.map f) =
        (tupleSet (singleArity r)).map (UniversalExtension.incl.map f) (e (e.symm y)) at he
      rw [Equiv.apply_symm_apply] at he
      rw [← he,Equiv.symm_apply_apply]
      rfl)).symm

#print axioms homEquiv
#print axioms repIso
end CMDG.CondensedCM5R0.BreenDeligneLiftRepresentable
