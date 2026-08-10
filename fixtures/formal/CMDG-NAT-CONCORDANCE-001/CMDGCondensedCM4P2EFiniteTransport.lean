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

abbrev R := CMDG.CondensedCM4P2D.R.{u}
abbrev PresheafModule := CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} R

noncomputable abbrev coefficientPresheaf : PresheafModule :=
  CMDG.CondensedCM4P2D.coefficientPresheaf

/-- The discrete presheaf attached to the ordinary finite function module `X.obj → R`. -/
noncomputable abbrev finiteFunctionPresheaf (X : FintypeCat.{u}) : PresheafModule :=
  (CondensedMod.LocallyConstant.functorToPresheaves R).obj
    (ModuleCat.of R (X.obj → R))

/-- A finite family of copies of the coefficient presheaf, written pointwise. -/
noncomputable def finiteCoefficientFamilyPresheaf (X : FintypeCat.{u}) : PresheafModule where
  obj S := ModuleCat.of R (X.obj → LocallyConstant S.unop R)
  map f := ModuleCat.ofHom
    { toFun := fun a x => coefficientPresheaf.map f (a x)
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
    LocallyConstant S (X.obj → R) ≃ₗ[R] (X.obj → LocallyConstant S R) where
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
        ModuleCat.of R (LocallyConstant S.unop (X.obj → R)) ≅
          ModuleCat.of R (X.obj → LocallyConstant S.unop R)
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
    (CondensedMod.LocallyConstant.functorToPresheaves R).obj
        (CMDG.CondensedCM4P2D.continuousFunctions.obj
          (op (FintypeCat.toProfinite.obj X))) ≅
      (CondensedMod.LocallyConstant.functorToPresheaves R).obj
        (ModuleCat.of R (X.obj → R))
  exact
    (CondensedMod.LocallyConstant.functorToPresheaves R).mapIso
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
