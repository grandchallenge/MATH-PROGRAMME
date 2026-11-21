# The November 2026 Riemann Hypothesis announcement

**A source-critical, Chaidez-style guide to the Alpöge–Claude Lean submission**

!!! warning "Status at 2026-11-20 22:05 UTC"
    **Result status:** external proof claim with substantial independently reported formal-check evidence; **not** a GCL-certified RH or GRH theorem.
    
    **Strongest supported conclusion:** Andrew Sutherland's MIT verification record reports that all 175,187 Lean modules compiled, module-level kernel replay passed, the five main theorems use only the three standard axioms, two further kernels accepted the exported proof, and a separately implemented statement comparator accepted the five challenge statements.
    
    **Not claimed:** GCL has not independently reproduced these checks, completed a source-lock and license audit, understood the 17-million-line proof, issued MATHCERT certification, or declared the classical Millennium Problem closed.
    
    **Support route:** external formal-proof replay and independent-check reports, **not local GCL formal proof**.
    
    **Foundational profile:** classical Lean 4 / Mathlib mathematics; exact definition and trusted-kernel reconciliation remain an explicit GCL audit obligation.
    
    **First executable step:** hash and admit the announcement and original 14-part archive into MATHFORGE; freeze the exact Lean, Mathlib, and toolchain revisions; independently compare the five declarations with GCL's RH-001 statement interface.

