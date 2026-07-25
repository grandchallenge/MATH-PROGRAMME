# RH-WP01 replay contract

The replay is semantic and structural, not numerical.

For each fixture the checker requires:

1. a unique stable identifier;
2. one explicit tempting but invalid inference;
3. the first missing obligation;
4. a countermodel, domain violation, or theorem-hypothesis failure;
5. a decision in `{REJECT, NARROW}`;
6. a bounded remediation;
7. at least one theorem-ledger interface;
8. a sentence stating what the fixture does not rule out.

The replay fails closed if an interface is unknown, a fixture is incomplete, a decision is unbounded, or the protected claim is silently changed.

The replay does not decide whether a new proof idea is correct. It only prevents known semantic substitutions from crossing the programme boundary unnoticed.
