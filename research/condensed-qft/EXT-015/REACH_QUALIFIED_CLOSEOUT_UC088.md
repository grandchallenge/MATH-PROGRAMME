# REACH closeout — a working renormalized model and the limits of the comparison

**Decision, 25 November 2026.** Close the investigation with the results below and retain ZFC, the programme's original set-theoretic foundation. We obtained a renormalization and quantum factorization theorem for the declared one-dimensional Gaussian/Wick model. We also proved that the original stage-natural weightwise liquid-to-observable equivalence fails in ZFC. The separate degree-two liquid support map has opposite outcomes under two additional set-theoretic principles. The original strong completion criterion remains unmet. This closeout records where the investigation ended and what the proofs establish.

## What we set out to do

REACH combined two questions. The first was whether a free scalar field could be treated rigorously when some of its inputs collide. This meant defining how to subtract singular terms, keeping enough information to perform quantum operations afterward, and proving that the resulting observables combine consistently across regions. The second question was whether two precise mathematical descriptions of that theory agree, one built using liquid mathematics and the other using smooth families of observables. A separate degree-two question asked whether a class in the liquid description can always be captured within a bounded support stage.

The [execution plan](REACH_CONDENSED_RENORMALIZATION_PLAN_090.md) ordered the work from the liquid bridge through zero-scale renormalization, quantum structure, and integration. It kept the degree-two comparison on a separate track. The [original integration adjudication](ORIGINAL_TYPED_INTEGRATION_VERDICT_UC085.md) preserves the original requirements and distinguishes each comparison by its source and target.

## What the model can do

R0 and R1 audited the analytic starting point and constructed the free-field theory on an explicitly controlled class of smooth families. The liquid bridge then gave us a way to compose regulator profiles while retaining their dependence on the regulator. Keeping only the finite physical answer can discard information needed for a subsequent operation. The enriched zero-scale construction keeps the normal data that describe how a kernel approaches a collision. It has a separate operation for reading out the finite physical answer. [R1 closeout](R1_ACCEPTANCE_CLOSEOUT_079.md) · [Liquid bridge](LIQUID_PROFILE_BRIDGE_ACCEPTANCE_093.md) · [Initial zero-scale construction](ZERO_SCALE_EXTENSION_ACCEPTANCE_098.md) · [Mixed-domain zero-scale theorem](MIXED_PUSHDOWN_ACCEPTANCE_110.md) · [Quantum theorem and closeout](QUANTUM_STRUCTURE_ACCEPTANCE_113.md)

For the declared singular Gaussian/Wick class, the subtraction rules are compatible with the quantum differential, changes of scale and the admitted changes of subtraction prescription. The differential squares to zero. A fixed eleven-edge model stressed the construction with 277 proper singular sources, both legal disjoint spinneys, and finite normal decorations. Here a spinney is a collection of disjoint subgraphs that can be subtracted together. Overlapping sources are handled as alternative choices within legal forests. The earlier fixed-host result and the later class-wide theorem have separate proofs and acceptance records. [Fixed-host result](CONSISTENT_HOST_ACCEPTANCE_089.md) · [Class-wide quantum result](QUANTUM_STRUCTURE_ACCEPTANCE_113.md)

For any finite family of disjoint open regions, the local quantum models compose over their common regulator and vacuum algebra at every weight. A region itself can have infinitely many components. At a fixed weight a compact source meets only finitely many components, and higher weights can involve different components. The empty region has the common vacuum algebra, which supplies the unit for composition. A separate gluing theorem reconstructs the completed smooth observable model from a Weiss cover at each fixed profinite test. Such a cover is one in which every finite collection of physical points lies in a member. These statements concern the constructed source class. Its smooth parameter theorem works by controlling entire source histories and retains the prescribed relation for negligible regulator errors. The stronger recovery claim that all the earlier retained families come from this class fails on an explicit two-slot example. [Separated-region composition](SEPARATED_OPENS_INTEGRATION_ACCEPTANCE_UC078.md) · [Completed gluing](EXTENDED_WEISS_ACCEPTANCE_137.md) · [Smooth parameter rule](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) · [Family recovery obstruction](TWO_SLOT_UNIFORM_SOURCE_BOUNDS_ACCEPTANCE_UC057.md)

