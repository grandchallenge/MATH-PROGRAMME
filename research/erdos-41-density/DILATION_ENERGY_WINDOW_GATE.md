# Erdős #41 — Dilation-energy window certificate and cross-bin inverse gate

**Status (2026-10-15):** PROVED finite identities and bin-local inverse-packing inequalities; OPEN density-sensitive interaction and multiscale decrement. This note is the prioritized Stage B successor to COMPLETE_CORRELATION_SELECTOR.md. No Erdős #41 solution, mathematical certification, or external novelty claim.

## 1. Complete positive-pair family and dilation identity

Let A be a repetition-permitted B3 set and let U,W be finite, disjoint subsets of A with U<W. Let P=P_U be the set of sums of unordered pairs from U (repetitions allowed). B3 implies B2, so |P|=binom(|U|+1,2). For an integer lambda, set

$$
C_\lambda(s)=\#\{(p,z)\in P\times W:p+\lambda z=s\},
\quad T=|P||W|,\quad E(\lambda)=\sum_s C_\lambda(s)^2.
$$

Uniqueness of B3 sums of type UUW gives E(1)=T. The ordered positive differences of W are all distinct by B2. Let H(W)={z'-z:z,z' in W and z'>z}, and define

$$
\mathcal M(U,H)=\sum_{h\in H}R_{UU}(2h),\qquad
R_{UU}(t)=\#\{(p,p')\in P^2:p-p'=t\}.
$$

**Theorem 1 (exact doubled-energy identity):**

$$
\boxed{E(2)-E(1)=2\mathcal M(U,H(W)),\qquad
\mathcal M(U,H(W))=\sum_s\binom{C_2(s)}2.}\tag{DIL}
$$

Proof: expand each squared representation function. E(1)=T because the map (p,z) to p+z is injective under B3. The non-diagonal pairs of representations in E(2) are exactly the equalities p+2z=p'+2z', with z!=z'. For each such unordered collision the positive outer difference belongs to H(W) uniquely, and p-p'=twice that difference after orienting the representations. Thus off-diagonal ordered collisions equal twice M. Four-versus-four collisions remain allowed by B3.

The unordered pair Fourier identity Q_U(theta)=(F_U(theta)^2+F_U(2theta))/2 also gives the exact formula

$$
2\mathcal M(U,H(W))=
\frac14\int_0^1|F_U(\theta)^2+F_U(2\theta)|^2
\bigl(|F_W(2\theta)|^2-|F_W(\theta)|^2\bigr)\,d\theta .
\tag{F-DIL}
$$

Neither the zero mode nor positive lower density independently forces this difference to be positive. In particular, E(1) already saturates the diagonal minimum E(1)=T.

## 2. Sharp integer interval-pressure certificate

Partition a finite interval covering the support of C_2 into disjoint integer intervals I. Define L_I=|I|, T_I=sum_{s in I} C_2(s), and write T_I=L_I a_I+r_I, with 0<=r_I<L_I.

**Theorem 2 (integer congestion):**

$$
\boxed{
\mathcal M(U,H(W))
\ge\sum_I\left[L_I\binom{a_I}{2}+r_Ia_I\right].
}\tag{INT}
$$

Proof: at a fixed total T_I, the number of unordered colliding representation pairs, sum_{s in I} binom(C_2(s),2), is minimized when the nonnegative integer loads are as equal as possible. Exactly r_I cells have load a_I+1 and the rest load a_I. This yields the claimed lower bound. Singleton intervals recover equality. In particular, M=0 implies T_I<=L_I for every interval. This is a sharp finite packing test, not yet a density-escape theorem.

## 3. Localized, genuinely nonredundant *outer-bin* identity

Let Z be a set of actual outer centers in a short coarse interval, partitioned into ordered disjoint fine bins Y_1<...<Y_B. Empty bins are harmless. Let

$$
H_{\rm inter}=\bigcup_{b<b'}(Y_{b'}-Y_b),
\qquad C_b(s)=\#\{(p,z)\in P\times Y_b:p+2z=s\}.
$$

B2 uniqueness ensures distinct positive differences from different ordered outer pairs never coincide. Consequently every h in H_inter belongs to exactly one outer-bin pair. We have the exact **nonduplicating** identity

$$
\boxed{
\mathcal M(U,H_{\rm inter})
=\sum_{b<b'}\sum_s C_b(s)C_{b'}(s).
}\tag{BIN}
$$

