# Replay registration

The final T3-011-C candidate must register both governed entrypoints in `ci/campaign_replay_registry.json` before review readiness:

- `OZ-RT-BZ-T3-011-C-PRODUCER` -> `python3 campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_011_c.py`;
- `OZ-RT-BZ-T3-011-C-VERIFIER` -> `python3 campaigns/odd_zeta/OZ_RT_BZ_T3_010/verify_t3_011_c.py`.

This note creates no exemption. Absence of either registry entry is a blocking implementation defect.
