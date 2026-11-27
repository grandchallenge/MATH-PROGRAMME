import CMDGCondensedCM4P3DerivedCM5R0OrderedGridPrism

/-! All-positive scalar exactness on rectangular ordered cell grids.
The primitive is constructed by successive coordinatewise clamps, using
the signed list prism. The size and number of coordinates are arbitrary. -/
noncomputable section
universe u
namespace CMDG.CondensedCM5R0.CompactCover.OrderedGrid

variable {I : Type u}
abbrev Vertex (I : Type u) := I → ℕ

def valid (M : ℕ) (xs : List (Vertex I)) : Prop :=
  (∀ v ∈ xs, ∀ i, v i ≤ M) ∧
  (∀ v ∈ xs, ∀ w ∈ xs, ∀ i, v i ≤ w i + 1)

def clamp (k : ℕ) (v : Vertex I) : Vertex I := fun i => min k (v i)

theorem valid_faces {M : ℕ} {xs ys : List (Vertex I)}
    (hx : valid M xs) (hy : ys ∈ faces xs) : valid M ys :=
  ⟨fun v hv i => hx.1 v (face_subset hy v hv) i,
   fun v hv w hw i => hx.2 v (face_subset hy v hv) w (face_subset hy w hw) i⟩

theorem min_adjacent (a b k l : ℕ) (hab : a ≤ b+1) (hkl : k ≤ l+1) :
    min k a ≤ min l b + 1 := by omega

theorem valid_prism {M k : ℕ} {xs ys : List (Vertex I)}
    (hx : valid M xs) (hy : ys ∈ prisms (clamp k) (clamp (k+1)) xs) :
    valid M ys := by
  constructor
  · intro v hv i
    obtain ⟨w,hw,h⟩ := prism_vertices hy v hv
    rcases h with rfl | rfl <;> exact (min_le_right _ _).trans (hx.1 w hw i)
  · intro v hv w hw i
    obtain ⟨a,ha,hv'⟩ := prism_vertices hy v hv
    obtain ⟨b,hb,hw'⟩ := prism_vertices hy w hw
    rcases hv' with rfl | rfl <;> rcases hw' with rfl | rfl <;>
      exact min_adjacent _ _ _ _ (hx.2 a ha b hb i) (by omega)

theorem valid_zero (M : ℕ) (xs : List (Vertex I)) :
    valid M ((fun _ : I => 0) :: xs.map (clamp 0)) := by
  have hz : ∀ v ∈ ((fun _ : I => 0) :: xs.map (clamp 0)), v = fun _ => 0 := by
    intro v hv
    simp only [List.mem_cons,List.mem_map] at hv
    rcases hv with rfl | ⟨w,hw,rfl⟩
    · rfl
    · funext i; simp [clamp]
  exact ⟨fun v hv i => by rw [hz v hv]; exact Nat.zero_le _,
    fun v hv w hw i => by rw [hz v hv,hz w hw]; omega⟩

theorem clamp_self_on_valid {M : ℕ} {xs : List (Vertex I)} (hx : valid M xs) :
    xs.map (clamp M) = xs := by
  have h : xs.map (clamp M) = xs.map id := by
    apply List.map_congr_left
    intro v hv
    funext i
    exact min_eq_right (hx.1 v hv i)
  simpa using h

def primitive (c : List (Vertex I) → ℤ) : ℕ → List (Vertex I) → ℤ
  | 0 => fun xs => c ((fun _ => 0) :: xs.map (clamp 0))
  | k+1 => fun xs => primitive c k xs + H (clamp k) (clamp (k+1)) c xs

theorem primitive_identity (M n : ℕ) (c : List (Vertex I) → ℤ)
    (hc : ∀ xs, valid M xs → xs.length = n+3 → D c xs = 0)
    (k : ℕ) (xs : List (Vertex I)) (hx : valid M xs) (hl : xs.length = n+2) :
    D (primitive c k) xs = c (xs.map (clamp k)) := by
  induction k with
  | zero =>
    have hz := hc ((fun _ => 0) :: xs.map (clamp 0)) (valid_zero M xs) (by simp [hl])
    rw [D_cons, D_map] at hz
    exact (sub_eq_zero.mp hz).symm
  | succ k ih =>
    have hz : H (clamp k) (clamp (k+1)) (D c) xs = 0 := by
      unfold H
      rw [← alt_zero (prisms (clamp k) (clamp (k+1)) xs)]
      apply alt_congr
      intro ys hy
      exact hc ys (valid_prism hx hy) (by rw [prism_length hy, hl])
    have h := prism_identity (clamp k) (clamp (k+1)) c xs
    rw [hz,add_zero] at h
    change D (fun ys => primitive c k ys + H (clamp k) (clamp (k+1)) c ys) xs = _
    have hadd : D (fun ys => primitive c k ys + H (clamp k) (clamp (k+1)) c ys) xs =
      D (primitive c k) xs + D (H (clamp k) (clamp (k+1)) c) xs :=
      alt_add _ _ _
    rw [hadd,ih,h]
    ring

/-- Genuine ordered-grid all-positive exactness. A single primitive
works on every admissible ordered tuple of the prescribed degree. -/
theorem grid_exact (M n : ℕ) (c : List (Vertex I) → ℤ)
    (hc : ∀ xs, valid M xs → xs.length = n+3 → D c xs = 0) :
    ∃ b : List (Vertex I) → ℤ, ∀ xs, valid M xs → xs.length = n+2 →
      D b xs = c xs := by
  refine ⟨primitive c M, fun xs hx hl => ?_⟩
  rw [primitive_identity M n c hc M xs hx hl, clamp_self_on_valid hx]

#print axioms valid_prism
#print axioms primitive_identity
#print axioms grid_exact
end CMDG.CondensedCM5R0.CompactCover.OrderedGrid
