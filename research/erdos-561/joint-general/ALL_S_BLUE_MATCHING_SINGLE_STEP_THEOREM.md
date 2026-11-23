# Erdős #561 — ALL-s RED forests versus THREE BLUE stars: a single-BLUE-matching exactness criterion

**Research date:** 2026-11-23. **Mathematics:** paper proof UNDER_REVIEW, finite arithmetic and explicit witness checks only CHECKED at exact source head. **Host class:** all finite simple graphs; ordinary non-induced vertex-disjoint positive star forests. The unrestricted all-profile Erdős #561 conjecture and the full joint-residual statement in #3490 remain OPEN/PARTIAL. No MATHCERT or historical priority claim.

**Substantive improvement:** For a large class of arbitrary heterogeneous profiles with ANY number $s\ge3$ of RED stars against three BLUE stars, a **single BLUE matching removal** proves a sharp JOINT residual bound. The method uses only the previously source-proved *two-component residual bridge* (three-by-three reconstruction, Lemma 1, after interchanging colours) and Gallai matching stability. It **does not require the full three-by-three JOINT theorem or induction on RED component count**. The result contains the all-lengths staircase and equal-top subfamilies as special zero-deficit cases, while covering many further unrelated RED profiles.

## 1. Exact theorem and finite parameter criterion

Let $s\ge3$. Let the original RED list $n=(n_1,\ldots,n_s)$ and original BLUE list $m=(u,v,g)$ be positive nonincreasing, where $u\ge v\ge g\ge1$. Define their terminally normalized lists

$$
a_i=n_i-n_s+1\quad(1\le i\le s),\qquad
U=u-g+1,\quad V=v-g+1.
$$

Thus $a_s=1$, and the BLUE normalized list is $(U,V,1)$. Assume

$$
V\ge2,\qquad
\boxed{\sum_{i=1}^{s}(a_i+1)\ge3s-1.}
$$

The latter is an explicit **vertex-support hypothesis**, equivalent to $\sum_i a_i\ge2s-1$, and not a restriction that the host graph be a forest.

For $1\le i\le s-1$ define the two-arm BLUE interference maximum

$$
T_i=\max\bigl(a_{i+1}+V-1,\quad
     a_{i+2}+U-1\text{ when }i+2\le s\bigr),
$$

where the second candidate is simply omitted at $i=s-1$. Put

$$
\boxed{P^{\rm BLUE}_s(n,m)=\sum_{i=1}^{s-1}(a_i-T_i)_+,
\qquad (x)_+=\max(0,x).}
$$

Let $J_{\rm can}(n,m)$ denote the canonical sum of the $s+1$ antidiagonal weights other than the first:

$$
J_{\rm can}(n,m)
=\sum_{k=3}^{s+3}\max_{i+j=k}(n_i+m_j-1).
$$

**Theorem (general all-s BLUE-matching lower bound).** Every finite simple graph $Q$ satisfying the TWO genuinely required joint-residual relations

$$
Q\to(F(n_2,\ldots,n_s),F(u,v,g)),
\qquad
Q\to(F(n),F(v,g))
$$

obeys the exact quantitative lower bound

$$
\boxed{e(Q)\ge J_{\rm can}(n,m)-P^{\rm BLUE}_s(n,m).}
$$

The canonical disjoint-star joint host has exactly $J_{\rm can}(n,m)$ edges. Therefore:

**If the explicit $s-1$ nonnegative summands all vanish, i.e. $a_i\le T_i$ for every $i$, the unrestricted-host JOINT residual minimum is EXACTLY $J_{\rm can}(n,m)$.**

Furthermore, whenever $P^{\rm BLUE}_s=0$ and the existing source-proved ORIGINAL core-transfer criterion

$$
W_{\rm can}(n,m)\le\frac{D(D+1)}2,\qquad D=n_1+u-2
$$

also holds (with positive leading caps), the ORIGINAL unrestricted size Ramsey number is EXACTLY

$$
\widehat r(F(n),F(m))=W_{\rm can}(n,m).
$$

If $P^{\rm BLUE}_s>0$, **only** the displayed quantitative lower is claimed. The theorem does not assume the JOINT conjecture for arbitrary profiles.

## 2. Matching-size obstruction for unrestricted host topology

The second joint relation implies $Q\to(F(n),F(v,g))$, where the BLUE target has TWO vertex-disjoint positive stars. For any vertex $t$, colour all $Q$ edges incident with $t$ BLUE and the rest RED. The BLUE graph has vertex cover $\{t\}$ and cannot contain $F(v,g)$. Thus **every** $Q-t$ contains all $s$ disjoint RED stars.

