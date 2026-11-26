# CM5 R0: stable suspension on actual reduced chains

The objectwise stable suspension theorem is verified in Lean, for every
abelian group A and all nonnegative n,k with k < n:
the homology of the genuine reduced chains of K(A,n) in degree n+k is
isomorphic to that of K(A,n+1) in degree n+k+1.
The actual map from the suspended reduced chains is fullSuspensionMap;
fullSuspension_isIso proves that its homology map is invertible in total
degrees j < 2n+1. No ordinary additive homology is substituted for
reduced free homology.

## Proof spine

- Interval: form the free interval cylinder as the diagonal of a
  bisimplicial integer module, with a coproduct indexed by maps into
  the ordered interval. The endpoint inclusions are natural.
- IntervalFill and IntervalChain: on each interval vertex use the
  corresponding endpoint chain map; on the nonconstant edge use
  minus the given chain homotopy, and on higher interval degrees use
  zero. Verify the two signed differential contributions. In interval
  degree two the alternating coefficient of the nonconstant edge
  cancels. This gives a genuine total chain map.
- IntervalEndpoints: compose with Alexander–Whitney; all nonzero cut
  degrees vanish on a constant endpoint, leaving precisely the
  prescribed chain map in cut degree zero.
- IntervalLift: normalize the filler and lift by Dold–Kan full
  faithfulness. Both simplicial endpoints are exactly the prescribed
  maps.
- IntervalPrism: construct the actual prism maps and verify all
  simplicial face and degeneracy identities. Postcompose with the
  lifted cylinder map to obtain a genuine simplicial homotopy.
- MooreHomotopyTransport: extend Moore homotopies to alternating
  chains by natural normalization, pass to integer modules, construct
  the simplicial homotopy, and transport back to abelian groups.
  Whisker by the non-additive reduced free functor and use the
  simplicial-to-chain homotopy theorem.
- ReducedNext: instantiate both homotopies for nextMap and
  nextInverse. Compose the resulting reduced chain-homotopy
  equivalence with the actual stable diagonal suspension.
- SuspensionDegree: identify each positive total degree of the
  horizontal single-one complex with its vertical term. The
  differential acquires a minus sign. An actual short-complex
  isomorphism gives the homology shift, hence stableSuspension.

## Scope

The objectwise stable range is established without additional
axioms. Functorial packaging of the stable suspension maps,
finite generation and additivity of the stable lattice homology,
finite-projective resolution extraction, condensed sheaf and
derived analytic comparisons, and genuine solid-source derived
biduality are distinct downstream obligations. No independent
certification is asserted.