Indeed p+2z=p'+2z' with z in Y_b, z' in Y_b' is equivalent to p-p'=2(z'-z). The bin-pair decomposition counts each actual difference exactly once. It includes **all** unordered inner positive pairs, so no inner color selection enters.

## 4. A proved, localized inverse-packing dichotomy

Fix an integer interval I. For each fine bin define

$$
T_{b,I}=\sum_{s\in I}C_b(s),\qquad
V_{b,I}=\sum_{s\in I}\binom{C_b(s)}2.
$$

Let S_{b,I} count occupied positions in I. Since binom(v,2)>=v-1 for every integer v>=1, S_{b,I}>=T_{b,I}-V_{b,I}. Two occupied supports in I intersect at least S_{b,I}+S_{b',I}-|I| times, and each common position contributes at least one cross representation.

**Theorem 3 (cross-bin support with self-collision defects):**

$$
\boxed{
\sum_{s\in I}C_b(s)C_{b'}(s)\ge
\bigl[T_{b,I}+T_{b',I}
-V_{b,I}-V_{b',I}-|I|\bigr]_+ .
}\tag{PACK}
$$

Summing over any disjoint integer interval partition of the common support gives a valid lower bound on each term of (BIN). A second valid local bound follows from Cauchy:

$$
\boxed{
\sum_{s\in I}C_b(s)C_{b'}(s)\ge
\frac12\left[
\frac{(T_{b,I}+T_{b',I})^2}{|I|}
-T_{b,I}-T_{b',I}-2(V_{b,I}+V_{b',I})
\right].
}\tag{CROSS-CS}
$$

**Exact avoidance consequence:** if the cross-bin correlation vanishes, then for every integer interval I,

$$
\boxed{T_{b,I}+T_{b',I}\le |I|+V_{b,I}+V_{b',I}.}\tag{AVOID}
$$

This provides a *falsifiable finite-window dichotomy*: either local representation congestion forces positive cross-bin correlation, or the actual supports and within-bin collisions accommodate avoidance at every tested interval. It is not yet an arithmetic inverse classification; (AVOID) is a necessary consequence, not a structural description.

## 5. Persistent-density input and unproved gate

Under the **hypothetical** persistent B3 lower bound A(t)>=c t^(1/3) for all sufficiently large t, previous GCL work chooses R=(6/c)^3, J=ceil(R^2), a coarse outer set Z with diameter <=N/R^2, and fine bins for which

$$
\boxed{
|H_{\rm inter}|\ge\frac{c^2}{16J^2}N^{2/3},
\quad H_{\rm inter}\subseteq[1,N/R^2].
}\tag{DENS-H}
$$

Take the complete inner union U=A intersect [1,N/R^2]. Both |P_U| and |Z| have lower bounds of critical order, making |P_U||Z| at least a positive c-dependent multiple of N. But their sums occupy O_c(N) positions with constants that can leave substantial unused capacity. None of (DENS-H), (INT), (PACK) or (CROSS-CS) proves that any local interval congests. **The desired positive density-sensitive bound remains OPEN.**

Do not mistake a lower bound of order N for a contradiction: the off-spectrum pointwise matching upper budget for this same aggregate is O(N). Stage C requires an additional genuinely independent multiscale deficit.

## 6. Focused Stage B research obligation

**Candidate dilation-escape/inverse-avoidance theorem (UNPROVED).** For each fixed c>0, and long base-eight windows on which the hypothetical persistent density holds, prove that the exact outer-bin profiles either (i) have quantitatively unavoidable positive cross-bin correlation, or (ii) satisfy a nontrivial arithmetic classification of the all-interval avoidance constraints (AVOID) with a *proved density cost across nested scales*. A classification merely restating (AVOID) does not count. Any claimed density cost must survive Sidon-digit lifts, the sparse infinite base-16 B3 example, and finite B3 prefixes.

A successful result must assign each counted outer pair and inner pair to a unique owner at the relevant scale. Recharging the same additive representation on many overlapping cuts is forbidden. The ultimate closure target is the base-eight finite-window valley criterion proved in SHELL_HARDY_AUDIT.md.

**Admissibility checks:** verify (DIL), (INT), (BIN), (PACK), (CROSS-CS) on genuine B3 data; include M=0 and positive M examples, multiple interval widths, and a non-B3 hostile control. If these pass, use an explicitly bounded finite-window search to falsify candidate quantitative inverse statements before attempting general proof.

## 7. Exact finite calibration

The genuine 29-point B3 fixture in CROSS_SCALE_OVERLAP_ENERGY.md gives:
- First 8 inner elements, other 21 outer: T=756, E(1)=E(2)=756, M=0.
- First 14 inner elements, other 15 outer: T=1575, E(1)=1575, E(2)=1581, M=3.
- Split the latter W after its first 3 elements: the localized outer-bin cross-correlation equals 1, detected by (PACK) using intervals of width 2. Whole-W width-2 integer congestion certifies at least 2 of the 3 collisions, but coarser widths may give zero pressure.

Primary source: https://www.erdosproblems.com/41 (repetition-permitted B3). Relevant external comparison: Christian Táfula, *Infinite Sidon-type sets for zero-sum linear forms*, 2026, DOI 10.1007/s00605-026-02211-4. That paper's pairwise-distinct tuple convention and additional gap hypotheses are not sufficient to complete this argument.

**Priority instruction:** focus exclusively on arithmetic control of localized cross-bin representation placement and self-collision defects across nested density windows. Do not return to unconditional selected inner-block overlap estimates without evidence of a new mechanism.


## 8. Thresholded forbidden-distance graphs: a rigorous inverse alternative

The all-interval packing inequalities are useful finite diagnostics, but controlling their actual bin defects may be just as hard as the desired cross-correlation. A second rigorous reduction recasts the remaining arithmetic issue as an **extremal graph problem independent of the chosen outer set**.

Let I be a finite interval of D integer positions where outer centers may lie. For fixed inner U and positive integer threshold t, define an undirected graph G_t(U,I): its vertex set is I, and distinct vertices x,y are adjacent exactly when

$$
R_{UU}(2|x-y|)\ge t.
$$

Let alpha_t(U,I) be the independence number of this actual, integer-computable graph (not an assumed random-graph model). Any actual outer set W subset of A intersect I has m=|W|, and its full positive-difference correlation satisfies

$$
\mathcal M(U,H(W))
=\sum_{\{x,y\}\subseteq W}R_{UU}(2|x-y|)
\ge t\,e(G_t[W]).
$$

**Theorem C (thresholded Turán gate, unconditional finite).** For every t>=1 and every m>=1,

$$
\boxed{
\mathcal M(U,H(W))
\ge \frac t2\left(\frac{m^2}{\alpha_t(U,I)}-m\right)_+.
}\tag{GRAPH}
$$

**Proof.** Every induced graph G_t[W] has independence number at most alpha_t. Its complement has clique number at most alpha_t. The classical Turán upper bound on the complement's number of edges gives
the number of induced graph edges is at least one half of the quantity m squared divided by alpha_t minus m. Every G_t-edge has weight at least t, and the exact outer-difference identity weights each actual unordered W-pair once. QED.

The quantitative inverse consequence, obtained by rearranging (GRAPH), is

$$
\boxed{
\alpha_t(U,I)\ge \frac{m^2}{m+2\mathcal M(U,H(W))/t}.
}\tag{INV-GRAPH}
$$

In particular, if M=0 then W itself is an independent set in G_1, and alpha_1>=m. This is an **exact structured-avoidance certificate**, but the existence of a large independent set is not yet an additive-combinatorial classification or a density-decrement proof.

**Research target with explicit density input.** Persistent density gives an outer coarse bin Z of size m>=c N^(1/3)/(2J) inside I with |I|<=N/R^2+1. Prove a nontrivial upper bound on alpha_t(U,I) from the actual B3 pair-sum spectrum of U. If alpha_1<m, Stage B positivity follows. If t is itself on the inner critical scale, the quantitative formula can amplify the bound. Conversely, a large alpha_t across every nested density window must be converted into an arithmetic or gap-structure classification with a *proved* cost for the normalized counting density. Neither step is currently established.

**Scaling caution.** An independence upper bound alpha_t=O(log N) with t=Omega(N^(1/3)) and m=Omega(N^(1/3)) yields only a lower bound of order N/log N from (GRAPH), not an Omega(N) matching-budget contradiction. The graph method is a research instrument, not an automatic way around Stage C.

**Finite computational gate.** On a short candidate outer interval, compute G_t by exact differences of the actual pair-sum set, certify alpha_t using an exact bitset maximum-independent-set solver, and compare the lower bound with the observed weighted correlation of actual B3 outer points. Include a threshold-free zero-overlap example and the previous Sidon lift; both are essential hostile cases. Full-scale independence or Fourier inverse claims require separate mathematical proofs.
