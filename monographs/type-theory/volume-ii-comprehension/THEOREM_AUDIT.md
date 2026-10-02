# Theorem Audit — Volume II: COMPREHENSION

> **Supersession notice.** The table below is the historical Stage-B1 theorem-audit seed. It does not describe the complete RC1 theorem layer. The exact comprehensive RC1 review scaffold is `reviews/RC1/THEOREM_REVIEW_MATRIX.json`; the review method and claim-boundary requirements are fixed by `reviews/RC1/GATE8_REVIEW_PACKET.md`.
>
> In particular, historical entries marked `planned` below must not be read as current RC1 status. The Gate 8 matrix records fifteen mandatory RC1 result/claim targets. Those candidate results remain subject to genuinely independent mathematical review under issue #853.

## Historical Stage-B1 audit seed

| Result | Statement scope | Dependencies | Critical cases | Status |
|---|---|---|---|---|
| Context formation | COMP-0 | type formation | extension by `x:A` | proved in Ch. 1 |
| Weakening | COMP-0 | context formation, freshness | variable lookup; `Fin(t)` formation | proved in Ch. 1 |
| Substitution on type formation | COMP-0 | term substitution | `Fin(t)` | proved in Ch. 2 |
| Generalized dependent substitution | COMP-0 | substitution on types; induction on trailing context/judgment | variable case; `Fin(t)`; dependent trailing declaration | proved in Ch. 2 |
| Substitution composition | COMP-0 | capture avoidance, freshness | variable collision/renaming | proof workshop; complete for COMP-0 |
| Subject reduction | COMP-ΠΣ | operational semantics | beta; first/second projection | planned |
| Decidable bidirectional checking | COMP-CHECK | syntax-directed equality/checking | application; dependent pair; conversion | planned |
| Strong normalization | none by default | would require separate proof/citation | recursion, universes, eliminators | not claimed |
| Canonicity | later selected fragment only | normalization or direct logical-relations route | closed Nat/Bool terms | postponed pending exact route |

## Historical audit note

The Volume-I publication correction was treated as a standing lesson: substitution is never stated only for `Γ,x:A` when its proof or downstream use requires substitution beneath a trailing dependent context. Volume II therefore began from the generalized form rather than rediscovering that defect later.

## Current RC1 non-result boundary

The exact RC1 Gate 8 packet explicitly requires the reviewer to police the absence of unsupported reliance on full strong normalization, global canonicity, arbitrary dependent definitional-equality decidability/completeness, general positivity/termination checking, full universe consistency, identity-type metatheory, or complete elaboration.
