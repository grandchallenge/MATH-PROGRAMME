# PC-WP04 — Fixture replay and mutation audit

## Bound corpus

The certificate manifest binds these WP03 inputs by Git blob SHA:

- `01_EVENT_SCHEMA.json`;
- `fixtures.json`;
- `validate_histories.py`.

## Replay matrix

The corpus contains fourteen cases:

- two valid histories: separating and nonseparating;
- twelve malformed histories covering source omission, event ordering, missing bundle factor, wrong separating arity, ancestry collision, component loss, unpermitted discard, orientation drift, inadequate finiteness premise, nonempty terminal slice, simple-connectivity conflict, and invalid `RP3#RP3` normalization.

Every run must produce exactly the expected validity result and expected error-code subset.

## Policy mutations

The PC-WP04 policy test copies the formal fixture and checks that the validator rejects:

1. removal of a governing source;
2. removal or renaming of a certified Lean declaration;
3. insertion of an inline `by sorry` placeholder.

These tests protect the certificate boundary; they do not replace the Lean kernel.

## Separation of evidence

- JSON replay checks record-level schema and semantic invariants.
- Policy mutation checks governance integrity.
- Lean replay checks formal definitions and theorems.

No single layer is advertised as proving the imported event relation.

## Repository evidence

Dedicated workflow run `30094600807` passed the complete policy, adversarial-mutation, fixture-replay, placeholder-rejection, and Lean kernel sequence.
