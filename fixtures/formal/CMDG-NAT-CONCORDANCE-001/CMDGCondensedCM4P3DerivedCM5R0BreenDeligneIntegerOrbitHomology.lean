import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneIntegerOrbits

/-! Positive homology of the actual orbit chains: straightening
kills every higher degree and identifies degree one with displacement. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits HomologicalComplex AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneIntegerVertices
open CMDG.CondensedCM5R0.BreenDeligneIntegerLine
open CMDG.CondensedCM5R0.BreenDeligneIntegerOrbits
open CMDG.CondensedCM5R0.BreenDeligneHomologyElements
open CMDG.CondensedCM5R0.BreenDeligneFiniteBar
namespace CMDG.CondensedCM5R0.BreenDeligneIntegerOrbitHomology

abbrev I := ModuleCat.of ℤ ℤ
abbrev K : Ch := ChainComplex.of B BD (AlternatingFaceMapComplex.d_squared rawBar)
theorem K_d (n : ℕ) : K.d (n+1) n = BD n :=
  ChainComplex.of_d B BD n

def unitEdge : B 1 := bgen (fun _ => 1)

theorem Q_edge (a b : ℤ) :
    Q 1 (gen (BreenDeligneIntegerLine.pair a b)) = bgen (fun _ => b-a) := by
  rw [Q_gen]
  congr 1
  funext i
  have hi : i = 0 := Subsingleton.elim _ _
  subst i
  rfl

