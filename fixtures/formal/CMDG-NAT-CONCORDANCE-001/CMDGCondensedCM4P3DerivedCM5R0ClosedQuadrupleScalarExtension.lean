import CMDGCondensedCM4P3DerivedCM5R0GlobalThirdRelationEpi
import CMDGCondensedCM4P3DerivedCM5R0ScalarCechH2ClosedRelation

/-!
# CMDG CM5 — closed true four-point fibre relation and scalar extension

For all profinite P,T and every genuine profinite map p:P→T, the
right-associated equal-image quadruple subset of P⁴ is closed.
This is proved using the four continuous vertex maps and closed
equalizers (three successive diagonal equalities).

Every locally constant integer-valued scalar cochain on that
genuine closed fourfold relation admits a locally constant extension
to the entire P⁴ ambient product. This is an explicit verified
topological source-normalization input for the next scalar Čech H³
primitive theorem, not the primitive theorem itself.

No scalar H³ acyclicity, Ext³ vanishing or full derived solidity
is asserted. The next substantive obligation is finite fourfold
clopen-box factorization and the finite-closed-family H³
coboundary lemma, followed by categorical/module transport.
-/

noncomputable section
universe u
open CategoryTheory Limits Set
namespace CMDG.CondensedCM5R0

def profiniteCechQuadrupleRelatedSet
    (P T : Profinite.{u}) (p : P ⟶ T) :
    Set (P × (P × (P × P))) :=
  {xyzw | p.hom.hom xyzw.1 = p.hom.hom xyzw.2.1 ∧
    p.hom.hom xyzw.2.1 = p.hom.hom xyzw.2.2.1 ∧
    p.hom.hom xyzw.2.2.1 = p.hom.hom xyzw.2.2.2}

theorem profiniteCechQuadrupleRelatedSet_isClosed
    (P T : Profinite.{u}) (p : P ⟶ T) :
    IsClosed (profiniteCechQuadrupleRelatedSet P T p) := by
  have h1 : Continuous
      (fun xyzw : P × (P × (P × P)) => p.hom.hom xyzw.1) :=
    p.hom.hom.continuous.comp continuous_fst
  have h2 : Continuous
      (fun xyzw : P × (P × (P × P)) => p.hom.hom xyzw.2.1) :=
    p.hom.hom.continuous.comp (continuous_fst.comp continuous_snd)
  have h3 : Continuous
      (fun xyzw : P × (P × (P × P)) => p.hom.hom xyzw.2.2.1) :=
    p.hom.hom.continuous.comp
      (continuous_fst.comp (continuous_snd.comp continuous_snd))
  have h4 : Continuous
      (fun xyzw : P × (P × (P × P)) => p.hom.hom xyzw.2.2.2) :=
    p.hom.hom.continuous.comp
      (continuous_snd.comp (continuous_snd.comp continuous_snd))
  have h12 : IsClosed
      {xyzw : P × (P × (P × P)) |
        p.hom.hom xyzw.1 = p.hom.hom xyzw.2.1} :=
    isClosed_eq h1 h2
  have h23 : IsClosed
      {xyzw : P × (P × (P × P)) |
        p.hom.hom xyzw.2.1 = p.hom.hom xyzw.2.2.1} :=
    isClosed_eq h2 h3
  have h34 : IsClosed
      {xyzw : P × (P × (P × P)) |
        p.hom.hom xyzw.2.2.1 = p.hom.hom xyzw.2.2.2} :=
    isClosed_eq h3 h4
  simpa only [profiniteCechQuadrupleRelatedSet, Set.setOf_and] using h12.inter (h23.inter h34)

/-- Any locally constant scalar cochain on the actual closed four-point
relation extends to an ambient locally constant four-product cochain. -/
theorem integerLocallyConstant_extendCechQuadruple
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant
      (↥(profiniteCechQuadrupleRelatedSet P T p)) ℤ) :
    ∃ C : LocallyConstant (P × (P × (P × P))) ℤ,
      ∀ w : ↥(profiniteCechQuadrupleRelatedSet P T p),
        C w.val = c w := by
  let Q : Profinite.{u} := Profinite.of (P × (P × (P × P)))
  exact locallyConstant_extend_closed_subset Q
    (profiniteCechQuadrupleRelatedSet P T p)
    (profiniteCechQuadrupleRelatedSet_isClosed P T p) c

#print axioms profiniteCechQuadrupleRelatedSet_isClosed
#print axioms integerLocallyConstant_extendCechQuadruple
end CMDG.CondensedCM5R0
