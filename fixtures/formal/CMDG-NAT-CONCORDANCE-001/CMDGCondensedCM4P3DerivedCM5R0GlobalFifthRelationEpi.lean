import CMDGCondensedCM4P3DerivedCM5R0TrueProbeDegreeFourExact
import CMDGCondensedCM4P3DerivedCM5R0GlobalFourthRelationEpi
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat

/-!
# CMDG CM5 degree five — global sixth-to-fifth Čech relation

This file transports the proved actual sixfold/fivefold Profinite
Čech differential through sheafification. All face maps and signs
are the actual categorical maps. No global epi or Ext5 vanishing
is assumed as input.
-/

noncomputable section
universe u
open CategoryTheory Limits CategoryTheory.Functor
namespace CMDG.CondensedCM5R0

/-- Genuine sixth differential on categorical (not surrogate)
iterated Čech Profinite objects. The middle fifth explicit object
is identified with its actual categorical pullback via the proved
Profinite isomorphism. -/
noncomputable def stoneanCechCategoricalSixthBoundary
    (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechSextuples T) ⟶
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuintuples T) :=
  (Condensed.profiniteFree Coeff).map
      (stoneanCechCategoricalSextupleToExplicit T) ≫
    stoneanCechSixthBoundary T ≫
      (Condensed.profiniteFree Coeff).map
        (stoneanCechExplicitQuintupleToAbstract T)

theorem stoneanCechCategoricalSixthBoundary_comp_fifth_zero
    (T : Profinite.{u}) :
    stoneanCechCategoricalSixthBoundary T ≫
      stoneanCechCategoricalFifthBoundary T = 0 := by
  unfold stoneanCechCategoricalSixthBoundary
    stoneanCechCategoricalFifthBoundary
  have hIso :
      (Condensed.profiniteFree Coeff).map
        (stoneanCechExplicitQuintupleToAbstract T) ≫
      (Condensed.profiniteFree Coeff).map
        (stoneanCechCategoricalQuintupleToExplicit T) = 𝟙 _ := by
    rw [← Functor.map_comp, stoneanCechExplicitQuintuple_roundtrip T,
      (Condensed.profiniteFree Coeff).map_id]
  simp only [Category.assoc]
  rw [← Category.assoc
     ((Condensed.profiniteFree Coeff).map
       (stoneanCechExplicitQuintupleToAbstract T))
     ((Condensed.profiniteFree Coeff).map
       (stoneanCechCategoricalQuintupleToExplicit T))
     (stoneanCechFifthBoundary T)]
  rw [hIso]
  simp only [Category.id_comp, Category.assoc]
  rw [stoneanCechSixthBoundary_comp_fifthBoundary_zero, comp_zero]

/-- Type-locked sixth last projection with the true categorical
sixfold source, avoiding implicit pullback normalization mismatch. -/
noncomputable def stoneanCechCategoricalSixthLastFace (T : Profinite.{u}) :
    stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuintuples T :=
  pullback.fst
    (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)

/-- The actual presheaf signed six-face morphism. -/
noncomputable def presheafStoneanCechSixthBoundary (T : Profinite.{u}) :
    freeCompHausModulePresheaf (stoneanPresentationCechSextuples T) ⟶
      freeCompHausModulePresheaf (stoneanPresentationCechQuintuples T) :=
  freeCompHausModulePresheafFunctor.map
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace0 T ≫ stoneanCechExplicitQuintupleToAbstract T) -
  freeCompHausModulePresheafFunctor.map
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace1 T ≫ stoneanCechExplicitQuintupleToAbstract T) +
  freeCompHausModulePresheafFunctor.map
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace2 T ≫ stoneanCechExplicitQuintupleToAbstract T) -
  freeCompHausModulePresheafFunctor.map
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace3 T ≫ stoneanCechExplicitQuintupleToAbstract T) +
  freeCompHausModulePresheafFunctor.map
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace4 T ≫ stoneanCechExplicitQuintupleToAbstract T) -
  freeCompHausModulePresheafFunctor.map
    (stoneanCechCategoricalSixthLastFace T)

