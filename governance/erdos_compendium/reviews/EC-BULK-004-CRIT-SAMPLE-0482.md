# EC-BULK-004 — Erdős #482 deterministic-sample critical review

Receipt: EC-BULK-004-CRIT-SAMPLE-0482  
Reviewed: 2026-10-14  
Authenticated reviewer and author account: fyremael. This is a separate post-draft mathematical/adversarial review under the SAME authenticated identity; it must NOT be represented as a second independent person or independent Lean kernel certification.  
Disposition: **SOURCE_AND_DRAFT_PASS; FINAL_CRITICAL_SAMPLE_FORMAL_REPLAY_AND_RENDER_GATE_PENDING.**

## 1. Original question and status fidelity

Directly inspected Erdős–Graham, *Old and New Problems and Results in Combinatorial Number Theory* (1980), printed p.96, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf#page=92 . It records the already-proved Graham–Pollak 1970 identity for $a_1=1$, $a_{n+1}=\lfloor\sqrt2(a_n+1/2)\rfloor$, $d_n=a_{2n+1}-2a_{2n-1}$, **$n\ge1$**; then asks **open-endedly** for analogous recurrences for other radicals/algebraic numbers. The modern catalogue status SOLVED refers to the existence of wide Stoll generalizations, not to a theorem that the identical formula generates all algebraic expansions or that every conceivable generalization has been classified. A statement asserting the original fixed $\sqrt2$ identity remains open would be false.

## 2. Historical primary proof provenance

**1970:** R. L. Graham and H. O. Pollak, *Mathematics Magazine* **43** (1970), 143–145, original annotated archival scan https://oeis.org/A001521/a001521_2.pdf, inspected ALL three scanned pages; SHA-256 of exact downloaded PDF **67e6f14407a9e7f9f8e06e150aa3e08b5a185ac845f2f9da3376971731b9bb8f**. Theorem at printed p.143, floor and Beatty lemmas at p.144, closing closed formula and explicit binary-digit deduction p.145. For $a_1=m=1$ the auxiliary $\tau=1$ and $a_n=\lfloor2^{(n-1)/2}+2^{(n-2)/2}\rfloor$ for $n>1$. This is FULL PRIMARY SOURCE READBACK, including the actual proof, not a bibliographic assertion.

**2005:** Thomas Stoll, *J. Integer Sequences* **8** article 05.3.2, original 8-page primary PDF https://cs.uwaterloo.ca/journals/JIS/VOL8/Stoll/stoll56.pdf checksum **2a14aeb40cede7985c769e402b0dd7cfb427af3847c1717ad962ac19d4b48313**.

**2006:** Thomas Stoll, *Acta Arithmetica* **125**, 89–100, fully accessible 12-page primary journal PDF https://www.impan.pl/shop/en/publication/transaction/download/product/83728 checksum **1250e33030785630b5e4e6bb8a0556a0376749096c54ca566dcdba8fae909d9f**. Printed p.89 Fact 1 cites the original, p.92 Theorem 3.1 gives $g\ge2,w>0$, explicit admissible sets $D_i$ for integer $(m,l,k)$, divisibility $(g-1)\mid(k-1)l$, exact $a,b,\varepsilon$ interval hypotheses; p.93 Theorem 3.3 recovers original with $(m,l,k)=(1,0,0),w=\sqrt2,a=b=\sqrt2,\varepsilon=1/2$. The article does NOT assert arbitrary coefficients without admissibility restrictions; manuscript is faithful.

## 3. Independent finite and symbolic mathematical review

For the original initial value, the 1970 explicit formula gives for $z=\sqrt2/2$:
$$
a_{2n+1}=2^n+\lfloor2^nz\rfloor,\qquad
a_{2n-1}=2^{n-1}+\lfloor2^{n-1}z\rfloor.
$$
The second formula holds even at $n=1$, using $a_1=1$ and $\lfloor z\rfloor=0$. Therefore
$$
d_n=\lfloor2^nz\rfloor-2\lfloor2^{n-1}z\rfloor
=\lfloor\sqrt2\,2^{n-1}\rfloor\bmod2.
$$
This is the nth bit of $\sqrt2/2=0.101101\ldots$ and the nth bit of $\sqrt2=1.01101\ldots$ **including the leading integer 1**, so $d_1=1$, $d_2=0$. If one instead calls the first digit after the binary point of $\sqrt2$ digit 1, that digit is 0 and the statement is off by one. This is a material edge-case tested both ways.

