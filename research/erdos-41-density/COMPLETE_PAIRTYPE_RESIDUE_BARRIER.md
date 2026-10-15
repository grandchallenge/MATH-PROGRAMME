# Erdős #41: complete pair-type residue barrier and the growing-complexity gate

**2026-10-15 status:** exact finite combinatorial theorem, sharp-order modulus construction, and a conditional infinite transfer theorem. The open Erdős #41 density-dip conjecture is **not solved**. This follows and strengthens MODULAR_CORRELATION_OBSTRUCTION.md, which handled only preassigned graphs of monochromatic inner-block pairs.

## 1. Complete, nonredundant positive-pair family

Let A be a repetition-allowed B3 set. Let X_0,...,X_(k-1) be pairwise disjoint inner subsets of A and let W be a disjoint outer subset. Set U=union_i X_i. Index **all** unordered inner positive pairs by their block **type** alpha={i,j}, 0<=i<=j<k:

$$
P_{ii}=\{a+b:a,b\in X_i,\ a\le b\},\qquad
P_{ij}=X_i+X_j\quad(i<j).
$$


The B2 property implies these pair-sum sets are disjoint and partition P_U, hence

$$
|P_U|=\sum_i\binom{|X_i|+1}{2}+\sum_{i<j}|X_i||X_j|
      =\binom{|U|+1}{2}.
$$


For each type alpha, define

$$
f_\alpha(d)=\#\{(p,z)\in P_\alpha\times W:p-2z=d\}.
$$


For two distinct types alpha!=beta, define

$$
O_{\alpha\beta}=\sum_d f_\alpha(d)f_\beta(d)
=\sum_{h\in W-W}R_{\alpha\beta}(2h)r_W(h).
$$


No positive inner pair appears twice in the partition. The zero-difference term vanishes for distinct types by B2.

## 2. Polynomial-size Sidon labels

**Lemma (explicit Sidon code).** For every k>=2 let p be an odd prime with p>=k. For i=0,...,k-1, write r_i for the representative of i^2 modulo p in {0,...,p-1}, and define

$$
e_i=i+2p\,r_i,\qquad q=6p^2+1.
$$


Then 0<=e_i<2p^2, q>3 max_i e_i, and the k(k+1)/2 unordered sums e_i+e_j (0<=i<=j<k) are pairwise different modulo q.

**Proof.** Each pair sum lies in [0,4p^2), strictly smaller than q, so congruence modulo q implies integer equality. Reducing that equality modulo 2p identifies the exact low-order sum i+j in [0,2p-2]. Subtracting low parts gives r_i+r_j=r_s+r_t, hence i^2+j^2=s^2+t^2 (mod p). From equal sums and equal sums of squares, and invertibility of 2 modulo p, get ij=st (mod p). The two unordered pairs are roots of the same monic quadratic over F_p, and therefore coincide modulo p; their members are 0,...,p-1, so coincide as integers. QED.

By Bertrand's postulate one can choose p<2k for k>=2 (taking an odd prime), hence q<24k^2+1 for k>=3. Any modulus with distinct unordered pair-type residues must have q>=k(k+1)/2. Therefore **the quadratic order q=Theta(k^2) is optimal for this type-separating modular mechanism**, although the constants are not claimed optimal.

## 3. Theorem: all distinct pair-type lag families can be disjoint

Let A be **any finite B3 set** with disjoint inner blocks X_0,...,X_(k-1) and outer W. Use the Sidon code above and define digit e(a)=e_i if a in X_i and 0 elsewhere (including every element of W). Set

$$
A'=\{qa+e(a):a\in A\},\quad X_i'=\{qa+e_i:a\in X_i\},\quad W'=qW.
$$


Then:
1. A' is B3, including repeated summands. Indeed, equality of lifted three-term sums implies q times the difference of the original three-term sums lies in [-3E,3E], E=max_i e_i, and q>3E. Thus the original sums agree, and B3 forces identical triple multisets.
2. All inner positive pairs are still accounted for exactly once by the k(k+1)/2 pair-type sets P'_{ij}.
3. For **every two distinct pair types** alpha={i,j}, beta={s,t} and **every** h in W'-W',

$$
\boxed{R'_{\alpha\beta}(2h)=0.}\tag{ZERO-COMPLETE}
$$


Indeed p'_alpha-p'_beta is congruent to (e_i+e_j)-(e_s+e_t), nonzero modulo q, whereas 2h is 0 modulo q.

4. Consequently the actual lag supports of all distinct inner pair-type families f'_alpha are **pairwise disjoint** for the same complete outer W' (not merely for a selected narrow bin):

$$
\boxed{O'_{\alpha\beta}(W')=0\quad (\alpha\ne\beta).}\tag{LAG-DISJOINT}
$$


