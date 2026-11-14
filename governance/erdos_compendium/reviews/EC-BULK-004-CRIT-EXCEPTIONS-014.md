# EC-BULK-004 — critical mathematical and source review of #471–472

Review receipt: EC-BULK-004-CRIT-EXCEPTIONS-014  
Date: 2026-10-14  
Accountable reviewer identity: fyremael. This is a logically separate adversarial editorial pass by the same authenticated account, **not** a different human reviewer, independent mathematical certification or protected V2 admission.

## Source fidelity and exact theorem boundaries

Both original problems were visually read from Erdős–Graham (1980), printed p.94, PDF zero-based page 89, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf#page=90 . They are two materially different Ulam mechanisms:

- #471: **sets** Q_k, repeatedly adjoin every prime that is a sum of three **distinct** elements already present; asks whether there exists **some** finite successful seed. A separate named example Q={3,5,7,11} is not established by the general answer.
- #472: **ordered greedy sequence** of primes with q_(n+1)=the **smallest prime** q_n+q_i−1 for any 1≤i≤n; asks whether there exists any seed generating an **infinite** sequence. In the named seed (3,5), long finite success and random-primality heuristic are not a proof.

Current maintained entries #471 https://www.erdosproblems.com/471 (PROVED) and #472 https://www.erdosproblems.com/472 (OPEN) match this division; the #472 October 2025 historical note and 2025 forum heuristic were not misclassified as a theorem.

## Mathematical adversarial challenge: #471

The source reduction requires **three pairwise distinct** prime summands, not only three primes with repetitions. Quantitative Vinogradov ternary Goldbach gives ≫N²/(log N)³ representations of a sufficiently large odd N by primes. Repeated-prime triples contribute at most O(N), because the repeated prime determines the remaining entry; hence at least one triple has three distinct primes for sufficiently large odd N. A strong induction on primes p with finite Q₀ containing **all** primes up to that threshold shows all smaller summands appear in bounded generations, so p appears one generation after their maximum generation. This is a valid analytic-input-to-existential-seed reduction, not a reproduced circle-method proof.

Failure mode checked: this argument does **not** produce a specific small threshold or prove the special seed {3,5,7,11} infinite. The manuscript preserves both limits. The first four generation cardinalities for the original named seed are exactly (4,6,12,29), and the first-generation sum enumeration is (15,19,21,23), with only the two prime values retained. The special-seed issue remains a bounded successor.

Primary original p.94 and K. Matomäki, J. Maynard and X. Shao, “Vinogradov's theorem with almost equal summands,” *Proc. London Math. Soc.* 115 (2017), 323–347, DOI 10.1112/plms.12040, are explicitly distinguished from the classical full quantitative theorem used as an external input. No GCL proof certification or independent Vinogradov analytic proof claimed.

## Mathematical adversarial challenge: #472

For the seed (3,5), each step enumerates exactly the finite list q_n+q_i−1, 1≤i≤n, tests actual primality and selects the minimum prime, not an arbitrary one. The exact first 27 terms ending in 109 are reproduced; after 89 the next term is 101, not 97, because 97 would require q_i=9. A distinct seed (5) terminates at once since its only candidate is 9. With odd seed primes ≥3, all candidates are odd and increase strictly by at least 2; this excludes cycles but cannot exclude an all-composite step. The article labels the general existence problem OPEN and does not promote the million-step claim in an unreviewed forum comment.

The $Q_{k+1}$ set closure theorem of #471 has no direct bearing on the q_(n+1) greedy-primality condition of #472. The reduction of both to the same proof would be incorrect.

## Exact provenance and QA status

| Problem | Authenticated issue return | LF-normalized return SHA256 | stripped UTF-8 manuscript SHA256 | Source classification |
| --- | --- | --- | --- | --- |
| 471 | https://github.com/grandchallenge/MATH-PROGRAMME/issues/1741#issuecomment-6166958720 | 83c602a9972bbc102a0b967d5e37db33f4f93f36d16218bf372caf1fe85310fc | 52bd5311bb678055174a22a252356ef90fafb004121f33b5dfdee401563dd908 | SOURCE_LOCK_READY documentary, proof external |
| 472 | https://github.com/grandchallenge/MATH-PROGRAMME/issues/1742#issuecomment-6166998538 | 70c853bbd132e2552485d7003220d086afcff9c734777f728830ec3b4acc05fe | 445a7c4d06042fccf0ffde9b56cd500d9d49be193b23f5382096cd1496ae88f5 | BOUNDED_TASK_DESIGNED open problem |

Original authenticated comment author is fyremael for both, read back with exact IDs and body hashes. Manuscripts: governance/erdos_compendium/editorial/0471.md and 0472.md; each has all six required sections exactly once and balanced dollar-delimited mathematics. Source-specific finite tests: tests/test_erdos_compendium_0471_0472_ulam.py, five tests passed at branch head cb69b1ec0879c96157f41d5b24485316f91a65ac.

**Final full repository pytest, MkDocs, public browser MathJax and protected V2 admission are not attested by this receipt**. They are required separately and must be measured at the final reviewed head.

## Decision

#471: CRITICAL_DRAFT_PASS_DOCUMENTARY, keeping external analytical input and special four-prime seed boundary.
#472: CRITICAL_DRAFT_PASS_OPEN_STATEMENT, keeping unproved infinitude and long-prefix heuristic boundary.

Both remain **UNACCEPTED_DRAFT**. These are additional source- and semantics-risk critical checks, **not** substitutes for the fixed deterministic 20-piece review sample and not GCL MathCert.
