#!/usr/bin/env python3
"""Validate that executable CI policy scripts are reachable from a governed workflow or shard registry."""
from __future__ import annotations
import ast, json, re, sys
from pathlib import Path
import yaml
from gcl import validate_tooling
from validate_administrative_maintenance_control import DEFAULT_CONTROL as ADMINISTRATIVE_MAINTENANCE_CONTROL, DEFAULT_SCHEMA as ADMINISTRATIVE_MAINTENANCE_SCHEMA, validate as validate_administrative_maintenance_control
from validate_gcl_truth_spine import DEFAULT_MATRIX as GCL_TRUTH_SPINE_MATRIX, DEFAULT_MATRIX_SCHEMA as GCL_TRUTH_SPINE_MATRIX_SCHEMA, DEFAULT_REGISTRY as GCL_TRUTH_SPINE_REGISTRY, DEFAULT_REGISTRY_SCHEMA as GCL_TRUTH_SPINE_REGISTRY_SCHEMA, validate as validate_gcl_truth_spine
from validate_negative_knowledge import validate as validate_negative_knowledge
from validate_portfolio import validate as validate_portfolio
from validate_synthesis import validate as validate_synthesis
ROOT=Path(__file__).resolve().parents[1]
PYTHON_COMMAND=re.compile(r"(?:^|[;&|({\s])python(?:3)?\s+([A-Za-z0-9_./-]+\.py)(?=\s|$)")
MAIN_GUARD=re.compile(r"if\s+__name__\s*==\s*['\"]__main__['\"]\s*:")
TOOLING_CONTROL_PATHS=('ci/gcl.py','governance/gcl_tooling_command_contract.json','schemas/gcl_tooling_command_contract.schema.json','schemas/gcl_local_identity_manifest.schema.json')
NEGATIVE_KNOWLEDGE_CONTROL_PATHS=('ci/validate_negative_knowledge.py','negative_knowledge/pilot_registry.json','schemas/negative_knowledge_registry.schema.json')
PORTFOLIO_CONTROL_PATHS=('ci/render_portfolio.py','ci/validate_portfolio.py','portfolio/pilot_registry.json','schemas/gcl_portfolio_registry.schema.json','docs/governance/GCL_PORTFOLIO_VIEW.md')
SYNTHESIS_CONTROL_PATHS=('ci/render_synthesis.py','ci/validate_synthesis.py','synthesis/pilot_registry.json','schemas/gcl_synthesis_registry.schema.json','docs/governance/GCL_SYNTHESIS_REPORT.md','docs/governance/GCL_SYNTHESIS_REVIEW_PACKET.md')
def registry_python_roots(path:Path)->set[str]:
    roots=set()
    if not path.is_file():return roots
    data=json.loads(path.read_text(encoding='utf-8'))
    for commands in data.get('shards',{}).values():
        if not isinstance(commands,list):continue
        for command in commands:
            if isinstance(command,list) and len(command)>=2 and command[0] in {'python','python3'} and str(command[1]).endswith('.py'):roots.add(str(command[1]))
    return roots
def workflow_python_roots(root:Path=ROOT)->set[str]:
    roots=set()
    for path in sorted((root/'.github/workflows').glob('*.y*ml')):
        workflow=yaml.load(path.read_text(encoding='utf-8'),Loader=yaml.BaseLoader)
        if not isinstance(workflow,dict):continue
        for job in workflow.get('jobs',{}).values():
            for step in job.get('steps',[]):
                run=str(step.get('run',''));roots.update(m.group(1) for m in PYTHON_COMMAND.finditer(run))
    campaign=root/'ci/campaign_replay_registry.json'
    if campaign.is_file():
        data=json.loads(campaign.read_text(encoding='utf-8'))
        for entry in data.get('entries',[]):
            cmd=entry.get('command',[])
            if len(cmd)>=2 and cmd[0] in {'python','python3'}:roots.add(str(cmd[1]))
    roots.update(registry_python_roots(root/'governance/policy_shard_registry.json'))
    return roots