theorem presheafStoneanCechSixthBoundary_sheafify
    (T : Profinite.{u}) :
    moduleSheafification.map (presheafStoneanCechSixthBoundary T) =
      stoneanCechCategoricalSixthBoundary T := by
  unfold presheafStoneanCechSixthBoundary
    stoneanCechCategoricalSixthBoundary stoneanCechSixthBoundary
  change _ = _
  rw [show stoneanCechCategoricalSixthLastFace T =
      stoneanCechCategoricalSextupleToExplicit T ≫
        sextupleFace5 T ≫ stoneanCechExplicitQuintupleToAbstract T from
        (stoneanCechCategoricalSextuple_face5_eq_first T).symm]
  rw [Functor.map_sub, Functor.map_add, Functor.map_sub,
    Functor.map_add, Functor.map_sub]
  simp only [Functor.map_comp, Preadditive.comp_add,
    Preadditive.comp_sub, Preadditive.add_comp,
    Preadditive.sub_comp, Category.assoc]
  rfl

private theorem sextupleQuintuple_cancel_iso_global
    (T : Profinite.{u}) {X : Profinite.{u}}
    (f : X ⟶ stoneanCechExplicitQuintupleProfinite T)
    (g : stoneanCechExplicitQuintupleProfinite T ⟶
      stoneanPresentationCechQuadruples T) :
    (f ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫ g) = f ≫ g := by
  rw [Category.assoc f (stoneanCechExplicitQuintupleToAbstract T)
    (stoneanCechCategoricalQuintupleToExplicit T ≫ g)]
  rw [← Category.assoc
    (stoneanCechExplicitQuintupleToAbstract T)
    (stoneanCechCategoricalQuintupleToExplicit T) g]
  rw [stoneanCechExplicitQuintuple_roundtrip T]
  exact congrArg (fun m : stoneanCechExplicitQuintupleProfinite T ⟶
    stoneanPresentationCechQuadruples T => f ≫ m) (Category.id_comp g)

/-- Genuine categorical sixth/fifth face identity (0,1). -/
theorem stoneanCechCategoricalSixthFace01_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace0 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace0 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace1 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace0 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace0 T
  let f1 := B ≫ sextupleFace1 T
  let d0 := stoneanCechFifthFace0 T
  let d1 := stoneanCechFifthFace0 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace01 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (0,2). -/
theorem stoneanCechCategoricalSixthFace02_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace0 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace1 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace2 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace0 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace0 T
  let f1 := B ≫ sextupleFace2 T
  let d0 := stoneanCechFifthFace1 T
  let d1 := stoneanCechFifthFace0 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace02 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (0,3). -/
theorem stoneanCechCategoricalSixthFace03_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace0 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace2 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace3 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace0 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace0 T
  let f1 := B ≫ sextupleFace3 T
  let d0 := stoneanCechFifthFace2 T
  let d1 := stoneanCechFifthFace0 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace03 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (0,4). -/
theorem stoneanCechCategoricalSixthFace04_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace0 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace3 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace4 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace0 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace0 T
  let f1 := B ≫ sextupleFace4 T
  let d0 := stoneanCechFifthFace3 T
  let d1 := stoneanCechFifthFace0 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace04 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (0,5). -/
theorem stoneanCechCategoricalSixthFace05_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace0 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace5 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace0 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace0 T
  let f1 := B ≫ sextupleFace5 T
  let d0 := stoneanCechFifthFace4 T
  let d1 := stoneanCechFifthFace0 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace05 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (1,2). -/
theorem stoneanCechCategoricalSixthFace12_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace1 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace1 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace2 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace1 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace1 T
  let f1 := B ≫ sextupleFace2 T
  let d0 := stoneanCechFifthFace1 T
  let d1 := stoneanCechFifthFace1 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace12 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (1,3). -/
theorem stoneanCechCategoricalSixthFace13_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace1 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace2 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace3 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace1 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace1 T
  let f1 := B ≫ sextupleFace3 T
  let d0 := stoneanCechFifthFace2 T
  let d1 := stoneanCechFifthFace1 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace13 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (1,4). -/
