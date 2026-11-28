import CMDGCondensedCM4P3DerivedCM5R0CompactProductContinuity

/-! Actual morphisms of compact-cover resolutions and Yoneda
naturality on their syzygy towers. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.CompactCover
variable {P Q : Profinite.{u}} {T U : CompHaus.{u}}
  {p : profiniteToCompHaus.obj P ⟶ T} {q : profiniteToCompHaus.obj Q ⟶ U}

structure CoverMap (p : profiniteToCompHaus.obj P ⟶ T)
    (q : profiniteToCompHaus.obj Q ⟶ U) where
  src : P ⟶ Q
  tgt : T ⟶ U
  square : profiniteToCompHaus.map src ≫ q = p ≫ tgt

namespace CoverMap
variable (a : CoverMap p q)

def rel (n : ℕ) : compactRelationProfinite P T p n ⟶ compactRelationProfinite Q U q n := by
  letI : CompactSpace (↥(compactCechArityRelatedSet n P T p)) :=
    isCompact_iff_compactSpace.mp (compactCechArityRelatedSet_isClosed n P T p).isCompact
  letI : CompactSpace (↥(compactCechArityRelatedSet n Q U q)) :=
    isCompact_iff_compactSpace.mp (compactCechArityRelatedSet_isClosed n Q U q).isCompact
  refine CompHausLike.ofHom _ (⟨fun z => ⟨fun j => a.src.hom.hom (z.val j),by
    intro j
    have h (x : P) := congrArg (fun f : profiniteToCompHaus.obj P ⟶ U => f.hom.hom x) a.square
    change q.hom.hom (a.src.hom.hom (z.val j)) = q.hom.hom (a.src.hom.hom (z.val 0))
    rw [show q.hom.hom (a.src.hom.hom (z.val j)) = a.tgt.hom.hom (p.hom.hom (z.val j)) from h _,
      show q.hom.hom (a.src.hom.hom (z.val 0)) = a.tgt.hom.hom (p.hom.hom (z.val 0)) from h _,
      z.property j]⟩,
    ?_⟩)
  apply Continuous.subtype_mk
  apply continuous_pi
  intro j
  exact a.src.hom.hom.continuous.comp ((continuous_apply j).comp continuous_subtype_val)

theorem rel_face (n : ℕ) (k : Fin (n+2)) :
    compactRelationFace P T p n k ≫ a.rel n =
      a.rel (n+1) ≫ compactRelationFace Q U q n k := by
  apply ConcreteCategory.hom_ext
  intro z
  apply Subtype.ext
  rfl

abbrev tm (n : ℕ) : term P T p n ⟶ term Q U q n :=
  (Condensed.profiniteFree Coeff).map (a.rel n)
abbrev tg : compactFreeFunctor.obj T ⟶ compactFreeFunctor.obj U :=
  compactFreeFunctor.map a.tgt

theorem d_square (n : ℕ) : d P T p n ≫ a.tm n = a.tm (n+1) ≫ d Q U q n := by
  unfold d compactFreeRelationBoundary
  rw [Preadditive.sum_comp,Preadditive.comp_sum]
  apply Finset.sum_congr rfl
  intro k hk
  rw [Preadditive.zsmul_comp,Preadditive.comp_zsmul,← Functor.map_comp,← Functor.map_comp,a.rel_face]

theorem aug_square : aug P T p ≫ a.tg = a.tm 0 ≫ aug Q U q := by
  change compactFreeFunctor.map (compactRelationAugMap P T p) ≫ compactFreeFunctor.map a.tgt =
    compactFreeFunctor.map (profiniteToCompHaus.map (a.rel 0)) ≫
      compactFreeFunctor.map (compactRelationAugMap Q U q)
  rw [← Functor.map_comp,← Functor.map_comp]
  congr 1
  apply ConcreteCategory.hom_ext
  intro z
  exact (congrArg (fun f : profiniteToCompHaus.obj P ⟶ U => f.hom.hom (z.val 0)) a.square).symm

def km : (n : ℕ) → syzygy P T p n ⟶ syzygy Q U q n
  | 0 => kernel.lift (aug Q U q) (syzygyι P T p 0 ≫ a.tm 0) (by
      rw [Category.assoc,← a.aug_square,← Category.assoc]
      rw [show syzygyι P T p 0 ≫ aug P T p = 0 from kernel.condition _,zero_comp])
  | n+1 => kernel.lift (d Q U q n) (syzygyι P T p (n+1) ≫ a.tm (n+1)) (by
      rw [Category.assoc,← a.d_square,← Category.assoc]
      rw [show syzygyι P T p (n+1) ≫ d P T p n = 0 from kernel.condition _,zero_comp])

theorem km_i (n : ℕ) : a.km n ≫ syzygyι Q U q n = syzygyι P T p n ≫ a.tm n := by
  cases n <;> exact kernel.lift_ι _ _ _

theorem cover_square (n : ℕ) :
    syzygyCover P T p n ≫ a.km n = a.tm (n+1) ≫ syzygyCover Q U q n := by
  letI := syzygyι_mono Q U q n
  apply (cancel_mono (syzygyι Q U q n)).1
  rw [Category.assoc,a.km_i,← Category.assoc,cover_comp_ι,Category.assoc,cover_comp_ι,a.d_square]

abbrev towerMap : (n : ℕ) → towerObj P T p n ⟶ towerObj Q U q n
  | 0 => a.tg
  | n+1 => a.km n

theorem tower_square (n : ℕ) :
    towerProjection P T p n ≫ a.towerMap n = a.tm n ≫ towerProjection Q U q n := by
  cases n with
  | zero => exact a.aug_square
  | succ n => exact a.cover_square n

def seqMap (n : ℕ) : towerSeq P T p n ⟶ towerSeq Q U q n :=
  ShortComplex.Hom.mk (a.km n) (a.tm n) (a.towerMap n)
    (a.km_i n) (a.tower_square n).symm

variable [Epi p] [Epi q]
abbrev pre (n r : ℕ) :
    Abelian.Ext (towerObj Q U q n) discreteIntegerCoeff r →+
      Abelian.Ext (towerObj P T p n) discreteIntegerCoeff r :=
  (Abelian.Ext.mk₀ (a.towerMap n)).precomp _ (zero_add r)

theorem connecting_natural (n r : ℕ)
    (e : Abelian.Ext (syzygy Q U q n) discreteIntegerCoeff r) :
    connecting P T p n r (a.pre (n+1) r e) =
      a.pre n (r+1) (connecting Q U q n r e) := by
  change (tower_shortExact P T p n).extClass.comp
      ((Abelian.Ext.mk₀ (a.km n)).comp e (zero_add r)) (by omega : 1+r=r+1) =
    (Abelian.Ext.mk₀ (a.towerMap n)).comp ((tower_shortExact Q U q n).extClass.comp e (by omega : 1+r=r+1)) (zero_add (r+1))
  have h := ShortComplex.ShortExact.extClass_naturality
    (tower_shortExact P T p n) (tower_shortExact Q U q n) (a.seqMap n)
  change (tower_shortExact P T p n).extClass.comp (Abelian.Ext.mk₀ (a.km n)) (add_zero 1) =
    (Abelian.Ext.mk₀ (a.towerMap n)).comp (tower_shortExact Q U q n).extClass (zero_add 1) at h
  rw [← Abelian.Ext.comp_assoc _ _ _ (add_zero 1) (zero_add r) (by omega : 1+0+r=r+1), h,
    Abelian.Ext.comp_assoc] <;> omega

#print axioms seqMap
#print axioms connecting_natural
end CoverMap
end CMDG.CondensedCM5R0.CompactCover
