import CMDGCondensedCM4P3DerivedCM5R0CompactCoverExtTransfer

/-! Canonical comparison of scalar cocycle classes to positive Ext.
The connecting maps are the actual Yoneda extension classes. -/
noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.CompactCover

variable (P : Profinite.{u}) (T : CompHaus.{u}) (p : profiniteToCompHaus.obj P ⟶ T)
variable [Epi p]

abbrev towerObj : ℕ → Ambient
  | 0 => compactFreeFunctor.obj T
  | n+1 => syzygy P T p n

def towerProjection : (n : ℕ) → term P T p n ⟶ towerObj P T p n
  | 0 => aug P T p
  | n+1 => syzygyCover P T p n

omit [Epi p] in
theorem tower_zero (n : ℕ) :
    syzygyι P T p n ≫ towerProjection P T p n = 0 := by
  cases n with
  | zero => exact kernel.condition (aug P T p)
  | succ n => exact ι_comp_cover_zero P T p n

abbrev towerSeq (n : ℕ) : ShortComplex Ambient :=
  ShortComplex.mk (syzygyι P T p n) (towerProjection P T p n) (tower_zero P T p n)

theorem tower_shortExact (n : ℕ) : (towerSeq P T p n).ShortExact := by
  cases n with
  | zero => exact aug_shortExact P T p
  | succ n => exact syzygy_shortExact P T p n

def connecting (n q : ℕ) :
    Abelian.Ext (syzygy P T p n) discreteIntegerCoeff q →+
      Abelian.Ext (towerObj P T p n) discreteIntegerCoeff (q+1) :=
  (tower_shortExact P T p n).extClass.precomp discreteIntegerCoeff (by omega)

theorem connecting_surj (n q : ℕ) :
    Function.Surjective (connecting P T p n q) := by
  intro e
  have hz : (Abelian.Ext.mk₀ (towerSeq P T p n).g).comp e
      (zero_add (q+1)) = 0 :=
    freeProfinite_extPositive_scalar_zero _ q _
  exact Abelian.Ext.contravariant_sequence_exact₃
    (tower_shortExact P T p n) discreteIntegerCoeff e hz (by omega)

theorem connecting_inj (n q : ℕ) :
    Function.Injective (connecting P T p n (q+1)) := by
  rw [← AddMonoidHom.ker_eq_bot_iff, AddSubgroup.eq_bot_iff_forall]
  intro x hx
  have hx' : (tower_shortExact P T p n).extClass.comp x
      (by omega : 1 + (q+1) = q+1+1) = 0 := hx
  obtain ⟨y,hy⟩ := Abelian.Ext.contravariant_sequence_exact₁
    (tower_shortExact P T p n) discreteIntegerCoeff x _ hx'
  rw [freeProfinite_extPositive_scalar_zero _ q y, Abelian.Ext.comp_zero] at hy
  exact hy.symm

def positiveShift (n q : ℕ) :
    Abelian.Ext (towerObj P T p (n+1)) discreteIntegerCoeff (q+1) ≃+
      Abelian.Ext (towerObj P T p n) discreteIntegerCoeff (q+2) :=
  AddEquiv.ofBijective (connecting P T p n (q+1))
    ⟨connecting_inj P T p n q, connecting_surj P T p n (q+1)⟩

def connectingHom (n : ℕ) :
    (syzygy P T p n ⟶ discreteIntegerCoeff) →+
      Abelian.Ext (towerObj P T p n) discreteIntegerCoeff 1 :=
  (connecting P T p n 0).comp Abelian.Ext.addEquiv₀.symm.toAddMonoidHom

theorem connectingHom_surj (n : ℕ) :
    Function.Surjective (connectingHom P T p n) :=
  (connecting_surj P T p n 0).comp Abelian.Ext.addEquiv₀.symm.surjective

theorem connectingHom_zero_iff (n : ℕ) (f : syzygy P T p n ⟶ discreteIntegerCoeff) :
    connectingHom P T p n f = 0 ↔
      ∃ g : term P T p n ⟶ discreteIntegerCoeff, syzygyι P T p n ≫ g = f := by
  let hS := tower_shortExact P T p n
  change hS.extClass.comp (Abelian.Ext.mk₀ f) (by omega : 1 + 0 = 1) = 0 ↔ _
  constructor
  · intro hz
    obtain ⟨y,hy⟩ := Abelian.Ext.contravariant_sequence_exact₁
      hS discreteIntegerCoeff (Abelian.Ext.mk₀ f) _ hz
    refine ⟨Abelian.Ext.addEquiv₀ y, ?_⟩
    apply Abelian.Ext.addEquiv₀.symm.injective
    change Abelian.Ext.mk₀ (syzygyι P T p n ≫ Abelian.Ext.addEquiv₀ y) = Abelian.Ext.mk₀ f
    rw [← Abelian.Ext.mk₀_comp_mk₀, Abelian.Ext.mk₀_addEquiv₀_apply]
    exact hy
  · rintro ⟨g,hg⟩
    rw [← hg, ← Abelian.Ext.mk₀_comp_mk₀]
    have hz : hS.extClass.comp (Abelian.Ext.mk₀ (towerSeq P T p n).f)
        (by omega : 1+0=1) = 0 := hS.extClass_comp
    change hS.extClass.comp
      ((Abelian.Ext.mk₀ (towerSeq P T p n).f).comp (Abelian.Ext.mk₀ g) (by omega : 0+0=0))
      (by omega : 1+0=1) = 0
    rw [← Abelian.Ext.comp_assoc, hz, Abelian.Ext.zero_comp] <;> omega

