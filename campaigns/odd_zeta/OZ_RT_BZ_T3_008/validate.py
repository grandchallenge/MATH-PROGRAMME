#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
RESULT_PATH = HERE / "SEARCH_RESULT.json"
RECORD_PATH = HERE / "OZ_RT_BZ_T3_008.json"
SCHEMA_PATH = HERE / "OZ_RT_BZ_T3_008.schema.json"
WITNESS_PATH = HERE / "Q2_RANK_WITNESS.json"

RESULT_SHA = "4f37b83be6b83663246c4dd0a7d24190709c9f7bc4b43ea411d29f742450101b"
WITNESS_SHA = "7d82b0088b6629c92bbb5c2457c5c520120ef275109503614b28910fe34eddc5"
BASIS_SHA = "cbdfe5798d360cb98f2d64743907a06ddc0612f88d17ef4bcef65c81c74e1438"
NORMALIZATION_SHA = "69738508f28433f9090f93621c8da3bc6b18279fd70941a31d07fb96b607700b"
Q2_INDEX_SHA = "d0bb330deff059c2afdc4e1a994d7c544c42ce7ec497e1c6490ca9f2781dc57f"


def canonical_sha(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_documents(result: dict, record: dict, witness: dict, schema: dict, *, check_digests: bool = True) -> None:
    errors = sorted(Draft202012Validator(schema).iter_errors(record), key=lambda e: list(e.path))
    if errors:
        raise AssertionError("campaign schema validation failed: " + "; ".join(e.message for e in errors[:3]))
    if check_digests:
        check(canonical_sha(result) == RESULT_SHA, "canonical SEARCH_RESULT digest drift")
        check(canonical_sha(witness) == WITNESS_SHA, "canonical degree-2 witness digest drift")
        check(record["artifacts"]["search_result_sha256"] == RESULT_SHA, "record result digest drift")
        check(record["artifacts"]["degree2_rank_witness_sha256"] == WITNESS_SHA, "record witness digest drift")
    check(result["operation"] == "OZ-RT-BZ-T3-008", "operation drift")
    check(result["route"] == "SYMMETRIC_2D_RAW_JET_DIVERGENCE_001", "route drift")
    check(result["prime"] == 1000003, "rank prime drift")
    check(result["predecessor"] == {"issue": 359, "pull_request": 360, "merge_commit": "5233b37506f28e80959139cbc0f89b7ad400b658", "merge_tree": "5f5fc435927888fbdf84c1ba15044c347506fbd0"}, "predecessor lock drift")
    check(result["execution_intake"] == {"protected_head": "5233b37506f28e80959139cbc0f89b7ad400b658", "protected_tree": "5f5fc435927888fbdf84c1ba15044c347506fbd0"}, "execution intake drift")
    basis = result["basis"]
    check(basis["monomial_count"] == 198, "basis cardinality drift")
    check(basis["basis_sha256"] == BASIS_SHA, "basis digest drift")
    check(basis["one_body_only_count"] == 158 and basis["one_nested_atom_count"] == 40, "nested-basis decomposition drift")
    check(basis["k_l_swap_invariant"] is True, "basis swap closure lost")
    norm = result["coordinate_normalization"]
    check(norm["monomial_multiplier_count"] == 198, "normalization cardinality drift")
    check(norm["multiplier_vector_sha256"] == NORMALIZATION_SHA, "normalization digest drift")
    check(norm["all_nonzero_integers"] is True and norm["all_nonzero_mod_prime"] is True, "normalization invertibility lost")
    sym = result["symmetry_completeness"]
    for key in ("target_swap_invariant", "basis_swap_closed", "denominator_swap_closed", "boundary_factor_swap_closed", "coefficient_envelope_swap_closed", "rank_prime_odd"):
        check(sym[key] is True, f"symmetry-completeness prerequisite lost: {key}")
    check(sym["lemma"] == "ANY_UNRESTRICTED_SWAP_CLOSED_TWO_FLUX_SOLUTION_SYMMETRIZES_TO_Q_EQUALS_TAU_P", "symmetry-completeness lemma drift")
    flux = result["flux"]
    check(flux["k_denominator"] == "(k+1)^3*(k+l+1)", "k denominator drift")
    check(flux["l_denominator"] == "(l+1)^3*(k+l+1)", "l denominator drift")
    check(flux["k_boundary_factor"] == "k*(n+1-k)", "k boundary drift")
    check(flux["l_boundary_factor"] == "l*(n+1-l)", "l boundary drift")
    check(result["search_class"]["coefficient_degrees"] == [0, 1, 2], "degree ladder drift")
    check(result["search_class"]["symmetric_subspace_complete_for_declared_swap_closed_two_flux_class"] is True, "symmetric search completeness drift")
    aliases = result["preliminary_alias_grids"]
    expected_aliases = [(0, 8, 280, 198, 154, 154), (1, 13, 1010, 792, 544, 544), (2, 18, 2465, 1980, 1309, 1309)]
    check(len(aliases) == 3, "preliminary alias ladder cardinality drift")
    for item, expected in zip(aliases, expected_aliases):
        got = (item["q_coefficient_degree"], item["n_max"], item["rows"], item["unknowns"], item["coefficient_rank"], item["augmented_rank"])
        check(got == expected, f"preliminary alias evidence drift: {got} != {expected}")
        check(item["classification"] == "FINITE_GRID_ALIAS_ONLY", "preliminary equal rank promoted to candidate evidence")
    stages = result["stages"]
    expected_stages = [(0, 20, 3306, 198, 198, 199), (1, 20, 3306, 792, 792, 793), (2, 22, 4319, 1980, 1980, 1981)]
    check(len(stages) == 3, "final stage ladder cardinality drift")
    for item, expected in zip(stages, expected_stages):
        got = (item["q_coefficient_degree"], item["n_max"], item["full_grid_rows"], item["unknowns"], item["coefficient_rank"], item["augmented_rank"])
        check(got == expected, f"final affine rank drift: {got} != {expected}")
        check(item["classification"] == "EXACT_AFFINE_INCONSISTENCY", "final affine classification drift")
        check(item["coefficient_rank"] == item["unknowns"], "coefficient matrix is not full column rank")
        check(item["augmented_rank"] == item["unknowns"] + 1, "augmented rank does not certify inconsistency")
    q2 = stages[2]
    check(q2["witness_file"] == "Q2_RANK_WITNESS.json", "degree-2 witness path drift")
    check(q2["coefficient_row_indices_sha256"] == Q2_INDEX_SHA, "degree-2 stage witness digest drift")
    check(q2["augmented_extra_row_index"] == 3674, "degree-2 extra row index drift")
    check(q2["augmented_extra_row_point"] == [21, 16, 16], "degree-2 extra row point drift")
    ids = witness["coefficient_row_indices"]
    check(len(ids) == 1980 and len(set(ids)) == 1980, "degree-2 witness rows not unique/full")
    check(canonical_sha(ids) == Q2_INDEX_SHA, "degree-2 witness row-list digest drift")
    check(witness["full_grid_rows"] == 4319, "degree-2 witness full-grid size drift")
    check(witness["coefficient_rank"] == 1980, "degree-2 coefficient witness rank drift")
    check(witness["augmented_rank"] == 1981, "degree-2 augmented witness rank drift")
    check(witness["augmented_extra_row_index"] == 3674, "degree-2 witness extra-row index drift")
    check(witness["augmented_extra_row_point"] == [21, 16, 16], "degree-2 witness extra-row point drift")
    check(result["terminal"] == "SYMMETRIC_2D_WEIGHT5_DIVERGENCE_BOUNDED_CLASS_EXHAUSTED", "bounded terminal drift")
    check(result["proof_effect"] == "NONE" and result["promotion_effect"] == "NONE", "claim-effect inflation")
    check(result["t3_status"] == "OPEN_WITH_CHARACTERIZED_BLOCKER", "T3 status inflation")
    check(result["next_distinct_route"] == "T3_SEQUENCE_RECURRENCE_EXTRACTION_001", "successor route drift")
    check(record["disposition"]["status"] == "OPEN_WITH_CHARACTERIZED_BLOCKER", "record disposition drift")
    check(record["disposition"]["bounded_search_terminal"] == result["terminal"], "record/result terminal mismatch")
    check(record["disposition"]["proof_found"] is False, "proof inflation")
    check(record["disposition"]["counterexample_found"] is False, "refutation inflation")
    check(record["disposition"]["not_a_refutation"] is True, "negative-result boundary lost")
    check(record["disposition"]["next_distinct_route"] == "T3_SEQUENCE_RECURRENCE_EXTRACTION_001", "record successor drift")
    check(all(v is False for v in record["nonclaims"].values()), "nonclaim firewall opened")


def main() -> int:
    result = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    record = json.loads(RECORD_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    witness = json.loads(WITNESS_PATH.read_text(encoding="utf-8"))
    validate_documents(result, record, witness, schema)
    print("OZ-RT-BZ-T3-008 exact bounded symmetric-2D divergence exhaustion package is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
