# PC-WP02 — Source-normalized theorem interfaces

## Interface contract

Each entry distinguishes four statuses:

- `PROVED_IN_PACKAGE`: elementary logic reconstructed here;
- `AUDITED_IMPORT`: source theorem identified with sufficient operational hypotheses for this proof spine;
- `AUDITED_IMPORT_WITH_EXTRACTION_DEBT`: mathematically standard interface is stable, but quotation-level historical extraction remains;
- `UNFORMALIZED_IMPORT`: no machine-checked proof is claimed.

All geometric and analytic results below are `UNFORMALIZED_IMPORT` unless explicitly marked otherwise.

---

## PC02-T001 — Dimension-three category bridge

**Role.** Convert the canonical topological input into a smooth manifold without changing its classification problem.

**Input.** A closed topological `3`-manifold `M`.

**Imported conclusion.** `M` admits compatible PL and smooth structures; the relevant structures and homeomorphisms are unique up to the dimension-three compatibility theorems needed to transfer a smooth diffeomorphism conclusion back to a topological homeomorphism conclusion.

**Sources.** `MOISE`, `SMOOTH`, and the category note in `MT`.

**Consumers.** `PC02-T002`, `PC02-T019`.

**Adversarial guards.** `PC-FP-004`.

**Status.** `AUDITED_IMPORT_WITH_EXTRACTION_DEBT`.

**Boundary.** This is special to dimension three; it is not a definitional or dimension-free equivalence.

---

## PC02-T002 — Smooth metric and short-time Ricci flow

**Role.** Enter the geometric evolution.

**Input.** A closed smooth `3`-manifold with a smooth Riemannian metric `g_0`.

**Imported conclusion.** There is a unique smooth Ricci flow on a nontrivial maximal interval

```math
\partial_t g=-2\operatorname{Ric}(g),
\qquad g(0)=g_0.
```

The metric may first be rescaled to the normalization assumed by the surgery theorem.

**Sources.** `HAM`, operationally reconstructed in `MT` and `KL`.

**Consumers.** `PC02-T003`–`PC02-T006`, then the singularity/surgery chain.

**Adversarial guards.** `PC-FP-005`.

**Status.** `AUDITED_IMPORT_WITH_EXTRACTION_DEBT`.

**Boundary.** Maximal smooth existence is not all-time smooth existence.

---

## PC02-T003 — `W`-entropy and `mu` monotonicity

**Role.** Supply a scale-sensitive monotone quantity and control minimizers used in noncollapsing arguments.

**Input.** A smooth Ricci flow on a closed manifold, a positive backward-time scale `tau`, and the normalized density/auxiliary function appearing in Perelman's `W` functional.

**Imported conclusion.** Along the coupled backward heat evolution, `W` is monotone with derivative equal to a nonnegative square integral. The infimum `mu(g,tau)` inherits the corresponding monotonicity under the Ricci-flow/time-scale coupling.

**Sources.** `P-I` section 3; `MT`; `KL`.

**Consumers.** `PC02-T006` and compactness/scale-control arguments.

**Adversarial guards.** `PC-FP-015`.

**Status.** `AUDITED_IMPORT`.

**Boundary.** Entropy monotonicity does not itself classify singularities or construct surgery.

---

## PC02-T004 — Reduced distance and reduced-volume monotonicity

**Role.** Control ancient limits from a spacetime basepoint without requiring a globally defined entropy minimizer.

**Input.** A smooth Ricci flow, a spacetime basepoint, and the backward reduced-length construction on an interval free of surgery.

**Imported conclusion.** Reduced distance satisfies the appropriate differential inequalities, and reduced volume is nonincreasing backward in the source convention, with equality characterizing shrinking-soliton behaviour under the required regularity hypotheses.

**Sources.** `P-I` sections 6–7; `MT`; `KL`.

**Consumers.** `PC02-T006`, `PC02-T007`.

