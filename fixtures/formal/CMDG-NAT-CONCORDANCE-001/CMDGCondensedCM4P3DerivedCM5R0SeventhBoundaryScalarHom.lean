import CMDGCondensedCM4P3DerivedCM5R0GenuineSixthBoundaryScalarHom

/-! Genuine seven-face Čech boundary scalar and product morphisms. -/
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem stoneanCechSeventhBoundary_integer_scalar
    (T : Profinite.{u})
    (g : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitSextupleProfinite T)) ⟶ discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitSeptupleProfinite T)
      (stoneanCechSeventhBoundary T ≫ g) =
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g).comap
      (septupleFace0 T).hom.hom
    - (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g).comap
      (septupleFace1 T).hom.hom
    + (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g).comap
      (septupleFace2 T).hom.hom
    - (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g).comap
      (septupleFace3 T).hom.hom
    + (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g).comap
      (septupleFace4 T).hom.hom
    - (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g).comap
      (septupleFace5 T).hom.hom
    + (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g).comap
      (septupleFace6 T).hom.hom := by
  unfold stoneanCechSeventhBoundary
  rw [Preadditive.add_comp, Preadditive.sub_comp,
    Preadditive.add_comp, Preadditive.sub_comp,
    Preadditive.add_comp, Preadditive.sub_comp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_add,
    freeProfiniteDiscreteIntegerHomScalarEquiv_sub,
    freeProfiniteDiscreteIntegerHomScalarEquiv_add,
    freeProfiniteDiscreteIntegerHomScalarEquiv_sub,
    freeProfiniteDiscreteIntegerHomScalarEquiv_add,
    freeProfiniteDiscreteIntegerHomScalarEquiv_sub]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]

theorem stoneanCechSeventhBoundary_product_scalar_atPoint
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (g : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitSextupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (i : ι) (r : stoneanCechExplicitSeptupleProfinite T) :
    (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSeptupleProfinite T)
      (stoneanCechSeventhBoundary T ≫ g) i) r =
    (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g i)
        ((septupleFace0 T).hom.hom r)
    - (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g i)
        ((septupleFace1 T).hom.hom r)
    + (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g i)
        ((septupleFace2 T).hom.hom r)
    - (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g i)
        ((septupleFace3 T).hom.hom r)
    + (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g i)
        ((septupleFace4 T).hom.hom r)
    - (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g i)
        ((septupleFace5 T).hom.hom r)
    + (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T) g i)
        ((septupleFace6 T).hom.hom r) := by
  have h := congrArg (fun F : LocallyConstant
      (stoneanCechExplicitSeptupleProfinite T) ℤ => F r)
    (stoneanCechSeventhBoundary_integer_scalar T
      (g ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i))
  simpa [freeProfiniteDiscreteProductHomScalarEquiv,
    Category.assoc, LocallyConstant.sub_apply,
    LocallyConstant.add_apply] using h

#print axioms stoneanCechSeventhBoundary_product_scalar_atPoint
end CMDG.CondensedCM5R0
