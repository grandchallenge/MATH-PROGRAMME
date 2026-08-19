import CMDGCondensedCM4P2EE3

/-!
# CMDG CM4-P3-C — exact underived IsSolid reduction

This fixture performs the bounded P3-C reduction from the actual pinned
`CondensedMod.IsSolid` field. It transports the target of the Yoneda
solidification-precomposition map across protected P2-E and then exposes the
protected P2-D tensor-Hom duality map.

It does not prove that the resulting residual tensor-Hom map is bijective,
and therefore does not make P3 available or nonblocking.
-/

namespace CMDG.CondensedCM4P3C

universe u

open CategoryTheory Opposite

/-- Exact lifted integral coefficient ring retained from CM4/P2/P3. -/
abbrev R := ULift.{u + 1} ℤ

/-- Protected P2-E objectwise comparison at a profinite set. -/
noncomputable def targetIso (S : Profinite.{u}) :
    CMDG.CondensedCM4P2D.measureFunctor.obj S ≅
      (Condensed.profiniteSolid R).obj S :=
  CMDG.CondensedCM4P2E.CanonicalRightKanUniqueness.measureProfiniteSolidNatIso.app S

/-- Apply Yoneda to the protected P2-E target comparison. -/
noncomputable def targetYonedaIso (S : Profinite.{u}) :
    yoneda.obj (CMDG.CondensedCM4P2D.measureFunctor.obj S) ≅
      yoneda.obj ((Condensed.profiniteSolid R).obj S) :=
  yoneda.mapIso (targetIso S)

/-- The actual pinned solidification morphism whose opposite is consumed by
`CondensedMod.IsSolid`. -/
noncomputable abbrev solidification (X : Profinite.{u}) :=
  (Condensed.profiniteSolidification R).app X

/-- The exact Yoneda precomposition map after transporting the target to the
protected P2-D measure object. -/
noncomputable def measurePrecomp (S X : Profinite.{u}) :=
  (yoneda.obj (CMDG.CondensedCM4P2D.measureFunctor.obj S)).map
    (solidification X).op

/-- The exact Yoneda precomposition map appearing in the pinned solidity
predicate for `profiniteSolid R S`. -/
noncomputable def solidPrecomp (S X : Profinite.{u}) :=
  (yoneda.obj ((Condensed.profiniteSolid R).obj S)).map
    (solidification X).op

/-- Naturality of Yoneda applied to protected P2-E gives the exact conjugacy
square between the measure-target and profinite-solid-target precomposition
maps. -/
theorem precomp_naturality (S X : Profinite.{u}) :
    measurePrecomp S X ≫
        (targetYonedaIso S).hom.app (op ((Condensed.profiniteFree R).obj X)) =
      (targetYonedaIso S).hom.app (op ((Condensed.profiniteSolid R).obj X)) ≫
        solidPrecomp S X := by
  simpa [measurePrecomp, solidPrecomp, solidification] using
    (targetYonedaIso S).hom.naturality (solidification X).op

/-- The pinned `IsSolid` precomposition map is an isomorphism exactly when the
same map with target transported to the protected measure model is an
isomorphism. This is a reduction theorem only; it supplies no instance for the
measure-target map. -/
theorem measurePrecomp_isIso_iff_solidPrecomp (S X : Profinite.{u}) :
    IsIso (measurePrecomp S X) ↔ IsIso (solidPrecomp S X) := by
  constructor
  · intro h
    letI : IsIso (measurePrecomp S X) := h
    haveI : IsIso
        ((targetYonedaIso S).hom.app (op ((Condensed.profiniteSolid R).obj X)) ≫
          solidPrecomp S X) := by
      rw [← precomp_naturality S X]
      infer_instance
    exact IsIso.of_isIso_comp_left
      ((targetYonedaIso S).hom.app (op ((Condensed.profiniteSolid R).obj X)))
      (solidPrecomp S X)
  · intro h
    letI : IsIso (solidPrecomp S X) := h
    haveI : IsIso
        (measurePrecomp S X ≫
          (targetYonedaIso S).hom.app (op ((Condensed.profiniteFree R).obj X))) := by
      rw [precomp_naturality S X]
      infer_instance
    exact IsIso.of_isIso_comp_right
      (measurePrecomp S X)
      ((targetYonedaIso S).hom.app (op ((Condensed.profiniteFree R).obj X)))

