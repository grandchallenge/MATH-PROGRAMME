from wp03_core import *
from wp03_exact import exact_certificate
from wp03_numeric import forward_response, recover_theta, classify_target

def build_results() -> dict[str, Any]:
    model = load_model()
    polys, _ = minor_polynomials(model)
    exact = exact_certificate(model)

    # Protected baseline quotient coordinates from WP02's inverse laws.
    target = {name: float(value) for name, value in model["qualified_exact_representative"]["target_plucker"].items()}
    baseline_log_response = np.array(
        [math.log(target[name] / target[REFERENCE]) for name in RESPONSE_ORDER], dtype=float
    )
    baseline_theta = recover_theta(baseline_log_response)

    feasible_delta = np.array([0.31,-0.27,0.19,-0.33,0.24,-0.15,0.28,-0.21], dtype=float)
    feasible_theta = baseline_theta + feasible_delta
    feasible_target = forward_response(feasible_theta, polys)
    feasible_check = classify_target(feasible_target, polys)
    feasible_theta_error = float(np.max(np.abs(np.array(feasible_check["recovered_theta"]) - feasible_theta)))

    adversarial = {}
    extractor_indices = {name: RESPONSE_ORDER.index(name) for name in EXTRACTOR_COORDS}
    for dep in DEPENDENT_COORDS:
        probe = baseline_log_response.copy()
        probe[RESPONSE_ORDER.index(dep)] += PROBE_DELTA
        check = classify_target(probe, polys)
        recovered = np.array(check["recovered_theta"])
        adversarial[dep] = {
            "status": check["status"],
            "max_abs_log_response_residual": check["max_abs_log_response_residual"],
            "worst_coordinate": check["worst_coordinate"],
            "max_abs_recovered_theta_change": float(np.max(np.abs(recovered - baseline_theta))),
            "extractor_coordinates_unchanged": all(
                probe[index] == baseline_log_response[index] for index in extractor_indices.values()
            ),
        }

    ambiguous_probe = baseline_log_response.copy()
    ambiguous_probe[RESPONSE_ORDER.index("125")] += AMBIGUOUS_DELTA
    ambiguous_check = classify_target(ambiguous_probe, polys)

    # Extractor-preserving retraction P(F)=F(recover_theta(F)).
    off_image = baseline_log_response.copy()
    off_image[RESPONSE_ORDER.index("256")] += PROBE_DELTA
    theta_off = recover_theta(off_image)
    retracted = forward_response(theta_off, polys)
    twice = forward_response(recover_theta(retracted), polys)
    extractor_preservation_error = max(
        abs(retracted[RESPONSE_ORDER.index(name)] - off_image[RESPONSE_ORDER.index(name)])
        for name in EXTRACTOR_COORDS
    )
    idempotence_error = float(np.max(np.abs(twice - retracted)))

    if feasible_check["status"] != "feasible":
        raise AssertionError("synthetic feasible target was rejected")
    if feasible_theta_error > 1e-12:
        raise AssertionError("feasible target recovery error too large")
    if any(item["status"] != "inconsistent" for item in adversarial.values()):
        raise AssertionError("an adversarial dependent-coordinate probe was not rejected")
    if ambiguous_check["status"] != "numerically_ambiguous":
        raise AssertionError("ambiguity band is not exercised")
    if extractor_preservation_error > 1e-12 or idempotence_error > 1e-12:
        raise AssertionError("extractor-preserving retraction failed")

    return {
        "schema_version": "1.0.0",
        "work_package": "VGSE-ENG-WP03",
        "evidence_binding": {
            "protected_wp02_merge": "52e2e3df6ac54ab63a03c867b2b82a80d93ee577",
            "reviewed_wp02_head": "229d5549689fde9d5397ed59f92890e8ba080c75",
            "current_protected_base_at_wp03_activation": "7c8b351cc74bcb6ac2ccd4009eb6dff99913bc19",
        },
        "exact_feasibility_certificate": {
            **exact,
            "extractor_coordinates": EXTRACTOR_COORDS,
            "dependent_coordinates": DEPENDENT_COORDS,
            "normalized_measurement_definition": "y_I = Delta_I / Delta_124 > 0",
            "relations": RELATION_TEXT,
            "completeness": "necessary_and_sufficient_on_positive_chart",
            "global_graph_statement": "Every positive feasible response is uniquely determined by the eight extractor coordinates; conversely every positive extractor tuple induces one feasible eighteen-coordinate response through the admitted matching polynomials.",
        },
        "deterministic_target_checker": {
            "coordinate_system": "eighteen log-projective responses F_I=log(y_I)",
            "feasible_tolerance": FEASIBLE_TOL,
            "inconsistent_tolerance": INCONSISTENT_TOL,
            "statuses": ["feasible", "numerically_ambiguous", "inconsistent"],
            "feasible_probe": {
                "log_coordinate_delta": [float(v) for v in feasible_delta],
                "status": feasible_check["status"],
                "max_abs_parameter_recovery_error": feasible_theta_error,
                "max_abs_log_response_residual": feasible_check["max_abs_log_response_residual"],
            },
            "adversarial_single_dependent_coordinate_probes": adversarial,
            "ambiguous_probe": {
                "coordinate": "125",
                "log_response_delta": AMBIGUOUS_DELTA,
                "status": ambiguous_check["status"],
                "max_abs_log_response_residual": ambiguous_check["max_abs_log_response_residual"],
            },
        },
        "retraction": {
            "definition": "P(F)=F(recover_theta(F)); the eight extractor coordinates are held fixed and the ten dependent coordinates are replayed from the admitted response map",
            "extractor_preservation_max_abs_error": float(extractor_preservation_error),
            "idempotence_max_abs_error": idempotence_error,
            "nearest_point_claim": "not established",
            "limitation": "This is a canonical extractor-preserving feasibility retraction, not a proof of the nearest feasible response under an unconstrained eighteen-dimensional Euclidean or application-specific norm.",
        },
        "claim_boundary": {
            "source_correspondence_c06": "not established",
            "geometry_coupling": "not established",
            "physical_stiffness_interpretation": "not established",
            "mechanical_advantage": "not established",
            "rigid_foldability": "not established",
            "collision_freedom": "not established",
            "finite_thickness": "not established",
            "manufacturability": "not established",
            "durability_fatigue": "not established",
            "product_performance": "not established",
            "novelty_priority_patentability_commercial_value": "not established",
        },
    }

