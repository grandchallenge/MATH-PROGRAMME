# Erdős #248 — source-critical adversarial review 001

**Review disposition:** PASS for the exact, weaker, formal Erdős #248 statement about distinct prime factors. **No** independent reconstruction, certification, or theorem-level verification of the stronger published Tao–Teräväinen result is claimed. The source-to-paper correspondence is only partially established, and a promised external author proof map is absent.

**Review identity and limits.** This is a GCL role-scoped adversarial review of an externally authored Lean development; it is not a distinct human reviewer, a MATHCERT examination, an independently written mathematical proof of all analytic estimates, or another computer execution. Logical Verifier, Cartographer, Adversary and Referee passes share the same authenticated operating identity. They must not be counted as separate human attestations.

## Exact sources and custody

- Reviewed repository: plby/lean-proofs, immutable commit **8822f7ddef30fadbd92e1c6ab4ed897af356af5e**, top-level file src/latest/ErdosProblems/Erdos248.lean, Git blob **166659f39a435831d1a751718f9a385effcd7dfa**, SHA-256 **292041372e8f0e45a2ac06fb78dafc32d79cdc4638253139ea4f495a3334a267**.
- Pin: 40 imported local Erdős248 modules, **16,369 lines**. Reproducible ordered bundle digest **7a4e16be1ef119996a7e3ee773a6a9abb0e6c041791565e679cab8cf1c28f815**. Its construction is SHA-256 of the concatenation, over sorted paths relative to the pinned checkout, of eight-byte big-endian path length, UTF-8 path, eight-byte big-endian file length, and exact file bytes.
- Formal target: google-deepmind/formal-conjectures at **85f863718beeec7b58a3a1926ee92e3472bc2020**, FormalConjectures/ErdosProblems/248.lean, Git blob **b80827cbaaf0da740901def1606e36f770d43756**. This is the original statement-only conjecture entry, whose own proof uses a placeholder; it is **not** the source of the GREEN proof.
- Published comparator: Tao and Teräväinen, *Quantitative correlations and some problems on prime factors of consecutive integers*, arXiv **2512.01739v2**, 25 April 2026, Theorem 1.1 and Section 2. URL: https://arxiv.org/html/2512.01739v2 . Historical problem statement: https://www.erdosproblems.com/248 .
- Kernel computation: MATH-PROGRAMME protected replay parent **1cf3b6d6a6f9ebcb53e032a2475e6257467f451c**, worker SHA-256 **2ca052173ee689533f2bc1d2594c503a036fcb146f7c41bd43e7e8c986361f7f**, Lean 4.33.0, Mathlib **db584cd6d46c92f209a44c0f1c829460d327499d**, full receipt SHA-256 **708fb9a104231e8d6a07f425226808a26c4a0227239a50ea139cb2777cd78f28**, full compressed log archive SHA-256 **def278ff642df48c17787d4d5c0fdbfd671138b63728b66a9105f3ac7d450e08**. Both objects are preserved on protected main through PR #3432, merge **a55255f01b18139ddf045d4c82fb566c3e77f36d**.

## Statement-level proof obligation — PASS

The external source declares Erdős248.erdos_248, with the same proposition as the Formal Conjectures entry, and proves it by reference to the separately imported erdos248_resolved. The independent Lean audit observed exactly:

$$
\exists C\in\mathbb R,\quad C>0
\ \land\
\left\{n\in\mathbb N:
\forall k\in\mathbb N,\ k\geq1\Longrightarrow
\omega(n+k)\leq Ck\right\}
\text{ is infinite}.
$$

The actual Lean type printed ArithmeticFunction.cardDistinctFactors for omega. In the pinned Arithmetic.lean, omega_eq_primeFactors_card equates this to the size of the distinct-prime-factor set. It does **not** mean the sum of prime-factor multiplicities.

Adversarial quantifier challenges:

1. **One fixed constant rather than a different constant per shift:** the existential constant is outside the infinite-set property and outside the universal shift quantifier. The final assembly selects one natural threshold T before any analytic dimension K or shift k. It takes C = 2T + 102, with C positive. The maximum of the uniform medium and large thresholds is fixed once.
2. **One witness satisfying all shifts rather than a different witness for each shift:** Extraction.lean proves that total bad-event weight strictly below total positive sieve mass produces a single integer avoiding every bad shift in a finite range. An elementary size bound then extends this same integer to every larger shift.
3. **Infinitely many positive witnesses:** the theorem states infinitude in the naturals. Removing zero cannot destroy infinitude. FinalReduction.lean more directly produces a witness above every prescribed natural lower bound.
4. **Zero and indexing edges:** only k at least 1 is required, so n + k is positive. There is no accidental k = 0 obligation. All three shift regimes, 1 through K, K+1 through the interval exponent, and beyond the interval exponent, are covered.
5. **Uniform constant independent of a large cutoff:** FinalReduction.lean selects K beyond any prescribed bound only *after* the uniform tail constant has been fixed. The required normalization condition is then proved using the all-endpoint Wirsing bound and sufficiently large K.

