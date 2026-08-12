import CMDGCondensedCM4P3D
import CMDGCondensedCM4P2EE2

/-!
# CMDG CM4-P3-E — canonical finite-limit reduction

This stacked successor to P3-D removes the remaining objectwise-product
hypothesis without choosing a Nöbeling basis. The protected P2-E finite
comparison already identifies each finite value of the measure functor with a
finite family of copies of the coefficient object, and protected E2 already
identifies every profinite value as the limit of those finite values.

The only hypothesis retained by the terminal theorem is solidity of the single
discrete lifted-integral coefficient object. No coefficient-solidity theorem
is asserted here, so P3 remains blocking.
-/

namespace CMDG.CondensedCM4P3E

universe u

open CategoryTheory Limits Opposite

abbrev R := CMDG.CondensedCM4P2D.R.{u}

/-- The explicit finite coefficient-family presheaf from protected P2-E is a
sheaf. This is transported across the already-certified finite family/free
isomorphism to the existing finite small-free condensed module. -/
theorem finiteCoefficientFamilyPresheaf_isSheaf (X : FintypeCat.{u}) :
    Presheaf.IsSheaf (coherentTopology CompHaus.{u})
      (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X) := by
  rw [Presheaf.isSheaf_of_iso_iff
    (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyFreeIso X)]
  exact
    (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedFunctor.obj X).property

/-- The finite coefficient family as an actual condensed module. -/
noncomputable def finiteCoefficientFamilyCondensed (X : FintypeCat.{u}) :
    CondensedMod.{u} R where
  obj := CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X
  property := finiteCoefficientFamilyPresheaf_isSheaf X

/-- Coordinate projection from the finite coefficient family to the single
coefficient object. -/
noncomputable def finiteCoefficientFamilyProjection
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteCoefficientFamilyCondensed X ⟶
      CMDG.CondensedCM4P3D.coefficientObject.{u} :=
  ObjectProperty.homMk
    (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoordinateProjection X x)

/-- The explicit product cone on the finite family of coefficient objects. -/
noncomputable def finiteCoefficientFamilyCone (X : FintypeCat.{u}) :
    Fan (fun _ : X.obj => CMDG.CondensedCM4P3D.coefficientObject.{u}) :=
  Fan.mk (finiteCoefficientFamilyCondensed X)
    (finiteCoefficientFamilyProjection X)

/-- Given any cone over the coefficient family, assemble its component maps
sectionwise into a morphism to the explicit family object. -/
noncomputable def finiteCoefficientFamilyLift
    (X : FintypeCat.{u})
    (s : Fan (fun _ : X.obj => CMDG.CondensedCM4P3D.coefficientObject.{u})) :
    s.pt ⟶ finiteCoefficientFamilyCondensed X :=
  ObjectProperty.homMk
    { app := fun S => ModuleCat.ofHom
        { toFun := fun a x => (s.proj x).hom.app S a
          map_add' := by
            intro a b
            funext x
            change
              (ConcreteCategory.hom ((s.proj x).hom.app S)) (a + b) =
                (ConcreteCategory.hom ((s.proj x).hom.app S)) a +
                  (ConcreteCategory.hom ((s.proj x).hom.app S)) b
            exact (ConcreteCategory.hom ((s.proj x).hom.app S)).map_add a b
          map_smul' := by
            intro r a
            funext x
            change
              (ConcreteCategory.hom ((s.proj x).hom.app S)) (r • a) =
                r • (ConcreteCategory.hom ((s.proj x).hom.app S)) a
            exact (ConcreteCategory.hom ((s.proj x).hom.app S)).map_smul r a }
      naturality := by
        intro S T f
        apply ModuleCat.hom_ext
        apply LinearMap.ext
        intro a
        funext x
        change
          ((s.proj x).hom.app S ≫
              CMDG.CondensedCM4P2D.coefficientPresheaf.map f) a =
            (s.pt.obj.map f ≫ (s.proj x).hom.app T) a
        rw [← (s.proj x).hom.naturality f] }

