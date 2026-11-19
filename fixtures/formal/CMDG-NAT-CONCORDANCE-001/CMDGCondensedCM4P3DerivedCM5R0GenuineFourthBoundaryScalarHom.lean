import CMDGCondensedCM4P3DerivedCM5R0GenuineQuadrupleRelationIso
import CMDGCondensedCM4P3DerivedCM5R0DiscreteProductCechDifferential
import CMDGCondensedCM4P3DerivedCM5R0ScalarCechH2ModuleBoundary

/-!
# CM5: actual categorical fourth differential evaluated in discrete scalar coefficients

All four categorical faces are genuine Profinite iterated-pullback morphisms.
Under the genuine free-profinite/discrete-integer Hom equivalence, the
actual free-module alternating fourth boundary maps to the corresponding
four point deletion signs, on EVERY closed fibre-related quadruple.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem stoneanCechFourthBoundary_integer_scalar
    (T : Profinite.{u})
    (g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)) ⟶ discreteIntegerCoeff) :
    freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechQuadruples T)
        (stoneanCechFourthBoundary T ≫ g) =
      (((freeProfiniteDiscreteIntegerHomScalarEquiv
          (stoneanPresentationCechTriples T) g).comap
          (quadFaceYZW T).hom.hom -
        (freeProfiniteDiscreteIntegerHomScalarEquiv
          (stoneanPresentationCechTriples T) g).comap
          (quadFaceXZW T).hom.hom) +
        (freeProfiniteDiscreteIntegerHomScalarEquiv
          (stoneanPresentationCechTriples T) g).comap
          (quadFaceXYW T).hom.hom) -
        (freeProfiniteDiscreteIntegerHomScalarEquiv
          (stoneanPresentationCechTriples T) g).comap
          (pullback.fst
            (stoneanCechTripleXY T ≫
              pullback.fst (Profinite.presentation.π T)
                (Profinite.presentation.π T) ≫
              Profinite.presentation.π T)
            (Profinite.presentation.π T)).hom.hom := by
  unfold stoneanCechFourthBoundary
  rw [Preadditive.sub_comp, Preadditive.add_comp, Preadditive.sub_comp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_sub]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_add]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_sub]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp]
  rfl


/-- Actual signed fourth Čech differential, evaluated at every true
closed-fibre quadruple via the proved categorical Profinite iso. -/
theorem stoneanCechFourthBoundary_integer_scalar_atClosed
    (T : Profinite.{u})
    (g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)) ⟶ discreteIntegerCoeff)
    (r : stoneanCechExplicitQuadrupleProfinite T) :
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechQuadruples T)
      (stoneanCechFourthBoundary T ≫ g))
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r) =
    (((freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechTriples T) g)
          (stoneanCechTripleOfRelated T
            r.val.2.1 r.val.2.2.1 r.val.2.2.2
            r.property.2.1 r.property.2.2) -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechTriples T) g)
          (stoneanCechTripleOfRelated T
            r.val.1 r.val.2.2.1 r.val.2.2.2
            (r.property.1.trans r.property.2.1) r.property.2.2)) +
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechTriples T) g)
          (stoneanCechTripleOfRelated T
            r.val.1 r.val.2.1 r.val.2.2.2
            r.property.1 (r.property.2.1.trans r.property.2.2))) -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
        (stoneanPresentationCechTriples T) g)
          (stoneanCechTripleOfRelated T
            r.val.1 r.val.2.1 r.val.2.2.1
            r.property.1 r.property.2.1) := by
  have h := congrArg (fun F : LocallyConstant
      (stoneanPresentationCechQuadruples T) ℤ =>
      F ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r))
    (stoneanCechFourthBoundary_integer_scalar T g)
  change
    (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechQuadruples T)
      (stoneanCechFourthBoundary T ≫ g))
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r) =
    (((freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechTriples T) g)
      ((quadFaceYZW T).hom.hom
        ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r)) -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechTriples T) g)
      ((quadFaceXZW T).hom.hom
        ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r))) +
      (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechTriples T) g)
      ((quadFaceXYW T).hom.hom
        ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r))) -
      (freeProfiniteDiscreteIntegerHomScalarEquiv
      (stoneanPresentationCechTriples T) g)
      ((pullback.fst
        (stoneanCechTripleXY T ≫
          pullback.fst (Profinite.presentation.π T)
            (Profinite.presentation.π T) ≫
          Profinite.presentation.π T)
        (Profinite.presentation.π T)).hom.hom
        ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r)) at h
  rw [stoneanCechExplicitQuadruple_yzw_atPoint,
    stoneanCechExplicitQuadruple_xzw_atPoint,
    stoneanCechExplicitQuadruple_xyw_atPoint,
    stoneanCechExplicitQuadruple_xyz_atPoint] at h
  exact h


