# EC-BULK-004 — Erdős #486 deterministic critical-sample review

Date: 2026-10-14. Authenticated writer/reviewer: fyremael, **same operator in a separate adversarial pass**, not independent-person peer review. Cohort sample member #486 per lexically sorted pinned issue-hash rule. Disposition: **SOURCE_FIDELITY_AND_BOUNDED_LEMMA_PASS; UNSOLVED_GENERAL_CASE_AND_PROTECTED_ADMISSION_PENDING**.

## Source fidelity

Original Erdős 1961, printed p.236, I.26.1, directly inspected: the exclusion applies when b >= a_i. Original Erdős 1980, printed p.114, directly inspected: applies when b > a_i. Current catalogue #486 uses m > n. This is not a typographical distinction to normalize without evidence, because equality occurs for one candidate m=n at *every* selected modulus. Whether the two universal log-density statements are equivalent is **not proved** here. Distinct set definitions are preserved in the manuscript.

Pinned teorth catalogue blob 4e60263a80af6207aca494d2e1388e44fa372889 records OPEN; indexed maintained revision of 2026-04-08 reports OPEN. The 1951 Davenport-Erdős primary article's introduction was checked, but the full original proof and 1936/1937 first proof remain unreplayed. The known special case X_n={0} is not a solution of the arbitrary-residue problem.

## Formal-statement challenge

Pinned google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020 FormalConjectures/ErdosProblems/486.lean blob 5998f9382b9f46c44844cfa5fb7d84ea3ab06aa7 quantifies over EVERY n and has no m>n / m>=n activation; the theorem body contains sorry. Thus it cannot be counted as statement-equivalent to either primary source, or as Lean-proved. The missing threshold is a mathematical difference, not a rendering typo.

## Adversarial mathematics

Finite A is eventually periodic under either convention: once m exceeds max(A), tests depend on m modulo lcm(A). All finite densities exist and equal the number of permitted residue classes divided by the lcm. For A={2,3}, X_2={0}, X_3={1}, the asymptotically allowed classes modulo 6 are exactly 3,5, giving 1/3. Under strict activation m=2 survives; under non-strict it does not. The example exposes and verifies the threshold distinction.

Summable-tail lemma: for c_n=|X_n|, count of forbidden residues from each modulus n contributing between activation n and x is <= c_n floor(x/n). As a result, for finite-cutoff B_N and full B, 0 <= count(B_N<=x)-count(B<=x) <= x sum_{n>N} c_n/n. Since finite truncation density d_N decreases and tail R_N tends to zero if sum c_n/n converges, d_N-R_N <= lower_d(B) <= upper_d(B) <= d_N, so natural density exists. No unjustified exchange of an infinite count and a limit is made; for each finite x only n<=x can activate. The inequality holds equally at m>=n. The argument does not cover nonsummable tails, so the general OPEN question is unaffected.

The fixture tests/test_erdos_compendium_0486_activated_residues.py checks 3 classes: exact 2/3-modulus example; exhaustive 2/3/4 residue-subset choices with both activation conventions and all specified x/cutoff values; infinite-powers-of-two finite-prefix values and exact geometric-tail inequality. All three tests passed at local review. Finite enumeration is not universal theorem certification.

## Editorial gate

Article governance/erdos_compendium/editorial/0486.md has the required six-section sequence and explicitly remains UNACCEPTED_DRAFT. Original issue #1757 authenticated RESULT/1 https://github.com/grandchallenge/MATH-PROGRAMME/issues/1757#issuecomment-6180871578 was read back, with six substantive headings and BOUNDED_TASK_DESIGNED disposition. No protected admission, independent-person review, external Lean replay, or public browser MathJax verification is claimed.

## Successor

Formalize the finite-sieve residue formula and tail union bound with exact m>n and m>=n definitions. Prove the restricted natural-density result under summability and test threshold boundary with a finite counterexample to pointwise equality. Halt at verified restricted result or first falsified inequality. Only after source adjudication, pursue the truly nonsummable residue-tail problem as a separately governed research item. The source research return does not authorize a Solve campaign.
