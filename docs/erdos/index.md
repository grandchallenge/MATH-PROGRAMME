# The Erdős Compendium

<p class="page-deck">A problem-by-problem guide to Paul Erdős's mathematical questions: what each asks, why it matters, what is known, what GCL has checked, and what remains open.</p>

!!! info "Read an entry at the right evidence level"
    This is a **reference compendium**, not a collection of certified discoveries. All **1,221** problems in GCL's protected registry have navigable source records. Only problems with separately authored and checked explanatory material receive a full layperson breakdown. A registered issue, source-reported "proved" label or AI-generated mathematical report is **not** proof of independent verification.

## Begin with three familiar problem examples

| Problem | The central question | Public result | GCL evidence |
| --- | --- | --- | --- |
| [Erdős #1](problems/0001/) | How efficiently can integers give every subset a different sum? | The original constant-factor conjecture has been disproved | Source/proof provenance audited; independent full replay outstanding |
| [Erdős #2](problems/0002/) | Can congruence systems cover all integers using only enormous periods? | No; an upper bound exists, with a large numerical gap remaining | Registered source-audit task; no independent proof replay |
| [Erdős #3](problems/0003/) | Does a divergent reciprocal sum force progressions of every length? | Open | Active dedicated GCL mathematics campaign; four-term frontier |

## Browse every registered problem

[Open the complete numbered catalogue](catalogue/)

The catalogue is divided into sets of roughly 100 problem numbers. Each entry links to the original problem, the exact corresponding GCL GitHub issue, the protected source snapshot and—when one exists—a developed mathematical explanation. The index is generated **deterministically** from the protected registry; no worker report is automatically promoted into public mathematics.

## What each fully reviewed explainer must contain

1. **The question in plain language.** Identify the mathematical object and the quantifiers without replacing them with an attractive analogy.
2. **A small example.** Demonstrate the definition, and preferably show a failure or boundary case.
3. **What is known.** Name relevant dated theorems and distinguish a conjecture from a verified result.
4. **GCL's current state.** Point to actual protected work and evidence, not just queue activity.
5. **What remains.** Isolate the smallest missing mathematical step rather than saying only "more research is needed".
6. **Sources and claim boundaries.** Link primary evidence, explicit assumptions, unresolved reviews and formal-check status.

The first three entries illustrate the editorial standard; they are not the full published selection. Hundreds of further entries have now crossed protected editorial admission, while unadmitted manuscripts and catalogue-only references retain their distinct public labels. The [editorial production protocol](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/erdos_compendium/EDITORIAL_PROTOCOL.md) specifies how those references become evidence-checked explanations without duplicating research jobs. This is deliberate: automatically converting topic labels into 1,221 invented mathematical stories would be misleading.

## Authority and updates

The registered problem IDs, frozen statuses, triage classes, topic metadata and issue references come from [the protected GCL catalogue](https://github.com/grandchallenge/MATH-PROGRAMME/blob/main/governance/erdos_catalogue/REGISTRY.json). This catalogue's source was [teorth/erdosproblems at a pinned commit](https://github.com/teorth/erdosproblems/blob/536408716724a2402bdfa7c1d764bf83d64a8c89/data/problems.yaml).

**Frozen catalogue status is historical source metadata, not an automatically refreshed live result.** For current mathematical truth, consult the linked [Erdős Problems site](https://www.erdosproblems.com/), its original papers, and any independently reviewed GCL claim record. For execution state, use the live issues and the protected MATHSOLVE campaign ledger.

The compendium is a **documentary reference annex**, not an admitted illustrated edition under the separate [Documentary Library release manifest](../documentaries/index.md). It claims no PDF or release artifact and leaves existing Forge → Solve → Cert authority unchanged.
