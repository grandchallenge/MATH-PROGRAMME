# EC-BULK-007 — #1181 logarithmic cutoff normalization

**SOURCE FIDELITY PENDING. No general prime theorem claimed.**

- Maintained original: https://www.erdosproblems.com/1181
- Authenticated return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2452#issuecomment-6185793047
- Original reference: Erdős (1979), Er79d, p.78; related source #457.

The printed $q(n,\log n)$ substitutes the **noninteger** real $\log n$ for $k$ in the product $\prod_{1\le i\le k}(n+i)$. The product only depends on integers $i$ with $i\le k$, naturally yielding $\lfloor\log n\rfloor$, but the exact original normalization and logarithm base must be sourced. This can matter at finite thresholds and in the numerical statement, though not necessarily in leading asymptotics. Do not silently change the frozen issue body.

The exact finite fixture evaluates $q(10,2)=5$, $q(100,4)=5$, $q(1000,7)=23$, $q(10000,10)=17$, all with **explicitly integral** $k$. No uniform constant $c>0$ in the asymptotic inequality is certified.

Primary-source duty: obtain Er79d p.78 and Tao's #457 remarks; verify the primorial upper bound and whether claimed worst-case lower constructions match the same normalization. **Review remains pending.**
