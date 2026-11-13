#!/usr/bin/env python3
"""Finite independent regression for the source-locked Erdős #1 binary-block lemma.

Not a proof of the global Erdos #1 disproof, nor a Lean kernel replay.
The universal transfer argument is separately documented.
"""
from __future__ import annotations
import hashlib, itertools, json

def fixture(weights:tuple[int,...],k:int)->dict:
 assert k>=1 and weights and all(isinstance(a,int) and a>0 for a in weights)
 q=1<<k
 vectors=itertools.product(range(-q+1,q),repeat=len(weights))
 bad=None
 for c in vectors:
  if any(c) and sum(x*y for x,y in zip(weights,c))==0:
   bad=c
   break
 blocks=[a*(1<<j) for a in weights for j in range(k)]
 sums={}
 collision=None
 for mask in range(1<<len(blocks)):
  value=sum(a for pos,a in enumerate(blocks) if mask>>pos&1)
  if value in sums and collision is None:
   collision={"first_subset_mask":sums[value],"second_subset_mask":mask,"sum":value}
  else:
   sums.setdefault(value,mask)
 return {"weights":list(weights),"k":k,"q":q,"relation_free":bad is None,
         "bad_relation":list(bad) if bad else None,"block_weights":blocks,
         "subset_count":1<<len(blocks),"distinct_subset_sum_count":len(sums),
         "all_subset_sums_distinct":collision is None,"collision":collision,
         "positive_and_bounded":min(blocks)>0 and
           max(blocks)<=max(weights)*(1<<(k-1))}
def evidence()->dict:
 results=[fixture((1,5),2),fixture((1,9),3),fixture((1,3),2)]
 assert [x["relation_free"] for x in results]==[True,True,False]
 assert [x["all_subset_sums_distinct"] for x in results]==[True,True,False]
 assert [x["distinct_subset_sum_count"] for x in results]==[16,64,13]
 assert all(x["positive_and_bounded"] for x in results)
 assert results[2]["collision"] is not None
 data={"record_type":"ERDOS_PV_0001_BINARY_BLOCK_FIXTURE/1",
       "assignment_id":"ERDOS-PV-0001-B",
       "result":"PASS_EXACT_FINITE_FIXTURES_NOT_UNIVERSAL_THEOREM",
       "fixtures":results,"limitations":{
         "formal_replay_executed":False,"full_erdos1_counterexample_verified":False,
         "mathcert_certified":False}}
 b=json.dumps(data,sort_keys=True,separators=(",",":")).encode()
 data["canonical_payload_sha256"]=hashlib.sha256(b).hexdigest()
 return data
if __name__=="__main__":
 print(json.dumps(evidence(),sort_keys=True))