**Adversarial guards.** `PC-FP-006`, `PC-FP-015`.

**Status.** `AUDITED_IMPORT`.

**Boundary.** The quantity is based at a spacetime point and controls pointed geometry; it does not globally identify the source manifold.

---

## PC02-T005 — Pseudolocality

**Role.** Prevent rapid curvature creation in a region that is initially sufficiently close, in an isoperimetric/geometric sense, to a regular Euclidean region.

**Input.** A smooth Ricci flow with an initial ball satisfying the source theorem's scalar-curvature lower bound and almost-Euclidean isoperimetric hypothesis, together with the required compactness/completeness profile.

**Imported conclusion.** Curvature remains quantitatively controlled for a definite short spacetime neighbourhood, with constants depending on the theorem's accuracy parameters.

**Sources.** `P-I` section 10; `MT`; `KL`.

**Consumers.** `PC02-T006`, surgery-persistence and locality arguments.

**Adversarial guards.** `PC-FP-007`, `PC-FP-015`.

**Status.** `AUDITED_IMPORT`.

**Boundary.** Pseudolocality is conditional local control, not a global regularity theorem.

---

## PC02-T006 — No-local-collapsing

**Role.** Ensure that curvature-controlled regions do not lose all volume after rescaling.

**Input.** A smooth Ricci flow on a closed normalized manifold over a bounded time interval; a parabolic ball on which curvature is bounded at the corresponding scale.

**Imported conclusion.** There is `kappa>0` such that every eligible ball of radius `rho` has volume at least `kappa rho^3`. Localized and surgery-compatible variants require their additional hypotheses.

**Sources.** `P-I` sections 4 and 8; `MT`; `KL`; surgery-compatible continuation in `P-II`/`MT`.

**Consumers.** Hamilton compactness/blow-up extraction, `PC02-T007`, `PC02-T008`, `PC02-T011`.

**Adversarial guards.** `PC-FP-006`, `PC-FP-007`, `PC-FP-015`.

**Status.** `AUDITED_IMPORT`.

**Boundary.** A qualitative statement that regions “do not collapse” is insufficient; the scale, curvature hypothesis, time horizon, and `kappa` dependence must be retained.

---

## PC02-T007 — Ancient `kappa`-solutions and compactness

**Role.** Describe possible blow-up limits at high curvature.

**Input.** A sequence of pointed, parabolically rescaled `3`-dimensional Ricci flows with nonnegative curvature in the limit, bounded normalized curvature at the basepoint, and uniform `kappa`-noncollapsing.

**Imported conclusion.** A subsequence converges in the pointed smooth sense to an ancient `kappa`-solution satisfying the corrected structural properties used by the canonical-neighbourhood theorem. Compactness holds for the normalized class.

**Sources.** `P-I` section 11, corrected in `P-II` section 1; expanded in `MT` and `KL`.

**Consumers.** `PC02-T008`.

**Adversarial guards.** `PC-FP-006`, `PC-FP-015`.

**Status.** `AUDITED_IMPORT_WITH_CORRECTION_DEPENDENCY`.

**Boundary.** The ancient limit is a pointed local model. The campaign does not import superseded `P-I` assertions.

---

## PC02-T008 — Canonical-neighbourhood theorem

**Role.** Turn sufficiently high curvature into a finite controlled list of local geometries.

**Input.** A normalized `3`-dimensional Ricci flow satisfying the relevant pinching and noncollapsing estimates, a fixed sufficiently small `epsilon`, and a point whose scalar curvature exceeds the threshold determined by `r` and the source theorem.

**Imported conclusion.** After rescaling by the local curvature scale, the point lies in an `epsilon`-canonical neighbourhood: a strong neck, a cap, a positively curved compact component, or the precise alternative supplied by the chosen theorem version, with derivative and volume controls.

**Sources.** `P-I` section 12; corrected surgery context in `P-II`; `MT` canonical-neighbourhood chapters; `KL`.

