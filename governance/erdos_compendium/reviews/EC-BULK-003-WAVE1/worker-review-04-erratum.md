# EC-BULK-003 wave 1 review 04 arithmetic erratum

Problem #264 review contains an invalid exact-arithmetic assertion: the sum through `k=999` is finite and is strictly less than `1/3`, rather than equal to it. The correct identity is

```python
from fractions import Fraction
partial = 4 * sum((Fraction(1, 4**k) for k in range(2, 1000)), Fraction())
assert partial == Fraction(1, 3) * (1 - Fraction(1, 4**998))
assert Fraction(1, 3) - partial == Fraction(1, 3 * 4**998)
assert partial < Fraction(1, 3)
```

The separate finite check through `k=7`, `1365/4096`, is correct. The manuscript's distinction between the finite partial sum and its infinite limit is correct. This erratum corrects the review evidence, not the underlying mathematics, source-return disposition, or certification status. Preserve the original worker review unchanged for provenance. Re-review the corrected evidence before editorial admission.
