# BSD-WP03 replay expectations

The deterministic replay must emit three accepted structural fixtures and three rejected adversarial fixtures:

```text
ACCEPT valid individual candidate
ACCEPT valid finite experiment
ACCEPT valid formal interface
REJECT finite experiment promoted to universal
REJECT numerical-only certificate
REJECT open BSD axiom in formal interface
BSD-WP03 substrate replay passed
```

The individual candidate is a schema fixture only. Its nonsingular Weierstrass model and placeholder claim test structure; they do not constitute a mathematical certificate.

A changed validator must fail closed when:

- an individual claim becomes universal or family-wide;
- a singular Weierstrass model is supplied;
- an analytic claim silently uses an incomplete complex L-function;
- `CERTIFIED` is asserted without proof-producing evidence;
- a finite experiment lacks an immutable snapshot or exact positive population count;
- a formal interface imports `BSD-RANK-Q`, `BSD-SHA-Q`, or `BSD-LEAD-Q` as an axiom;
- any WP04 or mechanism gate is opened inside WP03.
