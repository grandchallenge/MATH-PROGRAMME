#!/usr/bin/env python3
"""Source-lock exact finite counterexample-search findings, fail closed."""
import json,hashlib
from pathlib import Path
r=Path(__file__).resolve().parent
hashfile=lambda f:hashlib.sha256((r/f).read_bytes()).hexdigest()
star=[json.loads(x[7:]) for x in (r/'star_level3.log').read_text().splitlines() if x.startswith('RESULT')]
assert len(star)==420 and all(x['status']=='STAR_HOST_NO_WITNESS' for x in star)
assert sum(x['count'] for x in star)==155737
counts=[]
for f in ('five_fast_e12.log','five_fast_0_4.log','five_fast_4_41.log'):
 lines=(r/f).read_text().splitlines()
 assert lines[-1].startswith('NO_REFUTATION_IN_CLASS')
 counts.append({'file':f,'last_line':lines[-1],'sha256':hashfile(f)})
assert "'simple_candidates': 3208" in counts[0]['last_line']
assert "'simple_candidates': 461" in counts[1]['last_line']
assert "'simple_candidates': 5581" in counts[2]['last_line']
assert "'arrow_red_deleted': 11" in counts[0]['last_line']
assert "'arrow_red_deleted': 275" in counts[2]['last_line']
rigid12=json.loads((r/'RIGID_12EDGE_CERTIFICATE.json').read_text())
rigid13=json.loads((r/'RIGID_13EDGE_CERTIFICATE.json').read_text())
assert rigid12['strict_boundary_12_edge_candidates']==9194
assert rigid12['remaining_joint_counterexamples']==0
assert rigid13['counts']['generated']==31667
assert rigid13['counts']['passes_A']==1
assert rigid13['joint_counterexamples']==0
E={'record_type':'ERDOS561_JOINT_RESIDUAL_BOUNDED_FALSIFICATION/1',
   'status':'NO_COUNTEREXAMPLE_FOUND_IN_DECLARED_RESTRICTED_CLASSES',
   'unrestricted_joint_residual_hypothesis_proved_by_search':False,
   'star_host_parameter_pairs':420,'star_host_parameter_host_comparisons':155737,
   'star_host_max_budget_J':18,'star_host_edge_colourings':'ALL red arm counts for each tested star host',
   'star_host_log_sha256':hashfile('star_level3.log'),
   'genuine_nonstar_benchmark':{'red':[2,1,1],'blue':[4,1,1,1,1],
      'joint_candidate_min_edges':14,'tested_candidate_edgecounts':[12,13],
      'host_generation':'all nontrivial disjoint-star partitions of given edge count with >=5 components and a >=4 star, followed by one valid vertex identification; NOT every possible graph',
      'simple_candidate_graph_tests':9250,
      'first_residual_arrowed_candidates':286,
      'both_residuals_arrowed_candidates':0,
      'all_residual_tests_exact':True},
   'nonstar_source_logs':counts,
   'complete_rigid_exact_3x4_proved_cases':[
      {'red':[3,2,1],'blue':[3,1,1,1],'joint_minimum':13,
       'candidate_edgecount':12,'complete_attachment_cases':9194,
       'independent_replay_checkers':2,
       'certificate_sha256':hashfile('RIGID_12EDGE_CERTIFICATE.json'),
       'full_proof':'RIGID_12EDGE_FINITE_THEOREM.md'},
      {'red':[3,1,1],'blue':[4,3,1,1],'joint_minimum':14,
       'candidate_edgecount':13,'complete_attachment_cases':31667,
       'independent_replay_checkers':2,
       'certificate_sha256':hashfile('RIGID_13EDGE_CERTIFICATE.json'),
       'full_proof':'RIGID_13EDGE_FINITE_THEOREM.md'}],
   'interpretation':'These are finite negative searches; the benchmark is separately proved by the unbounded peeling theorem. They are not a global solution.'}
(r/'FALSIFICATION_SEARCH_EVIDENCE.json').write_text(json.dumps(E,indent=2)+'\n')
print('FALSIFICATION_EVIDENCE_SOURCE_LOCK_PASS',E['star_host_parameter_host_comparisons'],E['genuine_nonstar_benchmark']['simple_candidate_graph_tests'])
