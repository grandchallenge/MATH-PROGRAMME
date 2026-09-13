from __future__ import annotations

import hashlib
import json

from sympy import Rational, cancel, expand, symbols
from sympy.concrete.gosper import gosper_sum

N, K, L, Z = symbols("n k l _z")
PINV_TAG = 991337
SCALARS = ("TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK")
SCALAR_CHANNEL = {
    "TN1": "n1", "TN2": "n2", "TN3": "n3",
    "SK": "k1", "AK": "k1", "LKK": "k1", "LLK": "k1",
}
CHANNEL_ACTIVE = {"n1": (N, 1), "n2": (N, 2), "n3": (N, 3), "k1": (K, 1)}
MODULE_SHA256 = "cdabf6d7873f3aa8e9d53b39fd7b15341dbee58ce9684911d015aee9aaae04da"


def _sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    ).hexdigest()


def _factor_expr_strict_interior(factor):
    values = tuple(map(int, factor))
    if len(values) == 5 and values[0] == PINV_TAG:
        _, a, b, c, d = values
        return a*N + b*K + c*L + d
    if len(values) == 4:
        a, b, c, d = values
        return a*N + b*K + c*L + d
    raise AssertionError(f"unsupported protected rational factor: {values!r}")


def rat_expr_strict_interior(rows):
    """Interpret the protected coefficient serialization on the strict interior.

    The five-entry PINV_TAG encoding is the protected positive-reciprocal
    convention. On the strict interior its affine argument is positive, so it
    equals the corresponding ordinary Laurent factor. This conversion is not a
    global shell identity; every positive candidate still requires separate
    pole-free shell replay.
    """
    out = 0
    for num, den, factors in rows:
        term = Rational(int(num), int(den))
        for factor, exponent in factors:
            term *= _factor_expr_strict_interior(factor) ** int(exponent)
        out += term
    return cancel(out)


def tagged_factor_census(module):
    unique = set()
    occurrences = 0

    def visit(rows):
        nonlocal occurrences
        for _num, _den, factors in rows:
            for factor, _exponent in factors:
                values = tuple(map(int, factor))
                if len(values) == 5:
                    if values[0] != PINV_TAG:
                        raise AssertionError(f"unknown five-entry protected factor: {values!r}")
                    unique.add(values)
                    occurrences += 1
                elif len(values) != 4:
                    raise AssertionError(f"unsupported protected factor arity: {values!r}")

    for row in module["target_records"]:
        visit(row["coefficient"])
    for generator in module["generators"]:
        visit(generator["base_term"]["coefficient"])
        for term in generator["shifted_terms"]:
            visit(term["coefficient"])
    return {
        "tagged_positive_reciprocal_occurrences": occurrences,
        "tagged_positive_reciprocal_factors": [list(x) for x in sorted(unique)],
        "tagged_positive_reciprocal_factor_count": len(unique),
    }


def expr_json(expr):
    num, den = cancel(expr).as_numer_denom()
    return {"numerator": str(expand(num)), "denominator": str(expand(den))}


def shift(expr, delta):
    dn, dk, dl = map(int, delta)
    return cancel(expr.subs({N: N+dn, K: K+dk, L: L+dl}, simultaneous=True))


def antidifference(f, active, step):
    f = cancel(f)
    if f == 0:
        return 0
    scaled = cancel(f.subs(active, step*Z))
    qz = gosper_sum(scaled, Z)
    if qz is None:
        return None
    q = cancel(qz.subs(Z, active/Rational(step)))
    if cancel(q.subs(active, active+step) - q - f) != 0:
        raise AssertionError("Gosper candidate failed exact rational replay")
    return q


def apply_strict_interior(residual, generator, q):
    mon = tuple(generator["support_monomial"])
    qshift = shift(q, generator["shift"])
    residual[mon] = cancel(residual.get(mon, 0) + q)
    for term in generator["shifted_terms"]:
        dst = tuple(term["monomial"])
        residual[dst] = cancel(
            residual.get(dst, 0)
            - rat_expr_strict_interior(term["coefficient"]) * qshift
        )


def _blocked(reason, census, certificate, **fields):
    return {
        "status": "STRICT_INTERIOR_SCALAR_SEPARATED_ROUTE_BLOCKED",
        "reason": reason,
        **fields,
        **census,
        "interior_exact_scalarwise_replay": False,
        "shell_replay_required": True,
        "global_certificate_constructed": False,
        "prefix_certificate_sha256": _sha(certificate),
        "solved_generator_count": len(certificate),
        "class_nonexistence_proved": False,
    }


