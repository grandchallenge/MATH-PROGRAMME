# Figurate tuples: when three numbers cannot coexist

*FIGURATE mathematical guide · 4 November 2026*

**Reading level:** familiar with parity, square numbers and remainders. The examples can be checked with integer arithmetic; a short advanced appendix gives the precise classification.

**Research status:** The congruence arguments below are written as complete elementary proofs and checked by independent exact-integer code. Their admission into GCL research repositories is **not** independent mathematical certification, and their originality in the wider mathematical literature has **not** been established.

## 1. Start with a simple rule

Triangular numbers count dots in triangles:

$$
1,\ 3,\ 6,\ 10,\ 15,\ldots
$$

Square numbers count dots in squares. Octagonal numbers form another sequence:

$$
P_8(t)=3t^2-2t=1,\ 8,\ 21,\ 40,\ 65,\ 96,\ldots
$$

Now choose a fixed integer offset $c$ and ask for **three distinct positive integers** $a,b,d$ satisfying:

$$
ab+c=P_k(r),\qquad
ad+c=P_k(s),\qquad
bd+c=P_k(t).
$$

Each pair must produce a polygonal number of the *same order* $k$. The indices $r,s,t$ are allowed to differ. GCL calls this the **Type B** problem.

The distinction matters. In Type A, the *entries* themselves must be polygonal and the pairwise outputs are *squares*. Type C imposes both entry and polygonal-output restrictions. A conclusion for one type cannot automatically be transferred to the others.

## 2. Pairs are easy. Triples are difficult.

Let the polygonal sequence be fixed. Pick any index $t$ sufficiently large that $P_k(t)-c>1$. Define

$$
a=1,\qquad b=P_k(t)-c.
$$

Then $ab+c=P_k(t)$ exactly. This construction gives **infinitely many compatible Type B pairs for every order and every integer offset**.

But a third number $d$ must make *two new pairwise products* polygonal at once. What is easy for one equation can be impossible for three equations.

**A concrete nonextendible pair:** take octagonal numbers ($k=8$) and $c=2$. Since $P_8(2)=8$, the pair $\{1,6\}$ works: $1\cdot6+2=8$. The question is whether a third positive integer $d$ can satisfy both $d+2=P_8(s)$ and $6d+2=P_8(t)$. The answer is no, for a reason that applies to *every* possible $d$, not just the first million.

## 3. The tool: remainders rather than huge numbers

Instead of examining every possible integer, inspect remainders modulo 8. For any polygonal order divisible by 8, the sequence has exactly three possible remainders:

$$
P_k(t)\pmod8\in\{0,1,5\}.
$$

Why does the order matter only by its remainder? Use the identity

$$
P_k(t)=t+(k-2)\binom{t}{2}.
$$

Because the binomial coefficient is an integer, changing $k$ by a multiple of 8 does not change the value modulo 8. The sequence also repeats modulo 8 after a shift of 16 in the index. We can therefore check **16 small indices**, and that check covers arbitrarily large indices.

For example, at $k=8,c=2$, a putative third entry $d$ would require:

$$
d+2\pmod8\in\{0,1,5\}
$$

and simultaneously

$$
6d+2\pmod8\in\{0,1,5\}.
$$

The first condition leaves only $d\equiv3,6,7\pmod8$. For those three choices, the second expression gives $4,6,4\pmod8$, respectively. None is allowed. **No third entry exists.**

This is a miniature impossibility certificate: eight remainder classes cover every integer, and none satisfies the requirements.

## 4. The larger result: no triple at all

That specific pair is only the beginning. GCL's next argument removes *all restrictions on the entries*.

**Modulus-8 obstruction.** For every order $k$ divisible by 8, and every integer offset satisfying $c\equiv2$ or $6\pmod8$, there cannot be a Type B triple of any three distinct positive integers.

Here is the entire idea in ordinary arithmetic.

All polygonal outputs are congruent to $0,1,$ or $5$ modulo 8. In particular, they are $0$ or $1$ modulo 4. Because the offset is $2$ modulo 4, **each pairwise product must be $2$ or $3$ modulo 4.**

There are only three parity arrangements for three entries:

