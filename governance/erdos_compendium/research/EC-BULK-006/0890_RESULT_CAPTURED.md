RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0890-S01
PROBLEM_ID: 890
DISPOSITION: STATUS_CONFLICT
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For fixed k>=1, let omega(x) count DISTINCT prime divisors of x, and omega_k(x)=number of distinct prime divisors STRICTLY >k. Maintained https://www.erdosproblems.com/890 asks (A) liminf_{n->inf} sum_{0<=j<k} omega_k(n+j)<=k for each k, and (B) limsup_{n->inf} (sum_{0<=j<k} omega(n+j))*loglog n/log n=1 for each k. The ORIGINAL 1967 printed statement instead uses unrestricted omega and a bound involving k+pi(k), which is mathematically DIFFERENT; neither should be silently substituted. A separate 1971 Erdős–Selfridge discussion assumes consecutive COMPOSITE blocks for Grimm's conjecture, but this is not established to be part of 1967 question.

## Dated status and primary evidence
P. Erdős and J. L. Selfridge, 'Some problems on the prime factors of consecutive integers', Illinois Journal of Mathematics 11 (1967), pp428–430, DOI 10.1215/ijm/1256054564, primary indexed archival source https://combinatorica.hu/~p_erdos/1967-21.pdf, printed p430 records the sum of distinct-prime contributions and Pólya theorem for k-smooth numbers. Full primary page-image inspection could not be completed this run. Maintained live #890 last edited Apr 3, 2026 and frozen teorth catalogue 536408716724a2402bdfa7c1d764bf83d64a8c89 both retain OPEN multipart status; modern tracker explicitly warns of historical mismatch omega versus omega_k. Public April 3, 2026 forum https://www.erdosproblems.com/forum/thread/890 reports a DeepMind prover-agent LEAN counterexample for one first-part formalization at k=26; participants dispute statement conventions and possible composite hypothesis, so NOT GCL-adjudicated. Public google-deepmind/formal-conjectures main FormConjectures/ErdosProblems/890.lean still includes sorry theorem bodies. Printed 1971 original second paper https://renyi.hu/~p_erdos/1971-24.pdf discusses the related but DISTINCT consecutive-composite Grimm question.

## Strongest verified interface
For any n,k, identity sum_{j<k}omega(n+j)=sum_{j<k}omega_k(n+j)+S_small(n,k), where S_small counts each occurrence of each prime <=k in the k-block. Each p<=k divides at least floor(k/p) terms in every k-block, so S_small>=sum_{p<=k}floor(k/p). At k=26 this is 36 (9 primes), exceeding the original proposed unrestricted bound k+pi(k)=35. Thus the printed full-omega upper comparison at k=26 is contradicted by a deterministic elementary counting argument, independently of any deep prime tuples theorem. It does NOT refute the modern omega_k statement. CHAD finite_889_890.py/json checks full and >k counts for n=100..5100 and k={1,2,3,4,5,8,12,26}, exact small-prime decomposition and floor lower bound, independent SPF arithmetic; for k=26 observed minimum large-prime sum 11, full sum 49 in the finite search. Finite minima do not imply limiting infima. External Lean k26 argument is distinct, not independently GCL compiled or source-equivalent.

## Proposed bounded successor task
Source-lock and compare EXACT 1967 printed omega statement, maintained 2026 omega_k statement, April 2026 public k=26 Lean theorem and any hypothesized consecutive-composite restriction. Give a formal equivalence/mismatch table and a complete proved statement for one chosen version only. Acceptance: page-image readback, protected provider literal theorem blob and Lean dependency pin, clean Lake build + actual axioms, correct ordered block, exact finite counting checks and k26 small-prime obstruction. Falsify by switching omega/omega_k, changing liminf/limsup or integer k, omitting composite assumptions, or using mere uncompiled proof code. STOP without merging reported DeepMind answer or solving part B before independent verification.

## Prerequisites and blocker
Original 1967 full page scan not visually source-locked; April 2026 Lean proof and axiom report uninspected; first-part modernization is nontrivial and second-part fixed-k limsup remains unproved by one-number classical result alone. No protected source-provider proof admitted.

## Reuse and claim boundary
Used primary 1967 indexed text, maintained 2026 corrections and public forum, separately derived deterministic small-prime floor bound, exact CHAD finite test. No GCL certification of k26 Lean result, novel solution of part B, protected review/merge, or public site admission.