def probe(module):
    if module["hypothesis_class"] != "SOURCE_DECLARED_RATIONAL_DELTA_COEFFICIENT_CLASS_001":
        raise AssertionError("hypothesis-class drift")
    census = tagged_factor_census(module)
    if census["tagged_positive_reciprocal_factor_count"] == 0:
        raise AssertionError("protected pole-free factor grammar unexpectedly absent")

    support = {scalar: {} for scalar in SCALARS}
    for g in module["generators"]:
        scalar = g["scalar"]
        mon = tuple(g["support_monomial"])
        if g["channel"] != SCALAR_CHANNEL[scalar]:
            raise AssertionError("scalar/channel drift")
        if mon in support[scalar]:
            raise AssertionError("duplicate scalar/support generator")
        same = [t for t in g["shifted_terms"] if tuple(t["monomial"]) == mon]
        if (
            len(same) != 1
            or cancel(rat_expr_strict_interior(same[0]["coefficient"]) - 1) != 0
        ):
            raise AssertionError("unit diagonal shift drift")
        if any(
            tuple(t["monomial"]) != mon
            and len(tuple(t["monomial"])) >= len(mon)
            for t in g["shifted_terms"]
        ):
            raise AssertionError("non-lowering shift term")
        support[scalar][mon] = g

    target = {scalar: {} for scalar in SCALARS}
    for row in module["target_records"]:
        scalar = row["scalar"]
        mon = tuple(row["monomial"])
        target[scalar][mon] = cancel(
            target[scalar].get(mon, 0)
            + rat_expr_strict_interior(row["coefficient"])
        )

    coords = sorted(
        {tuple(mon) for mon in module["coordinate_monomials"]},
        key=lambda mon: (-len(mon), repr(mon)),
    )
    certificate = []
    solved_by_scalar = {}

    for scalar in SCALARS:
        residual = dict(target[scalar])
        solved = 0
        for mon in coords:
            f = cancel(residual.get(mon, 0))
            g = support[scalar].get(mon)
            if g is None:
                if f != 0:
                    return _blocked(
                        "UNSUPPORTED_TRIANGULAR_COORDINATE",
                        census,
                        certificate,
                        scalar=scalar,
                        monomial=list(mon),
                        residual=expr_json(f),
                    )
                continue
            active, step = CHANNEL_ACTIVE[g["channel"]]
            q = antidifference(f, active, step)
            if q is None:
                return _blocked(
                    "UNIVARIATE_RATIONAL_ANTIDIFFERENCE_ABSENT",
                    census,
                    certificate,
                    scalar=scalar,
                    channel=g["channel"],
                    generator_index=g["index"],
                    monomial=list(mon),
                    residual=expr_json(f),
                )
            certificate.append({
                "generator_index": g["index"],
                "scalar": scalar,
                "channel": g["channel"],
                "support_monomial": list(mon),
                "coefficient": expr_json(q),
            })
            solved += 1
            apply_strict_interior(residual, g, q)
            if cancel(residual.get(mon, 0)) != 0:
                raise AssertionError("triangular pivot failed to clear")
        if any(cancel(value) != 0 for value in residual.values()):
            raise AssertionError("unexpected terminal scalar residual")
        solved_by_scalar[scalar] = solved

    return {
        "status": "STRICT_INTERIOR_SCALAR_SEPARATED_RATIONAL_CERTIFICATE_CANDIDATE",
        "module_sha256": MODULE_SHA256,
        "certificate": certificate,
        "certificate_sha256": _sha(certificate),
        "certificate_generator_count": len(certificate),
        "solved_by_scalar": solved_by_scalar,
        **census,
        "interior_exact_scalarwise_replay": True,
        "shell_replay_required": True,
        "global_certificate_constructed": False,
        "class_nonexistence_proved": False,
    }


def compact(result):
    keys = [
        "status", "reason", "scalar", "channel", "generator_index", "monomial",
        "module_sha256", "certificate_sha256", "certificate_generator_count",
        "prefix_certificate_sha256", "solved_generator_count", "solved_by_scalar",
        "tagged_positive_reciprocal_occurrences",
        "tagged_positive_reciprocal_factor_count",
        "tagged_positive_reciprocal_factors",
        "interior_exact_scalarwise_replay", "shell_replay_required",
        "global_certificate_constructed", "class_nonexistence_proved",
    ]
    return {key: result[key] for key in keys if key in result}
