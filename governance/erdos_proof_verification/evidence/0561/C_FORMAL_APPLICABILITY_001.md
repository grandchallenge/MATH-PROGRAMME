# Erdős #561 — Phase C formal applicability and actual kernel scope

**Assignment:** `ERDOS-PV-0561-C` on [cohort issue #3243](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3243). **Held exact reservation:** `a5496eb0bdc1199ce0330de45abc26f05d90e0cd` under `fyremael`. Protected Phase B verification [PR #3458](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3458) merged at `070f9a9d71b22132d48d7c1dc0c05671c11c0a90`; [custody PR #3461](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3461) merged at `ce9775ca3bf86f7a85847e07e7d21c0afc6af391`. Phase C source branch started from the then protected main `3fd1d27e4d0d3942d2d7fe7f0ec72409f653ad99`.

## Formal source and theorem identity

The 1978 Burr–Erdős–Faudree–Rousseau–Schelp question is a **two-target, edge-minimal size Ramsey** conjecture for vertex-disjoint positive-leaf star forests. Its full unrestricted $s,t$ case is OPEN in the primary source. The particular October 2026 paper by Chunlin You, [arXiv:2610.25958v1](https://arxiv.org/html/2610.25958v1) (submitted 19 October 2026), claims to settle the case where one forest has exactly two star components. Only its last conditional factor-gate was reconstructed in Phase B.

The frozen programme catalogue is `teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89:data/problems.yaml` (Git blob `4e60263a80af6207aca494d2e1388e44fa372889`), entry 561, historical status OPEN, unformalized. Source issue #1832 body SHA-256 `040d064d6aa382dbc832b449e8d0869378c145523bf99e795b185997c49751b4`. The *frozen* provider path `google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020:FormalConjectures/ErdosProblems/561.lean` returned **HTTP 404** in an authenticated GitHub read. No existing provider proof or Lean theorem goal was available to replay, and an upstream branch cannot silently replace the protected source lock. The retrieved October preprint HTML byte receipt from B is SHA-256 `abcf3930c1b8d77578286b701d9317b63e7ea3832dcf10c627ef1220a32f04f7` for 433,901 bytes.

**Formal applicability:** `YES_FOR_BOUNDED_ARITHMETIC_LEMMAS`; `FORMAL_PROVIDER_AVAILABLE = NO_IN_FROZEN_SNAPSHOT`; `FULL_GRAPH_FACTOR_FORMALIZATION = FORMALIZATION_WORK_REQUIRED`. A successful local arithmetic compilation is not semantic equivalence with the full mathematical theorem.

## Exact Lean replay

A new, source-controlled module `experiments/erdos_proof_verification/0561/Erdos561Core.lean` imports **only `Init`** and compiles under pinned **Lean 4.33.0** (release compiler commit `d8b18978322de05a8f3dba51ef03cf5461676c17`). The actual kernel verified these **eleven auxiliary declarations**:

1. `degree_minus_lower_eq_min`: truncated degree subtracts to the minimum needed by Lovász's cut formula
2. `tight_degree_iff`: with a positive budget, the lower factor target is tight exactly at ambient maximum degree
3. `split_budget_iff`: local $(g,f)$ bounds are equivalent to the two edge-colour degree budgets, assuming the chosen subdegree does not exceed ambient degree
4. `factor_bounds`: a graph vertex of degree at most $D$ has the required lower factor bound
5. `min_degree_ratio`: the exact integer-cleared local estimate
6. `weighted_to_unweighted`: weighted cut boundary controls unweighted boundary when $\alpha\leq\beta$
7. `all_small_components_impossible`: the cut obstruction and $rD$ lower boundary are inconsistent when every counted component is small
8. `strict_factor_slope`: the reduced paper parameters imply $D<\alpha\beta$
9. `large_component_impossible`: the contrary large-component numerical boundary and Lovász-cut upper bound are inconsistent
10. `odd_odd_product_odd`: the odd-degree/odd-vertex numeric obstruction
11. `component_parity_flips`: the parity condition changes when an edge to $T$ is added

The type of every declaration was printed and hashed separately. The actual `#print axioms` reports contain only Lean's permitted `propext`, `Quot.sound`, and `Classical.choice`; no `sorryAx`, injected axioms, unknown imported theorem, or unfinished proof is accepted. These declarations are **mathematical arithmetic lemmas**, not a graph representation of Lovász's full factor theorem for $(g,f)$, nor a claim that any requisite star decomposition exists.

The fail-closed source/type/axiom replay is `ci/erdos_pv_0561_formal_replay.py`, with exact `C_LEAN_CORE_REPLAY_001.json` and `C_LEAN_CORE_STDOUT_001.txt` receipts. A fresh `--execute` run uses the pinned compiler and checks five deliberately false targets. **All five were rejected** by Lean with nonzero exit and actual error diagnostics. These attack a wrong minimum formula, zero-budget saturation, omitted parity edge, missing strict slope, and a reversed boundary inequality. The separate 12-test suite in `ci/test_erdos_pv_0561_formal_replay.py` rejects altered types, missing axiom reports, injected holes/imports, false-successful hostile results, and false full-theorem promotion. The source itself is stored and hash-checked in the protected receipt, not reconstituted from a claim of success.

## Mathematical and source-to-kernel gap

1. **Lovász factor theorem not encoded.** The source's Lemma 2.5 and Corollary 2.6 quantify over finite simple graphs, *all* disjoint cuts, connected components of an induced residual graph, parity of ambient-degree-saturated components, and existence of a spanning edge partition. The Lean auxiliary module treats vertexwise degree bounds and the already-derived *integer inequalities*; it does not define the graph's connected components, edge sets, or establish the graph-factor equivalence.
2. **Missing source-to-formal structural bridge.** The source's Claims 3.2–3.8 require a counterexample induction, extremal edge budget, maximum matching, star+matching+residual partition, a small residual-edge count, and every maximum-degree vertex being a vertex-disjoint star center. None is kernel checked. Even the paper's full special-case Theorem 1.2 is not independently proved.
3. **Graph cut-count implication not kernel checked.** The jump from each small counted component to at least $D$ crossing edges, or from a large component to at least $D+r$ distinct saturated vertices and then $\beta(D+r)-2e(R)$ crossing edges, is proved as ordinary mathematics in Phase B but not as a Lean graph lemma here.
4. **No source-to-Mathlib equivalence.** `Init` arithmetic types are honest formalized fragments but do not furnish or import a fixed Mathlib `SimpleGraph` source or prove equivalence to a full Ramsey problem statement. The original conjecture is still OPEN; MATHCERT is `NOT_SUBMITTED`.
5. **Compute-custody boundary.** The protected Colab registry exposes no #561 job (`ci/gcl_lean_colab_jobs.py list` returns only Erdős #41 and #248). The replay executed under CHAD's authenticated OS context, with exact toolchain and hash-bound logs, **not** under a Colab execution identity or independent mathematical referee.

## Next formal work and disposition

**Bounded acceptance:** `KERNEL_CHECKED_ARITHMETIC_BRIDGE_ONLY__FULL_GRAPH_FACTOR_AND_PRECURSOR_REDUCTIONS_OPEN`. Formal source semantics, restricted hypotheses, and held claim are recorded exactly. The next substantive work must formalize the finite graph model and exact Lovász cut criterion against a **pinned Mathlib revision or independent no-sorry graph theorem**, then prove the star-center component cut counting, and independently replay the paper's earlier counterexample Claims 3.2–3.8. Distinct nonauthoring logical-role criticism was performed on this scope; it is not independent human review or certification.

Phase C can be admitted as a bounded formal applicability/replay record only. Its success must **not** close the original conjecture, certify the paper's Theorem 1.2, bypass a missing graph theorem, or promote Phase D automatically.
