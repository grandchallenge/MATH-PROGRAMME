# EC-BULK-007 — #1146 essential component source-semantics exception

**Status: SOURCE_NORMALIZATION_CONFLICT, primary-source adjudication PENDING.** This is neither a reviewed disproof of Erdős's intended open problem nor a completed independent critical review.

- Maintained source: https://www.erdosproblems.com/1146 (OPEN)
- Source-linked RESULT/1: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2417#issuecomment-6181795595
- Published citation: Ruzsa (1999), discussion pp.139, 146–147; Vardi (1999), §1.19.
- Frozen formal-conjectures file 1146.lean: IsEssentialComponent declaration with a local proof placeholder; must review the **actual definition**, not rely on a name.

## Exact inconsistency

If $A=\{2^i3^j:i,j\ge0\}$ and $B$ is any set of **strictly positive** integers, then $1\notin A+B$. Under the literal Schnirelmann density

$$
\sigma(S)=\inf_{N\ge1}|S\cap[1,N]|/N
$$

we have $\sigma(A+B)=0$. For $B=\{1\}\cup 2\mathbb Z_{>0}$ one verifies $\sigma(B)=1/2$. Therefore the literal transcription, without further conventions, **cannot** define the intended open essential-component problem.

The likely repair is a convention involving $0$ in $A$, $B$ or an augmented sumset, but it is not legitimate to guess which convention the original mathematicians use. Ruzsa explicitly describes this as a nontrivial open question, rather than a trivial no-result.

## Required source-fidelity closure

1. Read Ruzsa (1999) primary §10 density definition and pp.146–147 passage, not only website snippets.
2. Obtain Vardi (1999), Problem 1.19, for zero-element convention.
3. Inspect Lean declaration of IsEssentialComponent and tests for add-zero semantics, without attributing an unproved Lean declaration to a kernel proof.
4. Specify source-equivalent corrected statement and prove it is no longer defeated by the missing-one obstruction.
5. Preserve OPEN until normalized statement and theorem-level evidence reviewed. No primary original issue body or SHA changes.

Reproducible phase17 fixture: ci/erdos_compendium_007_phase17_checks.py.
