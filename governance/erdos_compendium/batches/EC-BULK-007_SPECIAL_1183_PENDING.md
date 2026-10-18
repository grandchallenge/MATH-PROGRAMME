# EC-BULK-007 — #1183 union-closed versus lattice-closed monochromatic families

**SOURCE FIDELITY PENDING; original general growth OPEN.**

- Catalogue: https://www.erdosproblems.com/1183
- Authenticated source return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2454#issuecomment-6185793768
- Original: Erdős (1978), Er78 p.39; Howorka restricted-size-class result has no located primary reference.

Two extremal functions differ: $f(n)$ requires a monochromatic family closed under **both union and intersection**, whereas $F(n)$ requires **union only**. The family need not contain the empty or universal set, and closure applies to pairs of its members. A nested chain is closed under both operations, yielding the basic pigeonhole bound $\lceil(n+1)/2\rceil$.

Independent phase21 fixture enumerates all 256 2-colorings of the Boolean lattice on three points, finding 73 nonempty meet-and-join-closed families, 121 nonempty union-closed families, and exact $f(3)=F(3)=2$. This finite equality does **not** settle the superpolynomial lower bound for arbitrary $n$.

Primary-source review must locate original Howorka theorem and its **restricted** colorings depending on subset cardinality; that special case does not imply the claim for every 2-coloring. Verify whether original conventions require nonempty intersection, and audit live comments/proof claims independently. **No general theorem or source approval.**
