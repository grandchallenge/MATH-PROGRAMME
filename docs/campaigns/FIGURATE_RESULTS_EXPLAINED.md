# Figurate tuples: existence, obstruction and global arithmetic

*FIGURATE mathematical guide · originally 4 November 2026; research synthesis updated 10 November 2026*

**Reading level:** familiar with parity, square numbers and remainders for the early sections; the later Pell and ideal-class analysis is more technical. The worked examples can be checked with integer arithmetic; the advanced results give **partial classifications in explicitly stated families**, not an unrestricted Type B classification.

**Research status:** The congruence arguments below are written as complete elementary proofs and checked by independent exact-integer code. Their admission into GCL research repositories is **not** independent mathematical certification, and their originality in the wider mathematical literature has **not** been established.

## The research objective: from congruence tests to integer existence

**End-game.** Given a polygonal order and an offset, explain when **distinct positive-integer tuples really exist**, when they are impossible, and which arithmetic principle separates these outcomes. The current main research track is Type B; Types A and C require different hypotheses. A classification for all parameters and all types is **not** a completed result.

The results below follow five mathematical stages, not just a succession of calculations:

1. **Local obstructions (WP08 and early WP09):** test the polygonal conditions modulo powers of two and odd primes. Some congruence classes are ruled out for *all* integer triples, but passing every tested modulus is not an existence proof.
2. **Exact global constructions:** for stated families, find actual positive integers and positive polygonal indices. Pell recurrences can turn one rigorously verified seed into infinitely many triples.
3. **Ideal-class interpretation (WP09-027 and WP09-028):** in the recurring anchor $k=16m+4$ with offset $c=2$, identify the exact ideal-norm and **oriented ray-class** condition behind the constrained Pell equation; retain the nonmaximal order when its conductor is nontrivial.
4. **Compute the obstruction (WP09-029 through WP09-031):** determine the ray kernel, complete narrow Picard group and, for the infinite odd square-conductor subfamily, **the entire oriented ray-class group**, including invariant factors.
5. **Resolve realization (proved for specified infinite families; otherwise open):** show when an ideal of the prescribed norm **occupies the required ray class**. WP09-032 and WP09-033 now give explicit sufficient constructions for powers of three and for mixed 3/5/7 conductors, respectively. A general classification and genuine global-obstruction theorem remain open; a computed group alone does not produce an ideal of a prescribed norm.

For the anchor, the outstanding mathematical decision can be written schematically as:

$$
\exists\,\mathfrak a:\quad
N(\mathfrak a)=n_m,\qquad
[\mathfrak a]_{\mathrm{ray}}=[\rho_m]_{\mathrm{ray}},
$$

