import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneDegreeThreePentagon
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRealPentagon


/-!
# CMDG CM5: correspondence of five categorical and analytic faces

The real cochain five-face maps are literally the polynomial maps used
in the genuine CondensedAb pentagon, applied to the compact coordinates
with the parameter S held fixed. All five equations are proved, not
assumed from the names. Does not establish the all-degree derived sheaf
comparison or canonical solidification-unit equality.
-/
noncomputable section
universe u v
namespace CMDG.CondensedCM5R0

variable (A : Type u) (S : Type v)
variable [TopologicalSpace A] [CompactSpace A] [T2Space A]
  [AddCommGroup A] [ContinuousAdd A]
variable [TopologicalSpace S] [CompactSpace S]

theorem pentagonFace0_real_eq_source (p : (BreenDeligneCondensed.A4 A) × S) :
    BreenDeligneRealCochains.pface0 A S p =
      (BreenDeligneCondensed.face0 A p.1, p.2) := by rfl
theorem pentagonFace1_real_eq_source (p : (BreenDeligneCondensed.A4 A) × S) :
    BreenDeligneRealCochains.pface1 A S p =
      (BreenDeligneCondensed.face1 A p.1, p.2) := by rfl
theorem pentagonFace2_real_eq_source (p : (BreenDeligneCondensed.A4 A) × S) :
    BreenDeligneRealCochains.pface2 A S p =
      (BreenDeligneCondensed.face2 A p.1, p.2) := by rfl
theorem pentagonFace3_real_eq_source (p : (BreenDeligneCondensed.A4 A) × S) :
    BreenDeligneRealCochains.pface3 A S p =
      (BreenDeligneCondensed.face3 A p.1, p.2) := by rfl
theorem pentagonFace4_real_eq_source (p : (BreenDeligneCondensed.A4 A) × S) :
    BreenDeligneRealCochains.pface4 A S p =
      (BreenDeligneCondensed.face4 A p.1, p.2) := by rfl

#print axioms pentagonFace4_real_eq_source
end CMDG.CondensedCM5R0
