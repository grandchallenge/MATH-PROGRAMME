import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneIntegerStraightening

/-! Descend the homogeneous comparison through the actual edge
coordinates. Partial sums select orbit representatives. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBarObject
open CMDG.CondensedCM5R0.BreenDeligneIntegerVertices
open CMDG.CondensedCM5R0.BreenDeligneIntegerLine
open CMDG.CondensedCM5R0.BreenDeligneIntegerStraightening
namespace CMDG.CondensedCM5R0.BreenDeligneIntegerOrbits

abbrev Z := AddCommGrpCat.of ℤ
abbrev rawBar : SimplicialObject ZMod := bar Z ⋙ forget _ ⋙ ModuleCat.free ℤ
abbrev B (n : ℕ) := (ModuleCat.free ℤ).obj (Fin n → ℤ)
abbrev bgen {n : ℕ} (x : Fin n → ℤ) : B n := ModuleCat.freeMk x
abbrev BD (n : ℕ) : B (n+1) ⟶ B n := AlternatingFaceMapComplex.objD rawBar n

def edgeNat : vertices ⟶ bar Z ⋙ forget _ where
  app Δ := ↾fun v => edges v
  naturality {Δ Δ'} f := by
    apply ConcreteCategory.hom_ext
    intro v
    funext i
    change edges (v ∘ f.unop.toOrderHom) i =
      edges (Fin.partialSum (edges v) ∘ f.unop.toOrderHom) i
    change v (f.unop.toOrderHom i.succ) - v (f.unop.toOrderHom i.castSucc) =
      Fin.partialSum (edges v) (f.unop.toOrderHom i.succ) -
      Fin.partialSum (edges v) (f.unop.toOrderHom i.castSucc)
    rw [partialSum_edges,partialSum_edges]
    abel

def QNat : vertices ⋙ ModuleCat.free ℤ ⟶ rawBar :=
  Functor.whiskerRight edgeNat (ModuleCat.free ℤ)
abbrev Q (n : ℕ) : V n ⟶ B n := QNat.app (op (SimplexCategory.mk n))

theorem Q_gen (n : ℕ) (v : Vtx n) : Q n (gen v) = bgen (edges v) :=
  ModuleCat.free_map_apply _ _

theorem Q_D (n : ℕ) : D n ≫ Q n = Q (n+1) ≫ BD n := by
  unfold D BD
  simp only [AlternatingFaceMapComplex.objD,Preadditive.sum_comp,Preadditive.comp_sum,
    Preadditive.zsmul_comp,Preadditive.comp_zsmul]
  apply Finset.sum_congr rfl
  intro i _
  rw [SimplicialObject.δ_naturality QNat i]

def S (n : ℕ) : B n ⟶ V n :=
  (ModuleCat.free ℤ).map (↾fun x : Fin n → ℤ => Fin.partialSum x)
theorem S_gen (n : ℕ) (x : Fin n → ℤ) : S n (bgen x) = gen (Fin.partialSum x) :=
  ModuleCat.free_map_apply _ _

theorem S_Q (n : ℕ) : S n ≫ Q n = 𝟙 _ := by
  apply ModuleCat.free_hom_ext
  intro x
  change Q n (S n (bgen x)) = bgen x
  rw [S_gen,Q_gen,edges_partialSum]

theorem Q_T (a : ℤ) (n : ℕ) : T a n ≫ Q n = Q n := by
  apply ModuleCat.free_hom_ext
  intro v
  change Q n (T a n (gen v)) = Q n (gen v)
  rw [T_gen,Q_gen,Q_gen]
  congr 1
  funext i
  unfold edges tr
  abel

theorem SQ_gen (n : ℕ) (v : Vtx n) :
    S n (Q n (gen v)) = T (-v 0) n (gen v) := by
  rw [Q_gen,S_gen,T_gen]
  congr 1
  funext i
  rw [partialSum_edges]
  unfold tr
  abel

/-- A map commuting with translations descends to the orbit chains. -/
def desc {n m : ℕ} (f : V n ⟶ V m) : B n ⟶ B m :=
  S n ≫ f ≫ Q m

theorem desc_square {n m : ℕ} (f : V n ⟶ V m)
    (hf : ∀ a, f ≫ T a m = T a n ≫ f) :
    Q n ≫ desc f = f ≫ Q m := by
  apply ModuleCat.free_hom_ext
  intro v
  change Q m (f (S n (Q n (gen v)))) = Q m (f (gen v))
  rw [SQ_gen]
  have he := CategoryTheory.congr_fun (hf (-v 0)).symm (gen v)
  change f (T (-v 0) n (gen v)) = T (-v 0) m (f (gen v)) at he
  rw [he]
  exact CategoryTheory.congr_fun (Q_T (-v 0) m) (f (gen v))

instance (n : ℕ) : Epi (Q n) := epi_of_epi_fac (S_Q n)

def e (n : ℕ) : B n ⟶ B n := desc (E n)
def h (n : ℕ) : B n ⟶ B (n+1) := desc (H n)

theorem e_square (n : ℕ) : Q n ≫ e n = E n ≫ Q n :=
  desc_square (E n) (fun a => E_T a n)
theorem h_square (n : ℕ) : Q n ≫ h n = H n ≫ Q (n+1) :=
  desc_square (H n) (fun a => H_T a n)

theorem h_identity (n : ℕ) :
    h (n+1) ≫ BD (n+1) + BD n ≫ h n = 𝟙 _ - e (n+1) := by
  apply (cancel_epi (Q (n+1))).mp
  rw [Preadditive.comp_add,Preadditive.comp_sub,Category.comp_id,
    ← Category.assoc, h_square,Category.assoc,← Q_D,
    ← Category.assoc (Q (n+1)) (BD n) (h n),← Q_D,Category.assoc,h_square,
    ← Category.assoc (D n) (H n) (Q (n+1)),← Category.assoc (H (n+1)) (D (n+1)) (Q (n+1)),← Preadditive.add_comp,H_identity,
    Preadditive.sub_comp,Category.id_comp,e_square]

theorem e_high (n : ℕ) : e (n+2) = 0 := by simp [e,desc,E]

theorem e_one_gen (x : Fin 1 → ℤ) :
    e 1 (bgen x) = Q 1 (linePath 0 (x 0)) := by
  change Q 1 (E 1 (S 1 (bgen x))) = _
  rw [S_gen,E_one]
  have he : Fin.partialSum x (1 : Fin 2) = x 0 := by
    change Fin.partialSum x (0 : Fin 1).succ = x 0
    rw [Fin.partialSum_succ]
    simp
  rw [he]
  rfl

#print axioms h_identity
#print axioms e_high
end CMDG.CondensedCM5R0.BreenDeligneIntegerOrbits
