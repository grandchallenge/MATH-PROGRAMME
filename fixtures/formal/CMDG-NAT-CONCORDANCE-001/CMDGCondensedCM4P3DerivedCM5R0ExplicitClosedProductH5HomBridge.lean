import CMDGCondensedCM4P3DerivedCM5R0ClosedScalarH5Potential
import CMDGCondensedCM4P3DerivedCM5R0ExplicitClosedProductH4HomBridge

/-! CM5: true closed-sixfold free condensed Hom H5 primitives.
The target is an *arbitrary* categorical product of discrete integer
coefficients. Each coordinate may require its own finite observation.
No uniform finite quotient of an infinite coefficient product. -/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem stoneanCechExplicitSextuple_discreteProduct_H5_potential
    (T : Profinite.{u}) {ι : Type (u + 1)}
    (f : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitSextupleProfinite T)) ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff))
    (hc : ∀ (i : ι)
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
        (stoneanCechExplicitSextupleProfinite T) f i) ⟨(y,(z,(w,(v,(r,s))))),⟨hyz,hzw,hwv,hvr,hrs⟩⟩ - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i) ⟨(x,(z,(w,(v,(r,s))))),⟨hxy.trans hyz,hzw,hwv,hvr,hrs⟩⟩ + (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i) ⟨(x,(y,(w,(v,(r,s))))),⟨hxy,hyz.trans hzw,hwv,hvr,hrs⟩⟩ - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i) ⟨(x,(y,(z,(v,(r,s))))),⟨hxy,hyz,hzw.trans hwv,hvr,hrs⟩⟩ + (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i) ⟨(x,(y,(z,(w,(r,s))))),⟨hxy,hyz,hzw,hwv.trans hvr,hrs⟩⟩ - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i) ⟨(x,(y,(z,(w,(v,s))))),⟨hxy,hyz,hzw,hwv,hvr.trans hrs⟩⟩ + (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitSextupleProfinite T) f i) ⟨(x,(y,(z,(w,(v,r))))),⟨hxy,hyz,hzw,hwv,hvr⟩⟩ = 0) :
    ∃ g : ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) ⟶
      ∏ᶜ (fun _ : ι => discreteIntegerCoeff),
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
        (stoneanCechExplicitSextupleProfinite T) f i) ⟨(x,(y,(z,(w,(v,r))))),⟨hxy,hyz,hzw,hwv,hvr⟩⟩ =
      (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g i) ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩ - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g i) ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩ + (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g i) ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩ - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g i) ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩ + (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g i) ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩ - (freeProfiniteDiscreteProductHomScalarEquiv
        (stoneanCechExplicitQuintupleProfinite T) g i) ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ := by
  classical
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  let e6 := freeProfiniteDiscreteProductHomScalarEquiv
    (stoneanCechExplicitSextupleProfinite T) (ι := ι)
  let e5 := freeProfiniteDiscreteProductHomScalarEquiv
    (stoneanCechExplicitQuintupleProfinite T) (ι := ι)
  let c : ι → LocallyConstant
      (↥(profiniteCechSextupleRelatedSet P T p)) ℤ :=
    e6 f
  have hc' : ∀ (i : ι) (x y z w v r s : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w)
      (hwv : p.hom.hom w = p.hom.hom v)
      (hvr : p.hom.hom v = p.hom.hom r)
      (hrs : p.hom.hom r = p.hom.hom s),
      c i ⟨(y,(z,(w,(v,(r,s))))),⟨hyz,hzw,hwv,hvr,hrs⟩⟩ - c i ⟨(x,(z,(w,(v,(r,s))))),⟨hxy.trans hyz,hzw,hwv,hvr,hrs⟩⟩ + c i ⟨(x,(y,(w,(v,(r,s))))),⟨hxy,hyz.trans hzw,hwv,hvr,hrs⟩⟩ - c i ⟨(x,(y,(z,(v,(r,s))))),⟨hxy,hyz,hzw.trans hwv,hvr,hrs⟩⟩ + c i ⟨(x,(y,(z,(w,(r,s))))),⟨hxy,hyz,hzw,hwv.trans hvr,hrs⟩⟩ - c i ⟨(x,(y,(z,(w,(v,s))))),⟨hxy,hyz,hzw,hwv,hvr.trans hrs⟩⟩ + c i ⟨(x,(y,(z,(w,(v,r))))),⟨hxy,hyz,hzw,hwv,hvr⟩⟩ = 0 := hc
  obtain ⟨b,hb⟩ :=
    integerProfiniteFiveCocycle_closedSextuple_family_hasPotential
      P T p c hc'
  let g := e5.symm b
  refine ⟨g, ?_⟩
  intro i x y z w v r hxy hyz hzw hwv hvr
  have h := hb i x y z w v r hxy hyz hzw hwv hvr
  have hg : e5 g = b := e5.apply_symm_apply b
  change (c i) _ = (e5 g i) _ - (e5 g i) _ + (e5 g i) _ - (e5 g i) _ + (e5 g i) _ - (e5 g i) _
  rw [hg]
  exact h

#print axioms stoneanCechExplicitSextuple_discreteProduct_H5_potential
end CMDG.CondensedCM5R0
