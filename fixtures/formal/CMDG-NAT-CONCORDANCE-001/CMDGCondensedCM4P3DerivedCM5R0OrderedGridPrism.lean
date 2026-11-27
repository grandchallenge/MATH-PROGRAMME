import CMDGCondensedCM4P3DerivedCM5R0CompactCoverScalarCohomology

/-! Ordered tuple prism, with repetitions retained. The list recursion
is the unnormalized alternating face complex, including the empty face. -/
noncomputable section
universe u v
namespace CMDG.CondensedCM5R0.CompactCover.OrderedGrid

def alt {V : Type u} (c : V → ℤ) : List V → ℤ
  | [] => 0
  | x :: xs => c x - alt c xs

theorem alt_map {A : Type u} {B : Type v} (f : A → B) (c : B → ℤ) (xs : List A) :
    alt c (xs.map f) = alt (c ∘ f) xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [List.map_cons, alt, ih, Function.comp_apply]

theorem alt_add {V : Type u} (c e : V → ℤ) (xs : List V) :
    alt (fun x => c x + e x) xs = alt c xs + alt e xs := by
  induction xs with
  | nil => simp [alt]
  | cons x xs ih => simp only [alt, ih]; ring

theorem alt_sub {V : Type u} (c e : V → ℤ) (xs : List V) :
    alt (fun x => c x - e x) xs = alt c xs - alt e xs := by
  induction xs with
  | nil => simp [alt]
  | cons x xs ih => simp only [alt, ih]; ring

theorem alt_congr {V : Type u} (c e : V → ℤ) (xs : List V)
    (h : ∀ x ∈ xs, c x = e x) : alt c xs = alt e xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
    simp only [alt, h x (by simp)]
    rw [ih (fun y hy => h y (by simp [hy]))]

theorem alt_zero {V : Type u} (xs : List V) : alt (fun _ => 0) xs = 0 := by
  induction xs <;> simp_all [alt]

def faces {V : Type u} : List V → List (List V)
  | [] => []
  | x :: xs => xs :: (faces xs).map (List.cons x)

def prisms {V : Type u} (f g : V → V) : List V → List (List V)
  | [] => []
  | x :: xs => (f x :: g x :: xs.map g) :: (prisms f g xs).map (List.cons (f x))

def D {V : Type u} (c : List V → ℤ) (xs : List V) : ℤ :=
  alt c (faces xs)

def H {V : Type u} (f g : V → V) (c : List V → ℤ) (xs : List V) : ℤ :=
  alt c (prisms f g xs)

theorem D_cons {V : Type u} (c : List V → ℤ) (x : V) (xs : List V) :
    D c (x :: xs) = c xs - D (fun ys => c (x :: ys)) xs := by
  simp [D, faces, alt, alt_map, Function.comp_def]

theorem H_cons {V : Type u} (f g : V → V) (c : List V → ℤ) (x : V) (xs : List V) :
    H f g c (x :: xs) = c (f x :: g x :: xs.map g) -
      H f g (fun ys => c (f x :: ys)) xs := by
  simp [H, prisms, alt, alt_map, Function.comp_def]

theorem D_sub {V : Type u} (c e : List V → ℤ) (xs : List V) :
    D (fun ys => c ys - e ys) xs = D c xs - D e xs := alt_sub _ _ _

theorem H_sub {V : Type u} (f g : V → V) (c e : List V → ℤ) (xs : List V) :
    H f g (fun ys => c ys - e ys) xs = H f g c xs - H f g e xs := alt_sub _ _ _

theorem D_map {V : Type u} (g : V → V) (c : List V → ℤ) (xs : List V) :
    D c (xs.map g) = D (fun ys => c (ys.map g)) xs := by
  induction xs generalizing c with
  | nil => rfl
  | cons x xs ih =>
    rw [List.map_cons, D_cons, D_cons, ih]
    rfl