theorem stoneanCechCategoricalSixthFace14_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace1 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace3 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace4 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace1 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace1 T
  let f1 := B ≫ sextupleFace4 T
  let d0 := stoneanCechFifthFace3 T
  let d1 := stoneanCechFifthFace1 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace14 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (1,5). -/
theorem stoneanCechCategoricalSixthFace15_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace1 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace5 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace1 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace1 T
  let f1 := B ≫ sextupleFace5 T
  let d0 := stoneanCechFifthFace4 T
  let d1 := stoneanCechFifthFace1 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace15 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (2,3). -/
theorem stoneanCechCategoricalSixthFace23_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace2 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace2 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace3 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace2 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace2 T
  let f1 := B ≫ sextupleFace3 T
  let d0 := stoneanCechFifthFace2 T
  let d1 := stoneanCechFifthFace2 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace23 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (2,4). -/
theorem stoneanCechCategoricalSixthFace24_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace2 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace3 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace4 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace2 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace2 T
  let f1 := B ≫ sextupleFace4 T
  let d0 := stoneanCechFifthFace3 T
  let d1 := stoneanCechFifthFace2 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace24 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (2,5). -/
theorem stoneanCechCategoricalSixthFace25_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace2 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace5 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace2 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace2 T
  let f1 := B ≫ sextupleFace5 T
  let d0 := stoneanCechFifthFace4 T
  let d1 := stoneanCechFifthFace2 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace25 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (3,4). -/
theorem stoneanCechCategoricalSixthFace34_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace3 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace3 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace4 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace3 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace3 T
  let f1 := B ≫ sextupleFace4 T
  let d0 := stoneanCechFifthFace3 T
  let d1 := stoneanCechFifthFace3 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace34 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (3,5). -/
theorem stoneanCechCategoricalSixthFace35_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace3 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace5 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace3 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace3 T
  let f1 := B ≫ sextupleFace5 T
  let d0 := stoneanCechFifthFace4 T
  let d1 := stoneanCechFifthFace3 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace35 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Genuine categorical sixth/fifth face identity (4,5). -/
theorem stoneanCechCategoricalSixthFace45_commute
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace4 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace5 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) := by
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := B ≫ sextupleFace4 T
  let f1 := B ≫ sextupleFace5 T
  let d0 := stoneanCechFifthFace4 T
  let d1 := stoneanCechFifthFace4 T
  change (f0 ≫ A5) ≫ (B5 ≫ d0) =
    (f1 ≫ A5) ≫ (B5 ≫ d1)
  calc
    _ = f0 ≫ d0 := sextupleQuintuple_cancel_iso_global T f0 d0
    _ = f1 ≫ d1 := by
      have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace45 T)
      simpa only [f0, f1, d0, d1, Category.assoc] using h
    _ = _ := (sextupleQuintuple_cancel_iso_global T f1 d1).symm

/-- Actual presheaf sixth/fifth degree-four chain identity. -/
theorem presheafStoneanCechSixthBoundary_comp_fifth_zero
    (T : Profinite.{u}) :
    presheafStoneanCechSixthBoundary T ≫
      presheafStoneanCechFifthBoundary T = 0 := by
  unfold presheafStoneanCechSixthBoundary
    presheafStoneanCechFifthBoundary
  change _ = _
  rw [show stoneanCechCategoricalSixthLastFace T =
      stoneanCechCategoricalSextupleToExplicit T ≫
        sextupleFace5 T ≫ stoneanCechExplicitQuintupleToAbstract T from
        (stoneanCechCategoricalSextuple_face5_eq_first T).symm]
  simp only [Preadditive.add_comp, Preadditive.sub_comp,
    Preadditive.comp_add, Preadditive.comp_sub,
    ← Functor.map_comp]
  have h01 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace01_commute T)
  have h02 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace02_commute T)
  have h03 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace03_commute T)
  have h04 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace04_commute T)
  have h05 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace05_commute T)
  have h12 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace12_commute T)
  have h13 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace13_commute T)
  have h14 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace14_commute T)
  have h15 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace15_commute T)
  have h23 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace23_commute T)
  have h24 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace24_commute T)
  have h25 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace25_commute T)
  have h34 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace34_commute T)
  have h35 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace35_commute T)
  have h45 := congrArg
    (fun m : stoneanPresentationCechSextuples T ⟶
      stoneanPresentationCechQuadruples T =>
        freeCompHausModulePresheafFunctor.map m)
    (stoneanCechCategoricalSixthFace45_commute T)
  simp only [Category.assoc] at *
  rw [h01, h02, h03, h04, h05, h12, h13, h14, h15, h23, h24, h25, h34, h35, h45]
  simp only [sub_eq_add_neg]
  abel


