import CMDGCondensedCM4P3DerivedCM5R0ExplicitClosedProductH4HomBridge
import CMDGCondensedCM4P3DerivedCM5R0GenuineFifthCechBoundary
import CMDGCondensedCM4P3DerivedCM5R0GenuineFourthBoundaryScalarHom

/-!
# CM5 Ext⁴ — exact categorical fifth-boundary scalar Hom comparison

The fifth Čech boundary acts on the *actual* free condensed module
from the genuine closed five-point Profinite relation to the actual
fourfold categorical pullback. We transport that actual morphism
through the proved categorical fourth-pullback isomorphism.

The resulting five signed face maps are compared with continuous,
arbitrary-index product-valued scalar cochains. No fictitious
coefficient or pointwise-only replacement is used.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

noncomputable def stoneanCechExplicitFifthBoundary (T : Profinite.{u}) :
    ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
    ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuadrupleProfinite T)) :=
  (Condensed.profiniteFree Coeff).map (quintupleFace0 T) -
    (Condensed.profiniteFree Coeff).map (quintupleFace1 T) +
    (Condensed.profiniteFree Coeff).map (quintupleFace2 T) -
    (Condensed.profiniteFree Coeff).map (quintupleFace3 T) +
    (Condensed.profiniteFree Coeff).map (quintupleFace4 T)

theorem stoneanCechFifthBoundary_explicit_factor (T : Profinite.{u}) :
    stoneanCechFifthBoundary T =
      stoneanCechExplicitFifthBoundary T ≫
        (Condensed.profiniteFree Coeff).map
          (stoneanCechExplicitQuadrupleToAbstract T) := by
  unfold stoneanCechFifthBoundary stoneanCechExplicitFifthBoundary
    stoneanCechFifthFace0 stoneanCechFifthFace1
    stoneanCechFifthFace2 stoneanCechFifthFace3
    stoneanCechFifthFace4
  simp only [Preadditive.add_comp, Preadditive.sub_comp,
    ← Functor.map_comp]

theorem stoneanCechExplicitFifthBoundary_integer_scalar
    (T : Profinite.{u})
    (g : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuadrupleProfinite T)) ⟶ discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanCechExplicitQuintupleProfinite T)
      (stoneanCechExplicitFifthBoundary T ≫ g) =
      (((((freeProfiniteDiscreteIntegerHomScalarEquiv
          (stoneanCechExplicitQuadrupleProfinite T) g).comap
          (quintupleFace0 T).hom.hom -
        (freeProfiniteDiscreteIntegerHomScalarEquiv
          (stoneanCechExplicitQuadrupleProfinite T) g).comap
          (quintupleFace1 T).hom.hom) +
        (freeProfiniteDiscreteIntegerHomScalarEquiv
          (stoneanCechExplicitQuadrupleProfinite T) g).comap
          (quintupleFace2 T).hom.hom) -
        (freeProfiniteDiscreteIntegerHomScalarEquiv
          (stoneanCechExplicitQuadrupleProfinite T) g).comap
          (quintupleFace3 T).hom.hom) +
        (freeProfiniteDiscreteIntegerHomScalarEquiv
          (stoneanCechExplicitQuadrupleProfinite T) g).comap
          (quintupleFace4 T).hom.hom) := by
  unfold stoneanCechExplicitFifthBoundary
  rw [Preadditive.add_comp, Preadditive.sub_comp,
    Preadditive.add_comp, Preadditive.sub_comp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_add,
    freeProfiniteDiscreteIntegerHomScalarEquiv_sub,
    freeProfiniteDiscreteIntegerHomScalarEquiv_add,
    freeProfiniteDiscreteIntegerHomScalarEquiv_sub]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,
    freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]


