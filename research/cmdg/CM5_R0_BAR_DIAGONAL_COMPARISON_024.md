# CM5 R0: actual reduced bar diagonal comparison

## Result

The actual horizontally normalized reduced bar total and the reduced
alternating chains of its diagonal simplicial abelian group are
chain-homotopy equivalent for every simplicial abelian group X.
For X = K(A,n), the composite of the previously verified
reducedSuspensionMap with this comparison's inverse induces an
isomorphism on homology in total degree j < 2n+1.

## Proof spine

- NormalizationNaturality: the inductively constructed homotopies
  from the Dold–Kan projections P to identity commute with every
  simplicial abelian group morphism. Pass to the degreewise
  eventually constant homotopy from PInfty to identity.
- BarNormalization: whisker the actual Moore inclusion and
  projection along X and apply integer-module chains. The natural
  homotopy gives an actual horizontal homotopy of bicomplexes.
  The verified signed totalization homotopy lifts it. The opposite
  composite is exactly identity, so normalizationEquiv is a
  chain-homotopy equivalence using the actual inclusion/projection.
- BarDiagonalComparison: construct the reduced bisimplicial bar
  module with horizontal index first. Check that each horizontal
  and vertical differential is the corresponding alternating
  face sum; obtain an isomorphism of raw bicomplexes with the
  Eilenberg–Zilber double complex. Identify the diagonal via the
  naturality and composition of the actual bar maps. Apply the
  signed Alexander–Whitney/shuffle equivalence, and the
  normalization equivalence.
- DiagonalSuspension: compose the actual reduced suspension map
  with the inverse of diagonalComparison; transport the stable
  homology isomorphism through this actual chain map.

## Scope

The normalized total-to-diagonal comparison is complete. The
diagonal bar group still needs comparison with K(A,n+1) in a way
that transports reduced free chains, rather than merely additive
Moore homology. The full stable homology and CM5 derived biduality
claims remain open. No independent certification is asserted.
