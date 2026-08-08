# CMDG-NAT-CONCORDANCE-001

## Status

`CMDG-NAT-CONCORDANCE-001` is the first bounded foundational concordance operation under the Certified Reconstruction of the Mathematical Dependency Graph (CMDG).

It commences from protected `MATH-PROGRAMME` main at:

`f518ae19aa46733c77727ee353983721aa8ffa85`

and relies on the foundational profiles admitted by `CMDG-NAT-CONCORDANCE-FOUNDATIONS-PROFILE-001`.

The package is a **candidate pending independent exact-head review and protected admission**. The artifacts in this branch do not confer concordance authority by themselves.

## What is being compared

The operation keeps three identities distinct.

### `N_DTT`

`N_DTT` is Lean's kernel-level `Nat` object at the retained proof-environment pin:

- Lean toolchain: `leanprover/lean4:v4.33.0-rc1`;
- Lean commit: `62eed1db4d67327ec8120be05f1a1b0847d74561`;
- declaration: `Nat`;
- constructors: `Nat.zero`, `Nat.succ`.

The operation uses Lean's checked interfaces for addition, multiplication, order, and divisibility.

### `N_ZFC`

`N_ZFC` is the bounded finite-von-Neumann-ordinal image inside the retained `ZFSet` implementation:

```text
zNat n := ((n : Ordinal).toZFSet)
```

The retained mathlib revision is:

`79d0395a1825a6264ad5d269e35e60537518955e`

The checked construction uses mathlib's finite ordinal conversion and its `ZFSet` theorems. In particular, the implementation can prove the expected zero, successor, membership/order, and finite arithmetic transport facts.

This is deliberately narrower than a formula-by-formula certification of the Programme's syntactic ZFC object theory. Lean `Nat` is used as the metatheoretic index of the finite ordinal image. The package therefore does **not** claim that the syntactic ZFC theory, the `ZFSet` carrier, and Lean's DTT substrate are definitionally identical or globally equivalent.

For the finite image, arithmetic is represented by checked operations induced through ordinal rank:

```text
zAdd x y := (rank x + rank y).toZFSet
zMul x y := (rank x * rank y).toZFSet
zLe  x y := x ⊆ y
zDvd x y := ∃ k : Nat, zMul x (zNat k) = y
```

The concordance claims for these operations are restricted to inputs in the image of `zNat`.

### `N_NNO`

`N_NNO` is a concrete realization of the admitted categorical natural-numbers-object recursor profile in `Type`.

The chosen terminal object is `Unit`; the carrier is `Nat`; zero is `Unit → Nat`; successor is `Nat.succ`. The Lean fixture directly proves that for every target type `X`, point `x0 : Unit → X`, and endomorphism `s : X → X`, there exists a unique mediator `h : Nat → X` satisfying:

```text
h ∘ zero = x0
h ∘ succ = s ∘ h
```

This realizes the admitted recursor universal property without introducing a binary-coproduct assumption.

`N_DTT` and this concrete `N_NNO` realization share the formal Lean carrier `Nat`, so their operation transports are definitionally checked in this implementation. They remain distinct CMDG semantic roles; this fact is not promoted into a blanket equivalence of dependent type theory and categorical foundations.

## Directional maps

The package binds exactly three directional maps:

| Map | Source | Target | Formal realization |
|---|---|---|---|
| `CMDG:NAT:MAP:DTT_TO_ZFC` | `N_DTT` | `N_ZFC` | `CMDG.NatConcordance.zNat` |
| `CMDG:NAT:MAP:DTT_TO_NNO` | `N_DTT` | `N_NNO` | `CMDG.NatConcordance.dttToNNO` |
| `CMDG:NAT:MAP:NNO_TO_ZFC` | `N_NNO` | `N_ZFC` | `CMDG.NatConcordance.nnoToZfc` |

No reverse map is inferred automatically. No transitive composition is treated as direct semantic authority.