**Consumers.** `PC02-T009`, `PC02-T010`, `PC02-T012`, `PC02-T013`.

**Adversarial guards.** `PC-FP-006`, `PC-FP-007`, `PC-FP-015`.

**Status.** `AUDITED_IMPORT`.

**Boundary.** The theorem applies to high-curvature points in a controlled flow, not arbitrary high-curvature metrics.

---

## PC02-T009 — Standard cap solution

**Role.** Provide a geometrically controlled replacement for the high-curvature end removed during neck surgery.

**Input.** The standard initial cap metric and its Ricci flow, normalized according to `P-II`/the reconstruction.

**Imported conclusion.** The standard solution exists on its prescribed time interval and satisfies curvature, asymptotic-neck, and canonical-neighbourhood estimates adequate for insertion and later persistence comparison.

**Sources.** `P-II` section 2; `MT` chapter 12; `KL`.

**Consumers.** `PC02-T010`, `PC02-T011`, `PC02-T012`.

**Adversarial guards.** `PC-FP-007`, `PC-FP-015`.

**Status.** `AUDITED_IMPORT`.

**Boundary.** A topological `3`-ball cap is not enough; its metric and flow estimates are part of the surgery theorem.

---

## PC02-T010 — `delta`-neck surgery and pinching preservation

**Role.** Replace singular neck regions by controlled caps while preserving the estimates needed to restart the flow.

**Input.** A surgery flow immediately before a surgery time, satisfying pinching and canonical-neighbourhood hypotheses; a collection of sufficiently round `delta`-necks at the derived radius `h`; the source-dependent curvature cutoff.

**Imported conclusion.** Cutting the selected necks, inserting standard caps, and discarding only permitted components produces a smooth post-surgery metric satisfying the required curvature-pinching and restart estimates. The geometric modification is localized and compatible with the parameter hierarchy.

**Sources.** `P-II` surgery sections; `MT` chapters 13–15; `KL`.

**Consumers.** `PC02-T011`, `PC02-T013`, `PC02-T014`.

**Adversarial guards.** `PC-FP-005`, `PC-FP-007`, `PC-FP-008`, `PC-FP-010`, `PC-FP-015`.

**Status.** `AUDITED_IMPORT`.

**Boundary.** The output is not topologically identical to the input. The topology mutation is handled by `PC02-T014`.

---

## PC02-T011 — Noncollapsing through surgery

**Role.** Prevent the surgery procedure from destroying the compactness assumptions required at later singular times.

**Input.** A surgery flow satisfying the current stage's pinching, canonical-neighbourhood, surgery-quality, and prior noncollapsing contracts.

**Imported conclusion.** With surgery parameters chosen sufficiently small in the required dependency order, the post-surgery flow remains quantitatively noncollapsed at the scales and time horizon needed for the induction.

**Sources.** `P-II`; `MT` chapter 16, including its noncollapsing proposition; `KL` surgery analysis.

**Consumers.** `PC02-T012`, `PC02-T013`.

**Adversarial guards.** `PC-FP-007`, `PC-FP-014`, `PC-FP-015`.

**Status.** `AUDITED_IMPORT`.

**Boundary.** The constant is stage- and history-dependent; it is not a free uniform constant over every possible surgery flow.

---

## PC02-T012 — Strong canonical neighbourhoods for surgery flow

**Role.** Close the induction by proving that future high-curvature regions retain the required model structure despite prior surgeries.

**Input.** A surgery flow satisfying the full current parameter hierarchy, pinching, noncollapsing, and standard-cap persistence controls.

**Imported conclusion.** All sufficiently high-curvature points satisfy the strengthened canonical-neighbourhood assumptions required by the next surgery step.

**Sources.** `P-II`; `MT` chapter 17, including its strong canonical-neighbourhood proposition; `KL`.