For the normalized RED list $(a_i)$ the RED target requires at least $3s-1$ vertices. Since the original red sizes $(n_i)$ are no smaller, the same holds at every stage of terminal-size reduction below. If $\nu(Q)=s$, matching stability after EVERY vertex deletion and Gallai's factor-critical theorem force $Q$ to have at most $3s$ nonisolated vertices. RED target support after deletion of a nonisolated vertex forces equality, hence precisely $s$ connected factor-critical components of matching number one, each a triangle: $sK_3$. Colour $s-1$ triangles entirely RED, the remaining triangle BLUE. RED support has $3s-3$ vertices, less than $3s-1$; BLUE support three vertices, less than the four required for two positive blue stars. This is an avoiding colouring, contradiction. Therefore

$$
\boxed{\nu(Q)\ge s+1}
$$

for EVERY arbitrary-host joint graph satisfying the support condition.

The same proof applies to every intermediate joint host produced by monochromatic matching deletion as long as the normalized RED support remains at least $3s-1$ and the BLUE second residual still has two positive stars. Both facts hold by construction.

## 3. Exact normalization, BLUE deletion and algebraic penalty

If the RED minimum $n_s=f>1$, choose a matching of at least $s+1$ edges, extend any colouring of the edge-deleted graph by making the matching RED, and use both original JOINT relations. Each RED star meets the matching in at most one edge. Removing it therefore makes the edge-deleted graph jointly arrow the original RED list with ALL entries decremented by one and the same BLUE list. The RED forest remains positive.

If the BLUE minimum $g>1$, perform the analogous reduction with a matching coloured BLUE. Each BLUE star meets the matching in at most one edge, so ALL three BLUE entries decrease by one. The BLUE residual $(v,g)$ remains two positive stars throughout.

At each such decrement, **all $s+1$ JOINT canonical antidiagonal weights decrease by exactly one**. The terminally normalized lists $(a_i)$ and $(U,V,1)$ are invariant. Since the matching size is at least $s+1$, it is sufficient to prove the theorem for terminal minima $f=g=1$.

Now work with RED $a=(a_1,\ldots,a_{s-1},1)$ and BLUE $m^\flat=(U,V,1)$ with $V\ge2$. The matching lemma again provides $M$ of at least $s+1$ edges. Colour M **BLUE**. For either original residual relation, a blue star loses at most one edge from M. Hence the edge-deleted graph $Q-M$ jointly arrows

$$
Q-M\to(F(a_2,\ldots,a_s),F(U-1,V-1)),
$$

$$
Q-M\to(F(a),F(V-1)).
$$