This is an exact equality derived from the overlap identity, not an approximate capacity argument. Within-type self overlaps are not claimed to vanish.

## 4. Conditional infinite transfer with a localized macroscopic difference reservoir

Assume **hypothetically** there exists an infinite B3 A with A(t)>=c t^(1/3) for all t>=t0. Fix any integer k>=2, and let R=(6/c)^3. Prior proved persistent-density extraction gives at every sufficiently large N:
- k populated pairwise disjoint geometric inner shells X_j(N) within [1,N/R^2];
- an outer block W_N=A intersect (N/R,N] with |W_N|>= (c/2)N^(1/3);
- a localized subset of actual positive outer differences H_N satisfying
  |H_N|>=c^2/(16J^2) N^(2/3), h<=N/R^2, J=ceil(R^2).
  (See CROSS_BIN_LOCAL_DIFFERENCE_SUPPLY.md.)

Select an increasing sequence N_m whose active intervals (N_m/R^(2k+1),N_m] are pairwise disjoint, e.g. N_(m+1)>R^(2k+1)N_m. Assign the **same fixed k Sidon digits** e_j to shell X_j(N_m), and digit zero to W_(N_m) and all other points. Each element of A receives at most one label. The global lifted infinite set A'={qa+e(a):a in A} is B3. For all large t,

$$
A'(t)\ge A((t-E)/q)\ge c((t-E)/q)^{1/3},
$$


so its positive critical lower density survives with a changed constant approximately c/q^(1/3). All lifted local difference sets H'_m=qH_(N_m) retain cardinality at least kappa_c N_m^(2/3), with sizes <=qN_m/R^2. For **every** m and **every pair of distinct types** in the complete unordered inner-pair partition at scale m, the sampled correlation sum is zero.

**Interpretation:** even a truly complete, nonduplicated family of all inner pair types with a macroscopic, localized outer-difference reservoir can have **zero inter-type lag overlap at arbitrarily many scales**, conditionally on the hypothetical dense infinite B3 premise. The theorem does not construct such an infinite B3 carrier, and therefore does not refute Erdős #41. It forbids claiming that *fixed-k* completeness, by itself, guarantees positive inter-type overlap in a way insensitive to arithmetic residue coding.

## 5. Quantitative novelty of this obstruction and the viable proof architecture

The number of pair types is k(k+1)/2, and explicit Sidon labels make their residues distinct with modulus q=Theta(k^2). Under a fixed base carrier with hypothetical density coefficient c, the transformed coefficient is asymptotically c/q^(1/3)=Theta(c k^(-2/3)). This exact **density-versus-residue-complexity tradeoff** is the useful invariant. The transfer theorem is a conditional obstruction to proposed correlation lemmas, not a lower bound and not a density decrement for arbitrary B3 sets.

Consequently **k must not remain fixed** in any argument seeking an inevitable inter-type overlap solely from persistence of positive density and the complete pair-type partition. A possible research avenue is to prove an *inverse arithmetic theorem*: if all complete inter-type overlaps stay below a prescribed fraction of the exact matching budget over sufficiently many nested scales, then A develops a growing residue/spacing complexity whose density cost can be rigorously bounded. This inverse theorem is OPEN. Simple pigeonhole counting, an unproven analogy to pseudorandom mixing, or summation of the same inner pairs at several cuts is insufficient.

A defensible nonredundant attempt partitions positive inner pairs by **their unique block types** and outer differences by **their unique ordered element pairs** (B3 implies B2, hence nonzero differences are unique). It measures

$$
S_k(H)=\sum_{\alpha\ne\beta}\sum_{h\in H}R_{\alpha\beta}(2h)
$$


and separately the within-type terms. There is an exact, tautological decomposition

$$
S_k(H)=\sum_{h\in H}R_{UU}(2h)-
\sum_\alpha\sum_{h\in H}R_{\alpha\alpha}(2h).
$$


Do not infer a positive bound from this identity: the Sidon lift makes its right-hand side exactly zero.

