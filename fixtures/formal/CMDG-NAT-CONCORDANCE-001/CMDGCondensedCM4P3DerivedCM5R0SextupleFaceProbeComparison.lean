import CMDGCondensedCM4P3DerivedCM5R0SextupleRepresentedProbe

/-! The genuine represented sixth-to-fifth last-face square. -/
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Deleting the sixth vertex on the true represented categorical
sixfold Profinite pullback agrees exactly with deleting the sixth
vertex of the split-set sixfold represented probe. -/
theorem stoneanCompHausProbeCechSextupleUlift_face5
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechSextuples T))) :
    splitFreeCechSextFace5 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechSextupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuintupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (pullback.fst
          (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
          (Profinite.presentation.π T)))) := by
  rfl

#print axioms stoneanCompHausProbeCechSextupleUlift_face5


/-- The last face of the actual categorical sixth Čech pullback
is its first projection, checked through the categorical isomorphism. -/
theorem stoneanCechCategoricalSextuple_face5_eq_first
    (T : Profinite.{u}) :
    stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace5 T ≫ stoneanCechExplicitQuintupleToAbstract T =
    pullback.fst
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) := by
  have h := stoneanCechExplicitSextupleToAbstract_first T
  have he := congrArg
    (fun m : stoneanCechExplicitSextupleProfinite T ⟶
      stoneanPresentationCechQuintuples T =>
      stoneanCechCategoricalSextupleToExplicit T ≫ m) h
  have hh :
      stoneanCechCategoricalSextupleToExplicit T ≫
      (stoneanCechExplicitSextupleToAbstract T ≫
        pullback.fst
          (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
          (Profinite.presentation.π T)) =
        pullback.fst
          (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
          (Profinite.presentation.π T) := by
    rw [← (Category.assoc
      (stoneanCechCategoricalSextupleToExplicit T)
      (stoneanCechExplicitSextupleToAbstract T)
      (pullback.fst
        (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
        (Profinite.presentation.π T))),
      stoneanCechCategoricalSextuple_roundtrip T]
    exact Category.id_comp _
  rw [hh] at he
  simpa only [Category.assoc] using he.symm

#print axioms stoneanCechCategoricalSextuple_face5_eq_first


private theorem sextupleQuintuple_cancel_iso
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

/-- First-pair categorical sixth-to-fifth face square, genuinely on
the iterated Profinite pullbacks. -/
theorem stoneanCechCategoricalSextuple_face05_commute
    (T : Profinite.{u}) :
    (pullback.fst
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace0 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace0 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) := by
  rw [← stoneanCechCategoricalSextuple_face5_eq_first T]
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := sextupleFace0 T
  let f5 := sextupleFace5 T
  let d0 := stoneanCechFifthFace0 T
  let d4 := stoneanCechFifthFace4 T
  change (B ≫ f5 ≫ A5) ≫ (B5 ≫ d0) =
    (B ≫ f0 ≫ A5) ≫ (B5 ≫ d4)
  calc
    _ = (B ≫ f5) ≫ d0 := by
      rw [← Category.assoc B f5 A5]
      exact sextupleQuintuple_cancel_iso T (B ≫ f5) d0
    _ = (B ≫ f0) ≫ d4 := by
      have hc := congrArg
        (fun m : stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace05 T).symm
      simpa only [Category.assoc] using hc
    _ = (B ≫ f0 ≫ A5) ≫ (B5 ≫ d4) := by
      rw [← Category.assoc B f0 A5]
      exact (sextupleQuintuple_cancel_iso T (B ≫ f0) d4).symm

/-- Exact genuine categorical face-square (1,5). -/
theorem stoneanCechCategoricalSextuple_face15_commute
    (T : Profinite.{u}) :
    (pullback.fst
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace1 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace1 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) := by
  rw [← stoneanCechCategoricalSextuple_face5_eq_first T]
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := sextupleFace1 T
  let f5 := sextupleFace5 T
  let d0 := stoneanCechFifthFace1 T
  let d4 := stoneanCechFifthFace4 T
  change (B ≫ f5 ≫ A5) ≫ (B5 ≫ d0) =
    (B ≫ f0 ≫ A5) ≫ (B5 ≫ d4)
  calc
    _ = (B ≫ f5) ≫ d0 := by
      rw [← Category.assoc B f5 A5]
      exact sextupleQuintuple_cancel_iso T (B ≫ f5) d0
    _ = (B ≫ f0) ≫ d4 := by
      have hc := congrArg
        (fun m : stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace15 T).symm
      simpa only [Category.assoc] using hc
    _ = (B ≫ f0 ≫ A5) ≫ (B5 ≫ d4) := by
      rw [← Category.assoc B f0 A5]
      exact (sextupleQuintuple_cancel_iso T (B ≫ f0) d4).symm

#print axioms stoneanCechCategoricalSextuple_face15_commute

/-- Exact genuine categorical face-square (2,5). -/
theorem stoneanCechCategoricalSextuple_face25_commute
    (T : Profinite.{u}) :
    (pullback.fst
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace2 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace2 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) := by
  rw [← stoneanCechCategoricalSextuple_face5_eq_first T]
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := sextupleFace2 T
  let f5 := sextupleFace5 T
  let d0 := stoneanCechFifthFace2 T
  let d4 := stoneanCechFifthFace4 T
  change (B ≫ f5 ≫ A5) ≫ (B5 ≫ d0) =
    (B ≫ f0 ≫ A5) ≫ (B5 ≫ d4)
  calc
    _ = (B ≫ f5) ≫ d0 := by
      rw [← Category.assoc B f5 A5]
      exact sextupleQuintuple_cancel_iso T (B ≫ f5) d0
    _ = (B ≫ f0) ≫ d4 := by
      have hc := congrArg
        (fun m : stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace25 T).symm
      simpa only [Category.assoc] using hc
    _ = (B ≫ f0 ≫ A5) ≫ (B5 ≫ d4) := by
      rw [← Category.assoc B f0 A5]
      exact (sextupleQuintuple_cancel_iso T (B ≫ f0) d4).symm

#print axioms stoneanCechCategoricalSextuple_face25_commute

/-- Exact genuine categorical face-square (3,5). -/
theorem stoneanCechCategoricalSextuple_face35_commute
    (T : Profinite.{u}) :
    (pullback.fst
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace3 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace3 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) := by
  rw [← stoneanCechCategoricalSextuple_face5_eq_first T]
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := sextupleFace3 T
  let f5 := sextupleFace5 T
  let d0 := stoneanCechFifthFace3 T
  let d4 := stoneanCechFifthFace4 T
  change (B ≫ f5 ≫ A5) ≫ (B5 ≫ d0) =
    (B ≫ f0 ≫ A5) ≫ (B5 ≫ d4)
  calc
    _ = (B ≫ f5) ≫ d0 := by
      rw [← Category.assoc B f5 A5]
      exact sextupleQuintuple_cancel_iso T (B ≫ f5) d0
    _ = (B ≫ f0) ≫ d4 := by
      have hc := congrArg
        (fun m : stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace35 T).symm
      simpa only [Category.assoc] using hc
    _ = (B ≫ f0 ≫ A5) ≫ (B5 ≫ d4) := by
      rw [← Category.assoc B f0 A5]
      exact (sextupleQuintuple_cancel_iso T (B ≫ f0) d4).symm

#print axioms stoneanCechCategoricalSextuple_face35_commute

/-- Exact genuine categorical face-square (4,5). -/
theorem stoneanCechCategoricalSextuple_face45_commute
    (T : Profinite.{u}) :
    (pullback.fst
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) =
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace4 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      (stoneanCechCategoricalQuintupleToExplicit T ≫
        stoneanCechFifthFace4 T) := by
  rw [← stoneanCechCategoricalSextuple_face5_eq_first T]
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let f0 := sextupleFace4 T
  let f5 := sextupleFace5 T
  let d0 := stoneanCechFifthFace4 T
  let d4 := stoneanCechFifthFace4 T
  change (B ≫ f5 ≫ A5) ≫ (B5 ≫ d0) =
    (B ≫ f0 ≫ A5) ≫ (B5 ≫ d4)
  calc
    _ = (B ≫ f5) ≫ d0 := by
      rw [← Category.assoc B f5 A5]
      exact sextupleQuintuple_cancel_iso T (B ≫ f5) d0
    _ = (B ≫ f0) ≫ d4 := by
      have hc := congrArg
        (fun m : stoneanCechExplicitSextupleProfinite T ⟶
          stoneanPresentationCechQuadruples T => B ≫ m)
        (sextupleCategoricalFace45 T).symm
      simpa only [Category.assoc] using hc
    _ = (B ≫ f0 ≫ A5) ≫ (B5 ≫ d4) := by
      rw [← Category.assoc B f0 A5]
      exact (sextupleQuintuple_cancel_iso T (B ≫ f0) d4).symm

#print axioms stoneanCechCategoricalSextuple_face45_commute

#print axioms stoneanCechCategoricalSextuple_face05_commute
/-- Fifth vertex of true categorical fivefold probe is the
actual last pullback projection at every Stonean test object. -/
theorem stoneanCompHausProbeCechQuintupleUlift_fifthVertex
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechQuintuples T))) :
    (stoneanCompHausProbeCechQuintupleUliftEquiv T U z).val.2.2.2.2 =
      ULift.up (z.down ≫ profiniteToCompHaus.map
        (pullback.snd
          (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
          (Profinite.presentation.π T))) := by
  rfl

/-- Coordinate-free proof that deleting an early vertex from the
genuine categorical sixfold fibre relation retains its last vertex. -/
theorem stoneanCechCategoricalSextuple_face0_last
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace0 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      pullback.snd
        (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
        (Profinite.presentation.π T) =
    pullback.snd
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) := by
  apply ConcreteCategory.hom_ext
  intro z
  let q := (sextupleFace0 T).hom.hom
    ((stoneanCechCategoricalSextupleToExplicit T).hom.hom z)
  have h := congrArg (fun m :
    stoneanCechExplicitQuintupleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation => m.hom.hom q)
    (stoneanCechExplicitQuintupleToAbstract_fifth T)
  change
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
      ((stoneanCechExplicitQuintupleToAbstract T).hom.hom q) =
    (explicitQuintupleFifth T).hom.hom q at h
  change
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
      ((stoneanCechExplicitQuintupleToAbstract T).hom.hom q) =
    (pullback.snd
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z
  rw [h]
  rfl

#print axioms stoneanCechCategoricalSextuple_face0_last
/-- Actual sixth last vertex is preserved by face 1. -/
theorem stoneanCechCategoricalSextuple_face1_last
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace1 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      pullback.snd
        (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
        (Profinite.presentation.π T) =
    pullback.snd
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) := by
  apply ConcreteCategory.hom_ext
  intro z
  let q := (sextupleFace1 T).hom.hom
    ((stoneanCechCategoricalSextupleToExplicit T).hom.hom z)
  have h := congrArg (fun m :
    stoneanCechExplicitQuintupleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation => m.hom.hom q)
    (stoneanCechExplicitQuintupleToAbstract_fifth T)
  change
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
      ((stoneanCechExplicitQuintupleToAbstract T).hom.hom q) =
    (explicitQuintupleFifth T).hom.hom q at h
  change
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
      ((stoneanCechExplicitQuintupleToAbstract T).hom.hom q) =
    (pullback.snd
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z
  rw [h]
  rfl

#print axioms stoneanCechCategoricalSextuple_face1_last

/-- Actual sixth last vertex is preserved by face 2. -/
theorem stoneanCechCategoricalSextuple_face2_last
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace2 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      pullback.snd
        (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
        (Profinite.presentation.π T) =
    pullback.snd
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) := by
  apply ConcreteCategory.hom_ext
  intro z
  let q := (sextupleFace2 T).hom.hom
    ((stoneanCechCategoricalSextupleToExplicit T).hom.hom z)
  have h := congrArg (fun m :
    stoneanCechExplicitQuintupleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation => m.hom.hom q)
    (stoneanCechExplicitQuintupleToAbstract_fifth T)
  change
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
      ((stoneanCechExplicitQuintupleToAbstract T).hom.hom q) =
    (explicitQuintupleFifth T).hom.hom q at h
  change
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
      ((stoneanCechExplicitQuintupleToAbstract T).hom.hom q) =
    (pullback.snd
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z
  rw [h]
  rfl

#print axioms stoneanCechCategoricalSextuple_face2_last

/-- Actual sixth last vertex is preserved by face 3. -/
theorem stoneanCechCategoricalSextuple_face3_last
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace3 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      pullback.snd
        (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
        (Profinite.presentation.π T) =
    pullback.snd
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) := by
  apply ConcreteCategory.hom_ext
  intro z
  let q := (sextupleFace3 T).hom.hom
    ((stoneanCechCategoricalSextupleToExplicit T).hom.hom z)
  have h := congrArg (fun m :
    stoneanCechExplicitQuintupleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation => m.hom.hom q)
    (stoneanCechExplicitQuintupleToAbstract_fifth T)
  change
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
      ((stoneanCechExplicitQuintupleToAbstract T).hom.hom q) =
    (explicitQuintupleFifth T).hom.hom q at h
  change
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
      ((stoneanCechExplicitQuintupleToAbstract T).hom.hom q) =
    (pullback.snd
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z
  rw [h]
  rfl

#print axioms stoneanCechCategoricalSextuple_face3_last

/-- Actual sixth last vertex is preserved by face 4. -/
theorem stoneanCechCategoricalSextuple_face4_last
    (T : Profinite.{u}) :
    (stoneanCechCategoricalSextupleToExplicit T ≫
      sextupleFace4 T ≫ stoneanCechExplicitQuintupleToAbstract T) ≫
      pullback.snd
        (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
        (Profinite.presentation.π T) =
    pullback.snd
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T) := by
  apply ConcreteCategory.hom_ext
  intro z
  let q := (sextupleFace4 T).hom.hom
    ((stoneanCechCategoricalSextupleToExplicit T).hom.hom z)
  have h := congrArg (fun m :
    stoneanCechExplicitQuintupleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation => m.hom.hom q)
    (stoneanCechExplicitQuintupleToAbstract_fifth T)
  change
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
      ((stoneanCechExplicitQuintupleToAbstract T).hom.hom q) =
    (explicitQuintupleFifth T).hom.hom q at h
  change
    (pullback.snd
      (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom
      ((stoneanCechExplicitQuintupleToAbstract T).hom.hom q) =
    (pullback.snd
      (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
      (Profinite.presentation.π T)).hom.hom z
  rw [h]
  rfl

#print axioms stoneanCechCategoricalSextuple_face4_last


/-- True represented degree-four face square: early deletion zero. -/
theorem stoneanCompHausProbeCechSextupleUlift_face0
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechSextuples T))) :
    splitFreeCechSextFace0 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechSextupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuintupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (stoneanCechCategoricalSextupleToExplicit T ≫
          sextupleFace0 T ≫ stoneanCechExplicitQuintupleToAbstract T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let e5 := stoneanCompHausProbeCechQuintupleUliftEquiv T U
  let F := pullback.fst
    (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let W := pullback.snd
    (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let V := pullback.snd
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let D := stoneanCechCategoricalSextupleToExplicit T ≫
    sextupleFace0 T ≫ stoneanCechExplicitQuintupleToAbstract T
  let q0 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map F)
  let q1 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map D)
  have hquad :
      splitFreeCechQuintFace0 p (e5 q0) =
      splitFreeCechQuintFace4 p (e5 q1) := by
    rw [stoneanCompHausProbeCechQuintupleUlift_face0,
      stoneanCompHausProbeCechQuintupleUlift_face4]
    apply congrArg (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map
       (F ≫ (stoneanCechCategoricalQuintupleToExplicit T ≫
         stoneanCechFifthFace0 T)) =
      z.down ≫ profiniteToCompHaus.map
       (D ≫ (stoneanCechCategoricalQuintupleToExplicit T ≫
         stoneanCechFifthFace4 T))
    exact congrArg (fun m :
       stoneanPresentationCechSextuples T ⟶
         stoneanPresentationCechQuadruples T =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalSextuple_face05_commute T)
  have hlast :
      ULift.up (z.down ≫ profiniteToCompHaus.map W) =
      (e5 q1).val.2.2.2.2 := by
    rw [stoneanCompHausProbeCechQuintupleUlift_fifthVertex]
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map W =
      z.down ≫ profiniteToCompHaus.map (D ≫ V)
    exact congrArg (fun m :
      stoneanPresentationCechSextuples T ⟶
        Stonean.toProfinite.obj T.presentation =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalSextuple_face0_last T).symm
  apply Subtype.ext
  apply Prod.ext
  · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.1) hquad
  · apply Prod.ext
    · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.1) hquad
    · apply Prod.ext
      · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.2.1) hquad
      · apply Prod.ext
        · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.2.2) hquad
        · exact hlast

#print axioms stoneanCompHausProbeCechSextupleUlift_face0
/-- True represented degree-four face square: early deletion 1. -/
theorem stoneanCompHausProbeCechSextupleUlift_face1
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechSextuples T))) :
    splitFreeCechSextFace1 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechSextupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuintupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (stoneanCechCategoricalSextupleToExplicit T ≫
          sextupleFace1 T ≫ stoneanCechExplicitQuintupleToAbstract T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let e5 := stoneanCompHausProbeCechQuintupleUliftEquiv T U
  let F := pullback.fst
    (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let W := pullback.snd
    (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let V := pullback.snd
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let D := stoneanCechCategoricalSextupleToExplicit T ≫
    sextupleFace1 T ≫ stoneanCechExplicitQuintupleToAbstract T
  let q0 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map F)
  let q1 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map D)
  have hquad :
      splitFreeCechQuintFace1 p (e5 q0) =
      splitFreeCechQuintFace4 p (e5 q1) := by
    rw [stoneanCompHausProbeCechQuintupleUlift_face1,
      stoneanCompHausProbeCechQuintupleUlift_face4]
    apply congrArg (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map
       (F ≫ (stoneanCechCategoricalQuintupleToExplicit T ≫
         stoneanCechFifthFace1 T)) =
      z.down ≫ profiniteToCompHaus.map
       (D ≫ (stoneanCechCategoricalQuintupleToExplicit T ≫
         stoneanCechFifthFace4 T))
    exact congrArg (fun m :
       stoneanPresentationCechSextuples T ⟶
         stoneanPresentationCechQuadruples T =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalSextuple_face15_commute T)
  have hlast :
      ULift.up (z.down ≫ profiniteToCompHaus.map W) =
      (e5 q1).val.2.2.2.2 := by
    rw [stoneanCompHausProbeCechQuintupleUlift_fifthVertex]
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map W =
      z.down ≫ profiniteToCompHaus.map (D ≫ V)
    exact congrArg (fun m :
      stoneanPresentationCechSextuples T ⟶
        Stonean.toProfinite.obj T.presentation =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalSextuple_face1_last T).symm
  apply Subtype.ext
  apply Prod.ext
  · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.1) hquad
  · apply Prod.ext
    · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.1) hquad
    · apply Prod.ext
      · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.2.1) hquad
      · apply Prod.ext
        · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.2.2) hquad
        · exact hlast

