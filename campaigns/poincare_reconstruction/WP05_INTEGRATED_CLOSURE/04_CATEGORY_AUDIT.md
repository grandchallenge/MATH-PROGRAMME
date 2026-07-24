# PC-WP05 — final category and orientation audit

## Canonical input

The public theorem begins in `Top`:

```text
M is a closed, connected topological 3-manifold with pi1(M)=1.
```

Ricci flow requires a smooth Riemannian manifold. The archive therefore records, rather than suppresses, the dimension-three bridge:

```text
Top 3-manifold
  -> compatible PL structure
  -> compatible smooth structure
  -> smooth Riemannian metric.
```

The terminal analytic/topological result is first obtained in `Diff`, then returned to `Top`:

```text
M diffeomorphic to S3
  -> M homeomorphic to S3.
```

## Imported results

1. Dimension-three triangulation and uniqueness of PL structure.
2. Compatibility and uniqueness of smooth structures in dimension three at the classification level required here.
3. Existence of a smooth Riemannian metric on a smooth paracompact manifold.
4. Diffeomorphism implies homeomorphism.

These are classical imports. WP04 does not formalize them.

## Orientation

A connected simply connected manifold is orientable: a nonorientable connected manifold has a nontrivial orientation double cover. Consequently the Poincaré profile satisfies the orientability hypothesis in Perelman III and the no-locally-separating-`RP2` condition used in Morgan–Tian’s all-time surgery theorem.

The archive does not generalize this simplification to arbitrary nonorientable input profiles. The twisted `S2`-bundle and locally separating `RP2` qualifications remain explicit in the general finite-extinction classification language.

## Boundary and compactness

`Closed` means compact without boundary. No result for open, noncompact, bounded, or incomplete manifolds is substituted. Ricci-flow completeness and compactness hypotheses are carried independently at each analytic interface.

## Connectedness

Connectedness is part of the canonical theorem. Surgery time-slices may be disconnected. WP03 therefore tracks finite active component sets rather than silently preserving connectedness through surgery. The terminal conclusion returns to the single initial connected component.

## Category-forbidden shortcuts

The following are rejected:

- selecting a smooth metric directly on an unspecified topological manifold without the category bridge;
- treating homeomorphism and diffeomorphism as definitionally identical;
- using a smooth Ricci-flow conclusion directly as a topological conclusion without the final forgetful implication;
- importing four-dimensional smoothing behavior into dimension three;
- inferring orientation from surgery rather than from the input hypothesis;
- deleting compactness or boundary hypotheses.

## Audit disposition

No category mismatch blocks the qualified archive. The bridge remains a visible classical import, and the Lean certificate is correctly described as expression-level rather than a formalization of any manifold category.