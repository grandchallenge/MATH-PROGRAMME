# Erdős #41: historical B3 definition is not interchangeable with strong multisets

Original: P. Erdős, *A survey of problems in combinatorial number theory*, Annals of Discrete Mathematics 6 (1980), pp. 98–99, https://static.renyi.hu/~p_erdos/1980-03.pdf . The inspected publisher scan SHA256 is e2280c6cbba6bfecedb5c5134ce827c59695dccd7f3377d42658cbc30b8db3cf.

On printed p. 98 Erdős recalls Sidon's B_r convention through sums of at most r terms with coefficient epsilon_i equal to 0 or 1, equivalently sums of DISTINCT selected terms. Printed p. 99 explicitly discusses the OPEN infinite B3 growth problem, limsup a_k/k^3. The reference thereby supports a historical distinct-term, at-most-three interpretation. It does not independently establish that repeated summands are quantified by the 1980 source.

The originally pinned Lean Finset 3-subset uniqueness is weaker than the p. 98 at-most-three, cross-cardinality condition. The freshly fetched Lean Multiset, exactly three entries with repetition, imposes a different restriction, **not equivalent** to the scanned 1980 convention. The retained upstream implementation is a valid strong modern version, not an established formal equivalent of the historical claim.

Two finite mathematical countermodels prove non-equivalence in both directions. A={1,2,4} has all nonempty sums of at most three distinct elements different, but 1+1+4=2+2+2, so repeated three-multiset sums collide. Conversely A={1,4,5} has different repeated three-multiset sums, yet the distinct-subset sums collide because 1+4=5. A={1,2,3} passes the old exactly-three Finset condition vacuously but fails the strong Multiset condition (1+1+3=1+2+2). None of these finite examples settles the open infinite conjecture.

Executable `python3 governance/source_erdos_critical_005/erdos41_conventions.py` checks both separating examples plus 793 finite carrier cases, confirming each stricter property implies fixed-cardinality Finset uniqueness, but not a converse or historical-modern equivalence.

**Source-fidelity disposition:** historical source ambiguity is resolved in the narrow sense that the 1980 printed convention has been identified. The full #41 research-source correction remains pending, because old and new formal predicates both differ from that at-most-three historical definition. Do not clear #2536 `gcl-review:revise`, certify the B3 conjecture, or replace its immutable source issue with the upstream provider. A further exact Lean three-predicate bridge or separately named variants and historical-status editorial decision is required.