/-- Real fifth boundary on product-valued condensed-module Hom,
coordinatewise at every true closed fivefold-relation point. -/
theorem stoneanCechExplicitFifthBoundary_product_scalar_atPoint
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (g : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuadrupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (i : ι) (r : stoneanCechExplicitQuintupleProfinite T) :
    (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuintupleProfinite T)
      (stoneanCechExplicitFifthBoundary T ≫ g) i) r =
    ((((freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuadrupleProfinite T) g i)
        ((quintupleFace0 T).hom.hom r) -
      (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuadrupleProfinite T) g i)
        ((quintupleFace1 T).hom.hom r)) +
      (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuadrupleProfinite T) g i)
        ((quintupleFace2 T).hom.hom r)) -
      (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuadrupleProfinite T) g i)
        ((quintupleFace3 T).hom.hom r)) +
      (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuadrupleProfinite T) g i)
        ((quintupleFace4 T).hom.hom r) := by
  have h := congrArg (fun F : LocallyConstant
      (stoneanCechExplicitQuintupleProfinite T) ℤ => F r)
    (stoneanCechExplicitFifthBoundary_integer_scalar T
      (g ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i))
  simpa [freeProfiniteDiscreteProductHomScalarEquiv,
    Category.assoc, LocallyConstant.sub_apply,
    LocallyConstant.add_apply] using h

#print axioms stoneanCechExplicitFifthBoundary_product_scalar_atPoint

private theorem quintupleFace0_atClosed (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (quintupleFace0 T).hom.hom r =
      (⟨(r.val.2.1,(r.val.2.2.1,
        (r.val.2.2.2.1,r.val.2.2.2.2))),
          ⟨r.property.2.1,r.property.2.2.1,r.property.2.2.2⟩⟩ :
            stoneanCechExplicitQuadrupleProfinite T) := by
  rfl

private theorem quintupleFace1_atClosed (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (quintupleFace1 T).hom.hom r =
      (⟨(r.val.1,(r.val.2.2.1,(r.val.2.2.2.1,r.val.2.2.2.2))),
        ⟨r.property.1.trans r.property.2.1,r.property.2.2.1,r.property.2.2.2⟩⟩ :
          stoneanCechExplicitQuadrupleProfinite T) := by
  rfl

private theorem quintupleFace2_atClosed (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (quintupleFace2 T).hom.hom r =
      (⟨(r.val.1,(r.val.2.1,(r.val.2.2.2.1,r.val.2.2.2.2))),
        ⟨r.property.1,r.property.2.1.trans r.property.2.2.1,r.property.2.2.2⟩⟩ :
          stoneanCechExplicitQuadrupleProfinite T) := by
  rfl

private theorem quintupleFace3_atClosed (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (quintupleFace3 T).hom.hom r =
      (⟨(r.val.1,(r.val.2.1,(r.val.2.2.1,r.val.2.2.2.2))),
        ⟨r.property.1,r.property.2.1,r.property.2.2.1.trans r.property.2.2.2⟩⟩ :
          stoneanCechExplicitQuadrupleProfinite T) := by
  rfl

private theorem quintupleFace4_atClosed (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (quintupleFace4 T).hom.hom r =
      (⟨(r.val.1,(r.val.2.1,(r.val.2.2.1,r.val.2.2.2.1))),
        ⟨r.property.1,r.property.2.1,r.property.2.2.1⟩⟩ :
          stoneanCechExplicitQuadrupleProfinite T) := by
  rfl


/-- The six-signed-face condition required for product-valued
genuine closed-quintuple H4. This is a condition on the actual Hom,
not an independent axiom or assumption of Ext4 vanishing. -/
def stoneanCechClosedProductSixCocycle
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) : Prop :=
  ∀ (i : ι)
      (x y z w v r : Stonean.toProfinite.obj T.presentation)
      (hxy : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y)
      (hyz : (Profinite.presentation.π T).hom.hom y =
        (Profinite.presentation.π T).hom.hom z)
      (hzw : (Profinite.presentation.π T).hom.hom z =
        (Profinite.presentation.π T).hom.hom w)
      (hwv : (Profinite.presentation.π T).hom.hom w =
        (Profinite.presentation.π T).hom.hom v)
      (hvr : (Profinite.presentation.π T).hom.hom v =
        (Profinite.presentation.π T).hom.hom r),
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) f i)
        ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩ -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) f i)
        ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩ +
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) f i)
        ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩ -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) f i)
        ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩ +
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) f i)
        ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩ -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) f i)
        ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ = 0

