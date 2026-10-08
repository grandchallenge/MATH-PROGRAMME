# PNP-001 Accessible Research Guide

!!! info "Research surface authority"
    **LIVE:** [PNP-001 canonical tracker #162](https://github.com/grandchallenge/MATH-PROGRAMME/issues/162).  
    **AUTHORITY:** `PNP-WP00-source-definition-equivalence-audit.md`.  
    **EXPOSITION:** this guide explains current protected state; it does not assert `P = NP` or `P != NP`.

## 1. Status

P versus NP remains open. The campaign has a protected machine/encoding/source baseline, an executable false-proof atlas, and a theorem/barrier/lower-bound ledger. No terminal theorem packet is ready.

## 2. Plain object

The target is the exact uniform language-theoretic proposition comparing deterministic and nondeterministic polynomial time under locked Turing-machine, encoding, malformed-input, bit-length, and many-one reduction conventions.

## Reader entry and prerequisites

**Status:** open complexity separation, source/encoding baseline audited. **Audience:** undergraduate algorithms students, graduate complexity readers, agentic formalizers. **Time to first example:** 10 minutes. **Time to first fixture:** 10 minutes.

| Level | Concepts |
| --- | --- |
| Required | Boolean logic, finite algorithms, truth assignments |
| Helpful | Asymptotic bit complexity, reductions, Turing machines |
| Deferred | Relativization, circuit lower bounds, proof complexity |

## 3. Exact obstruction

The current blocker is definition-level concordance: any imported formal statement or restricted result must be shown to match the Programme machine-and-encoding lock before it can serve as a theorem interface. Restricted circuit, proof-complexity, oracle, or nonuniform results cannot be silently upgraded.

## 4. Working model

Historical theorem work embedded in Programme is frozen as lineage. New mathematical work must be Solve-owned or explicitly waived and must carry the full uniformity/encoding/reduction assumptions.

## Core bridge and first examples by hand

**Friendly example:** \(\varphi=(x\lor y)\land(\neg x\lor y)\) is satisfiable: take \(y=\mathrm{true}\), either value of \(x\). A supplied assignment is an efficiently checkable certificate.

**Edge example:** \(\psi=x\land\neg x\) is unsatisfiable. Trying both assignments proves this *one* instance unsatisfiable. This finite case does not imply an efficient general SAT solver or \(P=NP\).

Bridge: Boolean formula → assignment certificate → fast verification → potentially vast witness search → exact uniform complexity-class question.

## First computation or fixture

Run with Python 3:

```python
from itertools import product
def sat1(x, y): return (x or y) and ((not x) or y)
def sat2(x): return x and (not x)
print(sum(sat1(x, y) for x, y in product((False, True), repeat=2)))
print(sum(sat2(x) for x in (False, True)))
# Expected: 2 and 0, on separate lines
```

**Support route:** exact finite verification of two formulas. **Limitation:** exhaustive search is exponential in the number of variables in general.

## First theorem or local proposition

**Certificate verification lemma.** Given a CNF formula and a complete Boolean assignment, checking whether the assignment satisfies the formula requires inspecting each literal occurrence at most once and can be implemented in time linear in the encoded formula length. This proves efficient *verification*, not efficient discovery or the P/NP relation.

## 5. Theorem-spine location

Authority is `PNP-WP00-source-definition-equivalence-audit.md`; LIVE state is tracker #162. Protected successors include WP01 false-proof controls and WP02 theorem/barrier/lower-bound bookkeeping.

## 6. Debt audit

The next debt is an exact definition-concordance audit that yields one bounded theorem interface. Only after that should a restricted algorithmic or lower-bound target be opened.

## 7. Claim boundary

No new polynomial-time algorithm for an NP-complete language, unrestricted machine/circuit lower bound, barrier circumvention, novelty, or priority claim is admitted.

## Challenge ladder

| Stage | Duty | Completion test |
| --- | --- | --- |
| Exercise | Evaluate \(\varphi\) with \(y=1\) | Both clauses true |
| Exploration | Find all satisfying assignments | Exactly two |
| Fixture | Run enumeration script | Print 2 and 0 |
| Lemma candidate | State verifier runtime against bit encoding | Bound by formula length |
| Open direction | Choose one restricted complexity claim | State machine model, quantifiers and reductions |

## Certification path and continuation graph

The finite truth-table output is independently checkable; the verifier lemma can be proved from an exact encoding. Any imported formal complexity statement must first pass the locked definition-level concordance audit, then ordinary Solve and Cert review.

`truth-table fixture → certificate verifier → SAT encoding lock → exact restricted barrier/algorithm target → source concordance → Cert [only for named bounded claims]`

## Trust quartet

**Proved:** Boolean evaluation and linear-time certificate verification for a specified encoding. **Checked:** two tiny truth tables. **Open:** \(P\stackrel{?}=NP\). **External verification:** correspondence of imported formal definitions, machine conventions and reductions.

## Bibliography and source audit

| Source | Role | Audit state |
| --- | --- | --- |
| [WP00 source-definition audit](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/PNP-WP00-source-definition-equivalence-audit.md) | Machine and encoding lock | Protected Programme source |
| [Machine/encoding record](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/campaigns/p_vs_np/WP00_SOURCE_DEFINITION_EQUIVALENCE/02_MACHINE_AND_ENCODING_LOCK.md) | Exact model | Protected reference |
| Cook–Levin theorem (sources listed in WP00) | Background imported theorem | Check exact reduction semantics before use |

**First executable step / completion test:** Reproduce the two assignment counts, then write one exact encoding-level statement whose formalization could be compared to WP00 without weakening uniformity or bit-length rules.

## 8. First executable step

Resolve the definition-level relationship between the candidate formal statement and the locked Programme model. Then open one Solve-owned restricted target with all uniformity and encoding assumptions explicit.
