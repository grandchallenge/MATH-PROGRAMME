from pathlib import Path

_IMPL = Path(__file__).with_name("producer_impl.py.inc")
exec(compile(_IMPL.read_text(encoding="utf-8"), str(_IMPL), "exec"), globals(), globals())

_BASE_BUILD = build


def _all_zero_multiplier_audit() -> dict:
    primitive_full, strata, specialized, supports = o.f.d.build_context()
    banks = o.f._channel_banks(primitive_full, strata, specialized, supports)
    poly_cache = {}
    vector_cache = {}
    records = []
    first_nonzero = None

    for pair_index, pair in enumerate(p.ADMITTED_PAIRS):
        left, right = pair
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            for candidate_index, uid in enumerate(bank["candidates"]):
                vec_g = k.g._cached_vector_index(
                    endpoint, uid, (), strata, bank, poly_cache, vector_cache
                )[0]
                vec_gc = k.g._cached_vector_index(
                    endpoint, uid, (left,), strata, bank, poly_cache, vector_cache
                )[0]
                vec_gd = k.g._cached_vector_index(
                    endpoint, uid, (right,), strata, bank, poly_cache, vector_cache
                )[0]
                vec_gcd = k.g._cached_vector_index(
                    endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache
                )[0]
                value = k._direct_mixed_pairing(
                    bank["witness"], vec_gcd, vec_gc, vec_gd, vec_g
                )
                record = {
                    "pair_index": pair_index,
                    "endpoint_index": endpoint_index,
                    "candidate_index": candidate_index,
                    "pair": list(pair),
                    "endpoint": endpoint,
                    "candidate": p.unknown_json(uid),
                    "pairing": k.qjson(value),
                }
                records.append(record)
                if value != 0 and first_nonzero is None:
                    first_nonzero = dict(record)

    coverage_complete = len(records) == p.POSSIBLE_RECORD_COUNT
    return {
        "expected_record_count": p.POSSIBLE_RECORD_COUNT,
        "record_count": len(records),
        "record_sha256": sha(records),
        "first_nonzero": first_nonzero,
        "coverage_complete": coverage_complete,
        "all_zero_responses_annihilated": coverage_complete and first_nonzero is None,
        "records": records,
    }


def build() -> dict:
    result = _BASE_BUILD()
    zero_audit = _all_zero_multiplier_audit()
    result["all_zero_multiplier_audit"] = zero_audit

    full_closed = (
        result.get("terminal") == CLOSURE_TERMINAL
        and zero_audit["all_zero_responses_annihilated"]
    )
    result["full_coordinate_zero_laurent_algebra_corollary"] = (
        FULL_ALGEBRA_COROLLARY if full_closed else None
    )
    result["full_coordinate_zero_laurent_algebra_closed"] = full_closed
    result.setdefault("partition_basis", {})["all_exponents_zero"] = (
        "explicit R all-zero direct mixed-response audit"
    )
    return result
