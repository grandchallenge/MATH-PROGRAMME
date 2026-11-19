"""Erdos #249 WP08-A: exact over-logarithmic finite-tail phase separation.

All numerical operations use exact integers and Fraction. The mathematical
positive-density theorem is proved in OVERLOG_PHASE_SEPARATION_008.md, not
by assuming a finite experiment establishes an asymptotic.

Original infinite Euler-totient binary-series irrationality remains OPEN.
"""
from fractions import Fraction
from math import gcd, isqrt


def totients(limit: int) -> list[int]:
    if limit < 1:
        raise ValueError("positive sieve limit required")
    values = list(range(limit + 1))
    for p in range(2, limit + 1):
        if values[p] == p:
            for n in range(p, limit + 1, p):
                values[n] -= values[n] // p
    return values


def direct_totient(n: int) -> int:
    if n < 1:
        raise ValueError("positive n required")
    return sum(gcd(n, j) == 1 for j in range(1, n + 1))


def overlog_depth(X: int) -> int:
    if X < 64:
        raise ValueError("X>=64 required for uniform 3X endpoint")
    return X.bit_length() + 3  # floor(log2 X)+4


def centered(n: int, modulus: int) -> int:
    if modulus < 2 or modulus & (modulus - 1):
        raise ValueError("positive 2-power modulus>=2 required")
    return (n + modulus // 2) % modulus - modulus // 2


def finite_numerator(N: int, L: int, coeffs: list[int]) -> int:
    if N < 1 or L < 1 or N + L >= len(coeffs):
        raise ValueError("invalid N, L or source length")
    return sum(coeffs[N+j] << (L-j) for j in range(1, L+1))


def rolling_numerators(X: int, coeffs: list[int]) -> tuple[int, ...]:
    """Return all A_N for N in [X,2X] (extra last endpoint for checks)."""
    L = overlog_depth(X)
    Q = 1 << L
    if len(coeffs) <= 2*X + L:
        raise ValueError("source too short")
    a = finite_numerator(X, L, coeffs)
    results = [a]
    for N in range(X, 2*X):
        a = 2*a - Q*coeffs[N+1] + coeffs[N+L+1]
        results.append(a)
    return tuple(results)


def rational_baseline_half(limit: int) -> list[int]:
    if limit < 1:
        raise ValueError("limit>=1")
    return [n//2 for n in range(limit+1)]


def rational_baseline_three_quarters(limit: int) -> list[int]:
    if limit < 1:
        raise ValueError("limit>=1")
    return [(3*n)//4 for n in range(limit+1)]


def rational_six_defect(limit: int) -> list[int]:
    if limit < 1:
        raise ValueError("limit>=1")
    return [(n//2 - n//6 if n%6==0 else n//2)
            for n in range(limit+1)]


def rational_sum_half() -> Fraction:
    return Fraction(2,3)


def rational_sum_three_quarters() -> Fraction:
    return Fraction(14,15)


def rational_sum_six_defect() -> Fraction:
    return Fraction(2582,3969)


def exact_phase_gaps(X: int) -> dict[str, object]:
    """Compute direct integer phase events for totient and rational controls.

    Records exact integer numerator thresholds, never floating phase error.
    No empirical result is used as a proof of a density theorem.
    """
    L = overlog_depth(X)
    Q = 1 << L
    phi = totients(2*X + L + 1)
    half = rational_baseline_half(2*X + L + 1)
    three = rational_baseline_three_quarters(2*X + L + 1)
    six = rational_six_defect(2*X + L + 1)
    p = rolling_numerators(X, phi)
    h = rolling_numerators(X, half)
    t = rolling_numerators(X, three)
    s = rolling_numerators(X, six)

    # A: intrinsic phi-phase gap >= X/(6Q).
    good_phi = tuple(
        N for N in range(X, 2*X)
        if 6 * abs(centered(p[N-X], Q)) >= X
    )
    # B: totient versus half baseline gap >= X/(18Q).
    good_delta = tuple(
        N for N in range(X, 2*X)
        if 18 * abs(centered(p[N-X]-h[N-X], Q)) >= X
    )
    # R1 and R2: exact rational models satisfy equivalent criteria.
    good_three = tuple(
        N for N in range(X, 2*X)
        if 6 * abs(centered(t[N-X], Q)) >= X
    )
    good_six = tuple(
        N for N in range(X, 2*X)
        if 18 * abs(centered(s[N-X]-h[N-X], Q)) >= X
    )

    good_endpoint_indices = tuple(
        n for n in range(X+L+1,2*X+L)
        if 2*phi[n] >= n
    )
    multiples_six = tuple(
        n for n in range(X+L+1,2*X+L)
        if n%6==0
    )
    return {
        "X": X, "L": L, "Q": Q,
        "totient_intrinsic_phase_gap_starts": good_phi,
        "totient_vs_half_phase_gap_starts": good_delta,
        "rational_three_quarters_phase_gap_starts": good_three,
        "rational_six_defect_phase_gap_starts": good_six,
        "high_ratio_endpoint_indices": good_endpoint_indices,
        "multiple_six_endpoint_indices": multiples_six,
        "full_totient_irrationality": "OPEN",
        "proof_status": "ELEMENTARY_MANUSCRIPT__FINITE_EXACT_CHECKS_ONLY",
    }


def adjacent_phase_rigidity(X: int,
                            target: list[int],
                            comparator: list[int]) -> dict[str, object]:
    """Verify exact two-start phase rigidity for the given source block.

    For each N with both finite fractions identical mod 1, check that
    coefficient at n=N+L+1 must match. This is a deterministic witness
    check, not a proof of the all-X theorem.
    """
    L = overlog_depth(X)
    Q = 1 << L
    if len(target) <= 2*X+L or len(comparator) <= 2*X+L:
        raise ValueError("source too short")
    if any(not(0 <= seq[n] <= n)
           for seq in (target,comparator)
           for n in range(X+1,2*X+L+1)):
        raise ValueError("sequences must lie in [0,n] in this block")
    A=rolling_numerators(X,target)
    B=rolling_numerators(X,comparator)
    paired, violations = [], []
    for N in range(X,2*X-1):
        if (A[N-X]-B[N-X])%Q==0 and (A[N-X+1]-B[N-X+1])%Q==0:
            paired.append(N)
            if target[N+L+1]!=comparator[N+L+1]:
                violations.append(N)
    if violations:
        raise AssertionError("overlogarithmic exact rigidity falsified")
    return {
        "X": X, "L": L, "pairs_with_equal_finite_phases": len(paired),
        "rigidity_violations": len(violations),
        "conjecture_status": "OPEN",
    }



def canonical_prime_set(primes: tuple[int, ...]) -> tuple[int, ...]:
    """Reject malformed finite Euler support (no silent deduplication)."""
    if len(set(primes)) != len(primes):
        raise ValueError("prime support must have distinct members")
    for p in primes:
        if p < 2 or any(p % k == 0 for k in range(2, isqrt(p)+1)):
            raise ValueError("prime support must contain only primes")
    return tuple(sorted(primes))


def prime_euler_coefficients(limit: int,
                             primes: tuple[int, ...]) -> list[int]:
    """g_P(n)=n * prod_{p|n,p in P}(1-1/p), as exact integers."""
    if limit < 1:
        raise ValueError("positive limit required")
    ps=canonical_prime_set(primes)
    values=[]
    for n in range(limit+1):
        if n==0:
            values.append(0)
            continue
        v=n
        for p in ps:
            if n%p==0:
                if v%p!=0:
                    raise AssertionError("internal Euler factor calculation")
                v=(v//p)*(p-1)
        values.append(v)
    return values


def finite_prime_weight(primes: tuple[int, ...]) -> Fraction:
    ps=canonical_prime_set(primes)
    w=Fraction(1)
    for p in ps:
        w*=Fraction(p-1,p)
    return w


def finite_prime_rational_sum(primes: tuple[int, ...]) -> Fraction:
    """Exact finite Möbius formula Σ_{d|prod(P)} μ(d) 2^d/(2^d-1)^2."""
    ps=canonical_prime_set(primes)
    product=1
    for p in ps:
        product*=p
        if product>512:
            raise ValueError("finite exact evaluator limited to prime product <=512")
    terms=[(1,1)]
    for p in ps:
        terms += [(d*p,-sign) for d,sign in tuple(terms)]
    return sum((sign*Fraction(1<<d,((1<<d)-1)**2)
                for d,sign in terms),Fraction())


def prime_escape_phase_gaps(
    X: int, primes: tuple[int, ...], escape_prime: int
) -> dict[str, object]:
    """Finite integer check of Theorem D (prime not included in P)."""
    ps=canonical_prime_set(primes)
    if escape_prime in ps or escape_prime < 2:
        raise ValueError("escape prime must be omitted")
    if any(escape_prime%k==0
           for k in range(2,isqrt(escape_prime)+1)):
        raise ValueError("escape prime must be prime")
    L=overlog_depth(X)
    Q=1<<L
    w=finite_prime_weight(ps)
    phi=totients(2*X+L+1)
    gp=prime_euler_coefficients(2*X+L+1,ps)
    A=rolling_numerators(X,phi)
    B=rolling_numerators(X,gp)
    affected=tuple(
        n for n in range(X+L+1,2*X+L)
        if n%escape_prime==0
    )
    good=set(
        N for N in range(X,2*X)
        if 48*escape_prime*w.denominator*
        abs(centered(A[N-X]-B[N-X],Q)) >= w.numerator*Q
    )
    for n in affected:
        N=n-L-1
        if N not in good and N+1 not in good:
            raise AssertionError("prime escape local phase bound falsified")
        if escape_prime*(gp[n]-phi[n])*w.denominator < w.numerator*n:
            raise AssertionError("missing-prime Euler factor inequality falsified")
    if len(good) < len(affected):
        raise AssertionError("disjoint-pair prime escape count falsified")
    return {
        "X": X, "L":L, "prime_support":ps,
        "omitted_prime":escape_prime,
        "support_weight":str(w),
        "rational_full_sum":str(finite_prime_rational_sum(ps)),
        "omitted_prime_endpoints":len(affected),
        "phase_separated_starts":len(good),
        "all_prime_escape_implications":True,
        "actual_full_totient_sum_status":"OPEN",
    }
