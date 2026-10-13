# Erdős #41: multiscale cubic-shadow moment identities

**Disposition:** proved finite-partition mathematical results; no proof of the original infinite density conjecture.

## Exact moments of an additive shadow

Let X be a nonempty finite repetition-allowed B3 set of integers, with n elements, first moment S1 (sum of its elements) and second moment S2 (sum of their squares). Write

$$
T(X)=\{a+b-c:a,b,c\in X\},\qquad
f(n)=|T(X)|=\frac{n(n^2-n+2)}2.
$$

The first and second moments over the **distinct** shadow values satisfy

$$
\boxed{\sum_{t\in T(X)}t=\frac{n^2-n+2}{2}S_1.}\tag{M1}
$$

$$
\boxed{\sum_{t\in T(X)}t^2=\frac{3n^2+3n+2}{2}S_2-(n+2)S_1^2.}\tag{M2}
$$

**Proof.** Enumerate all n binom(n+1,2) representations (unordered pair {a,b}, distinguished subtraction term c). Every nontrivial representation with c not among {a,b} has a unique output outside X, by B3. Every x in X has exactly n trivial representations ({x,c},c). Therefore the moment over distinct shadow values is the moment over all representations minus (n-1) times the corresponding moment over X. The unordered-pair-sum list has first moment (n+1)S1 and second moment (n+2)S2+S1². Expanding a+b-c and (a+b-c)², summing over all pairs and c, and subtracting the trivial overcount proves (M1,M2).

With block mean $\mu=S_1/n$ and population variance $v=S_2/n-\mu^2$, the exact consequences are

$$
\boxed{\mathrm{mean}(T(X))=\mu,\quad
\mathrm{Var}(T(X))=\lambda_n v,\quad
\lambda_n=\frac{3n^2+3n+2}{n^2-n+2}.}\tag{M3}
$$

For n=1 both variances vanish. For n≥2 the multiplier exceeds three and tends to three as n tends to infinity. The identity is exact, not an independence approximation.

## An exact variance-sensitive spacing lower bound

Every set of f distinct integers has population variance at least $(f^2-1)/12$, with equality only for f consecutive integers. Since $T(X)$ has exactly $f(n)$ distinct integers, (M3) gives the **necessary B3 dispersion bound**

$$
\boxed{\sigma_X^2\ge\frac{f(n)^2-1}{12\lambda_n}.}\tag{VSH}
$$

This controls the *actual distribution* of elements within X, not merely its diameter. The right side is asymptotic to $n^6/144$, because $f(n)\sim n^3/2$ and $\lambda_n\to3$. As $\sigma_X^2\le D^2/4$ for a set of diameter D, it also implies a cubic lower bound on D. The strict finite geometry cannot be replaced by the size of a containing shell alone.

## Arbitrarily many disjoint blocks

Let $X_1,\ldots,X_r$ be any finite family of pairwise disjoint nonempty finite subsets of one B3 set, with r arbitrary. Put $n_i=|X_i|$, $f_i=f(n_i)$, $\mu_i=\mathrm{mean}(X_i)$, $v_i=\mathrm{Var}(X_i)$, $\lambda_i=\lambda_{n_i}$, and $F=\sum_i f_i$.

The previous cross-block cubic-shadow theorem proves the shadows $T(X_i)$ are pairwise disjoint. Thus their union has exactly F **distinct integer** elements. Apply the distinct-integer second-moment lower bound to that union. The within/between decomposition of its central second moment gives

$$
\boxed{12\left[
F\sum_i f_i\lambda_i v_i
+\sum_{i<j}f_if_j(\mu_i-\mu_j)^2
\right]\ge F^2(F^2-1).}\tag{CROSS}
$$

This theorem retains *actual block locations and variances* and is valid for any finite number of scales. It is stronger information than the individual sum-range capacities but is only a necessary condition.

Simultaneously, the already-proved disjoint-shadow support bound gives