## Why the original equivalence fails

The comparison can be made explicitly. First the old liquid mapping complexes are realized in the smooth differentiable category. A further, support-compatible map takes them to the actual Gaussian/Wick observables using compact test tensors and insertion into source histories. It is the proposed **equivalence of the two stage diagrams** that fails. The failure is already visible at weight zero, where there are no field inputs. In the original support-valued diagram the allowed output support grows with the stage. A smooth test function supported in the newly available part of a larger interval gives an element that could not occur at the smaller stage. By contrast, all stages on the actual vacuum side have the same regulator algebra and the transition maps are identities. An equivalence compatible with stages would have to carry the strict inclusions on the first side to isomorphisms. This is impossible in ZFC. [Exact smooth comparison and vacuum obstruction](SMOOTH_DERIVED_MAPPING_ACCEPTANCE_UC081.md)

There is also a separate failure of the real-scalar unit comparison. Finite extraction sends the retained Laurent record $\epsilon^{-1}$ to zero, even though the record is nonzero. It sends $\epsilon$ to zero too, yet their product has finite part one. This gives a nonzero kernel and rules out using finite extraction as a multiplicative change from regulator scalars to real scalars. The all-weight product for separated regions works over the shared regulator algebra. The corrected regulator-valued comparison with affine field observables on an interval is an equivalence in weights zero and one and has three additional collision classes in its fibre at weight two. Each of these claims concerns a specified arrow with its own scalar base. [Real-scalar unit and finite extraction](QUANTUM_UNIT_ACCEPTANCE_116.md) · [Regulator-valued affine comparison](FINITE_PARTITION_TENSOR_ACCEPTANCE_UC075.md) · [Typed adjudication](ORIGINAL_TYPED_INTEGRATION_VERDICT_UC085.md)

## What depends on the set-theoretic assumptions

The original R3 question is about a fixed liquid source $H=\underline{\mathcal D_{[-1,1]}(\mathbb R)}$ and the compactly supported test-function targets $G_b=\underline{\mathcal D_{[-b,b]}(\mathbb R)}$, with $G=\varinjlim_b G_b$, in real $p$ liquid modules for the original fixed $0<p\leq1$. The comparison is

$$
\theta_H^2:\varinjlim_b\mathrm{Ext}^2_{\mathrm{Liq}_p(\mathbb R)}(H,G_b)
\longrightarrow
\mathrm{Ext}^2_{\mathrm{Liq}_p(\mathbb R)}(H,G).
$$

Here degree two measures extension classes. The support question is whether every such class has a representative from some single compact-support stage, **after** allowing the changes of representative given by boundaries. An example with unbounded support in one representative would be insufficient. The CH proof produces a genuine class and excludes every possible boundary adjustment and bounded-stage correction.

| Assumption | Verdict on the original map |
| --- | --- |
| ZFC | Injective. Classes already defined on bounded stages retain their distinctions in the global group. |
| ZFC with the continuum hypothesis (CH) | Fails surjectivity. The proof exhibits a global class invisible in each individual output coordinate that still cannot be captured at any bounded stage. |
| ZFC with the partition principle PH1 | Is an isomorphism. The partition argument supplies corrections that work with one finite coordinate bound and yield an actual bounded-stage representative. |

The two implications are theorems under their stated hypotheses. The relative-independence conclusion uses the sufficient consistency premise in the proof, including a model with a weakly compact cardinal for the stated forcing argument and appropriate liquid site bounds. The proof specifies the additional premise for a Grothendieck-universe implementation. The programme retains ZFC and adopts neither CH nor PH1. [Conditional proofs, exact site assumptions and limitations](R3_GLOBAL_SUPPORT_DICHOTOMY_UC022.md) · [Accepted scope](R3_GLOBAL_SUPPORT_ACCEPTANCE_UC024.md)