with $n_m$, $\rho_m$ and the **actual** ray modulus defined by the [anchored ideal criterion](https://github.com/grandchallenge/MATHSOLVE/pull/1224) and [exact norm-ideal enumeration](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_IDEAL_RAY_ENUMERATION_028.md). The criterion already supports exact case-by-case decisions under its finite-enumeration conditions. **What remains is a uniform theorem** proving which parameter families satisfy it.

**Next research priority:** generalize the proved target-ray realization beyond 3/5/7-supported conductors by analyzing the prime-adic unit-lift condition and its possible obstructions, or prove a genuine globally obstructed family that is nonetheless everywhere locally compatible. Extend to other conductors only when it advances a concrete existence/nonexistence theorem. The longer goal includes separate Types A and C theories.

**Status distinction:** the linked proof dossiers and executable checks are internally admitted mathematical work. They do not establish the universal Type B local-to-global principle, exhaustive literature originality, or independent MATHCERT certification. The [programme overview](FIGURATE_PILOT_001.md) and [active WP09 tracker](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3145) preserve the wider scope and outstanding obligations.

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

### WP09: why modulo 25 can exclude triples that modulo five cannot

The modulo-nine result is not an isolated phenomenon. A new, exact **modulo-25 certificate** detects further infinite families where the weaker modulo-five test admits compatible residues.

For Type B, take a polygonal order $k\ge3$ and any integer offset $c$. **No triple of distinct positive integers exists** under either of these conditions:

- $k\equiv1\pmod5$, $c\equiv3\pmod5$, and $c\not\equiv k-3\pmod{25}$.
- $k\equiv3\pmod5$, $c\equiv3\pmod5$, and $c\not\equiv k\pmod{25}$.

To see what is different, use triangular numbers, with $k=3$. At offset $c=8$, the modulo-five test has compatible triples of entry remainders, but **none of the 25 possible entry residues for each of three entries** can satisfy all three polygonal-output requirements modulo 25 simultaneously. Therefore no integer Type B triple exists, no matter how large the entries. Offset $c=3$, by contrast, remains *locally compatible* modulo 25; this does not prove an actual triple exists.

The exact checker calculates all polygonal residues modulo 25 and checks all possible ordered entry-residue triples, **allowing repeated residues** because distinct integers may have equal remainders. Across 625 order/offset cells, exactly 40 are excluded; the corresponding modulo-five table has no excluded parameter classes. An independent arithmetic checker reconstructs the same table from the direct quadratic polygonal formula. These finite certificates prove an unbounded integer nonexistence theorem, not a negative search up to some entry cutoff.

See the [WP09 modulo-25 proof dossier, reproducible classifier, and tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_MOD25_GLOBAL_OBSTRUCTIONS_003.md). The result is internally proved and source-admitted; independent mathematical certification and literature novelty remain open.

### WP09: one theorem for every odd prime

The earlier modulo-nine, modulo-25 and modulo-49 examples have a common cause. We can now state it as **one structural theorem for every odd prime**, without enumerating cases individually.

For a polygonal order $k\ge3$ and an integer offset $c$, fix an odd prime $p$ that does not divide $k-2$. Suppose $(k-2)/2$ is a **quadratic nonresidue** modulo $p$: it is not the remainder of a nonzero square. If

$$
p\mid 8(k-2)c+(k-4)^2
$$

but

$$
p^2\nmid 8(k-2)c+(k-4)^2,
$$

then **there cannot be three distinct positive integer entries whose pairwise shifted products are all polygonal numbers of order $k$**. This conclusion holds regardless of how large the entries might be.

The reason is geometric arithmetic: completing the square gives

$$
P_k(t)=A(t-h)^2+B,
$$

where $A=(k-2)/2$ and $B=-(k-4)^2/[8(k-2)]$. Under the stated offset condition, each hypothetical pair would satisfy

$$
xy+pu=Az^2\pmod{p^2}
$$

for an invertible $u$ modulo $p$.

If none of the three entries is divisible by $p$, all three pair products would have to be quadratic nonresidues, but their product is itself a square. If two entries are divisible by $p$, their mutual pair output has exactly one factor of $p$, impossible for a square modulo $p^2$. If exactly one entry is divisible by $p$, the other two must be congruent modulo $p$, forcing their mutual product to be a square when a nonresidue is required. All cases contradict the pair equations.

**Example beyond the earlier prime tables:** triangular outputs have $k=3$. For the offset $c=26$, the expression $8c+1=209=11\cdot19$ has exactly one factor of 11. Because the inverse of 2 is a nonresidue modulo 11, the theorem rules out **every** triangular-output Type B triple at offset 26. Modulo nine and modulo 25 do not produce this exclusion.

For each odd prime $p$, the theorem excludes exactly $p(p-1)^2/2$ periodic order-and-offset residue classes modulo $p^2$. This formula recovers 6 cells for $p=3$, 40 for $p=5$, and 126 for $p=7$, and supplies new families for $p=11,13$ and every other qualifying odd prime.

The [full uniform-prime-square proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_UNIFORM_ODD_PRIME_SQUARE_005.md), [executable theorem checker](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_uniform_prime_square.py), and [independent tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_uniform_prime_square.py) are protected-admitted research artifacts. This is a **sufficient obstruction theorem**, not a complete classification at arbitrary primes and not a claim that any surviving local class contains an exact integer triple. Literature originality and independent MATHCERT certification remain open.

### WP09: a complete rule for all odd prime powers

The preceding prime-square theorem gave sufficient conditions for a triple to be impossible. A further theorem now supplies the **complete answer for every odd-prime-power congruence test**. We no longer need a new residue table each time the prime or exponent increases.

For polygonal order $k\ge3$, integer offset $c$, any odd prime $p$, and any integer $n\ge1$, define

$$
\Delta=8(k-2)c+(k-4)^2.
$$

There is **no compatible Type B triple modulo $p^n$ if and only if** the following all hold: $p$ does not divide $k-2$; the number $(k-2)/2$ is a quadratic nonresidue modulo $p$; and the number of factors of $p$ in $\Delta$ is **odd and less than $n$**.

The theorem is stronger in two ways. First, these conditions are necessary **and** sufficient for the absence of *any* locally compatible triple. Second, whenever they fail, a constructive arithmetic algorithm finds an entry remainder $x$ and an index remainder $t$ with

$$
x^2+c\equiv P_k(t)\pmod{p^n}.
$$

Choose the three entry remainders to equal $x$; positive distinct integer representatives $x+p^n$, $x+2p^n$, and $x+3p^n$ then satisfy **all three pairwise congruences simultaneously**. This is still **not** an exact integer Type B solution: it proves congruence compatibility only.

**Why does valuation parity matter?** A quadratic nonresidue coefficient cannot turn an odd power of $p$ into a square. The proof considers the valuations of all three pair products. If none reaches the discriminant valuation, the product of three nonsquare leading factors would be a square—impossible. If two reach it, the required cancellation forces the remaining pair to have a square leading factor, also impossible. In the compatible cases, finite-field squares and a one-digit-at-a-time lifting construction produce the required index.

**Worked higher-power example:** for triangular numbers ($k=3$) at offset $c=64$, the discriminant is $8c+1=513=3^3\cdot19$. The three congruences remain compatible modulo $3^3=27$ but are **impossible modulo $3^4=81$**. The first obstruction can therefore appear beyond the prime-square level.

Complete internal tests classified all 6,561 order–offset cells modulo 81 and excluded 540. Independent tests also compared full three-entry residue searches against the theorem for smaller odd prime powers.

The [WP09 complete theorem and proof](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_ALL_ODD_PRIME_POWERS_COMPLETE_006.md), [constructive calculator](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_odd_prime_power_complete.py), and [independent tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_odd_prime_power_complete.py) are in the protected research record. The theorem does not classify powers of two, exact integer solutions, or mathematical novelty in the prior literature.

### WP09: from local congruences to exact integer triples

The earlier FIGURATE work established complete odd-prime-power congruence criteria and a separate binary theory. **For any specified finite modulus**, we can now combine these prime-power results using the Chinese remainder theorem. It joins the three entry remainders *and* the three polygonal index remainders, with a binary index-period correction where necessary. A compatible result proves only that the equations hold modulo that number; it does not prove the three integer outputs are exactly polygonal.

There is, however, a stronger **exact integer construction** in a case already central to WP08.

For order 20 and offset 2, the triple of **distinct positive integers**

$$
(a,b,d)=(1,18,13375)
$$

has the three pair outputs

$$
ab+2=20=P_{20}(2),
$$

$$
ad+2=13377=P_{20}(39),
$$

$$
bd+2=240752=P_{20}(164).
$$

All three are exact equalities in ordinary integers. This is different from the earlier $(1,242,375)$ example, which passes all binary congruence tests but does not satisfy the exact Type B equations.

In fact, the new triple belongs to an **infinite family** with $a=1$ and $b=18$. Writing the remaining entry as $d=P_{20}(s)-2$, the last pair equation becomes

$$
P_{20}(t)=18P_{20}(s)-34.
$$

Set $S=9s-4$ and $T=9t-4$. Completing the square turns the equation into the generalized Pell equation

$$
T^2-18S^2=-578.
$$

The solution $(S,T)=(347,1472)$ gives the displayed triple. The recurrence

$$
T'=17T+72S,\qquad S'=4T+17S
$$

preserves the Pell equation. Applying it **18 times per family step** also preserves the required index congruences modulo 9, so each step creates a larger exact positive-integer 20-gonal Type B triple. This proves infinitely many actual solutions for the parameter pair $(k,c)=(20,2)$.

There is also a classical family at order 4: for **every integer offset** $c$, take a sufficiently large positive integer $t$ and set

$$
(a,b,d)=(1,t^2-c,(t+1)^2-c).
$$

The pair outputs are exactly $t^2$, $(t+1)^2$, and $(t(t+1)-c)^2$. This is the classical Euler regular construction, not an originality claim.

The [complete arithmetic dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_CRT_AND_EXACT_PELL_007.md) and [executable constructor](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_crt_exact_families.py) distinguish finite modular witnesses from exact integer identities. Independent arithmetic replay compared 684 complete small-modulus parameter cases with a separate all-entry search, checked 20 mixed-prime-power CRT examples, and verified 23 exact integer constructions. This does **not** establish that every everywhere-locally-compatible order and offset has an exact Type B triple. Literature novelty and independent mathematical certification remain open.

### WP09: when one exact solution becomes infinitely many

FIGURATE now has a **general theorem about exact integer solutions**, not simply another modular obstruction. Suppose a genuine Type B triple has entries $(1,b,d)$ with $b>1$ a **nonsquare integer**. Then there are infinitely many genuine Type B triples with the same first two entries $(1,b)$, the same polygonal order, and the same offset.

Write $P_k(n)$ for the polygonal formula and let $b=P_k(r)-c$, $d=P_k(s)-c$. The remaining exact equation is

$$
P_k(t)=bP_k(s)-(b-1)c.
$$

With $R=2(k-2)$, $L=k-4$, $S=Rs-L$, and $T=Rt-L$, the equation becomes

$$
T^2-bS^2=-(b-1)\bigl(8(k-2)c+(k-4)^2\bigr).
$$

This is a generalized Pell equation. Since $b$ is nonsquare, a norm-one Pell unit generates larger and larger solutions. By taking a suitable positive power of that unit, the transformed indices retain the required congruences modulo $R$, making the new indices positive integers. The resulting triples satisfy all three **exact polygonal equations**.

We can apply this to different polygonal orders, using verified starting triples:

| Order | Offset | Exact starting entries | Exact pair-output indices |
| --- | ---: | --- | --- |
| 5 (pentagonal) | 2 | $(1,3,3430)$ | $(2,48,83)$ |
| 6 (hexagonal) | 2 | $(1,13,43)$ | $(3,5,17)$ |
| 20 | 2 | $(1,18,13375)$ | $(2,39,164)$ |

For example, the next pentagonal member after $(1,3,3430)$ is $(1,3,25051687815)$, with indices $(2,129233,223838)$. Each of its three shifted pair products is **exactly** a pentagonal number.

There is a complementary **finite-extension theorem**. When the fixed second entry is a perfect square $b=h^2>1$, and $8(k-2)c+(k-4)^2$ is nonzero, the Pell equation instead factors into two integer terms:

$$
(T-hS)(T+hS)=-(b-1)\bigl(8(k-2)c+(k-4)^2\bigr).
$$

A fixed nonzero integer has only finitely many divisor pairs. Therefore there are only finitely many exact Type B extensions with that fixed first pair $(1,b)$. For example, at square order $k=4$ and offset $c=5$, the pair $(1,4)$ has the exact extension $(1,4,11)$ with indices $(3,4,7)$; its fixed-pair extensions are finite. The special zero-discriminant case is excluded from this finite assertion.

This is a **Pell-versus-split dichotomy**. It tells us when an actual fixed-pair seed forces infinitely many solutions, and when fixed-pair extensions are finite. It does **not** tell us whether an arbitrary locally admissible parameter pair has its first exact solution.

The full [proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_PELL_AMPLIFICATION_DICHOTOMY_008.md), [Pell recurrence and divisor-enumeration source](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_general_pell_amplification.py), and [independent mathematical tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_general_pell_amplification.py) preserve the proofs and exact identities. The result uses classical Pell arithmetic; priority in the published literature and independent mathematical certification remain open.

### WP09: an exact solution for every polygonal-minus-one offset

The earlier Pell theorem showed how to turn **one genuine exact tuple** into infinitely many. We now have a stronger existence result that works for **every polygonal order**, without first searching for an integer seed.

**Global seed-existence theorem.** For every order $k\ge3$ and every positive integer $u$, set the offset $c=P_k(u)-1$. Then there are infinitely many actual triples of distinct positive integers $(a,b,d)$ whose three shifted pair products are exactly polygonal numbers of order $k$ at positive indices. In fact, except when $(k,u)=(4,1)$, infinitely many different fixed nonsquare second entries $b$ each support infinitely many such triples.

**The construction.** Choose an index $r$ for which $b=P_k(r)-c>1$ is nonsquare. The temporary expressions $(1,b,1)$ satisfy all three exact polygonal-output identities because $1+c=P_k(u)$ and $b+c=P_k(r)$. But this **is not a Type B triple**: its first and third entries are the same. The key is to use its polygonal indices as a starting point of a generalized Pell equation. A suitable positive power of a norm-one Pell unit preserves the integer index congruences while making the third entry larger and distinct. All three resulting pair equations are exact identities, not just congruences.

Why can we always choose such a nonsquare $b$? The quadratic polynomial $P_k(r)-P_k(u)+1$ cannot be a square for all sufficiently large integers $r$, unless $(k,u)=(4,1)$. Otherwise its integer square-root differences would eventually be constant, forcing a polynomial-square identity that is possible only for that one exception. In the exceptional square-order case, $c=0$ and $(1,r^2,s^2)$ directly supplies infinitely many exact square-output triples.

**Examples, verified in ordinary integer arithmetic:**

| Polygonal order | Offset | Exact entries | Exact indices |
| --- | ---: | --- | --- |
| 3 (triangular) | 0 | $(1,3,210)$ | $(2,20,35)$ |
| 4 (square) | 0 | $(1,4,9)$ | $(2,3,6)$ |
| 7 (heptagonal) | 6 | $(1,12,28051219)$ | $(3,3350,11604)$ |

For the heptagonal example, the pair outputs are exactly $18=P_7(3)$, $28051225=P_7(3350)$, and $336614634=P_7(11604)$.

This is a **global existence result for an infinite family of offsets at every order**, rather than a local-modulus test. It does **not** show that all locally compatible offsets have an exact solution, nor claim that the classical Pell tools themselves are novel.

The complete [proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_GLOBAL_SEED_EXISTENCE_009.md), [constructive exact-tuple generator](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_seed_existence.py), and [independent regressions](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_seed_existence.py) are in the protected research record.

### WP09: exact solutions for every polygonal-minus-square offset

The previous existence theorem applied to offsets one less than a polygonal number. The next theorem generalizes the shift from $1$ to **any positive integer square**.

**Uniform exact-integer theorem.** Choose any polygonal order $k\ge3$, positive integers $u$ and $a$, and set $c=P_k(u)-a^2$. Then infinitely many distinct positive-integer Type B triples $(a,b,d)$ exist at this order and offset, with all three shifted pair products **exactly equal** to polygonal numbers at positive integer indices. The first entry $a$ is fixed, not merely a residue class.

To construct them, choose an index $r$ congruent to $u$ modulo $2a$, and set $b=(P_k(r)-c)/a$. For infinitely many such choices, $b>a$ and $ab$ is nonsquare. The formal repeated-entry triple $(a,b,a)$ satisfies the polygonal identities but is not a valid Type B triple. A generalized Pell recurrence transforms its two index coordinates into a **genuine third integer entry** different from the first two. The recurrence is chosen to preserve congruences modulo $4a(k-2)$: these ensure that both polygonal indices and the reconstructed entry remain integral.

The required nonsquare choices exist because $P_k(r)-P_k(u)+a^2$ cannot be a square for all sufficiently large $r$ in that progression, except for the square-order case $k=4,a=u$. The exception has a simple direct construction: at offset zero, $(u,4u,n^2u)$ gives exact square-output triples for every $n\ge3$.

**A genuinely new offset beyond WP09-009:** for heptagonal numbers, choose $k=7,u=2,a=2$. Then $c=P_7(2)-4=3$. The first promoted triple has entries

- $a=2$
- $b=39$
- $d=11293707732912017913758403774086454320790468713804$

with exact polygonal indices $(6,3005822048347109708020586,13273350768868706404017954)$. Each shifted pair output is verified against the heptagonal formula using exact integer arithmetic. The offset $3$ is not of the older form $P_7(v)-1$, so this result strictly enlarges the guaranteed global-realization family.

The [full mathematical proof](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_SQUARE_SHIFT_GLOBAL_EXISTENCE_010.md), [constructive generator](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_square_shift_existence.py), and [independent arithmetic tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_square_shift_existence.py) distinguish real integer solutions from local congruence witnesses. This is a sufficient global-existence theorem for a specific family of offsets, not a universal local-to-global result or a literature-originality assertion.

### WP09: why failure of the square-shift test is not nonexistence

The new square-shift theorem proves that many offsets have exact integer Type B triples. But **failure of its representation condition does not mean a triple is impossible**. The distinction can be proved uniformly using residues modulo four.

For every polygonal order divisible by four, the polygonal polynomial satisfies

$$
P_k(u)\equiv u^2\pmod4.
$$

Therefore the differences $P_k(u)-a^2$ can only be congruent to 0, 1 or 3 modulo four, **never 2**. Every offset $c\equiv2\pmod4$ falls outside the WP09-010 construction, even if we allow negative indices or a zero first entry.

Nevertheless, the three distinct entry residues $(1,2,3)$ work simultaneously modulo four: the shifted pair outputs are $(0,1,0)$, matching the polygonal index residues $(4,1,4)$. There is no single *diagonal* entry residue that works, but three **different** residues do. This explains why the diagonal construction is sufficient, not necessary. It also shows that the convenient diagonal compatibility criterion at odd prime powers cannot be assumed at powers of two.

The distinction survives when we demand **exact positive-integer equalities**, not just congruences:

| Polygonal order | Offset | Exact entries | Exact indices |
| --- | ---: | --- | --- |
| 4 | 2 | $(1,7,14)$ | $(3,4,10)$ |
| 20 | 2 | $(1,18,13375)$ | $(2,39,164)$ |
| 36 | 2 | $(1,343,6478)$ | $(5,20,362)$ |

The 36-gonal example is new to the FIGURATE proof record. Its three shifted products are exactly

$$
345=P_{36}(5),\qquad6480=P_{36}(20),\qquad2221956=P_{36}(362).
$$

Because 343 is not a perfect square, the earlier Pell amplification theorem converts this seed into **infinitely many exact 36-gonal Type B triples**, all at offset 2.

For square outputs ($k=4$), the result is even broader: the classical Euler regular construction gives infinitely many exact triples at **every** signed integer offset $c$, including all offsets congruent to 2 modulo four. Thus an infinite set of parameter pairs missed by WP09-010 is nevertheless globally realizable.

The [rigorous diagonal-gap proof](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_NONDIAGONAL_ANCHOR_GAP_011.md), [exact constructor](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_nondiagonal_anchor_gap.py), and [independent tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_nondiagonal_anchor_gap.py) explain the precise distinction.

This result does not prove that all orders divisible by four and all offsets congruent to two have exact integer solutions. It proves that **absence of a square-shift anchor must not be mistaken for an obstruction to the full three-entry problem**. The unresolved local-to-global question remains open.

### WP09: the full local test for orders divisible by four

Some earlier research found that three different entry residues can pass a modulus-four test even when no repeated entry residue works. **A solution modulo four is not enough to establish local compatibility at all powers of two.** The already-protected WP08 theorem gives stronger obstructions that settle several examples immediately.

For every polygonal order divisible by four and every offset congruent to two modulo four, the following is now a **complete decision rule for simultaneous Type B compatibility at every finite modulus**.

First, if $k$ is divisible by eight, **no Type B triple exists**, because the three pair-output congruences are impossible modulo eight. If $k\equiv12\pmod{16}$, the congruences are impossible modulo sixteen. These are established WP08 results; orders 8, 12, 16 and 24 at offset 2 were **already proved impossible** and must not be described as unresolved.

The remaining orders satisfy $k\equiv4\pmod{16}$. Here the binary local conditions are all compatible. To decide the odd-prime conditions, compute

$$
\Delta=8(k-2)c+(k-4)^2.
$$

Only odd primes dividing $\Delta$ to an **odd** power need checking. At such a prime $p$ not dividing $k-2$, the order and offset are locally impossible exactly when $(k-2)/2$ is a quadratic nonresidue modulo $p$. This comes from the already-proved WP09-006 theorem for all odd prime powers. If none of these obstructions occurs, the Chinese remainder theorem combines all local witnesses for **every specified modulus**.

**Examples:**

| Order | Offset | Complete local result | Explanation |
| --- | ---: | --- | --- |
| 8 | 2 | Impossible | WP08 obstruction modulo 8 |
| 12 | 2 | Impossible | WP08 obstruction modulo 16 |
| 16 | 2 | Impossible | WP08 obstruction modulo 8 |
| 24 | 2 | Impossible | WP08 obstruction modulo 8 |
| 20 | 2 | Compatible | Also has a previously proved exact integer Pell family |
| 36 | 2 | Compatible | An explicit exact example is protected-admitted in the WP09-011 research record |
| 36 | 18 | Impossible | Odd-prime obstructions at 5 and 37 |
| 68 | 2 | Impossible | Odd-prime obstructions at 7 and 23 |

An impossible local result rules out every exact integer Type B triple, regardless of size. A compatible local result is **not** an exact integer construction. The open problem is determining when everywhere-local compatibility yields genuine positive-integer triples.

This synthesis uses [WP08's uniform binary classification](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP08_UNIFORM_2ADIC_ADMISSIBILITY_009.md), [WP09's complete odd-prime-power classification](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_ALL_ODD_PRIME_POWERS_COMPLETE_006.md), and the [integrated decision theorem](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_EVERYWHERE_LOCAL_STRATIFICATION_012.md). The protected WP08 obstruction is not claimed as a new discovery.

### WP09: exact solutions with an arbitrary first entry

The earlier Pell theorem amplified exact Type B triples of the form $(1,b,d)$. The next result removes the restriction that the first entry must be one.

**General fixed-pair amplification.** Suppose an actual positive-integer Type B triple $(a,b,d)$ exists for polygonal order $k$ and offset $c$, with all three entries distinct. If the **product $ab$ is not a perfect square**, then infinitely many actual triples exist with the same first pair $(a,b)$, order $k$, and offset $c$. Each shifted pair product remains exactly polygonal at a positive integer index.

Let $r,s,t$ be the three polygonal indices, put $R=2(k-2)$, $L=k-4$, $D=8(k-2)c+L^2$, $S=Rs-L$, and $X=a(Rt-L)$. The two equations involving $d$ become the exact generalized Pell identity

$$
X^2-abS^2=a(a-b)D.
$$

A norm-one Pell unit for the nonsquare coefficient $ab$ preserves that equation. Taking a suitable power that acts as the identity modulo $2aR$ also preserves the integer polygonal indices and the divisibility required to reconstruct a new integer third entry. Increasing Pell powers produce infinitely many distinct positive exact solutions. This proves a stronger fixed-pair theorem than the earlier $a=1$ result.

**New exact-integer examples from bounded seed searches:**

| Order | Offset | Exact entries | Polygonal indices |
| --- | ---: | --- | --- |
| 52 | 2 | $(2,25,703)$ | $(2,8,27)$ |
| 116 | 2 | $(1,2399,5602386)$ | $(7,314,15356)$ |
| 36 | 6 | $(1,30,715)$ | $(2,7,36)$ |

For 52-gonal numbers, the three exact pair outputs are 52, 1408, and 17577. The second entry $25$ is a square, but its product with the first entry is $2\cdot25=50$, a nonsquare. Therefore the new general theorem gives an infinite exact family at order 52 and offset 2. An earlier search restricted to first entry 1 had missed this small valid seed.

A separate, independently implemented complete divisor-graph enumeration finds exactly one unordered 52-gonal Type B tuple whose three entries are all at most 2,000: $(2,25,703)$. The search factors every candidate $P_{52}(n)-2$ up to the squared bound and exhaustively tests graph triangles; it is **not** a proof of global uniqueness. The [independent bounded enumerator and Pell replay](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_k52_exact_pell_seed.py), [five regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_k52_exact_pell_seed.py), and [separate proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_K52_EXACT_PELL_SEED_013.md) are protected in the research record.

For 116-gonal numbers, the three exact outputs are 2401, 5602388, and 13440124016. Since $2399$ is nonsquare, this seed also amplifies to infinitely many exact triples.

The search records its precise finite bounds on the first entry and polygonal indices. **Failure within a finite search window is never treated as a proof of nonexistence.** Several locally compatible pairs remain unresolved globally, and no general local-to-global theorem or counterexample follows.

The [full generalized Pell proof](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_GENERAL_FIRST_PAIR_PELL_013.md), [bounded search and exact constructor](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_fixed_pair_seed_frontier.py), and [independent regression source](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_fixed_pair_seed_frontier.py) record the method and its limitations. These are internal research results using classical Pell techniques; external novelty and mathematical certification are not asserted.

### WP09: exact order-52 solutions at offset six

The generalized Pell theorem applies to another genuine exact example at the same polygonal order but a **different offset**. At order $k=52$ and offset $c=6$, the three distinct positive entries $(2,2279,4757)$ have positive polygonal indices $(14,20,659)$. The exact shifted pair products are

$$
2\cdot2279+6=4564=P_{52}(14),
$$

$$
2\cdot4757+6=9520=P_{52}(20),
$$

$$
2279\cdot4757+6=10841209=P_{52}(659).
$$

Although the complete local arithmetic sieve allows this parameter pair, it cannot alone establish integer existence. Here the displayed integers supply that additional evidence. The offset is outside the square-shift construction, because $6\equiv2\pmod4$ and $P_{52}(u)-a^2$ can never have residue 2 modulo four.

The first pair has product $2\cdot2279=4558$, which is not a square. The already-protected arbitrary-first-pair Pell theorem therefore proves **infinitely many exact Type B solutions keeping $(2,2279)$ fixed**. The independent exact-integer divisor-graph census finds exactly one unordered solution with all three entries at most 10,000, namely this seed. That is a bounded statement, not global uniqueness.

The [WP09-014 proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_K52_C6_EXACT_SEED_014.md), [exact bounded enumerator](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_k52_c6_exact_seed.py), and [six arithmetic tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_k52_c6_exact_seed.py) were admitted to protected MATHSOLVE research state. No independent MATHCERT certification or external literature originality is claimed.

### WP09: order-68 exact Type B families at offset six

The earlier frontier pair $(k,c)=(68,6)$ is **globally realizable**, not merely locally compatible. With $P_{68}(n)=33n^2-32n$, one exact positive distinct triple is $(a,b,d)=(10,44033,128739)$ at polygonal indices $(r,s,t)=(116,198,13107)$:

$$
10\cdot44033+6=440336=P_{68}(116),
$$

$$
10\cdot128739+6=1287396=P_{68}(198),
$$

$$
44033\cdot128739+6=5668764393=P_{68}(13107).
$$

Four other independently checked triples at the same parameter pair are $(22,13117,168855)$, $(55,4085,265746)$, $(61,55575,102610)$ and $(102145,629950,746915)$, with respective index triples $(94,336,8193)$, $(83,666,5736)$, $(321,436,13146)$ and $(44158,48083,119408)$. These are explicitly checked exact positive-integer examples, not a complete census up to one million.

For every displayed triple the product $ab$ is nonsquare. Hence the earlier protected WP09-013 fixed-first-pair Pell theorem generates **infinitely many exact positive Type B triples** from each seed. For the first one, the norm equation is

$$
X^2-440330S^2=-3197830720,
$$

with $(X,S)=(17300600,26072)$. Its exact seed and the previously admitted unit argument—not the local sieve alone—establish global integer existence.

A complete divisor-graph enumeration separately proves that there is **no unordered triple with all entries at most 100,000** at $(68,6)$. This is a finite-bound result only and is consistent with the larger positive seeds. The [protected proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_K68_C6_EXACT_SEEDS_015.md), [reproducible integer-only enumerator](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_k68_c6_exact_seeds.py) and [five source tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_k68_c6_exact_seeds.py) document its scope.

The globally unresolved local-compatible examples $(84,2)$ and $(100,2)$ remain open. No universal local-to-global theorem, external literature originality claim or independent MATHCERT certification is asserted.

### WP09: complete bounded census at orders 84 and 100

The remaining locally compatible candidates at orders $k=84$ and $k=100$, each with offset $c=2$, have now been checked by a complete **entry-bounded** arithmetic enumeration rather than only searching for small first entries or polygonal indices. The exact result is:

| Order | Offset | Entry bound | Exact graph edges | Type B triples found |
| --- | --- | ---: | ---: | ---: |
| 84 | 2 | 300,000 | 17,471 | 0 |
| 100 | 2 | 300,000 | 25,454 | 0 |

The method constructs an exact graph whose vertices are positive integers from 1 through 300,000. An edge connects $a,b$ precisely when $ab+c$ equals a polygonal number at some positive integer index. All factor pairs of every polygonal value up to the maximum product are enumerated, so a Type B triple within the entry bound corresponds exactly to a triangle in this graph. **Both complete graphs have zero triangles.** This proves the two finite-bound exclusions, not global nonexistence. A solution with one or more entries greater than 300,000 remains possible.

There is also a useful unrestricted structural theorem. For any order divisible by four and any offset congruent to two modulo four, **every exact Type B triple must have entries occupying residue classes 1, 2 and 3 modulo four, one entry in each class.** Indeed $P_k(n)$ has the same residue modulo four as $n^2$, so each pair product must be 2 or 3 modulo four. Two even entries are impossible, three odd entries are impossible, and the one even entry must be 2 modulo four while the odd entries must be 1 and 3 modulo four. This necessary condition does not exclude either target family.

Both targets still pass the previously proved complete local sieve at every modulus: their discriminants are $7712=2^5\cdot241$ and $10784=2^5\cdot337$ respectively. **Existence of actual positive-integer triples remains unknown** for these two parameter pairs; passing all finite congruences is insufficient to conclude otherwise.

The [protected WP09-016 proof and bounded-census dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_FRONTIER_CENSUS_016.md), [integer-exact full graph enumerator](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_frontier_census_016.py) and [independent regression source](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_frontier_census_016.py) record the precise bounds and reproduction instructions. The result is internally admitted research, not external originality or independent MATHCERT certification.

### WP09: seed-existence and two-index descent

The next question is not how far an exhaustive search can be extended, but **when its first exact integer seed must exist**. WP09-017 gives two exact reductions that make this question more structured.

Suppose three candidate polygonal indices give positive numbers

$$
A=P_k(r)-c,\qquad B=P_k(s)-c,\qquad C=P_k(t)-c.
$$

For them to be the pair products $ab$, $ad$, and $bd$ of three distinct positive integers, the quantity $T=\sqrt{ABC}$ must be an integer divisible by each of $A,B,C$. The recovered entries are then uniquely

$$
a=T/C,\qquad b=T/B,\qquad d=T/A,
$$

which must be pairwise distinct. Equivalently, at each prime, the exponents in $A,B,C$ must have even sum and satisfy all three triangle inequalities. This is a complete test for *specified polygonal indices*, but does not assert that appropriate indices exist.

An even more useful search reduction fixes **two** polygonal indices $r<s$. Write $A=P_k(r)-c$ and $B=P_k(s)-c$. Any exact Type B seed with these first two indices has

$$
a\mid\gcd(A,B),\qquad b=A/a,\qquad d=B/a.
$$

Each divisor candidate is accepted precisely when the three entries are positive and distinct and the third shifted pair product is an exact positive polygonal number of order $k$. The algorithm therefore examines index pairs and divisors of their gcd, rather than cubically enumerating entries.

For a fixed first pair $(a,b)$, the remaining seed conditions can also be organized as the generalized Pell norm equation

$$
X^2-abS^2=a(a-b)\Delta,\qquad
\Delta=8(k-2)c+(k-4)^2.
$$

But a solution of this norm equation alone is **not** enough: the polygonal index lattice, divisibility, positivity, and distinctness requirements must all hold. The known exact $(68,6)$ solution provides a positive control for these checks. The $(84,2)$ and $(100,2)$ cases are solved by WP09-018 and WP09-019; $(132,2)$ is solved by WP09-020, and WP09-021 adds four more exact cases.

The [protected WP09-017 theorem dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_SEED_DESCENT_017.md), [exact index-first implementation](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_seed_descent_017.py), and [six regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_seed_descent_017.py) provide the derivations and arithmetic checks. The next objective is to explain which locally compatible pairs admit an integral Pell-lattice point, and to prove a general sufficient criterion or a genuine unbounded obstruction; another larger finite census is not enough. These are internal research results, without independent MATHCERT certification or an external priority claim.

### WP09: exact global existence at the 84-gonal offset two

The previously unresolved pair $(k,c)=(84,2)$ now has an exact positive-integer Type B solution. Its entries are

$$
(a,b,d)=(2,41,172124700980346120000589924527450935999),
$$

and its polygonal indices are

$$
(r,s,t)=(2,2897641606046209200,13119630367519738931).
$$

Direct substitution gives the three exact pair outputs

$$
P_{84}(r)=84=2\cdot41+2,
$$

$$
P_{84}(s)=344249401960692240001179849054901872000=2d+2,
$$

$$
P_{84}(t)=7057112740194190920024186905625488375961=41d+2.
$$

The construction fixes the small first pair $a=2,b=41$ at index $r=2$. With $R=164$, $L=80$ and $\Delta=7712$, the remaining equations reduce to

$$
X^2-82S^2=-601536,
$$

where $S=164s-80$ and $X=2(164t-80)$. An exact starting solution is $(X,S)=(3585208,395920)$. The norm-one unit $163+18\sqrt{82}$, applied six times, gives

$$
(X,S)=(4303238760546474369208,\;
475213223391578308720),
$$

which lies in the required index lattice:
$S\equiv84\pmod{164}$ and $X\equiv168\pmod{328}$. Recovering $s,t,d$ then gives the exact triple above.

Because $ab=82$ is nonsquare, the protected WP09-013 fixed-first-pair Pell theorem applies. The unit has order 328 modulo the amplification lattice modulus $2aR=656$. Its 328th power preserves the seed's index and divisibility classes; the next exact family member has a 1,687-digit third entry. Thus this is not just one isolated seed: it establishes **infinitely many exact positive Type B triples** at $(84,2)$.

The 39-digit third entry explains why the result escaped the WP09-016 complete census with all entries at most 300,000. That bounded exclusion remains correct; it was never a global nonexistence theorem. The result is an exact global existence proof, not a local-to-global counterexample. WP09-019 below now resolves $(100,2)$ as well.

The [WP09-018 proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_84_GONAL_EXACT_SEED_018.md), [exact Pell-orbit constructor](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_exact_seed_018.py), and [seven direct-polynomial regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_exact_seed_018.py) record the full derivation and reproducible checks. These are internally admitted producer results; independent MATHCERT certification and external literature-priority review remain separate.

### WP09: exact global existence at the 100-gonal offset two

The second case from the WP09-016 bounded frontier is also solved. For $(k,c)=(100,2)$, an exact Type B seed is

$$
(a,b,d)=(1,98,394141484570467638798107106734400805257750080265189167281283878325018383881627360745786897584655),
$$

$$
(r,s,t)=(2,89686697824951931533091760698417159299075689513,887853010999532105318395994347406981537890234904).
$$

The three exact pair outputs are

$$
P_{100}(r)=100=98+2,
$$

$$
P_{100}(s)=394141484570467638798107106734400805257750080265189167281283878325018383881627360745786897584657=d+2,
$$

$$
P_{100}(t)=38625865487905828602214496459971278915259507865988538393565820075851801620399481353087115963296192=98d+2.
$$

The fixed first pair gives the norm equation $X^2-98S^2=-1046048$. Starting from $(4019472,406028)$ and applying $99+10\sqrt{98}$ nineteen times reaches the required lattice $X\equiv S\equiv100\pmod{196}$. Since $ab=98$ is nonsquare, WP09-013 gives infinitely many exact triples with this first pair. The amplification modulus is 392, the unit order is 196, and the next family member has a 996-digit third entry.

The 96-digit seed is consistent with the earlier complete exclusion for entries at most 300,000. The bounded result was correct; it did not settle global existence. See the [WP09-019 proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_100_GONAL_EXACT_SEED_019.md), [constructor](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_exact_seed_019.py), and [seven exact regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_exact_seed_019.py).

### WP09: exact global existence at the 132-gonal offset two

The same construction solves $(k,c)=(132,2)$. An exact seed is

$$
(a,b,d)=(1,130,8359584463533923231612770595169701590647797311),
$$

$$
(r,s,t)=(2,11340590449649248400673,129302625368040561155552).
$$

Its pair outputs are

$$
P_{132}(r)=132=130+2,
$$

$$
P_{132}(s)=8359584463533923231612770595169701590647797313=d+2,
$$

$$
P_{132}(t)=1086745980259410020109660177372061206784213650432=130d+2.
$$

Here $X^2-130S^2=-2381856$. The base point $(90608,7948)$, multiplied five times by the norm-one unit $6499+570\sqrt{130}$, reaches $X\equiv S\equiv132\pmod{260}$. The first-pair product 130 is nonsquare, so WP09-013 proves an infinite exact family. The amplification modulus is 520, the unit order is 52, and the next third entry has 474 digits.

The [WP09-020 proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_132_GONAL_EXACT_SEED_020.md), [constructor](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_exact_seed_020.py), and [seven exact regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_exact_seed_020.py) contain the full arithmetic.

### WP09: four further exact Pell seeds

Four more parameter pairs from the all-place locally compatible frontier now have exact global seeds. All use the first pair $(a,b)=(1,k-2)$ at $r=2$; in each case $ab=k-2\equiv2\pmod{16}$ is nonsquare, so WP09-013 supplies an infinite family.

| Order $k$ | Base Pell point $(X_0,S_0)$ | Norm-one unit | Seed steps | Third-entry digits | Amplification modulus / order |
|---:|---:|---:|---:|---:|---:|
| 164 | (72416,5692) | $19601+1540\sqrt{162}$ | 10 | 97 | 648 / 162 |
| 196 | (4828080,346636) | $195+14\sqrt{194}$ | 57 | 304 | 776 / 388 |
| 228 | (10227632,680332) | $451+30\sqrt{226}$ | 20 | 127 | 904 / 452 |
| 244 | (11376,772) | $19601+1260\sqrt{242}$ | 44 | 407 | 968 / 242 |

The exact indices, entries, norm identities, and next-family checks are recorded in the [WP09-021 dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_LOCAL_POSITIVE_SEED_BATCH_021.md), with its [constructor](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_local_positive_seed_batch_021.py) and [seven regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_local_positive_seed_batch_021.py). The next family third-entry sizes are 1,585, 2,314, 2,799 and 2,630 digits, respectively.

Together with $(84,2)$, $(100,2)$ and $(132,2)$, this gives seven newly solved locally compatible pairs in the present tranche. These examples do **not** prove that every locally compatible pair has a global seed. They provide concrete evidence for a more focused next question: whether the constrained Pell-lattice construction can be characterized uniformly across the local-positive parameter classes.

### WP09: three more exact Pell seeds at orders 308, 340 and 356

Further exact global Type B seeds have been constructed at offsets $c=2$ for polygonal orders $k=308,340,356$, all within the previously classified all-place locally compatible range. As in the preceding tranche, take $a=1$, $b=k-2$ and the first polygonal index $r=2$. The first pair satisfies $ab+2=k=P_k(2)$, and $ab=k-2$ is nonsquare.

The remaining two equations are solved by integral Pell norm and polygonal-index lattice conditions. The following data reproduce each seed from a norm-equation base point and a positive unit:

| Order $k$ | Pell base point $(X_0,S_0)$ | Norm-one unit | Seed steps | Digits in third entry |
|---:|---:|---:|---:|---:|
| 308 | $(7521856,429996)$ | $35+2\sqrt{306}$ | 1 | 12 |
| 340 | $(18592,1068)$ | $114243+6214\sqrt{338}$ | 8 | 89 |
| 356 | $(30800,1676)$ | $258065+13716\sqrt{354}$ | 32 | 369 |

For example, at order $308$ the exact triple is $(a,b,d)=(1,306,369944066839)$ with polygonal indices $(2,49173,860168)$. All shifted pair products match the corresponding positive polygonal values by integer arithmetic. For the other two cases, the exact large entries and indices are preserved in the source rather than rounded in the table.

Every constructed first-pair product $k-2$ is nonsquare, so the already protected WP09-013 Pell amplification theorem establishes infinitely many further exact Type B triples with that first pair. These are **three additional constructive existence results**, not evidence that the local-to-global principle holds universally.

The [WP09-022 producer dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_LOCAL_POSITIVE_SEED_BATCH_022.md), [exact Pell constructor](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_local_positive_seed_batch_022.py), and [seven arithmetic regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_local_positive_seed_batch_022.py) record full values, index lattice checks, and replay. No independent MATHCERT certification or external mathematical originality claim is made.

### WP09: a uniform finite decision for fixed-pair Pell index lattices

The accumulating enormous exact seeds raise a more fundamental question: *can we decide whether a given first pair can ever be extended to a third entry?* WP09-023 answers this in full for **each specified exact first pair $(a,b)$ whose product $Q=ab$ is nonsquare**. It is an exact mathematical decision procedure, although its worst-case cost may be very large.

Fix polygonal order $k$, offset $c$ and a verified first pair $(a,b)$ with $ab+c=P_k(r)$. As in the preceding theorem, set $R=2(k-2)$, $L=k-4$, and $\Delta=8(k-2)c+L^2$. An exact third entry must provide positive integer coordinates on

$$
X^2-abS^2=a(a-b)\Delta,
$$

along with congruences ensuring that $S=Rs-L$, $X=a(Rt-L)$, and $d=(P_k(s)-c)/a$ are all integral.

The new result has two steps. First, multiplication by the fundamental Pell unit moves *every* positive integer norm solution back into one bounded region. This produces a **finite, provably complete set of possible starting representatives**, rather than a search with an arbitrary stopping point. Second, multiplying a representative by that unit modulo $M=2aR$ has a finite periodic residue orbit. Each residue is tested against the integer-index and third-entry divisibility conditions. A compatible state yields a genuine exact positive seed after sufficiently many forward unit steps; if every orbit fails, no third entry exists **for that first pair**.

The [WP09-023 mathematical proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_UNIFORM_PELL_LATTICE_023.md) gives the necessary-and-sufficient criterion and finite-domain proof, with an [integer-exact decision implementation](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_uniform_pell_lattice_023.py) and [seven regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_uniform_pell_lattice_023.py). Existing exact positive families at orders 84, 100 and 308 provide controls. A first-pair negative at order 68, offset 2 is separately checked; it does not constitute a new global obstruction.

**Important limitation:** this decides extension of a **specified** first pair, not whether there exists some suitable first pair for every everywhere-locally-compatible order and offset. It also does not imply a fast algorithm: the fundamental unit and representative bounds may be enormous. A resource limit in the implementation raises an explicit error rather than pretending to prove nonexistence. The next substantial objective is to classify or bound the possible first pairs uniformly, so that the decision procedure can address whole parameter families. No independent MATHCERT certification or literature-priority assessment is asserted.

### WP09: uniform index restrictions and a smaller Pell-lattice test

A sequence of extremely large exact seeds does not, by itself, explain which polygonal orders admit solutions. WP09-024 instead proves two statements **uniformly across parameter classes**.

First consider the recurring construction at offset $c=2$, with first entries $a=1$, $b=k-2$, first polygonal index $r=2$, and order $k=16m+4$. Any exact positive Type B third entry $d$ at indices $s,t$ necessarily satisfies

$$
s\equiv1\pmod2,\qquad d\equiv7\pmod8,\qquad t\equiv0\pmod4.
$$

The condition can be sharpened: the residue class of $t$ modulo eight is uniquely determined by the parity of $m$ and the square class of $s$ modulo sixteen,

$$
\frac{t}{4}\equiv m+\frac{s^2-1}{8}\pmod2.
$$

The fraction is integral because $s$ must be odd. Thus every even candidate $s$ is impossible for this anchor, and the permitted $t$ branch is known before any expensive Pell computation. These conditions are **necessary, not sufficient**: meeting them does not manufacture an exact global solution.

The second result improves the complete fixed-first-pair decision from WP09-023. That method tests a finite Pell orbit modulo $2aR$, where $R=2(k-2)$. An exact integer-polynomial periodicity theorem shows that the smaller modulus $Rh$ is sufficient, with $h=a$ whenever $k$ is even or $a$ is odd, and $h=2a$ otherwise. Hence for the important anchor $a=1$, the modulus decreases from $2R$ to $R$, reducing the maximum possible number of residue states by a factor of four without losing any genuine solutions or false-negative protection.

These two theorems give a principled way to reject impossible index branches and reduce the exact solvability search. The results are checked against previously admitted positive anchors at orders 84, 100 and 308, and against the known negative fixed-pair control at order 68. Their complete proofs and explicit limitations are recorded in the [WP09-024 dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_ANCHOR_INDEX_LATTICE_024.md), [exact implementation](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_anchor_index_lattice_024.py), and [independent arithmetic regressions](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_anchor_index_lattice_024.py).

**What remains open:** whether every compatible order has an admissible first pair, whether its Pell norm equation possesses an integral lattice representative, and whether a family-wide construction or unbounded obstruction can be proved. A uniform necessary congruence theorem is not a universal local-to-global theorem, and internal research admission does not imply independent MATHCERT certification or literature priority.

### WP09: an exact primitive Pell criterion for the recurring anchor

The repeated exact examples at orders congruent to four modulo sixteen suggest studying the common first-pair construction *as a whole*. WP09-025 produces a stronger equivalence than simply testing larger and larger candidate seeds.

Set

$$
k=16m+4,\qquad A=8m+1,\qquad H=8m(m+1)+1,
$$

where $m$ is any nonnegative integer. Fix offset $c=2$ and first entries $(a,b)=(1,k-2)=(1,2A)$, with first polygonal index $r=2$.

**Exact theorem.** A positive distinct Type B seed with this fixed first pair exists **if and only if** the following reduced generalized Pell equation has a positive integer solution:

$$
x^2-2Ay^2=-2(2A-1)H,
$$

subject to just one prescribed **odd-modulus** residue class:

$$
2x\equiv2y\equiv1\pmod A.
$$

The reduction is exact. The original fixed-pair Pell coordinates $X,S$ are necessarily multiples of four; setting $X=4x$, $S=4y$ divides the original norm by sixteen. The required polygonal indices are recovered by

$$
t=\frac{x+(A-1)/2}{A},\qquad
s=\frac{y+(A-1)/2}{A}.
$$

Far enough forward along a residue-preserving norm-one Pell orbit, both indices are positive and the third entry $d=P_k(s)-2$ becomes positive and distinct from the first pair. Direct integer arithmetic then verifies all three original polygonal equations. Thus any positive solution of the reduced norm-and-residue system generates **infinitely many genuine exact Type B triples**.

This theorem treats every value of $m$ by the *same mathematical condition*. The reduced Pell-orbit test needs at most $A^2$ modular states, compared with $(4A)^2$ in the previous WP09-024 anchor construction. It also uses a norm whose magnitude is sixteen times smaller. This is a rigorous search-space reduction, not an assertion of polynomial runtime.

The [WP09-025 proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_ODD_RAY_LATTICE_025.md), [exact normalized solver](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_odd_ray_lattice_025.py), and [independent arithmetic tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_odd_ray_lattice_025.py) document the necessary-and-sufficient theorem, complete finite decision procedure, positive controls and guarded non-completion.

The remaining research question is **which values of $m$ satisfy the primitive norm-and-residue condition without running a separate Pell computation for each one**. WP09-025 does not prove that every locally compatible order has such a solution, nor that the recurring anchor covers every global solution using other first pairs. Generalized Pell finite-orbit theory is classical; this work specializes and normalizes its integral polygonal-index constraints. Independent mathematical certification and external novelty review remain separate.

### WP09: the Pell ray can be decided with two gcd tests

WP09-025 reduced the recurring order $k=16m+4$ anchor existence question to a primitive generalized Pell norm and a single target residue class modulo the odd integer $A=8m+1$. The remaining finite modular orbit can now be solved *algebraically*, without visiting its states.

Write $q=2A$, $r=(A+1)/2$, and let $U+V\sqrt q$ be the fundamental positive norm-one Pell unit. Fix any positive integer representative $(x_0,y_0)$ of the primitive norm. The entire infinite unit orbit meets the polygonal-index target $(r,r)$ modulo $A$ **if and only if** at least one of two alternatives holds:

$$
x_0\equiv r\pmod A,\qquad y_0\equiv r\pmod{\gcd(V,A)},
$$

or

$$
x_0\equiv Ur\pmod A,\qquad y_0\equiv Ur\pmod{\gcd(V,A)}.
$$

The reason is that, modulo $A$, the Pell unit multiplication matrix becomes triangular; its even powers are linear shears and its odd powers are their translate. The exponent needed to hit the ray is given by a solvable linear congruence, not an exhaustive orbit search. An exponent can therefore be constructed using gcd and modular inversion. Once it reaches the ray, residue-preserving further Pell steps yield genuine positive distinct exact Type B triples.

The [WP09-026 proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_LINEAR_RAY_026.md), [exact linear-ray implementation](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_linear_ray_026.py), and [six regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_linear_ray_026.py) document the necessary-and-sufficient ray criterion, constructive exponents and verification against complete finite orbits.

**What this does not establish:** whether the required *norm-equation representatives themselves* exist for all $m$, whether every locally compatible order has a seed, or mathematical certification and literature priority. The remaining family-wide problem lies in quadratic-order norm representation and principality, not Pell-unit residue traversal.

### WP09: local ideal norms versus global oriented ray principality

The next structural question is what prevents a locally compatible parameter from having an **exact global integer seed**. WP09-027 identifies the remaining condition in the arithmetic of a real quadratic order, while explicitly respecting its conductor.

For an order $k=16m+4$ at offset $c=2$, consider the recurring first pair $(a,b)=(1,k-2)$. Put $A=8m+1$, $D=2A$, $H=8m(m+1)+1$ and $N=-2(2A-1)H$. The WP09-025 result requires an integer element $x+y\sqrt D$ of norm $N$ with prescribed coefficients modulo $A$.

When $A=f^2 a_0$ with $a_0$ odd squarefree, the correct quadratic field is $K=\mathbf Q(\sqrt{2a_0})$ and the **actual order** is $\mathcal O=\mathbf Z[f\sqrt{2a_0}]$. Its conductor is $f$. The identity $8H=A^2+6A+1$ proves $\gcd(N,A)=1$, so any ideal of the required norm avoids the conductor, including in nonmaximal-order cases.

A new equivalence follows: for every order in this family, **WP09-012's everywhere-local compatibility holds exactly when the quadratic order has an invertible ideal of norm $|N|$**. This is proved by matching the odd-prime Legendre conditions in the protected local sieve to the even-exponent requirement for inert primes in ideal norms. It does not say that the ideal is generated by an integer with the required polygonal-index residues.

The decisive global requirement is more specific. Let $r=(A+1)/2$, $\rho=r(1+\sqrt D)$ and take the oriented ray class group of $\mathcal O$ modulo $A\mathcal O$, with positivity at the real embeddings. An exact anchor seed exists **if and only if** there is an invertible ideal of norm $|N|$ belonging to the **same oriented ray class as the principal ideal $(\rho)$**. Equality only in the ordinary class group, or only after passing to the maximal order, is insufficient: the integral coefficientwise ray must be preserved.

The [WP09-027 proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_RAY_CLASS_CONDUCTOR_027.md), [exact conductor and local ideal-norm diagnostics](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_ray_class_conductor_027.py), and [nine regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_ray_class_conductor_027.py) provide the detailed mathematics and checks against the protected local classifier.

**Remaining boundary:** This determines the correct class-theoretic obstruction but does **not yet compute** oriented ray class groups or classify all $m$. The next substantive work is a conductor-aware oriented ray-class calculator, tested against exact positive and negative anchors. No independent MATHCERT certification or external mathematical priority is asserted.

### WP09: exact ideal enumeration and targeted oriented ray classification

The preceding quadratic-order reformulation identifies the **oriented ray class** as the obstruction to an exact global anchor seed. WP09-028 now provides an exact finite way to classify **every candidate ideal of the required norm** for any specified polygonal order at which the complete computation fits the resource limit.

Write $A=8m+1$, $D=2A$ and $N=-2(2A-1)(8m(m+1)+1)$. Work in the actual quadratic order $\mathcal O=\mathbb Z[\sqrt D]$, including when it has a nontrivial conductor. Every integral ideal of norm $|N|$ has a unique integer-lattice basis determined by positive integers $c,h$ and residue $j$:

$$
I=\langle(ch,0),(cj,c)\rangle,\qquad
c^2h=|N|,\quad 0\le j<h,\quad j^2\equiv D\pmod h.
$$

The conditions are **necessary and sufficient** for an ideal, so the resulting enumeration cannot miss a norm ideal. Because $\gcd(A,N)=1$, every candidate ideal avoids the conductor and is invertible.

For each ideal, the code uses a complete generalized-Pell norm-representative enumeration and the already-proved WP09-026 two-gcd test to decide whether its norm generators reach the required oriented coefficientwise ray. It distinguishes a ray match, an oriented principal ideal in the **wrong** ray, and an ideal with no norm $N$ generator of the specified real-sign pattern. This is a genuine class-membership decision for the required norm ideals, without pretending that ordinary principality or locally compatible ideal norms suffice.

The first complete classifications expose the distinction:

| Order $k$ | Candidate norm ideals | Required ray matches |
|---:|---:|---:|
| 36 | 4 | 1 |
| 84 | 10 | 6 |
| 100 | 4 | 2 |
| 228 | 27 | 6 |

At order 36, for example, the four candidate ideals split among one target-ray match, one oriented principal ideal in the wrong ray, and two lacking a generator of the required negative norm and real signs. In the previously proved locally obstructed order-68 case, there are no norm ideals at all.

The [WP09-028 HNF and ray proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_IDEAL_RAY_ENUMERATION_028.md), [exact integer implementation](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_ideal_ray_enumeration_028.py), and [independent lattice and Pell tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_ideal_ray_enumeration_028.py) explain the complete finite decision and strict computation guards. A guard failure is **undecided**, never a mathematical NO.

**What remains genuinely open:** This is a **targeted norm-ideal fibre calculator**, not an abstract presentation of the whole oriented ray class group or a uniform classification of all parameters $m$. Removing the generalized-Pell representative bottleneck through independent reduced-ideal arithmetic, especially in nonmaximal orders, is the next research obligation. Mathematical certification and external novelty claims remain separate.

### WP09: computing the oriented ray kernel as a finite abelian group

The exact norm-ideal calculator of WP09-028 identifies which ideals of a specified norm occupy the required oriented ray class. WP09-029 now computes an entire **group-theoretic component** of that problem uniformly, without searching for generalized-Pell norm representatives.

For the recurring anchor family, put $A=8m+1$ and let the actual possibly nonmaximal order be $\mathcal O=\mathbb Z[\sqrt{2A}]$. Its ray modulus is $A\mathcal O$. Since $(\sqrt{2A})^2=2A$ vanishes modulo $A$, the residue ring is a ring of *dual numbers*: its nonconstant generator has square zero.

The unit group therefore has the exact form

$$
(\mathcal O/A\mathcal O)^\times
\cong(\mathbb Z/A\mathbb Z)^\times
\times(\mathbb Z/A\mathbb Z,+).
$$

If $U+V\sqrt{2A}$ is the smallest positive norm-one Pell unit, then the full **oriented ray kernel** is the quotient of this group by the cyclic subgroup generated by $(U,VU^{-1})$ modulo $A$. The calculator enumerates that finite quotient and determines its invariant factors exactly, respecting the conductor and both real embeddings.

For example, it finds kernel groups $C_3$ for $m=1$, $C_{16}$ for $m=2$, $C_{20}$ for $m=5$, and $C_3\times C_{18}$ for $m=7$. This is a substantive class-group calculation independent of the large third entries in individual Type B seeds.

Crucially, the *kernel* is not automatically the **full oriented ray class group**: the latter also involves the narrow Picard group of the quadratic order. That additional group is known in two proved base cases. At $m=0$, the maximal order $\mathbb Z[\sqrt2]$ is norm-Euclidean and has a norm-negative unit, making the full ray group trivial. At $m=1$, the conductor-three order $\mathbb Z[3\sqrt2]$ has trivial ordinary Picard group but narrow Picard group of order two; the ray kernel has order three, giving the **full oriented ray class group $C_6$**.

The [WP09-029 mathematical dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_RAY_KERNEL_029.md), [exact finite-group implementation](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_ray_kernel_029.py), and [independent dual-number and quotient tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_ray_kernel_029.py) provide the proof and reproducible computations.

**Unresolved:** The full ray class group for arbitrary $m$ still requires the narrow Picard group and the extension/group law. No uniform classification of all successful polygonal orders, independent MATHCERT certification, or external originality claim follows from this work.

### WP09: narrow Picard groups for an infinite nonmaximal-order family

WP09-029 computed the entire *ray kernel* but left the narrow Picard group—and hence most of the full ray class group—unknown. WP09-030 now supplies an exact computation of the **whole narrow Picard group** for the infinite square-conductor subfamily. Take a positive odd integer $f$, put $A=f^2=8m+1$, and consider the actual quadratic order $\mathcal O_f=\mathbb Z[f\sqrt2]$ with conductor $f$.

The maximal order $\mathbb Z[\sqrt2]$ is norm-Euclidean and has trivial narrow class group. Its totally positive units are powers of $3+2\sqrt2$. The conductor exact sequence therefore gives a complete finite-group representation of the narrow Picard group:

$$
\mathrm{Pic}^{+}(\mathcal O_f)
\cong
\frac{(\mathbb Z[\sqrt2]/f)^\times}
{(\mathbb Z/f)^\times\cdot\mathrm{im}\langle3+2\sqrt2\rangle}.
$$

Unlike a count of ideal classes alone, this quotient determines the actual abelian group law. The code enumerates its elements and computes invariant factors, checking the result separately against the classical conductor class-number formula and a direct modular Pell-unit recurrence. The computation retains the nonmaximal order rather than silently using the maximal-order ray.

| Conductor $f$ | Narrow Picard group | Full oriented ray-group order |
|---:|:---|---:|
| 3 | $C_2$ | 6 |
| 5 | $C_2$ | 20 |
| 7 | $C_2$ | 84 |
| 15 | $C_2\times C_2$ | 720 |
| 17 | $C_4$ | 544 |
| 21 | $C_2\times C_2$ | 1,512 |

The final column combines these complete narrow Picard groups with WP09-029's complete ray kernels through the exact short sequence. It determines **full ray-group cardinalities**, not the group extension structure or invariant factors. The full oriented ray groups have been established only for the already proved base cases $f=1$ and $f=3$.

The [WP09-030 proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_SQUARE_CONDUCTOR_PICARD_030.md), [exact narrow-Picard implementation](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_square_conductor_picard_030.py) and [independent tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_square_conductor_picard_030.py) record the full conductor proof, finite quotient arithmetic and strict resource guards.

**Remaining mathematics:** determine the full ray-group extension law even in this square-conductor family, then extend narrow Picard computations to more general quadratic fields and classify which parameter values carry an ideal in the required oriented ray class. None of the displayed orders proves global existence for all locally compatible parameters, and independent MATHCERT certification or literature priority is not claimed.

### WP09: full oriented ray groups for odd square conductors

WP09-030 determined the complete *narrow Picard group* of the quadratic order $\mathcal O_f=\mathbb Z[f\sqrt2]$ for odd $f$, and, using WP09-029, the **number** of classes in its oriented ray group. WP09-031 goes further: it determines the complete finite abelian group, including its invariant factors. Two groups can have the same number of elements but different structures, so this is information that an order calculation cannot supply.

For each positive odd $f$ put $A=f^2$, $m=(f^2-1)/8$, and retain the **actual nonmaximal order** $\mathcal O_f$ with ray modulus $I=f^2\mathcal O_f$. The maximal order is $\mathcal O_K=\mathbb Z[\sqrt2]$ and its totally positive units are generated by $u=3+2\sqrt2$. An exact residue-unit presentation of the entire oriented ray-class group is

$$
\mathrm{Cl}^{+}_{I}(\mathcal O_f)
\cong
\frac{(\mathcal O_K/f^3\mathcal O_K)^\times}
{\langle 3+2\sqrt2\rangle\,
 \{1+f^2j:j\in\mathbb Z/f\mathbb Z\}}.
$$

Why the cube? In the maximal-order basis, $f^2\mathcal O_f=f^2\mathbb Z+f^3\mathcal O_K$. Its extra scalar congruence is exactly the subgroup $1+f^2j$ after reduction modulo $f^3$. Invertible ideals prime to the conductor extend and contract to maximal-order ideals, which have totally positive generators; changing such a generator by a positive unit supplies the other quotient relation. Thus the formula retains both the true conductor and the sign-sensitive ray relation.

The [WP09-031 proof dossier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_FULL_RAY_GROUP_031.md) derives this quotient and its complete group law. The [exact finite-group implementation](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_full_ray_square_conductor_031.py) splits the calculation into prime-power residue rings, constructs their cyclic coordinates using finite-field generators and exact lifting, then imposes the *single global relation* from $u$. Prime-power torsion counts determine the invariant factors; this does not assume that the earlier ray-kernel exact sequence splits.

| Odd conductor $f$ | Complete oriented ray group | Group order |
|---:|:---|---:|
| 1 | trivial | 1 |
| 3 | $C_6$ | 6 |
| 5 | $C_{20}$ | 20 |
| 7 | $C_2\times C_{42}$ | 84 |
| 9 | $C_{54}$ | 54 |
| 11 | $C_{110}$ | 110 |
| 13 | $C_{13}\times C_{156}$ | 2,028 |
| 15 | $C_6\times C_{120}$ | 720 |
| 17 | $C_2\times C_{272}$ | 544 |
| 19 | $C_{342}$ | 342 |
| 21 | $C_6\times C_6\times C_{42}$ | 1,512 |

All eleven group orders agree with WP09-030. The [independent exact tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_full_ray_square_conductor_031.py) additionally enumerate the full underlying residue-unit quotient directly for $f=3,5,7$, check its torsion counts, test composite and prime-power CRT examples, and verify that resource limits raise an exception rather than reporting mathematical nonexistence. The five committed regression groups passed against the research candidate at exact head $8a4e54ae686758d6bb29aca6b1928445ea7ec8e8$; the research [protected PR #1233](https://github.com/grandchallenge/MATHSOLVE/pull/1233) was merged at $6dd6127a58ef99980f864ca47c1c496943af360c$.

**Limits:** This computes full oriented ray groups for the infinite *square-conductor* family $A=f^2$, not arbitrary squarefree part $a_0\ne1$. Knowing the abstract class group does not, by itself, show that a particular prescribed norm ideal occupies the target ray or that all locally admissible Type B parameters have actual positive-integer triples. Those problems, general-conductor Picard arithmetic, source priority, and independent MATHCERT mathematical certification remain separate.

### WP09: an infinite family where the target ray is actually attained

**WP09-032 moves beyond computing the obstruction:** for **every** positive integer $e$, set

$$
f=3^e,\qquad A=f^2=9^e,\qquad k=2A+2,\qquad c=2.
$$

There are **infinitely many distinct positive integers $d$** for which $(1,2A,d)$ is an exact Type B triple. Equivalently, all three required pairwise outputs are polygonal with **positive integer indices**:

$$
P_k(2)=2A+2,\qquad
P_k(s)=d+2,\qquad
P_k(t)=2Ad+2.
$$

This supplies a **uniform infinite family of polygonal orders** $k=20,164,1460,13124,\ldots$, not just one enormous search witness or a local-congruence prediction. The $k=20$ case was already known constructively; the new proof gives a single formula-and-lifting argument for **every** $e\ge1$. Literature originality has not been established.

**Why the theorem succeeds:** In the maximal ring $\mathbb Z[\sqrt2]$, construct an explicit element of the desired negative norm:

$$
\alpha=\frac{(1+f\sqrt2)(f^2+3+2\sqrt2)}2,\qquad
N(\alpha)=-2(2f^2-1)\frac{f^4+6f^2+1}{8}.
$$

The difficulty is that $\alpha$ need not belong to the **conductor order** $\mathbb Z[f\sqrt2]$ or satisfy its much stricter ray congruence. WP09-032 uses the positive norm-one unit $u=3+2\sqrt2$. Elementary 3-adic lifting proves that, for $L=4\cdot3^{2e-1}$, the unit $u^L$ can adjust exactly the missing coefficient of $\sqrt2$ modulo $f^3$. An explicitly computed exponent $E$ then gives

$$
\beta=\alpha u^E\in\mathbb Z[f\sqrt2],\qquad
\beta\equiv \frac{f^2+1}{2}(1+f\sqrt2)
\pmod{f^2\mathbb Z[f\sqrt2]}.
$$

Thus the **prescribed norm-ideal fibre contains an ideal in the actual oriented target ray class**, not merely an ideal in some class of a computed abstract group. The earlier exact Pell-to-polygonal equivalence then produces the desired triples; additional unit powers give infinitely many different $d$.

The [complete theorem and proof](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_POWER3_GLOBAL_SEEDS_032.md), [exact constructor](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_power3_global_seeds_032.py), and [independent matrix, norm, and polygonal-index regressions](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_power3_global_seeds_032.py) distinguish mathematical existence from the impracticality of printing very large witnesses. Exact positive triples were replayed at $e=1,2$; higher exponents were checked at the modular certificate level, while the proof covers **all** $e$.

**Still open:** which other conductors realize the target ray; whether there are everywhere-locally-compatible but genuinely globally obstructed infinite parameter families; the unrestricted Type B problem; and separate Types A/C questions. A theorem for $f=3^e$ does **not** imply one for arbitrary odd $f$. Independent MATHCERT certification and external novelty/priority review are also outstanding.

### WP09: mixed prime-power conductors give more uniform global existence

The power-of-three result in WP09-032 was **not** the limit of the method. WP09-033 proves a substantially larger, exact infinite family. Let

$$
f=3^a5^b7^c,\qquad a,b,c\ge0,\qquad a+b+c>0,
\qquad k=2f^2+2.
$$

For **every** such $f$, with offset 2, the fixed pair $(1,2f^2)$ has **infinitely many distinct positive Type B extensions**. All three pairwise outputs have positive integer polygonal indices, not merely matching residues.

For example, $f=5,7,15,21,35,105$ gives orders $52,100,452,884,2452,22052$. The mixed cases $f=15,21,35,105$ exhibit what the earlier power-of-three theorem did not cover. The claim is **uniform across all nonnegative exponents**, not a finite list of successful computations.

**Why mixing conductors works.** The same totally positive unit $u=3+2\sqrt2$ has exactly one factor of the relevant prime in the radical coefficient of the following explicitly computable powers:

$$
u^4=577+408\sqrt2,\quad
u^6=19601+13860\sqrt2,\quad
u^3=99+70\sqrt2.
$$

These are the starting points for 3-adic, 5-adic and 7-adic lifting, respectively. Raising each base to successive powers of its prime increases the radical-coefficient valuation **by exactly one each time**. The common exponent

$$
L=\operatorname{lcm}_{p\mid f}\left(t_p p^{2v_p(f)-1}\right),
\qquad (t_3,t_5,t_7)=(4,6,3),
$$

has exactly the required prime-adic valuations in every component. It therefore produces

$$
u^L\equiv1+f^2 B\sqrt2\pmod{f^3\mathbb Z[\sqrt2]},
\qquad \gcd(B,f)=1.
$$

Choose the computable inverse residue $jB\equiv2\pmod f$ and set $E=Lj-1$. Starting from the explicit norm element used in WP09-032,

$$
\alpha=\frac{(1+f\sqrt2)(f^2+3+2\sqrt2)}2,
$$

the corrected element $\beta=\alpha u^E$ has the prescribed negative norm and, crucially, lies in the **actual conductor order** with the correct *coefficientwise oriented ray*:

$$
\beta\in\mathbb Z[f\sqrt2],\qquad
\beta\equiv\frac{f^2+1}{2}(1+f\sqrt2)
\pmod{f^2\mathbb Z[f\sqrt2]}.
$$

Thus a norm ideal really **occupies the target ray class**. The previously proved exact Pell-to-polygonal formulas give the required positive-integer triples. Further ray-preserving unit powers give infinitely many distinct extensions. This is a global construction, not a general assertion that local compatibility implies a solution.

The [full WP09-033 proof](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_MIXED_CONDUCTOR_REALIZATION_033.md), [exact constructor](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp09_mixed_conductor_realization_033.py), and [independent exact matrix and discriminant tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_mixed_conductor_realization_033.py) preserve the distinctions between the theorem for all supported conductors and the finite regression sample. Exact independent tests cover 26 prime-power/mixed combinations, with full positive-index tuples checked for selected smaller conductors. Guarded large-witness cases do not become false nonexistence results.

**Boundary:** this theorem does **not** cover arbitrary odd primes, all first pairs, non-square conductors, Types A/C, independent MATHCERT certification or literature originality. The successor question is how to treat other primes and interactions where the unit's principal-component lift has higher valuation or the common exponent introduces incompatible divisibility.

## 7. What is established—and what remains open

**Proved nonexistence in specified families:** the congruence arguments rule out every Type B triple under their exact order/offset hypotheses, irrespective of the size of its entries. Independent finite residue-table checks support, but do not replace, the proofs.

**Proved existence in specified families:** the documented exact integer seeds, Pell amplifications and other constructions give genuine Type B solutions, in several cases infinitely many, with index positivity and integrality checked. These results are stronger than mere local compatibility.

**Proved structural reductions and uniform target-ray families:** for the recurring $k=16m+4$, $c=2$ anchor, the Pell and ideal-theoretic work identifies the conductor-sensitive oriented ray-class condition for an appropriate norm-ideal fibre. WP09-029 through WP09-031 compute the ray arithmetic for all odd square conductors; WP09-032 constructs target-class ideals for powers of three, and **WP09-033 extends the exact construction to all 3/5/7-supported conductors**, including mixed prime powers. These yield infinitely many positive Type B triples in each corresponding family.

**Not yet established:** a complete parameter-wide characterization of when those norm-ideal fibres contain the target ray **outside the proved 3/5/7-supported family**; a general local-to-global theorem for Type B; analogous classification for Types A and C; external priority or independent MATHCERT certification. The separate unrecovered original 2025 source remains a documentary fidelity obligation, not a theorem-proof substitute.

**Why this matters:** [the original bounded census](FIGURATE_CENSUS.md) asked what occurs below a finite cutoff. The next results proved infinite families of *impossibility* and *existence*. The ray-class machinery explains the **shape of a global obstruction**, while WP09-032 and WP09-033 constructively **overcome it across infinitely many prime-power and mixed-conductor parameter families**. The next payoff is a prime-general realization criterion or an actual global obstruction for another well-defined family. The [overview](FIGURATE_PILOT_001.md) describes this research end-game and the distinction between a completed bounded work package and a completed classification.

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
- [WP09 modulo-25 global obstruction and exact finite certificate](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_MOD25_GLOBAL_OBSTRUCTIONS_003.md)
- [WP09 uniform odd-prime-square obstruction theorem](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_UNIFORM_ODD_PRIME_SQUARE_005.md)
- [WP09 complete criterion for all odd prime powers](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_ALL_ODD_PRIME_POWERS_COMPLETE_006.md)
- [WP09 local CRT and exact Euler/Pell families](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_CRT_AND_EXACT_PELL_007.md)
- [WP09 general Pell amplification and finite square-entry extensions](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_PELL_AMPLIFICATION_DICHOTOMY_008.md)
- [WP09 generalized first-pair Pell amplification and seed frontier](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_GENERAL_FIRST_PAIR_PELL_013.md)
- [WP09 global existence at polygonal-minus-one offsets](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_GLOBAL_SEED_EXISTENCE_009.md)
- [WP09 global existence at polygonal-minus-square offsets](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_SQUARE_SHIFT_GLOBAL_EXISTENCE_010.md)
- [WP09 binary non-diagonal anchor gap and exact Type B counterexamples](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_NONDIAGONAL_ANCHOR_GAP_011.md)
- [WP09 oriented ideal-norm/ray-class criterion, protected research PR #1224](https://github.com/grandchallenge/MATHSOLVE/pull/1224)
- [WP09 exact norm-ideal enumeration and targeted class decision (WP09-028)](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_IDEAL_RAY_ENUMERATION_028.md)
- [WP09 full finite oriented ray kernel (WP09-029)](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_RAY_KERNEL_029.md)
- [WP09 complete narrow Picard groups for odd square conductors (WP09-030)](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_SQUARE_CONDUCTOR_PICARD_030.md)
- [WP09 full oriented ray groups and invariant factors for odd square conductors (WP09-031)](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_FULL_RAY_GROUP_031.md)
- [WP09-031 independent exact group tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_full_ray_square_conductor_031.py)
- [WP09-032 uniform 3-power oriented-ray realization and infinitely many exact Type B triples](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_POWER3_GLOBAL_SEEDS_032.md)
- [WP09-032 exact construction and independently verified regression tests](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_power3_global_seeds_032.py)
- [WP09-033 uniform mixed 3/5/7 conductor target-ray realization and proof](https://github.com/grandchallenge/MATHSOLVE/blob/main/work_packages/FIGURATE_WP09_MIXED_CONDUCTOR_REALIZATION_033.md)
- [WP09-033 exact construction and independent matrix/discriminant regressions](https://github.com/grandchallenge/MATHSOLVE/blob/main/tests/test_figurate_wp09_mixed_conductor_realization_033.py)
- [Exact modulo-32 certificate and independently checked witnesses](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp08_mod32.py)
- [Exact modulus-16 classifier](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp08_mod16_classification.py)
- [Source-critical bibliography](FIGURATE_SOURCES.md)
- [Active successor WP09](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3145)

**Publication status:** an internally admitted mathematical exposition, not a peer-reviewed article, a public mathematical certification, or a claim of priority.