/-- Explicit signed prism identity in every arity. No orientation,
nondegeneracy, or sorting assumption is made on the tuples. -/
theorem prism_identity {V : Type u} (f g : V → V) (c : List V → ℤ) (xs : List V) :
    D (H f g c) xs + H f g (D c) xs = c (xs.map g) - c (xs.map f) := by
  induction xs generalizing c with
  | nil => simp [D, H, faces, prisms, alt]
  | cons x xs ih =>
    rw [D_cons, H_cons, D_cons, D_cons]
    have h1 : D (fun ys => H f g c (x :: ys)) xs =
        D (fun ys => c (f x :: g x :: ys.map g) -
          H f g (fun zs => c (f x :: zs)) ys) xs := by
      congr 1
      funext ys
      exact H_cons f g c x ys
    have h2 : H f g (fun ys => D c (f x :: ys)) xs =
        H f g (fun ys => c ys - D (fun zs => c (f x :: zs)) ys) xs := by
      congr 1
      funext ys
      exact D_cons c (f x) ys
    rw [h1, h2, D_sub, H_sub, D_map]
    simp only [List.map_cons]
    have h := ih (fun ys => c (f x :: ys))
    linarith

theorem face_length {V : Type u} {xs ys : List V} (h : ys ∈ faces xs) :
    ys.length + 1 = xs.length := by
  induction xs generalizing ys with
  | nil => simp [faces] at h
  | cons x xs ih =>
    simp only [faces, List.mem_cons, List.mem_map] at h
    rcases h with rfl | ⟨zs,hzs,rfl⟩
    · simp
    · simp only [List.length_cons]; have := ih hzs; omega

theorem face_subset {V : Type u} {xs ys : List V} (h : ys ∈ faces xs) :
    ∀ v ∈ ys, v ∈ xs := by
  induction xs generalizing ys with
  | nil => simp [faces] at h
  | cons x xs ih =>
    simp only [faces,List.mem_cons,List.mem_map] at h
    rcases h with rfl | ⟨zs,hzs,rfl⟩
    · intro v hv; simp [hv]
    · intro v hv
      simp only [List.mem_cons] at hv ⊢
      exact hv.imp_right (fun hz => ih hzs v hz)

theorem prism_length {V : Type u} {f g : V → V} {xs ys : List V}
    (h : ys ∈ prisms f g xs) : ys.length = xs.length + 1 := by
  induction xs generalizing ys with
  | nil => simp [prisms] at h
  | cons x xs ih =>
    simp only [prisms,List.mem_cons,List.mem_map] at h
    rcases h with rfl | ⟨zs,hzs,rfl⟩
    · simp [Nat.add_assoc]
    · simp only [List.length_cons]; have := ih hzs; omega

theorem prism_vertices {V : Type u} {f g : V → V} {xs ys : List V}
    (h : ys ∈ prisms f g xs) :
    ∀ v ∈ ys, ∃ w ∈ xs, v = f w ∨ v = g w := by
  induction xs generalizing ys with
  | nil => simp [prisms] at h
  | cons x xs ih =>
    simp only [prisms,List.mem_cons,List.mem_map] at h
    rcases h with rfl | ⟨zs,hzs,rfl⟩
    · intro v hv
      simp only [List.mem_cons,List.mem_map] at hv
      rcases hv with rfl | rfl | ⟨w,hw,rfl⟩
      · exact ⟨x,by simp,Or.inl rfl⟩
      · exact ⟨x,by simp,Or.inr rfl⟩
      · exact ⟨w,by simp [hw],Or.inr rfl⟩
    · intro v hv
      rcases List.mem_cons.mp hv with rfl | hv
      · exact ⟨x,by simp,Or.inl rfl⟩
      · obtain ⟨w,hw,he⟩ := ih hzs v hv
        exact ⟨w,by simp [hw],he⟩

#print axioms prism_identity
#print axioms prism_vertices
end CMDG.CondensedCM5R0.CompactCover.OrderedGrid