Interchange RED and BLUE. These are **exactly** the two hypotheses of Lemma 1 in \`THREE_BY_THREE_JOINT_RECONSTRUCTION.md\`, with red two-arm original list $(U-1,V-1)$ and arbitrary blue original list $a$, possibly containing any number $s$ of positive components. The lemma is unrestricted-host and proves the sharp canonical two-arm JOINT residual lower

$$
e(Q-M)\ge J_{\rm can}(a,(U-1,V-1)).
$$

Now verify the exact algebra. Let $A_k$ be the antidiagonal maximum using only BLUE arms $U,V$, and let $C_k$ use BLUE $(U-1,V-1)$. For $3\le k\le s+2$, $C_k=A_k-1$. At $k=3$ the old three-BLUE antidiagonal equals $A_3$, contributing exactly one edge difference. For each $4\le k\le s+2$, the third BLUE arm contributes $a_{k-3}$, so the old maximum is $\max(A_k,a_{k-3})$, contributing

$$
\max(A_k,a_{k-3})-C_k
=1+(a_{k-3}-A_k)_+.
$$

The final original three-BLUE antidiagonal at $k=s+3$ is $a_s=1$. Summing the $s$ shared weights and the additional final weight yields

$$
\boxed{
J_{\rm can}(a,(U,V,1))
=(s+1)+J_{\rm can}(a,(U-1,V-1))
 +\sum_{i=1}^{s-1}(a_i-T_i)_+.
}
$$

This identity is **exact**, not a recurrence assumption or computational extrapolation. Combining it with $e(Q)\ge|M|+e(Q-M)$ proves the stated lower. Reversing all legitimate normalization steps adds at least $s+1$ graph edges for each red or blue terminal increment, matching the change in $J_{\rm can}$ exactly. The theorem holds for arbitrary positive terminal sizes $f,g$, provided the stated normalized red-support and $V\ge2$ conditions hold. QED.

## 4. Stronger reconstruction of the all-length staircase: one BLUE matching instead of length induction

For the heterogeneous staircase of \`ALL_RED_LENGTHS_THREE_BLUE_STAIRCASE_THEOREM.md\`, normalize $r,k$ to zero and write

$$
a_1=(2s-3)h+1,\quad a_2=2(s-3)h+1,
\quad a_i=2(s-i)h+1\ (3\le i\le s),
$$

with BLUE $(U,V,1)=(4h+1,2h+1,1)$.

The RED support is at least $3s-1$ for all $s\ge3,h\ge1$. The entire BLUE deficit vanishes term by term:

- For $i=1$, the second candidate $a_3+U-1=2(s-3)h+1+4h=2(s-1)h+1$ exceeds $a_1=(2s-3)h+1$ by $h$.
- For $i=2$, $a_3+V-1=a_2+2h$ exceeds $a_2$.
- For $3\le i\le s-1$, consecutive staircase arms have gap exactly $2h$, so $a_{i+1}+V-1=a_i$.

Thus **$P^{\rm BLUE}_s=0$ for EVERY $s$**, and a **single** BLUE matching deletion from the original JOINT host, followed by the already proved two-component residual bridge, establishes the full canonical lower immediately. No induction on the number of RED components and no FULL three-by-three JOINT theorem are needed to prove the staircase JOINT value.

The first individually required residual is an **equal-top** RED staircase $B_L$ with $L=s-1$. Its BLUE deficit vanishes just as directly: $a_1=a_2$, while all remaining consecutive arms after the second differ by $2h$; hence each $a_i$ is no larger than the appropriate $T_i$. Its normalized RED support satisfies the theorem hypothesis for $L\ge3$. Thus its JOINT formula ALSO follows directly from this single-BLUE-matching theorem, without the separate length induction previously used. For $L=3$, the ORIGINAL exact value is already source-proved by the complete three-by-three theorem; for $L\ge4$, protected ORIGINAL degree-core transfer applies with a strictly positive margin (minimum $4$ at $L=4,h=1,r=k=0$); and for $L=2$ the pinned published two-component original theorem applies.

Consequently BOTH individual ORIGINAL residual minima for the main staircase remain sharp, so the ACTUAL switching surplus of $h$ is retained. This source improvement **removes a long inductive dependency from the JOINT proof**, without weakening the evidence or altering any protected status. The earlier length-induction manuscript remains a valid alternative proof route, but is no longer essential to this family's joint claim.

## 5. Finite parameter coverage and exact remaining boundary

The separate deterministic checker \`verify_all_s_blue_matching_bridge.py\` computes all index maxima two different ways; independently checks the explicit BLUE deficit with $s-1$ terms against canonical JOINT subtraction on ordered profiles; counts zero-penalty cases meeting the RED support condition and positive switching cases; verifies red/blue terminal-shift invariance, source-proved staircase and equal-top ZERO penalties for multiple component counts and scales; and executes actual $sK_3$ avoiding-colouring graph-embedding checks.

The bounded declared search, RED length $s=3,\ldots,8$, sorted RED largest $s-1$ entries from $1,\ldots,8$ with terminal one, and BLUE $(U,V,1)$ with $2\le V\le U\le8$, contains 179,928 parameter cells, of which **177,856** satisfy the RED support condition, **134,447** have both support and $P^{\rm BLUE}_s=0$, and **11,142** of those also have positive *canonical* switching surplus. Under the protected ORIGINAL core criterion, **7,090** of those latter profiles also establish sharp ORIGINAL values. The switching surplus for arbitrary counted profiles is a **canonical** difference unless their individual residual minima have separately been proved sharp. The staircase's actual switching gap is proved separately above.

All numeric counts are bounded checks, not proof by sampling. The **mathematical boundary** outside the new theorem is precise: normalized RED support below $3s-1$, normalized BLUE second arm $V=1$, and/or a positive BLUE deficit $P^{\rm BLUE}_s>0$. Where this theorem's conditions fail, other source-proved RED matching, separate-residual and structural lemmas may still apply. The full arbitrary-profile JOINT lower, the complete original Erdős #561 conjecture and MATHCERT remain OPEN/PARTIAL.