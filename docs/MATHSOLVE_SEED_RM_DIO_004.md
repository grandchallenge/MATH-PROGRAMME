# MATHSOLVE Seed: RM-DIO-004

<p class="page-deck">This page is the reader-facing MATHSOLVE campaign seed produced by Fixture 004. It begins where MATHFORGE must stop: with a preserved source, audited uncertainty, and a bounded first action.</p>

## Result-status box

| Field | Value |
| --- | --- |
| Work Package seed | `WP-RM-DIO-004` |
| Source fixture | `RM-DIO-004` |
| Imported status | `unknown` |
| MATHFORGE status | `STATUS_UNVERIFIED_UNKNOWN` |
| MATHSOLVE status | `READY_FOR_TRIAGE` |
| Theorem claim | none |
| Certification claim | none |
| First executable step | finite exact sanity screen |

## Motivating object

The object is the integer-point problem on the affine plane curve:

```text
x^2 - x - y^5 + y = 0.
```

The source question asks for all integer pairs `(x, y)` satisfying the original equation.

## Obstruction

The obstruction is not writing down the polynomial. The obstruction is complete integer classification.

Several weaker objects are easier to produce but do not solve the problem:

- complex solutions;
- rational points;
- finite windows of integer points;
- symbolic manipulation of the polynomial curve;
- dataset status metadata.

MATHSOLVE must therefore make every support boundary explicit.

## Theorem spine seed

The first campaign spine should begin with four modest obligations:

1. **Source reconstruction lemma**  
   The problem statement and imported status are faithfully reconstructed from the source row.

2. **Canonical encoding lemma**  
   The equation `x^2 - x = y^5 - y` is equivalent to `x^2 - x - y^5 + y = 0` over integer pairs.

3. **Finite screen lemma**  
   For a declared finite set of `y` values, the discriminant test produces exactly the lifted integer `x` branches recorded in the ledger.

4. **Status preservation lemma**  
   The finite screen does not promote the problem to solved, certified, or globally classified.

## First executable step

The first step is a sanity screen, not an attack on the full theorem:

```text
Input: finite set Y = {-1, 0, 1, 2, 3}
For each y in Y:
  D := 1 + 4(y^5 - y)
  If D is a nonnegative square:
    x := (1 ± sqrt(D)) / 2
    retain integer x values
Output: finite-screen ledger
```

This step is useful because it is exact, bounded, explainable, and directly derived from the polynomial form.

It is insufficient because it gives no completeness theorem outside the declared finite set.

## Proof-debt register

| Debt | Owner | Promotion condition |
| --- | --- | --- |
| Independent literature/status audit | MATHFORGE + MATHSOLVE | source trail reconstructed beyond the dataset row |
| Source PDF reconstruction | MATHFORGE | cited problem list checked and summarized |
| Finite-screen implementation | MATHSOLVE | exact ledger generated and checked |
| Global arithmetic route selection | MATHSOLVE | number-theoretic method chosen or ruled out |
| Completeness criterion | MATHSOLVE + MATHCERT | theorem statement precise enough for certification handoff |

## Claim ledger seed

The campaign may initially create only these claim classes:

| Claim class | Allowed status | Forbidden promotion |
| --- | --- | --- |
| source reconstruction | `AUDITED` | `CERTIFIED` |
| canonical encoding | `AUDITED` or `CHECKED` after exact verification | global solution claim |
| finite screen | `COMPUTED_EXACTLY` for the declared finite set | completeness |
| route selection | `PROVISIONAL` | theorem proof |
| status audit | `AUDITED` | global open/solved authority without independent source review |

## Negative-result protocol

A failed screen is still evidence if it is bounded and reproducible.

MATHSOLVE should record:

- the finite set searched;
- the arithmetic test applied;
- all retained branches;
- all rejected `y` values;
- the exact reason for rejection;
- the statement that no conclusion outside the finite set follows.

## Escalation gate

The Work Package may escalate beyond intake only when it has:

1. a finite-screen ledger;
2. a clear statement of what the screen did not prove;
3. at least one plausible global method candidate;
4. a proof-debt register with owners;
5. a proposed certification target narrower than the original open problem.

## Handoff boundary

MATHSOLVE may use this seed to begin a campaign. It may not declare the ResearchMath problem solved. It may not treat `unknown` as independently verified open status. It may not ask MATHCERT to certify anything until a precise local theorem or exact certificate exists.

The first meaningful MATHSOLVE success is not a solution. It is a disciplined Work Package whose ledger makes the next honest mathematical move unavoidable.
