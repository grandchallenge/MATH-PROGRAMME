"""UC004 exact graph/partition regression; stdlib only, no source admission claim.

Compares component-intersection nullity with independently built restricted
covariance nullity. Finite arithmetic is not an analytic smoothing proof.
"""
from fractions import Fraction
from itertools import combinations
import json


def rref(rows, width):
    matrix = [[Fraction(x) for x in row] for row in rows]
    if any(len(row) != width for row in matrix):
        raise ValueError("ragged matrix")
    pivots = []
    for col in range(width):
        pivot = next((r for r in range(len(pivots), len(matrix))
                      if matrix[r][col]), None)
        if pivot is None:
            continue
        row = len(pivots)
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        scale = matrix[row][col]
        matrix[row] = [x / scale for x in matrix[row]]
        for r in range(len(matrix)):
            if r != row and matrix[r][col]:
                scale = matrix[r][col]
                matrix[r] = [a - scale * b
                             for a, b in zip(matrix[r], matrix[row])]
        pivots.append(col)
        if len(pivots) == len(matrix):
            break
    return matrix, pivots


def rank(rows, width):
    return len(rref(rows, width)[1])


def kernel_vector(rows, width):
    reduced, pivots = rref(rows, width)
    free = next((j for j in range(width) if j not in pivots), None)
    if free is None:
        return None
    vector = [Fraction(0)] * width
    vector[free] = Fraction(1)
    for row, col in enumerate(pivots):
        vector[col] = -reduced[row][free]
    return vector


def partitions(n):
    """Each unordered set partition once, with canonical block/root order."""
    def extend(blocks, vertex):
        if vertex == n:
            yield tuple(tuple(block) for block in blocks)
            return
        for block in range(len(blocks)):
            blocks[block].append(vertex)
            yield from extend(blocks, vertex + 1)
            blocks[block].pop()
        blocks.append([vertex])
        yield from extend(blocks, vertex + 1)
        blocks.pop()
    yield from extend([], 0)


def components(n, edges, grounded=False):
    """Combinatorial traversal, independent of covariance construction."""
    count = n + int(grounded)
    adjacency = [set() for _ in range(count)]
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    unseen = set(range(count))
    result = []
    while unseen:
        todo = [min(unseen)]
        component = set()
        while todo:
            vertex = todo.pop()
            if vertex in component:
                continue
            component.add(vertex)
            todo.extend(adjacency[vertex] - component)
        unseen -= component
        if not (grounded and n in component):
            result.append(component)
    return result


def intersection_matrix(partition, comps):
    return [[len(set(block) & comp) for comp in comps]
            for block in partition]


def conormal_basis(n, partition):
    basis = []
    for block in partition:
        for vertex in block[1:]:
            vector = [0] * n
            vector[vertex], vector[block[0]] = 1, -1
            basis.append(vector)
    return basis


def covariance(n, edges, weights):
    """Direct outer products of actual heat columns, dropping ground slot."""
    if len(edges) != len(weights):
        raise ValueError("edge/variance length mismatch")
    matrix = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for (i, j), weight in zip(edges, weights):
        if weight <= 0:
            raise ValueError("strictly positive edge variances required")
        vector = [0] * n
        if i < n:
            vector[i] += 1
        if j < n:
            vector[j] -= 1
        for row in range(n):
            for col in range(n):
                matrix[row][col] += weight * vector[row] * vector[col]
    return matrix


def matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def restricted_gram(matrix, basis):
    images = [matvec(matrix, vector) for vector in basis]
    return [[sum(a * b for a, b in zip(left, image))
             for image in images] for left in basis]


def verify_partition(n, partition, comps, matrix):
    incidence = intersection_matrix(partition, comps)
    basis = conormal_basis(n, partition)
    gram = restricted_gram(matrix, basis)
    component_nullity = len(comps) - rank(incidence, len(comps))
    gram_nullity = len(basis) - rank(gram, len(basis))
    assert component_nullity == gram_nullity, (n, partition, incidence, gram)
    if component_nullity:
        witness = kernel_vector(incidence, len(comps))
        assert witness is not None
        physical = [Fraction(0)] * n
        for comp, value in zip(comps, witness):
            for vertex in comp:
                physical[vertex] = value
        assert any(physical)
        assert all(sum(physical[i] for i in block) == 0
                   for block in partition)
        assert all(x == 0 for x in matvec(matrix, physical))
    return component_nullity == 0


