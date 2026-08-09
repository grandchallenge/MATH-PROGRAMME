import Mathlib.Condensed.Solid
import Mathlib.Algebra.Category.ModuleCat.ChangeOfRings
import Mathlib.CategoryTheory.Sites.Whiskering
import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.RingTheory.FiniteType
import Mathlib.Algebra.Ring.ULift

/-!
CMDG-SOLID-C05-001 definition/concordance fixture.

This file intentionally separates the pinned `CondensedMod.IsSolid` predicate,
the source-concordant finite-type commutative `ℤ`-algebra restriction, and an
elementwise reconstruction for arbitrary commutative rings using restriction
of scalars along `ℤ[X] → R`, `X ↦ r`.

No equivalence between the pinned arbitrary-`Ring` predicate and the reconstructed
commutative-ring predicate is asserted. No solid-object theorem, solid subcategory,
reflector, tensor closure, derived statement, liquid statement, CM4, C06,
`GRAPH_CERTIFIED`, minimality, or completeness claim is made.
-/

noncomputable section

open CategoryTheory
open CategoryTheory.Limits
open Polynomial

universe u

namespace CMDG.SolidC05

noncomputable def c05ProfiniteSolid
    (R : Type (u + 1)) [Ring R] :
    Profinite.{u} ⥤ CondensedMod.{u} R :=
  Condensed.profiniteSolid R

noncomputable def c05PointwiseRightKan
    (R : Type (u + 1)) [Ring R] :
    (Functor.RightExtension.mk _
      (Condensed.profiniteSolidCounit R)).IsPointwiseRightKanExtension :=
  Condensed.profiniteSolidIsPointwiseRightKanExtension R

noncomputable def c05Solidification
    (R : Type (u + 1)) [Ring R] :
    Condensed.profiniteFree R ⟶ Condensed.profiniteSolid.{u} R :=
  Condensed.profiniteSolidification R

noncomputable def pinnedSolidField
    (R : Type (u + 1)) [Ring R]
    (A : CondensedMod.{u} R) [hA : CondensedMod.IsSolid R A] :
    ∀ X : Profinite.{u},
      IsIso ((yoneda.obj A).map
        ((Condensed.profiniteSolidification R).app X).op) :=
  hA.isIso_solidification_map

/-- Restricted source-concordant wrapper for finite-type commutative `ℤ`-algebras. -/
def FiniteTypeZAlgebraSolid
    (R : Type (u + 1)) [CommRing R] [Algebra ℤ R]
    [Algebra.FiniteType ℤ R] (A : CondensedMod.{u} R) : Prop :=
  CondensedMod.IsSolid R A

/-- Universe-lifted implementation representative of `ℤ[X]`. -/
abbrev ZX : Type (u + 1) := ULift.{u + 1} (Polynomial ℤ)

/-- Evaluation `ℤ[X] → R`, transported from the universe-lifted copy. -/
def evalZXAt
    (R : Type (u + 1)) [CommRing R] (r : R) :
    ZX.{u} →+* R :=
  (Polynomial.eval₂RingHom (Int.castRingHom R) r).comp
    (ULift.ringEquiv (R := Polynomial ℤ)).toRingHom

/-- Restriction of scalars on condensed modules by pointwise composition of sheaves. -/
noncomputable def restrictCondensedScalars
    {R S : Type (u + 1)} [Ring R] [Ring S] (f : R →+* S) :
    CondensedMod.{u} S ⥤ CondensedMod.{u} R :=
  sheafCompose _ (ModuleCat.restrictScalars f)

/--
C05 general commutative-ring reconstruction: for every `r : R`, restrict along
`ℤ[X] → R`, `X ↦ r`, and require the resulting `ℤ[X]`-module to satisfy the
pinned solidification-map condition. This is a definition, not an equivalence theorem.
-/
def GeneralCommRingSolidReconstructed
    (R : Type (u + 1)) [CommRing R] (A : CondensedMod.{u} R) : Prop :=
  ∀ r : R,
    CondensedMod.IsSolid ZX
      ((restrictCondensedScalars (evalZXAt R r)).obj A)

end CMDG.SolidC05
