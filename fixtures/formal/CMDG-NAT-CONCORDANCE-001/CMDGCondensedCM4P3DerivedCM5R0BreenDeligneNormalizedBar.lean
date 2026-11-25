import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneBarObject

/-! The horizontally normalized *reduced* bar object.  Identify its actual
Moore projection with the tuple quotient, including vertical naturality. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology AlgebraicTopology.DoldKan
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneAdditiveBoundary
open CMDG.CondensedCM5R0.BreenDeligneBarTupleQuotient
open CMDG.CondensedCM5R0.BreenDeligneBarObject
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
namespace CMDG.CondensedCM5R0.BreenDeligneNormalizedBar

abbrev T (A : AGrp) (p : ℕ) := barTerm A (op (SimplexCategory.mk p))
abbrev Q (A : AGrp) (p : ℕ) := AddCommGrpCat.of (Smash A p)

def reducedBar (A : AGrp) : SimplicialObject AGrp := bar A ⋙ reducedFree

def reducedBarFunctor : AGrp ⥤ SimplicialObject AGrp :=
  barFunctor ⋙ (SimplicialObject.whiskering AGrp AGrp).obj reducedFree

def horizontalMoore : AGrp ⥤ ChainComplex AGrp ℕ :=
  reducedBarFunctor ⋙ normalizedMooreComplex AGrp

abbrev M (A : AGrp) (p : ℕ) := ((horizontalMoore.obj A).X p)

def project (A : AGrp) (p : ℕ) : reducedFree.obj (T A p) ⟶ M A p :=
  (PInftyToNormalizedMooreComplex (reducedBar A)).f p

def includeMoore (A : AGrp) (p : ℕ) : M A p ⟶ reducedFree.obj (T A p) :=
  (inclusionOfMooreComplexMap (reducedBar A)).f p

theorem include_project (A : AGrp) (p : ℕ) :
    includeMoore A p ≫ project A p = 𝟙 _ :=
  congrArg (fun f : (normalizedMooreComplex AGrp).obj (reducedBar A) ⟶ _ => f.f p)
    (splitMonoInclusionOfMooreComplexMap (reducedBar A)).id

theorem project_include (A : AGrp) (p : ℕ) :
    project A p ≫ includeMoore A p =
      (PInfty (X := reducedBar A)).f p :=
  congrArg (fun f : (alternatingFaceMapComplex AGrp).obj (reducedBar A) ⟶ _ => f.f p)
    (PInftyToNormalizedMooreComplex_comp_inclusionOfMooreComplexMap (reducedBar A))

set_option backward.isDefEq.respectTransparency false in
instance project_epi (A : AGrp) (p : ℕ) : Epi (project A p) :=
  epi_of_epi_fac (include_project A p)

def quot (A : AGrp) (p : ℕ) : reducedFree.obj (T A p) ⟶ Q A p :=
  reducedInclusion.app (T A p) ≫ AddCommGrpCat.ofHom (quotientMap A p)

def sectionQuot (A : AGrp) (p : ℕ) : Q A p ⟶ reducedFree.obj (T A p) :=
  AddCommGrpCat.ofHom (sectionMap A p) ≫ reducedProjectionApp (T A p)

set_option backward.isDefEq.respectTransparency false in
theorem quot_generator (A : AGrp) (p : ℕ) (x : Tuples A (p+1)) :
    quot A (p+1) (reducedGenerator (T A (p+1)) x) = quotientGen A (p+1) x := by
  have h := CategoryTheory.congr_fun (reducedProjectionApp_ι (T A (p+1))) (FreeAbelianGroup.of x)
  change kernel.ι (augmentation (T A (p+1))) (reducedProjectionApp (T A (p+1)) (FreeAbelianGroup.of x)) =
    (𝟙 (forgetFree.obj (T A (p+1))) - augmentation (T A (p+1)) ≫ basepoint (T A (p+1))) (FreeAbelianGroup.of x) at h
  change quotientMap A (p+1) (kernel.ι (augmentation (T A (p+1)))
    (reducedProjectionApp (T A (p+1)) (FreeAbelianGroup.of x))) = _
  rw [h]
  change quotientMap A (p+1) (FreeAbelianGroup.of x - FreeAbelianGroup.of 0) = _
  rw [map_sub]
  unfold quotientMap
  rw [FreeAbelianGroup.lift_apply_of,FreeAbelianGroup.lift_apply_of]
  rw [show quotientGen A (p+1) 0 = 0 from by simp [quotientGen], sub_zero]

