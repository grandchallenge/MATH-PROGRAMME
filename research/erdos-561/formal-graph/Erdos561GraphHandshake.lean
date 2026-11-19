import Lean.Elab.Tactic.Omega

/-!
Finite graph handshake lemma over arbitrary finite vertex type Fin n.
An undirected edge is an unordered pair, represented as two endpoint values.
The incidence degree counts each listed endpoint, including loops twice,
so the identity is valid for every edge list; simple graphs are a special case.
No user axioms, no sorry/admit/native_decide, no Mathlib.
-/
namespace Erdos561Graph

private theorem indicator_sum_countP {α : Type} [DecidableEq α]
    (xs : List α) (a : α) :
    ((xs.map fun x => if x = a then (1:Nat) else 0).sum) =
      xs.countP (fun x => decide (x = a)) := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp [List.sum_cons, List.countP_cons, ih, Nat.add_comm]

private theorem countP_decide_eq_count {n : Nat}
    (xs : List (Fin n)) (a : Fin n) :
    xs.countP (fun x => decide (x = a)) = xs.count a := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      by_cases h : x = a
      · subst x; simp [ih]
      · simp [ih, h]

theorem indicator_sum_one (n : Nat) (a : Fin n) :
    ((List.finRange n).map (fun v => if v = a then (1:Nat) else 0)).sum = 1 := by
  rw [indicator_sum_countP, countP_decide_eq_count]
  rw [List.Nodup.count (List.nodup_finRange n)]
  simp [List.mem_finRange]

private theorem sum_map_zero {α : Type} (xs : List α) :
    ((xs.map fun _ => (0:Nat)).sum) = 0 := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simpa [List.sum_cons] using ih

private theorem sum_map_add {α : Type} (xs : List α) (f g : α → Nat) :
    ((xs.map fun x => f x + g x).sum) =
    (xs.map f).sum + (xs.map g).sum := by
  induction xs with
  | nil => rfl
  | cons a xs ih =>
      simp [List.sum_cons, ih]
      omega

/-- Count endpoint incidences of each vertex. -/
def degree {n : Nat} (es : List (Fin n × Fin n)) (v : Fin n) : Nat :=
    (es.map fun e => (if v = e.1 then (1:Nat) else 0) +
                     (if v = e.2 then (1:Nat) else 0)).sum

/-- The full degree sum over an explicitly finite vertex type. -/
def degreeSum {n : Nat} (es : List (Fin n × Fin n)) : Nat :=
  ((List.finRange n).map fun v => degree es v).sum

private theorem degree_cons {n : Nat} (e : Fin n × Fin n)
    (es : List (Fin n × Fin n)) (v : Fin n) :
    degree (e :: es) v =
      ((if v = e.1 then (1:Nat) else 0) +
       (if v = e.2 then (1:Nat) else 0)) + degree es v := by
  simp [degree, List.sum_cons]

/-- Graph-level handshake lemma, for every number of vertices and every
    finite edge list; finite simple graphs are covered. -/
theorem handshake {n : Nat} (es : List (Fin n × Fin n)) :
    degreeSum es = 2 * es.length := by
  induction es with
  | nil =>
      change ((List.finRange n).map fun _ => (0:Nat)).sum = 0
      exact sum_map_zero (List.finRange n)
  | cons e es ih =>
      have hsplit : degreeSum (e :: es) =
          ((List.finRange n).map fun v =>
            (if v = e.1 then (1:Nat) else 0) +
            (if v = e.2 then (1:Nat) else 0)).sum + degreeSum es := by
        simp only [degreeSum, degree_cons]
        exact sum_map_add (List.finRange n)
          (fun v => (if v = e.1 then (1:Nat) else 0) + (if v = e.2 then (1:Nat) else 0))
          (fun v => degree es v)
      have hind :
          ((List.finRange n).map fun v =>
            (if v = e.1 then (1:Nat) else 0) +
            (if v = e.2 then (1:Nat) else 0)).sum = 2 := by
        rw [sum_map_add]
        rw [indicator_sum_one n e.1, indicator_sum_one n e.2]
      rw [hsplit, hind, ih]
      simp [List.length_cons, Nat.mul_add, Nat.add_comm]


/-- In any finite list of nonnegative integer quantities, entries equal to D
    contribute at least D each to the total sum. -/
private theorem count_degree_sum_bound {α : Type} (xs : List α)
    (f : α → Nat) (D : Nat) :
    D * (xs.filter (fun x => decide (f x = D))).length ≤ (xs.map f).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
      by_cases h : f x = D
      · simp [h, List.sum_cons, Nat.mul_add] at *
        omega
      · simp [h, List.sum_cons] at *
        omega

/-- Exact count of vertices of degree D in an explicit edge-list graph. -/
def saturatedCount {n : Nat} (es : List (Fin n × Fin n)) (D : Nat) : Nat :=
  ((List.finRange n).filter fun v => decide (degree es v = D)).length

/-- Graph-level degree-core edge-budget lemma, using the proved handshake
    identity instead of assuming the degree sum as a numeric premise. -/
