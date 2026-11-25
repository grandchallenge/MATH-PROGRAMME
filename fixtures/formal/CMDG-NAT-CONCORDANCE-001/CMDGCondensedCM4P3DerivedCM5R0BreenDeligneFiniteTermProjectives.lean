import CMDGCondensedCM4P3DerivedCM5R0EilenbergMacLaneModel
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneLatticeProjectives

/-! Actual finite-rank projective terms of the reduced Eilenberg–MacLane
complex, restricted to the established finite-free lattice skeleton.
This proves finite-type terms, not exactness of a Breen–Deligne resolution. -/
noncomputable section
open CategoryTheory
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneLatticeProjectives

namespace CMDG.CondensedCM5R0.BreenDeligneFiniteTermProjectives

def latticeChainDegree (n m : ℕ) : Latt ⥤ AddCommGrpCat.{0} :=
  valueFunctor ⋙ reducedChainDegree n m

/-- Each term is a retract of a single actual finite-rank free representable. -/
def latticeTermRetract (n m : ℕ) :
    Retract (latticeChainDegree n m) (polynomial (activeRank n m)) :=
  restrictedChainRetract valueFunctor (fullyFaithfulInducedFunctor lattice)
    (activeRank n m) n m (Iso.refl _)

instance latticeTermProjective (n m : ℕ) : Projective (latticeChainDegree n m) :=
  (latticeTermRetract n m).projective

#print axioms latticeTermRetract
#print axioms latticeTermProjective
end CMDG.CondensedCM5R0.BreenDeligneFiniteTermProjectives