set_option backward.isDefEq.respectTransparency false in
theorem section_quot (A : AGrp) (p : ℕ) :
    sectionQuot A (p+1) ≫ quot A (p+1) = 𝟙 _ := by
  apply AddCommGrpCat.hom_ext
  apply FreeAbelianGroup.lift_ext
  intro x
  change quot A (p+1) (reducedProjectionApp (T A (p+1))
    (FreeAbelianGroup.map Subtype.val (FreeAbelianGroup.of x))) = FreeAbelianGroup.of x
  rw [FreeAbelianGroup.map_of_apply]
  change quot A (p+1) (reducedGenerator (T A (p+1)) x.val) = _
  rw [quot_generator]
  simp [quotientGen,x.property]

set_option backward.isDefEq.respectTransparency false in
instance quot_epi (A : AGrp) (p : ℕ) : Epi (quot A (p+1)) :=
  epi_of_epi_fac (section_quot A p)

set_option backward.isDefEq.respectTransparency false in
theorem quot_degeneracies (A : AGrp) (p : ℕ) :
    DegeneraciesVanish (X := reducedBar A) (n := p+1) (quot A (p+1)) := by
  rw [degeneraciesVanish_succ_iff]
  intro i
  have hp : reducedInclusion.app (T A p) ≫ reducedProjectionApp (T A p) = 𝟙 _ :=
    congrArg (fun t => t.app (T A p)) reducedRetract_eq
  letI : Epi (reducedProjectionApp (T A p)) := epi_of_epi_fac hp
  apply (cancel_epi (reducedProjectionApp (T A p))).mp
  apply AddCommGrpCat.hom_ext
  apply FreeAbelianGroup.lift_ext
  intro x
  change quot A (p+1) (reducedFree.map ((bar A).σ i) (reducedGenerator (T A p) x)) = 0
  have hg := generator_natural ((bar A).σ i) x
  change reducedFree.map ((bar A).σ i) (reducedGenerator (T A p) x) =
    reducedGenerator (T A (p+1)) ((bar A).σ i x) at hg
  rw [hg,quot_generator]
  have h : ¬ ∀ j, ((bar A).σ i x) j ≠ 0 := fun hh => hh i (barDegeneracy_zero A p i x)
  simp [quotientGen,h]

set_option backward.isDefEq.respectTransparency false in
theorem project_include_quot (A : AGrp) (p : ℕ) :
    project A (p+1) ≫ includeMoore A (p+1) ≫ quot A (p+1) = quot A (p+1) := by
  rw [← Category.assoc,project_include]
  have hq := (degeneraciesVanish_iff_QInfty_f_comp (X := reducedBar A) (n := p+1) (quot A (p+1))).mp (quot_degeneracies A p)
  have h := congrArg (fun f => f ≫ quot A (p+1)) (PInfty_f_add_QInfty_f (X := reducedBar A) (p+1))
  rw [Preadditive.add_comp,hq,add_zero,Category.id_comp] at h
  exact h

