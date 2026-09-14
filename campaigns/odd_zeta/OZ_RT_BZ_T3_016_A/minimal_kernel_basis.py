from __future__ import annotations

import hashlib
from collections import defaultdict
from math import comb

import numpy as np

POTENTIAL_DEGREE = 23
POTENTIAL_DIMENSION = 576
E1_NUMERATOR_DEGREE = 28
E1_COLUMNS = 1624
RAW_COLUMN_DEGREE = 6
SATURATED_COLUMN_DEGREE = 5
EXCEPTIONAL_FIBERS = tuple(range(0, -8, -1))
PIVOT_MONOMIALS = tuple((21, 20 - j) for j in range(8))
PIVOT_COLUMNS = tuple(a * 24 + b for a, b in PIVOT_MONOMIALS)
WITNESS_PRIME = 4194301
LEADING_MATRIX_SHA256 = "90dfe904b4c5150793607c12f1a829f35090e540a287b9dddbb3102ee390a142"
EXCEPTIONAL_MATRIX_SHA256 = {
    0: "cd400bf88ab15c023df273d72bff5b7e1e979c421e29cdf70c7c50a77c222552",
    -1: "1314f0db35b0b909deddfb08116fff58ef772397eb37b560028e3b8516e72c24",
    -2: "0f00fe339faa2d9da62018ae70bd7396422ea80fb0f4901b1dcb57c0502270fc",
    -3: "54fc0579a2aba25a3ce8c68d225d778f0ddfb7cbe9b1603fd6308e2c4a1dd5e6",
    -4: "f047477838ef5d6a21de77df19fe776c5e344a68d7d7a3ec7101338b0d1eae01",
    -5: "5baf2519947cc3b92f5be04d3c36de6204b97ccfb6d9aff4db0777fee72749c4",
    -6: "1282acf87904cdfb159e479251171a5d9ff107a8bcb2ce9bbbe7e128260adf0a",
    -7: "b60522e738d2a8d082787e504fe57e5f4ab2c67a46ad494e44185a0706d9ef04",
}

R_MONOMIALS = tuple(
    (a, b) for a in range(1, E1_NUMERATOR_DEGREE + 1) for b in range(E1_NUMERATOR_DEGREE + 1)
)
S_MONOMIALS = tuple(
    (a, b) for a in range(E1_NUMERATOR_DEGREE + 1) for b in range(1, E1_NUMERATOR_DEGREE + 1)
)
R_INDEX = {monomial: index for index, monomial in enumerate(R_MONOMIALS)}
S_INDEX = {monomial: len(R_MONOMIALS) + index for index, monomial in enumerate(S_MONOMIALS)}


def _clean(mapping):
    return {key: int(value) for key, value in mapping.items() if value}


def _add(left, right, scale=1):
    out = dict(left)
    for key, value in right.items():
        new_value = out.get(key, 0) + scale * value
        if new_value:
            out[key] = new_value
        elif key in out:
            del out[key]
    return out


def _mul2(left, right):
    out = defaultdict(int)
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            out[(a + c, b + d)] += x * y
    return _clean(out)


def _shift2(poly, variable):
    out = defaultdict(int)
    if variable == "l":
        for (a, b), value in poly.items():
            for degree in range(b + 1):
                out[(a, degree)] += value * comb(b, degree)
    elif variable == "k":
        for (a, b), value in poly.items():
            for degree in range(a + 1):
                out[(degree, b)] += value * comb(a, degree)
    else:
        raise ValueError("variable must be k or l")
    return _clean(out)


def _univariate_from_roots(roots):
    coefficients = [1]
    for root in roots:
        updated = [0] * (len(coefficients) + 1)
        for degree, value in enumerate(coefficients):
            updated[degree] -= root * value
            updated[degree + 1] += value
        coefficients = updated
    return coefficients


