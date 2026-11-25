# Erdős #561 — bilateral vertex support strengthens the all-length BLUE matching theorem

**2026-11-24. Paper status UNDER_REVIEW.** Hosts are arbitrary finite simple graphs, forests are ordinary non-induced vertex-disjoint positive stars. The unrestricted Erdős #561 conjecture and joint residual hypothesis #3490 remain OPEN/PARTIAL; no MATHCERT or historical priority claim.

**New observation:** BOTH complete original forests survive deletion of every vertex of a JOINT residual host. The previous one-BLUE-matching theorem used only the RED forest vertex-support bound. Allowing EITHER forest to supply the bound yields a strictly stronger arbitrary-host theorem.

## Theorem A: a bilateral Gallai matching obstruction

Let original red forest F(n) have s positive star components, and blue F(m) have t positive components, with s>=t>=3. Let R denote the greater of their exact vertex counts:

$$
R=\max\left(\sum_{i=1}^s(n_i+1),\sum_{j=1}^t(m_j+1)\right).
$$

If R>=3s-1, then every finite simple graph Q jointly arrowing both original residual pairs satisfies

$$
\boxed{\nu(Q)\ge s+1.}
$$

**Proof.** Fix any vertex z. Colour all edges at z BLUE, the rest RED. The blue incident-star graph has one-vertex cover and therefore cannot contain the two-or-more disjoint positive stars of the BLUE residual F(m_2,...,m_t). The second joint arrow forces the entire red F(n) inside Q-z. Conversely colour incident edges RED, the remainder BLUE. The red incident-star graph cannot contain F(n_2,...,n_s), which has at least two components, so the first joint arrow forces the entire blue F(m) inside Q-z.

Thus Q-z contains copies of BOTH full forests, separately, for every z. In particular its matching number is >=s, so that of Q is >=s. Assume equality ν(Q)=s. Every deletion preserves matching number s. Classical Gallai matching stability makes each nontrivial connected component factor-critical; summing their orders 2ν(C)+1 shows that Q has at most 3s nonisolated vertices.

Choose a nonisolated z. Because Q-z contains both full forests, Q has at least R+1>=3s nonisolated vertices. Thus equality holds and Q is precisely s disjoint triangles up to isolates.

If red F(n) has at least 3s-1 vertices, colour s-1 triangles entirely RED and one BLUE. Red is supported on only 3s-3 vertices, too few for full F(n); blue is supported on only three, too few for the two blue residual stars F(m_2,...,m_t). This avoids the second joint relation.

Otherwise blue F(m) has at least 3s-1 vertices. Colour s-1 triangles entirely BLUE and one RED. Blue has only 3s-3 vertices, too few for full F(m); red has only three, too few for F(n_2,...,n_s), which has at least two disjoint positive components and needs at least four vertices. This avoids the first joint relation. Both cases contradict joint arrowing, so ν(Q)>=s+1. QED.

The theorem is genuinely about all finite simple host graphs, not only disjoint-star hosts.

## Theorem B: exact all-s BLUE matching under either forest's support

Let original sorted red n=(n_1,...,n_s) have s>=3 positive stars, and original BLUE m=(u,v,g) have three sorted positive stars. Normalize

$$
a_i=n_i-n_s+1,\quad U=u-g+1,\quad V=v-g+1,
$$

so a_s=1 and normalized blue is (U,V,1). Assume V>=2. Define the normalized **bilateral** vertex budget

$$
R^\flat=\max\left(\sum_{i=1}^s(a_i+1),\ U+V+4\right).
$$

For each i=1,...,s-1 define

$$
T_i=\max\left(a_{i+1}+V-1,\quad a_{i+2}+U-1\text{ when }i+2\le s\right)
$$

with the second candidate omitted when absent, and

$$
P_{\rm BLUE}=\sum_{i=1}^{s-1}(a_i-T_i)_+.
$$

**Quantitative arbitrary-host conclusion.** When Rflat>=3s-1 and V>=2, every JOINT host satisfies

