import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneLiftRepresentable

/-! Finite coproduct normalization by tagged free generators. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u v w
open CategoryTheory CategoryTheory.Limits
open scoped ZeroObject
open CMDG.CondensedCM5R0.BreenDeligneProbe
open CMDG.CondensedCM5R0.BreenDeligneUniverseLift
namespace CMDG.CondensedCM5R0.BreenDelignePolynomialSum

variable {C : Type v} [Category.{w} C]

def sumSet (X Y : C ⥤ Type (u+1)) : C ⥤ Type (u+1) where
  obj r := X.obj r ⊕ Y.obj r
  map f := ↾Sum.map (X.map f) (Y.map f)
  map_id r := by
    apply ConcreteCategory.hom_ext
    rintro (x|y)
    · exact congrArg Sum.inl (CategoryTheory.congr_fun (X.map_id r) x)
    · exact congrArg Sum.inr (CategoryTheory.congr_fun (Y.map_id r) y)
  map_comp f g := by
    apply ConcreteCategory.hom_ext
    rintro (x|y)
    · exact congrArg Sum.inl (CategoryTheory.congr_fun (X.map_comp f g) x)
    · exact congrArg Sum.inr (CategoryTheory.congr_fun (Y.map_comp f g) y)

abbrev freeF (X : C ⥤ Type (u+1)) := X ⋙ ModuleCat.free Coeff.{u}

def leftIn (X Y : C ⥤ Type (u+1)) : freeF X ⟶ freeF (sumSet X Y) where
  app r := (ModuleCat.free Coeff.{u}).map (↾Sum.inl)
  naturality {r s} f := by
    change (ModuleCat.free Coeff.{u}).map _ ≫ (ModuleCat.free Coeff.{u}).map _ =
      (ModuleCat.free Coeff.{u}).map _ ≫ (ModuleCat.free Coeff.{u}).map _
    rw [← Functor.map_comp,← Functor.map_comp]
    rfl

def rightIn (X Y : C ⥤ Type (u+1)) : freeF Y ⟶ freeF (sumSet X Y) where
  app r := (ModuleCat.free Coeff.{u}).map (↾Sum.inr)
  naturality {r s} f := by
    change (ModuleCat.free Coeff.{u}).map _ ≫ (ModuleCat.free Coeff.{u}).map _ =
      (ModuleCat.free Coeff.{u}).map _ ≫ (ModuleCat.free Coeff.{u}).map _
    rw [← Functor.map_comp,← Functor.map_comp]
    rfl

def sumDesc (X Y : C ⥤ Type (u+1)) (F : C ⥤ Mod.{u})
    (f : freeF X ⟶ F) (g : freeF Y ⟶ F) : freeF (sumSet X Y) ⟶ F where
  app r := ModuleCat.freeDesc (↾Sum.elim (fun x => f.app r (ModuleCat.freeMk x))
    (fun y => g.app r (ModuleCat.freeMk y)))
  naturality {r s} h := by
    apply ModuleCat.free_hom_ext
    rintro (x|y)
    · change ModuleCat.freeDesc _ ((ModuleCat.free Coeff.{u}).map ((sumSet X Y).map h)
        (ModuleCat.freeMk (Sum.inl x))) =
          F.map h (ModuleCat.freeDesc _ (ModuleCat.freeMk (Sum.inl x)))
      rw [ModuleCat.free_map_apply,ModuleCat.freeDesc_apply,ModuleCat.freeDesc_apply]
      change f.app s (ModuleCat.freeMk (X.map h x)) = F.map h (f.app r (ModuleCat.freeMk x))
      have hh := CategoryTheory.congr_fun (f.naturality h) (ModuleCat.freeMk x)
      change f.app s ((ModuleCat.free Coeff.{u}).map (X.map h) (ModuleCat.freeMk x)) = _ at hh
      rw [ModuleCat.free_map_apply] at hh
      exact hh
    · change ModuleCat.freeDesc _ ((ModuleCat.free Coeff.{u}).map ((sumSet X Y).map h)
        (ModuleCat.freeMk (Sum.inr y))) =
          F.map h (ModuleCat.freeDesc _ (ModuleCat.freeMk (Sum.inr y)))
      rw [ModuleCat.free_map_apply,ModuleCat.freeDesc_apply,ModuleCat.freeDesc_apply]
      change g.app s (ModuleCat.freeMk (Y.map h y)) = F.map h (g.app r (ModuleCat.freeMk y))
      have hh := CategoryTheory.congr_fun (g.naturality h) (ModuleCat.freeMk y)
      change g.app s ((ModuleCat.free Coeff.{u}).map (Y.map h) (ModuleCat.freeMk y)) = _ at hh
      rw [ModuleCat.free_map_apply] at hh
      exact hh

theorem left_desc (X Y : C ⥤ Type (u+1)) (F : C ⥤ Mod.{u})
    (f : freeF X ⟶ F) (g : freeF Y ⟶ F) :
    leftIn X Y ≫ sumDesc X Y F f g = f := by
  apply NatTrans.ext
  funext r
  apply ModuleCat.free_hom_ext
  intro x
  change ModuleCat.freeDesc _ ((ModuleCat.free Coeff.{u}).map (↾Sum.inl)
    (ModuleCat.freeMk x)) = _
  rw [ModuleCat.free_map_apply,ModuleCat.freeDesc_apply]
  rfl

