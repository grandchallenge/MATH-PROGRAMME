# Euclid, Book VII: measure, common measure, and the road to gcd

<div class="euclid-micro hero" role="note" aria-label="Edition scope">
<p class="kicker">GCL–Chaidez micro-edition · source-locked historical reader</p>
<p>This reader covers exactly eight admitted Book VII loci from Thomas Heath’s 1908 English edition. Historical statements are separated from modern normalization, executable evidence, and later mathematics.</p>
</div>

## Begin with 252 and 105

Take two positive numbers, `252` and `105`. A source-faithful repeated-subtraction trace can be written:

- `252 - 105 = 147`;
- `147 - 105 = 42`;
- `105 - 42 = 63`;
- `63 - 42 = 21`;
- `42 - 21 = 21`.

At this point `21` measures `42`, and it also measures the original two numbers. The Book VII language is about measuring, common measure, and repeated subtraction. It is not the modern quotient/remainder notation used below.

![Repeated-subtraction plate for 252 and 105](assets/documentaries/euclid_book_vii/plate_anthyphairesis.svg){ .euclid-plate }

**Interpretation.** This plate is `pedagogical_orientation_only`. The authoritative historical statements are the source-locked transcriptions below.

## The historical objects

### VII.def.1 — unit

> An unit is that by virtue of which each of the things that exist is called one.

The protected concordance keeps the unit distinct from Euclidean number. A modern arithmetic carrier with a distinguished multiplicative identity is an interpretive bridge, not a historical identity claim.

### VII.def.2 — number

> A number is a multitude composed of units.

For this bounded reader, admitted Euclidean numbers are represented by positive natural numbers greater than one. Zero, negative integers, and signed coefficients are outside the historical domain represented here.

### VII.def.3 — measuring

> A number is a part of a number, the less of the greater, when it measures the greater;

For positive representatives `m < n`, the bounded modern normalization reads “`m` measures `n`” as: there exists a positive natural `k` with `n = k*m`. The lesser-to-greater orientation is preserved.

### VII.def.5 — multiple

> The greater number is a multiple of the less when it is measured by the less.

In the bounded modern model, `n` is a multiple of positive `m` when `n = k*m` for a positive natural `k`.

### VII.def.12 — prime to one another

> Numbers prime to one another are those which are measured by an unit alone as a common measure.

For admitted positive representatives, the bounded modern normalization is `gcd(a,b) = 1`. This does not import Bézout coefficients or linear Diophantine solvability into the historical statement.

### VII.def.14 — composite to one another

> Numbers composite to one another are those which are measured by some number as a common measure.

For admitted positive representatives, the bounded normalization is existence of a common divisor greater than one, equivalently `gcd(a,b) > 1` in this model.

## The construction

### VII.1 — repeated subtraction and relative primality

> Two unequal numbers being set out, and the less being continually subtracted in turn from the greater, if the number which is left never measures the one before it until an unit is left, the original numbers will be prime to one another.

The protected concordance treats this as a constructive coprimality analogue for unequal positive inputs. “Algorithmic trace” and “certificate” are modern explanatory terms. Division-with-remainder, complexity bounds, extended Euclid, and Bézout identity are not verbatim content of this admitted locus.

### VII.2 — greatest common measure

> Given two numbers not prime to one another, to find their greatest common measure.

Attached porism:

> From this it is manifest that, if a number measure two numbers, it will also measure their greatest common measure.

For positive representatives with a non-unit common divisor, the protected concordance gives a bounded historical bridge to modern greatest-common-divisor reasoning. It does not widen the statement to zero or signed inputs.

## Modern remainder normalization — explicitly later

The compact modern calculation for the same pair is:

- `252 = 2 * 105 + 42`;
- `105 = 2 * 42 + 21`;
- `42 = 2 * 21 + 0`.

This is the **division-with-remainder Euclidean algorithm**, classified by the protected source record as `later_algorithmic_normalization` and `not_verbatim_in_admitted_loci`.

The mathematical output is the modern object `gcd(252,105) = 21`. Stage 1 then supplies a modern Bézout witness:

`21 = -2 * 252 + 5 * 105`.

Stage 2 uses that witness to certify the later linear Diophantine criterion. Neither the Bézout identity nor the linear Diophantine theorem is attributed to Euclid in this edition.

![Historical-to-modern concordance plate](assets/documentaries/euclid_book_vii/plate_concordance.svg){ .euclid-plate }

## Object, construction, witness, certificate

