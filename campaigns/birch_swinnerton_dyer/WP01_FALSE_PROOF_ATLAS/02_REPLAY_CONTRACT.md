# BSD-WP01 replay and interpretation contract

The replay checks structural completeness, unique identifiers, explicit missing obligations, a bounded rejection decision, remediation, and linkage to WP02 theorem interfaces.

The semantic verdicts are justified by exact countermodels or missing-interface arguments. The replay does not automate deep arithmetic verification. Its purpose is to prevent a route from silently crossing a known logical boundary.

Decision semantics:

- `REJECT`: the inference is invalid as stated;
- `NARROW`: the inference may support a strictly smaller claim after its quantifier or normalization is reduced.

No fixture establishes the negation of BSD. No fixture licenses a route that merely avoids its literal wording. A future route must identify every triggered fixture, state whether it rejects or narrows the route, and name the new theorem-grade obligation that bypasses the failure.