noncomputable def presheafStoneanCechDegreeFourComplex (T : Profinite.{u}) :
    ShortComplex (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  ShortComplex.mk (presheafStoneanCechSixthBoundary T)
    (presheafStoneanCechFifthBoundary T)
    (presheafStoneanCechSixthBoundary_comp_fifth_zero T)

noncomputable abbrev stoneanRestrictedCechDegreeFourComplex
    (T : Profinite.{u}) :
    ShortComplex (Stonean.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} Coeff) :=
  (presheafStoneanCechDegreeFourComplex T).map
    stoneanPresheafRestriction

theorem stoneanRestrictedCechDegreeFour_exact
    (T : Profinite.{u}) :
    (stoneanRestrictedCechDegreeFourComplex T).Exact := by
  apply functorShortComplex_exact_of_pointwise
  intro U
  change (trueProbeDegreeFourComplex T U.unop).Exact
  exact trueProbeDegreeFour_exact T U.unop

#print axioms stoneanRestrictedCechDegreeFour_exact


noncomputable def stoneanCechDegreeFourComplex
    (T : Profinite.{u}) : ShortComplex Ambient :=
  ShortComplex.mk (stoneanCechCategoricalSixthBoundary T)
    (stoneanCechCategoricalFifthBoundary T)
    (stoneanCechCategoricalSixthBoundary_comp_fifth_zero T)

theorem stoneanCechDegreeFour_exact_unconditional
    (T : Profinite.{u}) :
    (stoneanCechDegreeFourComplex T).Exact := by
  let S := presheafStoneanCechDegreeFourComplex T
  let R := stoneanPresheafRestriction
  let A := stoneanModuleSheafification
  let E := (Condensed.StoneanCompHaus.equivalence
    (ModuleCat Coeff)).inverse
  haveI : PreservesFiniteLimits A := by
    change PreservesFiniteLimits
      (presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff))
    infer_instance
  haveI : PreservesFiniteColimits A := by
    change PreservesFiniteColimits
      (presheafToSheaf (coherentTopology Stonean) (ModuleCat Coeff))
    infer_instance
  have hStonean : ((S.map R).map A).Exact :=
    (stoneanRestrictedCechDegreeFour_exact T).map A
  have hStonean' : (S.map (R ⋙ A)).Exact := by
    simpa only [ShortComplex.map_comp] using hStonean
  have hTransport :
      (S.map (moduleSheafification ⋙ E)).Exact :=
    ShortComplex.exact_of_iso
      (S.mapNatIso stoneanCompHausSheafificationCompatibility)
      hStonean'
  have hTransport' : ((S.map moduleSheafification).map E).Exact := by
    simpa only [ShortComplex.map_comp] using hTransport
  have hComp : (S.map moduleSheafification).Exact :=
    E.reflects_exact_of_faithful _ hTransport'
  have hZero :
      kernel.ι ((S.map moduleSheafification).g) ≫
      cokernel.π ((S.map moduleSheafification).f) = 0 :=
    ((S.map moduleSheafification).exact_iff_kernel_ι_comp_cokernel_π_zero).1
      hComp
  have hZero' :
      kernel.ι (stoneanCechCategoricalFifthBoundary T) ≫
      cokernel.π (stoneanCechCategoricalSixthBoundary T) = 0 := by
    rw [← presheafStoneanCechFifthBoundary_sheafify T,
      ← presheafStoneanCechSixthBoundary_sheafify T]
    exact hZero
  exact ((stoneanCechDegreeFourComplex T).exact_iff_kernel_ι_comp_cokernel_π_zero).2 hZero'

