# OAI-26 Family 002 — pinned PDF theorem concordance and editorial critic

Record type: `GCL_OAI26_ED01_F002_SOURCE_CRITIC/1`. Editorial source review only; not mathematical certification.

## Exact pinned source identities

All three files were fetched through the authenticated GitHub blob API at `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`, and read with pypdf:

| Manuscript | Git blob | Bytes | PDF pages |
| --- | --- | ---: | ---: |
| Exact Birch–Swinnerton-Dyer Formula from Low Selmer Corank (Oct 7) | `4621d1c197766f11d416b7e149343d938fcd9697` | 874353 | 94 |
| The Selmer converse for elliptic curves at every prime (Oct 7) | `384525874a5e9989e574a5f9ce7c9883258cc732` | 869458 | 82 |
| The two-primary BSD formula in Selmer corank at most one (Oct 6) | `9c1827e35640033bf16eac9fa88136079b1cc2de` | 1279386 | 164 |

## Statement-level fidelity and dependency check

1. **Exact-BSD main paper, PDF p. 3, Theorem 1.1**: if the *full* `q`-power Selmer group has corank zero or one at **any selected prime q**, then the paper claims `rank E(Q) = ord_(s=1) L(E,s) = s_q(E)`, the **entire** Tate–Shafarevich group is finite, and the full leading-term formula holds, with all finite-prime Tamagawa factors. The paper specifies the uncompleted L-function, global minimal Néron differential, real period over all real connected components, canonical-height normalization, full Mordell–Weil free lattice, and rank-zero regulator convention. The current Family 002 article describes these accurately.
2. **Selmer-converse companion, PDF pp. 1–3**: its stated role is rank equality and finiteness for any prime and corank at most one. In the exact-BSD paper these conclusions are explicitly attributed to its companion [23], not separately proved from the exact coefficient argument.
3. **Two-primary companion, PDF p. 4, Theorem 1.1 and Corollary 1.2**: claims equality of the 2-adic valuation of the normalized leading coefficient with `v_2(#Sha)`, including an any-prime criterion via finiteness and the Kummer exact sequence. Thus the main paper's all-prime result needs this companion at 2 **plus an odd-prime argument**; these are not interchangeable.
4. **Exact-BSD proof architecture, PDF pp. 4–6**: introduces an arithmetic discrepancy at an odd prime, a nonnegative single-curve comparison and a zero-sum quadratic-twist pair comparison. Its integral determinant quotient must be shown **integral and a unit**, not merely nonzero after inverting p; distinct residual, theta-congruence and tame-direction tests supply these steps. This is correctly described at high level in the article, but their mathematical proofs have not been verified in this review.
5. **Two-primary companion, pp. 5–6**: distinguishes the integral 2-adic valuation from rationalized rank/finiteness arguments and emphasizes real components and index-squared regulator effects. The article correctly warns that rank agreement alone does not establish exact BSD.

## Critical editorial verdict

**`SOURCE_THEOREM_CONCORDANCE_PASS / ACCEPTED_EXPOSITION_WITH_EXPLICIT_PROOF_LIMITS`** for the existing six-section Family 002 article as *publisher-attributed exposition*. The plain-language example is labelled heuristic. The statement that the complete BSD leading-term formula holds is attributed to the pinned paper, **not** to a GCL proof or certificate. The source also directly distinguishes arbitrary rational torsion/reduction/isogeny conditions from the essential full prime-power Selmer-corank hypothesis.

**Outstanding mathematical dependencies (NOT source-fidelity failures)**: independent verification of the unrestricted companion Selmer converse, exact dyadic determinant calculations, odd-prime integral unit/primitivity argument and all versions of their cited external inputs; withdrawn-citation history; Lean or Comparator mapping. None is silently claimed resolved. The density-one twist consequence requires the separately sourced twist-distribution input and does not follow from Family 002 alone.

**Coverage limitation**: theorem statements and opening proof architecture of the three pinned PDFs were directly inspected, including exact-BSD pp. 3–6 and two-primary pp. 4–6; this is **not** a line-by-line proof audit of the full 94+82+164 pages. Publication rendering and exact-hash protected admission are separate obligations.

Authored article: `governance/oai26_documentary/editorial/002.md` at Git blob `dee9a7f7a42885d36f1a5f3893f46d77f7d5a386`. Parent [OAI26-ED-01 #2901](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2901) remains open for the other families.
