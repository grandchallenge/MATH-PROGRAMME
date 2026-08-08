#!/usr/bin/env python3
"""Deterministic checked-environment Lean dependency extractor for CMDG.

Emits observed G_proof/G_implementation/G_provenance evidence only. It never
confers G_semantic authority, REALIZES_AS, foundational concordance, dependency
minimality, global completeness, or GRAPH_CERTIFIED.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EXTRACTOR_VERSION = "1.0.3"
NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_'.]*(?:\.[A-Za-z_][A-Za-z0-9_']*)*$")
COMMON_AXIOMS = ("propext", "Classical.choice", "Quot.sound")
EXPECTED_BOUNDARY = {
    "semantic_authority_conferred": False,
    "realizes_as_conferred": False,
    "foundational_concordance_conferred": False,
    "graph_certified_conferred": False,
    "dependency_minimality_claim": False,
}


class ExtractionError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def reject(code: str, message: str) -> None:
    raise ExtractionError(code, message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def git_head() -> str:
    proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0:
        reject("REPOSITORY_IDENTITY_UNAVAILABLE", proc.stderr.strip() or "git rev-parse HEAD failed")
    head = proc.stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        reject("REPOSITORY_IDENTITY_MALFORMED", f"unexpected repository head: {head!r}")
    return head


def candidate_head() -> str:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if event_path:
        try:
            event = json.loads(Path(event_path).read_text(encoding="utf-8"))
            sha = event.get("pull_request", {}).get("head", {}).get("sha")
            if isinstance(sha, str) and re.fullmatch(r"[0-9a-f]{40}", sha):
                return sha
        except (OSError, json.JSONDecodeError):
            pass
    return git_head()


def load_config(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        reject("CONFIG_LOAD_FAILED", f"{path}: {exc}")
    if not isinstance(value, dict):
        reject("CONFIG_MALFORMED", "config root must be an object")
    required = {
        "schema_version", "fixture_id", "project_dir", "module", "roots",
        "expected_toolchain_git_blob_sha1", "expected_lake_manifest_git_blob_sha1",
        "expected_axioms", "claim_boundary",
    }
    missing = sorted(required - value.keys())
    if missing:
        reject("CONFIG_MALFORMED", "missing config keys: " + ", ".join(missing))
    if value["schema_version"] != "1.0.0":
        reject("SCHEMA_VERSION_DRIFT", "extractor config schema version drift")
    roots = value["roots"]
    if not isinstance(roots, list) or not roots:
        reject("ROOT_SET_MALFORMED", "roots must be a nonempty list")
    if len(set(roots)) != len(roots):
        reject("DUPLICATE_REQUESTED_ROOT", "requested root declarations must be unique")
    for root in roots:
        if not isinstance(root, str) or not NAME_RE.fullmatch(root):
            reject("MALFORMED_DECLARATION_NAME", f"malformed declaration name: {root!r}")
    if not isinstance(value["module"], str) or not NAME_RE.fullmatch(value["module"]):
        reject("MALFORMED_MODULE_NAME", f"malformed module name: {value['module']!r}")
    if value["claim_boundary"] != EXPECTED_BOUNDARY:
        reject("PROHIBITED_AUTHORITY_PROMOTION", "extractor claim boundary is not fail-closed")
    return value


def validate_pins(config: dict[str, Any], project_dir: Path) -> dict[str, str]:
    toolchain = project_dir / "lean-toolchain"
    manifest = project_dir / "lake-manifest.json"
    if not toolchain.is_file() or not manifest.is_file():
        reject("PROJECT_PIN_MISSING", "lean-toolchain and lake-manifest.json are required")
    actual_toolchain = git_blob_sha1(toolchain)
    actual_manifest = git_blob_sha1(manifest)
    if actual_toolchain != config["expected_toolchain_git_blob_sha1"]:
        reject("STALE_TOOLCHAIN_PIN", f"lean-toolchain blob drift: {actual_toolchain} != {config['expected_toolchain_git_blob_sha1']}")
    if actual_manifest != config["expected_lake_manifest_git_blob_sha1"]:
        reject("STALE_LAKE_MANIFEST_PIN", f"lake-manifest blob drift: {actual_manifest} != {config['expected_lake_manifest_git_blob_sha1']}")
    return {
        "lean_toolchain_git_blob_sha1": actual_toolchain,
        "lake_manifest_git_blob_sha1": actual_manifest,
    }


def lean_probe_source(module: str, root: str) -> str:
    return f'''import Lean.Util.CollectAxioms
import {module}

open Lean Elab Command

private def sortedSet (s : NameSet) : Array Name := s.toArray.qsort Name.lt
private def sortedArray (a : Array Name) : Array Name := a.qsort Name.lt

private def mergeNames (a b : Array Name) : Array Name := Id.run do
  let mut s : NameSet := {{}}
  for n in a do s := s.insert n
  for n in b do s := s.insert n
  return sortedSet s

private def parts (ci : ConstantInfo) : Array Name × Array Name :=
  let deps (e : Expr) := sortedArray e.getUsedConstants
  match ci with
  | .axiomInfo v  => (deps v.type, #[])
  | .defnInfo v   => (deps v.type, deps v.value)
  | .thmInfo v    => (deps v.type, deps v.value)
  | .opaqueInfo v => (deps v.type, deps v.value)
  | .quotInfo _   => (#[], #[])
  | .ctorInfo v   => (deps v.type, #[])
  | .recInfo v    => (deps v.type, #[])
  | .inductInfo v => (deps v.type, sortedArray v.ctors.toArray)

private def kindString (ci : ConstantInfo) : String :=
  match ci with
  | .axiomInfo _  => "axiom"
  | .defnInfo _   => "definition"
  | .thmInfo _    => "theorem"
  | .opaqueInfo _ => "opaque"
  | .quotInfo _   => "quotient"
  | .ctorInfo _   => "constructor"
  | .recInfo _    => "recursor"
  | .inductInfo _ => "inductive"

private def moduleOf? (env : Environment) (n : Name) : Option Name :=
  match env.getModuleIdxFor? n with
  | some idx => env.header.moduleNames[idx]?
  | none => if (env.find? n).isSome then some env.header.mainModule else none

private def directImports (env : Environment) (n : Name) : Array Name :=
  match env.getModuleIdxFor? n with
  | some idx =>
      match env.header.moduleData[idx]? with
      | some data => (data.imports.map (fun imp => imp.module)).qsort Name.lt
      | none => #[]
  | none => #[]

private partial def visit
    (env : Environment) (rootModule : Name) (n : Name)
    (seen frontier : NameSet) (edges : Array (Name × Name)) :
    NameSet × NameSet × Array (Name × Name) :=
  if seen.contains n then (seen, frontier, edges) else
    let seen := seen.insert n
    match env.find? n with
    | none => (seen, frontier.insert n, edges)
    | some ci =>
      let p := parts ci
      (mergeNames p.1 p.2).foldl (init := (seen, frontier, edges)) fun state dep =>
        let (seen, frontier, edges) := state
        let edges := edges.push (n, dep)
        match moduleOf? env dep with
        | some modName =>
          if modName == rootModule then visit env rootModule dep seen frontier edges
          else (seen, frontier.insert dep, edges)
        | none => (seen, frontier.insert dep, edges)

private def edgeLt (a b : Name × Name) : Bool :=
  if a.1 == b.1 then Name.lt a.2 b.2 else Name.lt a.1 b.1

syntax (name := cmdgExtract) "#cmdg_extract" ident : command

elab_rules : command
  | `(#cmdg_extract $id:ident) => do
    let env ← getEnv
    let root := id.getId
    let some ci := env.find? root | throwError "CMDG_ROOT_NOT_FOUND|{{root}}"
    let some rootModule := moduleOf? env root | throwError "CMDG_ROOT_MODULE_UNKNOWN|{{root}}"
    let p := parts ci
    let direct := mergeNames p.1 p.2
    let axioms ← Lean.collectAxioms root
    let (seen, frontier, edges) := visit env rootModule root {{}} {{}} #[]
    let localClosure := (sortedSet seen).filter (fun n => n != root)
    let edges := edges.qsort edgeLt
    let imports := directImports env root
    liftIO <| IO.println s!"CMDG|ROOT|{{root}}"
    liftIO <| IO.println s!"CMDG|KIND|{{kindString ci}}"
    liftIO <| IO.println s!"CMDG|MODULE|{{rootModule}}"
    for n in p.1 do liftIO <| IO.println s!"CMDG|DIRECT_SIGNATURE|{{n}}"
    for n in p.2 do liftIO <| IO.println s!"CMDG|DIRECT_BODY|{{n}}"
    for n in direct do liftIO <| IO.println s!"CMDG|DIRECT|{{n}}"
    for n in localClosure do
      let kind := match env.find? n with | some c => kindString c | none => "unknown"
      let modName := (moduleOf? env n).getD `_unknown
      liftIO <| IO.println s!"CMDG|LOCAL_DECL|{{n}}|{{kind}}|{{modName}}"
    for edge in edges do
      let modName := (moduleOf? env edge.2).getD `_unknown
      liftIO <| IO.println s!"CMDG|EDGE|{{edge.1}}|{{edge.2}}|{{modName}}"
    for n in sortedSet frontier do
      let kind := match env.find? n with | some c => kindString c | none => "unknown"
      let modName := (moduleOf? env n).getD `_unknown
      liftIO <| IO.println s!"CMDG|FRONTIER|{{n}}|{{kind}}|{{modName}}"
    for ax in axioms do liftIO <| IO.println s!"CMDG|AXIOM|{{ax}}"
    for imp in imports do liftIO <| IO.println s!"CMDG|IMPORT|{{imp}}"
    liftIO <| IO.println "CMDG|SEMANTIC_AUTHORITY|false"
    liftIO <| IO.println "CMDG|GRAPH_CERTIFIED|false"

#cmdg_extract {root}
'''


def _unique_dicts(values: list[dict[str, str]], keys: tuple[str, ...]) -> list[dict[str, str]]:
    unique = {tuple(value[key] for key in keys): value for value in values}
    return [unique[key] for key in sorted(unique)]


def parse_probe(stdout: str, stderr: str) -> dict[str, Any]:
    lines = [line.strip() for line in (stdout + "\n" + stderr).splitlines() if line.strip().startswith("CMDG|")]
    if not lines:
        reject("PROBE_OUTPUT_MISSING", "Lean probe emitted no CMDG records")
    result: dict[str, Any] = {
        "direct_signature": [], "direct_body": [], "direct": [],
        "local_declarations": [], "edges": [], "frontier": [],
        "axioms": [], "imports": [],
    }
    scalar_seen: set[str] = set()
    for line in lines:
        parts = line.split("|")
        tag = parts[1]
        if tag in {"ROOT", "KIND", "MODULE", "SEMANTIC_AUTHORITY", "GRAPH_CERTIFIED"}:
            if len(parts) != 3:
                reject("PROBE_OUTPUT_MALFORMED", line)
            if tag in scalar_seen:
                reject("PROBE_OUTPUT_DUPLICATE_SCALAR", tag)
            scalar_seen.add(tag)
            result[tag.lower()] = parts[2]
        elif tag in {"DIRECT_SIGNATURE", "DIRECT_BODY", "DIRECT", "AXIOM", "IMPORT"}:
            if len(parts) != 3:
                reject("PROBE_OUTPUT_MALFORMED", line)
            key = {"AXIOM": "axioms", "IMPORT": "imports"}.get(tag, tag.lower())
            result[key].append(parts[2])
        elif tag in {"LOCAL_DECL", "FRONTIER"}:
            if len(parts) != 5:
                reject("PROBE_OUTPUT_MALFORMED", line)
            key = "local_declarations" if tag == "LOCAL_DECL" else "frontier"
            result[key].append({"declaration": parts[2], "kind": parts[3], "module": parts[4]})
        elif tag == "EDGE":
            if len(parts) != 5:
                reject("PROBE_OUTPUT_MALFORMED", line)
            result["edges"].append({"source": parts[2], "target": parts[3], "target_module": parts[4]})
        else:
            reject("PROBE_OUTPUT_UNKNOWN_TAG", line)

    required_scalars = {"ROOT", "KIND", "MODULE", "SEMANTIC_AUTHORITY", "GRAPH_CERTIFIED"}
    if scalar_seen != required_scalars:
        reject("PROBE_OUTPUT_MISSING_SCALAR", ", ".join(sorted(required_scalars - scalar_seen)))
    for key in ("direct_signature", "direct_body", "direct", "axioms", "imports"):
        result[key] = sorted(set(result[key]))
    result["local_declarations"] = _unique_dicts(result["local_declarations"], ("declaration", "kind", "module"))
    result["frontier"] = _unique_dicts(result["frontier"], ("declaration", "kind", "module"))
    result["edges"] = _unique_dicts(result["edges"], ("source", "target", "target_module"))
    if result["semantic_authority"] != "false" or result["graph_certified"] != "false":
        reject("PROHIBITED_AUTHORITY_PROMOTION", "Lean probe attempted authority promotion")
    return result


def run_probe(project_dir: Path, module: str, root: str) -> dict[str, Any]:
    probe_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".lean", prefix="CMDGExtract_", dir=project_dir, encoding="utf-8", delete=False) as handle:
            handle.write(lean_probe_source(module, root))
            probe_path = Path(handle.name)
        proc = subprocess.run(
            ["lake", "env", "lean", probe_path.name], cwd=project_dir,
            capture_output=True, text=True, env={**os.environ, "LC_ALL": "C.UTF-8"},
        )
        if proc.returncode != 0:
            combined = (proc.stdout + "\n" + proc.stderr).strip()
            if "CMDG_ROOT_NOT_FOUND" in combined:
                reject("ROOT_DECLARATION_NOT_FOUND", combined[-4000:])
            reject("LEAN_PROBE_FAILED", combined[-8000:])
        return parse_probe(proc.stdout, proc.stderr)
    finally:
        if probe_path is not None:
            probe_path.unlink(missing_ok=True)


def build_root_report(root: str, probe: dict[str, Any]) -> dict[str, Any]:
    if probe.get("root") != root:
        reject("ROOT_IDENTITY_MISMATCH", f"probe root {probe.get('root')!r} != requested {root!r}")
    axioms = probe["axioms"]
    return {
        "declaration": root,
        "kind": probe["kind"],
        "module": probe["module"],
        "direct_signature_dependencies": probe["direct_signature"],
        "direct_body_dependencies": probe["direct_body"],
        "direct_dependencies": probe["direct"],
        "observed_direct_proof_edges": [
            {**edge, "layer": "G_proof", "relation": "PROOF_USES_DECLARATION", "authority_state": "OBSERVED", "semantic_authority": False}
            for edge in probe["edges"]
        ],
        "derived_local_transitive_closure": [v["declaration"] for v in probe["local_declarations"]],
        "local_declarations": probe["local_declarations"],
        "external_proof_frontier": probe["frontier"],
        "axiom_footprint": {
            "axioms": axioms,
            "classicality_dependencies": [ax for ax in axioms if ax == "Classical.choice"],
            "common_axioms": {name: name in axioms for name in COMMON_AXIOMS},
            "other_axioms": [ax for ax in axioms if ax not in COMMON_AXIOMS],
        },
    }


def validate_expected_axioms(config: dict[str, Any], roots: list[dict[str, Any]]) -> None:
    expected = config["expected_axioms"]
    if not isinstance(expected, dict):
        reject("CONFIG_MALFORMED", "expected_axioms must be an object keyed by root declaration")
    actual = {root["declaration"]: root["axiom_footprint"]["axioms"] for root in roots}
    if expected != actual:
        reject("AXIOM_FOOTPRINT_MISMATCH", f"retained axiom footprint mismatch: expected={expected!r} actual={actual!r}")


def extract(config_path: Path) -> dict[str, Any]:
    config = load_config(config_path)
    project_dir = ROOT / config["project_dir"]
    if not project_dir.is_dir():
        reject("PROJECT_DIRECTORY_MISSING", str(project_dir))
    pins = validate_pins(config, project_dir)
    roots: list[dict[str, Any]] = []
    imports: set[str] = set()
    for root in config["roots"]:
        first = run_probe(project_dir, config["module"], root)
        second = run_probe(project_dir, config["module"], root)
        if first != second:
            reject("NONDETERMINISTIC_PROBE_CONTENT", f"repeated canonical extraction differs for {root}")
        roots.append(build_root_report(root, first))
        imports.update(first["imports"])
    validate_expected_axioms(config, roots)
    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "extractor_version": EXTRACTOR_VERSION,
        "fixture_id": config["fixture_id"],
        "candidate_head_commit": candidate_head(),
        "repository_checkout_commit": git_head(),
        "project": {"path": config["project_dir"], "module": config["module"], **pins},
        "roots": roots,
        "implementation_imports": sorted(imports),
        "authority_contract": {
            "proof_edges_layer": "G_proof",
            "proof_edge_authority": "OBSERVED",
            "derived_closure_authoritative": False,
            "implementation_imports_semantic": False,
            "semantic_reconciler_may_only_propose": True,
            **config["claim_boundary"],
        },
    }
    report["report_digest_sha256"] = sha256_json(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = extract(args.config)
    except ExtractionError as exc:
        print(f"CMDG Lean dependency extraction FAILED [{exc.code}]: {exc.message}")
        return 1
    encoded = json.dumps(report, sort_keys=True, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    print("CMDG Lean dependency extraction PASS")
    print("scope: checked proof/implementation evidence only; no G_semantic authority or GRAPH_CERTIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
