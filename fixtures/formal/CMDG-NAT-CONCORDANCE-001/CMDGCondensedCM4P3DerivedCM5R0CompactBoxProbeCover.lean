import CMDGCondensedCM4P3DerivedCM5R0CompactBoxProbeSlices

/-! Product with a genuine profinite probe. Its Čech relation is
homeomorphic to the probe times the actual cube relation. -/
noncomputable section
universe u
open Set CategoryTheory
namespace CMDG.CondensedCM5R0.CompactCover.Dyadic

variable (S : Profinite.{u}) (I : Type u)

def probeP : Profinite.{u} := Profinite.of (S × (I → Bits))
def probeT : CompHaus.{u} := CompHaus.of (S × (I → Interval))
def probeCover : profiniteToCompHaus.obj (probeP S I) ⟶ probeT S I :=
  CompHausLike.ofHom _ (⟨fun x => (x.1,fun i => value (x.2 i)),
    continuous_fst.prodMk (continuous_pi fun i => value_continuous.comp
      ((continuous_apply i).comp continuous_snd))⟩ :
    C((S × (I → Bits)),(S × (I → Interval))))

theorem probeCover_epi : Epi (probeCover S I) := by
  apply (CompHaus.epi_iff_surjective _).2
  intro y
  choose a ha using fun i => value_surj (y.2 i)
  exact ⟨(y.1,a),Prod.ext rfl (funext ha)⟩

abbrev ProbeRel (n : ℕ) :=
  compactRelationProfinite (probeP S I) (probeT S I) (probeCover S I) n

theorem probeRelation_fst (n : ℕ) (z : ProbeRel S I n) (j : Fin (n+1)) :
    (z.val j).1 = (z.val 0).1 :=
  congrArg (Prod.fst : S × (I → Interval) → S) (z.property j)

theorem probeRelation_snd (n : ℕ) (z : ProbeRel S I n) (j : Fin (n+1)) :
    (cubeCover I).hom.hom (z.val j).2 = (cubeCover I).hom.hom (z.val 0).2 :=
  congrArg Prod.snd (z.property j)

def probeRelationHomeo (n : ℕ) : ProbeRel S I n ≃ₜ (S × Rel I n) where
  toFun z := ((z.val 0).1,⟨fun j => (z.val j).2,probeRelation_snd S I n z⟩)
  invFun z := ⟨fun j => (z.1,z.2.val j),fun j => Prod.ext rfl (z.2.property j)⟩
  left_inv z := by
    apply Subtype.ext
    funext j
    exact Prod.ext (probeRelation_fst S I n z j).symm rfl
  right_inv z := by
    apply Prod.ext
    · rfl
    · apply Subtype.ext
      rfl
  continuous_toFun := by
    apply Continuous.prodMk
    · exact continuous_fst.comp ((continuous_apply 0).comp continuous_subtype_val)
    · apply Continuous.subtype_mk
      apply continuous_pi
      intro j
      exact continuous_snd.comp ((continuous_apply j).comp continuous_subtype_val)
  continuous_invFun := by
    apply Continuous.subtype_mk
    apply continuous_pi
    intro j
    exact continuous_fst.prodMk ((continuous_apply j).comp
      (continuous_subtype_val.comp continuous_snd))

def cubeFace (n : ℕ) (k : Fin (n+2)) : C(Rel I (n+1),Rel I n) :=
  (compactRelationFace (cubeP I) (cubeT I) (cubeCover I) n k).hom.hom

def probeFace (n : ℕ) (k : Fin (n+2)) : C(ProbeRel S I (n+1),ProbeRel S I n) :=
  (compactRelationFace (probeP S I) (probeT S I) (probeCover S I) n k).hom.hom

theorem probeRelationHomeo_face (n : ℕ) (k : Fin (n+2))
    (z : ProbeRel S I (n+1)) :
    probeRelationHomeo S I n (probeFace S I n k z) =
      ((probeRelationHomeo S I (n+1) z).1,
       cubeFace I n k (probeRelationHomeo S I (n+1) z).2) := by
  apply Prod.ext
  · exact probeRelation_fst S I (n+1) z (k.succAbove 0)
  · apply Subtype.ext
    rfl

theorem probeRelationHomeo_symm_face (n : ℕ) (k : Fin (n+2))
    (s : S) (r : Rel I (n+1)) :
    probeFace S I n k ((probeRelationHomeo S I (n+1)).symm (s,r)) =
      (probeRelationHomeo S I n).symm (s,cubeFace I n k r) := by
  apply Subtype.ext
  rfl

#print axioms probeCover_epi
#print axioms probeRelationHomeo
#print axioms probeRelationHomeo_face
end CMDG.CondensedCM5R0.CompactCover.Dyadic
