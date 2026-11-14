# Erdős #1, Stage C: independent GCL adjudication of pinned replay evidence

Task: `ERDOS-PV-0001-C`; original source audit #1270, source scope stage A #3212,
bounded mathematical proof stage B #3225, formal/adversarial stage C #3238.

## Source and compiler identity

GitHub Actions [run #43541084973](https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/43541084973)
executed on protected MATH-PROGRAMME commit
`006df1eae9a70d6c932cc1e37568fca412e2e1b5`, workflow attempt 1.
It fetched the author source
`tadamcz/erdos1@db6f9091dfaf9bac704e6b28fb3a094594869328`
with exact proof Git blob
`07d2f36647a2319e65c0c8c756527460925e9075`,
Lean `v4.28.0`, pinned Lake manifest and Mathlib revision
`8f9d9cff6bd728b17a24e163c9402775d9e6a365`.
See `INDEPENDENT_GCL_REVIEW.json` and the preserved `RECEIPT.json`
for the complete source lock, compiler statuses, artifact identity and hashes.

## Readback: positive and negative cases

The actual `BUILD.log` reports `Build completed successfully (8028 jobs)`.
The exact type-level `GCLReadback.lean` compilation exited zero and verified
both the bounded binary-block theorem
`ErdosCounter.exists_binary_block_set` and the declaration
`Erdos1.erdos_1.disproof`, the negation of the historical formalized
uniform-constant statement.

Both declarations' real `#print axioms` output contains precisely
`propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx` or
unexpected axiom was reported. The two explicit compiler output lines
are preserved in `READBACK.log`, with SHA256
`fff36092ba49ef2ea49d1bdca6cc5a9510ebf2fccc0ea0a6b137892f78a89fa7`.

The deliberately invalid `GCLNegative.lean` omits the exact required
`RelationFree a (2^k)` hypothesis. It failed compilation with exit 1 and
reported that the theorem still requires that relation-freedom premise.
This is a substantive adversarial altered-target check, not an unrelated
syntax error. Its log SHA256 is
`892e6a0c7f9bc0eba1f875b73999773bb862c6eb6c49357ae5c37604125ed6ad`.

The prior independent bounded mathematical argument compares signed
binary coefficients, including the necessary strict threshold $2^k$.
The weakened threshold $2^{k-1}$ is disproved by $a=(1,3)$, $k=2$;
the author theorem has the correctly stronger condition.
Cardinality also requires singleton injectivity, which the author
source explicitly establishes. These independent logical challenges
are documented in the prior Stage C
`FORMAL_APPLICABILITY_AND_ADVERSARIAL_AUDIT_001.md`.

## Scope and limits

**PASS:** an actual Lean kernel replay of the exact pinned source, type
matching for both declared theorems, standard-library axiom readback,
and the missing-hypothesis negative test. The bounded binary-block
transfer lemma has a distinct role-scoped mathematical review.

**NOT CLAIMED:** a fully independent mathematical reconstruction of all
lattice/cube-gadget steps of the global Erdős #1 disproof; an
independent human referee; a MathCERT certificate; or closure of the
complete 100-problem cohort. A green Lean elaboration proves that the
author's formal statements follow from the declared kernel and
allowed axioms, *not* that the formalization captures every historical
interpretation or that the surrounding research has been independently
re-derived.

The prior failed run #43539448622 had genuine successful compiler
outputs but failed to preserve exit statuses and parse quoted Lean
axiom names. It was replaced by repaired, protected workflow commit
`006df1eae9a70d6c932cc1e37568fca412e2e1b5`; its earlier
failure must not be counted as a successful original workflow receipt.

This scoped Phase C task may be admitted as **reviewed bounded formal
evidence**, without any theorem-level MATHCERT or independent-human
claim. Phase D is the separate documentary/admission obligation.
