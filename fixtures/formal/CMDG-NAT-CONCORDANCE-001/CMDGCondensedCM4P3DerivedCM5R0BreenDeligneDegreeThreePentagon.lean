import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCondensedChainProofs
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Abel


/-!
# CMDG CM5: genuine degree-three pentagon syzygy in CondensedAb

Construct a five-face compact-Hausdorff polynomial boundary from the
actual free condensed abelian object on A⁴ to the genuine free
associativity-relation object on A³. Verify its composite with the
protected association boundary is zero, including for an arbitrary
circle product A=(ℝ/ℤ)^I.

This is one explicit degree-three *syzygy*, not a complete F₃, not
exactness or a constructed all-degree Breen–Deligne resolution.
-/
noncomputable section
universe u
open CategoryTheory
open CategoryTheory.Limits
namespace CMDG.CondensedCM5R0.BreenDeligneCondensed

variable (A : Type u) [TopologicalSpace A] [CompactSpace A]
  [T2Space A] [AddCommGroup A] [ContinuousAdd A]

abbrev A4 := A × (A × (A × A))
noncomputable abbrev pentagonSource : CondensedAb.{u} :=
  (Condensed.freeAb).obj ((CompHaus.of (A4 A)).toCondensed)

noncomputable def face0 : C(A4 A, A × (A × A)) :=
  ⟨fun p => (p.2.1, (p.2.2.1, p.2.2.2)), by fun_prop⟩
noncomputable def face1 : C(A4 A, A × (A × A)) :=
  ⟨fun p => (p.1 + p.2.1, (p.2.2.1, p.2.2.2)), by fun_prop⟩
noncomputable def face2 : C(A4 A, A × (A × A)) :=
  ⟨fun p => (p.1, (p.2.1 + p.2.2.1, p.2.2.2)), by fun_prop⟩
noncomputable def face3 : C(A4 A, A × (A × A)) :=
  ⟨fun p => (p.1, (p.2.1, p.2.2.1 + p.2.2.2)), by fun_prop⟩
noncomputable def face4 : C(A4 A, A × (A × A)) :=
  ⟨fun p => (p.1, (p.2.1, p.2.2.1)), by fun_prop⟩

noncomputable def pentagonBoundary : pentagonSource A ⟶ src2assoc A :=
  polyMap (face0 A) - polyMap (face1 A) + polyMap (face2 A) -
    polyMap (face3 A) + polyMap (face4 A)

theorem pentagon_comp_d2assoc_zero :
    pentagonBoundary A ≫ d2assoc A = 0 := by
  have h0 :
      polyMap ((assocBC A).comp (face0 A)) =
      polyMap ((assocBC A).comp (face1 A)) := by
    congr 1
  have h1 :
      polyMap ((assocAB_C A).comp (face0 A)) =
      polyMap ((assocBC A).comp (face2 A)) := by
    congr 1
  have h2 :
      polyMap ((assocA_BC A).comp (face0 A)) =
      polyMap ((assocBC A).comp (face3 A)) := by
    congr 1
  have h3 :
      polyMap ((assocAB A).comp (face0 A)) =
      polyMap ((assocBC A).comp (face4 A)) := by
    congr 1
  have h4 :
      polyMap ((assocAB_C A).comp (face1 A)) =
      polyMap ((assocAB_C A).comp (face2 A)) := by
    congr 1
    ext p
    · exact add_assoc _ _ _
    · rfl
  have h5 :
      polyMap ((assocA_BC A).comp (face1 A)) =
      polyMap ((assocAB_C A).comp (face3 A)) := by
    congr 1
  have h6 :
      polyMap ((assocAB A).comp (face1 A)) =
      polyMap ((assocAB_C A).comp (face4 A)) := by
    congr 1
  have h7 :
      polyMap ((assocA_BC A).comp (face2 A)) =
      polyMap ((assocA_BC A).comp (face3 A)) := by
    congr 1
    ext p
    · rfl
    · exact add_assoc _ _ _
  have h8 :
      polyMap ((assocAB A).comp (face2 A)) =
      polyMap ((assocA_BC A).comp (face4 A)) := by
    congr 1
  have h9 :
      polyMap ((assocAB A).comp (face3 A)) =
      polyMap ((assocAB A).comp (face4 A)) := by
    congr 1
  change
      (polyMap (face0 A) - polyMap (face1 A) +
        polyMap (face2 A) - polyMap (face3 A) +
        polyMap (face4 A)) ≫
      (polyMap (assocBC A) - polyMap (assocAB_C A) +
        polyMap (assocA_BC A) - polyMap (assocAB A)) = 0
  simp only [Preadditive.add_comp, Preadditive.sub_comp,
    Preadditive.comp_add, Preadditive.comp_sub, polyMap_comp]
  rw [h0,h1,h2,h3,h4,h5,h6,h7,h8,h9]
  abel

#print axioms pentagon_comp_d2assoc_zero
/-- A genuine degree-three pentagon syzygy of the arbitrary circle product. -/
theorem circleTorus_pentagon_comp_d2assoc_zero
    (I : Type u) :
    pentagonBoundary (I → UnitAddCircle) ≫
      d2assoc (I → UnitAddCircle) = 0 :=
  pentagon_comp_d2assoc_zero (I → UnitAddCircle)

#print axioms circleTorus_pentagon_comp_d2assoc_zero

end CMDG.CondensedCM5R0.BreenDeligneCondensed