| Surface | In this reader | Authority |
| --- | --- | --- |
| Object | Euclidean unit/number/measuring relations at the eight admitted loci | Historical source surface |
| Construction | Repeated subtraction in VII.1 and VII.2 | Historical source plus bounded concordance |
| Modern object | `gcd(252,105)=21` | Protected Stage 1 modern result |
| Witness | `21 = -2*252 + 5*105` | Protected Stage 1 modern certificate |
| Later theorem | `ax+by=c` solvable iff normalized gcd divides the target | Protected Stage 2 modern certification |
| Plates | Two native SVG orientation aids | `pedagogical_orientation_only` |

## Historical-to-modern concordance

| Locus | Preserved historical content | Bounded modern normalization | Explicit non-extension |
| --- | --- | --- | --- |
| VII.def.1 | unit distinct from number | distinguished unit as interpretive bridge | no universal identification of Euclid’s unit with every modern use of `1` |
| VII.def.2 | multitude of units | positive naturals greater than one | no zero, negatives, or signed coefficients |
| VII.def.3 | lesser measures greater | positive exact divisibility `n=k*m` | no signed/zero-divisor widening |
| VII.def.5 | greater is multiple of less | positive multiple relation | no negative or zero multiple claim |
| VII.def.12 | unit alone is common measure | `gcd(a,b)=1` in admitted positive domain | no Bézout or Diophantine attribution |
| VII.def.14 | some number is common measure | common divisor `>1`, equivalently bounded `gcd>1` | no factorization-uniqueness or ring-general claim |
| VII.1 | alternating repeated subtraction; terminal unit | coprimality certificate for positive unequal representatives | no remainder algorithm, complexity, extended Euclid, or Bézout as verbatim text |
| VII.2 | greatest common measure; porism on every common measure | bounded bridge to modern gcd | no zero/signed inputs, extended Euclid, Bézout, or Diophantine theorem |

## Claim labels

**Historical theorem/evidence.** The quoted definitions, VII.1, VII.2, and its attached porism are the exact governed transcription surface for this edition.

**Modern theorem.** Stage 1 protects `gcd(252,105)=21` and a Bézout witness. Stage 2 protects the stated two-variable linear Diophantine solvability equivalence in its admitted modern scope.

**Interpretation.** “Gcd,” “algorithm,” “trace,” “witness,” and “certificate” organize the historical construction for a modern reader. Their use does not erase the historical unit/number or measuring distinctions.

**Nonclaim.** This edition does not establish historical-modern equivalence, claim that modern remainder notation occurs verbatim in Euclid, attribute extended Euclid, Bézout identity, or linear Diophantine solvability verbatim to Euclid, add another Book VII locus, or claim novelty, priority, or first formalization.

## Technical appendix

### Exact historical source authority

- source repository: `grandchallenge/MATHFORGE`;
- protected source-lock merge: `49071febcacd9c84fe4ff268d4e11d7e0c4ff0e5`;
- source-lock disposition: `EUCLID_BOOK_VII_HEATH_1908_SOURCE_LOCK_AND_BOUNDED_CONCORDANCE`;
- transcription path: `sources/EUCLID-ELEMENTS-BOOK-VII-MICRO-001/heath_1908_book_vii_selected_statements.txt`;
- transcription Git blob: `778718006a60e780ad996e72189bc413c92dc48c`;
- transcription SHA-256: `66d3d62cb75cccc0d705fa06c8845f3d9c2c61952f9994862d54c7679517e6d0`;
- source-lock/concordance Git blob: `287126ea40b30cdbb66bd2e489bde6076a51bcf7`;
- provider-manifest Git blob: `d3f3a36177cef3962fc8b320302e8cea6bb5bd86`.

Edition: *The Thirteen Books of Euclid’s Elements*, Volume II, Books III–IX; Thomas Little Heath, translator/editor; translated from the text of J. L. Heiberg; Cambridge University Press, 1908. The protected source record classifies the governed transcription as public-domain material and records the scan provenance separately from the governed exact-byte statement surface.

### Exact modern protected references

- Stage 1 Programme closeout: `183ff2a0adfbe5bd0ffd5f2e638089b94b868c54`;
- Stage 2 Programme closeout: `6dd51c29b8bcbac812bcf7a4e803b693ac8be69c`;
- Stage 1 MATHCERT merge: `78b69e6a3461a83f4893d61c421b1570c08a9ba6`;
- Stage 2 MATHCERT merge: `cd69013cf55d4ee96539d28ee27eadef64cca06f`.

### Edition authority

The machine-readable edition record, source-reference record, manifest membership, schema, validator, and mutation tests are part of the same atomic admission. The two SVG plates carry no proof, source, or certification authority.
