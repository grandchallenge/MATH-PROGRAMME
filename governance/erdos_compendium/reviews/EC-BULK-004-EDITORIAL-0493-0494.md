# EC-BULK-004 — Erdős #493–#494 source fidelity and same-operator review

Date: 2026-10-14 (CHAD local), 2026-10-15 UTC. Authenticated editorial operator fyremael. This is a separate same-operator critical reading, **not independent-person mathematical peer review or protected editorial admission**.

## #493 literal statement and elementary proof

Original Schinzel-attributed Erdős (1961), *Some unsolved problems*, printed p.238, contains the product-minus-sum question with factors at least two. Maintained #493 https://www.erdosproblems.com/493 says PROVED (LEAN), credits Eli Seamans with n=2(n+2)-[2+(n+2)], and explicitly warns about a possible omitted historical restriction. For each n>=0, the fixed k=2 and factors 2,n+2 solve the registered statement. The factors vary with n; k does NOT. At n=0 repetition is permitted because the source does not demand distinct factors, and n>=1 has distinct factors regardless. k=1 always gives zero, so k=2 is minimal for the positive-n variant.

Protected FC-GDM-85F86371 493.lean, blob 7020bd4f35fd107a081b72a9b9eff4ad53505a73, encodes essentially these quantifiers but has an unfinished theorem body (sorry) with an external formal proof pointer. No GCL Lean kernel run has been performed. The algebraic identity is already a complete ordinary mathematical proof, but no extra hypothetical Schinzel condition is presumed. tests/test_erdos_compendium_0493_fixed_two_factors.py checks n=0..100000, additional large integer and k=1 nonrepresentation. A finite test does not substitute for the displayed universal algebraic derivation. Original issue return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/1764#issuecomment-6185020695 .

## #494 three distinct mathematical propositions

The original Erdős 1961 p.238 inadvertently describes *products*. Selfridge–Straus (1958), *On the determination of numbers by their sums of a fixed order*, Pacific J. Math. 8, 847–856, primary https://msp.org/pjm/1958/8-4/pjm-v8-n4-p17-p.pdf, directly inspected, studies SUMS with multiplicities. This distinction matters.

(A) Literal PRODUCTS claim is false even without zeros: for third-order products, A={zeta^0,zeta^1,zeta^2,zeta^4} and B={zeta^0,zeta^2,zeta^3,zeta^4}, where zeta primitive sixth root, are different four-element sets but have identical product-exponent MULTISETS mod 6, namely {0,1,3,5}. The original product statement cannot be declared PROVED.

(B) General unrestricted SUMS claim is also false at small n. For k=n=3, A={0,1,4}, B={0,2,3}, both have only the sum 5. For k=3,n=6, zero-total A={-7,-3,-2,1,5,6}, B=-A, A!=B but the complement bijection on three-subsets yields identical three-sum multisets. At k=2,n=4, A={0,1,2,5}, B={-1,2,3,4} also have identical pair-sum multisets by the half-cardinality reflection; this case was checked after **rejecting an initially guessed invalid test pair**. All finite tests now pass.

(C) Fixed-k EVENTUAL sums uniqueness is PROVED: Gordon–Fraenkel–Straus, *On the determination of sets by the sets of sums of a certain order*, Pacific J. Math. 12 (1962), 187–196, primary https://msp.org/pjm/1962/12-1/pjm-v12-n1-p17-s.pdf, Section 4 theorem pp.189–191 inspected. For each FIXED k>2, F_k(n)=1 for all but finitely many n. The proof uses a power-sum coefficient criterion and an imported Ridout approximation theorem. The complete published Section 4 argument was read but the Ridout theorem is not independently rederived. This does not supply a bound uniform in k.

**Attribution exception:** the 1958 Selfridge–Straus original (Example 1, p.853) explicitly says that for s=3, n=27 and n=486 are *in doubt* by its criterion. The maintained catalogue's attribution of a universal k=3,n>6 proof to the 1958 article is not fully supported by this passage alone. The 1962 eventual theorem is unaffected; this exact 1958 low-order attribution remains a provenance task. Pinning the actual source statements prevents false retroactive proof claims.

The protected FC-GDM-85F86371 494.lean blob caa293977eeca275b9ec57aced136bcac97fb6ea contains SEPARATE variant theorems, all with proof placeholders. It is not a proof certificate. tests/test_erdos_compendium_0494_multiset_reconstruction.py tests preserved multiplicity, both small-cardinality sums examples, the nonzero product example and the two-sum power-sum coefficient. Exact source return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/1765#issuecomment-6185029649, disposition STATUS_CONFLICT.

## Admission and future work

Both drafts have six substantive headings, source URLs, bounded mathematical examples, precise known/open/false distinctions, and status UNACCEPTED_DRAFT. Neither is an invented new result. Next source-fidelity task: inspect any later exact proof of n=27,486 for k=3 before repeating the catalogue's stronger 1958 attribution. Formal Lean replay and deployed browser MathJax check are unperformed as of this same-operator review. Publish only via verified protected batch admission; original source comments authorize evidence collection rather than direct status certification.
