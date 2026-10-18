# Erdős #41: density-forced mixed-block mass and its capacity deficit

**Disposition:** rigorous density-dependent lower bounds for mixed centered representations and a precise quantitative obstruction. **No solution to Erdős #41.**

## 1. Finite B3 bounds and centered fibers

A B3 set has unique unordered three-term sums, repetitions permitted. For a finite B3 subset of [1,N] with m elements, its binomial(m+2,3) different triple sums are in [3,3N]. Therefore

$$
\binom{m+2}{3}\le3N-2,\qquad
\boxed{m\le(18N)^{1/3}<3N^{1/3}.}\tag{U}
$$

For a finite block Z, count centered representations (unordered positive pair {a,b}, center c), with d=a+b−2c. Their total number is |Z| binomial(|Z|+1,2). Every representation at d=0 is trivial a=b=c, by B3.

For disjoint nonempty blocks X,Y in one B3 set, write x=|X|, y=|Y| and m=x+y. Call a representation *mixed* if not all three elements are in the same block. Let M(X,Y) count mixed representations, and let W(X,Y) be their **support weight**, 2 if a≠b and 1 if a=b.

## 2. Exact mixed-block identities

**Theorem 1.** For every such partition,

$$
\boxed{
M(X,Y)=xy\left(\frac{3m}{2}+1\right),\qquad
W(X,Y)=3xym.}\tag{MIX}
$$

**Proof.** Subtract the monochromatic representations from the full total:

$$
M=m\binom{m+1}{2}-x\binom{x+1}{2}-y\binom{y+1}{2}
=xy(3m/2+1).
$$

The previous centered-fiber matching theorem proves that the complete nonzero support-weight mass of a B3 set of size s is s(s²−1). Subtract the two monochromatic masses from that of the union to obtain

$$
W=m(m^2-1)-x(x^2-1)-y(y^2-1)=3xym.
$$

No mixed zero-lag representations are possible by B3, so these differences count exactly the mixed terms.

**Theorem 2 (distinct mixed lags).** At every nonzero d, the positive-pair supports of all centered representations from X∪Y form a matching. Their total support weight is at most m, hence so is the mixed subfamily. If S_mix(X,Y) denotes the distinct mixed nonzero lags,

$$
\boxed{|S_{\mathrm{mix}}(X,Y)|\ge W(X,Y)/m=3xy.}\tag{SUPPORT}
$$

This is a genuine restriction on the positions of actual mixed sums, not on enclosing shell intervals.

## 3. A density-sensitive two-scale theorem

**Theorem 3.** Suppose an *infinite* B3 set A satisfies

$$
A(t)\ge c\,t^{1/3}\quad\text{for every sufficiently large }t,
\qquad 0<c\le1.\tag{DENS}
$$

Let R=(6/c)^3. For sufficiently large N choose

$$
X=A\cap[1,N/R^2],\qquad
Y=A\cap(N/R,N].
$$

These blocks are geometrically separated: every member of Y is more than R times each member of X. Set x=|X|, y=|Y|. By (DENS),

$$
x\ge c(N/R^2)^{1/3}=\frac{c^3}{36}N^{1/3}.
$$

And, by (U) and (DENS),

$$
y=A(N)-A(N/R)
\ge[c-3R^{-1/3}]N^{1/3}
=\frac c2N^{1/3}.
$$

Combining with (MIX) and (SUPPORT), and using m=x+y≥y, gives the explicit density-forced bounds

$$
\boxed{
M(X,Y)\ge\frac{c^5}{96}N,\quad
W(X,Y)\ge\frac{c^5}{48}N,\quad
|S_{\mathrm{mix}}(X,Y)|\ge\frac{c^4}{24}N^{2/3}.
}\tag{FORCED}
$$

Thus persistent positive lower density forces **linearly many actual mixed centered representations between separated geometric scales**, occupying at least order N^(2/3) different nonzero lags. These inequalities are rigorous consequences of the density hypothesis, not conjectural overlap assumptions.

## 4. Exact matching budget: no contradiction

