# Bibliography Plan — Volume IV: PROTOCOL

## Purpose

This plan identifies the literature families required to support formal imports, historical claims, and scope boundaries. It is not yet the final bibliography audit. Exact editions, dates, page/section loci, and theorem hypotheses must be verified before RC closure.

## Primary and foundational source families

### Process calculi and communication models

- C. A. R. Hoare — CSP / communicating sequential processes sources used for the historical account of communication-centered computation.
- Robin Milner — CCS and π-calculus sources used for process syntax, interaction, and behavioral reasoning history.
- Related early process-calculus sources only where a concrete historical or formal claim requires them.

### Linear logic and resource discipline

- Jean-Yves Girard — linear logic foundational source for resource-sensitive proof structure.
- Later process/linear-logic correspondences only when Chapter 13 states an exact theorem/translation.

### Binary session types

- Kohei Honda and collaborators — foundational session-type papers introducing structured typed communication.
- Simon Gay, Malcolm Hole, and later binary-session work for subtyping, duality, and type-system refinements where imported.
- Exact fidelity/progress sources matched to the calculus actually cited.

### Multiparty session types

- Kohei Honda, Nobuko Yoshida, Marco Carbone and related foundational MPST work.
- Later projectability/global-progress results only with exact hypotheses preserved.

### Asynchronous semantics and communicating automata

- Foundational asynchronous session-type sources used for queue semantics, fidelity, and subtyping boundaries.
- Communicating finite-state-machine literature where finite realizability/compliance comparisons are made.

### Runtime monitoring

- Session-monitor/runtime-verification literature supporting finite monitor construction or soundness claims.
- Every monitor theorem must specify the observation model and whether completeness is relative to observable events only.

### Propositions as sessions / proofs as processes

- Primary papers establishing the exact linear-logic/session/process correspondences used in Chapter 13.
- The manuscript will not retroactively attribute these later correspondences to the earliest session-type work.

## Modern expository references

- Standard texts on process calculi and concurrency.
- Programming-languages/type-systems texts with linear/session typing chapters.
- Survey literature on binary and multiparty session types.
- Distributed-systems texts used specifically to delimit failures, scheduling, fault tolerance, consistency, timing, and security claims outside the selected session calculi.

## Historical/date claims requiring verification

1. Exact publication chronology and bibliographic identities for CSP, CCS, and π-calculus references used in prose.
2. Exact bibliographic identity and formal calculus of the earliest session-type source cited.
3. Whether a given result is synchronous or asynchronous and whether channels are linear, shared, or delegated.
4. Exact hypotheses behind any imported fidelity, progress, deadlock-freedom, lock-freedom, or subtyping result.
5. Exact scope and projectability conditions behind any multiparty projection theorem.
6. Exact source for propositions-as-sessions/processes-as-proofs statements and which linear logic/process calculus is involved.
7. Exact observation model behind monitoring results.

## Attribution discipline

- Do not tell a single-origin story for concurrency/process calculi.
- Distinguish session typing from later propositions-as-sessions correspondences.
- Distinguish binary from multiparty and synchronous from asynchronous results.
- Distinguish historical influence from formal implication.
- No novelty or priority claim is authorized by this volume without a separate literature audit.

## Final RC audit requirements

The later `BIBLIOGRAPHY_AUDIT.md` must record every historical name/date claim and every imported theorem with source, exact calculus, verified metadata, and whether the source is primary or expository.
