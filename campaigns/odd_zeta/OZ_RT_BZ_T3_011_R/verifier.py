from pathlib import Path

_IMPL = Path(__file__).with_name("verifier_impl.py.inc")
exec(compile(_IMPL.read_text(encoding="utf-8"), str(_IMPL), "exec"), globals(), globals())

_BASE_VERIFY = verify


def _independent_all_zero_multiplier_audit() -> dict:
    primitive_full, strata, specialized, supports = ov.f.d.build_context()
    banks = ov.f._channel_banks(primitive_full, strata, specialized, supports)
    poly_cache = {}
    vector_cache = {}
    records = []
    first_nonzero = None

    for pair_index, pair in enumerate(producer.p.ADMITTED_PAIRS):
        left, right = pair
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            for candidate_index, uid in enumerate(bank["candidates"]):
                vec_g = kv._cached_vector_index(
                    endpoint, uid, (), strata, bank, poly_cache, vector_cache
                )[0]
                vec_gc = kv._cached_vector_index(
                    endpoint, uid, (left,), strata, bank, poly_cache, vector_cache
                )[0]
                vec_gd = kv._cached_vector_index(
                    endpoint, uid, (right,), strata, bank, poly_cache, vector_cache
                )[0]
                vec_gcd = kv._cached_vector_index(
                    endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache
                )[0]
                value = kv._direct_pairing(
                    bank["witness"], vec_gcd, vec_gc, vec_gd, vec_g
                )
                record = {
                    "pair_index": pair_index,
                    "endpoint_index": endpoint_index,
                    "candidate_index": candidate_index,
                    "pair": list(pair),
                    "endpoint": endpoint,
                    "candidate": producer.p.unknown_json(uid),
                    "pairing": producer.k.qjson(value),
                }
                records.append(record)
                if value != 0 and first_nonzero is None:
                    first_nonzero = dict(record)

    coverage_complete = len(records) == producer.p.POSSIBLE_RECORD_COUNT
    return {
        "expected_record_count": producer.p.POSSIBLE_RECORD_COUNT,
        "record_count": len(records),
        "record_sha256": sha(records),
        "first_nonzero": first_nonzero,
        "coverage_complete": coverage_complete,
        "all_zero_responses_annihilated": coverage_complete and first_nonzero is None,
        "records": records,
    }


def verify(result: dict) -> dict:
    legacy = dict(result)
    spectator_closed = result.get("terminal") == producer.CLOSURE_TERMINAL
    legacy["full_coordinate_zero_laurent_algebra_corollary"] = (
        producer.FULL_ALGEBRA_COROLLARY if spectator_closed else None
    )
    legacy["full_coordinate_zero_laurent_algebra_closed"] = spectator_closed
    base = _BASE_VERIFY(legacy)

    zero_audit = _independent_all_zero_multiplier_audit()
    if result.get("all_zero_multiplier_audit") != zero_audit:
        raise AssertionError("R all-zero producer audit disagrees with independent replay")

    full_closed = spectator_closed and zero_audit["all_zero_responses_annihilated"]
    expected_corollary = producer.FULL_ALGEBRA_COROLLARY if full_closed else None
    if result.get("full_coordinate_zero_laurent_algebra_corollary") != expected_corollary:
        raise AssertionError("R guarded full-algebra structural corollary drift")
    if result.get("full_coordinate_zero_laurent_algebra_closed") is not full_closed:
        raise AssertionError("R guarded full-algebra closure flag drift")
    if result.get("partition_basis", {}).get("all_exponents_zero") != (
        "explicit R all-zero direct mixed-response audit"
    ):
        raise AssertionError("R all-zero partition basis drift")

    base["all_zero_multiplier_audit"] = zero_audit
    base["full_coordinate_zero_laurent_algebra_corollary"] = expected_corollary
    base["full_coordinate_zero_laurent_algebra_closed"] = full_closed
    return base