theorem Q_linePath (a b : ℤ) : Q 1 (linePath a b) = (b-a) • unitEdge := by
  let P : ℤ → Prop := fun k => Q 1 (linePath a k) = (k-a) • unitEdge
  have h₀ : P a := by simp [P,linePath_self]
  have hs (k : ℤ) : P k ↔ P (k+1) := by
    have h' := congrArg (Q 1) (linePath_add a k (k+1))
    rw [map_add,linePath_step,Q_edge,show k+1-k=1 by omega] at h'
    change Q 1 (linePath a k) + unitEdge = Q 1 (linePath a (k+1)) at h'
    have he : (k+1-a) • unitEdge = (k-a) • unitEdge + unitEdge := by
      rw [show k+1-a=k-a+1 by omega,add_zsmul,one_zsmul]
    dsimp [P]
    rw [he,← h']
    exact ⟨fun h => congrArg (fun x => x+unitEdge) h,add_right_cancel⟩
  have H (k : ℤ) : P (a+k) := by
    induction k using Int.induction_on with
    | zero => simpa only [add_zero] using h₀
    | succ k hk =>
      rw [← add_assoc]
      exact (hs (a+k)).mp hk
    | pred k hk =>
      rw [← sub_eq_add_neg,← add_sub_assoc] at *
      apply (hs (a + -(k : ℤ) - 1)).mpr
      rw [show a + -(k : ℤ) - 1 + 1 = a - (k : ℤ) by omega]
      exact hk
  have he : a+(b-a)=b := by omega
  exact he ▸ H (b-a)

def weight : B 1 ⟶ I := ModuleCat.freeDesc (↾fun x : Fin 1 → ℤ => x 0)
def unitMap : I ⟶ B 1 :=
  ModuleCat.ofHom {
    toFun := fun x => x • unitEdge
    map_add' := fun x y => add_zsmul unitEdge x y
    map_smul' := by intro r x; exact mul_smul r x unitEdge }

theorem e_factor : e 1 = weight ≫ unitMap := by
  apply ModuleCat.free_hom_ext
  intro x
  change e 1 (bgen x) = unitMap (weight (bgen x))
  rw [e_one_gen,Q_linePath,sub_zero]
  have hw : weight (bgen x) = x 0 := ModuleCat.freeDesc_apply _ _
  rw [hw]
  rfl

theorem bd_zero : BD 0 = 0 := by
  apply ModuleCat.free_hom_ext
  intro x
  have h₀ (i : Fin 2) : rawBar.δ i (bgen x) = bgen (fun j : Fin 0 => Fin.elim0 j) := by
    change (ModuleCat.free ℤ).map (↾fun v : Fin 1 → ℤ =>
      (BreenDeligneBarObject.bar BreenDeligneIntegerOrbits.Z).δ i v) (bgen x) = _
    rw [ModuleCat.free_map_apply]
    congr 1
    funext j
    exact Fin.elim0 j
  change BD 0 (bgen x) = 0
  unfold BD AlternatingFaceMapComplex.objD
  rw [Fin.sum_univ_two]
  simp only [Fin.val_zero,Fin.val_one,pow_zero,pow_one,one_smul,neg_one_zsmul]
  change rawBar.δ 0 (bgen x) + -(rawBar.δ 1 (bgen x)) = 0
  rw [h₀,h₀,add_neg_cancel]

theorem weight_boundary : BD 1 ≫ weight = 0 := by
  apply (cancel_epi (Q 2)).mp
  rw [← Category.assoc,← Q_D,Category.assoc,comp_zero]
  apply ModuleCat.free_hom_ext
  intro v
  change weight (Q 1 (D 1 (gen v))) = 0
  rw [D_gen,map_sum,map_sum,Fin.sum_univ_succ,Fin.sum_univ_two]
  simp only [map_smul,Q_gen]
  have hw (x : Fin 1 → ℤ) : weight (bgen x) = x 0 := ModuleCat.freeDesc_apply _ _
  simp only [hw,Fin.val_zero,Fin.val_succ,Fin.val_one,pow_zero,pow_succ,mul_neg,mul_one,
    neg_neg,one_smul,neg_one_zsmul]
  change (v 2-v 1) + (-(v 2-v 0) + (v 1-v 0)) = 0
  abel

theorem high_zero (n : ℕ) (x : K.homology (n+2)) : x = 0 := by
  obtain ⟨z,rfl⟩ := class_surj K (n+2) x
  apply (class_zero_iff K (n+2) z).mpr
  refine ⟨h (n+2) (K.iCycles (n+2) z),?_⟩
  have he := CategoryTheory.congr_fun (h_identity (n+1)) (K.iCycles (n+2) z)
  change BD (n+2) (h (n+2) (K.iCycles (n+2) z)) +
      h (n+1) (BD (n+1) (K.iCycles (n+2) z)) =
    K.iCycles (n+2) z - e (n+2) (K.iCycles (n+2) z) at he
  have hz := cycle_closed K (n+2) z
  change K.d (n+2) (n+1) (K.iCycles (n+2) z) = 0 at hz
  rw [K_d] at hz
  rw [hz,map_zero,add_zero,e_high] at he
  change BD (n+2) (h (n+2) (K.iCycles (n+2) z)) =
    K.iCycles (n+2) z - 0 at he
  rw [sub_zero] at he
  rw [K_d]
  exact he

def unitCycle : K.cycles 1 :=
  cycleOf K 1 unitEdge (by change K.d 1 0 unitEdge=0; rw [K_d,bd_zero]; rfl)

def unitClass : K.homology 1 := K.homologyπ 1 unitCycle

theorem one_cyclic (x : K.homology 1) : ∃ k : ℤ, x = k • unitClass := by
  obtain ⟨z,rfl⟩ := class_surj K 1 x
  let k := weight (K.iCycles 1 z)
  refine ⟨k,?_⟩
  have he := CategoryTheory.congr_fun (h_identity 0) (K.iCycles 1 z)
  change BD 1 (h 1 (K.iCycles 1 z)) + h 0 (BD 0 (K.iCycles 1 z)) =
    K.iCycles 1 z - e 1 (K.iCycles 1 z) at he
  rw [bd_zero] at he
  change BD 1 (h 1 (K.iCycles 1 z)) + h 0 0 =
    K.iCycles 1 z - e 1 (K.iCycles 1 z) at he
  rw [map_zero,add_zero,e_factor] at he
  change BD 1 (h 1 (K.iCycles 1 z)) = K.iCycles 1 z - k • unitEdge at he
  have hc : K.iCycles 1 unitCycle = unitEdge := cycleOf_i _ _ _ _
  have h' := class_eq_of_boundary_diff K 1 z (k • unitCycle)
    (h 1 (K.iCycles 1 z)) (by rw [K_d,map_zsmul,hc]; exact he)
  rw [map_zsmul] at h'
  exact h'

theorem one_finite : Module.Finite ℤ (K.homology 1) := by
  let f : ℤ →ₗ[ℤ] K.homology 1 :=
    BreenDeligneFiniteTotal.intLinear {
      toFun := fun k => k • unitClass
      map_zero' := zero_zsmul _
      map_add' := fun a b => add_zsmul unitClass a b }
  exact Module.Finite.of_surjective f (fun x => by
    obtain ⟨k,hk⟩ := one_cyclic x
    exact ⟨k,hk.symm⟩)

theorem finite_all (n : ℕ) : Module.Finite ℤ (K.homology n) := by
  rcases n with _ | (_ | n)
  · haveI : Module.Finite ℤ (K.X 0) := by
      change Module.Finite ℤ ((Fin 0 → ℤ) →₀ ℤ)
      letI : Finite (Fin 0 → ℤ) := Finite.of_subsingleton
      infer_instance
    exact BreenDeligneFiniteTensor.finiteHomology K 0
  · exact one_finite
  · haveI : Subsingleton (K.homology (n+2)) := ⟨fun x y =>
        (high_zero n x).trans (high_zero n y).symm⟩
    infer_instance

#print axioms high_zero
#print axioms one_cyclic
#print axioms finite_all
end CMDG.CondensedCM5R0.BreenDeligneIntegerOrbitHomology
