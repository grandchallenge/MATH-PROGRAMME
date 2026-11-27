import CMDGCondensedCM4P3DerivedCM5R0DyadicProductNerve

/-! Every genuine scalar relation cochain factors through one finite
selection of axes and a common prefix length. This uses extension
from the closed relation into the full profinite tuple product. -/
noncomputable section
universe u
open Set CategoryTheory
namespace CMDG.CondensedCM5R0.CompactCover.Dyadic
open OrderedGrid
variable {I : Type u}

def curryBits (n : ℕ) :
    ((Fin (n+1) × (I × ℕ)) → Fin 2) ≃ₜ
      (Fin (n+1) → I → Bits) :=
  (Homeomorph.piCurry).trans (Homeomorph.piCongrRight fun _ => Homeomorph.piCurry)

theorem observation_factors (n : ℕ) (c : LocallyConstant (Rel I n) ℤ) :
    ∃ (F : Finset I) (m : ℕ), ∀ x y : Rel I n,
      observe F m n x = observe F m n y → c x = c y := by
  classical
  let Q : Profinite.{u} := Profinite.of (Fin (n+1) → I → Bits)
  let U : Set Q := compactCechArityRelatedSet n (cubeP I) (cubeT I) (cubeCover I)
  have hU : IsClosed U := compactCechArityRelatedSet_isClosed n _ _ _
  obtain ⟨g,hg⟩ := locallyConstant_extend_closed_subset Q U hU c
  let h := curryBits (I:=I) n
  let g' : LocallyConstant ((Fin (n+1) × (I × ℕ)) → Fin 2) ℤ :=
    g.comap ⟨h,h.continuous⟩
  obtain ⟨S,hS⟩ := finiteCoordinateSupport g'
  let F : Finset I := S.image fun t => t.2.1
  let m : ℕ := S.sup fun t => t.2.2+1
  refine ⟨F,m,?_⟩
  intro x y hxy
  have hbits : ∀ t ∈ S, h.symm x.val t = h.symm y.val t := by
    intro t ht
    have hi : t.2.1 ∈ F := Finset.mem_image_of_mem _ ht
    have hj : t.2.2 < m := by
      have hle : t.2.2+1 ≤ m := Finset.le_sup (f:=fun t => t.2.2+1) ht
      omega
    have he := congrFun (congrFun hxy t.1) (⟨t.2.1,hi⟩ : ↥F)
    change prefixIndex m (x.val t.1 t.2.1) = prefixIndex m (y.val t.1 t.2.1) at he
    change x.val t.1 t.2.1 t.2.2 = y.val t.1 t.2.1 t.2.2
    exact prefix_injective_on_digits m _ _ he _ hj
  have hval := hS (h.symm x.val) (h.symm y.val) hbits
  change g (h (h.symm x.val)) = g (h (h.symm y.val)) at hval
  have hxg : g (h (h.symm x.val)) = g x.val :=
    congrArg g (h.apply_symm_apply x.val)
  have hyg : g (h (h.symm y.val)) = g y.val :=
    congrArg g (h.apply_symm_apply y.val)
  exact (hg x).symm.trans (hxg.symm.trans (hval.trans (hyg.trans (hg y))))

/-- Lift every admissible list at the specified degree. -/
theorem observation_list_surj (F : Finset I) (m n : ℕ)
    (xs : List (Vertex (↥F))) (hx : valid (2^m-1) xs) (hl : xs.length = n+1) :
    ∃ z : Rel I n, observeList F m n z = xs := by
  let t : Fin (n+1) → Vertex (↥F) := fun i => xs.get (Fin.cast hl.symm i)
  have ht : List.ofFn t = xs := by
    rw [← List.ofFn_get xs]
    exact List.ofFn_congr hl.symm _
  obtain ⟨z,hz⟩ := observe_surj_valid F m n t (by rw [ht]; exact hx)
  exact ⟨z,by rw [observeList,hz,ht]⟩

/-- Descend along the actual image; arbitrary unused ambient list values
are set to zero and never enter the valid-tuple calculation. -/
def descend (F : Finset I) (m n : ℕ) (c : LocallyConstant (Rel I n) ℤ)
    (xs : List (Vertex (↥F))) : ℤ := by
  classical
  exact if h : ∃ z : Rel I n, observeList F m n z = xs then c (Classical.choose h) else 0

theorem descend_observe (F : Finset I) (m n : ℕ) (c : LocallyConstant (Rel I n) ℤ)
    (hc : ∀ x y : Rel I n, observe F m n x = observe F m n y → c x = c y)
    (z : Rel I n) : descend F m n c (observeList F m n z) = c z := by
  classical
  have h : ∃ w : Rel I n, observeList F m n w = observeList F m n z := ⟨z,rfl⟩
  unfold descend
  rw [dif_pos h]
  apply hc
  exact List.ofFn_injective (Classical.choose_spec h)

/-- Any integer function on observed ordered lists pulls back to a
locally constant function because the selected coordinate set is finite. -/
def pull (F : Finset I) (m n : ℕ) (b : List (Vertex (↥F)) → ℤ) :
    LocallyConstant (Rel I n) ℤ :=
  ⟨fun z => b (observeList F m n z),
    (IsLocallyConstant.of_discrete (fun t : Fin (n+1) → Vertex (↥F) => b (List.ofFn t))).comp_continuous
      (observe_continuous F m n)⟩

theorem differential_pull (F : Finset I) (m n : ℕ)
    (b : List (Vertex (↥F)) → ℤ) (z : Rel I (n+1)) :
    compactCategoricalRelationScalarDifferential (cubeP I) (cubeT I) (cubeCover I) n
      (pull F m n b) z = D b (observeList F m (n+1) z) := by
  rw [compactCategoricalRelationScalarDifferential_apply,observeList,D_ofFn]
  apply Finset.sum_congr rfl
  intro k hk
  change (-1 : ℤ) ^ (k : ℕ) * b (List.ofFn (observe F m n
      ((compactRelationFace (cubeP I) (cubeT I) (cubeCover I) n k).hom.hom z))) = _
  rw [observe_face]

#print axioms observation_factors
#print axioms observation_list_surj
#print axioms descend_observe
#print axioms differential_pull
end CMDG.CondensedCM5R0.CompactCover.Dyadic
