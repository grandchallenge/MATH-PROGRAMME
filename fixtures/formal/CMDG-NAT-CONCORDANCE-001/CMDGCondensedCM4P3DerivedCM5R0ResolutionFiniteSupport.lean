import CMDGCondensedCM4P3DerivedCM5R0CirclePowerExtContinuity
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneUniversalTransport

/-! All-degree finite-support transfer through an actual exact
augmented resolution, using natural Yoneda connecting maps.
No acyclicity of the resolution terms is required. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.AcyclicResolution

structure Endo (R : Resolution.{u}) where
  tgt : R.target ⟶ R.target
  tm : ∀ n, R.term n ⟶ R.term n
  aug_comm : R.aug ≫ tgt = tm 0 ≫ R.aug
  d_comm : ∀ n, R.d n ≫ tm n = tm (n+1) ≫ R.d n

variable {R : Resolution.{u}}
namespace Endo
variable (a : Endo R)
def km : (n : ℕ) → syzygy R n ⟶ syzygy R n
  | 0 => kernel.lift R.aug (inclusion R 0 ≫ a.tm 0) (by
      rw [Category.assoc,← a.aug_comm,← Category.assoc]
      rw [show inclusion R 0 ≫ R.aug = 0 from kernel.condition _,zero_comp])
  | n+1 => kernel.lift (R.d n) (inclusion R (n+1) ≫ a.tm (n+1)) (by
      rw [Category.assoc,← a.d_comm,← Category.assoc]
      rw [show inclusion R (n+1) ≫ R.d n = 0 from kernel.condition _,zero_comp])

theorem km_i (n : ℕ) : a.km n ≫ inclusion R n = inclusion R n ≫ a.tm n := by
  cases n <;> exact kernel.lift_ι _ _ _

theorem cover_comm (n : ℕ) :
    cover R n ≫ a.km n = a.tm (n+1) ≫ cover R n := by
  letI := inclusion_mono R n
  apply (cancel_mono (inclusion R n)).1
  rw [Category.assoc,a.km_i,← Category.assoc,cover_inclusion,Category.assoc,cover_inclusion,a.d_comm]
end Endo

abbrev tower (R : Resolution.{u}) : ℕ → Ambient.{u}
  | 0 => R.target
  | n+1 => syzygy R n

def towerCover (R : Resolution.{u}) : (n : ℕ) → R.term n ⟶ tower R n
  | 0 => R.aug
  | n+1 => cover R n

theorem towerCover_epi (R : Resolution.{u}) (n : ℕ) : Epi (towerCover R n) := by
  cases n with
  | zero => exact R.aug_epi
  | succ n => exact cover_epi R n

abbrev seq (R : Resolution.{u}) (n : ℕ) : ShortComplex Ambient.{u} :=
  ShortComplex.mk (inclusion R n) (towerCover R n) (by
    cases n with
    | zero => exact kernel.condition R.aug
    | succ n => exact inclusion_cover_zero R n)

theorem seq_shortExact (R : Resolution.{u}) (n : ℕ) : (seq R n).ShortExact := by
  cases n with
  | zero => exact aug_shortExact R
  | succ n => exact syzygy_shortExact R n

namespace Endo
variable (a : Endo R)
abbrev tw : (n : ℕ) → tower R n ⟶ tower R n
  | 0 => a.tgt
  | n+1 => a.km n

theorem tower_comm (n : ℕ) : towerCover R n ≫ a.tw n = a.tm n ≫ towerCover R n := by
  cases n with
  | zero => exact a.aug_comm
  | succ n => exact a.cover_comm n

def seqMap (n : ℕ) : seq R n ⟶ seq R n :=
  ShortComplex.Hom.mk (a.km n) (a.tm n) (a.tw n) (a.km_i n) (a.tower_comm n).symm
end Endo

variable (Y : Ambient.{u})
abbrev pb {X Z : Ambient.{u}} (f : X ⟶ Z) (q : ℕ) :
    Abelian.Ext Z Y q →+ Abelian.Ext X Y q :=
  (Abelian.Ext.mk₀ f).precomp Y (zero_add q)

theorem pb_comp {X Z W : Ambient.{u}} (f : X ⟶ Z) (g : Z ⟶ W) (q : ℕ)
    (e : Abelian.Ext W Y q) : pb Y f q (pb Y g q e) = pb Y (f ≫ g) q e := by
  change (Abelian.Ext.mk₀ f).comp ((Abelian.Ext.mk₀ g).comp e (zero_add q)) (zero_add q) = _
  rw [← Abelian.Ext.comp_assoc_of_second_deg_zero,Abelian.Ext.mk₀_comp_mk₀]
  rfl

abbrev boundary (n q : ℕ) :
    Abelian.Ext (tower R (n+1)) Y q →+ Abelian.Ext (tower R n) Y (q+1) :=
  (seq_shortExact R n).extClass.precomp Y (by omega)

theorem boundary_natural (a : Endo R) (n q : ℕ)
    (e : Abelian.Ext (tower R (n+1)) Y q) :
    pb Y (a.tw n) (q+1) (boundary Y n q e) =
      boundary Y n q (pb Y (a.tw (n+1)) q e) := by
  have h := ShortComplex.ShortExact.extClass_naturality
    (seq_shortExact R n) (seq_shortExact R n) (a.seqMap n)
  change (seq_shortExact R n).extClass.comp (Abelian.Ext.mk₀ (a.tw (n+1))) (add_zero 1) =
    (Abelian.Ext.mk₀ (a.tw n)).comp (seq_shortExact R n).extClass (zero_add 1) at h
  change (Abelian.Ext.mk₀ (a.tw n)).comp ((seq_shortExact R n).extClass.comp e (by omega : 1+q=q+1)) (zero_add (q+1)) =
    (seq_shortExact R n).extClass.comp ((Abelian.Ext.mk₀ (a.tw (n+1))).comp e (zero_add q)) (by omega : 1+q=q+1)
  calc
    _ = ((Abelian.Ext.mk₀ (a.tw n)).comp (seq_shortExact R n).extClass (zero_add 1)).comp e (by omega : 1+q=q+1) :=
      (Abelian.Ext.comp_assoc _ _ _ (zero_add 1) (by omega : 1+q=q+1) (by omega : 0+1+q=q+1)).symm
    _ = _ := by rw [← h,Abelian.Ext.comp_assoc_of_second_deg_zero]