def controls():
    # Original eleven-edge host, ONLY if these are directional convolutions.
    host = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
            (0, 4), (1, 4), (0, 5), (1, 5), (4, 5)]
    host_parts = list(partitions(6))
    assert len(host_parts) == 203
    host_comps = components(6, host)
    assert len(host_comps) == 1
    host_covariance = covariance(
        6, host, [Fraction(i + j + 1, j + 2) for i, j in host])
    assert all(verify_partition(6, p, host_comps, host_covariance)
               for p in host_parts)
    edges = [(0, 1), (2, 3)]
    matrix = covariance(4, edges, [Fraction(1), Fraction(1)])
    crossing = ((0, 2), (1, 3))
    comps = components(4, edges)
    assert intersection_matrix(crossing, comps) == [[1, 1], [1, 1]]
    gram = restricted_gram(matrix, conormal_basis(4, crossing))
    assert gram == [[2, -2], [-2, 2]]
    assert all(gram[i][i] == 2 for i in range(2))
    assert not verify_partition(4, crossing, comps, matrix)
    assert verify_partition(4, ((0, 1), (2, 3)), comps, matrix)
    assert not verify_partition(4, ((0, 1, 2, 3),), comps, matrix)
    # One free component passes every physical conormal, despite disconnection.
    edges = [(0, 3), (1, 2)]
    comps = components(3, edges, grounded=True)
    assert len(comps) == 1
    matrix = covariance(3, edges, [Fraction(2, 3), Fraction(7, 5)])
    assert all(verify_partition(3, p, comps, matrix) for p in partitions(3))
    edges = [(0, 2), (1, 2)]
    comps = components(2, edges, grounded=True)
    assert not comps
    matrix = covariance(2, edges, [Fraction(3, 7), Fraction(5, 11)])
    assert rank(matrix, 2) == 2
    assert all(verify_partition(2, p, comps, matrix) for p in partitions(2))
    # Zero weight must be rejected; deleting that edge really changes the gate.
    try:
        covariance(2, [(0, 1)], [Fraction(0)])
    except ValueError:
        pass
    else:
        raise AssertionError("zero weight was accepted")
    empty = covariance(2, [], [])
    assert not verify_partition(2, ((0, 1),), components(2, []), empty)
    positive = covariance(2, [(0, 1)], [Fraction(1, 13)])
    assert verify_partition(2, ((0, 1),), components(2, [(0, 1)]), positive)


def exhaustive(max_n, grounded):
    graph_count = pair_count = 0
    for n in range(1, max_n + 1):
        possible = list(combinations(range(n + int(grounded)), 2))
        block_partitions = list(partitions(n))
        for mask in range(1 << len(possible)):
            edges = [edge for bit, edge in enumerate(possible)
                     if mask & (1 << bit)]
            # Strictly positive, nonconstant exact rational variances.
            weights = [Fraction(i + j + 1, j + 2) for i, j in edges]
            matrix = covariance(n, edges, weights)
            comps = components(n, edges, grounded)
            outcomes = [verify_partition(n, p, comps, matrix)
                        for p in block_partitions]
            predicted = len(comps) <= 1 if grounded else len(comps) == 1
            assert all(outcomes) == predicted, (n, edges, grounded)
            graph_count += 1
            pair_count += len(outcomes)
    return {"graphs": graph_count, "graph_partition_pairs": pair_count}


def main():
    controls()
    result = {
        "status": "PASS",
        "arithmetic": "exact Fraction; strictly positive rational variances",
        "ungrounded_n_1_to_5": exhaustive(5, grounded=False),
        "grounded_n_1_to_4": exhaustive(4, grounded=True),
        "conditional_eleven_edge_host_partitions": 203,
        "scope": "finite algebraic regression; no analytic or source certification",
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