All centered differences of elements in [1,N] lie in [−2N,2N], containing at most 4N nonzero integer lags. Their pointwise support-weight cap is m≤A(N)<3N^(1/3). The **ambient global capacity** is therefore

$$
\boxed{\mathrm{CAP}(N)\le4Nm<12N^{4/3}.}\tag{CAP}
$$

The density-forced lower bound W≥(c^5/48)N is only linear; the ambient capacity grows like N^(4/3). Equivalently, the guaranteed distinct mixed lag set has size at least (c^4/24)N^(2/3), but O(N) different lag positions are available. These inequalities **do not establish that the matching budget is eventually exceeded**.

The missing condition can be stated as a falsifiable localization gate: if one could prove that the mixed representations of Theorem 3 must be supported on o_c(N^(2/3)) different lags, this would contradict (SUPPORT). Such localization is **not** proved and cannot be silently assumed.

## 5. An exact multicut multiplicity identity

Partition any finite B3 set into K+1 ordered blocks A_0,...,A_K. For every cut j between blocks 0..j and j+1..K, let M_j count centered representations involving elements on both sides. For an individual representation ({a,b},c), write i_a,i_b,i_c for its three block indices. It crosses exactly max(i_a,i_b,i_c)−min(i_a,i_b,i_c) cuts. Consequently

$$
\boxed{
\sum_{j=0}^{K-1}M_j
=\sum_{(\{a,b\},c)}
[\max(i_a,i_b,i_c)-\min(i_a,i_b,i_c)].
}\tag{CUT}
$$

This requires no B3 property. Summing over K geometric cuts may count the **same representation K times**. A purported logarithmic gain from the left side cannot be compared against an unweighted once-per-representation matching budget. Any valid scale-growing theorem must control this multiplicity or establish a new independence statement.

## 6. A grounded finite adversarial check

The authentic 29-element B3 fixture ending at N=50877 has normalized cardinality $29/N^{1/3}pprox0.783$. Split its elements by index into disjoint groups of sizes 14 and 15. Exhaustive exact enumeration gives **18,270** total mixed support weight distributed over **9,094** different nonzero lags. At any one lag, the maximum mixed weight is **6**, while the B3 matching cap is 29. The total ambient interval permits $4N=203,508$ nonzero slots. These are finite observational facts, not an infinite-density argument. They show that even a relatively dense finite B3 set can have little pointwise matching saturation, and therefore warn against inferring a forced overload from the total mixed mass.

## 7. Existing finite-critical obstruction and open boundary

The classical Bose–Chowla construction supplies a modular B3 set of q elements in Z/(q³−1) for every prime power q. Integer representatives yield a genuine integer B3 set of q elements in [1,q³−1]. Thus B3 sets exist with **finite-prefix cardinality of critical order N^(1/3)**. A single-scale theorem denying all such finite sets would be false. The infinite conjecture concerns maintaining such density at *every sufficiently large N in one nested infinite set*.

Source: K. O'Bryant, *Constructing Thick Bh-sets*, Journal of Integer Sequences 27 (2024), Theorem 3, https://cs.uwaterloo.ca/journals/JIS/VOL27/OBryant/obry7.pdf. For infinite context, see C. Táfula, *Infinite Sidon-type sets for zero-sum linear forms*, Monatsh. Math. 211 (2026), 315–327, DOI 10.1007/s00605-026-02211-4. Táfula's conditional general zero-sum result assumes extra control on gaps, not implied by (DENS). It also uses pairwise distinct ordered variables rather than the repeated-summand unordered positive pairs here.

**Proved here:** (MIX), (SUPPORT), (FORCED), and (CUT), including genuine density dependence and exact constants.

**Unproved:** a positive-density-dependent upper localization bound, a superlinear forced overlap of mixed fibers, any eventual violation of the pointwise matching budget, and Erdős #41. The new lower bound does not resolve the latter. An eligible successor must target an additional *cross-scale mixed-structure* estimate, not merely repeat the global capacity count. No mathematical certification, publication, or discovery-priority claim is asserted.
