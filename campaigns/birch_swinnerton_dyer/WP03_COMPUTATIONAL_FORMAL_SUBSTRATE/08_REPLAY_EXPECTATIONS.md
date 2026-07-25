# BSD-WP03 replay expectations

The deterministic replay must emit three accepted structural fixtures and five rejected adversarial fixtures:

```text
ACCEPT valid individual candidate
ACCEPT valid finite experiment
ACCEPT valid formal interface
REJECT finite experiment promoted to universal
REJECT numerical-only certificate
REJECT noncomposable WP02 interface
REJECT open BSD axiom in formal interface
REJECT hidden allowed path to universal BSD
BSD-WP03 substrate replay passed
```

The individual candidate is a schema fixture only. Its nonsingular Weierstrass model and placeholder claim test structure; they do not constitute a mathematical certificate.

A changed validator must fail closed when:

- an individual claim becomes universal or family-wide;
- a singular Weierstrass model is supplied;
- an imported WP02 interface is absent, noncomposable, duplicated, or lacks a hypothesis-verification record;
- an analytic claim silently uses an incomplete complex L-function;
- `CERTIFIED` is asserted without proof-producing evidence;
- a finite experiment lacks a content-addressed snapshot, exact query, outputs, or exact positive population count;
- a formal interface imports `BSD-RANK-Q`, `BSD-SHA-Q`, or `BSD-LEAD-Q` through any assumption field;
- the allowed-edge graph contains any direct or indirect path into a universal BSD target;
- any WP04, novelty, or mechanism gate is opened inside WP03.

Changes to the WP02 theorem ledger must trigger this replay because certificate composability is read from WP02 at execution time.
