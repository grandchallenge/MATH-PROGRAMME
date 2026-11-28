import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneLatticeFP

/-! The genuine augmented, shifted Eilenberg–Mac Lane lattice chain
complex. The bottom augmentation is the established Hurewicz map. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneBottomInjectivity
open CMDG.CondensedCM5R0.BreenDeligneLatticeProjectives
open CMDG.CondensedCM5R0.BreenDeligneFiniteTermProjectives
open CMDG.CondensedCM5R0.BreenDeligneLatticeFP
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
namespace CMDG.CondensedCM5R0.BreenDeligneLatticeAugmentation

local instance toZ_equivalence : toZModule.IsEquivalence := by
  let U := BreenDeligneAdditiveNextMap.U
  haveI : U.IsEquivalence := inferInstance
  haveI : (toZModule ⋙ U).IsEquivalence :=
    (Functor.isEquivalence_iff_of_iso BreenDeligneAdditiveNextMap.forgetToZIso).mpr inferInstance
  exact Functor.isEquivalence_of_comp_right toZModule U

abbrev C (A : AGrp) (n : ℕ) := (reducedEMChains n).obj A
def augAt (A : AGrp) (n : ℕ) : (C A n).X n ⟶ A :=
  ((bottomAugmentation n).app A).f n ≫ (singleObjXSelf c n A).hom

theorem augAt_natural (n : ℕ) {A B : AGrp} (f : A ⟶ B) :
    ((reducedEMChains n).map f).f n ≫ augAt B n = augAt A n ≫ f := by
  have h := congrArg (fun g => g.f n) ((bottomAugmentation n).naturality f)
  change ((reducedEMChains n).map f).f n ≫ ((bottomAugmentation n).app B).f n =
    ((bottomAugmentation n).app A).f n ≫ ((singleDegree n).map f).f n at h
  unfold augAt
  rw [← Category.assoc,h,Category.assoc]
  rw [show ((singleDegree n).map f).f n =
    (singleObjXSelf c n A).hom ≫ f ≫ (singleObjXSelf c n B).inv from single_map_f_self c n f]
  simp

theorem augAt_zero (A : AGrp) (n : ℕ) :
    (C A n).d (n+1) n ≫ augAt A n = 0 := by
  have h := ((bottomAugmentation n).app A).comm (n+1) n
  unfold augAt
  rw [← Category.assoc,← h]
  simp [singleDegree]

theorem augAt_epi (A : AGrp) (n : ℕ) : Epi (augAt A n) := by
  letI := bottomAugmentation_degree_epi A n n
  unfold augAt
  infer_instance

def bottomSC (A : AGrp) (n : ℕ) : ShortComplex AGrp :=
  ShortComplex.mk ((C A n).d (n+1) n) (augAt A n) (augAt_zero A n)