/-- Four-face signed scalar identity for an ACTUAL categorical product of
arbitrarily many discrete coefficients; no uniform finite observation. -/
theorem stoneanCechFourthBoundary_product_scalar_atClosed
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (r : stoneanCechExplicitQuadrupleProfinite T) (i : ι) :
    (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanPresentationCechQuadruples T)
      (stoneanCechFourthBoundary T ≫ g) i)
      ((stoneanCechExplicitQuadrupleToAbstract T).hom.hom r) =
    (((freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanPresentationCechTriples T) g i)
          (stoneanCechTripleOfRelated T
            r.val.2.1 r.val.2.2.1 r.val.2.2.2
            r.property.2.1 r.property.2.2) -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanPresentationCechTriples T) g i)
          (stoneanCechTripleOfRelated T
            r.val.1 r.val.2.2.1 r.val.2.2.2
            (r.property.1.trans r.property.2.1) r.property.2.2)) +
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanPresentationCechTriples T) g i)
          (stoneanCechTripleOfRelated T
            r.val.1 r.val.2.1 r.val.2.2.2
            r.property.1 (r.property.2.1.trans r.property.2.2))) -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanPresentationCechTriples T) g i)
          (stoneanCechTripleOfRelated T
            r.val.1 r.val.2.1 r.val.2.2.1
            r.property.1 r.property.2.1) := by
  simpa [freeProfiniteDiscreteProductHomScalarEquiv, Category.assoc] using
    (stoneanCechFourthBoundary_integer_scalar_atClosed T
      (g ≫ Pi.π (fun _ : ι => discreteIntegerCoeff) i) r)