/-- A complete family of measure-target precomposition isomorphisms would imply
the actual pinned solidity predicate. P3-C deliberately does not provide that
family. -/
theorem isSolid_of_measurePrecomp_isIso (S : Profinite.{u})
    (h : ∀ X : Profinite.{u}, IsIso (measurePrecomp S X)) :
    CondensedMod.IsSolid R ((Condensed.profiniteSolid R).obj S) := by
  constructor
  intro X
  exact (measurePrecomp_isIso_iff_solidPrecomp S X).mp (h X)

/-- Sheaf-level Hom into the protected measure object. -/
abbrev MeasureHom (S : Profinite.{u}) (F : CondensedMod.{u} R) :=
  F ⟶ CMDG.CondensedCM4P2D.measureFunctor.obj S

/-- Underlying presheaf of a condensed module. -/
abbrev UnderlyingPresheaf (F : CondensedMod.{u} R) :
    CMDG.CondensedCM4P2D.PresheafModule :=
  F.obj

/-- Tensor source appearing in the protected P2-D closed-monoidal duality. -/
noncomputable abbrev DualTensorObj (S : Profinite.{u}) (F : CondensedMod.{u} R) :
    CMDG.CondensedCM4P2D.PresheafModule :=
  MonoidalCategoryStruct.tensorObj
    (CMDG.CondensedCM4P2D.discreteContinuousPresheaf.obj (op S))
    (UnderlyingPresheaf F)

/-- Concrete tensor-Hom target of the protected P2-D duality. -/
abbrev DualTensorHom (S : Profinite.{u}) (F : CondensedMod.{u} R) :=
  DualTensorObj S F ⟶ CMDG.CondensedCM4P2D.coefficientPresheaf

/-- Protected P2-D, now presented directly at the sheaf level: morphisms into
the measure object are exactly tensor-Hom morphisms into the coefficient
presheaf. The first leg is full faithfulness of sheaves inside presheaves; the
second leg is the protected P2-D closed-monoidal duality. -/
noncomputable def measureHomDualityEquiv (S : Profinite.{u}) (F : CondensedMod.{u} R) :
    MeasureHom S F ≃ DualTensorHom S F := by
  refine CategoryTheory.Sheaf.homEquiv.trans ?_
  change (F.obj ⟶ CMDG.CondensedCM4P2D.measurePresheafObj S) ≃ DualTensorHom S F
  exact (CMDG.CondensedCM4P2D.dualityHomEquiv S F.obj).symm

/-- The concrete underived residual function. It is solidification
precomposition transported through the exact P2-D sheaf/presheaf and
closed-monoidal equivalences. Keeping this as an ordinary function makes the
residual mathematical obligation exactly bijectivity of this map. -/
noncomputable def dualPrecomp (S X : Profinite.{u}) :
    DualTensorHom S ((Condensed.profiniteSolid R).obj X) →
      DualTensorHom S ((Condensed.profiniteFree R).obj X) :=
  fun φ =>
    measureHomDualityEquiv S ((Condensed.profiniteFree R).obj X)
      (solidification X ≫
        (measureHomDualityEquiv S ((Condensed.profiniteSolid R).obj X)).symm φ)

/-- The same residual function explicitly promoted to a morphism in the
category `Type`, avoiding any accidental inference of structure from the Hom
objects themselves. -/
noncomputable def dualPrecompType (S X : Profinite.{u}) :
    DualTensorHom S ((Condensed.profiniteSolid R).obj X) ⟶
      DualTensorHom S ((Condensed.profiniteFree R).obj X) :=
  TypeCat.ofHom (dualPrecomp S X)

