# Reviewed MATHSOLVE Routing Terminology

## Complete Cert disposition

A content-addressed MATHCERT result whose status closes the requested review route. It can be positive, negative, or proof-debt-bearing. The complete states are `ready`, `submitted`, `certified`, `qualified`, `rejected`, and `proof_debt`.

## Positive Cert disposition

A MATHCERT result that can support positive mathematical promotion. The only positive states are `certified` and `qualified`.

## Stage-scoped Solve waiver

A reviewed exception that names the exact Programme stages it covers. It requires Referee, Steward, and Human Steward authority, a Human Steward authorization identity, a reason, a scope, and a future review date.

## Cert route identity

A concrete `grandchallenge/MATHCERT` issue that owns the certification intake and later disposition for one campaign.

## Programme-embedded retrospective route

A historical registration for Solve-owned work that already exists in MATH-PROGRAMME. It preserves exact lineage but does not authorize future Solve-owned work to remain in the Programme repository.
