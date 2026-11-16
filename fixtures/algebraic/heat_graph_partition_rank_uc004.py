"""Exact rational heat-graph / collision-partition rank regression (UC-OP-004).

This is an algebraic gate only, not original105 all-corner PHG admission.
"""
from fractions import Fraction


def components(n, edges):
    parent = list(range(n))
    def root(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    def join(a, b):
        ra, rb = root(a), root(b)
        if ra != rb:
            parent[rb] = ra
    for a, b in edges:
        assert 0 <= a < n and 0 <= b < n
        join(a, b)
    groups = {}
    for i in range(n):
        groups.setdefault(root(i), []).append(i)
    return sorted([tuple(v) for v in groups.values()])


def rref_and_kernel(matrix):
    cols = len(matrix[0]) if matrix else 0
    a = [[Fraction(v) for v in row] for row in matrix]
    if any(len(row) != cols for row in a):
        raise ValueError("ragged")
    r, pivots = 0, []
    for j in range(cols):
        k = next((i for i in range(r, len(a)) if a[i][j]), None)
        if k is None:
            continue
        a[r], a[k] = a[k], a[r]
        z = a[r][j]
        a[r] = [v / z for v in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                z = a[i][j]
                a[i] = [v - z*w for v, w in zip(a[i], a[r])]
        pivots.append(j)
        r += 1
        if r == len(a):
            break
    free = [j for j in range(cols) if j not in pivots]
    witness = None
    if free:
        witness = [Fraction(0)] * cols
        witness[free[0]] = Fraction(1)
        for i, j in enumerate(pivots):
            witness[j] = -a[i][free[0]]
    return r, witness


def partition_gate(n, edges, blocks):
    flattened = [i for block in blocks for i in block]
    if sorted(flattened) != list(range(n)):
        raise ValueError("must partition vertices exactly")
    hs = components(n, edges)
    matrix = [[len(set(block).intersection(h)) for h in hs] for block in blocks]
    rank, kernel = rref_and_kernel(matrix)
    if kernel is not None:
        zeta = [next(kernel[h] for h, comp in enumerate(hs) if i in comp)
                for i in range(n)]
        assert any(zeta)
        assert all(sum(zeta[i] for i in block) == 0 for block in blocks)
        assert all(zeta[a] == zeta[b] for a, b in edges)
    else:
        zeta = None
    return rank == len(hs), matrix, zeta


def test_uc004():
    # Connected three-vertex path: every partition including full diagonal passes.
    connected = [(0, 1), (1, 2)]
    import itertools
    partitions = [
        [[0,1,2]], [[0,1],[2]], [[0,2],[1]], [[0],[1,2]],
        [[0],[1],[2]]
    ]
    for p in partitions:
        ok, _, witness = partition_gate(3, connected, p)
        assert ok and witness is None
    # Disconnected graph passes one selected cross-component partition.
    ok, matrix, witness = partition_gate(3, [(0,1)], [[0,2],[1]])
    assert ok and matrix == [[1,1],[1,0]] and witness is None
    # The same graph fails its full collision partition.
    ok, matrix, witness = partition_gate(3, [(0,1)], [[0,1,2]])
    assert not ok and matrix == [[2,1]] and witness is not None
    # Disconnected crossing collision: explicit killed conormal.
    ok, matrix, witness = partition_gate(
        4, [(0,1),(2,3)], [[0,2],[1,3]]
    )
    assert not ok and matrix == [[1,1],[1,1]]
    assert witness in ([Fraction(-1),Fraction(-1),Fraction(1),Fraction(1)],
                       [Fraction(1),Fraction(1),Fraction(-1),Fraction(-1)])
    # Isolated vertices and singleton partition: vacuous conormal passes.
    ok, matrix, witness = partition_gate(3, [], [[0],[1],[2]])
    assert ok and matrix == [[1,0,0],[0,1,0],[0,0,1]]
    # The graph weights (when strictly positive) do not alter the kernel test.
    ok_a, matrix_a, _ = partition_gate(4, [(0,1),(1,2),(2,3)], [[0,2],[1,3]])
    ok_b, matrix_b, _ = partition_gate(4, [(2,3),(1,2),(0,1)], [[0,2],[1,3]])
    assert ok_a and ok_b and matrix_a == matrix_b
    print("UC-OP-004 heat-graph/partition exact rank cases: PASS (6 groups)")


if __name__ == "__main__":
    test_uc004()
