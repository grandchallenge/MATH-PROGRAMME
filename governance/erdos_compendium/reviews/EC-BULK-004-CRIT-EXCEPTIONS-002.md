# EC-BULK-004 — second exceptional-source editorial review

Review receipt: `EC-BULK-004-CRIT-EXCEPTIONS-002`  
Date: 2026-10-13  
Scope: Erdős #452, #453, #454  
Declared role: accountable **read-only adversarial editorial checking**, logically separate from the drafting step. Same authenticated GCL GitHub identity `fyremael`; independent human or physical-model review **not** asserted.  
Disposition: **documentary draft pass with preserved mathematical/formal exceptions**, not editorial admission or mathematical certification.

## Exact immutable evidence and manuscript hashes

| Problem | Original issue-bound research return | Normalized SHA-256 of stripped manuscript | Review |
| --- | --- | --- | --- |
| #452 | [#1722 RESULT/1](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1722#issuecomment-6144051742) | `746821f73fa802fddee7f526897fc574e30ebbcc73a33d20b2e2bae11116bcf3` | PASS as unaccepted mathematical documentary draft |
| #453 | [#1723 RESULT/1](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1723#issuecomment-6144060255) | `c7fbb70aae19a38ca53280adc99b50aefaadcf9e83284d579af4519636f03061` | PASS as unaccepted documentary draft |
| #454 | [#1724 RESULT/1](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1724#issuecomment-6144177198), [analytic correction](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1724#issuecomment-6144189158) | `15882239aca6427dedd3669bb01235e8091f797994db675ef86a41f35e163559` | PASS only with the explicit correction retained |

## 452: exact mathematical and status boundaries

Primary Erdős–Graham (1980), printed p. 90, describes $\omega(n)$ as **distinct** prime factors and seeks a maximal *consecutive* run in $[x,2x]$. It states a density-$1/2$ theorem of Erdős (1937) and the classical CRT lower bound $L(x)\ge(1+o(1))\log x/(\log\log x)^2$. The manuscript accurately distinguishes this from the unknown growth beyond the classical bound.

The source return's finite CRT fixture uses pairwise coprime moduli $5005$, $215441$, $2022161$ and the exact residue representative $a=2099999228442114$. Integer arithmetic confirms that for $j=1,2,3$, $a+j$ is divisible by the four distinct assigned primes, and $4>\log\log(a+j)$. This does not establish an infinite theorem. The reconstructed asymptotic uses the prime number theorem as an external prerequisite and records all fixed-$\varepsilon$ dependencies rather than claiming a GCL proof of PNT.

The maintained catalogue is OPEN; a formalization-metadata mismatch between pinned and later public snapshots is explicitly preserved. No Lean compilation, full site update, or proof certification.

## 453: Pomerance's strict geometric disproof versus separate open density question

The original Erdős–Graham (1980), printed p. 90, reports Pomerance's disproof of the eventual symmetric **prime-product** assertion. Pomerance's complete primary manuscript, *The Prime Number Graph*, Math. Comp. 33 (1979), pp. 399–408, was directly inspected: p. 399 equation (1.1), p. 400 Theorem 2.2 and its corollary, stating **infinitely many** indices with strict $2a_n>a_{n-i}+a_{n+i}$ for *every* offset $1\le i<n$. The substitution $a_n=\log p_n$ uses $a_n/n\to0$. The proof is Pomerance's; GCL checked theorem semantics, not a novel theorem or a Lean replay.

Finite checks at $n=3,5$ satisfy $p_n^2>p_{n-i}p_{n+i}$ for all offsets; $n=2,4$ do not. The document preserves the difference between *infinitely many* strict exceptions, the disproved universal eventual claim, and Erdős's separately open conjecture about their density.

The provider at `google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020` has an external proof link but `by sorry` in its protected declaration. Neither that nor any automated process exit is GCL proof certification.

## 454: mandatory quantitative-prime-asymptotic correction

Primary Erdős–Graham p. 90 and Pomerance p. 406 ask if $\limsup(f(n)-2p_n)=\infty$ for the **minimum** over positive symmetric offsets. This remains OPEN; Pomerance established infinitely many positive differences and the lower limsup bound $\ge2$.

The original issue-bound return included an insufficient explanation of why the exceptional offset $i=n-1$ eventually contributes more than 2. **First-order** $p_n\sim n\log n$ alone is not enough to subtract $p_{2n-1}-2p_n$ precisely. A separate immutable correction supplies the valid Cesàro–Cipolla input $p_n=n(\log n+\log\log n-1+o(1))$ and deduces $p_{2n-1}-2p_n=2n\log2+o(n)\to\infty$. This input is sourced to Arias de Reyna–Toulisse, *The n-th prime asymptotically*, J. Théor. Nombres Bordeaux 25 (2013). All other symmetric offsets use two odd primes, making every strictly positive difference at least 2. The published lower bound is consequently supported by correct hypotheses, while the infinite limsup remains unproved.

Finite signed gaps $(D(2),D(3),D(4),D(5))=(1,0,2,-2)$ were reproduced from the actual primes. The pinned FC454 uses $\mathbb N_\infty$ and has `sorry`; a finite signed test must not silently truncate the negative case. The manuscript reflects the correction faithfully and makes no MathCert claim.

## Mechanical QA, exception and admission boundaries

- At repository branch head `a7bbc41d7dc8a9420bb4ce04e1aeafbbf8f05d29`, `python3 -m pytest -q ci/test_ec_bulk_004_math_fixtures.py ci/test_erdos_compendium_*.py` passed **55 tests and 3 associated subtests**. Exact fixtures include #452 CRT and #454 signed gaps.
- `mkdocs build --strict --quiet --site-dir /tmp/EC-BULK-004-QA-SITE` completed with exit code zero. This is a **local build**, not successful protected GitHub Pages deployment or real-browser formula rendering.
- All three new manuscripts have the prescribed six headings and balanced dollar-delimited math markup. Their hashes are recorded above; altering their bytes invalidates this review.
- The historical error in the uncorrected #454 return remains visible as immutable provenance, with the corrective comment specifically linked.
- These are **exception-oriented early reviews**, not the required deterministic 20-article sampling across the completed 200-piece cohort.
- No protected production PR, protected V2 editorial admission, live deployed 200-page readback, or mathematical proof certification has occurred. All manuscripts remain **UNACCEPTED_DRAFT**.
