#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
int pc(unsigned x){return __builtin_popcount(x);} int low(unsigned x){return __builtin_ctz(x);}
int main(){
 uint64_t graph_count=0, cases=0, cuts=0, positive=0, multiple=0, dom_cases=0, budget_cases=0, proper_dom=0, chromatic_controls=0, paired_support_cases=0, paired_budget_checks=0;
 for(int n=3;n<=6;n++){
  vector<pair<int,int>> edges; for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)edges.emplace_back(i,j);
  unsigned lim=1u<<edges.size(), all=(1u<<n)-1; graph_count+=lim;
  vector<array<unsigned,6>> adj(lim); vector<array<int,6>> deg(lim); vector<int> delta(lim);
  for(unsigned G=1;G<lim;G++){unsigned bit=G&-G,rest=G^bit;auto [i,j]=edges[low(bit)];adj[G]=adj[rest];deg[G]=deg[rest];adj[G][i]|=1u<<j;adj[G][j]|=1u<<i;++deg[G][i];++deg[G][j];delta[G]=max({delta[rest],deg[G][i],deg[G][j]});}
  for(int D=2;D<n;D++)for(int a=1;a<D;a++){int b=D-a;
   for(unsigned G=0;G<lim;G++){
    if(delta[G]>D)continue;
    unsigned X=0;for(int i=0;i<n;i++)if(deg[G][i]==D)X|=1u<<i;
    // Full n<=5; for n=6 focus on graphs capable of positive deficit.
    if(n==6 && pc(X)<D+1)continue;
    ++cases;
    int h=0;
    for(unsigned S=all;;S=(S-1)&all){unsigned rem=all^S;
     for(unsigned T=rem;;T=(T-1)&rem){unsigned U=rem^T;int A=0,q=0;
      for(int i=0;i<n;i++){if(S>>i&1)A+=min(a,deg[G][i]);if(T>>i&1)A+=min(b,deg[G][i])-pc(adj[G][i]&S);}
      unsigned left=U; while(left){unsigned C=0,F=left&-left;while(F){int i=low(F);F&=F-1;if(C>>i&1)continue;C|=1u<<i;F|=adj[G][i]&U&~C;}left&=~C;if(C&~X)continue;int parity=a*pc(C);for(unsigned v=C;v;v&=v-1)parity+=pc(adj[G][low(v)]&T);q+=parity&1;}
      assert(A>=0);h=max(h,q-A);++cuts;if(!T)break;
     }if(!S)break;
    }
    assert(h<=pc(X)/(D+1));if(h)++positive;if(h>1)++multiple;
    // independent color-mask enumeration; store every attainable pair of defect masks.
    vector<pair<unsigned,unsigned>> options;
    for(unsigned R=G;;R=(R-1)&G){unsigned B=G^R,DR=0,DB=0;bool valid=true;
     for(int i=0;i<n;i++){int er=deg[R][i]-a,eb=deg[B][i]-b;if(er>0||eb>0){if(!(X>>i&1)||er>1||eb>1){valid=false;break;}if(er>0)DR|=1u<<i;if(eb>0)DB|=1u<<i;}}
     if(valid)options.emplace_back(DR,DB);
     if(!R)break;
    }
    vector<unsigned> dom;
    for(unsigned A=X;;A=(A-1)&X){unsigned covered=A;for(unsigned x=A;x;x&=x-1)covered|=adj[G][low(x)];if((covered&X)==X){
      dom.push_back(A);++dom_cases;if(A!=X)++proper_dom;int m=pc(A);bool attainable[7][7]{};
      for(auto [r,s]:options)if(!((r|s)&~A))attainable[pc(r)][pc(s)]=true;
      for(int r=0;r<=m;r++)for(int s=0;s<=m;s++){
       bool yes=false;for(int i=0;i<=r;i++)for(int j=0;j<=s;j++)yes|=attainable[i][j];
       assert(yes==(r+s>=h));++budget_cases;
      }
      if(h==0)++chromatic_controls;
     }if(!A)break;
    }
    // Separate prescribed supports for the two colors. Zero-deficit cases
    // have already exhibited a fully capped coloring; all support pairs
    // then work. Test all ordered pairs for every positive deficit.
    if(h) for(unsigned A:dom)for(unsigned B:dom){
      ++paired_support_cases; bool attainable[7][7]{};
      for(auto [r,s]:options)if(!(r&~A)&&!(s&~B))attainable[pc(r)][pc(s)]=true;
      for(int r=0;r<=pc(A);r++)for(int s=0;s<=pc(B);s++){
        bool yes=false;for(int i=0;i<=r;i++)for(int j=0;j<=s;j++)yes|=attainable[i][j];
        assert(yes==(r+s>=h));++paired_budget_checks;
      }
    }
   }
  }
 }
 cout<<"{\n  \"labelled_graphs\": "<<graph_count<<",\n  \"eligible_graph_cap_cases\": "<<cases<<",\n  \"cut_pairs\": "<<cuts<<",\n  \"positive_deficit_cases\": "<<positive<<",\n  \"multiple_deficit_cases\": "<<multiple<<",\n  \"dominating_set_cases\": "<<dom_cases<<",\n  \"proper_dominating_sets\": "<<proper_dom<<",\n  \"budget_feasibility_checks\": "<<budget_cases<<",\n  \"zero_deficit_domination_controls\": "<<chromatic_controls<<",\n  \"paired_support_cases\": "<<paired_support_cases<<",\n  \"paired_budget_checks\": "<<paired_budget_checks<<",\n  \"status\": \"PASS\"\n}\n";
}