def ci_modules(root:Path=ROOT)->dict[str,str]:return {p.stem:p.relative_to(root).as_posix() for p in sorted((root/'ci').glob('*.py')) if p.is_file()}
def imported_ci_paths(path:Path,modules:dict[str,str])->set[str]:
    try:tree=ast.parse(path.read_text(encoding='utf-8'),filename=str(path))
    except SyntaxError:return set()
    out=set()
    for node in ast.walk(tree):
        names=[]
        if isinstance(node,ast.Import):names.extend(a.name.split('.',1)[0] for a in node.names)
        elif isinstance(node,ast.ImportFrom) and node.module:names.append(node.module.split('.',1)[0])
        for name in names:
            if name in modules:out.add(modules[name])
    return out
def executable_ci_scripts(root:Path=ROOT)->set[str]:
    out=set()
    for p in sorted((root/'ci').glob('*.py')):
        text=p.read_text(encoding='utf-8')
        if text.startswith('#!') or MAIN_GUARD.search(text):out.add(p.relative_to(root).as_posix())
    return out
def reachable_ci_scripts(root:Path=ROOT)->tuple[set[str],list[str]]:
    errors=[];modules=ci_modules(root);roots=workflow_python_roots(root);graph={rel:imported_ci_paths(root/rel,modules) for rel in modules.values()};reachable=set();stack=[p for p in roots if p.startswith('ci/')]
    for p in sorted(roots):
        if p.endswith('.py') and not (root/p).is_file():errors.append(f'workflow or governed registry invokes missing Python script {p}')
    while stack:
        cur=stack.pop()
        if cur in reachable:continue
        reachable.add(cur);stack.extend(sorted(graph.get(cur,set())-reachable))
    return reachable,errors
def conditional(root:Path,label:str,paths:tuple[str,...],validator)->list[str]:
    present=[x for x in paths if (root/x).is_file()]
    if not present:return []
    missing=[x for x in paths if x not in present]
    if missing:return [f'{label}: incomplete control surface; missing '+', '.join(missing)]
    return [f'{label}: {e}' for e in validator()]
def policy_reachability_errors(root:Path=ROOT)->list[str]:
    reachable,errors=reachable_ci_scripts(root)
    for p in sorted(executable_ci_scripts(root)-reachable):errors.append(f'CI policy reachability: executable script is unreachable from workflows or governed shard registry: {p}')
    for e in validate_administrative_maintenance_control(ADMINISTRATIVE_MAINTENANCE_CONTROL,ADMINISTRATIVE_MAINTENANCE_SCHEMA):errors.append(f'administrative maintenance control: {e}')
    for e in validate_gcl_truth_spine(GCL_TRUTH_SPINE_REGISTRY,GCL_TRUTH_SPINE_REGISTRY_SCHEMA,GCL_TRUTH_SPINE_MATRIX,GCL_TRUTH_SPINE_MATRIX_SCHEMA):errors.append(f'GCL truth spine: {e}')
    present=[x for x in TOOLING_CONTROL_PATHS if (root/x).is_file()]
    if present:
        missing=[x for x in TOOLING_CONTROL_PATHS if x not in present]
        if missing:errors.append('GCL work-package tooling: incomplete tooling control surface; missing '+', '.join(missing))
        else:errors.extend(f'GCL work-package tooling: {e}' for e in validate_tooling(root))
    errors.extend(conditional(root,'GCL negative knowledge',NEGATIVE_KNOWLEDGE_CONTROL_PATHS,lambda:validate_negative_knowledge(root/'negative_knowledge/pilot_registry.json',root/'schemas/negative_knowledge_registry.schema.json')))
    errors.extend(conditional(root,'GCL portfolio',PORTFOLIO_CONTROL_PATHS,lambda:validate_portfolio(root/'portfolio/pilot_registry.json',root/'schemas/gcl_portfolio_registry.schema.json',root/'docs/governance/GCL_PORTFOLIO_VIEW.md')))
    errors.extend(conditional(root,'GCL synthesis',SYNTHESIS_CONTROL_PATHS,lambda:validate_synthesis(root/'synthesis/pilot_registry.json',root/'schemas/gcl_synthesis_registry.schema.json',root/'docs/governance/GCL_SYNTHESIS_REPORT.md',root/'docs/governance/GCL_SYNTHESIS_REVIEW_PACKET.md')))
    return errors
def main()->int:
    errors=policy_reachability_errors()
    if errors:
        for e in errors:print(e,file=sys.stderr)
        print(f'CI policy reachability failed with {len(errors)} error(s)',file=sys.stderr);return 1
    print('every executable CI policy script is reachable from a governed workflow or shard registry');return 0
if __name__=='__main__':raise SystemExit(main())
