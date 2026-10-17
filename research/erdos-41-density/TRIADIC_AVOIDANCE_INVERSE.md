# Erdős #41 Stage B — triadic arithmetic inverse for forbidden-distance avoidance

**Disposition (2026-10-17):** new finite weighted triangle / three-bin residue-capacity theorems PROVED in ordinary mathematics, exact computational controls included. **NOT PROVED:** the sought universal positive-critical-density avoidance-to-CRT-density-cost dichotomy or Erdős #41. This branch is independent of unmerged PRs #2696, #2713 and #2714.

## 1. Question and the missing arithmetic compatibility

For a finite repeated-summand B3 set A, let U,W be disjoint subsets, with every member of U below W. The complete unordered pair-sum family is

$$
P=P_U=\{u+v:u,v\in U,\ u\le v\},\quad
r_U(h)=\#\{(p,p')\in P^2:p-p'=2h\}
\quad(h\ge1).
$$

For positive outer differences the uniquely oriented aggregate is

$$
\mathcal M(U,W)=\sum_{\{x,y\}\subset W,\ x<y}r_U(y-x).
$$

A is B3, hence B2 (including repeated summands). Every nonzero ordered difference in W uniquely determines its **ordered endpoints**. This fact was already used in the pairwise residue-difference capacity theorem. The new constraint uses the *compatibility of several actual differences of W*.

Given x<y<z in W, their positive differences are a=y-x, b=z-y, and a+b=z-x. Their three differences must belong to the actual allowed spectrum if M=0. Also a!=b, because three distinct equally spaced B2 points would have the repeated two-term sum x+z=2y. Thus zero-correlation avoidance requires **nondegenerate additive Schur triangles**, not just sufficient isolated allowed differences.

## 2. Complete weighted triangle theorem

Let L>=2 be an integer bound for the span of W. Define the finite set of candidate *oriented nondegenerate gap pairs*

$$
\mathcal T_L=\{(a,b)\in\mathbb Z_{>0}^2:
a+b\le L,\ a\ne b\}.
$$

For each candidate let its nonnegative integer weight be

$$
\omega_U(a,b)=r_U(a)+r_U(b)+r_U(a+b).
$$

Order all these weights increasingly as omega_1<=...<=omega_T, including multiplicities: (a,b) and (b,a) are separate candidates. For m>=3, let k=binom(m,3), and assume k<=T (which is automatic for a genuine B2 set W of size m and span<=L).

**Theorem A (triadic order-statistic inverse):**

$$
\boxed{
(m-2)\mathcal M(U,W)
=\sum_{x<y<z,\ x,y,z\in W}
\omega_U(y-x,z-y)
\ge \sum_{j=1}^{\binom m3}\omega_j .
}\tag{TRI-WEIGHT}
$$

**Proof.** The equality holds because every unordered outer pair occurs in precisely m−2 unordered outer triples; each triple contributes its three distinct edges once. Because W is B2, distinct increasing outer triples cannot have the same ordered adjacent-gap pair (a,b): the gap a identifies the endpoints (x,y) uniquely, and therefore b identifies the remaining z uniquely. Nor can a=b by the B2 property. Thus the binom(m,3) observed candidates form a **subset without repetitions** of T_L; their weight sum cannot be smaller than the sum of the binom(m,3) smallest candidate weights. QED.

This is an arithmetic *three-difference compatibility* statement. It is not a general graph-independent-set bound when W fails B2; the same gap pair can recur for translated triples, and three-term progressions then occur.

For integer threshold t>=1 define

$$
T_t(U,L)=\#\{(a,b)\in\mathcal T_L:
r_U(a)<t,\ r_U(b)<t,\ r_U(a+b)<t\}.
$$

**Theorem B (thresholded Schur-triangle inverse):**

$$
\boxed{
\mathcal M(U,W)\ge
\frac{t}{m-2}
\left[\binom m3-T_t(U,L)\right]_+
\quad(m\ge3).
}\tag{TRI-THRESHOLD}
$$

**Proof.** Call an unordered W pair heavy if its difference has r_U(h)>=t. Their number is at most M/t. Every W triple containing no heavy edge contributes a distinct candidate counted by T_t. Every heavy edge occurs in only m−2 W triples. Hence at least binom(m,3)−(m−2)M/t distinct zero-heavy-edge candidate triangles exist, which yields the bound. QED.

