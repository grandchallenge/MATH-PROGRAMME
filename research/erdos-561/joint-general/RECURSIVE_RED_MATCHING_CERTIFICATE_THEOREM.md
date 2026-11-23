# Erdős #561: an additional RED-matching proof rule for arbitrary-length three-BLUE residuals

**2026-11-23. Mathematical state: UNDER_REVIEW.** The finite verifier is independently CHECKED only after exact-head replay. All host graphs below are arbitrary finite simple graphs; all target star forests use ordinary non-induced vertex-disjoint copies. This is an enlargement of the source-proved sufficient-certificate procedure, not a proof of the all-profile conjecture or a MATHCERT certification. Its input theorems are not independently re-certified here.

## 1. The missing complementary inference

For an original nonincreasing positive RED list $n=(n_1,\ldots,n_s)$, with $s\ge4$, and original BLUE list $m=(u,v,g)$, with $u\ge v\ge g\ge1$, let

$$
f=n_s,\qquad
a_i=n_i-f+1,\qquad
U=u-g+1,\qquad V=v-g+1.
$$

Thus the normalized RED list $a$ ends in one, and the normalized BLUE list $b=(U,V,1)$ has positive entries. Suppose that the penultimate normalized RED size is at least two:

$$
a_{s-1}\ge2.
$$

Let $q=(a_1-1,\ldots,a_{s-1}-1)$, a sorted positive RED list of length $s-1$. Define the nonnegative RED matching loss

$$
\boxed{
P_{\rm R}(n,m)=
\bigl(U-\max(a_{s-2},a_{s-1}+V-1)\bigr)_+
+\bigl(V-a_{s-1}\bigr)_+.
}
$$

Let $J_{\rm can}(n,m)$ be the sum of all canonical antidiagonal weights except the first, and let $J_{\rm actual}(n,m)$ be the least number of edges of an arbitrary simple graph arrowing BOTH original residual pairs.

**Theorem A (RED matching transfer, all RED lengths).** For every $s\ge4$ and positive lists satisfying the displayed hypotheses,

$$
\boxed{
J_{\rm actual}(n,m)
\ge J_{\rm can}(n,m)-P_{\rm R}(n,m)
-\bigl(J_{\rm can}(q,b)-J_{\rm actual}(q,b)\bigr).
}
$$

In particular, if $P_{\rm R}=0$ and the strictly shorter joint residual pair $(q,b)$ has an independently proved sharp canonical value, then the ORIGINAL arbitrary-host joint pair $(n,m)$ is also sharp canonical.

The result **does not assert** that $(q,b)$ is sharp merely because its canonical star host exists. The shorter result must be a valid source-backed certificate. When either deficit is positive, the theorem supplies a quantitative lower bound rather than an unsupported exact claim.

## 2. Arbitrary-host graph proof and exact arithmetic

The SECOND original joint arrowing relation is

$$
Q\to(F(n),F(v,g)).
$$

Colour all edges touching an arbitrary vertex BLUE and the others RED. Since the BLUE edge set has vertex cover one, it cannot contain the two vertex-disjoint positive BLUE stars $F(v,g)$. Hence the red full forest $F(n)$ embeds in every $Q-t$.

For the normalized RED list $a$, its last size is one and its first $s-1$ sizes are at least two. Therefore its total vertex support is at least

$$
3(s-1)+2=3s-1.
$$

The previously source-proved Gallai matching obstruction in ALL_RED_LENGTHS_THREE_BLUE_STAIRCASE_THEOREM.md now applies to **every intermediate joint host**: its matching number is at least $s+1$. Briefly, if matching number were exactly $s$ while every vertex deletion preserved matching number $s$, Gallai factor-critical decomposition would leave at most $3s$ nonisolated vertices. The required red support after arbitrary nonisolated-vertex deletion forces precisely $s$ disjoint triangles; colouring $s-1$ triangles all RED and one all BLUE avoids both targets. Thus matching number must exceed $s$.

If $f>1$, choose a matching containing at least $s+1$ edges. Remove all its edges and colour them RED in any extension of a red/blue colouring. Each original RED star loses at most one edge; the two original joint residual arrowing conditions therefore persist with every RED size decremented by one. Repeat until the RED terminal size equals one.

Likewise, if $g>1$, remove and colour a matching BLUE to decrement all three BLUE sizes uniformly until the BLUE terminal becomes one. Both BLUE residual targets remain positive at every intermediate step, so both arrowing relations survive. The normalized RED support and the matching guarantee remain intact.

Each RED or BLUE uniform decrement reduces **all $s+1$ nonleading canonical antidiagonal weights by precisely one**, so removing each matching contributes at least the exact canonical decrement. We may therefore work at the normalized pair $(a,b)$ without loss.

