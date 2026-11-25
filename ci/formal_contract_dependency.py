#!/usr/bin/env python3
"""Fail-open dependency proof for *existing* non-formal workflow contracts.

Only the precisely enumerated workflow contract scripts can avoid re-running
Lean. All changes to the material router, workflows, toolchain, registry and
unrecognised scripts retain the original full-fanout behavior.
"""
from __future__ import annotations
import ast
import json
import subprocess
from pathlib import Path

# No wildcards: a newly named validator cannot silently inherit an exception.
CONTRACT_FILES = frozenset({
    'ci/validate_workflow_coverage.py',
    'ci/validate_workflow_coverage_v2.py',
    'ci/test_workflow_coverage.py',
    'ci/test_workflow_coverage_v2.py',
    'ci/validate_workflow_semantics.py',
    'ci/test_workflow_semantics.py',
})
CONTRACT_REQUIRED_COMMANDS = frozenset({
    'ci/validate_workflow_coverage_v2.py', 'ci/test_workflow_coverage_v2.py',
    'ci/test_workflow_coverage.py', 'ci/validate_workflow_semantics.py',
    'ci/test_workflow_semantics.py',
})
# One dynamic subprocess replay is pinned by an exact Git blob in the PC-WP04
# manifest. Its validator runs in the other explicit PC-WP04 material lane.
PC_MANIFEST = 'fixtures/formal/PC-WP04/certificate_manifest.json'
KNOWN_IMPORTLIB_SOURCES = {
    'tests/test_cmdg_condensed_cm4_p3.py': ('MODULE_PATH', 'ci/validate_cmdg_condensed_cm4_p3.py'),
    'tests/test_cmdg_condensed_cm4_p2_e.py': ('PATH', 'ci/validate_cmdg_condensed_cm4_p2_e.py'),
}
KNOWN_PYTHON_SPAWN = frozenset({
    'ci/formal_validation.py', 'ci/validate_pc_wp04_fixture.py',
    'ci/test_pc_wp04_fixture.py', 'ci/formal_contract_dependency.py',
    # Exact source-scoped Lean core replay, reached only by the governed
    # erdos-pv-0560-core formal lane. Unknown future subprocesses still fail.
    'ci/erdos_pv_0560_formal_replay.py',
    # Exact Init-only #561 source/type/axiom replay, governed by its own lane.
    'ci/erdos_pv_0561_formal_replay.py',
    # Exact CRT source/type/axiom replay in its registered Mathlib lane.
    'ci/erdos_pv_0027_formal_replay.py',
    'governance/erdos_proof_verification/evidence/0027/check_weighted_lean.py',
    'governance/erdos_proof_verification/evidence/0027/check_independence_lean.py',
    'governance/erdos_proof_verification/evidence/0027/check_period_lean.py',
    'governance/erdos_proof_verification/evidence/0027/check_sequence_lean.py',
})


class DependencyUnproved(ValueError):
    pass


def _check_policy_contracts(root: Path) -> None:
    manifest = json.loads((root / 'governance/policy_shard_registry.json').read_text())
    commands = {tuple(x) for xs in manifest['shards'].values() for x in xs}
    for path in CONTRACT_REQUIRED_COMMANDS:
        if ('python3', path) not in commands:
            raise DependencyUnproved('governed contract not executable: ' + path)


def _dynamic_pc_target(root: Path) -> str:
    data = json.loads((root / PC_MANIFEST).read_text())
    replay = data['fixture_replay']
    relative = replay['validator']
    target = (root / relative).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file() or target.suffix != '.py':
        raise DependencyUnproved('PC-WP04 dynamic validator path unverified')
    # Pinned manifest is itself a material PC-WP04 path. Even when it remains
    # unchanged, verify its locked validator source and byte identity.
    check = subprocess.run(['git', 'hash-object', str(target)], cwd=root,
                           capture_output=True, text=True, timeout=8)
    if check.returncode or check.stdout.strip() != replay['validator_git_blob']:
        raise DependencyUnproved('PC-WP04 replay source blob mismatch')
    return target.relative_to(root.resolve()).as_posix()


