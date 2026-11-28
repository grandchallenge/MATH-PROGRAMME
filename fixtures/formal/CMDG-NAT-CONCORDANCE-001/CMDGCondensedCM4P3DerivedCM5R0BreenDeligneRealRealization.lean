import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneRealCoproduct

noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits Opposite
namespace CMDG.CondensedCM5R0.BreenDeligneProbe
open RealProductProjection CompactCover

variable (S : Profinite.{u}) (I : Type u) {k : ℕ} (arity : Fin k → ℕ)

theorem freeRealToProbe_eq (J : Type u) :
    FFree.map (realToProbe S J) = realProjection S J := by
  apply (freeProbeRealIsColimit S J).hom_ext
  intro r
  rw [realProjection_restrict]
  change FFree.map ((probeRealCocone S J).ι.app r).hom ≫
    FFree.map (realToProbe S J) = FFree.map (compHausToCondensed.map (radiusProjection S J r)).hom
  rw [← Functor.map_comp]
  congr 1

def realFreeIso :
    (transport (probeSet S) (realPsh I)).obj (polynomial arity) ≅
      FFree.obj (productSet (probeSet S) (realGeneratorPsh I arity)) :=
  moduleSheafification.mapIso (indexedFreeIso (probeSet S) (realGeneratorPsh I arity))

def zeroFreeIso :
    (transport (probeSet S) zeroPsh).obj (polynomial arity) ≅
      FFree.obj (productSet (probeSet S) (zeroGeneratorPsh arity)) :=
  moduleSheafification.mapIso (indexedFreeIso (probeSet S) (zeroGeneratorPsh arity))

def realSumIso : (∐ powerFamily S I arity) ≅
    FFree.obj (productSet (probeSet S) (realGeneratorPsh I arity)) :=
  IsColimit.coconePointUniqueUpToIso (colimit.isColimit _) (realCofanColimit S I arity)

def zeroSumIso : (∐ baseFamily S k) ≅
    FFree.obj (productSet (probeSet S) (zeroGeneratorPsh arity)) :=
  IsColimit.coconePointUniqueUpToIso (colimit.isColimit _) (zeroCofanColimit S arity)

theorem realSumIso_leg (j : Fin k) :
    Sigma.ι (powerFamily S I arity) j ≫ (realSumIso S I arity).hom =
      FFree.map (realLeg I S arity j) :=
  (colimit.isColimit (Discrete.functor (powerFamily S I arity))).fac _ ⟨j⟩

theorem zeroSumIso_leg (j : Fin k) :
    Sigma.ι (baseFamily S k) j ≫ (zeroSumIso S arity).hom =
      FFree.map (zeroLeg S arity j) :=
  (colimit.isColimit (Discrete.functor (baseFamily S k))).fac _ ⟨j⟩

theorem realSumIso_projection :
    (realSumIso S I arity).hom ≫ FFree.map (productMap (probeSet S) (realGeneratorProjection I arity)) =
      powerProjection S I arity ≫ (zeroSumIso S arity).hom := by
  apply Sigma.hom_ext
  intro j
  rw [← Category.assoc,realSumIso_leg,← Functor.map_comp,realLeg_projection,
    Functor.map_comp,freeRealToProbe_eq]
  rw [powerProjection,Sigma.ι_map_assoc,zeroSumIso_leg]

theorem realFreeIso_projection :
    changeInput (probeSet S) (pZero (realPsh I)) (polynomial arity) ≫
      (zeroFreeIso S arity).hom =
    (realFreeIso S I arity).hom ≫ FFree.map (productMap (probeSet S) (realGeneratorProjection I arity)) := by
  change moduleSheafification.map ((indexedFunctor (probeSet S)).map
    (freeOn.map (realGeneratorProjection I arity))) ≫
    moduleSheafification.map (indexedFreeIso (probeSet S) (zeroGeneratorPsh arity)).hom =
    moduleSheafification.map (indexedFreeIso (probeSet S) (realGeneratorPsh I arity)).hom ≫
    moduleSheafification.map (freeOn.map (productMap (probeSet S) (realGeneratorProjection I arity)))
  rw [← Functor.map_comp,← Functor.map_comp,indexedFreeIso_natural]

def realBD (B : UniversalBD.{u}) : FiniteTypeRealResolution S I where
  resolution := transportedResolution B (probeSet S) (realPsh I)
  zeroSplit := transportedZeroSplit B (probeSet S) (realPsh I)
  count := B.count
  arity := B.arity
  termIso n := realFreeIso S I (B.arity n) ≪≫ (realSumIso S I (B.arity n)).symm
  baseIso n := zeroFreeIso S (B.arity n) ≪≫ (zeroSumIso S (B.arity n)).symm
  projection_square n := by
    change changeInput (probeSet S) (pZero (realPsh I)) (polynomial (B.arity n)) ≫
      ((zeroFreeIso S (B.arity n)).hom ≫ (zeroSumIso S (B.arity n)).inv) =
      ((realFreeIso S I (B.arity n)).hom ≫ (realSumIso S I (B.arity n)).inv) ≫ powerProjection S I (B.arity n)
    apply (cancel_mono (zeroSumIso S (B.arity n)).hom).1
    simp only [Category.assoc,Iso.inv_hom_id,Category.comp_id]
    rw [realFreeIso_projection,← realSumIso_projection,Iso.inv_hom_id_assoc]

theorem relativeReal_extZero (B : UniversalBD.{u}) (q : ℕ)
    (e : Abelian.Ext (moduleSheafification.obj (indexedSum (probeSet S) (realPsh I)))
      discreteIntegerCoeff q) : e=0 :=
  (realBD S I B).target_extZero q e

#print axioms realBD
#print axioms relativeReal_extZero
end CMDG.CondensedCM5R0.BreenDeligneProbe