**Structural consequence (quantified, conditional):** If M=0 and W is B2 of size m in span L, the zero-correlation distance set

$$
Z_U(L)=\{1\le h\le L:r_U(h)=0\}
$$

must support at least binom(m,3) **distinct ordered nondegenerate Schur triangles** a,b,a+b. Under m>=cL^(1/3), this is at least (c^3/6)L−O_c(L^(2/3)). This is necessary arithmetic structure, not yet a density cost: a generic dense set Z can support order L² triangles, much more than the order-L critical requirement.

## 3. Exact finite strict improvement over pairwise capacities

Take the genuine B3 inner set U={1,2,5}. Its complete unordered pair sums are P={2,3,4,6,7,10}. Direct enumeration gives r_U(h)>0 for h=1,2,3,4 and r_U(h)=0 for h>=5.

Consider a candidate outer interval of **span L=10**, disjoint from U. The zero-correlation allowed positive distances are precisely 5,6,7,8,9,10.

A Q=1 *pairwise* difference-capacity certificate for an imagined three-point B2-independent W passes: it requests m(m−1)=6 distinct signed differences from 12 allowed signed integers. Ordinary mixed B3 triple-sum interval packing also permits m=3, since |P|m=6*3=18<=2 diam(U)+L+1=19.

But there is **no nondegenerate allowed additive triangle** in [1,10]. Any two allowed positive adjacent gaps a,b satisfy a+b>=10, and equality is possible only for a=b=5, which is forbidden by B2. Therefore T_1(U,10)=0 and (TRI-THRESHOLD) gives

$$
\boxed{
\text{For every three-point B2 }W
\text{ of span}\le10,\quad
\mathcal M(U,W)\ge1.
}\tag{STRICT-FINITE}
$$

This is a *strict and verifiable* improvement over the Q=1 pairwise capacity and the elementary mixed-triple **range-capacity** test. It is not a proof that a genuine six-element B3 set U union W realizes the equality case: the full B3 property imposes further restrictions and may exclude such W entirely. We distinguish the conditional implication from an existence witness.

A hostile non-B2 graph-independent set W={20,25,30} has all differences in {5,10}, hence M=0. It invalidates (STRICT-FINITE) if the B2 hypothesis is omitted. This is why ordinary alpha(G) cannot use the triadic theorem unconditionally.

## 4. More relevant: localized three-bin residue-triangle inverse

Let Y<Z<V be three **pairwise disjoint ordered** subsets of one B3 outer carrier, and Q>=1 a modulus. Write b^Y_s,b^Z_s,b^V_s for their occupancy counts in residue s.

The exact numbers of ordered outer triples with adjacent positive gaps congruent to (d,e) modulo Q are

$$
K_{d,e}=
\sum_{s\bmod Q} b^Y_s\,b^Z_{s+d}\,b^V_{s+d+e},
\qquad
\sum_{d,e}K_{d,e}=|Y||Z||V|.
$$

The candidate gaps satisfy

$$
\begin{aligned}
a&\in J_{YZ}=[\min Z-\max Y,\max Z-\min Y],\\
b&\in J_{ZV}=[\min V-\max Z,\max V-\min Z],\\
a+b&\in J_{YV}=[\min V-\max Y,\max V-\min Y],\\
a&\ne b.
\end{aligned}
$$

For each (d,e), list these candidate gap pairs with a=d mod Q, b=e mod Q and their exact costs omega_U(a,b). Sort their weights as omega_(d,e),j, in nondecreasing order.

**Theorem C (oriented three-bin residue-triangle inverse):**

$$
\boxed{
|V|\,\mathcal M_{Y,Z}(U)
+|Y|\,\mathcal M_{Z,V}(U)
+|Z|\,\mathcal M_{Y,V}(U)
\ge\sum_{d,e\bmod Q}\sum_{j=1}^{K_{d,e}}
\omega_{(d,e),j}.
}\tag{THREE-BIN}
$$

Here M_(Y,Z) counts each actual cross-bin outer pair exactly once, weighted by r_U; similarly for the other two pairs.

