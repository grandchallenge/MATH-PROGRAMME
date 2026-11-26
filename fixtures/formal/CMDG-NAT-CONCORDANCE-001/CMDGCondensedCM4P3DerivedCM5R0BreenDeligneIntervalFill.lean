import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneInterval

/-! A chain homotopy fills the free interval total complex. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology HomologicalComplex
open scoped CategoryTheory.Prod
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.EilenbergZilberMaps
open CMDG.CondensedCM5R0.EilenbergZilberAW
open CMDG.CondensedCM5R0.EilenbergZilberTotalHomotopy
open CMDG.CondensedCM5R0.BreenDeligneInterval
namespace CMDG.CondensedCM5R0.BreenDeligneIntervalFill

abbrev alt (X : SimplicialObject ZMod) := (alternatingFaceMapComplex ZMod).obj X
variable {X Y : SimplicialObject ZMod} {f g : alt X ⟶ alt Y}

def part (H : Homotopy f g) (p q n : ℕ) (h : p+q=n) (t : I (d p)) :
    X.obj (d q) ⟶ (alt Y).X n := by
  cases p with
  | zero =>
    exact (if firstValue t=0 then f.f q else g.f q) ≫ eqToHom (congrArg (alt Y).X (by omega : q=n))
  | succ p =>
    cases p with
    | zero =>
      exact (if t=𝟙 (SimplexCategory.mk 1) then -H.hom q (q+1) else 0) ≫
        eqToHom (congrArg (alt Y).X (by omega : q+1=n))
    | succ p => exact 0

@[simp] theorem part_zero (H : Homotopy f g) (q : ℕ) (t : I (d 0)) :
    part H 0 q q (by omega) t = if firstValue t=0 then f.f q else g.f q := by
  simp [part]
@[simp] theorem part_one (H : Homotopy f g) (q : ℕ) (t : I (d 1)) :
    part H 1 q (q+1) (by omega) t = if t=𝟙 (SimplexCategory.mk 1) then -H.hom q (q+1) else 0 := by
  simp [part]
@[simp] theorem part_high (H : Homotopy f g) (p q n : ℕ) (h : p+2+q=n) (t : I (d (p+2))) :
    part H (p+2) q n h t = 0 := rfl

def fillDegree (H : Homotopy f g) (n : ℕ) :
    (total (cylinderBi X)).X n ⟶ (alt Y).X n :=
  (double (cylinderBi X)).totalDesc (fun p q h =>
    Sigma.desc (fun t : I (d p) => part H p q n h t))

set_option backward.isDefEq.respectTransparency false in
@[reassoc]
theorem fill_summand (H : Homotopy f g) (p q n : ℕ) (h : p+q=n) (t : I (d p)) :
    inj X (d p) (d q) t ≫ (double (cylinderBi X)).ιTotal c p q n h ≫ fillDegree H n =
      part H p q n h t := by
  unfold fillDegree
  rw [HomologicalComplex₂.ι_totalDesc]
  exact Sigma.ι_desc _ _

theorem face_zero_vertex (v : Fin 2) (i : Fin 2) :
    firstValue (SimplexCategory.δ i ≫ vertex (d 1) v) = v := rfl

theorem face_zero_id (i : Fin 2) :
    firstValue (SimplexCategory.δ i ≫ 𝟙 (SimplexCategory.mk 1)) =
      if i=0 then 1 else 0 := by
  fin_cases i <;> rfl

theorem vertex_ne_id (v : Fin 2) : vertex (d 1) v ≠ 𝟙 (SimplexCategory.mk 1) := by
  intro h
  have h0 := congrArg (fun k : I (d 1) => k.toOrderHom 0) h
  have h1 := congrArg (fun k : I (d 1) => k.toOrderHom 1) h
  change v=0 at h0
  change v=1 at h1
  rw [h0] at h1
  exact (by decide : (0 : Fin 2) ≠ 1) h1

theorem face_two_coeff (t : I (d 2)) :
    (if SimplexCategory.δ (0 : Fin 3) ≫ t = 𝟙 (SimplexCategory.mk 1) then (1:ℤ) else 0) -
    (if SimplexCategory.δ (1 : Fin 3) ≫ t = 𝟙 (SimplexCategory.mk 1) then 1 else 0) +
    (if SimplexCategory.δ (2 : Fin 3) ≫ t = 𝟙 (SimplexCategory.mk 1) then 1 else 0) = 0 := by
  have hc (i : Fin 3) (a b : Fin 3) (h₀ : (SimplexCategory.δ i).toOrderHom 0=a)
      (h₁ : (SimplexCategory.δ i).toOrderHom 1=b) :
      SimplexCategory.δ i ≫ t = 𝟙 (SimplexCategory.mk 1) ↔
        t.toOrderHom a=0 ∧ t.toOrderHom b=1 := by
    constructor
    · intro h
      have h0 := congrArg (fun k : I (d 1) => k.toOrderHom 0) h
      have h1 := congrArg (fun k : I (d 1) => k.toOrderHom 1) h
      change t.toOrderHom ((SimplexCategory.δ i).toOrderHom 0)=0 at h0
      change t.toOrderHom ((SimplexCategory.δ i).toOrderHom 1)=1 at h1
      rw [h₀] at h0
      rw [h₁] at h1
      exact ⟨h0,h1⟩
    · intro h
      apply SimplexCategory.Hom.ext
      apply OrderHom.ext
      funext j
      fin_cases j
      · change t.toOrderHom ((SimplexCategory.δ i).toOrderHom 0)=0
        rw [h₀,h.1]
      · change t.toOrderHom ((SimplexCategory.δ i).toOrderHom 1)=1
        rw [h₁,h.2]
  rw [if_congr (hc 0 1 2 rfl rfl) rfl rfl,
    if_congr (hc 1 0 2 rfl rfl) rfl rfl,
    if_congr (hc 2 0 1 rfl rfl) rfl rfl]
  have h01 := t.toOrderHom.monotone (show (0 : Fin 3) ≤ 1 by decide)
  have h12 := t.toOrderHom.monotone (show (1 : Fin 3) ≤ 2 by decide)
  generalize t.toOrderHom 0 = a at *
  generalize t.toOrderHom 1 = b at *
  generalize t.toOrderHom 2 = e at *
  fin_cases a <;> fin_cases b <;> fin_cases e <;> simp_all

#print axioms fill_summand
#print axioms face_two_coeff
end CMDG.CondensedCM5R0.BreenDeligneIntervalFill
