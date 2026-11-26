import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneIntervalPrism

/-! A homotopy of the actual Moore maps yields an additive simplicial
homotopy. Arbitrary functors, in particular reducedFree, preserve it. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneAdditiveNextMap
open CMDG.CondensedCM5R0.BreenDeligneIntervalPrism
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneMooreHomotopyTransport

abbrev N := normalizedMooreComplex AGrp
abbrev K := alternatingFaceMapComplex AGrp
abbrev inc (X : SimplicialObject AGrp) := inclusionOfMooreComplexMap X
abbrev prj (X : SimplicialObject AGrp) := AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex X
variable {X Y : SimplicialObject AGrp} {f g : X ⟶ Y}

set_option backward.isDefEq.respectTransparency false in
def altFactorHomotopy (f : X ⟶ Y) :
    Homotopy (prj X ≫ N.map f ≫ inc Y) (K.map f) := by
  have he : N.map f ≫ inc Y = inc X ≫ K.map f :=
    (inclusionOfMooreComplex AGrp).naturality f
  rw [he,← Category.assoc]
  have hp : prj X ≫ inc X = AlgebraicTopology.DoldKan.PInfty :=
    AlgebraicTopology.DoldKan.PInftyToNormalizedMooreComplex_comp_inclusionOfMooreComplexMap X
  rw [hp]
  exact (AlgebraicTopology.DoldKan.homotopyPInftyToId X).compRightId (K.map f)

def alternatingFromMoore (H : Homotopy (N.map f) (N.map g)) :
    Homotopy (K.map f) (K.map g) :=
  (altFactorHomotopy f).symm.trans
    (((H.compRight (inc Y)).compLeft (prj X)).trans (altFactorHomotopy g))

abbrev Z := (SimplicialObject.whiskering AGrp ZMod).obj toZModule
abbrev ZK := alternatingFaceMapComplex ZMod

def mapAlternatingHomotopy (H : Homotopy (K.map f) (K.map g)) :
    Homotopy (ZK.map (Z.map f)) (ZK.map (Z.map g)) := by
  let P : SimplicialObject AGrp ⥤ Ch := K ⋙ toZModule.mapHomologicalComplex c
  let Q : SimplicialObject AGrp ⥤ Ch := Z ⋙ ZK
  have h : P=Q := AlgebraicTopology.map_alternatingFaceMapComplex toZModule
  have hP : Homotopy (P.map f) (P.map g) := toZModule.mapHomotopy H
  rw [h] at hP
  exact hP

def groupIso (X : SimplicialObject AGrp) : X ⋙ toZModule ⋙ U ≅ X :=
  Functor.isoWhiskerLeft X forgetToZIso ≪≫ Functor.rightUnitor X

def simplicialFromMoore (H : Homotopy (N.map f) (N.map g)) :
    SimplicialObject.Homotopy f g := by
  let h := (simplicialFromAlternating (mapAlternatingHomotopy (alternatingFromMoore H))).whiskerRight U
  let h' := (h.precomp (groupIso X).inv).postcomp (groupIso Y).hom
  have he (k : X ⟶ Y) :
      ((groupIso X).inv ≫ ((SimplicialObject.whiskering ZMod AGrp).obj U).map (Z.map k)) ≫
        (groupIso Y).hom = k := by
    apply NatTrans.ext
    funext a
    apply ConcreteCategory.hom_ext
    intro x
    rfl
  exact he f ▸ he g ▸ h'

abbrev reducedFunctor := (SimplicialObject.whiskering AGrp ZMod).obj (reducedFree ⋙ toZModule)

def reducedFromMoore (H : Homotopy (N.map f) (N.map g)) :
    Homotopy (ZK.map (reducedFunctor.map f)) (ZK.map (reducedFunctor.map g)) :=
  ((simplicialFromMoore H).whiskerRight (reducedFree ⋙ toZModule)).toChainHomotopy

#print axioms alternatingFromMoore
#print axioms simplicialFromMoore
#print axioms reducedFromMoore
end CMDG.CondensedCM5R0.BreenDeligneMooreHomotopyTransport