**Proof.** The left expression is precisely the sum of the three-edge weights over all |Y||Z||V| actual outer triples, because each cross-bin edge appears with the number of choices for the third-bin element. As in Theorem A, B2 uniqueness makes the observed ordered adjacent-gap pairs distinct. Moreover each actual triple has a candidate pair in the stated intervals and one congruence class (d,e), of which there are exactly K_(d,e) for the actual residue occupancies. Taking the smallest eligible candidate costs in each class proves the bound. QED.

The right side is zero when the zero-weight candidate triangle capacities suffice. If all three cross-bin correlations vanish, then for every (d,e)

$$
\boxed{
K_{d,e}\le Z^0_{d,e},
}\tag{TRIADIC-AVOID}
$$

where Z^0_(d,e) counts **distinct** candidates of zero weight among the displayed admissible gap pairs. These are explicit *cubic* constraints on the actual outer residue counts, whereas the prior oriented two-bin theorem imposes quadratic constraints. They may be combined without repeatedly counting the same outer pairs: for a chosen three-bin family use (THREE-BIN) as one joint constraint, not as an additional charge in a summed global budget.

For Q exceeding both candidate gap-range widths, every residue pair (d,e) identifies at most one candidate gap pair, and the bound becomes equality for the given actual outer bins. This is a verification limit, not an asymptotic density improvement.

## 4A. A proved localized residue-spectrum density cost (the stronger inverse gate)

There is a second, complementary inverse route that *does* convert **specific missing residues in the actual inner allowed-distance spectrum** into a quantified outer-density restriction. It uses the standard Cauchy–Davenport theorem in prime cyclic groups; no Fourier mixing assumption is introduced.

Let Y<Z be two nonempty actual B3 outer bins, of enclosing diameters D_Y,D_Z>=1, and put

$$
J=[\min Z-\max Y,\max Z-\min Y]\cap\mathbb Z,
\qquad m_Y=|Y|,\quad m_Z=|Z|.
$$

Fix integer threshold t>=1. For each prime p, let

$$
E_{p,t}=\{h\bmod p:h\in J,\ r_U(h)<t\},
\qquad e_{p,t}=|E_{p,t}|,
$$

and define the finite, **inner-spectrum-only** cap

$$
c_{p,t}=
\begin{cases}
(e_{p,t}+1)/2,&e_{p,t}<p,\\
p,&e_{p,t}=p.
\end{cases}
$$

The first value may be a half-integer; this only weakens an integer bound and is safe. Choose pairwise distinct primes p_1,...,p_s with product Q<=min(D_Y,D_Z), and define

$$
\boxed{
B_t(U;Y,Z,\mathbf p)
=
\left(\frac{144D_YD_Z}{Q^2}\right)^{1/3}
\prod_{j=1}^s c_{p_j,t}^{\,2}.
}\tag{BIN-CRT-BUDGET}
$$

**Theorem D (prime-residue localized inverse; robust form).** With
$\mathcal M_{Y,Z}(U)=\sum_{y\in Y,z\in Z}r_U(z-y)$, one has

$$
\boxed{
\mathcal M_{Y,Z}(U)\ge
\frac{t}{\max(m_Y,m_Z)}
\left[m_Ym_Z-B_t(U;Y,Z,\mathbf p)\right]_+ .
}\tag{LOCAL-CRT-INV}
$$

In particular if the actual cross-bin correlation is zero,

$$
\boxed{
m_Ym_Z\le B_1(U;Y,Z,\mathbf p).
}\tag{ZERO-CRT}
$$

**Proof, including the exact B3/B2 dependency.** Count the heavy cross-bin edges (y,z) whose weight r_U(z-y)>=t. Their number e is at most M_(Y,Z)/t. Delete at most one endpoint for every heavy edge, obtaining nonempty B3 subsets Y' subset Y and Z' subset Z without heavy cross edges unless e>=min(m_Y,m_Z), in which case the desired bound follows immediately from M>=t min(m_Y,m_Z) and B_t>=0.

For every prime p, the residue-difference set (Z' mod p)−(Y' mod p) is contained in E_(p,t). If e_(p,t)<p, **Cauchy–Davenport** gives
|Z' mod p|+|Y' mod p|−1<=e_(p,t); therefore their residue-class count product is at most ((e_(p,t)+1)/2)^2 by AM–GM. If e_(p,t)=p, each occupied residue count is at most p, yielding the same bound with c_(p,t)=p.

