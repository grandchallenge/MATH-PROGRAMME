import CMDGCondensedCM4P3DerivedCM5R0SextupleProbeComparison
import CMDGCondensedCM4P3DerivedCM5R0GenuineFifthCechBoundary

/-!
# CM5: genuine categorical sixth Čech fibre product

The categorical sixth iterated Profinite pullback is identified
with the actual compact closed equal-image sixfold relation.
No split-point surrogate or unproven cohomology is used.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- The first vertex of the actual categorical fifth Čech object. -/
noncomputable def stoneanCechQuintupleVertexFirst (T : Profinite.{u}) :
    stoneanPresentationCechQuintuples T ⟶
      Stonean.toProfinite.obj T.presentation :=
  pullback.fst
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T) ≫
      stoneanCechQuadrupleVertexFirst T

/-- The ACTUAL sixth iterated categorical Profinite pullback. -/
noncomputable def stoneanPresentationCechSextuples (T : Profinite.{u}) :
    Profinite.{u} :=
  pullback (stoneanCechQuintupleVertexFirst T ≫
    Profinite.presentation.π T) (Profinite.presentation.π T)

theorem stoneanCechQuintupleVertexFirst_atClosed
    (T : Profinite.{u})
    (r : stoneanCechExplicitQuintupleProfinite T) :
    (stoneanCechQuintupleVertexFirst T).hom.hom
      ((stoneanCechExplicitQuintupleToAbstract T).hom.hom r) =
        r.val.1 := by
  let F := pullback.fst
    (stoneanCechQuadrupleVertexFirst T ≫ Profinite.presentation.π T)
    (Profinite.presentation.π T)
  have h := congrArg (fun m :
      stoneanCechExplicitQuintupleProfinite T ⟶
        stoneanPresentationCechQuadruples T => m.hom.hom r)
    (stoneanCechExplicitQuintupleToAbstract_first T)
  change F.hom.hom
    ((stoneanCechExplicitQuintupleToAbstract T).hom.hom r) =
    (stoneanCechExplicitQuadrupleToAbstract T).hom.hom
      ((quintupleFace4 T).hom.hom r) at h
  change (stoneanCechQuadrupleVertexFirst T).hom.hom
    (F.hom.hom ((stoneanCechExplicitQuintupleToAbstract T).hom.hom r)) =
      r.val.1
  rw [h, stoneanCechQuadrupleVertexFirst_atClosed]
  rfl

noncomputable def explicitSextupleSixth (T : Profinite.{u}) :
    stoneanCechExplicitSextupleProfinite T ⟶
      Stonean.toProfinite.obj T.presentation := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  exact CompHausLike.ofHom _ (⟨fun q => q.val.2.2.2.2.2,
    by fun_prop⟩ : C(stoneanCechExplicitSextupleProfinite T, P))

/-- Genuine closed-sixfold to categorical-sixfold Profinite map. -/
noncomputable def stoneanCechExplicitSextupleToAbstract (T : Profinite.{u}) :
    stoneanCechExplicitSextupleProfinite T ⟶
      stoneanPresentationCechSextuples T := by
  let p := Profinite.presentation.π T
  let a := sextupleFace5 T ≫ stoneanCechExplicitQuintupleToAbstract T
  let b := explicitSextupleSixth T
  have h : a ≫ (stoneanCechQuintupleVertexFirst T ≫ p) = b ≫ p := by
    apply ConcreteCategory.hom_ext
    intro z
    change p.hom.hom
      ((stoneanCechQuintupleVertexFirst T).hom.hom
        ((stoneanCechExplicitQuintupleToAbstract T).hom.hom
          ((sextupleFace5 T).hom.hom z))) =
      p.hom.hom ((explicitSextupleSixth T).hom.hom z)
    rw [stoneanCechQuintupleVertexFirst_atClosed]
    have hf : ((sextupleFace5 T).hom.hom z).val.1 = z.val.1 := rfl
    have hv : (explicitSextupleSixth T).hom.hom z = z.val.2.2.2.2.2 := rfl
    rw [hf, hv]
    exact z.property.1.trans
      (z.property.2.1.trans
        (z.property.2.2.1.trans
          (z.property.2.2.2.1.trans z.property.2.2.2.2)))
  exact pullback.lift a b h

