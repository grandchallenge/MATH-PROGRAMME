import CMDGCondensedCM4P3DerivedCM5R0StoneanDenseSheafification
import CMDGCondensedCM4P3DerivedCM5R0GSCechTripleBoundary
import Mathlib.CategoryTheory.Preadditive.AdditiveFunctor

/-!
# CMDG CM5 — natural comparison of the TRUE Čech face differentials

Fix an arbitrary (not necessarily finite or Stonean) profinite T,
and its genuine canonical Stonean presentation P(T) → T.

We construct the first and second alternating Čech differentials
BEFORE SHEAFIFICATION, in the genuine free-module PRESHEAF category
on CompHaus. They use the actual two pair projections and three
triple projections of the original profinite Čech objects.

We prove that the presheaf maps satisfy d₂ ≫ d₁ = 0, using the
actual categorical pullback equations, not mere assumed descent.

We then prove, NATURALLY via the true sheafification functor,
that the two presheaf differentials become EXACTLY the existing
free CONDENSED module differentials already admitted on main.
This resolves the face-map/sign-compatibility part of the
global Čech descent bridge.

CAVEAT: The underlying free-module presheaf chain complex is
objectwise exact on Stonean probes only. The remaining step is
to transport that objectwise exactness to the full Stonean
presheaf short complex, by an explicit Čech-nerve comparison
under restricted Yoneda, then use exact sheafification / dense
Stonean equivalence to obtain global exactness in CondensedMod.

No global epi F_triples → L_T, Ext² vanishing, or derived solidity
is asserted here.
-/

noncomputable section

universe u

open CategoryTheory Limits CategoryTheory.Functor

namespace CMDG.CondensedCM5R0

/-- Actual presheaf alternating d₁ on pairs, with the
sign convention (x,y) ↦ x-y used in the protected source. -/
noncomputable def presheafStoneanCechDifference
    (T : Profinite.{u}) :
    freeCompHausModulePresheaf
      (stoneanPresentationCechPairs T) ⟶
    freeCompHausModulePresheaf
      (Stonean.toProfinite.obj T.presentation) :=
  freeCompHausModulePresheafFunctor.map
      (pullback.fst (Profinite.presentation.π T) (Profinite.presentation.π T)) -
    freeCompHausModulePresheafFunctor.map
      (pullback.snd (Profinite.presentation.π T) (Profinite.presentation.π T))

/-- Actual presheaf alternating d₂ on triples. The ordering and
signs match the protected d₂ = (x,z)-(x,y)-(y,z). -/
noncomputable def presheafStoneanCechTripleBoundary
    (T : Profinite.{u}) :
    freeCompHausModulePresheaf
      (stoneanPresentationCechTriples T) ⟶
    freeCompHausModulePresheaf
      (stoneanPresentationCechPairs T) :=
  freeCompHausModulePresheafFunctor.map (stoneanCechTripleXZ T) -
    freeCompHausModulePresheafFunctor.map (stoneanCechTripleXY T) -
    freeCompHausModulePresheafFunctor.map (stoneanCechTripleYZ T)

/-- Genuine presheaf Čech triple relation; the equality uses
only the pullback equations on the ACTUAL profinite triple. -/
theorem presheafStoneanCechDifference_triple
    (T : Profinite.{u}) :
    freeCompHausModulePresheafFunctor.map (stoneanCechTripleXZ T) ≫
        presheafStoneanCechDifference T =
      (freeCompHausModulePresheafFunctor.map (stoneanCechTripleXY T) ≫
        presheafStoneanCechDifference T) +
      (freeCompHausModulePresheafFunctor.map (stoneanCechTripleYZ T) ≫
        presheafStoneanCechDifference T) := by
  unfold presheafStoneanCechDifference
  simp only [Preadditive.comp_sub, ← Functor.map_comp,
    stoneanCechTripleXZ, stoneanCechTripleYZ,
    pullback.lift_fst, pullback.lift_snd]
  abel

/-- The actual presheaf faces form a complex in degrees 2→1→0.
This is a structural statement, not a claim of exactness. -/
theorem presheafStoneanCechTripleBoundary_comp_difference_zero
    (T : Profinite.{u}) :
    presheafStoneanCechTripleBoundary T ≫
      presheafStoneanCechDifference T = 0 := by
  unfold presheafStoneanCechTripleBoundary
  simp only [Preadditive.sub_comp]
  rw [presheafStoneanCechDifference_triple]
  simp only [add_sub_cancel_left, sub_self]

/-- Sheafification of the presheaf d₁ is literally the
genuine already-protected CondensedMod differential. -/
theorem presheafStoneanCechDifference_sheafify
    (T : Profinite.{u}) :
    moduleSheafification.map (presheafStoneanCechDifference T) =
      stoneanCechDifference T := by
  unfold presheafStoneanCechDifference stoneanCechDifference
  rw [Functor.map_sub]
  rfl

/-- Sheafification of the presheaf d₂ is literally the
genuine already-protected CondensedMod alternating triple boundary.
This pins EVERY sign and actual Čech face at degree 2. -/
theorem presheafStoneanCechTripleBoundary_sheafify
    (T : Profinite.{u}) :
    moduleSheafification.map (presheafStoneanCechTripleBoundary T) =
      stoneanCechTripleBoundary T := by
  unfold presheafStoneanCechTripleBoundary stoneanCechTripleBoundary
  rw [Functor.map_sub, Functor.map_sub]
  rfl

/-- The actual two-step free-presheaf Čech short complex;
all its objects are the authentic free-module presheaves. -/
noncomputable def presheafStoneanCechDegreeOneComplex
    (T : Profinite.{u}) :
    ShortComplex (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk
    (presheafStoneanCechTripleBoundary T)
    (presheafStoneanCechDifference T)
    (presheafStoneanCechTripleBoundary_comp_difference_zero T)

/-- Applying the true exact sheafification functor to the
presheaf complex recovers a short complex whose components and
differentials are definitionally the genuine d₂,d₁.
No surrogate module functor is used here. -/
theorem presheafStoneanCechDegreeOneComplex_sheafify_f
    (T : Profinite.{u}) :
    (presheafStoneanCechDegreeOneComplex T |>.map
      moduleSheafification).f = stoneanCechTripleBoundary T :=
  presheafStoneanCechTripleBoundary_sheafify T

theorem presheafStoneanCechDegreeOneComplex_sheafify_g
    (T : Profinite.{u}) :
    (presheafStoneanCechDegreeOneComplex T |>.map
      moduleSheafification).g = stoneanCechDifference T :=
  presheafStoneanCechDifference_sheafify T

#check presheafStoneanCechDegreeOneComplex
#check presheafStoneanCechTripleBoundary_sheafify
#print axioms presheafStoneanCechDifference_triple
#print axioms presheafStoneanCechTripleBoundary_comp_difference_zero
#print axioms presheafStoneanCechDifference_sheafify
#print axioms presheafStoneanCechTripleBoundary_sheafify
#print axioms presheafStoneanCechDegreeOneComplex_sheafify_f
#print axioms presheafStoneanCechDegreeOneComplex_sheafify_g

end CMDG.CondensedCM5R0
