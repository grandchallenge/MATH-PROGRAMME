# PC-WP05 — final non-circularity audit

## Required terminal order

The finite-extinction route is accepted only in the following order:

```text
A. establish/import a controlled Ricci flow with surgery;
B. establish/import finite extinction under an independently verified topology hypothesis;
C. derive a finite source-bound history;
D. reconstruct the initial manifold as a connected sum of standard factors;
E. compute the corresponding fundamental-group free product;
F. apply pi1(M)=1 to eliminate nontrivial factors;
G. conclude M is S3.
```

No conclusion from step `G` may be used to establish an earlier step.

## Audit of the high-risk edges

### Simple connectivity to finite extinction

The route does not say “Poincaré is true, so no aspherical prime occurs.” It uses the independent topology fact that an aspherical prime has nontrivial fundamental group, together with prime decomposition and van Kampen, to show that a simply connected input has no aspherical prime factor. Perelman III is then applied.

### Extinction to classification

Extinction alone does not classify the initial manifold. The topology-event theorem is imported independently, and WP03 records every cut, cap, discarded standard component, and ancestry relation. Backward reconstruction uses both extinction and event topology.

### Standard factors to S3

The archive first derives the standard-factor expression. Only then does it use van Kampen/free-product reasoning. It does not classify an arbitrary simply connected prime as `S3` in order to construct the expression.

### Spherical space forms

A spherical factor is represented as `S3/Gamma`. Trivial fundamental group forces `Gamma=1`; it is not assumed at factor-registration time. Nontrivial spherical quotients are retained in the general profile and rejected only by the terminal group discharge.

### Sphere-bundle factors

The orientable `S2 x S1` factor contributes an infinite-cyclic free factor and is therefore excluded by simple connectivity. The nonorientable sphere bundle is excluded already by the Poincaré orientation profile and remains represented in the general profile.

### `RP3#RP3`

This discarded class is normalized into two spherical factors before group discharge. It is not treated as a new prime or silently identified with `S3`.

### Formal certificate boundary

`ImportedEventRelation` is an assumption in the WP04 correctness theorem. Kernel checking proves the evaluator consequence, not the imported geometric event. The Boolean terminal predicate is not represented as a formal proof of van Kampen.

## Forbidden edges

```text
Poincare conclusion -> no aspherical factor
extinction -> topology classification without event theorem
schema-valid history -> existence of Ricci flow with surgery
Lean evaluator correctness -> ImportedEventRelation
simply connected -> every prime is S3 before reconstruction
geometrization -> equivalent to Poincare
homeomorphism conclusion -> smoothing/category bridge
```

## Audit disposition

No circular edge occurs in the integrated dependency graph at the stated interface level. The terminal group and category steps remain classical imports; their absence from the Lean model is disclosed rather than filled by an opaque axiom.