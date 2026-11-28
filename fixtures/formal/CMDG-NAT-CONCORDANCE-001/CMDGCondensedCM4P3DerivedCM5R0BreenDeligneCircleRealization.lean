import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneCircleCoordinates

/-! Actual finite-type circle terms and their natural truncations. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.BreenDeligneProbe
open RealProductProjection CompactCover CompactCover.CircleContinuity AcyclicResolution
variable (I : Type u) (S : Profinite.{u}) {k : ℕ} (arity : Fin k → ℕ)

abbrev circleFamilyFree (j : Fin k) : Ambient.{u} :=
  compactFreeFunctor.obj (circlePowerT S I (arity j))

def circleCofanColimit :
    IsColimit (Cofan.mk (FFree.obj (productSet (probeSet S) (circleGeneratorPsh I arity)))
      (fun j => FFree.map (circleLeg I S arity j))) :=
  freeCofanColimit _ (cofanEquivColimit _ (circleLegEquiv I S arity) (fun _ _ _ => rfl))

def circleFreeIso :
    (transport (probeSet S) (circlePsh I)).obj (polynomial arity) ≅
      FFree.obj (productSet (probeSet S) (circleGeneratorPsh I arity)) :=
  moduleSheafification.mapIso (indexedFreeIso (probeSet S) (circleGeneratorPsh I arity))

def circleSumIso : (∐ circleFamilyFree I S arity) ≅
    FFree.obj (productSet (probeSet S) (circleGeneratorPsh I arity)) :=
  IsColimit.coconePointUniqueUpToIso (colimit.isColimit _) (circleCofanColimit I S arity)

theorem circleSumIso_leg (j : Fin k) :
    Sigma.ι (circleFamilyFree I S arity) j ≫ (circleSumIso I S arity).hom =
      FFree.map (circleLeg I S arity j) :=
  (colimit.isColimit (Discrete.functor (circleFamilyFree I S arity))).fac _ ⟨j⟩

def circleTermIso :
    (∐ circleFamilyFree I S arity) ≅
      (transport (probeSet S) (circlePsh I)).obj (polynomial arity) :=
  circleSumIso I S arity ≪≫ (circleFreeIso I S arity).symm

variable (F : Finset I)

abbrev powerTrunc (j : Fin k) : circlePowerT S I (arity j) ⟶ circlePowerT S I (arity j) :=
  circleProjection S I (arity j) F ≫ circleSection S I (arity j) F

abbrev generatorTrunc : circleGeneratorPsh I arity ⟶ circleGeneratorPsh I arity :=
  Functor.whiskerRight (circleTrunc I F) (tupleSet arity)

theorem circleLeg_trunc (j : Fin k) :
    circleLeg I S arity j ≫ productMap (probeSet S) (generatorTrunc I arity F) =
      (compHausToCondensed.map (powerTrunc I S arity F j)).hom ≫ circleLeg I S arity j := by
  apply NatTrans.ext
  funext T
  apply ConcreteCategory.hom_ext
  intro x
  rfl

theorem circleFreeIso_trunc :
    changeInput (probeSet S) (circleTrunc I F) (polynomial arity) ≫
      (circleFreeIso I S arity).hom =
    (circleFreeIso I S arity).hom ≫ FFree.map (productMap (probeSet S) (generatorTrunc I arity F)) := by
  change moduleSheafification.map ((indexedFunctor (probeSet S)).map
    (freeOn.map (generatorTrunc I arity F))) ≫
    moduleSheafification.map (indexedFreeIso (probeSet S) (circleGeneratorPsh I arity)).hom =
    moduleSheafification.map (indexedFreeIso (probeSet S) (circleGeneratorPsh I arity)).hom ≫
    moduleSheafification.map (freeOn.map (productMap (probeSet S) (generatorTrunc I arity F)))
  rw [← Functor.map_comp,← Functor.map_comp,indexedFreeIso_natural]

theorem circleSumIso_trunc :
    (circleSumIso I S arity).hom ≫ FFree.map (productMap (probeSet S) (generatorTrunc I arity F)) =
      Limits.Sigma.map (fun j => compactFreeFunctor.map (powerTrunc I S arity F j)) ≫
        (circleSumIso I S arity).hom := by
  apply Sigma.hom_ext
  intro j
  rw [← Category.assoc,circleSumIso_leg,← Functor.map_comp,circleLeg_trunc,Functor.map_comp,
    Sigma.ι_map_assoc,circleSumIso_leg]
  rfl

theorem circleTermIso_trunc :
    (circleTermIso I S arity).hom ≫ changeInput (probeSet S) (circleTrunc I F) (polynomial arity) =
      Limits.Sigma.map (fun j => compactFreeFunctor.map (powerTrunc I S arity F j)) ≫
        (circleTermIso I S arity).hom := by
  apply (cancel_mono (circleFreeIso I S arity).hom).1
  change ((circleSumIso I S arity).hom ≫ (circleFreeIso I S arity).inv) ≫
    changeInput (probeSet S) (circleTrunc I F) (polynomial arity) ≫ (circleFreeIso I S arity).hom =
    Limits.Sigma.map (fun j => compactFreeFunctor.map (powerTrunc I S arity F j)) ≫
      ((circleSumIso I S arity).hom ≫ (circleFreeIso I S arity).inv) ≫ (circleFreeIso I S arity).hom
  simp only [Category.assoc,circleFreeIso_trunc,Iso.inv_hom_id_assoc,Iso.inv_hom_id,Category.comp_id]
  exact circleSumIso_trunc I S arity F

abbrev circleResolution (B : UniversalBD.{u}) :=
  transportedResolution B (probeSet S) (circlePsh I)

def circleEndo (B : UniversalBD.{u}) : Endo (circleResolution I S B) where
  tgt := changeInput (probeSet S) (circleTrunc I F) (𝟭 Mod.{u})
  tm n := changeInput (probeSet S) (circleTrunc I F) (polynomial (B.arity n))
  aug_comm := changeInput_natural (probeSet S) (circleTrunc I F) B.aug
  d_comm n := changeInput_natural (probeSet S) (circleTrunc I F) (B.d n)

def circleTruncations (B : UniversalBD.{u}) : FiniteTruncations I (circleResolution I S B) where
  trunc F := circleEndo I S F B
  tgt_absorb h := by
    change changeInput _ _ _ ≫ changeInput _ _ _ = changeInput _ _ _
    rw [changeInput_comp,circleTrunc_absorb I h]
  tm_absorb h n := by
    change changeInput _ _ _ ≫ changeInput _ _ _ = changeInput _ _ _
    rw [changeInput_comp,circleTrunc_absorb I h]

#print axioms circleTermIso_trunc
#print axioms circleTruncations
end CMDG.CondensedCM5R0.BreenDeligneProbe
