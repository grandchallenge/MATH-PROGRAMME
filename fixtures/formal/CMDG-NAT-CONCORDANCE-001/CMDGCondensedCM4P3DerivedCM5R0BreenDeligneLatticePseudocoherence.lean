import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneLatticeHomology

/-! Unconditional pseudocoherence of the identity finite-lattice
functor, using genuine augmented reduced Eilenberg–Mac Lane complexes
and the checked stable coefficient presentations. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits HomologicalComplex
open scoped ZeroObject
open CMDG.CondensedCM5R0.BreenDeligneFP
open CMDG.CondensedCM5R0.BreenDeligneFPApproximation
open CMDG.CondensedCM5R0.BreenDeligneLatticeFP
open CMDG.CondensedCM5R0.BreenDeligneLatticeAugmentation
open CMDG.CondensedCM5R0.BreenDeligneLatticeHomology
open CMDG.CondensedCM5R0.BreenDeligneLatticeProjectives
open CMDG.CondensedCM5R0.BreenDeligneStableAdditive
namespace CMDG.CondensedCM5R0.BreenDeligneLatticePseudocoherence

theorem stable_fp_all (r n k : ℕ) (hk : k<n) (h : FP latFinite r V) :
    FP latFinite r (valueFunctor ⋙ stableFunctor n k) := by
  cases r with
  | zero => exact stable_fp_zero n k hk h
  | succ r => exact stable_fp r n k hk h

theorem identity_fp (k : ℕ) : FP latFinite k V := by
  induction k using Nat.strong_induction_on with
  | h k ih =>
    cases k with
    | zero =>
      letI := latAug_epi 1
      exact fp0_epi latFinite (latAug 1) (term_fp 1 1 0)
    | succ r =>
      let n := r+2
      let K := augmented n
      apply approximate K latFinite r (augmented_epi n)
      · change FP latFinite (r+1) (Term n n)
        exact term_fp n n (r+1)
      · intro i hi
        change FP latFinite (r-i) (Term n (n+(i+1)))
        exact term_fp n _ _
      · intro i hi
        cases i with
        | zero =>
          have hz : IsZero (K.homology 1) :=
            (ShortComplex.exact_iff_isZero_homology _).mp (augmented_bottom_exact (r+1))
          exact fp_iso latFinite hz.isoZero.symm (fp_of_finite latFinite _ FinitePoly.zero)
        | succ i =>
          exact fp_iso latFinite (shiftedHomologyIso n i).symm
            (stable_fp_all (r-(i+1)) n (i+1) (by dsimp [n]; omega)
              (ih (r-(i+1)) (by omega)))

#print axioms identity_fp
end CMDG.CondensedCM5R0.BreenDeligneLatticePseudocoherence