1. **At least two entries are even.** Their product is divisible by 4, which is forbidden.
2. **All entries are odd.** Every pairwise product must be $3$ modulo 4. Multiplying the three pair products produces $(abd)^2$, a square congruent to $3$ modulo 4. But squares are only $0$ or $1$ modulo 4.
3. **Exactly one entry is even.** Call it $a$. Since $ab$ and $ad$ must be $2$ modulo 4, $a$ is twice an odd number. The two odd entries $b,d$ must be in opposite classes modulo 4 to make $bd\equiv3\pmod4$. Consequently $ab$ and $ad$ differ by $4$ modulo 8. Yet each of $ab+c$ and $ad+c$ is an even polygonal number, and the **only even allowable polygonal remainder modulo 8 is zero**. Both products would have to be congruent to $-c$ modulo 8. They cannot simultaneously differ by 4 and be equal.

All three arrangements fail. The theorem follows. There is no entry bound, no assumed special member, and no reliance on a computer's failure to find an example.

## 5. A sharper lens: modulus 16

If we distinguish sixteen remainders instead of eight, additional impossibilities appear. The current complete **modulus-16 local test** gives the following global obstructions.

| Polygonal order | Forbidden offsets for Type B triples |
| --- | --- |
| $k\equiv0\pmod8$ | $c\equiv2,3,$ or $6\pmod8$ |
| $k\equiv12\pmod{16}$ | $c\equiv2\pmod4$ |

Every listed row rules out **all** Type B triples of distinct positive integers, whatever their size.

The first row includes a new offset class, $3$ modulo 8, absent from the earlier modulus-8 test. The second row catches polygonal orders that the first row misses.

For exact reproducibility, the complete underlying residue table is:

| $k\bmod16$ | Offset remainders $c\bmod16$ giving no local triple |
| --- | --- |
| $0$ or $8$ | $2,3,6,10,11,14$ |
| $12$ | $2,6,10,14$ |
| Every other class | None |

**Important distinction:** “None” in the last row says that the *modulus-16 test* found no contradiction. It does **not** prove that any actual positive-integer triple exists. Another modulus or a global equation might still exclude it.

### A further step: modulus 32

The research next doubled the number of possible remainders, from sixteen to thirty-two. This reveals **two new global impossibility families** that the earlier modulus-16 test cannot detect:

| Polygonal order | Additional offsets that cannot give Type B triples |
| --- | --- |
| $k\equiv0\pmod{16}$ | $c\equiv5\pmod{16}$ |
| $k\equiv8\pmod{16}$ | $c\equiv9\pmod{16}$ |

For example, if $k=16$ and $c=5$, or if $k=8$ and $c=9$, there is no Type B triple of *any* size. Nevertheless, choosing $a=1$ and $b=P_k(t)-c$ still produces infinitely many actual compatible pairs. The obstruction concerns making **three** pairwise conditions true simultaneously.

**Why does doubling the modulus matter?** Modulo 16, certain potential pair products look indistinguishable. Modulo 32 they split into finer remainder classes. In these two families every permitted pair product has an odd remainder of $3$ modulo 4 or an even remainder of $8$ or $12$ modulo 16. Among even permitted products divisible by 8 but not 16, only **one remainder class modulo 32** is allowed. A parity case analysis shows any putative triple would force two such products to differ by 16 modulo 32—an impossibility.

The full [mathematical proof](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_MOD32_GLOBAL_OBSTRUCTIONS_004.md) examines all possibilities for how many entries are even, including cases where all three are even. The accompanying exact-integer check tests $\binom{34}{3}=5984$ unordered entry-remainder triples for each of $32\times32=1024$ order-and-offset classes. It includes repeated residues, because distinct integers can still have the same remainder.

The **complete modulo-32** test excludes the classes already listed in the modulus-16 table, plus exactly the two new offset families above. In every nonexcluded cell the checker supplies an explicit *local remainder witness*. Such a witness is not the same thing as an actual positive-integer Diophantine triple.

### A structural result: when every binary remainder is attainable

The successive tables suggest an important question: *why do the forbidden cases always have polygonal orders divisible by four?*

There is a precise answer, not just a pattern in the data.

**Binary surjectivity theorem.** The polygonal sequence $P_k(t)$ attains **every** remainder modulo $2^n$, for **every** $n\ge1$, **if and only if** the polygonal order $k$ is *not divisible by four*.

Here is the mechanism. For any index increment $H$,

$$
P_k(t+H)-P_k(t)
=\frac H2\bigl((k-2)(2t+H)-(k-4)\bigr).
$$

