# Erdős #41 — Reciprocal-band overlap is an exact fourth-order obstruction

**20 October 2026.** This note identifies the arithmetic interaction that the universal one-anchor distance tax does **not** control. For two complete and genuinely compatible B3 blocks, there is an exact decomposition of their positive pair-sum difference spectrum. The two near-future reciprocal bands can overlap, and every overlap beyond the unavoidable base differences witnesses a nontrivial equal **four-term** sum. A genuine finite B3 carrier with nonzero extra overlap is provided. These finite facts do not establish a critical-density valley or solve Erdős #41.

## 1. Three disjoint distance scales, no residue or location-alignment hypothesis

Let P and Y be nonempty, disjoint subsets of a single repetition-allowed B3 set, and suppose

$$
P\subseteq[1,R],\qquad
Y\subseteq[L,L+R-1],\qquad L>5R.
$$

Let $Q(Z)=\{a+b:a,b\in Z,\ a\le b\}$, $T(Z)=Z+Z-Z$, and $\Delta_+(E)=\{u-v:u,v\in E,\ u>v\}$. Thus $D(Z)=\Delta_+(Q(Z))$.

Pair sums of the full set split into three disjoint, ordered bands

$$
Q(P\cup Y)=
Q(P)\;\dot\cup\;(P+Y)\;\dot\cup\;Q(Y).
$$

**Theorem A (exact two-block difference decomposition).** The complete positive pair-sum difference spectrum is

$$
\boxed{
\begin{aligned}
D(P\cup Y)
={}&
\underbrace{[D(P)\cup\Delta_+(P+Y)\cup D(Y)]}_{\text{short distances}}\\
&\dot\cup\;
\underbrace{[(Y-T(P))\cup(T(Y)-P)]}_{\text{reciprocal near band}}\\
&\dot\cup\;
\underbrace{[Q(Y)-Q(P)]}_{\text{far band}}.
\end{aligned}
}\tag{TWO-BLOCK-EXACT-DECOMPOSITION}
$$

The three bracketed groups are mutually disjoint (even though the sets *within* a bracket may overlap). Every short distance is at most $2R-2$, the near band lies in $[L-2R+1,L+2R-3]$, and the far band begins at $2L-2R$.

**Proof.** Every difference between two elements of $Q(P\cup Y)$ belongs to one of six unordered pairings of its three ordered sum bands. Differences taken within $Q(P)$, $P+Y$, and $Q(Y)$ form the three short sets. Differences of the middle sum band minus the old sum band are

$$
(P+Y)-Q(P)=Y-(Q(P)-P)=Y-T(P).
$$

Differences of the new sum band minus the middle one are

$$
Q(Y)-(P+Y)=(Q(Y)-Y)-P=T(Y)-P.
$$

Finally $Q(Y)-Q(P)$ forms the far band. The stated interval bounds, using $L>5R$, show that the short, near and far bands cannot intersect each other. Thus the decomposition is exact. QED.

## 2. Fourth-order defect in reciprocal near-band amplification

Define the *reciprocal fourth-order overlap* and its nontrivial part by

$$
\mathcal O(P,Y)=(Y-T(P))\cap(T(Y)-P),
\qquad
\Xi_4(P,Y)=|\mathcal O(P,Y)\setminus(Y-P)|.
$$

**Theorem B (exact mixed-four-sum obstruction).** Because P union Y is B3, the map $(y,p)\mapsto y-p$ is injective. Furthermore,

$$
\boxed{
Y-P\subseteq\mathcal O(P,Y),\qquad
|\mathcal O(P,Y)|=|P||Y|+\Xi_4(P,Y).
}\tag{FOURTH-ORDER-DEFECT}
$$

Each value in $\mathcal O(P,Y)\setminus(Y-P)$ produces two **distinct unordered four-element multisets** from $P\cup Y$, with identical four-term sums and with two P terms and two Y terms on each side. These are genuine B4 collisions, which need not violate B3.

**Proof.** Both P⊂T(P) and Y⊂T(Y), so every $y-p$ is in both reciprocal bands. If $y-p=y'-p'$, then $y+p'=y'+p$; the B2 property of a B3 set forces equality of the two disjoint colour pairs, hence $(y,p)=(y',p')$ and $|Y-P|=|P||Y|$.

