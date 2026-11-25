// Independent exhaustive edge-partition and deletion DP; no augmented-factor solver.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;
int pc(unsigned x) { return __builtin_popcount(x); }
int first(unsigned x) { return __builtin_ctz(x); }
int main() {
  uint64_t graphs=0, cases=0, cut_cases=0, violated=0, multi=0;
  int largest=0;
  for (int n=3;n<=6;++n) {
    vector<pair<int,int>> edges;
    for(int i=0;i<n;i++) for(int j=i+1;j<n;j++) edges.emplace_back(i,j);
    unsigned size=1u<<edges.size(), all=(1u<<n)-1;
    vector<array<int,6>> degrees(size);
    vector<array<unsigned,6>> adj(size);
    vector<int> delta(size);
    graphs+=size;
    for(unsigned g=1;g<size;g++) {
      unsigned bit=g&-g, rest=g^bit;
      auto [x,y]=edges[first(bit)];
      degrees[g]=degrees[rest]; adj[g]=adj[rest];
      ++degrees[g][x]; ++degrees[g][y];
      adj[g][x]|=1u<<y; adj[g][y]|=1u<<x;
      delta[g]=max({delta[rest],degrees[g][x],degrees[g][y]});
    }
    for(int D=2;D<n;D++) for(int a=1;a<D;a++) {
      int b=D-a;
      vector<int> defect(size,0);
      for(unsigned g=0;g<size;g++) {
        if(delta[g]>D) continue;
        bool split=false;
        for(unsigned r=g;;r=(r-1)&g) {
          if(delta[r]<=a && delta[g^r]<=b) { split=true; break; }
          if(!r) break;
        }
        if(!split) {
          defect[g]=100;
          for(unsigned x=g;x;x&=x-1) defect[g]=min(defect[g],1+defect[g^(x&-x)]);
        }
        unsigned sat=0;
        for(int x=0;x<n;x++) if(degrees[g][x]==D) sat|=1u<<x;
        int p=pc(sat), bound=p/(D+1);
        assert(defect[g]<=bound);
        ++cases; largest=max(largest,defect[g]);
        if(defect[g]) ++violated;
        if(defect[g]>=2) ++multi;
        // Enumerate all disjoint cut pairs for all n<=5, and every n=6
        // graph with enough saturated vertices to have a positive bound.
        if(n==6 && !bound) continue;
        int h=0;
        for(unsigned S=all;;S=(S-1)&all) {
          unsigned complement=all^S;
          for(unsigned T=complement;;T=(T-1)&complement) {
            int A=0;
            for(int x=0;x<n;x++) {
              if(S>>x&1) A+=min(a,degrees[g][x]);
              if(T>>x&1) A+=min(b,degrees[g][x])-pc(adj[g][x]&S);
            }
            assert(A>=0);
            unsigned U=all^(S|T), rem=U;
            int q=0, big=0, small=0, boundary=0;
            while(rem) {
              unsigned C=0, fringe=rem&-rem;
              while(fringe) {
                int x=first(fringe); fringe&=fringe-1;
                if(C>>x&1) continue;
                C|=1u<<x;
                fringe|=(adj[g][x]&U&~C);
              }
              rem&=~C;
              if(C&~sat) continue;
              int parity=a*pc(C), cb=0;
              for(unsigned x=C;x;x&=x-1) {
                auto v=first(x);
                parity+=pc(adj[g][v]&T);
                cb+=a*pc(adj[g][v]&S)+b*pc(adj[g][v]&T);
              }
              if(!(parity&1)) continue;
              ++q;
              if(pc(C)>D) { ++big; boundary+=cb; }
              else ++small;
            }
            assert(q-A<=big && big<=bound && A>=small);
            if(q-A==big) assert(boundary==0);
            h=max(h,q-A);
            if(!T) break;
          }
          if(!S) break;
        }
        assert(defect[g]<=h && h<=bound);
        assert((h==0)==split);
        ++cut_cases;
      }
    }
  }
  cout << "{\n  \"scope\": \"all labelled simple graphs on 3..6 vertices, positive caps summing to D<=n-1 with delta<=D; cut replay all n<=5 and n=6 with positive core bound\",\n";
  cout << "  \"graphs\": "<<graphs<<",\n  \"graph_cap_cases\": "<<cases<<",\n";
  cout << "  \"cut_replay_cases\": "<<cut_cases<<",\n  \"positive_exact_defect_cases\": "<<violated<<",\n";
  cout << "  \"multiple_exact_defect_cases\": "<<multi<<",\n  \"largest_exact_defect\": "<<largest<<",\n  \"status\": \"PASS\"\n}\n";
}