Start with an index representing the desired last binary digit. If $k$ is odd, adding $2^{n+1}$ to that index **flips exactly the next bit** of the polygonal remainder modulo $2^{n+1}$, while preserving the lower $n$ bits. If $k\equiv2\pmod4$, adding $2^n$ does the same job. Choosing to add the increment or not at each stage constructs a polygonal number with **any** specified binary remainder, however many bits it has.

Conversely, when $k$ is divisible by four, polygonal numbers can only be $0$ or $1$ modulo $4$. The remainders $2$ and $3$ are unavailable, so the universal statement fails immediately.

For a tangible calculation, suppose the target is remainder $317$ modulo $512$. The exact index-construction algorithm gives $P_3(361)\equiv317\pmod{512}$ for triangular numbers, and $P_6(181)\equiv317\pmod{512}$ for hexagonal numbers. Both were produced by the binary-lifting rule, not by searching for a lucky index.

**What does this mean for triples?** For an order $k$ not divisible by four, no test using **only one power-of-two modulus** can rule out all Type B triples: choose all three *entry remainders* to be zero, and the theorem supplies a polygonal output congruent to the offset. Repeated remainders are permissible because distinct positive entries can all be divisible by the modulus. This says the *local remainders* are compatible, **not** that a genuine triple satisfying the original integer equations exists.

This is a structural limitation on a whole family of obstruction methods, not merely one more negative search result.

### A further refinement: modulus 64

The complementary search at modulus 64 identifies **four additional global impossibility families**, beyond the preceding modulus-32 table:

| Polygonal order | Additional offsets with no Type B triple |
| --- | --- |
| $k\equiv0\pmod{32}$ | $c\equiv9\pmod{32}$ |
| $k\equiv16\pmod{32}$ | $c\equiv25\pmod{32}$ |
| $k\equiv8\pmod{16}$ | $c\equiv13\pmod{32}$ |
| $k\equiv12\pmod{16}$ | $c\equiv4\pmod{16}$ |

These are unbounded nonexistence statements because every integer triple must project into a residue triple modulo 64. The exact certificate checks all 64 order residues and 64 offset residues, admits repeated entry classes, and independently reproduces the **first local witness** in every nonexcluded cell. The four listed families have a complete **finite modular certificate**; they are not claimed to have a separate short analytic proof or to be novel in the literature.

The [structural proof, complete modulus-64 table, executable index builder and independent tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_2ADIC_SURJECTIVITY_MOD64_006.md) preserve the full hypotheses and validation record.

### A complete square test for orders divisible by four

There is a complementary theorem for the other polygonal orders. Suppose $k$ is divisible by four and put

$$
A=\frac{k}{2}-1,\qquad q=\frac{k}{4}-1.
$$

Here $A$ is odd. Completing the square gives the *exact identity*

$$
A P_k(t)+q^2=(At-q)^2.
$$

Because $A$ is invertible modulo every power of two, the polygonal values modulo $2^n$ are **exactly** the residues $z$ for which $Az+q^2$ is a square modulo $2^n$. This is a two-way criterion, not merely a quick way to reject candidates.

For example, for octagonal numbers ($k=8$), we have $A=3$ and $q=1$. Thus a number $z$ is *locally octagonal* modulo $2^n$ precisely when $3z+1$ is a square modulo $2^n$. The actual octagonal value $z=21$ gives $3\cdot21+1=64=8^2$. But satisfying the criterion modulo a fixed power of two does not mean a particular integer is globally octagonal; the positive integer index condition still matters.

**Why is this useful?** Every integer square has an even power-of-two valuation until it vanishes modulo the chosen power. After removing that even power, an odd square must equal $1$ modulo $8$ when at least three binary digits remain. Therefore the apparently complicated polygonal residue question becomes a very specific test of the valuation and low three bits of $Az+q^2$.

For a Type B triple, apply this test separately to

$$
A(ab+c)+q^2,\quad A(ad+c)+q^2,\quad A(bd+c)+q^2.
$$

All three must be squares *modulo the same power of two*. This reframes the whole binary obstruction hierarchy as a simultaneous square-residue problem and explains why finer moduli detect contradictions missed by coarser ones.