/-- Yoneda precomposition is definitionally ordinary categorical
precomposition on the underlying Hom type. -/
theorem measurePrecomp_apply (S X : Profinite.{u})
    (g : (Condensed.profiniteSolid R).obj X ⟶
      CMDG.CondensedCM4P2D.measureFunctor.obj S) :
    measurePrecomp S X g = solidification X ≫ g := by
  rfl

/-- C2 commuting statement: the actual measure-target Yoneda map and the
explicit P2-D tensor-Hom residual function are conjugate by
`measureHomDualityEquiv`. This identifies the residual underived theorem
without proving it. -/
theorem dualPrecomp_measurePrecomp_commutes (S X : Profinite.{u})
    (g : (Condensed.profiniteSolid R).obj X ⟶
      CMDG.CondensedCM4P2D.measureFunctor.obj S) :
    dualPrecomp S X
        (measureHomDualityEquiv S ((Condensed.profiniteSolid R).obj X) g) =
      measureHomDualityEquiv S ((Condensed.profiniteFree R).obj X)
        (measurePrecomp S X g) := by
  rw [measurePrecomp_apply]
  simp [dualPrecomp]

/-- Categorical isomorphism in `Type` associated to the protected P2-D Hom
equivalence. -/
noncomputable def measureHomDualityIso (S : Profinite.{u}) (F : CondensedMod.{u} R) :
    MeasureHom S F ≅ DualTensorHom S F :=
  (measureHomDualityEquiv S F).toIso

/-- C3 categorical square in `Type`: actual measure-target precomposition is
conjugate to the explicitly promoted residual function by the P2-D Hom
isomorphisms. -/
theorem dualPrecompType_measurePrecomp_square (S X : Profinite.{u}) :
    measurePrecomp S X ≫
        (measureHomDualityIso S ((Condensed.profiniteFree R).obj X)).hom =
      (measureHomDualityIso S ((Condensed.profiniteSolid R).obj X)).hom ≫
        dualPrecompType S X := by
  apply TypeCat.homEquiv.injective
  funext g
  exact (dualPrecomp_measurePrecomp_commutes S X g).symm

/-- The explicitly promoted residual Type morphism is an isomorphism exactly
when the actual measure-target Yoneda precomposition map is an isomorphism. -/
theorem dualPrecompType_isIso_iff_measurePrecomp (S X : Profinite.{u}) :
    IsIso (dualPrecompType S X) ↔ IsIso (measurePrecomp S X) := by
  constructor
  · intro h
    letI : IsIso (dualPrecompType S X) := h
    haveI : IsIso
        (measurePrecomp S X ≫
          (measureHomDualityIso S ((Condensed.profiniteFree R).obj X)).hom) := by
      rw [dualPrecompType_measurePrecomp_square S X]
      infer_instance
    exact IsIso.of_isIso_comp_right
      (measurePrecomp S X)
      (measureHomDualityIso S ((Condensed.profiniteFree R).obj X)).hom
  · intro h
    letI : IsIso (measurePrecomp S X) := h
    haveI : IsIso
        ((measureHomDualityIso S ((Condensed.profiniteSolid R).obj X)).hom ≫
          dualPrecompType S X) := by
      rw [← dualPrecompType_measurePrecomp_square S X]
      infer_instance
    exact IsIso.of_isIso_comp_left
      (measureHomDualityIso S ((Condensed.profiniteSolid R).obj X)).hom
      (dualPrecompType S X)

/-- Conjugacy-induced bridge requested by P3-C: bijectivity of the residual
ordinary function is exactly categorical `IsIso` of the actual measure-target
Yoneda map. -/
theorem dualPrecomp_bijective_iff_measurePrecomp_isIso (S X : Profinite.{u}) :
    Function.Bijective (dualPrecomp S X) ↔ IsIso (measurePrecomp S X) := by
  calc
    Function.Bijective (dualPrecomp S X) ↔ IsIso (dualPrecompType S X) := by
      simpa [dualPrecompType] using
        (CategoryTheory.bijective_iff_isIso_ofHom (dualPrecomp S X))
    _ ↔ IsIso (measurePrecomp S X) :=
      dualPrecompType_isIso_iff_measurePrecomp S X