theorem stoneanCechExplicitSextupleToAbstract_first (T : Profinite.{u}) :
    stoneanCechExplicitSextupleToAbstract T ≫
      pullback.fst
        (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
        (Profinite.presentation.π T) =
      sextupleFace5 T ≫ stoneanCechExplicitQuintupleToAbstract T := by
  unfold stoneanCechExplicitSextupleToAbstract
  exact pullback.lift_fst _ _ _

theorem stoneanCechExplicitSextupleToAbstract_sixth (T : Profinite.{u}) :
    stoneanCechExplicitSextupleToAbstract T ≫
      pullback.snd
        (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
        (Profinite.presentation.π T) =
      explicitSextupleSixth T := by
  unfold stoneanCechExplicitSextupleToAbstract
  exact pullback.lift_snd _ _ _


/-- Reverse true categorical sixth pullback to the *closed* profinite
equal-image relation, preserving all six genuine coordinates. -/
noncomputable def stoneanCechCategoricalSextupleToExplicit (T : Profinite.{u}) :
    stoneanPresentationCechSextuples T ⟶
      stoneanCechExplicitSextupleProfinite T := by
  let P := Stonean.toProfinite.obj T.presentation
  let p := Profinite.presentation.π T
  let F := pullback.fst (stoneanCechQuintupleVertexFirst T ≫ p) p
  let W := pullback.snd (stoneanCechQuintupleVertexFirst T ≫ p) p
  let B := stoneanCechCategoricalQuintupleToExplicit T
  letI : CompactSpace
      (↥(profiniteCechSextupleRelatedSet P T p)) :=
    isCompact_iff_compactSpace.mp
      (profiniteCechSextupleRelatedSet_isClosed P T p).isCompact
  have hlast (z : stoneanPresentationCechSextuples T) :
      p.hom.hom ((B.hom.hom (F.hom.hom z)).val.2.2.2.2) =
      p.hom.hom (W.hom.hom z) := by
    let r5 := B.hom.hom (F.hom.hom z)
    have hBA := congrArg (fun f :
        stoneanPresentationCechQuintuples T ⟶
          stoneanPresentationCechQuintuples T =>
            f.hom.hom (F.hom.hom z))
      (stoneanCechCategoricalQuintuple_roundtrip T)
    change (stoneanCechExplicitQuintupleToAbstract T).hom.hom r5 =
        F.hom.hom z at hBA
    have hfirst := stoneanCechQuintupleVertexFirst_atClosed T r5
    rw [hBA] at hfirst
    have hf := congrArg (fun k :
        stoneanPresentationCechSextuples T ⟶ T => k.hom.hom z)
      (pullback.condition :
        F ≫ (stoneanCechQuintupleVertexFirst T ≫ p) = W ≫ p)
    change p.hom.hom
        ((stoneanCechQuintupleVertexFirst T).hom.hom (F.hom.hom z)) =
      p.hom.hom (W.hom.hom z) at hf
    have he : p.hom.hom r5.val.1 = p.hom.hom (W.hom.hom z) := by
      rw [← hfirst]
      exact hf
    exact (r5.property.1.trans
      (r5.property.2.1.trans
        (r5.property.2.2.1.trans r5.property.2.2.2))).symm.trans he
  let c : C(stoneanPresentationCechSextuples T,
      ↥(profiniteCechSextupleRelatedSet P T p)) := by
    refine ⟨fun z =>
      ⟨((B.hom.hom (F.hom.hom z)).val.1,
        ((B.hom.hom (F.hom.hom z)).val.2.1,
          ((B.hom.hom (F.hom.hom z)).val.2.2.1,
            ((B.hom.hom (F.hom.hom z)).val.2.2.2.1,
              ((B.hom.hom (F.hom.hom z)).val.2.2.2.2,
                W.hom.hom z))))),
        ⟨(B.hom.hom (F.hom.hom z)).property.1,
          (B.hom.hom (F.hom.hom z)).property.2.1,
          (B.hom.hom (F.hom.hom z)).property.2.2.1,
          (B.hom.hom (F.hom.hom z)).property.2.2.2,
          hlast z⟩⟩, ?_⟩
    apply Continuous.subtype_mk
    let tr : stoneanPresentationCechSextuples T ⟶
        stoneanCechExplicitQuintupleProfinite T := F ≫ B
    have htr : Continuous (fun z : stoneanPresentationCechSextuples T =>
        (B.hom.hom (F.hom.hom z)).val) :=
      continuous_subtype_val.comp tr.hom.hom.continuous
    exact (continuous_fst.comp htr).prodMk
      ((continuous_fst.comp (continuous_snd.comp htr)).prodMk
        ((continuous_fst.comp
          (continuous_snd.comp (continuous_snd.comp htr))).prodMk
          ((continuous_fst.comp
            (continuous_snd.comp
              (continuous_snd.comp (continuous_snd.comp htr)))).prodMk
            ((continuous_snd.comp
              (continuous_snd.comp
                (continuous_snd.comp (continuous_snd.comp htr)))).prodMk
                  W.hom.hom.continuous))))
  exact CompHausLike.ofHom _ c


/-- Closed sixfold → categorical sixth pullback → closed sixfold
is the identity on the ACTUAL compact Profinite relation. -/
theorem stoneanCechExplicitSextuple_roundtrip (T : Profinite.{u}) :
    stoneanCechExplicitSextupleToAbstract T ≫
      stoneanCechCategoricalSextupleToExplicit T =
        𝟙 (stoneanCechExplicitSextupleProfinite T) := by
  apply ConcreteCategory.hom_ext
  intro z
  apply Subtype.ext
  change ((stoneanCechCategoricalSextupleToExplicit T).hom.hom
    ((stoneanCechExplicitSextupleToAbstract T).hom.hom z)).val = z.val
  let p := Profinite.presentation.π T
  let F := pullback.fst (stoneanCechQuintupleVertexFirst T ≫ p) p
  let W := pullback.snd (stoneanCechQuintupleVertexFirst T ≫ p) p
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  have hf : F.hom.hom
      ((stoneanCechExplicitSextupleToAbstract T).hom.hom z) =
    A5.hom.hom ((sextupleFace5 T).hom.hom z) := by
    have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
        stoneanPresentationCechQuintuples T => m.hom.hom z)
      (stoneanCechExplicitSextupleToAbstract_first T)
    exact h
  have hw : W.hom.hom
      ((stoneanCechExplicitSextupleToAbstract T).hom.hom z) =
        z.val.2.2.2.2.2 := by
    have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
        Stonean.toProfinite.obj T.presentation => m.hom.hom z)
      (stoneanCechExplicitSextupleToAbstract_sixth T)
    exact h
  have h5 : B5.hom.hom (F.hom.hom
      ((stoneanCechExplicitSextupleToAbstract T).hom.hom z)) =
      (sextupleFace5 T).hom.hom z := by
    rw [hf]
    have h := congrArg (fun m :
        stoneanCechExplicitQuintupleProfinite T ⟶
          stoneanCechExplicitQuintupleProfinite T =>
            m.hom.hom ((sextupleFace5 T).hom.hom z))
      (stoneanCechExplicitQuintuple_roundtrip T)
    exact h
  change
    ((B5.hom.hom (F.hom.hom
      ((stoneanCechExplicitSextupleToAbstract T).hom.hom z))).val.1,
      ((B5.hom.hom (F.hom.hom
        ((stoneanCechExplicitSextupleToAbstract T).hom.hom z))).val.2.1,
        ((B5.hom.hom (F.hom.hom
          ((stoneanCechExplicitSextupleToAbstract T).hom.hom z))).val.2.2.1,
          ((B5.hom.hom (F.hom.hom
            ((stoneanCechExplicitSextupleToAbstract T).hom.hom z))).val.2.2.2.1,
            ((B5.hom.hom (F.hom.hom
              ((stoneanCechExplicitSextupleToAbstract T).hom.hom z))).val.2.2.2.2,
              W.hom.hom ((stoneanCechExplicitSextupleToAbstract T).hom.hom z)))))) =
      z.val
  rw [h5, hw]
  rfl