The maps also explain exactly where the CH class matters. It survives when the original class is realized in the intermediate differentiable Ext group, and it remains outside every differentiable bounded-stage image. The next map evaluates on an actual compact test and passes through degree zero. It kills the degree-two class. So the passage to smooth families preserves this piece of extension information and the subsequent observable readout loses it. PH1 settles the original liquid support question under its assumptions and gives no surjectivity conclusion for that intermediate differentiable map. The construction of the model, its composition over the regulator algebra, its fixed-test gluing and the weight-zero obstruction have their own ZFC proofs. [Survival at differentiable Ext](DIFFERENTIABLE_EXT_CLASS_ACCEPTANCE_UC084.md) · [Observable transfer and three separate conclusions](ORIGINAL_TYPED_INTEGRATION_VERDICT_UC085.md)

## Plan and final disposition

| Planned part | Outcome |
| --- | --- |
| Protocol and liquid bridge | The execution record and the positive-scale liquid realization/composition were admitted. Their comparison uses the declared profile stages and genuine family controls. |
| Zero-scale extension and renormalized quantum structure | R2 is complete on the declared mixed augmented record class, with collision data, legal forest rules, quantum identities and transport. |
| Original degree-two liquid support comparison | R3 yielded the proved conditional verdicts and ZFC injectivity. The original unconditional requirement remains unfulfilled under the programme's chosen foundation. |
| Derived integration | The bounded R4/EXT-015D deliverable is complete by its explicit failure-map option. The original positive equivalence is refuted in ZFC. The admitted narrower maps, composition and gluing have the stated positive scopes. |
| Full original strong exit | Unmet. The investigation is closed with the supported partial, negative and conditional outcomes documented above. |

CP297 recorded the unchanged original terminal condition:

> Full original REACH requires accepted original R3 and correctly typed M5/R4 integration verdicts after protected admission/readback. R0/R1/R2 and separate087-089 are complete within reviewed scopes. One comparison arrow, a nonzero unit cone or this bounded return does not complete the programme.