#print axioms stoneanCompHausProbeCechSextupleUlift_face1

/-- True represented degree-four face square: early deletion 2. -/
theorem stoneanCompHausProbeCechSextupleUlift_face2
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechSextuples T))) :
    splitFreeCechSextFace2 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechSextupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuintupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (stoneanCechCategoricalSextupleToExplicit T ≫
          sextupleFace2 T ≫ stoneanCechExplicitQuintupleToAbstract T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let e5 := stoneanCompHausProbeCechQuintupleUliftEquiv T U
  let F := pullback.fst
    (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let W := pullback.snd
    (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let V := pullback.snd
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let D := stoneanCechCategoricalSextupleToExplicit T ≫
    sextupleFace2 T ≫ stoneanCechExplicitQuintupleToAbstract T
  let q0 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map F)
  let q1 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map D)
  have hquad :
      splitFreeCechQuintFace2 p (e5 q0) =
      splitFreeCechQuintFace4 p (e5 q1) := by
    rw [stoneanCompHausProbeCechQuintupleUlift_face2,
      stoneanCompHausProbeCechQuintupleUlift_face4]
    apply congrArg (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map
       (F ≫ (stoneanCechCategoricalQuintupleToExplicit T ≫
         stoneanCechFifthFace2 T)) =
      z.down ≫ profiniteToCompHaus.map
       (D ≫ (stoneanCechCategoricalQuintupleToExplicit T ≫
         stoneanCechFifthFace4 T))
    exact congrArg (fun m :
       stoneanPresentationCechSextuples T ⟶
         stoneanPresentationCechQuadruples T =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalSextuple_face25_commute T)
  have hlast :
      ULift.up (z.down ≫ profiniteToCompHaus.map W) =
      (e5 q1).val.2.2.2.2 := by
    rw [stoneanCompHausProbeCechQuintupleUlift_fifthVertex]
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map W =
      z.down ≫ profiniteToCompHaus.map (D ≫ V)
    exact congrArg (fun m :
      stoneanPresentationCechSextuples T ⟶
        Stonean.toProfinite.obj T.presentation =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalSextuple_face2_last T).symm
  apply Subtype.ext
  apply Prod.ext
  · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.1) hquad
  · apply Prod.ext
    · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.1) hquad
    · apply Prod.ext
      · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.2.1) hquad
      · apply Prod.ext
        · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.2.2) hquad
        · exact hlast

