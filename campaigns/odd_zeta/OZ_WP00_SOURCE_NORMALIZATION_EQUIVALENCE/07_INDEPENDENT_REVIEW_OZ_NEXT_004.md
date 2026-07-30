# OZ-NEXT-004 — Independent intake review

## Decision

The eight-role review package is admissible. Promotion is not.

`OZ-NEXT-004` closes the independent intake-review obligation with a fail-closed Referee verdict. `OZ-WP00` remains open. The package does not authorize `OZ-WP01`, `OZ-WP02`, mechanism generation, new numerical experimentation, a novelty claim, or a new irrationality claim.

## Axiomatist

The formal theorem `Zeta5Odd.zeta_odd_irrational` has a clear target and source-reported axiom boundary. The pinned replay workflow must confirm that boundary independently. The abstract theorem `ZetaLucas.theorem_LB` is correctly read as an implication from H1–H5; it is not a proof that all fifteen submitted families satisfy those hypotheses.

The Brown–Zudilin sharp-12 headline is not presently unconditional. The source certificate ledger states that Theorem B and `(T1-top)` are not certified, while the source referee report identifies verified or certificate-only dependencies in the headline theorem. The intake status `PROVED_IN_PACKAGE` is therefore too strong for `OZ-MSS-S006` and `OZ-CER-E004`.

## Cartographer

`CLAIM_COMPUTATION_INDEX.yaml` indexes every non-literature intake record: ten manuscript statements, three recurrences, four harmonic formulas, six congruences, eight Lean declarations, five certificates, and seven computations. It separates operator definitions from annihilation theorems, paper proofs from Lean proofs, and finite evidence from unbounded statements.

## Grammarian

The following terms are not interchangeable:

- **source-proved**: a proof is present in the acquired package;
- **formally replayed**: the pinned proof object compiled under independent CI and passed an axiom audit;
- **computed exactly**: a bounded exact calculation passed;
- **certified**: an explicit checker or telescoper independently replayed;
- **Referee-accepted**: the complete dependency chain passed independent review.

Every restatement must preserve the modulus and range. In particular, the single-digit congruence modulo `p`, the computed multi-digit statement modulo `p^3`, and the integral-row congruences modulo `p` or `p^2` are different objects.

The minimal companion `bMin` is the factor-six normalization of the classical secondary solution `B(n)` used in much of the literature. This equivalence must be explicit.

## Verifier

The independent local replay produced these results:

| Target | Result | Boundary |
|---|---|---|
| Frobenius certificate checker | PASS | 420 declared prime-window pairs |
| Brown–Zudilin worthiness calculation | PASS | numerical and exact-anchor self-test |
| Brown–Zudilin audit pipeline | PARTIAL | anchor values passed; full validation timed out after 300 seconds |
| Apéry second-row validation | PASS | declared finite exact ranges |
| Phase-2 falsification sweep | PASS | `n <= 360`, `p <= 73`, 5,989 descents |
| Fifteen-family finite sweep | PASS WITH SCOPE FINDING | finite master sweep passed; application hypotheses are not uniformly discharged |

`OZ-CMP-X005` and `OZ-CMP-X007` do not yet have normalized, environment-locked replay commands. The manifest command for `OZ-CMP-X002` omits the required `validate` subcommand.

Pinned Lean replay is performed by the review workflow. A review revision cannot claim `FORMALLY_REPLAYED` until all four workflow jobs pass against that exact revision.

## Adversary

Blocking findings:

1. `OZ-MSS-S006` and `OZ-CER-E004` overstate the sharp-12 status. The acquired source itself records missing decomposition certificates.
2. `lean/ZetaLucas/BZClosedForm.lean` and `lean/ZetaLucas/BZStar.lean` contain quarantined `sorry` declarations. The BZ compact-form Lean theorems downstream of `bz_creative_telescoping` are not certificates.
3. The source-designated proof review for the Apéry second solution is useful evidence but is not independent of the submitted package.
4. The source-locked 37-document corpus does not include the nearest Malik–Straub, Gorodetsky, Straub, Apéry-limits, and Lean-zeta(3) comparison sources. Novelty cannot be completed from the locked corpus alone.
5. `work/lbw/t4_proofcheck.py` prints a `tame` diagnostic based on an argument bound below `p^2`, while formal H4 requires every letter argument to be at most `n`. The script is evidence, not a discharge of H4.

## Formalist

The semantic correspondence audit accepts the following boundaries:

- `OZ-L4-T001` targets only `OZ-MSS-S001`.
- `OZ-L4-T002` targets only the Brown–Zudilin Q-row Lucas theorem.
- `OZ-L4-T003` targets only the clean prime window.
- `OZ-L4-T004` targets the classical integral Apéry row.
- `OZ-L4-T005` targets the abstract H1–H5 theorem.
- `OZ-L4-T006` targets the minimal harmonic Apéry instance, not the computed multi-digit modulus-`p^3` statement.
- `OZ-L4-T007` certifies the exact index `n=2`, not a uniform denominator theorem.
- `OZ-L4-T008` is an operator definition. It does not certify that the submitted double sums satisfy that operator.

## Amanuensis

The review is bound to the A004 manifest blob `a2b55233a77ad05a49f55096864b7c98741411e3`, acquisition-record blob `20771d4515f2238920ac46a8e0186a24c1c06275`, and the two pinned River commits. Local and CI evidence are recorded separately. Source-internal labels are preserved but are not adopted without independent review.

## Theorem-level literature comparison

The 37 locked sources have been classified. The direct findings are:

- `OZ-MSS-S001` is a known special case/fallback in Zudilin’s 2018 elementary theorem. It is not a new mathematical theorem.
- `OZ-CON-C001` and the integral sporadic-row Lucas results are established prior art.
- `OZ-REC-R001` and the classical secondary Apéry solution are prior art; `OZ-HAR-H001` is an equivalent normalization.
- Brown–Zudilin is the direct source for the cellular family, recurrence and displayed coefficients. Its displayed `P_2=1190161/384` contradicts its experimental uncorrected `d_n^5 P_n` integrality statement. The factor-12 correction and submitted compact formulas are extensions beyond that paper.
- The nearest reviewed sporadic-congruence papers concern integral rows. They do not, on the evidence audited here, establish the submitted harmonic B-row congruence or the abstract character-twisted companion theorem. Those objects remain `APPARENTLY_NEW_PENDING_REVIEW`, not `NEW_AFTER_AUDIT`.

The external nearest sources must be acquired and content-addressed before the novelty audit can close.

## Referee verdict

```text
OZ-NEXT-004                         COMPLETE_WITH_BLOCKING_FINDINGS
OZ-WP00                             OPEN
SOURCE LOCK                         COMPLETE
INDEPENDENT FORMAL REPLAY           PENDING UNTIL CI PASSES
SHARP-12 UNIFORM THEOREM             NOT ACCEPTED
APERY SINGLE-DIGIT B-ROW PROOF       SOURCE-PROVED; SPECIALIST REVIEW OPEN
MULTI-DIGIT MOD-p^3 LAW              FINITE EVIDENCE ONLY
THEOREM LB                           ABSTRACT CONDITIONAL THEOREM
BZ COMPACT MIDDLE/ANCHOR FORMULAS     PAPER PROOFS; DEPENDENCY AUDIT OPEN
BZ THREE-TERM COMPACT TOP FORMULA     OPEN
NOVELTY                              NOT AUTHORIZED
NEW IRRATIONALITY CLAIM              NOT AUTHORIZED
```

The next corrective sequence is `OZ-NEXT-005A` through `OZ-NEXT-005D`, as recorded in `REVIEW_REGISTER.yaml`.
