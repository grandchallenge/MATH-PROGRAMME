import CMDGCondensedCM4P2ERankOneNaturalIso

/-!
# CMDG CM4-P2-E finite comparison transport

This auxiliary fixture begins the transport-only closure of E1 after certification of the
rank-one internal-Hom natural isomorphism. It first decomposes the discrete finite-function
presheaf canonically as a finite family of copies of the coefficient presheaf.

No finite measure/free comparison, right-Kan-extension claim, or P2-E global equivalence is
asserted in this checkpoint.
-/

namespace CMDG.CondensedCM4P2E.FiniteTransport

universe u

open CategoryTheory Opposite

attribute [local instance] FintypeCat.fintype

/-- The discrete presheaf attached to the ordinary finite function module `X.obj → R`. -/
noncomputable abbrev finiteFunctionPresheaf (X : FintypeCat.{u}) :
    CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u} :=
  (CondensedMod.LocallyConstant.functorToPresheaves CMDG.CondensedCM4P2D.R.{u}).obj
    (ModuleCat.of CMDG.CondensedCM4P2D.R.{u}
      (X.obj → CMDG.CondensedCM4P2D.R.{u}))

/-- A finite family of copies of the coefficient presheaf, written pointwise. -/
noncomputable def finiteCoefficientFamilyPresheaf (X : FintypeCat.{u}) :
    CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u} where
  obj S := ModuleCat.of CMDG.CondensedCM4P2D.R.{u}
    (X.obj → LocallyConstant S.unop CMDG.CondensedCM4P2D.R.{u})
  map f := ModuleCat.ofHom
    { toFun := fun a x =>
        CMDG.CondensedCM4P2D.coefficientPresheaf.map f (a x)
      map_add' := by
        intro a b
        funext x
        rfl
      map_smul' := by
        intro c a
        funext x
        rfl }
  map_id S := by
    apply ModuleCat.hom_ext
    ext a x s
    rfl
  map_comp f g := by
    apply ModuleCat.hom_ext
    ext a x s
    rfl

/-- For finite `X`, locally constant maps into `X.obj → R` are canonically finite families of
locally constant `R`-valued maps. -/
noncomputable def locallyConstantPiLinearEquiv
    (S : CompHaus.{u}) (X : FintypeCat.{u}) :
    LocallyConstant S (X.obj → CMDG.CondensedCM4P2D.R.{u}) ≃ₗ[
      CMDG.CondensedCM4P2D.R.{u}]
      (X.obj → LocallyConstant S CMDG.CondensedCM4P2D.R.{u}) where
  toFun f := f.flip
  invFun f := LocallyConstant.unflip f
  left_inv f := LocallyConstant.unflip_flip f
  right_inv f := LocallyConstant.flip_unflip f
  map_add' f g := by
    funext x
    rfl
  map_smul' c f := by
    funext x
    rfl

/-- The finite product decomposition is natural in the compact-Hausdorff test object. -/
noncomputable def finiteFunctionPresheafFamilyIso (X : FintypeCat.{u}) :
    finiteFunctionPresheaf X ≅ finiteCoefficientFamilyPresheaf X :=
  NatIso.ofComponents
    (fun S => by
      change
        ModuleCat.of CMDG.CondensedCM4P2D.R.{u}
            (LocallyConstant S.unop (X.obj → CMDG.CondensedCM4P2D.R.{u})) ≅
          ModuleCat.of CMDG.CondensedCM4P2D.R.{u}
            (X.obj → LocallyConstant S.unop CMDG.CondensedCM4P2D.R.{u})
      exact (locallyConstantPiLinearEquiv S.unop X).toModuleIso)
    (by
      intro S T f
      apply ModuleCat.hom_ext
      ext h x s
      rfl)

/-- Transport the already-certified finite continuous-function comparison through the
locally-constant/discrete presheaf functor. -/
noncomputable def finiteDiscreteContinuousPresheafIso (X : FintypeCat.{u}) :
    CMDG.CondensedCM4P2D.discreteContinuousPresheaf.obj
        (op (FintypeCat.toProfinite.obj X)) ≅
      finiteFunctionPresheaf X := by
  change
    (CondensedMod.LocallyConstant.functorToPresheaves
        CMDG.CondensedCM4P2D.R.{u}).obj
        (CMDG.CondensedCM4P2D.continuousFunctions.obj
          (op (FintypeCat.toProfinite.obj X))) ≅
      (CondensedMod.LocallyConstant.functorToPresheaves
        CMDG.CondensedCM4P2D.R.{u}).obj
        (ModuleCat.of CMDG.CondensedCM4P2D.R.{u}
          (X.obj → CMDG.CondensedCM4P2D.R.{u}))
  exact
    (CondensedMod.LocallyConstant.functorToPresheaves
      CMDG.CondensedCM4P2D.R.{u}).mapIso
      (CMDG.CondensedCM4P2E.finiteContinuousFunctionsIso X)

/-- Canonical source decomposition for the finite E1 transport. -/
noncomputable def finiteDiscreteContinuousPresheafFamilyIso (X : FintypeCat.{u}) :
    CMDG.CondensedCM4P2D.discreteContinuousPresheaf.obj
        (op (FintypeCat.toProfinite.obj X)) ≅
      finiteCoefficientFamilyPresheaf X :=
  finiteDiscreteContinuousPresheafIso X ≪≫ finiteFunctionPresheafFamilyIso X

#check finiteFunctionPresheaf
#check finiteCoefficientFamilyPresheaf
#check locallyConstantPiLinearEquiv
#check finiteFunctionPresheafFamilyIso
#check finiteDiscreteContinuousPresheafIso
#check finiteDiscreteContinuousPresheafFamilyIso

#print axioms locallyConstantPiLinearEquiv
#print axioms finiteFunctionPresheafFamilyIso
#print axioms finiteDiscreteContinuousPresheafIso
#print axioms finiteDiscreteContinuousPresheafFamilyIso

end CMDG.CondensedCM4P2E.FiniteTransport