**Consumers.** `PC02-T013`.

**Adversarial guards.** `PC-FP-006`, `PC-FP-007`, `PC-FP-015`.

**Status.** `AUDITED_IMPORT`.

**Boundary.** This theorem is a surgery-flow theorem, not merely the smooth-flow canonical-neighbourhood statement.

---

## PC02-T013 — All-time Ricci flow with surgery

**Role.** Produce the controlled dynamical object used by the finite-extinction theorem.

**Input.** A normalized closed orientable Riemannian `3`-manifold satisfying the source theorem's `RP^2` qualification; stagewise sequences `kappa_i`, `r_i`, `delta_i` chosen in the permitted dependency order.

**Imported conclusion.** There exists a Ricci flow with surgery for all positive times satisfying pinching, noncollapsing, and canonical-neighbourhood assumptions. Surgery times are finite in number on every bounded time interval, and every surgery/discard operation belongs to the prescribed geometric and topological classes.

**Sources.** `P-II` and `MT` Theorem 15.9 with chapters 16–17; compared with `KL`.

**Consumers.** `PC02-T014`, `PC02-T016`.

**Adversarial guards.** `PC-FP-005`, `PC-FP-008`, `PC-FP-010`, `PC-FP-014`, `PC-FP-015`.

**Status.** `AUDITED_IMPORT_AT_THEOREM_INTERFACE_LEVEL`.

**Boundary.** “All positive times” refers to the piecewise-smooth surgery flow. It does not mean one globally smooth metric family or finitely many surgeries over an infinite interval.

---

## PC02-T014 — Topology of surgery and discarded components

**Role.** Make the piecewise geometric evolution reversible at the level of manifold classification.

**Input.** One surgery transition satisfying `PC02-T010` and the source theorem's orientability/embedded-projective-plane profile.

**Imported conclusion.** The pre-surgery component can be reconstructed from the surviving post-surgery components by connected sum with factors from the explicit permitted list. Separating and nonseparating cuts, cap insertions, and discarded spherical or cylindrical components have specified reconstruction rules.

**Sources.** `P-II` topological conclusion; `MT` Theorem 0.3, Corollary 15.4, and surgery-topology discussion.

**Consumers.** `PC02-T017`.

**Adversarial guards.** `PC-FP-008`, `PC-FP-009`, `PC-FP-010`.

**Status.** `AUDITED_IMPORT_AT_TOPOLOGY_INTERFACE_LEVEL`.

**Boundary.** PC-WP03 must still encode the event-by-event finite history and verify the induction mechanically or formally.

---

## PC02-T015 — Simply connected input satisfies the extinction class

**Role.** Enter the hypothesis profile of the finite-extinction theorem without using Poincaré circularly.

**Input.** A closed connected simply connected orientable `3`-manifold.

**Conclusion.** Its prime-decomposition/fundamental-group profile has no aspherical prime contribution and satisfies the equivalent sufficient group condition used by the selected finite-extinction reconstruction.

**Sources.** `P-III` hypothesis; `MT` Corollary 0.5; foundational `KM` and `VK` interfaces.

**Consumers.** `PC02-T016`.

**Adversarial guards.** `PC-FP-010`, `PC-FP-012`.

**Status.** `AUDITED_TOPOLOGY_BRIDGE_WITH_EXTRACTION_DEBT`.

**Non-circular proof sketch.** Prime decomposition gives a free-product decomposition of the fundamental group. If the total group is trivial, every factor group is trivial. An aspherical closed prime has nontrivial fundamental group because its universal cover is contractible and the manifold itself is not contractible. Thus no aspherical prime occurs. This argument does not classify the remaining simply connected prime as `S^3`.

---

## PC02-T016 — Finite-time extinction

**Role.** Turn the all-time surgery flow into a finite terminal history for the Poincaré input class.

