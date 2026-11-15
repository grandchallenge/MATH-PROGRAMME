import CMDGCondensedCM4P3DerivedCM5R0ScalarClopenRectangleFactorization
import Mathlib.Topology.Category.CompHausLike.Limits

/-!
# CM5: actual scalar Čech primitives for arbitrary profinite quotients

The canonical Čech relation of p:P→T is the closed profinite
subspace of P×P consisting of pairs with equal images. Given a
locally constant integer-valued cocycle on this *actual relation*,
first extend it to the entire product (protected closed-subset
extension), then use the pinned finite clopen-box rectangular
factorization and protected finite closed-cover H¹ theorem to
construct a globally locally constant source potential.

The proof requires neither P nor T to be finite and does not
select a potentially discontinuous fiber section. The result is
pure scalar Čech acyclicity; the separate bridge from genuine
condensed-module coefficient sections into scalar locally constant
functions, and the G_S product model, remain later obligations.
-/

noncomputable section

universe u

open CategoryTheory Limits Set

namespace CMDG.CondensedCM5R0

/-- The closed equivalence relation of a profinite morphism,
realized as the honest subtype of the ordinary product. -/
def profiniteCechRelatedSet (P T : Profinite.{u}) (p : P ⟶ T) :
    Set (P × P) :=
  { xy | p.hom.hom xy.1 = p.hom.hom xy.2 }

/-- The honest Čech relation of any profinite map is closed in
the product, even if neither of its projections splits. -/
theorem profiniteCechRelatedSet_isClosed
    (P T : Profinite.{u}) (p : P ⟶ T) :
    IsClosed (profiniteCechRelatedSet P T p) := by
  exact isClosed_eq
    (p.hom.hom.continuous.comp continuous_fst)
    (p.hom.hom.continuous.comp continuous_snd)

/-- Every genuine locally constant scalar Čech 1-cocycle over
an arbitrary profinite map has a continuous source primitive.
The cocycle and coboundary identities are imposed only on
the actual closed relation p(x)=p(y), not all pairs. -/
theorem integerProfiniteCechCocycle_hasPotential
    (P T : Profinite.{u}) (p : P ⟶ T)
    (c : LocallyConstant (↥(profiniteCechRelatedSet P T p)) ℤ)
    (hc : ∀ (x y z : P)
      (hxy : p.hom.hom x = p.hom.hom y)
      (hyz : p.hom.hom y = p.hom.hom z),
      c ⟨(x, z), hxy.trans hyz⟩ =
        c ⟨(x, y), hxy⟩ + c ⟨(y, z), hyz⟩) :
    ∃ b : LocallyConstant P ℤ,
      ∀ (x y : P) (hxy : p.hom.hom x = p.hom.hom y),
        c ⟨(x, y), hxy⟩ = b x - b y := by
  let Q : Profinite.{u} := Profinite.of (P × P)
  obtain ⟨C, hC⟩ :=
    locallyConstant_extend_closed_subset Q
      (profiniteCechRelatedSet P T p)
      (profiniteCechRelatedSet_isClosed P T p) c
  have hCx (x y : P) (hxy : p.hom.hom x = p.hom.hom y) :
      C (x, y) = c ⟨(x, y), hxy⟩ := by
    exact hC ⟨(x, y), hxy⟩
  have hCcocycle : ∀ x y z : P,
      p.hom.hom x = p.hom.hom y →
      p.hom.hom y = p.hom.hom z →
      C (x, z) = C (x, y) + C (y, z) := by
    intro x y z hxy hyz
    rw [hCx x z (hxy.trans hyz), hCx x y hxy, hCx y z hyz]
    exact hc x y z hxy hyz
  obtain ⟨b, hb⟩ :=
    integerProfiniteCocycle_ambientProduct_potential P T p C hCcocycle
  refine ⟨b, ?_⟩
  intro x y hxy
  rw [← hCx x y hxy]
  exact hb x y hxy

/-- Scalar cocycle primitives on the **canonical** Stonean
Čech fiber product. Mathlib's explicit profinite pullback is
the closed subtype of the ordinary pair product, so this is
the exact topological relation used in the CM5 resolution.
This is not yet a statement about G_S-valued condensed sections. -/
theorem integerStoneanCechCocycle_hasPotential
    (T : Profinite.{u})
    (c : LocallyConstant (stoneanPresentationCechPairs T) ℤ)
    (hc : ∀ (x y z : Stonean.toProfinite.obj T.presentation)
      (hxy : (Profinite.presentation.π T).hom.hom x =
        (Profinite.presentation.π T).hom.hom y)
      (hyz : (Profinite.presentation.π T).hom.hom y =
        (Profinite.presentation.π T).hom.hom z),
      c ⟨(x, z), hxy.trans hyz⟩ =
        c ⟨(x, y), hxy⟩ + c ⟨(y, z), hyz⟩) :
    ∃ b : LocallyConstant (Stonean.toProfinite.obj T.presentation) ℤ,
      ∀ (x y : Stonean.toProfinite.obj T.presentation)
        (hxy : (Profinite.presentation.π T).hom.hom x =
          (Profinite.presentation.π T).hom.hom y),
        c ⟨(x, y), hxy⟩ = b x - b y := by
  exact integerProfiniteCechCocycle_hasPotential
    (Stonean.toProfinite.obj T.presentation) T
    (Profinite.presentation.π T) c hc

#print axioms profiniteCechRelatedSet_isClosed
#print axioms integerProfiniteCechCocycle_hasPotential
#print axioms integerStoneanCechCocycle_hasPotential

end CMDG.CondensedCM5R0