$$
\boxed{e(Q)\ge J_{\rm can}(n,m)-P_{\rm BLUE}.}
$$

In particular if P_BLUE=0, the exact JOINT residual minimum equals the canonical antidiagonal sum. This is an unbounded theorem for ANY number s of red stars. The original size Ramsey value is also sharp whenever one of the separately source-proved original transfers applies to its proved sharp JOINT premise.

**Proof.** At every intermediate uniform RED or BLUE terminal-size decrement, the full original forests have vertex counts no smaller than their normalized minima. Thus the bilateral condition Rflat>=3s-1 persists; Theorem A forces a matching of at least s+1 edges at every step.

Colour a deleted matching RED to uniformly decrement all red arms, or BLUE to uniformly decrement all three blue arms, while preserving both joint residual arrows. Each decrement reduces the s+1 nonleading canonical antidiagonal weights by exactly one. This legally reaches the original normalized lists a=(a_1,...,a_{s-1},1) and (U,V,1).

Remove one more matching of at least s+1 edges, coloured BLUE in both extensions. Its removal leaves exactly the two JOINT residual relations for original red a and original blue pair (U-1,V-1), whose arms remain positive. After swapping colours, apply the previously source-proved complete two-component JOINT residual bridge, Lemma 1 of THREE_BY_THREE_JOINT_RECONSTRUCTION.md, valid for arbitrary other-side component count.

The exact antidiagonal identity from ALL_S_BLUE_MATCHING_SINGLE_STEP_THEOREM.md remains unchanged:

$$
J_{\rm can}(a,(U,V,1))
=(s+1)+J_{\rm can}(a,(U-1,V-1))+P_{\rm BLUE}.
$$

Adding the removed matching edges and undoing the legal normalization steps proves the quantitative lower. Canonical star hosts provide the sharp upper when P_BLUE=0. No unrestricted joint conjecture is used. QED.

## A new positive-switching example

Take red n=(3,1,1,1) and blue m=(4,3,1). Here s=4 and 3s-1=11. Red requires only ten vertices, so it fails the old RED-only matching hypothesis. Blue requires eleven, satisfying the new **bilateral** hypothesis. The deficit P_BLUE vanishes.

The canonical original antidiagonal weights are (6,5,4,4,3,1), so J=17, W=23. The two individually required residual canonical totals are only 16 and 15. Therefore the new theorem proves

$$
\boxed{\mathcal J((3,1,1,1),(4,3,1))=17.}
$$

The source-proved original core transfer also applies because the leading sizes 3 and 4 have opposite parity and W=23<=D(D+1)=30 for D=5. Hence

$$
\boxed{\widehat r(F(3,1,1,1),F(4,3,1))=23.}
$$

These hold for arbitrary host graph topology.

## Finite proof-tree extension and remaining boundary

The dependent checker imports the protected 54-claim fifth-core proof engine UNMODIFIED. It inserts the bilateral BLUE zero-loss rule only after checking V>=2, Rflat>=3s-1 and P_BLUE=0. New ORIGINAL proof traces require independently certified sharp JOINT of the same original lists. Additional JOINT proof rules may depend on newly proved ORIGINAL for a STRICTLY shorter red list, or source-proved zero-loss RED matching to a strictly shorter red list, so the procedure is well founded.

In the 179,928-profile declared bounded grid, exactly 355 profiles satisfy zero BLUE deficit and are rescued by BLUE support after failing the RED-only vertex threshold. Of those, 304 were already proved by other source rules and 51 become newly sharp directly. Recursive propagation yields **74 further exact JOINT** and **55 further exact ORIGINAL** classifications beyond the protected fifth-core engine. The finite counts are corroboration, not proof by enumeration of arbitrary hosts.

Profiles with positive P_BLUE, V=1, or insufficient support for BOTH forests remain unresolved under this particular transfer, and other separate source rules may still apply. The full Erdős #561 conjecture, arbitrary-profile joint residual problem, and MATHCERT remain OPEN/PARTIAL.