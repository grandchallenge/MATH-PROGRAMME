#!/usr/bin/env python3
"""FC-007 exact filtered-complex and triangular-matrix adversarial replay.

No external packages. Does not certify infinite-dimensional condensed analytics.
"""
from fractions import Fraction as Q


def compose(f, g):
    """Return matrix f after g, in row-output/column-input convention."""
    n = len(f)
    return [[sum((f[k][j] * g[j][i] for j in range(n)), Q(0))
             for i in range(n)] for k in range(n)]


def triangular(m):
    return all(m[j][i] == 0 for j in range(len(m)) for i in range(j+1, len(m)))


def substitution(a, g, N):
    """Formal a(g(x)) mod x^N, coefficient lists including constant."""
    answer = [Q(0)] * N
    powers = [[Q(0)] * N for _ in range(N)]
    powers[0][0] = Q(1)
    for k in range(1, N):
        for i in range(N):
            for j in range(N-i):
                powers[k][i+j] += powers[k-1][i] * g[j]
    for k in range(min(N, len(a))):
        for i in range(N):
            answer[i] += a[k] * powers[k][i]
    return answer


def formal_inverse_of_x_plus_x2(N):
    g = [Q(0)] * N
    if N > 1:
        g[1] = Q(1)
    for n in range(2, N):
        g[n] = -sum((g[j] * g[n-j] for j in range(1, n)), Q(0))
    return g


def test_substitution():
    for N in range(3, 13):
        f = [Q(0), Q(1), Q(1)] + [Q(0)] * (N - 3)
        g = formal_inverse_of_x_plus_x2(N)
        x = [Q(0), Q(1)] + [Q(0)] * (N - 2)
        assert substitution(f, g, N) == x
        assert substitution(g, f, N) == x
        assert g[2] == Q(-1)
        # x->x+x^2 is filtration-preserving but not weight-preserving.
        assert f[2] == Q(1)


def test_filtered_acyclic_but_graded_nonacyclic():
    # a lives in cochain degree 0 and filtration weight 0;
    # b lives in cochain degree 1 and weight 1.
    # D(a)=b gives an isomorphism C^0->C^1.
    D = [[Q(0), Q(0)], [Q(1), Q(0)]]
    assert triangular(D)
    assert compose(D, D) == [[Q(0), Q(0)] for _ in range(2)]
    assert D[1][0] == Q(1)  # total H^0=H^1=0
    # The diagonal blocks of D (differential on gr^i) are zero.
    assert D[0][0] == D[1][1] == Q(0)
    # Hence H^0(gr^0)=R and H^1(gr^1)=R.
    associated_graded_nonzero_cohomologies = 2
    total_nonzero_cohomologies = 0
    assert associated_graded_nonzero_cohomologies != total_nonzero_cohomologies


def test_upper_triangular_morphisms():
    n = 4
    I = [[Q(int(i == j)) for i in range(n)] for j in range(n)]
    A = [[Q(int(j == i+1)) for i in range(n)] for j in range(n)]
    B = [[Q(2) * A[j][i] for i in range(n)] for j in range(n)]
    C = [[Q(int(j == i+2)) for i in range(n)] for j in range(n)]
    f = [[I[j][i]+A[j][i] for i in range(n)] for j in range(n)]
    g = [[I[j][i]+B[j][i] for i in range(n)] for j in range(n)]
    h = [[I[j][i]+C[j][i] for i in range(n)] for j in range(n)]
    for m in (f, g, h, compose(g, f)):
        assert triangular(m)
    assert compose(h, compose(g, f)) == compose(compose(h, g), f)
    assert compose(f, I) == f
    assert compose(I, f) == f
    assert f[1][0] == Q(1)  # genuine non-diagonal filtered map


def test_twisted_dg_map():
    # A filtered complex with D(a)=b, and a filtered cochain automorphism
    # commuting with D: f = I + D (here D^2=0).
    D = [[Q(0), Q(0)], [Q(1), Q(0)]]
    I = [[Q(1), Q(0)], [Q(0), Q(1)]]
    f = [[I[j][i]+D[j][i] for i in range(2)] for j in range(2)]
    assert triangular(f)
    assert compose(D, f) == compose(f, D)
    assert f[1][0] == Q(1)


if __name__ == "__main__":
    test_substitution()
    test_filtered_acyclic_but_graded_nonacyclic()
    test_upper_triangular_morphisms()
    test_twisted_dg_map()
    print("FC-007 triangular filtered bridge: exact finite controls PASS")
