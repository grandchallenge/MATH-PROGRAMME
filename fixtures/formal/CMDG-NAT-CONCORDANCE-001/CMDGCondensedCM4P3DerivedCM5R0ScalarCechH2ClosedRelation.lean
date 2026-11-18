import CMDGCondensedCM4P3DerivedCM5R0ScalarCechH2AmbientPotential
import CMDGCondensedCM4P3DerivedCM5R0StoneanScalarCechPrimitive

/-!
# CM5 — scalar Čech H² on the actual closed triple relation

For any profinite map p:P→T, the genuine equivalence-relation triple
subspace of P³ is closed. A locally constant integer-valued 2-cocycle
on that subspace extends to the ambient triple product; the existing
ambient product theorem then constructs a primitive and restricts it
to the actual closed pair relation. This is a genuine arbitrary-profinite
SCALAR Čech H² acyclicity theorem, not Ext² in CondensedMod.

Transferring it into the categorical Čech fibre products, the genuine
free condensed-module Hom equivalences, and the second-relation-kernel
extension criterion remains a separate formally checkable obligation.
-/

noncomputable section

universe u
open CategoryTheory Limits Set

namespace CMDG.CondensedCM5R0

def profiniteCechTripleRelatedSet
    (P T : Profinite.{u}) (p : P ⟶ T) :
    Set (P × (P × P)) :=
  {xyz | p.hom.hom xyz.1 = p.hom.hom xyz.2.1 ∧
         p.hom.hom xyz.2.1 = p.hom.hom xyz.2.2}

theorem profiniteCechTripleRelatedSet_isClosed
    (P T : Profinite.{u}) (p : P ⟶ T) :
    IsClosed (profiniteCechTripleRelatedSet P T p) := by
  have hfirst : Continuous
      (fun xyz : P × (P × P) => p.hom.hom xyz.1) :=
    p.hom.hom.continuous.comp continuous_fst
  have hsecond : Continuous
      (fun xyz : P × (P × P) => p.hom.hom xyz.2.1) :=
    p.hom.hom.continuous.comp (continuous_fst.comp continuous_snd)
  have hthird : Continuous
      (fun xyz : P × (P × P) => p.hom.hom xyz.2.2) :=
    p.hom.hom.continuous.comp (continuous_snd.comp continuous_snd)
  have hxy : IsClosed
      {xyz : P × (P × P) | p.hom.hom xyz.1 = p.hom.hom xyz.2.1} :=
    isClosed_eq hfirst hsecond
  have hyz : IsClosed
      {xyz : P × (P × P) | p.hom.hom xyz.2.1 = p.hom.hom xyz.2.2} :=
    isClosed_eq hsecond hthird
  exact hxy.inter hyz

theorem integerProfiniteTwoCocycle_hasPotential
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant (↥(profiniteCechTripleRelatedSet P T p)) ℤ)
    (hc : ∀ (x y z w : P)
        (hxy : p.hom.hom x = p.hom.hom y)
        (hyz : p.hom.hom y = p.hom.hom z)
        (hzw : p.hom.hom z = p.hom.hom w),
      c ⟨(y, (z, w)), ⟨hyz, hzw⟩⟩ -
      c ⟨(x, (z, w)), ⟨hxy.trans hyz, hzw⟩⟩ +
      c ⟨(x, (y, w)), ⟨hxy, hyz.trans hzw⟩⟩ -
      c ⟨(x, (y, z)), ⟨hxy, hyz⟩⟩ = 0) :
    ∃ b : LocallyConstant (↥(profiniteCechRelatedSet P T p)) ℤ,
      ∀ (x y z : P)
        (hxy : p.hom.hom x = p.hom.hom y)
        (hyz : p.hom.hom y = p.hom.hom z),
      c ⟨(x, (y, z)), ⟨hxy, hyz⟩⟩ =
        b ⟨(y, z), hyz⟩ -
        b ⟨(x, z), hxy.trans hyz⟩ +
        b ⟨(x, y), hxy⟩ := by
  let Q : Profinite.{u} := Profinite.of (P × (P × P))
  obtain ⟨C, hC⟩ :=
    locallyConstant_extend_closed_subset Q
      (profiniteCechTripleRelatedSet P T p)
      (profiniteCechTripleRelatedSet_isClosed P T p) c
  have h4 (x y z w : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z)
      (hzw : p.hom.hom z = p.hom.hom w) :
      C (y, (z, w)) - C (x, (z, w)) +
        C (x, (y, w)) - C (x, (y, z)) = 0 := by
    rw [hC ⟨(y, (z, w)), ⟨hyz, hzw⟩⟩,
      hC ⟨(x, (z, w)), ⟨hxy.trans hyz, hzw⟩⟩,
      hC ⟨(x, (y, w)), ⟨hxy, hyz.trans hzw⟩⟩,
      hC ⟨(x, (y, z)), ⟨hxy, hyz⟩⟩]
    exact hc x y z w hxy hyz hzw
  obtain ⟨B, hB⟩ :=
    integerProfiniteTwoCocycle_ambientTriple_potential
      P T p C h4
  let b : LocallyConstant (↥(profiniteCechRelatedSet P T p)) ℤ :=
    B.comap (⟨(fun z => z.val), continuous_subtype_val⟩ :
      C(↥(profiniteCechRelatedSet P T p), P × P))
  refine ⟨b, ?_⟩
  intro x y z hxy hyz
  change c ⟨(x, (y, z)), ⟨hxy, hyz⟩⟩ =
    B (y, z) - B (x, z) + B (x, y)
  rw [← hC ⟨(x, (y, z)), ⟨hxy, hyz⟩⟩]
  exact hB x y z hxy hyz

#print axioms profiniteCechTripleRelatedSet_isClosed
#print axioms integerProfiniteTwoCocycle_hasPotential

end CMDG.CondensedCM5R0
