# R2/065 parity erratum — source-locked logical critical audit

**Disposition:** bounded support for the corrective narrowing of Theorem 65.2. This is a separate logical critic pass in the same Codex session and authenticated identity as the correction author. It is not an external independent referee, mathematical certification, or a fabricated second account.

**Exact material reviewed:** correction commit `5fa9fdf51844d2e7a9684b6f7d63eaa302c82f1e`; [R2/065 proof](R2_NESTED_GAUSSIAN_JET_FOREST_065.md) blob `87b013559eb8485d80f7fa714db0b65a9272d6ed`; [expanded source fixture](fixtures/check_nested_gaussian_jet_forest_065.py) blob `9e1e58d5df15cdbbeec5c443199d748742d5d45c`. Historical source and R2/066 admission remain recorded in PRs [#2864](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2864) and [#2865](https://github.com/grandchallenge/MATH-PROGRAMME/pull/2865).

## Defect and corrected claim

The previously admitted source said that after subtracting all negative Laurent orders every source in the finite family has a strong zero limit with an $O(\epsilon)$ remainder. That assertion is false for even cycle rank. The normal Taylor degree $d$ contributes with power $\epsilon^{d-h}$, and the amplitude and its prescribed pole insertions have only even total degrees. For odd $h$, the first unremoved even degree is $h+1$; for even $h$, it is $h$.

The correction therefore retains the pole recursion and all negative-power coefficients, and replaces the universal zero-limit assertion with:

- odd $h$: strong zero limit with $O(\epsilon)$ error;
- even $h$: finite local delta-jet limit of degree $h$, generally nonzero, with $O(\epsilon^2)$ error.

The finite coefficients of degree $h$ are computed on polynomial tests by the same preparation recurrence, while source insertions still contain only their negative-power counterterms. Adding those finite terms to embedded source counterterms would change schemes and is not done here.

## Independent counterexample and four-loop check

For the diamond $D=\{01,02,03,12,13\}$, the root-zero reduced Laplacian is

$$
Q_D=
\begin{pmatrix}
3&-1&-1\\
-1&2&0\\
-1&0&2
\end{pmatrix},
\qquad
\det Q_D=8,\qquad (Q_D^{-1})_{11}=\frac12.
$$

Its only proper 1PI sources are three cycles, each containing both vertices 0 and 1. Their scalar counterterms vanish on a compact smooth test equal to $(x_1-x_0)^2$ near the collision. Consequently the prepared normalized second moment is exactly $\sqrt2/8$ at order $\epsilon^0$. This alone falsifies the former universal zero-limit statement.

For $F$, the reduced Laplacian and the quotient obtained by contracting triangle 023 are

$$
Q_F=
\begin{pmatrix}
4&-1&-1&-1\\
-1&3&-1&0\\
-1&-1&3&0\\
-1&0&0&2
\end{pmatrix},
\qquad
D_{\mathrm{quot}}=
\begin{pmatrix}
4&-1\\
-1&2
\end{pmatrix}.
$$

Their determinants are 40 and 7, and their first inverse entries are $2/5$ and $2/7$. On the quartic test $(x_1-x_0)^4$, every proper source containing both vertices 0 and 1 vanishes: the available source pole derivatives have degree at most two. The only remaining proper sources are triangles 023 and 123. The latter has the same quotient contribution by the symmetry exchanging vertices 0 and 1. Thus the full finite quartic moment is

$$
\frac{3(2/5)^2}{\sqrt{40}}
-2\frac{3(2/7)^2}{\sqrt{21}}
=\frac{3\sqrt{10}}{125}-\frac{8\sqrt{21}}{343}\ne0.
$$

This derivation does not use the producer fixture's graph recursion. The accompanying [separate exact check](fixtures/check_r2_065_parity_review.py) uses the determinant Leibniz formula and cofactor ratios, imports no producer code and shares no producer state. It checks both moment identities and nonvanishing through rational arithmetic. It is computationally separate, but remains the same logical agent/session rather than an external certification.

## Retained host theorem and validation

The full host $G$ has odd cycle rank five. Its negative-power counterterms, 85-source inventory, 2542 forests, nested derivative contacts and all 86 scalar/quadratic/quartic moments are unchanged. In particular its nonzero fourth-order pole remains $\sqrt6/72-\sqrt3/32$, and after all three negative orders are subtracted its next degree is six, giving the original strong $O(\epsilon)$ zero limit.

The uniform remainder argument is finite-family Gaussian Taylor expansion on bounded compact smooth tests: after the first retained degree, the next allowed even degree differs by two; Gaussian moment and tail estimates bound the error. No assertion of uniformity over arbitrary graphs or kernels is introduced.

Validation on 2026-10-27: corrected mathematical Markdown source gate PASS; expanded source fixture PASS, including all original assertions and the two new even-rank finite moments; separate determinant/cofactor check PASS. Runtime: Windows, isolated CPython 3.12.12 virtual environment, uv 0.10.0, standard library only, owner-local cache paths. No committed uv lockfile is present in this replay environment; this is recorded as an unpinned local mathematical replay, not a reproducible deployment or hosted provenance claim.

**Audit conclusion:** the parity correction removes the demonstrated false generalization and preserves the stated five-loop host result. The original R2/066 audit missed this overgeneralization in Theorem 65.2; its historical source binding is retained and its assessment must be read with this erratum. Protected admission and exact readback remain separate operational requirements. Parent [REACH-R2 #2797](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2797) remains OPEN; overlapping nonnested singular-source compatibility and global BV/QME are still unproved.