/-- Closed-fibre H4 vanishing transported all the way to equality
of actual free condensed-module Hom under the genuine fifth-point
alternating differential with explicit fourfold Profinite target. -/
theorem stoneanCechExplicitFifthBoundary_product_exact_ofClosedCocycle
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hc : stoneanCechClosedProductSixCocycle T f) :
    ∃ b : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuadrupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff),
      stoneanCechExplicitFifthBoundary T ≫ b = f := by
  classical
  obtain ⟨b,hb⟩ :=
    stoneanCechExplicitQuintuple_discreteProduct_H4_potential T f hc
  refine ⟨b, ?_⟩
  apply (freeProfiniteDiscreteProductHomScalarEquiv
    (stoneanCechExplicitQuintupleProfinite T)).injective
  funext i
  ext r
  have hxy := r.property.1
  have hyz := r.property.2.1
  have hzw := r.property.2.2.1
  have hwv := r.property.2.2.2
  have h := hb i r.val.1 r.val.2.1 r.val.2.2.1
    r.val.2.2.2.1 r.val.2.2.2.2 hxy hyz hzw hwv
  have hd :=
    stoneanCechExplicitFifthBoundary_product_scalar_atPoint T b i r
  rw [quintupleFace0_atClosed, quintupleFace1_atClosed,
    quintupleFace2_atClosed, quintupleFace3_atClosed,
    quintupleFace4_atClosed] at hd
  exact hd.trans h.symm

#print axioms stoneanCechExplicitFifthBoundary_product_exact_ofClosedCocycle

/-- Genuine categorical fifth-Čech H4 Hom exactness for arbitrary
discrete-integer product targets. The target of the fifth boundary
is the ACTUAL fourth iterated categorical Profinite pullback.
No surrogate closed-relation target or unverified comparison is used. -/
theorem stoneanCechFifthBoundary_product_exact_ofClosedCocycle
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hc : stoneanCechClosedProductSixCocycle T f) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff),
      stoneanCechFifthBoundary T ≫ g = f := by
  classical
  obtain ⟨b,hb⟩ :=
    stoneanCechExplicitFifthBoundary_product_exact_ofClosedCocycle
      T f hc
  let A := stoneanCechExplicitQuadrupleToAbstract T
  let B := stoneanCechCategoricalQuadrupleToExplicit T
  let g := (Condensed.profiniteFree Coeff).map B ≫ b
  refine ⟨g, ?_⟩
  calc
    stoneanCechFifthBoundary T ≫ g =
        (stoneanCechExplicitFifthBoundary T ≫
          (Condensed.profiniteFree Coeff).map A) ≫
          ((Condensed.profiniteFree Coeff).map B ≫ b) := by
            rw [stoneanCechFifthBoundary_explicit_factor]
    _ = stoneanCechExplicitFifthBoundary T ≫
          ((Condensed.profiniteFree Coeff).map (A ≫ B) ≫ b) := by
            simp only [Category.assoc, Functor.map_comp]
    _ = stoneanCechExplicitFifthBoundary T ≫ b := by
          rw [stoneanCechExplicitQuadruple_roundtrip]
          simp
    _ = f := hb

#print axioms stoneanCechFifthBoundary_product_exact_ofClosedCocycle
#print axioms stoneanCechFifthBoundary_explicit_factor
#print axioms stoneanCechExplicitFifthBoundary_integer_scalar
end CMDG.CondensedCM5R0
