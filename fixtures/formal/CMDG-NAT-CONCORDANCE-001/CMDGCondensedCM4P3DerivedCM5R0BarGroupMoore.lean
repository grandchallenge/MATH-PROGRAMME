import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneBarTotal
import Mathlib.AlgebraicTopology.DoldKan.HomotopyEquivalence

/-! Normalize the bar of the abelian group itself, before applying
the reduced free functor. This computes the horizontal Moore complex
of the bisimplicial abelian group used for the next Dold–Kan stage. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology AlgebraicTopology.DoldKan
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBarObject
open CMDG.CondensedCM5R0.BreenDeligneBarTupleQuotient
open CMDG.CondensedCM5R0.BreenDeligneNormalizedBar
namespace CMDG.CondensedCM5R0.BarGroupMoore

def groupMoore : AGrp ⥤ ChainComplex AGrp ℕ := barFunctor ⋙ normalizedMooreComplex AGrp

abbrev G (A : AGrp) (p : ℕ) := (groupMoore.obj A).X p

def projectG (A : AGrp) (p : ℕ) : T A p ⟶ G A p :=
  (PInftyToNormalizedMooreComplex (bar A)).f p

def includeG (A : AGrp) (p : ℕ) : G A p ⟶ T A p :=
  (inclusionOfMooreComplexMap (bar A)).f p

theorem include_project (A : AGrp) (p : ℕ) :
    includeG A p ≫ projectG A p = 𝟙 _ :=
  congrArg (fun f : (normalizedMooreComplex AGrp).obj (bar A) ⟶ _ => f.f p)
    (splitMonoInclusionOfMooreComplexMap (bar A)).id

theorem project_include (A : AGrp) (p : ℕ) :
    projectG A p ≫ includeG A p = (PInfty (X := bar A)).f p :=
  congrArg (fun f : (alternatingFaceMapComplex AGrp).obj (bar A) ⟶ _ => f.f p)
    (PInftyToNormalizedMooreComplex_comp_inclusionOfMooreComplexMap (bar A))

instance (A : AGrp) (p : ℕ) : Epi (projectG A p) :=
  epi_of_epi_fac (include_project A p)

instance (A : AGrp) (p : ℕ) : Mono (includeG A p) :=
  mono_of_mono_fac (include_project A p)

theorem barZero (A : AGrp) : IsZero (T A 0) := by
  apply (IsZero.iff_id_eq_zero _).mpr
  apply ConcreteCategory.hom_ext
  intro x
  funext i
  exact Fin.elim0 i

theorem groupMooreZero (A : AGrp) : IsZero (G A 0) :=
  IsZero.of_epi (projectG A 0) (barZero A)

set_option backward.isDefEq.respectTransparency false in
theorem projectG_degeneracy (A : AGrp) (p : ℕ) (i : Fin (p+1)) :
    (bar A).σ i ≫ projectG A (p+1) = 0 := by
  apply (cancel_mono (includeG A (p+1))).mp
  rw [Category.assoc, project_include,zero_comp]
  exact σ_comp_PInfty (bar A) i

set_option backward.isDefEq.respectTransparency false in
theorem projectG_degenerate_tuple (A : AGrp) (p : ℕ) (x : Tuples A (p+1))
    (hx : ∃ i, x i = 0) : projectG A (p+1) x = 0 := by
  obtain ⟨i,y,h⟩ := (degenerate_iff_insert A p x).mp hx
  rw [h,← barDegeneracy_insert]
  exact CategoryTheory.congr_fun (projectG_degeneracy A p i) y

set_option backward.isDefEq.respectTransparency false in
theorem projectG_high_zero (A : AGrp) (p : ℕ) :
    projectG A (p+2) = 0 := by
  apply ConcreteCategory.hom_ext
  intro x
  let f : T A (p+2) →+ G A (p+2) := (projectG A (p+2)).hom
  change f x = 0
  have hx : (∑ i : Fin (p+2), Pi.single i (x i)) = x := by
    funext j
    simp [Finset.sum_apply,Pi.single_apply]
  rw [← hx,map_sum]
  apply Finset.sum_eq_zero
  intro i _
  have hne : ∃ j : Fin (p+2), j ≠ i := by
    by_cases h : i = 0
    · exact ⟨⟨1,by omega⟩,by rw [h]; intro he; have hh := congrArg (fun x : Fin (p+2) => x.val) he; simp at hh⟩
    · exact ⟨0,Ne.symm h⟩
  obtain ⟨j,hj⟩ := hne
  exact projectG_degenerate_tuple A (p+1) (Pi.single i (x i))
    ⟨j,by simp [hj]⟩

theorem groupMooreHighZero (A : AGrp) (p : ℕ) : IsZero (G A (p+2)) := by
  apply (IsZero.iff_id_eq_zero _).mpr
  rw [← include_project A (p+2),projectG_high_zero,comp_zero]

set_option backward.isDefEq.respectTransparency false in
theorem groupMooreOneProjector (A : AGrp) :
    (PInfty (X := bar A)).f 1 = 𝟙 _ := by
  have hz : DegeneraciesVanish (X := bar A) (n := 1) (𝟙 (T A 1)) := by
    rw [degeneraciesVanish_succ_iff]
    intro i
    exact (barZero A).eq_of_src _ _
  have h := (degeneraciesVanish_iff_QInfty_f_comp (X := bar A) (n := 1) (𝟙 (T A 1))).mp hz
  change (QInfty (X := bar A)).f 1 ≫ 𝟙 ((AlternatingFaceMapComplex.obj (bar A)).X 1) = 0 at h
  rw [Category.comp_id] at h
  have he := PInfty_f_add_QInfty_f (X := bar A) 1
  rw [h,add_zero] at he
  exact he

