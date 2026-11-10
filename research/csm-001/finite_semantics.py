"""CSM-001 finite weighted-kernel specimen. Exact finite algebra; not theorem certification.

Matrix convention: a morphism X -> Y has rows indexed by Y, columns by X.
No floating-point evaluation, normalization, or stochastic-kernel assumption.
"""
from fractions import Fraction
from itertools import product


def matrix(rows):
    """Return a nonnegative rectangular matrix with exact rational entries."""
    out = tuple(tuple(Fraction(v) for v in row) for row in rows)
    if not out or not out[0] or any(len(row) != len(out[0]) for row in out):
        raise ValueError("nonempty rectangular matrix required")
    if any(v < 0 for row in out for v in row):
        raise ValueError("weights must be nonnegative")
    return out


def identity(n):
    if n < 1:
        raise ValueError("dimension must be positive")
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def compose(g, f):
    """g ∘ f: sum over the intermediate finite state space."""
    if len(g[0]) != len(f):
        raise ValueError("source-target dimensions do not match")
    return matrix([
        [sum(g[z][y] * f[y][x] for y in range(len(f)))
         for x in range(len(f[0]))]
        for z in range(len(g))
    ])


def tensor(a, b):
    """Kronecker product, with (y1,y2) row and (x1,x2) column order."""
    return matrix([
        [a[y1][x1] * b[y2][x2]
         for x1 in range(len(a[0])) for x2 in range(len(b[0]))]
        for y1 in range(len(a)) for y2 in range(len(b))
    ])


def trace(a):
    if len(a) != len(a[0]):
        raise ValueError("trace requires a square matrix")
    return sum((a[i][i] for i in range(len(a))), Fraction(0))


def power(a, n):
    if n < 0 or len(a) != len(a[0]):
        raise ValueError("nonnegative power of square matrix required")
    out = identity(len(a))
    for _ in range(n):
        out = compose(a, out)
    return out


def ising_transfer(equal=2, unequal=1):
    """Two-spin nearest-neighbour bond weights (not normalized)."""
    return matrix([[equal, unequal], [unequal, equal]])


def ising_partition_transfer(n, equal=2, unequal=1):
    if n < 1:
        raise ValueError("number of periodic links must be positive")
    return trace(power(ising_transfer(equal, unequal), n))


def ising_partition_enumeration(n, equal=2, unequal=1):
    """Independent enumeration of all 2**n configurations."""
    if n < 1:
        raise ValueError("number of periodic links must be positive")
    a, b = Fraction(equal), Fraction(unequal)
    if a < 0 or b < 0:
        raise ValueError("weights must be nonnegative")
    total = Fraction(0)
    for spins in product((0, 1), repeat=n):
        weight = Fraction(1)
        for i in range(n):
            weight *= a if spins[i] == spins[(i + 1) % n] else b
        total += weight
    return total


def pushforward(weights, coarse_map):
    """Finite deterministic coarse-graining with exact total-weight retention.

    coarse_map must assign a macrostate to every microstate key.
    """
    if set(weights) != set(coarse_map):
        raise ValueError("coarse map must cover exactly the weighted states")
    result = {}
    for x, w in weights.items():
        v = Fraction(w)
        if v < 0:
            raise ValueError("weights must be nonnegative")
        y = coarse_map[x]
        result[y] = result.get(y, Fraction(0)) + v
    return result
