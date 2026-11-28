import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRealCoordinates

noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.BreenDeligneProbe
open RealProductProjection CompactCover

def cofanEquivColimit {k : ℕ} {X : Fin k → SetPsh.{u}} {Y : SetPsh.{u}}
    (leg : ∀ j, X j ⟶ Y)
    (e : ∀ T, (Σ j, (X j).obj T) ≃ Y.obj T)
    (he : ∀ T j x, e T ⟨j,x⟩ = (leg j).app T x) :
    IsColimit (Cofan.mk Y leg) := by
  apply evaluationJointlyReflectsColimits
  intro T
  refine { desc := fun c => ↾fun y => c.ι.app ⟨((e T).symm y).1⟩ ((e T).symm y).2
           fac := ?_
           uniq := ?_ }
  · intro c j
    apply ConcreteCategory.hom_ext
    intro x
    change c.ι.app ⟨((e T).symm ((leg j.as).app T x)).1⟩
      ((e T).symm ((leg j.as).app T x)).2 = c.ι.app j x
    rw [← he, Equiv.symm_apply_apply]
  · intro c m hm
    apply ConcreteCategory.hom_ext
    intro y
    let z := (e T).symm y
    have h : (leg z.1).app T z.2 = y := (he T z.1 z.2).symm.trans ((e T).apply_symm_apply y)
    have h' := congrArg (fun f => f z.2) (hm ⟨z.1⟩)
    change m ((leg z.1).app T z.2) = _ at h'
    rw [h] at h'
    exact h'

abbrev FFree : SetPsh.{u} ⥤ Ambient.{u} := freeOn ⋙ moduleSheafification

def freeCofanColimit {k : ℕ} {X : Fin k → SetPsh.{u}} {Y : SetPsh.{u}}
    (leg : ∀ j, X j ⟶ Y) (h : IsColimit (Cofan.mk Y leg)) :
    IsColimit (Cofan.mk (FFree.obj Y) (fun j => FFree.map (leg j))) := by
  letI := (ModuleCat.adj Coeff).isLeftAdjoint
  exact (Cofan.isColimitMapCoconeEquiv FFree _ _) (isColimitOfPreserves FFree h)

variable (S : Profinite.{u}) (I : Type u) {k : ℕ} (arity : Fin k → ℕ)

def realCofanColimit :
    IsColimit (Cofan.mk (FFree.obj (productSet (probeSet S) (realGeneratorPsh I arity)))
      (fun j => FFree.map (realLeg I S arity j))) :=
  freeCofanColimit _ (cofanEquivColimit _ (realLegEquiv I S arity) (fun _ _ _ => rfl))

def zeroCofanColimit :
    IsColimit (Cofan.mk (FFree.obj (productSet (probeSet S) (zeroGeneratorPsh arity)))
      (fun j => FFree.map (zeroLeg S arity j))) :=
  freeCofanColimit _ (cofanEquivColimit _ (zeroLegEquiv S arity) (fun _ _ _ => rfl))

end CMDG.CondensedCM5R0.BreenDeligneProbe