#print axioms stoneanCechDegreeFour_exact_unconditional


/-- The actual fifth Čech boundary maps into the actual fourth
relation by the protected categorical fifth-to-fourth epi. -/
noncomputable def stoneanCechCategoricalFifthToFourthRelation
    (T : Profinite.{u}) :
    (Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuintuples T) ⟶
    stoneanCechFourthRelationKernel T :=
  (Condensed.profiniteFree Coeff).map
    (stoneanCechCategoricalQuintupleToExplicit T) ≫
      stoneanCechFifthToFourthRelation T

theorem stoneanCechCategoricalFifthToFourthRelation_comp_inclusion
    (T : Profinite.{u}) :
    stoneanCechCategoricalFifthToFourthRelation T ≫
      kernel.ι (stoneanCechFourthToThirdRelation T) =
    stoneanCechCategoricalFifthBoundary T := by
  simp only [stoneanCechCategoricalFifthToFourthRelation,
    stoneanCechCategoricalFifthBoundary, Category.assoc]
  rw [stoneanCechFifthToFourthRelation_comp_inclusion]

theorem stoneanCechCategoricalSixthBoundary_comp_fourthRelation_zero
    (T : Profinite.{u}) :
    stoneanCechCategoricalSixthBoundary T ≫
      stoneanCechCategoricalFifthToFourthRelation T = 0 := by
  apply (cancel_mono
    (kernel.ι (stoneanCechFourthToThirdRelation T))).1
  rw [Category.assoc,
    stoneanCechCategoricalFifthToFourthRelation_comp_inclusion,
    zero_comp]
  exact stoneanCechCategoricalSixthBoundary_comp_fifth_zero T

noncomputable def stoneanCechDegreeFourKernelComplex
    (T : Profinite.{u}) : ShortComplex Ambient :=
  ShortComplex.mk
    (stoneanCechCategoricalSixthBoundary T)
    (stoneanCechCategoricalFifthToFourthRelation T)
    (stoneanCechCategoricalSixthBoundary_comp_fourthRelation_zero T)

noncomputable def stoneanCechDegreeFourKernelComparison
    (T : Profinite.{u}) :
    stoneanCechDegreeFourKernelComplex T ⟶
      stoneanCechDegreeFourComplex T :=
  ShortComplex.homMk
    (𝟙 _) (𝟙 _) (kernel.ι (stoneanCechFourthToThirdRelation T))
    (by dsimp [stoneanCechDegreeFourKernelComplex,
      stoneanCechDegreeFourComplex]; simp)
    (by dsimp [stoneanCechDegreeFourKernelComplex,
      stoneanCechDegreeFourComplex]
        simpa only [Category.id_comp] using
          (stoneanCechCategoricalFifthToFourthRelation_comp_inclusion T).symm)

theorem stoneanCechCategoricalSixthToFifthRelation_epi
    (T : Profinite.{u}) :
    Epi (kernel.lift (stoneanCechCategoricalFifthToFourthRelation T)
      (stoneanCechCategoricalSixthBoundary T)
      (stoneanCechCategoricalSixthBoundary_comp_fourthRelation_zero T)) := by
  haveI : Epi (stoneanCechDegreeFourKernelComparison T).τ₁ := by
    change Epi (𝟙 ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechSextuples T)))
    infer_instance
  haveI : IsIso (stoneanCechDegreeFourKernelComparison T).τ₂ := by
    change IsIso (𝟙 ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechQuintuples T)))
    infer_instance
  haveI : Mono (stoneanCechDegreeFourKernelComparison T).τ₃ := by
    change Mono (kernel.ι (stoneanCechFourthToThirdRelation T))
    infer_instance
  have hk : (stoneanCechDegreeFourKernelComplex T).Exact :=
    (ShortComplex.exact_iff_of_epi_of_isIso_of_mono
      (stoneanCechDegreeFourKernelComparison T)).mpr
        (stoneanCechDegreeFour_exact_unconditional T)
  exact ((stoneanCechDegreeFourKernelComplex T).exact_iff_epi_kernel_lift).mp hk

#print axioms stoneanCechCategoricalSixthToFifthRelation_epi

