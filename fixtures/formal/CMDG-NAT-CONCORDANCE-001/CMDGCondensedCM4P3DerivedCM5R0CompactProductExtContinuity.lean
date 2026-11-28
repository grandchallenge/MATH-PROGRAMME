import CMDGCondensedCM4P3DerivedCM5R0CompactCoverNaturality
import CMDGCondensedCM4P3DerivedCM5R0CompactBoxProjectionHom

/-! Finite-coordinate descent of genuine Ext classes. Iterating the
natural connecting maps avoids any noncanonical cohomology-class
identification or exchange of limits with Ext. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.CompactCover.ProductContinuity
open CompactCover
variable {I : Type u} (P : I → Profinite.{u}) (T : I → CompHaus.{u})
  (p : ∀ i, profiniteToCompHaus.obj (P i) ⟶ T i)

variable (F : Finset I)
abbrev PP := prodP P
abbrev TT := prodT T
abbrev pc := prodCover P T p
abbrev PF := prodP (subP P F)
abbrev TF := prodT (subT T F)
abbrev fc := prodCover (subP P F) (subT T F) (subCover P T p F)

def projection : CoverMap (pc P T p) (fc P T p F) where
  src := CompHausLike.ofHom _ (restrictCoordinates F)
  tgt := CompHausLike.ofHom _ (restrictCoordinates F)
  square := by
    apply ConcreteCategory.hom_ext
    intro x
    rfl

theorem projection_rel (n : ℕ) :
    ((projection P T p F).rel n).hom.hom = restrictRel P T p F n := by
  apply ContinuousMap.ext
  intro z
  apply Subtype.ext
  rfl

theorem scalar_precomp (n : ℕ)
    (g : term (PF P F) (TF T F) (fc P T p F) n ⟶ discreteIntegerCoeff) :
    scalarAddEquiv (PP P) (TT T) (pc P T p) n ((projection P T p F).tm n ≫ g) =
      pull P T p F n (scalarAddEquiv (PF P F) (TF T F) (fc P T p F) n g) := by
  change freeProfiniteDiscreteIntegerHomScalarEquiv _
    ((Condensed.profiniteFree Coeff).map ((projection P T p F).rel n) ≫ g) =
    (freeProfiniteDiscreteIntegerHomScalarEquiv _ g).comap (restrictRel P T p F n)
  rw [freeProfiniteDiscreteIntegerHomScalarEquiv_precomp,projection_rel]

def targetSection (x : ∀ i, T i) : TF T F ⟶ TT T :=
  CompHausLike.ofHom _ (extendCoordinates F x)

theorem targetSection_projection (x : ∀ i, T i) :
    targetSection T F x ≫ (projection P T p F).tgt = 𝟙 _ := by
  apply ConcreteCategory.hom_ext
  intro z
  funext i
  classical
  change (if h : i.val ∈ F then z ⟨i.val,h⟩ else x i.val) = z i
  rw [dif_pos i.property]

theorem projection_ext_injective (x : ∀ i, T i) (r : ℕ) :
    Function.Injective (fun e : Abelian.Ext (compactFreeFunctor.obj (TF T F)) discreteIntegerCoeff r =>
      (Abelian.Ext.mk₀ ((projection P T p F).tg)).comp e (zero_add r)) := by
  intro a b h
  have hh := congrArg (fun e => (Abelian.Ext.mk₀ (compactFreeFunctor.map (targetSection T F x))).comp e (zero_add r)) h
  change (Abelian.Ext.mk₀ (compactFreeFunctor.map (targetSection T F x))).comp
    ((Abelian.Ext.mk₀ ((projection P T p F).tg)).comp a (zero_add r)) (zero_add r) =
      (Abelian.Ext.mk₀ (compactFreeFunctor.map (targetSection T F x))).comp
    ((Abelian.Ext.mk₀ ((projection P T p F).tg)).comp b (zero_add r)) (zero_add r) at hh
  simpa only [← Abelian.Ext.comp_assoc_of_second_deg_zero,Abelian.Ext.mk₀_comp_mk₀,
    ← Functor.map_comp,targetSection_projection,compactFreeFunctor.map_id,Abelian.Ext.mk₀_id_comp] using hh

theorem hom_finiteSupport (x : ∀ i, T i)
    (g : compactFreeFunctor.obj (TT T) ⟶ discreteIntegerCoeff) :
    ∃ F : Finset I, ∃ b : compactFreeFunctor.obj (TF T F) ⟶ discreteIntegerCoeff,
      (projection P T p F).tg ≫ b = g := by
  let c := Dyadic.compactIntegerHom (TT T) g
  obtain ⟨G,b,hb⟩ := finiteCoordinateFactor c x
  refine ⟨G,(Dyadic.compactIntegerHom (TF T G)).symm b,?_⟩
  apply (Dyadic.compactIntegerHom (TT T)).injective
  rw [Dyadic.compactIntegerHom_precomp,Equiv.apply_symm_apply]
  exact hb

variable [∀ i, Epi (p i)]
local instance fullEpi : Epi (pc P T p) := prodCover_epi P T p inferInstance
local instance finiteEpi : Epi (fc P T p F) :=
  prodCover_epi (subP P F) (subT T F) (subCover P T p F) (fun _i => inferInstance)