$$
\sum_i f_i\le
\left|\bigcup_i[2\min X_i-\max X_i,\ 2\max X_i-\min X_i]\cap\mathbb Z\right|.\tag{RANGE}
$$

These two conditions are compatible, not substitutes for one another.

## Why translation does not produce a logarithmic gain

For every integer shift h, an exact identity holds:

$$
\boxed{T(X+h)=T(X)+h.}\tag{SHIFT}
$$

In contrast, $(X+h)-(X+h)=X-X$. Thus translating different geometric blocks so their centers coincide also **translates their shadows separately**. The original shadow-disjointness theorem cannot be applied to these recentered shadows. We cannot count the shadows of all blocks inside one common short interval by subtracting the block locations: this is the odd-order translation-covariance barrier behind the failure of the familiar even-order Sidon logarithmic-dip argument.

The superficially promising translation-invariant signed expression $a+b-2c$ is not B3-injective. The three-element B3 set $X=\{1,2,5\}$ gives distinct representations

$$
1+5-2\cdot2=2+2-2\cdot1=2.
$$

Hence replacing a+b-c by a+b-2c discards the precise cubic injection. The parity obstruction is a substantive algebraic defect, not just an inconvenient coordinate choice.

## Quantitative scaling test against persistent positive density

Suppose hypothetically that a B3 set has $A(N)\ge cN^{1/3}$ for every sufficiently large N, where c>0. Take successive geometric shells indexed by j≤K, with occupancies on the critical scale $n_j\asymp c 2^{j/3}$, centroids $\mu_j\asymp2^j$, and internal variance $v_j=O(2^{2j})$. These are a **model of a possible configuration**, not deductions about the occupancy of each shell from the lower-density assumption.

For sufficiently large j, $f_j\asymp n_j^3/2\asymp c^3 2^j$. Consequently, with $F=\sum_{j\le K}f_j$,

$$
F=O(c^3 2^K),
\qquad
F\sum_j f_j\lambda_jv_j
+\sum_{i<j}f_if_j(\mu_i-\mu_j)^2
=O(c^6 2^{4K}).
$$

The right-hand side of (CROSS) is $O(c^{12}2^{4K})$. The geometric factor $2^{4K}$ cancels: the moment inequality can at best impose a restriction on the **fixed** density coefficient c under such a regular shell model. It does not by itself provide a factor growing with K that would rule out every c>0.

This is a scaling diagnosis, not a proof that any positive-density infinite B3 sequence exists. In particular, the displayed big-O upper estimates cannot themselves establish the inequality. Direct exact finite-prefix tests of the genuine B3 fixtures and adversarial hypothetical critical profiles are included with the executable receipt.

More basically, disjoint cubic shadows in geometric shell ranges obey $\sum_{j\le K}f_j=O(2^K)$, and their enclosing union has $O(2^K)$ positions. Both sides grow in the same scale. A proof by **shadow counts alone** therefore still lacks a divergent logarithmic factor.

## A bounded conclusion rather than a claimed proof of Erdős #41

**Established:** exact cubic-shadow first and second moments, a closed-form shadow variance multiplier, and the inequality (CROSS) combining actual centroids and dispersions for arbitrary finite partitions of B3 sets. These supply algebraic obstructions beyond the earlier interval-only Hall inequalities.

**Not established:** a contradiction to persistent positive B3 density; a universal logarithmic shadow-overlap enhancement; the M3 shell-energy deficit; or Erdős #41. In particular, finding that the same geometric factors occur on both sides of (CROSS) rules out the naive scale-counting argument, but not a more subtle exploitation of the actual moment statistics of genuine B3 sets.

**Research boundary:** derive a quantitative **cross-scale deficit** beyond (CROSS) from arithmetic correlations among distinct shadows and their mixed-difference sets, or instead exploit known conditional gap results (including Táfula 2026) to control large irregular gaps. Any claim that the density conjecture follows must supply a missing factor diverging with the number of scales or another explicit contradiction for each fixed c>0, not simply reproduce the exact moment identity.