At $a_s=1$, choose one further matching of at least $s+1$ edges, colour all its edges RED, and delete them. A red copy of the original forest loses at most one edge from each star. Discard its last one-edge star; the remaining forest contains $F(q)$. Likewise, a red copy of the first residual forest loses at most one edge from each remaining star and contains $F(q_{2:})$. BLUE edges are unchanged.

Thus the remaining graph is a JOINT residual host for the **shorter original** red list $q$ and the same blue list $b$:

$$
Q-M\to(F(q_{2:}),F(b)),
\qquad
Q-M\to(F(q),F(b_{2:})).
$$

Consequently

$$
e(Q)\ge(s+1)+J_{\rm actual}(q,b).
$$

An independent term-by-term antidiagonal calculation gives the exact identity

$$
\boxed{
J_{\rm can}(a,b)
=(s+1)+J_{\rm can}(q,b)+P_{\rm R}(n,m).
}
$$

All but the last two terms cancel as an exact one-edge decrease. The last two are the maxima producing the two displayed positive-part terms. Combining the two formulas and undoing all uniform decrements proves Theorem A for arbitrary $f,g$ and arbitrary finite simple host topology.

### Well-founded proof-certificate rule

The previous admitted certificate in RECURSIVE_THREE_BLUE_CERTIFICATE_THEOREM.md uses a BLUE matching, an individually exact two-BLUE residual, or a recursively certified shorter original residual. Add precisely this fourth possibility:

> **RED transfer:** After normalization, if $a_{s-1}\ge2$, $P_{\rm R}(n,m)=0$, and the proof procedure independently returns a sharp JOINT certificate for $(q,b)$, then return a sharp JOINT certificate for $(n,m)$ recording $P_{\rm R}=0$ and the complete nested shorter proof trace.

This is **well founded** because $q$ has exactly $s-1$ RED components. It may compose with the previously admitted first-residual ORIGINAL rule. Proof traces retain their leaf theorem, exact normalized parameters, canonical values and guard inequalities. No new self-certification authority is inferred from an automated trace.

## 3. New independently reproduced bounded coverage

The source-locked baseline proof procedure certifies **162,839** JOINT and **129,885** ORIGINAL profiles in its declared 179,928-profile grid, leaving 17,089 JOINT UNKNOWN.

Adding the RED matching rule and recursively re-evaluating ORIGINAL sharpness under the same protected transfer conditions yields:

| Value | Old certificate | Enhanced certificate |
| --- | ---: | ---: |
| Total profiles | 179,928 | 179,928 |
| Sharp JOINT proven by sourced sufficient rules | 162,839 | **165,677** |
| Sharp ORIGINAL proven by sourced sufficient rules | 129,885 | **131,052** |
| JOINT profiles still UNKNOWN by these rules | 17,089 | **14,251** |

Hence **2,838 additional JOINT** and **1,167 additional ORIGINAL** classifications become exact under already-established all-host mathematical lemmas. The enhanced count includes 78 joint and 24 original classifications omitted by a preliminary unit-terminal-only check; those omissions arose when a shorter RED list still had minimum size above one and required further normalization. These numbers are full counts within the **declared finite arithmetic parameter grid**, not a host graph census, not an independently verified universal theorem and not evidence that any UNKNOWN profile violates the canonical formula.

A minimal newly certified example is

$$
n=(7,5,2,1),\qquad m=(5,2,1).
$$

Here the normalized RED loss vanishes because

$$
P_{\rm R}=(5-\max(5,2+2-1))_++(2-2)_+=0.
$$

The shorter pair $q=(6,4,1)$ against the same blue list has a complete source-proved THREE-BY-THREE JOINT theorem. The RED transfer therefore establishes exact JOINT for $(7,5,2,1)$ versus $(5,2,1)$ over arbitrary finite simple graphs. The old recursive certificate did not recognize this implication.

The standalone verifier verify_recursive_red_matching_certificates.py imports the admitted baseline, adds only the source-backed RED rule, replays the entire grid, checks each old certificate remains accepted, records exact counts, and emits one inspectable nested proof. It guards normalization and the new exact antidiagonal identity independently over additional parameter cells. All output records have explicit theorem labels; computational success does not certify the source lemmas.

## 4. Remaining boundary

The 14,251 still UNKNOWN bounded cells do not imply a counterexample. They are profiles for which the combined direct BLUE loss, separate original residual, RED transfer, and protected ORIGINAL transfer have not established sharpness. Some exhibit genuinely positive BLUE and RED losses; others fail the vertex-support or protected degree-core criteria. Their resolution needs a stronger graph-theoretic bound, an additional legitimate transfer, or a verified counterexample.

The all-profile Erdős #561 conjecture remains OPEN/PARTIAL. Mathematical paper claim UNDER_REVIEW; finite trace classification CHECKED after exact-head replay; MATHCERT not issued.
