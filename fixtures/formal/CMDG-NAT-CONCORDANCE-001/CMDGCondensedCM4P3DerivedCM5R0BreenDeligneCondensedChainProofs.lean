import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCondensed
import Mathlib.Tactic.Abel

/-!
# CMDG CM5: true condensed Breen–Deligne chain identities and first doubling identity

This module builds on the *actual* F0,F1,F2 and maps in
CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCondensed. It proves
the functorial compact-polynomial map, the associativity and
commutativity boundary cancellations, hence d2 ≫ d1 = 0 as an
equation in the genuine CondensedAb category. It also proves
h0 ≫ d1 = 2 id − [2] as an actual CondensedAb morphism identity.

All components are constructed through CompHaus.toCondensed and
Condensed.freeAb, not merely ordinary free-group surrogates.

No assertion of exactness in degree one, an all-degree resolution,
derived Hom into real/circle, the higher-degree doubling homotopy,
or canonical derived biduality follows from these theorems.
-/

noncomputable section

universe u

open CategoryTheory
open CategoryTheory.Limits

namespace CMDG.CondensedCM5R0.BreenDeligneCondensed

variable (A : Type u) [TopologicalSpace A] [CompactSpace A]
  [T2Space A] [AddCommGroup A] [ContinuousAdd A]

theorem polyMap_id {X : Type u}
    [TopologicalSpace X] [CompactSpace X] [T2Space X] :
    (polyMap (X := X) (Y := X) (ContinuousMap.id X)) =
      𝟙 ((Condensed.freeAb).obj ((CompHaus.of X).toCondensed)) := by
  simp [polyMap]

theorem polyMap_comp {X Y Z : Type u}
    [TopologicalSpace X] [CompactSpace X] [T2Space X]
    [TopologicalSpace Y] [CompactSpace Y] [T2Space Y]
    [TopologicalSpace Z] [CompactSpace Z] [T2Space Z]
    (f : C(X,Y)) (g : C(Y,Z)) :
    polyMap f ≫ polyMap g = polyMap (g.comp f) := by
  simp [polyMap, ← Functor.map_comp]

theorem condensed_homotopy0 :
    h0 A ≫ d1 A =
      (𝟙 (src0 A)) + (𝟙 (src0 A)) - double0 A := by
  let diag : C(A, A × A) :=
    ⟨fun a => (a,a), continuous_id.prodMk continuous_id⟩
  let plus : C(A × A, A) :=
    ⟨fun p => p.1+p.2, continuous_fst.add continuous_snd⟩
  let fst : C(A × A, A) := ⟨fun p => p.1, continuous_fst⟩
  let snd : C(A × A, A) := ⟨fun p => p.2, continuous_snd⟩
  let dbl : C(A, A) :=
    ⟨fun a => a+a, continuous_id.add continuous_id⟩
  have ha : polyMap diag ≫ polyMap plus = polyMap dbl := by
    rw [polyMap_comp]
    rfl
  have hb : polyMap diag ≫ polyMap fst = 𝟙 (src0 A) := by
    rw [polyMap_comp]
    have heq : fst.comp diag = ContinuousMap.id A := by
      ext a
      rfl
    rw [heq,polyMap_id]
    rfl
  have hc : polyMap diag ≫ polyMap snd = 𝟙 (src0 A) := by
    rw [polyMap_comp]
    have heq : snd.comp diag = ContinuousMap.id A := by
      ext a
      rfl
    rw [heq,polyMap_id]
    rfl
  change (-polyMap diag) ≫
      (polyMap plus - polyMap fst - polyMap snd) =
      (𝟙 ((Condensed.freeAb).obj ((CompHaus.of A).toCondensed))) +
      (𝟙 ((Condensed.freeAb).obj ((CompHaus.of A).toCondensed))) - polyMap dbl
  simp only [Preadditive.neg_comp,Preadditive.comp_sub]
  rw [ha,hb,hc]
  abel

theorem condensed_commutativity_boundary_zero :
    d2comm A ≫ d1 A = 0 := by
  let swap : C(A × A, A × A) :=
    ⟨fun p => (p.2,p.1), continuous_snd.prodMk continuous_fst⟩
  let plus : C(A × A, A) :=
    ⟨fun p => p.1 + p.2, continuous_fst.add continuous_snd⟩
  let fst : C(A × A, A) :=
    ⟨fun p => p.1, continuous_fst⟩
  let snd : C(A × A, A) :=
    ⟨fun p => p.2, continuous_snd⟩
  have ha : polyMap swap ≫ polyMap plus = polyMap plus := by
    rw [polyMap_comp]
    congr 1
    ext p
    exact add_comm p.2 p.1
  have hb : polyMap swap ≫ polyMap fst = polyMap snd := by
    rw [polyMap_comp]
    rfl
  have hc : polyMap swap ≫ polyMap snd = polyMap fst := by
    rw [polyMap_comp]
    rfl
  change ((𝟙 _) - polyMap swap) ≫
    (polyMap plus - polyMap fst - polyMap snd) = 0
  dsimp only [src1] at *
  simp only [Preadditive.sub_comp, Preadditive.comp_sub,
    Category.id_comp]
  rw [ha,hb,hc]
  abel

theorem condensed_associativity_boundary_zero :
    d2assoc A ≫ d1 A = 0 := by
  let plus : C(A × A, A) :=
    ⟨fun p => p.1 + p.2, continuous_fst.add continuous_snd⟩
  let fst : C(A × A, A) := ⟨fun p => p.1, continuous_fst⟩
  let snd : C(A × A, A) := ⟨fun p => p.2, continuous_snd⟩
  have h1 : polyMap (plus.comp (assocBC A)) =
      polyMap (snd.comp (assocA_BC A)) := by
    congr 1
  have h2 : polyMap (plus.comp (assocAB_C A)) =
      polyMap (plus.comp (assocA_BC A)) := by
    congr 1
    ext p
    exact add_assoc _ _ _
  have h3 : polyMap (plus.comp (assocAB A)) =
      polyMap (fst.comp (assocAB_C A)) := by
    congr 1
  have h4 : polyMap (fst.comp (assocBC A)) =
      polyMap (snd.comp (assocAB A)) := by
    congr 1
  have h5 : polyMap (snd.comp (assocBC A)) =
      polyMap (snd.comp (assocAB_C A)) := by
    congr 1
  have h6 : polyMap (fst.comp (assocA_BC A)) =
      polyMap (fst.comp (assocAB A)) := by
    congr 1
  dsimp only [src0,src1,src2assoc] at *
  simp only [d2assoc,d1,Preadditive.sub_comp,Preadditive.add_comp,
    Preadditive.comp_sub,polyMap_comp]
  rw [h1,h2,h3,h4,h5,h6]
  abel

theorem condensed_d2_comp_d1_zero :
    d2 A ≫ d1 A = 0 := by
  dsimp only [src2,src1,src2assoc] at *
  change biprod.desc (d2assoc A) (d2comm A) ≫ d1 A = 0
  rw [biprod.desc_eq,Preadditive.add_comp]
  simp only [Category.assoc,condensed_associativity_boundary_zero,
    condensed_commutativity_boundary_zero, comp_zero, add_zero]


#print axioms condensed_d2_comp_d1_zero

#print axioms condensed_associativity_boundary_zero

#print axioms condensed_commutativity_boundary_zero

#print axioms condensed_homotopy0

#print axioms polyMap_comp


end CMDG.CondensedCM5R0.BreenDeligneCondensed
