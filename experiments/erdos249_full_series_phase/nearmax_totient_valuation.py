"""WP07-C: self-contained integer evidence for rare near-maximal v2(phi(n)).

Classical prime factorization gives the universal theorem, not finite scans.
This module neither proves the original irrationality of the full series nor
supplies a cofinal finite-sum fractional-part gap.
"""
from math import isqrt


def totients(limit: int) -> list[int]:
    if limit < 1:
        raise ValueError("positive sieve limit")
    values = list(range(limit + 1))
    for p in range(2, limit + 1):
        if values[p] == p:
            for n in range(p, limit + 1, p):
                values[n] -= values[n] // p
    return values


def factors(n: int) -> tuple[tuple[int, int], ...]:
    """Independent exact trial-factorization oracle."""
    if n < 1:
        raise ValueError("positive integer required")
    out = []
    for p in range(2, isqrt(n) + 1):
        if n % p == 0:
            a = 0
            while n % p == 0:
                n //= p
                a += 1
            out.append((p, a))
    if n > 1:
        out.append((n, 1))
    return tuple(out)


def v2(n: int) -> int:
    if n == 0:
        raise ValueError("undefined valuation of zero")
    return (abs(n) & -abs(n)).bit_length() - 1


def odd_part(n: int) -> int:
    if n < 1:
        raise ValueError("positive integer required")
    return n >> v2(n)


def is_nearmax(n: int, C: int, phi: list[int]) -> bool:
    if n < 1 or C < 0 or len(phi) <= n:
        raise ValueError("invalid n, C or totient data")
    return v2(phi[n]) >= n.bit_length() - 1 - C


def restricted_factor_shape(n: int, C: int, phi: list[int]) -> dict[str, object]:
    """Independent necessary-shape check only when n is near-max."""
    if not is_nearmax(n, C, phi):
        raise ValueError("n is not in E_C")
    B = 1 << (C + 1)
    odd = odd_part(phi[n])
    if not odd < B:
        raise AssertionError("bounded odd part falsified")
    rows = []
    for p, exponent in factors(n):
        if p == 2:
            continue
        d = odd_part(p - 1)
        r = v2(p - 1)
        if not (d < B and d % 2 == 1 and r >= 1):
            raise AssertionError("restricted large-prime shape falsified")
        if p > B and exponent != 1:
            raise AssertionError("large-prime exponent limit falsified")
        if p <= B and pow(p, exponent - 1) > B:
            raise AssertionError("small-prime exponent limit falsified")
        rows.append((p, exponent, r, d))
    return {
        "n": n, "C": C, "bounded_odd_part": odd,
        "odd_primes": rows, "boundary": "SHAPE_NECESSARY_ONLY__FULL_S_OPEN",
    }


def small_odd_exponent_patterns(B: int) -> int:
    if B < 2:
        raise ValueError("B>=2 required")
    product = 1
    for p in range(3, B + 1, 2):
        if any(p % k == 0 for k in range(3, isqrt(p) + 1, 2)):
            continue
        power, log_p_B = p, 0
        while power <= B:
            log_p_B += 1
            power *= p
        product *= 2 + log_p_B
    return product


def weighted_subset_envelope(R: int, B: int) -> int:
    """Exact coefficient sum <=R of prod_{r>=1}(1+t^r)^B."""
    if R < 1 or B < 2:
        raise ValueError("R>=1 and B>=2")
    coeff = [1] + [0] * R
    for r in range(1, R + 1):
        for _ in range(B):
            for k in range(R, r - 1, -1):
                coeff[k] += coeff[k - r]
    return sum(coeff)


def finite_shape_envelope(X: int, C: int) -> int:
    """Exact combinatorial majorant, pre-exponential-optimization."""
    if X < 2 or C < 0:
        raise ValueError("X>=2 and C>=0")
    R = X.bit_length() - 1
    B = 1 << (C + 1)
    return ((R + 1) * small_odd_exponent_patterns(B)
            * weighted_subset_envelope(R, B))


def nearmax_witnesses(X: int, C: int,
                      phi: list[int] | None = None) -> tuple[int, ...]:
    if X < 2 or C < 0:
        raise ValueError("X>=2 and C>=0")
    values = phi if phi is not None else totients(X)
    if len(values) <= X:
        raise ValueError("totient data too short")
    return tuple(n for n in range(1, X + 1)
                 if is_nearmax(n, C, values))


