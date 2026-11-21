import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCondensedChainProofs
import Mathlib.Tactic.Abel

/-!
# CMDG CM5 E3: actual categorical degree-one doubling homotopy

This proves the missing low-degree Breen–Deligne doubling identity in the
**genuine condensed abelian category**, not merely ordinary free groups and
not just after applying Hom to real coefficients.

The previously protected F0,F1,F2 low-degree source terms use the same
actual CompHaus.toCondensed and Condensed.freeAb functors. To make the
definitional identity between their categorical objects transparent
to Lean type-class synthesis, this exact PR changes four synonymous
opaque object definitions into reducible abbreviations; this changes
neither their terms nor the maps.

This file proves every finite polynomial-coordinate cancellation and
the real equation h1 ≫ d2 + d1 ≫ h0 = 2 id - [2] as a genuine
CondensedAb morphism identity, for any compact Hausdorff abelian group
including the arbitrary product torus (R/Z)^I.

The **all-degree** Breen–Deligne resolution, full derived-real/circle
comparison, circle integer degree-one Ext and canonical derived solidification
unit still require independent proofs. This statement only settles
the categorical homotopy through degree one.
-/

noncomputable section
universe u
open CategoryTheory
open CategoryTheory.Limits
namespace CMDG.CondensedCM5R0.BreenDeligneCondensed

variable (A : Type u) [TopologicalSpace A] [CompactSpace A]
  [T2Space A] [AddCommGroup A] [ContinuousAdd A]

noncomputable def pairPlus : C(A × A, A) :=
  ⟨fun p => p.1+p.2, continuous_fst.add continuous_snd⟩
noncomputable def pairFst : C(A × A, A) :=
  ⟨fun p => p.1, continuous_fst⟩
noncomputable def pairSnd : C(A × A, A) :=
  ⟨fun p => p.2, continuous_snd⟩
noncomputable def pairDiag : C(A, A × A) :=
  ⟨fun a => (a,a), continuous_id.prodMk continuous_id⟩
noncomputable def pairSwap : C(A × A, A × A) :=
  ⟨fun p => (p.2,p.1), continuous_snd.prodMk continuous_fst⟩
noncomputable def pairDouble : C(A × A, A × A) :=
  ⟨fun p => (p.1+p.1,p.2+p.2),
    (continuous_fst.add continuous_fst).prodMk
      (continuous_snd.add continuous_snd)⟩

theorem poly_bc_q2_eq_diagSnd :
    polyMap ((assocBC A).comp (q2 A)) =
      polyMap ((pairDiag A).comp (pairSnd A)) := by
  congr 1

theorem poly_bc_q3_eq_swapQc :
    polyMap ((assocBC A).comp (q3 A)) =
      polyMap ((pairSwap A).comp (qc A)) := by
  congr 1

theorem poly_abc_q1_eq_double :
    polyMap ((assocAB_C A).comp (q1 A)) =
      polyMap (pairDouble A) := by
  congr 1

theorem poly_abc_q2_eq_qc :
    polyMap ((assocAB_C A).comp (q2 A)) =
      polyMap (qc A) := by
  congr 1

theorem poly_abc_q3_eq_diagPlus :
    polyMap ((assocAB_C A).comp (q3 A)) =
      polyMap ((pairDiag A).comp (pairPlus A)) := by
  congr 1

theorem poly_ab_q1_eq_diagFst :
    polyMap ((assocAB A).comp (q1 A)) =
      polyMap ((pairDiag A).comp (pairFst A)) := by
  congr 1

theorem poly_ab_q2_eq_id :
    polyMap ((assocAB A).comp (q2 A)) = 𝟙 (src1 A) := by
  have h : ((assocAB A).comp (q2 A)) = ContinuousMap.id (A × A) := by
    ext p <;> rfl
  rw [h, polyMap_id]

theorem poly_ab_q3_eq_id :
    polyMap ((assocAB A).comp (q3 A)) = 𝟙 (src1 A) := by
  have h : ((assocAB A).comp (q3 A)) = ContinuousMap.id (A × A) := by
    ext p <;> rfl
  rw [h,polyMap_id]

#print axioms poly_abc_q3_eq_diagPlus
#print axioms poly_ab_q3_eq_id

theorem d1_comp_h0_expanded :
    d1 A ≫ h0 A =
      -polyMap ((pairDiag A).comp (pairPlus A)) +
       polyMap ((pairDiag A).comp (pairFst A)) +
       polyMap ((pairDiag A).comp (pairSnd A)) := by
  dsimp only [src0,src1] at *
  simp only [d1,h0,Preadditive.sub_comp,Preadditive.comp_neg,
    Preadditive.add_comp,polyMap_comp]
  abel

#print axioms d1_comp_h0_expanded

theorem poly_bc_q1_eq_ab_c_q2 :
    polyMap ((assocBC A).comp (q1 A)) =
      polyMap ((assocA_BC A).comp (q2 A)) := by
  congr 1

theorem poly_a_bc_q1_eq_q3 :
    polyMap ((assocA_BC A).comp (q1 A)) =
      polyMap ((assocA_BC A).comp (q3 A)) := by
  congr 1
  ext p
  · rfl
  · change p.1 + (p.2 + p.2) = p.2 + (p.1 + p.2)
    abel

theorem pairDouble_matches_double1 :
    polyMap (pairDouble A) = double1 A := by
  rfl

theorem condensed_homotopy1 :
    h1 A ≫ d2 A + d1 A ≫ h0 A =
      (𝟙 (src1 A)) + (𝟙 (src1 A)) - double1 A := by
  rw [h1_comp_d2_expanded, d1_comp_h0_expanded]
  simp only [d2assoc, d2comm,
    Preadditive.sub_comp, Preadditive.add_comp,
    Preadditive.comp_sub, Preadditive.comp_add,
    Preadditive.comp_neg, Category.comp_id,polyMap_comp]
  rw [poly_bc_q1_eq_ab_c_q2, poly_bc_q2_eq_diagSnd,
    poly_bc_q3_eq_swapQc, poly_abc_q1_eq_double,
    poly_abc_q2_eq_qc, poly_abc_q3_eq_diagPlus,
    poly_a_bc_q1_eq_q3, poly_ab_q1_eq_diagFst,
    poly_ab_q2_eq_id, poly_ab_q3_eq_id,
    pairDouble_matches_double1]
  have hswap :
      polyMap ((pairSwap A).comp (qc A)) =
        polyMap ((⟨fun p : A × A => (p.2,p.1),
          continuous_snd.prodMk continuous_fst⟩ : C(A × A,A × A)).comp (qc A)) :=
          rfl
  rw [hswap]
  abel

#print axioms condensed_homotopy1
/-- Genuine infinite-dimensional circle-torus specialization of the
categorical degree-one Breen–Deligne doubling homotopy. -/
theorem torus_degreeOne_condensed_homotopy
    (I : Type u) :
    h1 (I → UnitAddCircle) ≫ d2 (I → UnitAddCircle) +
      d1 (I → UnitAddCircle) ≫ h0 (I → UnitAddCircle) =
      (𝟙 (src1 (I → UnitAddCircle))) +
      (𝟙 (src1 (I → UnitAddCircle))) -
        double1 (I → UnitAddCircle) :=
  condensed_homotopy1 (I → UnitAddCircle)

#print axioms torus_degreeOne_condensed_homotopy

end CMDG.CondensedCM5R0.BreenDeligneCondensed
