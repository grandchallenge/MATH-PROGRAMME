import CMDGCondensedCM4P3DerivedCM5R0FreeYonedaAdjunction
import Mathlib.Condensed.Epi
import Mathlib.CategoryTheory.Abelian.Projective.Dimension

/-!
# CM5: free condensed modules on Stonean profinite probes are projective

This is the first *condensed-category* positive-degree Ext vanishing
result on a genuinely infinite-capable test family.  Stonean spaces
are a strict subclass of profinite spaces, so the theorem does not
establish arbitrary-profinite Ext vanishing or derived solidity.

Proof: the canonical free-profinite Hom/sections equivalence is
natural in the target. An epimorphism of condensed modules is
surjective on evaluation at Stonean test objects. Together these
give the projective lifting property for the actual free condensed
module, hence all positive-degree Ext groups out of it vanish.
-/

noncomputable section

universe u

open CategoryTheory

namespace CMDG.CondensedCM5R0

/-- The previously established free-Hom/sections equivalence commutes
with maps of target condensed modules, at arbitrary profinite T. -/
theorem freeProfiniteSectionsEquiv_naturality_target
    (T : Profinite.{u}) {A B : Ambient}
    (g : ((Condensed.profiniteFree Coeff).obj T) ⟶ A) (f : A ⟶ B) :
    freeProfiniteSectionsEquiv T B (g ≫ f) =
      (((Condensed.forget Coeff).map f).hom.app
        (Opposite.op (profiniteToCompHaus.obj T)))
        (freeProfiniteSectionsEquiv T A g) := by
  change (coherentTopology CompHaus).uliftYonedaEquiv
      (freeProfiniteHomEquiv T B (g ≫ f)) =
    (((Condensed.forget Coeff).map f).hom.app
      (Opposite.op (profiniteToCompHaus.obj T)))
      ((coherentTopology CompHaus).uliftYonedaEquiv (freeProfiniteHomEquiv T A g))
  rw [freeProfiniteHomEquiv_naturality_target]
  exact (coherentTopology CompHaus).uliftYonedaEquiv_comp _ _

/-- The actual free condensed module on a Stonean test is projective,
even when that Stonean space is infinite. -/
theorem freeStonean_projective (S : Stonean.{u}) :
    Projective
      ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj S)) := by
  let T : Profinite.{u} := Stonean.toProfinite.obj S
  constructor
  intro E X g e he
  have hsurj :
      Function.Surjective
        (((Condensed.forget Coeff).map e).hom.app
          (Opposite.op (profiniteToCompHaus.obj T))) := by
    change Function.Surjective (e.hom.app (Opposite.op S.compHaus))
    exact (CondensedMod.epi_iff_surjective_on_stonean Coeff e).mp he S
  obtain ⟨x, hx⟩ := hsurj (freeProfiniteSectionsEquiv T X g)
  refine ⟨(freeProfiniteSectionsEquiv T E).symm x, ?_⟩
  apply (freeProfiniteSectionsEquiv T X).injective
  rw [freeProfiniteSectionsEquiv_naturality_target, Equiv.apply_symm_apply]
  exact hx

/-- Higher Ext from the free condensed module on a Stonean test
vanishes in the actual universe-lifted condensed-module category. -/
theorem freeStonean_extPositive_eq_zero
    (S : Stonean.{u}) (A : Ambient) (n : ℕ)
    (e : Abelian.Ext
      ((Condensed.profiniteFree Coeff).obj (Stonean.toProfinite.obj S)) A (n + 1)) :
    e = 0 := by
  letI : Projective
      ((Condensed.profiniteFree Coeff).obj (Stonean.toProfinite.obj S)) :=
    freeStonean_projective S
  exact e.eq_zero_of_projective

#print axioms freeProfiniteSectionsEquiv_naturality_target
#print axioms freeStonean_projective
#print axioms freeStonean_extPositive_eq_zero

end CMDG.CondensedCM5R0