These checks reject the common invalid replacements with a constant dependent on k, with a witness dependent on k, with merely finite simultaneous shifts, or with a bounded rather than infinite supply of n.

## Logical source-to-proof crosswalk — PASS for the stated formal target

The following is a **new reviewer crosswalk**, not the missing author Leanization map.

| Formal source | Verified interface and mathematical function | Published comparator |
| --- | --- | --- |
| Core.lean; Arithmetic.lean | Defines the exact good/bad predicates, computes omega from the prime-factor finset, establishes the large-shift binary estimate and infinitude from arbitrarily large witnesses | Theorem 1.1 statement and Section 2 initial union-bound reduction |
| Scales.lean; Weight.lean | Sets the dyadic endpoint x(K) = 2 raised to the interval exponent, defines pre-sieve modulus, Y coefficients, nonnegative squared sieve weight and sieve mass | Section 2.2, near-shift scales and weighted Selberg/Maynard sieve |
| Normalization.lean; NormalizationBounds.lean; Mass.lean; SieveMassBounds.lean | Uses the imported all-endpoint Wirsing theorem, establishes regular dimensions and a strictly positive sieve mass despite cross-corrections and finite interval errors | Section 2.2 normalization, sieve-mass lower bound |
| EventMass.lean; Correlation.lean; CorrelationBounds.lean; PrimeTransform.lean | Reduces weighted divisibility events to finite residue/sieve-coefficient expansions, with near/far event estimates | Section 2.3 through Section 2.7, prime-event correlations |
| MediumEventMass.lean; MediumMoment.lean; MediumSharpEnergy.lean; MediumSharpEventMass.lean; MediumTail.lean | Establishes a uniform weighted second moment of medium distinct-prime counts and derives one fixed threshold for the medium exceptional event | Section 2.1 medium-prime second-moment step |
| LargeMoment.lean; LargeRangeMoment.lean; LargeTail.lean | Establishes centered fourth-moment bounds for near/far large distinct-prime counts, then obtains one fixed large-prime threshold | Section 2.1 large-prime fourth-moment step |
| PrimeRanges.lean; BadMassAssembly.lean; TailAssembly.lean | Splits distinct primes into tiny/small, medium, large, and very large ranges; bounds total weighted bad-shift mass and combines both thresholds | Section 2.1, prime-range and summable-tail assembly |
| Extraction.lean; FinalReduction.lean | Weighted finite union bound yields one simultaneous witness; beyond the interval exponent the elementary omega bound controls all shifts. K can grow without bound | Section 2 beginning, probability less than one and arbitrarily large n |

The exact last theorem is TailAssembly.lean:144, erdos248_resolved. It calls exists_uniform_mediumPrimeBadMass_tail (MediumTail.lean:458) and exists_uniform_largePrimeBadMass_tail (LargeTail.lean:21), then takes a common threshold. BadMassAssembly.lean:169 bounds the total bad-shift weight via two tails, each at most one-sixteenth of the sieve mass times the reciprocal square of the shift. For positive total sieve mass, the total is at most one quarter of that mass, which is strictly less than the mass. Extraction.lean:89 handles remaining shifts, and FinalReduction.lean:48 handles arbitrarily large endpoints. These are proved Lean theorems, not new axioms or permanent hypotheses of the final theorem.

The exact choice of powers of 2 and 100 in Scales.lean is different from the paper's continuously varying large x. It suffices for the *existence of infinitely many n*: a sparse unbounded sequence of x is adequate. This does not by itself establish the stronger paper estimate for every sufficiently large x.

## Comparison to the published stronger theorem — essential limitation

Published Theorem 1.1 (arXiv v2, Section 1.2) bounds both the number of distinct factors and the number counted with multiplicity:

$$
\omega(n+k)\leq\Omega(n+k)\leq Ck.
$$

The pinned Lean statement instead establishes only the left-hand target:

$$
\omega(n+k)\leq Ck.
$$

For any positive integer m, write its prime factorization as a product of powers with exponents at least 1. Every distinct prime factor contributes one to omega and at least one to Omega, so omega(m) is at most Omega(m). Because n+k is positive, this implication applies here without an exceptional zero case.

Thus the **published result implies** the formal Erdős #248 target, but the **formal target does not imply** the published multiplicity bound. The precise direction is important. No argument in this review upgrades a bound on omega to a bound on Omega.

