import CMDGCondensedCM4P3DerivedCM5R0CechExtOnePotentialEquivalence
import CMDGCondensedCM4P3DerivedCM5R0FreeYonedaAdjunction

/-!
# CM5: genuine Čech cochains as sections of the actual solid condensed target

The projective Stonean presentation of an arbitrary profinite T supplies
an actual profinite Čech pair object P(T) ×_T P(T).  The free/forgetful
adjunction and profinite Yoneda evaluation identify genuine morphisms
from its free condensed module into the protected underived solid target
G_S with sections of the underlying condensed sheaf on *that exact pair*.

The same identification on the Stonean source transports the genuine
Čech difference to an actual coboundary operation on solid sections.
It yields an equivalent section-level criterion for Ext¹ vanishing,
and proves that a section pulled back from the base has zero coboundary.

This is a precise degree-zero bridge from actual condensed-module
morphisms to actual sheaf sections. It is NOT a representation of those
sections by finite-quotient cocycles, a compatible inverse-limit
potential construction, an Ext¹ vanishing result, or derived solidity.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- The true section type of the protected CM4 solid object G_S on an
arbitrary profinite test X, with all universe lifts retained. -/
abbrev solidSections (S X : Profinite.{u}) :=
  ((Condensed.forget Coeff).obj (underivedObject S)).obj.obj
    (Opposite.op (profiniteToCompHaus.obj X))

/-- Genuine Čech pair cochains in the actual ambient abelian category
are exactly sections of the underlying condensed target on that pair. -/
noncomputable def stoneanCechCochainSectionsEquiv
    (T S : Profinite.{u}) :
    (((Condensed.profiniteFree Coeff).obj (stoneanPresentationCechPairs T)) ⟶
      underivedObject S) ≃ solidSections S (stoneanPresentationCechPairs T) :=
  freeProfiniteSectionsEquiv (stoneanPresentationCechPairs T) (underivedObject S)

/-- Genuine Stonean potentials are exactly sections of G_S on P(T). -/
noncomputable def stoneanCechPotentialSectionsEquiv
    (T S : Profinite.{u}) :
    (((Condensed.profiniteFree Coeff).obj
       (Stonean.toProfinite.obj T.presentation)) ⟶ underivedObject S) ≃
      solidSections S (Stonean.toProfinite.obj T.presentation) :=
  freeProfiniteSectionsEquiv
    (Stonean.toProfinite.obj T.presentation) (underivedObject S)

/-- The genuine relation functional of an actual kernel map,
transported into a section of the actual sheaf on the Čech pair. -/
noncomputable def stoneanCechSolidRelationSection
    (T S : Profinite.{u})
    (f : stoneanPresentationKernel T ⟶ underivedObject S) :
    solidSections S (stoneanPresentationCechPairs T) :=
  stoneanCechCochainSectionsEquiv T S
    (stoneanCechSolidRelationFunctional T S f)

/-- Genuine Čech differential: a solid section on the Stonean source
gives a section on the actual fiber-product pair. It is defined by
transporting the proven free-module difference, so no pairwise
set-function or finite-factorization hypothesis is inserted. -/
noncomputable def stoneanCechSolidSectionCoboundary
    (T S : Profinite.{u}) :
    solidSections S (Stonean.toProfinite.obj T.presentation) →
      solidSections S (stoneanPresentationCechPairs T) :=
  fun b => stoneanCechCochainSectionsEquiv T S
    (stoneanCechDifference T ≫
      (stoneanCechPotentialSectionsEquiv T S).symm b)

