import CMDGCondensedCM4P3DerivedCM5R0CompactBoxProbeCover

/-! Relative compact-box acyclicity after product with a profinite probe.
The compact-fiber slice is locally constant as an entire cochain;
therefore a choice of primitive per cocycle gives a jointly locally
constant primitive on the genuine probe relation. -/
noncomputable section
universe u
open Set CategoryTheory
namespace CMDG.CondensedCM5R0.CompactCover.Dyadic

variable (S : Profinite.{u}) (I : Type u)

abbrev cubeDiff (n : ℕ) :=
  compactCategoricalRelationScalarDifferential (cubeP I) (cubeT I) (cubeCover I) n
abbrev probeDiff (n : ℕ) :=
  compactCategoricalRelationScalarDifferential (probeP S I) (probeT S I) (probeCover S I) n

def probeSlice (n : ℕ) (c : LocallyConstant (ProbeRel S I n) ℤ) (s : S) :
    LocallyConstant (Rel I n) ℤ :=
  slice (c.comap ⟨(probeRelationHomeo S I n).symm,
    (probeRelationHomeo S I n).symm.continuous⟩) s

theorem probeSlice_diff (n : ℕ) (c : LocallyConstant (ProbeRel S I n) ℤ) (s : S) :
    probeSlice S I (n+1) (probeDiff S I n c) s =
      cubeDiff I n (probeSlice S I n c s) := by
  ext r
  change probeDiff S I n c ((probeRelationHomeo S I (n+1)).symm (s,r)) =
    cubeDiff I n (probeSlice S I n c s) r
  rw [compactCategoricalRelationScalarDifferential_apply,
    compactCategoricalRelationScalarDifferential_apply]
  apply Finset.sum_congr rfl
  intro k hk
  change (-1 : ℤ) ^ (k : ℕ) *
    c (probeFace S I n k ((probeRelationHomeo S I (n+1)).symm (s,r))) =
    (-1 : ℤ) ^ (k : ℕ) *
    c ((probeRelationHomeo S I n).symm (s,cubeFace I n k r))
  rw [probeRelationHomeo_symm_face]

theorem probeSlice_zero (n : ℕ) (s : S) :
    probeSlice S I n (0 : LocallyConstant (ProbeRel S I n) ℤ) s = 0 := by
  ext r
  rfl

def primitiveChoice (n : ℕ) (c : LocallyConstant (Rel I (n+1)) ℤ) :
    LocallyConstant (Rel I n) ℤ := by
  classical
  exact if h : cubeDiff I (n+1) c = 0 then
    Classical.choose (cube_scalarExact I n c h) else 0

theorem primitiveChoice_diff (n : ℕ) (c : LocallyConstant (Rel I (n+1)) ℤ)
    (hc : cubeDiff I (n+1) c = 0) :
    cubeDiff I n (primitiveChoice I n c) = c := by
  classical
  unfold primitiveChoice
  rw [dif_pos hc]
  exact Classical.choose_spec (cube_scalarExact I n c hc)

def probeGlue (n : ℕ) (B : LocallyConstant S (LocallyConstant (Rel I n) ℤ)) :
    LocallyConstant (ProbeRel S I n) ℤ :=
  (unslice B).comap ⟨probeRelationHomeo S I n,(probeRelationHomeo S I n).continuous⟩

theorem probeSlice_apply (n : ℕ) (c : LocallyConstant (ProbeRel S I n) ℤ)
    (s : S) (r : Rel I n) :
    probeSlice S I n c s r = c ((probeRelationHomeo S I n).symm (s,r)) := rfl

theorem probeGlue_apply (n : ℕ) (B : LocallyConstant S (LocallyConstant (Rel I n) ℤ))
    (z : ProbeRel S I n) :
    probeGlue S I n B z = B (probeRelationHomeo S I n z).1 (probeRelationHomeo S I n z).2 := rfl

theorem probeSlice_glue (n : ℕ) (B : LocallyConstant S (LocallyConstant (Rel I n) ℤ))
    (s : S) :
    probeSlice S I n (probeGlue S I n B) s = B s := by
  ext r
  rw [probeSlice_apply,probeGlue_apply]
  have h : probeRelationHomeo S I n ((probeRelationHomeo S I n).symm (s,r)) = (s,r) :=
    (probeRelationHomeo S I n).apply_symm_apply (s,r)
  rw [h]

theorem probeSlice_injective (n : ℕ) :
    Function.Injective (probeSlice S I n) := by
  intro a b h
  ext z
  obtain ⟨⟨s,r⟩,rfl⟩ := (probeRelationHomeo S I n).symm.surjective z
  exact congrFun (congrArg DFunLike.coe (congrFun h s)) r

theorem probeSlice_locallyConstant (n : ℕ)
    (c : LocallyConstant (ProbeRel S I n) ℤ) :
    IsLocallyConstant (probeSlice S I n c) :=
  slice_locallyConstant (c.comap ⟨(probeRelationHomeo S I n).symm,
        (probeRelationHomeo S I n).symm.continuous⟩)

