import CMDGCondensedCM4P3DerivedCM5R0DiscreteCoefficientCechBridge
import Mathlib.Condensed.Limits
import Mathlib.CategoryTheory.Limits.Shapes.Products

/-!
# CM5: exact categorical product-of-discrete-sections comparison

For arbitrary profinite X and an arbitrary index type, the actual
condensed-module Hom set from F_X into a categorical product of the
discrete lifted-integer coefficient object is equivalent to an indexed
family of locally constant integer functions on X.

This directly uses the categorical product's universal property and
the genuine degree-zero discrete coefficient comparison.  The family
does NOT need a common finite quotient of X.  In particular, do not
mistake it for LocallyConstant X (ι → ℤ) with a discrete codomain.

The conditional application to G_S is formulated with an explicit
isomorphism e : G_S ≅ ∏ discreteIntegerCoeff.  This module does not
construct e; that remains a separate substantive CM5 obligation.
No Ext or derived solidity is claimed.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The pinned lifted-integer coefficient function space and ordinary
integer-valued locally constant functions are equivalent by ULift. -/
noncomputable def liftedIntegerLocallyConstantEquiv
    (X : Profinite.{u}) :
    LocallyConstant X Coeff ≃ LocallyConstant X ℤ where
  toFun f := f.map ULift.down
  invFun f := f.map ULift.up
  left_inv f := by
    ext x
    rfl
  right_inv f := by
    ext x
    rfl

/-- Exact scalar representation of genuine condensed-module morphisms
from F_X to the *discrete* integral coefficient sheaf. -/
noncomputable def freeProfiniteDiscreteIntegerHomScalarEquiv
    (X : Profinite.{u}) :
    (((Condensed.profiniteFree Coeff).obj X) ⟶
      discreteIntegerCoeff) ≃ LocallyConstant X ℤ :=
  (freeProfiniteDiscreteIntegerHomEquiv X).trans
    (liftedIntegerLocallyConstantEquiv X)

/-- For every profinite X and arbitrary (potentially infinite) ι,
actual morphisms F_X → ∏ᶜ Z_disc are precisely ι-indexed families
of locally constant scalar functions on X.  No uniform discrete
finite observation is required by this theorem. -/
noncomputable def freeProfiniteDiscreteProductHomScalarEquiv
    (X : Profinite.{u}) {ι : Type (u + 1)} :
    (((Condensed.profiniteFree Coeff).obj X) ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) ≃
        (ι → LocallyConstant X ℤ) where
  toFun f i :=
    (freeProfiniteDiscreteIntegerHomScalarEquiv X)
      (f ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i)
  invFun a :=
    Pi.lift (fun i =>
      (freeProfiniteDiscreteIntegerHomScalarEquiv X).symm (a i))
  left_inv f := by
    apply Pi.hom_ext
    intro i
    simp
  right_inv a := by
    funext i
    simp

/-- If the actual solid target G_S admits a given categorical
product presentation by discrete lifted integers, its genuine
free-profinite morphism space has the corresponding scalar-family
description. This is conditional on the explicitly supplied model
e and does not construct or assume one globally. -/
noncomputable def freeProfiniteSolidHomScalarFamilyEquiv_of_productModel
    (X S : Profinite.{u}) {ι : Type (u + 1)}
    (e : underivedObject S ≅
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) :
    (((Condensed.profiniteFree Coeff).obj X) ⟶
      underivedObject S) ≃ (ι → LocallyConstant X ℤ) where
  toFun f :=
    (freeProfiniteDiscreteProductHomScalarEquiv X) (f ≫ e.hom)
  invFun b :=
    (freeProfiniteDiscreteProductHomScalarEquiv X).symm b ≫ e.inv
  left_inv f := by
    change ((freeProfiniteDiscreteProductHomScalarEquiv X).symm
      ((freeProfiniteDiscreteProductHomScalarEquiv X)
        (f ≫ e.hom))) ≫ e.inv = f
    simp
  right_inv b := by
    change (freeProfiniteDiscreteProductHomScalarEquiv X)
      (((freeProfiniteDiscreteProductHomScalarEquiv X).symm b ≫
        e.inv) ≫ e.hom) = b
    simp

#print axioms liftedIntegerLocallyConstantEquiv
#print axioms freeProfiniteDiscreteIntegerHomScalarEquiv
#print axioms freeProfiniteDiscreteProductHomScalarEquiv
#print axioms freeProfiniteSolidHomScalarFamilyEquiv_of_productModel

end CMDG.CondensedCM5R0