#print axioms stoneanCompHausProbeCechSextupleUlift_face2

/-- True represented degree-four face square: early deletion 3. -/
theorem stoneanCompHausProbeCechSextupleUlift_face3
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechSextuples T))) :
    splitFreeCechSextFace3 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechSextupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuintupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (stoneanCechCategoricalSextupleToExplicit T ≫
          sextupleFace3 T ≫ stoneanCechExplicitQuintupleToAbstract T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let e5 := stoneanCompHausProbeCechQuintupleUliftEquiv T U
  let F := pullback.fst
    (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let W := pullback.snd
    (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let V := pullback.snd
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let D := stoneanCechCategoricalSextupleToExplicit T ≫
    sextupleFace3 T ≫ stoneanCechExplicitQuintupleToAbstract T
  let q0 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map F)
  let q1 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map D)
  have hquad :
      splitFreeCechQuintFace3 p (e5 q0) =
      splitFreeCechQuintFace4 p (e5 q1) := by
    rw [stoneanCompHausProbeCechQuintupleUlift_face3,
      stoneanCompHausProbeCechQuintupleUlift_face4]
    apply congrArg (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map
       (F ≫ (stoneanCechCategoricalQuintupleToExplicit T ≫
         stoneanCechFifthFace3 T)) =
      z.down ≫ profiniteToCompHaus.map
       (D ≫ (stoneanCechCategoricalQuintupleToExplicit T ≫
         stoneanCechFifthFace4 T))
    exact congrArg (fun m :
       stoneanPresentationCechSextuples T ⟶
         stoneanPresentationCechQuadruples T =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalSextuple_face35_commute T)
  have hlast :
      ULift.up (z.down ≫ profiniteToCompHaus.map W) =
      (e5 q1).val.2.2.2.2 := by
    rw [stoneanCompHausProbeCechQuintupleUlift_fifthVertex]
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map W =
      z.down ≫ profiniteToCompHaus.map (D ≫ V)
    exact congrArg (fun m :
      stoneanPresentationCechSextuples T ⟶
        Stonean.toProfinite.obj T.presentation =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalSextuple_face3_last T).symm
  apply Subtype.ext
  apply Prod.ext
  · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.1) hquad
  · apply Prod.ext
    · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.1) hquad
    · apply Prod.ext
      · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.2.1) hquad
      · apply Prod.ext
        · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.2.2) hquad
        · exact hlast