/-- Pointwise exact reduction from residual tensor-Hom bijectivity to the actual
pinned solidity precomposition map. -/
theorem dualPrecomp_bijective_iff_solidPrecomp (S X : Profinite.{u}) :
    Function.Bijective (dualPrecomp S X) ↔ IsIso (solidPrecomp S X) :=
  (dualPrecomp_bijective_iff_measurePrecomp_isIso S X).trans
    (measurePrecomp_isIso_iff_solidPrecomp S X)

/-- The exact residual underived theorem identified by P3-C. This proposition is
not proved by this fixture. -/
def ResidualHomTheorem (S : Profinite.{u}) : Prop :=
  ∀ X : Profinite.{u}, Function.Bijective (dualPrecomp S X)

/-- Proving the residual underived theorem would discharge the actual pinned
module-level solidity predicate for the chosen `S`. -/
theorem isSolid_of_residualHomTheorem (S : Profinite.{u})
    (h : ResidualHomTheorem S) :
    CondensedMod.IsSolid R ((Condensed.profiniteSolid R).obj S) := by
  apply isSolid_of_measurePrecomp_isIso S
  intro X
  exact (dualPrecomp_bijective_iff_measurePrecomp_isIso S X).mp (h X)

/-- C3 terminal reduction: the residual tensor-Hom bijectivity theorem is
logically identical to the actual pinned `CondensedMod.IsSolid` obligation. No
inhabitant of either side is constructed here. -/
theorem residualHomTheorem_iff_isSolid (S : Profinite.{u}) :
    ResidualHomTheorem S ↔
      CondensedMod.IsSolid R ((Condensed.profiniteSolid R).obj S) := by
  constructor
  · exact isSolid_of_residualHomTheorem S
  · intro h
    change ∀ X : Profinite.{u}, Function.Bijective (dualPrecomp S X)
    intro X
    apply (dualPrecomp_bijective_iff_solidPrecomp S X).mpr
    simpa [solidPrecomp, solidification] using h.isIso_solidification_map X

#check targetIso
#check targetYonedaIso
#check precomp_naturality
#check measurePrecomp_isIso_iff_solidPrecomp
#check isSolid_of_measurePrecomp_isIso
#check CategoryTheory.Sheaf.homEquiv
#check MeasureHom
#check UnderlyingPresheaf
#check DualTensorObj
#check DualTensorHom
#check measureHomDualityEquiv
#check dualPrecomp
#check dualPrecompType
#check measurePrecomp_apply
#check dualPrecomp_measurePrecomp_commutes
#check measureHomDualityIso
#check dualPrecompType_measurePrecomp_square
#check dualPrecompType_isIso_iff_measurePrecomp
#check dualPrecomp_bijective_iff_measurePrecomp_isIso
#check dualPrecomp_bijective_iff_solidPrecomp
#check ResidualHomTheorem
#check isSolid_of_residualHomTheorem
#check residualHomTheorem_iff_isSolid

#print axioms precomp_naturality
#print axioms measurePrecomp_isIso_iff_solidPrecomp
#print axioms isSolid_of_measurePrecomp_isIso
#print axioms measureHomDualityEquiv
#print axioms dualPrecomp_measurePrecomp_commutes
#print axioms dualPrecompType_measurePrecomp_square
#print axioms dualPrecompType_isIso_iff_measurePrecomp
#print axioms dualPrecomp_bijective_iff_measurePrecomp_isIso
#print axioms dualPrecomp_bijective_iff_solidPrecomp
#print axioms isSolid_of_residualHomTheorem
#print axioms residualHomTheorem_iff_isSolid

end CMDG.CondensedCM4P3C