/-- The explicit finite coefficient-family cone satisfies the categorical
product universal property in `CondensedMod`. -/
noncomputable def finiteCoefficientFamilyConeIsLimit (X : FintypeCat.{u}) :
    IsLimit (finiteCoefficientFamilyCone X) :=
  Fan.IsLimit.mk _ (finiteCoefficientFamilyLift X)
    (by
      intro s x
      apply ObjectProperty.hom_ext
      apply NatTrans.ext'
      funext S
      apply ModuleCat.hom_ext
      apply LinearMap.ext
      intro a
      rfl)
    (by
      intro s m hm
      apply ObjectProperty.hom_ext
      apply NatTrans.ext'
      funext S
      apply ModuleCat.hom_ext
      apply LinearMap.ext
      intro a
      funext x
      have h := congrArg (fun q => q.hom.app S) (hm x)
      have h' := congrArg (fun q => q a) h
      simpa [finiteCoefficientFamilyCone, finiteCoefficientFamilyProjection,
        finiteCoefficientFamilyLift] using h')

/-- Lift the protected finite family/free presheaf isomorphism to condensed
modules. -/
noncomputable def finiteCoefficientFamilySmallFreeIso (X : FintypeCat.{u}) :
    finiteCoefficientFamilyCondensed X ≅
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedFunctor.obj X :=
  ObjectProperty.isoMk
    (Presheaf.IsSheaf (coherentTopology CompHaus.{u}))
    (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteCoefficientFamilyFreeIso X)

/-- If the single coefficient object is solid, the explicit finite coefficient
family is solid by the P3-D closure of solid objects under limits. -/
theorem finiteCoefficientFamily_isSolid_of_coefficient
    (X : FintypeCat.{u})
    (hCoeff : CondensedMod.IsSolid R
      CMDG.CondensedCM4P3D.coefficientObject.{u}) :
    CondensedMod.IsSolid R (finiteCoefficientFamilyCondensed X) := by
  apply CMDG.CondensedCM4P3D.isSolid_of_isLimit.{u, u}
    (Discrete.functor
      (fun _ : X.obj => CMDG.CondensedCM4P3D.coefficientObject.{u}))
    (finiteCoefficientFamilyCone X)
    (finiteCoefficientFamilyConeIsLimit X)
  intro _
  exact hCoeff

/-- The protected finite small-free condensed module is solid whenever the
single coefficient object is solid. -/
theorem finiteSmallFree_isSolid_of_coefficient
    (X : FintypeCat.{u})
    (hCoeff : CondensedMod.IsSolid R
      CMDG.CondensedCM4P3D.coefficientObject.{u}) :
    CondensedMod.IsSolid R
      (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteSmallFreeCondensedFunctor.obj X) := by
  exact CMDG.CondensedCM4P3D.isSolid_of_iso.{u}
    (finiteCoefficientFamilySmallFreeIso X)
    (finiteCoefficientFamily_isSolid_of_coefficient X hCoeff)

/-- Each finite value of the protected measure functor is solid under the
single coefficient-solidity hypothesis. -/
theorem finiteMeasure_isSolid_of_coefficient
    (X : FintypeCat.{u})
    (hCoeff : CondensedMod.IsSolid R
      CMDG.CondensedCM4P3D.coefficientObject.{u}) :
    CondensedMod.IsSolid R (CMDG.CondensedCM4P2E.finiteMeasure.obj X) := by
  exact CMDG.CondensedCM4P3D.isSolid_of_iso.{u}
    (CMDG.CondensedCM4P2E.FiniteDualTransport.finiteMeasureSmallFreeCondensedIso X).symm
    (finiteSmallFree_isSolid_of_coefficient X hCoeff)

/-- Protected E2 now removes every remaining profinite product-presentation
hypothesis: a profinite value is the limit of its finite quotient values, and
P3-D proves solidity is closed under that limit. -/
theorem measureFunctor_isSolid_of_coefficient
    (S : Profinite.{u})
    (hCoeff : CondensedMod.IsSolid R
      CMDG.CondensedCM4P3D.coefficientObject.{u}) :
    CondensedMod.IsSolid R (CMDG.CondensedCM4P2D.measureFunctor.obj S) := by
  apply CMDG.CondensedCM4P3D.isSolid_of_isLimit.{u, u}
    (S.diagram ⋙ CMDG.CondensedCM4P2D.measureFunctor)
    (CMDG.CondensedCM4P2D.measureFunctor.mapCone S.asLimitCone)
    (CMDG.CondensedCM4P2E.RightKanReconstruction.measureFunctorMapConeIsLimit S)
  intro j
  change CondensedMod.IsSolid R
    (CMDG.CondensedCM4P2E.finiteMeasure.obj (S.fintypeDiagram.obj j))
  exact finiteMeasure_isSolid_of_coefficient (S.fintypeDiagram.obj j) hCoeff

/-- Transport the canonical measure-side limit result through protected P2-E
canonical right-Kan uniqueness. -/
theorem profiniteSolid_isSolid_of_coefficient
    (S : Profinite.{u})
    (hCoeff : CondensedMod.IsSolid R
      CMDG.CondensedCM4P3D.coefficientObject.{u}) :
    CondensedMod.IsSolid R ((Condensed.profiniteSolid R).obj S) := by
  exact CMDG.CondensedCM4P3D.isSolid_of_iso.{u}
    (CMDG.CondensedCM4P3C.targetIso S)
    (measureFunctor_isSolid_of_coefficient S hCoeff)

/-- The P3-C residual theorem for every profinite `S` now follows from the
single coefficient-solidity theorem, with no chosen basis or objectwise
product-presentation hypothesis. -/
theorem residualHomTheorem_of_coefficientSolid
    (S : Profinite.{u})
    (hCoeff : CondensedMod.IsSolid R
      CMDG.CondensedCM4P3D.coefficientObject.{u}) :
    CMDG.CondensedCM4P3C.ResidualHomTheorem S := by
  apply (CMDG.CondensedCM4P3C.residualHomTheorem_iff_isSolid S).mpr
  exact profiniteSolid_isSolid_of_coefficient S hCoeff

/-- Equivalent terminal reduction stated in the exact P3-D coefficient Hom
language. This is not a proof of the coefficient theorem itself. -/
theorem residualHomTheorem_of_coefficientResidual
    (S : Profinite.{u})
    (hCoeff : CMDG.CondensedCM4P3D.CoefficientResidualHomTheorem.{u}) :
    CMDG.CondensedCM4P3C.ResidualHomTheorem S := by
  apply residualHomTheorem_of_coefficientSolid S
  exact CMDG.CondensedCM4P3D.coefficientResidualHomTheorem_iff_isSolid.{u}.mp hCoeff

#check finiteCoefficientFamilyPresheaf_isSheaf
#check finiteCoefficientFamilyCondensed
#check finiteCoefficientFamilyCone
#check finiteCoefficientFamilyConeIsLimit
#check finiteMeasure_isSolid_of_coefficient
#check measureFunctor_isSolid_of_coefficient
#check profiniteSolid_isSolid_of_coefficient
#check residualHomTheorem_of_coefficientResidual

#print axioms finiteCoefficientFamilyConeIsLimit
#print axioms finiteMeasure_isSolid_of_coefficient
#print axioms measureFunctor_isSolid_of_coefficient
#print axioms profiniteSolid_isSolid_of_coefficient
#print axioms residualHomTheorem_of_coefficientResidual

end CMDG.CondensedCM4P3E
