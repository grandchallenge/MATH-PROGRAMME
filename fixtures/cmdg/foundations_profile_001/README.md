# CMDG C03 foundational-profile adversarial fixture lane

The canonical positive artifact is
`governance/cmdg_nat_concordance_foundations_profile_001.json`.

Negative fixtures are generated as deterministic in-memory mutations of that
canonical artifact by `tests/test_cmdg_nat_foundations_profile.py`. This avoids
maintaining stale duplicate JSON while still exercising fail-closed rejection
for every required mutation class under issue #304.

No artifact in this directory confers `REALIZES_AS`, foundational concordance,
or `GRAPH_CERTIFIED` authority.