theorem right_desc (X Y : C ⥤ Type (u+1)) (F : C ⥤ Mod.{u})
    (f : freeF X ⟶ F) (g : freeF Y ⟶ F) :
    rightIn X Y ≫ sumDesc X Y F f g = g := by
  apply NatTrans.ext
  funext r
  apply ModuleCat.free_hom_ext
  intro y
  change ModuleCat.freeDesc _ ((ModuleCat.free Coeff.{u}).map (↾Sum.inr)
    (ModuleCat.freeMk y)) = _
  rw [ModuleCat.free_map_apply,ModuleCat.freeDesc_apply]
  rfl

theorem sum_hom_ext (X Y : C ⥤ Type (u+1)) {F : C ⥤ Mod.{u}}
    (f g : freeF (sumSet X Y) ⟶ F)
    (hl : leftIn X Y ≫ f = leftIn X Y ≫ g)
    (hr : rightIn X Y ≫ f = rightIn X Y ≫ g) : f = g := by
  apply NatTrans.ext
  funext r
  apply ModuleCat.free_hom_ext
  rintro (x|y)
  · have h := CategoryTheory.congr_fun (NatTrans.congr_app hl r) (ModuleCat.freeMk x)
    change f.app r ((ModuleCat.free Coeff.{u}).map (↾Sum.inl) (ModuleCat.freeMk x)) =
      g.app r ((ModuleCat.free Coeff.{u}).map (↾Sum.inl) (ModuleCat.freeMk x)) at h
    rw [ModuleCat.free_map_apply] at h
    exact h
  · have h := CategoryTheory.congr_fun (NatTrans.congr_app hr r) (ModuleCat.freeMk y)
    change f.app r ((ModuleCat.free Coeff.{u}).map (↾Sum.inr) (ModuleCat.freeMk y)) =
      g.app r ((ModuleCat.free Coeff.{u}).map (↾Sum.inr) (ModuleCat.freeMk y)) at h
    rw [ModuleCat.free_map_apply] at h
    exact h

def sumFreeIso (X Y : C ⥤ Type (u+1)) :
    freeF X ⊞ freeF Y ≅ freeF (sumSet X Y) where
  hom := biprod.desc (leftIn X Y) (rightIn X Y)
  inv := sumDesc X Y _ biprod.inl biprod.inr
  hom_inv_id := by
    apply biprod.hom_ext'
    · rw [biprod.inl_desc_assoc,left_desc,Category.comp_id]
    · rw [biprod.inr_desc_assoc,right_desc,Category.comp_id]
  inv_hom_id := by
    apply sum_hom_ext X Y
    · rw [← Category.assoc,left_desc,biprod.inl_desc,Category.comp_id]
    · rw [← Category.assoc,right_desc,biprod.inr_desc,Category.comp_id]

variable {k l : ℕ}

def append (a : Fin k → ℕ) (b : Fin l → ℕ) : Fin (k+l) → ℕ :=
  Sum.elim a b ∘ finSumFinEquiv.symm

def joined (a : Fin k → ℕ) (b : Fin l → ℕ) (M : Mod.{u}) :
    ((tupleSet a).obj M ⊕ (tupleSet b).obj M) ≃ (tupleSet (append a b)).obj M :=
  (Equiv.sumSigmaDistrib (fun i : Fin k ⊕ Fin l => Fin (Sum.elim a b i) → M)).symm.trans
    (Equiv.sigmaCongr finSumFinEquiv (fun j => Equiv.arrowCongr (finCongr (by simp [append])) (Equiv.refl M)))

theorem joined_natural (a : Fin k → ℕ) (b : Fin l → ℕ) {M N : Mod.{u}} (f : M ⟶ N)
    (z : (tupleSet a).obj M ⊕ (tupleSet b).obj M) :
    joined a b N (Sum.map ((tupleSet a).map f) ((tupleSet b).map f) z) =
      (tupleSet (append a b)).map f (joined a b M z) := by
  rcases z with ⟨j,x⟩|⟨j,x⟩ <;> rfl

def joinedIso (a : Fin k → ℕ) (b : Fin l → ℕ) :
    sumSet (tupleSet.{u} a) (tupleSet.{u} b) ≅ tupleSet (append a b) :=
  NatIso.ofComponents (fun M => (joined a b M).toIso) (fun {M N} f => by
    apply ConcreteCategory.hom_ext
    exact joined_natural a b f)

def polynomialSumIso (a : Fin k → ℕ) (b : Fin l → ℕ) :
    (UniversalExtension.incl.{u} ⋙ polynomial a) ⊞
      (UniversalExtension.incl ⋙ polynomial b) ≅
        UniversalExtension.incl ⋙ polynomial (append a b) :=
  sumFreeIso (UniversalExtension.incl ⋙ tupleSet a) (UniversalExtension.incl ⋙ tupleSet b) ≪≫
    Functor.isoWhiskerRight (Functor.isoWhiskerLeft UniversalExtension.incl (joinedIso a b))
      (ModuleCat.free Coeff.{u})

#print axioms sumFreeIso
#print axioms polynomialSumIso
end CMDG.CondensedCM5R0.BreenDelignePolynomialSum
