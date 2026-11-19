import CMDGCondensedCM4P3DerivedCM5R0ClosedScalarH4Potential
import CMDGCondensedCM4P3DerivedCM5R0ExplicitClosedProductH3HomBridge

/-!
# CM5 Ext⁴: actual closed-quintuple free-module Hom H4 primitive

For the true profinite *closed fivefold relation* of the Stonean
presentation, transport the arbitrary product-valued scalar H4
vanishing theorem to an honest morphism of free condensed modules.
The coefficient target is an arbitrary categorical product of
discrete integer modules, with no common finite observation.

This is a real free-condensed-module Hom construction, not a setwise
surrogate or an assumption that H4 vanishes. The remaining step is
identifying it with the true fifth categorical boundary and verifying
the sixth-point cocycle for actual fourth-relation Hom.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem stoneanCechExplicitQuintuple_discreteProduct_H4_potential
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hc : ∀ (i : ι)
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
        ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ = 0) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuadrupleProfinite T)) ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff),
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
        (stoneanCechExplicitQuintupleProfinite T) f i)
        ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ =
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T) g i)
        ⟨(y,(z,(w,v))),⟨hyz,hzw,hwv⟩⟩ -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T) g i)
        ⟨(x,(z,(w,v))),⟨hxy.trans hyz,hzw,hwv⟩⟩ +
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T) g i)
        ⟨(x,(y,(w,v))),⟨hxy,hyz.trans hzw,hwv⟩⟩ -
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T) g i)
        ⟨(x,(y,(z,v))),⟨hxy,hyz,hzw.trans hwv⟩⟩ +
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuadrupleProfinite T) g i)
        ⟨(x,(y,(z,w))),⟨hxy,hyz,hzw⟩⟩ := by
  classical
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  let e5 := freeProfiniteDiscreteProductHomScalarEquiv
    (stoneanCechExplicitQuintupleProfinite T) (ι := ι)
  let e4 := freeProfiniteDiscreteProductHomScalarEquiv
    (stoneanCechExplicitQuadrupleProfinite T) (ι := ι)
  let c : ι → LocallyConstant
      (↥(profiniteCechQuintupleRelatedSet P T p)) ℤ :=
    e5 f
  have hc' : ∀ (i : ι) (x y z w v r : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w)
      (hwv : p.hom.hom w = p.hom.hom v)
      (hvr : p.hom.hom v = p.hom.hom r),
      c i ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩ -
      c i ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩ +
      c i ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩ -
      c i ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩ +
      c i ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩ -
      c i ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ = 0 :=
    hc
  obtain ⟨b,hb⟩ :=
    integerProfiniteFourCocycle_closedQuintuple_family_hasPotential
      P T p c hc'
  let g := e4.symm b
  refine ⟨g, ?_⟩
  intro i x y z w v hxy hyz hzw hwv
  have h := hb i x y z w v hxy hyz hzw hwv
  have hg : e4 g = b := e4.apply_symm_apply b
  change (c i) _ = (e4 g i) _ - (e4 g i) _ +
    (e4 g i) _ - (e4 g i) _ + (e4 g i) _
  rw [hg]
  exact h

#print axioms stoneanCechExplicitQuintuple_discreteProduct_H4_potential
end CMDG.CondensedCM5R0
