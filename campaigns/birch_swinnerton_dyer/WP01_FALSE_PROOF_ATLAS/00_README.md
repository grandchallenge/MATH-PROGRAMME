# BSD-WP01 — False-proof atlas

Campaign `BSD-001`; state `REVIEW_READY_ELIMINATIVE_ATLAS`.

WP01 is an executable semantic firewall. It rejects recurrent invalid inferences without claiming that the protected BSD statements are false or that a route avoiding the fixtures is correct.

Protected statements remain separate:

- `BSD-RANK-Q`: universal equality of Mordell–Weil and complex analytic rank;
- `BSD-SHA-Q`: universal finiteness of the Tate–Shafarevich group;
- `BSD-LEAD-Q`: the universal normalized complex leading-term formula.

The atlas contains eighteen fixtures covering parity-to-rank promotion, numerical-zero promotion, Selmer/rank conflation, hidden `Sha`, one-prime-to-global promotion, `p`-adic/complex transfer, reduction-profile drift, primitive/imprimitive and complete/incomplete Euler-factor drift, period/isogeny drift, rank-one-to-higher-rank extrapolation, family-to-universal promotion, finite-database promotion, unproved height nondegeneracy, local-condition drift, and circular use of BSD.

Run:

```bash
python campaigns/birch_swinnerton_dyer/WP01_FALSE_PROOF_ATLAS/replay.py
```

A triggered fixture requires route rejection or explicit narrowing. Passing every fixture is not a proof certificate. Mechanism generation and restricted-target selection remain gated.
