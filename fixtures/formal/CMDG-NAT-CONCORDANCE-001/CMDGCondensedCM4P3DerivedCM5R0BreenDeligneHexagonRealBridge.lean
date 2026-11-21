import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneHexagonInvolution
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRealHexagon


/-!
# CMDG CM5: exact face correspondence on real hexagon cochains

For every compact abelian group A and compact parameter S, verify
that all seven compact continuous maps underlying the analytic
hexagon/symmetry/diagonal cochain operators are exactly the genuine
categorical compact-polynomial source maps × identity on S.
No semantic replacement of the condensed source occurs at the
individual face-map level. This does NOT prove a sheaf-derived
internal-Hom comparison or source-resolution exactness.
-/
noncomputable section
universe u v
namespace CMDG.CondensedCM5R0

variable (A : Type u) (S : Type v)
variable [TopologicalSpace A] [CompactSpace A] [T2Space A]
  [AddCommGroup A] [ContinuousAdd A]
variable [TopologicalSpace S] [CompactSpace S]

theorem hexSwapReal_eq_source (p : (A × (A × A)) × S) :
    BreenDeligneRealCochains.pHexSwap A S p =
      (BreenDeligneCondensed.hexSwap A p.1,p.2) := by rfl

theorem hexRotateReal_eq_source (p : (A × (A × A)) × S) :
    BreenDeligneRealCochains.pHexRotate A S p =
      (BreenDeligneCondensed.hexRotate A p.1,p.2) := by rfl

theorem hexPair0Real_eq_source (p : (A × (A × A)) × S) :
    BreenDeligneRealCochains.pHexPair0 A S p =
      (BreenDeligneCondensed.hexPair0 A p.1,p.2) := by rfl

theorem hexPair1Real_eq_source (p : (A × (A × A)) × S) :
    BreenDeligneRealCochains.pHexPair1 A S p =
      (BreenDeligneCondensed.hexPair1 A p.1,p.2) := by rfl

theorem hexPair2Real_eq_source (p : (A × (A × A)) × S) :
    BreenDeligneRealCochains.pHexPair2 A S p =
      (BreenDeligneCondensed.hexPair2 A p.1,p.2) := by rfl

theorem hexSymReal_eq_source (p : (A × A) × S) :
    BreenDeligneRealCochains.pSwap A S p =
      (BreenDeligneCondensed.hexSwapPair A p.1,p.2) := by rfl

theorem hexDiagonalReal_eq_source (p : A × S) :
    BreenDeligneRealCochains.pDiag A S p =
      (BreenDeligneCondensed.diagonalPair A p.1,p.2) := by rfl

#print axioms hexSwapReal_eq_source
#print axioms hexRotateReal_eq_source
#print axioms hexPair0Real_eq_source
#print axioms hexPair1Real_eq_source
#print axioms hexPair2Real_eq_source
#print axioms hexSymReal_eq_source
#print axioms hexDiagonalReal_eq_source
end CMDG.CondensedCM5R0