theorem saturated_edge_budget {n : Nat} (es : List (Fin n × Fin n))
    (D : Nat) (hcore : D + 1 ≤ saturatedCount es D) :
    D * (D + 1) ≤ 2 * es.length := by
  have hbound : D * saturatedCount es D ≤ degreeSum es :=
    count_degree_sum_bound (List.finRange n) (degree es) D
  have hmult : D * (D + 1) ≤ D * saturatedCount es D :=
    Nat.mul_le_mul_left D hcore
  calc
    D * (D + 1) ≤ D * saturatedCount es D := hmult
    _ ≤ degreeSum es := hbound
    _ = 2 * es.length := handshake es


/-- Sum of degrees splits into each positive-degree vertex's one mandatory
    incidence plus its remaining degree excess. -/
private theorem sum_positive_excess {α : Type} (xs : List α) (f : α → Nat) :
    (xs.map f).sum =
      (xs.map (fun x => f x - 1)).sum +
      (xs.filter (fun x => decide (0 < f x))).length := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      by_cases h : 0 < f x
      · simp [h, List.sum_cons, ih]
        omega
      · have hz : f x = 0 := by omega
        simp [hz, ih, List.sum_cons]

/-- A vertex with degree D≥1 contributes exactly D−1 to degree excess;
    every other vertex contributes a nonnegative amount. -/
private theorem saturated_excess_sum_bound {α : Type} (xs : List α)
    (f : α → Nat) (D : Nat) (_hD : 1 ≤ D) :
    (D - 1) * (xs.filter (fun x => decide (f x = D))).length ≤
      (xs.map (fun x => f x - 1)).sum := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
      by_cases h : f x = D
      · simp [h, List.sum_cons, Nat.mul_add] at *
        omega
      · simp [h, List.sum_cons] at *
        omega

/-- Number of graph vertices with positive incidence degree. -/
def positiveCount {n : Nat} (es : List (Fin n × Fin n)) : Nat :=
  ((List.finRange n).filter fun v => decide (0 < degree es v)).length

/-- Graph-level saturated-degree VERTEX budget, now with handshake and
    degree excess established inside Lean. -/
theorem saturated_vertex_budget {n : Nat} (es : List (Fin n × Fin n))
    (D : Nat) (hD : 1 ≤ D)
    (hcore : D + 1 ≤ saturatedCount es D) :
    (D - 1) * (D + 1) + positiveCount es ≤ 2 * es.length := by
  have hexcess : (D - 1) * saturatedCount es D ≤
      ((List.finRange n).map (fun v => degree es v - 1)).sum :=
    saturated_excess_sum_bound (List.finRange n) (degree es) D hD
  have hmul : (D - 1) * (D + 1) ≤ (D - 1) * saturatedCount es D :=
    Nat.mul_le_mul_left (D - 1) hcore
  have hsplit : degreeSum es =
      ((List.finRange n).map (fun v => degree es v - 1)).sum +
      positiveCount es :=
    sum_positive_excess (List.finRange n) (degree es)
  rw [handshake es] at hsplit
  omega


/-- A graph with at least D+1 vertices of degree D and less than D-1
    units of residual degree-excess slack has EXACTLY D+1 such vertices.
    This is the unbounded graph-level low-slack count lemma, conditional
    only on the explicit degree-excess budget and the D+1 core premise. -/
theorem low_slack_exact_core {n : Nat} (es : List (Fin n × Fin n))
    (D slack : Nat) (hD : 2 ≤ D)
    (hcore : D + 1 ≤ saturatedCount es D)
    (hbudget : 2 * es.length ≤
      (D - 1) * (D + 1) + positiveCount es + slack)
    (hsmall : slack < D - 1) :
    saturatedCount es D = D + 1 := by
  have hexcess : (D - 1) * saturatedCount es D ≤
      ((List.finRange n).map (fun v => degree es v - 1)).sum :=
    saturated_excess_sum_bound (List.finRange n) (degree es) D (by omega)
  have hsplit : degreeSum es =
      ((List.finRange n).map (fun v => degree es v - 1)).sum +
      positiveCount es :=
    sum_positive_excess (List.finRange n) (degree es)
  rw [handshake es] at hsplit
  have hn : (D - 1) * saturatedCount es D ≤
      (D - 1) * (D + 1) + slack := by omega
  apply Classical.byContradiction
  intro hne
  have hk2 : D + 2 ≤ saturatedCount es D := by omega
  have hmul : (D - 1) * (D + 2) ≤
      (D - 1) * saturatedCount es D :=
    Nat.mul_le_mul_left (D - 1) hk2
  have hstep : (D - 1) * (D + 2) =
      (D - 1) * (D + 1) + (D - 1) := by
    have ha : D + 2 = D + 1 + 1 := by omega
    rw [ha, Nat.mul_add]
    simp
  omega

#print axioms Erdos561Graph.indicator_sum_one
#print axioms Erdos561Graph.handshake
#print axioms Erdos561Graph.saturated_edge_budget
#print axioms Erdos561Graph.saturated_vertex_budget
#print axioms Erdos561Graph.low_slack_exact_core

end Erdos561Graph