structure FiniteTruncations (I : Type u) (R : Resolution.{u}) where
  trunc : Finset I → Endo R
  tgt_absorb : ∀ {F G : Finset I}, F ⊆ G → (trunc G).tgt ≫ (trunc F).tgt = (trunc F).tgt
  tm_absorb : ∀ {F G : Finset I}, F ⊆ G → ∀ n, (trunc G).tm n ≫ (trunc F).tm n = (trunc F).tm n

namespace FiniteTruncations
variable {I : Type u} (B : FiniteTruncations I R)

theorem tower_absorb {F G : Finset I} (h : F ⊆ G) (n : ℕ) :
    (B.trunc G).tw n ≫ (B.trunc F).tw n = (B.trunc F).tw n := by
  cases n with
  | zero => exact B.tgt_absorb h
  | succ n =>
    letI := inclusion_mono R n
    change (B.trunc G).km n ≫ (B.trunc F).km n = (B.trunc F).km n
    apply (cancel_mono (inclusion R n)).1
    rw [Category.assoc,Endo.km_i,← Category.assoc,Endo.km_i,Category.assoc,B.tm_absorb h]

abbrev termFinite : Prop := ∀ n q (e : Abelian.Ext (R.term n) Y q),
  ∃ F : Finset I, pb Y ((B.trunc F).tm n) q e = e

theorem fixed_mono {F G : Finset I} (h : F ⊆ G) (n q : ℕ)
    (e : Abelian.Ext (tower R n) Y q) (he : pb Y ((B.trunc F).tw n) q e = e) :
    pb Y ((B.trunc G).tw n) q e = e := by
  calc
    _ = pb Y ((B.trunc G).tw n) q (pb Y ((B.trunc F).tw n) q e) := by rw [he]
    _ = e := by rw [pb_comp,B.tower_absorb h,he]

theorem fixed_add {F G : Finset I} (n q : ℕ)
    (e : Abelian.Ext (tower R n) Y q) (b : Abelian.Ext (tower R n) Y q)
    (he : pb Y ((B.trunc F).tw n) q e = e)
    (hb : pb Y ((B.trunc G).tw n) q b = b) :
    ∃ H : Finset I, pb Y ((B.trunc H).tw n) q (e+b) = e+b := by
  classical
  refine ⟨F ∪ G,?_⟩
  rw [map_add,B.fixed_mono Y Finset.subset_union_left n q e he,
    B.fixed_mono Y Finset.subset_union_right n q b hb]

theorem term_to_tower (ht : B.termFinite Y) :
    ∀ q n (e : Abelian.Ext (tower R n) Y q),
      ∃ F : Finset I, pb Y ((B.trunc F).tw n) q e = e := by
  intro q
  induction q with
  | zero =>
    intro n e
    obtain ⟨F,hF⟩ := ht n 0 (pb Y (towerCover R n) 0 e)
    refine ⟨F,?_⟩
    letI := towerCover_epi R n
    apply Abelian.Ext.precomp_mk₀_injective_of_epi Y (towerCover R n)
    change pb Y (towerCover R n) 0 (pb Y ((B.trunc F).tw n) 0 e) = _
    rw [pb_comp,Endo.tower_comm,← pb_comp]
    exact hF
  | succ q ih =>
    intro n e
    obtain ⟨F,hF⟩ := ht n (q+1) (pb Y (towerCover R n) (q+1) e)
    let eF := pb Y ((B.trunc F).tw n) (q+1) e
    have heF : pb Y ((B.trunc F).tw n) (q+1) eF = eF := by
      unfold eF
      rw [pb_comp,B.tower_absorb (Finset.Subset.refl F)]
    have hz : pb Y (towerCover R n) (q+1) (e-eF) = 0 := by
      rw [map_sub]
      unfold eF
      rw [pb_comp,Endo.tower_comm,← pb_comp,hF,sub_self]
    obtain ⟨b,hb⟩ := Abelian.Ext.contravariant_sequence_exact₃
      (seq_shortExact R n) Y (e-eF) hz (by omega : 1+q=q+1)
    obtain ⟨G,hG⟩ := ih (n+1) b
    have hg : pb Y ((B.trunc G).tw n) (q+1) (boundary Y n q b) = boundary Y n q b := by
      rw [boundary_natural,hG]
    have he : eF + boundary Y n q b = e := by
      change eF + (seq_shortExact R n).extClass.comp b (by omega : 1+q=q+1) = e
      rw [hb]
      abel
    obtain ⟨H,hH⟩ := B.fixed_add Y n (q+1) eF (boundary Y n q b) heF hg
    exact ⟨H,by rw [← he]; exact hH⟩

theorem target_finiteSupport (ht : B.termFinite Y) (q : ℕ)
    (e : Abelian.Ext R.target Y q) :
    ∃ F : Finset I, pb Y ((B.trunc F).tgt) q e = e :=
  B.term_to_tower Y ht q 0 e

#print axioms target_finiteSupport
end FiniteTruncations
end CMDG.CondensedCM5R0.AcyclicResolution
