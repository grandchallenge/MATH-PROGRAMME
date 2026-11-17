# Erdős #560 — separate logical Adversary pass on Phase C

**Role scope:** adversarial, nonauthoring logical review performed under the same authenticated GCL operator as the producer. This is **not** an independent human or independent external theorem referee. Reviewed objects: exact source-locked primary Proposition 2.2; GCL protected Phase B #3434/#3436; new Lean 4.33.0 helper module, full compiler output and `#print axioms`; governed negative tests and source-to-formal gap ledger.

## Threat model and actual tests

**A. Deliberately false statements sent to Lean.** Three negative targets were compiled as fresh temporary files against the *same* core compiler used for the positive source. Each must exit nonzero with a real Lean `error:`, never a resource timeout. All three did:

- **Wrong exponent range:** `2*18^2 < 25^2` is false since `648 > 625`; the true universal gate requires exponent at least four under the original paper's hypotheses. This attacks omitted lower bounds.
- **Divergent-tail exponent:** at `s=2`, `a=1`, the integer-cleared analytic factor inequality is false; dropping `t-s>=2` invalidates this proof method. This is not evidence the original theorem is false in a different regime.
- **Missing looplessness:** take a one-element vertex set with a reflexive adjacency and both parts containing the same vertex. All cross-adjacencies hold, but disjointness fails. The actual `SimpleAdj` premise includes looplessness.

The frozen negative inputs and each compiler diagnostic SHA-256 are in `C_LEAN_CORE_REPLAY_001.json`. All positive theorems report either zero axioms or the standard logical `propext`/`Quot.sound`; no unexpected dependency or unfinished proof is accepted. A separate receipt validator rejects a substituted axiom, removed theorem signature, absent axiom report, injected proof hole, false-successful negative receipt, source/import drift, and false theorem-level completion. Its eleven direct hostile and semantic tests passed.

**B. Host graph source-semantic attacks.**

- **Induced vs non-induced:** the complete seven-vertex host graph contains precisely 105 oriented pairs of sizes 2 and 4 forming non-induced complete bipartite copies. It contains **zero induced** copies of this type because each proposed part contains intra-side edges. A formal theorem using induced copies would be the *wrong* formalization even if Lean proved it.
- **Omitted multiplicity:** with the same complete host, the final degree-ranked left-vertex bucket contains **30** oriented copies, but there are only **15** four-neighbour subsets of that fixed vertex. The choice of remaining left-side vertices cannot be suppressed.
- **Orientation when parameters are equal:** in a complete four-vertex graph, the 2–2 side-pair count is six but the unordered bipartition count is three. Our paper proof requires `s<t`; replacing this with `s<=t` without a new counting convention would create an invalid equality case.
- **Copy-event dependence:** two size-(2,4) copies with the same smaller side and larger sides `{2,3,4,5}` and `{2,3,4,6}` share six cross-edges, with ten distinct cross-edges in their union. Their monochromatic events have joint probability `2/2^10=1/512`, whereas the product of their individual probabilities is `1/16384`. They are *not independent*. The genuine first-moment argument uses linearity of expectation only.
- **Vertex-vs-edge budget:** the variable `q` is the *host edge count* rather than the host vertex count or the number of bipartite pairs. The future proof must use a finite edge set and the degree-sum identity to obtain `i*d_i <= 2*q`.

**C. Source-to-kernel epistemic attacks.** The new Lean semantic predicate is hand-written for an abstract loopless symmetric adjacency relation. It has not been connected in the kernel to `SimpleGraph.IsCompleteBetween` at pinned Mathlib revision `79d0395a1825a6264ad5d269e35e60537518955e`. The frozen FormalConjectures snapshot contains no #560 theorem file. The published Proposition 2.2's graph-count injection, real exponential/binomial power-tail bound, and finite colourings/union-bound reasoning have not been elaborated into Lean. Thus a green compile of our twelve auxiliary results **must not** be advertised as a full theorem proof. The strengthened `4e^2` bound is only an elementary algebraic tightening of known work, not novelty.

## Critical assessment and final scoped disposition

**PASS:** exact source scope, twelve kernel-proved auxiliary lemmas, standard axiom reports, three genuine compiler-rejected false targets, three further mathematically explicit counterexample families, and eleven CI review/receipt tests. **FORMALIZATION_WORK_REQUIRED:** a direct source-to-formal transfer of the central `N_i` bucket injection, the real analytic summation, and the finite edge-colouring union bound. **NOT ESTABLISHED:** original diagonal conjecture, full bounded Proposition 2.2 in Lean, Mathlib semantic equivalence in kernel, independent external verification, or MATHCERT certification.

The Phase C **bounded formal-applicability and adversarial-review assignment** is supported as a reviewed partial-formal evidence packet. Its residual full-formalization obligation is deliberately explicit. Protected admission is an editorial/evidence action; it must not close the mathematical problem or imply that a purported missing no-hole full proof exists.

**Next falsifiable bridge task:** formalize the finite `Finset` of `(S,T)` satisfying `G.IsCompleteBetween`, with side cardinality, disjointness, and non-inducedness; then prove the bucket injection `N_i <= choose(i-1,s-1)*choose(d_i,t)` on a degree-sorted `Fin n` host. Acceptance requires correct exact theorem type, source-to-Mathlib equivalence, a genuine no-hole kernel proof with standard axiom list, a deliberately invalid missing-left-multiplicity target rejected by the compiler, and one protected exact-head replay receipt. If that bridge is not available, the remaining analytic and probabilistic work must remain unadmitted as formal proof.
