from __future__ import annotations
from fractions import Fraction as Q
from math import factorial
import t3_003_target as target

def cumulant_pochhammer(length: int, offset: int, order: int) -> Q:
    if length < 0 or offset < 0 or order < 1:
        raise ValueError("invalid lift indices")
    return Q((-1) ** (order - 1) * factorial(order - 1)) * (
        target.H(offset + length, order) - target.H(offset, order)
    )

def letter_from_cumulant(value: Q, order: int) -> Q:
    return Q((-1) ** (order - 1), factorial(order - 1)) * value

def H(m: int, r: int) -> Q:
    return letter_from_cumulant(cumulant_pochhammer(m, 0, r), r)

def A(n: int, x: int, r: int) -> Q:
    return letter_from_cumulant(cumulant_pochhammer(n, x, r), r)

def B(n: int, x: int, r: int) -> Q:
    left = cumulant_pochhammer(n - x, 0, r)
    right = cumulant_pochhammer(x, 0, r)
    return letter_from_cumulant(left - right, r)

def C(n: int, k: int, l: int, r: int) -> Q:
    return letter_from_cumulant(cumulant_pochhammer(n, k + l, r), r)

def ES(x: int, r: int, m: int) -> Q:
    return sum((H(t, m) / Q(t ** r) for t in range(1, x + 1)), Q(0))

def U(a: int, b: int, r: int, m: int) -> Q:
    return sum((H(t + b, m) / Q(t ** r) for t in range(1, a + 1)), Q(0))

def L(n: int, k: int, l: int, x: int) -> Q:
    return -A(n, x, 1) - C(n, k, l, 1) - 2 * B(n, x, 1)

def r11(k: int, l: int) -> Q:
    return ((H(k + l, 1) - H(k, 1) - H(l, 1)) * (H(k, 2) + H(l, 2))
            - H(k, 3) - H(l, 3) + U(k, l, 1, 2) + U(l, k, 1, 2))

def r12(k: int, l: int) -> Q:
    return (-2 * (H(k, 1) + H(l, 1) - H(k + l, 1)) * H(l, 3)
            + H(k, 2) * H(k + l, 2) - H(l, 2) ** 2 / 2
            + H(k + l, 2) * H(l, 2) - Q(5, 2) * H(l, 4)
            + 2 * ES(l, 1, 3) - U(k, l, 2, 2))

def r22(k: int, l: int) -> Q:
    return (-2 * (H(k, 2) + H(l, 2)) * (H(k, 3) + H(l, 3))
            + 2 * H(k + l, 3) * (H(k, 2) + H(l, 2))
            + 2 * H(k + l, 2) * (H(k, 3) + H(l, 3))
            - 2 * H(k, 5) - 2 * H(l, 5)
            - 6 * ES(k, 1, 4) - 6 * ES(l, 1, 4)
            - 2 * ES(k, 2, 3) - 2 * ES(l, 2, 3)
            + 6 * U(k, l, 1, 4) + 6 * U(l, k, 1, 4)
            + 2 * U(k, l, 2, 3) + 2 * U(l, k, 2, 3))

def W1(n: int, k: int, l: int) -> Q:
    lk=L(n,k,l,k); ll=L(n,k,l,l)
    return r22(k,l)+lk*r12(k,l)+ll*r12(l,k)+(lk*ll-C(n,k,l,2))*r11(k,l)

def w5(n: int, k: int, l: int) -> Q:
    alpha=A(n,k,1)-A(n,l,1)
    beta=B(n,k,1)-B(n,l,1)
    psi=alpha/2+beta
    cc=(A(n,k,2)+A(n,l,2))/4-alpha*psi/2
    return H(n+k,5)+(alpha-beta)*H(n+k,4)/2+cc*H(n+k,3)

def w5sym(n: int, k: int, l: int) -> Q:
    return (w5(n,k,l)+w5(n,l,k))/2

def cell(n: int, k: int, l: int) -> Q:
    return Q(target.T(n,k,l))*(W1(n,k,l)+2*w5sym(n,k,l))
