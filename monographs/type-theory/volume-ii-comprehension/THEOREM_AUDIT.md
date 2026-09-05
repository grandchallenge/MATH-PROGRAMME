# Theorem Audit — Volume II: COMPREHENSION

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

## Audit note

The Volume-I publication correction is treated as a standing lesson: substitution is never stated only for `Γ,x:A` when its proof or downstream use requires substitution beneath a trailing dependent context. Volume II starts from the generalized form rather than rediscovering that defect later.
