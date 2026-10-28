"""Exact Wick sign control tied to the smooth-generator witness in audit 082.

For a normalized nonzero compact smooth real f, write
  x = a(f)b(f), y = d(x), and 1 = the arity-zero unit.
Then d(x)=y, B(y)=1, B(x)=0, so [B,d](x)=1.
The basis below is (1,y,x), of cohomological degrees (0,0,-1).
This quotient of the actual generator calculation detects the source sign.
It does not prove any infinite normal-topology or completed Weiss assertion.
"""

from fractions import Fraction as F


def zero():
    return [[F(0) for _ in range(3)] for _ in range(3)]


def eye():
    a = zero()
    for i in range(3):
        a[i][i] = F(1)
    return a


def add(a, b):
    return [[a[i][j] + b[i][j] for j in range(3)] for i in range(3)]


def scale(a, t):
    return [[t * a[i][j] for j in range(3)] for i in range(3)]


def mul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(3)), F(0))
             for j in range(3)] for i in range(3)]


def sub(a, b):
    return add(a, scale(b, F(-1)))


d = zero()
d[1][2] = F(1)
B = zero()
B[0][1] = F(1)
Delta = sub(mul(B, d), mul(d, B))  # |B|=0: ordinary commutator.
assert Delta[0][2] == 1
assert mul(B, B) == zero()
assert mul(B, Delta) == mul(Delta, B) == zero()
assert mul(d, d) == zero()


def W(t):
    return add(eye(), scale(B, t))  # Exact exponential because B^2=0.


def positive_d(t):
    return add(d, scale(Delta, t))


scales = [F(-2), F(-1, 2), F(0), F(1, 3), F(1), F(2)]
for t in scales:
    assert mul(W(t), W(-t)) == eye()
    assert mul(mul(W(t), d), W(-t)) == positive_d(t)
    inverse_conjugation = mul(mul(W(-t), d), W(t))
    assert inverse_conjugation == sub(d, scale(Delta, t))
    if t:
        assert inverse_conjugation != positive_d(t)

for s in scales:
    for t in scales:
        corrected_transport = mul(W(t), W(-s))
        assert mul(corrected_transport, positive_d(s)) == mul(
            positive_d(t), corrected_transport)
        source_transport = mul(W(-t), W(s))
        if t != s:
            assert mul(source_transport, positive_d(s)) != mul(
                positive_d(t), source_transport)

# For W(t)=exp(tB), positive-family connection has gauge term -B.
# Compatibility is d'(t)+[A(t),d(t)]=0. The reverse gauge term fails.
for t in scales:
    corrected_gauge = scale(B, F(-1))
    corrected_commutator = sub(mul(corrected_gauge, positive_d(t)),
                               mul(positive_d(t), corrected_gauge))
    assert add(Delta, corrected_commutator) == zero()
    reverse_commutator = sub(mul(B, positive_d(t)), mul(positive_d(t), B))
    assert add(Delta, reverse_commutator)[0][2] == 2

print("PASS: actual-generator commutator [B,d]=Delta is nonzero")
print("PASS: positive and inverse Wick conjugations have opposite BV signs")
print("PASS: corrected transport intertwines all 36 positive-model pairs")
print("PASS: reversed transport fails on every pair of distinct scales")
print("PASS: positive-family connection requires the opposite gauge sign")
print("LIMIT: finite quotient checks the sign; audit 082 supplies the smooth-kernel realization")
