import CMDGCondensedCM4P3DerivedCM5R0CechDegreeOneEpiCriterion
import Mathlib.CategoryTheory.Abelian.Exact
import Mathlib.CategoryTheory.Sites.DenseSubsite.SheafEquiv

/-!
# CMDG CM5 — exactness transfer from the dense Stonean site

Protected predecessor theorems establish the actual presheaf Čech
differentials, the exact sheafification functor, its natural
dense Stonean/CompHaus compatibility, and the criterion
Epi(F_triples → L_T) iff exactness of the actual Čech complex.

THIS MODULE shows that exactness of the genuine free Čech
PRESHEAF complex restricted to Stonean test objects implies
global exactness in CondensedMod. The proof transports the
short complex through the exact Stonean sheafification, a
NATURAL functor iso for the dense site, and reflection of
exactness by the fully faithful Stonean/CompHaus equivalence.

The missing next theorem is exactness of the Stonean presheaf
complex via the pointwise Stonean-projective Hom-set bar
contraction. This file neither assumes that as globally
proved nor asserts unconditional epi, Ext² vanishing, or
higher derived solidity.
-/

noncomputable section

universe u

open CategoryTheory Limits

namespace CMDG.CondensedCM5R0

/-- Restriction of genuine module presheaves from CompHaus to Stonean. -/
noncomputable abbrev stoneanPresheafRestriction :
    (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) ⥤
      (Stonean.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  (Functor.whiskeringLeft _ _ (ModuleCat Coeff)).obj
    Stonean.toCompHaus.op

/-- Genuine coherent Stonean module sheafification. -/
noncomputable abbrev stoneanModuleSheafification :
    (Stonean.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) ⥤
      Sheaf (coherentTopology Stonean) (ModuleCat Coeff) :=
  presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff)

/-- The ACTUAL free Čech degree-one presheaf complex
restricted to the dense Stonean site. -/
noncomputable abbrev stoneanRestrictedCechDegreeOneComplex
    (T : Profinite.{u}) :
    ShortComplex (Stonean.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  (presheafStoneanCechDegreeOneComplex T).map
    stoneanPresheafRestriction

/-- Genuine global exactness follows from Stonean presheaf
exactness, by the exact natural dense-site comparison. -/
theorem stoneanCechDegreeOneExact_of_stoneanPresheafExact
    (T : Profinite.{u})
    (h : (stoneanRestrictedCechDegreeOneComplex T).Exact) :
    (stoneanCechDegreeOneComplex T).Exact := by
  let S := presheafStoneanCechDegreeOneComplex T
  let R := stoneanPresheafRestriction
  let A := stoneanModuleSheafification
  let E := (Condensed.StoneanCompHaus.equivalence
    (ModuleCat Coeff)).inverse
  haveI : PreservesFiniteLimits A := by
    change PreservesFiniteLimits
      (presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff))
    infer_instance
  haveI : PreservesFiniteColimits A := by
    change PreservesFiniteColimits
      (presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff))
    infer_instance
  have hStonean : ((S.map R).map A).Exact := h.map A
  have hStonean' : (S.map (R ⋙ A)).Exact := by
    simpa only [ShortComplex.map_comp] using hStonean
  have hTransport :
      (S.map (moduleSheafification ⋙ E)).Exact := by
    exact ShortComplex.exact_of_iso
      (S.mapNatIso stoneanCompHausSheafificationCompatibility)
      hStonean'
  have hTransport' :
      ((S.map moduleSheafification).map E).Exact := by
    simpa only [ShortComplex.map_comp] using hTransport
  have hComp : (S.map moduleSheafification).Exact :=
    E.reflects_exact_of_faithful _ hTransport'
  let e : S.map moduleSheafification ≅
      stoneanCechDegreeOneComplex T :=
    ShortComplex.isoMk (Iso.refl _) (Iso.refl _) (Iso.refl _)
      (by simpa only [Iso.refl_hom, Category.id_comp, Category.comp_id]
        using (presheafStoneanCechDegreeOneComplex_sheafify_f T).symm)
      (by simpa only [Iso.refl_hom, Category.id_comp, Category.comp_id]
        using (presheafStoneanCechDegreeOneComplex_sheafify_g T).symm)
  exact ShortComplex.exact_of_iso e hComp

/-- The authentic second-relation epi follows from exactness
on the dense Stonean PRESHEAF site. -/
theorem stoneanCechTripleToSecondRelation_epi_of_stoneanPresheafExact
    (T : Profinite.{u})
    (h : (stoneanRestrictedCechDegreeOneComplex T).Exact) :
    Epi (stoneanCechTripleToSecondRelation T) :=
  stoneanCechTripleToSecondRelation_epi_of_degreeOneExact T
    (stoneanCechDegreeOneExact_of_stoneanPresheafExact T h)

#check stoneanRestrictedCechDegreeOneComplex
#check stoneanCechDegreeOneExact_of_stoneanPresheafExact
#print axioms stoneanCechDegreeOneExact_of_stoneanPresheafExact
#print axioms stoneanCechTripleToSecondRelation_epi_of_stoneanPresheafExact

end CMDG.CondensedCM5R0
