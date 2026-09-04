from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
POLICY = Path("docs/council/submissions/GCL-TCS-00/GCL-TCS-00.policy.yaml")
DECL_SCHEMA = Path("docs/council/submissions/GCL-TCS-00/schemas/gcl-tcs-conformance.schema.json")
RECORD_SCHEMA = Path("docs/council/submissions/GCL-TCS-00/schemas/gcl-tcs-record-contracts.schema.json")
DECL_TEMPLATE = Path("docs/council/submissions/GCL-TCS-00/templates/GCL-TCS-00.conformance.template.yaml")
RECORD_TEMPLATE = Path("docs/council/submissions/GCL-TCS-00/templates/GCL-TCS-00.records.template.yaml")
MATRIX = Path("governance/gcl_tcs_normative_agreement_matrix.json")
HISTORICAL_MANIFEST = Path("docs/council/submissions/SUBMISSION_MANIFEST.yaml")
SOURCE_PARTS = tuple(Path(f"council_submissions/GCL-TCS-00/parts/{name}") for name in (
    "00-frontmatter-purpose-principles.md",
    "01-hierarchy-conformance-impact.md",
    "02-conformance-profiles.md",
    "03-metadata-language-structure.md",
    "04-exceptions-promotion-gates.md",
    "05-review-roles-controls-change.md",
    "06-adoption-acceptance-appendices.md",
))
EXPECTED_SOURCE_SHA256 = "ea750b9b80b53c7d6ed755978fa4bdf59413fad93cec1db81eb3238372ce61c9"
EXPECTED_HISTORICAL_POLICY_SHA256 = "8102c0012b79698f6294b479471117a7884609fa0bf03518a940224dae7c9735"
EXPECTED_HISTORICAL_SCHEMA_SHA256 = "906d5a85cb26175667590eb2a0def92db3a03871d4a5a25719328ff39523dce9"
HARD_RE = re.compile(r"\bMUST(?:\s+NOT)?\b")
STRONG_RE = re.compile(r"\bSHOULD(?:\s+NOT)?\b")


class AgreementError(RuntimeError):
    pass