This completed-square identity is **classical**, including its standard polygonal discriminant form; see [Wolfram MathWorld](https://mathworld.wolfram.com/PolygonalNumber.html) and the [GCL proof-and-test dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_2ADIC_SQUARE_NORMAL_FORM_007.md). The contribution here is its explicit use as a complete all-exponents local test in the FIGURATE Type B programme, not an assertion that the identity has newly been discovered.

### Exactly one-sixth of offsets escape every binary obstruction test

The completed-square method has a further, quantitative consequence. For a polygonal order divisible by four, the proportion of possible polygonal output remainders modulo larger and larger powers of two tends to **one-sixth**. This limit is the same for square numbers, octagonal numbers, and every polygonal order divisible by four.

More precisely, let $N(n)$ count the distinct polygonal output remainders modulo $2^n$. Then $N(n)=(2^n+8)/6$ if $n$ is even, and $N(n)=(2^n+10)/6$ if $n$ is odd. The count comes from the classical formula for quadratic residues modulo powers of two, via the invertible affine square normal form. These exact counts and their recurrence are documented in the [WP08 density and coherence proof](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_2ADIC_DENSITY_COHERENCE_008.md); the classical square-count source is [Stangl, *Counting Squares in Z_n* (1996)](https://www.jstor.org/stable/2690536).

There is a stronger observation than simply obtaining some compatible remainders. Suppose $k$ is divisible by four, set $A=k/2-1$, $q=k/4-1$, and let $D=Ac+q^2$. If this *transformed offset* is a square in the 2-adic integers, it is possible to choose **one fixed triple of distinct positive integers** whose three pairwise outputs pass the polygonal congruence test modulo **every** power of two, with the entries never changing.

Here is an explicit example. For octagonal numbers take $k=8$ and offset $c=-8$. Then $A=3$, $q=1$, and $D=-23$. Although negative, $-23$ is a 2-adic square, because it is an odd number congruent to $1$ modulo $8$. The fixed triple $(4,8,16)$ has shifted pair products $24,56,120$. Each is a legitimate octagonal *remainder* modulo every $2^n$, but this does **not** mean that $24,56,120$ are all ordinary octagonal integers.

Why does a fixed triple work? If the transformed offset has the form $D=2^{2j}u$ with $u$ odd and congruent to $1$ modulo $8$, choose entries $2^{j+2}$, $2^{j+3}$ and $2^{j+4}$. Their pair products are divisible by sufficiently high powers of two that adding them changes none of the valuation or low odd-unit bits that make $D$ a 2-adic square. Hence all three transformed outputs remain 2-adic squares simultaneously, at all binary precisions.

**Interpretation:** for exactly one-sixth of integer offsets (in the natural-density sense), this construction is available when $k$ is divisible by four. Such offsets are immune to *purely power-of-two congruence nonexistence arguments*. The complementary five-sixths are **not automatically impossible**; another argument would be needed to establish an obstruction. No claim about actual integer Type B triple existence follows from the local construction.

### Which polygonal orders admit *every* offset locally?

The earlier one-sixth density is a useful sufficient test for individual offsets, but it does not exhaust all the ways a Type B triple can be compatible in 2-adic arithmetic. The next result completely classifies **orders for which every integer offset works locally**.

**Uniform binary admissibility theorem.** For every polygonal order $k\ge3$, and every integer offset $c$, a *single fixed triple of distinct positive integers* can be found whose three shifted pair products are polygonal residues modulo **every** power $2^n$ if and only if

$$
4\nmid k\quad\text{or}\quad k\equiv4\pmod{16}.
$$

For $4\nmid k$, the already-proved binary surjectivity means that the fixed entries $(1,2,3)$ always pass every local test. For $k\equiv4\pmod{16}$, something different happens: the completed-square coefficient $A=k/2-1$ is $1$ modulo $8$, so it has a square root in the 2-adic integers. The classical Euler pair-to-triple identity then provides a *formal* 2-adic triple; approximating its entries sufficiently accurately by ordinary positive integers preserves all three nonzero square conditions at every binary precision.

**Worked example:** choose $k=20,c=2$. The previous offset test fails because $D=9\cdot2+4^2=34$ is not a 2-adic square. Nevertheless, the new construction produces the fixed entries $(1,242,375)$. Their shifted pair products are $244$, $377$, and $90752$. All three are **20-gonal residues modulo every power of two**, but this says nothing about their being actual 20-gonal integers.

The reverse direction is equally concrete. If $k$ is divisible by eight, the offset $c=2$ is impossible for Type B triples already modulo eight. If $k\equiv12\pmod{16}$, that same offset is impossible modulo sixteen: the only allowed pair-product remainders are $7,10,14,15$, and their parity relations cannot be satisfied by a triple. These are exactly the order classes omitted by the displayed theorem.

**What is classified?** The theorem answers the question “Does *every offset* have a fixed triple passing all binary congruence tests?” It does **not** establish that every individual offset outside those classes is forbidden, nor does it prove the existence of actual integer Diophantine triples. The proof, positive-integer constructor, and independent converse tests are in the [WP08 uniform 2-adic admissibility dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_UNIFORM_2ADIC_ADMISSIBILITY_009.md).

## 6. How the finite certificate proves an infinite statement

Think of each integer as a box labeled by its remainder modulo 16. Although there are infinitely many integers, there are only 16 box labels. A possible triple lands in some **unordered triple of boxes**, and the labels may repeat even though the integers themselves must be distinct.

The exact checker does this:

1. Compute all allowed polygonal output remainders for the specified order.
2. Enumerate every unordered triple of entry remainders, *allowing repetitions*.
3. Check whether the three shifted products are all allowed remainders.
4. If every triple fails, conclude that no real integer triple can exist.

There are $\binom{16+3-1}{3}=816$ such remainder triples. Repeating the analysis for all 16 order classes and 16 offset classes yields the table above.

The [independent test suite](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp08_mod16_classification.py) reproduces this complete table using a separate direct arithmetic formula. It checks nonempty control cases, checks the periodicity in polygonal order, and verifies that compatible pairs themselves really exist.

The computer is not **guessing** that large triples are absent. It exhausts an exact finite list that every hypothetical large triple would have to pass.

### WP09: binary compatibility is not enough

The previous theorem supplies a triple of **fixed positive integers** whose pairwise outputs pass every power-of-two test. Does that mean they are actual polygonal numbers? **No.** The next research package identifies exactly where another prime can intervene.

Consider 20-gonal numbers:

$$
P_{20}(t)=9t^2-8t.
$$

Fix the three distinct positive integers $(1,242,375)$ and choose an offset from the infinite family

$$
c=2+640m,\qquad m\in\mathbb Z.
$$

For $m=0$, the three pair products plus the offset are $244$, $377$, and $90{,}752$. The completed-square test transforms them into $2212$, $3409$, and $816784$, respectively:

| Transformed value | Power of two extracted | Remaining odd number modulo 8 |
| --- | --- | --- |
| $2212$ | $2^2$ | 1 |
| $3409$ | $2^0$ | 1 |
| $816784$ | $2^4$ | 1 |

These are **2-adic squares**, since their powers of two are even and their remaining odd factors are $1$ modulo $8$. When $m$ changes by one, each transformed output changes by $5760=2^7\cdot45$, too high a binary power to alter any of these square tests. So **the same fixed triple works modulo every power of two for every integer $m$**, including negative values.

Now examine remainders modulo **five**, a completely different prime:

$$
P_{20}(t)\bmod5\in\{0,1,2\}.
$$

But the first pair output is always

$$
1\cdot242+c=244+640m\equiv4\pmod5.
$$

Four is not a possible 20-gonal remainder modulo five. Therefore **this particular triple is never an exact Type B integer triple** for any offset in the family, regardless of how thoroughly it passes binary tests.

The distinction is essential: *we have excluded the specified triple, not every possible triple at the same polygonal order and offset*. This result establishes an infinite family of **fixed-witness local-to-global failures**, not a global nonexistence theorem. The [WP09 proof, exact calculator and independent tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_ODD_PRIME_SEPARATION_001.md) preserve that narrower, rigorous conclusion.

[WP09's ongoing research tracker](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3145) now targets exact integer Type B constructions and simultaneous constraints from odd primes and powers of two. The earlier source-fidelity issue WP05 remains separate.

### WP09: an odd-prime-power obstruction that rules out *every* triple

The previous WP09 example showed that a *particular* triple can pass every binary test but fail modulo five. A stronger question is whether an odd modulus can rule out **all possible triples**, without specifying their entries.

The answer is yes. **For every polygonal order $k$ divisible by three, and every offset $c$ congruent to 4 or 7 modulo nine, no Type B triple exists.** The conclusion applies to arbitrarily large positive integers.

Why nine instead of three? For any $k$ divisible by three, the polygonal sequence has exactly the residues

\`\`\`text
0, 1, 3, 6  (modulo 9)
\`\`\`

If the offset is 4 modulo nine, every pair product must be one of $2,5,6,8$ modulo nine. If the offset is 7 modulo nine, the allowed products are $2,3,5,8$. Both lists have two remarkable properties: **no allowed product is 1 modulo three**, and **only one allowed product is divisible by three**.

Now imagine three entries:

1. If at least two are divisible by three, their product is zero modulo nine, which is not on either list.
2. If none is divisible by three, all three pair products would have to be 2 modulo three. Multiplying them produces the square of the product of the three entries, but that square would be 2 modulo three—impossible.
3. If exactly one is divisible by three, its two products force the remaining two entries to have the **same** nonzero remainder modulo three. Their mutual product must then be 1 modulo three, again forbidden.

These cases exhaust the possibilities, so no triple can exist.

For example, triangular numbers ($k=3$) with offset $c=4$ admit many **compatible pairs** such as $\{1,P_3(t)-4\}$ for sufficiently large $t$, but **none can ever be extended to a Type B triple**. This is a global impossibility proof, not a bounded computer search.

The [WP09 full mathematical proof and independent modulus-nine certificate](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_GLOBAL_MOD9_OBSTRUCTIONS_002.md) also shows that the weaker modulus-three test misses these contradictions entirely. This conclusion is new to the GCL research programme; it is **not** asserted original in the wider mathematical literature or externally certified.

## 7. What is established—and what is not

**Established by the displayed arithmetic:** the specific global nonexistence statements under the stated congruence hypotheses. The argument applies to infinitely many polygonal orders and offsets, not just the bounded surveys.

**Established computationally:** the complete local exclusion tables modulo 8, 16, 32 and 64, with independently repeated exact-integer tests. The two additional modulo-32 nonexistence families also have a direct elementary 2-adic proof.

**Not established:** novelty relative to the entire literature, independent specialist certification, or a global classification of all polygonal Type B triples. Results for Type A and Type C require their own hypotheses. The still-open source review of one 2025 *Mathematica Slovaca* paper remains a separate documentary obligation.

The progression matters: the initial [bounded census](FIGURATE_CENSUS.md) reported what happened below a numerical cutoff; the [pilot overview](FIGURATE_PILOT_001.md) introduced the questions; the present page explains **why certain entire infinite families cannot exist**, using proofs rather than negative search results.

## 8. Primary GCL research record

The public pedagogical exposition is deliberately separate from the versioned evidence:

- [WP08 modulus-8 proof and classification](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_GLOBAL_TRIPLE_OBSTRUCTION_002.md)
- [WP08 modulus-16 proof and classification](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_MOD16_GLOBAL_OBSTRUCTIONS_003.md)
- [WP08 modulus-32 global obstruction proof and classification](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_MOD32_GLOBAL_OBSTRUCTIONS_004.md)
- [WP08 binary-surjectivity theorem and modulus-64 full certificate](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_2ADIC_SURJECTIVITY_MOD64_006.md)
- [WP08 complete 2-adic square normal form, proof and independent tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_2ADIC_SQUARE_NORMAL_FORM_007.md)
- [WP08 one-sixth 2-adic offset density and fixed coherent local triples](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_2ADIC_DENSITY_COHERENCE_008.md)
- [WP08 complete all-offset 2-adic order classification, proof and tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_UNIFORM_2ADIC_ADMISSIBILITY_009.md)
- [WP09 infinite binary-versus-odd-prime separation, proof and tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_ODD_PRIME_SEPARATION_001.md)
- [WP09 global all-triples modulo-nine obstruction and exact verification](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_GLOBAL_MOD9_OBSTRUCTIONS_002.md)
- [Exact modulo-32 certificate and independently checked witnesses](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp08_mod32.py)
- [Exact modulus-16 classifier](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp08_mod16_classification.py)
- [Source-critical bibliography](FIGURATE_SOURCES.md)
- [Active successor WP09](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3145)

**Publication status:** an internally admitted mathematical exposition, not a peer-reviewed article, a public mathematical certification, or a claim of priority.
