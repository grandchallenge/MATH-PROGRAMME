# Erdős #560 — Phase D independent logical-role documentary review

**Assignment:** `ERDOS-PV-0560-D`, authenticated operator `fyremael`, claim `0ac8ec3ce8d59868e1d260f8974fb62c36ab0b85`. **Scope of review:** separate logical Adversary/Referee pass on the *public documentary and evidence-state interpretation*, not a separate human mathematical referee. Reviewed objects: the GCL public verification page, its source list, A/B/C protected evidence, CI tests, and the protected cohort ledger at custody commit `1f2c11fe2c3f40c9083ebf8603f0fd25e36d5f21`.

## Documentary attacks and observations

1. **Open diagonal vs proved off-diagonal.** The public page must not replace the target `K_(n,n)` with `K_(s,t)` and then call the original problem solved. The independent bounded lower bound assumes `s>=2, t>=s+2`; the diagonal sets `s=t` and does not satisfy that assumption. The page includes both the precise hypothesis and the explicit exclusion.
2. **Host size is an edge count, not vertices.** The page defines the size Ramsey number using edges, and repeats that `q` is the number of host edges. It does not substitute the ordinary vertex Ramsey number.
3. **Induced vs non-induced.** In `K_7`, there are 105 non-induced `K_(2,4)` cross-complete ordered vertex-set pairs and zero induced such bipartite copies. The page explicitly counts copies with arbitrary intra-part edges; source/statement compatibility is preserved.
4. **Nonauthor review vs logical-role criticism.** GCL's separately executed Adversary pass is by the same authenticated operator, not a distinct externally independent mathematician. The page says this, and does not claim human external certification.
5. **A passing compiler is not a proof of the paper.** Twelve Lean auxiliary lemmas have `#print axioms` and green actual compilation; no source-to-Mathlib equivalence, finite bucket injection, analytic tail, or edge-colouring theorem has been Lean-proved. The page names these exact missing bridges. The frozen FormalConjectures commit lacked `560.lean`; that fact is explicitly bound to the old commit rather than asserted about all future upstream states.
6. **Finite cases cannot establish universality.** The two graph counters independently agreed on 36,168 finite cases and the arithmetic factor passed 987 rational instances. The GCL ordinary proof supplies the general mathematical argument; the page does not extrapolate a theorem from empirical checks.
7. **Provenance is not certification.** Phase B proof evidence, Phase C Lean applicability evidence, and their separate custody merges are individually identified. The page describes a pending Phase D admission rather than falsely claiming that its own unmerged documentation is already protected-admitted. No MATHCERT submission or original-problem closure is implied.
8. **Literature authority and currentness.** The protected catalogue snapshot was historically OPEN, and the maintained Erdős Problems entry is indexed as OPEN, with bounds and citations on its LaTeX/source page. The original 1978/1993 sources were referenced through that bibliography but were not separately re-proved by this work. The 2023 Conlon–Fox–Wigderson paper is the exact source for the bounded method.
9. **No automatic cohort completion.** One of 100 problem records is being reviewed here. Other items remain governed by their own proofs, blockers and per-item returns. Even eventual status `ADMITTED_BOUNDED_COMPLETE` for this specific documentary scope is not a claim that all 100/1,221 entries or the problem itself have terminal mathematical solutions.

## Independent cross-check contract

The documentary evidence validator must reject: changed claimed source number, omitted original-open flag, any claim that all of Proposition 2.2 was Lean-proved, a missing exact Phase B or C receipt, a fabricated external reviewer, a missing residual formalization obligation, an altered public page or main bibliography, wrong original problem citation, a MatCERT/certification promotion, and an improperly admitted D status without protected custody.

## Disposition

**PASS — bounded documentary and source-to-evidence reconciliation, conditional on protected admission.** The documentation accurately explains a known off-diagonal result and discloses the full theorem's missing formal bridges. The diagonal `K_(n,n)` asymptotic remains open and MathCERT remains `NOT_SUBMITTED`. The next proof-work obligation is a genuine, exact-head Mathlib finite-copy bucket injection and then the analytic/first-moment bridges, not additional editorial restatement.
