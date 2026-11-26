import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneStableMatrix
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneSuspensionDegree

/-! Natural stabilization on the finite lattice skeleton, transported
from the actual rank-one stable suspension through natural matrix
coordinates. This does not assert equality with the geometric
suspension at every rank. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneLatticeProjectives
open CMDG.CondensedCM5R0.BreenDeligneStableAdditive
open CMDG.CondensedCM5R0.BreenDeligneStableLattice
open CMDG.CondensedCM5R0.BreenDeligneStableMatrix
open CMDG.CondensedCM5R0.BreenDeligneReducedNext
open CMDG.CondensedCM5R0.BreenDeligneSuspensionDegree
namespace CMDG.CondensedCM5R0.BreenDeligneLatticeStabilization

def rankOneIso (n k : ℕ) (hk : k<n) :
    (stableFunctor n k).obj Z ≅ (stableFunctor (n+1) k).obj Z :=
  homologyMapIso (reducedEMChainIso Z n) (n+k) ≪≫
    stableSuspension Z n k hk ≪≫
    eqToIso (congrArg (fun j : ℕ => (reducedChainsZ Z (n+1)).homology j)
      (by omega : n+k+1=n+1+k)) ≪≫
    (homologyMapIso (reducedEMChainIso Z (n+1)) (n+1+k)).symm

def coordinateMap {M N : ZMod} (f : M ⟶ N) (r : ℕ) :
    coordModule M r ⟶ coordModule N r := by
  letI : Module ℤ (coordModule M r) := (coordModule M r).isModule
  letI : Module ℤ (coordModule N r) := (coordModule N r).isModule
  exact ConcreteCategory.ofHom (C := ZMod) (X := coordModule M r) (Y := coordModule N r) {
    toFun := fun x i => f (x i)
    map_add' := by intro x y; funext i; exact map_add f.hom (x i) (y i)
    map_smul' := by intro a x; funext i; exact f.hom.map_smul a (x i) }

def coordinateMapIso {M N : ZMod} (e : M ≅ N) (r : ℕ) :
    coordModule M r ≅ coordModule N r where
  hom := coordinateMap e.hom r
  inv := coordinateMap e.inv r
  hom_inv_id := by
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    exact CategoryTheory.congr_fun e.hom_inv_id (x i)
  inv_hom_id := by
    apply ConcreteCategory.hom_ext
    intro x
    funext i
    exact CategoryTheory.congr_fun e.inv_hom_id (x i)

def latticeComponent (n k : ℕ) (hk : k<n) (r : Latt) :
    (valueFunctor ⋙ stableFunctor n k).obj r ≅
      (valueFunctor ⋙ stableFunctor (n+1) k).obj r :=
  stableLatticeIso n k r hk ≪≫ coordinateMapIso (rankOneIso n k hk) r ≪≫
    (stableLatticeIso (n+1) k r (by omega)).symm

set_option backward.isDefEq.respectTransparency false in
def latticeStabilization (n k : ℕ) (hk : k<n) :
    valueFunctor ⋙ stableFunctor n k ≅ valueFunctor ⋙ stableFunctor (n+1) k :=
  NatIso.ofComponents (latticeComponent n k hk) (fun {r s} f => by
    let F := stableFunctor n k
    let G := stableFunctor (n+1) k
    let e := rankOneIso n k hk
    let a (t : Latt) := stableLatticeIso n k t hk
    let b (t : Latt) := stableLatticeIso (n+1) k t (by omega)
    let g := valueFunctor.map f
    apply (cancel_mono (b s).hom).mp
    apply ConcreteCategory.hom_ext
    intro x
    funext j
    change (b s).hom ((latticeComponent n k hk s).hom (F.map g x)) j =
      (b s).hom (G.map g ((latticeComponent n k hk r).hom x)) j
    have hc (t : Latt) (y : F.obj (lattice t)) (i : Fin t) :
        (b t).hom ((latticeComponent n k hk t).hom y) i =
          e.hom ((a t).hom y i) := by
      change (b t).hom ((b t).inv (coordinateMap e.hom t ((a t).hom y))) i = _
      have hh := CategoryTheory.congr_fun (b t).inv_hom_id (coordinateMap e.hom t ((a t).hom y))
      change (b t).hom ((b t).inv _) = _ at hh
      rw [hh]
      rfl
    rw [hc]
    have hF := stableMatrix n k hk g x j
    have hG := stableMatrix (n+1) k (by omega) g ((latticeComponent n k hk r).hom x) j
    change (a s).hom (F.map g x) j = _ at hF
    change (b s).hom (G.map g ((latticeComponent n k hk r).hom x)) j = _ at hG
    rw [hF,hG]
    change e.hom.hom (∑ i : Fin r, entry g j i • ((a r).hom x i)) = _
    rw [map_sum]
    apply Finset.sum_congr rfl
    intro i _
    change e.hom.hom (entry g j i • ((a r).hom x i)) = entry g j i • (b r).hom ((latticeComponent n k hk r).hom x) i
    rw [hc]
    exact map_zsmul e.hom.hom _ _)

#print axioms rankOneIso
#print axioms latticeStabilization
end CMDG.CondensedCM5R0.BreenDeligneLatticeStabilization