/-- Given an actual product-valued primitive on the closed triple relation,
the true categorical alternating d3 admits an actual Hom lift.
No coefficient model or global cocycle assumption is hidden here. -/
theorem stoneanCechFourthBoundary_product_exact_ofClosedPrimitive
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (h : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (b : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitTripleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hprim : ∀ (i : ι)
      (r : stoneanCechExplicitQuadrupleProfinite T),
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T)
        ((Condensed.profiniteFree Coeff).map
          (stoneanCechExplicitQuadrupleToAbstract T) ≫ h) i) r =
      (((freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) b i)
        ⟨(r.val.2.1,(r.val.2.2.1,r.val.2.2.2)),
          ⟨r.property.2.1,r.property.2.2⟩⟩ -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) b i)
        ⟨(r.val.1,(r.val.2.2.1,r.val.2.2.2)),
          ⟨r.property.1.trans r.property.2.1,r.property.2.2⟩⟩) +
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) b i)
        ⟨(r.val.1,(r.val.2.1,r.val.2.2.2)),
          ⟨r.property.1,r.property.2.1.trans r.property.2.2⟩⟩) -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) b i)
        ⟨(r.val.1,(r.val.2.1,r.val.2.2.1)),
          ⟨r.property.1,r.property.2.1⟩⟩) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff),
      stoneanCechFourthBoundary T ≫ g = h := by
  classical
  let A := stoneanCechExplicitQuadrupleToAbstract T
  let B := stoneanCechCategoricalTripleToExplicitProfinite T
  let A3 := stoneanCechExplicitTripleToAbstract T
  let g := (Condensed.profiniteFree Coeff).map B ≫ b
  refine ⟨g, ?_⟩
  have htriple (i : ι)
      (t : stoneanCechExplicitTripleProfinite T) :
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanPresentationCechTriples T) g i)
        (A3.hom.hom t) =
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) b i) t := by
    have hBA : B.hom.hom (A3.hom.hom t) = t :=
      stoneanCechExplicitTriple_roundtrip T t
    change (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanPresentationCechTriples T)
      ((Condensed.profiniteFree Coeff).map B ≫ b) i)
      (A3.hom.hom t) =
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) b i) t
    rw [freeProfiniteDiscreteProductHomScalarEquiv_precomp]
    change (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitTripleProfinite T) b i)
      (B.hom.hom (A3.hom.hom t)) = _
    rw [hBA]
  have htrip (i : ι) (x y z : Stonean.toProfinite.obj T.presentation)
      (hxy : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y)
      (hyz : (Profinite.presentation.π T).hom.hom y =
        (Profinite.presentation.π T).hom.hom z) :
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanPresentationCechTriples T) g i)
          (stoneanCechTripleOfRelated T x y z hxy hyz) =
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) b i)
          ⟨(x,(y,z)),⟨hxy,hyz⟩⟩ := by
    rw [← stoneanCechExplicitTripleToAbstract_ofRelated]
    exact htriple i ⟨(x,(y,z)),⟨hxy,hyz⟩⟩
  have hpre :
      (Condensed.profiniteFree Coeff).map A ≫
        (stoneanCechFourthBoundary T ≫ g) =
      (Condensed.profiniteFree Coeff).map A ≫ h := by
    apply (freeProfiniteDiscreteProductHomScalarEquiv
      (stoneanCechExplicitQuadrupleProfinite T)).injective
    funext i
    ext r
    calc
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T)
        ((Condensed.profiniteFree Coeff).map A ≫
          (stoneanCechFourthBoundary T ≫ g)) i) r =
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanPresentationCechQuadruples T)
          (stoneanCechFourthBoundary T ≫ g) i) (A.hom.hom r) := by
            rw [freeProfiniteDiscreteProductHomScalarEquiv_precomp]
            rfl
      _ = (((freeProfiniteDiscreteProductHomScalarEquiv
          (stoneanPresentationCechTriples T) g i)
          (stoneanCechTripleOfRelated T
            r.val.2.1 r.val.2.2.1 r.val.2.2.2
            r.property.2.1 r.property.2.2) -
          (freeProfiniteDiscreteProductHomScalarEquiv
          (stoneanPresentationCechTriples T) g i)
          (stoneanCechTripleOfRelated T
            r.val.1 r.val.2.2.1 r.val.2.2.2
            (r.property.1.trans r.property.2.1) r.property.2.2)) +
          (freeProfiniteDiscreteProductHomScalarEquiv
          (stoneanPresentationCechTriples T) g i)
          (stoneanCechTripleOfRelated T
            r.val.1 r.val.2.1 r.val.2.2.2
            r.property.1 (r.property.2.1.trans r.property.2.2))) -
          (freeProfiniteDiscreteProductHomScalarEquiv
          (stoneanPresentationCechTriples T) g i)
          (stoneanCechTripleOfRelated T
            r.val.1 r.val.2.1 r.val.2.2.1
            r.property.1 r.property.2.1) :=
            stoneanCechFourthBoundary_product_scalar_atClosed T g r i
      _ = (((freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) b i)
          ⟨(r.val.2.1,(r.val.2.2.1,r.val.2.2.2)),
            ⟨r.property.2.1,r.property.2.2⟩⟩ -
          (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) b i)
          ⟨(r.val.1,(r.val.2.2.1,r.val.2.2.2)),
            ⟨r.property.1.trans r.property.2.1,r.property.2.2⟩⟩) +
          (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) b i)
          ⟨(r.val.1,(r.val.2.1,r.val.2.2.2)),
            ⟨r.property.1,r.property.2.1.trans r.property.2.2⟩⟩) -
          (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) b i)
          ⟨(r.val.1,(r.val.2.1,r.val.2.2.1)),
            ⟨r.property.1,r.property.2.1⟩⟩ := by
            rw [htrip, htrip, htrip, htrip]
      _ = (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T)
        ((Condensed.profiniteFree Coeff).map A ≫ h) i) r :=
        (hprim i r).symm
  haveI : IsIso A := by
    change IsIso (stoneanCechExplicitQuadrupleIso T).hom
    infer_instance
  haveI : Epi ((Condensed.profiniteFree Coeff).map A) := by
    infer_instance
  exact (cancel_epi ((Condensed.profiniteFree Coeff).map A)).1
    (by simpa only [Category.assoc] using hpre)


