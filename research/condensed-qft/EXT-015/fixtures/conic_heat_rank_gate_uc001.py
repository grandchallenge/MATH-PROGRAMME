"""Exact rational finite-rank regression for REACH UC-OP-001.

Only algebraic gate examples. Does not prove original105 scalar heat-stage
polyhomogeneity or original108 completed source membership.
"""
from fractions import Fraction


def _rank(rows):
    if not rows:
        return 0
    matrix = [[Fraction(x) for x in row] for row in rows]
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("ragged matrix")
    pivot_row = 0
    for col in range(width):
        pivot = next((r for r in range(pivot_row, len(matrix))
                      if matrix[r][col] != 0), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        factor = matrix[pivot_row][col]
        matrix[pivot_row] = [x / factor for x in matrix[pivot_row]]
        for r in range(len(matrix)):
            if r != pivot_row:
                factor = matrix[r][col]
                if factor:
                    matrix[r] = [a - factor * b
                                 for a, b in zip(matrix[r], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def heat_elliptic_on_conormal(heat_rows, conormal_basis):
    """Whether heat-direction matrix is injective on a conormal subspace.

    heat_rows: m-vectors representing fixed heat directions.
    conormal_basis: linearly independent m-vectors spanning the conormal.
    """
    if not conormal_basis:
        return True
    m = len(conormal_basis[0])
    if any(len(x) != m for x in heat_rows + conormal_basis):
        raise ValueError("dimension mismatch")
    if _rank(conormal_basis) != len(conormal_basis):
        raise ValueError("conormal vectors must be a basis")
    images = [[sum(Fraction(a) * Fraction(b)
                   for a, b in zip(heat, direction))
               for direction in conormal_basis] for heat in heat_rows]
    return _rank(images) == len(conormal_basis)


def run_regression():
    # Protected conic195: (r,t) forbidden ray, heat in t -> elliptic.
    assert heat_elliptic_on_conormal(
        [(0, 1)], [(1, -1)]
    )
    # UC1.8: r=u partition has a conormal untouched by t-only heat.
    assert not heat_elliptic_on_conormal(
        [(0, 1, 0)], [(1, 0, -1)]
    )
    # An additional r heat direction removes that specific degeneracy.
    assert heat_elliptic_on_conormal(
        [(0, 1, 0), (1, 0, 0)], [(1, 0, -1)]
    )
    # Both generators individually interact with t heat, but their span
    # contains (1,0,-1), so a basis-vector-only test is unsound.
    full_diagonal = [(1, -1, 0), (0, 1, -1)]
    assert all(sum(a*b for a,b in zip((0, 1, 0), v)) != 0
               for v in full_diagonal)
    assert not heat_elliptic_on_conormal([(0, 1, 0)], full_diagonal)
    # Two independent heat directions pass the complete two-dimensional gate.
    assert heat_elliptic_on_conormal(
        [(0, 1, 0), (1, 0, 0)], full_diagonal
    )
    print("UC-OP-001 exact rational heat-rank gates: PASS (5 cases)")


if __name__ == "__main__":
    run_regression()
