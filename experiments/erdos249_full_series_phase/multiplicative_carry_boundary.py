"""WP09-O exact rational prime truncation and cyclotomic denominator checks."""
from fractions import Fraction
from math import gcd, isqrt, prod


def _integer(n):
    return type(n) is int


def primes_through(y):
    if not _integer(y) or y < 2:
        raise ValueError("integer cutoff >=2 required")
    return tuple(p for p in range(2, y+1)
                 if all(p % d for d in range(2, isqrt(p)+1)))


def cutoff_coefficient(n, P):
    if not _integer(n) or n < 1:
        raise ValueError("positive integer index required")
    a = n
    for p in P:
        if n % p == 0:
            a = a // p * (p-1)
    return a


def signed_divisors(P):
    terms = [(1, 1)]
    for p in P:
        terms += [(p*d, -sign) for d, sign in terms]
    return tuple(sorted(terms))


def exact_cutoff_value(y):
    P = primes_through(y)
    M = prod(P)
    if M > 30030:
        raise ValueError("finite exact arithmetic resource bound exceeded")
    terms = signed_divisors(P)
    S = sum((Fraction(sign * (1 << d), ((1 << d)-1)**2)
             for d, sign in terms), Fraction())
    C = prod(((1 << d)-1 for d, sign in terms if sign == (-1)**len(P)))
    Cden = prod(((1 << d)-1 for d, sign in terms if sign != (-1)**len(P)))
    C, rem = divmod(C, Cden)
    if rem:
        raise AssertionError("noninteger cyclotomic product")
    primitive = C // gcd(C, M)
    if S.denominator % (primitive**2):
        raise AssertionError("primitive denominator divisor absent")
    return dict(P=P, M=M, value=S, cyclotomic=C, primitive=primitive,
                denominator_bits=S.denominator.bit_length())


def carry_trace(y, N):
    """Exact actual rational-tail carries/digits, no finite-tail approximation."""
    if not _integer(N) or N < 1 or N > 10000:
        raise ValueError("bounded positive trace length required")
    a = exact_cutoff_value(y)
    P = a["P"]
    tail = a["value"]
    c, d = [tail.numerator // tail.denominator], [None]
    for n in range(1, N+1):
        digit = int(2*(tail-c[-1]))
        tail = 2*tail-cutoff_coefficient(n, P)
        cn = tail.numerator // tail.denominator
        if not 0 <= tail <= n+2 or digit not in (0, 1):
            raise AssertionError("tail envelope or binary digit invalid")
        if cutoff_coefficient(n,P) != 2*c[-1]-cn+digit:
            raise AssertionError("carry identity failure")
        c.append(cn)
        d.append(digit)
    return c,d


def sparse_coefficient(n, P):
    if not _integer(n) or n < 1:
        raise ValueError("positive integer index required")
    r=n
    for p in P:
        while r % p == 0:
            r //= p
    return cutoff_coefficient(n, P) if r==1 else 0


def finite_support_coefficient(n, B):
    """Exact multiplicative finite support preserving prefix <=B and parity."""
    if not _integer(n) or not _integer(B) or min(n,B) < 1:
        raise ValueError("positive integer scope required")
    r, a = n, 1
    for p in range(2, isqrt(n)+1):
        if r % p == 0:
            pp=1
            while r % p == 0:
                pp *= p
                r //= p
            if pp > B:
                return 0
            a *= pp//p*(p-1)
    if r>1:
        if r>B:
            return 0
        a *= r-1
    return a