def _vertical_root_multiplicities(j):
    """Root multiplicities for U_j when the exceptional fiber is n=-j."""
    orders = defaultdict(int)
    orders[0] += 2
    orders[-1] += 1
    orders[j - 7] += 1
    orders[7 - j] -= 2
    orders[j - 1] -= 2
    lo = min(orders) - 2
    hi = max(orders) + 2
    current = 0
    roots = []
    multiplicities = {}
    for point in range(lo, hi + 1):
        if current < 0:
            raise AssertionError("negative vertical divisor multiplicity")
        if current:
            multiplicities[point] = current
            roots.extend([point] * current)
        current += orders[point]
    if current != 0:
        raise AssertionError("vertical divisor does not close")
    return multiplicities, roots


def _exceptional_u(j):
    _, roots = _vertical_root_multiplicities(j)
    return _univariate_from_roots(roots)


def _exceptional_v(j):
    roots = [-s for s in range(-j + 1, 2)]
    return _univariate_from_roots(roots)


def _exceptional_h(j):
    u = _exceptional_u(j)
    v = _exceptional_v(j)
    uk = {(degree, 0): value for degree, value in enumerate(u) if value}
    ul = {(0, degree): value for degree, value in enumerate(u) if value}
    diagonal = defaultdict(int)
    for degree, value in enumerate(v):
        if not value:
            continue
        for k_degree in range(degree + 1):
            diagonal[(k_degree, degree - k_degree)] += value * comb(degree, k_degree)
    return _mul2(_mul2(uk, ul), _clean(diagonal))


def _mul3(left, right):
    out = defaultdict(int)
    for (an, ak, al), x in left.items():
        for (bn, bk, bl), y in right.items():
            out[(an + bn, ak + bk, al + bl)] += x * y
    return _clean(out)


def _lin3(constant=0, n_coefficient=0, k_coefficient=0, l_coefficient=0):
    out = {}
    if constant:
        out[(0, 0, 0)] = constant
    if n_coefficient:
        out[(1, 0, 0)] = n_coefficient
    if k_coefficient:
        out[(0, 1, 0)] = k_coefficient
    if l_coefficient:
        out[(0, 0, 1)] = l_coefficient
    return out


def _pow3(poly, exponent):
    out = {(0, 0, 0): 1}
    for _ in range(exponent):
        out = _mul3(out, poly)
    return out


def _embed2(poly):
    return {(0, a, b): value for (a, b), value in poly.items()}


def _curl_pair(potential):
    h0 = _embed2(potential)
    hl1 = _embed2(_shift2(potential, "l"))
    hk1 = _embed2(_shift2(potential, "k"))

    outer_r = _mul3(
        _pow3(_lin3(k_coefficient=1), 2),
        _mul3(_lin3(constant=1, k_coefficient=1), _lin3(constant=7, n_coefficient=1, k_coefficient=1)),
    )
    left_r = _mul3(
        _pow3(_lin3(constant=7, n_coefficient=1, l_coefficient=-1), 2),
        _mul3(
            _pow3(_lin3(constant=1, n_coefficient=1, l_coefficient=1), 2),
            _lin3(constant=1, n_coefficient=1, k_coefficient=1, l_coefficient=1),
        ),
    )
    right_r = _mul3(
        _pow3(_lin3(l_coefficient=1), 2),
        _mul3(
            _lin3(constant=1, l_coefficient=1),
            _mul3(
                _lin3(constant=2, k_coefficient=1, l_coefficient=1),
                _lin3(constant=7, n_coefficient=1, l_coefficient=1),
            ),
        ),
    )
    nr = _mul3(outer_r, _add(_mul3(left_r, hl1), _mul3(right_r, h0), scale=-1))

    outer_s = _mul3(
        _pow3(_lin3(l_coefficient=1), 2),
        _mul3(_lin3(constant=1, l_coefficient=1), _lin3(constant=7, n_coefficient=1, l_coefficient=1)),
    )
    left_s = _mul3(
        _pow3(_lin3(k_coefficient=1), 2),
        _mul3(
            _lin3(constant=1, k_coefficient=1),
            _mul3(
                _lin3(constant=2, k_coefficient=1, l_coefficient=1),
                _lin3(constant=7, n_coefficient=1, k_coefficient=1),
            ),
        ),
    )
    right_s = _mul3(
        _pow3(_lin3(constant=7, n_coefficient=1, k_coefficient=-1), 2),
        _mul3(
            _pow3(_lin3(constant=1, n_coefficient=1, k_coefficient=1), 2),
            _lin3(constant=1, n_coefficient=1, k_coefficient=1, l_coefficient=1),
        ),
    )
    ns = _mul3(outer_s, _add(_mul3(left_s, h0), _mul3(right_s, hk1), scale=-1))
    return nr, ns


