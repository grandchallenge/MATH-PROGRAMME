# Erdős #561: independent-core obstruction and unit-star normalization

**2026-11-26. Status:** paper deductions UNDER_REVIEW. This reconstructs the 2026-11-25 working manuscript; the earlier local worktree was not found after CHAD recovery, and no protected admission of that draft had occurred. No claim of priority, mathematical certification, or unrestricted conjecture closure.

The external Ansatz manuscript, [Size Ramsey numbers of two stars versus a star forest](https://github.com/uclanlp/continual-graph-memory/blob/main/results/erdos_561.pdf), dated 25 September 2026, was acquired and inspected in the preceding research turn (Git blob f5ab3603b495348c100400fcf2d88d63d8320b4c; SHA-256 2e58628af4b519fc068d6256e56ea7681074d34e42945fa3f3a024cda65a4c86). It reports an even-diagonal theorem without expanding two structural lemmas, and does not contain the unrestricted proof reported in the later research overview. This does not rule out a different unpublished full candidate. The independent argument here uses the protected quantitative cap-defect theorem, not either unexpanded lemma.

## 1. Independent-set signed-area obstruction

Use the frontier notation from #3490 and CAP_DEFECT_AND_PLATEAU_THEOREM.md (protected blob 84f65a064d0de9bf34697da152b802f09dfdc4b9). Consider a counterexample of least frontier length $L=s+t-k+1$, either globally or in a class closed under successor frontiers. Then $e(H)=W_k-1$, $\Delta(H)=D=w_k-1$, and $D\ge2$. The latter follows because any maximizing pair with a leading arm one is defeated by the all-opposite-colour colouring under this degree cap. Let $P$ denote the initial plateau length. For a maximizing pair attaining $P$, both caps are positive and the earlier factor-defect bound gives $h\ge P$ and at least $P(D+1)$ saturated vertices.

For an independent set of $r\le L$ saturated vertices, deletion removes precisely $rD$ edges and advances the frontier by $r$. The least-length principle implies

$$
\sum_{j=0}^{r-1}(w_{k+j}-D)\ge1.
$$

Choose a factor cut attaining $h$. Let $B$ be its number of large counted components (at least $D+1$ vertices), and $C$ the number of these components which are complete. The weighted boundary argument gives $B\ge h\ge P$. A counted complete component must be an isolated clique on $D+1$ vertices, with odd order and odd caps: its saturation makes it isolated, and its counted parity is $\alpha(D+1)$ odd. Every noncomplete large counted component contains two nonadjacent saturated vertices. Distinct counted components have no intercomponent edges. Therefore there is an independent saturated set of size at least $2B-C$.

If a first prefix length $\rho\le L$ with signed area nonpositive exists, then necessarily $2B-C<\rho$. This applies to any profile.

## 2. Steep first descent and even weights

A completely flat frontier is impossible: the degree sum gives $PD<2L$ whereas $P=L$ and $D\ge2$. Suppose the first drop is $\delta=w_k-w_{k+P}\ge2$.

If $D\ge3$, the frontier must have $L>2P$: otherwise $W_k-1\le2PD-1$, since the weights following the plateau are at most $D-1$, whereas the saturated degree sum forces $e(H)\ge PD(D+1)/2\ge2PD$. Set

$$
\rho_0=P+\left\lceil P/(\delta-1)\right\rceil\le2P.
$$

Its signed area is at most $P-(\rho_0-P)(\delta-1)\le0$. Hence every witnessing cut satisfies

$$
C\ge2B-\rho_0+1\ge1,\qquad B\le\rho_0-1.
$$

In particular it contains an isolated saturated clique of odd order and both caps are odd. This excludes the steep descent when $D$ is odd or a plateau-maximizing pair has an even cap.

For $D=2$, a steep drop is from 3 to 1, so $W_k=L+2P$. Any triangle in $H$ is isolated, and the prior matching-budget component-removal lemma excludes such a triangle in a least-length failure: colour it entirely red or blue to absorb a single component, removing three edges and advancing one frontier. Paths and even cycles permit a degree-one split; each odd cycle requires and suffices with one exceptional vertex or edge. Therefore the cap-defect bound forces at least $P$ odd cycles of length at least five. Thus $L+2P-1=e(H)\ge5P$, so $L\ge3P+1$. Selecting two nonadjacent vertices in each of $P$ odd cycles gives the forbidden independent saturated set of size $2P$ with zero signed area. This excludes the remaining steep case at $D=2$.

Consequently a global least-length obstruction either has a first drop of exactly one, or has even $D\ge4$ and the isolated-clique constraint above.

**Even-antidiagonal theorem.** If all remaining antidiagonal weights are even, the frontier inequality holds for arbitrary hosts. Otherwise select a least-length failure within this successor-closed class. Its $D$ is odd, its plateau is not the entire frontier, and its first drop must be at least two. The preceding argument contradicts the existence of its required isolated clique. In particular the canonical star-forest upper construction gives the conjectured exact size Ramsey formula whenever all original antidiagonal weights are even. No assumption of general frontier sharpness is used.

## 3. Tutte–Berge matching-budget normalization

**Theorem.** If a finite graph $G$ arrows two forests of $s$ and $t$ vertex-disjoint stars and every target star has at least two edges, then $\nu(G)\ge s+t-1$.

Suppose not. By Tutte–Berge there is a set $S$ such that

$$
\nu(G)=|S|+\sum_C\lfloor |C|/2\rfloor\le s+t-2,
$$

where $C$ runs over components of $G-S$. Allocate these integer units between red and blue subject to total budgets $s-1,t-1$. This is possible by splitting each component's units arbitrarily and each vertex of $S$ individually. Let $S_R,S_B$ be the resulting partition of $S$. Colour all edges meeting $S_R$ red, all edges meeting $S_B$ blue, and choose either colour on edges between the two sets. Every red star that meets $S$ must meet $S_R$: an edge at a vertex of $S_B$ can be red only if its other endpoint is in $S_R$. The blue statement is symmetric. Thus disjoint stars touching $S$ consume at most the respective vertex budgets there.

For each component $C$ let its allocations be $x,y$ with $x+y=\lfloor |C|/2\rfloor$. If $x\le y$, choose $x$ vertices of $C$ and colour the edges incident to them red, all other component edges blue. Every red star meets that set, so at most $x$ disjoint red stars fit. Any blue star occupies at least three vertices outside the set, and

$$
|C|-x\le 2(x+y)+1-x=x+2y+1\le3y+1.
$$

Hence at most $y$ disjoint blue target stars fit. For $y<x$, interchange the colours. This includes the zero allocations and isolated vertices. Summing over components and $S$ shows that neither full target fits. Contradiction.

If both terminal arms of a frontier are at least two, apply this theorem to any of its pairs (the combined component count is $L+1$). A matching of $L$ edges can therefore be removed and assigned one colour in the extension argument. All arms of that colour decrease by one without disappearing, and each frontier weight decreases by exactly one. Hence a failure of least $L$ and then least $W_k$ must have at least one terminal arm equal to one. This normalization is unconditional; it does not assume an adequate matching in advance.

As a corollary, when both original lists consist of even positive arms, remove a matching of $s+t-1$ edges and decrement one colour. The new mixed-parity lists have all antidiagonal weights even. The even-antidiagonal theorem and the exact subtraction of $s+t-1$ from the canonical budget prove the original formula.

## 4. Remaining boundary

The normalized global problem retains unit-drop frontiers and the steep even-degree isolated-clique branch. LOCALIZED_FACTOR_DEFECT_THEOREM.md provides a new independent-support apportionment theorem and a two-layer saturation constraint for the first branch. Neither manuscript settles the unrestricted conjecture. Prior source inspection is distinguished from mathematical reconstruction; no external proof has been certified.
