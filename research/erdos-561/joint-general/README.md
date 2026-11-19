# Erdős #561 — joint residual hypothesis: an unrestricted-host partial theorem

**Disposition: PARTIAL, with several rigorously proved unbounded subcases. The full issue #3490 is NOT proved or refuted.** Research date 2026-11-19.

The joint-residual issue asks: if a graph arrows both the red-largest-star-deleted forest versus the full blue forest and the full red forest versus the blue-largest-star-deleted forest, must it have at least the sum of the antidiagonal star-host weights except the first? This package proves important parts of that claim without limiting the host graph to stars.

**Main mathematical result (Theorem B):** If the red target has `s≥3` positive stars and the blue target has `t≥4` positive stars, then every finite simple graph satisfying BOTH residual arrowing conditions has at least

`2*m1 + sum(n) + (t-4)*n1`

edges. A symmetric bound `2*n1 + sum(m) + (s-4)*m1` holds when `s≥4`. This is a constructive theorem: below that threshold, `verify_iterated_peeling.py` outputs an actual edge two-colouring defeating at least one residual relation, and `exact_arbitrary_host.py` independently detects both target forests as ordinary vertex-disjoint noninduced subgraphs. The manuscript proves the claim for ALL finite simple graphs, regardless of size or topology. No computational enumeration is used as a substitute for the proof.

**Exact infinite families:** For `s=3` and arbitrary `t≥4`, `n=(a,1,1)`, `m=(b,c,1,...,1)` with `a≥c≥1`, `b≥a+c−1`, the joint-residual minimum is exactly `2b+(t−3)a+2`. In particular, `(2,1,1)` versus `(4,1,1,1,1)` has exact threshold **14 edges**. For `(2r,1,1)` versus `(3r,r,1,1)`, the threshold is `8r+2` while the algebraic switching surplus is `r`, unbounded. Also exact for `(a,1^(s−1))` versus `(a,1^(t−1))` for all `s,t≥3`, and the all-matching case.

**All star hosts, all parameters:** Theorem A gives an unconditional if-and-only-if characterization of when a disjoint union of stars arrows any two star forests. The simultaneous residual star-host problem is exactly solved for all lengths `s,t`, and its minimum is `J=Σ(k≥3)w_k`; the unique equality host consists of the corresponding antidiagonal stars. This does not settle nonstar hosts.

**Falsification searches:** 155,737 disjoint-star host/parameter-pair comparisons covering 420 parameter pairs with three through five target components; no witness. For the genuinely unresolved `(2,1,1)` versus `(4,1,1,1,1)`, we separately checked all 9,250 eligible-simple one-vertex-identification candidates derived from all relevant 12- and 13-edge star-host partitions. That example was subsequently PROVED unconditionally by the iterated-peeling theorem; this graph search is retained as corroborating, not needed for the proof. For general targets with nonunit lower-star sizes, the full hypothesis is still OPEN.

**Narrow unresolved benchmark:** `(3,2,1)` versus `(4,2,2,1)` has conjectured `J=15` while the proved elementary and peeling inequalities yield 14. A graph with 14 edges arrowing BOTH residual pairs would refute the issue; a proof excluding every such graph would close this benchmark. We found neither and do not infer that the hypothesis holds in general.

Files: `JOINT_RESIDUAL_ITERATED_PEELING_THEOREM.md` (unbounded proofs) and `RIGID_12EDGE_FINITE_THEOREM.md` and `RIGID_13EDGE_FINITE_THEOREM.md` (two complete finite 3×4 strict-switching cases), `verify_iterated_peeling.py` and `exact_arbitrary_host.py` (explicit constructive colouring + independent target embeddings), `verify_unbounded_families.py`, `verify_star_host_iff.py`, `star_host_falsifier.py` (independent integer/star tests), `fast_A.py` + `search_five_fast.py` (complete bounded nonstar search), `FALSIFICATION_SEARCH_EVIDENCE.json`, source logs, `RUN_MATRIX.md`, `CLAIM_LEDGER.json`, `EXECUTION_EVIDENCE.json`, `SHA256SUMS.txt`, and `run_all.sh`.

**Governance:** The general full issue must retain `OPEN/PARTIAL`. The proved paper theorems are new **research claims under mathematical review**, not MATHCERT/public certification; the separate finite checks are CHECKED. No need for separate identities or repetitive approvals under GI-STEWARD-0003, but do not promote the unrestricted conjecture on CI evidence.