def shiftAll (n q : ℕ) :
    Abelian.Ext (towerObj P T p (n+q)) discreteIntegerCoeff 1 ≃+
      Abelian.Ext (towerObj P T p n) discreteIntegerCoeff (q+1) :=
  match q with
  | 0 => AddEquiv.refl _
  | q+1 =>
    let e : Abelian.Ext (towerObj P T p (n+(q+1))) discreteIntegerCoeff 1 ≃+
        Abelian.Ext (towerObj P T p (n+1)) discreteIntegerCoeff (q+1) := by
      rw [show n+(q+1) = n+1+q by omega]
      exact shiftAll (n+1) q
    e.trans (positiveShift P T p n q)
termination_by q

def shiftToTarget (n : ℕ) :
    Abelian.Ext (towerObj P T p n) discreteIntegerCoeff 1 ≃+
      Abelian.Ext (compactFreeFunctor.obj T) discreteIntegerCoeff (n+1) := by
  change Abelian.Ext (towerObj P T p n) discreteIntegerCoeff 1 ≃+
    Abelian.Ext (towerObj P T p 0) discreteIntegerCoeff (n+1)
  exact Eq.mp (congrArg (fun k => Abelian.Ext (towerObj P T p k)
      discreteIntegerCoeff 1 ≃+ Abelian.Ext (towerObj P T p 0)
      discreteIntegerCoeff (n+1)) (Nat.zero_add n)) (shiftAll P T p 0 n)

def classOfSyzygyHom (n : ℕ) :
    (syzygy P T p n ⟶ discreteIntegerCoeff) →+
      Abelian.Ext (compactFreeFunctor.obj T) discreteIntegerCoeff (n+1) :=
  (shiftToTarget P T p n).toAddMonoidHom.comp (connectingHom P T p n)

theorem classOfSyzygyHom_surj (n : ℕ) :
    Function.Surjective (classOfSyzygyHom P T p n) :=
  (shiftToTarget P T p n).surjective.comp (connectingHom_surj P T p n)

theorem classOfSyzygyHom_zero_iff (n : ℕ) (f : syzygy P T p n ⟶ discreteIntegerCoeff) :
    classOfSyzygyHom P T p n f = 0 ↔
      ∃ g : term P T p n ⟶ discreteIntegerCoeff, syzygyι P T p n ≫ g = f := by
  change shiftToTarget P T p n (connectingHom P T p n f) = 0 ↔ _
  rw [map_eq_zero_iff (shiftToTarget P T p n) (shiftToTarget P T p n).injective]
  exact connectingHom_zero_iff P T p n f

theorem cocycle_factors_unique (n : ℕ) (f : term P T p (n+1) ⟶ discreteIntegerCoeff)
    (hf : d P T p (n+1) ≫ f = 0) :
    ∃! g : syzygy P T p n ⟶ discreteIntegerCoeff, syzygyCover P T p n ≫ g = f := by
  letI := cover_epi P T p n
  letI := cover_epi P T p (n+1)
  have hz : syzygyι P T p (n+1) ≫ f = 0 := by
    apply (cancel_epi (syzygyCover P T p (n+1))).1
    rw [← Category.assoc, cover_comp_ι, hf, comp_zero]
  let S := ShortComplex.mk (syzygyι P T p (n+1)) (syzygyCover P T p n)
    (ι_comp_cover_zero P T p n)
  have hS : S.ShortExact := syzygy_shortExact P T p n
  haveI : Epi S.g := hS.epi_g
  obtain ⟨g,hg⟩ := hS.exact.desc' f hz
  refine ⟨g,hg,?_⟩
  intro k hk
  apply (cancel_epi (syzygyCover P T p n)).1
  exact hk.trans hg.symm

#print axioms positiveShift
#print axioms classOfSyzygyHom_zero_iff
#print axioms classOfSyzygyHom_surj
#print axioms cocycle_factors_unique
end CMDG.CondensedCM5R0.CompactCover
