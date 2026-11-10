"""Exact finite controls for 147; no analytic or liquid-category certification."""
from fractions import Fraction as Q
from math import factorial


def add(*polys):
    result = {}
    for poly in polys:
        for key, value in poly.items():
            result[key] = result.get(key, Q(0)) + value
    return {key: value for key, value in result.items() if value}


def scale(c, poly):
    return {key: Q(c) * value for key, value in poly.items() if c * value}


def mul(a, b):
    result = {}
    for (t, u), c in a.items():
        for (v, w), d in b.items():
            key = (t + v, u + w)
            result[key] = result.get(key, Q(0)) + c * d
    return {key: value for key, value in result.items() if value}


def monomial(t, u, c=1):
    return {(t, u): Q(c)} if c else {}


def reflect(poly):
    return {key: value * (-1) ** key[1] for key, value in poly.items()}


def remainder(poly, divisor):
    value = dict(poly)
    while value and max(u for t, u in value) >= 2:
        degree = max(u for t, u in value)
        terms = [(t, c) for (t, u), c in value.items() if u == degree]
        for t, c in terms:
            value = add(value, scale(-1, mul(monomial(t, degree - 2, c), divisor)))
    return value


def detector(poly, index):
    """Return a formal linear combination of center moments of one coefficient."""
    output = {}
    for (t, u), coefficient in poly.items():
        requests = []
        if index < 3 and u == 0:
            requests.append((index, Q(1)))
        if index == 2 and u == 2:
            requests.append((0, Q(-1, 2)))
        if index == 3 and u == 1:
            requests.append((0, Q(1)))
        for moment, factor in requests:
            if t <= moment:
                power = moment - t
                c = coefficient * factor * (-1) ** t
                c *= Q(factorial(moment), factorial(power))
                output[power] = output.get(power, Q(0)) + c
    return {key: value for key, value in output.items() if value}


def main():
    f = add(monomial(0, 2), monomial(1, 1, -1), monomial(2, 0, Q(1, 4)))
    g = reflect(f)
    assert add(g, scale(-1, f)) == monomial(1, 1, 2)
    assert add(mul(f, scale(-1, g)), mul(g, f)) == {}
    assert remainder(g, f) == monomial(1, 1, 2)
    assert remainder(mul(g, monomial(0, 1)), f) == add(
        monomial(3, 0, Q(-1, 2)), monomial(2, 1, 2)
    )
    assert reflect(g) == f
    controls = 5
    for t in range(5):
        for u in range(9):
            term = monomial(t, u)
            for operator in (f, g):
                for index in range(4):
                    assert detector(mul(operator, term), index) == {}
                    controls += 1
            for index in range(4):
                sign = 1 if index < 3 else -1
                assert detector(reflect(term), index) == {
                    key: sign * value for key, value in detector(term, index).items()
                }
                controls += 1
    assert detector(monomial(0, 2), 2) == {0: Q(-1, 2)}
    assert detector(monomial(2, 0, Q(-1, 4)), 2) == {0: Q(-1, 2)}
    assert all(detector(monomial(0, 4), i) == {} for i in range(4))
    print(f"PASS: {controls + 3} exact finite algebra controls; analytic claims untested")


if __name__ == "__main__":
    main()
