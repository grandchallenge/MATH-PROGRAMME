# CM5 R0: actual additive bar map to the next Dold–Kan object

## Result

For every abelian group A and nonnegative integer n, the ordinary
normalized Moore complex of the diagonal bar of K(A,n) is
chain-homotopy equivalent to that of K(A,n+1). Dold–Kan full
faithfulness constructs actual simplicial group maps nextMap
and nextInverse with precisely those normalized chain maps.
The map nextMap induces an isomorphism on ordinary Moore homology
in every degree.

## Proof spine

- AdditiveBarMoore: in the ordinary group-valued bar object, deleting
  the last vertex drops the last edge, and the penultimate face merges
  the final two edges. The two higher-face conditions in degree at
  least two force every edge to vanish. Degree zero is zero and
  degree one is naturally isomorphic to A. Thus the actual Moore
  complex is naturally isomorphic to the single complex in degree one.
- DiagramNormalization and DiagramComparison: generalize the verified
  horizontal normalization and Eilenberg–Zilber comparison to any
  simplicial-group-valued diagram. This permits application to the
  ordinary bar functor, not just the reduced free bar functor.
- AdditiveBarTotal: identify the ordinary normalized bar diagram with
  a single-degree diagram. Verify the totalization symmetry sign
  given by (-1) raised to the product of the two degrees. Use the
  Dold–Kan counit and normalization homotopy to replace the input
  alternating chains by the single complex in degree n. The actual
  ordinary diagonal chains are equivalent to a double single total.
- AdditiveBarShift: the double single total has exactly one surviving
  bidegree, with total degree n+1. Explicit summand maps identify
  this total complex with the single complex containing A in degree
  n+1. Compare with the actual next Eilenberg–MacLane object.
- AdditiveNextMap: forget integer scalar structure, normalize both
  chain complexes, and lift the actual homotopy-equivalence maps by
  the full faithfulness of Dold–Kan. The theorem nextMap_homology_isIso
  is about the actual simplicial map.

## Remaining obligation

The chain-homotopy equivalence of ordinary Moore complexes must
still be transported through reducedFree, which is not additive.
The available Mathlib simplicial-homotopy machinery sends simplicial
homotopies to alternating-chain homotopies and permits whiskering
by arbitrary functors; the reverse construction from normalized
chain homotopies has not yet been established here. A concrete
route is the Dold–Kan tensor interval cylinder with Alexander–Whitney,
or an independently verified simplicial weak-equivalence/homology
invariance theorem. Neither can be replaced by asserting that
reducedFree preserves ordinary chain homotopies. No complete
stable suspension theorem or CM5 certification is claimed.
