# ERDOS-PV-0562-B — finite triple Ramsey lower bound

Source lock: catalogue 536408716724a2402bdfa7c1d764bf83d64a8c89; source issue #1833 body SHA-256 610b492566fd1ebaf5a156c39fe26850a0f492f18923e607175c9e719e281f5c; protected triage `governance/erdos_proof_verification/triage/0560-0564.json`. Formal provider `google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020`, statement blob fd7acee416ff89473a9b35896f209327f4ab6625 and Ramsey definition blob b427594cfd9e18ddf33ab2eee9c9a76f0dd3527d.

## Exact result

For any natural numbers $M,n$ with $n\ge 4$ and

$$
M^{12}\le 2^{(n-1)(n-2)},
$$

there exists a two-colouring of the triples of a set of $M$ vertices having no monochromatic subset of size $n$. In fact the Lean theorem `finite_integer_bound` negates the precise universal-colouring predicate `RamseyProperty M n`. The predicate quantifies over colourings of all finite subsets of `Fin M`; only triples are tested, as in the locked provider. Nontriple values may be arbitrary. `finite_at_root` specializes this result to the exact integer root `rootFloor ((n-1)*(n-2))`.

The proof orders the actual triple Finset, enumerates Boolean colour vectors, and generates two masks for each actual subset of size $n$. `edgeMask_free`, `fits_edgeMask_of_mono` and `finite_first_moment` establish the coordinate counts and transfer rather than assume them. The number of masks is $2\binom{M}{n}$, each fixes $k=\binom n3$ entries. The union bound applies to overlapping masks. The strict inequality follows from the checked identity $6k=n(n-1)(n-2)$ and the checked bound $\binom{M}{n}\le M^n$. If $M<n$, the colouring condition is vacuous, handled separately. `all_smaller_fail` proves the same failure for every $m\le M$.

`rootFloor a` is defined as the least integer whose twelfth power exceeds $2^a$, minus one. Lean proves both adjacent inequalities, so the root is exact. In ordinary real arithmetic, monotonicity of the positive twelfth power gives $\mathrm{rootFloor}(a)=\lfloor 2^{a/12}\rfloor$. The real-rpow/floor spelling is not itself kernel-checked here. `providerRamsey` is a literal definitional mirror (with attribution) of the locked provider body, not an imported upstream theorem. `provider_triple_eq` checks definitional equality to the infimum of the precise triple predicate. `provider_root_lower` proves the lower bound under the explicit nonemptiness hypothesis that some finite $m$ satisfies that predicate. This is the classical finite hypergraph Ramsey theorem, used in the ordinary mathematical corollary, not a new formal proof of finiteness. No conjectural lower bound is assumed. Thus the ordinary conclusion is

$$
R_3(n)>\left\lfloor 2^{(n-1)(n-2)/12}\right\rfloor \quad(n\ge 4).
$$

The finite colouring theorem is unconditional under its displayed integer hypotheses. The exact provider-shaped infimum corollary is conditional on finite Ramsey existence. This singly exponential bound in $n^2$ does not prove the iterated-logarithm conjecture, even for triples. Phase C must check the exact upstream-definition import or statement bridge, retain the finiteness and real-floor translation limits unless separately formalized, and run the protected formal lane. No MathCERT certification or conjecture promotion.