An arbitrary $d\in\mathcal O$ admits

$$
d=y_0-(p_1+p_2-p_3)
=(y_1+y_2-y_3)-p_0,
$$

and hence

$$
\boxed{
y_0+y_3+p_3+p_0=y_1+y_2+p_1+p_2.
}\tag{MIXED-FOUR-SUM-COLLISION}
$$

If the two unordered four-multisets were equal, comparing their P and Y colour parts would give $p_1+p_2=p_3+p_0$ and $y_1+y_2=y_0+y_3$, so $d=y_0-p_0\in Y-P$. Consequently any $d\notin Y-P$ forces a **nontrivial** equal four-term sum. Moreover, because the full set is B3, such unequal four-multisets cannot share even one common element: cancelling that element would give a nontrivial B3 triple collision. QED.

**Corollary (exact reciprocal amplification balance).** Writing $U=Y-T(P)$ and $V=T(Y)-P$,

$$
\boxed{
|U\cup V|=|U|+|V|-|P||Y|-\Xi_4(P,Y).
}\tag{RECIPROCAL-AMPLIFICATION-BALANCE}
$$

Thus adding the sizes of both reciprocal bands *as if they were independent* would overcharge the available distance capacity by the unavoidable $|P||Y|$ plus the genuine fourth-order defect $\Xi_4$. The B3 property by itself does not assert $\Xi_4=0$ or $\Xi_4=o(R)$.

If the whole carrier were also B4, then $\Xi_4=0$; Erdős #41 concerns only B3, and no B4 assumption is permitted.

## 3. Exact hostile finite B3 witness

Take the genuine eight-element B3 prefix

$$
(1,2,5,14,33,72,125,219)
$$

and set

$$
P=\{1,2,5,14\},\quad
Y=\{1033,1072,1125,1219\},\quad
R=187,\quad L=1033>5R.
$$

The translated union P∪Y is **genuinely B3**, including repeated summands. Direct exact enumeration yields

$$
\begin{aligned}
|U|&=111,&|V|&=110,\\
|U\cap V|&=27,&|Y-P|&=16,\\
\Xi_4(P,Y)&=11,&|U\cup V|&=194.
\end{aligned}
$$

The short, reciprocal and far distance bands have 112, 194 and 97 distinct positive values, respectively, for a complete spectrum of 403 values; the independent complete difference enumeration gives the same 403. The eleven extra reciprocal coincidences are not a violation of B3: they correspond to admissible equal **four-term** sums.

A concrete nontrivial witness is

$$
1+1+1033+1125=2+14+1072+1072=2160.
$$

The two four-term multisets have no common element, so no term can be cancelled to obtain a forbidden three-term equality.

The defect is invariant under any additional translation of Y that keeps the blocks separated, so it cannot be dismissed as an accidental choice of absolute position.

## 4. Consequence for the sought density deficit

We have a full accounting of **what changes when a critically populated future block arrives**:

- the one-anchor bands are exact and nonduplicated;
- a multi-element block adds reciprocal near bands but their union is reduced by the exact fourth-order overlap defect;
- these fourth-order coincidences are permitted by B3 and can persist under changes of absolute scale or block centres.

A universal density-loss theorem must therefore do more than sum first-order signed-shadow or distance counts. It must control the **dependent future cost** of the mixed B4 collision witnesses, or prove that sustained overlap forces a different shortage in the later signed-code compatibility conditions.

A possible new sufficient gate is a c-sensitive dichotomy: on successive actually populated windows, either the *new* reciprocal bands occupy too much disjoint range, or the fourth-order defect needed to absorb their overlap forces a quantified further incompatibility of later B3 batches. **Neither alternative is presently proved**. Requiring a small $\Xi_4$ without proof would simply replace the original conjecture with a new unproved regularity assumption.

Known external context: the even/odd distinction in infinite Sidon-type density results is discussed in Christian Táfula, *Infinite Sidon-type sets for zero-sum linear forms* (2026), https://doi.org/10.1007/s00605-026-02211-4. This note proves only its displayed finite identities, not a new theorem about the general liminf.

GCL research docket #2622; independent mathematical review remains required. Erdős #41 remains OPEN.
