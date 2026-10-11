#!/usr/bin/env python3
"""Queue Class cutover: targeted semantic, view, and fail-closed fixtures."""
import unittest
from gcl_queue_class_cutover import classify, prepare, VIEW_FILTERS, PROJECT_ID, QUEUE_FIELD_ID, AVAILABLE_VIEW_ID

DIRECT = "gcl-pickup:direct-editorial"

def make_item(n,repo,title,labels,observed):
    return {
      "id":f"PVTI_{n}",
      "content":{
        "number":n,"title":title,"state":"OPEN",
        "repository":{"nameWithOwner":repo},
        "labels":{"totalCount":len(labels),"nodes":[{"name":x} for x in labels]}
      },
      "fieldValueByName":{"name":observed} if observed else None
    }

def project():
    return {
      "id": PROJECT_ID,
      "fields":{"nodes":[{"id":QUEUE_FIELD_ID,"name":"Queue Class",
        "options":[{"id":"optE","name":"Editorial"},{"id":"optM","name":"Mathematics"}]}]},
      "views":{"nodes":[{"id":AVAILABLE_VIEW_ID,"name":"AVAILABLE",
                            "filter":'is:open "GCL State":AVAILABLE'}]}
    }

class Contract(unittest.TestCase):
    def test_cross_class_same_pickup(self):
        src=make_item(1273,"grandchallenge/MATH-PROGRAMME",
          "[GCL-ERDOS] ERDOS-CATALOGUE-0004-S01 — prime gaps",
          ["gcl-job",DIRECT,"gcl-role:source-audit"],"Editorial")
        ed=make_item(2556,"grandchallenge/MATH-PROGRAMME",
          "EC-ED02 — Erdős #7 explanation",
          ["gcl-job",DIRECT,"gcl-role:constructive"],None)
        self.assertEqual(classify(src),("Mathematics","direct_editorial"))
        self.assertEqual(classify(ed),("Editorial","direct_editorial"))
        corrections,totals=prepare(project(),[src,ed])
        self.assertEqual(totals["classes_expected"],{"Mathematics":1,"Editorial":1})
        self.assertEqual({x["issue"] for x in corrections},{1273,2556})
        self.assertEqual({x["class"] for x in corrections},{"Editorial","Mathematics"})

    def test_mathsolve_pickup_unchanged(self):
        proof=make_item(999,"grandchallenge/MATHSOLVE","Proof",
                        ["gcl-job","gcl-state:available"],"Mathematics")
        self.assertEqual(classify(proof),("Mathematics","reservation_controlled"))
        self.assertEqual(prepare(project(),[proof])[0],[])

    def test_unknown_route_is_blocked(self):
        x=make_item(17,"grandchallenge/UNKNOWN","Editorial",["gcl-job",DIRECT],"Editorial")
        with self.assertRaisesRegex(ValueError,"unrecognized"):
            classify(x)
        x=make_item(1276,"grandchallenge/MATH-PROGRAMME","ERDOS-CATALOGUE-0007-S01",
                    ["gcl-job",DIRECT],"Editorial")
        with self.assertRaisesRegex(ValueError,"ambiguous"):
            classify(x)
        x=make_item(1279,"grandchallenge/MATH-PROGRAMME",
                    "[GCL-ERDOS] ERDOS-CATALOGUE-0010-S01",
                    ["gcl-job",DIRECT,"gcl-role:source-audit"],"Mathematics")
        x["content"]["labels"]["totalCount"]=999
        with self.assertRaisesRegex(ValueError,"truncated"):
            classify(x)

    def test_bad_project_identity_and_available_view(self):
        p=project();p["fields"]["nodes"][0]["id"]="WRONG"
        with self.assertRaisesRegex(ValueError,"Queue Class identity"):
            prepare(p,[])
        p=project();p["views"]["nodes"][0]["filter"]="is:open"
        with self.assertRaisesRegex(ValueError,"AVAILABLE filter drift"):
            prepare(p,[])

    def test_view_filter_contract(self):
        self.assertEqual(VIEW_FILTERS["EDITORIAL"],'is:open "Queue Class":Editorial')
        self.assertEqual(VIEW_FILTERS["MATHEMATICS"],'is:open "Queue Class":Mathematics')

if __name__=="__main__":
    unittest.main()
