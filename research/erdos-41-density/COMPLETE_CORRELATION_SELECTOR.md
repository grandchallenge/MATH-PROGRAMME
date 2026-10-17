# Erdős #41: exact complete-family selector and the remaining uncolored correlation gate

**Disposition (2026-10-15): PROVED** exact partition/refinement theorem and a sharp finite probabilistic selector, with computational regression. **OPEN** is the uncolored density-sensitive correlation lower bound. This note improves the operational target without claiming a solution of Erdős #41.

## 1. The correct uncolored target

Let A be a repetition-allowed B3 set, U and W disjoint subsets of A with every element of U below W, and H a set of **distinct positive actual differences** of W. Write

$$
P_U=\{a+b:a,b\in U,\ a\le b\},\quad
R_{UU}(t)=\#\{(p,p')\in P_U^2:p-p'=t\}.
$$


The single, coloring-invariant correlation is

$$
\boxed{\mathcal M(U,H)=\sum_{h\in H}R_{UU}(2h).}\tag{UNCOLORED}
$$


Every term is an actual integer relation involving four inner summands and two outer summands, with no artificial block labels. Since A is B3, its unordered pair sums and nonzero ordered differences are unique.

**Selector fact:** for every nonzero h in A-A, 2h is *not* in A-A: an equality a-b=2(z-z') with z!=z' would give a+z'+z'=b+z+z, contradicting B3. Consequently for every representation p-p'=2h with h in H, the two inner unordered pairs behind p and p' have **disjoint vertex supports**. Otherwise cancellation of a common vertex would express 2h as an element difference of A.

Moreover these two pairs cannot both be diagonals {a,a},{b,b}: then h=a-b would equal an actual ordered difference in the **disjoint** outer W, violating uniqueness of nonzero ordered B2 differences.

## 2. No-double-counting identity and monotone refinement

Partition U into arbitrary disjoint inner subblocks X_1,...,X_r (empty blocks omitted), optionally each lying in a chosen geometric inner shell. For every unordered block-type alpha={i,j}, use *all* positive pairs from X_i,X_j, including mixed pairs and diagonals. These type sets P_alpha **partition P_U**, because B3 implies B2.

For an oriented positive difference h, let

$$
S_{\mathcal P}(H)
=\sum_{\alpha\ne\beta}\sum_{h\in H}
R_{\alpha\beta}(2h).
$$


Types are ordered in the R correlation. No event at h>0 is duplicated with its opposite sign, and the outer set H consists of distinct actual positive differences. The exact identity is

$$
\boxed{
\mathcal M(U,H)=S_{\mathcal P}(H)
+\sum_\alpha\sum_{h\in H}R_{\alpha\alpha}(2h).
}\tag{PARTITION}
$$


**Refinement theorem.** If P' refines P by subdividing some inner blocks, then S_(P')(H)>=S_P(H). Every old cross-type representation stays cross-type, and some formerly within-type representations become cross-type. Since each positive inner pair retains a unique new type, the counting remains exact.

For the partition of U into **singleton blocks**, every P_alpha has exactly one member. Since h>0, R_alpha,alpha(2h)=0, and therefore

$$
\boxed{\max_{\mathcal P}S_{\mathcal P}(H)
=\mathcal M(U,H),}
\tag{SINGLETON}
$$


where the maximum ranges over all partitions of U. **Thus the block-selection/nonredundancy question is solved exactly:** a complete selection always captures the uncolored correlation with no loss. What remains unproved is a *positive density-sensitive lower bound on* M(U,H).

This does **not** make a positive M inevitable: genuine finite B3 examples, including the complete Sidon-digit lift in COMPLETE_PAIRTYPE_RESIDUE_BARRIER.md, can have M=0 for a natural choice of U,W.

## 3. Capture almost all correlation with only a bounded refinement

The singleton partition has O(|U|^2) pair types and is operationally expensive. We can preserve geometric shell provenance and capture most of M with only a small multiple of the original blocks.

For an integer K>=2, assign each element of U an independent uniform color in {1,...,K}. Refine every original geometric subblock X_i into its K color classes. Define the resulting complete pair-type correlation S_K(H) as above.

