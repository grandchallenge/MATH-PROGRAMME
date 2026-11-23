# CSM-01-WP01 — exact typed open-network semantics and finite obstruction

**Programme:** CSM-001. **Status:** finite mathematical proof candidate plus executable exact-arithmetic specimen; internal review pending. **Claim boundary:** elementary prior mathematics, not an original discovery, infinite-volume Gibbs theorem or MATHCERT certificate. Source-semantic G0 audit remains open.

## Objects and boundary conventions

An open network consists of a finite set of variables $V$, a nonempty finite state set $D_v$ for each variable, ordered input and output port lists $I,O$ without repeated ports within either list, and a finite multiset of nonnegative rational factors. Each factor is a complete table on a finite subset of the variables. A variable may occur in several factors; it represents one shared state. The same variable may serve as input and output, expressing a direct identity wire.

Let $H$ consist of variables which appear on neither boundary. For a fixed input tuple $x$ and output tuple $y$, with compatible values wherever a variable belongs to both boundaries, define

$$
\llbracket N\rrbracket(y,x)
=\sum_{h\in\prod_{v\in H}D_v}\prod_{f\in F} f((x,y,h)|_{S_f}).
$$

If shared boundary assignments disagree, the entry is zero. Empty products are one; an empty assignment space has one element. This convention also yields a scalar partition function for a closed network. These are **unnormalized** weights, not Markov kernels.

## Elementary finite semantics lemma

For compatible typed networks $N:I\to J$ and $M:J\to K$, gluing first renames their variables disjointly, then identifies corresponding output and input variables. Variables on the identified interface are summed out unless they remain on an external boundary. A tensor product is disjoint union with concatenated port lists; identity has coincident input and output variable names; swap exchanges port order. Copying is an explicit three-port equality factor; deleting is the empty-factor network with one input and no output.

The evaluation satisfies

$$
\llbracket M\circ N\rrbracket(z,x)
=\sum_{y\in D_J}\llbracket M\rrbracket(z,y)\llbracket N\rrbracket(y,x)
$$

and

$$
\llbracket N\otimes M\rrbracket
=\llbracket N\rrbracket\otimes\llbracket M\rrbracket.
$$

**Proof.** Fix the external assignments. Any consistent assignment of the glued diagram is uniquely determined by a compatible assignment to the identified interface and assignments to the two original networks' internal variables. The product of factors splits into a product of factors belonging to the two original networks. Distributivity permits the two finite internal sums to be separated, giving matrix multiplication. Where an interface port is also external, consistency fixes that port's value, as reflected in the Kronecker constraints. For disjoint union, variable assignments and factor products are independent, so the finite sum is a product, giving the Kronecker matrix tensor. Identity and swap evaluate to their usual Kronecker-delta matrices. Dummy-variable renaming and factor ordering do not affect evaluation. Thus association of gluing, tensor interchange, symmetry, and copy/delete counit and coassociativity hold up to the canonical boundary-preserving network relabelings. QED.

This gives a symmetric monoidal semantics of typed diagrams into the category of nonnegative-rational matrices. Raw code representations may differ by fresh variable names; categorical equations are between their diagrams and denotations, not literal Python object identities.

## Worked marginalization and an exact interaction obstruction

Take visible binary spins $a,b,c$ and a hidden binary spin $u$. Give the hidden spin a field $h(0)=1$ and $h(1)=2$. Every bond has weight two for equal spins and one for unequal spins. Marginalize $u$:

$$
W(a,b,c)=\sum_{u\in\{0,1\}}h(u)b(u,a)b(u,b)b(u,c).
$$

| Assignment | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Effective weight | 10 | 8 | 8 | 10 | 8 | 10 | 10 | 17 |

These weights total $81$, matching the independent microscopic calculation $(1+2)(2+1)^3=81$.

**Factor-width obstruction.** A strictly positive weight on three binary spins that factors entirely into factors depending on at most two spins must satisfy equality of even-parity and odd-parity products:

$$
\prod_{a+b+c\ \mathrm{even}}W(a,b,c)
=\prod_{a+b+c\ \mathrm{odd}}W(a,b,c).
$$

**Proof.** Each factor omits at least one spin. Holding all its arguments fixed, assignments to the omitted spins have equal even and odd parity counts. That factor therefore contributes equally to both parity products. Multiply these equalities over all factors. QED.

In the explicit network above the even product equals $10^4=10000$, whereas the odd product equals $8^3\cdot17=8704$. Therefore the effective weight **cannot be factored solely into arbitrary one-spin and two-spin positive factors**. Marginalization has generated an irreducible three-body interaction, despite the microscopic network containing only one-body and two-body factors. This is an exact, elementary finite example; it is **not** evidence of infinite-volume non-Gibbsianness or mathematical novelty.

## Replay, complexity, and limits

The exact-rational evaluator is in `research/csm-001/open_networks.py`; the separately constructed tests are in `tests/test_csm_open_networks.py`. They check typed gluing versus independent matrix multiplication, associativity, tensor interchange, identities, swaps, copy/delete equations, closed scalar evaluation, validation failures, full hidden-spin enumeration, and the parity obstruction. No GPU or stochastic sampling is needed for this finite exact specimen.

If the input, output, and internal assignment counts are $B_I,B_O,H$ with $m$ factors, direct enumeration takes at most $O(B_IB_OHm)$ arithmetic operations and $O(B_IB_O)$ matrix-result storage beyond the factor tables. It is a correctness reference, not an optimized contraction algorithm.

**Unresolved:** G0 theorem-level prior-art/source lock; any new G2 Gibbs preservation or obstruction theorem; G3 DLR and infinite-volume regularity; CSM-02 entropy compatibility; and conditional G4 quantum/dynamical scope. The finite proof and tests do not discharge these obligations.
