import CMDGCondensedCM4P3GBasisBooleanPairing

/-!
# CMDG CM4-P3-G generic free/section interface

This successor fixture generalizes the already-certified lower-Hom/Yoneda calculation from the
coefficient target to an arbitrary condensed module. It is the exact interface needed to turn a
section of a finite measure object over a profinite parameter space into a morphism from the
corresponding profinite-free condensed module.
-/

namespace CMDG.CondensedCM4P3G.FreeSections

universe u

open CategoryTheory Opposite

abbrev R := CMDG.CondensedCM4P3G.R.{u}

abbrev FreeHom (T : Profinite.{u}) (A : CondensedMod.{u} R) :=
  (Condensed.profiniteFree R).obj T ⟶ A

abbrev Sections (T : Profinite.{u}) (A : CondensedMod.{u} R) :=
  ((Condensed.forget R).obj A).obj.obj (op ((profiniteToCompHaus).obj T))

/-- Morphisms from the profinite free object are canonically the target sections over the same
profinite space. -/
noncomputable def freeHomSectionsEquiv (T : Profinite.{u}) (A : CondensedMod.{u} R) :
    FreeHom T A ≃ Sections T A := by
  change
    (((Condensed.free R).obj ((profiniteToCondensed).obj T) ⟶ A) ≃ Sections T A)
  refine ((Condensed.freeForgetAdjunction R).homEquiv
    ((profiniteToCondensed).obj T) A).trans ?_
  change
    (((coherentTopology CompHaus.{u}).uliftYoneda.obj ((profiniteToCompHaus).obj T) ⟶
      (Condensed.forget R).obj A) ≃ Sections T A)
  exact (coherentTopology CompHaus.{u}).uliftYonedaEquiv

/-- Naturality in the target condensed module. -/
theorem freeHomSectionsEquiv_postcomp
    (T : Profinite.{u}) {A B : CondensedMod.{u} R}
    (g : FreeHom T A) (f : A ⟶ B) :
    freeHomSectionsEquiv T B (g ≫ f) =
      ((Condensed.forget R).map f).obj.app
        (op ((profiniteToCompHaus).obj T))
        (freeHomSectionsEquiv T A g) := by
  change
    (coherentTopology CompHaus.{u}).uliftYonedaEquiv
      ((Condensed.freeForgetAdjunction R).homEquiv
        ((profiniteToCondensed).obj T) B (g ≫ f)) = _
  rw [(Condensed.freeForgetAdjunction R).homEquiv_naturality_right]
  exact (coherentTopology CompHaus.{u}).uliftYonedaEquiv_naturality_right
    ((Condensed.freeForgetAdjunction R).homEquiv
      ((profiniteToCondensed).obj T) A g)
    ((Condensed.forget R).map f)

#print freeHomSectionsEquiv
#print freeHomSectionsEquiv_postcomp
#print axioms freeHomSectionsEquiv
#print axioms freeHomSectionsEquiv_postcomp

end CMDG.CondensedCM4P3G.FreeSections