The integer-only recurrence uses
$$
\lfloor\sqrt2(a+\tfrac12)\rfloor
=\operatorname{isqrt}(\lfloor(2a+1)^2/2\rfloor),
$$
exact for all $a\in\mathbb N$. Five committed tests in tests/test_erdos_compendium_0482_binary_digits.py PASSED at source head **796452a810ffe6e579bc4d88c93dad443c4737ac**:
1. Original first 13 exact terms, first eight digits [1,0,1,1,0,1,0,1] and first fractional-bit trap.
2. Original 1970 closed-form versus independent integer recurrence for **260 terms**.
3. Recovered first **120 binary digits** from recurrence and independent $\operatorname{isqrt}(2^{2n-1})\bmod2$.
4. A separate 320-/400-digit decimal square-root computation confirmed **100 digits**, with both precisions agreeing on each truncation.
5. Prefix reconstruction of $\sqrt2/2$ with **70 bits**.

These are reproducible finite fixtures, not a machine proof of the all-index Graham–Pollak floor lemma or an independent formalization of the entire Stoll theorem family. The algebraic digit extractor is a complete deduction FROM the cited 1970 formula.

## 4. Formal source provenance and exceptions

**Pinned GCL provider:** google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020 has NO FormalConjectures/ErdosProblems/482.lean. **New unpinned upstream source**, Git blob 5075caaf5b08b492962dfed71f6840dc59371d9a, introduces the original digit statement and two generalized statements with **by sorry** placeholders; being tagged research solved or carrying a citation to external code does not make the protected GCL provider complete.

**External purported Lean proof:** gotrevor/lean-gallery@a28a487968d989b24c9dde9b1958aa5b92c6fccb, LeanGallery/NumberTheory/Erdos482/Statement.lean Git blob fcc45fb023539b41120354af209a23edf80539bc, organizes aliases, says only usual Lean axioms after a build, but GCL has **NOT independently checked** the exact transitive imports, Lean/Mathlib pins, axiom readback, theorem definitions, or Stoll parameter hypotheses. Separate generalized proof cite is @a834bbad2f36eedcc16066b2bc4da49f98ab5b85, Statement.lean blob bd7ec82ddfd992ef872c1d1f2e573d45684ea7f5. A future GCL Lean verification must distinguish the two commits and preserve exact source and axioms. Also compare the external \`Real.digits (√2/2) 2 (n-1)\` to original *leading integer digit* indexing. The generalized Stoll theorem has normalization by mantissa $w/g^{\lfloor\log_gw\rfloor}$ and many discrete hypotheses; deleting any would make the source statement overbroad.

## 5. Authenticated source custody and disposition

Original issue #1752 RESULT/1 https://github.com/grandchallenge/MATH-PROGRAMME/issues/1752#issuecomment-6169299792, author fyremael, LF-normalized body SHA-256 **0e6e9ba7924641b4d60ed31fabe2f18f8e23b5d0c7c58cb9bc83292727326203**, disposition SOURCE_LOCK_READY for verified published primary evidence.

Manuscript governance/erdos_compendium/editorial/0482.md has six canonical headings each exactly once, balanced dollar-delimited mathematical text, SHA-256(UTF8(strip)) **27b1e028681a99b4b6f4a98aa8b49c41dbf80fb378e68cabc180992f96645ad7**, raw bytes SHA-256 **7e2b70c32cf7617bd0d6fbc9b62cf6ce947a1d25980b626d69a8354124c81878**. Five exact tests are committed and independently measured PASS; this record is an **adversarial source/sample review**, but not a mathematical certification of the external Lean implementation.

**Decision:** SOURCE_LOCK_READY documentary, ARTICLE_UNACCEPTED_DRAFT critical-source-and-math review PASS, FINAL_DETERMINISTIC_SAMPLE_NOT_YET_FULLY_ADJUDICATED. Next bounded gate: independent GCL Lean replay of the full external pinned files and transitive dependencies, explicit review of general Stoll theorem hypotheses, strict MkDocs and real-browser MathJax readback on the actual future protected production head. No independent human signoff, GCL MathCert, novelty, public deployment or V2 admission is claimed.
