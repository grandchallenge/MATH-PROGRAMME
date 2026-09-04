"""Cross-surface orphan discovery for GCL-TCS candidate-readiness.

This module is deliberately library-only. It discovers references and composes
incumbent authoritative registrations; it is not a registry and confers no authority.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_INDEX = Path("docs/governance/GCL_TCS_PILOT_EVIDENCE_INDEX.md")
PILOT_ROOT = Path("governance/gcl_tcs_pilots")

TEXT_SUFFIXES = {".md", ".html", ".htm", ".txt", ".tex", ".json", ".yaml", ".yml"}
SCRATCH_PARTS = {"scratch", "_scratch", "scratchpad", "unregistered_scratch", "tmp", "temp"}
REPOSITORY_ROOT_PREFIXES = (
    ".github/",
    "campaigns/",
    "ci/",
    "council_submissions/",
    "docs/",
    "fixtures/",
    "governance/",
    "handoffs/",
    "reviews/",
    "schemas/",
    "tests/",
)
STRONG_GOVERNANCE_KEYS = {
    "record_id",
    "operation_id",
    "authority_status",
    "promotion_status",
    "candidate_revision",
    "review_record",
    "claim_ledger",
}
STRONG_TEXT_MARKERS = (
    "**Artifact ID:**",
    "authority_status:",
    "promotion_status:",
    '"record_id"',
    '"operation_id"',
)

MARKDOWN_REF_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)")
HTML_REF_RE = re.compile(r"(?:href|src)=[\"']([^\"']+)[\"']", re.IGNORECASE)
TEX_REF_RE = re.compile(
    r"\\(?:input|include|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}"
)
STATIC_PATH_RE = re.compile(
    r"(?:`|\b(?:path|file|source|candidate|asset|directory)\s*[:=]\s*[\"']?)"
    r"([A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+(?:\.[A-Za-z0-9_.-]+)?)/?"
)


def _iter_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from _iter_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _iter_strings(item)


def _structured_value(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    return None


def _structured_governance_keys(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key) in STRONG_GOVERNANCE_KEYS:
                found.add(str(key))
            found.update(_structured_governance_keys(item))
    elif isinstance(value, list):
        for item in value:
            found.update(_structured_governance_keys(item))
    return found


def has_strong_governance_identity(path: Path) -> bool:
    """Return true only for explicit machine/text governance identity markers."""
    if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
        return False
    try:
        if path.suffix.lower() in {".json", ".yaml", ".yml"}:
            value = _structured_value(path)
            if _structured_governance_keys(value):
                return True
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, yaml.YAMLError):
        return False
    return any(marker in text for marker in STRONG_TEXT_MARKERS)


def is_deliberate_scratch(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    return any(part.lower() in SCRATCH_PARTS for part in parts)


def _github_repository_path(raw: str) -> str | None:
    parsed = urlparse(raw)
    if parsed.netloc == "github.com":
        parts = [unquote(part) for part in parsed.path.split("/") if part]
        if (
            len(parts) >= 5
            and parts[:2] == ["grandchallenge", "MATH-PROGRAMME"]
            and parts[2] in {"blob", "tree"}
        ):
            return "/".join(parts[4:])
    if parsed.netloc == "raw.githubusercontent.com":
        parts = [unquote(part) for part in parsed.path.split("/") if part]
        if len(parts) >= 4 and parts[:2] == ["grandchallenge", "MATH-PROGRAMME"]:
            return "/".join(parts[3:])
    return None


def _looks_like_path(value: str) -> bool:
    value = value.strip().strip("`\"'")
    if not value or value.startswith(("#", "mailto:", "data:", "javascript:")):
        return False
    if value.startswith(("http://", "https://")):
        return _github_repository_path(value) is not None
    return "/" in value or bool(Path(value).suffix)


def raw_references(path: Path) -> list[str]:
    """Discover repository-like references without assigning authority to them."""
    if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
        return []
    text = path.read_text(encoding="utf-8")
    refs: list[str] = []
    suffix = path.suffix.lower()
    if suffix in {".md", ".html", ".htm"}:
        refs.extend(MARKDOWN_REF_RE.findall(text))
        refs.extend(HTML_REF_RE.findall(text))
    if suffix == ".tex":
        refs.extend(TEX_REF_RE.findall(text))
    if suffix in {".json", ".yaml", ".yml"}:
        try:
            refs.extend(
                value for value in _iter_strings(_structured_value(path)) if _looks_like_path(value)
            )
        except (json.JSONDecodeError, yaml.YAMLError):
            pass
    if suffix in {".md", ".html", ".htm", ".txt", ".tex"}:
        refs.extend(STATIC_PATH_RE.findall(text))
    return list(dict.fromkeys(ref.strip() for ref in refs if ref.strip()))


def resolve_reference(source: Path, raw: str, root: Path) -> tuple[Path | None, str | None]:
    """Resolve a discovered repository reference, returning (target, error)."""
    raw = raw.strip().strip("`\"'")
    repository_path = _github_repository_path(raw)
    if raw.startswith(("http://", "https://")) and repository_path is None:
        return None, None
    if repository_path is not None:
        candidate = root / repository_path
    else:
        clean = raw.split("#", 1)[0].split("?", 1)[0]
        if not clean or clean.startswith(("mailto:", "data:", "javascript:")):
            return None, None
        if clean.startswith("/") or clean.startswith(REPOSITORY_ROOT_PREFIXES):
            candidate = root / clean.lstrip("/")
        else:
            candidate = source.parent / clean
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root.resolve())
    except ValueError:
        return None, f"{source.relative_to(root)}: repository reference escapes root: {raw}"

    if resolved.exists():
        return resolved, None

    if source.suffix.lower() == ".tex" and not resolved.suffix:
        tex = resolved.with_suffix(".tex")
        if tex.exists():
            return tex, None
        for suffix in (".svg", ".png", ".jpg", ".jpeg", ".pdf"):
            graphic = resolved.with_suffix(suffix)
            if graphic.exists():
                return graphic, None
    return resolved, f"{source.relative_to(root)}: missing repository reference target: {raw}"


def reference_errors(paths: Iterable[Path], root: Path) -> list[str]:
    errors: list[str] = []
    for source in paths:
        if not source.is_file():
            continue
        for raw in raw_references(source):
            _, error = resolve_reference(source, raw, root)
            if error:
                errors.append(error)
    return sorted(set(errors))


def registered_by_text(target: Path, registrars: Iterable[Path], root: Path) -> bool:
    """Return whether an incumbent discovery surface references the target."""
    relative = target.relative_to(root).as_posix()
    for registrar in registrars:
        if not registrar.is_file():
            continue
        text = registrar.read_text(encoding="utf-8")
        if relative in text:
            return True
        for raw in raw_references(registrar):
            resolved, error = resolve_reference(registrar, raw, root)
            if error is None and resolved is not None and resolved == target.resolve():
                return True
    return False


def governed_root_orphan_errors(
    governed_root: Path,
    registrars: Iterable[Path],
    root: Path,
) -> list[str]:
    """Require each immediate governed package/file to be discoverable from a registrar."""
    errors: list[str] = []
    if not governed_root.is_dir():
        return [f"{governed_root.relative_to(root)}: governed directory is missing"]
    for target in sorted(governed_root.iterdir()):
        if not registered_by_text(target, registrars, root):
            errors.append(f"{target.relative_to(root)}: definite governed orphan")
    return errors


def scratch_boundary_errors(root: Path) -> list[str]:
    """Permit scratch paths unless their content asserts a strong governed identity."""
    errors: list[str] = []
    for path in root.rglob("*"):
        if (
            path.is_file()
            and is_deliberate_scratch(path, root)
            and has_strong_governance_identity(path)
        ):
            errors.append(f"{path.relative_to(root)}: scratch path contains governed identity markers")
    return sorted(set(errors))


def gcl_tcs_json_orphan_errors(registrars: Iterable[Path], root: Path) -> list[str]:
    errors: list[str] = []
    governance = root / "governance"
    for target in sorted(governance.glob("gcl_tcs_*.json")):
        if not registered_by_text(target, registrars, root):
            errors.append(f"{target.relative_to(root)}: definite governed JSON orphan")
    return errors


def cross_surface_orphan_errors(root: Path = ROOT) -> list[str]:
    """Run the live GCL-TCS criterion-7 discovery layer.

    The Documentary Library's manifest-driven source/candidate/web/asset/static/TeX
    discovery remains authoritative and is already executed by `ci/validate_programme.py`.
    This layer adds the missing generic reference graph for the GCL-TCS governed pilot
    surface and does not copy the Documentary Library inventory.
    """
    index = root / EVIDENCE_INDEX
    if not index.is_file():
        return [f"{EVIDENCE_INDEX}: current GCL-TCS evidence index is missing"]

    errors: list[str] = []
    errors.extend(reference_errors([index], root))
    errors.extend(governed_root_orphan_errors(root / PILOT_ROOT, [index], root))
    errors.extend(gcl_tcs_json_orphan_errors([index], root))
    errors.extend(scratch_boundary_errors(root))
    return sorted(set(errors))
