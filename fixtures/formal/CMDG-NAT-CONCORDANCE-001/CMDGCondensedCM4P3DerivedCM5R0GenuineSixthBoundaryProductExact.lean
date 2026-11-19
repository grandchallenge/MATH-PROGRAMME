import CMDGCondensedCM4P3DerivedCM5R0SeventhFaceCocycle

/-!
# CM5: actual sixfold free condensed-module H5 Hom exactness
for an arbitrary product of discrete integers. The source is
the actual closed Profinite sextuple and actual 6-face differential.
The seventh closed-fibre cocycle comes from the authentic d7*d6
simplicial cancellation, not an assumed Ext5 assertion.
-/
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem stoneanCechSixthBoundary_product_exact_ofClosedCocycle
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitSextupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hc : stoneanCechClosedProductSevenCocycle T f) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff),
      stoneanCechSixthBoundary T ≫ g = f := by
  classical
  have hc' : ∀ (i : ι)
      (x y z w v r s : Stonean.toProfinite.obj T.presentation)
      (hxy : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y)
      (hyz : (Profinite.presentation.π T).hom.hom y =
        (Profinite.presentation.π T).hom.hom z)
      (hzw : (Profinite.presentation.π T).hom.hom z =
        (Profinite.presentation.π T).hom.hom w)
      (hwv : (Profinite.presentation.π T).hom.hom w =
        (Profinite.presentation.π T).hom.hom v)
      (hvr : (Profinite.presentation.π T).hom.hom v =
        (Profinite.presentation.π T).hom.hom r)
      (hrs : (Profinite.presentation.π T).hom.hom r =
        (Profinite.presentation.π T).hom.hom s),
            (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ⟨(y,(z,(w,(v,(r,s))))),⟨hyz,hzw,hwv,hvr,hrs⟩⟩
      - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ⟨(x,(z,(w,(v,(r,s))))),⟨hxy.trans hyz,hzw,hwv,hvr,hrs⟩⟩
      + (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ⟨(x,(y,(w,(v,(r,s))))),⟨hxy,hyz.trans hzw,hwv,hvr,hrs⟩⟩
      - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ⟨(x,(y,(z,(v,(r,s))))),⟨hxy,hyz,hzw.trans hwv,hvr,hrs⟩⟩
      + (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ⟨(x,(y,(z,(w,(r,s))))),⟨hxy,hyz,hzw,hwv.trans hvr,hrs⟩⟩
      - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ⟨(x,(y,(z,(w,(v,s))))),⟨hxy,hyz,hzw,hwv,hvr.trans hrs⟩⟩
      + (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ⟨(x,(y,(z,(w,(v,r))))),⟨hxy,hyz,hzw,hwv,hvr⟩⟩ = 0 := by
    intro i x y z w v r s hxy hyz hzw hwv hvr hrs
    let q : stoneanCechExplicitSeptupleProfinite T :=
      ⟨(x,(y,(z,(w,(v,(r,s)))))),⟨hxy,hyz,hzw,hwv,hvr,hrs⟩⟩
    have h := hc i q
    change       (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace0 T).hom.hom q)
      - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace1 T).hom.hom q)
      + (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace2 T).hom.hom q)
      - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace3 T).hom.hom q)
      + (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace4 T).hom.hom q)
      - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace5 T).hom.hom q)
      + (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i)
        ((septupleFace6 T).hom.hom q) = 0 at h
    exact h
  obtain ⟨g,hg⟩ :=
    stoneanCechExplicitSextuple_discreteProduct_H5_potential T f hc'
  refine ⟨g, ?_⟩
  apply (freeProfiniteDiscreteProductHomScalarEquiv
    (stoneanCechExplicitSextupleProfinite T)).injective
  funext i
  ext r
  have hxy := r.property.1
  have hyz := r.property.2.1
  have hzw := r.property.2.2.1
  have hwv := r.property.2.2.2.1
  have hvr := r.property.2.2.2.2
  have h := hg i r.val.1 r.val.2.1 r.val.2.2.1
    r.val.2.2.2.1 r.val.2.2.2.2.1 r.val.2.2.2.2.2
    hxy hyz hzw hwv hvr
  have hd := stoneanCechSixthBoundary_product_scalar_atPoint T g i r
  exact hd.trans h.symm

#print axioms stoneanCechSixthBoundary_product_exact_ofClosedCocycle
end CMDG.CondensedCM5R0