The published sieve construction uses square-divisibility information at tiny primes and a fourth axiom controlling higher prime powers. Arithmetic.lean explicitly notes that a single primorial divisor suffices for omega, and the reviewed development works with distinct-prime events. Consequently, the absence of a formal prime-power axiom (iv) is an acceptable simplification for the weaker formal problem, **not** a formal reconstruction of all of Section 2 or the divisor-function consequence. Do not describe this as a kernel verification of the paper's full Theorem 1.1.

## Trust, dependency and compatibility audit — PASS with custody limits

The exact fourth run compiled **8,918/8,918 jobs**. The separate Lean #check confirmed the final type, and #print axioms reported exactly **propext, Classical.choice, Quot.sound**, with no sorryAx. Every one of the 60 archived stage-output SHA-256 digests matched the receipt. All nine upstream-declared compatibility patch checks and applications succeeded, and the original Lake dependency manifest byte identity and pinned commits were preserved.

Direct static inspection covered all 40 local Erdős248 modules (16,369 lines). No executable axiom declaration, sorry, admit, sorryAx, unsafe declaration, opaque declaration or partial declaration was found. Three literal occurrences of the word “constant” at the beginning of a line belong to explanatory comments, not Lean declarations. The imported BoundedGaps and Mathlib results are **dependencies of a kernel-checked proof**, not a mathematical independence attestation.

Patch provenance is nontrivial. The nine frozen patches alter four dependency checkouts and include large edits outside Erdős248. In particular, the Hasse–Weil AINTLIB patch adds proof-level declarations. The review confirms the patched executable source was checked by the Lean kernel and **none of the nine patches directly edits an Erdős248 source file or adds an explicit forbidden axiom token in its added lines**. It does **not** certify that the patched dependencies are textually or mathematically identical to their unpatched upstream versions. This is the correct identity of the actual replay.

## Explicit falsification and residuals

- **Falsification target: quantifier drift.** Rejected by exact final declaration, the uniform threshold order, and a successful #check; no drift observed.
- **Falsification target: hidden analytic assumption discharged by an axiom.** Final theorem has no such hypothesis, and #print axioms reports only the three allowed foundational axioms. No unexpected axiom was observed.
- **Falsification target: empty/zero sieve weight.** The reduction depends on sieveMass_pos, which is proved from the diagonal lower bound and an explicit error bound in Mass.lean and SieveMassBounds.lean, not supplied as a final hypothesis.
- **Falsification target: shift gap.** Near shifts and far shifts are handled by the moment estimates. Shifts beyond the chosen exponent are controlled by the independent elementary bound in Arithmetic.lean and Extraction.lean.
- **Falsification target: mixing omega with Omega.** **Material scope mismatch** to the stronger paper result, but no mismatch to the original Erdős #248 conjecture.
- **Falsification target: undocumented proof correspondence.** **Outstanding documentary defect.** Top-level source explicitly refers to tex/248.tex as its detailed mathematical proof and Leanization map. Exact GitHub directory and pinned checkout inspection found no tex/248.tex at commit 8822f7ddef30fadbd92e1c6ab4ed897af356af5e. The root Erdős248.md contains only a pointer to the Lean module. This new review crosswalk does not replace an absent author-supplied fine-grained map.
- **Falsification target: claiming a new independently derived sieve proof.** Not met. Reviewing the key theorem interfaces and checking the complete Lean kernel dependency is different from independently reconstructing every technical inequality across 16,369 local lines and external Maynard/analytic dependencies. This review makes no such assertion.

## Decision and admissible next state

**Adversarial source-semantic decision:** PASS, **limited to the exact Erdős #248 omega theorem**, the end-to-end source-locked Lean proof chain and the listed critical boundary checks. This qualifies a role-scoped adversarial review of an externally authored formal theorem; it does not independently reprove the complete sieve analysis or certify the paper's stronger Omega result.

**Open obligations:** (1) explain or replace the missing author Leanization map without passing this reviewer crosswalk off as its original; (2) if GCL intends to claim equivalence to the *full* published theorem, formalize and verify the prime-multiplicity part separately; (3) give this qualified result a distinct internal Referee adjudication and protected readback; (4) reserve any external/public mathematical certification to MATHCERT. Until then, keep work status IN_PROGRESS, certification NOT_SUBMITTED, internal adjudication PENDING, protected evidence-admission stage PENDING, and issue #3204 OPEN.

**Outcome classifier:** QUALIFIED_ADVERSARIAL_PASS_OMEGA248_ONLY__FULL_PAPER_OMEGA_NOT_FORMALIZED__PROMISED_AUTHOR_MAP_ABSENT.
