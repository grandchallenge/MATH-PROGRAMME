# EC-BULK-004 critical sample #498 — source and mathematical boundary receipt

Observed 2026-10-15 UTC, editorial actor fyremael. This is a same-operator, reproducible critical reading of #498. It is **NOT** an independently approved specialist review or a protected editorial admission. The manifest must continue to show that critical review is required until the appropriate independent review process records a genuine result.

## Exact original historical statement

The original Erdős 1961 *Some unsolved problems*, printed p.240, Problem II.3, PDF https://users.renyi.hu/~p_erdos/1961-22.pdf#page=20, has been visually read. The author explicitly says **interior** of any circle of radius 1 for the complex sums; this is an OPEN disc. He discusses complex vectors and Hilbert-space vectors of norm >=1. The sharp bound is C(n,floor n/2) of SIGN ASSIGNMENTS, NOT the number of distinct geometric endpoints.

If one substitutes closed disc |w-c|<=1 for open disc |w-c|<1 while keeping |z_i|>=1, the theorem is false even for n=1. With z1=1,c=0, both +/-z1 lie ON the boundary and would be counted, giving 2>1. Another failure is n=2,z1=z2=1,c=1: closed disc contains two zero sums plus the sum 2, giving 3>2. The exact OPEN disk for this same second example contains ZERO sums; an initially wrong fixture expectation of one was discovered by independent computation and corrected prior to passing tests. With all z_i=1 and center 0 (even n) or 1 (odd n), the open disc attains precisely C(n,floor n/2); sharpness verified.

## Primary-provenance distinction

Erdős 1945, *On a lemma of Littlewood and Offord*, *Bulletin AMS* 51, 898–902, is the original real-version paper cited in 1961. The real version reduces exactly to Sperner: for real z_i>=1, strictly nested plus-sign subsets have sums differing by >=2 and cannot both lie in an open interval of length 2. For arbitrary real z_i of modulus>=1, absorb the original signs into the choices. This independently verifies the real mechanism.

Complex version resolved by D. J. Kleitman, *On a lemma of Littlewood and Offord on the distribution of certain sums*, *Math. Z.* 90 (1965) 251–259, DOI 10.1007/BF01158565. Springer publisher record https://link.springer.com/article/10.1007/BF01158565 directly confirms the bibliographic metadata; full proof PDF is paywalled and was **not** independently reviewed. Kleitman's later Hilbert-space extension (1970), *Advances in Mathematics* 5, 155–157, remains a source dependency for generalizations, not a proxy for the 1965 proof.

GCL protected pinned Formal Conjectures provider FC-GDM-85F86371 has NO 498.lean. An unpinned newer source encodes Metric.ball c 1 and norms >=1 and links to external plby/lean-proofs@1268917..., but uses a by sorry proof placeholder locally. The maintained catalogue labels the problem PROVED (LEAN); the external Lean claim is **not independently replayed on CHAD** with an exact formal dependency snapshot. Current 2026 site discussion notes published norm >1 versus modern >=1 differences and open versus closed ball. Do not equate these formulations without a primary paper comparison.

## Testable obligations and disposition

Tests/test_erdos_compendium_0498_littlewood_offord_disc.py is an exact finite lattice check: sign choices are counted WITH repetitions, vectors are Gaussian integers of norm>=1, centers on a half-integer grid, and all squared distances are exact binary rational numbers. It checks the open bound n<=4, closed disc failures n=1,2, sharpness all real vectors for n<=20 and real-comparable subsets' gap >=2. These finite facts cannot certify Kleitman's theorem over all complex inputs.

**Critical review conclusion: CONDITIONAL / SOURCE_PROOF_REPLAY_PENDING.** Required gate for genuine independent critical review: obtain and read Kleitman 1965 full original pp.251–259 OR replay the external reported Lean theorem in a pinned toolchain with an independent authenticated specialist reviewer; verify exact norms/open-disc and any proof-version theorem bridge. No reviewer signoff or source proof certainty is invented. Original source-comment return https://github.com/grandchallenge/MATH-PROGRAMME/issues/1769#issuecomment-6186824545 is authenticated issue-bound evidence. Status remains UNACCEPTED_DRAFT and critical_review_required=true.