/-- A genuine potential exists for a relation functional if and only
if its actual sheaf-section cochain is the coboundary of an actual
sheaf section on the Stonean source. -/
theorem stoneanCechSectionPotential_iff_modulePotential
    (T S : Profinite.{u})
    (f : stoneanPresentationKernel T ⟶ underivedObject S) :
    (∃ b : solidSections S (Stonean.toProfinite.obj T.presentation),
      stoneanCechSolidSectionCoboundary T S b =
        stoneanCechSolidRelationSection T S f) ↔
    (∃ g : ((Condensed.profiniteFree Coeff).obj
        (Stonean.toProfinite.obj T.presentation)) ⟶ underivedObject S,
      stoneanCechDifference T ≫ g =
        stoneanCechSolidRelationFunctional T S f) := by
  constructor
  · rintro ⟨b, hb⟩
    refine ⟨(stoneanCechPotentialSectionsEquiv T S).symm b, ?_⟩
    apply (stoneanCechCochainSectionsEquiv T S).injective
    exact hb
  · rintro ⟨g, hg⟩
    refine ⟨stoneanCechPotentialSectionsEquiv T S g, ?_⟩
    change (stoneanCechCochainSectionsEquiv T S)
        (stoneanCechDifference T ≫
          (stoneanCechPotentialSectionsEquiv T S).symm
            (stoneanCechPotentialSectionsEquiv T S g)) =
      (stoneanCechCochainSectionsEquiv T S)
        (stoneanCechSolidRelationFunctional T S f)
    simpa only [Equiv.symm_apply_apply] using
      congrArg (stoneanCechCochainSectionsEquiv T S) hg

/-- A true solid section pulled back from the base T to P(T)
has zero Čech difference, expressed via the zero ambient morphism.
This is a genuine condensed-module computation, not a pointwise
finite-fiber calculation. -/
theorem stoneanCechSolidSectionCoboundary_of_base
    (T S : Profinite.{u})
    (h : ((Condensed.profiniteFree Coeff).obj T) ⟶ underivedObject S) :
    stoneanCechSolidSectionCoboundary T S
        (stoneanCechPotentialSectionsEquiv T S
          (freeStoneanPresentationMap T ≫ h)) =
      stoneanCechCochainSectionsEquiv T S (0 :
        ((Condensed.profiniteFree Coeff).obj (stoneanPresentationCechPairs T)) ⟶
        underivedObject S) := by
  change (stoneanCechCochainSectionsEquiv T S)
      (stoneanCechDifference T ≫
        (stoneanCechPotentialSectionsEquiv T S).symm
          (stoneanCechPotentialSectionsEquiv T S
            (freeStoneanPresentationMap T ≫ h))) =
    stoneanCechCochainSectionsEquiv T S 0
  simp only [Equiv.symm_apply_apply]
  rw [← Category.assoc, stoneanCechDifference_comp_zero, zero_comp]

/-- The missing arbitrary-profinite Ext¹-vanishing condition is
*equivalent* to every actual Čech relation section having a genuine
Stonean-source section potential. The theorem does not construct
potentials or assert the left or right side. -/
theorem freeProfinite_extOne_vanishes_iff_all_solidCechSectionPotentials
    (T S : Profinite.{u}) :
    (∀ e : Abelian.Ext
        ((Condensed.profiniteFree Coeff).obj T) (underivedObject S) 1,
        e = 0) ↔
      (∀ f : stoneanPresentationKernel T ⟶ underivedObject S,
        ∃ b : solidSections S (Stonean.toProfinite.obj T.presentation),
          stoneanCechSolidSectionCoboundary T S b =
            stoneanCechSolidRelationSection T S f) := by
  rw [freeProfinite_extOne_vanishes_iff_all_solidCechPotentials]
  exact forall_congr' (fun f =>
    (stoneanCechSectionPotential_iff_modulePotential T S f).symm)

#print axioms stoneanCechCochainSectionsEquiv
#print axioms stoneanCechPotentialSectionsEquiv
#print axioms stoneanCechSectionPotential_iff_modulePotential
#print axioms stoneanCechSolidSectionCoboundary_of_base
#print axioms freeProfinite_extOne_vanishes_iff_all_solidCechSectionPotentials

end CMDG.CondensedCM5R0
