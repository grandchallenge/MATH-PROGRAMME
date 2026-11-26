import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneStableLattice

/-! Natural matrix coordinates on finite lattices; the rank-one
coefficient determines every morphism, not merely the object ranks. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneLatticeProjectives
open CMDG.CondensedCM5R0.BreenDeligneStableAdditive
open CMDG.CondensedCM5R0.BreenDeligneStableLattice
namespace CMDG.CondensedCM5R0.BreenDeligneStableMatrix

def basisVector (r : ℕ) (i : Fin r) : lattice r := Pi.single i 1

def entry {r s : ℕ} (f : lattice r ⟶ lattice s) (j : Fin s) (i : Fin r) : ℤ :=
  f (basisVector r i) j

theorem basis_expansion (r : ℕ) (x : lattice r) :
    ∑ i : Fin r, x i • basisVector r i = x := by
  change (∑ i : Fin r, x i • Pi.single i (1:ℤ)) = x
  funext j
  rw [Finset.sum_apply,Finset.sum_eq_single j]
  · simp
  · intro i _ hi
    simp [Pi.single_eq_of_ne hi.symm]
  · simp

set_option backward.isDefEq.respectTransparency false in
theorem coordinate_expansion {r s : ℕ} (f : lattice r ⟶ lattice s) (j : Fin s) :
    f ≫ coordinate s j = ∑ i : Fin r, entry f j i • coordinate r i := by
  apply AddCommGrpCat.hom_ext
  ext x
  change f x j = _
  have h := congrArg (fun y : lattice r => f y j) (basis_expansion r x)
  have he : f (∑ i : Fin r, x i • basisVector r i) j =
      ∑ i : Fin r, x i * entry f j i := by
    rw [map_sum]
    change (∑ i : Fin r, f (x i • basisVector r i)) j = _
    rw [Finset.sum_apply]
    apply Finset.sum_congr rfl
    intro i _
    rw [map_zsmul]
    rfl
  rw [he] at h
  rw [← h]
  change ∑ i : Fin r, x i * entry f j i =
    AddCommGrpCat.homAddEquiv (∑ i : Fin r, entry f j i • coordinate r i) x
  rw [map_sum]
  change _ = (AddMonoidHom.eval x) (∑ i : Fin r, AddCommGrpCat.homAddEquiv (entry f j i • coordinate r i))
  rw [map_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [map_zsmul,map_zsmul]
  change _ = entry f j i * x i
  exact mul_comm _ _

set_option backward.isDefEq.respectTransparency false in
theorem matrix_action (F : AGrp ⥤ ZMod) [F.Additive] {r s : ℕ}
    (f : lattice r ⟶ lattice s) (x : F.obj (lattice r)) (j : Fin s) :
    (coordinateIso F s).hom (F.map f x) j =
      ∑ i : Fin r, entry f j i • ((coordinateIso F r).hom x i) := by
  rw [coordinateIso_apply]
  have h := CategoryTheory.congr_fun (F.map_comp f (coordinate s j)) x
  change F.map (f ≫ coordinate s j) x = F.map (coordinate s j) (F.map f x) at h
  rw [← h,coordinate_expansion,F.map_sum]
  change (∑ i : Fin r, F.map (entry f j i • coordinate r i)) x = _
  rw [show (∑ i : Fin r, F.map (entry f j i • coordinate r i)) =
    ∑ i : Fin r, entry f j i • F.map (coordinate r i) by simp only [Functor.map_zsmul]]
  change (∑ i : Fin r, entry f j i • F.map (coordinate r i)).hom x = _
  rw [ModuleCat.hom_sum]
  rw [LinearMap.sum_apply]
  apply Finset.sum_congr rfl
  intro i _
  rw [coordinateIso_apply]
  rfl

theorem stableMatrix (n k : ℕ) (hk : k<n) {r s : ℕ}
    (f : lattice r ⟶ lattice s) (x : (stableFunctor n k).obj (lattice r)) (j : Fin s) :
    (stableLatticeIso n k s hk).hom ((stableFunctor n k).map f x) j =
      ∑ i : Fin r, entry f j i • ((stableLatticeIso n k r hk).hom x i) := by
  letI := stableFunctor_additive n k hk
  exact matrix_action (stableFunctor n k) f x j

#print axioms coordinate_expansion
#print axioms matrix_action
#print axioms stableMatrix
end CMDG.CondensedCM5R0.BreenDeligneStableMatrix
