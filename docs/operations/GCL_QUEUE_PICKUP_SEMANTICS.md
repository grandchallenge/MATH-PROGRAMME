# GCL Worker Queue Project #2 — pickup eligibility contract

**Operational rule:** `AVAILABLE` names a **saved Project view**, not a
Project `Status` option. Its protected filter is exactly:

```text
is:open label:gcl-state:available
```

The issue's GitHub **open/closed state** and `gcl-state:available` **label**
control view membership. Project `Status` is a separate workflow/projection
field (`Todo`, `In Progress`, `RETURNED`, `Done`, or unset). The organization
Issue Field `GCL State` is a distinct lifecycle field. No equality test
`Project Status == AVAILABLE` is valid for pickup eligibility.

## Agent preflight (targeted; no whole-Project scan)

1. Read the exact GitHub issue state and labels using the authenticated GitHub
   integration. Require `open` and `gcl-state:available` for AVAILABLE-view
   eligibility.
2. For direct-editorial work, also require
   `gcl-pickup:direct-editorial`, confirm the assignment identity and inspect
   its current RESULT/1, review, claim, and terminal custody before writing.
3. For reservation-controlled work, obey the separate native controller and
   lease requirements; never infer permission to claim from view membership.
4. If necessary, confirm the saved view identity/filter through the existing
   `gcl_queue_class_cutover.py` controls or the read-only queue-view readback.
   A `Todo` or unset Project Status must not produce a false negative.
5. If a direct-editorial result is accepted by the return projector, expect
   the `gcl-state:available` label to be removed and Status to transition to
   `RETURNED` with appropriate Issue Field readback. `RETURNED` is not
   mathematical certification or editorial acceptance.

## Examples (illustrative, not current queue observations)

| Issue | Availability label | Pickup mode | Project Status | AVAILABLE view? | Direct-editorial pickup? |
|---|---|---|---|---|---|
| Open | Present | Direct-editorial | Unset | Yes | Yes, subject to custody |
| Open | Present | Direct-editorial | Todo | Yes | Yes, subject to custody |
| Open | Absent | Direct-editorial | Todo | No | No |
| Open | Present | Reservation-controlled | Todo | Yes | No; obtain native lease |
| Closed | Present | Direct-editorial | Todo | No | No; contradictory state requires reconciliation |
| Open | Absent | Direct-editorial | RETURNED | No | No |

The authoritative filter is defined by `AVAILABLE_FILTER` in
`ci/gcl_queue_class_cutover.py` and checked by its test suite. The existing
return-projection transaction is documented in
`docs/operations/ERDOS_QUEUE_RETURN_PROJECTION.md`. Do not change Project
configuration or lifecycle metadata merely to correct a worker's query.
