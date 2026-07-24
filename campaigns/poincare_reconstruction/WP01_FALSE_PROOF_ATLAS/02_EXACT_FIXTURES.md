# PC-WP01 — Exact adversarial fixtures

Each fixture has five fields: the tempting move, the smallest failure, the exact conclusion ruled out, the viable remainder, and the protected theorem-spine edge.

## PC-FP-001 — Homology is not simple connectivity

**Tempting move.** Replace `pi_1(M)=1` by the assertion that `M` has the integral homology of `S^3`.

**Smallest failure.** The Poincaré homology sphere has

```text
H_0 = H_3 = Z,
H_1 = H_2 = 0,
```

but has nontrivial finite fundamental group. Homology records the abelianization of the fundamental group in degree one; a perfect nontrivial group is invisible there.

**Ruled out.** A proof using only ordinary homology cannot identify an arbitrary homology 3-sphere with `S^3`.

**Still viable.** Homology remains useful after the nonabelian fundamental-group and surgery information has been retained.

**Protected edge.** `PC-D000 -> PC-L012`.

## PC-FP-002 — Contractibility does not control infinity

**Tempting move.** Generalize the closed theorem to “every contractible 3-manifold is `R^3`.”

**Smallest failure.** The Whitehead manifold is open and contractible but not homeomorphic to `R^3`; its end is not simply connected at infinity.

**Ruled out.** Contractibility alone does not classify noncompact 3-manifolds.

**Still viable.** The canonical theorem retains compactness and empty boundary. Open-manifold analogues require end hypotheses.

**Protected edge.** `PC-D000`.

## PC-FP-003 — Closedness is not cosmetic

**Tempting move.** Drop “without boundary.”

**Smallest failure.** `B^3` is compact and simply connected, but its boundary is `S^2`, so it is not `S^3`.

**Ruled out.** Compact plus simply connected is insufficient.

**Still viable.** State `closed = compact without boundary`; relative and bounded-manifold theorems form a separate lane.

**Protected edge.** `PC-D000`.

## PC-FP-004 — Category equivalence is a theorem

**Tempting move.** Pass from a topological input to a smooth metric without naming any bridge.

**Smallest failure.** “Topological manifold,” “PL manifold,” and “smooth manifold” are different structures. Their compatibility and uniqueness in dimension three follow from special theorems; the unrestricted higher-dimensional analogue fails.

**Ruled out.** The phrase “choose a metric” cannot silently create a smooth structure on an arbitrary topological manifold.

**Still viable.** Import the dimension-three triangulation/Hauptvermutung and smoothing package, then choose a Riemannian metric.

**Protected edge.** `PC-D000 -> PC-L001 -> PC-L003`.

## PC-FP-005 — Ricci flow does not remain smooth automatically

**Tempting move.** Treat Ricci flow as a globally smooth deformation from every metric to a round metric.

**Smallest failure.** For a round `3`-sphere with `Ric(g_0)=2g_0`, the unnormalized solution has the form

```math
g(t)=(1-4t)g_0,
```

up to the chosen curvature normalization, and becomes singular in finite time. Curvature scales as the reciprocal of the shrinking factor.

**Ruled out.** Short-time existence does not provide a smooth solution for all time.

**Still viable.** Analyze singularities, identify canonical necks/caps, perform controlled surgery, and restart a new smooth segment.

**Protected edge.** `PC-L004 -> PC-L007`.

## PC-FP-006 — A blow-up is not the original manifold

**Tempting move.** Identify the topology of a pointed parabolic blow-up with the topology of the closed input manifold.

**Smallest failure.** A sequence centered on a developing neck may converge after rescaling to the noncompact shrinking cylinder `S^2 x R`, although the original manifold is closed and may be topologically `S^3`.

**Ruled out.** A singularity model cannot be substituted globally for the source manifold.

**Still viable.** Use the limit to obtain local geometric control and a surgery model near the selected high-curvature point.

**Protected edge.** `PC-L005 -> PC-L006`.

## PC-FP-007 — Canonical neighbourhoods require a controlled flow

**Tempting move.** Assert that any high-curvature point in any 3-metric lies in a neck, cap, or round component.

**Smallest failure.** The canonical-neighbourhood theorem is conditional on a Ricci-flow history with curvature pinching, quantitative noncollapsing, a high-curvature threshold relative to a scale `r`, and a fixed approximation accuracy `epsilon`.

**Ruled out.** High scalar curvature by itself does not imply the theorem's model geometry.

**Still viable.** Carry the full hypothesis profile and parameter order into each consumer.

**Protected edge.** `PC-L005 -> PC-L006 -> PC-L007`.

## PC-FP-008 — Surgery changes topology and must be reversible on paper

**Tempting move.** Describe surgery as removing a geometrically bad patch while preserving the manifold.

**Smallest failure.** Cutting along an embedded `S^2` and capping the two new boundary spheres may split a connected component. If the sphere is nonseparating, reconstruction adds an `S^2`-bundle-over-`S^1` factor. Discarded components also contribute prescribed connected-sum factors.

