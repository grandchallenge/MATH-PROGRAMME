# UC-001 Accessible Research Guide

!!! info "Research surface authority"
    **LIVE:** [UC-001 canonical tracker #1](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1).  
    **AUTHORITY:** `DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md`.  
    **EXPOSITION:** this guide explains current protected state; it does not prove Frankl's conjecture.

## 1. Status

Frankl's union-closed sets conjecture remains open. The campaign has a mature programme spine, qualified restricted claims, exact finite checks, Lean-facing lemmas, and a separate documentary-production route.

## 2. Plain object

For every finite nonempty union-closed family with nonempty support (excluding both the empty family and the singleton family consisting only of the empty set), the target is to prove that some element belongs to at least half of the member sets.

## Reader entry and prerequisites

**Status:** open conjecture; exact finite and restricted proof evidence only. **Audience:** undergraduate combinatorics readers, research collaborators, and independent checkers. **Time to first example:** 5 minutes. **Time to first fixture:** 10 minutes.

| Level | Concepts |
| --- | --- |
| Required | Finite sets, unions, counting, injections |
| Helpful | Lattices, double-counting, elementary probability |
| Deferred | Entropy methods, the governed UC-WP05 lattice spine, Lean formalization |

A family is *union-closed* if the union of any two members is a member. Its *support* is the union of all member sets. The support must be nonempty for the target statement.

## 3. Current obstruction

The missing step is a genuine local-to-global bridge. Verified small-universe results, pairing lemmas, lattice constraints, and restricted certificates do not by themselves imply the universal conjecture.

## 4. Working model

Mathematical work should consume only the exact restricted claims protected in the campaign spine. Documentary work is separate: the full-tier documentary *The Element in Half the Worlds* is admitted and navigable at [the published reader](../documentaries/union_closed.md). Public admission supplies exposition, not a proof of Frankl's conjecture.

## Core bridge and first examples by hand

**Friendly example.** On the universe \(\{1,2\}\), take \(\mathcal F=\{\varnothing,\{1\},\{2\},\{1,2\}\}\). This is union-closed. Each element occurs in exactly two of four sets, reaching the half threshold with equality.

**Edge example.** \(\mathcal F=\{\varnothing\}\) is nonempty as a family and union-closed, but its support is empty. It has no candidate witness. This is why the conjecture must exclude the empty-support case, not merely the empty family.

The bridge is: union operation → closed family → frequency count → witnessed small cases → the missing uniform all-families argument.

## First computation or fixture

Run this Python 3 fixture (standard library only), which **checks one instance**, not the universal conjecture:

```python
F = [frozenset(), frozenset({1}), frozenset({2}), frozenset({1,2})]
closed = all(a | b in F for a in F for b in F)
support = set().union(*F)
counts = {x: sum(x in a for a in F) for x in support}
print(closed, counts, max(counts.values()) * 2 >= len(F))
# Expected: True {1: 2, 2: 2} True
```

**Support route:** regression audit / exact check of this four-set instance. **Limitation:** no extrapolation to larger universes.

## First theorem or local proposition

**Singleton lemma.** If a finite union-closed family contains \(\{x\}\), then at least half its member sets contain \(x\). **Proof:** map each member \(A\) missing \(x\) to \(A\cup\{x\}\). Union-closure ensures the image is present, and deleting \(x\) recovers \(A\), so the map is injective into the containing members. This is elementary and does not settle the universal problem.

## 5. Theorem-spine location

Programme authority is `DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md`. Supporting protected artifacts include the WP01 status spine, WP02 Lean handoff, Agent Council audit, and the qualified downstream certification records referenced by tracker #1.

## 6. Debt audit

Mathematical debt: the universal bridge beyond bounded/restricted results. Documentary admission is complete; any remaining source-concordance, mathematics, or accessibility corrections are separate editorial debt, not an unperformed initial publication.

## 7. Claim boundary

No protected record proves or refutes Frankl's conjecture. Certification of restricted claims, finite verification, and publication work do not promote the universal statement.

## Challenge ladder

| Stage | Bounded duty | Completion test |
| --- | --- | --- |
| Exercise | Count frequencies in the four-set example | Obtain 2 and 2 |
| Exploration | List all families on \(\{1\}\) | Identify the empty-support exclusion |
| Fixture | Re-run the four-set checker | Reproduce three expected outputs |
| Lemma candidate | Verify singleton injection for a new family | Exhibit injection and inverse on image |
| Open direction | Describe a proof route for families without singleton members | State the missing noncircular lemma; do not claim it |

## Certification path and continuation graph

The first independently checkable claim is finite union closure plus frequency counts; its code can be reproduced without MATHSOLVE. The singleton lemma admits a short Lean statement under finite-family hypotheses. Any broader theorem requires a protected Solve package and independent Cert review.

`four-set fixture → singleton lemma → two-element member families → exact small-universe certificates → universal local-to-global bridge [OPEN]`

## Trust quartet

**What is proved?** The elementary singleton lemma and protected restricted claims within their hypotheses. **What is checked?** The displayed finite family and registered bounded replay artifacts. **What remains open?** Universal half-frequency. **External verification?** New source-dependent or purported universal proof steps require independent audit.

## Bibliography and source audit

| Source | Use | Imported claim / audit state |
| --- | --- | --- |
| [Domain master plan](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/DOMAIN_01_UNION_CLOSED_MASTER_PLAN.md) | Locked definitions, bounds, debt | Protected Programme authority |
| [Published documentary](../documentaries/union_closed.md) | Examples and historical exposition | Reader source, not theorem authority |
| Reimer, Gilmer, Yu (listed in master plan) | Further learning | Imported results; check exact source statement before reuse |

**First executable step with completion test:** Run the four-set fixture above, independently verify the singleton injection, and write an exact one-paragraph account of why neither verifies every finite family.

## 8. First executable step

Read tracker #1 and the current protected master plan. For mathematics, select the smallest exact residual not already covered by qualified restricted claims. For documentary work, inspect the admitted edition record and full-tier reader, then open a bounded editorial correction supported by exact published sources.
