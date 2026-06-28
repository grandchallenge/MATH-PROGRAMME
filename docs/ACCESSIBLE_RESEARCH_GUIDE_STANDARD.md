# Accessible Research Guide Standard

<p class="page-deck">Accessible research is not easier mathematics. It is mathematics with its entrance, rails, examples, and proof boundary made visible.</p>

## Source posture

This standard is inspired by the project-based undergraduate-research pattern: prerequisites, accessible exposition, exercises, challenge problems, open problems, and further reading arranged so a serious reader can begin research after working through the guide.

The Grand Challenge version is broader. It is for undergraduate readers, independent researchers, collaborators, reviewers, and agentic assistants. It does not lower the claim boundary. It lowers the cost of finding the first honest move.

## Binding rule

Every new domain, theorem-spine campaign, serious Work Package, fixture family, or cross-pillar research lane should either:

1. include an `ACCESSIBLE_RESEARCH_GUIDE.md`; or
2. explicitly defer the guide in the proof-debt register with a reason and a named completion condition.

A result may be technically correct and still fail programme handoff if no capable reader can determine how to enter it.

## The guide contract

An Accessible Research Guide must contain the following sections. They may be brief, but none may silently disappear.

### 1. Status and intended reader

State the current claim status, support route, and target reader.

```text
Status: exploratory | audited | computed | locally proved | certified | superseded
Audience: undergraduate | graduate | domain expert | agentic assistant | mixed
Expected time to first example:
Expected time to first runnable fixture:
```

### 2. Plain object

Name the mathematical object before the method.

The reader should be able to answer:

- What is the object?
- What data specifies one instance?
- What counts as a small example?
- What does it mean for two examples to be the same or different?

### 3. Prerequisites and refreshers

List prerequisites by concept, not by prestige.

Use three levels:

| Level | Meaning |
| --- | --- |
| Required | Needed to follow the first worked example. |
| Helpful | Makes the surrounding theory easier. |
| Deferred | Needed later, but not needed for the first fixture. |

When possible, include a one-paragraph refresher or point to a stable companion note.

### 4. Core bridge

Give the smallest honest bridge from familiar mathematics to the programme object.

Good bridges usually have this shape:

```text
familiar object -> changed rule -> new object -> first obstruction -> first fixture
```

The bridge is not allowed to smuggle in the theorem.

### 5. First examples by hand

Provide at least two examples:

1. a friendly example where the definitions work cleanly;
2. an edge example where the obstruction becomes visible.

Examples should be small enough that a reader can reproduce them without trusting code.

### 6. First computation or fixture

Provide a bounded computation, exact enumeration, checker, notebook, or fixture script.

Record:

- input;
- operation;
- output artifact;
- reproducibility command;
- support-route class;
- known limitation.

### 7. First theorem or local proposition

State one modest proposition that the guide actually explains.

The proposition may be elementary, local, or already known. Its purpose is to show the reader what proof feels like in this terrain.

### 8. Challenge ladder

Provide a ladder rather than a list of unrelated exercises.

| Stage | Duty |
| --- | --- |
| Exercise | Confirms the reader can use the definitions. |
| Exploration | Produces examples, data, or patterns. |
| Fixture | Produces a replayable artifact. |
| Lemma candidate | Names a restricted claim worth attacking. |
| Open direction | Points beyond the guide without overstating novelty. |

Every challenge should state a completion test.

### 9. Certification path

Name what could be checked independently.

Examples:

- Lean statement;
- exact Python/Sage replay;
- JSON certificate;
- interval-arithmetic witness;
- SAT/SMT certificate;
- human-audited lemma with formalization blockers named.

If no certification path is known, say so and record that as proof debt.

### 10. Continuation graph

Show how the project can move laterally.

Use this compact form:

```text
first fixture
  -> restricted lemma
  -> neighbouring example family
  -> stronger conjecture
  -> certification target
  -> adjacent domain
```

A continuation graph is successful when it gives the next three useful projects without requiring a new act of taste.

### 11. Bibliography and source audit

Separate learning sources from claim support.

| Source | Used for | Imported claim? | Audit state |
| --- | --- | --- | --- |
| | exposition | no | provenance only |
| | theorem dependency | yes | reconstructed / pending |

A source may inspire the guide. It does not certify the guide.

## Pillar mapping

| Pillar | Accessible-guide duty |
| --- | --- |
| MATHFORGE | Make the source object, examples, and route suggestions inspectable. |
| MATHSOLVE | Turn the guide into a theorem-spine entrance and work-package ladder. |
| MATHCERT | State the first checkable boundary and the smallest certificate target. |

## Lateral movement rule

A guide should not end with atmosphere. It should end with neighbouring doors.

A lateral move is valid when it preserves at least one of:

- the object class;
- the obstruction;
- the support route;
- the fixture type;
- the certification method;
- the foundational profile.

A lateral move is invalid when it changes all of these at once and leaves the reader in a new field with no bridge.

## Review checklist

Before merging a guide, check:

- [ ] The target reader is named.
- [ ] The object appears before machinery.
- [ ] Prerequisites are honest and not inflated.
- [ ] At least one example can be done by hand.
- [ ] At least one fixture or computation has a completion test.
- [ ] A modest theorem or local proposition is stated.
- [ ] The challenge ladder has stages, not a pile of tasks.
- [ ] The certification path is named or explicitly marked as unknown.
- [ ] The continuation graph gives the next useful moves.
- [ ] Bibliography is separated from claim support.

## Compact

Accessible research means:

> the entrance is visible, the first example is reproducible, the first obstruction is honest, the first claim is bounded, the first checker is named, and the next project is not hidden in the mentor's head.
