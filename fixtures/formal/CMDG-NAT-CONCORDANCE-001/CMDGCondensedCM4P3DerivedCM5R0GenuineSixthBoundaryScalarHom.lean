import CMDGCondensedCM4P3DerivedCM5R0GenuineSeventhCechFaces
import CMDGCondensedCM4P3DerivedCM5R0ExplicitClosedProductH5HomBridge
import CMDGCondensedCM4P3DerivedCM5R0GenuineFifthBoundaryScalarHom

/-! Actual six-face free condensed Čech Hom differential:
transport genuine sixfold/six-face continuous Profinite maps into
locally constant scalar and arbitrary categorical product coefficients.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem stoneanCechSixthBoundary_integer_scalar
    (T : Profinite.{u})
    (g : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶ discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T)
      (stoneanCechSixthBoundary T ≫ g) =
    (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g).comap
        (sextupleFace0 T).hom.hom
    - (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g).comap
        (sextupleFace1 T).hom.hom
    + (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g).comap
        (sextupleFace2 T).hom.hom
    - (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g).comap
        (sextupleFace3 T).hom.hom
    + (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g).comap
        (sextupleFace4 T).hom.hom
    - (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g).comap
        (sextupleFace5 T).hom.hom := by
  unfold stoneanCechSixthBoundary
  rw [Preadditive.sub_comp, Preadditive.add_comp,
    Preadditive.sub_comp, Preadditive.add_comp, Preadditive.sub_comp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_sub,
    freeProfiniteDiscreteIntegerHomScalarEquiv_add,
    freeProfiniteDiscreteIntegerHomScalarEquiv_sub,
    freeProfiniteDiscreteIntegerHomScalarEquiv_add,
    freeProfiniteDiscreteIntegerHomScalarEquiv_sub]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]

theorem stoneanCechSixthBoundary_product_scalar_atPoint
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (g : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (i : ι) (r : stoneanCechExplicitSextupleProfinite T) :
    (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitSextupleProfinite T)
      (stoneanCechSixthBoundary T ≫ g) i) r =
    (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuintupleProfinite T) g i)
        ((sextupleFace0 T).hom.hom r)
    - (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuintupleProfinite T) g i)
        ((sextupleFace1 T).hom.hom r)
    + (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuintupleProfinite T) g i)
        ((sextupleFace2 T).hom.hom r)
    - (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuintupleProfinite T) g i)
        ((sextupleFace3 T).hom.hom r)
    + (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuintupleProfinite T) g i)
        ((sextupleFace4 T).hom.hom r)
    - (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuintupleProfinite T) g i)
        ((sextupleFace5 T).hom.hom r) := by
  have h := congrArg (fun F : LocallyConstant
      (stoneanCechExplicitSextupleProfinite T) ℤ => F r)
    (stoneanCechSixthBoundary_integer_scalar T
      (g ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i))
  simpa [freeProfiniteDiscreteProductHomScalarEquiv,
    Category.assoc, LocallyConstant.sub_apply,
    LocallyConstant.add_apply] using h

#print axioms stoneanCechSixthBoundary_product_scalar_atPoint
end CMDG.CondensedCM5R0
