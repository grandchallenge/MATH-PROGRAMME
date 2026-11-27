import CMDGCondensedCM4P3DerivedCM5R0CompactBoxAcyclic

/-! Locally constant families of entire compact-fiber cochains.
The tube lemma gives local constancy uniformly over the fiber,
so choosing a primitive for each cochain preserves local constancy. -/
noncomputable section
universe u v w
open Set CategoryTheory
namespace CMDG.CondensedCM5R0.CompactCover.Dyadic

section Slices
variable {S : Type u} {R : Type v} {A : Type w}
  [TopologicalSpace S] [TopologicalSpace R]

def slice (c : LocallyConstant (S × R) A) (s : S) : LocallyConstant R A :=
  c.comap ⟨fun r => (s,r),continuous_const.prodMk continuous_id⟩

theorem slice_apply (c : LocallyConstant (S × R) A) (s : S) (r : R) :
    slice c s r = c (s,r) := rfl

theorem slice_locallyConstant [CompactSpace R] (c : LocallyConstant (S × R) A) :
    IsLocallyConstant (slice c) := by
  apply (IsLocallyConstant.iff_exists_open _).2
  intro s
  let W : Set (S × R) := {z | c z = c (s,z.2)}
  have hw : IsOpen W := by
    have h₁ := c.isLocallyConstant
    have h₂ := (slice c s).isLocallyConstant.comp_continuous
      (continuous_snd : Continuous (Prod.snd : S × R → R))
    exact (h₁.prodMk h₂) {p : A × A | p.1 = p.2}
  have hsub : ({s} : Set S) ×ˢ (Set.univ : Set R) ⊆ W := by
    intro z hz
    have h : z.1 = s := hz.1
    change c z = c (s,z.2)
    exact congrArg c (Prod.ext h rfl)
  obtain ⟨U,V,hU,hV,hs,hall,hUV⟩ :=
    generalized_tube_lemma (isCompact_singleton (x:=s)) isCompact_univ hw hsub
  refine ⟨U,hU,hs rfl,?_⟩
  intro s' hs'
  ext r
  exact hUV ⟨hs',hall (Set.mem_univ r)⟩

def unslice (b : LocallyConstant S (LocallyConstant R A)) :
    LocallyConstant (S × R) A := by
  refine ⟨fun z => b z.1 z.2, ?_⟩
  apply (IsLocallyConstant.iff_exists_open _).2
  intro z
  obtain ⟨U,hU,hzU,hu⟩ := b.isLocallyConstant.exists_open z.1
  obtain ⟨V,hV,hzV,hv⟩ := (b z.1).isLocallyConstant.exists_open z.2
  refine ⟨U ×ˢ V,hU.prod hV,⟨hzU,hzV⟩,?_⟩
  intro z' hz'
  change b z'.1 z'.2 = b z.1 z.2
  have h : b z'.1 = b z.1 := hu z'.1 hz'.1
  rw [h]
  exact hv z'.2 hz'.2

end Slices

#print axioms slice_locallyConstant
#print axioms unslice
end CMDG.CondensedCM5R0.CompactCover.Dyadic
