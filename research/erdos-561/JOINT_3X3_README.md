# ERDOS-561-DEGREE-CORE-JOINT-3X3 — review candidate

**Status:** DRAFT mathematical research evidence. **Not** protected-certified, peer-reviewed, or a proof of unrestricted Erdős #561.

## Main contributions

1. A universal degree-core obstruction for failed bounded-degree edge partitions, with explicit edge- and vertex-budget consequences.
2. Exact simultaneous joint residual Ramsey bound for **all** pairs of three-star forests, using a bounded 82-instance arithmetic certificate (not a search over arbitrary graphs).
3. An original Erdős #561 theorem for all three-star pairs with `n_1+m_1 >=12`, including asymmetric, nonuniform forests.
4. A complete ordinary mathematical proof (with finite integer-bound certificate) for `rhat(F(4,2,2),F(4,3,1))=24` replacing the earlier 11,197-graph classification and Δ=5 critical graph density dependence.
5. A finite parameter shortlist of 851 originally, narrowed to **845** by the odd-degree equality-colouring lemma, then to **835** by the even-degree core-equality classification, ordered small pairs **not excluded by these particular gates**; do not treat the list as a list of unresolved problems without literature reconciliation.

Read `JOINT_3x3_AND_DEGREE_CORE_PROOF.md` first, then run the certificate scripts. The theorem relies on standard Lovász `(g,f)` factor and Vizing edge-colouring theorems and on You's 2026 two-component preprint for the no-switch case.

## Run

```bash
python verify_joint3_finite.py > /tmp/joint3.json
python verify_original_remaining.py > /tmp/original_remaining.json
python verify_odd_core.py > /tmp/oddcore.json
python verify_even_core.py > /tmp/even_core.json
python verify_even_core_independent.py > /tmp/even_core_independent.json
python verify_core_and_switching.py > /tmp/core_checks.json
sha256sum -c SHA256SUMS.txt
```

`verify_core_and_switching.py` requires NetworkX 3.x solely for a small graph-atlas corroboration; the main 82-case and 851-shortlist scripts use **only the Python standard library**. Exact finite results are checked by assertions. The mathematical proof is required for the unbounded reduction; script success alone does not establish the general theorem.

## Source authority

- Chunlin You, *Size Ramsey numbers of star forests with two components on one side*, arXiv:2610.25958v1 (2026-10-19): https://arxiv.org/abs/2610.25958
- Lovász `(g,f)` factor theorem, matching statement in Kano's manuscript: https://gorogoro.cis.ibaraki.ac.jp/web/papers/kano2001-c.pdf
- Vizing's edge-colouring theorem: standard classical theorem; no conjectural density bound used.

Research tracking: `grandchallenge/MATH-PROGRAMME` issues #3490 (joint residual) and #3502 (exact fixed instance). This packet does **not** supersede draft PR #3509's records until internal adjudication accepts the shorter derivation.
## Separate review addendum (2026-11-18)

The role-separated adversarial audit is in `ODD_CORE_PARITY_AND_REVIEW.md` and its standalone verifier is `verify_odd_core.py`. The joint-residual deletion directions are now specified explicitly in the manuscript. Theorem C no longer requires zero switching surplus: `W≤D(D+1)/2` suffices for any 3×3 pair with both leading sizes ≥2. This review is performed by the same assistant in a separate logical pass; it is **not independent external certification**. No theorem has been promoted to protected-certified status.

## Even-degree core equality refinement (2026-11-18)

`EVEN_CORE_CAP_PARTITION_THEOREM.md` completely classifies the cap-partition obstruction when the degree-core vertex budget is attained. The only non-partitionable configuration is a complete `K_(D+1)` core with even `D` and odd/odd degree caps; an absent core edge always restores a cap partition. This proves 10 additional ordered 3×3 size-Ramsey instances via the full 3×3 joint-residual result, changing the current arithmetic-gate shortlist `851→845→835`. All new mathematics remains `UNDER_REVIEW`.

## One-slack stability refinement

The standalone mathematical manuscript `ONE_SLACK_CORE_THEOREM.md` proves the exact cap-partition classification when the degree-core vertex bound has one unit of slack, provided `D>=3`. It excludes **80 further ordered** original three-star cases, conditional on the underlying joint residual theorem. The arithmetic research shortlist is now `851→845→835→755`; this is a count of parameters not excluded by the specified gates, **not** a claim of 755 open problems. The case `D=2` is expressly excluded from the stability theorem. Run `python verify_one_slack.py` to replay 29,685 independent finite cap tests and the integer parameters. All mathematics retains `UNDER_REVIEW`.
