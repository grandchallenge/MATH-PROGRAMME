import CMDGCondensedCM4P3DerivedCM5R0ClosedScalarH5Potential

/-! CM5: arbitrary product of coordinatewise closed H⁵ scalar primitives,
with no common finite observation across coefficient indices. -/
noncomputable section
universe u v
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem integerProfiniteFiveCocycle_closedSextuple_family_hasPotential
    (P T : Profinite.{u}) (p : P ⟶ T)
    {ι : Type v} (c : ι → LocallyConstant
      (↥(profiniteCechSextupleRelatedSet P T p)) ℤ)
    (hc : ∀ (i : ι) (x y z w v r s : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w)
      (hwv : p.hom.hom w = p.hom.hom v)
      (hvr : p.hom.hom v = p.hom.hom r)
      (hrs : p.hom.hom r = p.hom.hom s),
        c i ⟨(y,(z,(w,(v,(r,s))))),
          ⟨hyz,hzw,hwv,hvr,hrs⟩⟩ -
        c i ⟨(x,(z,(w,(v,(r,s))))),
          ⟨hxy.trans hyz,hzw,hwv,hvr,hrs⟩⟩ +
        c i ⟨(x,(y,(w,(v,(r,s))))),
          ⟨hxy,hyz.trans hzw,hwv,hvr,hrs⟩⟩ -
        c i ⟨(x,(y,(z,(v,(r,s))))),
          ⟨hxy,hyz,hzw.trans hwv,hvr,hrs⟩⟩ +
        c i ⟨(x,(y,(z,(w,(r,s))))),
          ⟨hxy,hyz,hzw,hwv.trans hvr,hrs⟩⟩ -
        c i ⟨(x,(y,(z,(w,(v,s))))),
          ⟨hxy,hyz,hzw,hwv,hvr.trans hrs⟩⟩ +
        c i ⟨(x,(y,(z,(w,(v,r))))),
          ⟨hxy,hyz,hzw,hwv,hvr⟩⟩ = 0) :
    ∃ b : ι → LocallyConstant
        (↥(profiniteCechQuintupleRelatedSet P T p)) ℤ,
      ∀ (i : ι) (x y z w v r : P)
        (hxy : p.hom.hom x = p.hom.hom y)
        (hyz : p.hom.hom y = p.hom.hom z)
        (hzw : p.hom.hom z = p.hom.hom w)
        (hwv : p.hom.hom w = p.hom.hom v)
        (hvr : p.hom.hom v = p.hom.hom r),
        c i ⟨(x,(y,(z,(w,(v,r))))),⟨hxy,hyz,hzw,hwv,hvr⟩⟩ =
          b i ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩ -
          b i ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩ +
          b i ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩ -
          b i ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩ +
          b i ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩ -
          b i ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ := by
  classical
  have h (i : ι) :
    ∃ b : LocallyConstant
        (↥(profiniteCechQuintupleRelatedSet P T p)) ℤ,
      ∀ (x y z w v r : P)
        (hxy : p.hom.hom x = p.hom.hom y)
        (hyz : p.hom.hom y = p.hom.hom z)
        (hzw : p.hom.hom z = p.hom.hom w)
        (hwv : p.hom.hom w = p.hom.hom v)
        (hvr : p.hom.hom v = p.hom.hom r),
        c i ⟨(x,(y,(z,(w,(v,r))))),⟨hxy,hyz,hzw,hwv,hvr⟩⟩ =
          b ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩ -
          b ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩ +
          b ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩ -
          b ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩ +
          b ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩ -
          b ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ :=
    integerProfiniteFiveCocycle_closedSextuple_potential P T p (c i) (hc i)
  choose b hb using h
  exact ⟨b,hb⟩

#print axioms integerProfiniteFiveCocycle_closedSextuple_family_hasPotential
end CMDG.CondensedCM5R0
