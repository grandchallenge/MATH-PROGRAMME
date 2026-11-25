# CM5 R0: unconditional Eilenberg–Zilber chain comparison

## Formal result

For every bisimplicial integer module B, the actual Alexander–Whitney
chain map from alternating diagonal chains to the signed total complex
is a natural chain-homotopy equivalence. No assumed Eilenberg–Zilber
theorem is used. The reverse chain map agrees with the explicit signed
shuffle in degrees zero and one and is constructed by acyclic-model
cycle filling in higher degrees. The two actual chain homotopies are
instantiated using the verified universal diagonal and total homotopy
constructors.

## Dependency spine

- Shuffle: naturality of the signed shuffle family; its chain law iff
  its residual vanishes on every free representable summand generator.
- TotalHomotopy: totalization of a horizontal chain homotopy. Horizontal
  terms reproduce the homotopy relation; vertical terms cancel because
  raising horizontal degree reverses the Koszul sign.
- HorizontalModel: prepend initial vertex in the first coordinate of
  the free model, naturally in the vertical coordinate, and linearize.
- SingleTotal: totalization of a horizontal complex concentrated in
  degree zero is canonically isomorphic to its vertical complex.
- TotalModel: totalized horizontal contraction followed by the vertical
  contraction; positive-degree cycle filling on the actual total model.
- TotalSide: universal natural homotopy of total chain maps agreeing
  in degree zero.
- Zero: both explicit signed-shuffle/AW degree-zero composites are identity.
- Axes: the signed path family on either axis consists of a unique
  positively signed path, and its differential identity holds in all
  axis bidegrees; in particular the full degree-one chain identity holds.
- Comparison: reverseDegree and reverseNat extend the signed shuffle
  in degrees zero and one by explicit universal-model cone filling.
  The homotopy equivalence comparison is unconditional. signedComparison
  gives the same result for the explicit signed formula conditional on
  its remaining universal boundary identity.

## Claim boundary

The interior signed-shuffle differential identity is not yet formally
proved. The reverse map above is not asserted to be the signed shuffle
in higher degrees. The unconditional homotopy equivalence suffices to
advance the tensor-support and diagonal comparisons without that identity.
The actual normalized-column support transfer, filtered bar suspension,
and comparison with the next Dold–Kan object remain to be formally
instantiated. No CM5 closure, independent certification, or promotion
is asserted.
