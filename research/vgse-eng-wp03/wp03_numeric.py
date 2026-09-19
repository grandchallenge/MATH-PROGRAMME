from wp03_core import *

def forward_response(theta: np.ndarray, polys: dict[str, sp.Expr]) -> np.ndarray:
    x_syms = sp.symbols("x1:9", positive=True)
    values = {x_syms[i]: float(math.exp(theta[i])) for i in range(8)}
    ref = float(polys[REFERENCE].subs(values))
    out = []
    for name in RESPONSE_ORDER:
        y = float(polys[name].subs(values)) / ref
        out.append(math.log(y))
    return np.array(out, dtype=float)


def recover_theta(log_response: np.ndarray) -> np.ndarray:
    if log_response.shape != (18,):
        raise ValueError("expected 18 log-response coordinates")
    y = {name: math.exp(float(log_response[i])) for i, name in enumerate(RESPONSE_ORDER)}
    extracted = extractor_from_y(y)
    return np.log(np.array(extracted, dtype=float))


def classify_target(log_response: np.ndarray, polys: dict[str, sp.Expr]) -> dict[str, Any]:
    theta = recover_theta(log_response)
    replay = forward_response(theta, polys)
    residual = log_response - replay
    max_abs = float(np.max(np.abs(residual)))
    if max_abs <= FEASIBLE_TOL:
        status = "feasible"
    elif max_abs >= INCONSISTENT_TOL:
        status = "inconsistent"
    else:
        status = "numerically_ambiguous"
    worst = RESPONSE_ORDER[int(np.argmax(np.abs(residual)))]
    return {
        "status": status,
        "max_abs_log_response_residual": max_abs,
        "worst_coordinate": worst,
        "recovered_theta": [float(v) for v in theta],
        "residual_by_coordinate": {name: float(residual[i]) for i, name in enumerate(RESPONSE_ORDER)},
    }

