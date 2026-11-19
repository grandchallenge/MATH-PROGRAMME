import CMDGCondensedCM4P3DerivedCM5R0UniformArityFiniteObservation
import CMDGCondensedCM4P3DerivedCM5R0UniformRelationFiniteObservation

/-!
# Genuine all-arity profinite Čech relation complex

For every profinite morphism p:P→T, construct continuous deletion
face maps between the true closed equal-image tuple spaces and the
alternating scalar differential, with no quotient surrogate.
-/

noncomputable section
universe u v
open Set CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Delete one coordinate of a genuinely related tuple, retaining
the true profinite equal-image condition. -/
def uniformProfiniteRelationFaceMap
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (k : Fin (n + 2)) :
    C(↥(profiniteCechArityRelatedSet (n + 1) P T p),
      ↥(profiniteCechArityRelatedSet n P T p)) :=
  ⟨fun xs =>
    ⟨xs.val ∘ k.succAbove, by
      intro i
      exact (xs.property (k.succAbove i)).trans
        (xs.property (k.succAbove 0)).symm⟩,
    Continuous.subtype_mk
      (by
        apply continuous_pi
        intro i
        exact (continuous_apply (k.succAbove i)).comp
          continuous_subtype_val) _⟩

/-- Genuine unnormalized all-tuple Čech differential for the
closed relations of p. -/
def uniformProfiniteRelationDifferential
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ) :
    LocallyConstant (↥(profiniteCechArityRelatedSet n P T p)) ℤ →
    LocallyConstant (↥(profiniteCechArityRelatedSet (n + 1) P T p)) ℤ :=
  fun c => ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
    c.comap (uniformProfiniteRelationFaceMap P T p n k)

theorem uniformProfiniteRelationDifferential_apply
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (c : LocallyConstant (↥(profiniteCechArityRelatedSet n P T p)) ℤ)
    (xs : ↥(profiniteCechArityRelatedSet (n + 1) P T p)) :
    (uniformProfiniteRelationDifferential P T p n c) xs =
      ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) *
        c (uniformProfiniteRelationFaceMap P T p n k xs) := by
  change (LocallyConstant.evalₗ ℤ xs)
    (∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) •
      c.comap (uniformProfiniteRelationFaceMap P T p n k)) =
    ∑ k : Fin (n + 2), (-1 : ℤ) ^ (k : ℕ) *
      c (uniformProfiniteRelationFaceMap P T p n k xs)
  simp only [map_sum, map_smul, LocallyConstant.evalₗ_apply,
    smul_eq_mul]
  rfl

/-- **Unconditional all-positive-degree scalar Čech exactness on the
genuine closed equal-image profinite relations.** This is not merely
the finite-closed-cover surrogate: c is a locally constant function
on the actual relation R_(n+2), and the primitive is a locally constant
function on R_(n+1) for an arbitrary map p:P→T.

