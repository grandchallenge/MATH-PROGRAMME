# Degree-core saturation stability — Erdős #561

This research packet contains the unconditional graph-theoretic Theorems 1–2 and Lemma 3 in `LOW_SLACK_CORE_STABILITY_THEOREM.md`, plus a conditional original three-star size-Ramsey application. It reduces the *previously recorded arithmetic gate* from 851 to 535 ordered pairs; it is not a claim that 535 open problems remain.

## Exact execution

```bash
python verify_core_isolation.py > core_isolation_recheck.json
python verify_three_star_low_slack.py > three_star_low_slack_recheck.json
python verify_three_star_independent.py > three_star_independent_recheck.json
sha256sum -c SHA256SUMS.txt
```

`verify_core_isolation.py` requires NetworkX 3.x for an independent bounded seven-vertex graph-atlas test. The two arithmetic checkers use the Python standard library. The unbounded structural theorem is proven mathematically in the manuscript, not by finite checks. The arithmetic corollary depends on the three-star joint residual theorem still under internal review in MATH-PROGRAMME draft PR #3523.

## Review and authorization

Bounded independent-algorithm replay and same-assistant adversarial review are evidence, **not** independently authenticated specialist certification. Keep claims UNDER_REVIEW, draft PR unmerged, the unrestricted Erdős #561 conjecture OPEN. For full certification, verify the exact Lovász non-parity factor specialization and the October 2026 two-component result as a pinned source, and obtain the governed reviewer disposition.