theorem bottomSC_exact (A : AGrp) (k : ℕ) : (bottomSC A (k+1)).Exact := by
  let n := k+1
  let K := C A n
  let L := (singleDegree n).obj A
  let f := (bottomAugmentation n).app A
  let e := K.iCyclesIso n _ rfl (reducedBottom_outgoing_zero A n)
  letI := bottomHomologyToGroup_iso A k
  let S := ShortComplex.mk (K.toCycles (n+1) n) (K.homologyπ n)
    (K.toCycles_comp_homologyπ _ _)
  have hS : S.Exact := ShortComplex.exact_of_g_is_cokernel _
    (K.homologyIsCokernel (n+1) n ((ComplexShape.down ℕ).prev_eq' (by rfl)))
  have hs : S ≅ bottomSC A n := ShortComplex.isoMk (Iso.refl _) e
    (asIso (bottomHomologyToGroup A n)) (by
      change 𝟙 _ ≫ K.d (n+1) n = K.toCycles (n+1) n ≫ K.iCycles n
      rw [K.toCycles_i,Category.id_comp]) (by
      change K.iCycles n ≫ augAt A n = K.homologyπ n ≫ bottomHomologyToGroup A n
      symm
      unfold bottomHomologyToGroup augAt
      rw [homologyπ_naturality_assoc]
      have hh : L.homologyπ n ≫
          (singleObjHomologySelfIso (ComplexShape.down ℕ) n A).hom =
          L.iCycles n ≫ (singleObjXSelf c n A).hom :=
        homologyπ_singleObjHomologySelfIso_hom (C := AGrp) (c := ComplexShape.down ℕ) (j := n) (A := A)
      rw [hh,← Category.assoc,cyclesMap_i,Category.assoc])
  exact ShortComplex.exact_of_iso hs hS

abbrev Term (n m : ℕ) := latticeChainDegree n m ⋙ toZModule

def latD (n m : ℕ) : Term n (m+1) ⟶ Term n m where
  app r := toZModule.map ((C (lattice r) n).d (m+1) m)
  naturality {r s} f := by
    change toZModule.map (((reducedEMChains n).map (valueFunctor.map f)).f (m+1)) ≫
      toZModule.map ((C (lattice s) n).d (m+1) m) =
      toZModule.map ((C (lattice r) n).d (m+1) m) ≫
        toZModule.map (((reducedEMChains n).map (valueFunctor.map f)).f m)
    rw [← Functor.map_comp,← Functor.map_comp]
    exact congrArg toZModule.map (((reducedEMChains n).map (valueFunctor.map f)).comm (m+1) m)

def latAug (n : ℕ) : Term n n ⟶ V where
  app r := toZModule.map (augAt (lattice r) n)
  naturality {r s} f := by
    change toZModule.map (((reducedEMChains n).map (valueFunctor.map f)).f n) ≫
      toZModule.map (augAt (lattice s) n) =
      toZModule.map (augAt (lattice r) n) ≫ toZModule.map (valueFunctor.map f)
    rw [← Functor.map_comp,← Functor.map_comp]
    exact congrArg toZModule.map (augAt_natural n (valueFunctor.map f))

theorem latAug_epi (n : ℕ) : Epi (latAug n) := by
  apply (NatTrans.epi_iff_epi_app _).mpr
  intro r
  change Epi (toZModule.map (augAt (lattice r) n))
  letI := augAt_epi (lattice r) n
  infer_instance

theorem latAug_zero (n : ℕ) : latD n n ≫ latAug n = 0 := by
  apply NatTrans.ext
  funext r
  change toZModule.map ((C (lattice r) n).d (n+1) n) ≫
    toZModule.map (augAt (lattice r) n) = 0
  rw [← Functor.map_comp,augAt_zero,toZModule.map_zero]

theorem latD_sq (n m : ℕ) : latD n (m+1) ≫ latD n m = 0 := by
  apply NatTrans.ext
  funext r
  change toZModule.map ((C (lattice r) n).d (m+2) (m+1)) ≫
    toZModule.map ((C (lattice r) n).d (m+1) m) = 0
  rw [← Functor.map_comp,HomologicalComplex.d_comp_d,toZModule.map_zero]

def augmentedRow (n : ℕ) : ℕ → LC
  | 0 => V
  | j+1 => Term n (n+j)

def augmentedD (n : ℕ) : (j : ℕ) → augmentedRow n (j+1) ⟶ augmentedRow n j
  | 0 => latAug n
  | j+1 => latD n (n+j)

theorem augmentedSq (n j : ℕ) : augmentedD n (j+1) ≫ augmentedD n j = 0 := by
  cases j with
  | zero => exact latAug_zero n
  | succ j => exact latD_sq n (n+j)

def augmented (n : ℕ) : ChainComplex LC ℕ :=
  ChainComplex.of (augmentedRow n) (augmentedD n) (augmentedSq n)

theorem augmented_d (n j : ℕ) :
    (augmented n).d (j+1) j = augmentedD n j := ChainComplex.of_d _ _ _

theorem augmented_epi (n : ℕ) : Epi ((augmented n).d 1 0) := by
  rw [augmented_d]
  exact latAug_epi n

theorem augmented_bottom_exact (k : ℕ) : ((augmented (k+1)).sc 1).Exact := by
  let K := augmented (k+1)
  have he : (K.sc' 2 1 0).Exact := by
    apply functorShortComplex_exact_of_pointwise
    intro r
    have h := (bottomSC_exact (lattice r) k).map toZModule
    apply ShortComplex.exact_of_iso (ShortComplex.isoMk (Iso.refl _) (Iso.refl _) (Iso.refl _)
      (by simp [K,augmented_d,augmentedD,bottomSC,latD])
      (by simp [K,augmented_d,augmentedD,bottomSC,latAug])) h
  exact ShortComplex.exact_of_iso
    (K.isoSc' 2 1 0 ((ComplexShape.down ℕ).prev_eq' (by decide))
      ((ComplexShape.down ℕ).next_eq' (by decide))).symm he

#print axioms bottomSC_exact
#print axioms augmented_epi
#print axioms augmented_bottom_exact
end CMDG.CondensedCM5R0.BreenDeligneLatticeAugmentation
