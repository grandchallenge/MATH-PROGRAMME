# Erdős #41 — No-go for three-colour window-envelope Hall pressure under persistent critical occupancy

**21 October 2026.** Exact infinite **occupancy-profile countermodel** to deriving a B3 density valley from cumulative lower density plus ALL three-distinct-colour window-envelope Hall inequalities. The construction uses genuine finite B3 blocks INSIDE each separate window but **does not establish the union is B3**. No resolution of Erdős #41, and no claim that all arithmetic compatibility tests pass.

This is a limitation of the candidate sufficient forcing gate developed in \`MULTISCALE_MIXED_COLOUR_RESONANCE_FORCING.md\`, not an objection to the exact sixth-defect identity.

## Theorem: permanently positive lower critical occupancy, yet every coloured-window envelope cut is feasible

Fix any integer K>=5. For every integer j>=0 define

$$
R_j=(16K)^3\,64^j,\qquad
m_j=K\,4^j=\frac1{16}R_j^{1/3},\qquad
J_j=(R_j,2R_j]\cap\mathbb Z.
$$

Then all of the following hold.

**(1) Genuine individual B3 occupancy.** There exists a finite repetition-permitted B3 block $B_j\subseteq J_j$ containing **exactly** $m_j$ integers, for every j. The blocks are automatically pairwise disjoint.

Indeed by Bertrand's postulate, for each m_j>=5 there is a prime $m_j\le p_j\le2m_j$. The finite-field moment code from the protected first-tranche notes supplies a p_j-point genuine B3 set contained in [1,W_j] with

$$
W_j<12p_j^3\le96m_j^3=\frac{96}{4096}R_j<R_j.
$$

Select any $m_j$ of those p_j points and translate them by R_j. The resulting B_j is individually B3 within J_j. **We make NO claim that their infinite union is globally B3**: cross-window triple-sum collisions and reciprocal constraints have not been established.

**(2) Persistent positive cumulative critical-order counting function.** Put $E=\bigcup_{j\ge0}B_j$, without assuming E is B3. Then

$$
\boxed{
|E\cap[1,N]|\ge\frac1{256}N^{1/3}
\quad\text{for all integers }N\ge R_1.
}
\tag{PERSISTENT-WINDOW-PROFILE}
$$

To see this, let $R_j\le N<R_{j+1}$ (j>=1). The entire preceding block B_(j−1) lies below $2R_(j−1)<R_j$, so the number of points at or below N is at least $m_{j-1}=m_j/4=R_j^{1/3}/64$. On the other hand $N^{1/3}<R_(j+1)^{1/3}=4R_j^{1/3}$. This proves the stated coefficient, uniformly through arbitrarily large gaps between the occupied windows.

**(3) Every selected three-distinct-colour envelope Hall cut passes.** For i<j<k let the window-envelope of their mixed triple colour type be

$$
I_{ijk}=
[R_i+R_j+R_k+3,\ 2R_i+2R_j+2R_k]\cap\mathbb Z,
$$

and define its demand $M_{ijk}=m_im_jm_k$. For **EVERY finite nonempty collection $\mathcal F$** of distinct-colour triples i<j<k, the window-level three-colour Hall inequality holds:

$$
\boxed{
\sum_{(i,j,k)\in\mathcal F}m_im_jm_k
\le
\left|\bigcup_{(i,j,k)\in\mathcal F}I_{ijk}\right|.
}
\tag{ALL-MULTISCALE-WINDOW-HALL-CUTS}
$$

**Proof of (3).** Partition $\mathcal F$ into groups $\mathcal F_k$ according to the largest colour index k. The total population demand for *all* triple types with maximal index k (and hence for any subfamily) satisfies

$$
M_k:=m_k\sum_{0\le i<j<k}m_im_j
\le
\frac{m_k}{2}\left(\sum_{i<k}m_i\right)^2
<
\frac{m_k^3}{18}
=
\frac{R_k}{73728}.
$$

Here $\sum_{i<k}m_i=K(4^k-1)/3<m_k/3$. Every interval $I_{ijk}$ with i<j<k contains the **common core**

$$
C_k=[R_k+2R_{k-1}+3,\ 2R_k]\cap\mathbb Z,
$$

because both earlier window starts are at most R_(k−1), and both earlier window ends are nonnegative. Since R_(k−1)=R_k/64, the core has $|C_k|=(31/32)R_k-2>R_k/2$. Therefore the union of envelopes from ANY nonempty subfamily $\mathcal F_k$ has size exceeding R_k/2, much larger than its combined demand M_k.

Envelopes belonging to different maximal indices k are mutually disjoint: the upper endpoint of any i<j<k envelope is at most

$$
2(R_k+R_{k-1}+R_{k-2})<3R_k,
$$

whereas the lower endpoint of any type with largest index k+1 is at least $R_{k+1}+3=64R_k+3$. Hence the demand and union capacities add across the groups k. Summing the proven inequalities establishes the displayed statement for all finite families. QED.

## Precise interpretation, and the remaining mathematical work

The exact three-colour Hall-to-sixth-defect theorem gives a real positive collision whenever its demand exceeds the union of the TRUE envelopes. However, the hypotheses

- cumulative lower critical density at **every sufficiently large integer**, and
- critically populated genuinely B3 **individual** shell windows,

do **not** force violation of **ANY** three-distinct-colour HALL cut computed from these declared shell-window envelopes, even across infinitely many scales. Our construction demonstrates this with an explicit fixed lower coefficient 1/256.

This does not establish that any actual global B3 set can realize the occupancy profile; other constraints can still obstruct it, including:

- actual narrower within-window supports, beyond the coarse declared envelopes;
- repeated-colour triple types (XXY, XYY, XXX);
- collisions BETWEEN different types even when each individual envelope has spare room;
- arithmetic avoidance of the exact mixed-pair difference correlations $K_{XY}(d)G_Z(d)$;
- dependencies across growing prefixes not visible to the envelope bookkeeping.

The next worthwhile mathematical object is therefore a **fine-grained arithmetic occupancy/resonance invariant**, which must distinguish actual integer supports and signed-sum coincidences from feasible scalar window envelopes. The proof may combine richer Fourier cross-moments, exact sumset overlap geometry, or an adaptive integer hypergraph capacity certificate. Simply enlarging the family of *coarse* three-distinct-colour envelope cuts cannot prove Erdős #41.

**Governance:** candidate author theorem for GCL coordinator #2789, Track A #2790, Track B #2791, Track D #2793, with independent review #2792 required. Related PR #2808; parent Erdős #41 remains open.
