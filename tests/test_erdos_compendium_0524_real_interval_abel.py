"""Exact finite Abel summation and two-walk sandwich for #524.

No finite sign enumeration determines the Letwin--Sawhney almost-sure envelope.
"""
from fractions import Fraction as F
from itertools import product

SAMPLE = (F(-1),F(-3,4),F(-1,2),F(-1,4),F(0),F(1,4),F(1,2),F(3,4),F(1))


def prefixes(signs):
    out, acc = [], 0
    for a in signs:
        acc += a
        out.append(acc)
    return out


def evaluation(signs, x):
    return sum((a*x**k for k,a in enumerate(signs)),F(0))


def abel(signs, x):
    assert 0 <= x <= 1
    pre=prefixes(signs)
    return (1-x)*sum((pre[j]*x**j for j in range(len(signs)-1)),F(0)) + pre[-1]*x**(len(signs)-1)


def test_524_abel_identity_all_short_sign_patterns():
    for n in range(0,10):
        for signs in product((-1,1),repeat=n+1):
            for x in SAMPLE:
                if x>=0:
                    assert evaluation(signs,x)==abel(signs,x)
                else:
                    alternating=tuple(a*(-1)**k for k,a in enumerate(signs))
                    assert evaluation(signs,x)==abel(alternating,-x)


def test_524_two_random_walk_sandwich_rational_points():
    for n in range(1,10):
        for signs in product((-1,1),repeat=n+1):
            S=prefixes(signs)
            T=prefixes(tuple(a*(-1)**k for k,a in enumerate(signs)))
            bound=max(*(abs(v) for v in S+T))
            endpoints=max(abs(S[-1]),abs(T[-1]))
            samples=[abs(evaluation(signs,x)) for x in SAMPLE]
            assert endpoints <= max(samples) <= bound


def test_524_endpoints_are_not_full_interval_maximum():
    signs=(1,1,-1)
    assert max(abs(evaluation(signs,F(-1))),abs(evaluation(signs,F(1))))==1
    assert evaluation(signs,F(1,2))==F(5,4)>1


def test_524_abel_convex_weights_sum_to_one_exactly():
    for n in range(1,20):
        for x in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
            weights=[(1-x)*x**j for j in range(n)]+[x**n]
            assert sum(weights,F(0))==1
            assert all(w>=0 for w in weights)
