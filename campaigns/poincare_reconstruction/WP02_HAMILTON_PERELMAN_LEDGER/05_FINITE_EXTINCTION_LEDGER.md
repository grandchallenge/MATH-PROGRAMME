# PC-WP02 — Finite-extinction and terminal-topology ledger

## Purpose

The Poincaré-specific proof does not need the complete long-time geometrization analysis. It needs a controlled surgery flow and a theorem that the flow becomes extinct for the relevant topological class. This file isolates that route and prevents three common compressions:

```text
positive scalar curvature -> extinction,
extinction -> S3,
prime decomposition -> Poincare.
```

None is valid in that unqualified form.

## Input profile

The finite-extinction lane begins with:

- a closed orientable normalized `3`-manifold;
- no aspherical prime factor, or the equivalent group/topology hypothesis in the selected reconstruction;
- an all-time Ricci flow with surgery satisfying the pinching, canonical-neighbourhood, noncollapsing, and sufficiently small surgery-control contracts.

For the canonical Poincaré input, orientability follows from simple connectivity. The no-aspherical-prime condition is discharged through prime-decomposition and group arguments without classifying simply connected primes as spheres.

## Mechanism A — elimination of essential `2`-spheres

The first mechanism follows the least-area representative of a nontrivial `pi_2` class, or an appropriately regularized infimum over essential `2`-spheres/disks in the reconstruction's formulation.

Between surgery times, the area satisfies a differential upper bound whose leading curvature contribution forces decay after the standard scalar-curvature estimates are inserted. Across surgery times, the comparison is arranged so that the relevant infimum does not jump upward in a way that defeats the estimate.

Consequences:

1. persistent essential `pi_2` classes would force a positive area quantity to become nonpositive in finite time;
2. therefore, after finite time, the surviving components have vanishing `pi_2` or have already disappeared;
3. topology changes at surgery remain recorded separately.

This mechanism is not by itself full extinction: a component can have `pi_2=0` and still be nonempty.

## Mechanism B — `pi_3` minimax width

For a surviving component in the remaining topological class, one considers a nontrivial sweepout/minimax class represented by maps of `S^2` parameterized by an interval or equivalent `pi_3` data. Define a width by minimizing the maximal energy/area over all representatives of the class.

The proof requires:

- existence of sufficiently regular near-minimizing sweepouts;
- replacement of maximal slices by almost-minimal spheres;
- an evolution inequality for the width under Ricci flow;
- control of scalar-curvature/time terms;
- a comparison across surgery times showing that the class and width can be transported or reduced in the permitted manner;
- a positive lower meaning for the width while the relevant component/class survives.

The resulting differential inequality forces the positive width to vanish in finite time, a contradiction unless the component becomes extinct.

## Schematic inequality boundary

The campaign records the mechanism schematically as

```math
\frac{d}{dt}W(t)
\le -c + E(t,W(t)),
```

where `c>0` is the decay term and `E` is an explicitly controlled curvature/time correction in the source theorem. This is not promoted as the exact source formula. Exact coefficients, barrier/upper-derivative interpretation, and regularization errors remain `PC-WP02-D007` until quotation-level reconstruction.

No derivative is asserted at a surgery time. Surgery comparison is a separate statement.

## Surgery-time contract

At a surgery time `t_s`, the extinction functional must satisfy a source-approved transition rule of one of these forms:

- the relevant class survives in a post-surgery component with no harmful increase in its comparison quantity;
- the class is killed, which advances extinction;
- the component carrying the class is discarded, which also advances extinction.

A metric-local statement about cap closeness is not enough. The topology class and comparison map must be tracked.

## Finite-time conclusion

Combining the smooth-interval differential inequality, surgery-time comparison, and the topological hypothesis gives a finite `T_ext` such that the surgery flow is empty after `T_ext`.

Local finiteness of surgery times on bounded intervals now implies that only finitely many surgery events occur before extinction. This is the first point at which a globally finite event history is justified in the Poincaré lane.

## Topology reconstruction

Let the surgery times be

```text
t_1 < t_2 < ... < t_N < T_ext.
```

For each event, record:

- pre-surgery component identifiers;
- cut spheres and whether they are separating;
- newly capped components;
- surviving component identifiers;
- discarded components and their permitted types;
- the connected-sum reconstruction expression.

Starting from the empty final state, apply the event rules backward. The initial manifold is reconstructed as a finite connected sum of permitted factors, including spherical space forms and `S^2`-bundle-over-`S^1` factors in the oriented theorem profile.

## Terminal simple-connectivity discharge

By van Kampen,

```math
\pi_1(M_1\#\cdots\#M_k)
\cong
\pi_1(M_1)*\cdots*\pi_1(M_k).
```

If the free product is trivial, each factor group is trivial.

- A nontrivial spherical space form `S^3/Gamma` has fundamental group `Gamma`, so only `Gamma=1` remains.
- An `S^2`-bundle-over-`S^1` factor has nontrivial fundamental group and is excluded.
- A surviving spherical factor with trivial deck group is `S^3`.
- Connected sum with `S^3` is neutral.

Therefore the connected initial manifold is diffeomorphic to `S^3`.

This argument uses only the surgery-derived factor list. It does not invoke the statement “every simply connected prime `3`-manifold is `S^3`.”

## Source map

| Obligation | Primary source | Detailed reconstruction |
|---|---|---|
| extinction theorem and width mechanism | `P-III` | `MT` Theorem 0.4, Theorem 18.1, chapters 18–19 |
| all-time controlled surgery flow | `P-II` | `MT` Theorem 15.9, chapters 15–17 |
| topology of surgery | `P-II` consequence | `MT` Theorem 0.3 and Corollary 15.4 |
| Poincaré-specific topology/group hypothesis | `P-III` | `MT` Corollary 0.5 |
| terminal factor elimination | standard topology | terminal argument following `MT` Theorem 18.1 |

## Adversarial guards

- `PC-FP-008`: every surgery changes or preserves topology only through an explicit event rule.
- `PC-FP-009`: extinction is not used without the factor reconstruction.
- `PC-FP-010`: orientability and projective-plane qualifications are discharged before entry.
- `PC-FP-012`: the target theorem is not imported in the prime-factor step.
- `PC-FP-014`: global finiteness follows only after finite extinction.

## Remaining proof debt

The following are source-normalized interfaces but not reconstructed line by line here:

- regularity and minimax construction for the width;
- exact upper-derivative formula and constants;
- surgery-time comparison for each topological case;
- exact equivalence among the source versions of the topological hypothesis;
- the complete permitted-factor list under each orientation/`RP^2` profile.

These debts block a claim of independent analytic verification. They do not change the classical solved status or the correctness of the cited theorem chain.