/-- Actual categorical sixth pullback → closed sixfold → original
categorical object equals the identity, by both universal projections. -/
theorem stoneanCechCategoricalSextuple_roundtrip (T : Profinite.{u}) :
    stoneanCechCategoricalSextupleToExplicit T ≫
      stoneanCechExplicitSextupleToAbstract T =
        𝟙 (stoneanPresentationCechSextuples T) := by
  let p := Profinite.presentation.π T
  let F := pullback.fst (stoneanCechQuintupleVertexFirst T ≫ p) p
  let W := pullback.snd (stoneanCechQuintupleVertexFirst T ≫ p) p
  let A := stoneanCechExplicitSextupleToAbstract T
  let B := stoneanCechCategoricalSextupleToExplicit T
  let A5 := stoneanCechExplicitQuintupleToAbstract T
  let B5 := stoneanCechCategoricalQuintupleToExplicit T
  let E := sextupleFace5 T
  let V := explicitSextupleSixth T
  have hf : B ≫ E = F ≫ B5 := by
    apply ConcreteCategory.hom_ext
    intro z
    apply Subtype.ext
    change (E.hom.hom (B.hom.hom z)).val =
      (B5.hom.hom (F.hom.hom z)).val
    rfl
  have hw : B ≫ V = W := by
    apply ConcreteCategory.hom_ext
    intro z
    change V.hom.hom (B.hom.hom z) = W.hom.hom z
    rfl
  apply pullback.hom_ext
  · apply ConcreteCategory.hom_ext
    intro z
    change F.hom.hom (A.hom.hom (B.hom.hom z)) = F.hom.hom z
    have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
        stoneanPresentationCechQuintuples T =>
          m.hom.hom (B.hom.hom z))
      (stoneanCechExplicitSextupleToAbstract_first T)
    change F.hom.hom (A.hom.hom (B.hom.hom z)) =
      A5.hom.hom (E.hom.hom (B.hom.hom z)) at h
    rw [h]
    have he := congrArg (fun m :
        stoneanPresentationCechSextuples T ⟶
        stoneanCechExplicitQuintupleProfinite T => m.hom.hom z) hf
    change E.hom.hom (B.hom.hom z) =
      B5.hom.hom (F.hom.hom z) at he
    rw [he]
    have hr := congrArg (fun m :
        stoneanPresentationCechQuintuples T ⟶
        stoneanPresentationCechQuintuples T =>
          m.hom.hom (F.hom.hom z))
      (stoneanCechCategoricalQuintuple_roundtrip T)
    exact hr
  · apply ConcreteCategory.hom_ext
    intro z
    change W.hom.hom (A.hom.hom (B.hom.hom z)) = W.hom.hom z
    have h := congrArg (fun m :
        stoneanCechExplicitSextupleProfinite T ⟶
        Stonean.toProfinite.obj T.presentation =>
          m.hom.hom (B.hom.hom z))
      (stoneanCechExplicitSextupleToAbstract_sixth T)
    change W.hom.hom (A.hom.hom (B.hom.hom z)) =
      V.hom.hom (B.hom.hom z) at h
    rw [h]
    have he := congrArg (fun m :
        stoneanPresentationCechSextuples T ⟶
        Stonean.toProfinite.obj T.presentation => m.hom.hom z) hw
    exact he

noncomputable def stoneanCechExplicitSextupleIso (T : Profinite.{u}) :
    stoneanCechExplicitSextupleProfinite T ≅
      stoneanPresentationCechSextuples T where
  hom := stoneanCechExplicitSextupleToAbstract T
  inv := stoneanCechCategoricalSextupleToExplicit T
  hom_inv_id := stoneanCechExplicitSextuple_roundtrip T
  inv_hom_id := stoneanCechCategoricalSextuple_roundtrip T

#print axioms stoneanCechExplicitSextupleIso
#print axioms stoneanCechCategoricalSextupleToExplicit
#print axioms stoneanCechExplicitSextupleToAbstract
end CMDG.CondensedCM5R0
