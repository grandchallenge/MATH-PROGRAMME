# Infinite, source-faithful B3 predicate countermodels

This is an elementary theorem about **definitions**, not a result on the Erdős #41 open asymptotic conjecture. It strengthens the finite evidence in source-dossier PR #2691. All sets are subsets of positive integers.

Let H(A) say that distinct finite subsets of A having at most three elements have different sums (the historical coefficient-zero-or-one convention on Erdős 1980, pp.98–99). Let M(A) say that distinct size-three **multisets**, allowing repetition, have different sums (the current Formal Conjectures provider's strong B3 convention).

## An infinite H-set that fails M

Take A={1,2,4} union {10^k:k=1,2,...}. The sequence is strictly superincreasing: 2>1, 4>1+2 and, for k>=1, 10^k > 7 + sum_{i=1}^{k-1} 10^i. If two finite subsets of A have the same sum, look at the largest element belonging to exactly one subset: it exceeds the sum of every smaller element and so prevents equality. Hence **all distinct finite-subset sums** are unique, implying H(A).

But the different size-three multisets [1,1,4] and [2,2,2] both sum to 6. Thus M(A) is false. This obstruction is inherited by the infinite set and cannot be dismissed as a finite-carrier artifact.

## An infinite M-set that fails H

Take B={1,4,5} union {100^k:k=1,2,...}. For k>=1, 100^k > 3(10 + sum_{i=1}^{k-1}100^i). Thus, for two sums of **exactly three** terms with repetition, if coefficients of the largest tail power differ, its contribution cannot be cancelled by at most three smaller terms. Working down the tail, equal sums have identical tail multiplicities.

After cancelling identical tail multiplicities, the remaining base terms are drawn from {1,4,5} with identical fixed cardinality 0<=ell<=3. If beta and gamma are the counts of 4 and 5, the sum is ell+3 beta+4 gamma. Equality yields 3(delta beta)+4(delta gamma)=0; since |delta beta|<=3, integer divisibility forces delta beta=delta gamma=0. Hence B satisfies M(B) for all triples, including repeated entries.

However {5} and {1,4} are different distinct-element subsets with the same sum 5, so H(B) is false.

**Conclusion:** H and M are logically incomparable even among infinite subsets of positive natural numbers. Both imply the very weak predicate of unique sums over fixed-cardinality three-element subsets, but neither is a substitute for the other. Source #41 must not be certified using a theorem about the wrong variant.

## Machine validation and scope

The accompanying source `erdos41_infinite_models.py` exhaustively checks both properties for eight successive finite prefixes of these two infinite families. The proof above handles every index and does not extrapolate a finite computation to infinity. The suite's role is to catch transcription and convention errors.

This does not prove or disprove the original Erdős liminf-density question; both exhibited sets have zero counting-density normalization at the relevant scale. The original and new provider theorem types still require separately named and governed source specifications and an actual imported Lean predicate bridge. Preserve `gcl-review:revise` for #2536 pending those actions.
