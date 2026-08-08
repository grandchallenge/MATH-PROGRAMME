# OZ-RT-SHARP12-T1TOP-001

This package audits the source-locked unbounded T1-top obligation

`P_n = sum_{0<=k,l<=n} T(n,k,l) * w5_I(n,k,l)`

against upstream commit `790685b7ee4f642a8a88a1bd120636d1b8b39ea8`, tree `646ee73dd9066e059b043fad64fb20959f111cbf`, Sharp-12 blob `6a347e2a483ec781afac98016635ce1d73b3c38e`.

The source contains substantial finite evidence and a successful weight-3 certificate programme, but no independently replayable unbounded proof object for the exact `w5_I` representative. The weight-5 holonomic route is source-recorded as not obtained; the retained `t_w5` script/log checks finite modular component data only. The later 20-commit source delta changes neither Sharp-12 nor `work/z5la`, so it supplies no silent successor certificate.

Terminal disposition: `OPEN_WITH_CHARACTERIZED_BLOCKER`.

This has `proof_effect: NONE` and `promotion_effect: NONE`. It neither proves nor refutes T1-top, does not certify DEPTH, does not prove Sharp-12 or T3, and does not cover primes 2 or 3.

Reopening requires a deterministic source-locked producer, a canonical unbounded symbolic proof object, complete singularity/boundary treatment, exact recurrence comparison and initial-value propagation where applicable, and an independently implemented verifier, followed by governed replay and protected review/merge gates.
