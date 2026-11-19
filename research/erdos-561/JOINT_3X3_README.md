# ERDOS-561-DEGREE-CORE-JOINT-3X3 — review candidate

**Status:** DRAFT mathematical research evidence. **Not** protected-certified, peer-reviewed, or a proof of unrestricted Erdős #561.

## Main contributions

1. A universal degree-core obstruction for failed bounded-degree edge partitions, with explicit edge- and vertex-budget consequences.
2. Exact simultaneous joint residual Ramsey bound for **all** pairs of three-star forests, using a bounded 82-instance arithmetic certificate (not a search over arbitrary graphs).
3. An original Erdős #561 theorem for all three-star pairs with `n_1+m_1 >=12`, including asymmetric, nonuniform forests.
4. A complete ordinary mathematical proof (with finite integer-bound certificate) for `rhat(F(4,2,2),F(4,3,1))=24` replacing the earlier 11,197-graph classification and Δ=5 critical graph density dependence.
5. A finite parameter shortlist of 851 ordered small pairs **not excluded by these particular gates**; do not treat the list as a list of unresolved problems without literature reconciliation.

Read `JOINT_3x3_AND_DEGREE_CORE_PROOF.md` first, then run the certificate scripts. The theorem relies on standard Lovász `(g,f)` factor and Vizing edge-colouring theorems and on You's 2026 two-component preprint for the no-switch case.

## Run

```bash
python verify_joint3_finite.py > /tmp/joint3.json
python verify_original_remaining.py > /tmp/original_remaining.json
python verify_core_and_switching.py > /tmp/core_checks.json
sha256sum -c SHA256SUMS.txt
```

`verify_core_and_switching.py` requires NetworkX 3.x solely for a small graph-atlas corroboration; the main 82-case and 851-shortlist scripts use **only the Python standard library**. Exact finite results are checked by assertions. The mathematical proof is required for the unbounded reduction; script success alone does not establish the general theorem.

## Source authority

- Chunlin You, *Size Ramsey numbers of star forests with two components on one side*, arXiv:2610.25958v1 (2026-10-19): https://arxiv.org/abs/2610.25958
- Lovász `(g,f)` factor theorem, matching statement in Kano's manuscript: https://gorogoro.cis.ibaraki.ac.jp/web/papers/kano2001-c.pdf
- Vizing's edge-colouring theorem: standard classical theorem; no conjectural density bound used.

Research tracking: `grandchallenge/MATH-PROGRAMME` issues #3490 (joint residual) and #3502 (exact fixed instance). This packet does **not** supersede draft PR #3509's records until internal adjudication accepts the shorter derivation.