/-- The exact *five-point* Čech 3-cocycle condition on an actual
product-valued Hom from the free condensed module on the genuine
CLOSED fourfold equal-image relation. No uniform finite quotient. -/
def stoneanCechClosedProductFiveCocycle
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuadrupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff)) : Prop :=
  ∀ (i : ι)
      (x y z w v : Stonean.toProfinite.obj T.presentation)
      (hxy : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y)
      (hyz : (Profinite.presentation.π T).hom.hom y =
        (Profinite.presentation.π T).hom.hom z)
      (hzw : (Profinite.presentation.π T).hom.hom z =
        (Profinite.presentation.π T).hom.hom w)
      (hwv : (Profinite.presentation.π T).hom.hom w =
        (Profinite.presentation.π T).hom.hom v),
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T) f i)
          ⟨(y,(z,(w,v))),⟨hyz,hzw,hwv⟩⟩ -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T) f i)
          ⟨(x,(z,(w,v))),⟨hxy.trans hyz,hzw,hwv⟩⟩ +
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T) f i)
          ⟨(x,(y,(w,v))),⟨hxy,hyz.trans hzw,hwv⟩⟩ -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T) f i)
          ⟨(x,(y,(z,v))),⟨hxy,hyz,hzw.trans hwv⟩⟩ +
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T) f i)
          ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ = 0

/-- Genuine categorical d3-Hom exactness for arbitrary products
of discrete integer coefficients, provided the true closed-relation
five-point cocycle identity holds for the input. -/
theorem stoneanCechFourthBoundary_product_exact_ofClosedCocycle
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (h : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuadruples T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hc : stoneanCechClosedProductFiveCocycle T
      ((Condensed.profiniteFree Coeff).map
        (stoneanCechExplicitQuadrupleToAbstract T) ≫ h)) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechTriples T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff),
      stoneanCechFourthBoundary T ≫ g = h := by
  let f := (Condensed.profiniteFree Coeff).map
    (stoneanCechExplicitQuadrupleToAbstract T) ≫ h
  obtain ⟨b, hb⟩ :=
    stoneanCechExplicitQuadruple_discreteProduct_H3_potential T f hc
  apply stoneanCechFourthBoundary_product_exact_ofClosedPrimitive T h b
  intro i r
  exact hb i r.val.1 r.val.2.1 r.val.2.2.1 r.val.2.2.2
    r.property.1 r.property.2.1 r.property.2.2

#print axioms stoneanCechFourthBoundary_product_exact_ofClosedCocycle
#print axioms stoneanCechFourthBoundary_product_exact_ofClosedPrimitive
#print axioms stoneanCechFourthBoundary_product_scalar_atClosed
#print axioms stoneanCechFourthBoundary_integer_scalar_atClosed
#print axioms stoneanCechFourthBoundary_integer_scalar
end CMDG.CondensedCM5R0