set_option backward.isDefEq.respectTransparency false in
theorem project_degeneracy (A : AGrp) (p : ℕ) (i : Fin (p+1)) :
    (reducedBar A).σ i ≫ project A (p+1) = 0 := by
  -- Cancel the inclusion of the actual split Moore subobject.
  letI : Mono (includeMoore A (p+1)) := mono_of_mono_fac (include_project A (p+1))
  apply (cancel_mono (includeMoore A (p+1))).mp
  rw [Category.assoc,project_include,zero_comp]
  exact σ_comp_PInfty (reducedBar A) i

set_option backward.isDefEq.respectTransparency false in
theorem quot_section_project (A : AGrp) (p : ℕ) :
    quot A (p+1) ≫ sectionQuot A (p+1) ≫ project A (p+1) = project A (p+1) := by
  have hp : reducedInclusion.app (T A (p+1)) ≫ reducedProjectionApp (T A (p+1)) = 𝟙 _ :=
    congrArg (fun t => t.app (T A (p+1))) reducedRetract_eq
  letI : Epi (reducedProjectionApp (T A (p+1))) := epi_of_epi_fac hp
  apply (cancel_epi (reducedProjectionApp (T A (p+1)))).mp
  apply AddCommGrpCat.hom_ext
  apply FreeAbelianGroup.lift_ext
  intro x
  change project A (p+1) (sectionQuot A (p+1) (quot A (p+1)
    (reducedGenerator (T A (p+1)) x))) = project A (p+1) (reducedGenerator (T A (p+1)) x)
  rw [quot_generator]
  classical
  by_cases h : ∀ i, x i ≠ 0
  · rw [quotientGen,dif_pos h]
    change project A (p+1) (reducedProjectionApp (T A (p+1))
      (FreeAbelianGroup.map Subtype.val (FreeAbelianGroup.of ⟨x,h⟩))) = _
    rw [FreeAbelianGroup.map_of_apply]
    rfl
  · rw [quotientGen,dif_neg h]
    change (project A (p+1)).hom ((sectionQuot A (p+1)).hom 0) = _
    rw [map_zero,map_zero]
    push Not at h
    obtain ⟨i,y,hy⟩ := (degenerate_iff_insert A p x).mp h
    rw [hy,← barDegeneracy_insert]
    have hg := generator_natural ((bar A).σ i) y
    change reducedFree.map ((bar A).σ i) (reducedGenerator (T A p) y) =
      reducedGenerator (T A (p+1)) ((bar A).σ i y) at hg
    rw [← hg]
    have hz := CategoryTheory.congr_fun (project_degeneracy A p i) (reducedGenerator (T A p) y)
    exact hz.symm

set_option backward.isDefEq.respectTransparency false in
def mooreQuotIso (A : AGrp) (p : ℕ) : M A (p+1) ≅ Q A (p+1) where
  hom := includeMoore A (p+1) ≫ quot A (p+1)
  inv := sectionQuot A (p+1) ≫ project A (p+1)
  hom_inv_id := by
    rw [Category.assoc,quot_section_project,include_project]
  inv_hom_id := by
    rw [Category.assoc,project_include_quot,section_quot]

set_option backward.isDefEq.respectTransparency false in
theorem quot_natural {A B : AGrp} (f : A ⟶ B) (p : ℕ) :
    ((reducedBarFunctor.map f).app (op (SimplexCategory.mk (p+1)))) ≫ quot B (p+1) =
      quot A (p+1) ≫ AddCommGrpCat.ofHom (smashMap f (p+1)) := by
  have hp : reducedInclusion.app (T A (p+1)) ≫ reducedProjectionApp (T A (p+1)) = 𝟙 _ :=
    congrArg (fun t => t.app (T A (p+1))) reducedRetract_eq
  letI : Epi (reducedProjectionApp (T A (p+1))) := epi_of_epi_fac hp
  apply (cancel_epi (reducedProjectionApp (T A (p+1)))).mp
  apply AddCommGrpCat.hom_ext
  apply FreeAbelianGroup.lift_ext
  intro x
  let g : T A (p+1) ⟶ T B (p+1) := (barNat f).app (op (SimplexCategory.mk (p+1)))
  change quot B (p+1) (reducedFree.map g (reducedGenerator (T A (p+1)) x)) =
    smashMap f (p+1) (quot A (p+1) (reducedGenerator (T A (p+1)) x))
  rw [generator_natural,quot_generator,quot_generator,smashMap_generator]
  rfl