theorem syzygy_hom_finiteSupport (x : ∀ i, P i) (n : ℕ)
    (g : syzygy (PP P) (TT T) (pc P T p) n ⟶ discreteIntegerCoeff) :
    ∃ F : Finset I,
      ∃ h : syzygy (PF P F) (TF T F) (fc P T p F) n ⟶ discreteIntegerCoeff,
        (projection P T p F).km n ≫ h = g := by
  let c := scalarFromSyzygy (PP P) (TT T) (pc P T p) n g
  obtain ⟨G,b,hb,hpull⟩ := cocycle_finiteSupport P T p x n c.val c.property
  obtain ⟨h,hh⟩ := (scalarFromSyzygy_bijective (PF P G) (TF T G) (fc P T p G) n).2
    (⟨b,hb⟩ : scalarCocycles (PF P G) (TF T G) (fc P T p G) n)
  refine ⟨G,h,?_⟩
  letI := cover_epi (PP P) (TT T) (pc P T p) n
  apply (cancel_epi (syzygyCover (PP P) (TT T) (pc P T p) n)).1
  apply (scalarAddEquiv (PP P) (TT T) (pc P T p) (n+1)).injective
  rw [← Category.assoc,(projection P T p G).cover_square,Category.assoc,scalar_precomp]
  change pull P T p G (n+1) (scalarFromSyzygy (PF P G) (TF T G) (fc P T p G) n h).val = c.val
  rw [hh]
  exact hpull

theorem syzygy_ext_finiteSupport (x : ∀ i, P i) (r n : ℕ)
    (e : Abelian.Ext (syzygy (PP P) (TT T) (pc P T p) n) discreteIntegerCoeff r) :
    ∃ F : Finset I,
      ∃ b : Abelian.Ext (syzygy (PF P F) (TF T F) (fc P T p F) n) discreteIntegerCoeff r,
        (projection P T p F).pre (n+1) r b = e := by
  induction r generalizing n with
  | zero =>
    obtain ⟨G,h,hh⟩ := syzygy_hom_finiteSupport P T p x n (Abelian.Ext.addEquiv₀ e)
    refine ⟨G,Abelian.Ext.mk₀ h,?_⟩
    change (Abelian.Ext.mk₀ ((projection P T p G).km n)).comp (Abelian.Ext.mk₀ h) (zero_add 0) = e
    rw [Abelian.Ext.mk₀_comp_mk₀,hh,Abelian.Ext.mk₀_addEquiv₀_apply]
  | succ r ih =>
    obtain ⟨b,hb⟩ := connecting_surj (PP P) (TT T) (pc P T p) (n+1) r e
    obtain ⟨G,c,hc⟩ := ih (n+1) b
    refine ⟨G,connecting (PF P G) (TF T G) (fc P T p G) (n+1) r c,?_⟩
    rw [← (projection P T p G).connecting_natural (n+1) r c,hc,hb]

theorem extPositive_finiteSupport (x : ∀ i, P i) (r : ℕ)
    (e : Abelian.Ext (compactFreeFunctor.obj (TT T)) discreteIntegerCoeff (r+1)) :
    ∃ F : Finset I,
      ∃ b : Abelian.Ext (compactFreeFunctor.obj (TF T F)) discreteIntegerCoeff (r+1),
        (Abelian.Ext.mk₀ ((projection P T p F).tg)).comp b (zero_add (r+1)) = e := by
  obtain ⟨b,hb⟩ := connecting_surj (PP P) (TT T) (pc P T p) 0 r e
  obtain ⟨G,c,hc⟩ := syzygy_ext_finiteSupport P T p x r 0 b
  refine ⟨G,connecting (PF P G) (TF T G) (fc P T p G) 0 r c,?_⟩
  change (projection P T p G).pre 0 (r+1) _ = _
  rw [← (projection P T p G).connecting_natural 0 r c,hc,hb]

theorem ext_finiteSupport (x : ∀ i, P i) (r : ℕ)
    (e : Abelian.Ext (compactFreeFunctor.obj (TT T)) discreteIntegerCoeff r) :
    ∃ F : Finset I,
      ∃ b : Abelian.Ext (compactFreeFunctor.obj (TF T F)) discreteIntegerCoeff r,
        (Abelian.Ext.mk₀ ((projection P T p F).tg)).comp b (zero_add r) = e := by
  cases r with
  | zero =>
    obtain ⟨G,b,hb⟩ := hom_finiteSupport P T p (fun i => (p i).hom.hom (x i)) (Abelian.Ext.addEquiv₀ e)
    refine ⟨G,Abelian.Ext.mk₀ b,?_⟩
    rw [Abelian.Ext.mk₀_comp_mk₀,hb,Abelian.Ext.mk₀_addEquiv₀_apply]
  | succ r => exact extPositive_finiteSupport P T p x r e

#print axioms projection_ext_injective
#print axioms ext_finiteSupport
#print axioms syzygy_hom_finiteSupport
#print axioms extPositive_finiteSupport
end CMDG.CondensedCM5R0.CompactCover.ProductContinuity