def oneTermIso (A : AGrp) : T A 1 ≅ A where
  hom := AddCommGrpCat.ofHom {toFun x := x 0, map_zero' := rfl, map_add' := fun _ _ => rfl}
  inv := AddCommGrpCat.ofHom {toFun a := fun _ => a, map_zero' := rfl, map_add' := fun _ _ => rfl}
  hom_inv_id := by
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    have h : i = 0 := Subsingleton.elim _ _
    subst i
    rfl
  inv_hom_id := by
    apply ConcreteCategory.hom_ext
    intro x
    rfl

def groupMooreOneIso (A : AGrp) : G A 1 ≅ A :=
  { hom := includeG A 1
    inv := projectG A 1
    hom_inv_id := include_project A 1
    inv_hom_id := (project_include A 1).trans (groupMooreOneProjector A) } ≪≫ oneTermIso A

theorem groupMooreOtherZero (A : AGrp) (p : ℕ) (hp : p ≠ 1) :
    IsZero (G A p) := by
  rcases p with _ | (_ | p)
  · exact groupMooreZero A
  · exact (hp rfl).elim
  · exact groupMooreHighZero A p

set_option backward.isDefEq.respectTransparency false in
theorem groupMooreOne_natural {A B : AGrp} (f : A ⟶ B) :
    (groupMoore.map f).f 1 ≫ (groupMooreOneIso B).hom = (groupMooreOneIso A).hom ≫ f := by
  have h := congrArg (fun g => g.f 1)
    ((inclusionOfMooreComplex AGrp).naturality (barNat f))
  change (groupMoore.map f).f 1 ≫ includeG B 1 =
    includeG A 1 ≫ (barNat f).app (op (SimplexCategory.mk 1)) at h
  change (groupMoore.map f).f 1 ≫ includeG B 1 ≫ (oneTermIso B).hom =
    (includeG A 1 ≫ (oneTermIso A).hom) ≫ f
  rw [← Category.assoc, h, Category.assoc, Category.assoc]
  congr 1

def groupMooreComponent (A : AGrp) (p : ℕ) :
    G A p ≅ ((HomologicalComplex.single AGrp (ComplexShape.down ℕ) 1).obj A).X p :=
  if h : p = 1 then
    eqToIso (by rw [h]) ≪≫ groupMooreOneIso A ≪≫
      (HomologicalComplex.singleObjXIsoOfEq (ComplexShape.down ℕ) 1 A p h).symm
  else
    (groupMooreOtherZero A p h).iso
      (HomologicalComplex.isZero_single_obj_X (ComplexShape.down ℕ) 1 A p h)

set_option backward.isDefEq.respectTransparency false in
def groupMooreIso (A : AGrp) :
    groupMoore.obj A ≅ (HomologicalComplex.single AGrp (ComplexShape.down ℕ) 1).obj A :=
  HomologicalComplex.Hom.isoOfComponents (groupMooreComponent A) (by
    intro i j hij
    by_cases hi : i = 1
    · have hj : j = 0 := by change j+1=i at hij; omega
      subst i
      subst j
      exact (HomologicalComplex.isZero_single_obj_X (ComplexShape.down ℕ) 1 A 0 (by decide)).eq_of_tgt _ _
    · exact (groupMooreOtherZero A i hi).eq_of_src _ _)

set_option backward.isDefEq.respectTransparency false in
def groupMooreNatIso :
    groupMoore ≅ HomologicalComplex.single AGrp (ComplexShape.down ℕ) 1 :=
  NatIso.ofComponents groupMooreIso (fun {A B} f => by
    apply HomologicalComplex.Hom.ext
    funext i
    by_cases hi : i = 1
    · subst i
      change (groupMoore.map f).f 1 ≫ (groupMooreComponent B 1).hom =
        (groupMooreComponent A 1).hom ≫ ((HomologicalComplex.single AGrp (ComplexShape.down ℕ) 1).map f).f 1
      change (groupMoore.map f).f 1 ≫
          ((groupMooreOneIso B).hom ≫ (HomologicalComplex.singleObjXSelf (ComplexShape.down ℕ) 1 B).inv) =
        ((groupMooreOneIso A).hom ≫ (HomologicalComplex.singleObjXSelf (ComplexShape.down ℕ) 1 A).inv) ≫ _
      rw [HomologicalComplex.single_map_f_self]
      simp only [Category.assoc,Iso.inv_hom_id_assoc]
      rw [← Category.assoc,groupMooreOne_natural,Category.assoc]
    · change (groupMoore.map f).f i ≫ (groupMooreComponent B i).hom =
        (groupMooreComponent A i).hom ≫ ((HomologicalComplex.single AGrp (ComplexShape.down ℕ) 1).map f).f i
      exact (groupMooreOtherZero A i hi).eq_of_src _ _)

#print axioms groupMooreHighZero
#print axioms groupMooreOneIso
#print axioms groupMooreNatIso
end CMDG.CondensedCM5R0.BarGroupMoore
