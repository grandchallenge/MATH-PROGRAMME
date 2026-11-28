import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneLatticeAugmentation

/-! Natural homology comparison of the shifted augmented lattice
complex with the actual stable homology functors. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits HomologicalComplex AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneLatticeProjectives
open CMDG.CondensedCM5R0.BreenDeligneLatticeFP
open CMDG.CondensedCM5R0.BreenDeligneLatticeAugmentation
open CMDG.CondensedCM5R0.BreenDeligneStableAdditive
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneLatticeHomology

def evalSC (S : ShortComplex LC) : Latt ⥤ ShortComplex ZMod where
  obj r := S.map ((evaluation Latt ZMod).obj r)
  map f := S.mapNatTrans ((evaluation Latt ZMod).map f)
  map_id r := by
    apply ShortComplex.hom_ext
    · exact S.X₁.map_id r
    · exact S.X₂.map_id r
    · exact S.X₃.map_id r
  map_comp f g := by
    apply ShortComplex.hom_ext
    · exact S.X₁.map_comp f g
    · exact S.X₂.map_comp f g
    · exact S.X₃.map_comp f g

def evalHomologyIso (S : ShortComplex LC) :
    evalSC S ⋙ ShortComplex.homologyFunctor ZMod ≅ S.homology :=
  NatIso.ofComponents (fun r => S.mapHomologyIso ((evaluation Latt ZMod).obj r))
    (fun {r s} f => by
      have he := NatTrans.app_homology ((evaluation Latt ZMod).map f) S
      change S.homology.map f = _ at he
      change ShortComplex.homologyMap (S.mapNatTrans ((evaluation Latt ZMod).map f)) ≫
        (S.mapHomologyIso ((evaluation Latt ZMod).obj s)).hom =
        (S.mapHomologyIso ((evaluation Latt ZMod).obj r)).hom ≫ S.homology.map f
      rw [he,Iso.hom_inv_id_assoc])

abbrev orig (n : ℕ) : Latt ⥤ Ch :=
  valueFunctor ⋙ reducedEMChains n ⋙ toZModule.mapHomologicalComplex c

theorem orig_eq (n : ℕ) : orig n = valueFunctor ⋙ em n ⋙ redFunctor := by
  change valueFunctor ⋙ em n ⋙ (SimplicialObject.whiskering AGrp AGrp).obj reducedFree ⋙
      (alternatingFaceMapComplex AGrp ⋙ toZModule.mapHomologicalComplex c) = _
  rw [AlgebraicTopology.map_alternatingFaceMapComplex toZModule]
  rfl

abbrev highSC (n j : ℕ) := (augmented n).sc' (j+3) (j+2) (j+1)
abbrev origSC (n j : ℕ) := orig n ⋙
  shortComplexFunctor' ZMod c (n+j+2) (n+j+1) (n+j)

def highSCComponent (n j : ℕ) (r : Latt) :
    (evalSC (highSC n j)).obj r ≅ (origSC n j).obj r :=
  ShortComplex.isoMk (Iso.refl _) (Iso.refl _) (Iso.refl _)
    (by
      simp only [Iso.refl_hom,Category.id_comp,Category.comp_id]
      change toZModule.map ((C (lattice r) n).d (n+j+2) (n+j+1)) =
        ((augmented n).d (j+3) (j+2)).app r
      rw [augmented_d]
      rfl)
    (by
      simp only [Iso.refl_hom,Category.id_comp,Category.comp_id]
      change toZModule.map ((C (lattice r) n).d (n+j+1) (n+j)) =
        ((augmented n).d (j+2) (j+1)).app r
      rw [augmented_d]
      rfl)

def highSCIso (n j : ℕ) : evalSC (highSC n j) ≅ origSC n j :=
  NatIso.ofComponents (highSCComponent n j) (fun {r s} f => by
    apply ShortComplex.hom_ext
    · simp only [ShortComplex.comp_τ₁]
      rfl
    · simp only [ShortComplex.comp_τ₂]
      rfl
    · simp only [ShortComplex.comp_τ₃]
      rfl)

def shiftedHomologyIso (n j : ℕ) :
    (augmented n).homology (j+2) ≅ valueFunctor ⋙ stableFunctor n (j+1) := by
  let K := augmented n
  let e := K.isoSc' (j+3) (j+2) (j+1) ((ComplexShape.down ℕ).prev_eq' (by rfl))
    ((ComplexShape.down ℕ).next_eq' (by rfl))
  let e' := natIsoSc' ZMod c (n+j+2) (n+j+1) (n+j)
    ((ComplexShape.down ℕ).prev_eq' (by rfl)) ((ComplexShape.down ℕ).next_eq' (by rfl))
  refine ShortComplex.homologyMapIso e ≪≫ (evalHomologyIso (highSC n j)).symm ≪≫
    Functor.isoWhiskerRight (highSCIso n j) (ShortComplex.homologyFunctor ZMod) ≪≫
    Functor.isoWhiskerRight (Functor.isoWhiskerLeft (orig n) e'.symm)
      (ShortComplex.homologyFunctor ZMod) ≪≫ ?_
  apply eqToIso
  change orig n ⋙ homologyFunctor ZMod c (n+j+1) = _
  rw [orig_eq]
  have he : n+j+1=n+(j+1) := by omega
  rw [he]
  rfl

#print axioms evalHomologyIso
#print axioms shiftedHomologyIso
end CMDG.CondensedCM5R0.BreenDeligneLatticeHomology