def probePrimitive (n : ℕ) (c : LocallyConstant (ProbeRel S I (n+1)) ℤ) :
    LocallyConstant S (LocallyConstant (Rel I n) ℤ) :=
  ⟨fun s => primitiveChoice I n (probeSlice S I (n+1) c s),
    (probeSlice_locallyConstant S I (n+1) c).comp (primitiveChoice I n)⟩

theorem probePrimitive_closed (n : ℕ) (c : LocallyConstant (ProbeRel S I (n+1)) ℤ)
    (hc : probeDiff S I (n+1) c = 0) (s : S) :
    cubeDiff I n (probePrimitive S I n c s) = probeSlice S I (n+1) c s := by
  have hz : probeSlice S I (n+2) (probeDiff S I (n+1) c) s = 0 := by
    rw [hc,probeSlice_zero]
  have hclosed : cubeDiff I (n+1) (probeSlice S I (n+1) c s) = 0 :=
    (probeSlice_diff S I (n+1) c s).symm.trans hz
  exact primitiveChoice_diff I n _ hclosed

theorem probe_scalarExact :
    scalarExact (probeP S I) (probeT S I) (probeCover S I) := by
  intro n c hc
  refine ⟨probeGlue S I n (probePrimitive S I n c),?_⟩
  apply probeSlice_injective S I (n+1)
  funext s
  change probeSlice S I (n+1) (probeDiff S I n (probeGlue S I n
    (probePrimitive S I n c))) s = probeSlice S I (n+1) c s
  rw [probeSlice_diff,probeSlice_glue]
  exact probePrimitive_closed S I n c hc s

theorem probe_cube_extPositive_zero (q : ℕ)
    (e : Abelian.Ext (compactFreeFunctor.obj (probeT S I)) discreteIntegerCoeff (q+1)) :
    e = 0 := by
  letI := probeCover_epi S I
  exact compactFree_extPositive_zero_of_scalarExact
    (probeP S I) (probeT S I) (probeCover S I) (probe_scalarExact S I) q e

def probeBoxT (a b : I → ℝ) : CompHaus.{u} :=
  CompHaus.of (S × (∀ i, Set.Icc (a i) (b i)))

def probeBoxProjection (a b : I → ℝ) (h : ∀ i, a i ≤ b i) :
    probeT S I ⟶ probeBoxT S I a b :=
  CompHausLike.ofHom _ (⟨fun x => (x.1,fun i => affine (a i) (b i) (h i) (x.2 i)),
    continuous_fst.prodMk (continuous_pi fun i =>
      (affine (a i) (b i) (h i)).continuous.comp ((continuous_apply i).comp continuous_snd))⟩ :
    C((S × (I → Interval)),(S × (∀ i, Set.Icc (a i) (b i)))))

def probeBoxSection (a b : I → ℝ) (h : ∀ i, a i ≤ b i) :
    probeBoxT S I a b ⟶ probeT S I :=
  CompHausLike.ofHom _ (⟨fun x => (x.1,fun i => affineSection (a i) (b i) (h i) (x.2 i)),
    continuous_fst.prodMk (continuous_pi fun i =>
      (affineSection (a i) (b i) (h i)).continuous.comp ((continuous_apply i).comp continuous_snd))⟩ :
    C((S × (∀ i, Set.Icc (a i) (b i))),(S × (I → Interval))))

theorem probeBoxSection_projection (a b : I → ℝ) (h : ∀ i, a i ≤ b i) :
    probeBoxSection S I a b h ≫ probeBoxProjection S I a b h = 𝟙 (probeBoxT S I a b) := by
  apply CategoryTheory.ConcreteCategory.hom_ext
  intro x
  apply Prod.ext
  · rfl
  · funext i
    exact affineSection_rightInverse (a i) (b i) (h i) (x.2 i)

/-- Actual compact boxes tested after product with an arbitrary profinite
probe, in every positive Ext degree. Includes Stonean probes and
degenerate intervals. -/
theorem probe_box_extPositive_zero (a b : I → ℝ) (h : ∀ i, a i ≤ b i) (q : ℕ)
    (e : Abelian.Ext (compactFreeFunctor.obj (probeBoxT S I a b)) discreteIntegerCoeff (q+1)) :
    e=0 := by
  apply ext_zero_of_retract (compactFreeFunctor.map (probeBoxSection S I a b h))
    (compactFreeFunctor.map (probeBoxProjection S I a b h)) _ q
    (probe_cube_extPositive_zero S I q) e
  rw [← Functor.map_comp,probeBoxSection_projection]
  exact compactFreeFunctor.map_id _

#print axioms probe_scalarExact
#print axioms probe_cube_extPositive_zero
#print axioms probe_box_extPositive_zero
end CMDG.CondensedCM5R0.CompactCover.Dyadic