def _load_yaml(path: Path, root: Path = ROOT) -> dict[str, Any]:
    raw = yaml.safe_load((root / path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise AgreementError(f"{path}: expected mapping")
    return raw


def _load_json(path: Path, root: Path = ROOT) -> dict[str, Any]:
    raw = json.loads((root / path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise AgreementError(f"{path}: expected mapping")
    return raw


def load_matrix(root: Path = ROOT) -> dict[str, Any]:
    index = _load_json(MATRIX, root)
    shards = index.get("shards")
    if not isinstance(shards, list) or not shards:
        raise AgreementError("matrix.shards: missing_or_empty")
    rows: list[Any] = []
    for entry in shards:
        if not isinstance(entry, Mapping) or not isinstance(entry.get("path"), str) or not isinstance(entry.get("source"), str):
            raise AgreementError("matrix.shards: malformed_entry")
        shard = _load_json(Path(entry["path"]), root)
        if shard.get("source") != entry["source"]:
            raise AgreementError(f"matrix shard source drift: {entry['path']}")
        shard_rows = shard.get("rows")
        if not isinstance(shard_rows, list):
            raise AgreementError(f"matrix shard rows missing: {entry['path']}")
        rows.extend(shard_rows)
    if index.get("row_count") != len(rows):
        raise AgreementError(f"matrix row count drift: expected {index.get('row_count')}, got {len(rows)}")
    merged = dict(index)
    merged["rows"] = rows
    return merged


def _norm(text: str) -> str:
    text = text.replace("`", "").replace("**", "")
    return re.sub(r"\s+", " ", text).strip().lower()


def source_digest(root: Path = ROOT) -> str:
    data = b"".join((root / path).read_bytes() for path in SOURCE_PARTS)
    return hashlib.sha256(data).hexdigest()


def _paragraphs(text: str) -> list[str]:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


def source_coverage_errors(matrix: Mapping[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    rows = matrix.get("rows")
    if not isinstance(rows, list) or not rows:
        return ["matrix.rows: missing_or_empty"]
    by_source: dict[str, list[Mapping[str, Any]]] = {}
    ids: set[str] = set()
    for item in rows:
        if not isinstance(item, Mapping):
            errors.append("matrix.rows: malformed_row")
            continue
        rid = item.get("id")
        if not isinstance(rid, str) or not rid:
            errors.append("matrix.rows: missing_id")
        elif rid in ids:
            errors.append(f"matrix.rows: duplicate_id:{rid}")
        else:
            ids.add(rid)
        source = item.get("source")
        match = item.get("source_match")
        if not isinstance(source, str) or not source:
            errors.append(f"{rid}: missing_source")
            continue
        if not isinstance(match, str) or not match:
            errors.append(f"{rid}: missing_source_match")
            continue
        by_source.setdefault(source, []).append(item)
    expected_sources = {str(p) for p in SOURCE_PARTS}
    missing_sources = expected_sources - set(by_source)
    if missing_sources:
        errors.extend(f"matrix: source_uncovered:{p}" for p in sorted(missing_sources))
    for path in SOURCE_PARTS:
        source_name = str(path)
        text = (root / path).read_text(encoding="utf-8")
        norm_text = _norm(text)
        source_rows = by_source.get(source_name, [])
        for row in source_rows:
            match = _norm(str(row.get("source_match", "")))
            if match and match not in norm_text:
                errors.append(f"{row.get('id')}: source_match_not_found")
        for paragraph in _paragraphs(text):
            hard_count = len(HARD_RE.findall(paragraph))
            strong_count = len(STRONG_RE.findall(paragraph))
            if not hard_count and not strong_count:
                continue
            norm_para = _norm(paragraph)
            matched = [row for row in source_rows if _norm(str(row.get("source_match", ""))) in norm_para]
            required_count = hard_count + strong_count
            if len(matched) < required_count:
                errors.append(f"{source_name}: uncovered_normative_clause:required={required_count}:matched={len(matched)}:{norm_para[:120]}")
    return sorted(set(errors))


def _require_policy_path(policy: Mapping[str, Any], path: str) -> bool:
    cur: Any = policy
    for token in path.split("."):
        if not isinstance(cur, Mapping) or token not in cur:
            return False
        cur = cur[token]
    return True


def policy_contract_errors(policy: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    standard = policy.get("standard")
    if not isinstance(standard, Mapping) or (standard.get("id"), standard.get("version"), standard.get("status")) != ("GCL-TCS-00", "0.1.0", "candidate"):
        errors.append("policy: candidate_identity_drift")
    required_paths = (
        "normative_source_contract", "normative_obligations", "conformance_rules",
        "record_contracts.claim", "record_contracts.evidence", "record_contracts.review",
        "record_contracts.exception", "record_contracts.gate", "record_contracts.conformance_statement",
        "record_contracts.release", "language_structure_contract", "exception_contract",
        "gate_contracts", "promotion_contract", "review_control", "change_control", "strong_defaults", "machine_contracts",
    )
    for path in required_paths:
        if not _require_policy_path(policy, path):
            errors.append(f"policy: missing:{path}")
    source = policy.get("normative_source_contract")
    if isinstance(source, Mapping):
        if source.get("assembled_sha256") != EXPECTED_SOURCE_SHA256:
            errors.append("policy: normative_source_digest_drift")
        if source.get("source_controls_meaning") is not True:
            errors.append("policy: source_must_control_meaning")
        if source.get("machine_surfaces_are_derivative") is not True:
            errors.append("policy: machine_surface_authority_inflation")
    contracts = policy.get("record_contracts")
    expected_fields = {
        "claim": {"claim_id","statement_or_immutable_pointer","claim_type","claim_status","scope","assumptions","dependencies","supporting_evidence","counterevidence","falsifiers","limitations","owner","last_reviewed"},
        "evidence": {"evidence_id","evidence_type","location","version_or_hash","method","result_summary","scope","limitations","created_by","created_at"},
        "review": {"review_id","gate_id","reviewer","review_role","independence_statement","date","decision","findings","required_actions","resolved_actions","evidence","reviewed_revision"},
        "exception": {"exception_id","rule_id","artifact_scope","affected_content","justification","risk_assessment","compensating_controls","requested_by","approved_by","issued_date","status"},
        "gate": {"gate_id","artifact_id","reviewed_revision","decision","review_record_ref","evidence"},
        "conformance_statement": {"primary_profile","secondary_profiles","impact_class","target_state","dimensions","active_exceptions","promotion_status","date","standard_versions"},
        "release": {"change_log","migration_note","compatibility_statement","previous_standard_identifier","new_standard_identifier","review_record","promotion_record"},
    }
    if isinstance(contracts, Mapping):
        for name, fields in expected_fields.items():
            block = contracts.get(name)
            vals = block.get("required_fields") if isinstance(block, Mapping) else None
            if not isinstance(vals, list) or not fields.issubset(set(vals)):
                errors.append(f"policy: record_contract_fields:{name}")
    exception_model = policy.get("exception_model")
    if not isinstance(exception_model, Mapping):
        errors.append("policy: exception_model_missing")
    else:
        if set(exception_model.get("statuses") or []) != {"requested","approved","rejected","expired","revoked","superseded"}:
            errors.append("policy: exception_status_drift")
        non_waivable = set(exception_model.get("non_waivable") or [])
        for value in ("truthful_nonmisleading_communication", "exception_registration", "fail_closed_missing_record_behaviour", "no_fabricated_evidence_reviews_or_authority"):
            if value not in non_waivable:
                errors.append(f"policy: missing_non_waivable:{value}")
    return sorted(set(errors))


def schema_contract_errors(declaration_schema: Mapping[str, Any], record_schema: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        Draft202012Validator.check_schema(dict(declaration_schema))
    except Exception as exc:
        errors.append(f"declaration_schema: invalid:{exc}")
    try:
        Draft202012Validator.check_schema(dict(record_schema))
    except Exception as exc:
        errors.append(f"record_schema: invalid:{exc}")
    defs = declaration_schema.get("$defs")
    if not isinstance(defs, Mapping):
        return errors + ["declaration_schema: missing_defs"]
    standard = defs.get("standardIdentifier")
    profile = defs.get("profile")
    if not isinstance(standard, Mapping):
        errors.append("declaration_schema: standard_identifier_not_locked")
    else:
        props = standard.get("properties")
        if not isinstance(props, Mapping) or props.get("id", {}).get("const") != "GCL-TCS-00" or props.get("version", {}).get("const") != "0.1.0":
            errors.append("declaration_schema: standard_identifier_not_locked")
    if not isinstance(profile, Mapping):
        errors.append("declaration_schema: profile_version_not_locked")
    else:
        props = profile.get("properties")
        if not isinstance(props, Mapping) or props.get("version", {}).get("const") != "0.1.0":
            errors.append("declaration_schema: profile_version_not_locked")
    record_defs = record_schema.get("$defs")
    required = {"claimRecord","evidenceRecord","reviewRecord","exceptionRecord","gateRecord","conformanceStatement","releaseRecord"}
    if not isinstance(record_defs, Mapping) or not required.issubset(record_defs):
        errors.append("record_schema: missing_normative_record_defs")
    return sorted(set(errors))


def _validation_errors(instance: Any, schema: Mapping[str, Any]) -> list[str]:
    validator = Draft202012Validator(dict(schema), format_checker=FormatChecker())
    return [err.message for err in validator.iter_errors(instance)]


def template_contract_errors(declaration_schema: Mapping[str, Any], record_schema: Mapping[str, Any], declaration_template: Mapping[str, Any], record_template: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    errors.extend(f"declaration_template: {x}" for x in _validation_errors(declaration_template, declaration_schema))
    defs = record_schema.get("$defs")
    if not isinstance(defs, Mapping):
        return errors + ["record_template: schema_defs_missing"]
    mapping = {"claim_record":"claimRecord", "evidence_record":"evidenceRecord", "review_record":"reviewRecord", "exception_record":"exceptionRecord", "gate_record":"gateRecord", "conformance_statement":"conformanceStatement", "release_record":"releaseRecord"}
    for template_key, def_key in mapping.items():
        if template_key not in record_template:
            errors.append(f"record_template: missing:{template_key}")
            continue
        schema = defs.get(def_key)
        if not isinstance(schema, Mapping):
            errors.append(f"record_template: missing_schema:{def_key}")
            continue
        errors.extend(f"record_template:{template_key}: {x}" for x in _validation_errors(record_template[template_key], schema))
    contract = record_template.get("template_contract")
    if not isinstance(contract, Mapping) or contract.get("authority") != "candidate_template_only":
        errors.append("record_template: authority_boundary_missing")
    return sorted(set(errors))


def historical_manifest_errors(manifest: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        return ["historical_manifest: artifacts_missing"]
    tcs = next((x for x in artifacts if isinstance(x, Mapping) and x.get("artifact_id") == "GCL-TCS-00"), None)
    if not isinstance(tcs, Mapping):
        return ["historical_manifest: GCL-TCS-00_missing"]
    policy = tcs.get("machine_policy")
    schema = tcs.get("conformance_schema")
    if not isinstance(policy, Mapping) or policy.get("sha256") != EXPECTED_HISTORICAL_POLICY_SHA256:
        errors.append("historical_manifest: issued_policy_hash_rewritten")
    if not isinstance(schema, Mapping) or schema.get("sha256") != EXPECTED_HISTORICAL_SCHEMA_SHA256:
        errors.append("historical_manifest: issued_schema_hash_rewritten")
    normative = tcs.get("normative_source")
    if not isinstance(normative, Mapping) or normative.get("assembled_sha256") != EXPECTED_SOURCE_SHA256:
        errors.append("historical_manifest: normative_source_hash_rewritten")
    return errors


def repository_agreement_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if source_digest(root) != EXPECTED_SOURCE_SHA256:
        errors.append("normative_source: assembled_digest_mismatch")
    matrix = load_matrix(root)
    policy = _load_yaml(POLICY, root)
    decl_schema = _load_json(DECL_SCHEMA, root)
    record_schema = _load_json(RECORD_SCHEMA, root)
    decl_template = _load_yaml(DECL_TEMPLATE, root)
    record_template = _load_yaml(RECORD_TEMPLATE, root)
    historical = _load_yaml(HISTORICAL_MANIFEST, root)
    errors.extend(source_coverage_errors(matrix, root))
    errors.extend(policy_contract_errors(policy))
    errors.extend(schema_contract_errors(decl_schema, record_schema))
    errors.extend(template_contract_errors(decl_schema, record_schema, decl_template, record_template))
    errors.extend(historical_manifest_errors(historical))
    rows = matrix.get("rows")
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, Mapping) and row.get("gap") not in {"CLOSED", "NOT_MACHINE_CHECKABLE"}:
                errors.append(f"{row.get('id')}: open_gap:{row.get('gap')}")
    if matrix.get("authority_boundary") != "DERIVATIVE_RECONCILIATION_ONLY__NO_V1_PROMOTION":
        errors.append("matrix: authority_boundary_drift")
    return sorted(set(errors))
