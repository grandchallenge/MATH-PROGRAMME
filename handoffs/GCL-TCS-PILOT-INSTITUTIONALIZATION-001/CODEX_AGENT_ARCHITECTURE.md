# Codex agent architecture map

This file is the GitHub-native illustration for execution agents. Protected doctrine and live repository state control any conflict.

## Three non-collapsible integrity layers

```mermaid
flowchart LR
  subgraph EXEC[GHOS — execution / control integrity]
    W[Workflow bytes] --> R[Routing classification]
    R --> C[Admitted controller]
    C --> P[Protection + routing enforcement]
    P --> E[Material execution evidence]
  end

  subgraph MATH[MATH-CORE — mathematical coordination]
    I[INTELLECT control/allocation] --> MC[MATH-CORE typed reasoning state]
    MC --> F[MATHFORGE]
    MC --> S[MATHSOLVE]
    MC --> Cert[MATHCERT]
  end

  subgraph ACCEPT[Trusted acceptance boundary]
    PR[Proof / replay checking] --> IA[Independent assurance]
    IA --> CL[Canonical Claim Ledger]
    CL --> PD[Policy / downstream authority]
  end

  subgraph COMMS[GCL-TCS / POS — communication and authority-boundary integrity]
    AI[Artifact identity] --> CS[Claims + scope + assumptions]
    CS --> EV[Evidence + limitations]
    EV --> RV[Applicable review state]
    RV --> AU[Authorized uses]
  end

  Cert --> PR
  F --> PR
  S --> PR
  MC -. working state; not canonical .-> PR
  E -. execution evidence .-> COMMS
  MATH -. mathematical provenance/state .-> COMMS
  ACCEPT -. accepted authority/status .-> COMMS
```

Do not collapse these layers:

- GHOS answers whether execution routing/controller/protection state is materially governed.
- MATH-CORE answers what typed mathematical reasoning/obligation/conflict/evidence coordination state exists.
- GCL-TCS/POS answers whether artifacts and consequential claims carry inspectable identity, scope, evidence, limitations, provenance, review state and permitted use.
- Trusted acceptance answers what has actually received the applicable proof/replay, assurance, certification, canonical recording and policy disposition.

## MATH-CORE placement

```mermaid
flowchart LR
  INT[INTELLECT
control / allocation] --> CORE[MATH-CORE
reasoning-state coordination]
  CORE --> FORGE[MATHFORGE
discovery / source foundry]
  CORE --> SOLVE[MATHSOLVE
disciplined reasoning]
  CORE --> CERT[MATHCERT
independent assurance]
  FORGE --> TA[Trusted acceptance boundary]
  SOLVE --> TA
  CERT --> TA
  TA --> CAN[Canonical recording / downstream authority]

  CORE -. not canonical truth .- CAN
```

MATH-CORE is not a fourth pillar, proof kernel, MATHCERT, canonical Claim Ledger, canonical truth, or Human Steward authority.

## Successor-operation workstreams

```mermaid
flowchart TD
  P[Live preflight + readiness matrix] --> A[A. Detect-only GHOS material sentinel]
  P --> B[B. Shallow evidence discovery]
  P --> C[C. Six-class GCL-TCS pilot evidence]
  A --> D[D. Measurement + institutional learning]
  B --> D
  C --> D
  D --> S[Successor evaluation:
retain / simplify / automate / narrow / strengthen / revise / continue pilot]
  S -. separate future governed operation if warranted .-> V1[Possible GCL-TCS/POS promotion candidate]
```

`V1` is not an expected automatic outcome.

## Streamlined routine path

```mermaid
flowchart LR
  M[Classify material closure] --> K[Run affected checks]
  K --> D[Delegated disposition]
  D --> PM[Protected merge]
  PM --> RB[Protected readback]
```

Do not insert Human Steward or Referee boxes into this routine path unless a controlling instrument materially reserves that exact transition.

## Escalation branch

Escalate only for the real boundary, for example:

```text
mathematical/certification authority
constitutional or policy expansion
security-sensitive weakening/controller transition
C04-C07 MATH-CORE capability transition
reserved external publication/claim authority
actual standard-promotion review
unrecoverable authentication/evidence boundary
```

A new commit, another session, ordinary CI pending, a repairable implementation failure, or unrelated `main` movement is not an approval boundary.

## Sentinel contract

```mermaid
flowchart LR
  LIVE[Live material identities] --> CMP[Compare against governed dependencies]
  CMP --> U[UNCHANGED]
  CMP --> L[LOCAL REVALIDATION]
  CMP --> N[NEW MEMBER / SUCCESSOR ADMISSION]
  CMP --> T[CONTROLLER / PROTECTION / SHARED-GATE TRANSITION]
  CMP --> X[UNKNOWN FAIL CLOSED]
```

The sentinel detects and routes. It does not self-authorize repairs or authority changes.

## Review / authority decision test

```mermaid
flowchart TD
  X[Proposed next transition] --> Q{Does a protected governing instrument
materially reserve this transition?}
  Q -- No --> R[Proceed under standing delegated authority
with affected material checks]
  Q -- Yes --> B[Name exact boundary and exact reserved actor]
  B --> A[Obtain only the required specialist / Referee / Human Steward disposition]
```

Do not infer a reserved gate from importance, template shape, exact-head freshness, or historical ceremony.

## Agent quick reference

1. Re-fetch protected state before trusting any handoff value.
2. Read `STATE.json` as bootstrap only, not authority or checkpoint.
3. Preserve the historical GHOS terminal result; use successor transactions for later state.
4. Build/read the live GCL-TCS v1.0 readiness matrix before selecting pilots.
5. Apply `MATH_CORE_INTEGRITY.md` to mathematical work.
6. Use one execution lead; spawn specialists only for material value.
7. Cite the protected rule before claiming a reserved approval is required.
8. Prefer less ceremony when material protection is equal.