**Input.** A Ricci flow with surgery as in `PC02-T013` whose initial manifold satisfies the no-aspherical-prime/equivalent group hypothesis, with surgery parameters sufficiently small for the finite-extinction comparison.

**Imported conclusion.** There is a finite time `T_ext` after which no component remains. The proof uses a minimal-disk/minimax width quantity, differential control between surgery times, and comparison across surgery events.

**Sources.** `P-III`; `MT` Theorem 0.4, Theorem 18.1, chapters 18–19.

**Consumers.** `PC02-T017`.

**Adversarial guards.** `PC-FP-009`, `PC-FP-012`, `PC-FP-014`.

**Status.** `AUDITED_IMPORT_AT_THEOREM_AND_MECHANISM_LEVEL`.

**Boundary.** Extinction does not identify the original topology until all surgery events are reversed using `PC02-T014`.

---

## PC02-T017 — Finite history and connected-sum reconstruction

**Role.** Convert extinction into a finite classification expression for the initial manifold.

**Input.** `PC02-T013`, finite extinction time from `PC02-T016`, local finiteness of surgery times, and the per-event topology theorem `PC02-T014`.

**Conclusion.** There are finitely many surgery events before `T_ext`. Backward induction reconstructs the initial manifold as a connected sum of factors from the permitted spherical-space-form and `S^2`-bundle-over-`S^1` list, with any source-specific auxiliary factors recorded explicitly.

**Sources.** `MT` Corollary 15.4 and the terminal proof following Theorem 18.1.

**Consumers.** `PC02-T018`.

**Adversarial guards.** `PC-FP-008`, `PC-FP-009`, `PC-FP-014`.

**Status.** `PROVED_IN_PACKAGE_CONDITIONAL_ON_IMPORTED_EVENT_INTERFACE`.

**Proof.** Finite extinction gives a bounded interval. Local finiteness yields finitely many surgery times in that interval. At the final time the surviving collection is empty. Apply the reconstruction rule at the last event and induct backward through the finite ordered history.

---

## PC02-T018 — Terminal fundamental-group elimination

**Role.** Use simple connectivity only after the independently derived factor list is available.

**Input.** A connected-sum expression from `PC02-T017` and `pi_1(M)=1`.

**Conclusion.** Every factor with nontrivial finite deck group is excluded, and every `S^2`-bundle-over-`S^1` factor is excluded because it has a nontrivial/infinite-cyclic fundamental-group contribution. The remaining spherical-space-form factors have trivial deck group and are `S^3`; connected sum with `S^3` is neutral. Hence `M` is diffeomorphic to `S^3`.

**Sources.** `VK`, definitions of spherical space forms, and the terminal argument in `MT`.

**Consumers.** `PC02-T019`.

**Adversarial guards.** `PC-FP-001`, `PC-FP-009`, `PC-FP-011`, `PC-FP-012`.

**Status.** `PROVED_IN_PACKAGE_CONDITIONAL_ON_PC02-T017`.

**Boundary.** The proof never assumes that an arbitrary simply connected prime `3`-manifold is `S^3`.

---

## PC02-T019 — Smooth and topological Poincaré conclusions

**Role.** Close the campaign theorem spine.

**Input.** The smooth manifold produced through `PC02-T001`, the terminal diffeomorphism from `PC02-T018`, and the category compatibility theorem.

**Conclusion.** The smooth input is diffeomorphic to `S^3`; the original topological input is homeomorphic to `S^3`.

**Sources.** The full chain above; `MT` terminal conclusion; official theorem statement.

**Adversarial guards.** `PC-FP-004`, `PC-FP-011`, `PC-FP-013`.

**Status.** `SOLVED_CLASSICAL_THEOREM_RECONSTRUCTED_CONDITIONALLY_ON_AUDITED_IMPORTS`.

**Claim boundary.** This ledger exposes and composes the established theorem interfaces. It does not independently re-prove or machine-check `PC02-T002` through `PC02-T016`.
