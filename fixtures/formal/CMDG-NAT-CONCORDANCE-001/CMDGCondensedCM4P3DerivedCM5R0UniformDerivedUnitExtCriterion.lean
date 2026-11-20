import CMDGCondensedCM4P3DerivedCM5R0PositiveShifts
import CMDGCondensedCM4P3DerivedCM5R0UniformGenuineSolidExtAcyclic
import Mathlib.Algebra.Homology.DerivedCategory.Ext.Basic
import Mathlib.CategoryTheory.Shift.ShiftedHom

/-!
# CMDG CM5: full shifted solidification comparison iff higher Ext of solid source vanishes

This file does not assume higher Ext vanishing for the genuine solid source.
It proves a *precise* equivalence: the existing actual shifted comparison is
bijective in every shift if and only if higher Ext out of genuine G_T into G_S
vanishes for every profinite T.

The forward direction uses the exact derived comparison map and the
already-protected Ext vanishing out of F_T. The reverse direction uses
canonical shifted Ext-Hom equivalences, not any projectivity of G_T.
-/

noncomputable section
universe u
open CategoryTheory Pretriangulated
namespace CMDG.CondensedCM5R0

private noncomputable instance : HasDerivedCategory Ambient :=
  HasDerivedCategory.standard Ambient

private noncomputable instance : HasExt.{u + 2} Ambient.{u} :=
  HasExt.standard Ambient.{u}

/-- The actual equivalence from any positive Ext degree to the corresponding
negative *source* shift morphism in the genuine derived category. -/
noncomputable def extPositiveToNegativeSourceHomEquiv
    (X Y : Ambient) (q : ℕ) :
    Abelian.Ext X Y (q + 1) ≃
      ((shiftFunctor (DerivedCategory Ambient) (-(((q + 1 : ℕ) : ℤ)))).obj
        ((DerivedCategory.singleFunctor Ambient 0).obj X)) ⟶
        ((DerivedCategory.singleFunctor Ambient 0).obj Y)) := by
  let A := (DerivedCategory.singleFunctor Ambient 0).obj X
  let B := (DerivedCategory.singleFunctor Ambient 0).obj Y
  let m : ℤ := ((q + 1 : ℕ) : ℤ)
  let F := shiftFunctor (DerivedCategory Ambient) (-m)
  let i : F.obj (B⟦m⟧) ≅ B :=
    ((shiftFunctorAdd' (DerivedCategory Ambient) m (-m) 0
      (by omega)).symm.app B) ≪≫
        ((shiftFunctorZero (DerivedCategory Ambient) ℤ).app B)
  exact (Abelian.Ext.homEquiv (X := X) (Y := Y) (n := q + 1)).trans
    (((Functor.FullyFaithful.ofFullyFaithful F).homEquiv).trans i.homToEquiv)

/-- At a strictly negative source shift the known vanishing on the FREE
source makes the solidification comparison bijective exactly when the
corresponding positive Ext group out of the SOLID source vanishes.

There is no assumption of derived solidity or solid-source acyclicity. -/
theorem comparisonAtShift_negative_bijective_iff_solidExtZero
    (S T : Profinite.{u}) (q : ℕ) :
    Function.Bijective
      (comparisonAtShift S T (-(((q + 1 : ℕ) : ℤ)))) ↔
    (∀ e : Abelian.Ext (underivedObject T) (underivedObject S) (q + 1),
      e = 0) := by
  let hSolid := extPositiveToNegativeSourceHomEquiv
    (underivedObject T) (underivedObject S) q
  let hFree := extPositiveToNegativeSourceHomEquiv
    ((Condensed.profiniteFree Coeff).obj T) (underivedObject S) q
  have hFreeZero :
      ∀ e : Abelian.Ext
        ((Condensed.profiniteFree Coeff).obj T) (underivedObject S) (q + 1),
        e = 0 := by
    exact freeProfinite_extPositive_genuineSolid_zero T S q
  have hCodomain :
      ∀ a b : ((shiftFunctor (DerivedCategory Ambient)
        (-(((q + 1 : ℕ) : ℤ)))).obj (freeAtZero T) ⟶ degreeZeroObject S),
        a = b := by
    intro a b
    apply hFree.symm.injective
    exact (hFreeZero (hFree.symm a)).trans
      (hFreeZero (hFree.symm b)).symm
  constructor
  · intro hBij e
    apply hSolid.injective
    apply hBij.1
    exact hCodomain _ _
  · intro hZero
    constructor
    · intro a b _
      apply hSolid.symm.injective
      exact (hZero (hSolid.symm a)).trans
        (hZero (hSolid.symm b)).symm
    · intro y
      refine ⟨0, ?_⟩
      exact hCodomain _ _

/-- The EXISTING complete all-integer-shifts comparison candidate is
equivalent to one remaining source-side Ext-acyclicity family. This is
a source-faithful exact criterion, not a claim that the family vanishes.

The nonnegative comparisons are already proven by CM4 and the t-structure.
All negative comparisons are now reduced without further chain/shift gaps. -/
theorem shiftedComparisonCandidate_iff_genuineSolidSourceExtZero
    (S : Profinite.{u}) :
    ShiftedComparisonBijectiveCandidate S ↔
      (∀ (T : Profinite.{u}) (q : ℕ)
        (e : Abelian.Ext (underivedObject T) (underivedObject S) (q + 1)),
        e = 0) := by
  constructor
  · intro h T q
    exact (comparisonAtShift_negative_bijective_iff_solidExtZero
      S T q).1 (h T (-(((q + 1 : ℕ) : ℤ))))
  · intro h T n
    by_cases hn : 0 ≤ n
    · exact comparisonAtShift_nonneg_bijective S T n hn
    · have hneg : n < 0 := lt_of_not_ge hn
      let q : ℕ := Int.toNat (-n - 1)
      have hq : n = -(((q + 1 : ℕ) : ℤ)) := by
        dsimp [q]
        omega
      rw [hq]
      exact (comparisonAtShift_negative_bijective_iff_solidExtZero
        S T q).2 (h T q)

#print axioms extPositiveToNegativeSourceHomEquiv
#print axioms comparisonAtShift_negative_bijective_iff_solidExtZero
#print axioms shiftedComparisonCandidate_iff_genuineSolidSourceExtZero

end CMDG.CondensedCM5R0
