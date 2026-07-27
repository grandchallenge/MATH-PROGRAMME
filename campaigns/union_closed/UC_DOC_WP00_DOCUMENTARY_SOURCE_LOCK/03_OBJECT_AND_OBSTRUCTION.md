# Object and obstruction

## Object

For a finite universe `U` and family `F subseteq P(U)`:

- `F` is union-closed when `A,B in F` implies `A union B in F`;
- `support(F)` is the union of all members;
- `frequency_F(x)` counts members containing `x`;
- `x` is abundant when `2 * frequency_F(x) >= |F|`.

Frankl's conjecture asserts an abundant element for every finite nontrivial union-closed family.

## Small exact model

The family

```text
{{1,2}, {2,3}, {1,2,3}, {2,4}, {1,2,4}, {1,2,3,4}}
```

is union-closed. Element `2` occurs six times, so it is abundant.

The powerset is the sharp model: every ground element occurs in exactly half of its members.

## Principal obstruction

Union-closure is local and algebraic; abundance is global and statistical. Pairwise closure must force a column of the incidence matrix to reach one half without a preferred coordinate.

The smallest exact failures of common mechanisms are:

1. union maps collide unless a singleton supplies an injective toggle;
2. average-set-size bounds retain a support-size denominator;
3. compressions may destroy closure or frequency monotonicity;
4. minimal-counterexample restrictions need not be jointly inconsistent;
5. finite verification has no unbounded reduction;
6. entropy growth of the basic form stalls near the golden-ratio constant.

The documentary must expose these obstructions before presenting theorem terrain.