def termwise_nearlog_starts(X: int, C: int,
                            phi: list[int] | None = None) -> tuple[int, ...]:
    if X < 2 or C < 0:
        raise ValueError("X>=2 and C>=0")
    L = X.bit_length() - 1 - C
    if not 1 <= L <= X:
        raise ValueError("nearlog depth positive and <=X required")
    values = phi if phi is not None else totients(2 * X + L)
    if len(values) <= 2 * X - 1 + L:
        raise ValueError("totient source too short")
    return tuple(N for N in range(X, 2 * X)
                 if all(values[N + j] % (1 << j) == 0
                        for j in range(1, L + 1)))



def finite_scaled_numerator(N: int, L: int, phi: list[int]) -> int:
    """Exact 2^L-scaled sum, independent direct definition."""
    if N < 1 or L < 1 or len(phi) <= N + L:
        raise ValueError("invalid source/depth")
    return sum(phi[N + j] << (L - j) for j in range(1, L + 1))


def nearlog_integral_sums_and_adjacent_pairs(
    X: int, C: int, phi: list[int] | None = None
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Rolling exact residue recurrence for actual totient finite sums.

    Returns starting positions with integral finite sum and those with
    both the sum at N and at N+1 integral, including N=2X-1.
    """
    if X < 2 or C < 0:
        raise ValueError("X>=2 and C>=0")
    L = X.bit_length() - 1 - C
    if not 1 <= L <= X:
        raise ValueError("nearlog depth positive and <=X required")
    values = phi if phi is not None else totients(2 * X + L)
    if len(values) <= 2 * X + L:
        raise ValueError("totient source too short for next-start comparison")
    modulus = 1 << L
    A = finite_scaled_numerator(X, L, values)
    starts, adjacent = [], []
    for N in range(X, 2 * X):
        next_A = 2 * A - modulus * values[N + 1] + values[N + L + 1]
        integral = A % modulus == 0
        next_integral = next_A % modulus == 0
        if integral:
            starts.append(N)
        if integral and next_integral:
            adjacent.append(N)
        A = next_A
    return tuple(starts), tuple(adjacent)

def research_receipt(X: int, C: int) -> dict[str, object]:
    """A finite control; no finite sample is a proof of X^{o(1)}."""
    if X < 2 or C < 0:
        raise ValueError("X>=2 and C>=0")
    L = X.bit_length() - 1 - C
    if L < 1:
        raise ValueError("depth nonpositive")
    values = totients(3 * X)
    starts = termwise_nearlog_starts(X, C, values)
    eligible = set(nearmax_witnesses(3 * X, C + 2, values))
    if any((N + L) not in eligible for N in starts):
        raise AssertionError("termwise window implication falsified")
    integral_sums, adjacent_pairs = nearlog_integral_sums_and_adjacent_pairs(X, C, values)
    if any(N+L+1 not in eligible for N in adjacent_pairs):
        raise AssertionError("adjacent-integrality nearmax implication falsified")
    if len(integral_sums) > ((X+1)//2 + len(adjacent_pairs)):
        raise AssertionError("adjacent pair combinatorial density bound falsified")
    finite_bound = finite_shape_envelope(3 * X, C + 2)
    if len(eligible) > finite_bound:
        raise AssertionError("finite combinatorial bound falsified")
    return {
        "X": X, "C": C, "L": L,
        "termwise_integer_starts": len(starts),
        "integral_finite_sum_starts": len(integral_sums),
        "adjacent_integral_sum_pairs": len(adjacent_pairs),
        "nearmax_eligible_until_3X": len(eligible),
        "exact_integer_combinatorial_envelope": str(finite_bound),
        "all_implications_checked": True,
        "claim_boundary": "FINITE_CHECK_ONLY__EXACT_ELEMENTARY_PROOF__FULL_S_OPEN",
    }



def odd_part_budget(B: int) -> int:
    """Largest K>=0 with 3**K < B, for B>=2; exact integer arithmetic."""
    if B < 2:
        raise ValueError("B>=2 required")
    k, power = 0, 1
    while 3 * power < B:
        power *= 3
        k += 1
    return k


def fermat_exponent_slots(R: int) -> int:
    """Count r in {1,2,4,8,...} satisfying r<=R."""
    if R < 1:
        raise ValueError("R>=1 required")
    return R.bit_length()


def polylog_fermat_envelope(X: int, C: int) -> int:
    """Theorem WP07-D(A), exact integer upper bound, *not* empirical proof.

    Evaluator limited to C<=10 to avoid unbounded exponentially large
    candidate registries in constrained runs. The *manuscript* theorem has
    no fixed-C ceiling; symbolic proof is independent of this evaluator.
    """
    if X < 2 or C < 0 or C > 10:
        raise ValueError("X>=2 and 0<=C<=10 required by finite evaluator")
    from math import comb
    R = X.bit_length() - 1
    B = 1 << (C + 1)
    K = odd_part_budget(B)
    subset_choices = sum(comb(B * R, j)
                         for j in range(min(K, B * R) + 1))
    return ((R + 1) * small_odd_exponent_patterns(B)
            * (1 << fermat_exponent_slots(R)) * subset_choices)


def fermat_prime_shape_check(n: int, C: int, phi: list[int]) -> dict[str, object]:
    """Check 2-adic nearmax necessity with independently factored n."""
    if not is_nearmax(n, C, phi):
        raise ValueError("not nearmax")
    B = 1 << (C + 1)
    u = odd_part(phi[n])
    if not 1 <= u < B:
        raise AssertionError("bounded odd part falsified")
    non_fermat_large = []
    fermat_large = []
    small_odd = []
    odd_d_product = 1
    for p, a in factors(n):
        if p == 2:
            continue
        r = v2(p - 1)
        d = (p - 1) >> r
        if not (r >= 1 and d & 1 and d < B):
            raise AssertionError("restricted prime factor shape falsified")
        odd_d_product *= d
        if d == 1:
            if r & (r - 1):
                raise AssertionError("composite Fermat-exponent candidate")
            if p > B:
                fermat_large.append(p)
        elif p > B:
            if a != 1:
                raise AssertionError("large odd prime repeated")
            non_fermat_large.append(p)
        if p <= B:
            small_odd.append((p, a))
    if odd_d_product > u or u % odd_d_product:
        raise AssertionError("oddpart budget product falsified")
    if len(non_fermat_large) > odd_part_budget(B):
        raise AssertionError("non-Fermat large-prime count budget falsified")
    if C == 0:
        if n % 2 == 0:
            raise AssertionError("even equality witness")
        if any(a != 1 for p, a in factors(n) if p != 2):
            raise AssertionError("repeated Fermat prime equality witness")
    return {
        "n": n, "C": C,
        "odd_part": u, "odd_d_product": odd_d_product,
        "large_fermat_factors": tuple(fermat_large),
        "large_nonfermat_factors": tuple(non_fermat_large),
        "small_odd_exponent_patterns": tuple(small_odd),
        "claim_boundary": "NECESSARY_SHAPE_ONLY__ORIGINAL_249_OPEN",
    }


def fermat_equality_criterion(n: int) -> bool:
    """Independent factorization criterion from Zhao's known C=0 theorem.

    No inference that currently unknown Fermat numbers are prime.
    """
    if n < 1:
        raise ValueError("positive integer required")
    if n % 2 == 0:
        return False
    for p, exponent in factors(n):
        if exponent != 1 or p == 2:
            return False
        r = v2(p - 1)
        if r < 1 or ((p - 1) >> r) != 1 or (r & (r - 1)):
            return False
    return True


def polylog_research_receipt(X: int, C: int) -> dict[str, object]:
    """Finite exact cross-checks; the asymptotic is established by proof."""
    if X < 2 or C < 0 or C > 8:
        raise ValueError("finite receipt requires X>=2, 0<=C<=8")
    phi = totients(3 * X)
    near = nearmax_witnesses(X, C, phi)
    bound = polylog_fermat_envelope(X, C)
    if len(near) > bound:
        raise AssertionError("new upper bound falsified")
    if C == 0:
        if any(is_nearmax(n, 0, phi) != fermat_equality_criterion(n)
               for n in range(1, X + 1)):
            raise AssertionError("Zhao equality criterion falsified")
    for n in near:
        fermat_prime_shape_check(n, C, phi)
    L = X.bit_length() - 1 - C
    adjacent = ()
    if L >= 1 and L <= X:
        _, adjacent = nearlog_integral_sums_and_adjacent_pairs(X, C, phi)
        relevant = set(nearmax_witnesses(3 * X, C + 2, phi))
        if any(N+L+1 not in relevant for N in adjacent):
            raise AssertionError("nearmax adjacent endpoint implication")
        if len(adjacent) > polylog_fermat_envelope(3*X, C+2):
            raise AssertionError("nearlog adjacent polylog upper bound")
    return {
        "X": X, "C": C, "eligible_count": len(near),
        "exact_polylog_envelope": str(bound),
        "adjacent_integral_pairs": len(adjacent),
        "full_series_status": "OPEN",
        "claim_boundary": "FINITE_CHECK_ONLY__EXACT_MANUSCRIPT_PROOF__NOT_MATHCERT",
    }
