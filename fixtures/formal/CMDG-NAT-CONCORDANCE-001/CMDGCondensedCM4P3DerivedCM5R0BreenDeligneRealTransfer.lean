import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneSplitReduction

/-! Finite-type Breen--Deligne transfer. The input is an actual exact
augmented resolution with the canonical projection to its zero-value
complex. All analytic Ext/Hom vanishing is proved, not assumed. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0
open AcyclicResolution RealProductProjection

variable (S : Profinite.{u}) (I : Type u)

abbrev powerFamily {k : ℕ} (arity : Fin k → ℕ) (j : Fin k) : Ambient.{u} :=
  FreeReal S (Fin (arity j) × I)

abbrev baseFamily (k : ℕ) (_ : Fin k) : Ambient.{u} := FreeProbe S

def powerProjection {k : ℕ} (arity : Fin k → ℕ) :
    (∐ powerFamily S I arity) ⟶ (∐ baseFamily S k) :=
  Limits.Sigma.map (fun j => realProjection S (Fin (arity j) × I))

theorem powerProjection_homSurj {k : ℕ} (arity : Fin k → ℕ) :
    Function.Surjective (fun g : (∐ baseFamily S k) ⟶ discreteIntegerCoeff =>
      powerProjection S I arity ≫ g) := by
  intro f
  choose g hg using fun j : Fin k =>
    (realProjection_hom_bijective S (Fin (arity j) × I)).2
      (Sigma.ι (powerFamily S I arity) j ≫ f)
  refine ⟨Sigma.desc g,?_⟩
  apply Sigma.hom_ext
  intro j
  change Sigma.ι (powerFamily S I arity) j ≫
    Limits.Sigma.map (fun j => realProjection S (Fin (arity j) × I)) ≫
      Sigma.desc g = _
  rw [Sigma.ι_map_assoc,Sigma.ι_desc]
  exact hg j

theorem powerFamily_extZero {k : ℕ} (arity : Fin k → ℕ) (q : ℕ)
    (e : Abelian.Ext (∐ powerFamily S I arity) discreteIntegerCoeff (q+1)) : e=0 := by
  let X (j : ULift.{u} (Fin k)) : Ambient.{u} := powerFamily S I arity j.down
  let iso : (∐ powerFamily S I arity) ≅ (∐ X) :=
    Sigma.whiskerEquiv (f := powerFamily S I arity) (g := X) (Equiv.ulift.symm : Fin k ≃ ULift.{u} (Fin k)) (fun _ => Iso.refl _)
  exact CompactCover.Dyadic.ext_zero_of_retract iso.hom iso.inv iso.hom_inv_id q
    (coproduct_extPositive_zero X discreteIntegerCoeff q
      (fun j => freeProbeReal_extPositive_zero S (Fin (arity j.down) × I) q)) e

/-- The only data needed from the genuine finite-type resolution:
exact augmented complex, natural zero split, finite free-power
coordinates and the canonical projection in those coordinates. -/
structure FiniteTypeRealResolution where
  resolution : Resolution.{u}
  zeroSplit : SplitResolution resolution
  count : ℕ → ℕ
  arity : ∀ n, Fin (count n) → ℕ
  termIso : ∀ n, resolution.term n ≅ (∐ powerFamily S I (arity n))
  baseIso : ∀ n, zeroSplit.base n ≅ (∐ baseFamily S (count n))
  projection_square : ∀ n, zeroSplit.p n ≫ (baseIso n).hom =
    (termIso n).hom ≫ powerProjection S I (arity n)

namespace FiniteTypeRealResolution
variable {S I} (B : FiniteTypeRealResolution S I)

theorem term_extZero (n q : ℕ)
    (e : Abelian.Ext (B.resolution.term n) discreteIntegerCoeff (q+1)) : e=0 :=
  CompactCover.Dyadic.ext_zero_of_retract (B.termIso n).hom (B.termIso n).inv
    (B.termIso n).hom_inv_id q (powerFamily_extZero S I (B.arity n) q) e

theorem projection_homSurj (n : ℕ) :
    Function.Surjective (fun g : B.zeroSplit.base n ⟶ discreteIntegerCoeff =>
      B.zeroSplit.p n ≫ g) := by
  intro f
  obtain ⟨g,hg⟩ := powerProjection_homSurj S I (B.arity n)
    ((B.termIso n).inv ≫ f)
  refine ⟨(B.baseIso n).hom ≫ g,?_⟩
  change B.zeroSplit.p n ≫ (B.baseIso n).hom ≫ g = f
  rw [← Category.assoc,B.projection_square,Category.assoc]
  change powerProjection S I (B.arity n) ≫ g = (B.termIso n).inv ≫ f at hg
  rw [hg, Iso.hom_inv_id_assoc]

theorem reduced_term_homZero (n : ℕ)
    (f : B.zeroSplit.K n ⟶ discreteIntegerCoeff) : f=0 :=
  splitKernel_homZero _ (B.zeroSplit.s n) (B.zeroSplit.split n)
    (B.projection_homSurj n) f

theorem reduced_term_extZero (n q : ℕ)
    (e : Abelian.Ext (B.zeroSplit.K n) discreteIntegerCoeff (q+1)) : e=0 :=
  CompactCover.Dyadic.ext_zero_of_retract (B.zeroSplit.i n) (B.zeroSplit.r n)
    (B.zeroSplit.ir n) q (B.term_extZero n q) e

theorem target_homZero (f : B.resolution.target ⟶ discreteIntegerCoeff) : f=0 := by
  letI := B.zeroSplit.ka_epi
  apply (cancel_epi B.zeroSplit.ka).1
  rw [comp_zero]
  exact B.reduced_term_homZero 0 _

theorem target_extPositive_zero (q : ℕ)
    (e : Abelian.Ext B.resolution.target discreteIntegerCoeff (q+1)) : e=0 := by
  apply AcyclicResolution.target_extZero B.zeroSplit.reducedResolution discreteIntegerCoeff
    (B.reduced_term_extZero) _ q e
  intro n f hf
  refine ⟨0,?_⟩
  rw [comp_zero]
  exact (B.reduced_term_homZero (n+1) f).symm

theorem target_extZero (q : ℕ)
    (e : Abelian.Ext B.resolution.target discreteIntegerCoeff q) : e=0 := by
  cases q with
  | zero =>
    apply Abelian.Ext.addEquiv₀.injective
    rw [map_zero]
    exact B.target_homZero _
  | succ q => exact B.target_extPositive_zero q e

#print axioms target_extZero
end FiniteTypeRealResolution
end CMDG.CondensedCM5R0
