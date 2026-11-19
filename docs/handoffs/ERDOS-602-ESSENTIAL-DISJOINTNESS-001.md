# Erdős #602 — essential disjointness and a sharpness obstruction

**Research object:** ERDOS-602-ESSENTIAL-DISJOINTNESS-001  
**Status:** PROVED_ON_PAPER_UNADJUDICATED — no Lean kernel proof, protected mathematical certification or global resolution  
**Date:** 2026-11-19 UTC  
**Related source audit:** [MATH-PROGRAMME #1873](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1873); result comment 7005914332 and source-critical review comment 7008579001.

## Exact problem and sources

Erdős, *Some problems on finite and infinite graphs* (1987), item 12, printed p. 227, asks whether any indexed family of countably infinite sets having finite pairwise intersections of cardinality other than one always has Property B (no member monochromatic under some two-colouring): <https://www.renyi.hu/~p_erdos/1987-28.pdf>.

The protected catalogue pin teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89, entry 602, records the original question OPEN. The admitted formal statement is google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020, FormalConjectures/ErdosProblems/602.lean, blob 9b85fd453afcfa95c6572e2a98d214d50f7e8caa; its main declaration contains a sorry, not a proof. Csernák–Soukup, *Infinite combinatorics revisited in the absence of Axiom of choice*, Archive for Mathematical Logic 64 (2025), Theorem 4.2(4), establish Property B for uniformly bounded finite pair-intersections. Their result is already known and does not settle the unbounded finite-intersection problem. <https://doi.org/10.1007/s00153-024-00946-1>.

## Theorem A — finite backward overlap

Let $I$ and $X$ be sets and let $A_i\subseteq X$ be infinite for all $i\in I$. Suppose all distinct pairwise intersections $A_i\cap A_j$ are finite. Suppose also that the index set admits a well-order $\prec$ such that for every $i$ the set

$$
P_i=\{j\in I:j\prec i,\;A_i\cap A_j\ne\varnothing\}
$$

is finite. Then there are finite $F_i\subseteq A_i$ such that the residuals $B_i=A_i\setminus F_i$ are infinite and pairwise disjoint.

**Proof.** For each $i$, define

$$
F_i=\bigcup_{j\in P_i}(A_i\cap A_j).
$$

Each $F_i$ is finite because it is the union of finitely many finite sets, so $B_i$ is infinite. Given distinct indices, assume $i\prec j$. If the original intersection is empty, the residuals cannot meet. Otherwise $i\in P_j$, so every point of $A_i\cap A_j$ belongs to $F_j$. Again $B_i\cap B_j=\varnothing$. This proves the assertion. QED.

**Property B consequence.** If the $A_i$ are countably infinite, each $B_i$ is countably infinite. Select an enumeration of each residual in ZFC. Colour its even-indexed elements red and odd-indexed elements blue. As the residuals are pairwise disjoint, no assigned colours conflict. Colour unused points arbitrarily. Each original member has infinitely many points of each colour. The no-singleton-intersection condition is not needed for this sufficient theorem.

## Corollary B — locally countable intersection graph

Assume the $A_i$ are infinite, their distinct pairwise intersections finite, and each $A_i$ meets only countably many other indexed sets. Then there are finite deletions making the residual sets infinite and pairwise disjoint. If the members are countably infinite, Property B follows with both colours occurring infinitely often.

**Proof.** Construct the graph on the indices joining distinct $i,j$ whenever $A_i\cap A_j$ is nonempty. It has countable vertex degrees. Every connected component is countable in ZFC, being the union of its countably many finite-distance balls, each countable. Well-order the components and enumerate each component in finite or $\omega$ order. Concatenate these orders. Any earlier neighbour of $i$ belongs to its own component, and there are only finitely many earlier members in that component. Thus the order satisfies Theorem A. QED.

This strengthens the prior GCL #1873 local-countability **colouring** theorem to **essential disjointness** when pairwise finite intersections are also assumed. The conclusion is more structural, but not universal.

## Counterexample C — Property B does not imply essential disjointness in the original class

Let $X$ be the countable set of finite binary strings together with two distinct new points $p,q$. For every infinite binary sequence $x\in 2^{\mathbb N}$ define

$$
A_x=\{x\upharpoonright n:n\in\mathbb N\}\cup\{p,q\}.
$$

Each $A_x$ is countably infinite. Distinct infinite binary sequences have only finitely many common finite prefixes; thus all distinct pairwise intersections are finite. Every such intersection contains both $p$ and $q$, so it never has size one. The family satisfies **every assumption of the original Erdős #602 question**. Colour $p$ red and $q$ blue, then colour other points arbitrarily: every member has both colours, so the family has Property B.

Nevertheless, there can be no finite $F_x\subseteq A_x$ making the residuals infinite and pairwise disjoint. If they existed, choose for each residual its least element relative to a fixed enumeration of the countable $X$. This would inject the uncountable index set $2^{\mathbb N}$ into $X$, a contradiction. QED.

This is a counterexample to the proposed proof **method** of deducing unrestricted Property B from universal essential disjointness. It is **not** a counterexample to Property B. Within the exact original hypothesis class, essential disjointness is strictly stronger than Property B.

## Adversarial review gates and next formal obligation

1. The finite-intersection assumption is necessary for the explicit finite-deletion construction in Theorem A. Finite intersections **alone** do not imply finite backward neighbour sets.
2. The corollary requires ZFC countable choice and uses a well-order of components. It never asserts that the whole index set is countable.
3. The finite binary prefix example has uncountably many indices but a countable ground set, so the residual-disjointness contradiction needs no extra cardinal arithmetic assumption.
4. Splitting all finite subfamilies is insufficient to obtain a global splitting by ordinary compactness; nonmonochromaticity for an infinite set is an open, generally nonclosed condition in the binary product space.
5. Lean target A: formalize finite backward overlap, finite deletions and pairwise disjoint infinite residuals.
6. Lean target B: formalize countable components and their concatenated ordering.
7. Lean target C: formalize the binary-prefix construction and verify it satisfies the no-singleton hypothesis, has Property B, and is not essentially disjoint.

**Acceptance:** exact source/toolchain identity, no sorry/admit in the completed proof, axiom report, exact-head replay, specialist source-semantic and mathematical review. None is claimed here. This is a candidate research handoff, not mathematical certification, unrestricted solution, or permission to launch a new Solve campaign.

**Residual:** unrestricted families with unbounded finite intersections and no adequate finite-backward-neighbour ordering. The full Erdős #602 question remains OPEN; the earlier source-audit issue #1873 remains administratively closed.