**GCL research-surface authority:** **LIVE** — [RH-001 tracker](https://github.com/grandchallenge/MATH-PROGRAMME/issues/163); **AUTHORITY** — [protected RH-WP00 audit](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/RH-WP00-source-normalization-equivalence-audit.md), [RH-R080 protected state](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/rh_001_authority_transition_r080.json), and the canonical protected campaign registry; **EXPOSITION** — this page. This page does not change any of those authority records.

**Computational companion:** [Run the Wolfram Language exhibits](../assets/wolfram/rh_pedagogical_exhibits.wl). They reproduce the finite examples and check the exact algebra below; they neither replay the submitted Lean proof nor establish RH.

## 1. The object: what would RH actually say?

Prime numbers occur in a pattern that seems irregular locally but has a global analytic structure. Riemann's zeta function is a device for translating statements about primes into statements about the zeros of a complex function.

The classical Riemann Hypothesis says that every zero of the analytically continued zeta function in the critical strip lies on its middle line:

$$
\zeta(s)=0,\qquad 0<\Re(s)<1
\quad\Longrightarrow\quad
\Re(s)=\frac12.
$$

This is a statement about **all** such complex numbers, not about the first billion or trillion zeros. A related Dirichlet GRH asks for the same critical-line phenomenon for the Dirichlet $L$ functions of characters. In this announcement, **GRH refers to the Dirichlet family**. Broader Artin, Dedekind, or other extensions are not established by the five headline declarations reviewed here.

### Wolfram exhibit A: five known zeros, not all possible zeros

The following are the imaginary parts $t$ of five known zeros $s=\tfrac12+it$, evaluated with Wolfram Language's [`ZetaZero`](https://reference.wolfram.com/language/ref/ZetaZero.html):

| Known zero | Height $t$ |
| --- | ---: |
| 1 | 14.134725 |
| 2 | 21.022040 |
| 3 | 25.010858 |
| 4 | 30.424876 |
| 5 | 32.935062 |

These samples help locate zeros in the complex plane. The `ZetaZero` computation **enumerates known zeros on the critical line**: it does not certify that no other zeros occur elsewhere in the strip. Finitely many values cannot establish a universal assertion.

The author [reports](https://alpo.ge/remark.pdf) that a collaboration with Claude produced formal arguments for RH and Dirichlet GRH. The four-page note is **an account of the discovery**, not a conventional readable proof. It points to [14 original Lean archive parts](https://alpo.ge/lean.tar.gz.part01). The author explicitly anticipates a later, shorter mathematical exposition.

## 2. The exact obstruction: symmetry does not force a zero onto the line

The functional equation and complex conjugation make the zeta zeros symmetric. A hypothetical zero off the critical line would have reflected companions. **Symmetry alone does not exclude such a configuration.**

The finite set

$$
S=\left\{\frac13,\frac23\right\}
$$

is unchanged under reflection $x\mapsto1-x$, yet neither element equals $1/2$. Thus an argument that only pairs zeros by reflection cannot prove RH. One needs an extra mechanism that rules out an entire off-line pair (or quartet), not merely an explanation of why the pair is mirrored.

This small example is a **working model**, not a counterexample to RH. It identifies the missing logical force in a common naive route.

### Wolfram exhibit B: an exact four-zero countermodel

The symmetry obstruction survives even when complex conjugation is included. Consider

$$
P(s)=\left((s-\tfrac13)^2+4\right)
     \left((s-\tfrac23)^2+4\right).
$$

Its zeros are $\tfrac13\pm2i$ and $\tfrac23\pm2i$, **all off the critical line**. Yet it has real coefficients and satisfies the exact identity $P(s)=P(1-s)$. Its zero set therefore has both reflection and conjugation symmetry.

Wolfram symbolic algebra also verifies that, for every real $t$,

$$
P(\tfrac12+it)
=\left(\tfrac{145}{36}-t^2\right)^2+\frac{t^2}{9}
>0.
$$

Thus **even those two symmetries together do not force zeros onto the line**. This is a proved fact about the explicit polynomial, **not** a counterexample to RH: $P$ is not the zeta function. [Reproduce the exact checks](../assets/wolfram/rh_pedagogical_exhibits.wl).

## 3. The working model: multiplicity as a resource

The announcement's proposed mathematical narrative begins with an analogy to **Stepanov's method over function fields**, where vanishing with multiplicity is a powerful tool for bounding zeros or arithmetic points. Over integers, one cannot simply differentiate integer arithmetic to obtain the same multiplicity device.

The author reports searching for an arithmetic analogue built from determinants, Fourier analysis, and **iterated theta lifts** between automorphic representations. In the note's description, each successive lift plays a role analogous to an additional order of vanishing. For a von Mangoldt sum of length $X$, the proposed chain length is of order

$$
m\asymp\sqrt X.
$$

The note also refers to positivity and sign arguments, weighted von Mangoldt sums, Guinand–Weil, periods and seesaw identities, Bost slope inequalities, Iwasawa towers, arithmetic divisibility, and a calculation of the cost of each lift.

### Wolfram exhibit C: from prime powers to the announced weighted sum

The *von Mangoldt function* $\Lambda(n)$ equals $\log p$ when $n$ is a positive power of a prime $p$, and zero otherwise. The simpler cumulative sum

$$
\psi(X)=\sum_{n\le X}\Lambda(n)
$$

is a staircase with a jump of $\log p$ at every prime power $p^k$. For positive integer $X$, an exact identity makes this concrete:

$$
\psi(X)=\log\bigl(\mathrm{lcm}(1,2,\ldots,X)\bigr).
$$

The [announcement](https://alpo.ge/remark.pdf) discusses a more specific **weighted and centered** sum. For integer $X\ge1$, denote its displayed arithmetic expression by

$$
F(X)=\sum_{n\le X}\Lambda(n)
\left(\frac{X}{n}-1\right)
-X\log X+(1+\gamma)X,
$$

where $\gamma$ is the Euler–Mascheroni constant. A Wolfram Language calculation using [`MangoldtLambda`](https://reference.wolfram.com/language/ref/MangoldtLambda.html) gives:

| $X$ | $\psi(X)$ | $F(X)$ |
| ---: | ---: | ---: |
| 10 | 7.832014 | 1.860798 |
| 20 | 19.265658 | 1.861944 |
| 50 | 49.485381 | 1.879515 |
| 100 | 94.045311 | 1.721687 |

The table distinguishes **what is elementary and directly calculable** from what the proposed argument would need to prove about such sums. Four positive values of $F(X)$ do not establish positivity for every $X$, an analytic bound, a theta-lift construction, or RH. [Reproduce all four rows](../assets/wolfram/rh_pedagogical_exhibits.wl).

These are **source-attributed route descriptions**, not independently derived lemmas on this page. In particular, the short note does not supply the inequalities, constants, conductor bookkeeping, or bridges needed to reconstruct its proof from prose alone. A successful mechanical check of the Lean source is a different form of evidence.

**Intuition:** Imagine an ordinary sieve that removes candidates one at a time. The claimed construction attempts to manufacture a stronger sieve whose successive stages accumulate constraints. The difficult question is not merely whether each stage helps, but whether the accumulated gain outweighs the cost of adding stages. The note attributes the needed gain to automorphic lifts and intricate arithmetic identities. This analogy teaches the target mechanism; it is not a proof.

## 4. The restricted claim we can actually inspect

A [byte-mirrored, third-party source snapshot](https://github.com/Deicyde/riemann-hypothesis/blob/e50d09817ad81469f737e8f637561e6ccf86c670/src/Main.lean) displays five headline declarations. Among them:

```lean
theorem riemannHypothesis : RiemannHypothesis := rhOfAll
theorem LFunction_eq_zero_re : DirichletLZerosOnLine := claimAll.2.1
```

The mirror's [`Statements.lean`](https://github.com/Deicyde/riemann-hypothesis/blob/e50d09817ad81469f737e8f637561e6ccf86c670/src/Statements.lean) contains explicit Dirichlet $L$ function claims. The first headline theorem uses Mathlib's own `RiemannHypothesis` definition, not a newly defined local proposition bearing an impressive name.

These observations identify the formal targets **as displayed in the external mirror**. GCL has read these declarations but has **not independently established byte identity of the mirror against the original author's archive**. The [MIT verification record](https://math.mit.edu/~drew/grh/) reports that the source archive and one mirror agree under the recorded hash.

## 5. Where the claim sits on GCL's theorem spine

| Node | Role | Present status | Advancement criterion |
| --- | --- | --- | --- |
| RH-A26-SOURCE | External source lock | **Pending local admission** | Hash and retain PDF and all original archive parts; check rights, exact toolchain, provenance |
| RH-A26-STATEMENT | Formal-to-human semantic bridge | **Externally checked, locally pending** | Compare RH and Dirichlet GRH definitions, assumptions, quantifiers and exception cases with protected RH-WP00 |
| RH-A26-REPLAY | Mechanical proof validation | **Externally reported passing** | Repeat a bounded independent audit on locked original bytes; retain exact logs, verifier identities, and toolchain revisions |
| RH-A26-MECHANISM | Human mathematical reconstruction | **Open** | Produce a readable dependency skeleton and prove selected analytic/arithmetic bridging lemmas |
| RH-A26-GCL-CERT | GCL claim disposition | **Not issued** | GCL-controlled evidence, non-author adjudication under current policy, and a scoped MATHCERT decision |

This is an **incoming candidate spine**, not a promotion of GCL's existing RH-001 route. The established RH-R080 result concerning signed-projective normality remains its own bounded result; it does not automatically validate or refute the new submission.

## 6. What independent checkers have actually reported

Andrew Sutherland's [MIT verification dossier](https://math.mit.edu/~drew/grh/), last updated **20 November 2026, 22:05 UTC** at the time of this edition, reports:

| Check | Reported result | Meaning and limit |
| --- | --- | --- |
| Lean 4.33.1 / Mathlib 4.33.1 source | 175,187 modules compile | No compilation errors for the examined source; compilation itself is not semantic reconciliation |
| Five theorem axiom audit | `propext`, `Classical.choice`, `Quot.sound` only | No nonstandard axioms reported for the headline theorems |
| Lean `leanchecker` | All modules accepted | Independent replay through the Lean kernel |
| Independent `nanoda` kernel | Full export accepted | Strong additional evidence against implementation-specific checking errors |
| Independent `con-leche` kernel | Full export accepted | A second implementation accepted 1,468,418 declarations |
| `con-leche --compare` | Five challenge statements accepted | The formal targets match that independent comparator's challenge definition |
| `lean4lean` | All compiled modules accepted | Separate formal checker; five modules required increased checking limits |
| Official `lake comparator` and separate Lean export replay | **Still running** at edition time | No completion claim may be inferred from the other successful checks |

This is exceptionally substantial **external proof-check evidence**.

The MIT record identifies the 14-part assembled original source as 239,275,554 bytes, SHA-256:

```text
9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc
```

This digest is **quoted from the MIT record**, not a digest independently recomputed by GCL in this edition. The public four-page PDF has been read visually and textually; local byte-retention and hashing remain pending. The [State of Proof intake](https://stateofproof.org/paper-watch/paper-2026-11-20-a-claimed-proof-of-the-riemann-hypothesis) independently reports PDF SHA-256 `3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d`, also **not yet GCL-recomputed**.

## 7. The debt audit and the trust quartet

**What is proved?** GCL makes no new theorem claim in this publication. The standard mathematical definitions and simple reflection countermodel above require no claim of RH. The submission asserts proofs of classical RH and Dirichlet GRH.

**What is checked?** An MIT-hosted verification dossier reports successful compilation, standard-axiom audit, full Lean and independent-kernel replay, and statement comparison. GCL has inspected the PDF and headline declarations, but no original-code replay is claimed here.

**What remains open?** Whether GCL can reconstruct the original bytes, independently validate the entire dependency closure, and explain the proof's decisive mathematics in a readable form; the status of the still-running MIT checks; and a scoped MATHCERT disposition.

**What requires external verification?** The third-party check logs and their exact-source provenance, remaining independent checking results, mathematical review of the major steps, and any external scientific or prize-process acceptance.

The active proof-debt register is:

| ID | Class | Exact obligation |
| --- | --- | --- |
| RH-A26-D01 | EXTERNAL_SOURCE | Acquire/hash the original PDF and 14-part archive; record source identity, licensing and downstream redistribution limits |
| RH-A26-D02 | SEMANTIC_CORRESPONDENCE | Prove the statement bridge from the five Lean theorems and imported definitions to GCL RH-WP00 and Dirichlet GRH |
| RH-A26-D03 | COMPUTATIONAL_REPLAY | Independently re-execute selected axiom, kernel, and statement checks on the pinned original code with retained receipts |
| RH-A26-D04 | FORMALIZATION_BLOCKER | Confirm dependency imports, metaprogramming paths, generated artifacts, compiler flags, and possible trust-bypass mechanisms |
| RH-A26-D05 | MISSING_LEMMA | Reconstruct a readable theorem spine for theta lifts, accumulated multiplicity, arithmetic cost, and the final critical-line inference |
| RH-A26-D06 | FOUNDATIONAL_PROFILE_GAP | Record exact classical foundations, imported Mathlib definitions, and their equivalence to the intended analytic objects |
| RH-A26-D07 | EXTERNAL_SOURCE | Track formal and mathematical follow-up by the author and independent reviewers, without importing status automatically |

**Downgrade rule:** any source-hash mismatch, nonstandard hidden assumption, semantic mismatch, untrusted proof shortcut, or independent checking rejection reopens the relevant node. A failed or incomplete verification attempt is not, by itself, a mathematical refutation.

## 8. Contextual consequences for GCL

**MATHFORGE / RH-001.** Treat this as the highest-priority new **external source-and-claim intake** for the RH campaign. Preserve the old campaign's protected claims and blockers until a separate governed transition. Do not rename an external announcement "GCL solved RH."

**MATHCERT.** The crucial workflow is **source fidelity → proposition fidelity → kernel/proof replay → theorem-scope adjudication**. Compilation and a small axiom list are important but not a substitute for the whole chain. The reported independent kernels make the submission unusually strong; those reports should be ingested as attributed evidence.

**GLOSS / mathematical accessibility.** The author says the argument lacks a manageable human exposition, and the published formal corpus is approximately 17.4 million lines. This is a concrete stress test for theorem-dependency compression and semantics-grounded explanation: extract the five statements, a minimal dependency spine, and human commentary with explicit loss labels. A fluent generated explanation is not an independent proof.

**OAI26 Family 003.** RH, if ultimately admitted as a genuine theorem, would imply broad consequences exceeding a seven-eighths-type zero-free statement. It would **not retroactively prove the particular Gaussian-energy inequalities or exact natural-family obligations** in OAI26, nor establish that unrelated formal artifacts mean what their source statements mean. Preserve the original proof debts while assessing logical consequence separately.

**Agentic mathematics / AETHER.** The account credits a human collaborator with choosing structural analogies and an AI with substantial mathematical innovations. This raises a useful practical test: can GCL preserve role attribution, source lineage, proposal history, independent checking, and public explanation when neither partner possesses a short understanding of the final formal corpus? These are research and institutional implications, not evidence about AI autonomy or a general guarantee that AI-generated proofs are correct.

## 9. First executable move

**RH-A26-WP00 — source-locked statement concordance**, owned by MATHFORGE with an RH-001 MATHSOLVE handoff only after reviewed source semantics.

**Input:** the exact `remark.pdf`; the 14 original archive parts; `Main.lean`, `Statements.lean`, the complete dependency manifests, Lean 4.33.1, Mathlib 4.33.1, and the dated MIT verification report.

**Bounded output:** one immutable source manifest, five declaration-level statement cards, a side-by-side comparison with protected RH-WP00, a list of assumptions and imported definitions, an audit of syntactic shortcuts and metaprogramming, and an independent-replay evidence matrix.

**Acceptance test:** all five formal targets identified by pinned path and hashes; equivalence or precise mismatch established for each intended human target; all source bytes and toolchain versions accounted for; external check results preserved as *external*; no certification or proof claim inferred from an unchecked dependency.

**Stopping condition:** a specific missing original source object, legal redistribution boundary, semantic mismatch, or reproducible checking failure. Otherwise continue toward selective independent replay and readable theorem-spine reconstruction.

**Challenge ladder for readers:** (a) verify the reflection example; (b) read Mathlib's `RiemannHypothesis` definition; (c) compare it with the classical critical-strip formulation; (d) read the five Lean declarations; (e) classify each externally reported check by what it actually establishes; (f) pick one source-named analytic lemma and attempt a direct mathematical reconstruction.

---

### Sources and edition limitations

- [Primary four-page announcement, 20 November 2026](https://alpo.ge/remark.pdf); its original 14-part Lean release is referenced in the PDF's first footnote.
- [MIT independent verification dossier](https://math.mit.edu/~drew/grh/), observed edition 20 November 2026, 22:05 UTC.
- [Pinned third-party source mirror, commit `e50d098`](https://github.com/Deicyde/riemann-hypothesis/tree/e50d09817ad81469f737e8f637561e6ccf86c670), used for inspection, not substituted for the author's original source.
- [Reproducible Wolfram Language companion](../assets/wolfram/rh_pedagogical_exhibits.wl): exact polynomial symmetry/positivity checks, five known zero heights, and finite von Mangoldt sums. These are pedagogical calculations, not validation of the submitted proof.
- [GCL protected RH-WP00](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/RH-WP00-source-normalization-equivalence-audit.md), [RH-001 live tracker](https://github.com/grandchallenge/MATH-PROGRAMME/issues/163), [Chaidez Pedagogical Protocol](../CHAIDEZ_PEDAGOGICAL_PROTOCOL.md), and [Claim Boundary Doctrine](../CLAIM_BOUNDARY_DOCTRINE.md).

**Editorial classification:** dated external-source analysis and pedagogical exposition. Neither this edition nor its publication constitutes the mathematical theorem, an independent GCL proof replay, or a change to the current protected RH claim state.
