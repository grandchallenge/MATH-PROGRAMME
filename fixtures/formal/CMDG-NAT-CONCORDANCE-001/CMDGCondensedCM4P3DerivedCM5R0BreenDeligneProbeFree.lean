import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneUniversalTransport

/-! Indexed free modules are the free modules on the genuine product
of the indexing set and generator set, naturally in both variables. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.BreenDeligneProbe
open RealProductProjection

abbrev Free := ModuleCat.free Coeff.{u}
abbrev freeOn : SetPsh.{u} ⥤ Psh.{u} :=
  (Functor.whiskeringRight _ _ _).obj Free

def productSet (P Q : SetPsh.{u}) : SetPsh.{u} where
  obj T := P.obj T × Q.obj T
  map f := ↾fun z => (P.map f z.1,Q.map f z.2)
  map_id T := by
    apply ConcreteCategory.hom_ext
    intro z
    simp
  map_comp f g := by
    apply ConcreteCategory.hom_ext
    intro z
    simp

def productMap (P : SetPsh.{u}) {Q R : SetPsh.{u}} (f : Q ⟶ R) :
    productSet P Q ⟶ productSet P R where
  app T := ↾fun z => (z.1,f.app T z.2)
  naturality := by
    intro T U g
    apply ConcreteCategory.hom_ext
    intro z
    change (P.map g z.1, f.app U (Q.map g z.2)) =
      (P.map g z.1, R.map g (f.app T z.2))
    exact Prod.ext rfl (NatTrans.naturality_apply f g z.2)

def indexedFreeHom (P Q : SetPsh.{u}) (T : CompHaus.{u}ᵒᵖ) :
    (indexedSum P (freeOn.obj Q)).obj T ⟶ (freeOn.obj (productSet P Q)).obj T :=
  Sigma.desc (fun p : P.obj T => Free.map (↾fun q : Q.obj T => (p,q)))

def indexedFreeInv (P Q : SetPsh.{u}) (T : CompHaus.{u}ᵒᵖ) :
    (freeOn.obj (productSet P Q)).obj T ⟶ (indexedSum P (freeOn.obj Q)).obj T :=
  ModuleCat.freeDesc (↾fun z : P.obj T × Q.obj T =>
    Sigma.ι (fun _ : P.obj T => (freeOn.obj Q).obj T) z.1 (ModuleCat.freeMk z.2))

theorem indexedFreeHom_leg (P Q : SetPsh.{u}) (T : CompHaus.{u}ᵒᵖ)
    (p : P.obj T) :
    Sigma.ι (fun _ : P.obj T => (freeOn.obj Q).obj T) p ≫ indexedFreeHom P Q T =
      Free.map (↾fun q : Q.obj T => (p,q)) := Sigma.ι_desc _ _

theorem indexedFreeHom_apply (P Q : SetPsh.{u}) (T : CompHaus.{u}ᵒᵖ)
    (p : P.obj T) (q : Q.obj T) :
    indexedFreeHom P Q T (Sigma.ι (fun _ : P.obj T => (freeOn.obj Q).obj T) p
      (ModuleCat.freeMk q)) = ModuleCat.freeMk (p,q) := by
  change (Sigma.ι _ p ≫ indexedFreeHom P Q T) (ModuleCat.freeMk q) = _
  rw [indexedFreeHom_leg]
  exact ModuleCat.free_map_apply _ _

theorem indexedFreeInv_apply (P Q : SetPsh.{u}) (T : CompHaus.{u}ᵒᵖ)
    (p : P.obj T) (q : Q.obj T) :
    indexedFreeInv P Q T (ModuleCat.freeMk (p,q)) =
      Sigma.ι (fun _ : P.obj T => (freeOn.obj Q).obj T) p (ModuleCat.freeMk q) :=
  ModuleCat.freeDesc_apply _ _

def indexedFreeIsoAt (P Q : SetPsh.{u}) (T : CompHaus.{u}ᵒᵖ) :
    (indexedSum P (freeOn.obj Q)).obj T ≅ (freeOn.obj (productSet P Q)).obj T where
  hom := indexedFreeHom P Q T
  inv := indexedFreeInv P Q T
  hom_inv_id := by
    apply Sigma.hom_ext
    intro p
    rw [← Category.assoc,indexedFreeHom_leg]
    change Free.map (↾fun q : Q.obj T => (p,q)) ≫ indexedFreeInv P Q T =
      Sigma.ι (fun _ : P.obj T => (freeOn.obj Q).obj T) p ≫ 𝟙 _
    simp only [Category.comp_id]
    apply ModuleCat.free_hom_ext
    intro q
    change indexedFreeInv P Q T (Free.map (↾fun q : Q.obj T => (p,q))
      (ModuleCat.freeMk q)) = _
    rw [ModuleCat.free_map_apply,indexedFreeInv_apply]
    rfl
  inv_hom_id := by
    apply ModuleCat.free_hom_ext
    rintro ⟨p,q⟩
    change indexedFreeHom P Q T (indexedFreeInv P Q T (ModuleCat.freeMk (p,q))) = _
    rw [indexedFreeInv_apply,indexedFreeHom_apply]
    rfl

def indexedFreeIso (P Q : SetPsh.{u}) :
    indexedSum P (freeOn.obj Q) ≅ freeOn.obj (productSet P Q) :=
  NatIso.ofComponents (indexedFreeIsoAt P Q) (by
    intro T U f
    apply Sigma.hom_ext
    intro p
    change Sigma.ι _ p ≫ Limits.Sigma.map' (P.map f) (fun _ => Free.map (Q.map f)) ≫
      indexedFreeHom P Q U =
      Sigma.ι _ p ≫ indexedFreeHom P Q T ≫ Free.map ((productSet P Q).map f)
    rw [Sigma.ι_comp_map'_assoc,indexedFreeHom_leg,← Category.assoc,indexedFreeHom_leg]
    rw [← Functor.map_comp,← Functor.map_comp]
    rfl)

theorem indexedFreeIso_natural (P : SetPsh.{u}) {Q R : SetPsh.{u}} (f : Q ⟶ R) :
    (indexedFunctor P).map (freeOn.map f) ≫ (indexedFreeIso P R).hom =
      (indexedFreeIso P Q).hom ≫ freeOn.map (productMap P f) := by
  apply NatTrans.ext
  funext T
  apply Sigma.hom_ext
  intro p
  change Sigma.ι _ p ≫ Limits.Sigma.map (fun _ : P.obj T => Free.map (f.app T)) ≫
    indexedFreeHom P R T =
    Sigma.ι _ p ≫ indexedFreeHom P Q T ≫ Free.map ((productMap P f).app T)
  rw [Sigma.ι_map_assoc]
  change Free.map (f.app T) ≫ Sigma.ι (fun _ : P.obj T => (freeOn.obj R).obj T) p ≫ indexedFreeHom P R T =
    Sigma.ι (fun _ : P.obj T => (freeOn.obj Q).obj T) p ≫ indexedFreeHom P Q T ≫
      Free.map ((productMap P f).app T)
  rw [indexedFreeHom_leg,← Category.assoc,indexedFreeHom_leg,
    ← Functor.map_comp,← Functor.map_comp]
  rfl

#print axioms indexedFreeIso
#print axioms indexedFreeIso_natural
end CMDG.CondensedCM5R0.BreenDeligneProbe
