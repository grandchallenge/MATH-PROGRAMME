# EC-BULK-004 — Erdős #528–529 connective constant and displacement audit

Observed 2026-10-16 UTC. Authenticated editorial operator fyremael; **same-operator** source and exact-fixture QA, not independent mathematical acceptance, specialist signoff or protected admission.

## #528 — OPEN exact connective constant; existence known

Original Erdős, *Some unsolved problems* (1961), printed p254 V.5, https://users.renyi.hu/~p_erdos/1961-22.pdf#page=34 directly read. Ordered origin-anchored n-step nearest-neighbour self-avoiding walks gamma in hypercubic Z^k, all visited vertices distinct, c_n(k) total. Determine mu_k=lim c_n(k)^(1/n), existence already observed. Do not call existence OPEN, or apply exact honeycomb constant to Z². k=1 c_n=2 (n≥1), mu_1=1; open exact k≥2. Historical Hammersley/Morton, *Poor Man's Monte Carlo*, JRSS B 16(1) (1954) 23–38, DOI 10.1111/j.2517-6161.1954.tb00145.x, publisher primary abstract/bibliography checked, full proof not reread. Kesten, *On the number of self-avoiding walks*, J Math Phys 4 (1963) 960–969, high-k expansion mu_k=2k−1−1/(2k)+O(k^-2), reported through maintained erdosproblems.com/528; full original Kesten analysis not independently retrieved. Jacobsen, Scullard, Guttmann, *On the growth constant for square-lattice self-avoiding walks*, arXiv:1607.02984 original abstract directly read: mu_2 numerical 2.63815853032790(3), not proved exact expression. Maintained catalogue OPEN and pinned source OPEN, no FC-GDM-85F86371 528.lean.

Elementary proof of existence: split walk m+n at m, translate suffix, inject SAW_(m+n) into SAW_m × SAW_n, c_(m+n)≤c_m c_n. Fekete log implies mu_k=inf c_n^(1/n). k^n positive-coordinate monotone walks lower, 2k(2k−1)^(n−1) non-backtracking upper, hence k≤mu_k≤2k−1. Finite nth roots give upper bounds not exact values; arbitrary c_n/c_(n−1) is NOT automatically certified monotone or a bound. tests/test_erdos_compendium_0528_connective_constant.py independent DFS self-avoiding enumeration dimensions 1,2,3 through n≤8, exact Z² 1,4,12,36,100,284,780,2172,5916, independent brute-force short step sequences, finite submultiplicativity. Four focused tests PASS. These are finite checks, not determination of mu_2.

Authenticated source return https://github.com/grandchallenge/MATH-PROGRAMME/issues/1799#issuecomment-6227152077 BOUNDED_TASK_DESIGNED; scientific exact-value obligation open.

## #529 — OPEN low-dimensional endpoint exponent; high-k diffusive theorem

Original same Erdős 1961 p254 V.5, distinct problem: uniformly chosen ordered n-step self-avoiding gamma from origin; d_k(n)=E||gamma_n||_2, not E gamma_n (vector 0 by symmetry), and not sqrt(E||gamma_n||²). Questions d_2(n)/sqrt n→∞ and d_k=O(sqrt n) for all k≥3. In k=5 and higher Hara–Slade 1992 lace expansion proves Brownian scaling and E||gamma_n||²~D_k n, giving original upper via Jensen and positive scaling via Brownian limit and uniform integrability. Hara/Slade, *Self-avoiding walk in five or more dimensions I. The critical behaviour*, Commun Math Phys 147 (1992) 101–136, DOI 10.1007/BF02099530, original research abstract reviewed, not full proof.

Duminil-Copin and Hammond, *Self-avoiding walk is sub-ballistic*, Commun Math Phys 324(2) (2013), 401–423, DOI 10.1007/s00220-013-1811-1, full 27-page original arXiv:1205.0401 PDF obtained CHAD /tmp/ec004-subball.pdf; primary Theorem1.1 directly read: for k≥2 any v>0, P_SAW_n(max_j ||gamma_j||≥vn)≤e^(-eta n) with eta>0. With ||gamma_n||≤n, d_k(n)/n≤v+e^(-eta n) -> limit0 as v↓0, so d_k=o(n), NOT d_2/sqrt n→∞ or three/four-dimensional diffusive upper. Maintained erdosproblems.com/529 OPEN; conjectures d_2~D n^(3/4), d_3~n^nu (~0.59), d_4~D sqrt n(log n)^(1/8), making original all k≥3 O(sqrt n) prediction expected FALSE in k3/4 but without strict-lattice proof. 1993 Madras/Slade monograph Chapter1 §1.4 source citation; no FC-GDM-85F86371 529.lean.

For n=2,k=2, exactly twelve SAWs, four straight distance2 and eight turning distance sqrt2, so d_2(2)=(2+2sqrt2)/3; second moment 8/3; Jensen strict. For k=1 d_1(n)=n. Exact integer endpoint squared-distance histograms and reflected coordinate mean zero; parity r=||gamma_n||²≡n mod2. tests/test_erdos_compendium_0529_saw_endpoint.py uses independent DFS, SymPy exact radicals and independent brute-force word enumeration on short n. Four focused tests PASS. No asymptotic scaling inference from finite enumeration.

Authenticated source return https://github.com/grandchallenge/MATH-PROGRAMME/issues/1800#issuecomment-6227152321 BOUNDED_TASK_DESIGNED; low-dimensional scientific boundary open.

## Admission boundary

Both articles six substantive sections, UNACCEPTED_DRAFT. Full suite, strict MkDocs, Chromium and custody SHA256 receipts will be written before editorial commit. No non-author INTELLECT review represented, no protected canonical statement/source change, no selected Solve campaign, no GCL Lean kernel certification, no public deployed rendering.
