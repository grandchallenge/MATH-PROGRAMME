"""ERDOS-249-S-WP05: exact CRT witnesses for cofinal finite totient patterns.

Infinitude follows from classical Dirichlet, not from any finite search.
The original irrationality problem is OPEN; no result here certifies S.
"""
from fractions import Fraction
from math import gcd, isqrt


def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    return n % 2 != 0 and all(n % d for d in range(3, isqrt(n) + 1, 2))


def phi(n):
    if n < 1:
        raise ValueError("positive integer required")
    output, t = n, n
    d = 2
    while d * d <= t:
        if t % d == 0:
            output -= output // d
            while t % d == 0:
                t //= d
        d = 3 if d == 2 else d + 2
    if t > 1:
        output -= output // t
    return output


def v2(n):
    if n == 0:
        raise ValueError("undefined valuation at zero")
    return (abs(n) & -abs(n)).bit_length() - 1


def progression(offsets, power, base_modulus, base_residue):
    """CRT reduced progression with separate q_t = 1 (mod 2^power).

    Offset t means q_t divides p+t. A certified infinite prime family
    relies on Dirichlet's theorem for the resulting reduced progression.
    """
    offsets = tuple(sorted(set(offsets)))
    if not offsets or 0 in offsets or power < 2:
        raise ValueError("invalid nonzero offsets or power")
    if base_modulus < 4 or (base_modulus & (base_modulus - 1)):
        raise ValueError("base modulus must be a power of two >=4")
    if not (0 <= base_residue < base_modulus) or gcd(base_residue, base_modulus) != 1:
        raise ValueError("base residue must be a unit")
    r, modulus = base_residue, base_modulus
    max_offset = max(map(abs, offsets))
    step = 1 << power
    candidate = (max_offset // step + 1) * step + 1
    assignment = {}
    for offset in offsets:
        while not is_prime(candidate):
            candidate += step
        q = candidate
        assignment[offset] = q
        r += modulus * (((-offset - r) * pow(modulus, -1, q)) % q)
        modulus *= q
        r %= modulus
        candidate += step
    if gcd(r, modulus) != 1:
        raise AssertionError("CRT class is not reduced")
    return {"offset_primes": assignment, "residue": r, "modulus": modulus,
            "power": power, "base_modulus": base_modulus,
            "base_residue": base_residue}


def forward_family(shifts, depth, power):
    shifts = tuple(sorted(set(shifts)))
    if not shifts or min(shifts) < 1 or depth < 1 or power < 1:
        raise ValueError("positive finite shift family, depth, power required")
    offsets = set(range(1, depth + 1))
    for h in shifts:
        offsets.add(4 * h)
        offsets.update(4 * h + j for j in range(1, depth + 1))
    data = progression(offsets, max(2, power), 4, 3)
    data.update({"shifts": shifts, "depth": depth, "requested_power": power})
    return data


def backward_midpoint(shift, power):
    """Cook 2026 Prop. 6.92 antecedent; not a fresh theorem claim."""
    if shift <= power or power < 2:
        raise ValueError("requires H>K>=2")
    offsets = {shift}
    for j in range(1, power):
        offsets.add(-j)
        offsets.add(shift - j)
    data = progression(offsets, power, 1 << power, 1 + (1 << (power - 1)))
    data.update({"shift": shift, "depth": power})
    return data


def scan_prime(data, *, lower=0, max_steps=500):
    """A bounded finite witness search; failure is not a refutation of Dirichlet."""
    if max_steps < 1:
        raise ValueError("search bound must be positive")
    modulus, residue = data["modulus"], data["residue"]
    k = max(0, (lower - residue + modulus - 1) // modulus)
    for offset in range(max_steps):
        p = residue + (k + offset) * modulus
        if is_prime(p):
            return p
    raise LookupError("bounded search exhausted; infinitude not falsified")


def forward_receipt(data, p):
    if not is_prime(p) or p % 4 != 3:
        raise ValueError("p must be prime and 3 mod 4")
    for offset, q in data["offset_primes"].items():
        if (p + offset) % q or phi(p + offset) % (1 << data["power"]):
            raise AssertionError("totient witness fails")
    depth = data["depth"]
    values = {}
    for h in data["shifts"]:
        delta0 = phi(p + 4 * h) - phi(p)
        deltas = [phi(p + 4 * h + j) - phi(p + j)
                  for j in range(1, depth + 1)]
        numerator = sum(d * (1 << (depth - j))
                        for j, d in enumerate(deltas, 1))
        if delta0 % 4 != 2:
            raise AssertionError("mod-four pulse absent")
        if data["requested_power"] >= depth and numerator % (1 << depth):
            raise AssertionError("finite-front integrality absent")
        values[h] = {"delta0": delta0, "deltas": deltas,
                     "numerator": numerator, "residue": numerator % (1 << depth),
                     "finite_fraction": Fraction(numerator, 1 << depth),
                     "tail_error_upper": Fraction(p + 4 * h + depth + 2, 1 << depth)}
    return {"prime": p, "shift_values": values,
            "boundary": "FINITE_CONGRUENCE_ONLY__FULL_S_OPEN"}


def midpoint_receipt(data, p):
    H, K = data["shift"], data["depth"]
    if not is_prime(p) or p <= H + K:
        raise ValueError("prime larger than H+K required")
    if p % (1 << K) != 1 + (1 << (K - 1)):
        raise AssertionError("wrong prime residue")
    for offset, q in data["offset_primes"].items():
        if (p + offset) % q or phi(p + offset) % (1 << K):
            raise AssertionError("two-adic source witness fails")
    N = p - K
    delta = [phi(N + H + j) - phi(N + j) for j in range(1, K + 1)]
    d = sum(v * (1 << (K - j)) for j, v in enumerate(delta, 1))
    r = d % (1 << K)
    if r != 1 << (K - 1) or phi(p - 1) % (1 << K):
        raise AssertionError("Cook midpoint conditions drifted")
    if p - 1 < (1 << K) or not (p + 2 > (1 << K) - 1):
        raise AssertionError("same-depth obstruction failed")
    return {"prime": p, "start": N, "residue": r, "depth": K,
            "directed_lower_threshold": p + 2,
            "same_depth_certificate_passes": False,
            "boundary": "COOK_MIDPOINT_SAME_DEPTH_NO_GO__FULL_S_OPEN"}
