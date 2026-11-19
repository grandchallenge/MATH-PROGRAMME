import CMDGCondensedCM4P3DerivedCM5R0ClosedScalarH3Potential
import CMDGCondensedCM4P3DerivedCM5R0DiscreteProductSections
import CMDGCondensedCM4P3DerivedCM5R0CategoricalTripleRelationIso

/-!
# CMDG CM5 — genuine product-coefficient Hom bridge at explicit Čech relations

For the actual closed profinite fourfold relation R4(T) of the Stonean
presentation, form the genuine free condensed-module object F_R4(T).
Given an actual categorical morphism F_R4(T) → ∏ᶜ Z_disc and the true
five-face scalar cocycle identity in every coordinate, construct an
actual categorical morphism F_R3(T) → ∏ᶜ Z_disc whose coordinatewise
locally constant functions satisfy the genuine four-face primitive
identity. Infinite coefficient index types are supported. This uses
the protected free-profinite Hom equivalence, not a fictional uniform
finite quotient of the product coefficient object.

The two source objects are the genuine free condensed modules of the
EXPLICIT closed equal-image Profinite spaces. The categorical
comparison to the iterated pullback Čech nerve and boundary d₃ remains
a separate step. There is NO unconditional identification of G_S with
this product, no unconditional Ext³, and no certification claim.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

noncomputable abbrev stoneanCechExplicitQuadrupleProfinite
    (T : Profinite.{u}) : Profinite.{u} := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechQuadrupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechQuadrupleRelatedSet_isClosed P T p).isCompact
  exact Profinite.of (↥(profiniteCechQuadrupleRelatedSet P T p))

theorem stoneanCechExplicitQuadruple_discreteProduct_H3_potential
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuadrupleProfinite T)) ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hc : ∀ (i : ι)
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
          ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ = 0) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
        (stoneanCechExplicitTripleProfinite T)) ⟶
        ∏ᶜ (fun _ : ι => discreteIntegerCoeff),
      ∀ (i : ι)
      (x y z w : Stonean.toProfinite.obj T.presentation)
      (hxy : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y)
      (hyz : (Profinite.presentation.π T).hom.hom y =
        (Profinite.presentation.π T).hom.hom z)
      (hzw : (Profinite.presentation.π T).hom.hom z =
        (Profinite.presentation.π T).hom.hom w),
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T) f i)
        ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ =
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) g i)
        ⟨(y,(z,w)),⟨hyz,hzw⟩⟩ -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) g i)
        ⟨(x,(z,w)),⟨hxy.trans hyz,hzw⟩⟩ +
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) g i)
        ⟨(x,(y,w)),⟨hxy,hyz.trans hzw⟩⟩ -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitTripleProfinite T) g i)
        ⟨(x,(y,z)),⟨hxy,hyz⟩⟩ := by
  classical
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  let e4 := freeProfiniteDiscreteProductHomScalarEquiv
    (stoneanCechExplicitQuadrupleProfinite T) (ι := ι)
  let e3 := freeProfiniteDiscreteProductHomScalarEquiv
    (stoneanCechExplicitTripleProfinite T) (ι := ι)
  let c : ι → LocallyConstant
      (↥(profiniteCechQuadrupleRelatedSet P T p)) ℤ :=
    e4 f
  have hc' : ∀ (i : ι) (x y z w v : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w)
      (hwv : p.hom.hom w = p.hom.hom v),
      c i ⟨(y,(z,(w,v))),⟨hyz,hzw,hwv⟩⟩ -
      c i ⟨(x,(z,(w,v))),⟨hxy.trans hyz,hzw,hwv⟩⟩ +
      c i ⟨(x,(y,(w,v))),⟨hxy,hyz.trans hzw,hwv⟩⟩ -
      c i ⟨(x,(y,(z,v))),⟨hxy,hyz,hzw.trans hwv⟩⟩ +
      c i ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ = 0 :=
    hc
  obtain ⟨b, hb⟩ :=
    integerProfiniteThreeCocycle_closedQuadruple_family_hasPotential
      P T p c hc'
  let g := e3.symm b
  refine ⟨g, ?_⟩
  intro i x y z w hxy hyz hzw
  have h := hb i x y z w hxy hyz hzw
  have hg : e3 g = b := e3.apply_symm_apply b
  change (c i) _ = (e3 g i) _ - (e3 g i) _ +
    (e3 g i) _ - (e3 g i) _
  rw [hg]
  exact h

#print axioms stoneanCechExplicitQuadruple_discreteProduct_H3_potential
end CMDG.CondensedCM5R0