The Chinese remainder theorem bounds the number of occupied classes modulo Q by the product of occupied classes modulo the individual primes. The elementary B3 cubic-shadow dispersion theorem (proved separately in PR #2714) bounds any B3 subset X of an enclosing integer span D>=Q by

$$
|X|^3Q\le12D\,t_Q(X)^3.
$$

This remains true for |X|<=1 by Q<=D. Apply it to Y',Z', multiply, and insert the prime residue-product bounds. We obtain $|Y'||Z'|\le B_t$. If a elements of Y and b elements of Z were removed, a+b<=e, so

$$
|Y'||Z'|=(m_Y-a)(m_Z-b)
\ge m_Ym_Z-e\,\max(m_Y,m_Z).
$$

Combine with e<=M/t and rearrange. This proves (LOCAL-CRT-INV). QED.

**What is genuinely achieved:** a **density-sensitive positive lower bound** whenever the actual narrow-window inner allowed-distance residue projections omit enough classes across the chosen primes. The formula depends on U, the exact geometry of the outer bins, and explicit moduli; it requires neither a random-spectrum assumption nor any selection of inner block comparisons.

**What is not achieved:** showing that *every* persistent-density configuration has such a prime/modulus family. If e_(p,t)=p for every usable small prime, the residue budget B_t is enormous and the inequality usually says only M>=0. Dense inner forbidden distances by themselves do not guarantee a missing allowed residue modulo any small prime: a relatively sparse zero-weight set can still hit every residue class. The need to prove *unavoidable prime-residue deficiency or another density-cost mechanism at arbitrarily many owned scales* is the remaining open Stage B boundary.

## 4B. Composite-modulus inverse: a stronger, fully elementary theorem

The prime theorem can be strengthened, particularly when the allowed differences cover **every** residue in each small prime projection but not every residue modulo their product.

Fix the same actual ordered B3 outer bins Y<Z and integer threshold t>=1. For *any integer modulus* Q satisfying 1<=Q<=min(D_Y,D_Z), form the actual permitted residue set

$$
E_{Q,t}=\{h\bmod Q:h\in J,\ r_U(h)<t\}.
$$

Define a **finite difference-biclique capacity** depending only on the inner spectrum and candidate interval,

$$
\boxed{
\beta_Q(E)=
\max_{\substack{S,T\subseteq\mathbb Z/Q\mathbb Z\\
T-S\subseteq E}} |S||T|,
}\tag{BICLIQUE}
$$

where empty S or T are allowed, giving a valid maximum of zero when E is empty. For a fixed nonempty S, the largest possible T is the exact intersection of translates

$$
T_{\max}(S)=\bigcap_{s\in S}(s+E).
$$

Thus beta_Q is precisely and reproducibly computable by enumerating the 2^Q residue subsets S for modest Q, without optimizing over unknown actual outer points. Put

$$
\boxed{
B_{Q,t}^{\mathrm{comp}}=
\left(\frac{144D_YD_Z}{Q^2}\right)^{1/3}
\beta_Q(E_{Q,t}).
}\tag{COMPOSITE-BUDGET}
$$

**Theorem E (robust composite-modulus arithmetic inverse):**

$$
\boxed{
\mathcal M_{Y,Z}(U)\ge
\frac{t}{\max(m_Y,m_Z)}
\left[m_Ym_Z-B_{Q,t}^{\mathrm{comp}}\right]_+ .
}\tag{COMPOSITE-INVERSE}
$$

**Proof (elementary; no Cauchy–Davenport needed).** Remove one endpoint of each cross-bin edge with r_U(z-y)>=t, at most M/t deletions. If one bin disappears, the bound follows as in Theorem D. Otherwise the surviving actual B3 subsets Y',Z' have residue supports S=Y' mod Q and T=Z' mod Q satisfying T−S subset E_(Q,t). Hence |S||T|<=beta_Q(E). For either B3 subset X with enclosing diameter D_X>=Q, the cubic-shadow pigeonhole proof gives $|X|^3 Q\le12D_Xt_Q(X)^3$. Multiply the inequalities for Y',Z' and take cube roots to obtain

$$
|Y'||Z'|\le
\left(\frac{144D_YD_Z}{Q^2}\right)^{1/3}
|S||T|\le B_{Q,t}^{\mathrm{comp}}.
$$

As before the product of the surviving bin sizes is at least m_Y m_Z−(M/t) max(m_Y,m_Z). Rearranging proves (COMPOSITE-INVERSE). QED.

**Prime CRT dominance.** When Q is a product of distinct primes p_j, every allowed-biclique pair S,T projects to allowed difference pairs modulo each p_j. The CRT and Cauchy–Davenport upper bounds give

$$
\boxed{\beta_Q(E_{Q,t})\le\prod_j c_{p_j,t}^{\,2}.}\tag{DOMINATES}
$$

Here the prime allowed sets E_(p,t) may be **larger** than the projections of E_(Q,t) if the candidate set is changed; in this theorem all are reductions of the same actual candidate interval J, so containment and the inequality are valid. Therefore Theorem E is at least as strong as Theorem D for the same product modulus.

**Concrete B3-compatible structural witness.** Take an inner B3 block U={1,2,5,14}, and two B3 outer bins Y={100,106}, Z={108,115}. The separate sets are B3; the combined U union Y union Z is **not asserted to be B3**. The candidate positive differences range over J=[2,15]. The actual zero-weight differences of U in J are {10,14,15}, so their residues modulo 6 are {4,2,3}. They cover both residue classes modulo 2 and all three residue classes modulo 3, yet omit three of the six classes modulo 6. Exhaustive residue-subset enumeration gives

$$
\boxed{
\beta_6(\{2,3,4\})=4<36
=\bigl(2\cdot3\bigr)^2.
}\tag{COMPOSITE-STRICT}
$$

The prime CRT upper bound of 36 sees no restriction, whereas the composite biclique bound is 4. This is a **strict improvement in the arithmetic structural certificate**, not a claim of a positive Stage B correlation bound in that particular fixture. The actual cross-bin weight there is 6, so both inequalities hold.

**Open universal step, explicitly:** for the long persistent-density windows in Erdős #41, prove that some Q<=min(D_Y,D_Z) has composite capacity beta_Q(E) small enough to force positive overlap, **or** show that consistently large beta_Q across a growing family of scale-owned windows creates a separately quantified density cost. The present theorem does not show this. An allowed spectrum may have E=all residues for every accessible modulus despite exact B3 avoidance.

## 4C. A genuine B3 finite hostile example: why residue deficiency cannot be presumed

The distinction between an available certificate and a *forced* certificate is essential. The original 29-point genuine B3 fixture contains a robust zero-correlation countercontrol even after considering the complete positive inner pair family.

Let A=(a_0,...,a_28) denote that fixture in increasing order (see the executable test file). Use q=151 and four Sidon pair-type labels (0,11,42,43). Lift the first twelve elements (four disjoint three-point inner groups) by

$$
U'=\{151a_i+e_{\lfloor i/3\rfloor}:0\le i<12\},
\quad W'=\{151a_i:12\le i<29\}.
$$

Because q exceeds three times the largest digit and the original A is B3, the entire lifted U' union W' remains B3. Exact enumeration gives

$$
\boxed{
\mathcal M(U',W')=0
\quad\text{for the COMPLETE unordered inner pair-sum family.}
}\tag{HOSTILE-B3}
$$

Take Y as the first three elements of W' and Z as the next three. Their candidate positive difference interval contains **633,748 integer positions**, although the actual differences of outer W' are multiples of 151. The zero-weight inner differences in that interval represent **every** class modulo each Q in {2,3,6,12}. Hence

$$
\boxed{
E_{Q,1}=\mathbb Z/Q\mathbb Z,\qquad
\beta_Q(E_{Q,1})=Q^2\quad(Q=2,3,6,12).
}\tag{HOSTILE-SURJECTION}
$$

The composite bound is correctly satisfied but uninformative for these moduli. This is a bona fide finite B3 configuration, *not* a hypothetical independent set that fails B2. It excludes any argument assuming that positive finite critical-scale cardinalities, B3 alone, or many popular inner differences automatically create a defect in one of these fixed small residue quotients. It does **not** construct an infinite positive-critical-lower-density B3 sequence or disprove Erdős #41. A successful asymptotic inverse theorem must force **growing/adaptive modulus complexity**, a stronger geometric restriction, or a genuine multiscale accumulation mechanism.

## 4D. Exact critical-density inverse threshold (proved, but not a deficit)

The composite inverse implies an unconditional **quantitative structural alternative** at each fixed density coefficient; unlike an assumed inverse theorem, the statement is an immediate consequence of the proved inequality.

Suppose an actual pair of B3 outer bins Y<Z has

$$
m_Y\ge c_Y D_Y^{1/3},\qquad
m_Z\ge c_Z D_Z^{1/3}
$$

for fixed positive coefficients c_Y,c_Z, and suppose its cross-correlation at all actual differences vanishes. For every modulus Q<=min(D_Y,D_Z), the composite theorem gives

$$
\boxed{
\beta_Q(E_{Q,1})\ge
\frac{c_Yc_Z}{144^{1/3}}\,Q^{2/3}.
}\tag{FORCED-BICLIQUE}
$$

Thus the **allowed actual inner distance residues must contain a complete bipartite difference pattern involving at least order Q^(2/3) ordered pairs of occupied residue positions**. Moreover any nonempty biclique S,T satisfies |S|<=|E| and |T|<=|E| (fix an element of the opposite set, then translate). Hence

$$
\boxed{
|E_{Q,1}|\ge
\left(\frac{c_Yc_Z}{144^{1/3}}\right)^{1/2}Q^{1/3}.
}\tag{FORCED-ALLOWED-RESIDUES}
$$

For small nonzero cross-correlation, the precise quantitative version is

$$
\boxed{
\beta_Q(E_{Q,t})\ge
\left[
m_Ym_Z-\frac{\mathcal M_{Y,Z}(U)}{t}\max(m_Y,m_Z)
\right]_+
\left(\frac{Q^2}{144D_YD_Z}\right)^{1/3}.
}\tag{ROBUST-BICLIQUE}
$$

**Scope:** this is a proved **structure-or-correlation** theorem for every individual actual finite density window. It establishes *necessary growing structural complexity* in residue space when correlations are small. It is not yet a theorem that such complexity is *costly* for critical B3 density across scales: a full allowed residue set E=Z/Q has beta_Q=Q² and satisfies these conditions without strain. The genuine digit-lift hostile fixture above exhibits exactly that escape at fixed small Q. An Erdős #41 proof would have to show that realizing sufficiently many such large bicliques over adaptively growing Q and uniquely owned scales forces a **separate** density decrement. Nothing in (FORCED-BICLIQUE) alone supplies it.

## 5. What was and was not proved about persistent density

Under the **hypothetical** persistent critical bound A(N)>=cN^(1/3), existing GCL selection gives large actual outer cohorts. If a chosen m-element outer B3 subset has m>=kappa_c L^(1/3) in an interval of span L and M=0, Theorem A forces at least kappa_c^3 L/6−O_c(L^(2/3)) distinct nondegenerate additive triangles in the zero-weight distance set. This is a rigorous quantitative *structure-or-correlation* alternative.

**It is not yet the requested 'quantitatively costly' structure theorem.** The general candidate set T_L has order L² possible gap pairs, while binom(m,3) has order L at critical density. A zero-weight spectrum can have ample Schur triangles even when many forbidden distances are popular; the independently proved positive-density inner forbidden spectrum does not force the zero set to have few triangles. Neither CRT deficit nor an accumulating Stage C decrement follows.

The next admissible research lemma is specifically an **arithmetic triangle-scarcity / residue-capacity theorem for real B3 pair-sum spectra**, strong enough to show that avoidance across a sequence of *scale-owned* outer windows forces both (i) near saturation or failure of the THREE-BIN capacities and (ii) a joint residue/gap structural cost incompatible with a fixed density coefficient. No such universal estimate is currently proved; claiming one from interval counts or positive forbidden-edge density would be false reasoning.

This work eliminates the assumption that different outer differences can be placed in allowed positions **independently**. It does not eliminate the possibility that a structured allowed set admits all required triangles at small density.

## 6. Exact replay scope and source context

Tests enumerate complete unordered U pair sums; actual B3 and B2 properties; weighted pairwise and triadic collision energies; all candidate nondegenerate triangles for several short spans; multiple congruence moduli; genuine outer-bin triples; the above hostile non-B2 progression; and cross-check the exact left-side triangle identity. All tests are finite integer-exact assertions.

External status source: https://www.erdosproblems.com/41 (repeated-summand B3; open). Prior GCL research: issue #2622 and research PRs #2696, #2713, #2714. The theorem is mathematical synthesis, not certified novelty.
