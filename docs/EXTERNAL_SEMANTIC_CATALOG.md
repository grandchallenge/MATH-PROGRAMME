# External Mathematical Catalog

This view presents immutable mathematical source records admitted through MATHFORGE. It makes provenance and assurance visible without turning source metadata into Programme truth.

!!! warning "Read the badges literally"
    `SOURCE_LOCKED` means the source object is preserved. `NORMALIZED_REPLAYED` adds reproducible extraction. `SEMANTICALLY_REVIEWED` adds qualified source comparison. `CAMPAIGN_CONCORDANT` adds a reviewed relation to a Programme target. None of these is a proof or MATHCERT certificate.

<div id="semantic-catalog" data-index="../assets/external-semantic-catalog-index.json">
  <div class="catalog-controls">
    <label>Search <input id="catalog-query" type="search" placeholder="Identifier, title, subject, or status"></label>
    <label>Source <select id="catalog-provider"><option value="">All sources</option></select></label>
    <label>MSC subject <select id="catalog-msc"><option value="">All subjects</option></select></label>
    <label>Status assertion <select id="catalog-status"><option value="">All attributed statuses</option></select></label>
    <label>Formal language <select id="catalog-language"><option value="">All languages</option></select></label>
    <label>Assurance <select id="catalog-assurance"><option value="">All tiers</option></select></label>
    <label>Campaign relation <select id="catalog-campaign"><option value="">All campaign relations</option></select></label>
  </div>
  <p id="catalog-summary" role="status">Loading protected catalog metadata…</p>
  <div id="catalog-results"></div>
</div>

Only license-cleared text is displayed. DeepMind entries are public metadata only because individual declarations may retain third-party source terms. Historical superseded entries remain provenance-visible and are never silently rewritten.

## Pillar routing

- MATHFORGE owns intake, normalization, catalog construction, and review evidence.
- MATHSOLVE may consider reviewed catalog entries as proposals. A catalog entry is never a result.
- MATH-CORE receives read-only provenance-bound nodes and typed edges. The catalog cannot mutate the canonical Claim Ledger.
- MATHCERT receives a separately scoped local claim and evidence package. Certification is never inferred from an assurance badge.

## Chaidez promotion boundary

Catalog entries are source records, not work packages, so ordinary intake does
not manufacture a theorem spine or proof dossier. When a qualified reviewer
promotes a `SEMANTICALLY_REVIEWED` entry as a MATHSOLVE proposal, the promotion
must carry a complete Chaidez dossier governed by
`CHAIDEZ-PEDAGOGY-001` version `2.0.0`. An exact imported campaign target also
requires `CAMPAIGN_CONCORDANT` assurance and a reviewed typed relation. The
dossier describes the proposed local work and its limits; it does not upgrade
the source assertion, establish a claim, or authorize certification.