def audited_code_paths(root: Path, registry: dict) -> set[str]:
    # Resolve imports by module path and calling script directory. Do not
    # treat every Python file named `validate.py` in unrelated campaigns as a
    # possible runtime import of every other `validate` module.
    def local_modules(module: str, caller: str) -> set[str]:
        parts = module.split('.')
        if not parts or any(not item.isidentifier() for item in parts):
            raise DependencyUnproved('unresolvable module name in ' + caller)
        package_path = root.joinpath(*parts)
        candidates = [package_path.with_suffix('.py'), package_path / '__init__.py']
        if len(parts) == 1:
            candidates.append(root / Path(caller).parent / (module + '.py'))
            candidates.append(root / 'ci' / (module + '.py'))
            candidates.append(root / 'tests' / (module + '.py'))
        out = set()
        for path in candidates:
            if path.is_file():
                resolved = path.resolve()
                if not resolved.is_relative_to(root.resolve()):
                    raise DependencyUnproved('local module resolves outside repo')
                out.add(resolved.relative_to(root.resolve()).as_posix())
        return out
    initial = {'ci/formal_validation.py', _dynamic_pc_target(root)}
    for lane in registry['lanes']:
        for cmd in lane['validator_commands']:
            if len(cmd) > 1 and cmd[0] in ('python', 'python3'):
                if cmd[1].endswith('.py'):
                    initial.add(cmd[1])
                elif len(cmd) == 4 and cmd[1:3] == ['-m', 'unittest'] and cmd[3].startswith('tests.test_'):
                    initial.add(cmd[3].replace('.', '/') + '.py')
                else:
                    raise DependencyUnproved('unknown Python validator invocation')
            elif cmd:
                raise DependencyUnproved('unrecognised non-Python lane validator')
    stack = list(initial)
    visited = set()
    while stack:
        relative = stack.pop()
        if relative in visited:
            continue
        visited.add(relative)
        source = root / relative
        if not source.is_file() or source.suffix != '.py':
            raise DependencyUnproved('missing Python dependency: ' + relative)
        tree = ast.parse(source.read_text(encoding='utf-8'), filename=relative)
        # Two CMDG unit tests load one explicitly pinned local validator using
        # importlib.util. Allow only their exact variable and path expressions;
        # a new dynamic importer must restore full formal replay.
        importlib_nodes = [node for node in ast.walk(tree)
                           if isinstance(node, ast.Import) and any(alias.name.startswith('importlib') for alias in node.names)]
        if importlib_nodes:
            allowed = KNOWN_IMPORTLIB_SOURCES.get(relative)
            if not allowed:
                raise DependencyUnproved('unreviewed importlib loader: ' + relative)
            var, expected = allowed
            bindings = [node.value for node in ast.walk(tree)
                        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == var for t in node.targets)]
            exact_binding = (len(bindings) == 1 and isinstance(bindings[0], ast.BinOp)
                             and isinstance(bindings[0].op, ast.Div)
                             and isinstance(bindings[0].left, ast.Name)
                             and bindings[0].left.id == 'ROOT'
                             and isinstance(bindings[0].right, ast.Constant)
                             and bindings[0].right.value == expected)
            loaders = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                       and isinstance(node.func, ast.Attribute) and node.func.attr == 'spec_from_file_location']
            exact_loader = (len(loaders) == 1 and len(loaders[0].args) == 2
                            and isinstance(loaders[0].args[1], ast.Name)
                            and loaders[0].args[1].id == var)
            if not exact_binding or not exact_loader:
                raise DependencyUnproved('dynamic validator source identity not proved: ' + relative)
        for node in ast.walk(tree):
            modules = []
            if isinstance(node, ast.Import):
                modules.extend(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    raise DependencyUnproved('unreviewed relative module import: ' + relative)
                if node.module:
                    modules.append(node.module)
                    modules.extend(node.module + '.' + a.name for a in node.names)
            for module in modules:
                parts = module.split('.')
                if any(part in {Path(name).stem for name in CONTRACT_FILES} for part in parts):
                    raise DependencyUnproved('formal validator imports contract code: ' + relative + ':' + module)
                stack.extend(local_modules(module, relative))
                if module.split('.')[0] == 'runpy' or (module.split('.')[0] == 'importlib' and relative not in KNOWN_IMPORTLIB_SOURCES):
                    raise DependencyUnproved('dynamic module loader in ' + relative)
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Name) and func.id in ('__import__', 'eval', 'exec'):
                    raise DependencyUnproved('dynamic Python execution in ' + relative)
                if isinstance(func, ast.Attribute) and func.attr in ('import_module', 'run_module', 'run_path'):
                    raise DependencyUnproved('runtime module loading in ' + relative)
                if (isinstance(func, ast.Attribute) and func.attr in ('run', 'check_call', 'check_output', 'Popen')
                        and isinstance(func.value, ast.Name) and func.value.id == 'subprocess'
                        and relative not in KNOWN_PYTHON_SPAWN):
                    raise DependencyUnproved('unreviewed subprocess dependency: ' + relative)
    return visited


def contract_only_safe(root: Path, registry: dict) -> tuple[bool, str]:
    """Do not exempt contract-file changes while runtime independence is unproved.

    An authorized formal subprocess can construct a guarded script name from
    fragments without importing it. Static import tracing is not a safety
    proof. Keep the existing routing API but require all formal lanes.
    """
    return False, "CONTRACT_NONINTERFERENCE_UNPROVED__FULL_FORMAL_REPLAY"