**Multiscale closure criterion.** A claimed density-dip proof must convert a proven arithmetic mixing or inverse-structure lemma into the already established base-8 finite-window valley criterion in SHELL_HARDY_AUDIT.md. A mere S_k(H)>=delta_c N at isolated N does not suffice: the general matching upper budget has the same order O(N), and the geometric sum over scales is dominated by the largest scale. An actual proof requires an explicit bounded potential with a strict decrement at every sufficiently long block of scales, or another quantified contradiction for each fixed c>0. This is a proof obligation, not an established result.

## 5A. Exact Fourier diagnostic for the next arithmetic-mixing attempt

The residue barrier points to a concrete **mixing-versus-resonance** approach, not a claim of mixing. Let all elements of U union W lie in [1,H] and choose any integer modulus M>4H. There is no wrap-around ambiguity among centered lags p-2z, which lie in an interval of length at most 4H. For a function on Z/MZ define

$$
\widehat F(\xi)=\sum_{x\bmod M}F(x)\exp(-2\pi i\xi x/M).
$$


Using the entire pair-type partition, direct Fourier expansion and Parseval give for every two types alpha,beta

$$
\boxed{
O_{\alpha\beta}(W)=
\frac{1}{M}\sum_{\xi\bmod M}
\widehat{\mathbf 1_{P_\alpha}}(\xi)\,
\overline{\widehat{\mathbf 1_{P_\beta}}(\xi)}
\,|\widehat{\mathbf 1_W}(2\xi)|^2 .
}\tag{FOURIER}
$$


This holds for actual integer overlap, not a periodic surrogate, because of M>4H. The zero-frequency term is strictly positive for nonempty types and W:

$$
\frac{|P_\alpha||P_\beta||W|^2}{M}.
$$


If O_alpha,beta=0, the nonzero Fourier frequencies must cancel this term **exactly**:

$$
\boxed{
\sum_{\xi\ne0}
\widehat{\mathbf 1_{P_\alpha}}(\xi)
\overline{\widehat{\mathbf 1_{P_\beta}}(\xi)}
|\widehat{\mathbf 1_W}(2\xi)|^2
=-|P_\alpha||P_\beta||W|^2 .
}\tag{RESONANCE}
$$


The finite modular lift supplies explicit examples where this cancellation occurs for **all** distinct pair types simultaneously. Therefore one cannot assume pseudorandom Fourier cancellation bounds merely from B3 and positive lower density.

**Precise next proof attempt:** obtain a quantitative *inverse* for near equality in (RESONANCE) across a growing set of pair types and many nested scales. It should show either (a) an arithmetic cross-correlation lower bound together with a rigorously identified **independent** matching deficit, or (b) a structural progression/residue concentration whose **quantified** cost forces a drop in the normalized counting function. Neither (a) nor (b) is currently proved. Even the bound O_alpha,beta>=epsilon N at one scale is not sufficient by itself: the global B3 matching budget is O(N).

Test the inverse theorem first against (i) the complete Sidon digit lifts, (ii) the sparse infinite B3 base-16 example, (iii) the genuine greedy finite B3 prefix, and (iv) all remaining terms in the full pair-type partition. An inverse claim failing any of these is not admissible.

## 6. Finite replay fixture

The genuine 29-point B3 set in CROSS_SCALE_OVERLAP_ENERGY.md has four consecutive 3-point inner blocks and a 17-point outer block. Take k=4, p=5, q=151, e=(0,11,42,43). The unordered pair-type residue labels are

$$
0,11,42,43,22,53,54,84,85,86
$$


(all distinct). Direct exact enumeration gives: 4495 distinct three-summand sums from 29 elements before and after the lift; 78 distinct inner unordered pair sums partitioned into all ten types (four diagonal types of size 6, six mixed types of size 9); 136 distinct positive differences from the 17-point outer block; and **zero** distinct-type correlations at twice those outer differences. All checks use integers and are implemented in tests/test_erdos41_modular_overlap_gate.py.

**Disposition:** PROVED finite and conditional transfer lemmas; OPEN density-sensitive growing-complexity inverse theorem and multiscale decrement; Erdős #41 OPEN. No novelty-priority or mathematical certification claim.

Sources: [CROSS_BIN_LOCAL_DIFFERENCE_SUPPLY.md](CROSS_BIN_LOCAL_DIFFERENCE_SUPPLY.md), [CROSS_SCALE_OVERLAP_ENERGY.md](CROSS_SCALE_OVERLAP_ENERGY.md), [SHELL_HARDY_AUDIT.md](SHELL_HARDY_AUDIT.md), [MODULAR_CORRELATION_OBSTRUCTION.md](MODULAR_CORRELATION_OBSTRUCTION.md).
