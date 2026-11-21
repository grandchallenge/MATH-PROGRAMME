import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneH2Actual
import Mathlib.Tactic.Abel


/-!
# CM5: the four degree-three real cochain relations commute with doubling

The actual degree-two doubling endomorphism on Banach cochains
commutes with each genuine candidate degree-three differential:
pentagon, hexagon, symmetry, diagonal. For a compact A and S,
each right-hand map is the actual finite-coordinate doubling
pullback on C(A^r×S,ℝ).

This supplies the invariant-closed-subspace input for the degree-two
Neumann argument; it does NOT independently imply exactness.
-/
noncomputable section
universe u v

namespace CMDG.CondensedCM5R0.BreenDeligneRealCochains

variable (A : Type u) (S : Type v)
variable [TopologicalSpace A] [CompactSpace A]
    [AddCommGroup A] [ContinuousAdd A]
variable [TopologicalSpace S] [CompactSpace S]

theorem pentagonReal_commutes_doubling (f : C2 A S) :
    pentagonCochainDifferential A S ((doubleStar2 A S f).1) =
      doubleStar3 A S (pentagonCochainDifferential A S f.1) := by
  simpa [doubleStar2,doubleStar2Assoc] using
    pentagon_differential_commutes_doubling A S f.1

theorem hexagonReal_commutes_doubling (f : C2 A S) :
    hexRealDifferential A S (doubleStar2 A S f) =
      (hexRealDifferential A S f).comp (pDouble2a A S) := by
  ext p
  simp [hexRealDifferential,hexAssocStar,hexCommStar,
    doubleStar2,doubleStar1,pDouble2a,pDouble1,
    pHexSwap,pHexRotate,pHexPair0,pHexPair1,pHexPair2,add_assoc]
  abel

theorem symmetryReal_commutes_doubling (f : C2 A S) :
    symRealDifferential A S (doubleStar2 A S f) =
      (symRealDifferential A S f).comp (pDouble1 A S) := by
  ext p
  simp [symRealDifferential,doubleStar2,doubleStar1,
    pDouble1,pDouble2a,pSwap,add_assoc]

theorem diagonalReal_commutes_doubling (f : C2 A S) :
    diagonalRealDifferential A S (doubleStar2 A S f) =
      (diagonalRealDifferential A S f).comp (pDouble0 A S) := by
  ext p
  simp [diagonalRealDifferential,doubleStar2,doubleStar1,
    pDouble1,pDouble0,pDiag,add_assoc]

#print axioms pentagonReal_commutes_doubling
#print axioms hexagonReal_commutes_doubling
#print axioms symmetryReal_commutes_doubling
#print axioms diagonalReal_commutes_doubling

end CMDG.CondensedCM5R0.BreenDeligneRealCochains
