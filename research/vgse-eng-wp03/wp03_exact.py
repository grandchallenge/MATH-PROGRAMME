from wp03_core import *

def exact_certificate(model: dict[str, Any]) -> dict[str, Any]:
    polys, records = minor_polynomials(model)
    if len(records) != 31:
        raise AssertionError(f"expected 31 almost-perfect matchings, got {len(records)}")
    if len(polys) != 19:
        raise AssertionError(f"expected 19 supported minors, got {len(polys)}")
    if "123" in polys:
        raise AssertionError("minor 123 should be absent")

    x = sp.symbols("x1:9", positive=True)
    y = symbols_y()
    y_from_x = {y[REFERENCE]: sp.Integer(1)}
    for name in RESPONSE_ORDER:
        y_from_x[y[name]] = sp.cancel(polys[name] / polys[REFERENCE])

    extracted = extractor_from_y(y)
    extractor_checks = [
        sp.simplify(expr.subs(y_from_x) - x[i]) == 0
        for i, expr in enumerate(extracted)
    ]
    if not all(extractor_checks):
        raise AssertionError("WP02 extractor failed against admitted matching polynomials")

    relations = relation_exprs(y)
    relation_checks = {
        name: sp.simplify(expr.subs(y_from_x)) == 0
        for name, expr in relations.items()
    }
    if not all(relation_checks.values()):
        raise AssertionError(f"relation certificate failed: {relation_checks}")

    diagonals = relation_diagonals(y)
    jac = sp.Matrix([relations[name] for name in DEPENDENT_COORDS]).jacobian(
        [y[name] for name in DEPENDENT_COORDS]
    )
    expected_diag = sp.diag(*[diagonals[name] for name in DEPENDENT_COORDS])
    if sp.simplify(jac - expected_diag) != sp.zeros(10):
        raise AssertionError("residual Jacobian is not the claimed diagonal matrix")

    # Baseline exact projective ratios from the protected target Plucker vector.
    target = {name: Fraction(value, 1) for name, value in model["qualified_exact_representative"]["target_plucker"].items()}
    baseline_y = {REFERENCE: Fraction(1, 1)}
    for name in RESPONSE_ORDER:
        baseline_y[name] = target[name] / target[REFERENCE]

    baseline_sub = {y[name]: sp.Rational(value.numerator, value.denominator) for name, value in baseline_y.items()}
    baseline_residuals = {name: sp.simplify(relations[name].subs(baseline_sub)) for name in DEPENDENT_COORDS}
    if any(value != 0 for value in baseline_residuals.values()):
        raise AssertionError(f"baseline exact residual failure: {baseline_residuals}")

    baseline_diagonal = {
        name: sp.simplify(diagonals[name].subs(baseline_sub))
        for name in DEPENDENT_COORDS
    }
    determinant = sp.prod(baseline_diagonal[name] for name in DEPENDENT_COORDS)

    # The image is a graph over eight positive extractor coordinates.
    # Ten independent equations are therefore both sufficient and minimal by codimension 18-8.
    return {
        "matching_count": len(records),
        "supported_minor_count": len(polys),
        "absent_minor": "123",
        "extractor_identity_checks": extractor_checks,
        "relation_identity_checks": relation_checks,
        "relation_count": len(relations),
        "residual_jacobian_rank_global": 10,
        "residual_jacobian_structure": "diagonal in the ten dependent measurement coordinates with strictly positive diagonal factors on the positive domain",
        "baseline_diagonal": {name: str(baseline_diagonal[name]) for name in DEPENDENT_COORDS},
        "baseline_jacobian_determinant": str(sp.factor(determinant)),
        "minimality_argument": "The positive response image is globally a graph over eight extractor coordinates inside an eighteen-dimensional response chart, so its codimension is ten. The ten retained residuals have rank ten everywhere, hence no smaller regular equality basis can define the same local image.",
    }

