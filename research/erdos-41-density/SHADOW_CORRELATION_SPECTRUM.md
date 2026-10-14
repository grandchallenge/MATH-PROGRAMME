# Erdős #41: exact pair-sum autocorrelation on the B3 difference spectrum

**Disposition:** elementary but exact arithmetic-combinatorial theorems, a multi-block difference-exclusion consequence, and a no-go for the naive second-order Gram/positive-definiteness approach. Erdős #41 remains OPEN. No novelty priority is claimed.

## Definitions

Let A be a finite repetition-allowed B3 set of positive integers: all unordered three-element multisets drawn from A have different sums. This implies B2 pair-sum uniqueness, because a collision of two unordered pair sums can be padded with a common third element of A; the empty case is trivial.

For X contained in A, write n=|X| and let

$$
P_X=\{u+v:u,v\in X\},\qquad q=|P_X|=\binom{n+1}{2}.
$$

Repeated pair entries are permitted. For every integer d define the ordered pair-sum autocorrelation

$$
r_X(d)=|\{(p,p')\in P_X^2:p-p'=d\}|.
$$

When X is empty, P_X is empty and every r_X(d)=0.

## Exact autocorrelation selector theorem

**Theorem A.** For each pair of distinct a,b in A,

$$
\boxed{r_X(a-b)=n\,\boldsymbol{1}_{a\in X}\boldsymbol{1}_{b\in X}.}\tag{AC}
$$

Also r_X(0)=q.

**Proof.** An equality p-p'=a-b is equivalent to p+b=p'+a. The terms p and p' uniquely correspond to unordered pairs from X by B2. Thus the latter equality compares two three-element multisets drawn from A.

If a,b belong to X, B3 uniqueness forces the two triples to be equal. Since a is different from b, a must occur in the pair for p and b must occur in the pair for p'. Cancelling these occurrences gives a common x in X, so p=a+x and p'=b+x. Conversely every x in X supplies exactly one such solution; B2 makes the representations unique. Hence r_X(a-b)=n.

If a is outside X but b belongs to X, the left triple contains three X elements, while the right triple contains the outsider a: equality is impossible. If b lies outside X while a belongs to X, reverse the argument. If both a and b lie outside X and a!=b, each side contains a different unique outsider; the triples cannot agree. Thus r_X(a-b)=0 in all these cases.

The diagonal r_X(0)=q follows from p=p' and pair-sum uniqueness.

**Corollary A1.** The nonzero ordered differences of an M3 set are pairwise unique, as for any Sidon/B2 set. Hence if |A|=m,

$$
|D(A)|=m(m-1)+1,\qquad D(A)=\{a-b:a,b\in A\}.
$$

For X of size n the exact restriction (AC) implies

$$
\boxed{\sum_{d\in D(A)\setminus\{0\}}r_X(d)=n^2(n-1),}\tag{ACSUM}
$$

and r_X vanishes on the other m(m-1)-n(n-1) nonzero differences of A.

## Cross-pair-sum exclusion on every block pair

**Theorem B.** If X and Y are disjoint subsets of a finite B3 set A, then

$$
\boxed{(P_X-P_Y)\cap D(A)=\varnothing.}\tag{CROSS0}
$$

**Proof.** A putative intersection gives p_X-p_Y=a-b for p_X a sum of two members of X, p_Y a sum of two members of Y, and a,b in A. Rearrangement yields p_X+b=p_Y+a. The left triple contains *at least two X terms* whereas the right triple contains *at most one X term*, because Y is disjoint from X. Thus these cannot be the same three-element multiset, contradicting B3. This covers a=b and empty-block cases without exceptions.

In particular, when X and Y are nonempty, P_X-P_Y is a nonempty set entirely in the complement of A-A. Standard integer sumset growth gives

$$
|P_X-P_Y|\ge |P_X|+|P_Y|-1
=\binom{|X|+1}{2}+\binom{|Y|+1}{2}-1.
$$

The inability to sum these forbidden-spectrum sizes is not merely hypothetical. In the genuine B3 greedy prefix with blocks (X_0={1,2,5}), (X_1={14,33,72}), (X_2={125,219,376}), the number (-435) belongs to **both** cross spectra:

$$
3-438=(1+2)-(219+219)=-435,
$$

$$
66-501=(33+33)-(125+376)=-435.
$$

These expressions involve different block pairs and are allowed by B3 because equating them is a four-term versus four-term relation, not forbidden by three-term uniqueness.

Across an arbitrary finite partition of A, every pair of disjoint blocks yields this forbidden-difference family. **The individual forbidden sets for different block pairs need not be disjoint.** Claiming that their sizes can all be added would be false: an explicit B3 fixture with overlapping different-block-pair spectra appears in the executable regression tests.

## A complete finite-dimensional Gram spectrum

Let the finite set A have m elements and let X be a subset of size n≥1. Define the m by m matrix

$$
M_{a,b}=r_X(a-b)\quad(a,b\in A).
$$

It is automatically positive semidefinite, being a Gram matrix of translates of the indicator of P_X. Theorem A gives its **exact structure** without knowing the positions of the points:

$$
\boxed{M=(q-n)I_X+nJ_X\;\oplus\;qI_{A\setminus X},}\tag{GRAM}
$$

where J_X is the all-ones matrix on the X coordinates and q=n(n+1)/2.

Its eigenvalues, with multiplicities, are

$$
\boxed{
\frac{n(3n-1)}2\quad(1),\qquad
\frac{n(n-1)}2\quad(n-1),\qquad
\frac{n(n+1)}2\quad(m-n).
}\tag{EIG}
$$

For n=1 the middle eigenspace is absent. All eigenvalues are nonnegative for all n≥1. Thus merely imposing **positive semidefiniteness of this A-indexed pair-sum autocorrelation matrix adds no new condition beyond the selector identity**: its spectrum is fixed by m and n, independently of the locations or scales of the B3 points. This is a precise no-go for that particular second-order Fourier/Gram strategy, not for more sophisticated harmonic analysis.

The Gram quadratic form also has the explicit decomposition

$$
\sum_{a,b\in A}M_{a,b}z_a z_b
=(q-n)\sum_{a\in X}z_a^2+
n\left(\sum_{a\in X}z_a\right)^2+
q\sum_{a\in A\setminus X}z_a^2.
$$

The decomposition exhibits why no scale-dependent contradiction follows from positivity alone.

## Arbitrarily many blocks: exact orthogonality of translated pair-sum families

Let $A$ have m elements, and let $X_1,\ldots,X_k$ be **pairwise disjoint nonempty** subsets of A; they need not cover A. Define a real-valued vector indexed by integers for each pair (i,a), where $a\in A$:

$$
\phi_{i,a}(t)=\boldsymbol{1}_{P_{X_i}}(t-a).
$$

The vector is supported on the translated pair-sum set $P_{X_i}+a$. From (CROSS0), for i distinct from j and any a,b in A,

$$
\boxed{\langle\phi_{i,a},\phi_{j,b}\rangle=0.}\tag{ORTH}
$$

Indeed, intersection of their supports would yield $p_i-p_j=b-a\in D(A)$, contradicting (CROSS0). Within a fixed block i the entire Gram submatrix is given by (GRAM) and has **strictly positive** eigenvalues: for $n_i=1$, only q=1 appears; for $n_i\ge2$, all of q, q−n_i and q+n_i(n_i−1) are positive. Thus the family of **km** vectors $\{\phi_{i,a}\}$ is linearly independent.

All these vectors are supported inside the finite union of intervals

$$
U=\bigcup_{i=1}^k
[\,2\min X_i+\min A,\ 2\max X_i+\max A\,]\cap\mathbb Z.
$$

Linear algebra gives the exact **multi-block rank-packing bound**

$$
\boxed{km\le |U|\le 3(\max A-\min A)+1.}\tag{RANK}
$$

This theorem holds for *arbitrarily many finite blocks*, uses exact orthogonality of actual translated pair-sum sets rather than enclosing intervals alone, and can be checked on genuine B3 data. However its rank bound is **not an improvement on ordinary B3 triple packing**: $k\le m$ makes it at most quadratic in m, whereas full triple-counting is cubic. The orthogonality proof does not extend automatically to independently recentered or higher-order signed sums. A logarithmic or other unbounded scale gain remains missing.

## Cross-scale consequence and limitations

For a sequence of disjoint finite B3 blocks, (AC) identifies *exactly which pair differences* have autocorrelation n and which are zero; (CROSS0) supplies further forbidden differences from different block-pair sumsets. These are true arithmetic-location restrictions and are stronger information than the enclosing shell intervals.

However, the global count of nonzero differences is only m(m-1), and each cross-pair forbidden spectrum can overlap others. At hypothetical critical cardinality m≈cN^(1/3), the number of specified differences is O(c²N^(2/3)), while the natural ambient difference interval has O(N) slots. Elementary capacity alone therefore has no growing contradiction. More importantly, the finite Gram matrix is automatically positive semidefinite with the above fixed spectrum. These facts do not prove consistency of a genuine infinite critical-density B3 set; they identify precisely why a naive second-order positivity/counting argument cannot resolve the problem.

A viable successor must couple *different pair-sum autocorrelation spectra beyond differences of A*, or exploit a genuinely nontrivial higher-order Fourier/cumulant inequality, with a quantitative scale gain that excludes every c>0. Before claiming a theorem, any proposed inequality must survive exact adversarial tests for finite B3 sequences and tests on fake critical-density occupancy profiles.

**Sources:** Martin Helm (1996), *On the Distribution of B3-Sequences*, DOI 10.1006/jnth.1996.0069; Christian Táfula (2026), *Infinite Sidon-type sets for zero-sum linear forms*, DOI 10.1007/s00605-026-02211-4. Táfula explicitly notes the odd-order B_h density problem is open and supplies conditional zero-sum form results. We do not infer an unconditional B3 bound from those theorems. GCL's previous [shadow moment note](CROSS_SCALE_SHADOW_MOMENTS.md) remains the reference for the cubic shadow moments and parity obstruction.
