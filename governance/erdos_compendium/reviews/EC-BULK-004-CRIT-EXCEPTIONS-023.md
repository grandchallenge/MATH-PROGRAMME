# EC-BULK-004 — Erdős #487 critical exception review

Date: 2026-10-14. Author/reviewer fyremael, separate reasoning pass by the SAME authenticated operator, not independent-person peer review or a mathematical certification. Disposition: **SOURCE_STATEMENT_AND_FINITE_BRIDGE_PASS; PRIMARY_1971_AND_FORMAL_KERNEL_VERIFICATION_PENDING**.

## Primary source vs claimed solution

Erdős, *Some unsolved problems* (1961), printed p.236, last paragraph of Problem I.26, **directly inspected image**: positive-density set and three distinct elements with lcm(a,b)=c. The prior divisibility-chain statement is separate and cannot itself establish a triple of distinct values. The maintained #487 database reports PROVED (LEAN), with the mathematical solution attributed via #447 to Kleitman, *Collections of subsets containing no two sets and their union*, American Mathematical Society *Combinatorics* (1971), pp.153–155. The original proceedings table of contents confirms these bibliographic coordinates, but full 1971 proof NOT inspected. The 1976 Kleitman Journal of Combinatorial Theory Ser. A 20(3), 390–392 publisher abstract directly inspected, complete proof not reconstructed.

Kleitman's union-free upper estimate is **catalogue-reported**, not an independently proof-checked quantitative constant. The arithmetic transfer from all positive-density sets to Boolean cubes is a nontrivial lemma, neither derived from the elementary product identity nor independently reconstructed here. In particular the original historical description 'positive density', external Lean statement positive LOWER density, and upper logarithmic density in intermediate lemmas are NOT silently equated.

## Formal exception

Pinned GCL FC-GDM-85F86371 lacks 487.lean. Unpinned google-deepmind/formal-conjectures main contains a 487.lean statement but theorem body is sorry. The published version of external plby/lean-proofs exact commit 1d7b3f00780b85ed0462e79a1cd5650ee9055655, path src/v4.29.1/ErdosProblems/Erdos487.lean, imports Erdos447. Its own comments describe the 2-adic slice, odd set, upper-log-density lower bound and I(N) asymptotic contradiction. Source text read, but there is **no GCL exact-toolchain build, axiom print or transitive dependency closure**, so do not claim formal certification.

Maintained #487 metadata 'Formalised statement? No' conflicts with pinned teorth 'formalized: yes' and displayed PROVED (LEAN). This is documentary drift, not a mathematical counterexample.

## Exact adversarial checks

For q>0 coprime to k distinct primes, define d(S)=q product_{i in S}p_i. Unique factorization gives injectivity. Primewise maximum of exponents yields lcm(d(S),d(T))=d(S union T). Thus three pairwise distinct subset witnesses correspond bijectively to three pairwise distinct integer witnesses inside the mapped finite family. This has no density hypothesis and is not a substitute for the infinite transference.

The exact fixture tests/test_erdos_compendium_0487_lcm_union.py enumerates EVERY subset family for bases of k=0,1,2,3 distinct primes, compares all ordered triple witnesses after mapping by q=1,7,11, and tests a concrete (6,10,30) triple. The chain 2,4,8,16 has no three-distinct lcm triple, exposing the primary trap. It also enumerates small union-free extremal sizes. Three focused tests passed; this does NOT verify the global Kleitman bound or the external Lean theorem.

## Scope, evidence, successor

Article governance/erdos_compendium/editorial/0487.md has six substantive sections, the historical/certification distinctions, and UNACCEPTED_DRAFT status. Original issue #1758 now has authenticated RESULT/1 return https://github.com/grandchallenge/MATH-PROGRAMME/issues/1758#issuecomment-6181027541, disposition BOUNDED_TASK_DESIGNED. A same-operator post-draft adversarial pass is not independent-person certification.

Next: obtain full 1971 Kleitman pp.153–155, reconstruct the density-to-cube step and prove the lower/upper/log-density mapping; then run exact-commit Lean 4.29.1 plus imports with a full axiom report. Bounded source-fidelity exceptions may remain without blocking routine **drafting**; they cannot be represented as performed proof replay. Final protected production batch and public deployed MathJax gate remain pending.