## Operation matrix

Each directional map must carry checked evidence for exactly six operations.

| Operation | DTT → ZFC | DTT → NNO | NNO → ZFC |
|---|---|---|---|
| zero | `zNat_zero` | `dttToNNO_zero` | `nnoToZfc_zero` |
| successor | `zNat_succ` | `dttToNNO_succ` | `nnoToZfc_succ` |
| addition | `zAdd_zNat` | `dttToNNO_add` | `nnoToZfc_add` |
| multiplication | `zMul_zNat` | `dttToNNO_mul` | `nnoToZfc_mul` |
| order | `zLe_zNat` | `dttToNNO_le` | `nnoToZfc_le` |
| divisibility | `zDvd_zNat` | `dttToNNO_dvd` | `nnoToZfc_dvd` |

The root theorem `CMDG.NatConcordance.bounded_concordance` touches the complete declared operation surface and the concrete NNO universal property. It is used as the declaration-level dependency and axiom extraction root.

## Evidence and replay

The formal fixture is:

`fixtures/formal/CMDG-NAT-CONCORDANCE-001`

It is independently pinned by its own `lean-toolchain` and `lake-manifest.json`. The Programme workflow must:

1. validate the governed concordance record and graph proposal artifacts;
2. run the adversarial mutation suite;
3. build the Lean fixture in the pinned environment;
4. run the checked declaration dependency extractor against `CMDG.NatConcordance.bounded_concordance`;
5. compare the observed declaration-level axiom footprint with the retained expected footprint;
6. fail closed on any mismatch.

The dependency extractor emits `G_proof`, implementation, and provenance evidence only. It does not itself confer semantic authority.

## Graph authority

The package contains three semantic `TRANSPORTS_ALONG` proposals and three cross-layer `REALIZES_AS` proposals. Every one is intentionally recorded as:

`authority_state: PROPOSED`

The candidate therefore cannot self-ratify its semantic edges. Promotion, if warranted, requires independent exact-head review and protected admission under the existing CMDG contracts.

Every proposed `REALIZES_AS` record keeps the automatic stronger claims false:

- no definitional equality;
- no automatic mathematical equivalence;
- no automatic source-faithful identity;
- no automatic foundational concordance.

## Fail-closed conditions

The validator and mutation suite reject at least:

- foundational-profile version or protected-merge drift;
- Lean or mathlib pin drift;
- `N_DTT`, `N_ZFC`, or `N_NNO` identity drift;
- transport-direction reversal;
- missing or duplicate operation evidence;
- substituted order or divisibility evidence;
- an unproved operation marked admitted;
- direct semantic authority without the required review state;
- `REALIZES_AS` automatic-claim promotion;
- cross-foundational definitional-identity claims;
- foundational-equivalence promotion;
- artifact-only admission bypass;
- `GRAPH_CERTIFIED` promotion;
- global dependency-completeness promotion.

## Claim boundary

If independently reviewed and admitted to protected `main`, this operation may establish only the **bounded natural-number concordance** represented by the checked maps and operation matrix above.

It does not establish:

- equivalence of DTT and ZFC foundations;
- consistency of ZFC or of the retained implementation;
- standardness of a ZFC model;
- a formula-by-formula realization of the complete syntactic ZFC object theory;
- categorical-foundational equivalence beyond the proved NNO universal property;
- minimality or uniqueness of the CMDG foundational path;
- global dependency completeness;
- `GRAPH_CERTIFIED` status absent a separate production manifest satisfying all protected runtime gates.

`CMDG-C04`, `CMDG-C05`, and `CMDG-C06` remain unchanged.

## Successor

After protected closure of this bounded concordance operation, the next authorized substantive operation is:

`CMDG-EUCLID-BRIDGE-001`

Its purpose is to transport the already protected Euclid GCD exemplar across the admitted natural-number concordance boundary without changing the original theorem's certification status or claim scope.
