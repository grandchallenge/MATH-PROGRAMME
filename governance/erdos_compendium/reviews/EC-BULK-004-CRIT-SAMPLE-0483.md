# EC-BULK-004 — Erdős #483 deterministic critical-sample review

Receipt: EC-BULK-004-CRIT-SAMPLE-0483  
Observed: 2026-10-14  
Authenticated editorial author/reviewer: fyremael. This is a separate logical/adversarial pass by the **same identity**, NOT independent-person mathematical certification.  
Disposition: **CRITICAL_SOURCE_AND_FINITE_MATH_PASS; FINAL_SAMPLE_PROTECTED_BROWSER_AND_FORMAL_BOUNDARIES_PENDING**.

## Exact quantifier and status fidelity

The historical original was directly read as image pages 232 and 233 of P. Erdős, *Some unsolved problems* (1961), https://users.renyi.hu/~p_erdos/1961-22.pdf#page=13 , Problem 20: f(k) is the FIRST interval length for which all k-colorings of positive integers force a monochromatic x+y=z, including x=y; the problem asks especially if ∃C>0 ∀k≥1, f(k)<C^k, and separately speculates whether f(k)^(1/k) tends to a finite constant. These are different mathematical statements; the latter includes a convergence requirement beyond boundedness of kth roots. Adjacent Turán interval result explicitly assumes x≠y but is NOT the ordinary Schur coloring problem.

Standard literature calls S(k) the LAST length for which a k-coloring avoiding monochromatic sums still exists. Therefore f(k)=S(k)+1. The proper exact thresholds are (2,5,14,45,161) for f(k), versus (1,4,13,44,160) for S(k). The manuscript and original issue return preserve this off-by-one, the positive k≥1 domain, and a=b permitted. **Status remains OPEN**, not a new solution.

## Published primary interfaces and unreplayed claims

R. Ageron, P. Casteras, T. Pellerin, Y. Portella, A. Rimmel and J. Tomasik, *New lower bounds for Schur and weak Schur numbers*, arXiv:2112.03175, primary PDF https://arxiv.org/pdf/2112.03175 version dated 4 April 2022. Definition 2.1 preprint p.3: S-template includes additional wraparound sum-free constraints for all but its special color. Theorem 2.3 preprint pp.3–4 composes templates and partitions. Inequalities (5)–(7) preprint p.6 and Corollary 2.9 p.7 give $S(k+5)\ge380S(k)+148$ and growth base $\sqrt[5]{380}\approx3.28$ FROM BELOW. The paper's complete published lower-bound template certificates and entire 20-page proof have not been independently re-enumerated by GCL. Correct affine conversion is $f(k+5)\ge380f(k)-231$. This is neither the conjectured upper bound nor its negation.

M. J. H. Heule, *Schur Number Five*, *AAAI* (2018) pp.6598–6606, primary PDF https://arxiv.org/pdf/1711.08076 and author certificate page https://www.cs.utexas.edu/~marijn/Schur/ , establishes $S(5)=160$ and $f(5)=161$. The approximately 2-PB SAT proof was verified with the author's certified checking infrastructure but was NOT independently downloaded/replayed by GCL. Thus do not present f(5) as a GCL-certified new calculation.

The maintained https://www.erdosproblems.com/483 revised 10 April 2026 gives **OPEN** status and attributes $f(k)\le(e-\frac16)k!$ to Xu, Xie and Chen (2002), *Upper bounds for Ramsey numbers R_n(3) and Schur numbers*, *Mathematical Economics*, 81–84. This exact original [XXC02] paper and [Er65] 1965 p.188 historical reiteration were NOT directly read. The corresponding attribution is marked catalogue-reported, not independently source-proved. A factorial upper bound is asymptotically larger than every fixed-C exponential; the exponential upper-bound question remains open.

## Independent adversarial exact mathematics

Source-specific test tests/test_erdos_compendium_0483_schur.py **5 PASSED** at source commit bc38d502c8fb26b6e85cb7794d9ef7a1c7cfb441. One exact color-symmetry-reduced DFS checks the constraint on each newly colored n by enumerating all a+b=n, including a=b. It returns witnesses [0,1,1,0] for k=2,N=4 and [0,1,1,0,2,2,0,2,2,0,1,1,0] for k=3,N=13, and proves unsatisfiability for k=2,N=5 (6 search states) and k=3,N=14 (327 states). Canonical new-color naming examines all colorings modulo color-label permutations; the finite search is exhaustive under this symmetry. A **second independent complete enumeration of all 2^5 labeled two-colorings** confirms the k=2,N=5 obstruction. No k=5 full certificate is claimed.

The formal reduction $f(k)\le R(3;k)-1$ is checked: color edges of K_{N+1} on vertices 0..N by color of positive edge difference; for any monochromatic triangle i<j<l, its three differences (j−i,l−j,l−i) satisfy a+b=c and have one color. The direction is only upper bounding f by multicolor triangle Ramsey R, **not** an identity or a lower bound, and known multicolor R(3;k) estimates do not close the fixed exponential conjecture.

Three separate trap fixtures are present: *allowing equal summands* (1+1=2), *upper/lower versus first/last convention* ($f=S+1$), and *Schur templates with all wraparound constraints*. The latter still requires its own certified template check and cannot be inferred from a finite plain sum-free coloring.

## Audit custody, mandatory sample gate and blockers

Authenticated original issue #1753 research return https://github.com/grandchallenge/MATH-PROGRAMME/issues/1753#issuecomment-6179196927, author fyremael, six substantive RESULT/1 sections, disposition SOURCE_LOCK_READY documentary, LF-normalized SHA256 **310f5cfca0ddaa5cd7250b46a18b6f2d525aaf2ccd7a54677f2b56eccb941dd1**.

Six canonical headings in manuscript governance/erdos_compendium/editorial/0483.md occur once each, mathematics uses balanced dollar delimiters, stripped UTF8 SHA256 **1aed914723cb532ba2e65a6885898fae263028cc3767796ae51fb98ccd8ffa79**, raw SHA256 **761d0627795f6de609f140495b1ee27b4512fd80059adf7cec59a72b9d9f9825**.

GCL pinned google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020 **lacks #483**. Unpinned main file FormalConjectures/ErdosProblems/483.lean blob **37042fa62e1cb70657f147a35b84b911a561202c** specifies k-colorings and repeated summands correctly, with trivial one-color tests by decide; general exponential statement still by `sorry`. No independent GCL Lean kernel certification.

Sample source/math reviewing passes under specified limits, but **final deterministic sample acceptance is NOT asserted**: exact-head full pytest, strict MkDocs, genuine browser MathJax public HTML readback, and the source/statement/formal-status adjudication still require protected head receipts. The main conjecture itself is OPEN; no proof of the asymptotic exponential upper bound can be treated as an ordinary editorial gate. Exact 2002 upper-bound proof, full Ageron template witness, and huge Heule proof not independently replayed; no protected PR merge, V2 admission, new theorem/priority or external worker launch.

## Bounded successor

EC004-0483-CERTIFIED-TEMPLATE-AND-SAT: preserve exact 1961 original and 2022 theorem images, independently implement S-template wraparound checker, replay one published example supporting S(k+5)≥380S(k)+148 with a bounded concrete k, and formally prove the generic template composition and $f\le R-1$ implication. Require two independently generated finite k≤3 UNSAT/sum-free checks and explicit leading source hashes. Falsify on a=b exclusion, S/f offset, one wraparound violation, or false Ramsey direction. Stop at bounded template certification; don't launch solve programme, claim k→∞ conjecture, or require a review of the enormous Heule certificate merely for routine documentary exposition.