**Ruled out.** Equality of pre- and post-surgery topology cannot be assumed.

**Still viable.** Maintain a component-ancestry graph and a reconstruction rule for each surgery event.

**Protected edge.** `PC-L007 -> PC-L008 -> PC-L011`.

## PC-FP-009 — Extinction is not a classifier by itself

**Tempting move.** Infer `M=S^3` directly from finite-time extinction.

**Smallest failure.** A nontrivial spherical space form `S^3/Gamma` with a round quotient metric shrinks under unnormalized Ricci flow and becomes extinct, while its fundamental group is `Gamma`.

**Ruled out.** Extinction alone does not distinguish `S^3` from other spherical factors or from a surgically decomposed connected sum.

**Still viable.** Combine extinction with the surgery topology theorem and then apply the trivial-fundamental-group hypothesis.

**Protected edge.** `PC-L010 -> PC-L011 -> PC-L012`.

## PC-FP-010 — Orientability and `RP^2` hypotheses are structural

**Tempting move.** Quote an oriented surgery theorem for an arbitrary closed 3-manifold.

**Smallest failure.** Nonorientable manifolds may contain two-sided embedded projective planes whose neighbourhood and cutting behaviour fall outside the stated oriented surgery interface.

**Ruled out.** The topology conclusion cannot survive silent deletion of the orientability or `RP^2` condition.

**Still viable.** A connected simply connected manifold is orientable. Record this before entering the oriented Hamilton–Perelman lane.

**Protected edge.** `PC-L002 -> PC-L007` and `PC-L009`.

## PC-FP-011 — Stronger theorems are not equivalent to Poincaré

**Tempting move.** Replace the implication chain by three equivalent labels.

**Smallest failure.** Elliptization classifies closed 3-manifolds with arbitrary finite fundamental group. Lens spaces lie in that class but are outside the simply connected hypothesis of Poincaré.

**Ruled out.** Poincaré does not imply elliptization, and neither alone implies full geometrization.

**Still viable.** Preserve

```text
geometrization -> elliptization -> Poincare.
```

**Protected edge.** `PC-B016 -> PC-B015 -> PC-C014`.

## PC-FP-012 — Prime decomposition can hide the target theorem

**Tempting move.** Invoke prime decomposition and then state that the simply connected prime summand is `S^3`.

**Smallest failure.** That classification sentence is precisely the Poincaré conclusion for a prime input.

**Ruled out.** Kneser–Milnor alone is not a proof of Poincaré.

**Still viable.** The Ricci-flow/surgery theorem supplies an independently restricted terminal factor list. Fundamental groups of those factors are then computed without assuming Poincaré.

**Protected edge.** `PC-L009 -> PC-L011 -> PC-L012`.

## PC-FP-013 — Conditional formalization is not full formalization

**Tempting move.** Declare the proof formalized after checking

```text
HamiltonPerelmanInterfaces -> M is S3.
```

**Smallest failure.** The antecedent contains the main nonlinear PDE, compactness, surgery, and extinction work. A kernel-checked implication does not construct or verify the antecedent.

**Ruled out.** A theorem-interface certificate cannot be advertised as a formal proof of the Hamilton–Perelman analytic core.

**Still viable.** Certify the terminal algebraic/topological logic and label every imported interface visibly.

**Protected edge.** `PC-T017`.

## PC-FP-014 — Local finiteness is not global finiteness

**Tempting move.** Read “finitely many surgeries on each finite interval” as “finitely many surgeries over all time.”

**Smallest failure.** Local finiteness permits an unbounded sequence of surgery times tending to infinity.

**Ruled out.** Surgery-flow existence alone does not make the complete history finite.

**Still viable.** In the Poincaré lane, finite extinction supplies a finite terminal time; local finiteness then gives a finite history.

**Protected edge.** `PC-L007 -> PC-L010 -> PC-L011`.

## PC-FP-015 — Source correction is part of the theorem

**Tempting move.** Treat the first Perelman preprint as a frozen, self-contained final proof.

**Smallest failure.** The surgery preprint explicitly states that selected assertions from the earlier paper were unjustified or deferred and corrects inaccuracies in its ancient-solution discussion.

**Ruled out.** An unversioned source collage is not a reliable theorem ledger.

**Still viable.** Use a primary-source correction map and compare against detailed reconstructions.

**Protected edge.** `PC-L005 -> PC-L006 -> PC-L007`.

## Atlas acceptance rule

A route survives WP01 only if it:

1. preserves the exact input category and hypotheses;
2. distinguishes local models from global topology;
3. records all surgery topology changes;
4. uses extinction only with the terminal factor theorem;
5. avoids importing the target conclusion;
6. preserves source versions and correction notices;
7. states the formalization boundary explicitly.

Survival means “not rejected by this atlas,” not “proved.”
