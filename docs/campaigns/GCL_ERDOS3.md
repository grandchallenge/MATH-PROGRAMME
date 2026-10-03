# GCL-ERDOS3

GCL-ERDOS3 has advanced from the dyadic sufficiency bridge to an exact quantitative reformulation.

Protected Solve state: `a8abc98d7bd7017202fcb40ee3d5c04ad20769d6`.

## Exact reformulation

For each fixed (kge3),

[
	ext{every reciprocally divergent set contains a non-trivial }k	ext{-AP}
]

is equivalent to

[
sum_{nge1}rac{r_k(2^n)}{2^n}<infty.
]

The reverse implication is proved natively in E3-B02 by placing extremal (k)-AP-free sets in scale-separated blocks
([4^d,	frac32 4^d)). Those blocks admit no mixed three-term arithmetic progression, so their union is globally (k)-AP-free, while the reciprocal contribution is a constant fraction of the odd-index extremal series.

This equivalence is also explicitly stated by Green–Tao (2017), citing Tao–Vu, Exercise 10.0.6.

## Active frontier

The minimal unresolved case is now:

[
oxed{	ext{E3-Q4-SERIES: }sum_{nge1}r_4(2^n)/2^n<infty.}
]

Current pointwise theory gives (r_4(N)ll N(log N)^{-c}) for some absolute (c>0), which alone does not cross the required summability threshold.

## Live tranche-02 lanes

- Q01 — quantitative four-term extremal-series attack: issue #772.
- X01 — cross-scale / renormalization inequality search: issue #773.
- A02 — adversarial attack on false cross-scale upgrades: issue #774.
- S03 — primary-source audit for sequence-level (r_4) information: issue #775.
- V02 — one independent verification of the B02 reverse construction: issue #776.

Q01 and X01 are the primary mathematical lanes. A02 is falsification pressure; S03 supplies exact interfaces. V02 is the only verification lane and closes after one valid replay.

No result here proves Erdős Problem 3.
