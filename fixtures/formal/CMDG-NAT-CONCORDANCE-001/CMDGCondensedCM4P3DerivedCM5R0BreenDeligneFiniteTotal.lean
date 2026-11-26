import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFiniteImage
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneFiniteColumnRemoval

/-! Finite generation of actual total homology from finite column homology,
by an explicit finite filtration of the images of supported cycles. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
open CMDG.CondensedCM5R0.BreenDeligneTotalCoordinates
open CMDG.CondensedCM5R0.BreenDeligneHomologyElements
open CMDG.CondensedCM5R0.BreenDeligneFiniteImage
open CMDG.CondensedCM5R0.BreenDeligneFiniteColumnRemoval
namespace CMDG.CondensedCM5R0.BreenDeligneFiniteTotal
set_option backward.isDefEq.respectTransparency false

def intLinear {M N : Type} [AddCommGroup M] [AddCommGroup N]
    [Module ℤ M] [Module ℤ N] (f : M →+ N) : M →ₗ[ℤ] N where
  toFun := f
  map_add' := map_add f
  map_smul' := by intro k x; simpa only [Int.cast_id,RingHom.id_apply] using map_intCast_smul f ℤ ℤ k x

def before (K : BC) (n r : ℕ) : Submodule ℤ ((K.total c).cycles n) where
  carrier := {z | ∀ p q (h : p+q=n), r≤p →
    proj K n p q h ((K.total c).iCycles n z)=0}
  zero_mem' := by
    intro p q h hp
    rw [map_zero,map_zero]
  add_mem' := by
    intro a b ha hb p q h hp
    rw [map_add,map_add,ha p q h hp,hb p q h hp,add_zero]
  smul_mem' := by
    intro k a ha p q h hp
    let F := (proj K n p q h).hom.comp ((K.total c).iCycles n).hom
    have hf : F a = 0 := ha p q h hp
    have he := F.map_smul k a
    rw [hf,smul_zero] at he
    exact he


def classMap (K : BC) (n r : ℕ) :
    before K n r →ₗ[ℤ] (K.total c).homology n :=
  intLinear { toFun := fun z => (K.total c).homologyπ n z.val
              map_zero' := map_zero ((K.total c).homologyπ n).hom
              map_add' := fun a b => map_add ((K.total c).homologyπ n).hom a.val b.val }


def imageBefore (K : BC) (n r : ℕ) : Submodule ℤ ((K.total c).homology n) :=
  LinearMap.range (classMap K n r)

theorem supported (K : BC) (r q : ℕ) (z : before K (r+q) (r+1)) :
    SupportedThrough K (r+q) r ((K.total c).iCycles (r+q) z.val) := by
  intro p t h hp
  exact z.property p t h (by omega)

def topAdd (K : BC) (r q : ℕ) :
    before K (r+q) (r+1) →+ (K.X r).cycles q where
  toFun z := topCycle K r q z.val (supported K r q z)
  map_zero' := by
    apply iCycles_injective
    rw [topCycle_i]
    change proj K (r+q) r q rfl ((K.total c).iCycles (r+q) 0)=_
    rw [map_zero,map_zero,map_zero]
  map_add' a b := by
    apply iCycles_injective
    rw [topCycle_i,map_add,topCycle_i,topCycle_i]
    change proj K (r+q) r q rfl ((K.total c).iCycles (r+q) (a.val+b.val))=_
    rw [map_add,map_add]

def topClass (K : BC) (r q : ℕ) :
    before K (r+q) (r+1) →ₗ[ℤ] (K.X r).homology q :=
  intLinear (((K.X r).homologyπ q).hom.toAddMonoidHom.comp (topAdd K r q))


theorem top_kernel (K : BC) (r q : ℕ) (z : before K (r+q) (r+1))
    (hz : topClass K r q z=0) :
    classMap K (r+q) (r+1) z ∈ imageBefore K (r+q) r := by
  obtain ⟨w,hw,hs⟩ := remove_top_class K r q z.val (supported K r q z) hz
  exact ⟨⟨w,hs⟩,hw.symm⟩

theorem finite_step (K : BC) (r q : ℕ)
    (h : (imageBefore K (r+q) r).FG)
    [Module.Finite ℤ ((K.X r).homology q)] :
    (imageBefore K (r+q) (r+1)).FG :=
  finite_image_of_control (classMap K (r+q) (r+1)) (topClass K r q)
    (imageBefore K (r+q) r) h (top_kernel K r q)

theorem zero_image (K : BC) (n : ℕ) : imageBefore K n 0=⊥ := by
  apply eq_bot_iff.mpr
  rintro x ⟨z,rfl⟩
  have hz : z.val=0 := by
    apply iCycles_injective
    apply coord_ext
    intro p q h
    rw [map_zero,map_zero]
    exact z.property p q h (by omega)
  change (K.total c).homologyπ n z.val ∈ (⊥ : Submodule ℤ ((K.total c).homology n))
  rw [hz,map_zero]
  exact zero_mem _

theorem finite_filtration (K : BC) (n r : ℕ) (hr : r≤n+1)
    (h : ∀ p q, p+q=n → Module.Finite ℤ ((K.X p).homology q)) :
    (imageBefore K n r).FG := by
  induction r with
  | zero => rw [zero_image]; exact Submodule.fg_bot
  | succ r ih =>
    have hn : r≤n := by omega
    let q := n-r
    have he : r+q=n := by dsimp [q]; omega
    have hh := ih (by omega)
    haveI := h r q he
    rw [← he] at hh ⊢
    exact finite_step K r q hh

theorem full_image (K : BC) (n : ℕ) : imageBefore K n (n+1)=⊤ := by
  apply eq_top_iff.mpr
  intro x _
  obtain ⟨z,hz⟩ := class_surj (K.total c) n x
  exact ⟨⟨z,fun p q h hp => by omega⟩,hz⟩

theorem total_finite (K : BC) (n : ℕ)
    (h : ∀ p q, p+q=n → Module.Finite ℤ ((K.X p).homology q)) :
    Module.Finite ℤ ((K.total c).homology n) := by
  have h' := finite_filtration K n (n+1) (le_refl _) h
  rw [full_image] at h'
  exact ⟨h'⟩

#print axioms top_kernel
#print axioms total_finite
end CMDG.CondensedCM5R0.BreenDeligneFiniteTotal
