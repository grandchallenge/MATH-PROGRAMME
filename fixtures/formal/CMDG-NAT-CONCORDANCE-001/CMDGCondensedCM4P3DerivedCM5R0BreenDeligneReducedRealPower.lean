import CMDGCondensedCM4P3DerivedCM5R0RealBoxCechHom

/-! The canonical reduced free relative real power is invisible to
the discrete integers in every Ext degree, including Hom. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
set_option maxHeartbeats 100000
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0.RealProductProjection
open CompactCover CompactCover.Dyadic RealProductCondensedColimit
variable (S : Profinite.{u}) (I : Type u)

abbrev FreeReal := (freeProbeRealCocone S I).pt
abbrev FreeProbe := compactFreeFunctor.obj (profiniteToCompHaus.obj S)

def realZeroSection : FreeProbe S ⟶ FreeReal S I :=
  compactFreeFunctor.map (radiusZero S I (zeroRadius I)) ≫
    (freeProbeRealCocone S I).ι.app (zeroRadius I)

theorem realZeroSection_projection :
    realZeroSection S I ≫ realProjection S I = 𝟙 _ := by
  unfold realZeroSection
  rw [Category.assoc,realProjection_restrict,← Functor.map_comp,radiusZero_projection]
  exact compactFreeFunctor.map_id _

/-- Canonical kernel of the actual projection, not quotient by an
arbitrarily chosen rank-one summand. -/
abbrev reducedRealPower := kernel (realProjection S I)

def splitKernelRetraction {X Y : Ambient.{u}} (p : X ⟶ Y) (s : Y ⟶ X)
    (hs : s ≫ p = 𝟙 Y) : X ⟶ kernel p :=
  kernel.lift p (𝟙 X - p ≫ s) (by
    rw [Preadditive.sub_comp,Category.id_comp,Category.assoc,hs,Category.comp_id,sub_self])

theorem splitKernelRetraction_spec {X Y : Ambient.{u}} (p : X ⟶ Y) (s : Y ⟶ X)
    (hs : s ≫ p = 𝟙 Y) :
    splitKernelRetraction p s hs ≫ kernel.ι p = 𝟙 X - p ≫ s :=
  kernel.lift_ι _ _ _

theorem splitKernelRetraction_retract {X Y : Ambient.{u}} (p : X ⟶ Y) (s : Y ⟶ X)
    (hs : s ≫ p = 𝟙 Y) :
    kernel.ι p ≫ splitKernelRetraction p s hs = 𝟙 _ := by
  apply (cancel_mono (kernel.ι p)).1
  rw [Category.assoc,splitKernelRetraction_spec,Preadditive.comp_sub,Category.comp_id,
    ← Category.assoc,kernel.condition,zero_comp,sub_zero,Category.id_comp]

theorem splitKernel_homZero {X Y G : Ambient.{u}} (p : X ⟶ Y) (s : Y ⟶ X)
    (hs : s ≫ p = 𝟙 Y)
    (h : Function.Surjective (fun g : Y ⟶ G => p ≫ g))
    (f : kernel p ⟶ G) : f=0 := by
  obtain ⟨g,hg⟩ := h (splitKernelRetraction p s hs ≫ f)
  change p ≫ g = splitKernelRetraction p s hs ≫ f at hg
  calc
    f = kernel.ι p ≫ (splitKernelRetraction p s hs ≫ f) := by
      rw [← Category.assoc,splitKernelRetraction_retract,Category.id_comp]
    _ = kernel.ι p ≫ (p ≫ g) := by rw [hg]
    _ = 0 := by rw [← Category.assoc,kernel.condition,zero_comp]

theorem reducedRealPower_homZero (f : reducedRealPower S I ⟶ discreteIntegerCoeff) : f=0 :=
  splitKernel_homZero _ (realZeroSection S I) (realZeroSection_projection S I)
    (realProjection_hom_bijective S I).2 f

theorem reducedRealPower_extPositive_zero (q : ℕ)
    (e : Abelian.Ext (reducedRealPower S I) discreteIntegerCoeff (q+1)) : e=0 :=
  ext_zero_of_retract (kernel.ι _) (splitKernelRetraction _ (realZeroSection S I)
    (realZeroSection_projection S I))
    (splitKernelRetraction_retract _ _ _) q (freeProbeReal_extPositive_zero S I q) e

theorem reducedRealPower_extZero (q : ℕ)
    (e : Abelian.Ext (reducedRealPower S I) discreteIntegerCoeff q) : e=0 := by
  cases q with
  | zero =>
    apply Abelian.Ext.addEquiv₀.injective
    rw [map_zero]
    exact reducedRealPower_homZero S I _
  | succ q => exact reducedRealPower_extPositive_zero S I q e

#print axioms realZeroSection_projection
#print axioms reducedRealPower_extZero
end CMDG.CondensedCM5R0.RealProductProjection