**Theorem (random K-way selector).** Some coloring satisfies

$$
\boxed{
S_K(H)\ge
\left(1-\frac{2K-1}{K^3}\right)\mathcal M(U,H).
}\tag{SELECT}
$$


In particular, a two-way refinement within each original geometric block captures **at least 5/8** of the entire genuine uncolored correlation:

$$
\boxed{S_2(H)\ge\frac58\,\mathcal M(U,H).}\tag{BINARY}
$$


**Proof.** Consider one event p-p'=2h counted by M, with two disjoint vertex supports. If the original block types of the pairs differ, every refinement retains the event as a cross-type event. Otherwise color the vertices independently.

The original pairs cannot both be diagonal, as proved in section 1. If exactly one pair is diagonal, their *refined types* coincide with probability at most 1/K^2. If both are off-diagonal and their original two block-type components lie in different geometric blocks, equality of their refined types has probability 1/K^2. In the remaining (worst) case both off-diagonal pairs belong to the same geometric block. The unordered color-pair distribution has K diagonal types of probability 1/K^2 and K(K-1)/2 off-diagonal types of probability 2/K^2. Hence the collision probability between two independent color-pair types is

$$
K(1/K^2)^2+\binom K2(2/K^2)^2
=\frac{2K-1}{K^3}.
$$


For K>=2 this is at least 1/K^2. Every event therefore survives as cross-type with probability at least 1-(2K-1)/K^3. Sum the indicators and use linearity of expectation to obtain a coloring achieving the bound. No independence between different events is needed. QED.

A deterministic coloring exists by the **method of conditional expectations**: reveal vertex colors one at a time and retain an option whose conditional expected S does not fall. Every event involves at most four inner vertices, so the relevant expectations are exactly enumerable using finite integer/rational arithmetic. The statement requires no randomized proof certificate, and the number of refined blocks is at most K times the number of geometric blocks.

## 4. What has actually been eliminated, and what has not

**Closed:** (a) complete positive-pair coverage, (b) orientation, (c) repeated-center difference multiplicities (B2 uniqueness), (d) duplicate representations across arbitrary shell cuts, and (e) choice of inner-block partition. The last reduces exactly to the single arithmetic number M(U,H), with a practical constant-fraction selector.

**Open:** show that hypothetical persistence A(t)>=c t^(1/3) for every sufficiently large t forces M(U_N,H_N) to be large for a **selection-invariant** inner union U_N and an actual localized outer difference set H_N. A mere count |H_N|=Omega_c(N^(2/3)) is not a spectral intersection theorem. The precise gate is

$$
\boxed{\mathcal M(U_N,H_N)
=\sum_{h\in H_N}R_{U_NU_N}(2h)\quad
\text{versus the universal cap }
\mathcal M(U_N,H_N)\le |U_N||H_N|.}
\tag{GATE}
$$


The upper cap follows from the positive-pair off-spectrum matching theorem. At critical density, both a prospective positive lower bound of order N and the cap are O(N). Therefore even *proving* M>=epsilon_c N would not alone prove Erdős #41. A successful successor must additionally show how its real arithmetic overlap consumes an **independent** multiscale matching budget or else forces a quantified inverse-structure/density decrement. Repeatedly charging the same event at multiple cuts is forbidden.

The Fourier identity and residue barrier in COMPLETE_PAIRTYPE_RESIDUE_BARRIER.md supply a falsifiable mixing-versus-resonance research avenue. The exact base-8 finite-window valley criterion (V) in SHELL_HARDY_AUDIT.md is the intended closure condition.

## 5. Finite hostile controls

For genuine finite B3 fixtures, compute M by enumerating unordered pair sums of U, unique positive actual differences of W, and all identities p-p'=2h. Verify the partition equality for a random partition, monotonicity under refinements, the singleton equality, and the K=2 expected capture using exact rational probabilities. Test the Sidon-digit lift on which M=0, rather than treating the positive finite examples as universal evidence.

**Research status:** theorem on selection, not a proof of the density-sensitive arithmetic gate or of Erdős #41. No independent referee or publication claim.