set_option backward.isDefEq.respectTransparency false in
theorem project_natural {A B : AGrp} (f : A ⟶ B) (p : ℕ) :
    (reducedBarFunctor.map f).app (op (SimplexCategory.mk p)) ≫ project B p =
      project A p ≫ (horizontalMoore.map f).f p :=
  congrArg (fun g => g.f p)
    (PInftyToNormalizedMooreComplex_naturality (reducedBarFunctor.map f))

set_option backward.isDefEq.respectTransparency false in
theorem mooreQuotIso_natural {A B : AGrp} (f : A ⟶ B) (p : ℕ) :
    (horizontalMoore.map f).f (p+1) ≫ (mooreQuotIso B p).hom =
      (mooreQuotIso A p).hom ≫ AddCommGrpCat.ofHom (smashMap f (p+1)) := by
  apply (cancel_epi (project A (p+1))).mp
  change project A (p+1) ≫ (horizontalMoore.map f).f (p+1) ≫
      includeMoore B (p+1) ≫ quot B (p+1) =
    project A (p+1) ≫ (includeMoore A (p+1) ≫ quot A (p+1)) ≫
      AddCommGrpCat.ofHom (smashMap f (p+1))
  rw [← Category.assoc, ← project_natural, Category.assoc, project_include_quot]
  simp only [Category.assoc]
  have h := congrArg (fun k => k ≫ AddCommGrpCat.ofHom (smashMap f (p+1))) (project_include_quot A p)
  simp only [Category.assoc] at h
  exact (quot_natural f p).trans h.symm

set_option backward.isDefEq.respectTransparency false in
/-- Actual normalized horizontal columns identify naturally with the
tuple quotient, as integer modules. -/
def horizontalColumnIso (p : ℕ) :
    horizontalMoore ⋙ HomologicalComplex.eval AGrp (ComplexShape.down ℕ) (p+1) ⋙ toZModule
      ≅ smashFunctor (p+1) :=
  NatIso.ofComponents (fun A => toZModule.mapIso (mooreQuotIso A p)) (fun {A B} f => by
    change toZModule.map ((horizontalMoore.map f).f (p+1)) ≫
      toZModule.map (mooreQuotIso B p).hom =
      toZModule.map (mooreQuotIso A p).hom ≫ toZModule.map (AddCommGrpCat.ofHom (smashMap f (p+1)))
    rw [← Functor.map_comp, ← Functor.map_comp, mooreQuotIso_natural])

def actualVerticalColumn (X : SimplicialObject AGrp) (p : ℕ) : Ch :=
  (alternatingFaceMapComplex ZMod).obj
    (X ⋙ horizontalMoore ⋙ HomologicalComplex.eval AGrp (ComplexShape.down ℕ) p ⋙ toZModule)

def actualColumnIso (X : SimplicialObject AGrp) (p : ℕ) :
    actualVerticalColumn X (p+1) ≅ verticalSmashChains X (p+1) :=
  (alternatingFaceMapComplex ZMod).mapIso
    (Functor.isoWhiskerLeft X (horizontalColumnIso p))

def actualFirstColumnIso (A : AGrp) (n : ℕ) :
    actualVerticalColumn ((EilenbergMacLaneModel.em n).obj A) 1 ≅ reducedChainsZ A n :=
  actualColumnIso _ 0 ≪≫ firstColumnIso A n

#print axioms mooreQuotIso
#print axioms horizontalColumnIso
#print axioms actualColumnIso
#print axioms actualFirstColumnIso
end CMDG.CondensedCM5R0.BreenDeligneNormalizedBar