/-- The actual *explicit* sixth/fifth relation kernel complex. -/
noncomputable def stoneanCechDegreeFourExplicitKernelComplex
    (T : Profinite.{u}) : ShortComplex Ambient :=
  ShortComplex.mk
    (stoneanCechSixthBoundary T)
    (stoneanCechFifthToFourthRelation T)
    (stoneanCechSixthBoundary_comp_fourthRelation_zero T)

/-- The exact categorical and explicit sixfold/fivefold kernel complexes
are isomorphic, by both verified Profinite categorical isomorphisms. -/
noncomputable def stoneanCechDegreeFourExplicitKernelIso
    (T : Profinite.{u}) :
    stoneanCechDegreeFourKernelComplex T ≅
      stoneanCechDegreeFourExplicitKernelComplex T := by
  let B6 := (Condensed.profiniteFree Coeff).mapIso
    (stoneanCechExplicitSextupleIso T).symm
  let B5 := (Condensed.profiniteFree Coeff).mapIso
    (stoneanCechExplicitQuintupleIso T).symm
  refine ShortComplex.isoMk B6 B5 (Iso.refl _) ?_ ?_
  · change (Condensed.profiniteFree Coeff).map
        (stoneanCechCategoricalSextupleToExplicit T) ≫
        stoneanCechSixthBoundary T =
      stoneanCechCategoricalSixthBoundary T ≫
        (Condensed.profiniteFree Coeff).map
          (stoneanCechCategoricalQuintupleToExplicit T)
    unfold stoneanCechCategoricalSixthBoundary
    simp only [Category.assoc]
    have hIso :
        (Condensed.profiniteFree Coeff).map
          (stoneanCechExplicitQuintupleToAbstract T) ≫
        (Condensed.profiniteFree Coeff).map
          (stoneanCechCategoricalQuintupleToExplicit T) = 𝟙 _ := by
      rw [← Functor.map_comp, stoneanCechExplicitQuintuple_roundtrip T,
        (Condensed.profiniteFree Coeff).map_id]
    rw [hIso, Category.comp_id]
  · change (Condensed.profiniteFree Coeff).map
      (stoneanCechCategoricalQuintupleToExplicit T) ≫
      stoneanCechFifthToFourthRelation T =
      stoneanCechCategoricalFifthToFourthRelation T ≫ 𝟙 _
    unfold stoneanCechCategoricalFifthToFourthRelation
    simp only [Category.comp_id]


theorem stoneanCechSixthToFifthRelation_epi_unconditional
    (T : Profinite.{u}) :
    Epi (stoneanCechSixthToFifthRelation T) := by
  have hk : (stoneanCechDegreeFourKernelComplex T).Exact := by
    haveI : Epi (stoneanCechDegreeFourKernelComparison T).τ₁ := by
      change Epi (𝟙 ((Condensed.profiniteFree Coeff).obj
        (stoneanPresentationCechSextuples T)))
      infer_instance
    haveI : IsIso (stoneanCechDegreeFourKernelComparison T).τ₂ := by
      change IsIso (𝟙 ((Condensed.profiniteFree Coeff).obj
        (stoneanPresentationCechQuintuples T)))
      infer_instance
    haveI : Mono (stoneanCechDegreeFourKernelComparison T).τ₃ := by
      change Mono (kernel.ι (stoneanCechFourthToThirdRelation T))
      infer_instance
    exact (ShortComplex.exact_iff_of_epi_of_isIso_of_mono
      (stoneanCechDegreeFourKernelComparison T)).mpr
        (stoneanCechDegreeFour_exact_unconditional T)
  have he : (stoneanCechDegreeFourExplicitKernelComplex T).Exact :=
    ShortComplex.exact_of_iso
      (stoneanCechDegreeFourExplicitKernelIso T) hk
  exact ((stoneanCechDegreeFourExplicitKernelComplex T).exact_iff_epi_kernel_lift).mp
    he

#print axioms stoneanCechSixthToFifthRelation_epi_unconditional
#print axioms stoneanCechCategoricalSixthBoundary_comp_fifth_zero
#print axioms presheafStoneanCechSixthBoundary_sheafify
end CMDG.CondensedCM5R0