def _divide_by_n_plus_j(poly, j):
    groups = defaultdict(dict)
    for (n_degree, k_degree, l_degree), value in poly.items():
        groups[(k_degree, l_degree)][n_degree] = value
    quotient = {}
    for (k_degree, l_degree), coefficients in groups.items():
        degree = max(coefficients)
        source = [coefficients.get(index, 0) for index in range(degree + 1)]
        if degree == 0:
            if source[0]:
                raise AssertionError("nonzero constant is not divisible by n+j")
            continue
        target = [0] * degree
        target[-1] = source[-1]
        for index in range(degree - 1, 0, -1):
            target[index - 1] = source[index] - j * target[index]
        remainder = source[0] - j * target[0]
        if remainder:
            raise AssertionError(f"curl column is not divisible by n+{j}")
        for n_degree, value in enumerate(target):
            if value:
                quotient[(n_degree, k_degree, l_degree)] = value
    return quotient


def _degree_n(poly):
    return max(n_degree for n_degree, _, _ in poly)


def _evaluate_n(poly, value, modulus):
    out = defaultdict(int)
    n_mod = value % modulus
    powers = [1]
    max_degree = _degree_n(poly)
    for _ in range(max_degree):
        powers.append(powers[-1] * n_mod % modulus)
    for (n_degree, k_degree, l_degree), coefficient in poly.items():
        out[(k_degree, l_degree)] = (
            out[(k_degree, l_degree)] + (coefficient % modulus) * powers[n_degree]
        ) % modulus
    return _clean(out)


def _pair_to_vector(nr, ns, n_value, modulus):
    vector = np.zeros(E1_COLUMNS, dtype=np.int64)
    for monomial, value in _evaluate_n(nr, n_value, modulus).items():
        vector[R_INDEX[monomial]] = value % modulus
    for monomial, value in _evaluate_n(ns, n_value, modulus).items():
        vector[S_INDEX[monomial]] = value % modulus
    return vector


def _coefficient_vector(nr, ns, degree, modulus):
    vector = np.zeros(E1_COLUMNS, dtype=np.int64)
    for (n_degree, k_degree, l_degree), value in nr.items():
        if n_degree == degree:
            vector[R_INDEX[(k_degree, l_degree)]] = value % modulus
    for (n_degree, k_degree, l_degree), value in ns.items():
        if n_degree == degree:
            vector[S_INDEX[(k_degree, l_degree)]] = value % modulus
    return vector


def _rank_mod(matrix, modulus):
    a = np.asarray(matrix, dtype=np.int64).copy() % modulus
    rows, columns = a.shape
    rank = 0
    for column in range(columns):
        nonzero = np.flatnonzero(a[rank:, column])
        if nonzero.size == 0:
            continue
        pivot = rank + int(nonzero[0])
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        inverse = pow(int(a[rank, column]), modulus - 2, modulus)
        a[rank, column:] = a[rank, column:] * inverse % modulus
        targets = np.flatnonzero(a[rank + 1 :, column]) + rank + 1
        if targets.size:
            factors = a[targets, column].copy()
            a[targets, column:] = (
                a[targets, column:] - factors[:, None] * a[rank, column:][None, :]
            ) % modulus
        rank += 1
        if rank == columns:
            break
    return rank


def _matrix_sha256(matrix):
    canonical = np.asarray(matrix, dtype="<i8", order="C")
    return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


