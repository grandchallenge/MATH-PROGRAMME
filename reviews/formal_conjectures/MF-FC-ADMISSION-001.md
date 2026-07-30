# MF-FC-ADMISSION-001 — Formal Conjectures Provider Admission

## Admission state

`ADMITTED AS SUPPLEMENTAL MATHFORGE EVIDENCE`

## Provider identity

- Repository: `grandchallenge/MATHFORGE`
- Merge commit: `b1cad1a9ed9256b863bb0a8658f06ea715db1230`
- Upstream formal source: `google-deepmind/formal-conjectures`
- Upstream commit: `85f863718beeec7b58a3a1926ee92e3472bc2020`

## Verified MATHFORGE artifacts

| Artifact | Path | Git blob SHA-1 |
|---|---|---|
| External formal-source registry | `governance/external_formal_sources.json` | `4ac46df340e46697452cde4bda5c257df688e68a` |
| Source lock | `formal_sources/formal_conjectures/source_lock.json` | `0ef71adea9bcdfb63da78118f7fee053ccaa73ce` |
| RH/NS pilot snapshot | `formal_sources/formal_conjectures/snapshots/FC-GDM-001-RH-NS-PILOT.json` | `c171b542a60956e59f4cac14fb9413bcdd7ede66` |
| RH concordance | `formal_sources/formal_conjectures/concordance/RH-001.json` | `7332c99795f810ca1d50dda8151c267855d851e7` |
| NS-CI concordance | `formal_sources/formal_conjectures/concordance/NS-CI-001.json` | `1ebe5de5194f48217dff3db02f389154af351592` |

## Campaign dispositions

### RH-001

The upstream Lean declaration is admitted as an exact human-reviewed formulation match. This does not create a Programme-owned Lean equivalence theorem and does not change the campaign's retrospective provider coverage mode.

### NS-CI-001

The upstream Clay alternative A declaration is admitted only as the endpoint of the one-way route:

```text
universal critical integrability
  -> continuation and regularity
  -> Clay alternative A
```

No reverse implication or equivalence is admitted. Existing native MATHFORGE coverage remains authoritative for the NS-CI source and false-proof ledgers.

## Authority boundary

Upstream category metadata is advisory. MATH-PROGRAMME retains current-status and promotion authority. MATHCERT retains proof and certificate authority. The imported artifacts establish provenance and statement concordance only.