The proof extends the relation cochain to the ambient finite product,
finds one finite clopen coordinate observation at the given arity,
uses finite closed-family all-degree exactness, and reassembles the
primitive continuously on the actual relation. -/
theorem uniformProfiniteRelationAllPositive_cocycle_coboundary
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    (c : LocallyConstant
      (↥(profiniteCechArityRelatedSet (n + 1) P T p)) ℤ)
    (hc : uniformProfiniteRelationDifferential P T p (n + 1) c = 0) :
    ∃ b : LocallyConstant
        (↥(profiniteCechArityRelatedSet n P T p)) ℤ,
      uniformProfiniteRelationDifferential P T p n b = c := by
  classical
  obtain ⟨C,hC⟩ :=
    integerCechArityRelated_locallyConstant_extends
      (n + 1) P T p c
  obtain ⟨J,fintJ,q,d,hfact⟩ :=
    integerLocallyConstant_allFiniteArity_finiteObservation
      P (n + 1) C
  letI : Fintype J := fintJ
  have hdc : ∀ xs : Fin (n + 3) → P,
      (∀ i : Fin (n + 3),
        p.hom.hom (xs i) = p.hom.hom (xs 0)) →
      (∑ k : Fin (n + 3),
        (-1 : ℤ) ^ (k : ℕ) *
          d (fun j => q (xs (k.succAbove j)))) = 0 := by
    intro xs hrel
    have hface (k : Fin (n + 3)) :
        (xs ∘ k.succAbove) ∈
          profiniteCechArityRelatedSet (n + 1) P T p := by
      intro j
      exact (hrel (k.succAbove j)).trans
        (hrel (k.succAbove 0)).symm
    have hz :
        (uniformProfiniteRelationDifferential P T p (n + 1) c)
          ⟨xs,hrel⟩ = 0 := by
      rw [hc]
      rfl
    rw [uniformProfiniteRelationDifferential_apply] at hz
    calc
      (∑ k : Fin (n + 3),
        (-1 : ℤ) ^ (k : ℕ) *
          d (fun j => q (xs (k.succAbove j)))) =
        (∑ k : Fin (n + 3),
          (-1 : ℤ) ^ (k : ℕ) *
            C (xs ∘ k.succAbove)) := by
          apply Finset.sum_congr rfl
          intro k hk
          rw [hfact (xs ∘ k.succAbove)]
          rfl
      _ = (∑ k : Fin (n + 3),
          (-1 : ℤ) ^ (k : ℕ) *
            c ⟨xs ∘ k.succAbove, hface k⟩) := by
          apply Finset.sum_congr rfl
          intro k hk
          rw [hC ⟨xs ∘ k.succAbove, hface k⟩]
      _ = 0 := by
          convert hz using 1
          apply Finset.sum_congr rfl
          intro k hk
          rfl
  obtain ⟨g,hg⟩ :=
    uniformProfiniteFiniteObserved_relationCocycle_potential
      P T p q n d hdc
  let b : LocallyConstant
      (↥(profiniteCechArityRelatedSet n P T p)) ℤ :=
    g.comap (⟨Subtype.val,continuous_subtype_val⟩ :
      C(↥(profiniteCechArityRelatedSet n P T p),
        Fin (n + 1) → P))
  refine ⟨b, ?_⟩
  apply DFunLike.ext
  intro xs
  have h := hg xs.val xs.property
  rw [← hfact xs.val, hC xs] at h
  rw [uniformProfiniteRelationDifferential_apply]
  change (∑ k : Fin (n + 2),
    (-1 : ℤ) ^ (k : ℕ) * g (xs.val ∘ k.succAbove)) = c xs
  exact h

/-- Arbitrary (including infinite) product-index families of
genuine relation cocycles have coordinatewise actual primitives.
There is no common finite observation across coefficient coordinates. -/
theorem uniformProfiniteRelationAllPositive_product_family
    (P T : Profinite.{u}) (p : P ⟶ T) (n : ℕ)
    {ι : Type v}
    (c : ι → LocallyConstant
      (↥(profiniteCechArityRelatedSet (n + 1) P T p)) ℤ)
    (hc : ∀ a, uniformProfiniteRelationDifferential P T p (n + 1)
      (c a) = 0) :
    ∃ b : ι → LocallyConstant
        (↥(profiniteCechArityRelatedSet n P T p)) ℤ,
      ∀ a, uniformProfiniteRelationDifferential P T p n (b a) =
        c a := by
  classical
  have hex (a : ι) : ∃ b : LocallyConstant
        (↥(profiniteCechArityRelatedSet n P T p)) ℤ,
      uniformProfiniteRelationDifferential P T p n b = c a :=
    uniformProfiniteRelationAllPositive_cocycle_coboundary
      P T p n (c a) (hc a)
  choose b hb using hex
  exact ⟨b, hb⟩

#print axioms uniformProfiniteRelationAllPositive_product_family

#print axioms uniformProfiniteRelationAllPositive_cocycle_coboundary

#print axioms uniformProfiniteRelationDifferential_apply
end CMDG.CondensedCM5R0
