# EC-BULK-007 — #1196 primitive-set reciprocal logarithm 2026 theorem

**Source-proved externally, independent theorem/Lean certification PENDING.**

The catalogue https://www.erdosproblems.com/1196 reports a 2026 GPT-5.4 Pro argument written by Alexeev–Barreto–Li–Lichtman–Price–Shah–Tang–Tao. It claims sum_{a in primitive A,a>x} 1/(a log a) <= 1 + O(1/log x) uniformly over primitive sets A, strengthening Lichtman's previously reported constant 1.399 bound. Read the 2026 original with exact cutoff and constants, and source-check asymptotic near-one examples from GLW24; a formalized statement alone is not a kernel proof.

Phase23 uses the primitive finite set {2,3,5,7,11}, whose reciprocal-log sum is 1.26035. This set has elements below the large cutoff and is NOT a counterexample.

**Review pending.** Authenticated return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2467#issuecomment-6187245548
