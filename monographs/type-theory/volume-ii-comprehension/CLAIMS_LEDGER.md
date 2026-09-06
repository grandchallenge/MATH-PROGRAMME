# Claims Ledger — Volume II: COMPREHENSION

> **Supersession notice.** The ledger below is the historical Stage-B1 claim seed. Entries marked `planned` describe the state of the first executable tranche and are not current comprehensive RC1 disposition records.
>
> For the exact comprehensive RC1 claim/review surface, use `releases/RC1/`, `WORKSET_STATE.json`, `reviews/RC1/GATE8_REVIEW_PACKET.md`, and `reviews/RC1/THEOREM_REVIEW_MATRIX.json`. The RC1 candidate remains `RC_COMPOSITION_COMPLETE` and `RC_DURABLY_ADMITTED`; independent mathematical review is pending and publication authority is not granted.

## Historical Stage-B1 claim seed

| ID | Claim | Status | Exact scope | Evidence/source |
|---|---|---|---|---|
| V2-C001 | A type family permits a well-formed type expression to depend on a term already available in the context. | theorem/definition | COMP-0 | Ch. 1 formation rules |
| V2-C002 | Dependent contexts are telescopes: a later declaration may depend on earlier declarations, so context order can be semantically significant. | theorem/definition | COMP-0 | Ch. 1 + Plate 2 |
| V2-C003 | Generalized substitution in a dependent context must rewrite the subject judgment and every trailing declaration that depends on the substituted variable. | theorem | COMP-0 | Ch. 2 theorem + lab evidence |
| V2-C004 | Weakening is admissible when the inserted declaration is well formed and freshness/dependency conditions are respected. | theorem | COMP-0 | Ch. 1 formal interlude |
| V2-C005 | `Π(x:A).B(x)` specializes to an ordinary function type when `x` is not free in `B`. | planned theorem/definitional correspondence | COMP-ΠΣ | Ch. 3 |
| V2-C006 | `Σ(x:A).B(x)` specializes to an ordinary product when `x` is not free in `B`. | planned theorem/definitional correspondence | COMP-ΠΣ | Ch. 4 |
| V2-C007 | Indexed families can make selected invalid states unrepresentable, but only relative to the invariants actually encoded by the family. | formal example + bounded claim | COMP-I | Ch. 6–8 |
| V2-C008 | Bidirectional type checking is decidable for the deliberately restricted COMP-CHECK fragment. | planned theorem + executable result | COMP-CHECK | Ch. 10–13 |
| V2-C009 | The volume does not claim strong normalization or canonicity for every fragment merely because the syntax is dependently typed. | claim boundary | all | VOLUME_PLAN / theorem audit |
| V2-C010 | Categorical comprehension is used as a semantic organization of dependency, not as literal identity between syntax and category theory. | interpretive boundary | semantic chapters | Ch. 13 |
| V2-C011 | “Comprehension” here is not unrestricted set comprehension. | terminology boundary | whole volume | front matter / Ch. 1 |
| V2-C012 | The series-wide claim that type theory is a candidate grammar of computational possibility remains a research thesis. | research hypothesis | series | series handoff + front matter |
