# External Intake to Certification

<p class="page-deck">This is the operating guide for using an external mathematical source without confusing provenance, review, campaign work, or certification.</p>

!!! warning "The boundary is deliberate"
    A catalog entry is a source record, not a theorem result. Assurance, replay, formal annotations, a Chaidez dossier, and green CI do not certify a mathematical claim. The current production promotion and certification-intake registries are empty.

## The process at a glance

```text
upstream source
  -> immutable MATHFORGE snapshot
  -> normalized catalog entry
  -> semantic review and typed relation
  -> MATHSOLVE proposal
  -> reviewed-promotion Chaidez dossier
  -> scoped MATHCERT handoff
  -> independent certification decision
```

Each arrow is a gate. A later-stage artifact does not rewrite or upgrade the earlier source assertion.

## 1. Admit a source snapshot

MATHFORGE is the intake authority. An observer may notice a changed upstream head, tag, or release, but it never changes admitted identity automatically. Admission requires an immutable snapshot with:

- provider and revision identity;
- source locator and raw-content digest;
- adapter or extractor identity and replay command;
- software, content, and third-party licence dispositions;
- visibility restrictions and known reliability limits.

Use a reviewed exact commit when no suitable immutable release exists, and record why a tag or benchmark release was not used. If a source object disappears or changes, retain the old record historically and fail closed until replay and review are renewed.

## 2. Build and inspect the catalog

Every admitted object receives a stable catalog identifier and a deterministic normalized representation. The catalog records the original statement, formal language and toolchain, MSC2020 classification, separately attributed status assertions, licensing class, review evidence, unresolved ambiguity, and excluded inferences.

Read the assurance badge literally:

| Tier | What it means | What it does not mean |
| --- | --- | --- |
| `SOURCE_LOCKED` | Exact source object is preserved | The statement is understood or true |
| `NORMALIZED_REPLAYED` | Extraction and normalization replay deterministically | The normalized form is semantically equivalent |
| `SEMANTICALLY_REVIEWED` | Qualified review confirms the normalized meaning against the source | A campaign result or proof exists |
| `CAMPAIGN_CONCORDANT` | A reviewed exact relation to a Programme target exists | The target is certified |

Automated matching may propose only `related` or `duplicate_candidate`. Stronger relations such as `same_statement`, `formalizes`, `implies`, or `conflicts` require review.

## 3. Route work to MATHSOLVE

Use a catalog entry as a campaign proposal only when it is `SEMANTICALLY_REVIEWED`. For an exact imported campaign target, require both `CAMPAIGN_CONCORDANT` and the reviewed typed relation.

Do not attach a Chaidez dossier to ordinary intake. A full Chaidez v2 dossier begins only at qualified reviewed promotion into MATHSOLVE. The dossier must identify the immutable catalog release, reviewer and decision, result-status fields, nine-stage exposition, trust quartet, theorem spine, proof debt, foundational profile, first executable step, artifact digests, and explicit non-claim boundary.

Promotion is recorded in the MATHSOLVE promotion registry. It is never inferred from catalog presence, lexical similarity, a status field, or ingestion-time automation.

## 4. Hand off a local claim to MATHCERT

MATHCERT does not receive catalog entries directly. MATHSOLVE must submit the supplemental external-catalog handoff containing:

- protected MATHSOLVE commit;
- registry, dossier, and supplement paths with Git blob and SHA-256 identities;
- catalog and promotion provenance;
- the exact local claim selected for certification;
- theorem-spine node and applicable proof-debt identifiers;
- trust-quartet snapshot and support-route class;
- local replay evidence, certification route, and independent-verification disposition.

The receiving validator rejects mutable references, omitted debt, contradictory trust or status fields, claim inflation, direct catalog intake, and any attempt to infer certification from assurance, replay, formal annotations, or CI.

## Practical checklist

When using an external source, ask these questions in order:

1. Is the exact source snapshot immutable, licensed, and replayable?
2. Is the item present in the catalog with a visible assurance tier and attributed status?
3. Has a qualified reviewer confirmed the normalized meaning?
4. If it is an imported target, is there a reviewed `CAMPAIGN_CONCORDANT` relation?
5. Is the MATHSOLVE proposal accompanied by a complete Chaidez v2 dossier?
6. Does the MATHCERT handoff identify one exact local claim and all applicable debt?
7. Has MATHCERT independently verified that claim?

If an answer is “no”, stop at that boundary. Preserve the source record and its history; do not silently promote it.

## Current state

The protected documentary implementation has been replayed end to end as a canary. It accounts for the 17,288-entry catalog and records zero production promotions and zero production certification intakes. This proves the controls and routing; it does not represent a mathematical promotion or certificate.

For the normative implementation details, see the [Chaidez Conformance Implementation](CHAIDEZ_CONFORMANCE_IMPLEMENTATION.md), [External Mathematical Catalog](EXTERNAL_SEMANTIC_CATALOG.md), and [External Corpus Intake Standard](EXTERNAL_CORPUS_INTAKE_STANDARD.md).
