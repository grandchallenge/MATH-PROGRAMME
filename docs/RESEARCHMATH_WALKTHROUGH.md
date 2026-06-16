# ResearchMath Walkthrough

<p class="page-deck">This walkthrough follows one ResearchMath-14k row through MATHFORGE without letting the row become an authority. The goal is not to solve the Diophantine problem; the goal is to prove that the intake machine preserves provenance, uncertainty, route choice, and handoff discipline.</p>

## Source row

Fixture `RM-DIO-004` begins with a ResearchMath row whose problem statement is:

```text
Determine all integer pairs (x, y) that satisfy x^2 - x = y^5 - y.
```

The imported dataset status is `unknown`. MATHFORGE does not upgrade that status. It records:

- dataset name and license;
- original and self-contained problem statements;
- `paper_id` and source URL;
- taxonomy as number theory / Diophantine equations;
- evidence URL;
- imported status;
- explicit statement that global status has not been independently reconstructed.

## Step 1: preserve the source

The first artifact is `source_row.json`.

Its role is not interpretation. Its role is preservation. The row is kept as an object that can be hashed, audited, compared, and later rechecked.

```text
source row
  -> serialized bytes
  -> SHA-256 reference
  -> provenance record
```

This prevents later stages from silently rewriting the problem.

## Step 2: build the audited problem card

The second artifact is `problem_card.json`.

MATHFORGE transforms the row into a problem card with a canonical mathematical object:

```text
x^2 - x - y^5 + y = 0
```

The model class is not “polynomial system” in the abstract. It is:

```text
integer points on an affine plane curve
```

That distinction matters. The complex algebraic curve, the rational points, and the integer points are different obligations.

## Step 3: classify the route

The fixture assigns the route:

```text
DIOPHANTINE_ALGEBRAIC_INTAKE
```

and the application lane:

```text
APP-DIO-01
```

This does not mean Gröbner bases solve the problem. It means the polynomial form is useful for intake, finite exact screens, local obstruction search, and deciding when to switch to number-theoretic methods.

The excluded relaxations are part of the artifact:

- complex affine variety does not solve the integer classification problem;
- finite search window does not prove completeness;
- dataset `open_status` is not a certification claim.

## Step 4: emit the MATHSOLVE handoff

The third artifact is `mathsolve_handoff.json`.

It states that MATHSOLVE may open a campaign package and run bounded exact screens. It also states what MATHSOLVE may not do:

```text
mark the ResearchMath problem solved
or certify global status from this intake fixture
```

The handoff contains a Work Package seed with:

- motivating object;
- obstruction;
- theorem spine seed;
- proof-debt register;
- first executable step;
- questions for campaign triage.

## Step 5: propose the first executable step

The first step is deliberately small:

```text
for y in {-1, 0, 1, 2, 3}:
    compute D = 1 + 4(y^5 - y)
    retain y only when D is a nonnegative square
    lift corresponding x values exactly
```

This follows from rewriting the equation as a quadratic in `x`:

```text
x^2 - x - (y^5 - y) = 0.
```

The discriminant is:

```text
D = 1 + 4(y^5 - y).
```

For integer `x`, the discriminant must be a nonnegative square. This is a finite exact sanity screen, not a proof of completeness.

## Step 6: ledger the claims

The claim ledger allows only three claims:

| Claim | Status | Meaning |
| --- | --- | --- |
| `RM-DIO-004-C001` | `AUDITED` | the source row was serialized with provenance |
| `RM-DIO-004-C002` | `AUDITED` | the route classification and canonical extraction were recorded |
| `RM-DIO-004-C003` | `PROVISIONAL` | the row is ready for MATHSOLVE triage |

Forbidden promotions include:

```text
SOLVED
CERTIFIED
CHECKED_GLOBAL_STATUS
COMPLETE_INTEGER_CLASSIFICATION
```

## What CI attacks

The adversarial suite rejects attempts to:

- change imported `unknown` to `solved`;
- remove source provenance;
- falsify artifact hashes;
- allow status promotion;
- alter the canonical polynomial;
- remove the excluded inference;
- mark the handoff solved;
- remove the first executable step;
- certify the provisional handoff;
- remove forbidden promotions.

## What the walkthrough proves

The walkthrough proves that MATHFORGE can ingest a research-problem row without becoming credulous.

It does not prove the Diophantine theorem. It proves the intake discipline:

```text
preserve
  -> audit
  -> classify
  -> bound
  -> hand off
  -> refuse overclaim
```

That is the right first success for a sourcing corpus.
