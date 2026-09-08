# Volume IV bibliography and historical-attribution audit

Status: Gate-7 scholarship audit. Publication authority is not granted.

The audit verifies the source families used for historical orientation and for the deliberately
calculus-specific comparisons in Chapters 8, 9, 10, and 13. The monograph does not claim priority
or novelty from these references. Metadata below was reconciled against publisher records where
available; the Girard page range follows the current Elsevier record.

| Role in Volume IV | Verified source | Metadata / identifier | Use and boundary |
|---|---|---|---|
| CSP/process-interaction lineage | C. A. R. Hoare, “Communicating Sequential Processes,” *Communications of the ACM* 21(8), 666-677 (1978) | DOI `10.1145/359576.359585` | Historical orientation only; PROTO-0 is not claimed to be CSP. |
| CCS lineage | Robin Milner, *A Calculus of Communicating Systems*, LNCS 92 (1980) | DOI `10.1007/3-540-10235-3` | Process-calculus lineage; no semantic identity claim. |
| pi-calculus lineage | R. Milner, J. Parrow, D. Walker, “A calculus of mobile processes, I/II,” *Information and Computation* 100(1), 1-40 and 41-77 (1992) | DOIs `10.1016/0890-5401(92)90008-4`, `10.1016/0890-5401(92)90009-5` | Historical orientation; PROTO-0 omits name mobility. |
| Linear logic | Jean-Yves Girard, “Linear logic,” *Theoretical Computer Science* 50(1), 1-101 (1987) | DOI `10.1016/0304-3975(87)90045-4` | Proof-theoretic lineage. Session duality is not identified with negation in general. |
| Early dyadic sessions | Kohei Honda, “Types for dyadic interaction,” CONCUR'93, LNCS 715, 509-523 (1993) | DOI `10.1007/3-540-57208-2_35` | Historical session-type lineage. |
| Structured session programming | K. Honda, V. T. Vasconcelos, M. Kubo, “Language primitives and type discipline for structured communication-based programming,” ESOP'98, LNCS 1381, 122-138 (1998) | DOI `10.1007/BFb0053567` | Historical/calculus source; not silently substituted for PROTO-0. |
| Session subtyping | S. J. Gay, M. Hole, “Subtyping for session types in the pi calculus,” *Acta Informatica* 42(2-3), 191-225 (2005) | DOI `10.1007/s00236-005-0177-z` | Chapter 10 historical source. PROTO-S1 uses a smaller finite synchronous relation. |
| Multiparty sessions | K. Honda, N. Yoshida, M. Carbone, “Multiparty asynchronous session types,” POPL 2008, 273-284 | DOI `10.1145/1328438.1328472` | Chapter 9 lineage. General MPST projection correctness is cited, not re-proved. |
| Asynchronous sessions | S. J. Gay, V. T. Vasconcelos, “Linear type theory for asynchronous session types,” *JFP* 20(1), 19-50 (2010) | DOI `10.1017/S0956796809990268` | Chapter 8 literature comparison; PROTO-A1 remains its own bounded FIFO teaching fragment. |
| Intuitionistic propositions-as-sessions | L. Caires, F. Pfenning, “Session Types as Intuitionistic Linear Propositions,” CONCUR 2010, LNCS 6269, 222-236 | DOI `10.1007/978-3-642-15375-4_16` | Chapter 13 exact cited correspondence for that calculus only. |
| Classical propositions-as-sessions / GV-CP | Philip Wadler, “Propositions as sessions,” *JFP* 24(2-3), 384-418 (2014) | DOI `10.1017/S095679681400001X` | Chapter 13 exact cited correspondence for CP/GV; not transferred to PROTO-0. |

## Claim discipline

- Historical precedence is attributed to the source family actually used.
- The manuscript distinguishes synchronous and asynchronous calculi.
- The general MPST theorem surface is not reproduced as an internal theorem.
- The propositions-as-sessions chapter uses exact source-scoped statements and labels local diagrams as comparison/analogy.
- No novelty or priority claim is made for session types, subtyping, monitoring, asynchronous semantics, or proof/process correspondences.
