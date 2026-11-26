# CM5 R0: genuine normalized bar-column connectivity

## Result

The actual normalized horizontal bar column in positive horizontal degree
p is chain-homotopy equivalent to the p-fold tensor power of the
alternating reduced chains of the original simplicial abelian group.
For the genuine Dold–Kan object K(A,n), its vertical homology is zero
in degree q whenever q < pn. In total degree p+q, the column has no
homology below p(n+1). For p at least two, the resulting bound is 2n+2.

## Formal proof spine

- TensorComparison: form the external tensor bisimplicial integer
  module from arbitrary simplicial integer modules. Verify both
  alternating differential sums against the actual Mathlib tensor
  bicomplex, and obtain an isomorphism of bicomplexes. Apply the
  unconditional signed Eilenberg–Zilber equivalence.
- ColumnConnectivity: tensoring by a fixed chain complex preserves
  chain homotopy equivalences using Mathlib's BifunctorHomotopy.
  Iterate the comparison on the actual pointwise tensor functors.
  Compose with the established normalized Moore/tuple quotient and
  tuple quotient/tensor isomorphisms. Transport tensor support to
  homology of the original column.
- ColumnPower: compare the positive right-associated powers with
  the original left-associated tensorPower construction by explicit
  unit and associator isomorphisms. Instantiate the comparison
  directly on reducedChainsZ A n. Prove higherColumnStableVanish.

## Scope

This establishes actual column connectivity, not just support of a
surrogate tensor complex. The first-column inclusion must still be
shown to induce an isomorphism on total homology in the stable range;
the two adjacent total degrees of the higher-column bound are the
input to that filtration argument. The diagonal normalization
comparison and the weak equivalence with K(A,n+1) remain separate
obligations. No CM5 closure or independent certification is claimed.
