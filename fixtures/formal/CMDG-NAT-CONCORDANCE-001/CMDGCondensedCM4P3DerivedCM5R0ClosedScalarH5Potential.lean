import CMDGCondensedCM4P3DerivedCM5R0ProfiniteScalarH5AmbientPotential
import CMDGCondensedCM4P3DerivedCM5R0GenuineSixfoldCechFaces

/-!
# CM5 Ext5: genuine closed sixfold scalar H⁵ primitive

For an arbitrary profinite presentation p:P→T, a locally constant
5-cocycle on the ACTUAL closed sixfold equal-image relation
admits a locally constant primitive on the closed fivefold relation.
No finite substitute, section, or unproved Ext5 vanishing is used.
-/
noncomputable section
universe u v
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem integerProfiniteFiveCocycle_closedSextuple_potential
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant
      (↥(profiniteCechSextupleRelatedSet P T p)) ℤ)
    (hc : ∀ (x y z w v r s : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w)
      (hwv : p.hom.hom w = p.hom.hom v)
      (hvr : p.hom.hom v = p.hom.hom r)
      (hrs : p.hom.hom r = p.hom.hom s),
        c ⟨(y,(z,(w,(v,(r,s))))),
          ⟨hyz,hzw,hwv,hvr,hrs⟩⟩ -
        c ⟨(x,(z,(w,(v,(r,s))))),
          ⟨hxy.trans hyz,hzw,hwv,hvr,hrs⟩⟩ +
        c ⟨(x,(y,(w,(v,(r,s))))),
          ⟨hxy,hyz.trans hzw,hwv,hvr,hrs⟩⟩ -
        c ⟨(x,(y,(z,(v,(r,s))))),
          ⟨hxy,hyz,hzw.trans hwv,hvr,hrs⟩⟩ +
        c ⟨(x,(y,(z,(w,(r,s))))),
          ⟨hxy,hyz,hzw,hwv.trans hvr,hrs⟩⟩ -
        c ⟨(x,(y,(z,(w,(v,s))))),
          ⟨hxy,hyz,hzw,hwv,hvr.trans hrs⟩⟩ +
        c ⟨(x,(y,(z,(w,(v,r))))),
          ⟨hxy,hyz,hzw,hwv,hvr⟩⟩ = 0) :
    ∃ b : LocallyConstant
        (↥(profiniteCechQuintupleRelatedSet P T p)) ℤ,
      ∀ (x y z w v r : P)
        (hxy : p.hom.hom x = p.hom.hom y)
        (hyz : p.hom.hom y = p.hom.hom z)
        (hzw : p.hom.hom z = p.hom.hom w)
        (hwv : p.hom.hom w = p.hom.hom v)
        (hvr : p.hom.hom v = p.hom.hom r),
        c ⟨(x,(y,(z,(w,(v,r))))),⟨hxy,hyz,hzw,hwv,hvr⟩⟩ =
          b ⟨(y,(z,(w,(v,r)))),⟨hyz,hzw,hwv,hvr⟩⟩ -
          b ⟨(x,(z,(w,(v,r)))),⟨hxy.trans hyz,hzw,hwv,hvr⟩⟩ +
          b ⟨(x,(y,(w,(v,r)))),⟨hxy,hyz.trans hzw,hwv,hvr⟩⟩ -
          b ⟨(x,(y,(z,(v,r)))),⟨hxy,hyz,hzw.trans hwv,hvr⟩⟩ +
          b ⟨(x,(y,(z,(w,r)))),⟨hxy,hyz,hzw,hwv.trans hvr⟩⟩ -
          b ⟨(x,(y,(z,(w,v)))),⟨hxy,hyz,hzw,hwv⟩⟩ := by
  let Q : Profinite.{u} := Profinite.of (P × (P × (P × (P × (P × P)))))
  obtain ⟨C,hC⟩ := locallyConstant_extend_closed_subset Q
      (profiniteCechSextupleRelatedSet P T p)
      (profiniteCechSextupleRelatedSet_isClosed P T p) c
  have hc' : ∀ (x y z w v r s : P),
      p.hom.hom x = p.hom.hom y →
      p.hom.hom y = p.hom.hom z →
      p.hom.hom z = p.hom.hom w →
      p.hom.hom w = p.hom.hom v →
      p.hom.hom v = p.hom.hom r →
      p.hom.hom r = p.hom.hom s →
      C (y,(z,(w,(v,(r,s))))) -
        C (x,(z,(w,(v,(r,s))))) +
        C (x,(y,(w,(v,(r,s))))) -
        C (x,(y,(z,(v,(r,s))))) +
        C (x,(y,(z,(w,(r,s))))) -
        C (x,(y,(z,(w,(v,s))))) +
        C (x,(y,(z,(w,(v,r))))) = 0 := by
    intro x y z w v r s hxy hyz hzw hwv hvr hrs
    rw [hC ⟨(y,(z,(w,(v,(r,s))))),⟨hyz,hzw,hwv,hvr,hrs⟩⟩,
      hC ⟨(x,(z,(w,(v,(r,s))))),
        ⟨hxy.trans hyz,hzw,hwv,hvr,hrs⟩⟩,
      hC ⟨(x,(y,(w,(v,(r,s))))),
        ⟨hxy,hyz.trans hzw,hwv,hvr,hrs⟩⟩,
      hC ⟨(x,(y,(z,(v,(r,s))))),
        ⟨hxy,hyz,hzw.trans hwv,hvr,hrs⟩⟩,
      hC ⟨(x,(y,(z,(w,(r,s))))),
        ⟨hxy,hyz,hzw,hwv.trans hvr,hrs⟩⟩,
      hC ⟨(x,(y,(z,(w,(v,s))))),
        ⟨hxy,hyz,hzw,hwv,hvr.trans hrs⟩⟩,
      hC ⟨(x,(y,(z,(w,(v,r))))),
        ⟨hxy,hyz,hzw,hwv,hvr⟩⟩]
    exact hc x y z w v r s hxy hyz hzw hwv hvr hrs
  obtain ⟨B,hB⟩ :=
    integerProfiniteFiveCocycle_ambientSextuple_potential P T p C hc'
  let b : LocallyConstant
      (↥(profiniteCechQuintupleRelatedSet P T p)) ℤ :=
    B.comap ⟨fun z => z.val, continuous_subtype_val⟩
  refine ⟨b, ?_⟩
  intro x y z w v r hxy hyz hzw hwv hvr
  change c ⟨(x,(y,(z,(w,(v,r))))),⟨hxy,hyz,hzw,hwv,hvr⟩⟩ =
    B (y,(z,(w,(v,r)))) -
      B (x,(z,(w,(v,r)))) +
      B (x,(y,(w,(v,r)))) -
      B (x,(y,(z,(v,r)))) +
      B (x,(y,(z,(w,r)))) -
      B (x,(y,(z,(w,v))))
  rw [← hC ⟨(x,(y,(z,(w,(v,r))))),⟨hxy,hyz,hzw,hwv,hvr⟩⟩]
  exact hB x y z w v r hxy hyz hzw hwv hvr

#print axioms integerProfiniteFiveCocycle_closedSextuple_potential
end CMDG.CondensedCM5R0