def _bareiss_det(matrix):
    a = [list(map(int, row)) for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((row for row in range(k + 1, n) if a[row][k] != 0), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        pivot_value = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot_value - a[i][k] * a[k][j]
                if k:
                    if numerator % previous:
                        raise AssertionError("Bareiss division was not exact")
                    numerator //= previous
                a[i][j] = numerator
        previous = pivot_value
    return sign * a[-1][-1]


def _raw_pairs():
    return [_curl_pair({(a, b): 1}) for a in range(24) for b in range(24)]


def _replacement_pairs():
    pairs = []
    potentials = []
    for j in range(8):
        h = _exceptional_h(j)
        nr, ns = _curl_pair(h)
        q_nr = _divide_by_n_plus_j(nr, j)
        q_ns = _divide_by_n_plus_j(ns, j)
        if _degree_n(q_nr) != SATURATED_COLUMN_DEGREE or _degree_n(q_ns) != SATURATED_COLUMN_DEGREE:
            raise AssertionError("saturated replacement degree drift")
        pairs.append((q_nr, q_ns))
        potentials.append(h)
    return potentials, pairs


def _build_final_matrix(raw, replacements, n_value, modulus):
    matrix = np.zeros((E1_COLUMNS, POTENTIAL_DIMENSION), dtype=np.int64)
    for column, (nr, ns) in enumerate(raw):
        matrix[:, column] = _pair_to_vector(nr, ns, n_value, modulus)
    for j, column in enumerate(PIVOT_COLUMNS):
        nr, ns = replacements[j]
        matrix[:, column] = _pair_to_vector(nr, ns, n_value, modulus)
    return matrix


def _build_raw_matrix(raw, n_value, modulus):
    matrix = np.zeros((E1_COLUMNS, POTENTIAL_DIMENSION), dtype=np.int64)
    for column, (nr, ns) in enumerate(raw):
        matrix[:, column] = _pair_to_vector(nr, ns, n_value, modulus)
    return matrix


def _build_leading_matrix(raw, replacements, modulus):
    matrix = np.zeros((E1_COLUMNS, POTENTIAL_DIMENSION), dtype=np.int64)
    pivot_to_j = {column: j for j, column in enumerate(PIVOT_COLUMNS)}
    for column, (nr, ns) in enumerate(raw):
        if column in pivot_to_j:
            q_nr, q_ns = replacements[pivot_to_j[column]]
            matrix[:, column] = _coefficient_vector(
                q_nr, q_ns, SATURATED_COLUMN_DEGREE, modulus
            )
        else:
            matrix[:, column] = _coefficient_vector(nr, ns, RAW_COLUMN_DEGREE, modulus)
    return matrix


def build_minimal_kernel_basis():
    potentials, replacements = _replacement_pairs()
    raw = _raw_pairs()

    pivot_matrix = [
        [potentials[column].get(PIVOT_MONOMIALS[row], 0) for column in range(8)]
        for row in range(8)
    ]
    if _bareiss_det(pivot_matrix) != 1:
        raise AssertionError("exceptional potential pivot matrix is not unimodular")

    raw_exceptional_ranks = {}
    final_exceptional_ranks = {}
    final_exceptional_hashes = {}
    for fiber in EXCEPTIONAL_FIBERS:
        raw_matrix = _build_raw_matrix(raw, fiber, WITNESS_PRIME)
        raw_rank = _rank_mod(raw_matrix, WITNESS_PRIME)
        if raw_rank != POTENTIAL_DIMENSION - 1:
            raise AssertionError(f"raw curl rank drift at n={fiber}: {raw_rank}")
        raw_exceptional_ranks[str(fiber)] = raw_rank

        final_matrix = _build_final_matrix(raw, replacements, fiber, WITNESS_PRIME)
        final_rank = _rank_mod(final_matrix, WITNESS_PRIME)
        digest = _matrix_sha256(final_matrix)
        if final_rank != POTENTIAL_DIMENSION:
            raise AssertionError(f"saturated basis rank drift at n={fiber}: {final_rank}")
        if digest != EXCEPTIONAL_MATRIX_SHA256[fiber]:
            raise AssertionError(f"saturated basis digest drift at n={fiber}")
        final_exceptional_ranks[str(fiber)] = final_rank
        final_exceptional_hashes[str(fiber)] = digest

    for fiber in (1, -8):
        raw_rank = _rank_mod(_build_raw_matrix(raw, fiber, WITNESS_PRIME), WITNESS_PRIME)
        if raw_rank != POTENTIAL_DIMENSION:
            raise AssertionError(f"raw generic-neighbor rank drift at n={fiber}: {raw_rank}")

    leading = _build_leading_matrix(raw, replacements, WITNESS_PRIME)
    leading_rank = _rank_mod(leading, WITNESS_PRIME)
    leading_digest = _matrix_sha256(leading)
    if leading_rank != POTENTIAL_DIMENSION or leading_digest != LEADING_MATRIX_SHA256:
        raise AssertionError("column-reduced leading witness drift")

    u_degrees = []
    v_degrees = []
    h_bidegrees = []
    for j, h in enumerate(potentials):
        u_degrees.append(len(_exceptional_u(j)) - 1)
        v_degrees.append(len(_exceptional_v(j)) - 1)
        h_bidegrees.append([max(a for a, _ in h), max(b for _, b in h)])

    return {
        "raw_kernel_basis_dimension": POTENTIAL_DIMENSION,
        "raw_column_degree": RAW_COLUMN_DEGREE,
        "raw_total_column_degree": POTENTIAL_DIMENSION * RAW_COLUMN_DEGREE,
        "fixed_fiber_kernel_classification": {
            "characteristic_zero_exact": True,
            "exceptional_fibers": list(EXCEPTIONAL_FIBERS),
            "kernel_dimension_at_each_exceptional_fiber": 1,
            "kernel_dimension_elsewhere": 0,
            "u_degrees_j_0_through_7": u_degrees,
            "v_degrees_j_0_through_7": v_degrees,
            "h_bidegrees": h_bidegrees,
        },
        "saturation": {
            "pivot_monomials": [list(monomial) for monomial in PIVOT_MONOMIALS],
            "pivot_matrix": pivot_matrix,
            "pivot_matrix_determinant": 1,
            "divided_linear_factors": [f"n+{j}" if j else "n" for j in range(8)],
            "generic_change_of_basis_determinant": "1/(n*(n+1)*(n+2)*(n+3)*(n+4)*(n+5)*(n+6)*(n+7))",
            "replacement_column_degree": SATURATED_COLUMN_DEGREE,
            "replacement_columns": len(PIVOT_COLUMNS),
            "unchanged_columns": POTENTIAL_DIMENSION - len(PIVOT_COLUMNS),
            "final_total_column_degree": (POTENTIAL_DIMENSION - 8) * RAW_COLUMN_DEGREE + 8 * SATURATED_COLUMN_DEGREE,
        },
        "witness": {
            "prime": WITNESS_PRIME,
            "raw_exceptional_ranks": raw_exceptional_ranks,
            "saturated_exceptional_ranks": final_exceptional_ranks,
            "saturated_exceptional_matrix_sha256": final_exceptional_hashes,
            "leading_matrix_rank": leading_rank,
            "leading_matrix_sha256": leading_digest,
        },
        "minimal_polynomial_kernel_basis": True,
        "minimal_basis_criterion": (
            "exact fixed-fiber classification plus full-rank exceptional witnesses gives finite irreducibility; "
            "the degree-leading matrix has rank 576, so the polynomial basis is column-reduced; "
            "finite irreducibility plus column reduction is the minimal-basis criterion"
        ),
        "overall_terminal": "ORDER7_E1_KERNEL_IDENTIFIED_AS_DISCRETE_CURL__POTENTIAL_SECTION_REDUCTION_REQUIRED",
        "next_obligation": "AFFINE_SECTION_REDUCTION_IN_SATURATED_MINIMAL_KERNEL_BASIS",
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_proved": False,
        "t3_refuted": False,
        "global_certificate_constructed": False,
    }
