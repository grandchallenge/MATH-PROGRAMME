# RH-WP02 composition rules

## 1. Status is not implication

`THEOREM_PARTIAL`, `THEOREM_COMPUTATIONAL`, `STATISTICAL_PARTIAL_OR_CONJECTURAL`, and `ROUTE_CONTRACT_NOT_A_THEOREM` records do not imply `RH-T-000`.

Only an entry explicitly marked as an equivalence may be composed in both directions, and only after its normalization and quantifiers are identical to the ledger record.

## 2. Finite and asymptotic scopes remain distinct

- `RH-T-070` and `RH-T-210` certify bounded intervals only.
- `RH-T-050` controls density, not emptiness.
- `RH-T-060` controls a liminf proportion, not every zero.
- moment records control averages, not pointwise zero location.

## 3. Normalization is part of the theorem

The following may not be silently exchanged:

- `zeta`, `Lambda`, `xi`, `Xi`, and Hardy `Z`;
- `N(T)`, `N0(T)`, and `N(sigma,T)`;
- primitive, smoothed, and endpoint-modified explicit formulae;
- Fourier and Mellin transform conventions;
- real and complex spans in approximation criteria;
- strict and non-strict arithmetic inequalities;
- finite computation and continuum proof.

## 4. Noncomposable records

A record whose `composition_state` begins with `NONCOMPOSABLE` requires the named debt to be discharged before use. Citation alone does not discharge semantic correspondence.

## 5. Terminal routes

A route into `RH-T-000` must provide one of:

1. a global proof that every nontrivial zero has real part one-half;
2. a complete exact equivalent with every quantifier discharged;
3. a Hilbert–Pólya construction satisfying the full operator contract;
4. an explicit rigorously certified off-line zero, which refutes RH.

No statistical resemblance, finite verification, or sampled positivity is terminal.