The 25 November authorization allows a terminal **qualified investigation closeout**, subject to distinct review, protected admission and exact tracker reconciliation. This leaves the historical mathematical criterion above as the measure of the original claim. The bounded comparison docket [EXT-015D](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2657) has a delivered failure map and is eligible for closure as completed after exact protected readback. The recommended closure reason for the original unconditional [R3 docket](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2798) and the strong [parent programme docket](https://github.com/grandchallenge/MATH-PROGRAMME/issues/2617) is GitHub's “not planned”, as administrative endings of the remaining work within this investigation. A qualified closeout supplies neither a new scientific theorem nor an external certification.

## Evidence and limitations

The category, domains, proofs and hostile controls remain in the accepted sources cited above. They include the nonzero even-rank and overlapping-source alternatives, the fixed-test raw lift failures and replacement gluing proof, an escaping-support witness checked against all boundaries, and the nonmultiplicativity and vacuum transition tests. The finite symbolic fixtures check algebra and forest combinatorics. The family estimates, categorical comparisons and dependence on extra foundations use mathematical arguments in the cited proofs. No program run replaces those arguments. The closeout inherits the source assumptions and proves no extension to arbitrary interactions, arbitrary earlier family classes or an equivalence of whole derived categories.

The exact original authority is [the original programme](https://github.com/grandchallenge/MATH-PROGRAMME/blob/1da62ee3e3fadfbdc796ded8330a2d4ebc5ab058/research/condensed-qft/EXT-015/REACH_PROGRAMME.md), with the specification and work packages at the original source identities recorded in [UC085 §1](ORIGINAL_TYPED_INTEGRATION_VERDICT_UC085.md#1-authority-and-exact-evidence). The following sources are fixed at the retained CP298 input cut **1096d2377761080dd4e7b956f00f76b80055d710** (`research/reach-qualified-closeout-uc088-input-20261125`).

| Primary input at the frozen cut | Git blob |
| --- | --- |
| [REACH_CONDENSED_RENORMALIZATION_PLAN_090.md](REACH_CONDENSED_RENORMALIZATION_PLAN_090.md) | 6b642bf10c3328bb64d37474e290810fb45cbca1 |
| [ORIGINAL_TYPED_INTEGRATION_VERDICT_UC085.md](ORIGINAL_TYPED_INTEGRATION_VERDICT_UC085.md) | e407b53dbb944c95bc1eead6de034e0017ea42b5 |
| [R1_ACCEPTANCE_CLOSEOUT_079.md](R1_ACCEPTANCE_CLOSEOUT_079.md) | 360f14cc391da1db9c067181e512953b9ac324fb |
| [LIQUID_PROFILE_BRIDGE_ACCEPTANCE_093.md](LIQUID_PROFILE_BRIDGE_ACCEPTANCE_093.md) | ee6d1c089847f3d5b482e1624d9923a6277ddbe0 |
| [ZERO_SCALE_EXTENSION_ACCEPTANCE_098.md](ZERO_SCALE_EXTENSION_ACCEPTANCE_098.md) | ffd103c5caeebfae6f8d86755daa09ba38cfcd90 |
| [QUANTUM_STRUCTURE_ACCEPTANCE_113.md](QUANTUM_STRUCTURE_ACCEPTANCE_113.md) | e9e0ff6ff3719c23b895e21e9d1e96117a393efe |
| [CONSISTENT_HOST_ACCEPTANCE_089.md](CONSISTENT_HOST_ACCEPTANCE_089.md) | 600a269ffd47b84b1bc9c671125aea3bf61a2f80 |
| [SEPARATED_OPENS_INTEGRATION_ACCEPTANCE_UC078.md](SEPARATED_OPENS_INTEGRATION_ACCEPTANCE_UC078.md) | 22205a07aa522e56283b181b72ccb1934b78409f |
| [EXTENDED_WEISS_ACCEPTANCE_137.md](EXTENDED_WEISS_ACCEPTANCE_137.md) | c573111a3861d2daf6a80ac9767401ad497051ed |
| [COMBINED_PARAMETER_LIQUID_REALIZATION_126.md](COMBINED_PARAMETER_LIQUID_REALIZATION_126.md) | 5b05c6147d237ca1d22e4dcbce9262b0f038c163 |
| [TWO_SLOT_UNIFORM_SOURCE_BOUNDS_ACCEPTANCE_UC057.md](TWO_SLOT_UNIFORM_SOURCE_BOUNDS_ACCEPTANCE_UC057.md) | 5e044cf24d7fb47129c268d1c33e7b4dccd2a771 |
| [SMOOTH_DERIVED_MAPPING_ACCEPTANCE_UC081.md](SMOOTH_DERIVED_MAPPING_ACCEPTANCE_UC081.md) | 1875486fe9dd7a5572f49399ab2afe66ab1815ab |
| [QUANTUM_UNIT_ACCEPTANCE_116.md](QUANTUM_UNIT_ACCEPTANCE_116.md) | 1081ab434ed49309a763d5a119c2d88554ca0742 |
| [FINITE_PARTITION_TENSOR_ACCEPTANCE_UC075.md](FINITE_PARTITION_TENSOR_ACCEPTANCE_UC075.md) | 596e596a7bfb93fd95e8f97639cbaeb11a70a0fa |
| [R3_GLOBAL_SUPPORT_DICHOTOMY_UC022.md](R3_GLOBAL_SUPPORT_DICHOTOMY_UC022.md) | a04aa1f9d420a96eb0a782f0e3914d0724972710 |
| [R3_GLOBAL_SUPPORT_ACCEPTANCE_UC024.md](R3_GLOBAL_SUPPORT_ACCEPTANCE_UC024.md) | 0f3b36f362d2636fed10c2a5492f546eb0d1f29b |
| [DIFFERENTIABLE_EXT_CLASS_ACCEPTANCE_UC084.md](DIFFERENTIABLE_EXT_CLASS_ACCEPTANCE_UC084.md) | aa27e5f3eaa76a18d66a622362858aab5982c65b |
| [AGENT_CRITICAL_REVIEW_ORIGINAL_INTEGRATION_UC086.md](AGENT_CRITICAL_REVIEW_ORIGINAL_INTEGRATION_UC086.md) | a9dfffc457adaf4706871ae4e5d985a57b61ce5e |
| [ORIGINAL_TYPED_INTEGRATION_ACCEPTANCE_UC087.md](ORIGINAL_TYPED_INTEGRATION_ACCEPTANCE_UC087.md) | a3b7913a75a076fe8d58c4ac2c155c135942b334 |
| [MIXED_PUSHDOWN_ACCEPTANCE_110.md](MIXED_PUSHDOWN_ACCEPTANCE_110.md) | d48b02a42cd1ac4064ca556579e31949e903e63d |
