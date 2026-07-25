# BSD-WP03 — Computational and formal substrate

Campaign `BSD-001`; state `REVIEW_READY_SUBSTRATE`.

WP03 creates a governed substrate for three activities that must never be conflated:

1. **individual-curve certification** — a bounded claim about one explicitly identified elliptic curve;
2. **finite database experimentation** — descriptive, falsifying, or hypothesis-generating analysis over a frozen finite population;
3. **formal interfaces** — algebraic and logical lemmas that can be certified without assuming BSD.

The package supplies machine-readable schemas, positive and adversarial fixtures, a deterministic replay, a claim-promotion policy, and a formal-interface registry. It proves no instance of BSD and contains no certified curve result.

Run:

```bash
python campaigns/birch_swinnerton_dyer/WP03_COMPUTATIONAL_FORMAL_SUBSTRATE/replay.py
```

The replay checks that:

- a certificate cannot be universal, family-wide, or numerically supported only;
- a database experiment must bind a finite snapshot, explicit query, and exact population count;
- no finite dataset can discharge `BSD-RANK-Q`, `BSD-SHA-Q`, or `BSD-LEAD-Q`;
- formal interfaces cannot import an open BSD statement as an axiom;
- incomplete and complete \(L\)-function normalizations remain distinct;
- one-prime information cannot be promoted to a global leading-term identity;
- WP04 target selection remains closed.

Passing WP03 validates the substrate contract only. It is not evidence for BSD, a mechanism, novelty, or a restricted target.
