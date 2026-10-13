# EC-BULK-004 — special-status critical review 004

Date: 2026-10-13. Scope: Erdős #458. Role: same accountable coordinator's adversarial documentary review, not an independent mathematical referee or a mathematical certificate. Disposition: **local pre-return documentary QA PASS WITH EXCEPTIONS**, not protected editorial acceptance.

## Source and mathematical semantics

Original Erdős–Graham 1980 printed p.91 was visually inspected. It asks for every $k\geq1$ whether $L(p_{k+1}-1)<p_kL(p_k)$, where $L(n)=\operatorname{lcm}(1,\ldots,n)$. The maintained special status **FALSIFIABLE** is interpreted correctly as OPEN with a finite-counterexample route, not as disproved, independent, or algorithmically decided in full. The source describes both prime-square clustering and small-prime obstructions.

The exact quotient identity follows from the prime-power decomposition of $L(n)$. Between consecutive primes $p<r$, every new prime-power factor is a proper power $q^a$ with $a\geq2$. Hence $L(r-1)/L(p)=\prod_{p<q^a<r}q$. Bertrand's theorem $r<2p$ ensures that a fixed base cannot appear twice: if $q^a>p$, its next power is at least $2q^a>2p>r$. The universal claim is therefore equivalent to the computable inequality $B(p,r)<p$ for every prime gap. The finite witness predicate is decidable; the universally quantified $\Pi^0_1$ assertion is **not** thereby known decidable or independent in PA.

## Formal and live-source exceptions

The exact pinned Lean blob `a0cd551ed43e9eb8f9782375f4dd5ddcd27a425f` uses zero-indexed `nth Prime` and `answer(sorry)` with theorem `by sorry`. This is a formal **statement scaffold**, not a Lean proof. The pinned catalogue status date is 2025-08-31 and the public tracker reports edit 2025-10-07. The public discussion contains external April and June 2026 claims of verification to $10^{12}$ and $10^{20}$; neither was independently replayed or certified by GCL. The manuscript does not promote these reports to established bounds.

## Exact finite verification

`tests/test_erdos_compendium_0458_prime_power_lcm.py` independently enumerates all prime gaps with upper prime at most 99,991 (9,591 gaps) and the proper prime powers in each. No counterexample was found. Exactly five gaps with multiple powers occur below 100,000: $(7,11)$ with base product 6; $(23,29)$ with 15; $(113,127)$ with 55; $(2179,2203)$ with 39; $(32749,32771)$ with 362. Direct LCM arithmetic crosschecks 167 gaps ending at or below 1000. The two methods are mathematically different but neither extrapolates beyond the finite bound.

## Custody, hashes, and admission

Source return is staged at `governance/erdos_compendium/batches/EC-BULK-004_0458_UNPOSTED_RESULT.md`, SHA-256 `8012581063c5eba12ecc8c660b57549ef2a8f71a7b6fce06b1af22dfd582968d`. It is **UNPOSTED**: the original issue #1728 had no `RESULT/1` at readback. Manuscript `governance/erdos_compendium/editorial/0458.md` has normalized stripped-text SHA-256 `3bea117e422dab3a31b10639ca7086d675a207ff97452ab10ec1219eb33e068f`. The source-return write channel was blocked by execution safety checks, and no return identity is invented.

The full bounded suite passed **66 tests and 5 subtests**. Strict MkDocs build succeeded and local HTML includes the manuscript's six headings and Arithmatex math markup. These checks do not replace public real-browser formula rendering. The deterministic 20-sample review, 200-article protected production merge, protected V2 admission and MathCert all remain **NOT DONE**.
