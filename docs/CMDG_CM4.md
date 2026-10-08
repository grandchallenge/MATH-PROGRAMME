# CMDG-CM4 — Free Solid Abelian Groups on Profinite Spaces

<p class="page-deck">A human-facing account of GCL's protected CM4 result: what was proved, why the inherited route was difficult, how the Point-functional bypass works, what remains open, and where to follow the live external-review and mathlib-upstream work.</p>

!!! info "Research surface authority"
    **Canonical campaign tracker:** [MATH-PROGRAMME #355](https://github.com/grandchallenge/MATH-PROGRAMME/issues/355)  
    **Protected mathematical claims** on this page are projections of protected repository records.  
    **Live external-review status** is tracked in [MATH-PROGRAMME #1222](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222).  
    **Live mathlib-upstream status** is tracked in [MATH-PROGRAMME #1223](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1223).  
    If this page and an issue disagree about active work, the issue governs the active-work state. If either conflicts with a protected theorem receipt about an already-certified claim, the protected receipt governs the claim.

## 1. Status

| Field | Current meaning |
| --- | --- |
| Result status | **Protected formal proof** |
| Strongest supported claim | For every profinite space (S), the governed integer-coefficient free solid abelian group is solid at the module level. |
| Formal target | `CMDG.CondensedCM4.cm4Target_via_pointFunctional : CM4Target` |
| Support route | Formal proof |
| Certification state | Formally checked, independently reviewed, protected on `main` |
| P3 disposition | `PROTECTED_CLOSED_BY_UNDERIVED_BYPASS` |
| P4–P6 | Unproved source-route auxiliaries; nonblocking for the selected proof |
| Not claimed | Derived/complex source theorem, arbitrary-ring generalization, C06, CM5, graph/global CMDG completion |
| Live next move | External mathematical review and staged mathlib port; see #1222 and #1223 |

Protected terminal merge: `28aa80edc08833b9945380a848552cd5fb1da363`.

## 2. Plain object

Start with a profinite space (S): a compact, totally disconnected topological space, such as an inverse limit of finite sets.

Condensed mathematics provides a way to form a free condensed abelian group on (S). Solid mathematics then asks for a stronger object, usually written informally as

[
\mathbb Z[S]^{\solid}.
]

The CM4 target asks whether this free solid object is actually **solid** in the precise sense encoded by mathlib's `CondensedMod.IsSolid` predicate.

For a lay reader: this is a load-bearing interface check. We construct an object intended to live in the solid world, and CM4 proves that it really does.

## 3. Exact obstruction

Current mathlib still describes the corresponding theorem as a hard TODO:

```text
TODO (hard): prove that ((profiniteSolid ℤ).obj S).IsSolid for S : Profinite.
```

The inherited source route passes through derived and cohomological machinery. In GCL's dependency decomposition, that created a difficult P3 profinite Ext/cohomology bridge and downstream source-route obligations P4–P6.

The key question became:

> Are those obligations necessary for the exact module-level theorem, or only for that particular proof architecture?

Our result answers: **they are not necessary for the selected module-level target.**

## 4. Working model

The successful route replaces the difficult global derived obstruction with a detection problem at a single Point fibre.

Very roughly:

1. represent a candidate morphism by the scalar information it induces on locally constant integer-valued functions;
2. express that information in an integral basis supplied by Nöbeling-type freeness;
3. reconstruct arbitrary Point-level measure data from weighted finite Boolean probes;
4. prove that if the scalar functional vanishes, the original morphism vanishes;
5. use that faithfulness to obtain the required solidity statement.

The intuition is analogous to proving that a complicated linear object is zero by finding a family of coordinates that detects every nonzero element.

## 5. Restricted claim

The protected result is deliberately narrow:

```lean
def CM4Target : Prop :=
  ∀ S : Profinite.{u},
    CondensedMod.IsSolid (ULift.{u + 1} ℤ)
      ((Condensed.profiniteSolid (ULift.{u + 1} ℤ)).obj S)
```

and

```lean
theorem cm4Target_via_pointFunctional : CM4Target
```

The `ULift` is the universe-correct form of the integer coefficient ring used by the fixture. The human mathematical content is the integer-coefficient profinite-solid solidity theorem.

## 6. Theorem-spine location

```text
Foundations / sheaves / sites
          │
         CM0  condensed contact
          │
         CM1  discrete–underlying adjunction       [protected closed]
          │
         CM2  Cartesian-closed condensed sets      [protected closed]
          │
         CM3  abelian / homological structure      [protected closed]
          │
         C05  solid definition boundary            [protected closed]
          │
         CM4  solid mathematics                    [protected closed: module-level ℤ]
          │
         CM5  Liquid-Tensor-class benchmark        [open frontier]
```

Inside CM4, the selected route is:

```text
finite Boolean / Nöbeling data
          ↓
Point-measure reconstruction
          ↓
kernel product functional
          ↓
functional faithfulness
          ↓
coefficient solidity
          ↓
profinite-solid solidity
          ↓
CM4 target
```

The historical source route remains represented separately:

```text
P5 ──→ P4 ──→ P6
       ↑       ↑
       └── P3 ┘

P3 is closed by the underived bypass.
P4–P6 remain unproved source auxiliaries, not requirements of the selected route.
```

## 7. Support route

The critical formal interfaces are:

- `measurePointProjection_zero_reflects`
- `measurePointFunctional_zero_reflects`
- `measurePointIntegralFunctional_zero_reflects`
- `weightedFiniteBooleanMeasureLimitLift_measurePoint_allTrue`
- `kernelProductFunctional_eq_zero_of_solidification_kernel`
- `coefficient_eq_zero_of_solidification_kernel`
- `coefficientMappingOutInjectivity_of_pointFunctional`
- `coefficientObject_isSolid_via_pointFunctional`
- `profiniteSolid_isSolid_via_pointFunctional`

The terminal theorem has axiom readback

```text
[propext, Classical.choice, Quot.sound]
```

and no `sorryAx`.

For a reviewer-oriented treatment, see [External Mathematical Review Packet](CMDG-CM4-EXTERNAL-MATHEMATICAL-REVIEW.md).

## 8. Debt audit and claim boundary

### Trust quartet

**What is proved?**  
The governed module-level integer-coefficient CM4 target.

**What is checked?**  
Lean replay, axiom readback, policy/conformance gates, exact-head independent review, protected merge, and terminal protected-main readback.

**What remains open?**  
The broader derived/complex source theorem, arbitrary-ring generalizations, C06, CM5, graph certification, and global CMDG completion.

**What requires external verification now?**  
Independent specialist assessment of the mathematical proof architecture and community review of a mathlib-native upstream port.

### Why P4–P6 still appear

They are not deleted because they encode genuine proof debt for the historical source route. They are marked `NONBLOCKING_SOURCE_AUXILIARY` because the selected underived proof no longer consumes them.

That distinction is part of the result, not administrative cleanup.

## 9. First executable step

There are now two live bounded actions.

1. **External mathematical review:** independently audit the Point-functional proof and return a disposition on [issue #1222](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1222).
2. **Mathlib upstream port:** refactor the downstream proof into mathlib-native layers and track the staged port on [issue #1223](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1223).

The detailed upstream assessment is [Mathlib Upstream Readiness Assessment](CMDG-CM4-MATHLIB-UPSTREAM-ASSESSMENT.md).

## Protected evidence

- Terminal CM4 readback: [repository record](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/cmdg_condensed_cm4_terminal_readback_001.json)
- Terminal P3 closure: [repository record](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/cmdg_condensed_cm4_p3_underived_closure_001.json)
- Terminal CM4 reconciliation: [repository record](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/cmdg_condensed_cm4_underived_reconciliation_001.json)
- Primary proof source: [Point-functional bridge](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4P3GPointFunctional.lean)
- Final wrapper: [CM4 target fixture](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/fixtures/formal/CMDG-NAT-CONCORDANCE-001/CMDGCondensedCM4Blocker.lean)
