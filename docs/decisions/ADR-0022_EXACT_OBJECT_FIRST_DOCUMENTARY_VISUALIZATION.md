# ADR-0022 — Exact-object-first documentary visualization

**Date:** 2026-09-16  
**Status:** Human Steward adopted for future new and materially revised documentary plates; protected merge required for repository authority  
**Supersession boundary:** Extends ADR-0018 for prospective documentary work. It does not authorize blanket replacement of stable existing plates.

## Context

ADR-0018 replaced SVG-first production with representation-first visual pedagogy. The subsequent BSD exemplar exposed a more specific production lesson. Several visually polished plates were semantically weaker than the mathematical concepts they accompanied because the plate rendered an analogy, ledger, or decorative schematic where an exact mathematical object or computation was available.

The corrective BSD pass used computationally generated mathematical objects as the semantic basis of the plates: an elliptic-curve plot with an exact rational point, an exact chord-tangent construction, a finite-field point set and local trace calculation, the strong BSD factor dependency, and a quantified theorem-status frontier. The resulting plates were judged materially more faithful and pedagogically useful.

The Human Steward directed: **"Make this our approach going forward."**

This decision records that direction without converting a visualization into mathematical evidence and without declaring every existing plate defective.

## Decision

For every new documentary plate, and for every existing plate undergoing material visual revision, MATH-PROGRAMME adopts **exact object first; computational rendering where appropriate; delivery format last**.

The default production graph is:

```text
mathematical source / exact object / governed data
  -> domain computation or exact construction
  -> canonical semantic master
  -> visual-semantic review
  -> deterministic annotation and composition
  -> delivery derivatives
       |- PNG / WebP
       |- SVG where the object is naturally vectorial
       |- PDF for print/archive composition
       `- motion / interactive form where mathematically intrinsic
```

## Prospective plate rule

A numbered mathematical plate should contain at least one of the following whenever the adjacent concept admits it:

1. an exact mathematical object or construction;
2. a data-derived or simulation-derived rendering with recoverable provenance;
3. an exact finite computation;
4. a quantified logical, dependency, or theorem-status structure.

A purely atmospheric or metaphorical image should not occupy the primary numbered-plate role when a faithful mathematical representation is reasonably available.

If a concept cannot be rendered faithfully in one of these classes, a schematic or metaphorical plate remains permitted under the literal/nonliteral semantics contract in `docs/VISUAL_PEDAGOGY_STANDARD.md`.

## Renderer policy

Wolfram Language is the preferred default renderer for analytic, geometric, arithmetic, finite-field, symbolic, and scientific visualizations when its mathematical primitives can faithfully generate the intended object.

This preference is not exclusive. A domain-specific renderer, proof assistant, numerical package, plotting system, or exact construction tool should be used instead when it produces a more faithful or auditable semantic master.

The renderer has no mathematical authority. Its role is to generate a reproducible visual representation from an independently governed mathematical source or computation.

## Generative-image boundary

Generative-image systems may contribute non-semantic framing, texture, ornament, or composition only after the mathematical semantic layer is fixed and reviewed.

They must not be the source of truth for:

- curve or surface geometry;
- plotted coordinates or point locations;
- finite-field solution sets;
- numerical values or data encodings;
- equations, symbols, or mathematical labels;
- graph adjacency, topology, multiplicity, direction, or scale;
- theorem-status scope or logical dependency.

If generative composition is used, the exact computational layer must remain available for comparison and the final composition must be checked against it before publication.

## Canonical semantic master

For an `exact`, `data-derived`, or `simulation-derived` plate, the canonical semantic master must retain enough information to audit the mathematics shown. As applicable this includes:

- mathematical source or exact object;
- generator code or notebook;
- renderer identity and material version information;
- parameters, ranges, conventions, and numerical precision;
- source data identity;
- exact labels and values;
- canonical output identity or digest;
- declared post-render annotation operations.

The web-delivery image is a derivative, not the semantic authority.

## BSD exemplar

`BSD-001 — The Hidden Music of Elliptic Curves` is the first positive exemplar for this prospective rule. Its revised visual grammar is:

1. rational point on an elliptic curve -> exact rational triangle;
2. chord-tangent construction -> group-law addition;
3. finite-field point set -> local factor;
4. strong BSD formula -> arithmetic-factor dependency ledger;
5. quantified theorem frontier -> established versus universally open scope.

The exemplar is a production reference, not proof evidence and not a claim promotion.

## Existing documentary estate

This decision does not require immediate full-library replacement.

Existing plates retain their recorded identities and audit dispositions. When an existing documentary is materially revised, its plates must be evaluated against this decision. Stable assets may remain until they are otherwise touched or separately scheduled for migration.

This prospective rule therefore changes the default for future work without silently rewriting the historical documentary estate.

## Authority boundary

This decision changes visual-production method only. It does not:

- certify a theorem;
- promote a mathematical claim;
- make a Wolfram rendering, plot, computation, or generated image proof evidence;
- eliminate the independent visual-semantic review requirement;
- supersede ADR-0010 documentary authority;
- authorize automatic mass migration of all existing plates.

Presentation can expose mathematical structure. Presentation cannot create mathematical authority.
