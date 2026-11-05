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
- [Exact modulo-32 certificate and independently checked witnesses](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp08_mod32.py)
- [Exact modulus-16 classifier](https://github.com/grandchallenge/MATHSOLVE/blob/main/research/figurate_wp08_mod16_classification.py)
- [Source-critical bibliography](FIGURATE_SOURCES.md)
- [Research programme and current status](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3125)

**Publication status:** an internally admitted mathematical exposition, not a peer-reviewed article, a public mathematical certification, or a claim of priority.
