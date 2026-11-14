# EC-BULK-004 — Erdős #480 critical source and quantifier review

Review receipt: EC-BULK-004-CRIT-EXCEPTIONS-019  
Date: 2026-10-14  
Authenticated accountable editorial identity: fyremael  
Adjudication: **CRITICAL_DRAFT_PASS_WITH_HISTORICAL_QUANTIFIER_AND_SHARPNESS_SOURCE_BLOCKER**. This is a second logical editorial pass, not independent-person peer review, kernel-checked formal proof or protected V2 admission.

## Original primary source versus later theorem

The original Erdős–Graham monograph (1980) was visually inspected at **printed pp. 96 and 107** (scanned PDF zero-based pp. 91,102), https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf . Printed p.96 states Newman's question as existence of “infinitely many m and n” obeying $|x_{m+n}-x_m|\le1/(n\sqrt5)$ for a bounded infinite real sequence, then says “This is known to be false (see Added in proof p.107).” Printed p.107 instead says Chung and Graham proved **some fixed positive n** for **infinitely many m**, even with a stronger constant $1/(c-\varepsilon)$, $c=1+\sum_{k\ge1}1/F_{2k}$. The apparent historical verdict and the possible “infinitely many DISTINCT n” versus “infinitely many (m,n) pairs” ambiguity remain unresolved. Modern source-fidelity clearance must **not** silently equate those different scopes.

The complete 42-page full solution is primary Chung–Graham, *On Irregularities of Distribution* (1984), *Finite and Infinite Sets*, Colloq. Math. Soc. János Bolyai 37, 181–222, author's original https://mathweb.ucsd.edu/~ronspubs/81_12_irregularities.pdf . Theorems 1 and 2 on printed pp.182–183 were visually inspected. Theorem 1 proves for every sequence in $[0,1]$ the exact modern statistic

$$
C(x)=\inf_{n\ge1}\liminf_{m\to\infty}n|x_{m+n}-x_m|\le
\alpha=\bigl(1+\sum_{k\ge1}1/F_{2k}\bigr)^{-1}.
$$

Theorem 2 constructs an extremizing sequence by unique constrained even-index Fibonacci digits $\varepsilon_i(N)\in\{0,1,2\}$, with $x_N^*=\alpha\sum_i\varepsilon_i(N)/F_{2i}$ and $\inf_{n\ge1}\inf_{m\ge0}n|x_{m+n}^*-x_m^*|=\alpha$. The identical theorem content was independently read in authors' **1981 PNAS announcement**, https://fanchung.ucsd.edu/mypaps/fanpap/55oiodors_a.PDF , printed p.4001. The complete interior 1984 argument was not independently re-proved or formalized by GCL. This is source-verified historical theorem evidence, not MathCert.

## Sharp constant and suspect 1980 golden-rotation parenthetical

Partial-sum bounds are exact: $F_2=1,F_4=3,F_6=8$, so $c_2=1+1+1/3=7/3>\sqrt5$. Hence $0<\alpha<1/\sqrt5$. Numeric c_8 and c_12 reciprocals are respectively approximately 0.394517106 and 0.394421744, converging downward to the **published** $\alpha=0.39441967...$; no GCL numerical fitting or new constant claim.

At 1980 printed p.107 the parenthesis purports to demonstrate sharpness using the golden rotation $y_m=\{m\tau\}$, $\tau=(\sqrt5-1)/2$. Direct adversarial check at **n=1**: the absolute adjacent differences take values $\tau$ and $1-\tau$ infinitely often, because the irrational rotation visits each of the two corresponding intervals infinitely often. Thus $C(y)\le1-\tau=(3-\sqrt5)/2\approx0.381966<\alpha$. It cannot witness equality for the modern statistic as literally printed. The source-critical manuscript instead attributes sharpness to Chung–Graham's genuine **1984 Theorem 2** Fibonacci-digit construction and leaves the early parenthetical unexplained rather than inventing an erratum.

## Formalization and exact QA custody

Pinned google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020 file FormalConjectures/ErdosProblems/480.lean blob 532f911ab0688921ca4af18696e580c0cac3b72b, accurately uses n:ℕ+ and atTop.liminf over m for the normalized theorem, and includes improved-bound and best-possible variants, **each with by sorry**. Earlier Formal Conjectures issue #1282 identified an obsolete n=0 loophole, which the protected source no longer uses. No Lean checker/axiom or 42-page proof replay was claimed.

Authenticated original issue-bound research return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/1750#issuecomment-6168422064, author fyremael, LF-normalized SHA-256 **d14c465464b6d48737af76ae111b702ec68fe63947703e29dc8109a429c03d90**, disposition PARTIAL due historical source ambiguity, six complete RESULT/1 sections.

Six-section substantive draft: `governance/erdos_compendium/editorial/0480.md`, SHA256(UTF8(text.strip())) **bb3593889143115fe7c4402372178a3b62e83f807d21e81e9c116a71c084c82a**, raw bytes SHA256 **988bf0e224f1420dd682fc9063937669c1c701a1df5f4ff4e702a4c8255e95c2**, six required headings each exactly once, math dollar count balanced.

Five new exact finite tests in `tests/test_erdos_compendium_0480_fibonacci_clustering.py` PASSED at commit 1376786fea5b8f3a221e2e482f91aec71d51dd3a. They verify rational Fibonacci partial sums and certified geometric tail enclosure of α, strict α<1/√5, n=1 golden-rotation discrepancy, periodic test sequences having C=0, and the fact that n=0 is vacuous and disallowed. These calculations are NOT proof of the published universal or optimality theorem.

## Decision and successor gate

Documentary interpretation of **modern** $C(x)$ theorem and published sharp constant: source-researched and suitable as an **unaccepted** accessible article. Original 1980 wording and sharpness parenthetical: **PARTIAL primary-source fidelity**, exact stronger variant not adjudicated. The smallest next task is to settle whether the 1980 “false” line applies to the different requirement of infinitely many DISTINCT shifts n, using original editorial context, explicit counterexample if intended, and complete 1984 theorem proof. Another task is independent kernel replay of actual Fibonacci-digit witness without \`sorry\`, preserving reference theorem/citations.

This review neither passes a deterministic sample gate nor replaces any independent mathematical referee. No protected production PR, successful live browser MathJax for #480, V2 admission, proof priority, external worker identity, or novel mathematical result is claimed.