#print axioms stoneanCompHausProbeCechSextupleUlift_face3

/-- True represented degree-four face square: early deletion 4. -/
theorem stoneanCompHausProbeCechSextupleUlift_face4
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechSextuples T))) :
    splitFreeCechSextFace4 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechSextupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuintupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (stoneanCechCategoricalSextupleToExplicit T ≫
          sextupleFace4 T ≫ stoneanCechExplicitQuintupleToAbstract T))) := by
  let p := stoneanCompHausProbePresentationMap T U
  let e5 := stoneanCompHausProbeCechQuintupleUliftEquiv T U
  let F := pullback.fst
    (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let W := pullback.snd
    (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let V := pullback.snd
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  let D := stoneanCechCategoricalSextupleToExplicit T ≫
    sextupleFace4 T ≫ stoneanCechExplicitQuintupleToAbstract T
  let q0 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map F)
  let q1 : ULift.{u + 1}
    (U.compHaus ⟶ profiniteToCompHaus.obj
      (stoneanPresentationCechQuintuples T)) :=
      ULift.up (z.down ≫ profiniteToCompHaus.map D)
  have hquad :
      splitFreeCechQuintFace4 p (e5 q0) =
      splitFreeCechQuintFace4 p (e5 q1) := by
    rw [stoneanCompHausProbeCechQuintupleUlift_face4,
      stoneanCompHausProbeCechQuintupleUlift_face4]
    apply congrArg (stoneanCompHausProbeCechQuadrupleUliftEquiv T U)
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map
       (F ≫ (stoneanCechCategoricalQuintupleToExplicit T ≫
         stoneanCechFifthFace4 T)) =
      z.down ≫ profiniteToCompHaus.map
       (D ≫ (stoneanCechCategoricalQuintupleToExplicit T ≫
         stoneanCechFifthFace4 T))
    exact congrArg (fun m :
       stoneanPresentationCechSextuples T ⟶
         stoneanPresentationCechQuadruples T =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalSextuple_face45_commute T)
  have hlast :
      ULift.up (z.down ≫ profiniteToCompHaus.map W) =
      (e5 q1).val.2.2.2.2 := by
    rw [stoneanCompHausProbeCechQuintupleUlift_fifthVertex]
    apply congrArg ULift.up
    change z.down ≫ profiniteToCompHaus.map W =
      z.down ≫ profiniteToCompHaus.map (D ≫ V)
    exact congrArg (fun m :
      stoneanPresentationCechSextuples T ⟶
        Stonean.toProfinite.obj T.presentation =>
        z.down ≫ profiniteToCompHaus.map m)
      (stoneanCechCategoricalSextuple_face4_last T).symm
  apply Subtype.ext
  apply Prod.ext
  · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.1) hquad
  · apply Prod.ext
    · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.1) hquad
    · apply Prod.ext
      · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.2.1) hquad
      · apply Prod.ext
        · exact congrArg (fun t : splitFreeCechQuadruple p => t.val.2.2.2) hquad
        · exact hlast

#print axioms stoneanCompHausProbeCechSextupleUlift_face4

end CMDG.CondensedCM5R0
